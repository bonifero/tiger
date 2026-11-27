"""Матричные игры в смешанных стратегиях: седловая точка и сведение к ЛП."""
from dataclasses import dataclass
from fractions import Fraction as Q


def number(value):
    text = str(value).strip().replace(',', '.').replace('_', ' ')
    try:
        if ' ' in text:
            whole, rest = text.split()
            return Q(whole) + (-1 if whole.startswith('-') else 1) * Q(rest)
        return Q(text)
    except (ValueError, ZeroDivisionError):
        raise ValueError(f'Не удаётся распознать число: {value!r}')


@dataclass(frozen=True)
class Saddle:
    alpha: object
    beta: object
    rows: tuple
    cols: tuple

    @property
    def exists(self):
        return self.alpha == self.beta


def saddle_point(matrix):
    m, n = len(matrix), len(matrix[0])
    row_mins = [min(row) for row in matrix]
    col_maxs = [max(matrix[i][j] for i in range(m)) for j in range(n)]
    alpha, beta = max(row_mins), min(col_maxs)
    rows = tuple(i for i in range(m) if row_mins[i] == alpha)
    cols = tuple(j for j in range(n) if col_maxs[j] == beta)
    return Saddle(alpha, beta, rows, cols)


def solve_lp(c, A, b, signs, sense, limit=2000):
    """Точный двухфазный симплекс-метод. x,A,b,c — Fraction; переменные >=0."""
    if sense not in ('min', 'max'):
        raise ValueError('Направление оптимизации должно быть min или max.')
    if len(A) != len(b) or len(signs) != len(b) or any(len(row) != len(c) for row in A):
        raise ValueError('Неверные размеры задачи линейного программирования.')
    k = len(c)
    data = []
    for row, bi, s in zip(A, b, signs):
        row = list(row)
        if bi < 0:
            row = [-v for v in row]
            bi = -bi
            s = {'<=': '>=', '>=': '<=', '=': '='}[s]
        data.append([row, bi, s])
    rows = [list(row) + [bi] for row, bi, _ in data]
    ncols = k
    basis = []
    art = set()

    def column():
        nonlocal ncols
        for row_ in rows:
            row_.insert(-1, Q(0))
        ncols += 1
        return ncols - 1

    for i, (_, _, s) in enumerate(data):
        if s != '=':
            j = column()
            rows[i][j] = Q(1 if s == '<=' else -1)
        if s == '<=':
            basis.append(j)
        else:
            j = column()
            rows[i][j] = Q(1)
            basis.append(j)
            art.add(j)

    count = 0

    def objective(costs_full):
        z = [-v for v in costs_full] + [Q(0)]
        for row, j in zip(rows, basis):
            v = z[j]
            z = [a - v * bb for a, bb in zip(z, row)]
        return z

    def pivot(i, j, z):
        nonlocal count
        d = rows[i][j]
        rows[i] = [v / d for v in rows[i]]
        for idx in range(len(rows)):
            if idx != i:
                d2 = rows[idx][j]
                rows[idx] = [a - d2 * bb for a, bb in zip(rows[idx], rows[i])]
        d3 = z[j]
        z[:] = [a - d3 * bb for a, bb in zip(z, rows[i])]
        basis[i] = j
        count += 1

    def primal(z):
        while True:
            if count >= limit:
                return 'limit'
            entering = next((j for j, v in enumerate(z[:-1]) if v < 0), None)
            if entering is None:
                return 'optimal'
            candidates = [i for i, row in enumerate(rows) if row[entering] > 0]
            if not candidates:
                return 'unbounded'
            i = min(candidates, key=lambda i: (rows[i][-1] / rows[i][entering], basis[i]))
            pivot(i, entering, z)

    if art:
        z = objective([Q(-1) if j in art else Q(0) for j in range(ncols)])
        status = primal(z)
        if status == 'limit':
            raise RuntimeError('Превышен лимит итераций.')
        if z[-1] != 0:
            return 'infeasible', (), None
        for i in reversed(range(len(rows))):
            if basis[i] in art:
                j = next((j for j, v in enumerate(rows[i][:-1]) if j not in art and v), None)
                if j is None:
                    rows.pop(i)
                    basis.pop(i)
                else:
                    pivot(i, j, z)
        keep = [j for j in range(ncols) if j not in art]
        rows[:] = [[row[j] for j in keep] + [row[-1]] for row in rows]
        basis[:] = [keep.index(j) for j in basis]
        ncols = len(keep)

    direction = 1 if sense == 'max' else -1
    full_costs = [direction * c[j] if j < k else Q(0) for j in range(ncols)]
    z = objective(full_costs)
    status = primal(z)
    if status == 'unbounded':
        return 'unbounded', (), None
    if status == 'limit':
        raise RuntimeError('Превышен лимит итераций.')
    x = [Q(0)] * ncols
    for row, j in zip(rows, basis):
        x[j] = row[-1]
    objective_value = sum(a * v for a, v in zip(c, x[:k]))
    return 'optimal', tuple(x[:k]), objective_value


@dataclass(frozen=True)
class GameSolution:
    value: object
    p: tuple
    q: tuple
    shift: object
    x: tuple
    y: tuple
    lmin: object


def solve_mixed(matrix):
    """Решение матричной игры в смешанных стратегиях через пару двойственных ЛП."""
    m, n = len(matrix), len(matrix[0])
    lo = min(v for row in matrix for v in row)
    shift = Q(0) if lo > 0 else Q(1) - lo
    shifted = tuple(tuple(v + shift for v in row) for row in matrix)

    # Игрок B: max sum(y) при A'y <= 1 по каждой строке.
    status_b, y, lmax = solve_lp(
        tuple(Q(1) for _ in range(n)), shifted,
        tuple(Q(1) for _ in range(m)), tuple('<=' for _ in range(m)), 'max')

    # Игрок A: min sum(x) при A'^T x >= 1 по каждому столбцу.
    columns = tuple(tuple(shifted[i][j] for i in range(m)) for j in range(n))
    status_a, x, lmin = solve_lp(
        tuple(Q(1) for _ in range(m)), columns,
        tuple(Q(1) for _ in range(n)), tuple('>=' for _ in range(n)), 'min')

    if status_a != 'optimal' or status_b != 'optimal':
        raise ArithmeticError('Не удалось найти решение игры.')
    if lmin != lmax:
        raise ArithmeticError('Нарушена двойственность.')

    nu_star = Q(1) / lmin
    value = nu_star - shift
    p = tuple(xi * nu_star for xi in x)
    q = tuple(yj * nu_star for yj in y)
    return GameSolution(value, p, q, shift, x, y, lmin)
