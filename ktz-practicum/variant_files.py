"""Validated, portable JSON variants; imports are staged before changing the UI."""
import json
from pathlib import Path
import sys
from transport import Problem


def variants_directory():
    base = Path(sys.executable) if getattr(sys, 'frozen', False) else Path(__file__)
    return base.resolve().parent / 'variants'


def validate_variant(data):
    if not isinstance(data, dict):
        raise ValueError('Ожидается JSON-объект.')
    required = {'costs', 'supply', 'demand'}
    if not required <= data.keys():
        raise ValueError('Обязательные поля: costs, supply, demand.')
    if data.keys() - required - {'name', 'dummy_row', 'dummy_col'}:
        raise ValueError('Неизвестные поля в файле варианта.')
    if 'name' in data and (not isinstance(data['name'], str) or not data['name'].strip()):
        raise ValueError('Название name должно быть непустой строкой.')
    for key in required:
        if not isinstance(data[key], list):
            raise ValueError(f'Поле {key} должно быть массивом.')
    if any(not isinstance(row, list) for row in data['costs']):
        raise ValueError('costs должна быть матрицей массивов.')
    row, col = data.get('dummy_row', False), data.get('dummy_col', False)
    if type(row) is not bool or type(col) is not bool:
        raise ValueError('Признаки фиктивной вершины должны быть true или false.')
    if row and col:
        raise ValueError('Нельзя указать одновременно фиктивную строку и столбец.')
    problem = Problem(tuple(tuple(r) for r in data['costs']),
                      tuple(data['supply']), tuple(data['demand']), row, col)
    if not (1 <= problem.m - int(row) <= 30 and 1 <= problem.n - int(col) <= 30):
        raise ValueError('Допустимо от 1 до 30 реальных строк и столбцов.')
    if any(x > 10**12 for x in (*problem.supply, *problem.demand,
                               *(x for r in problem.costs for x in r))):
        raise ValueError('Значения не должны превышать 1 000 000 000 000.')
    return problem


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
        problem = validate_variant(data)
        return data.get('name', path.stem).strip(), problem
    except (OSError, ValueError, TypeError, RecursionError) as error:
        raise ValueError(f'{path.name}: {error}') from error


def load_variant(path):
    return read_variant(path)[1]


def append_variant(variants, name, problem):
    label = name
    suffix = 2
    while label in variants:
        label = f'{name} ({suffix})'
        suffix += 1
    variants[label] = problem
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


def save_variant(path, problem, name=None):
    data = dict(costs=[list(row) for row in problem.costs], supply=list(problem.supply),
                demand=list(problem.demand), dummy_row=problem.dummy_row, dummy_col=problem.dummy_col)
    if name is not None:
        data['name'] = name
    validate_variant(data)
    path = Path(path)
    if not path.suffix:
        path = path.with_suffix('.json')
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return path
