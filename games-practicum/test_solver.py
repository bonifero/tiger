import random
import unittest
from fractions import Fraction as Q
from solver import number, saddle_point, solve_lp, solve_mixed


def check_equilibrium(test, matrix, solution):
    m, n = len(matrix), len(matrix[0])
    test.assertEqual(sum(solution.p), 1)
    test.assertEqual(sum(solution.q), 1)
    test.assertTrue(all(v >= 0 for v in solution.p))
    test.assertTrue(all(v >= 0 for v in solution.q))
    for j in range(n):
        test.assertGreaterEqual(sum(solution.p[i] * matrix[i][j] for i in range(m)), solution.value)
    for i in range(m):
        test.assertLessEqual(sum(solution.q[j] * matrix[i][j] for j in range(n)), solution.value)


class NumberTests(unittest.TestCase):
    def test_parsing(self):
        self.assertEqual(number('0.8'), Q(4, 5))
        self.assertEqual(number('2,5'), Q(5, 2))
        self.assertEqual(number('-3'), Q(-3))
        self.assertEqual(number('1/3'), Q(1, 3))
        self.assertEqual(number('-3 2/5'), -Q(17, 5))
        self.assertEqual(number(2), Q(2))

    def test_garbage(self):
        with self.assertRaises(ValueError):
            number('abc')
        with self.assertRaises(ValueError):
            number('1/0')


class SaddleTests(unittest.TestCase):
    def test_no_saddle(self):
        matrix = tuple(tuple(number(v) for v in row) for row in
                        [['0.8', '0.2', '0.4'], ['0.4', '0.5', '0.6'], ['0.1', '0.7', '0.3']])
        s = saddle_point(matrix)
        self.assertEqual(s.alpha, Q(2, 5))
        self.assertEqual(s.beta, Q(3, 5))
        self.assertFalse(s.exists)

    def test_saddle_exists(self):
        matrix = (
            (Q(4), Q(3), Q(2)),
            (Q(5), Q(4), Q(1)),
            (Q(2), Q(0), Q(-1)),
        )
        # Row mins: 2,1,-1 -> alpha=2 at row 0. Col maxs: 5,4,2 -> beta=2 at col 2.
        s = saddle_point(matrix)
        self.assertTrue(s.exists)
        self.assertEqual(s.alpha, Q(2))
        self.assertEqual(s.beta, Q(2))
        self.assertEqual(s.rows, (0,))
        self.assertEqual(s.cols, (2,))


class SolveLpTests(unittest.TestCase):
    def test_trivial_le(self):
        status, x, obj = solve_lp((Q(1),), ((Q(1),),), (Q(5),), ('<=',), 'max')
        self.assertEqual((status, x, obj), ('optimal', (Q(5),), Q(5)))

    def test_phase_one_ge(self):
        # min x1+x2 s.t. x1+2x2>=4, 3x1+x2>=6, x>=0
        status, x, obj = solve_lp(
            (Q(1), Q(1)), ((Q(1), Q(2)), (Q(3), Q(1))), (Q(4), Q(6)), ('>=', '>='), 'min')
        self.assertEqual(status, 'optimal')
        self.assertEqual(obj, Q(14, 5))
        self.assertEqual(x, (Q(8, 5), Q(6, 5)))

    def test_infeasible(self):
        status, x, obj = solve_lp(
            (Q(1),), ((Q(1),), (Q(-1),)), (Q(1), Q(-2)), ('<=', '<='), 'max')
        self.assertEqual((status, x, obj), ('infeasible', (), None))

    def test_unbounded(self):
        status, x, obj = solve_lp((Q(1),), ((Q(-1),),), (Q(0),), ('<=',), 'max')
        self.assertEqual((status, x, obj), ('unbounded', (), None))


class SolveMixedTests(unittest.TestCase):
    def test_textbook_example(self):
        matrix = tuple(tuple(number(v) for v in row) for row in
                        [['0.8', '0.2', '0.4'], ['0.4', '0.5', '0.6'], ['0.1', '0.7', '0.3']])
        s = saddle_point(matrix)
        self.assertFalse(s.exists)
        solution = solve_mixed(matrix)
        self.assertEqual(solution.value, Q(16, 35))
        self.assertEqual(solution.p, (Q(1, 7), Q(6, 7), Q(0)))
        self.assertEqual(solution.q, (Q(3, 7), Q(4, 7), Q(0)))
        self.assertEqual(solution.shift, 0)
        check_equilibrium(self, matrix, solution)

    def test_rock_paper_scissors(self):
        matrix = ((Q(0), Q(1), Q(-1)), (Q(-1), Q(0), Q(1)), (Q(1), Q(-1), Q(0)))
        solution = solve_mixed(matrix)
        self.assertGreater(solution.shift, 0)
        self.assertEqual(solution.shift, 2)
        self.assertEqual(solution.value, 0)
        third = (Q(1, 3), Q(1, 3), Q(1, 3))
        self.assertEqual(solution.p, third)
        self.assertEqual(solution.q, third)
        check_equilibrium(self, matrix, solution)

    def test_random_sweep(self):
        rng = random.Random(42)
        for _ in range(40):
            m, n = rng.randint(2, 5), rng.randint(2, 5)
            matrix = tuple(tuple(Q(rng.randint(-6, 6), rng.choice([1, 2, 3])) for _ in range(n))
                            for _ in range(m))
            solution = solve_mixed(matrix)
            check_equilibrium(self, matrix, solution)


if __name__ == '__main__':
    unittest.main()
