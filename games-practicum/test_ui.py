"""Tk widget construction/rendering checks, without mouse/keyboard injection."""
import unittest
import tkinter as tk
from fractions import Fraction as Q
from app import App
from lesson import Lesson
from variant_files import Game


EXAMPLE = Game(
    matrix=(('0.8', '0.2', '0.4'), ('0.4', '0.5', '0.6'), ('0.1', '0.7', '0.3')),
    row_labels=('А1', 'А2', 'А3'), col_labels=('В1', 'В2', 'В3'),
    name='Пример', description='Вооружение и помехи.')

SADDLE = Game(matrix=(('3', '4'), ('1', '2')), row_labels=('А1', 'А2'),
              col_labels=('B1', 'B2'), name='Седловая', description='')


def enter(entry, text):
    entry.delete(0, 'end')
    entry.insert(0, text)


class RenderingTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = App(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_no_saddle_full_path_with_hints_and_errors(self):
        app = self.app
        app.lesson = Lesson(EXAMPLE)
        app.show_lesson()
        self.root.update_idletasks()

        # --- alpha: wrong answer first, does not advance, does not reveal value.
        enter(app.answer_entry, '0')
        app.check()
        self.assertEqual(app.lesson.phase, 'alpha')
        self.assertEqual(app.lesson.errors, 1)
        self.assertNotIn('2/5', app.feedback)
        hints_before = app.lesson.hints
        app.hint_button.invoke()
        self.assertEqual(app.lesson.hints, hints_before + 1)
        self.assertIn('2/5', app.hint_label.cget('text'))
        enter(app.answer_entry, '2/5')
        app.check()
        self.assertEqual(app.lesson.phase, 'beta')
        self.assertEqual(app.lesson.errors, 1)

        # --- beta
        enter(app.answer_entry, '3/5')
        app.check()
        self.assertEqual(app.lesson.phase, 'saddle')

        # --- saddle: no saddle point in this matrix
        app.check(False)
        self.assertEqual(app.lesson.phase, 'solve')
        self.assertIsNone(app.hint_button)

        # --- solve: single action button, no judged answer
        app.check()
        self.assertEqual(app.lesson.phase, 'value')
        self.assertIsNotNone(app.lesson.solution)

        # --- value: wrong, then hint, then correct
        enter(app.answer_entry, '0')
        app.check()
        self.assertEqual(app.lesson.phase, 'value')
        self.assertEqual(app.lesson.errors, 2)
        app.hint_button.invoke()
        self.assertIn(str(app.lesson.solution.value), app.hint_label.cget('text'))
        enter(app.answer_entry, str(app.lesson.solution.value))
        app.check()
        self.assertEqual(app.lesson.phase, 'prob_a')
        self.assertEqual(app.lesson.value, Q(16, 35))

        # --- prob_a
        self.assertEqual(len(app.prob_entries), 3)
        for e, v in zip(app.prob_entries, app.lesson.solution.p):
            enter(e, str(v))
        app.check()
        self.assertEqual(app.lesson.phase, 'prob_b')

        # --- prob_b: wrong vector first
        self.assertEqual(len(app.prob_entries), 3)
        for e in app.prob_entries:
            enter(e, '0')
        app.check()
        self.assertEqual(app.lesson.phase, 'prob_b')
        self.assertEqual(app.lesson.errors, 3)
        for e, v in zip(app.prob_entries, app.lesson.solution.q):
            enter(e, str(v))
        app.check()
        self.assertEqual(app.lesson.phase, 'done')
        self.assertEqual(app.lesson.errors, 3)

        # --- done screen shows the final summary; a fresh setup resets cleanly.
        summary_texts = [w.cget('text') for w in app.question.winfo_children()
                          if isinstance(w, tk.Label) and 'ν = ' in w.cget('text')]
        self.assertTrue(any('16/35' in text for text in summary_texts))
        app._setup()
        self.root.update_idletasks()
        self.assertIsNone(app.lesson)

    def test_saddle_point_path(self):
        app = self.app
        app.lesson = Lesson(SADDLE)
        app.show_lesson()
        self.root.update_idletasks()
        self.assertTrue(app.lesson.saddle.exists)

        enter(app.answer_entry, '3')
        app.check()
        self.assertEqual(app.lesson.phase, 'beta')
        enter(app.answer_entry, '3')
        app.check()
        self.assertEqual(app.lesson.phase, 'saddle')

        app.check(True)
        self.assertEqual(app.lesson.phase, 'pure')

        self.assertEqual(app.row_combo.get(), '1')
        self.assertEqual(app.col_combo.get(), '1')
        app.check()
        self.assertEqual(app.lesson.phase, 'done')
        self.assertEqual(app.lesson.value, Q(3))
        self.assertEqual(app.lesson.errors, 0)

    def test_wrong_saddle_answer_is_rejected(self):
        app = self.app
        app.lesson = Lesson(SADDLE)
        app.show_lesson()
        enter(app.answer_entry, '3')
        app.check()
        enter(app.answer_entry, '3')
        app.check()
        self.assertEqual(app.lesson.phase, 'saddle')
        app.check(False)
        self.assertEqual(app.lesson.phase, 'saddle')
        self.assertEqual(app.lesson.errors, 1)

    def test_custom_dimensions_round_trip_into_lesson(self):
        app = self.app
        app.rows.set('2')
        app.cols.set('2')
        app.create_empty()
        self.root.update_idletasks()
        for row in app.cell_entries:
            for e in row:
                enter(e, '1')
        app.start()
        self.root.update_idletasks()
        self.assertIsNotNone(app.lesson)
        self.assertEqual(app.lesson.matrix, ((Q(1), Q(1)), (Q(1), Q(1))))


if __name__ == '__main__':
    unittest.main()
