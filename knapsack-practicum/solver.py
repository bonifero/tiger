"""Backward Bellman tables and exact optimal-plan reconstruction."""
from dataclasses import dataclass
from fractions import Fraction

from model import Problem


@dataclass(frozen=True)
class Stage:
    index: int
    states: tuple
    candidates: dict
    best: dict
    choices: dict


@dataclass(frozen=True)
class Solution:
    objective: Fraction
    plan: tuple
    used: int
    stages: tuple


def solve(problem: Problem) -> Solution:
    """Solve sum F_j(x_j) -> max, sum a_j*x_j <= B, 0<=x_j<=q_j.

    State y is capacity already used before item j. Stages proceed from the
    last item to the first. Only y=0 is needed for the first item.
    """
    following = {y: Fraction(0) for y in range(problem.capacity + 1)}
    stages = []
    for j in reversed(range(len(problem.weights))):
        states = (0,) if j == 0 else tuple(range(problem.capacity + 1))
        candidates, best, choices = {}, {}, {}
        for y in states:
            row = tuple(
                value + following[y + problem.weights[j] * x]
                if y + problem.weights[j] * x <= problem.capacity else None
                for x, value in enumerate(problem.values[j])
            )
            optimum = max(value for value in row if value is not None)
            candidates[y] = row
            best[y] = optimum
            choices[y] = tuple(x for x, value in enumerate(row) if value == optimum)
        stages.append(Stage(j, states, candidates, best, choices))
        following = best
    used, plan = 0, []
    for stage in reversed(stages):
        quantity = stage.choices[used][0]
        plan.append(quantity)
        used += problem.weights[stage.index] * quantity
    return Solution(stages[-1].best[0], tuple(plan), used, tuple(stages))
