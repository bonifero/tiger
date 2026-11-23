"""An offline, keyboard-friendly dynamic programming classroom.

The canvas table keeps a small, visible set of items even for wide problems.
Only answers already accepted by the lesson are available in the review drawer.
"""
from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
from pathlib import Path

from model import Problem, parse_number, fmt_number
from lesson import Lesson
from formats import load, save
from presets import PRESETS

TITLE = 'Рюкзак · Практикум'
BG = '#f3f5f9'
INK = '#17243b'
NAVY = '#12233c'
BLUE = '#315fea'
MUTED = '#68768b'
LINE = '#e2e8f1'
WHITE = '#ffffff'
PALE = '#edf2ff'
GREEN = '#17795a'
GREEN_BG = '#eaf6ef'
RED = '#bf3946'
RED_BG = '#fff0f1'


class NavButton(tk.Label):
    """Flat navigation that retains the same colors on Windows and Cocoa."""

    def __init__(self, parent, *, command, **kwargs):
        super().__init__(parent, takefocus=1, highlightthickness=1,
                         highlightbackground=NAVY, highlightcolor='#7f9df4',
                         disabledforeground='#61748f', **kwargs)
        self.command = command
        self.bind('<Button-1>', lambda e: self.invoke())
        self.bind('<Return>', lambda e: self.invoke())
        self.bind('<space>', lambda e: self.invoke())

    def invoke(self):
        if self.cget('state') != 'disabled':
            return self.command()
        return None


class DataGrid(tk.Frame):
    """Virtual table with a single native edit control and TSV paste.

    Values are strings; read-only and unavailable cells remain part of the model.
    Row and column coordinates in ``invalid`` use the table's own coordinates.
    """

    def __init__(self, parent, columns, rows, *, editable=None, widths=None,
                 on_change=None, font_family='Segoe UI', font_size=11, height=300):
        super().__init__(parent, bg=WHITE, highlightthickness=1,
                         highlightbackground=LINE)
        self.columns = tuple(columns)
        self.rows = [[str(v) if v is not None else '—' for v in row] for row in rows]
        self.editable = set(editable or ())
        self.widths = [round(w * font_size / 11) for w in (widths or [110] * len(columns))]
        self.on_change = on_change
        self.freeze_first = not any(c == 0 for _, c in self.editable)
        self.family = font_family
        self.font_size = font_size
        self.row_height = max(38, round(font_size * 3.4))
        self.header_height = self.row_height + 6
        self.invalid = set()
        self.selected = None
        self.entry = None
        self.entry_window = None
        self.positions = [0]
        for width in self.widths:
            self.positions.append(self.positions[-1] + width)
        self.canvas = tk.Canvas(self, bg=WHITE, highlightthickness=0,
                                bd=0, height=height, takefocus=1)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.horizontal = ttk.Scrollbar(self, orient='horizontal', command=self._xview)
        self.horizontal.grid(row=1, column=0, sticky='ew')
        self.vertical = ttk.Scrollbar(self, orient='vertical', command=self._yview)
        self.vertical.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(xscrollcommand=self._set_horizontal,
                              yscrollcommand=self._set_vertical,
                              scrollregion=(0, 0, self.positions[-1],
                                            self.header_height + len(self.rows) * self.row_height))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.canvas.bind('<Configure>', self._redraw)
        self.canvas.bind('<Button-1>', self._click)
        self.canvas.bind('<Double-1>', self._click)
        self.canvas.bind('<Return>', self._edit_selected)
        self.canvas.bind('<F2>', self._edit_selected)
        self.canvas.bind('<Key>', self._type)
        self.canvas.bind('<Tab>', lambda e: self._next_editable(1))
        self.canvas.bind('<Shift-Tab>', lambda e: self._next_editable(-1))
        self.canvas.bind('<ISO_Left_Tab>', lambda e: self._next_editable(-1))
        for key, dr, dc in [('Up', -1, 0), ('Down', 1, 0), ('Left', 0, -1), ('Right', 0, 1)]:
            self.canvas.bind('<' + key + '>', lambda e, r=dr, c=dc: self._move(r, c))
        self.canvas.bind('<<Paste>>', self._paste)
        self.canvas.bind('<MouseWheel>', self._wheel)
        self.canvas.bind('<Shift-MouseWheel>', lambda e: self._wheel(e, horizontal=True))
        self.canvas.bind('<Button-4>', lambda e: self._scroll_units(-3))
        self.canvas.bind('<Button-5>', lambda e: self._scroll_units(3))
        self.after_idle(self._redraw)

    def _set_horizontal(self, first, last):
        self.horizontal.set(first, last)
        if float(first) <= 0 and float(last) >= 1:
            self.horizontal.grid_remove()
        else:
            self.horizontal.grid()

    def _set_vertical(self, first, last):
        self.vertical.set(first, last)
        if float(first) <= 0 and float(last) >= 1:
            self.vertical.grid_remove()
        else:
            self.vertical.grid()

    def _xview(self, *args):
        self.commit()
        self.canvas.xview(*args)
        self._redraw()

    def _yview(self, *args):
        self.commit()
        self.canvas.yview(*args)
        self._redraw()

    def _scroll_units(self, amount, horizontal=False):
        self.commit()
        if horizontal:
            self.canvas.xview_scroll(amount, 'units')
        else:
            self.canvas.yview_scroll(amount, 'units')
        self._redraw()
        return 'break'

    def _wheel(self, event, horizontal=False):
        # Windows sends multiples of 120; Cocoa sends small integral deltas.
        amount = -int(event.delta / 120) if abs(event.delta) >= 120 else -int(event.delta)
        return self._scroll_units(amount or (-1 if event.delta > 0 else 1), horizontal)

    def _redraw(self, _event=None):
        self.canvas.delete('cells')
        if not self.rows and not self.columns:
            return
        top = self.canvas.canvasy(0)
        left = self.canvas.canvasx(0)
        bottom = top + self.canvas.winfo_height()
        right = left + self.canvas.winfo_width()
        first = max(0, int((top - self.header_height) // self.row_height))
        last = min(len(self.rows), int((bottom - self.header_height) // self.row_height) + 2)
        visible_columns = [c for c in range(len(self.columns))
                           if self.positions[c + 1] >= left and self.positions[c] <= right]
        for r in range(first, last):
            y0 = self.header_height + r * self.row_height
            y1 = y0 + self.row_height
            for c in visible_columns:
                x0, x1 = self.positions[c:c + 2]
                enabled = (r, c) in self.editable
                value = self.rows[r][c]
                fill = WHITE if r % 2 == 0 else '#fbfcfe'
                color = INK
                if value == '—':
                    fill, color = '#f5f7fa', '#bdc5d1'
                elif c == 0 and not enabled:
                    fill, color = '#f7f9fc', MUTED
                if (r, c) in self.invalid:
                    fill = RED_BG
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill,
                                             outline=LINE, tags='cells')
                label = value if value else ('·' if enabled else '')
                self.canvas.create_text(x0 + 15, (y0 + y1) / 2, text=label,
                                        anchor='w', fill=color if value else '#bec7d6',
                                        width=max(20, x1 - x0 - 26),
                                        font=(self.family, self.font_size), tags='cells')
        if self.selected is not None:
            r, c = self.selected
            x0, x1 = self.positions[c:c + 2]
            y0 = self.header_height + r * self.row_height
            self.canvas.create_rectangle(x0 + 1, y0 + 1, x1 - 1,
                                         y0 + self.row_height - 1, outline=BLUE,
                                         width=2, tags='cells')
        # Frozen headers keep a large table legible while scrolling.
        if self.freeze_first and left > 0 and self.columns:
            for r in range(first, last):
                y0 = self.header_height + r * self.row_height
                self.canvas.create_rectangle(left, y0, left + self.widths[0],
                    y0 + self.row_height, fill='#f7f9fc', outline=LINE, tags='cells')
                self.canvas.create_text(left + 15, y0 + self.row_height / 2,
                    text=self.rows[r][0], anchor='w', fill=MUTED,
                    font=(self.family, self.font_size), width=self.widths[0] - 26, tags='cells')
        header_columns = visible_columns[:]
        if self.freeze_first:
            header_columns = [c for c in header_columns if c != 0] + [0]
        for c in header_columns:
            x0, x1 = self.positions[c:c + 2]
            if c == 0 and self.freeze_first:
                x0, x1 = left, left + self.widths[0]
            self.canvas.create_rectangle(x0, top, x1, top + self.header_height,
                                         fill='#f4f6fa', outline=LINE, tags='cells')
            self.canvas.create_text(x0 + 15, top + self.header_height / 2,
                                    text=self.columns[c], anchor='w', fill=MUTED,
                                    font=(self.family, self.font_size - 1, 'bold'), tags='cells')
        if self.entry_window:
            self.canvas.tag_raise(self.entry_window)

    def _cell_at(self, event):
        from bisect import bisect_right
        if event.y < self.header_height:
            return None
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        row = int((y - self.header_height) // self.row_height)
        col = bisect_right(self.positions, x) - 1
        if self.freeze_first and event.x < self.widths[0]:
            col = 0
        if 0 <= row < len(self.rows) and 0 <= col < len(self.columns):
            return row, col
        return None

    def _click(self, event):
        self.commit()
        cell = self._cell_at(event)
        if cell is not None:
            self.selected = cell
            self.canvas.focus_set()
            self._redraw()
            if cell in self.editable:
                self._start_edit()
        return 'break'

    def _edit_selected(self, _event=None):
        if self.selected is None and self.editable:
            self.selected = min(self.editable)
        self._start_edit()
        return 'break'

    def _type(self, event):
        if event.char and event.char.isprintable() and not (event.state & 0x0c):
            if self.selected in self.editable:
                self._start_edit(replacement=event.char)
                return 'break'
        return None

    def _start_edit(self, replacement=None):
        if self.selected not in self.editable:
            return
        self.commit()
        r, c = self.selected
        self._ensure_visible(r, c)
        x0, x1 = self.positions[c:c + 2]
        y0 = self.header_height + r * self.row_height
        self.entry = tk.Entry(self.canvas, font=(self.family, self.font_size),
                              bg=WHITE, fg=INK, insertbackground=BLUE,
                              relief='flat', bd=0, highlightthickness=2,
                              highlightbackground=BLUE, highlightcolor=BLUE)
        self.entry.insert(0, self.rows[r][c] if replacement is None else replacement)
        self.entry_window = self.canvas.create_window(x0 + 1, y0 + 1, anchor='nw',
                                                      window=self.entry,
                                                      width=x1 - x0 - 2,
                                                      height=self.row_height - 2)
        self.entry.focus_set()
        if replacement is None:
            self.entry.selection_range(0, 'end')
        self.entry.bind('<Return>', lambda e: self._move(1, 0, editing=True))
        self.entry.bind('<Tab>', lambda e: self._next_editable(1, editing=True))
        self.entry.bind('<Shift-Tab>', lambda e: self._next_editable(-1, editing=True))
        self.entry.bind('<ISO_Left_Tab>', lambda e: self._next_editable(-1, editing=True))
        self.entry.bind('<Escape>', self._cancel_edit)
        self.entry.bind('<<Paste>>', self._paste)
        self.entry.bind('<FocusOut>', self._focus_out)

    def _focus_out(self, event):
        # Windows may deliver queued focus events after an editor was replaced,
        # or after focus has already returned to the current editor.
        if (self.winfo_exists() and event.widget is self.entry
                and self.focus_get() is not self.entry):
            self.commit()

    def _cancel_edit(self, _event=None):
        self._remove_entry()
        self.canvas.focus_set()
        return 'break'

    def _remove_entry(self):
        entry, window = self.entry, self.entry_window
        self.entry = self.entry_window = None
        if window:
            self.canvas.delete(window)
        if entry:
            entry.destroy()

    def commit(self):
        if self.entry is not None and self.selected is not None:
            value = self.entry.get().strip()
            r, c = self.selected
            changed = self.rows[r][c] != value
            self.rows[r][c] = value
            self.invalid.discard((r, c))
            self._remove_entry()
            self._redraw()
            if changed and self.on_change:
                self.on_change()

    def _ensure_visible(self, r, c):
        total_h = self.header_height + len(self.rows) * self.row_height
        total_w = self.positions[-1]
        x0, x1 = self.positions[c:c + 2]
        y0 = self.header_height + r * self.row_height
        top, left = self.canvas.canvasy(0), self.canvas.canvasx(0)
        view_h, view_w = self.canvas.winfo_height(), self.canvas.winfo_width()
        if y0 < top + self.header_height:
            self.canvas.yview_moveto((y0 - self.header_height) / max(total_h, 1))
        elif y0 + self.row_height > top + view_h:
            self.canvas.yview_moveto((y0 + self.row_height - view_h) / max(total_h, 1))
        frozen_width = self.widths[0] if self.freeze_first else 0
        if x0 < left + frozen_width:
            self.canvas.xview_moveto((x0 - frozen_width) / max(total_w, 1))
        elif x1 > left + view_w:
            self.canvas.xview_moveto((x1 - view_w) / max(total_w, 1))
        self._redraw()

    def _move(self, dr, dc, editing=False):
        self.commit()
        if self.selected is None:
            self.selected = min(self.editable) if self.editable else (0, 0)
        else:
            r, c = self.selected
            self.selected = (max(0, min(len(self.rows) - 1, r + dr)),
                             max(0, min(len(self.columns) - 1, c + dc)))
        if self.rows and self.columns:
            self._ensure_visible(*self.selected)
            if editing:
                self._start_edit()
        return 'break'

    def _next_editable(self, direction, editing=False):
        self.commit()
        cells = sorted(self.editable)
        if not cells:
            return None
        if self.selected in self.editable:
            index = (cells.index(self.selected) + direction) % len(cells)
        else:
            index = 0 if direction > 0 else len(cells) - 1
        self.selected = cells[index]
        self._ensure_visible(*self.selected)
        if editing:
            self._start_edit()
        return 'break'

    def _paste(self, _event=None):
        try:
            raw = self.clipboard_get()
        except tk.TclError:
            return 'break'
        if self.selected not in self.editable:
            return 'break'
        # A single value keeps normal native selection/insertion behavior.
        if '\t' not in raw and '\n' not in raw.rstrip('\r\n') and self.entry is not None:
            if self.entry.selection_present():
                self.entry.delete('sel.first', 'sel.last')
            self.entry.insert('insert', raw.strip())
            return 'break'
        self.commit()
        row0, col0 = self.selected
        changes = []
        for dr, line in enumerate(raw.rstrip('\r\n').splitlines()):
            for dc, value in enumerate(line.split('\t')):
                cell = row0 + dr, col0 + dc
                if cell in self.editable:
                    changes.append((cell, value.strip()))
        for (r, c), value in changes:
            self.rows[r][c] = value
            self.invalid.discard((r, c))
        self._redraw()
        if changes and self.on_change:
            self.on_change()
        return 'break'

    def get_rows(self):
        self.commit()
        return [row[:] for row in self.rows]

    def set_value(self, row, col, value):
        """Programmatic input, also used by UI acceptance tests."""
        if (row, col) not in self.editable:
            raise ValueError('Эта ячейка недоступна для ввода.')
        self.commit()
        self.rows[row][col] = str(value)
        self.invalid.discard((row, col))
        self._redraw()
        if self.on_change:
            self.on_change()

    def mark_invalid(self, cells):
        self.commit()
        self.invalid = {cell for cell in cells if cell in self.editable}
        if self.invalid:
            self.selected = min(self.invalid)
            self._ensure_visible(*self.selected)
            self.canvas.focus_set()
        self._redraw()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITLE)
        width = max(1100, min(1380, self.winfo_screenwidth() - 60))
        height = max(680, min(920, self.winfo_screenheight() - 100))
        self.geometry(f'{width}x{height}')
        self.minsize(1100, 680)
        self.compact = height < 820
        self._resize_job = None
        self.configure(bg=BG)
        families = set(tkfont.families(self))
        self.family = next((f for f in ('Segoe UI', 'SF Pro Text', 'Helvetica Neue', 'Arial')
                            if f in families), 'TkDefaultFont')
        self.font_size = 11
        self.table_font_size = 11
        self.zoom = tk.StringVar(value='100%')
        self.lesson = None
        self.problem = None
        self.final_plan = None
        self.accepted = []
        self.dirty = False
        self.screen = 'editor'
        self.answer_grid = None
        self.editor_grid = None
        self._pending_editor = None
        self._style()
        self._build_shell()
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.bind('<Control-s>', lambda e: self.save_file())
        self.bind('<Command-s>', lambda e: self.save_file())
        self.set_problem(PRESETS[0])
        self.bind('<Configure>', self._on_resize, add='+')

    def _on_resize(self, event):
        if event.widget is not self or (event.height < 820) == self.compact:
            return
        if self._resize_job:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(120, self._apply_compact_layout)

    def _apply_compact_layout(self):
        if self._resize_job:
            self.after_cancel(self._resize_job)
        self._resize_job = None
        compact = self.winfo_height() < 820
        if compact != self.compact:
            self.compact = compact
            self.header.configure(height=64 if compact else 76)
            self.content.configure(pady=16 if compact else 24)
            self.footer.configure(pady=10 if compact else 14)
            self.rescale()

    def _style(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('.', font=(self.family, self.font_size), background=BG,
                        foreground=INK, bordercolor=LINE)
        style.configure('TButton', padding=(15, 10), background=WHITE,
                        foreground=INK, relief='flat', borderwidth=1, focusthickness=2,
                        focuscolor=BLUE)
        style.map('TButton', background=[('active', '#eaf0fa'), ('disabled', BG)],
                  foreground=[('disabled', '#a8b2c2')])
        style.configure('Primary.TButton', background=BLUE, foreground=WHITE,
                        borderwidth=0, font=(self.family, self.font_size, 'bold'), padding=(20, 12))
        style.map('Primary.TButton', background=[('active', '#244dd2'), ('disabled', '#a6b8ee')],
                  foreground=[('disabled', WHITE)])
        style.configure('Small.TButton', padding=(11, 7), font=(self.family, self.font_size - 1))
        style.configure('TEntry', fieldbackground=WHITE, padding=(9, 8), borderwidth=1)
        style.configure('TCombobox', fieldbackground=WHITE, padding=(9, 8), arrowsize=14)
        style.map('TCombobox', fieldbackground=[('readonly', WHITE)], foreground=[('readonly', INK)])
        style.configure('TSpinbox', fieldbackground=WHITE, padding=(7, 8), arrowsize=12)
        for orient, sticky in [('Horizontal', 'we'), ('Vertical', 'ns')]:
            style.layout(f'{orient}.TScrollbar', [(f'{orient}.Scrollbar.trough',
                {'sticky': 'nsew', 'children': [(f'{orient}.Scrollbar.thumb',
                    {'expand': '1', 'sticky': 'nsew'})]})])
            style.configure(f'{orient}.TScrollbar', background='#cbd6e8', troughcolor='#f4f6fa',
                            borderwidth=0, arrowsize=10, width=10)

    def _label(self, parent, text='', *, size=None, bold=False, color=INK,
               bg=WHITE, **kwargs):
        return tk.Label(parent, text=text, font=(self.family, size or self.font_size,
                        'bold' if bold else 'normal'), fg=color, bg=bg, **kwargs)

    def _card(self, parent, *, padding=20, bg=WHITE):
        if self.compact:
            padding = min(padding, 15)
        outer = tk.Frame(parent, bg=bg, highlightbackground=LINE, highlightthickness=1)
        inner = tk.Frame(outer, bg=bg, padx=padding, pady=padding)
        inner.pack(fill='both', expand=True)
        return outer, inner

    def _build_shell(self):
        self.header = tk.Frame(self, bg=NAVY, height=64 if self.compact else 76)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)
        brand = tk.Frame(self.header, bg=NAVY)
        brand.pack(side='left', padx=28)
        self._label(brand, 'РЮКЗАК', size=18, bold=True, color=WHITE, bg=NAVY).pack(anchor='w')
        self._label(brand, 'П Р А К Т И К У М  /  0 3', size=8, color='#a9b8cf', bg=NAVY).pack(anchor='w', pady=(3, 0))
        nav = tk.Frame(self.header, bg=NAVY)
        nav.pack(side='left', padx=42)
        self.nav_buttons = []
        for label, callback in [('01  Условие', self.return_to_editor),
                                ('02  Решение', self.navigate_to_lesson),
                                ('03  Итог', self.show_result)]:
            button = NavButton(nav, text=label, font=(self.family, 11), relief='flat',
                               bd=0, bg=NAVY, fg='#a9b8cf', padx=16, pady=11,
                               cursor='hand2', command=callback)
            button.pack(side='left', padx=3)
            self.nav_buttons.append(button)
        zoom_box = tk.Frame(self.header, bg=NAVY)
        zoom_box.pack(side='right', padx=28)
        self._label(zoom_box, 'Таблица', size=9, color='#a9b8cf', bg=NAVY).pack(side='left', padx=8)
        zoom = ttk.Combobox(zoom_box, textvariable=self.zoom, values=['80%', '100%', '120%', '140%'],
                            state='readonly', width=5)
        zoom.pack(side='left')
        zoom.bind('<<ComboboxSelected>>', self.rescale)
        self.footer = tk.Frame(self, bg=WHITE, highlightbackground=LINE, highlightthickness=1,
                               padx=28, pady=10 if self.compact else 14)
        self.footer.pack(side='bottom', fill='x')
        self.content = tk.Frame(self, bg=BG, padx=28, pady=16 if self.compact else 24)
        self.content.pack(fill='both', expand=True)
        self.message_var = tk.StringVar(value='')
        self.hint_var = tk.StringVar(value='')

    def _clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()
        for child in self.footer.winfo_children():
            child.destroy()
        self.answer_grid = None
        self.editor_grid = None
        self.hint_var.set('')
        for i, button in enumerate(self.nav_buttons):
            selected = i == {'editor': 0, 'lesson': 1, 'result': 2}[self.screen]
            button.configure(bg='#263e60' if selected else NAVY,
                             fg=WHITE if selected else '#a9b8cf')
        self.nav_buttons[1].configure(state='normal' if self.lesson else 'disabled')
        self.nav_buttons[2].configure(state='normal' if self.lesson and self.lesson.phase == 'done' else 'disabled')

    def _heading(self, eyebrow, title, subtitle):
        self._label(self.content, eyebrow.upper(), size=9, bold=True, color=BLUE,
                    bg=BG, anchor='w').pack(fill='x')
        row = tk.Frame(self.content, bg=BG)
        row.pack(fill='x', pady=(8, 0))
        self._label(row, title, size=21 if self.compact else 27, bold=True, bg=BG, anchor='w').pack(side='left')
        self._label(self.content, subtitle, size=10 if self.compact else self.font_size,
                    color=MUTED, bg=BG, anchor='w',
                    wraplength=1120, justify='left').pack(fill='x', pady=(6, 12 if self.compact else 22))
        return row

    def _footer_message(self):
        area = tk.Frame(self.footer, bg=WHITE)
        area.pack(side='left', fill='both', expand=True)
        self.message_label = self._label(area, text='', color=MUTED, anchor='w',
                                         wraplength=340, justify='left')
        self.message_label.configure(textvariable=self.message_var)
        self.message_label.pack(anchor='w')
        return area

    def _message(self, text, error=False):
        self.message_var.set(text)
        if hasattr(self, 'message_label') and self.message_label.winfo_exists():
            self.message_label.configure(fg=RED if error else MUTED)

    def _confirm_replace(self):
        if self.screen == 'editor':
            self.editor_grid.commit()
        if self.lesson and self.lesson.phase != 'done':
            return messagebox.askyesno('Начать заново?',
                                       'Принятые шаги и введённые ответы будут сброшены. Продолжить?', parent=self)
        if self.dirty:
            return messagebox.askyesno('Заменить условие?',
                                       'В условии есть несохранённые изменения. Продолжить?', parent=self)
        return True

    def set_problem(self, problem):
        self.problem = problem
        self.lesson = None
        self.final_plan = None
        self.accepted = []
        self.dirty = False
        self.name_var = tk.StringVar(value=problem.name)
        self.capacity_var = tk.StringVar(value=str(problem.capacity))
        self.count_var = tk.StringVar(value=str(len(problem.weights)))
        self.limit_var = tk.StringVar(value=str(max(len(v) - 1 for v in problem.values)))
        # Observe values, including native paste/cut and spinbox actions.
        for variable in (self.name_var, self.capacity_var, self.count_var, self.limit_var):
            variable.trace_add('write', self.mark_dirty)
        self.description = problem.description
        self._pending_editor = None
        self.screen = 'editor'
        self.show_editor()
        self._message('Укажите веса и полную ценность каждого количества. F(0) всегда равно 0.')

    def mark_dirty(self, *_):
        self.dirty = True

    def show_editor(self):
        self.screen = 'editor'
        self._clear_content()
        if self.compact:
            self._label(self.content, 'Условие задачи', size=20, bold=True, bg=BG,
                        anchor='w').pack(fill='x', pady=(0, 12))
        else:
            self._heading('Динамическое программирование', 'У каждого выбора есть ценность',
                          'Задайте ресурс, веса и ценности. Затем самостоятельно пройдите все шаги поиска оптимального плана.')
        picker = tk.Frame(self.content, bg=BG)
        picker.pack(fill='x', pady=(0, 10 if self.compact else 16))
        self.preset_var = tk.StringVar(value=self.problem.name)
        self.preset_box = ttk.Combobox(picker, values=[p.name for p in PRESETS],
                                       textvariable=self.preset_var, state='readonly', width=38)
        self.preset_box.pack(side='left')
        ttk.Button(picker, text='Выбрать пример', command=self.choose_preset).pack(side='left', padx=(8, 0))
        ttk.Button(picker, text='Открыть JSON', command=self.open_file).pack(side='right')
        ttk.Button(picker, text='Сохранить', command=self.save_file).pack(side='right', padx=8)
        layout = tk.Frame(self.content, bg=BG)
        layout.pack(fill='both', expand=True)
        layout.columnconfigure(0, weight=1)
        layout.rowconfigure(0, weight=1)
        left, inner = self._card(layout)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 18))
        inner.rowconfigure(4, weight=1)
        inner.columnconfigure(0, weight=1)
        title_row = tk.Frame(inner, bg=WHITE)
        if not self.compact:
            title_row.grid(row=0, column=0, sticky='ew')
        self._label(title_row, 'УСЛОВИЕ ЗАДАЧИ', size=9, bold=True, color=MUTED).pack(side='left')
        self._label(title_row, '01', size=11, bold=True, color=BLUE).pack(side='right')
        name = ttk.Entry(inner, textvariable=self.name_var, font=(self.family, self.font_size + 2))
        name.grid(row=1, column=0, sticky='ew', pady=(8, 10) if self.compact else (12, 16))
        dims = tk.Frame(inner, bg=WHITE)
        dims.grid(row=2, column=0, sticky='ew')
        for label, var, frm, to in [('Ёмкость B', self.capacity_var, 1, 200),
                                    ('Типов грузов', self.count_var, 1, 12),
                                    ('Лимит x', self.limit_var, 0, 200)]:
            field = tk.Frame(dims, bg=WHITE)
            field.pack(side='left', padx=(0, 14))
            self._label(field, label, size=9, color=MUTED).pack(
                side='left' if self.compact else 'top', anchor='w',
                padx=(0, 5) if self.compact else 0, pady=0 if self.compact else (0, 5))
            spin = ttk.Spinbox(field, from_=frm, to=to, textvariable=var, width=4 if self.compact else 6)
            spin.pack(side='left' if self.compact else 'top', anchor='w')
        ttk.Button(dims, text='Новая таблица', command=self.new_table,
                   style='Small.TButton').pack(side='right', anchor='s')
        table_heading = tk.Frame(inner, bg=WHITE)
        table_heading.grid(row=3, column=0, sticky='ew', pady=(10, 6) if self.compact else (20, 10))
        self._label(table_heading, 'Веса и таблица ценностей', bold=True).pack(side='left')
        ttk.Button(table_heading, text='Применить лимиты', command=self.apply_limits,
                   style='Small.TButton').pack(side='right')
        labels = self.problem.labels or tuple(f'Груз {i + 1}' for i in range(len(self.problem.weights)))
        if self._pending_editor is None:
            raw_rows = [[labels[i], str(self.problem.weights[i]), str(len(vals) - 1),
                         *[fmt_number(v) for v in vals]] for i, vals in enumerate(self.problem.values)]
        else:
            raw_rows = self._pending_editor
        self._mount_editor_grid(inner, raw_rows)
        footnote = 'Клик — ввод  ·  Tab — следующая ячейка  ·  Enter — ниже  ·  Ctrl/Cmd+V — вставить таблицу'
        self._label(inner, footnote, size=9, color=MUTED, anchor='w',
                    wraplength=760, justify='left').grid(row=5, column=0, sticky='ew', pady=(12, 0))
        side = tk.Frame(layout, bg=BG, width=270)
        side.grid(row=0, column=1, sticky='ns')
        side.grid_propagate(False)
        self._editor_side(side)
        self._footer_message()
        ttk.Button(self.footer, text='Начать практикум  →', style='Primary.TButton',
                   command=self.begin).pack(side='right')

    def _mount_editor_grid(self, parent, raw_rows):
        max_columns = max(len(row) for row in raw_rows)
        rows = [row + [None] * (max_columns - len(row)) for row in raw_rows]
        editable = {(r, c) for r, row in enumerate(raw_rows) for c in range(len(row)) if c != 3}
        self.editor_grid = DataGrid(parent, ['Название', 'Вес a', 'Лимит',
                                             *[f'F({i})' for i in range(max_columns - 3)]], rows,
                                    editable=editable, widths=[150, 80, 80] + [87] * (max_columns - 3),
                                    on_change=self.mark_dirty, font_family=self.family,
                                    font_size=self.table_font_size)
        self.editor_grid.grid(row=4, column=0, sticky='nsew')

    def _editor_side(self, parent):
        outer, card = self._card(parent, padding=18, bg=PALE)
        outer.pack(fill='x')
        self._label(card, 'СМЫСЛ ЗАДАЧИ', size=9, bold=True, color=BLUE, bg=PALE).pack(anchor='w')
        if not self.compact:
            self._label(card, 'Максимум ценности.\nОдин общий ресурс.', size=17, bold=True,
                        bg=PALE, justify='left', anchor='w').pack(fill='x', pady=(14, 10))
        self._label(card, 'Σ aⱼ · xⱼ ≤ B', size=16 if self.compact else 18, bold=True, color=BLUE, bg=PALE).pack(anchor='w', pady=(10, 8) if self.compact else (0, 12))
        self._label(card, 'x — целое количество. Оставлять часть ресурса свободной можно.',
                    size=10, color=MUTED, bg=PALE, wraplength=225, justify='left', anchor='w').pack(fill='x')
        outer2, desc = self._card(parent, padding=18)
        outer2.pack(fill='both', expand=True, pady=(16, 0))
        self._label(desc, 'ОБ ЭТОМ ПРИМЕРЕ', size=9, bold=True, color=MUTED).pack(anchor='w')
        description = self.description or 'Создайте собственную задачу: укажите число типов, ёмкость и доступные количества.'
        text = tk.Text(desc, bg=WHITE, fg=INK, relief='flat', bd=0, wrap='word',
                       font=(self.family, self.font_size), height=5, width=24,
                       highlightthickness=0, padx=0, pady=0, cursor='arrow', takefocus=0)
        text.pack(fill='both', expand=True, pady=(12, 10))
        # Long source notes remain available by mouse wheel and in a full text window.
        text.insert('1.0', description)
        text.configure(state='disabled')
        ttk.Button(desc, text='Полное описание ↗', style='Small.TButton',
                   command=self.open_description).pack(fill='x', pady=(0, 12))
        self._label(desc, 'F(x) — ценность всего набора из x единиц, а не цена одной единицы.',
                    size=10, color=BLUE, wraplength=225, justify='left', anchor='w').pack(fill='x')

    @staticmethod
    def _integer(raw, label, minimum, maximum):
        value = parse_number(str(raw).strip())
        if value.denominator != 1 or not minimum <= value <= maximum:
            raise ValueError(f'{label}: нужно целое число от {minimum} до {maximum}.')
        return int(value)

    def read_problem(self):
        rows = self.editor_grid.get_rows()
        capacity = self._integer(self.capacity_var.get(), 'Ёмкость', 1, 200)
        labels, weights, values = [], [], []
        for i, row in enumerate(rows):
            labels.append(row[0].strip() or f'Груз {i + 1}')
            weights.append(self._integer(row[1], f'Вес груза {i + 1}', 1, 10**12))
            limit = self._integer(row[2], f'Лимит груза {i + 1}', 0, 200)
            available = [row[c] for c in range(3, len(row))
                         if c == 3 or (i, c) in self.editor_grid.editable]
            if len(available) != limit + 1:
                raise ValueError('После изменения лимитов нажмите «Применить лимиты» и заполните новые ячейки.')
            values.append(tuple(parse_number(v) for v in available))
        return Problem(name=self.name_var.get().strip() or 'Новая задача', capacity=capacity,
                       weights=tuple(weights), values=tuple(values), labels=tuple(labels),
                       description=self.description)

    def apply_limits(self):
        try:
            rows = self.editor_grid.get_rows()
            new_rows = []
            for i, row in enumerate(rows):
                limit = self._integer(row[2], f'Лимит груза {i + 1}', 0, 200)
                values = [row[c] for c in range(3, len(row))
                          if c == 3 or (i, c) in self.editor_grid.editable]
                values = (values + [''] * (limit + 1))[:limit + 1]
                values[0] = '0'
                new_rows.append(row[:3] + values)
            parent = self.editor_grid.master
            self.editor_grid.destroy()
            self._mount_editor_grid(parent, new_rows)
            self.mark_dirty()
            self._message('Лимиты применены. Заполните новые значения ценностей.')
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            self._message(str(exc), error=True)

    def new_table(self):
        try:
            count = self._integer(self.count_var.get(), 'Число типов', 1, 12)
            capacity = self._integer(self.capacity_var.get(), 'Ёмкость', 1, 200)
            limit = self._integer(self.limit_var.get(), 'Лимит', 0, 200)
            candidate = Problem(name='Своя задача', capacity=capacity, weights=(1,) * count,
                                values=tuple((0,) * (limit + 1) for _ in range(count)),
                                labels=tuple(f'Груз {i + 1}' for i in range(count)))
            if not self._confirm_replace():
                return
            self.set_problem(candidate)
            self.dirty = True
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            self._message(str(exc), error=True)

    def choose_preset(self):
        index = self.preset_box.current()
        if index >= 0 and self._confirm_replace():
            self.set_problem(PRESETS[index])

    def open_file(self):
        path = filedialog.askopenfilename(parent=self, title='Открыть условие',
                                          filetypes=[('Условие рюкзака', '*.json'), ('Все файлы', '*.*')])
        if not path:
            return
        try:
            problem = load(path)
            if self._confirm_replace():
                self.set_problem(problem)
                self._message(f'Условие загружено: {Path(path).name}')
        except (ValueError, OSError, TypeError) as exc:
            messagebox.showerror('Не удалось открыть условие', str(exc), parent=self)

    def save_file(self):
        try:
            problem = self.read_problem() if self.screen == 'editor' else self.problem
            path = filedialog.asksaveasfilename(parent=self, title='Сохранить условие',
                                                defaultextension='.json',
                                                initialfile='knapsack.json',
                                                filetypes=[('Условие рюкзака', '*.json')])
            if not path:
                return
            save(path, problem)
            self.dirty = False
            self._message(f'Условие сохранено: {Path(path).name}')
        except (ValueError, TypeError, OSError, ZeroDivisionError) as exc:
            messagebox.showerror('Не удалось сохранить условие', str(exc), parent=self)

    def begin(self):
        try:
            problem = self.read_problem()
            lesson = Lesson(problem)
        except (ValueError, TypeError, ZeroDivisionError, ArithmeticError) as exc:
            self._message(str(exc), error=True)
            return False
        self.problem = problem
        self.lesson = lesson
        self.final_plan = None
        self.accepted = []
        self._pending_editor = None
        self.show_lesson()
        self._message('Заполните все доступные ячейки. Недопустимые варианты отмечены прочерком.')
        return True

    def return_to_editor(self):
        if self.screen == 'editor':
            return
        if self.lesson and self.lesson.phase != 'done' and not self._confirm_replace():
            return
        problem, dirty = self.problem, self.dirty
        self.set_problem(problem)
        self.dirty = dirty

    def _stats(self, parent):
        stats = tk.Frame(parent, bg=WHITE)
        stats.pack(side='left', padx=(20, 0))
        self.errors_label = self._label(stats, f'Ошибки  {self.lesson.errors}', size=10, color=MUTED)
        self.errors_label.pack(side='left', padx=(0, 16))
        self.hints_label = self._label(stats, f'Подсказки  {self.lesson.hints}', size=10, color=MUTED)
        self.hints_label.pack(side='left')

    def navigate_to_lesson(self):
        # Re-selecting an active tab must never discard work in progress.
        if self.screen != 'lesson':
            self.show_lesson()

    def show_lesson(self):
        if self.lesson is None:
            return
        if self.lesson.phase == 'done':
            self.show_result()
            return
        self.screen = 'lesson'
        self._clear_content()
        phase = self.lesson.phase
        restoring = phase == 'restore'
        if restoring:
            eyebrow, title = 'Все этапы пройдены', 'Соберите оптимальный план'
            subtitle = 'Заполните состояния y и количества x для итогового плана.'
        else:
            stage = self.lesson.current_stage
            name = self._item_name(stage.index)
            eyebrow = f'Этап {self.lesson.stage_index + 1} из {len(self.problem.weights)} · {name}'
            title = 'Сравните допустимые решения' if phase == 'candidates' else 'Найдите лучшие значения'
            subtitle = ('Заполните доступные ячейки таблицы значений.'
                        if phase == 'candidates' else
                        'Заполните столбцы f(y) и x* для каждого состояния.')
        title_row = self._heading(eyebrow, title, subtitle)
        chip = 'Восстановление' if restoring else ('1 / 2  Вычисления' if phase == 'candidates' else '2 / 2  Максимумы')
        self._label(title_row, chip, size=10, bold=True, color=BLUE, bg=PALE,
                    padx=13, pady=8).pack(side='right', padx=(15, 0))
        layout = tk.Frame(self.content, bg=BG)
        layout.pack(fill='both', expand=True)
        layout.columnconfigure(0, weight=1)
        layout.rowconfigure(0, weight=1)
        outer, main = self._card(layout, padding=20)
        outer.grid(row=0, column=0, sticky='nsew', padx=(0, 18))
        if restoring:
            self._build_restore(main)
        else:
            self._build_stage(main)
        side = tk.Frame(layout, bg=BG, width=270)
        side.grid(row=0, column=1, sticky='ns')
        side.pack_propagate(False)
        self._build_reference(side)
        hint = self._label(self.content, '', size=10, color=BLUE, bg=BG,
                           wraplength=1100, justify='left', anchor='w')
        hint.configure(textvariable=self.hint_var)
        hint.pack(fill='x', pady=(10, 0))
        self._footer_message()
        self._stats(self.footer)
        self.check_button = ttk.Button(self.footer,
            text='Проверить план  →' if restoring else 'Проверить таблицу  →',
            style='Primary.TButton', command=self.check_answers)
        self.check_button.pack(side='right')
        ttk.Button(self.footer, text='Подсказка', command=self.show_hint).pack(side='right', padx=(12, 10))

    def _item_name(self, index):
        return self.problem.labels[index] if self.problem.labels else f'Груз {index + 1}'

    def _build_stage(self, parent):
        stage = self.lesson.current_stage
        index = stage.index
        phase = self.lesson.phase
        top = tk.Frame(parent, bg=WHITE)
        top.pack(fill='x')
        self._label(top, f'ГРУЗ {index + 1}  /  {self._item_name(index)}', size=9,
                    bold=True, color=MUTED).pack(side='left')
        self._label(top, f'Вес: {self.problem.weights[index]}    ·    Ёмкость: {self.problem.capacity}',
                    size=10, color=MUTED).pack(side='right')
        formula = ('Fⱼ(x) + fⱼ₊₁(y + aⱼ · x)' if index < len(self.problem.weights) - 1 else 'Fⱼ(x)  ·  последний тип груза')
        self._label(parent, formula if phase == 'candidates' else 'fⱼ(y) = max по допустимым x',
                    size=18, bold=True, color=BLUE, anchor='w').pack(fill='x', pady=(18, 8))
        self._label(parent, 'y — ресурс, израсходованный до этого груза.  x — количество текущего груза.',
                    size=10, color=MUTED, anchor='w', justify='left', wraplength=750).pack(fill='x', pady=(0, 18))
        if phase == 'candidates':
            columns = ['Состояние y'] + [f'x = {x}' for x in range(len(self.problem.values[index]))]
            rows = [[str(y)] + ['' if v is not None else None for v in stage.candidates[y]] for y in stage.states]
            editable = {(r, x + 1) for r, y in enumerate(stage.states)
                        for x, value in enumerate(stage.candidates[y]) if value is not None}
            widths = [125] + [95] * (len(columns) - 1)
        else:
            columns = ['Состояние y', 'Максимум f(y)', 'Количество x*']
            rows = [[str(y), '', ''] for y in stage.states]
            editable = {(r, c) for r in range(len(rows)) for c in (1, 2)}
            widths = [150, 240, 240]
        self.answer_grid = DataGrid(parent, columns, rows, editable=editable,
                                    widths=widths, font_family=self.family,
                                    font_size=self.table_font_size, height=280)
        self.answer_grid.pack(fill='both', expand=True)
        bottom = tk.Frame(parent, bg=WHITE)
        bottom.pack(side='bottom', fill='x', pady=(12, 0), before=self.answer_grid)
        self._label(bottom, '—  выбор не помещается в оставшийся ресурс', size=9, color=MUTED).pack(side='left')
        if phase == 'summary':
            ttk.Button(bottom, text='Посмотреть вычисления', style='Small.TButton',
                       command=lambda: self.open_review(len(self.accepted) - 1)).pack(side='right')

    def _build_restore(self, parent):
        self._label(parent, 'ОБРАТНОЕ ДВИЖЕНИЕ', size=9, bold=True, color=MUTED).pack(anchor='w')
        self._label(parent, 'yⱼ₊₁ = yⱼ + aⱼ · xⱼ', size=20, bold=True, color=BLUE).pack(anchor='w', pady=(16, 10))
        self._label(parent, 'Введите ресурс y до каждого груза и его количество x. Любой оптимальный допустимый план будет принят.',
                    color=MUTED, wraplength=740, justify='left', anchor='w').pack(fill='x', pady=(0, 20))
        columns = ['Обратный ход'] + [f'Груз {i + 1}' for i in range(len(self.problem.weights))]
        rows = [['Ресурс до груза yⱼ'] + [''] * len(self.problem.weights),
                ['Количество xⱼ'] + [''] * len(self.problem.weights)]
        self.answer_grid = DataGrid(parent, columns, rows,
                                    editable={(r, c + 1) for r in (0, 1) for c in range(len(self.problem.weights))},
                                    widths=[230] + [125] * len(self.problem.weights), font_family=self.family,
                                    font_size=self.table_font_size, height=300)
        self.answer_grid.pack(fill='both', expand=True)
        ttk.Button(parent, text='Открыть все принятые максимумы', command=self.open_summary_sheet,
                   style='Small.TButton').pack(side='bottom', anchor='w', pady=(15, 0), before=self.answer_grid)

    def _build_reference(self, parent):
        outer, card = self._card(parent, padding=18)
        outer.pack(fill='x')
        self._label(card, 'ПОД РУКОЙ', size=9, bold=True, color=MUTED).pack(anchor='w')
        self._label(card, self.problem.name, size=15, bold=True, anchor='w',
                    wraplength=228, justify='left').pack(fill='x', pady=(13, 9))
        self._label(card, f'{len(self.problem.weights)} типа · ресурс {self.problem.capacity}',
                    size=10, color=MUTED).pack(anchor='w', pady=(0, 12))
        ttk.Button(card, text='Исходные данные ↗', command=self.open_source,
                   style='Small.TButton').pack(fill='x')
        outer2, review = self._card(parent, padding=18)
        outer2.pack(fill='both', expand=True, pady=(16, 0))
        self._label(review, 'ПРИНЯТЫЕ ТАБЛИЦЫ', size=9, bold=True, color=MUTED).pack(anchor='w')
        self._label(review, 'Можно опираться на уже\nвыполненные вычисления.',
                    size=10, color=MUTED, justify='left').pack(anchor='w', pady=(12, 12))
        self.review_list = tk.Listbox(review, bg=WHITE, fg=INK, bd=0, highlightthickness=0,
                                     selectbackground=PALE, selectforeground=BLUE,
                                     activestyle='none', font=(self.family, 10),
                                     height=5, width=26, exportselection=False)
        self.review_list.pack(fill='both', expand=True)
        for entry in self.accepted:
            label = 'Вычисления' if entry['phase'] == 'candidates' else 'Максимумы'
            self.review_list.insert('end', f"  Груз {entry['index'] + 1} · {label}")
        self.review_list.bind('<Double-1>', lambda e: self.open_selected_review())
        self.review_list.bind('<Return>', lambda e: self.open_selected_review())
        button = ttk.Button(review, text='Открыть таблицу', command=self.open_selected_review,
                            style='Small.TButton')
        button.pack(side='bottom', fill='x', pady=(12, 0), before=self.review_list)
        if not self.accepted:
            button.configure(state='disabled')
            self._label(review, 'Здесь появятся ваши\nпроверенные ответы.', color=MUTED,
                        size=10, justify='left').pack(side='bottom', anchor='w', pady=(10, 0), before=self.review_list)
        else:
            self.review_list.selection_set(len(self.accepted) - 1)
            self.review_list.see('end')

    def check_answers(self):
        if not self.lesson or self.lesson.phase == 'done' or self.answer_grid is None:
            return False
        rows = self.answer_grid.get_rows()
        phase = self.lesson.phase
        if phase == 'restore':
            states, plan = rows[0][1:], rows[1][1:]
            feedback = self.lesson.submit_plan(plan, states=states)
            invalid = [(1 if kind == 0 else 0, j + 1) for kind, j in feedback.invalid]
            if feedback.accepted:
                self.final_plan = self.lesson.accepted_plan
                self.show_result()
                self._message('Практикум завершён. План допустим, его оптимальность подтверждена.')
                return True
        else:
            stage = self.lesson.current_stage
            values = {y: row[1:] for y, row in zip(stage.states, rows)}
            if phase == 'candidates':
                payload = {y: [None if value is None else values[y][x]
                               for x, value in enumerate(stage.candidates[y])] for y in stage.states}
                feedback = self.lesson.submit_candidates(payload)
            else:
                payload = {y: tuple(values[y]) for y in stage.states}
                feedback = self.lesson.submit_summary(payload)
            invalid = [(stage.states.index(y), column + 1) for y, column in feedback.invalid
                       if y in stage.states]
            if feedback.accepted:
                self.accepted.append({'phase': phase, 'index': stage.index,
                                      'states': tuple(stage.states),
                                      'columns': tuple(self.answer_grid.columns),
                                      'rows': rows})
                self.show_lesson()
                self._message('Таблица принята. Продолжайте решение.')
                return True
        self.answer_grid.mark_invalid(invalid)
        self._message(feedback.message, error=True)
        self.errors_label.configure(text=f'Ошибки  {self.lesson.errors}', fg=RED)
        return False

    def show_hint(self):
        if self.lesson and self.lesson.phase != 'done':
            self.hint_var.set(self.lesson.hint())
            self.hints_label.configure(text=f'Подсказки  {self.lesson.hints}')

    def _table_window(self, title, subtitle, columns, rows, widths):
        window = tk.Toplevel(self)
        window.title(title + ' · Рюкзак')
        window.geometry('1000x650')
        window.minsize(700, 420)
        window.configure(bg=BG)
        window.transient(self)
        content = tk.Frame(window, bg=BG, padx=24, pady=24)
        content.pack(fill='both', expand=True)
        self._label(content, title, size=22, bold=True, bg=BG).pack(anchor='w')
        self._label(content, subtitle, color=MUTED, bg=BG, wraplength=920,
                    justify='left').pack(anchor='w', pady=(9, 20))
        grid = DataGrid(content, columns, rows, widths=widths,
                        font_family=self.family, font_size=self.table_font_size)
        grid.pack(fill='both', expand=True)
        ttk.Button(content, text='Закрыть', command=window.destroy).pack(anchor='e', pady=(16, 0))
        window.bind('<Escape>', lambda e: window.destroy())
        return window

    def open_description(self):
        window = tk.Toplevel(self)
        window.title('Условие и примечания · Рюкзак')
        window.geometry('760x520')
        window.minsize(520, 350)
        window.configure(bg=WHITE)
        window.transient(self)
        self._label(window, self.name_var.get(), size=19, bold=True,
                    wraplength=680, justify='left').pack(anchor='w', padx=24, pady=(24, 15))
        frame = tk.Frame(window, bg=WHITE)
        frame.pack(fill='both', expand=True, padx=24)
        text = tk.Text(frame, wrap='word', font=(self.family, self.font_size + 1),
                       bg=WHITE, fg=INK, bd=0, relief='flat', highlightthickness=0, padx=0, pady=0)
        scroll = ttk.Scrollbar(frame, command=text.yview)
        scroll.pack(side='right', fill='y')
        text.configure(yscrollcommand=scroll.set)
        text.pack(fill='both', expand=True)
        text.insert('1.0', self.description or 'Для этой задачи описание не задано.')
        text.configure(state='disabled')
        ttk.Button(window, text='Закрыть', command=window.destroy).pack(anchor='e', padx=24, pady=20)
        window.bind('<Escape>', lambda e: window.destroy())
        return window

    def open_source(self):
        p = self.problem
        length = max(len(v) for v in p.values)
        rows = [[self._item_name(i), str(p.weights[i]), str(len(vals) - 1),
                 *[fmt_number(v) for v in vals], *[None] * (length - len(vals))]
                for i, vals in enumerate(p.values)]
        return self._table_window(p.name, f'Ёмкость B = {p.capacity}. {p.description}',
            ['Груз', 'Вес a', 'Лимит', *[f'F({x})' for x in range(length)]], rows,
            [200, 85, 85] + [90] * length)

    def open_selected_review(self):
        selection = self.review_list.curselection()
        if selection:
            return self.open_review(selection[0])
        return None

    def open_review(self, index):
        if not 0 <= index < len(self.accepted):
            return None
        entry = self.accepted[index]
        label = 'Вычисления' if entry['phase'] == 'candidates' else 'Максимумы'
        return self._table_window(f"Груз {entry['index'] + 1} · {label}",
                                 'Ваши ответы, принятые при проверке.', entry['columns'],
                                 entry['rows'], [150] + [130] * (len(entry['columns']) - 1))

    def open_summary_sheet(self):
        summaries = [e for e in self.accepted if e['phase'] == 'summary']
        rows = [[f"Груз {e['index'] + 1}", *row] for e in reversed(summaries) for row in e['rows']]
        return self._table_window('Принятые максимумы',
                                 'Проверенные максимумы и количества для каждого состояния.',
                                 ['Тип груза', 'Состояние y', 'Максимум f(y)', 'Ваш выбор x*'],
                                 rows, [160, 160, 220, 220])

    def show_result(self):
        if not self.lesson or self.lesson.phase != 'done' or self.final_plan is None:
            return
        self.screen = 'result'
        self._clear_content()
        self._heading('Практикум завершён', 'Лучший план найден',
                      'Вы сравнили допустимые решения, нашли максимумы и восстановили оптимальную загрузку.')
        plan = self.final_plan
        used = sum(w * x for w, x in zip(self.problem.weights, plan))
        objective = sum(self.problem.values[i][x] for i, x in enumerate(plan))
        metrics = tk.Frame(self.content, bg=BG)
        metrics.pack(fill='x', pady=(0, 18))
        for i in range(3):
            metrics.columnconfigure(i, weight=1, uniform='metric')
        for i, (label, value, subtitle) in enumerate([
            ('МАКСИМАЛЬНАЯ ЦЕННОСТЬ', fmt_number(objective), 'Оптимальный результат'),
            ('ИСПОЛЬЗОВАНО РЕСУРСА', f'{used} / {self.problem.capacity}',
             f'Свободно: {self.problem.capacity - used}'),
            ('ВАША РАБОТА', f'{self.lesson.errors} ошибок', f'Подсказок: {self.lesson.hints}')]):
            outer, card = self._card(metrics, padding=14 if self.compact else 20, bg=PALE if i == 0 else WHITE)
            outer.grid(row=0, column=i, sticky='nsew', padx=(0 if i == 0 else 9, 0 if i == 2 else 9))
            bg = PALE if i == 0 else WHITE
            self._label(card, label, size=9, bold=True, color=BLUE if i == 0 else MUTED,
                        bg=bg).pack(anchor='w')
            self._label(card, value, size=(26 if self.compact else 30) if i < 2 else 24, bold=True,
                        color=BLUE if i == 0 else INK, bg=bg).pack(anchor='w', pady=(8, 4) if self.compact else (14, 8))
            self._label(card, subtitle, size=10, color=MUTED, bg=bg).pack(anchor='w')
        outer, body = self._card(self.content, padding=22)
        outer.pack(fill='both', expand=True)
        self._label(body, 'ВАШ ОПТИМАЛЬНЫЙ ПЛАН', size=9, bold=True, color=MUTED).pack(anchor='w')
        rows = [[self._item_name(i), str(self.lesson.accepted_states[i]), str(x),
                 str(self.problem.weights[i] * x), fmt_number(self.problem.values[i][x])]
                for i, x in enumerate(plan)]
        grid = DataGrid(body, ['Груз', 'Ресурс до yⱼ', 'Количество xⱼ', 'Расход', 'Ценность'], rows,
                        widths=[280, 150, 170, 160, 180], font_family=self.family,
                        font_size=self.table_font_size, height=220)
        grid.pack(fill='both', expand=True, pady=(16, 18))
        bar = tk.Canvas(body, height=10, bg='#e8edf5', bd=0, highlightthickness=0)
        bar.pack(side='bottom', fill='x', before=grid)
        colors = [BLUE, '#6a87ed', '#92a8f1', '#b5c5f7']
        def draw_bar(event):
            bar.delete('all')
            x0 = 0
            for i, count in enumerate(plan):
                width = event.width * self.problem.weights[i] * count / self.problem.capacity
                bar.create_rectangle(x0, 0, x0 + width, 10, fill=colors[i % len(colors)], outline='')
                x0 += width
        bar.bind('<Configure>', draw_bar)
        self._label(body, 'Суммарный расход не превышает ёмкость. Свободный ресурс допустим.',
                    size=9, color=MUTED).pack(side='bottom', anchor='w', pady=(10, 0), before=bar)
        self._footer_message()
        ttk.Button(self.footer, text='Сохранить отчёт  ↓', command=self.export_report,
                   style='Primary.TButton').pack(side='right')
        ttk.Button(self.footer, text='К условию', command=self.return_to_editor).pack(side='right', padx=10)
        ttk.Button(self.footer, text='Принятые таблицы', command=self.open_summary_sheet).pack(side='right')

    def report_text(self):
        if not self.lesson or self.lesson.phase != 'done' or self.final_plan is None:
            raise ValueError('Отчёт доступен после завершения практикума.')
        p = self.problem
        used = sum(a * x for a, x in zip(p.weights, self.final_plan))
        objective = sum(p.values[i][x] for i, x in enumerate(self.final_plan))
        lines = ['ЛАБОРАТОРНАЯ РАБОТА 3 · ЗАДАЧА О ЗАГРУЗКЕ РЮКЗАКА', '',
                 p.name, p.description, '', 'Условие', f'Ёмкость B = {p.capacity}',
                 'Максимизировать Σ Fⱼ(xⱼ), Σ aⱼ·xⱼ ≤ B; xⱼ — целые неотрицательные.']
        for i, vals in enumerate(p.values):
            lines.append(f'{self._item_name(i)}: вес {p.weights[i]}, 0 ≤ x ≤ {len(vals) - 1}; '
                         f'F(0…{len(vals) - 1}) = ' + ', '.join(fmt_number(v) for v in vals))
        lines.extend(['', 'Принятые шаги динамического программирования'])
        for entry in self.accepted:
            label = 'вычисления' if entry['phase'] == 'candidates' else 'максимумы'
            lines.extend(['', f"Груз {entry['index'] + 1} · {label}", '\t'.join(entry['columns'])])
            lines.extend('\t'.join(row) for row in entry['rows'])
        lines.extend(['', 'Оптимальный план'])
        lines.extend(f'{self._item_name(i)}: y={self.lesson.accepted_states[i]}, x={x}'
                     for i, x in enumerate(self.final_plan))
        lines.extend([f'Максимальная ценность: {fmt_number(objective)}',
                      f'Расход ресурса: {used} из {p.capacity}',
                      f'Свободный ресурс: {p.capacity - used}',
                      f'Ошибки: {self.lesson.errors}', f'Подсказки: {self.lesson.hints}', ''])
        return '\n'.join(lines)

    def export_report(self):
        path = filedialog.asksaveasfilename(parent=self, title='Сохранить учебный отчёт',
                                            initialfile='knapsack-report.txt', defaultextension='.txt',
                                            filetypes=[('Текстовый отчёт', '*.txt')])
        if path:
            try:
                Path(path).write_text(self.report_text(), encoding='utf-8')
                self._message(f'Отчёт сохранён: {Path(path).name}')
            except OSError as exc:
                messagebox.showerror('Не удалось сохранить отчёт', str(exc), parent=self)

    def rescale(self, _event=None):
        factor = int(self.zoom.get().rstrip('%')) / 100
        self.table_font_size = max(9, round(11 * factor))
        pending = None
        selected = None
        invalid = set()
        if self.screen == 'editor':
            self._pending_editor = self.editor_grid.get_rows()
            # Remove padding, which represents unavailable counts of a type.
            self._pending_editor = [[row[c] for c in range(len(row))
                                     if c < 4 or (r, c) in self.editor_grid.editable]
                                    for r, row in enumerate(self._pending_editor)]
        elif self.screen == 'lesson' and self.answer_grid is not None:
            pending = self.answer_grid.get_rows()
            selected = self.answer_grid.selected
            invalid = self.answer_grid.invalid.copy()
        error = hasattr(self, 'message_label') and self.message_label.cget('fg') == RED
        message = self.message_var.get()
        hint = self.hint_var.get()
        self._style()
        if self.screen == 'editor':
            self.show_editor()
        elif self.screen == 'lesson':
            self.show_lesson()
            if pending is not None:
                self.answer_grid.rows = pending
                self.answer_grid.selected = selected
                self.answer_grid.invalid = invalid
                self.answer_grid._redraw()
        else:
            self.show_result()
        self._message(message, error=error)
        self.hint_var.set(hint)

    def destroy(self):
        if self._resize_job:
            self.after_cancel(self._resize_job)
            self._resize_job = None
        super().destroy()

    def close(self):
        if self.screen == 'editor':
            self.editor_grid.commit()
        if self.dirty or (self.lesson and self.lesson.phase != 'done'):
            if not messagebox.askyesno('Закрыть практикум?',
                                       'Несохранённое условие и текущий ход решения будут потеряны.', parent=self):
                return
        self.destroy()


def create_window():
    return App()


def main():
    app = create_window()
    if '--smoke-test' in sys.argv:
        app.after(150, app.destroy)
    app.mainloop()


if __name__ == '__main__':
    main()
