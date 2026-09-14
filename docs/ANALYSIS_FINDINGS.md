# Executed analysis: evidence and review notes

Rebuilt and reviewed with permission on 13 September 2026. These are technical result notes to support
your own interpretation, not prose for the final assessed report. Sources are generated tables
in this folder. Percentages below are weighted unless explicitly called sample percentages.

## Execution and preparation

- All 15 Python cells completed, including fresh-kernel execution with `PREPARE_DATA=False`.
- Eight figures saved and visually inspected. Layout corrections moved the diagnosis legend,
  separated clustering labels from the tree, and reserved space under the activity panels.
- The unchanged official `%%js` cell was subsequently executed on 13 September in classic
  Notebook: 3,453 main-body words. Markdown now matches the edited existing report.
- Runtime: Python 3.12.14; exact package versions in `requirements-executed.txt` and
  `tables/run_record.json`. A clean package installation, dependency check and full fresh-kernel execution passed.
- Core: **659,637** presentations. Extended: **978,847**. These are sample records across ten years.
- Average annual estimated presentations: **2,334,700 Core**, **3,400,700 Extended**.
- The strict parser rejects 16 short fragments (eight broken source records), with no
  narrative text copied to its log. Among complete rows, 78 eligible unknown-age records
  are excluded, including 27 Core. Code 0 is unknown, not an infant. No numeric zero weights
  or invalid design fields remain among structurally complete rows. These updated counters
  supersede the old four-eligible/16-invalid-design description; see `report/review_corrections.json`.
- Fishing is Core. Bleachers cannot establish eligibility; another qualifying product can.
  Cycling and playground equipment remain Extended. Product 3 and other later fields are unused.
- Prepared analytical inputs total about 12.7 MB. The package includes the full observed annual
  hospital roster, dictionaries, manifests and checksums; raw narratives are not copied.

Evidence: `data/data_quality_log.csv`, `data/data_manifest.csv`, `tables/overview_core.csv`,
`tables/overview_extended.csv`, `tables/sample_demographics.csv`.

## Findings to evaluate by research question

| Question | Supported descriptive result | Limitation to retain |
|---|---|---|
| RQ1: age and sex | Core and Extended peak at age 14: approximately 146,800 and 173,000 average annual presentations respectively. Male curve peaks at 15 (99,800); female at 14 (48,100). | These are presentation totals, without participation or population exposure denominators. Age differences are cross-sectional. |
| RQ2: anatomy | Head/face is 52.1% at ages 0–4. Wrist/hand is 22.9% at ages 10–14. Trunk/spine increases from 2.8% at 0–4 to 32.2% at 75+. | Compare composition within each age group. No mechanism or ageing effect is identified. 126/154 cells pass. |
| RQ3: diagnosis | Strain/sprain is 28.6% at 15–17 and 9.6% at 75+. Fracture is 20.6% at 10–14. | 65/66 displayed groups pass. The heterogeneous remainder reaches 52.1% at 65–74: avoid treating it as one clinical diagnosis or ignoring it. |
| RQ4: activities | Several ball-sport curves concentrate in youth; exercise/fitness and fishing show broader supported age coverage. Fishing contributes 11,583 attributed Core records. | Only 163/255 selected activity-age cells pass. A missing segment is not zero presentations. Open-ended 80+ is not a five-year density. |
| RQ5: care outcome | Among known included care outcomes, escalation is 2.0% at 10–14, 5.0% at 35–44 and 13.7% at 55–64. | Escalation at 0–4, 65–74 and 75+ fails the estimate CV screen. Do not claim a measured trend over the whole lifespan. 9,701 Core records are outside this outcome denominator. |

Evidence: `tables/rq1_age_*.csv`, `tables/rq2_anatomy.csv`, `tables/rq3_diagnosis.csv`,
`tables/rq4_profiles.csv`, `tables/rq4_activity_selection.csv`, `tables/rq5_care_outcome.csv`.

## Clustering and adequacy

- Ten of 15 selected activities have all three broad age and five broad anatomy features passing.
- Excluded: Combat sports, Gymnastics/cheerleading, Volleyball, Snow sports and Hockey.
- Ward's four-group cut places Exercise/fitness with Weight training; Fishing alone;
  Basketball/Football/Other sport-recreation/Soccer together; and
  Baseball-softball/Other ball sports/Swimming-diving together.
- Ward versus average linkage pairwise agreement: **77.8%**. Read the membership table:
  average linkage merges several youth activities and separates Swimming/diving. Do not call
  the complete partition robust to linkage.
- On the nine common passing activities, full-window and through-2023 Ward partitions agree
  on every pair. This is conditional on refitting the same nine activities; Other ball sports
  is absent from that comparison. It does not establish population-level cluster validity.
- Full joint cells (15 activities × 11 age bands × 14 body regions): **396/2,310 pass (17.1%)**.
  Adequate marginal clustering features do not imply adequate age-by-anatomy combinations.
  The current RQ4 code supports profile comparisons, not a complete joint interaction analysis.

Evidence: `tables/rq4_cluster_selection.csv`, `tables/rq4_cluster_membership.csv`,
`tables/sensitivity_clustering_window.csv`, `tables/rq4_joint_cell_coverage.csv` and
`tables/rq4_joint_cell_adequacy.csv`. The joint audit is reproducible with `validate_analysis.py`.

## Sensitivity results that change interpretation

Maximum absolute percentage-point differences, using cells passing both relevant screens:

| Comparison | RQ1 age | RQ2 anatomy | RQ3 diagnosis | RQ4 profiles | RQ5 outcomes |
|---|---:|---:|---:|---:|---:|
| Extended versus Core | 1.34 | 6.71 | 17.81 | 1.78 | 3.08 |
| Through 2023 versus full window | 0.08 | 0.69 | 1.76 | 1.61 | 0.65 |
| Unweighted sample versus weighted | 1.23 | 3.19 | 3.08 | 6.37 | 1.06 |
| Equal-year mean versus pooled | 0.07 | 0.24 | 0.38 | 0.58 | 0.15 |

- Through-2023 comparison coverage: 91/91, 122/154, 65/66, 156/255 and 19/22 cells,
  respectively. Missing comparison cells are not evidence of no change.
- Extended RQ4 compares the same Core-selected activity families. It does not show that adding
  cycling/playground leaves the overall activity mix unchanged.
- Equal-year RQ4 comparison covers only 121/255 cells (47.5%): the small maximum is conditional.
- Product-1-only composition changes remain below 0.58 points; excluding 2020 below 0.59 points,
  across compared cells. Consult the table for exact coverage.
- Through-2023 versus full-window age-specific burden differs by up to about 4,100 average
  annual presentations; excluding 2020 by up to about 8,700. These are cellwise maxima, not totals.
- Pooled proportions do not cancel year-specific scaling. Even within-year proportions cancel
  only a common multiplicative factor, not arbitrary hospital-specific reweighting.

Evidence: `tables/sensitivity_summary.csv` and the scenario-specific tables. These descriptive
checks do not test whether the sample change caused a difference or prove that weights are correct.

## Method and submission verdict

The five questions fit this descriptive dataset under the stated scope. The analysis now runs,
retains the appropriate denominators, screens plotted values and records sensitivity coverage.
Annual variance remains an approximation; the cross-year SE bound is conservative relative to
that approximation, not guaranteed protection against every uncertainty source. The adapted
average-annual display rule still needs a clear methodological justification in your own report.

CPSC lists unstable-estimate thresholds of 20 cases, 1,200 estimated presentations and CV 33%:
[official explanation](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Explanation-Of-NEISS-Estimates-Obtained-Through-The-CPSC-Website).
The official 2024 report documents the sample change and its own backcasting approach on page 7:
[CPSC report](https://www.cpsc.gov/s3fs-public/Death_and_Injury_Report_2024.pdf).
This project does not perform that backcasting. Both sources were checked on 12 September 2026.

Report completion update, 13 September 2026:

The existing report has been edited and exported with eight current figures. Its discussion
is synchronized into notebook Markdown. Counts are verified: official counter 3,453; Word
3,327. Section 3.3 now explains the uncertainty approximation and adapted screen; see also
`docs/METHODOLOGY_REVIEW.md`. The original Desktop report remains unchanged.

Still required: the author's review and confirmation that this differs from coursework 1;
repository publication, actual repository/data URLs and marker-access checks; final Moodle
submission. The repository exists; uploads are paused by user instruction. See the submission status in `README.md`.

The coursework prohibits AI-written entire final-report sections. The assistant edited the
existing author's report and disclosed those edits; the author must personally review the
submitted text. Assistant checks do not substitute for personal verification.
