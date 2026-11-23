"""Build the standalone Windows application and include editable task files."""
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    if sys.platform != 'win32':
        raise SystemExit('Windows EXE нужно собирать на Windows. Используйте workflow «Загрузка рюкзака — tests / EXE».')
    root = Path(__file__).resolve().parent
    subprocess.run([sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean',
                    '--onefile', '--windowed', '--name', 'Knapsack-Practicum',
                    '--distpath', str(root / 'dist'), '--workpath', str(root / '.build'),
                    str(root / 'app.py')], cwd=root, check=True)
    shutil.copytree(root / 'variants', root / 'dist' / 'variants', dirs_exist_ok=True)
    shutil.copy2(root / 'README.md', root / 'dist' / 'README.md')
    shutil.copytree(root / 'docs', root / 'dist' / 'docs', dirs_exist_ok=True)


if __name__ == '__main__':
    main()
