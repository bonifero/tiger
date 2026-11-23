"""Student workflow regressions, including alternative optimal answers."""
import unittest

from lesson import Lesson
from model import Problem


def complete_tables(lesson, last_choice=False):
    while lesson.phase in ("candidates", "summary"):
        stage = lesson.current_stage
        if lesson.phase == "candidates":
            rows = {y: [None if x is None else str(x) for x in row]
                    for y, row in stage.candidates.items()}
            assert lesson.submit_candidates(rows).accepted
        rows = {y: (str(stage.best[y]), str(stage.choices[y][-1 if last_choice else 0]))
                for y in stage.states}
        assert lesson.submit_summary(rows).accepted


class LessonTests(unittest.TestCase):
    def setUp(self):
        self.problem = Problem("Ничьи", 2, (1, 1), ((0, 1, 2), (0, 1, 2)))

    def test_all_equal_optima_accepted(self):
        for plan in ((0, 2), (1, 1), (2, 0)):
            lesson = Lesson(self.problem)
            complete_tables(lesson, last_choice=True)
            self.assertEqual(lesson.phase, "restore")
            self.assertTrue(lesson.submit_plan(list(map(str, plan))).accepted)
            self.assertEqual(lesson.accepted_plan, plan)
            self.assertEqual(lesson.phase, "done")
            self.assertEqual(lesson.errors, 0)

    def test_wrong_values_never_advance_or_destroy_answers(self):
        lesson = Lesson(self.problem)
        stage = lesson.current_stage
        rows = {y: list(row) for y, row in stage.candidates.items()}
        rows[0][1] = "10"
        feedback = lesson.submit_candidates(rows)
        self.assertFalse(feedback.accepted)
        self.assertEqual(feedback.invalid, ((0, 1),))
        self.assertEqual((lesson.stage_index, lesson.phase, lesson.errors), (0, "candidates", 1))
        self.assertEqual(lesson.history, [])
        rows[0][1] = ""
        self.assertFalse(lesson.submit_candidates(rows).accepted)
        rows[0][1] = "1"
        rows[2][2] = "0"
        self.assertEqual(lesson.submit_candidates(rows).invalid, ((2, 2),))
        rows[2][2] = None
        self.assertTrue(lesson.submit_candidates(rows).accepted)
        self.assertEqual(lesson.phase, "summary")
        self.assertEqual(lesson.errors, 3)

    def test_summary_checks_maximum_and_integer_argmax(self):
        lesson = Lesson(self.problem)
        stage = lesson.current_stage
        lesson.submit_candidates(stage.candidates)
        rows = {y: (stage.best[y], stage.choices[y][0]) for y in stage.states}
        rows[0] = ("999", "0.5")
        feedback = lesson.submit_summary(rows)
        self.assertEqual(feedback.invalid, ((0, 0), (0, 1)))
        self.assertEqual((lesson.stage_index, lesson.phase), (0, "summary"))
        self.assertEqual(lesson.accepted_summaries, {})
        rows[0] = (2, 2)
        self.assertTrue(lesson.submit_summary(rows).accepted)
        self.assertEqual((lesson.stage_index, lesson.phase), (1, "candidates"))
        self.assertEqual(lesson.accepted_summaries[1][0], (2, 2))

    def test_restoration_rejects_invalid_and_suboptimal_plans(self):
        lesson = Lesson(self.problem)
        complete_tables(lesson)
        for plan in ((1,), (-1, 2), (True, 1), (0.5, 1), (3, 0), (2, 2), (0, 0)):
            with self.subTest(plan=plan):
                self.assertFalse(lesson.submit_plan(plan).accepted)
                self.assertEqual(lesson.phase, "restore")
                self.assertIsNone(lesson.accepted_plan)
        self.assertEqual(lesson.errors, 7)
        self.assertTrue(lesson.submit_plan((1, 1)).accepted)

    def test_shape_mismatch_and_wrong_phase(self):
        lesson = Lesson(self.problem)
        self.assertFalse(lesson.submit_plan((1, 1)).accepted)
        self.assertEqual(lesson.errors, 0)
        self.assertFalse(lesson.submit_candidates({0: [0, 1, 2]}).accepted)
        rows = dict(lesson.current_stage.candidates)
        rows[0] = rows[0][:-1]
        self.assertEqual(lesson.submit_candidates(rows).invalid, ((0, -1),))

    def test_hints_are_counted_without_advancing(self):
        lesson = Lesson(self.problem)
        self.assertIn("последнего", lesson.hint())
        self.assertEqual((lesson.hints, lesson.errors, lesson.phase), (1, 0, "candidates"))
        lesson.submit_candidates(lesson.current_stage.candidates)
        self.assertIn("максимумах", lesson.hint())
        complete_tables(lesson)
        self.assertIn("y₁", lesson.hint())
        self.assertEqual(lesson.hints, 3)

    def test_answer_fractions_can_be_larger_than_each_input(self):
        # Coprime odd denominators force a result larger than 256 bits.
        p = Problem("Точные дроби", 2, (1, 1),
                    ((0, f"1/{2**200 - 1}"), (0, f"1/{2**199 - 1}")))
        lesson = Lesson(p)
        self.assertGreater(lesson.solution.objective.denominator.bit_length(), 256)
        complete_tables(lesson)
        self.assertTrue(lesson.submit_plan((1, 1)).accepted)

    def test_restoration_requires_states_matching_the_actual_alternative(self):
        for plan, states in (((0, 2), (0, 0)), ((1, 1), (0, 1)), ((2, 0), (0, 2))):
            with self.subTest(plan=plan):
                lesson = Lesson(self.problem)
                complete_tables(lesson, last_choice=True)
                feedback = lesson.submit_plan(plan, states)
                self.assertTrue(feedback.accepted)
                self.assertEqual(lesson.accepted_plan, plan)
                self.assertEqual(lesson.accepted_states, states)

    def test_wrong_states_do_not_advance_or_publish_accepted_plan(self):
        lesson = Lesson(self.problem)
        complete_tables(lesson)
        cases = [((1, 1), ((1, 0),)), ((0, 0), ((1, 1),)),
                 ((0, -1), ((1, 1),)), ((0, "1/2"), ((1, 1),)),
                 ((True, 1), ((1, 0),)), ((0,), ((1, 0), (1, 1))),
                 ("0,1", ((1, 0), (1, 1)))]
        for attempt, (states, invalid) in enumerate(cases, 1):
            with self.subTest(states=states):
                feedback = lesson.submit_plan((1, 1), states)
                self.assertFalse(feedback.accepted)
                self.assertEqual(feedback.invalid, invalid)
                self.assertEqual(lesson.errors, attempt)
                self.assertEqual(lesson.phase, "restore")
                self.assertIsNone(lesson.accepted_plan)
                self.assertIsNone(lesson.accepted_states)
        self.assertTrue(lesson.submit_plan((1, 1), ("0", "1")).accepted)

    def test_states_use_weighted_resource_and_legacy_call_computes_them(self):
        problem = Problem("Веса", 5, (2, 1), ((0, 5, 10), (0, 1)))
        lesson = Lesson(problem)
        complete_tables(lesson)
        self.assertEqual(lesson.submit_plan((2, 1), (0, 2)).invalid, ((1, 1),))
        self.assertTrue(lesson.submit_plan((2, 1)).accepted)
        self.assertEqual(lesson.accepted_states, (0, 4))


if __name__ == "__main__":
    unittest.main()
