"""Validated, portable JSON variants for matrix-game scenarios; numbers are kept as exact fractions."""
from dataclasses import dataclass, replace
from fractions import Fraction as Q
import json
from pathlib import Path
import sys


def variants_directory():
    base = Path(sys.executable) if getattr(sys, 'frozen', False) else Path(__file__)
    return base.resolve().parent / 'variants'


def number(value):
    if isinstance(value, Q):
        return value
    if isinstance(value, bool):
        raise ValueError(f'Число не может быть логическим значением: {value!r}')
    if isinstance(value, int):
        return Q(value)
    if not isinstance(value, str):
        raise ValueError(f'Не удаётся распознать число: {value!r}')
    text = value.strip().replace(',', '.')
    if not text:
        raise ValueError('Пустое число.')
    try:
        if ' ' in text:
            whole, rest = text.split(None, 1)
            whole, rest = whole.strip(), rest.strip()
            sign = -1 if whole.startswith('-') else 1
            return Q(whole) + sign * Q(rest)
        return Q(text)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f'Не удаётся распознать число: {value!r}') from error


@dataclass(frozen=True)
class Game:
    matrix: tuple
    row_labels: tuple
    col_labels: tuple
    name: str = 'Новая игра'
    description: str = ''

    def __post_init__(self):
        object.__setattr__(self, 'matrix', tuple(tuple(number(x) for x in row) for row in self.matrix))
        object.__setattr__(self, 'row_labels', tuple(self.row_labels))
        object.__setattr__(self, 'col_labels', tuple(self.col_labels))
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError('Название name должно быть непустой строкой.')
        if not isinstance(self.description, str):
            raise ValueError('Поле description должно быть строкой.')
        m = len(self.matrix)
        if not 1 <= m <= 8:
            raise ValueError('Число строк матрицы (стратегий игрока А) должно быть от 1 до 8.')
        n = len(self.matrix[0]) if m else 0
        if not 1 <= n <= 8:
            raise ValueError('Число столбцов матрицы (стратегий игрока В) должно быть от 1 до 8.')
        if any(len(row) != n for row in self.matrix):
            raise ValueError('Все строки матрицы должны содержать одинаковое число элементов.')
        if len(self.row_labels) != m:
            raise ValueError('Число названий строк (row_labels) должно совпадать с числом строк матрицы.')
        if len(self.col_labels) != n:
            raise ValueError('Число названий столбцов (col_labels) должно совпадать с числом столбцов матрицы.')
        if any(not isinstance(label, str) or not label.strip() for label in (*self.row_labels, *self.col_labels)):
            raise ValueError('Названия строк и столбцов должны быть непустыми строками.')
        for row in self.matrix:
            for value in row:
                if value.numerator.bit_length() > 256 or value.denominator.bit_length() > 256:
                    raise ValueError('Числа в матрице слишком велики.')


def validate_variant(data):
    if not isinstance(data, dict):
        raise ValueError('Ожидается JSON-объект.')
    required = {'matrix', 'row_labels', 'col_labels'}
    if not required <= data.keys():
        raise ValueError('Обязательные поля: matrix, row_labels, col_labels.')
    if data.keys() - required - {'name', 'description'}:
        raise ValueError('Неизвестные поля в файле варианта.')
    if 'name' in data and (not isinstance(data['name'], str) or not data['name'].strip()):
        raise ValueError('Название name должно быть непустой строкой.')
    if 'description' in data and not isinstance(data['description'], str):
        raise ValueError('Поле description должно быть строкой.')
    if not isinstance(data['matrix'], list) or any(not isinstance(row, list) for row in data['matrix']):
        raise ValueError('Поле matrix должно быть матрицей (массивом массивов).')
    if not isinstance(data['row_labels'], list):
        raise ValueError('Поле row_labels должно быть массивом.')
    if not isinstance(data['col_labels'], list):
        raise ValueError('Поле col_labels должно быть массивом.')
    kwargs = dict(matrix=tuple(tuple(row) for row in data['matrix']),
                  row_labels=tuple(data['row_labels']),
                  col_labels=tuple(data['col_labels']))
    if 'name' in data:
        kwargs['name'] = data['name'].strip()
    if 'description' in data:
        kwargs['description'] = data['description']
    return Game(**kwargs)


def _unique_keys(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise ValueError(f'Повторяющееся поле: {key}.')
        data[key] = value
    return data


def read_variant(path):
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=_unique_keys)
        game = validate_variant(data)
        name = data.get('name', path.stem).strip()
        if name != game.name:
            game = replace(game, name=name)
        return name, game
    except (OSError, ValueError, TypeError, RecursionError) as error:
        raise ValueError(f'{path.name}: {error}') from error


def load_variant(path):
    return read_variant(path)[1]


def append_variant(variants, name, game):
    label = name
    suffix = 2
    while label in variants:
        label = f'{name} ({suffix})'
        suffix += 1
    variants[label] = game
    return label


def load_variants(directory):
    directory = Path(directory)
    if not directory.is_dir():
        raise ValueError(f'Папка вариантов не найдена: {directory}')
    try:
        paths = sorted((p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == '.json'),
                       key=lambda p: p.name.casefold())
    except OSError as error:
        raise ValueError(f'Не удалось прочитать папку: {directory}') from error
    if not paths:
        raise ValueError('В выбранной папке нет JSON-файлов вариантов.')
    variants = {}
    for path in paths:
        append_variant(variants, *read_variant(path))
    return variants


def save_variant(path, game, name=None):
    data = dict(
        name=name if name is not None else game.name,
        description=game.description,
        row_labels=list(game.row_labels),
        col_labels=list(game.col_labels),
        matrix=[[str(value) for value in row] for row in game.matrix],
    )
    validate_variant(data)
    path = Path(path)
    if not path.suffix:
        path = path.with_suffix('.json')
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return path
