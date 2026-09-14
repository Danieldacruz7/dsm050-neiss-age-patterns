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
Independent numerical and masking checks are recorded in `tables/validation_record.json`.
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

Previous Claude assistance is preserved in `docs/AI_USAGE_PREVIOUS.md`. It contains historical
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

The execution assistance also produced `docs/ANALYSIS_FINDINGS.md`, a technical evidence ledger,
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
`report/editorial_changes.json`; the author must review the edits and confirm their own work.

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
`report/review_corrections.json`; personal author approval remains open.


## Raw exploration addition: 13 September 2026

At the author's request, AI added five executable cells before cleaning to expose raw-data
profiling, missingness, age/weight diagnostics and sequential cohort exclusions. Calculations
are visible in the notebook; a helper verifies the saved aggregate profiles for portable runs.
The report prose and word-counter source were not changed.
