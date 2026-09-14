"""Create a verified local ZIP. This script never contacts or uploads to GitHub."""
from pathlib import Path
import os
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
subprocess.run([sys.executable, str(ROOT / 'verify_artifacts.py')], check=True)
destination = ROOT.parent / f'{ROOT.name}.zip'
temporary = destination.with_suffix('.pending.zip')
excluded = {'.runtime', '.venv', '.wordcount-venv', '__pycache__', '.ipynb_checkpoints', '.git'}
files = []
for folder, dirs, names in os.walk(ROOT):
    dirs[:] = sorted(d for d in dirs if d not in excluded)
    relative = Path(folder).relative_to(ROOT)
    if relative == Path('data/source'):
        dirs[:] = []
        continue
    for name in sorted(names):
        if name not in {'Thumbs.db', '.DS_Store'} and not name.endswith(('.pyc', '.pyo')):
            files.append(Path(folder) / name)
with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for path in files:
        archive.write(path, str(Path(ROOT.name) / path.relative_to(ROOT)))
with zipfile.ZipFile(temporary) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    assert sum('/data/analysis/cohort_' in name and name.endswith('.csv.gz') for name in names) == 10
    assert sum('/figures/figure_' in name and name.endswith('.png') for name in names) == 8
    assert not any('/.runtime/' in name or '/data/source/' in name for name in names)
temporary.replace(destination)
print(f'Packaged {len(files)} files; {destination.stat().st_size:,} bytes; CRC checks passed.')
print(destination)
