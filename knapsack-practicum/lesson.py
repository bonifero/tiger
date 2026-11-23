"""Teaching state machine; only accepted answers advance the lesson."""
from dataclasses import dataclass

from model import parse_number
from solver import solve


@dataclass(frozen=True)
class Feedback:
    accepted: bool
    message: str
    invalid: tuple = ()


class Lesson:
    def __init__(self, problem):
        self.problem = problem
        self.solution = solve(problem)
        self.stage_index = 0
        self.phase = "candidates"
        self.errors = 0
        self.hints = 0
        self.history = []
        self.accepted_plan = None
        self.accepted_states = None
        self.accepted_summaries = {}

    @property
    def current_stage(self):
        return self.solution.stages[self.stage_index]

    def _wrong(self, invalid=()):
        self.errors += 1
        return Feedback(False, "Ответ неверный. Проверьте отмеченные поля. Пояснение доступно по кнопке «Подсказка».", tuple(invalid))

    @staticmethod
    def _number(value):
        try:
            return parse_number(value)
        except (ValueError, TypeError):
            return None

    def submit_candidates(self, rows):
        if self.phase != "candidates":
            return Feedback(False, "Сейчас нужно выполнить другой этап.")
        stage = self.current_stage
        if not isinstance(rows, dict) or set(rows) != set(stage.states):
            return self._wrong()
        invalid = []
        for y in stage.states:
            actual, expected = rows[y], stage.candidates[y]
            if not isinstance(actual, (list, tuple)) or len(actual) != len(expected):
                invalid.append((y, -1))
                continue
            for x, (value, target) in enumerate(zip(actual, expected)):
                if target is None:
                    if value not in (None, "", "—", "-"):
                        invalid.append((y, x))
                elif self._number(value) != target:
                    invalid.append((y, x))
        if invalid:
            return self._wrong(invalid)
        self.phase = "summary"
        message = f"Таблица значений для груза {stage.index + 1} принята."
        self.history.append(message)
        return Feedback(True, message)

    def submit_summary(self, rows):
        if self.phase != "summary":
            return Feedback(False, "Сначала заполните таблицу значений.")
        stage = self.current_stage
        if not isinstance(rows, dict) or set(rows) != set(stage.states):
            return self._wrong()
        invalid, accepted = [], {}
        for y in stage.states:
            row = rows[y]
            if not isinstance(row, (list, tuple)) or len(row) != 2:
                invalid.append((y, -1))
                continue
            value, choice = self._number(row[0]), self._number(row[1])
            if value != stage.best[y]:
                invalid.append((y, 0))
            if choice is None or choice.denominator != 1 or choice not in stage.choices[y]:
                invalid.append((y, 1))
            if choice is not None and choice.denominator == 1:
                accepted[y] = (value, int(choice))
        if invalid:
            return self._wrong(invalid)
        self.accepted_summaries[stage.index] = accepted
        message = f"Максимумы и решения для груза {stage.index + 1} приняты."
        self.history.append(message)
        if self.stage_index + 1 < len(self.solution.stages):
            self.stage_index += 1
            self.phase = "candidates"
        else:
            self.phase = "restore"
        return Feedback(True, message)

    def submit_plan(self, plan, states=None):
        if self.phase != "restore":
            return Feedback(False, "Сначала заполните все таблицы.")
        if not isinstance(plan, (tuple, list)) or len(plan) != len(self.problem.weights):
            return self._wrong()
        values, invalid = [], []
        for j, raw in enumerate(plan):
            value = self._number(raw)
            if value is None or value.denominator != 1 or not 0 <= value < len(self.problem.values[j]):
                invalid.append((0, j))
            else:
                values.append(int(value))
        if invalid:
            return self._wrong(invalid)
        expected_states, resource = [], 0
        for weight, quantity in zip(self.problem.weights, values):
            expected_states.append(resource)
            resource += weight * quantity
        if states is not None:
            if not isinstance(states, (tuple, list)) or len(states) != len(values):
                return self._wrong(tuple((1, j) for j in range(len(values))))
            invalid_states = []
            for j, (raw, expected) in enumerate(zip(states, expected_states)):
                value = self._number(raw)
                if value is None or value.denominator != 1 or value < 0 or value != expected:
                    invalid_states.append((1, j))
            if invalid_states:
                return self._wrong(invalid_states)
        used = sum(w * x for w, x in zip(self.problem.weights, values))
        if used > self.problem.capacity:
            return self._wrong(tuple((0, j) for j in range(len(values))))
        objective = sum(row[x] for row, x in zip(self.problem.values, values))
        if objective != self.solution.objective:
            return self._wrong(tuple((0, j) for j in range(len(values))))
        self.accepted_plan = tuple(values)
        self.accepted_states = tuple(expected_states)
        self.phase = "done"
        self.history.append("Оптимальный план восстановлен. Работа завершена.")
        return Feedback(True, self.history[-1])

    def hint(self):
        self.hints += 1
        if self.phase == "candidates":
            if self.current_stage.index == len(self.problem.weights) - 1:
                return "Для последнего груза запишите F(x), если y + a·x ≤ B. Недопустимые клетки остаются пустыми."
            return "В каждой допустимой клетке сложите Fⱼ(x) и fⱼ₊₁(y + aⱼ·x) из предыдущего этапа. y — уже израсходованный ресурс."
        if self.phase == "summary":
            return "В каждой строке найдите наибольшее значение и номер его столбца x. При равных максимумах подходит любой из этих столбцов."
        if self.phase == "restore":
            return "Начните с y₁ = 0. Возьмите оптимальное x₁, затем переходите к y₂ = y₁ + a₁·x₁ и повторяйте для следующих грузов."
        return "Работа завершена. Можно начать новую задачу."
