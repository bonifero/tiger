"""Teaching state machine for the matrix-game mixed-strategy lab. Wrong
answers never reveal the correct value in the error text; use Lesson.hint()."""
from solver import saddle_point, solve_mixed


PHASE_TITLES = {
    'alpha': 'Нижняя цена игры α',
    'beta': 'Верхняя цена игры β',
    'saddle': 'Седловая точка',
    'pure': 'Оптимальные чистые стратегии',
    'solve': 'Вспомогательные задачи ЛП',
    'value': 'Цена игры ν',
    'prob_a': 'Вероятности игрока А',
    'prob_b': 'Вероятности игрока B',
    'done': 'Решение завершено',
}

# Sidebar step index; setup page (matrix entry) is step 0.
_STEP_INDEX = {'alpha': 1, 'beta': 1, 'saddle': 2, 'pure': 3, 'solve': 3,
               'value': 4, 'prob_a': 5, 'prob_b': 5, 'done': 6}


class Lesson:
    def __init__(self, game):
        self.game = game
        self.matrix = game.matrix
        self.m = len(self.matrix)
        self.n = len(self.matrix[0])
        self.saddle = saddle_point(self.matrix)
        self.solution = None
        self.value = None
        self.phase = 'alpha'
        self.errors = 0
        self.hints = 0
        self.history = []

    @property
    def step(self):
        return _STEP_INDEX[self.phase]

    def check(self, answer=None):
        """Returns (accepted, feedback); only accepted answers advance the lesson."""
        previous_phase = self.phase
        try:
            self._answer(answer)
        except (ValueError, TypeError):
            self.errors += 1
            return False, 'Ошибка ответа.'
        self.history.append({
            'alpha': 'Нижняя цена игры α принята.',
            'beta': 'Верхняя цена игры β принята.',
            'saddle': 'Ответ о седловой точке принят.',
            'pure': 'Чистые стратегии приняты.',
            'solve': 'Вспомогательные задачи линейного программирования решены.',
            'value': 'Цена игры ν принята.',
            'prob_a': 'Вероятности игрока А приняты.',
            'prob_b': 'Вероятности игрока B приняты.',
        }.get(previous_phase, 'Ответ принят.'))
        return True, ''

    def _answer(self, answer):
        if self.phase == 'alpha':
            if answer != self.saddle.alpha:
                raise ValueError('α — это максимум из минимумов по строкам матрицы.')
            self.phase = 'beta'
            return
        if self.phase == 'beta':
            if answer != self.saddle.beta:
                raise ValueError('β — это минимум из максимумов по столбцам матрицы.')
            self.phase = 'saddle'
            return
        if self.phase == 'saddle':
            if type(answer) is not bool or answer != self.saddle.exists:
                raise ValueError('Седловая точка существует, только если α = β. Сравните свои значения α и β.')
            self.phase = 'pure' if answer else 'solve'
            return
        if self.phase == 'pure':
            if (not isinstance(answer, tuple) or len(answer) != 2
                    or answer[0] not in self.saddle.rows or answer[1] not in self.saddle.cols):
                raise ValueError('Нужна строка с минимумом, равным α, и столбец с максимумом, равным β.')
            self.value = self.saddle.alpha
            self.phase = 'done'
            return
        if self.phase == 'solve':
            self.solution = solve_mixed(self.matrix)
            self.phase = 'value'
            return
        if self.phase == 'value':
            if answer != self.solution.value:
                raise ValueError('ν = ν* − c, где ν* = 1/Lmin — цена игры со сдвинутой матрицей, c — сдвиг.')
            self.value = self.solution.value
            self.phase = 'prob_a'
            return
        if self.phase == 'prob_a':
            if tuple(answer) != tuple(self.solution.p):
                raise ValueError('pᵢ = xᵢ·ν*. Вероятности неотрицательны и в сумме равны 1.')
            self.phase = 'prob_b'
            return
        if self.phase == 'prob_b':
            if tuple(answer) != tuple(self.solution.q):
                raise ValueError('qⱼ = yⱼ·ν*. Вероятности неотрицательны и в сумме равны 1.')
            self.phase = 'done'
            return
        raise ValueError('Решение уже завершено.')

    def hint(self):
        self.hints += 1
        if self.phase == 'alpha':
            mins = tuple(min(row) for row in self.matrix)
            return f'Минимумы строк: {mins}. α = максимум из них = {self.saddle.alpha}.'
        if self.phase == 'beta':
            maxs = tuple(max(self.matrix[i][j] for i in range(self.m)) for j in range(self.n))
            return f'Максимумы столбцов: {maxs}. β = минимум из них = {self.saddle.beta}.'
        if self.phase == 'saddle':
            relation = '=' if self.saddle.exists else '≠'
            state = 'есть' if self.saddle.exists else 'отсутствует'
            return f'α {relation} β ({self.saddle.alpha} и {self.saddle.beta}), значит седловая точка {state}.'
        if self.phase == 'pure':
            rows = ', '.join(str(i + 1) for i in self.saddle.rows)
            cols = ', '.join(str(j + 1) for j in self.saddle.cols)
            return f'Подходят строки № {rows} и столбцы № {cols}. Цена игры равна α = β = {self.saddle.alpha}.'
        if self.phase == 'value':
            s = self.solution
            nu_star = 1 / s.lmin
            return (f'Lmin = {s.lmin}; ν* = 1/Lmin = {nu_star}; '
                    f'сдвиг c = {s.shift}; ν = ν* − c = {s.value}.')
        if self.phase == 'prob_a':
            return f'p = {self.solution.p}.'
        if self.phase == 'prob_b':
            return f'q = {self.solution.q}.'
        return 'Следуйте инструкции текущего этапа.'
