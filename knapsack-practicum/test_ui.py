"""End-to-end Tk teaching workflow, including retained inputs and alternate optima."""
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

from app import App, DataGrid
from model import Problem, fmt_number
from presets import PRESETS


class InterfaceTests(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.withdraw()
        self.app.update_idletasks()

    def tearDown(self):
        self.app.destroy()

    def complete_tables(self):
        while self.app.lesson.phase in ('candidates', 'summary'):
            stage = self.app.lesson.current_stage
            grid = self.app.answer_grid
            if self.app.lesson.phase == 'candidates':
                for r, y in enumerate(stage.states):
                    for x, value in enumerate(stage.candidates[y]):
                        if value is not None:
                            grid.set_value(r, x + 1, fmt_number(value))
            else:
                for r, y in enumerate(stage.states):
                    grid.set_value(r, 1, fmt_number(stage.best[y]))
                    grid.set_value(r, 2, stage.choices[y][0])
            self.assertTrue(self.app.check_answers())

    def test_editor_roundtrip_and_ragged_limits(self):
        self.app.set_problem(PRESETS[4])
        self.assertEqual(self.app.read_problem(), PRESETS[4])
        grid = self.app.editor_grid
        grid.set_value(1, 2, 2)
        self.app.apply_limits()
        self.app.editor_grid.set_value(1, 5, '2000')
        p = self.app.read_problem()
        self.assertEqual(len(p.values[1]), 3)
        self.assertEqual(p.values[1][-1], 2000)
        self.app.zoom.set('140%')
        self.app.rescale()
        self.assertEqual(self.app.read_problem(), p)
        self.assertEqual(self.app.table_font_size, 15)

    def test_error_keeps_input_and_step_rescale_keeps_input(self):
        self.assertTrue(self.app.begin())
        grid = self.app.answer_grid
        grid.set_value(0, 1, '1234')
        self.assertFalse(self.app.check_answers())
        self.assertEqual(self.app.lesson.phase, 'candidates')
        self.assertEqual(self.app.lesson.errors, 1)
        self.assertEqual(grid.rows[0][1], '1234')
        self.assertIn((0, 1), grid.invalid)
        self.app.nav_buttons[1].invoke()
        self.assertEqual(self.app.answer_grid.rows[0][1], '1234')
        self.assertIs(self.app.answer_grid, grid)
        self.app.zoom.set('120%')
        self.app.rescale()
        self.assertEqual(self.app.answer_grid.rows[0][1], '1234')
        self.assertIn((0, 1), self.app.answer_grid.invalid)
        self.assertEqual(self.app.message_label.cget('fg'), '#bf3946')
        self.app.show_hint()
        self.assertEqual(self.app.lesson.hints, 1)
        self.assertTrue(self.app.hint_var.get())

    def test_full_workflow_accepts_alternate_optimum_with_states(self):
        self.app.set_problem(PRESETS[0])
        self.assertTrue(self.app.begin())
        self.complete_tables()
        self.assertEqual(self.app.lesson.phase, 'restore')
        self.assertEqual(len(self.app.accepted), 2 * len(PRESETS[0].weights))
        # The canonical sequence chosen in summary tables differs from this optimum.
        plan, states = (1, 1, 1, 1), (0, 1, 2, 3)
        for i, x in enumerate(plan):
            self.app.answer_grid.set_value(1, i + 1, x)
            self.app.answer_grid.set_value(0, i + 1, states[i])
        self.app.answer_grid.set_value(0, 3, 99)
        self.assertFalse(self.app.check_answers())
        self.assertIn((0, 3), self.app.answer_grid.invalid)
        self.app.answer_grid.set_value(0, 3, states[2])
        self.assertTrue(self.app.check_answers())
        self.assertEqual(self.app.screen, 'result')
        self.assertEqual(self.app.final_plan, plan)
        self.assertEqual(self.app.lesson.accepted_states, states)
        report = self.app.report_text()
        self.assertIn('Максимальная ценность: 40', report)
        self.assertIn('Ошибки: 1', report)
        self.assertIn('y=2, x=1', report)
        self.assertIn('Принятые шаги', report)
        window = self.app.open_summary_sheet()
        window.destroy()

    def test_underfilled_plan_and_export(self):
        self.app.set_problem(PRESETS[3])
        self.assertTrue(self.app.begin())
        self.complete_tables()
        for i, (x, y) in enumerate(zip((1, 2), (0, 3))):
            self.app.answer_grid.set_value(0, i + 1, y)
            self.app.answer_grid.set_value(1, i + 1, x)
        self.assertTrue(self.app.check_answers())
        self.assertIn('Свободный ресурс: 1', self.app.report_text())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'report.txt'
            with patch('app.filedialog.asksaveasfilename', return_value=str(path)):
                self.app.export_report()
            self.assertIn('3400', path.read_text(encoding='utf-8'))

    def test_failed_import_preserves_edited_problem(self):
        self.app.editor_grid.set_value(0, 4, '31/2')
        before = self.app.read_problem()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid.json'
            path.write_text('{}', encoding='utf-8')
            with patch('app.filedialog.askopenfilename', return_value=str(path)), \
                 patch('app.messagebox.showerror') as error:
                self.app.open_file()
                error.assert_called_once()
        self.assertEqual(self.app.read_problem(), before)

    def test_review_contains_only_accepted_tables(self):
        self.app.begin()
        self.assertEqual(self.app.accepted, [])
        self.assertEqual(self.app.review_list.size(), 0)
        source = self.app.open_source()
        source.destroy()
        self.assertIsNone(self.app.open_review(0))
        stage = self.app.lesson.current_stage
        for r, y in enumerate(stage.states):
            for x, value in enumerate(stage.candidates[y]):
                if value is not None:
                    self.app.answer_grid.set_value(r, x + 1, value)
        self.app.check_answers()
        self.assertEqual(self.app.lesson.phase, 'summary')
        self.assertEqual(self.app.review_list.size(), 1)
        self.assertEqual(self.app.accepted[0]['phase'], 'candidates')

    def test_tab_and_tsv_paste_respect_read_only_cells(self):
        grid = self.app.editor_grid
        grid.selected = (0, 3)  # F(0) is immutable.
        self.app.clipboard_clear()
        self.app.clipboard_append('999')
        grid._paste()
        self.assertEqual(grid.rows[0][3], '0')
        grid.selected = (0, 4)
        self.app.clipboard_clear()
        self.app.clipboard_append('1/2\t17\n11\t16')
        grid._paste()
        self.assertEqual(grid.rows[0][4:6], ['1/2', '17'])
        self.assertEqual(grid.rows[1][4:6], ['11', '16'])
        grid._next_editable(1)
        self.assertEqual(grid.selected, (0, 5))
        grid._start_edit()
        grid.entry.delete(0, 'end')
        grid.entry.insert(0, '9/2')
        grid.commit()
        self.assertEqual(grid.rows[0][5], '9/2')

    def test_compact_window_keeps_three_editor_rows_at_140_percent(self):
        self.app.geometry('1100x740')
        self.app.deiconify()
        self.app.update()
        self.app._apply_compact_layout()
        self.app.zoom.set('140%')
        self.app.rescale()
        self.app.update_idletasks()
        grid = self.app.editor_grid
        self.assertGreaterEqual(grid.canvas.winfo_height(),
                                grid.header_height + 3 * grid.row_height)
        self.assertEqual(self.app.read_problem(), PRESETS[0])
        self.app.editor_grid.set_value(0, 4, '31/2')
        self.app.compact = False
        self.app._apply_compact_layout()
        self.assertEqual(self.app.read_problem().values[0][1], Fraction(31, 2))
        self.assertTrue(self.app.begin())
        self.app.update_idletasks()
        self.assertTrue(self.app.check_button.winfo_ismapped())
        self.assertGreater(self.app.check_button.winfo_width(), 100)

    def test_stale_focus_event_does_not_commit_replacement_editor(self):
        from types import SimpleNamespace
        grid = self.app.editor_grid
        grid.selected = (0, 4)
        grid._start_edit()
        previous = grid.entry
        grid._next_editable(1, editing=True)
        current = grid.entry
        current.delete(0, 'end')
        current.insert(0, '123')
        grid._focus_out(SimpleNamespace(widget=previous))
        self.assertIs(grid.entry, current)
        self.assertEqual(grid.rows[0][5], '17')
        grid.commit()
        self.assertEqual(grid.rows[0][5], '123')

    def test_destroy_before_idle_does_not_leave_background_errors(self):
        errors = []
        self.app.tk.createcommand('bgerror', errors.append)
        grid = DataGrid(self.app, ['x'], [['0']])
        grid.destroy()
        self.app.update()
        self.assertEqual(errors, [])

    def test_large_grid_draws_only_viewport(self):
        window = self.app.open_source()
        window.destroy()
        host = __import__('tkinter').Toplevel(self.app)
        host.geometry('800x450')
        grid = DataGrid(host, [str(i) for i in range(201)],
                        [['0'] * 201 for _ in range(201)],
                        editable={(r, c) for r in range(201) for c in range(201)})
        grid.pack(fill='both', expand=True)
        host.update_idletasks()
        self.assertLess(len(grid.canvas.find_all()), 1000)
        grid.selected = (199, 199)
        grid._start_edit()
        self.assertIsNotNone(grid.entry)
        self.assertLess(len(grid.canvas.find_all()), 1000)
        host.destroy()


if __name__ == '__main__':
    unittest.main()
