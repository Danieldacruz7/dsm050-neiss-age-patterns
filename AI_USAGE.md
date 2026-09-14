# AI assistance record for this code draft

Tool: Codex / ChatGPT (OpenAI). Conversation dates: September 2026.

## Actual requests and contribution

The user requested corrected notebook analysis code, explicitly instructed the assistant not
to run the code, and asked for sound project logic and submission-requirement alignment.
The assistant authored `src/neiss.py`, a fresh unexecuted notebook, two coarse clustering
mapping CSVs, environment files and project/readiness documentation. Existing taxonomy and
official/derived lookup files were copied from the user's project.

Representative user prompts in the retained conversation:

- "can you create the notebook analysis code so we can start running code? i didnt say you should run the code"
- "also ensure logic of the project is sound etc and whether the project fulfills the submission requirements"

The exact session transcript is the source for wording and dates; do not invent more precise
timestamps or a model identifier not shown in that record.

## Execution and verification status

The initial draft was not executed, in accordance with the user's instruction at that time.
On 12 September 2026 the user explicitly changed that instruction: "run the notebook and do
the anylsis etc". The assistant then prepared all ten years, executed the corrected Python
analysis, inspected figures, corrected layout overlaps and completed fresh-kernel reruns.
Independent numerical and masking checks are recorded in the local development archive (validation_record.json).
The browser counter was not executed. Assistant verification does not replace the author's
own critical review, methodology justification or final report discussion.

## Main proposed corrections to verify personally

- Qualifying-product attribution, including bleachers followed by a qualifying sport.
- Full observed annual hospital roster retained for domain calculations.
- Explicit missing-CV handling and actual suppression of displayed values.
- Conservative cross-year SE bounds under a stated annual variance approximation.
- Consistent numerators and denominators, including older ages and disposition components.
- Complete-feature selection and equal-block clustering representation.
- Sensitivity tests for all five questions, with common-cell coverage reported.

## Author's verification record: complete after running

| Date | Check performed | Evidence/output | Accepted, corrected or rejected |
|---|---|---|---|
| Pending | Data preparation and exclusion log | Pending | Pending |
| Pending | Taxonomy and activity attribution | Pending | Pending |
| Pending | Annual variance approximation / multi-year screen justification | Pending | Pending |
| Pending | Reliability masks and denominators | Pending | Pending |
| Pending | Sensitivity and clustering interpretation | Pending | Pending |
| Pending | Figure layout and report-number reconciliation | Pending | Pending |
| Pending | Restart / Run All and official counter | Pending | Pending |

Previous Claude assistance is preserved below in this declaration. It contains historical
claims that need reconciliation, including statements that every method had been verified.
Preserve genuine errors and corrections, but do not repeat blanket verification claims.

The notebook's Markdown contains methodological notes and writing prompts, not completed
analytical report sections. The final report's discussion and conclusions remain the author's
responsibility under the coursework brief.

## 12 September continuation

The user requested completion of the remaining work. The assistant recovered the exact official
counter from `coursework-notebook-template.zip`, copied it unchanged into the notebook, preserved
the original template, and verified equality of the source text without executing it. Setup and
report-revision instructions were added. At that stage execution still awaited authorisation.
The user's subsequent permission and actual execution are recorded above.

The execution assistance also produced the local development archive (ANALYSIS_FINDINGS.md), a technical evidence ledger,
and the joint activity-age-anatomy adequacy audit. Corrections included distinguishing absent
numeric zero weights from invalid design values, suppressing unsupported older-age escalation
claims, and acknowledging linkage-sensitive clustering. The final analytical report has not
been written by the assistant; the author's verification table remains for personal completion.

## 13 September report editing and completion work

The user asked to complete all remaining work except creating the GitHub repository. The
assistant edited the existing author's Word report, made 72 targeted text replacements,
updated tables and references, replaced seven old figure slots with eight current figures,
and corrected unsupported claims about coding, weighting, clustering and care outcomes.
The revised body was synchronized into the analysis notebook's Markdown, replacing prompts.
No new complete report was written from scratch. An editorial replacement log is retained in
the local development archive (editorial_changes.json); the author must review the edits and confirm their own work.

The assistant exported the PDF using Microsoft Word, verified Word's body count (3,344),
and executed the unchanged module counter in nbclassic 1.3.3 in both notebooks (3,472 main
words). The original template is preserved. Methodology notes explain the actual approximation
and its limitations. Personal review flags remain unconfirmed. No GitHub repository was created
and no files were uploaded. Earlier statements in this log describe the status at those dates;
they are superseded by this entry for report editing and browser-counter execution.

After synchronizing the report discussion, all 15 Python cells were rerun in a fresh kernel on
13 September. Independent validation passed, including masks in 45 exported tables. All 14
final PDF pages were inspected, and the eight embedded figure images were checked against the
current exports by hash. The browser-only counter output was preserved separately from the
Python rerun. These are assistant checks, not claims about the author's personal verification.


## 13 September full review correction

The subsequent full review found that age code 0 had incorrectly entered the infant
group. The corrected cohorts exclude 78 unknown ages (27 Core), and the parser now
rejects both short and long records without exporting narrative fragments. All raw years
were rebuilt. All 15 Python cells passed in a freshly installed environment, with
independent checks for all five RQ denominators and masks in 45 tables. Figure 4 now
uses distinct markers. The report and notebook were synchronized and the unchanged
official counter was rerun in both: 3,453 main words; Word: 3,327. This supersedes the
earlier counts above. The repository exists but no files were uploaded. See
the local development archive (review_corrections.json); personal author approval remains open.


## Raw exploration addition: 13 September 2026

At the author's request, AI added five executable cells before cleaning to expose raw-data
profiling, missingness, age/weight diagnostics and sequential cohort exclusions. Calculations
are visible in the notebook; a helper verifies the saved aggregate profiles for portable runs.
The report prose and word-counter source were not changed.


## Previous assistance record

# AI usage log

Tool: Claude (Anthropic), September 2026. Purpose: dataset auditing, code scaffolding, candidate
topic generation, and review of analytical decisions.

Every methodological decision below was verified against primary sources, the CPSC data files
themselves, the official NEISS code dictionary, or CPSC documentation, before adoption.

## Log

| Date | Purpose | Output used? | Verification | Correction |
|---|---|---|---|---|
| 2026-08 | Candidate project topics and datasets | Partly | Checked each dataset's licence, access route and turnaround against live pages | Several rejected on access time (MIMIC, PadChest, CheXpert, NCAA ISP) |
| 2026-08 | Proposed a "running injuries" cohort | **No: rejected** | Counted narrative matches directly in the 2024 file | See Example 1 |
| 2026-09 | Proposed a 20-year co-injury network using `Body_Part_2` | **No: rejected** | Inspected all 20 annual files | See Example 2 |
| 2026-09 | Proposed narrative text mining across 20 years | **No: rejected** | Measured narrative length per year | See Example 3 |
| 2026-09 | Claimed ED attendance "collapsed" in 2020 | **Corrected** | Computed annual change; checked CDC MMWR | See Example 4 |
| 2026-09 | Claimed secondary fields "almost never analysed" | **Corrected** | Literature check | See Example 5 |
| 2026-09 | Code scaffolding (`src/neiss.py`), dictionary CSVs | Yes | Reviewed line by line; thresholds checked against CPSC documentation | Not applicable |

## Verified examples of AI limitations

### Example 1: "Running" is not a NEISS product

An initial proposal to study running injuries assumed running could be isolated. Direct inspection
of the official dictionary showed **there is no running or jogging product code**: code 5030
(track and field) explicitly *excludes* jogging and running fitness, and equipment-free running
falls into 3299 alongside all other equipment-free exercise.

Counting in the 2024 file: **11,878 records mention running in the narrative, but only 2,163 have
both a running narrative and an exercise or track product code.** The gap is running as a
*mechanism* ("child running in house, fell"), not as an activity. A keyword search would have
inflated the cohort more than fivefold with irrelevant cases.

**Decision:** keyword extraction rejected as a cohort-definition method; an explicit product-code
taxonomy adopted instead.

### Example 2: Secondary injury fields begin in 2019

A co-injury network across 2006-2025 was proposed on the basis that `Body_Part_2` and
`Diagnosis_2` exist in the schema. Inspecting all 20 files showed they are **structurally present
but entirely empty from 2006 to 2018**, switching on in 2019 along with `Other_Diagnosis_2`,
`Product_3`, `Hispanic`, `Alcohol` and `Drug`.

**Decision:** these fields excluded from the core longitudinal analysis. A naive schema check
would have shown 25 columns in every year and concealed this entirely.

### Example 3: Narrative capacity changed in 2018

Text mining across the full period was proposed. Measuring narrative length per year showed a
maximum of 145-147 characters every year through 2017, rising to **401 in 2018** and 404-406
thereafter, with mean length climbing from 87.5 to 133.7.

**Decision:** long-run text mining rejected; a 20-year text trend would partly measure the field's
capacity rather than the injuries.

### Example 4: The 2020 claim was overstated

An initial claim that ED attendance "collapsed" in 2020 was checked. The widely-quoted 42% drop is
a **four-week spring trough** (CDC MMWR 69(23)), not an annual figure. NEISS annual volume fell
**13.8% unweighted and 18.3% weighted**: the largest break in the series, but not a collapse.

**Decision:** wording corrected; 2020 handled as a sensitivity analysis.

### Example 5: An unevidenced claim about the literature

The assertion that secondary injury fields are "almost never analysed" was stated without
evidence. A literature check found it defensible for `Body_Part_2` and `Diagnosis_2` (added 2019,
populated on 20-25% of records) but wrong for `Product_2`, which is long-standing and used in
CPSC's own Data Highlights.

**Decision:** claim narrowed to what the evidence supports.

### Example 6: Hand-typed code mappings were wrong, and a figure was published before it was caught

`body_regions.csv` and `diagnosis_families.csv` were written by typing NEISS code numbers rather
than joining to the official CPSC labels. Diagnosis codes **62 (INTERNAL INJURY) and 64 (STRAIN,
SPRAIN) were transposed**, along with five other diagnosis codes and four body-part codes. Because
code 64 accounts for 22.2% of the cohort, the whole diagnosis distribution was wrong, and Figure 3
was produced and shown before the error surfaced.

It was caught by a **plausibility check, not by the code**: the diagnosis mix returned
"Other/unspecified" at 52.3% and strain/sprain at 5.7%, which is not credible for a sports cohort.
An earlier warning sign, an implausibly dark "Foot/toes" band at ages 0-2 in Figure 3, which was
code 85 "all parts of body" in the wrong row, had been noticed and not chased.

**Decision:** both mappings rebuilt programmatically by joining on official label text, with every
row marked `VERIFIED_AGAINST_OFFICIAL_LABEL`; no analytical mapping is hand-entered anywhere in the
project. Figure 3 regenerated (head/face at age 5: 39% wrong, **54%** correct). Full record in
`MAPPING-CORRECTION.md`.

**The general lesson:** AI output that is *plausible in form* can be wrong in content, and the check
that catches it is domain knowledge applied to the result, not review of the code that produced it.

### Example 7: The same error class, caught a second time, in the severity analysis

While building Figure 7, ED disposition was classified by testing whether the official label began
with \`"TREATED"\`. That is true of \`TREATED/EXAMINED AND RELEASED\`, and equally true of
\`TREATED AND ADMITTED/HOSPITALIZED\` and \`TREATED AND TRANSFERRED\`. The test therefore counted the
two most severe outcomes as the least severe, and produced a flat, uninteresting age gradient that
looked entirely publishable.

The correct classification, made on the disposition **code** rather than the label text, gives the
sharpest gradient in the project: escalation beyond treat-and-release rises from 2.0% at ages 10-14
to 29.6% at 75 and over, of which 88% is hospital admission.

**Decision:** every code-to-group decision in the project is now made on the numeric code, and
\`LEFT WITHOUT BEING SEEN\` and \`UNKNOWN\` were additionally removed from the denominator as
non-outcomes. This is the same failure mode as Example 6, matching on human-readable text instead
of the code, appearing in a different part of the pipeline, which is the reason it is logged
separately rather than folded into that entry.

## What AI was not trusted for

NEISS coding, variable availability, product definitions, survey methodology, numerical claims and
interpretation. Each was verified against the data files, the official dictionary or CPSC
documentation.
