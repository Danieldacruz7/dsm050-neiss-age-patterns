"""Exercise the actual notebook profiling cell against deliberately dirty raw input."""
import csv
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
import neiss
import raw_eda


class RawExplorationTests(unittest.TestCase):
    def test_profiles_keep_dirty_records_and_preview_cleaning(self):
        notebook = json.loads((ROOT / 'notebooks/DSM050_Final_Project.ipynb').read_text(encoding='utf-8'))
        cell = next(c for c in notebook['cells'] if
                    'raw-eda-calculation' in c.get('metadata', {}).get('tags', []))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'neiss2016.tsv'
            rows = []
            # One unknown age, one zero weight, one wrong-year date, one valid infant,
            # two identical good records. Exploration must not silently remove them.
            for i in range(6):
                row = dict.fromkeys(neiss.SCHEMA, '')
                row.update(CPSC_Case_Number=str(i), Treatment_Date='01/01/2016', Age='20',
                           Sex='1', Body_Part='0', Diagnosis='57', Disposition='1',
                           Product_1='3223', Product_2='0', Stratum='L', PSU='1', Weight='5')
                rows.append(row)
            rows[0]['Age'] = '0'
            rows[1]['Weight'] = '0'
            rows[2]['Treatment_Date'] = '01/01/2015'
            rows[3]['Age'] = '201'
            rows[5] = rows[4].copy()
            with path.open('w', newline='', encoding='utf-8') as stream:
                writer = csv.writer(stream, delimiter='\t')
                writer.writerow(neiss.SCHEMA)
                writer.writerows([[r[k] for k in neiss.SCHEMA] for r in rows])
                writer.writerow(['broken', 'fragment'])
            before = path.read_bytes()
            namespace = dict(READ_RAW_EDA=True, YEARS=[2016], raw_paths=[path],
                PROJECT_ROOT=ROOT, neiss=neiss, pd=pd, np=np, display=lambda *args: None,
                raw_eda=SimpleNamespace(TABLE_NAMES=raw_eda.TABLE_NAMES, save_profiles=lambda *args: None))
            exec(''.join(cell['source']), namespace)
            profiles = namespace['raw_profiles']
            summary = profiles['annual'].iloc[0]
            self.assertEqual(summary.rows, 6)
            self.assertEqual(summary.rejected_fragments, 1)
            self.assertEqual(summary.unknown_age_code_0, 1)
            self.assertEqual(summary.zero_weight, 1)
            self.assertEqual(summary.invalid_date_or_year, 1)
            self.assertEqual(summary.infant_month_codes, 1)
            self.assertEqual(summary.duplicate_id_rows, 2)
            self.assertEqual(summary.exact_duplicate_rows, 1)
            self.assertEqual(profiles['flow'].set_index('stage').remaining_n['Then valid treatment year'], 3)
            age_field = profiles['fields'].set_index('field').loc['Age']
            self.assertEqual(age_field.blank_n, 0)
            self.assertEqual(profiles['codes'].query("field == 'Body_Part'").iloc[0].label, 'INTERNAL')
            self.assertEqual(path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
