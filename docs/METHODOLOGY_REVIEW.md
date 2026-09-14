# Methodology review

Reviewed 13 September 2026. This note explains the implemented method and its practical
limits. The assessed report contains the concise justification in section 3.3 and evaluates
the consequences in sections 4–7. This is supporting documentation, not a replacement report.

## Design and estimands

The five questions describe the distribution and composition of product/activity-associated
ED presentations. They do not require a participation denominator, but cannot estimate risk,
incidence or a longitudinal effect of ageing. Core is primary; Extended tests a broader scope.
Fishing is included as sport; bleachers cannot establish eligibility. Cycling and playground
equipment belong to Extended. A qualifying second product can establish eligibility even when
the first product is excluded. Each presentation is counted once within a cohort.

The ten annual files are one surveillance dataset. Keeping 2016–2025 is a defensible scope
choice, not a statistically optimal window. Restricting inputs to comparable fields prevents
later years from gaining extra eligibility from Product 3. Excluding 2024–2025 tests the recent
sample boundary; excluding 2020 tests dependence on that unusual year. Neither test identifies
the cause of a change.

For annual weighted numerator N_y and denominator D_y:

- Average annual burden = sum(N_y) / 10.
- Pooled composition = sum(N_y) / sum(D_y).
- Equal-year composition = mean(N_y / D_y), a separate sensitivity estimand.

A year-specific common weight multiplier cancels within that year, but generally changes
pooled composition by changing the year's influence. Hospital-specific reweighting may change
even a within-year proportion. The report therefore avoids the earlier blanket cancellation claim.

## Annual variance approximation

Within year y and stratum h, let z_hi be the sum of record weights contributing to a domain
at hospital i. The implemented with-replacement ultimate-cluster approximation is:

    v_y = sum_h [m_h / (m_h - 1)] * sum_i (z_hi - mean_h(z))^2

The full observed annual hospital roster supplies m_h, including hospitals with no domain
records. Restricting the roster to the domain would change the design and omit zero contributions.
Singleton strata stop the calculation rather than silently contributing zero variance.

This is an approximation to survey uncertainty. The code does not reproduce all finite-population
or ratio-adjustment corrections in CPSC production estimation. Its CVs must not be presented
as exact official CVs. Weight totals and variance are separate questions: matching annual totals
does not validate the variance method.

## Cross-year uncertainty and proportions

Annual hospital samples can overlap. Unknown annual covariance is not set to zero. If s_y
denotes an annual SD, Cauchy–Schwarz gives Cov(T_y,T_z) <= s_y*s_z, hence:

    Var(sum T_y) <= (sum s_y)^2
    SE_bound(average annual total) = sum(approximate annual SE_y) / 10

This is conservative relative to the annual approximations, not a guarantee against all
sampling, coding, selection or non-sampling error. It can suppress estimates that an exact
design analysis might retain; that loss of coverage is explicitly reported.

For p = N/D, use the first-order ratio residual z_hi = N_hi - p*D_hi. Applying the annual
formula to these residuals and dividing the sum of annual residual SEs by pooled D retains
within-year numerator–denominator covariance. Computing two independent SEs for N and D
would discard that covariance. Ratio linearisation is itself an approximation.

## Display screen

The project requires pooled n >= 20, average annual estimate >= 1,200 and a finite estimate
CV bound <= 0.33. Percentages must also pass their proportion CV bound. Missing or failed
values are suppressed and kept in the denominator; they are never replaced with zero.

The numerical thresholds come from the [CPSC explanation of unstable estimates](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Explanation-Of-NEISS-Estimates-Obtained-Through-The-CPSC-Website).
Their combination with pooled n, average annual totals and a covariance bound is this project's
declared working adaptation. CPSC does not endorse that particular multi-year rule in this source.
No confidence intervals, hypothesis tests or claims of statistical significance are made.

Coverage matters: 163/255 activity-age cells and 396/2,310 joint activity-age-anatomy cells pass.
Marginal feature adequacy does not justify a complete joint interaction analysis. RQ5 escalation
at 0–4, 65–74 and 75+ fails the screen, so the report does not claim a whole-lifespan U shape.

## Clustering justification

Three coarse age proportions and five coarse anatomy proportions form two complete blocks.
Square roots of proportions divided by sqrt(2) give each block the same norm and maximum
influence. Euclidean Ward linkage is compatible with this representation; unit-variance scaling
would instead amplify low-variance features. See [SciPy linkage documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html).

The grouping is exploratory and depends on category boundaries, the selected activities,
distance representation and linkage. Ten of fifteen selected activities have complete passing
features. Ward versus average-linkage agreement is 77.8%, so the four-group taxonomy is not
linkage-invariant. The through-2023 comparison agrees on nine common eligible activities only.
Pairwise agreement is descriptive and can be high when most pairs are separate in both trees.

## Evidence and residual limits

Independent numerical checks in `validate_analysis.py` cover a known artificial design,
ratio covariance, annual totals, masks in 45 exported tables and joint coverage. Execution
and figure hashes are recorded in `tables/`. The report, notebook discussion and counts are
synchronized. These checks support the implementation; they do not certify a coursework mark.

The [CPSC 2024 injury report, page 7](https://www.cpsc.gov/s3fs-public/Death_and_Injury_Report_2024.pdf)
documents its sample change and backcasting. This project does not backcast its annual totals.
Exact official variance estimation, more clinical grouping validation and a stronger domain
literature review remain possible improvements. The current analysis is coherent as a clearly
qualified descriptive visualisation project; the author must understand and accept its assumptions.
