# NEISS age patterns in sport-associated ED presentations

DSM050 Data Visualisation coursework, University of London. Study window: 2016–2025.
Core includes fishing; cycling and playground equipment are Extended. Bleachers cannot
establish eligibility. The analysis describes emergency department presentations and their
composition, not injury risk or incidence.

## Project contents

| Location | Purpose |
|---|---|
| `notebooks/DSM050_Final_Project.ipynb` | Sequential data exploration, cleaning, analysis, figures and interpretation |
| `notebooks/DSM050_Report_Word_Count.ipynb` | Report text and the official module word counter |
| `report/DSM050_Report_Revised.docx` and `.pdf` | Editable report and PDF for submission |
| `data/analysis/` | Prepared annual cohorts, hospital roster and provenance |
| `data/exploration/` | Raw-data profiles, missing-value checks and exclusion summaries |
| `data/data_manifest.csv` | Annual source locations and checksums |
| `src/` | Shared analysis, exploration and verification code |
| `figures/` and `tables/` | Saved results and validation records |
| `docs/` | Coursework brief, official counter and supporting documentation |
| `AI_USAGE.md` | AI contribution record |
| `docs/ANALYSIS_FINDINGS.md` and `docs/METHODOLOGY_REVIEW.md` | Supporting results and methodological justification |

## Analysis structure

The notebook introduces the source and research questions, inspects all raw records,
explains the cleaning rules, describes the retained cohorts, then presents each analysis.
Each research-question section places the method before its code and interpretation after
its output. Numerical interpretations identify the supporting saved tables.

Inputs and outputs have separate locations: `data/source/` holds local annual source files,
`data/exploration/` holds checks before cleaning, and `data/analysis/` holds prepared cohorts.
`src/` contains shared Python functions. `tables/` contains numerical results and validation
records, while `figures/` contains exported charts. The notebooks bring these together;
`report/` contains the shorter submission document. Supporting notes explain decisions and
are not additional entry points for running the project.

The analysis notebook is deliberately fuller than the report. Its explanations and data
checks are not constrained by the report word limit. Cached exploration output is identified
as previously saved evidence, not presented as a fresh source-file inspection.

## Environment and execution

Use Python 3.12. From this project folder:

```powershell
$neissEnv = Join-Path $env:LOCALAPPDATA "neiss-env"
py -3.12 -m venv $neissEnv
& "$neissEnv\Scripts\python.exe" -m pip install -r requirements.txt
```

Select that interpreter in the analysis notebook. Python cells run sequentially.
With `PREPARE_DATA = False`, the analysis uses the included prepared cohorts.
Raw exploration reads all ten annual source files when available; otherwise it loads
verified aggregate profiles. A partial set of annual files raises an error.
`RAW_EDA_MODE` can explicitly select `raw` or `cached`.

For a raw-data rebuild, set `RAW_SOURCE_DIR` in the exploration section and
`PREPARE_DATA = True` in the cleaning section, or use:

```powershell
& "$neissEnv\Scripts\python.exe" execute_notebook.py --prepare --raw-dir "C:\path\to\annual-files"
```

The default source directory is `data/source/`. `NEISS_RAW_DIR` or the local
`.runtime/raw_source_dir.txt` can point to files stored elsewhere. Raw files and local
runtime settings are excluded from the packaged project.

The command-line execution and checks are:

```powershell
& "$neissEnv\Scripts\python.exe" execute_notebook.py
& "$neissEnv\Scripts\python.exe" validate_analysis.py
& "$neissEnv\Scripts\python.exe" test_pipeline.py -v
& "$neissEnv\Scripts\python.exe" test_raw_eda.py -v
& "$neissEnv\Scripts\python.exe" verify_artifacts.py
```

`requirements-lock.txt` records the resolved environment. `requirements-executed.txt`
records the versions used for the saved analysis. Verification deliberately fails when
notebooks, reports or outputs have changed since their recorded checks.
`package_project.py` creates a local ZIP only after verification passes.

## Report word count

The official `%%js` counter requires classic Jupyter Notebook and does not work in VS Code.
Its dependencies are separate from the analysis environment:

```powershell
$neissCounterEnv = Join-Path $env:LOCALAPPDATA "neiss-wordcount"
py -3.12 -m venv $neissCounterEnv
& "$neissCounterEnv\Scripts\python.exe" -m pip install -r requirements-wordcount.txt
& "$neissCounterEnv\Scripts\python.exe" -m nbclassic
```

Run the official counter in `notebooks/DSM050_Report_Word_Count.ipynb` after synchronizing
its text with the final report. The analysis notebook includes additional methodological
explanations, so its total Markdown count is not the report word count.

## Submission status

The report versions are synchronized as of 14 September 2026. The unchanged official
counter returned **3,485 report words** in classic Jupyter Notebook. The PDF was exported
with LibreOffice in the background and all 18 pages were visually checked. The analytical
notebook includes additional method explanations and is not the report-count source.
This project uses a different dataset and topic from Coursework 1.

The repository is [dsm050-neiss-age-patterns](https://github.com/Danieldacruz7/dsm050-neiss-age-patterns).
The [prepared analysis data](https://github.com/Danieldacruz7/dsm050-neiss-age-patterns/tree/main/data/analysis)
and notebooks are included in this repository. The author must review the report and AI declaration before submission.
The full submission requirements are in `docs/coursework-requirements.md`.
