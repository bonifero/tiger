import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import tkinter as tk
from app import App
from transport import Problem, solve
from test_oracle import solve as min_cost_flow
from variant_files import load_variant, read_variant, load_variants, save_variant, variants_directory


class VariantTests(unittest.TestCase):
    def test_bundled_variants_and_fifth_solution(self):
        variants=load_variants(variants_directory())
        self.assertEqual(len(variants),6)
        p=variants['Вариант 5 · ремонт локомотивов']
        self.assertEqual((p.m,p.n),(4,5))
        self.assertEqual(p.supply,(15,19,17,21))
        self.assertEqual(p.demand,(12,16,10,19,13))
        self.assertEqual(p.costs[0],(13,11,9,13,17))
        balanced=p.balanced()
        self.assertEqual(solve(balanced).cost,min_cost_flow(balanced.supply,balanced.demand,balanced.costs)['objective'])

    def test_validation_and_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'custom'
            p=Problem(((2,),),(4,),(5,))
            saved=save_variant(path,p)
            self.assertEqual(saved.suffix,'.json')
            self.assertEqual(read_variant(saved),('custom',p))
            valid=json.loads(saved.read_text(encoding='utf-8'))
            invalid=[[],{},dict(valid,costs=[1]),dict(valid,costs=[[1,2]]),
                     dict(valid,supply=[True]),dict(valid,demand=[-1]),
                     dict(valid,demand=[1.5]),dict(valid,demand=[10**12+1]),
                     dict(valid,dummy_row=1),dict(valid,dummy_row=True,dummy_col=True),
                     dict(valid,name=''),dict(valid,supply='4')]
            for data in invalid:
                with self.subTest(data=data):
                    saved.write_text(json.dumps(data),encoding='utf-8')
                    with self.assertRaises(ValueError):load_variant(saved)
            saved.write_text('{"costs":[],"costs":[]}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Повторяющееся'):load_variant(saved)

    def test_imports_are_atomic_and_single_import_appends(self):
        root=tk.Tk();root.withdraw()
        try:
            app=App(root)
            with tempfile.TemporaryDirectory() as directory:
                folder=Path(directory)
                p=Problem(((3,),),(5,),(4,))
                first=save_variant(folder/'a.json',p,'Новый')
                with patch('app.filedialog.askopenfilename',return_value=str(first)):
                    count=len(app.variants)
                    app.open_variant();app.open_variant()
                    self.assertEqual(len(app.variants),count+2)
                    self.assertEqual(list(app.variants)[-2:],['Новый','Новый (2)'])
                app.cost_entries[0][0].delete(0,'end')
                app.cost_entries[0][0].insert(0,'123')
                before=dict(app.variants);selected=app.preset.get()
                bad=folder/'b.json';bad.write_text('bad json',encoding='utf-8')
                with patch('app.filedialog.askdirectory',return_value=str(folder)):
                    app.open_variants()
                    self.assertEqual(app.variants,before)
                    self.assertEqual(app.preset.get(),selected)
                    self.assertEqual(app.cost_entries[0][0].get(),'123')
                    self.assertIn('b.json',app.setup_note.cget('text'))
                    save_variant(bad,p,'Второй')
                    app.open_variants()
                    self.assertEqual(list(app.variants),['Новый','Второй'])
                    self.assertEqual(app.read_problem(),p)
                with patch('app.filedialog.asksaveasfilename',return_value=str(folder/'export')):
                    app.export_variant()
                    self.assertEqual(load_variant(folder/'export.json'),p)
                app._setup()
                self.assertEqual(list(app.variants),['Новый','Второй'])
                with tempfile.TemporaryDirectory() as empty:
                    with patch('app.filedialog.askdirectory',return_value=empty):
                        app.open_variants()
                        self.assertEqual(list(app.variants),['Новый','Второй'])
        finally:root.destroy()

    def test_start_without_default_folder(self):
        root=tk.Tk();root.withdraw()
        try:
            with tempfile.TemporaryDirectory() as directory:
                with patch('app.variants_directory',return_value=Path(directory)/'missing'):
                    app=App(root)
                    self.assertEqual(app.variants,{})
                    self.assertEqual(app.read_problem().m,4)
        finally:root.destroy()
