"""Tk widget construction/rendering checks, without mouse/keyboard injection."""
import unittest
import tkinter as tk
import tempfile
from pathlib import Path
from types import SimpleNamespace
from app import App
from lesson import Lesson
from presets import PRESETS
from variant_files import load_variant, save_variant
from transport import Problem


class RenderingTests(unittest.TestCase):
    def test_all_lesson_screens(self):
        root=tk.Tk();root.withdraw()
        try:
            app=App(root)
            app.start()
            self.assertIsNone(app.lesson)
            app.check_balance()
            app.add_dummy()
            app.demand_entries[-1].insert(0,'89')
            app.start()
            self.assertIsNone(app.lesson)
            app.demand_entries[-1].delete(0,'end')
            app.demand_entries[-1].insert(0,'90')
            app.start()
            self.assertIsNotNone(app.lesson)
            visited=set()
            for problem in [next(iter(PRESETS.values())), list(PRESETS.values())[-1]]:
                app.lesson=Lesson(problem.balanced())
                app.show_lesson()
                while True:
                    root.update_idletasks()
                    phase=app.lesson.phase;visited.add(phase)
                    self.assertEqual(app.hint_label.cget('text'),'')
                    self.assertEqual(app.hint_label.winfo_manager(),'')
                    if phase in ('done','basis','pivot'):
                        self.assertIsNone(app.hint_button)
                    else:
                        hints=app.lesson.hints
                        errors=app.lesson.errors
                        history=list(app.lesson.history)
                        app.hint_button.invoke()
                        self.assertEqual(app.lesson.hints,hints+1)
                        self.assertEqual(app.lesson.errors,errors)
                        self.assertEqual(app.lesson.phase,phase)
                        self.assertEqual(app.lesson.history,history)
                        self.assertEqual(app.hint_label.winfo_manager(),'pack')
                        self.assertTrue(app.hint_label.cget('text').startswith('Подсказка\n\n'))
                        self.assertNotIn('Следуйте инструкции',app.hint_label.cget('text'))
                        self.assertEqual(app.stat_labels[2].cget('text'),f'{errors} / {hints+1}')
                    self.assertTrue(app.matrix.canvas.find_all())
                    texts=[app.matrix.canvas.itemcget(item,'text')
                           for item in app.matrix.canvas.find_all()
                           if app.matrix.canvas.type(item)=='text']
                    shown=[text for text in texts if text.startswith(('u = ', 'v = '))]
                    expected=[]
                    if app.lesson.accepted_potentials is not None:
                        u,v=app.lesson.accepted_potentials
                        expected=[f'u = {value}' for value in u]+[f'v = {value}' for value in v]
                    self.assertCountEqual(shown,expected)
                    self.assertNotIn('План оптимален?',texts)
                    if phase=='potentials':
                        entries=app.matrix.potential_entries
                        self.assertEqual(len(entries),app.lesson.problem.m+app.lesson.problem.n)
                        for e in entries:e.insert(0,'999')
                        app.check()
                        self.assertEqual(app.lesson.phase,'potentials')
                        self.assertEqual(app.feedback,'Ошибка ответа.')
                        app.zoom.set(50);app.change_zoom()
                        self.assertTrue(all(e.get()=='999' for e in app.matrix.potential_entries))
                        app.zoom.set(150);app.change_zoom()
                        app.zoom_plus.invoke()
                        app.zoom_fit.invoke()
                        app.reset_zoom()
                        self.assertTrue(all(e.get()=='999' for e in app.matrix.potential_entries))
                        u,v=app.lesson.state.potentials()
                        for e,value in zip(app.matrix.potential_entries,u+v):
                            e.delete(0,'end');e.insert(0,str(value))
                        app.check()
                        self.assertEqual(app.lesson.phase,'optimal')
                        app.zoom.set(100);app.change_zoom()
                        continue
                    if phase=='done':break
                    answer=None;l=app.lesson
                    if phase=='cell':l.selected={l.builder.candidates[0]}
                    elif phase=='amount':answer=l.builder.amount(l.entering)
                    elif phase=='potentials':answer=l.state.potentials()
                    elif phase=='optimal':answer=not l.state.improving()
                    elif phase=='enter':l.selected={l.state.entering_candidates()[0]}
                    elif phase=='cycle':
                        instructions=[widget.cget('text') for widget in app.question.winfo_children()
                                      if isinstance(widget,tk.Label)]
                        self.assertTrue(any('Уже выделенную входящую клетку выбирать повторно не нужно.' in text
                                            for text in instructions))
                        l.selected=set(l.state.cycle(l.entering))-{l.entering}
                    elif phase=='theta':answer=l.state.theta(l.entering)
                    self.assertTrue(l.check(answer)[0])
                    app.refresh()
            self.assertEqual(visited,{'cell','amount','basis','potentials','optimal','enter','cycle','theta','pivot','done'})
        finally:root.destroy()

    def test_manual_balance_and_scaled_selection(self):
        root=tk.Tk();root.withdraw()
        try:
            app=App(root)
            app.edit_problem(Problem(((1,),),(2,),(5,)))
            app.check_balance()
            self.assertEqual(app.setup_note.cget('text'),'Ошибка баланса или исходных данных.')
            app.add_dummy('col')  # Student may choose the wrong side; no automatic correction.
            app.demand_entries[-1].insert(0,'3')
            app.start();self.assertIsNone(app.lesson)
            app.edit_problem(Problem(((1,),),(2,),(5,)))
            app.add_dummy('row')
            self.assertEqual(app.supply_entries[-1].get(),'')
            self.assertEqual(app.setup_note.cget('text'),'')
            app.supply_entries[-1].insert(0,'3')
            app.start();self.assertIsNotNone(app.lesson)
            for zoom in (50,100,150):
                app.zoom.set(zoom);app.change_zoom()
                m=app.matrix
                m.canvas.xview_moveto(0);m.canvas.yview_moveto(0)
                m._click(SimpleNamespace(x=1.5*m.W,y=1.5*m.H))
                self.assertEqual(app.lesson.selected,{(0,0)})
        finally:root.destroy()

    def test_hints_are_explicit_and_reset_for_new_lesson(self):
        root=tk.Tk();root.withdraw()
        try:
            app=App(root)
            app.edit_problem(Problem(((1,),),(5,),(5,)))
            app.start()
            app.check()  # No cell selected: an error must not reveal a hint.
            self.assertEqual(app.feedback,'Ошибка ответа.')
            self.assertEqual(app.lesson.hints,0)
            self.assertEqual(app.hint_label.winfo_manager(),'')
            for count in (1,2):
                app.hint_button.invoke()
                self.assertEqual(app.lesson.hints,count)
                self.assertEqual(app.stat_labels[2].cget('text'),f'1 / {count}')
            app.select((0,0));app.check()
            self.assertEqual(app.hint_label.cget('text'),'')
            self.assertEqual(app.hint_label.winfo_manager(),'')
            self.assertEqual(app.lesson.hints,2)
            app.answer.insert(0,'incorrect');app.check()
            self.assertEqual(app.feedback,'Ошибка ввода.')
            self.assertEqual(app.hint_label.winfo_manager(),'')
            self.assertEqual(app.lesson.hints,2)
            app._setup()
            app.edit_problem(Problem(((1,),),(5,),(5,)))
            app.start()
            self.assertEqual(app.stat_labels[2].cget('text'),'0 / 0')
            self.assertEqual(app.hint_label.winfo_manager(),'')
        finally:root.destroy()

    def test_zoom_controls_preserve_editor_and_selection(self):
        root=tk.Tk()
        try:
            app=App(root)
            root.update_idletasks()
            app.cost_entries[0][0].delete(0,'end')
            app.cost_entries[0][0].insert(0,'123')
            app.zoom_plus.invoke()
            self.assertEqual(app.zoom.get(),110)
            app.zoom_minus.invoke()
            self.assertEqual(app.zoom.get(),100)
            app.zoom_text.set('125%');app.apply_zoom()
            self.assertEqual(app.zoom.get(),125)
            for invalid in ('abc','0','201',''):
                app.zoom_text.set(invalid);app.apply_zoom()
                self.assertEqual(app.zoom.get(),125)
                self.assertEqual(app.zoom_text.get(),'125%')
            app.zoom_fit.invoke()
            self.assertLessEqual(app.editor.inner.winfo_reqwidth(),app.editor.canvas.winfo_width())
            self.assertEqual(app.cost_entries[0][0].get(),'123')
            app.reset_zoom()
            self.assertEqual(app.zoom.get(),100)
            app.edit_problem(Problem(((1,)*8,)*8,(8,)*8,(8,)*8))
            app.start();root.update_idletasks()
            app.select((0,0))
            canvas=app.matrix.canvas
            canvas.xview_moveto(.2);canvas.yview_moveto(.2)
            x,y=80,80
            before=(canvas.canvasx(x)/app.matrix.W,canvas.canvasy(y)/app.matrix.H)
            event=SimpleNamespace(widget=canvas,delta=120,
                                  x_root=canvas.winfo_rootx()+x,y_root=canvas.winfo_rooty()+y)
            self.assertEqual(app.zoom_wheel(event),'break')
            self.assertEqual(app.zoom.get(),110)
            after=(canvas.canvasx(x)/app.matrix.W,canvas.canvasy(y)/app.matrix.H)
            for a,b in zip(before,after):self.assertAlmostEqual(a,b,delta=.03)
            self.assertEqual(app.lesson.selected,{(0,0)})
            app.zoom_fit.invoke()
            width=float(canvas.tk.splitlist(canvas.cget('scrollregion'))[2])
            self.assertLessEqual(width,canvas.winfo_width())
            self.assertEqual(app.lesson.selected,{(0,0)})
            app.notebook.select(1);root.update_idletasks()
            app.zoom_fit.invoke()
            original=app.original_matrix.canvas
            width=float(original.tk.splitlist(original.cget('scrollregion'))[2])
            self.assertLessEqual(width,original.winfo_width())
            app.notebook.select(0)
            app.check()
            app.answer.insert(0,'7')
            app.step_zoom(10);app.reset_zoom()
            self.assertEqual(app.answer.get(),'7')
        finally:root.destroy()

    def test_zoom_does_not_scroll_a_fitting_table(self):
        root=tk.Tk()
        try:
            app=App(root);root.update_idletasks()
            for lesson in (False,True):
                if lesson:
                    app.edit_problem(Problem(((1,)*8,)*8,(8,)*8,(8,)*8))
                    app.start()
                app.change_zoom(50)
                canvas=app.matrix.canvas if lesson else app.editor.canvas
                root.update_idletasks()
                # Zoom from a fitting table to an overflowing one, with the
                # pointer near the far edge (possibly over blank space).
                app.change_zoom(200,anchor=(canvas,canvas.winfo_width()-10,
                                            canvas.winfo_height()-10))
                self.assertEqual(canvas.canvasx(0),0)
                self.assertEqual(canvas.canvasy(0),0)
                canvas.xview_moveto(.5);canvas.yview_moveto(.5)
                app.fit_width()
                self.assertEqual(canvas.canvasx(0),0)
                self.assertEqual(canvas.canvasy(0),0)
                for value in (100,200,50,150,100):
                    app.change_zoom(value)
                    self.assertEqual(canvas.canvasx(0),0)
                    self.assertEqual(canvas.canvasy(0),0)
        finally:root.destroy()

    def test_variant_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'вариант.json'
            for problem in PRESETS.values():
                save_variant(path,problem)
                self.assertEqual(load_variant(path),problem)
            path.write_text('{"costs": [[-1]], "supply": [5], "demand": [5]}',encoding='utf-8')
            with self.assertRaises(ValueError):load_variant(path)


if __name__=='__main__':unittest.main()
