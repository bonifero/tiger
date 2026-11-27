"""Build offline executable; use available project-local PyInstaller."""
from pathlib import Path
import sys
import shutil

ROOT = Path(__file__).resolve().parent
for deps in (ROOT / '.build-deps', ROOT.parent / 'ktz-practicum/.build-deps'):
    if deps.exists():
        sys.path.insert(0, str(deps))

if __name__ == '__main__':
    from variant_files import load_variants
    load_variants(ROOT / 'variants')
    import PyInstaller.__main__
    PyInstaller.__main__.run(['--noconfirm', '--clean', '--onefile', '--windowed', '--name', 'Games-Practicum',
                               '--distpath', str(ROOT / 'dist'), '--workpath', str(ROOT / '.build'),
                               '--specpath', str(ROOT), str(ROOT / 'app.py')])
    shutil.copytree(ROOT / 'variants', ROOT / 'dist' / 'variants', dirs_exist_ok=True)
    destination = ROOT / 'Игры-Практикум.exe'
    shutil.copy2(ROOT / 'dist' / 'Games-Practicum.exe', destination)
    print('Built:', destination)
