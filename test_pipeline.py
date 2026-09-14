"""Regression tests for source coding, malformed input and audit invalidation.

Run with python -m unittest test_pipeline -v. No study files are modified.
"""
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
import neiss
from artifact_audit import markdown_hash, report_checks, counter_hash, file_hash


class PipelineTests(unittest.TestCase):
    def test_official_age_coding(self):
        raw = pd.Series([0, 1, 2, 114, 115, 116, 200, 201, 211, 212, 223, 224, 999,
                         np.nan, 'bad', 12.5, 201.5])
        actual = neiss.decode_age(raw)
        self.assertEqual(actual.notna().tolist(),
                         [False, False, True, True, True, False, False, True, True,
                          True, True, False, False, False, False, False, False])
        np.testing.assert_allclose(actual.dropna(), [2, 114, 115, 1/12, 11/12, 1, 23/12])
        self.assertEqual(np.floor(actual.iloc[7]), 0)  # Actual infant, not unknown age.

    def test_parser_rejects_both_widths_and_preserves_quoted_fields(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'toy.tsv'
            good = ['x'] * len(neiss.SCHEMA)
            good[21] = 'quoted\ttab and\nnewline'
            with path.open('w', newline='', encoding='utf-8') as stream:
                writer = csv.writer(stream, delimiter='\t')
                writer.writerows([neiss.SCHEMA, good + ['extra'], good[:-1], good])
            frame, encoding, rejected = neiss.read_raw(path)
            self.assertEqual(len(frame), 1)
            self.assertEqual(frame.Narrative_1.iloc[0], good[21])
            self.assertEqual([r['field_count'] for r in rejected], [26, 24])
            self.assertTrue(all(r['case_number'] == '' for r in rejected))

    def test_counter_invalidates_on_markdown_edit_only(self):
        nb = {'cells': [{'cell_type': 'markdown', 'source': 'body'},
                        {'cell_type': 'code', 'source': 'print(1)'},
                        {'cell_type': 'markdown', 'source': '## Word Count\n123'}]}
        initial = markdown_hash(nb)
        nb['cells'][1]['source'] = 'print(2)'
        nb['cells'][2]['source'] = '## Word Count\n456'
        self.assertEqual(initial, markdown_hash(nb))
        nb['cells'][0]['source'] = 'changed body'
        self.assertNotEqual(initial, markdown_hash(nb))
        with tempfile.TemporaryDirectory() as folder:
            self.assertFalse(report_checks(folder)['official_counter_current'])

    def test_changed_counter_cannot_reuse_audit(self):
        nb = {'cells': [{'cell_type': 'markdown', 'source': 'body'},
                        {'cell_type': 'code', 'source': '%%js\noriginal counter'}]}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'report').mkdir(); (root/'notebooks').mkdir()
            report = root/'report/DSM050_Report_Revised.docx'
            report.write_bytes(b'fixture report')
            path = root/'notebooks/DSM050_Report_Word_Count.ipynb'
            path.write_text(json.dumps(nb), encoding='utf-8')
            audit = {'source_report_sha256': file_hash(report),
                     'report_markdown_sha256': markdown_hash(nb),
                     'counter_source_sha256': counter_hash(nb)}
            (root/'report/word_counter_verification.json').write_text(json.dumps(audit),encoding='utf-8')
            self.assertTrue(report_checks(root)['official_counter_current'])
            # Extra analysis commentary does not change the report's word count.
            analysis = root/'notebooks/DSM050_Final_Project.ipynb'
            analysis.write_text(json.dumps({'cells': [{'cell_type': 'markdown',
                'source': 'Additional exploration and explanation'}]}), encoding='utf-8')
            self.assertTrue(report_checks(root)['official_counter_current'])
            original_body = nb['cells'][0]['source']
            nb['cells'][0]['source'] = 'Changed report prose'
            path.write_text(json.dumps(nb), encoding='utf-8')
            self.assertFalse(report_checks(root)['official_counter_current'])
            nb['cells'][0]['source'] = original_body
            nb['cells'][1]['source'] = '%%js\nmodified counter'
            path.write_text(json.dumps(nb), encoding='utf-8')
            self.assertFalse(report_checks(root)['official_counter_current'])


if __name__ == '__main__':
    unittest.main()
