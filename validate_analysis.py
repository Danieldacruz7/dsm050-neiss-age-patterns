"""Independent numerical checks and a joint-cell adequacy audit after execution."""
from pathlib import Path
import json
import sys
from datetime import datetime, timezone
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
import neiss

data, roster = neiss.load_data()
core = data.loc[data.In_Core].copy()
core['Activity'] = core.Activity_Core
checks = {}
checks['verified_at_utc'] = datetime.now(timezone.utc).isoformat()
checks['helper_sha256'] = neiss.sha256(ROOT / 'src/neiss.py')
checks['build_metadata_sha256'] = neiss.sha256(ROOT / 'data/analysis/build_metadata.json')
assert core.Age_Raw.ne(0).all() and data.Age_Raw.ne(0).all()
checks['unknown_age_not_misclassified_as_infant'] = True

# Reconstruct all five estimands directly from records, without domain_summary.
# This also checks that a selected activity catalog does not shrink denominators.
core['Age_Display'] = core.Age_Integer.clip(upper=90)
care = core.loc[core.Disposition.isin(neiss.RELEASED | neiss.ESCALATED)].copy()
care['Care_Outcome'] = np.where(care.Disposition.isin(neiss.ESCALATED), 'Escalated', 'Released')
specs = [
    ('rq1_age_core', core, ['Age_Display'], []),
    ('rq2_anatomy', core, ['Body_Region', 'Age_Band'], ['Age_Band']),
    ('rq3_diagnosis', core, ['Diagnosis_Plot', 'Age_Band'], ['Age_Band']),
    ('rq4_profiles', core, ['Activity', 'Profile_Age'], ['Activity']),
    ('rq5_care_outcome', care, ['Care_Outcome', 'Age_Band'], ['Age_Band']),
]
for name, frame, keys, den in specs:
    saved = pd.read_csv(ROOT / f'tables/{name}.csv')
    grouped = frame.groupby(keys, observed=True).Weight.agg(actual_n='size', numerator='sum').reset_index()
    joined = saved.merge(grouped, on=keys, how='left').fillna({'actual_n': 0, 'numerator': 0})
    if den:
        totals = frame.groupby(den, observed=True).Weight.sum().rename('denominator').reset_index()
        joined = joined.merge(totals, on=den, how='left')
    else:
        joined['denominator'] = frame.Weight.sum()
    assert joined.n.eq(joined.actual_n).all(), name
    passing = joined.loc[joined.reportable]
    assert np.allclose(passing.percent, (100 * passing.numerator / passing.denominator).round(1)), name
    assert np.allclose(passing.estimate_rounded, (passing.numerator / 10).round(-2)), name
    checks[f'{name}_independent_counts_totals_and_denominators'] = True

# Independently sum record weights and compare with the published rounded totals.
for label, frame in [('core', core), ('extended', data)]:
    saved = pd.read_csv(ROOT / f'tables/overview_{label}_annual_diagnostics.csv')
    actual = frame.groupby('Source_Year').Weight.sum().round(-2)
    observed = saved.set_index('Source_Year').estimate
    assert np.allclose(actual.loc[observed.index], observed)
    checks[f'{label}_annual_weight_mass_balance'] = True

# Known artificial design: two hospitals in each of five strata, two repeated years.
# Each year has hospital totals 10 and 20 within every stratum. Annual variance = 500.
toy = pd.DataFrame([
    {'Source_Year': year, 'Stratum': stratum, 'PSU': 2*i+j+1,
     'Weight': weight, 'All': 'All', 'Group': 'A' if j == 0 else 'B'}
    for year in [2016, 2017] for i, stratum in enumerate(neiss.STRATA)
    for j, weight in enumerate([10., 20.])
])
design = toy[['Source_Year', 'Stratum', 'PSU']].drop_duplicates()
t, a = neiss.domain_summary(toy, design, ['All'], years=[2016, 2017])
assert np.isclose(t.estimate.iloc[0], 150.)
assert np.isclose(t.se_bound.iloc[0], np.sqrt(500.))
g, _ = neiss.domain_summary(toy, design, ['Group'], denominator=[], years=[2016, 2017])
assert np.allclose(g.percent, [100/3, 200/3])
# For A the residuals per stratum are +20/3 and -20/3.
assert np.isclose(g.percent_se_bound.iloc[0], np.sqrt(5*1600/9)/150*100)
checks['known_design_totals_variance_and_ratio_covariance'] = True

# Joint cells are stricter than the marginal age/anatomy features used by clustering.
selection = pd.read_csv(ROOT / 'tables/rq4_activity_selection.csv')
activities = selection.loc[selection.selected, 'Activity'].tolist()
catalog = pd.MultiIndex.from_product([activities, neiss.AGE_LABELS, neiss.REGION_ORDER],
                                    names=['Activity', 'Age_Band', 'Body_Region'])
joint, _ = neiss.domain_summary(core, roster, list(catalog.names),
                               denominator=['Activity', 'Age_Band'], catalog=catalog,
                               years=neiss.YEARS)
neiss.report_table(joint).to_csv(ROOT / 'tables/rq4_joint_cell_adequacy.csv', index=False)
coverage = joint.groupby('Activity', observed=True).reportable.agg(['sum', 'size'])
coverage.columns = ['passing_joint_cells', 'total_joint_cells']
coverage.to_csv(ROOT / 'tables/rq4_joint_cell_coverage.csv')
# Include the newly written joint audit in the mask check.
checked = 0
for path in (ROOT / 'tables').glob('*.csv'):
    table = pd.read_csv(path)
    if 'reportable' in table:
        numeric = [c for c in ['estimate', 'estimate_rounded', 'percent'] if c in table]
        assert table.loc[~table.reportable, numeric].isna().all().all(), path.name
        checked += 1
checks['masked_tables_checked'] = checked
checks['joint_cells_passing'] = int(joint.reportable.sum())
checks['joint_cells_total'] = len(joint)
checks['core_n'] = len(core)
checks['extended_n'] = len(data)
checks['care_denominator_exclusions'] = int((~core.Disposition.isin(neiss.RELEASED | neiss.ESCALATED)).sum())
checks['main_table_coverage'] = {}
for name in ['rq1_age_core', 'rq2_anatomy', 'rq3_diagnosis', 'rq4_profiles', 'rq5_care_outcome']:
    table = pd.read_csv(ROOT / f'tables/{name}.csv')
    checks['main_table_coverage'][name] = {'passing': int(table.reportable.sum()), 'total': len(table)}
for label in ['core', 'extended', 'male', 'female']:
    age = pd.read_csv(ROOT / f'tables/rq1_age_{label}.csv').query('Age_Display < 90 and reportable')
    peak = age.loc[age.estimate.idxmax()]
    checks[f'{label}_peak_age'] = int(peak.Age_Display)
    checks[f'{label}_peak_annual_estimate'] = float(peak.estimate)
checks['prepared_data_megabytes'] = sum(p.stat().st_size for p in (ROOT / 'data/analysis').iterdir()) / 1e6
checks['table_hashes'] = {str(p.relative_to(ROOT)).replace('\\', '/'): neiss.sha256(p)
                        for p in sorted((ROOT / 'tables').glob('*.csv'))}
(ROOT / 'tables/validation_record.json').write_text(json.dumps(checks, indent=2), encoding='utf-8')
print(json.dumps(checks, indent=2))
