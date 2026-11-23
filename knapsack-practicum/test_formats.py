import json
from fractions import Fraction
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from formats import from_dict, load, save, to_dict, MAX_FILE_BYTES
from model import Problem
from solver import solve


class FormatTests(unittest.TestCase):
    def setUp(self):
        self.problem = Problem("Ценность · дроби", 4, (1, 2), ((0, "1/3", "2,5"), (0, 7)),
                               ("Первый", "Второй"), "Условие\nс пояснением.")

    def test_exact_roundtrip_and_automatic_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            path = save(Path(directory) / "задача", self.problem)
            self.assertEqual(path.suffix, ".json")
            self.assertEqual(load(path), self.problem)
            data = json.loads(path.read_text())
            self.assertEqual(data["values"][0], ["0", "1/3", "5/2"])
            self.assertEqual(list(Path(directory).glob("*.tmp")), [])

    def test_failed_atomic_replace_preserves_old_file_and_removes_temp(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "задача.json"
            path.write_text("old data")
            with patch("formats.os.replace", side_effect=OSError("simulated")), self.assertRaises(OSError):
                save(path, self.problem)
            self.assertEqual(path.read_text(), "old data")
            self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_schema_version_and_validation(self):
        data = to_dict(self.problem)
        for version in (None, True, "1", 0, 2):
            with self.subTest(version=version), self.assertRaises(ValueError):
                from_dict(data | {"version": version})
        with self.assertRaises(ValueError):
            from_dict([])
        for key in ("name", "capacity", "weights", "values"):
            missing = dict(data)
            del missing[key]
            with self.subTest(key=key), self.assertRaises(ValueError):
                from_dict(missing)

    def test_bad_json_duplicate_keys_nonfinite_and_size(self):
        cases = ('{', '{"version":1,"version":1}', '{"value":NaN}', '{"value":Infinity}', '[]')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            for payload in cases:
                path.write_text(payload)
                with self.subTest(payload=payload), self.assertRaises(ValueError):
                    load(path)
            path.write_bytes(b"x" * (MAX_FILE_BYTES + 1))
            with self.assertRaisesRegex(ValueError, "велик"):
                load(path)

    def test_raw_json_decimals_keep_the_exact_optimum(self):
        payload = ('{"version":1,"name":"Точный выбор","capacity":2,'
                   '"weights":[1],"values":[[0,1,1.00000000000000001]]}')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "decimal.json"
            path.write_text(payload, encoding="utf-8")
            problem = load(path)
            self.assertEqual(problem.values[0][2], Fraction("1.00000000000000001"))
            answer = solve(problem)
            self.assertEqual(answer.plan, (2,))
            self.assertEqual(answer.stages[0].choices[0], (2,))
            self.assertEqual(answer.objective, Fraction("1.00000000000000001"))

    def test_excessive_json_nesting_is_a_controlled_validation_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested.json"
            path.write_text("[" * 5000 + "0" + "]" * 5000, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "JSON"):
                load(path)


if __name__ == "__main__":
    unittest.main()
