import json
from pathlib import Path
import tempfile
import unittest

from variant_files import (
    Game, append_variant, load_variant, load_variants, number,
    read_variant, save_variant, validate_variant, variants_directory,
)


class VariantFilesTests(unittest.TestCase):
    def test_bundled_variants_load(self):
        variants = load_variants(variants_directory())
        self.assertEqual(len(variants), 7)
        for name, game in variants.items():
            self.assertIsInstance(game, Game)
            self.assertEqual(game.name, name)
            self.assertTrue(1 <= len(game.matrix) <= 8)
            self.assertTrue(1 <= len(game.matrix[0]) <= 8)

    def test_roundtrip_through_save_and_read(self):
        variants = load_variants(variants_directory())
        with tempfile.TemporaryDirectory() as directory:
            for index, (name, game) in enumerate(variants.items()):
                path = Path(directory) / f'v{index}.json'
                saved = save_variant(path, game, name=name)
                read_name, read_game = read_variant(saved)
                self.assertEqual(read_name, name)
                self.assertEqual(read_game.matrix, game.matrix)
                self.assertEqual(read_game.row_labels, game.row_labels)
                self.assertEqual(read_game.col_labels, game.col_labels)
                self.assertEqual(read_game.name, game.name)

    def test_validate_variant_accepts_minimal_valid_data(self):
        data = dict(matrix=[["1", "2"], ["3", "4"]],
                    row_labels=["A1", "A2"], col_labels=["B1", "B2"])
        game = validate_variant(data)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.matrix, ((1, 2), (3, 4)))

    def test_validate_variant_rejects_bad_input(self):
        base = dict(matrix=[["1", "2"], ["3", "4"]],
                    row_labels=["A1", "A2"], col_labels=["B1", "B2"])
        invalid = [
            [],
            {},
            {k: v for k, v in base.items() if k != 'matrix'},
            dict(base, extra='нет такого поля'),
            dict(base, name=123),
            dict(base, name=''),
            dict(base, name='   '),
            dict(base, matrix=[["1", "2"], ["3"]]),
            dict(base, matrix=[["1", "2", "3"], ["4", "5", "6"]]),
            dict(base, row_labels=["A1"]),
            dict(base, col_labels=["B1"]),
            dict(base, matrix=[['1'] * 9 for _ in range(1)], row_labels=['R'], col_labels=[f'C{i}' for i in range(9)]),
            dict(base, matrix=[['1'] for _ in range(9)], row_labels=[f'R{i}' for i in range(9)], col_labels=['C']),
            dict(base, matrix=[["abc", "2"], ["3", "4"]]),
            dict(base, description=5),
        ]
        for data in invalid:
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    validate_variant(data)

    def test_append_variant_deduplicates_names(self):
        variants = {}
        game = Game(matrix=(('1',),), row_labels=('R',), col_labels=('C',), name='Игра')
        label1 = append_variant(variants, 'Дубликат', game)
        label2 = append_variant(variants, 'Дубликат', game)
        label3 = append_variant(variants, 'Дубликат', game)
        self.assertEqual([label1, label2, label3], ['Дубликат', 'Дубликат (2)', 'Дубликат (3)'])
        self.assertEqual(set(variants), {'Дубликат', 'Дубликат (2)', 'Дубликат (3)'})

    def test_load_variants_is_all_or_nothing_on_broken_file(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            game = Game(matrix=(('1', '2'),), row_labels=('R',), col_labels=('C1', 'C2'))
            save_variant(folder / 'good.json', game, name='Хорошая игра')
            (folder / 'bad.json').write_text('не json', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'bad.json'):
                load_variants(folder)

    def test_number_parsing(self):
        self.assertEqual(number('0,8'), number('0.8'))
        self.assertEqual(number('0.8').numerator, 4)
        self.assertEqual(number('0.8').denominator, 5)
        self.assertEqual(number('-3'), -3)
        self.assertEqual(number('1/3').numerator, 1)
        self.assertEqual(number('1/3').denominator, 3)
        self.assertEqual(number('-3 2/5'), number('-17/5'))
        self.assertEqual(number(4), 4)
        with self.assertRaises(ValueError):
            number('abc')
        with self.assertRaises(ValueError):
            number(True)

    def test_game_rejects_too_many_rows_or_columns(self):
        with self.assertRaises(ValueError):
            Game(matrix=tuple(('1',) for _ in range(9)),
                 row_labels=tuple(f'R{i}' for i in range(9)), col_labels=('C',))
        with self.assertRaises(ValueError):
            Game(matrix=(tuple('1' for _ in range(9)),),
                 row_labels=('R',), col_labels=tuple(f'C{i}' for i in range(9)))

    def test_game_rejects_huge_numbers(self):
        huge = str(2 ** 300)
        with self.assertRaises(ValueError):
            Game(matrix=((huge,),), row_labels=('R',), col_labels=('C',))

    def test_game_requires_nonempty_labels(self):
        with self.assertRaises(ValueError):
            Game(matrix=(('1', '2'),), row_labels=('R',), col_labels=('', 'C2'))


if __name__ == '__main__':
    unittest.main()
