"""Run macOS pointer/navigation scenarios and capture only this process's window."""
from pathlib import Path
import sys
import tempfile
from tkinter import ttk
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'knapsack-practicum'))
sys.path.insert(0, str(ROOT / 'qa/lab3-2026-11-23'))
from test_usability import UsabilityTests, widgets
from presets import PRESETS
from formats import load
from native_snapshot import snapshot

out = Path(__file__).resolve().parent
case = UsabilityTests()
case.setUp()
a = case.app

def click(button):
    a.update()
    button.event_generate('<Enter>')
    button.event_generate('<ButtonPress-1>', x=12, y=12)
    button.event_generate('<ButtonRelease-1>', x=12, y=12)
    a.update()

def capture(path):
    a.update()
    snapshot(path)

def button(label):
    return next(w for w in widgets(a) if isinstance(w, ttk.Button) and w.cget('text') == label)

try:
    a.geometry('1280x820'); a.update(); a._apply_compact_layout(); a.update()
    a.preset_box.current(1)
    a.preset_box.event_generate('<<ComboboxSelected>>'); a.update()
    assert a.problem == PRESETS[1]
    a.set_problem(PRESETS[0]); a.update()
    capture(out / '01-editor.png')
    a.geometry('1024x700'); a.update(); a._apply_compact_layout(); a.update()
    a.limit_var.set('6'); click(button('Применить лимиты'))
    grid = a.editor_grid
    matrix = [[str(v) for v in row] + ['40', '45'] for row in PRESETS[0].values]
    matrix[0][0] = '5'
    a.clipboard_clear(); a.clipboard_append('\r\n'.join('\t'.join(row) for row in matrix))
    grid.selected = (0, 3); grid._start_edit(); grid.entry.focus_force(); a.update()
    grid.entry.event_generate('<Command-KeyPress-v>'); a.update()
    assert [row[3:] for row in grid.get_rows()] == matrix
    click(a.begin_button)
    assert a.screen == 'editor' and (0, 3) in grid.invalid
    capture(out / '02-paste-validation.png')
    grid.set_value(0, 3, '0')
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'custom.json'
        with patch('app.filedialog.asksaveasfilename', return_value=str(path)), \
             patch('app.simpledialog.askstring', return_value='Мой вариант'):
            click(button('Сохранить'))
        assert load(path).name == 'Мой вариант'
        assert a.name_var.get() == 'Мой вариант'
    a.set_problem(PRESETS[0]); a.update(); click(a.begin_button)
    click(a.check_button); click(button('Подсказка'))
    lesson, errors, hint = a.lesson, a.lesson.errors, a.hint_var.get()
    a.answer_grid.set_value(0, 1, '123')
    rows = a.answer_grid.get_rows()
    click(a.nav_buttons[0]); assert a.lesson is lesson
    click(a.nav_buttons[1])
    assert a.lesson is lesson and a.lesson.errors == errors and a.hint_var.get() == hint
    assert a.answer_grid.get_rows() == rows
    capture(out / '03-resumed-lesson.png')
    click(a.nav_buttons[0]); a.editor_grid.set_value(0, 4, '12')
    assert a.lesson is None and a.nav_buttons[1].instate(['disabled'])
    capture(out / '04-invalidated-lesson.png')
    a.set_problem(PRESETS[0]); a.update(); click(a.begin_button)
    case.accept_table(); case.accept_table(); a.update()
    capture(out / '05-reference.png')
    while a.lesson.phase in ('candidates', 'summary'):
        case.accept_table()
    a.zoom.set('140%'); a.rescale(); a.update()
    capture(out / '06-restore-140.png')
    for i in range(4):
        a.answer_grid.set_value(0, i+1, i)
        a.answer_grid.set_value(1, i+1, 1)
    click(a.check_button); assert a.final_plan == (1, 1, 1, 1)
    a.zoom.set('100%'); a.rescale(); a.update()
    capture(out / '07-result.png')
    report = a.report_text()
    click(a.nav_buttons[0]); click(a.nav_buttons[2])
    assert a.report_text() == report
    print('PASS: example selection event, pointer actions, Excel paste, F(0) validation, save/rename, progress resume/invalidation, complete lab and result return.')
finally:
    case.tearDown()
