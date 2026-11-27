"""Игры · Практикум. Offline Windows desktop application (Python/Tk)."""
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from solver import number
from lesson import Lesson, PHASE_TITLES
from variant_files import Game, read_variant, save_variant, load_variants, variants_directory, append_variant

BG = '#f3f5f9'
INK = '#17243b'
MUTED = '#66758d'
NAVY = '#12233c'
BLUE = '#315fea'
GREEN = '#087f69'
RED = '#b33c41'
LINE = '#dce3ee'
FONT = 'Segoe UI'

NAV_ITEMS = ['01   Условие', '02   Нижняя/верхняя цена', '03   Седловая точка',
             '04   Стратегии игры', '05   Цена игры', '06   Вероятности', '07   Результат']


def label(parent, text='', size=11, color=INK, bold=False, bg='white', **kw):
    return tk.Label(parent, text=text, font=(FONT, size, 'bold' if bold else 'normal'),
                     fg=color, bg=bg, **kw)


def fmt_row(values):
    return '(' + ', '.join(str(v) for v in values) + ')'


class ScrollArea(tk.Frame):
    def __init__(self, parent, bg='white'):
        super().__init__(parent, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.canvas.create_window(0, 0, anchor='nw', window=self.inner)
        self.v = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.h = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v.set, xscrollcommand=self.h.set)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.v.grid(row=0, column=1, sticky='ns')
        self.h.grid(row=1, column=0, sticky='ew')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.inner.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))


class App:
    def __init__(self, root):
        self.root = root
        self.lesson = None
        self.feedback = ''
        self.feedback_ok = True
        self.variants_dir = variants_directory()
        self.variants = {}
        startup_error = ''
        if self.variants_dir.exists():
            try:
                self.variants = load_variants(self.variants_dir)
            except ValueError as error:
                startup_error = str(error)
        root.title('Игры · Практикум')
        root.geometry('1280x850')
        root.minsize(1050, 720)
        root.configure(bg=BG)
        style = ttk.Style(root)
        style.theme_use('clam')
        style.configure('.', font=(FONT, 11))
        style.configure('TButton', padding=(14, 10), background='#edf1f8', foreground=INK, borderwidth=0)
        style.map('TButton', background=[('active', '#e0e7f3')])
        style.configure('Primary.TButton', background=BLUE, foreground='white', padding=(16, 11))
        style.map('Primary.TButton', background=[('active', '#244ed1'), ('disabled', '#9bafd9')])
        style.configure('TEntry', padding=7, fieldbackground='white', bordercolor=LINE)
        style.configure('TCombobox', padding=7, fieldbackground='white')
        style.configure('TNotebook', background=BG, borderwidth=0)
        style.configure('TNotebook.Tab', padding=(8, 10), background=BG, font=(FONT, 10))
        style.map('TNotebook.Tab', background=[('selected', 'white')], foreground=[('selected', BLUE)])
        self.sidebar = tk.Frame(root, bg=NAVY, width=220)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        label(self.sidebar, 'ИГРЫ', size=28, bold=True, color='white', bg=NAVY).pack(anchor='w', padx=25, pady=(27, 0))
        label(self.sidebar, 'П Р А К Т И К У М', size=9, color='#93a8c6', bg=NAVY).pack(anchor='w', padx=27, pady=(0, 32))
        label(self.sidebar, 'МАТРИЧНЫЕ ИГРЫ', size=8, color='#8298b6', bg=NAVY).pack(anchor='w', padx=25, pady=(0, 14))
        self.nav = []
        for title in NAV_ITEMS:
            item = label(self.sidebar, title, size=11, color='#aabbd2', bg=NAVY, anchor='w', padx=15, pady=13)
            item.pack(fill='x', padx=10, pady=3)
            self.nav.append(item)
        label(self.sidebar, 'Лабораторная работа № 4\n\nСмешанные стратегии.\nСведение к ЛП.',
              size=10, color='#93a8c6', bg=NAVY, justify='left').pack(side='bottom', anchor='w', padx=25, pady=28)
        self.main = tk.Frame(root, bg=BG)
        self.main.pack(side='left', fill='both', expand=True)
        self.header = tk.Frame(self.main, bg=BG)
        self.header.pack(fill='x', padx=28, pady=(24, 16))
        label(self.header, 'Матричные игры', size=23, bold=True, bg=BG).pack(side='left')
        self.new_button = ttk.Button(self.header, text='Новая задача', command=self.setup)
        self.body = tk.Frame(self.main, bg=BG)
        self.body.pack(fill='both', expand=True, padx=28, pady=(0, 22))
        self.setup()
        if startup_error:
            self.setup_error(startup_error)

    def activate_nav(self, index):
        for k, item in enumerate(self.nav):
            item.configure(bg='#253e61' if k == index else NAVY, fg='white' if k == index else '#aabbd2')

    def clear(self):
        for widget in self.body.winfo_children():
            widget.destroy()

    # ---------------------------------------------------------------- setup
    def setup(self):
        if self.lesson and self.lesson.phase != 'done':
            self._confirm_reset()
            return
        self._setup()

    def _confirm_reset(self):
        dialog = tk.Toplevel(self.root)
        dialog.withdraw()
        dialog.title('Новая задача')
        dialog.transient(self.root)
        dialog.configure(bg='white')
        dialog.resizable(False, False)
        label(dialog, 'Начать новую задачу?', size=16, bold=True).pack(padx=28, pady=(25, 12))
        label(dialog, 'Текущий учебный сеанс будет завершён.\nИсходные файлы приложения не изменяются.',
              justify='left').pack(padx=28, pady=(0, 20))
        buttons = tk.Frame(dialog, bg='white')
        buttons.pack(padx=24, pady=(0, 24))
        ttk.Button(buttons, text='Продолжить решение', command=dialog.destroy).pack(side='left', padx=5)
        ttk.Button(buttons, text='Новая задача', style='Primary.TButton',
                   command=lambda: (dialog.destroy(), self._setup())).pack(side='left', padx=5)
        dialog.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - dialog.winfo_reqwidth()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - dialog.winfo_reqheight()) // 2
        dialog.geometry(f'{x:+d}{y:+d}')
        dialog.deiconify()
        dialog.grab_set()

    def _setup(self):
        self.lesson = None
        self.clear()
        self.activate_nav(0)
        self.new_button.pack_forget()
        label(self.body, 'Начните с платёжной матрицы игрока А', size=15, bold=True, bg=BG).pack(anchor='w')
        label(self.body, 'Строки — стратегии игрока А, столбцы — стратегии игрока B. Игрок А максимизирует, B минимизирует свой проигрыш (платёж = выигрыш А).',
              size=10, bg=BG, color=MUTED, wraplength=890, justify='left').pack(anchor='w', pady=(2, 10))
        bar = tk.Frame(self.body, bg='white', padx=16, pady=16)
        bar.pack(fill='x', pady=(0, 12))
        self.preset = ttk.Combobox(bar, values=list(self.variants), state='readonly', width=34)
        if self.variants:
            self.preset.current(0)
        self.preset.grid(row=0, column=0, padx=(0, 8), sticky='w')
        ttk.Button(bar, text='Загрузить', command=self.load_preset).grid(row=0, column=1, padx=(0, 20))
        label(bar, 'Строк (А)').grid(row=0, column=2, padx=(0, 5))
        self.rows = ttk.Spinbox(bar, from_=2, to=8, width=3)
        self.rows.set('3')
        self.rows.grid(row=0, column=3, padx=(0, 10))
        label(bar, 'Столбцов (B)').grid(row=0, column=4, padx=(0, 5))
        self.cols = ttk.Spinbox(bar, from_=2, to=8, width=3)
        self.cols.set('3')
        self.cols.grid(row=0, column=5, padx=(0, 8))
        ttk.Button(bar, text='Создать таблицу', command=self.create_empty).grid(row=0, column=6)
        files = tk.Frame(self.body, bg=BG)
        files.pack(fill='x', pady=(0, 12))
        ttk.Button(files, text='Загрузить вариант из файла', command=self.open_variant).pack(side='left')
        ttk.Button(files, text='Сохранить вариант в файл', command=self.export_variant).pack(side='left', padx=8)
        ttk.Button(files, text='Загрузить все варианты', command=self.open_variants).pack(side='left')
        self.editor = ScrollArea(self.body)
        self.editor.pack(fill='both', expand=True)
        desc_bar = tk.Frame(self.body, bg=BG)
        desc_bar.pack(fill='x', pady=(10, 0))
        label(desc_bar, 'Описание задачи (необязательно)', size=10, bg=BG, color=MUTED).pack(anchor='w')
        self.description_box = tk.Text(desc_bar, height=3, wrap='word', font=(FONT, 10), padx=8, pady=6)
        self.description_box.pack(fill='x', pady=(2, 0))
        self.setup_note = label(self.body, '', bg=BG, color=MUTED, anchor='w', justify='left', wraplength=890)
        self.setup_note.pack(fill='x', pady=12)
        footer = tk.Frame(self.body, bg=BG)
        footer.pack(fill='x')
        ttk.Button(footer, text='Приступить к решению →', style='Primary.TButton', command=self.start).pack(side='right')
        if self.variants:
            self.load_preset()
        else:
            self.create_empty()

    def load_preset(self):
        if self.preset.get() not in self.variants:
            return
        g = self.variants[self.preset.get()]
        self.rows.set(str(len(g.matrix)))
        self.cols.set(str(len(g.matrix[0])))
        self.edit_problem(g)
        self.setup_note.configure(text='')

    def open_variant(self):
        path = filedialog.askopenfilename(parent=self.root, title='Загрузить вариант',
                                           initialdir=str(self.variants_dir), filetypes=[('Вариант JSON', '*.json')])
        if not path:
            return
        try:
            name, g = read_variant(path)
        except ValueError as error:
            self.setup_error(str(error))
            return
        name = append_variant(self.variants, name, g)
        self.preset.configure(values=list(self.variants))
        self.preset.set(name)
        self.load_preset()

    def open_variants(self):
        directory = filedialog.askdirectory(parent=self.root, title='Загрузить все варианты из папки',
                                             initialdir=str(self.variants_dir), mustexist=True)
        if not directory:
            return
        try:
            variants = load_variants(directory)
        except ValueError as error:
            self.setup_error(str(error))
            return
        self.variants = variants
        self.variants_dir = Path(directory)
        self.preset.configure(values=list(self.variants))
        self.preset.current(0)
        self.load_preset()

    def export_variant(self):
        try:
            g = self.read_problem()
        except ValueError as error:
            self.setup_error(str(error))
            return
        path = filedialog.asksaveasfilename(parent=self.root, title='Сохранить вариант',
                                             initialdir=str(self.variants_dir), defaultextension='.json',
                                             filetypes=[('Вариант JSON', '*.json')])
        if not path:
            return
        try:
            save_variant(path, g, name=Path(path).stem)
            self.setup_note.configure(text='')
        except (OSError, ValueError) as error:
            self.setup_error(str(error))

    def create_empty(self):
        try:
            m, n = int(self.rows.get()), int(self.cols.get())
            if not (2 <= m <= 8 and 2 <= n <= 8):
                raise ValueError()
            g = Game(tuple((0,) * n for _ in range(m)),
                      tuple(f'А{i + 1}' for i in range(m)), tuple(f'B{j + 1}' for j in range(n)),
                      name='Новая задача', description='')
            self.edit_problem(g)
            self.setup_note.configure(text='')
        except ValueError:
            self.setup_note.configure(text='Размерность: целые числа от 2 до 8.', fg=RED)

    def edit_problem(self, g):
        for widget in self.editor.inner.winfo_children():
            widget.destroy()
        self.edit_shape = len(g.matrix), len(g.matrix[0])
        self.edit_source = g
        frame = self.editor.inner
        label(frame, 'A \\ B', size=10, color=MUTED).grid(row=0, column=0, padx=10, pady=12)
        self.col_entries = []
        for j in range(self.edit_shape[1]):
            e = ttk.Entry(frame, width=10, justify='center', font=(FONT, 10))
            e.insert(0, g.col_labels[j])
            e.grid(row=0, column=j + 1, padx=4, pady=12)
            self.col_entries.append(e)
        self.row_entries = []
        self.cell_entries = []
        for i in range(self.edit_shape[0]):
            re = ttk.Entry(frame, width=12, font=(FONT, 10))
            re.insert(0, g.row_labels[i])
            re.grid(row=i + 1, column=0, padx=(0, 8), pady=4)
            self.row_entries.append(re)
            row_cells = []
            for j in range(self.edit_shape[1]):
                ce = ttk.Entry(frame, width=8, justify='center')
                ce.insert(0, str(g.matrix[i][j]))
                ce.grid(row=i + 1, column=j + 1, padx=4, pady=4, ipady=4)
                row_cells.append(ce)
            self.cell_entries.append(row_cells)
        self.description_box.delete('1.0', 'end')
        self.description_box.insert('end', g.description)

    def read_problem(self):
        m, n = self.edit_shape
        matrix = tuple(tuple(number(e.get().strip()) for e in row) for row in self.cell_entries)
        row_labels = tuple(e.get().strip() for e in self.row_entries)
        col_labels = tuple(e.get().strip() for e in self.col_entries)
        description = self.description_box.get('1.0', 'end').strip()
        name = getattr(self.edit_source, 'name', 'Новая задача')
        return Game(matrix, row_labels, col_labels, name=name, description=description)

    def setup_error(self, error):
        self.setup_note.configure(text=str(error), fg=RED)

    # --------------------------------------------------------------- lesson
    def start(self):
        try:
            g = self.read_problem()
            self.lesson = Lesson(g)
        except ValueError as error:
            self.setup_error(error)
            return
        self.feedback = 'Условие принято.'
        self.feedback_ok = True
        self.show_lesson()

    def show_lesson(self):
        self.clear()
        self.new_button.pack(side='right')
        self.summary = tk.Frame(self.body, bg=BG)
        self.summary.pack(fill='x', pady=(0, 15))
        self.stat_labels = []
        for title in ['ЭТАП', 'ЦЕНА ИГРЫ', 'ОШИБКИ / ПОДСКАЗКИ']:
            card = tk.Frame(self.summary, bg='white', padx=18, pady=12)
            card.pack(side='left', fill='x', expand=True, padx=(0, 10))
            label(card, title, size=8, color=MUTED).pack(anchor='w')
            val = label(card, '', size=16, bold=True)
            val.pack(anchor='w')
            self.stat_labels.append(val)
        self.workspace = tk.Frame(self.body, bg=BG)
        self.workspace.pack(fill='both', expand=True)
        self.workspace.columnconfigure(0, weight=1)
        self.workspace.columnconfigure(1, weight=0, minsize=360)
        self.workspace.rowconfigure(0, weight=1)
        left = tk.Frame(self.workspace, bg='white')
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 14))
        self.notebook = ttk.Notebook(left)
        self.notebook.pack(fill='both', expand=True)
        matrixtab = ScrollArea(self.notebook)
        desctab = tk.Frame(self.notebook, bg='white')
        historytab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(matrixtab, text='Матрица')
        self.notebook.add(desctab, text='Описание')
        self.notebook.add(historytab, text='Журнал')
        self.draw_matrix(matrixtab.inner)
        label(desctab, self.lesson.game.description or 'Описание не задано.', size=12, bg='white',
              wraplength=560, justify='left', anchor='nw', padx=20, pady=20).pack(anchor='nw', fill='both', expand=True)
        self.log = tk.Text(historytab, bg='white', fg=INK, font=(FONT, 11), wrap='word', relief='flat', padx=15, pady=15)
        logbar = ttk.Scrollbar(historytab, command=self.log.yview)
        self.log.configure(yscrollcommand=logbar.set)
        logbar.pack(side='right', fill='y')
        self.log.pack(fill='both', expand=True)
        question_scroll = ScrollArea(self.workspace)
        question_scroll.grid(row=0, column=1, sticky='nsew')
        question_scroll.grid_propagate(False)
        self.question = tk.Frame(question_scroll.inner, bg='white', padx=20, pady=20)
        self.question.pack(fill='both', expand=True)
        self.refresh()

    def draw_matrix(self, frame):
        g = self.lesson.game
        m, n = self.lesson.m, self.lesson.n
        label(frame, 'A \\ B', size=10, color=MUTED, padx=10, pady=9).grid(row=0, column=0, sticky='nsew')
        for j in range(n):
            label(frame, g.col_labels[j], bold=True, bg='#edf5ff', padx=10, pady=9).grid(row=0, column=j + 1, sticky='nsew')
        for i in range(m):
            label(frame, g.row_labels[i], bold=True, bg='#edf5ff', padx=10, pady=9).grid(row=i + 1, column=0, sticky='nsew')
            for j in range(n):
                label(frame, str(self.lesson.matrix[i][j]), padx=10, pady=9).grid(row=i + 1, column=j + 1, sticky='nsew')

    def refresh(self):
        lsn = self.lesson
        self.activate_nav(lsn.step)
        self.stat_labels[0].configure(text=PHASE_TITLES[lsn.phase])
        self.stat_labels[1].configure(text=str(lsn.value) if lsn.value is not None else '—')
        self.stat_labels[2].configure(text=f'{lsn.errors} / {lsn.hints}')
        self.log.configure(state='normal')
        self.log.delete('1.0', 'end')
        for k, item in enumerate(lsn.history, 1):
            self.log.insert('end', f'{k:02d}   {item}\n\n')
        self.log.configure(state='disabled')
        self.log.see('end')
        for widget in self.question.winfo_children():
            widget.destroy()
        phase = lsn.phase
        label(self.question, f'ШАГ {lsn.step:02d}', size=9, bold=True, color=BLUE).pack(anchor='w')
        label(self.question, PHASE_TITLES[phase], size=17, bold=True, wraplength=300, justify='left').pack(anchor='w', pady=(9, 10))
        label(self.question, self._formula(phase), size=10, wraplength=300, justify='left', color=MUTED).pack(anchor='w', pady=(0, 14))
        if phase == 'value' and lsn.solution:
            s = lsn.solution
            info = f'x = {fmt_row(s.x)}\ny = {fmt_row(s.y)}\nLmin = {s.lmin}'
            label(self.question, info, size=10, bg='#edf4ff', color=INK, justify='left', anchor='w',
                  padx=10, pady=10, wraplength=300).pack(anchor='w', fill='x', pady=(0, 12))
        self._build_input(phase)
        self.feedback_label = label(self.question, '', size=10, color=RED, bg='#fff0f0', wraplength=280, justify='left', anchor='w', padx=10, pady=10)
        self.update_feedback()
        self.hint_button = None
        if phase not in ('done', 'solve'):
            self.hint_button = ttk.Button(self.question, text='Подсказка', command=self.hint)
            self.hint_button.pack(fill='x', pady=(0, 8))
        self.hint_label = label(self.question, '', size=10, color='#2454a6', bg='#edf4ff', wraplength=280, justify='left', anchor='w', padx=10, pady=10)

    @staticmethod
    def _formula(phase):
        return {
            'alpha': 'α = max по строкам из минимумов строки — нижняя цена игры (гарантированный выигрыш А при чистых стратегиях).',
            'beta': 'β = min по столбцам из максимумов столбца — верхняя цена игры (гарантированный проигрыш B).',
            'saddle': 'Если α = β, матрица имеет седловую точку: оптимальны чистые стратегии, а цена игры равна α (=β).',
            'pure': 'Укажите строку и столбец, образующие седловую точку: строку с минимумом, равным α, и столбец с максимумом, равным β.',
            'solve': 'Нажмите, чтобы получить решения вспомогательных задач линейного программирования для обоих игроков (симплекс-метод).',
            'value': 'ν = ν* − c, где ν* = 1/Lmin — цена игры со сдвинутой (положительной) матрицей, c — добавленный сдвиг.',
            'prob_a': 'pᵢ = xᵢ·ν* — вероятность применения стратегии i игроком А. Σp = 1.',
            'prob_b': 'qⱼ = yⱼ·ν* — вероятность применения стратегии j игроком B. Σq = 1.',
            'done': 'Решение зафиксировано. Можно начать новую задачу.',
        }[phase]

    def _build_input(self, phase):
        lsn = self.lesson
        if phase in ('alpha', 'beta', 'value'):
            label(self.question, 'Ваш ответ', size=10, bold=True).pack(anchor='w', pady=(4, 5))
            self.answer_entry = ttk.Entry(self.question, width=22, font=(FONT, 15))
            self.answer_entry.pack(fill='x')
            self.answer_entry.bind('<Return>', lambda e: self.check())
            ttk.Button(self.question, text='Проверить ответ', style='Primary.TButton',
                       command=self.check).pack(fill='x', pady=(10, 8))
        elif phase == 'saddle':
            buttons = tk.Frame(self.question, bg='white')
            buttons.pack(fill='x', pady=(0, 8))
            ttk.Button(buttons, text='Да, есть', style='Primary.TButton',
                       command=lambda: self.check(True)).pack(side='left', expand=True, fill='x', padx=(0, 6))
            ttk.Button(buttons, text='Нет', command=lambda: self.check(False)).pack(side='left', expand=True, fill='x')
        elif phase == 'pure':
            label(self.question, 'Строка (А)', size=10, bold=True).pack(anchor='w', pady=(4, 3))
            self.row_combo = ttk.Combobox(self.question, values=list(range(1, lsn.m + 1)), state='readonly', width=6)
            self.row_combo.current(0)
            self.row_combo.pack(anchor='w')
            label(self.question, 'Столбец (B)', size=10, bold=True).pack(anchor='w', pady=(10, 3))
            self.col_combo = ttk.Combobox(self.question, values=list(range(1, lsn.n + 1)), state='readonly', width=6)
            self.col_combo.current(0)
            self.col_combo.pack(anchor='w')
            ttk.Button(self.question, text='Проверить ответ', style='Primary.TButton',
                       command=self.check).pack(fill='x', pady=(14, 8))
        elif phase == 'solve':
            ttk.Button(self.question, text='Решить задачи ЛП', style='Primary.TButton',
                       command=self.check).pack(fill='x', pady=(4, 8))
        elif phase in ('prob_a', 'prob_b'):
            labels = lsn.game.row_labels if phase == 'prob_a' else lsn.game.col_labels
            self.prob_entries = []
            for name in labels:
                label(self.question, name, size=10).pack(anchor='w', pady=(6, 2))
                e = ttk.Entry(self.question, width=16)
                e.pack(anchor='w')
                self.prob_entries.append(e)
            ttk.Button(self.question, text='Проверить ответ', style='Primary.TButton',
                       command=self.check).pack(fill='x', pady=(14, 8))
        elif phase == 'done':
            lsn2 = lsn
            if lsn2.solution:
                summary = (f'Цена игры ν = {lsn2.value}\n'
                           f'p = {fmt_row(lsn2.solution.p)}\n'
                           f'q = {fmt_row(lsn2.solution.q)}')
            else:
                summary = f'Седловая точка, цена игры = {lsn2.value}.'
            label(self.question, summary, size=11, bg='#edf9f3', color=GREEN, justify='left', anchor='w',
                  padx=10, pady=10, wraplength=280).pack(anchor='w', fill='x', pady=(0, 10))
            ttk.Button(self.question, text='Решить другую задачу', style='Primary.TButton',
                       command=self._setup).pack(fill='x')

    def hint(self):
        self.hint_label.configure(text='Подсказка\n\n' + self.lesson.hint())
        self.hint_label.pack(fill='x', pady=(0, 12))
        self.stat_labels[2].configure(text=f'{self.lesson.errors} / {self.lesson.hints}')

    def check(self, forced=None):
        lsn = self.lesson
        try:
            if lsn.phase in ('alpha', 'beta', 'value'):
                answer = number(self.answer_entry.get().strip())
            elif lsn.phase == 'saddle':
                answer = forced
            elif lsn.phase == 'pure':
                answer = (int(self.row_combo.get()) - 1, int(self.col_combo.get()) - 1)
            elif lsn.phase in ('prob_a', 'prob_b'):
                answer = tuple(number(e.get().strip()) for e in self.prob_entries)
            else:
                answer = None
        except ValueError:
            lsn.errors += 1
            self.feedback, self.feedback_ok = 'Ошибка ввода.', False
            self.update_feedback()
            return
        try:
            accepted, feedback = lsn.check(answer)
        except Exception as error:
            messagebox.showerror('Ошибка вычисления', str(error))
            return
        self.feedback, self.feedback_ok = ('' if accepted else feedback), accepted
        if accepted:
            self.refresh()
        else:
            self.update_feedback()

    def update_feedback(self):
        self.stat_labels[2].configure(text=f'{self.lesson.errors} / {self.lesson.hints}')
        if self.feedback_ok:
            self.feedback_label.pack_forget()
        else:
            self.feedback_label.configure(text=self.feedback)
            self.feedback_label.pack(fill='x', pady=(0, 12))


def main():
    if sys.platform == 'win32':
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            pass
    root = tk.Tk()
    if '--smoke-test' in sys.argv:
        root.withdraw()
    app = App(root)
    if '--smoke-test' in sys.argv:
        root.update_idletasks()
        assert app.lesson is None
        app.start()
        root.update_idletasks()
        assert app.lesson is not None
        root.destroy()
        print('Tk startup, problem editor and lesson rendering: OK')
    else:
        root.mainloop()


if __name__ == '__main__':
    main()
