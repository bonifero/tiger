"""Validated, exact input model for the bounded nonlinear knapsack problem."""
from dataclasses import dataclass
from fractions import Fraction
import math
import re

MAX_CAPACITY = 200
MAX_ITEMS = 12
MAX_QUANTITY = 200
MAX_CELLS = 60_000


def parse_number(value):
    """Read integers, decimal commas and fractions without rounding."""
    if isinstance(value, bool) or value is None:
        raise ValueError("Введите число, например 12, 2,5 или 1/3.")
    if isinstance(value, Fraction):
        result = value
    elif isinstance(value, int):
        result = Fraction(value)
    elif isinstance(value, (str, float)):
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("Число должно быть конечным.")
        text = str(value).strip().replace(",", ".")
        # Fraction also accepts Python-style digit separators in exponents.
        # They are outside our input syntax and must not bypass the guard below.
        if "_" in text:
            raise ValueError("Введите число без символов подчёркивания.")
        # Answers can sum up to twelve 256-bit input fractions. Keep enough
        # room for their common denominator while bounding hostile inputs.
        if not text or len(text) > 2600:
            raise ValueError("Введите число длиной не более 2600 символов.")
        # Fraction expands decimal exponents before we can inspect bit lengths.
        # Reject oversized exponents first, without converting huge digit strings.
        exponent = re.search(r"[eE]([+-]?\d+)$", text)
        if exponent:
            digits = exponent.group(1).lstrip("+-").lstrip("0") or "0"
            if len(digits) > 4 or int(digits) > 1200:
                raise ValueError("Показатель степени должен быть от −1200 до 1200.")
        try:
            result = Fraction(text)
        except (ValueError, ZeroDivisionError, OverflowError) as exc:
            raise ValueError("Введите число, например 12, 2,5 или 1/3.") from exc
    else:
        raise ValueError("Ожидалось число.")
    if result.numerator.bit_length() > 4096 or result.denominator.bit_length() > 4096:
        raise ValueError("Слишком большое число: используйте не более 4096 бит.")
    return result


def fmt_number(value):
    """Exact, locale-independent display suitable for subsequent editing."""
    if isinstance(value, Fraction) or type(value) is int:
        return str(value)
    return str(parse_number(value))


@dataclass(frozen=True)
class Problem:
    name: str
    capacity: int
    weights: tuple
    values: tuple
    labels: tuple = ()
    description: str = ""

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Укажите название задачи.")
        if not isinstance(self.description, str):
            raise ValueError("Описание задачи должно быть текстом.")
        if type(self.capacity) is not int or not 1 <= self.capacity <= MAX_CAPACITY:
            raise ValueError(f"Вместимость должна быть целой от 1 до {MAX_CAPACITY}.")
        if not isinstance(self.weights, (tuple, list)):
            raise ValueError("Веса должны быть списком.")
        weights = tuple(self.weights)
        if not 1 <= len(weights) <= MAX_ITEMS:
            raise ValueError(f"Допустимо от 1 до {MAX_ITEMS} видов груза.")
        if any(type(w) is not int or w <= 0 for w in weights):
            raise ValueError("Вес каждого предмета должен быть положительным целым.")
        if any(w > 10**12 for w in weights):
            raise ValueError("Вес не должен превышать 10¹².")
        if not isinstance(self.values, (tuple, list)) or len(self.values) != len(weights):
            raise ValueError("Для каждого вида груза нужна строка ценностей.")
        converted = []
        for row in self.values:
            if not isinstance(row, (tuple, list)) or not 1 <= len(row) <= MAX_QUANTITY + 1:
                raise ValueError(f"Таблица ценностей должна содержать количества от 0 до не более {MAX_QUANTITY}.")
            numbers = tuple(parse_number(value) for value in row)
            if any(value.numerator.bit_length() > 256 or value.denominator.bit_length() > 256 for value in numbers):
                raise ValueError("Исходные ценности должны содержать не более 256 бит в числителе и знаменателе.")
            if numbers[0] != 0:
                raise ValueError("Ценность нулевого количества должна быть равна 0.")
            if any(value < 0 for value in numbers):
                raise ValueError("Ценности должны быть неотрицательными.")
            converted.append(numbers)
        # Count the cells actually shown to the student, including impossible ones.
        cells = len(converted[0]) + (self.capacity + 1) * sum(len(row) for row in converted[1:])
        if cells > MAX_CELLS:
            raise ValueError(f"Таблицы слишком велики: {cells} ячеек, допустимо не более {MAX_CELLS}.")
        if not isinstance(self.labels, (tuple, list)):
            raise ValueError("Названия грузов должны быть списком.")
        labels = tuple(self.labels)
        if labels and (len(labels) != len(weights) or any(not isinstance(s, str) or not s.strip() for s in labels)):
            raise ValueError("Укажите непустое название для каждого вида груза.")
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "values", tuple(converted))
        object.__setattr__(self, "labels", labels)

    @property
    def names(self):
        return self.labels or tuple(f"Груз {j + 1}" for j in range(len(self.weights)))

    @property
    def quantities(self):
        return tuple(len(row) - 1 for row in self.values)
