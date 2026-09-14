"""Check that the saved execution, numerical validation and report audits are current.

This verifies recorded evidence; it does not execute the analysis or review the prose.
Run after execute_notebook.py and validate_analysis.py.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
from artifact_audit import file_hash, read_json, report_checks, checked_files

status = read_json(ROOT / 'tables/execution_status.json')
assert status.get('status') == 'passed', 'Latest execution did not finish successfully.'
nb_path = ROOT / 'notebooks/DSM050_Final_Project.ipynb'
assert file_hash(nb_path) == status['notebook_sha256'], 'Notebook changed after execution.'
assert checked_files(ROOT, status['artifact_hashes']), 'Execution artifacts changed.'
validation = read_json(ROOT / 'tables/validation_record.json')
assert validation.get('helper_sha256') == file_hash(ROOT / 'src/neiss.py')
assert validation.get('build_metadata_sha256') == file_hash(ROOT / 'data/analysis/build_metadata.json')
assert validation.get('masked_tables_checked', 0) >= 45
assert checked_files(ROOT, validation.get('table_hashes', {})), 'Tables changed since numerical validation.'
nb = read_json(nb_path)
python_cells = [c for c in nb['cells'] if c['cell_type'] == 'code' and not ''.join(c['source']).startswith('%%js')]
assert len(python_cells) == 19
assert [c['execution_count'] for c in python_cells] == list(range(1, 20))
eda_cells = [c for c in python_cells if 'raw-eda' in c.get('metadata', {}).get('tags', [])]
assert len(eda_cells) == 5
assert all(python_cells.index(c) < 6 for c in eda_cells), 'Raw exploration must precede cleaning.'
from raw_eda import load_profiles
load_profiles(ROOT)  # Verify raw provenance, calculation source and aggregate checksums.
assert not any(o['output_type'] == 'error' for c in python_cells for o in c['outputs'])
prepare = next(''.join(c['source']) for c in python_cells if ''.join(c['source']).startswith('PREPARE_DATA ='))
assert prepare.startswith('PREPARE_DATA = False'), 'Submission notebook must use prepared data.'
checks = report_checks(ROOT)
assert checks['official_counter_current'] and checks['pdf_count_current']
assert checks['figures_review_current'] and 3000 <= checks['word_count'] <= 3500
inline_images = sum('image/png' in o.get('data', {}) for c in python_cells for o in c['outputs'])
assert inline_images == 10
result = {'verified_at_utc': datetime.now(timezone.utc).isoformat(),
          'all_python_cells_passed': True, 'python_cell_count': 19, 'inline_figures': inline_images,
          'raw_eda_cells': 5, 'raw_eda_before_cleaning_verified': True,
          'prepared_data_mode': True, 'notebook_sha256': file_hash(nb_path),
          'current_report_checks': checks,
          'execution_status_sha256': file_hash(ROOT / 'tables/execution_status.json'),
          'validation_record_sha256': file_hash(ROOT / 'tables/validation_record.json'),
          'author_and_publication_requirements_complete': False}
(ROOT / 'tables/execution_verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print('Saved execution and report evidence is current; author/publication items remain open.')
