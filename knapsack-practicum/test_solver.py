"""Independent enumeration checks for the exact Bellman solver."""
from fractions import Fraction as Q
from itertools import product
import random
import unittest

from model import Problem, parse_number, fmt_number
from solver import solve


def enumerate_optima(problem, start=0, already_used=0):
    best, plans = None, []
    ranges = [range(len(row)) for row in problem.values[start:]]
    for plan in product(*ranges):
        if already_used + sum(w * x for w, x in zip(problem.weights[start:], plan)) > problem.capacity:
            continue
        value = sum(row[x] for row, x in zip(problem.values[start:], plan))
        if best is None or value > best:
            best, plans = value, [plan]
        elif value == best:
            plans.append(plan)
    return best, plans


class SolverTests(unittest.TestCase):
    def test_manual_example_and_ties(self):
        p = Problem("Капитал", 4, (1, 1, 1, 1), (
            (0, 10, 17, 25, 36), (0, 11, 16, 25, 35),
            (0, 10, 18, 24, 34), (0, 9, 19, 26, 35)))
        answer = solve(p)
        self.assertEqual(answer.objective, 40)
        self.assertEqual(answer.plan, (0, 1, 1, 2))
        self.assertEqual(answer.stages[-1].choices[0], (0, 1))
        self.assertEqual(answer.stages[-1].states, (0,))
        self.assertEqual(answer.stages[0].candidates[3], (Q(0), Q(9), None, None, None))

    def test_random_models_and_every_suffix_against_enumeration(self):
        rng = random.Random(8124)
        for case in range(220):
            n, capacity = rng.randint(1, 4), rng.randint(1, 9)
            weights = tuple(rng.randint(1, 7) for _ in range(n))
            values = tuple(tuple([0] + [Q(rng.randint(0, 35), rng.randint(1, 5))
                                       for _ in range(rng.randint(0, 4))]) for _ in range(n))
            p = Problem(str(case), capacity, weights, values)
            answer = solve(p)
            expected, plans = enumerate_optima(p)
            with self.subTest(case=case):
                self.assertEqual(answer.objective, expected)
                self.assertIn(answer.plan, plans)
                self.assertEqual(answer.used, sum(w * x for w, x in zip(weights, answer.plan)))
                for stage in answer.stages:
                    for y in stage.states:
                        best, suffixes = enumerate_optima(p, stage.index, y)
                        self.assertEqual(stage.best[y], best)
                        self.assertEqual(set(stage.choices[y]), {suffix[0] for suffix in suffixes})

    def test_unused_capacity_zero_quantity_and_unavailable_items(self):
        p = Problem("Не всё помещается", 5, (2, 10, 1), ((0, 9, 7), (0, 100), (0,)))
        answer = solve(p)
        self.assertEqual((answer.plan, answer.used, answer.objective), ((1, 0, 0), 2, 9))
        self.assertEqual(solve(Problem("Ничего", 1, (2,), ((0, 5),))).objective, 0)

    def test_exact_numeric_input(self):
        self.assertEqual(parse_number(" 0,125 "), Q(1, 8))
        self.assertEqual(parse_number("2/3"), Q(2, 3))
        self.assertEqual(parse_number(0.1), Q(1, 10))
        self.assertEqual(fmt_number(Q(12, 5)), "12/5")
        for value in (True, None, "", "nan", "Infinity", "1/0", float("nan"), float("inf"), [], "2" * 2601):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_number(value)

    def test_model_validation(self):
        valid = dict(name="Задача", capacity=3, weights=(1, 2), values=((0, 1), (0, 2)))
        bad = [dict(capacity=0), dict(capacity=201), dict(capacity=True), dict(capacity="3"),
               dict(weights=(0, 1)), dict(weights=(True, 2)), dict(weights=(1.5, 2)),
               dict(weights=()), dict(weights=None), dict(values=((1, 2), (0, 1))),
               dict(values=((0, -1), (0, 1))), dict(values=((0, True), (0, 1))),
               dict(values=((0, None), (0, 1))), dict(values=((0, 1),)),
               dict(values=((0, "nan"), (0, 1))), dict(labels=("А",)),
               dict(labels=("А", "")), dict(description=None), dict(name=" ")]
        for change in bad:
            with self.subTest(change=change), self.assertRaises(ValueError):
                Problem(**(valid | change))

    def test_exponent_is_bounded_before_fraction_expansion(self):
        for value in ("1e999999999", "1e-999999999", "1e1201", "1e-1201",
                      "1e" + "9" * 2500):
            with self.subTest(value=value[:40]), self.assertRaisesRegex(ValueError, "Показатель"):
                parse_number(value)
        self.assertEqual(parse_number("1e-1200"), Q(1, 10**1200))
        self.assertEqual(parse_number("1e+1200"), 10**1200)
        self.assertEqual(parse_number("1e" + "0" * 2500), 1)
        for value in ("1e1_201", "1e1_0", "1_000", "1/1_000"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "подчёркивания"):
                parse_number(value)

    def test_resource_budget(self):
        with self.assertRaisesRegex(ValueError, "ячеек"):
            Problem("Слишком большая", 200, (1,) * 12, ((0,) * 201,) * 12)
        # At the supported maximum capacity, one stage still needs one row.
        answer = solve(Problem("Большая", 200, (1,), (tuple(range(201)),)))
        self.assertEqual((answer.objective, answer.plan), (200, (200,)))


if __name__ == "__main__":
    unittest.main()
