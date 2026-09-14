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
