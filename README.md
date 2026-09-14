# NEISS age patterns in sport-associated ED presentations

DSM050 Data Visualisation coursework, University of London. Study window: 2016–2025.
The analysis describes emergency department presentations and their composition, not risk or incidence.

## Submission contents

- `report/DSM050_Report_Revised.pdf`: final report, 3,485 main-body words.
- `notebooks/DSM050_Final_Project.ipynb`: sequential exploration, cleaning, analysis and interpretation, with saved outputs.
- `data/analysis/`: ten prepared annual datasets, hospital roster and build metadata.
- `data/dictionaries/`: official code labels and declared classifications.
- `data/exploration/`: verified aggregate raw-data profiles.
- Data manifest, quality log and parser rejection CSVs: provenance and cleaning records.
- `src/neiss.py` and `src/raw_eda.py`: functions imported by the notebook.
- `figures/`: exported analytical charts. Raw-data plots are embedded in the notebook and report appendices.
- `tables/`: numerical results explicitly cited by the notebook. Additional diagnostic and sensitivity tables are regenerated when it runs.
- `requirements.txt`: package versions used for the analysis.
- `AI_USAGE.md`: AI assistance declaration and retained history.

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
