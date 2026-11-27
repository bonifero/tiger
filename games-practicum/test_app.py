"""Startup regression: Tk window, variant catalogue and the setup → lesson transition."""
import unittest
import tkinter as tk
from app import App
from presets import PRESETS


class StartupTests(unittest.TestCase):
    def test_setup_loads_presets_and_starts_lesson(self):
        root = tk.Tk()
        root.withdraw()
        try:
            app = App(root)
            root.update_idletasks()
            self.assertIsNone(app.lesson)
            self.assertEqual(set(app.variants), set(PRESETS))
            app.start()
            root.update_idletasks()
            self.assertIsNotNone(app.lesson)
            self.assertEqual(app.lesson.phase, 'alpha')
        finally:
            root.destroy()

    def test_custom_table_dimensions(self):
        root = tk.Tk()
        root.withdraw()
        try:
            app = App(root)
            app.rows.set('4')
            app.cols.set('5')
            app.create_empty()
            root.update_idletasks()
            self.assertEqual(app.edit_shape, (4, 5))
            self.assertEqual(len(app.row_entries), 4)
            self.assertEqual(len(app.col_entries), 5)
        finally:
            root.destroy()


if __name__ == '__main__':
    unittest.main()
