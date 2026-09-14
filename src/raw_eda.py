"""Integrity checks for aggregate raw-data exploration; no cohort cleaning here."""
import json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import neiss

TABLE_NAMES = ['annual', 'fields', 'codes', 'weights', 'age_counts', 'flow']


def calculation_hash(notebook):
    cells = json.loads(Path(notebook).read_text(encoding='utf-8'))['cells']
    sources = [''.join(c['source']) for c in cells
               if 'raw-eda-calculation' in c.get('metadata', {}).get('tags', [])]
    if len(sources) != 1:
        raise ValueError('Expected exactly one raw exploration calculation cell.')
    import hashlib
    return hashlib.sha256(sources[0].encode('utf-8')).hexdigest()


def save_profiles(root, profiles, source_hashes):
    folder = root / 'data/exploration'
    folder.mkdir(parents=True, exist_ok=True)
    marker = folder / 'metadata.json'
    marker.unlink(missing_ok=True)
    for name in TABLE_NAMES:
        profiles[name].to_csv(folder / f'{name}.csv', index=False)
    marker.write_text(json.dumps({
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'All structurally readable annual raw records, before cohort cleaning',
        'years': neiss.YEARS, 'source_hashes': source_hashes,
        'parser_helper_sha256': neiss.sha256(neiss.__file__),
        'cache_helper_sha256': neiss.sha256(__file__),
        'calculation_sha256': calculation_hash(root / 'notebooks/DSM050_Final_Project.ipynb'),
        'dictionary_hashes': neiss.dictionary_fingerprint(),
        'tables': {name: neiss.sha256(folder / f'{name}.csv') for name in TABLE_NAMES},
    }, indent=2), encoding='utf-8')


def load_profiles(root):
    folder = root / 'data/exploration'
    meta = json.loads((folder / 'metadata.json').read_text(encoding='utf-8'))
    expected = {
        'years': neiss.YEARS, 'parser_helper_sha256': neiss.sha256(neiss.__file__),
        'cache_helper_sha256': neiss.sha256(__file__),
        'calculation_sha256': calculation_hash(root / 'notebooks/DSM050_Final_Project.ipynb'),
        'dictionary_hashes': neiss.dictionary_fingerprint(),
    }
    for key, value in expected.items():
        if meta.get(key) != value:
            raise ValueError(f'Raw EDA cache is stale ({key}); rerun using annual source files.')
    manifest = pd.read_csv(root / 'data/data_manifest.csv')
    if meta['source_hashes'] != dict(zip(manifest.source_file, manifest.source_sha256)):
        raise ValueError('EDA and prepared cohorts refer to different raw source files.')
    for name in TABLE_NAMES:
        if neiss.sha256(folder / f'{name}.csv') != meta['tables'][name]:
            raise ValueError(f'Raw EDA table changed: {name}')
    return {name: pd.read_csv(folder / f'{name}.csv') for name in TABLE_NAMES}
