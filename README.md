# NEISS age patterns in sport-associated ED presentations

This University of London DSM050 Data Visualisation project examines how sport- and recreation-associated injuries presenting to US emergency departments vary across the lifespan. It uses National Electronic Injury Surveillance System (NEISS) public-use data from 2016–2025 to investigate five questions about age and recorded sex, injured body regions, diagnosis groups, activity profiles and care outcomes. The prepared data contain 659,637 Core presentations associated with sport and exercise and 978,847 presentations in an Extended cohort that includes broader recreation.

The notebook shows the process from raw-data exploration and cleaning through survey-weighted analysis, visualisation and sensitivity checks. The report explains how cohort definitions, age coding, survey weights and reliability screening affect the findings. These results describe emergency department presentations and their composition. NEISS does not provide participation denominators, so the analysis cannot estimate injury risk or incidence, and product involvement does not establish active participation in sport.

## Key findings

- **Presentations peak in adolescence.** Core presentation estimates peak at age 14 and fall approximately ninefold by age 40. The male and female peaks occur at ages 15 and 14 respectively.
- **The anatomical mix changes with age.** Head and face injuries account for 52% of Core presentations before age five and 13% at ages 45–54. Trunk and spine injuries rise from 6% at ages 5–9 to 32% at age 75 and over.
- **Diagnosis patterns shift across the lifespan.** Strain and sprain reach 29% at ages 15–17 and fall below 10% in the oldest age group. Fracture and internal injury become more prominent after mid-life.
- **Activities have distinct age profiles.** Team sports concentrate around adolescence, while exercise and fitness, weight training and fishing have broader supported age profiles. Only 163 of 255 selected activity-age cells pass the reliability screen, limiting comparisons where data are sparse.
- **Care escalation increases across supported adolescent and adult groups.** The share transferred, admitted, observed or dying in the emergency department rises from 2.0% at ages 10–14 to 13.7% at ages 55–64. Escalation estimates for ages 0–4, 65–74 and 75+ fail the working screen and are omitted from the plotted series. Care outcomes also depend on admission practice and are not a direct severity measure.

## Submission contents

- `report/DSM050_Final_Report_Daniel_da_Cruz.pdf`: final report, 3,478 main-body words.
- `notebooks/DSM050_Final_Project.ipynb`: sequential exploration, cleaning, analysis and interpretation, with saved outputs.
- `data/analysis/`: ten prepared annual datasets, hospital roster and build metadata.
- `data/dictionaries/`: official code labels and declared classifications.
- `data/exploration/`: verified aggregate raw-data profiles.
- Data manifest, quality log and parser rejection CSVs: provenance and cleaning records.
- `src/neiss.py` and `src/raw_eda.py`: functions imported by the notebook.
- `figures/`: exported analytical charts. Raw-data plots are embedded in the notebook and report appendices.
- `tables/`: numerical results explicitly cited by the notebook. Additional diagnostic and sensitivity tables are regenerated when it runs.
- `requirements.txt`: package versions used for the analysis.

## Reproducing the analysis

Use Python 3.12 and install dependencies with `python -m pip install -r requirements.txt`.
Open the analysis notebook in Jupyter or VS Code, select that environment and run its cells in order.
Keep `PREPARE_DATA = False` to use the included prepared data.
Without annual raw files, exploration uses verified saved aggregate profiles and labels this explicitly.

For a raw-data rebuild, obtain the ten annual files from the URLs in `data/data_manifest.csv`,
set `RAW_SOURCE_DIR` to their directory and set `PREPARE_DATA = True` in the notebook.
Expected filenames are `neiss2016.tsv` through `neiss2025.tsv`.
A partial source window raises an error rather than silently omitting years.

[Prepared datasets](https://github.com/Danieldacruz7/dsm050-neiss-age-patterns/tree/main/data/analysis)

Development tests, editing logs, the editable report and the report word-counter notebook
are retained separately by the author and are not part of this submission package.
