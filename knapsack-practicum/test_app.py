"""Проверка запуска стартового окна на Windows с Tkinter."""
import tkinter as tk
from tkinter import ttk
import unittest

from app import create_window, TITLE, DESCRIPTION, STATUS


class StartupTests(unittest.TestCase):
    def test_window_and_close_button(self):
        root = create_window()
        try:
            root.withdraw()
            root.update_idletasks()
            self.assertEqual(root.title(), TITLE)
            frame, = root.winfo_children()
            labels = [child.cget("text") for child in frame.winfo_children()
                      if isinstance(child, ttk.Label)]
            self.assertEqual(labels, [DESCRIPTION, STATUS])
            button, = [child for child in frame.winfo_children()
                       if isinstance(child, ttk.Button)]
            button.invoke()
            with self.assertRaises(tk.TclError):
                root.winfo_exists()
        finally:
            try:
                root.destroy()
            except tk.TclError:
                pass


if __name__ == "__main__":
    unittest.main()
