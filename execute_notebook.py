"""Execute Python cells in a fresh kernel; preserve the browser-only official counter."""
import argparse
import json
import os
from pathlib import Path
import sys
import time
from datetime import datetime, timezone

parser = argparse.ArgumentParser()
parser.add_argument('--prepare', action='store_true')
parser.add_argument('--raw-dir', type=Path, help='Directory containing neiss2016.tsv through neiss2025.tsv')
args = parser.parse_args()
root = Path(__file__).resolve().parent
sys.path.insert(0, str(root / 'src'))
from artifact_audit import file_hash, markdown_hash, counter_hash, read_json
if args.raw_dir:
    os.environ['NEISS_RAW_DIR'] = str(args.raw_dir.resolve())
for key, folder in [('IPYTHONDIR', 'ipython'), ('JUPYTER_CONFIG_DIR', 'jupyter'),
                    ('JUPYTER_RUNTIME_DIR', 'runtime'), ('JUPYTER_DATA_DIR', 'jupyter-data'),
                    ('MPLCONFIGDIR', 'matplotlib')]:
    location = root / '.runtime' / folder
    location.mkdir(parents=True, exist_ok=True)
    os.environ[key] = str(location)
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

path = root / 'notebooks/DSM050_Final_Project.ipynb'
nb = nbformat.read(path, as_version=4)
counter_audit = read_json(root / 'report/word_counter_verification.json')
counter_current = (markdown_hash(nb) == counter_audit.get('analysis_markdown_sha256')
                   and counter_hash(nb) == counter_audit.get('counter_source_sha256'))
for cell in nb.cells:
    if cell.cell_type == 'code':
        if cell.source.startswith('%%js'):
            cell.metadata['tags'] = ['browser-only']
            if not counter_current:
                cell.outputs = []
                cell.execution_count = None
            continue  # Preserve only a counter verified against this Markdown.
        cell.outputs = []
        cell.execution_count = None
        if cell.source.startswith('PREPARE_DATA ='):
            cell.source = cell.source.replace('PREPARE_DATA = False', 'PREPARE_DATA = True') if args.prepare else cell.source.replace('PREPARE_DATA = True', 'PREPARE_DATA = False')

def progress(cell, cell_index, **kwargs):
    print(f'CELL {cell_index}: {cell.source.splitlines()[0][:100]}', flush=True)

manager = KernelManager(kernel_name='python3')
manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
client = NotebookClient(nb, km=manager, timeout=1800, resources={'metadata': {'path': str(root)}},
                        skip_cells_with_tag='browser-only', on_cell_start=progress)
start = time.time()
status_path = root / 'tables/execution_status.json'
status_path.parent.mkdir(exist_ok=True)
status = {'status': 'running', 'started_at_utc': datetime.now(timezone.utc).isoformat(),
          'raw_rebuild': args.prepare, 'python_executable': sys.executable}
status_path.write_text(json.dumps(status, indent=2), encoding='utf-8')
try:
    client.execute()
    status['status'] = 'passed'
except BaseException as error:
    status.update(status='failed', error_type=type(error).__name__, error=str(error)[-2000:])
    raise
finally:
    nbformat.write(nb, path)
    status.update(elapsed_seconds=round(time.time()-start, 2),
                  finished_at_utc=datetime.now(timezone.utc).isoformat(),
                  notebook_sha256=file_hash(path))
    if status['status'] == 'passed':
        files = [root / 'src/neiss.py', root / 'src/raw_eda.py', root / 'src/artifact_audit.py', root / 'execute_notebook.py',
                 root / 'data/analysis/build_metadata.json',
                 root / 'data/data_manifest.csv', root / 'tables/run_record.json']
        files += sorted((root / 'figures').glob('*.png'))
        files += sorted((root / 'data/exploration').glob('*.*'))
        status['artifact_hashes'] = {str(p.relative_to(root)).replace('\\', '/'): file_hash(p) for p in files}
    status_path.write_text(json.dumps(status, indent=2), encoding='utf-8')
    print(f'Saved notebook; elapsed {time.time()-start:.1f}s', flush=True)
print('ALL PYTHON CELLS PASSED; browser counter intentionally not executed.', flush=True)
