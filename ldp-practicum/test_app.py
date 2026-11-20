"""Startup regression for the implemented LP workbench."""
import unittest
from app import App

class StartupTests(unittest.TestCase):
    def test_editor_and_pages(self):
        root=App()
        try:
            root.withdraw();root.update_idletasks()
            self.assertEqual(len(root.tabs.tabs()),4)
            self.assertEqual(root.read_problem().c,root.problem.c)
            self.assertFalse(root.running)
        finally:
            root.stop();root.destroy()

if __name__=='__main__':unittest.main()
