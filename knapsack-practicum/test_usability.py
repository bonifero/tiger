"""Regression checks for simultaneous references, navigation and source validation."""
import unittest
from tkinter import ttk, font
from unittest.mock import patch

from app import App, DataGrid, GREEN, RED
from model import Problem
from presets import PRESETS


def widgets(parent):
    for child in parent.winfo_children():
        yield child
        yield from widgets(child)


class UsabilityTests(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.geometry('1024x700')
        self.app.update()
        self.app._apply_compact_layout()
        self.callback_errors = []
        self.app.report_callback_exception = lambda *args: self.callback_errors.append(args)

    def tearDown(self):
        self.app.destroy()
        self.assertEqual(self.callback_errors, [])

    def accept_table(self):
        stage = self.app.lesson.current_stage
        grid = self.app.answer_grid
        if self.app.lesson.phase == 'candidates':
            for r, y in enumerate(stage.states):
                for x, value in enumerate(stage.candidates[y]):
                    if value is not None:
                        grid.set_value(r, x + 1, value)
        else:
            for r, y in enumerate(stage.states):
                grid.set_value(r, 1, stage.best[y])
                grid.set_value(r, 2, stage.choices[y][0])
        self.assertTrue(self.app.check_answers())
        self.app.update_idletasks()

    def test_example_candidates_fit_beside_reference_at_normal_zoom(self):
        self.app.begin()
        self.app.update_idletasks()
        grid = self.app.answer_grid
        self.assertEqual(len(grid.columns), 6)  # y and x=0…4
        self.assertLessEqual(grid.positions[-1], grid.canvas.winfo_width())
        self.assertFalse(grid.horizontal.winfo_ismapped())
        self.assertLessEqual(grid.header_height + len(grid.rows) * grid.row_height,
                             grid.canvas.winfo_height())
        self.assertFalse(grid.vertical.winfo_ismapped())
        self.assertTrue(self.app.reference_notebook.winfo_ismapped())
        self.assertTrue(self.app.check_button.winfo_ismapped())

    def test_impossible_trailing_quantities_are_hidden_but_full_model_payload_is_preserved(self):
        self.app.set_problem(Problem('Тяжёлый груз', 3, (1, 2), ((0, 2), (0, 5, 10, 15, 20))))
        self.app.begin()
        self.assertEqual(self.app.answer_grid.columns, ('y', 'x = 0', 'x = 1'))
        self.assertEqual(self.app.answer_grid.rows[2], ['2', '', '—'])
        self.assertEqual(len(self.app.lesson.current_stage.candidates[0]), 5)
        with patch.object(self.app.lesson, 'submit_candidates',
                          wraps=self.app.lesson.submit_candidates) as submit:
            self.accept_table()
        payload = submit.call_args.args[0]
        self.assertEqual(payload[0], ['0', '5', None, None, None])
        self.assertEqual(payload[2], ['0', None, None, None, None])
        self.assertEqual(self.app.lesson.phase, 'summary')
        self.assertEqual(len(self.app.reference_grids[0].columns), 3)
        self.assertEqual(self.app.accepted[0]['rows'][0], ['0', '0', '5'])

    def test_footer_uses_available_width_and_preserves_feedback_on_resize(self):
        self.app.geometry('1440x900')
        self.app.update()
        self.app._apply_compact_layout()
        self.app.begin()
        self.accept_table()
        self.app.update()
        label = self.app.message_label
        metrics = font.Font(font=label.cget('font'))
        self.assertGreater(label.winfo_width(), metrics.measure(self.app.message_var.get()))
        self.assertLessEqual(label.winfo_reqheight(), metrics.metrics('linespace') + 8)
        self.assertEqual(label.cget('fg'), GREEN)
        wide_wrap = int(label.cget('wraplength'))
        self.app.geometry('1024x700')
        self.app.update()
        self.app._apply_compact_layout()
        self.app.zoom.set('140%')
        self.app.rescale()
        self.app.update()
        label = self.app.message_label
        self.assertLess(int(label.cget('wraplength')), wide_wrap)
        self.assertAlmostEqual(int(label.cget('wraplength')), label.master.winfo_width() - 4, delta=1)
        self.assertEqual(label.cget('fg'), GREEN)
        self.assertGreaterEqual(self.app.check_button.winfo_width(), self.app.check_button.winfo_reqwidth())
        self.assertFalse(self.app.check_answers())
        self.app.update()
        self.assertEqual(self.app.message_label.cget('fg'), RED)

    def test_step_references_only_show_source_and_accepted_answers(self):
        self.app.begin()
        self.app.update_idletasks()
        self.assertEqual(len(self.app.reference_grids), 1)
        self.assertEqual(self.app.reference_grids[0].rows, [['0', '9', '19', '26', '35']])
        self.assertFalse(self.app.reference_grids[0].editable)
        self.assertEqual(self.app.accepted, [])
        self.accept_table()
        self.assertEqual(self.app.lesson.phase, 'summary')
        self.assertEqual(self.app.reference_grids[0].rows, self.app.accepted[-1]['rows'])
        self.assertFalse(self.app.reference_grids[0].editable)
        self.accept_table()
        self.assertEqual(self.app.lesson.phase, 'candidates')
        self.assertEqual(len(self.app.reference_grids), 2)
        self.assertEqual(self.app.reference_grids[0].rows, [['0', '10', '18', '24', '34']])
        self.assertEqual(self.app.reference_grids[1].rows, self.app.accepted[-1]['rows'])
        self.assertFalse(any(grid.editable for grid in self.app.reference_grids))
        self.assertFalse(any(widget.winfo_class() == 'Toplevel' for widget in self.app.winfo_children()))

    def test_restore_has_all_accepted_states_visible_in_inline_table(self):
        self.app.begin()
        while self.app.lesson.phase in ('candidates', 'summary'):
            self.accept_table()
        self.assertEqual(self.app.lesson.phase, 'restore')
        expected = [[str(e['index'] + 1), *row] for e in reversed(self.app.accepted)
                    if e['phase'] == 'summary' for row in e['rows']]
        self.assertEqual(self.app.reference_grids[0].rows, expected)
        self.assertEqual(len(expected), 16)  # 1 state for item 1, five for items 2–4.
        self.assertTrue(self.app.reference_grids[0].winfo_ismapped())
        self.app.update()
        grid = self.app.answer_grid
        self.assertLessEqual(grid.positions[-1], grid.canvas.winfo_width())
        self.assertFalse(grid.horizontal.winfo_ismapped())

    def test_restore_shows_original_weights_and_capacity_beside_answers(self):
        self.app.set_problem(Problem('Разные веса', 5, (2, 3), ((0, 5, 9), (0, 8))))
        self.app.begin()
        while self.app.lesson.phase in ('candidates', 'summary'):
            self.accept_table()
        self.assertEqual(self.app.lesson.phase, 'restore')
        self.assertEqual(self.app.restore_weights_grid.columns, ('1', '2'))
        self.assertEqual(self.app.restore_weights_grid.rows, [['2', '3']])
        self.assertFalse(self.app.restore_weights_grid.editable)
        self.assertIn('B = 5', self.app.restore_source_label.cget('text'))
        self.assertTrue(self.app.restore_weights_grid.winfo_ismapped())
        self.assertEqual(len(self.app.answer_grid.rows), 2)
        self.assertTrue(all(cell == '' for row in self.app.answer_grid.rows for cell in row[1:]))
        self.assertEqual(len(self.app.reference_grids[0].rows), 7)

    def test_finished_lesson_retains_every_candidate_and_summary_table(self):
        self.app.begin()
        while self.app.lesson.phase in ('candidates', 'summary'):
            self.accept_table()
        for i in range(4):
            self.app.answer_grid.set_value(0, i + 1, i)
            self.app.answer_grid.set_value(1, i + 1, 1)
        self.assertTrue(self.app.check_answers())
        self.assertEqual(self.app.screen, 'result')
        button = next(w for w in widgets(self.app.footer)
                      if isinstance(w, ttk.Button) and w.cget('text') == 'Принятые таблицы')
        button.invoke()
        self.app.update_idletasks()
        window = next(w for w in self.app.winfo_children() if w.winfo_class() == 'Toplevel')
        self.assertEqual(len(window.review_selector.cget('values')), len(self.app.accepted))
        for i, entry in enumerate(self.app.accepted):
            window.review_selector.current(i)
            window.review_selector.event_generate('<<ComboboxSelected>>')
            self.assertEqual(window.review_grid.rows, entry['rows'])
            self.assertEqual(window.review_grid.columns, entry['columns'])
            self.assertFalse(window.review_grid.editable)
        window.review_grid.copy_table()
        self.assertIn('\t'.join(self.app.accepted[-1]['rows'][0]), self.app.clipboard_get())
        lesson, history = self.app.lesson, list(self.app.accepted)
        source_button = next(w for w in widgets(window)
                             if isinstance(w, ttk.Button) and w.cget('text') == 'Исходные данные')
        source_button.invoke()
        self.app.update()
        source_window = next(w for w in self.app.winfo_children()
                             if w.winfo_class() == 'Toplevel' and w is not window)
        source_grid = next(w for w in widgets(source_window) if isinstance(w, DataGrid))
        self.assertEqual(source_grid.rows[0][1:3], ['1', '4'])
        self.assertIs(self.app.lesson, lesson)
        self.assertEqual(self.app.accepted, history)
        self.assertEqual(self.app.screen, 'result')
        source_window.destroy()
        window.destroy()

    def test_rejected_source_attempts_count_through_result_and_reset_for_new_session(self):
        self.app.editor_grid.set_value(0, 1, '0')
        self.assertFalse(self.app.begin())
        self.assertFalse(self.app.begin())
        self.assertEqual(self.app.editor_errors, 2)
        self.app.zoom.set('140%')
        self.app.rescale()
        self.assertEqual(self.app.editor_errors, 2)
        self.app.editor_grid.set_value(0, 1, '1')
        self.assertTrue(self.app.begin())
        self.assertEqual(self.app.lesson.errors, 2)
        while self.app.lesson.phase in ('candidates', 'summary'):
            self.accept_table()
        for i in range(4):
            self.app.answer_grid.set_value(0, i + 1, i)
            self.app.answer_grid.set_value(1, i + 1, 1)
        self.assertTrue(self.app.check_answers())
        self.assertIn('Ошибки: 2', self.app.report_text())
        self.app.return_to_editor()
        self.assertEqual(self.app.editor_errors, 2)
        self.app.editor_grid.set_value(0, 1, '0')
        self.assertEqual(self.app.editor_errors, 0)
        self.assertFalse(self.app.begin())
        self.app.set_problem(PRESETS[0])
        self.assertEqual(self.app.editor_errors, 0)
        self.assertTrue(self.app.begin())
        self.assertEqual(self.app.lesson.errors, 0)

    def test_editor_utilities_do_not_count_as_failed_submission(self):
        self.app.editor_grid.set_value(0, 2, '-1')
        self.app.apply_limits()
        self.assertEqual(self.app.editor_errors, 0)
        with patch('app.messagebox.showerror'):
            self.app.save_file()
        self.assertEqual(self.app.editor_errors, 0)
        self.app.count_var.set('0')
        self.app.new_table()
        self.assertEqual(self.app.editor_errors, 0)

    def test_error_in_source_identifies_and_focuses_cell(self):
        for column, raw, label in [(1, '0', 'Вес груза 2'), (2, '-1', 'Лимит груза 2'),
                                    (5, 'nan', 'Груз 2, F(2)'), (5, '-1', 'Груз 2, F(2)')]:
            with self.subTest(column=column, raw=raw):
                self.app.set_problem(PRESETS[0])
                self.app.editor_grid.set_value(1, column, raw)
                self.assertFalse(self.app.begin())
                self.assertIn(label, self.app.message_var.get())
                self.assertEqual(self.app.editor_grid.invalid, {(1, column)})
                self.assertEqual(self.app.editor_grid.selected, (1, column))
                self.assertEqual(self.app.screen, 'editor')

    def test_zoom_keeps_distant_answer_visible_and_retains_value(self):
        self.app.set_problem(Problem('Большая', 200, (1, 1), ((0, 1), (0, 2))))
        self.app.begin()
        self.app.update()
        grid = self.app.answer_grid
        grid.set_value(150, 1, '123')
        grid.selected = (150, 1)
        grid._ensure_visible(150, 1)
        self.app.zoom.set('140%')
        self.app.rescale()
        self.app.update_idletasks()
        grid = self.app.answer_grid
        self.assertEqual(grid.selected, (150, 1))
        self.assertEqual(grid.rows[150][1], '123')
        top = grid.canvas.canvasy(0)
        y = grid.header_height + 150 * grid.row_height
        self.assertGreater(grid.canvas.yview()[0], 0.5)
        self.assertGreaterEqual(y, top + grid.header_height - 1)
        self.assertLessEqual(y + grid.row_height, top + grid.canvas.winfo_height() + 1)

    def test_zoom_keeps_distant_editor_cell_selected_and_visible(self):
        self.app.set_problem(Problem('Широкая', 200, (1,), (tuple(range(201)),)))
        self.app.update()
        grid = self.app.editor_grid
        grid.selected = (0, 180)
        grid._ensure_visible(0, 180)
        self.app.zoom.set('120%')
        self.app.rescale()
        grid = self.app.editor_grid
        self.assertEqual(grid.selected, (0, 180))
        self.assertGreater(grid.canvas.xview()[0], 0.5)
        self.assertEqual(self.app.read_problem().values[0][177], 177)

    def test_readonly_cell_and_table_can_be_copied(self):
        window = self.app.open_source()
        grid = next(w for w in widgets(window) if isinstance(w, DataGrid))
        # Native Windows mapping/clipboard messages need a full event cycle.
        # Select by clicking the displayed cell rather than mutating selection.
        window.lift()
        self.app.update()
        self.assertTrue(grid.canvas.winfo_ismapped())
        self.app.clipboard_clear()
        self.app.clipboard_append('before-copy')
        grid.canvas.focus_force()
        grid.canvas.event_generate('<Button-1>', x=grid.positions[4] + 10,
                                   y=grid.header_height + grid.row_height // 2)
        grid.canvas.event_generate('<ButtonRelease-1>', x=grid.positions[4] + 10,
                                   y=grid.header_height + grid.row_height // 2)
        self.app.update()
        self.assertEqual(grid.selected, (0, 4))
        shortcut = '<Command-c>' if self.app.tk.call('tk', 'windowingsystem') == 'aqua' else '<Control-c>'
        grid.canvas.event_generate(shortcut)
        self.app.update()
        self.assertEqual(self.app.clipboard_get(), '10')
        copy_button = next(w for w in widgets(window)
                           if isinstance(w, ttk.Button) and w.cget('text') == 'Копировать таблицу')
        copy_button.invoke()
        self.app.update()
        copied = self.app.clipboard_get()
        self.assertIn('F(1)', copied.splitlines()[0])
        self.assertIn('Предприятие 1\t1\t4\t0\t10\t17\t25\t36', copied)
        window.destroy()

    def test_small_window_preserves_actions_and_reference_at_all_phases(self):
        self.assertLessEqual(self.app.minsize()[0], 1024)
        self.assertLessEqual(self.app.minsize()[1], 700)
        self.app.zoom.set('140%')
        self.app.rescale()
        self.app.begin()
        for phase in ('candidates', 'summary', 'candidates'):
            self.app.update_idletasks()
            self.assertEqual(self.app.lesson.phase, phase)
            self.assertTrue(self.app.check_button.winfo_ismapped())
            self.assertGreaterEqual(self.app.check_button.winfo_width(), self.app.check_button.winfo_reqwidth())
            self.assertTrue(self.app.reference_notebook.winfo_ismapped())
            for grid in self.app.reference_grids:
                self.assertTrue(grid.winfo_ismapped())
                self.assertGreaterEqual(grid.canvas.winfo_height(), grid.header_height + grid.row_height)
            for label in (self.app.errors_label, self.app.hints_label):
                self.assertGreaterEqual(label.winfo_width(), label.winfo_reqwidth())
            self.accept_table()


if __name__ == '__main__':
    unittest.main()
