"""Acceptance scenarios driven by Tk events and an exhaustive, non-DP oracle.

Run with a working display: python -m unittest test_acceptance -v
Optional LAB3_QA_OUTPUT writes the six calculation protocols as evidence.
"""
import itertools
import os
from pathlib import Path
import tempfile
import tkinter as tk
from tkinter import ttk
import unittest
from unittest.mock import patch

from app import App
from formats import load
from model import Problem
from presets import PRESETS


def exhaustive(problem, start=0, used=0):
    scored = [(sum(row[x] for row, x in zip(problem.values[start:], plan)), plan)
              for plan in itertools.product(*(range(len(row)) for row in problem.values[start:]))
              if used + sum(w*x for w, x in zip(problem.weights[start:], plan)) <= problem.capacity]
    best = max(value for value, _ in scored)
    return best, [plan for value, plan in scored if value == best]


def widgets(parent):
    for child in parent.winfo_children():
        yield child
        yield from widgets(child)


class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.geometry('1280x820')
        self.app.update()
        self.app._apply_compact_layout()
        self.callback_errors = []
        self.app.report_callback_exception = lambda *args: self.callback_errors.append(args)

    def tearDown(self):
        self.app.destroy()
        self.assertEqual(self.callback_errors, [], 'Unhandled Tk callback exception')

    def click_cell(self, grid, row=0, col=1):
        self.app.update_idletasks()
        grid._ensure_visible(row, col)
        self.app.update_idletasks()
        x = int(grid.positions[col] + 10 - grid.canvas.canvasx(0))
        y = int(grid.header_height + row*grid.row_height + 10 - grid.canvas.canvasy(0))
        grid.canvas.event_generate('<Button-1>', x=x, y=y)
        self.app.update()
        self.assertEqual(grid.selected, (row, col))

    def paste(self, grid, rows, row=0, col=1):
        self.click_cell(grid, row, col)
        self.app.clipboard_clear()
        self.app.clipboard_append('\n'.join('\t'.join(map(str, r)) for r in rows))
        target = grid.entry if grid.entry is not None else grid.canvas
        target.event_generate('<<Paste>>')
        self.app.update()

    def complete_tables(self, p):
        # Expected answers never come from Lesson.solution / solver / displayed rows.
        for j in reversed(range(len(p.weights))):
            states = [0] if j == 0 else range(p.capacity + 1)
            candidates, summaries = [], []
            for y in states:
                row = []
                for x, own in enumerate(p.values[j]):
                    used = y + p.weights[j]*x
                    row.append('—' if used > p.capacity else own + exhaustive(p, j+1, used)[0])
                best = max(v for v in row if v != '—')
                candidates.append(row)
                # Last tied column tests that first-maximum-only checking is absent.
                summaries.append([best, max(x for x, v in enumerate(row) if v == best)])
            self.assertEqual((self.app.lesson.phase, self.app.lesson.current_stage.index), ('candidates', j))
            self.paste(self.app.answer_grid, candidates)
            self.app.check_button.invoke()
            self.assertEqual(self.app.lesson.phase, 'summary')
            self.paste(self.app.answer_grid, summaries)
            self.app.check_button.invoke()
        self.assertEqual(self.app.lesson.phase, 'restore')

    def finish(self, p, plan):
        states, used = [], 0
        for w, x in zip(p.weights, plan):
            states.append(used)
            used += w*x
        self.paste(self.app.answer_grid, [states, plan])
        self.app.check_button.invoke()
        self.assertEqual(self.app.screen, 'result')
        self.assertEqual(self.app.final_plan, plan)
        self.assertEqual(self.app.lesson.accepted_states, tuple(states))
        return self.app.report_text()

    def test_all_six_tasks_all_ten_optima_through_interface(self):
        expected = [40, 21, 34, 3400, 2500, 320]
        completed = 0
        for index, p in enumerate(PRESETS):
            value, plans = exhaustive(p)
            self.assertEqual(value, expected[index])
            for plan in plans:
                with self.subTest(task=index, plan=plan):
                    self.app.set_problem(p)
                    self.assertTrue(self.app.begin())
                    self.complete_tables(p)
                    report = self.finish(p, plan)
                    self.assertEqual(self.app.lesson.errors, 0)
                    self.assertEqual(len(self.app.accepted), 2*len(p.weights))
                    self.assertIn(f'Максимальная ценность: {value}', report)
                    if directory := os.environ.get('LAB3_QA_OUTPUT'):
                        Path(directory).mkdir(parents=True, exist_ok=True)
                        Path(directory, f'task-{index}-plan-{completed}.txt').write_text(report, encoding='utf-8')
                    completed += 1
        self.assertEqual(completed, 10)

    def test_custom_boundary_and_nonlinear_tasks(self):
        problems = [Problem('B=1', 1, (1,), ((0, '1/3'),)),
                    Problem('Недоступные грузы', 1, (2, 1), ((0, 99), (0,))),
                    Problem('Нелинейные дроби', 5, (2, 1), ((0, '2,5', 1), (0, '1/3', '2/3'))),
                    Problem('B=200', 200, (1,), (tuple(range(201)),))]
        for p in problems:
            with self.subTest(name=p.name):
                self.app.set_problem(p)
                self.assertTrue(self.app.begin())
                self.complete_tables(p)
                self.finish(p, exhaustive(p)[1][-1])

    def test_keyboard_tab_return_escape_and_readonly_cells(self):
        g = self.app.editor_grid
        self.click_cell(g, 0, 4)
        g.entry.focus_force()
        for key in ('3', 'slash', '2'):
            g.entry.event_generate('<KeyPress>', keysym=key)
        g.entry.event_generate('<Tab>')
        self.app.update()  # Let native focus settle before the next user action.
        self.assertEqual(g.rows[0][4], '3/2')
        self.assertEqual(g.selected, (0, 5))
        g.entry.insert(0, '999')
        g.entry.event_generate('<Escape>')
        self.app.update()
        self.assertIsNone(g.entry)
        self.assertEqual(g.rows[0][5], '17')
        self.click_cell(g, 0, 4)
        g.entry.event_generate('<Return>')
        self.app.update()
        self.assertEqual(g.selected, (1, 4))
        self.click_cell(g, 0, 3)
        self.assertIsNone(g.entry)
        self.app.clipboard_clear()
        self.app.clipboard_append('999')
        g.canvas.event_generate('<<Paste>>')
        self.assertEqual(g.rows[0][3], '0')

    def test_arrow_keys_commit_input_and_move_in_all_four_directions(self):
        g = self.app.editor_grid
        self.click_cell(g, 0, 4)
        g.entry.focus_force()
        self.app.update()
        for key, destination, value in [('Right', (0, 5), '12'),
                                        ('Down', (1, 5), '34'),
                                        ('Left', (1, 4), '56'),
                                        ('Up', (0, 4), '78')]:
            origin = g.selected
            g.entry.delete(0, 'end')
            g.entry.insert(0, value)
            g.entry.event_generate('<' + key + '>')
            self.app.update()
            self.assertEqual(g.rows[origin[0]][origin[1]], value)
            self.assertEqual(g.selected, destination)
            self.assertIsNotNone(g.entry)
            self.assertIs(self.app.focus_get(), g.entry)
        g.entry.event_generate('<Left>')  # Immutable F(0).
        self.app.update()
        self.assertEqual(g.selected, (0, 3))
        self.assertIsNone(g.entry)
        self.assertIs(self.app.focus_get(), g.canvas)
        g.canvas.event_generate('<Right>')
        self.app.update()
        self.assertEqual(g.selected, (0, 4))
        g.canvas.event_generate('<KeyPress>', keysym='7')
        self.app.update()
        self.assertEqual(g.entry.get(), '7')
        self.assertEqual(g.rows[0][3], '0')
        g.entry.event_generate('<Up>')  # Stay within the top edge.
        self.app.update()
        self.assertEqual(g.selected, (0, 4))
        self.assertEqual(g.rows[0][4], '7')

    def test_arrows_scroll_lesson_and_leave_unavailable_cells_readonly(self):
        self.app.set_problem(Problem('Scrolling', 200, (1, 1), ((0, 1), (0, 2))))
        self.app.begin()
        self.click_cell(self.app.answer_grid, 0, 2)
        g = self.app.answer_grid
        g.entry.focus_force()
        self.app.update()
        for row in range(25):
            g.entry.delete(0, 'end')
            g.entry.insert(0, str(row))
            g.entry.event_generate('<Down>')
            self.app.update()
            self.assertEqual(g.rows[row][2], str(row))
            self.assertEqual(g.selected, (row + 1, 2))
        self.assertGreater(g.canvas.yview()[0], 0)
        self.click_cell(g, 199, 2)
        g.entry.event_generate('<Down>')
        self.app.update()
        self.assertEqual(g.selected, (200, 2))
        self.assertIsNone(g.entry)
        self.assertEqual(g.rows[200][2], '—')
        g.canvas.event_generate('<Up>')
        self.app.update()
        self.assertEqual(g.selected, (199, 2))

    def test_pending_cell_is_protected_on_replace(self):
        g = self.app.editor_grid
        self.click_cell(g, 0, 4)
        g.entry.delete(0, 'end')
        g.entry.insert(0, '123')
        self.app.preset_box.current(1)
        with patch('app.messagebox.askyesno', return_value=False) as confirm:
            self.app.choose_preset()
            confirm.assert_called_once()
        self.assertEqual(self.app.editor_grid.get_rows()[0][4], '123')
        self.assertEqual(self.app.problem, PRESETS[0])

    def test_pending_cell_is_protected_on_close(self):
        g = self.app.editor_grid
        self.click_cell(g, 0, 4)
        g.entry.delete(0, 'end')
        g.entry.insert(0, '123')
        with patch('app.messagebox.askyesno', return_value=False) as confirm, patch.object(self.app, 'destroy') as destroy:
            self.app.close()
            confirm.assert_called_once()
            destroy.assert_not_called()

    def test_context_menu_paste_marks_name_dirty(self):
        entry = next(w for w in widgets(self.app) if isinstance(w, ttk.Entry)
                     and str(w.cget('textvariable')) == str(self.app.name_var))
        self.app.clipboard_clear()
        self.app.clipboard_append('Название после вставки')
        entry.selection_range(0, 'end')
        entry.event_generate('<<Paste>>')
        self.app.update()
        self.assertEqual(self.app.name_var.get(), 'Название после вставки')
        self.assertTrue(self.app.dirty)

    def test_file_dialog_cancellation_and_save_failure_keep_edits(self):
        self.paste(self.app.editor_grid, [['7/3']], col=4)
        before = self.app.read_problem()
        with patch('app.filedialog.askopenfilename', return_value=''), patch('app.filedialog.asksaveasfilename', return_value=''):
            self.app.open_file()
            self.app.save_file()
        self.assertEqual(self.app.read_problem(), before)
        self.assertTrue(self.app.dirty)
        with patch('app.filedialog.asksaveasfilename', return_value='/unused.json'), \
             patch('app.save', side_effect=OSError('test write error')), patch('app.messagebox.showerror') as error:
            self.app.save_file()
            error.assert_called_once()
        self.assertTrue(self.app.dirty)
        self.assertEqual(self.app.read_problem(), before)

    def test_save_reload_and_declined_import(self):
        self.paste(self.app.editor_grid, [['7/3']], col=4)
        before = self.app.read_problem()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, 'моё условие.json')
            with patch('app.filedialog.asksaveasfilename', return_value=str(path)):
                self.app.save_file()
            self.assertEqual(load(path), before)
            self.assertFalse(self.app.dirty)
            self.paste(self.app.editor_grid, [['8/3']], col=4)
            with patch('app.filedialog.askopenfilename', return_value=str(path)), patch('app.messagebox.askyesno', return_value=False):
                self.app.open_file()
            self.assertEqual(str(self.app.read_problem().values[0][1]), '8/3')
            with patch('app.filedialog.askopenfilename', return_value=str(path)), patch('app.messagebox.askyesno', return_value=True):
                self.app.open_file()
            self.assertEqual(self.app.read_problem(), before)
            self.assertFalse(self.app.dirty)

    def test_invalid_editor_values_do_not_start_lesson(self):
        for col, value in [(1, '0'), (1, '1/2'), (2, '-1'), (2, '201'), (4, ''),
                           (4, '-1'), (4, '1/0'), (4, 'nan'), (4, '1e99999')]:
            with self.subTest(col=col, value=value):
                self.app.set_problem(PRESETS[0])
                self.paste(self.app.editor_grid, [[value]], col=col)
                self.assertFalse(self.app.begin())
                self.assertEqual(self.app.screen, 'editor')
                self.assertIsNone(self.app.lesson)
        for capacity in ('0', '201', '2.5', 'abc'):
            self.app.set_problem(PRESETS[0])
            self.app.capacity_var.set(capacity)
            self.assertFalse(self.app.begin())

    def test_abandon_lesson_cancel_then_confirm(self):
        self.app.begin()
        self.paste(self.app.answer_grid, [['123']])
        original = self.app.lesson
        with patch('app.messagebox.askyesno', return_value=False):
            self.app.return_to_editor()
        self.assertIs(self.app.lesson, original)
        self.assertEqual(self.app.answer_grid.get_rows()[0][1], '123')
        with patch('app.messagebox.askyesno', return_value=True):
            self.app.return_to_editor()
        self.assertEqual(self.app.screen, 'editor')
        self.assertIsNone(self.app.lesson)
        self.assertEqual(self.app.read_problem(), PRESETS[0])

    def test_wrong_maximum_and_restore_can_be_corrected(self):
        p = Problem('Контроль ошибок', 2, (1,), ((0, 2, 3),))
        self.app.set_problem(p)
        self.app.begin()
        self.paste(self.app.answer_grid, [[0, 2, 3]])
        self.app.check_button.invoke()
        self.paste(self.app.answer_grid, [[2, 1]])
        self.app.check_button.invoke()
        self.assertEqual(self.app.lesson.phase, 'summary')
        self.assertEqual(self.app.lesson.errors, 1)
        self.assertTrue(self.app.answer_grid.invalid)
        self.paste(self.app.answer_grid, [[3, 2]])
        self.app.check_button.invoke()
        for states, plan in [([1], [2]), ([0], [1]), ([0], ['1/2']), ([0], [3])]:
            self.paste(self.app.answer_grid, [states, plan])
            self.app.check_button.invoke()
            self.assertEqual(self.app.lesson.phase, 'restore')
        self.finish(p, (2,))
        self.assertEqual(self.app.lesson.errors, 5)

    def test_explanation_requires_explicit_hint_and_has_no_attempt_limit(self):
        p = Problem('Подсказки', 1, (1,), ((0, 3),))
        self.app.set_problem(p)
        self.app.begin()
        for _ in range(25):
            self.app.check_button.invoke()
        self.assertEqual(self.app.lesson.errors, 25)
        self.assertEqual(self.app.lesson.phase, 'candidates')
        self.assertEqual(self.app.hint_var.get(), '')
        self.assertEqual(self.app.message_var.get(),
                         'Ответ неверный. Проверьте отмеченные поля. Пояснение доступно по кнопке «Подсказка».')
        self.complete_tables(p)
        labels = [str(w.cget('text')) for w in widgets(self.app) if 'text' in w.keys()]
        self.assertFalse(any('Начните с y₁ = 0' in text for text in labels))
        self.assertEqual(self.app.lesson.hints, 0)
        self.app.show_hint()
        self.assertIn('Начните с y₁ = 0', self.app.hint_var.get())
        self.assertEqual(self.app.lesson.hints, 1)
        self.finish(p, (1,))
        self.assertIn('Ошибки: 25', self.app.report_text())
        self.assertIn('Подсказки: 1', self.app.report_text())

    def test_new_table_and_individual_limits(self):
        self.app.count_var.set('2')
        self.app.limit_var.set('1')
        self.app.capacity_var.set('3')
        with patch('app.messagebox.askyesno', return_value=False):
            self.app.new_table()
        self.assertEqual(len(self.app.editor_grid.rows), 4)
        with patch('app.messagebox.askyesno', return_value=True):
            self.app.new_table()
        self.assertEqual(len(self.app.editor_grid.rows), 2)
        self.paste(self.app.editor_grid, [['2']], row=1, col=2)
        self.app.apply_limits()
        self.assertFalse(self.app.begin())  # Newly available F(2) must be filled.
        self.paste(self.app.editor_grid, [['5', '9']], row=1, col=4)
        p = self.app.read_problem()
        self.assertEqual(p.quantities, (1, 2))
        self.assertEqual(p.values[1], (0, 5, 9))
        self.assertTrue(self.app.begin())
        self.complete_tables(p)
        self.finish(p, exhaustive(p)[1][-1])

    def test_minimum_window_keeps_review_and_restore_actions_visible(self):
        self.app.geometry('1100x680')
        self.app.update()
        self.app._apply_compact_layout()
        self.app.zoom.set('140%')
        self.app.rescale()
        self.app.begin()
        def assert_button(text):
            self.app.update_idletasks()
            button = next(w for w in widgets(self.app) if isinstance(w, ttk.Button)
                          and w.cget('text') == text)
            self.assertTrue(button.winfo_ismapped(), text)
            self.assertGreaterEqual(button.winfo_height(), button.winfo_reqheight(), text)
            self.assertLessEqual(button.winfo_rooty() + button.winfo_height(),
                                 self.app.winfo_rooty() + self.app.winfo_height(), text)
        assert_button('Открыть таблицу')
        self.complete_tables(PRESETS[0])
        assert_button('Открыть все принятые максимумы')
        self.finish(PRESETS[0], (1, 1, 1, 1))
        assert_button('Сохранить отчёт  ↓')
        assert_button('Принятые таблицы')
        note = next(w for w in widgets(self.app) if 'text' in w.keys()
                    and w.cget('text') == 'Суммарный расход не превышает ёмкость. Свободный ресурс допустим.')
        self.assertTrue(note.winfo_ismapped())

    def test_resize_and_all_zoom_levels_preserve_active_input(self):
        for width, height in [(1100, 680), (1440, 900)]:
            for zoom in ['80%', '100%', '120%', '140%']:
                with self.subTest(size=(width, height), zoom=zoom):
                    self.app.geometry(f'{width}x{height}')
                    self.app.update()
                    self.app._apply_compact_layout()
                    self.paste(self.app.editor_grid, [['7/3']], col=4)
                    self.app.zoom.set(zoom)
                    self.app.rescale()
                    self.app.update()
                    self.assertEqual(str(self.app.read_problem().values[0][1]), '7/3')
                    self.assertGreater(self.app.editor_grid.canvas.winfo_height(), self.app.editor_grid.header_height)
                    start = next(w for w in widgets(self.app) if isinstance(w, ttk.Button)
                                 and w.cget('text') == 'Начать практикум  →')
                    self.assertTrue(start.winfo_ismapped())
                    self.assertLessEqual(start.winfo_rooty()+start.winfo_height(), self.app.winfo_rooty()+self.app.winfo_height())


if __name__ == '__main__':
    unittest.main()
