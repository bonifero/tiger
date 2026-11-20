"""Build offline executable; use available project-local PyInstaller."""
from pathlib import Path
import sys
import shutil

ROOT=Path(__file__).resolve().parent
for deps in (ROOT/'.build-deps',ROOT.parent/'ktz-practicum/.build-deps'):
    if deps.exists():sys.path.insert(0,str(deps))

if __name__=='__main__':
    import PyInstaller.__main__
    PyInstaller.__main__.run(['--noconfirm','--clean','--onefile','--windowed','--name','LP-Practicum',
                             '--distpath',str(ROOT/'dist'),'--workpath',str(ROOT/'.build'),
                             '--specpath',str(ROOT),str(ROOT/'app.py')])
    shutil.copy2(ROOT/'dist/LP-Practicum.exe',ROOT/'ЛП-Практикум.exe')
    print('Built:',ROOT/'ЛП-Практикум.exe')
