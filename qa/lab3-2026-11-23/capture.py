from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'knapsack-practicum'))
from test_acceptance import AcceptanceTests
from presets import PRESETS
from native_snapshot import snapshot
out=Path(__file__).resolve().parent / 'screenshots';out.mkdir(exist_ok=True)
t=AcceptanceTests();t.setUp()
a=t.app
try:
    a.geometry('1100x680');a.update();a._apply_compact_layout()
    a.zoom.set('140%');a.rescale();a.update()
    snapshot(out/'editor-1100x680-140.png')
    a.begin();a.update()
    snapshot(out/'lesson-1100x680-140.png')
    t.complete_tables(PRESETS[0]);a.update()
    snapshot(out/'restore-1100x680-140.png')
    t.finish(PRESETS[0], (1,1,1,1));a.update()
    snapshot(out/'result-1100x680-140.png')
    print('Captured editor, lesson, restore and result at 1100x680, 140%.')
finally:
    t.tearDown()
