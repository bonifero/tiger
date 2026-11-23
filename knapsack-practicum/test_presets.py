"""Manual fixtures and an independent exhaustive oracle for every preset."""
import itertools
import unittest
from pathlib import Path
from presets import PRESETS
from solver import solve
from formats import load


class PresetTests(unittest.TestCase):
    def test_all_manual_optima_and_alternatives(self):
        expected = [
            (40, {(0, 1, 1, 2), (1, 1, 0, 2), (1, 1, 1, 1)}),
            (21, {(2, 0, 1), (2, 2, 0), (3, 1, 0)}),
            (34, {(1, 0, 0, 1)}), (3400, {(1, 2)}),
            (2500, {(5, 0, 0)}), (320, {(2, 0, 1)}),
        ]
        for problem, (objective, plans) in zip(PRESETS, expected):
            with self.subTest(problem=problem.name):
                feasible = [(sum(row[x] for row, x in zip(problem.values, plan)), plan)
                            for plan in itertools.product(*(range(len(row)) for row in problem.values))
                            if sum(w*x for w, x in zip(problem.weights, plan)) <= problem.capacity]
                best = max(v for v, _ in feasible)
                self.assertEqual(best, objective)
                self.assertEqual({p for v, p in feasible if v == best}, plans)
                solution = solve(problem)
                self.assertEqual(solution.objective, objective)
                self.assertIn(solution.plan, plans)
        self.assertEqual(solve(PRESETS[3]).used, 5)

    def test_manual_example_intermediate_tables(self):
        stages = solve(PRESETS[0]).stages
        self.assertEqual(list(stages[0].best.values()), [35, 26, 19, 9, 0])
        self.assertEqual(list(stages[1].best.values()), [37, 29, 19, 10, 0])
        self.assertEqual(stages[1].choices[2], (0, 1))
        self.assertEqual(list(stages[2].best.values()), [40, 30, 21, 11, 0])
        self.assertEqual(stages[3].candidates[0], (40, 40, 38, 36, 36))
        self.assertEqual(stages[3].choices[0], (0, 1))

    def test_distributed_json_matches_presets(self):
        folder = Path(__file__).parent / 'variants'
        paths = [folder / 'example.json'] + [folder / f'variant-{i}.json' for i in range(1, 6)]
        self.assertEqual([load(path) for path in paths], PRESETS)


if __name__ == '__main__':
    unittest.main()
