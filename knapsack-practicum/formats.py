"""Versioned JSON problem files with exact values and atomic saves."""
import json
import os
from pathlib import Path
import tempfile

from model import Problem, fmt_number

MAX_FILE_BYTES = 2 * 1024 * 1024


def to_dict(problem):
    return {
        "version": 1,
        "name": problem.name,
        "capacity": problem.capacity,
        "weights": list(problem.weights),
        "values": [[fmt_number(value) for value in row] for row in problem.values],
        "labels": list(problem.labels),
        "description": problem.description,
    }


def from_dict(data):
    if not isinstance(data, dict):
        raise ValueError("Файл должен содержать JSON-объект задачи.")
    if type(data.get("version")) is not int or data["version"] != 1:
        raise ValueError("Поддерживается только версия формата 1.")
    for key in ("name", "capacity", "weights", "values"):
        if key not in data:
            raise ValueError(f"В файле отсутствует поле {key}.")
    return Problem(data["name"], data["capacity"], data["weights"], data["values"],
                   data.get("labels", ()), data.get("description", ""))


def _object(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise ValueError(f"Повторяющееся поле JSON: {key}.")
        data[key] = value
    return data


def _constant(value):
    raise ValueError(f"Недопустимая числовая константа JSON: {value}.")


def load(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_FILE_BYTES + 1)
    if len(raw) > MAX_FILE_BYTES:
        raise ValueError("Файл слишком велик: допустимо не более 2 МиБ.")
    try:
        # Preserve JSON decimal spelling for Fraction; binary floats can turn
        # distinct objective values into ties before model validation begins.
        data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_object,
                          parse_constant=_constant, parse_float=str)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError("Не удалось прочитать JSON в кодировке UTF-8.") from exc
    return from_dict(data)


def save(path, problem):
    destination = Path(path)
    if not destination.suffix:
        destination = destination.with_suffix(".json")
    payload = json.dumps(to_dict(problem), ensure_ascii=False, indent=2) + "\n"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination.parent,
                                         prefix=f".{destination.name}.", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return destination
