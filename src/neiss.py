"""NEISS coursework preparation and descriptive survey helpers.

The notebook is the analysis entry point; validation is in validate_analysis.py.
Annual uncertainty uses a with-replacement ultimate-cluster approximation.
Across years, sum annual standard errors to bound uncertainty conservatively;
do not assume independence of recurring hospitals. This is not CPSC software.
"""
from __future__ import annotations

import hashlib
import json
import csv
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
YEARS = list(range(2016, 2026))
STRATA = list("VLMSC")
MIN_CASES, MIN_ESTIMATE, MAX_CV = 20, 1200.0, 0.33
PIPELINE_VERSION = "2026-09-13-age-validation-2"
SCHEMA = [
    "CPSC_Case_Number", "Treatment_Date", "Age", "Sex", "Race", "Other_Race",
    "Hispanic", "Body_Part", "Diagnosis", "Other_Diagnosis", "Body_Part_2",
    "Diagnosis_2", "Other_Diagnosis_2", "Disposition", "Location",
    "Fire_Involvement", "Product_1", "Product_2", "Product_3", "Alcohol", "Drug",
    "Narrative_1", "Stratum", "PSU", "Weight",
]
AGE_EDGES = [0, 5, 10, 15, 18, 25, 35, 45, 55, 65, 75, 130]
AGE_LABELS = ["0-4", "5-9", "10-14", "15-17", "18-24", "25-34", "35-44",
              "45-54", "55-64", "65-74", "75+"]
PROFILE_EDGES = list(range(0, 81, 5)) + [130]
PROFILE_LABELS = [f"{a}-{a+4}" for a in range(0, 80, 5)] + ["80+"]
REGION_ORDER = ["Head/face", "Neck", "Shoulder/upper arm", "Elbow/forearm",
                "Wrist/hand", "Trunk/spine", "Hip/thigh", "Knee", "Lower leg",
                "Ankle", "Foot/toes", "Multiple/systemic", "Internal/systemic",
                "Not stated/other"]
DIAGNOSIS_FOCUS = ["Strain/sprain", "Fracture", "Contusion/abrasion",
                   "Laceration/open wound", "Internal injury"]
RELEASED = {1}
ESCALATED = {2, 4, 5, 8}


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def dictionary(name):
    return pd.read_csv(ROOT / "data/dictionaries" / f"{name}.csv")


def strict_bool(series):
    s = series.astype(str).str.strip().str.upper()
    if not s.isin(["TRUE", "FALSE"]).all():
        raise ValueError("Inclusion fields must contain only TRUE/FALSE; resolve REVIEW first.")
    return s.eq("TRUE")


def taxonomy():
    c = dictionary("product_classification")
    if c.product_code.duplicated().any():
        raise ValueError("Duplicate taxonomy product codes.")
    core = set(c.loc[strict_bool(c.include_core), "product_code"].astype(int))
    extended = set(c.loc[strict_bool(c.include_extended), "product_code"].astype(int))
    if not core <= extended:
        raise ValueError("Extended must include every Core code.")
    if 3223 not in core or 1294 in extended:
        raise ValueError("Agreed decisions: fishing in Core; bleachers excluded.")
    if c.loc[c.product_code.isin(extended), "activity_family"].isna().any():
        raise ValueError("Every included code needs an activity family.")
    official = dictionary("product_codes")
    official_code = "product_code" if "product_code" in official else "code"
    known = set(official[official_code].astype(int))
    if not set(c.product_code.astype(int)) <= known:
        raise ValueError("Taxonomy contains undefined official codes.")
    return core, extended, c.set_index("product_code").activity_family.to_dict(), c


def dictionary_fingerprint():
    return {p.name: sha256(p) for p in sorted((ROOT / "data/dictionaries").glob("*.csv"))}


def verify_mappings():
    """Verify code/label joins. Clinical grouping choices still need human judgement."""
    for original, derived in [("body_parts", "body_regions"),
                               ("diagnoses", "diagnosis_families")]:
        a, b = dictionary(original), dictionary(derived)
        if a.code.duplicated().any() or b.code.duplicated().any():
            raise ValueError(f"Duplicate code in {original}/{derived}.")
        left, right = a.set_index("code"), b.set_index("code")
        if set(left.index) != set(right.index):
            raise ValueError(f"Mapping coverage differs: {derived}")
        x = left.official_label.astype(str).str.strip()
        y = right.loc[left.index, "official_label"].astype(str).str.strip()
        if not x.equals(y):
            raise ValueError(f"Official code/label mismatch in {derived}")


def decode_age(values):
    """CPSC age coding: 0 is unknown; 201–223 are months; 2–115 are years.

    Age 201 also includes infants younger than one month. Historical top codes
    (e.g. 114) fall within the accepted year range; no exact age is inferred.
    Unknown and malformed values become missing, never age zero.
    """
    raw = pd.to_numeric(values, errors="coerce")
    integral = raw.mod(1).eq(0)
    years = integral & raw.between(2, 115)
    months = integral & raw.between(201, 223)
    return raw.where(years).where(~months, (raw - 200) / 12)


def read_raw(path):
    """Read with explicit encoding and log rejected-width records; never hide them.

    Parser failures not handled by the bad-line callback stop the preparation.
    Rejected row contents/narratives are not copied to the public audit log.
    """
    for encoding in ["utf-8", "cp1252", "latin-1"]:
        rejected = []

        try:
            # pandas pads short rows silently and can infer an index from excess
            # fields in the first record. Check both widths before constructing.
            rows = []
            with Path(path).open(encoding=encoding, newline="") as stream:
                reader = csv.reader(stream, delimiter="\t", strict=True)
                header = next(reader)
                if [x.strip().strip('"') for x in header] != SCHEMA:
                    raise ValueError(f"Unexpected schema in {path}; do not proceed.")
                for fields in reader:
                    if len(fields) != len(SCHEMA):
                        # A continuation fragment can begin with narrative text,
                        # not an identifier. Never export that as a case number.
                        identifier = fields[0].strip() if fields else ""
                        rejected.append({"issue": "parser_field_count",
                                         "case_number": identifier if identifier.isdigit() else "",
                                         "field_count": len(fields), "line_number": reader.line_num})
                    else:
                        rows.append(fields)
            frame = pd.DataFrame(rows, columns=SCHEMA)
            return frame, encoding, rejected
        except UnicodeDecodeError:
            continue
    raise UnicodeError(f"No supported encoding for {path}")


def attribute(frame, eligible, family):
    """Excluded Product_1 must never override a qualifying Product_2."""
    p1 = frame.Product_1.where(frame.Product_1.isin(eligible)).map(family)
    p2 = frame.Product_2.where(frame.Product_2.isin(eligible)).map(family)
    return p1.fillna(p2)


def prepare_data(raw_dir, years=YEARS):
    """User-run rebuild: cohorts, full annual PSU rosters, manifests and audit logs.

    Quality counters are overlapping diagnostics, not a sum of unique exclusions.
    The design roster is collected BEFORE cohort, date and age restrictions.
    """
    raw_dir = Path(raw_dir)
    core_codes, ext_codes, families, _ = taxonomy()
    verify_mappings()
    for year in years:
        if not (raw_dir / f"neiss{year}.tsv").is_file():
            raise FileNotFoundError(f"Missing raw annual file: neiss{year}.tsv in {raw_dir}")
    outdir = ROOT / "data/analysis"
    outdir.mkdir(parents=True, exist_ok=True)
    # Remove a prior success marker before overwriting any cohort, so interrupted
    # preparation cannot masquerade as a complete compatible build.
    marker = outdir / "build_metadata.json"
    marker.unlink(missing_ok=True)
    manifest, quality, rosters, rejects = [], [], [], []
    for year in years:
        print(f"Preparing {year} ...", flush=True)
        path = raw_dir / f"neiss{year}.tsv"
        raw, encoding, parser_rejects = read_raw(path)
        n_raw = len(raw)
        for item in parser_rejects:
            rejects.append({"Source_Year": year, **item})
        num = {col: pd.to_numeric(raw[col], errors="coerce") for col in
               ["Age", "Weight", "PSU", "Sex", "Body_Part", "Diagnosis", "Disposition",
                "Product_1", "Product_2"]}
        invalid_weight = ~np.isfinite(num["Weight"]) | num["Weight"].le(0)
        invalid_psu = (~np.isfinite(num["PSU"]) | num["PSU"].le(0)
                       | num["PSU"].mod(1).ne(0))
        invalid_stratum = ~raw.Stratum.str.strip().isin(STRATA)
        valid_design = ~(invalid_weight | invalid_psu | invalid_stratum)
        roster = pd.DataFrame({"Source_Year": year, "Stratum": raw.Stratum.str.strip(),
                               "PSU": num["PSU"]}).loc[valid_design].drop_duplicates()
        roster.PSU = roster.PSU.astype(int)
        if roster.groupby("PSU").Stratum.nunique().gt(1).any():
            raise ValueError(f"A hospital appears in multiple strata in {year}; investigate.")
        if set(roster.Stratum) != set(STRATA):
            raise ValueError(f"Missing stratum in full-year design roster {year}")
        if roster.groupby("Stratum").size().lt(2).any():
            raise ValueError(f"Singleton stratum in {year}: seek a justified design treatment.")
        rosters.append(roster)
        age_raw = num["Age"]
        age = decode_age(age_raw)
        valid_age = age.notna()
        date = pd.to_datetime(raw.Treatment_Date, format="%m/%d/%Y", errors="coerce")
        valid_date = date.dt.year.eq(year)
        p1, p2 = num["Product_1"], num["Product_2"]
        eligible = p1.isin(ext_codes) | p2.isin(ext_codes)
        keep = eligible & valid_design & valid_age & valid_date
        cohort = pd.DataFrame({
            "CPSC_Case_Number": raw.CPSC_Case_Number, "Treatment_Date": raw.Treatment_Date,
            "Source_Year": year, "Age_Raw": age_raw, "Age_Years": age,
            "Sex": num["Sex"], "Body_Part": num["Body_Part"], "Diagnosis": num["Diagnosis"],
            "Disposition": num["Disposition"], "Product_1": p1, "Product_2": p2,
            "Stratum": raw.Stratum.str.strip(), "PSU": num["PSU"], "Weight": num["Weight"],
            "In_Core": p1.isin(core_codes) | p2.isin(core_codes),
        }).loc[keep].copy()
        if (cohort.CPSC_Case_Number.isna().any() or cohort.CPSC_Case_Number.eq("").any()
                or cohort.CPSC_Case_Number.duplicated().any()):
            raise ValueError(f"Missing/duplicate case identifiers in eligible {year} records.")
        cohort.PSU = cohort.PSU.astype(int)
        # Sex codes outside the official set are treated as unknown, not guessed.
        cohort.loc[~cohort.Sex.isin([0, 1, 2]), "Sex"] = 0
        cohort["Activity_Core"] = attribute(cohort, core_codes, families)
        cohort["Activity_Extended"] = attribute(cohort, ext_codes, families)
        if cohort.Activity_Extended.isna().any() or cohort.loc[cohort.In_Core, "Activity_Core"].isna().any():
            raise ValueError("Eligible presentation has no qualifying activity attribution.")
        for field, codes in [("Body_Part", dictionary("body_parts").code),
                             ("Diagnosis", dictionary("diagnoses").code),
                             ("Disposition", dictionary("dispositions").code)]:
            if not cohort[field].isin(codes).all():
                raise ValueError(f"Unmapped {field} in {year}; investigate rather than silently drop.")
        target = outdir / f"cohort_{year}.csv.gz"
        cohort.to_csv(target, index=False, compression={"method": "gzip", "mtime": 0})
        quality.append({
            "year": year, "parsed_rows": n_raw, "parser_rejected_records": len(parser_rejects),
            "invalid_design_unique": int((~valid_design).sum()),
            "zero_weight": int(num["Weight"].eq(0).sum()),
            "invalid_weight": int(invalid_weight.sum()), "invalid_psu": int(invalid_psu.sum()),
            "invalid_stratum": int(invalid_stratum.sum()),
            "same_weight_psu_stratum_masks": bool(invalid_weight.equals(invalid_psu)
                                                   and invalid_psu.equals(invalid_stratum)),
            "invalid_age": int((~valid_age).sum()), "invalid_date_or_year": int((~valid_date).sum()),
            "unknown_age": int(age_raw.eq(0).sum()),
            "eligible_unknown_age": int((eligible & age_raw.eq(0)).sum()),
            "eligible_invalid_age": int((eligible & ~valid_age).sum()),
            "eligible_before_quality": int(eligible.sum()),
            "eligible_excluded_unique": int((eligible & ~keep).sum()),
            "sex_reclassified_unknown": int((keep & ~num["Sex"].isin([0, 1, 2])).sum()),
            "extended_rows": len(cohort), "core_rows": int(cohort.In_Core.sum()),
            "two_extended_products": int((cohort.Product_1.isin(ext_codes)
                                            & cohort.Product_2.isin(ext_codes)).sum()),
        })
        manifest.append({
            "year": year, "source_url": f"https://www.cpsc.gov/cgibin/NEISSQuery/Data/Archived%20Data/{year}/neiss{year}.tsv",
            "source_file": path.name, "encoding": encoding, "source_sha256": sha256(path),
            "cohort_file": target.name, "cohort_sha256": sha256(target),
            "original_parsed_rows": n_raw, "extended_rows": len(cohort),
            "core_rows": int(cohort.In_Core.sum()),
            "prepared_at_utc": datetime.now(timezone.utc).isoformat(),
        })
    pd.concat(rosters, ignore_index=True).to_csv(outdir / "design_roster.csv", index=False)
    pd.DataFrame(manifest).to_csv(ROOT / "data/data_manifest.csv", index=False)
    pd.DataFrame(quality).to_csv(ROOT / "data/data_quality_log.csv", index=False)
    pd.DataFrame(rejects, columns=["Source_Year", "issue", "case_number", "field_count", "line_number"]).to_csv(
        ROOT / "data/parser_rejections.csv", index=False)
    marker.write_text(json.dumps({"pipeline_version": PIPELINE_VERSION, "years": list(years),
                                 "dictionary_hashes": dictionary_fingerprint(),
                                 "helper_sha256": sha256(__file__),
                                 "design_roster_sha256": sha256(outdir / "design_roster.csv")}, indent=2),
                      encoding="utf-8")
    return pd.DataFrame(quality)


def load_data():
    """Require a complete fresh build; never quietly use stale cohorts."""
    outdir = ROOT / "data/analysis"
    metadata_path = outdir / "build_metadata.json"
    if not metadata_path.exists():
        raise FileNotFoundError("Prepare the data first: set PREPARE_DATA=True in notebook section 2.")
    meta = json.loads(metadata_path.read_text(encoding="utf-8"))
    if meta["years"] != YEARS or meta["pipeline_version"] != PIPELINE_VERSION:
        raise ValueError("Study window or pipeline changed: rebuild data.")
    if meta["dictionary_hashes"] != dictionary_fingerprint():
        raise ValueError("Dictionaries changed: rebuild data before analysis.")
    if meta["helper_sha256"] != sha256(__file__):
        raise ValueError("Helper code changed since preparation: rebuild or deliberately verify compatibility.")
    if meta["design_roster_sha256"] != sha256(outdir / "design_roster.csv"):
        raise ValueError("Design roster checksum mismatch.")
    manifest = pd.read_csv(ROOT / "data/data_manifest.csv")
    if set(manifest.year) != set(YEARS) or manifest.year.duplicated().any():
        raise ValueError("Manifest does not cover the study window exactly once.")
    frames = []
    for row in manifest.itertuples():
        path = outdir / row.cohort_file
        if sha256(path) != row.cohort_sha256:
            raise ValueError(f"Cohort checksum mismatch: {path.name}")
        annual = pd.read_csv(path, dtype={"CPSC_Case_Number": str})
        if len(annual) != row.extended_rows or not annual.Source_Year.eq(row.year).all():
            raise ValueError(f"Annual cohort does not match manifest: {path.name}")
        frames.append(annual)
    frame = pd.concat(frames, ignore_index=True)
    frame.In_Core = strict_bool(frame.In_Core)
    decoded = decode_age(frame.Age_Raw)
    if decoded.isna().any() or not np.allclose(decoded, frame.Age_Years):
        raise ValueError("Prepared ages do not match the official age coding rule.")
    if frame.duplicated(["Source_Year", "CPSC_Case_Number"]).any():
        raise ValueError("Duplicate year/case records in prepared data.")
    verify_mappings()
    core, ext, family, _ = taxonomy()
    expected_core = frame.Product_1.isin(core) | frame.Product_2.isin(core)
    if not frame.In_Core.equals(expected_core):
        raise ValueError("Core flags differ from current taxonomy.")
    for name, codes in [("Activity_Core", core), ("Activity_Extended", ext)]:
        expected = attribute(frame, codes, family)
        if not frame[name].fillna("").eq(expected.fillna("")).all():
            raise ValueError(f"Incorrect {name} attribution.")
    frame["Body_Region"] = frame.Body_Part.map(dictionary("body_regions").set_index("code").derived_region)
    frame["Diagnosis_Family"] = frame.Diagnosis.map(dictionary("diagnosis_families").set_index("code").derived_family)
    frame["Diagnosis_Plot"] = frame.Diagnosis_Family.where(frame.Diagnosis_Family.isin(DIAGNOSIS_FOCUS), "All other diagnoses")
    frame["Disposition_Label"] = frame.Disposition.map(dictionary("dispositions").set_index("code").official_label)
    frame["Age_Band"] = pd.cut(frame.Age_Years, AGE_EDGES, labels=AGE_LABELS, right=False)
    frame["Profile_Age"] = pd.cut(frame.Age_Years, PROFILE_EDGES, labels=PROFILE_LABELS, right=False)
    frame["Age_Integer"] = np.floor(frame.Age_Years).astype(int)
    frame["All"] = "All"
    needed = ["Age_Band", "Profile_Age", "Body_Region", "Diagnosis_Family", "Disposition_Label"]
    if frame[needed].isna().any().any():
        raise ValueError("Unmapped analytical values: inspect dictionaries and source codes.")
    roster = pd.read_csv(outdir / "design_roster.csv")
    return frame, roster


def reliability(n, estimate, cv):
    """Conjunctive screen; missing or non-finite values cannot pass."""
    reasons = []
    for label, value in [("n", n), ("estimate", estimate), ("CV", cv)]:
        if value is None or not np.isfinite(value):
            reasons.append(f"{label} unassessed")
    if reasons:
        return False, "; ".join(reasons)
    if n < MIN_CASES:
        reasons.append("n < 20")
    if estimate < MIN_ESTIMATE:
        reasons.append("estimate < 1200")
    if cv < 0 or cv > MAX_CV:
        reasons.append("CV bound outside [0, 0.33]")
    return not reasons, "; ".join(reasons) if reasons else "passes conservative screen"


def _keys(index):
    return list(index) if isinstance(index, pd.MultiIndex) else [(x,) for x in index]


def _psu_matrix(frame, group_cols, catalog, design_columns):
    totals = frame.groupby(group_cols + ["Source_Year", "Stratum", "PSU"], observed=True)["Weight"].sum()
    matrix = totals.unstack(["Source_Year", "Stratum", "PSU"], fill_value=0)
    return matrix.reindex(index=catalog, columns=design_columns, fill_value=0).fillna(0)


def _annual_variance(matrix, design, year):
    """Zero-contributing hospitals retained through the full design roster."""
    variance = np.zeros(matrix.shape[0])
    for stratum in STRATA:
        cols = (design.get_level_values("Source_Year") == year) & (design.get_level_values("Stratum") == stratum)
        values = matrix[:, cols]
        nh = values.shape[1]
        if nh < 2:
            raise ValueError(f"Need >=2 PSUs in {year}/{stratum}; cannot assign zero variance.")
        variance += nh / (nh - 1) * np.square(values - values.mean(axis=1, keepdims=True)).sum(axis=1)
    return variance


def domain_summary(frame, roster, groups, denominator=None, catalog=None, years=None):
    """Average annual totals and pooled composition with conservative SE bounds.

    For annual variance V_y, SD(sum annual totals) <= sum sqrt(V_y), regardless
    of the unknown cross-year correlations. Annual V_y is a with-replacement
    ultimate-cluster approximation, without finite-population or ratio-adjustment
    corrections. This does not reproduce the official CPSC variance estimator.

    A proportion is sum annual numerator / sum annual denominator, NOT the
    equal-year average proportion. Its Taylor residual is N_psu - p * D_psu;
    the same bound is applied to annual residual standard errors. No normal CIs
    or significance claims are produced.

    The conservative working screen uses pooled n and average annual estimate,
    plus the upper-bound CV; it is not an official multi-year CPSC certification.
    Returns (pooled table, annual diagnostic table).
    """
    groups = list(groups)
    years = sorted(frame.Source_Year.unique()) if years is None else list(years)
    if not years or len(set(years)) != len(years):
        raise ValueError("Supply distinct nonempty years.")
    frame = frame.loc[frame.Source_Year.isin(years)].copy()
    roster = roster.loc[roster.Source_Year.isin(years)].copy()
    if set(roster.Source_Year) != set(years):
        raise ValueError("Full design roster missing a requested year.")
    if roster.duplicated(["Source_Year", "Stratum", "PSU"]).any():
        raise ValueError("Duplicate PSU in annual roster.")
    if roster.groupby(["Source_Year", "PSU"]).Stratum.nunique().gt(1).any():
        raise ValueError("A hospital appears in multiple strata within a year.")
    design = pd.MultiIndex.from_frame(roster[["Source_Year", "Stratum", "PSU"]].sort_values(["Source_Year", "Stratum", "PSU"]))
    observed_design = pd.MultiIndex.from_frame(frame[["Source_Year", "Stratum", "PSU"]].drop_duplicates())
    if not observed_design.isin(design).all():
        raise ValueError("Analytical records contain hospitals absent from full-year roster.")
    if frame.empty:
        raise ValueError("No analytical records in requested domain.")
    if not (np.isfinite(frame.Weight) & frame.Weight.gt(0)).all():
        raise ValueError("Domain calculations require finite positive weights.")
    if frame[groups].isna().any().any():
        raise ValueError("Missing grouping values must be classified explicitly, not silently dropped.")
    if catalog is None:
        catalog = frame.groupby(groups, observed=True).size().index
    matrix = _psu_matrix(frame, groups, catalog, design)
    values = matrix.to_numpy(dtype=float)
    counts = frame.groupby(groups, observed=True).size().reindex(catalog, fill_value=0)
    total = values.sum(axis=1)
    annual_sd = np.zeros(len(matrix))
    annual = []
    for year in years:
        est_y = values[:, design.get_level_values("Source_Year") == year].sum(axis=1)
        sd_y = np.sqrt(_annual_variance(values, design, year))
        n_y = frame.loc[frame.Source_Year.eq(year)].groupby(groups, observed=True).size().reindex(catalog, fill_value=0)
        cv_y = np.divide(sd_y, est_y, out=np.full_like(sd_y, np.nan), where=est_y > 0)
        a = matrix.index.to_frame(index=False)
        a["Source_Year"], a["n"], a["estimate"], a["cv_approx"] = year, n_y.to_numpy(), est_y, cv_y
        flags = [reliability(n, e, c)[0] for n, e, c in zip(n_y, est_y, cv_y)]
        a["annual_pass"] = flags
        annual.append(a)
        annual_sd += sd_y
    out = matrix.index.to_frame(index=False)
    out["n"] = counts.to_numpy()
    out["estimate"] = total / len(years)
    out["se_bound"] = annual_sd / len(years)
    out["cv_bound"] = np.divide(annual_sd, total, out=np.full_like(total, np.nan), where=total > 0)
    out["estimate_rounded"] = np.round(out.estimate / 100) * 100
    assessments = [reliability(n, e, c) for n, e, c in zip(out.n, out.estimate, out.cv_bound)]
    out["reportable"] = [x[0] for x in assessments]
    out["reason"] = [x[1] for x in assessments]
    if denominator is not None:
        denominator = list(denominator)
        if not set(denominator) <= set(groups):
            raise ValueError("Denominator columns must be a subset of group columns.")
        if denominator:
            di = frame.groupby(denominator, observed=True).size().index
            dm = _psu_matrix(frame, denominator, di, design)
            lookup = dict(zip(_keys(dm.index), dm.to_numpy(dtype=float)))
            dvalues = np.array([lookup.get(tuple(row), np.zeros(len(design)))
                                for row in out[denominator].itertuples(index=False, name=None)])
        else:
            den = frame.groupby(["Source_Year", "Stratum", "PSU"], observed=True).Weight.sum().reindex(design, fill_value=0)
            dvalues = np.broadcast_to(den.to_numpy(dtype=float), values.shape)
        dtotal = dvalues.sum(axis=1)
        p = np.divide(total, dtotal, out=np.full_like(total, np.nan), where=dtotal > 0)
        residuals = values - p[:, None] * dvalues
        ratio_sd = sum(np.sqrt(_annual_variance(residuals, design, year)) for year in years)
        ratio_se = np.divide(ratio_sd, dtotal, out=np.full_like(total, np.nan), where=dtotal > 0)
        out["percent"] = p * 100
        out["percent_se_bound"] = ratio_se * 100
        out["percent_cv_bound"] = np.divide(ratio_se, p, out=np.full_like(total, np.nan), where=p > 0)
        ratio_ok = np.isfinite(out.percent_cv_bound) & out.percent_cv_bound.between(0, MAX_CV)
        out.loc[~ratio_ok, "reason"] += "; proportion CV unassessed or > 0.33"
        out["reportable"] &= ratio_ok
    out["years"] = len(years)
    return out, pd.concat(annual, ignore_index=True)


def report_table(table):
    """Mask and round presentation values, retaining unrounded inputs in the caller."""
    out = table.copy()
    values = [c for c in ["estimate", "estimate_rounded", "percent"] if c in out]
    out.loc[~out.reportable, values] = np.nan
    if "estimate" in out:
        out["estimate"] = np.round(out.estimate / 100) * 100
    if "percent" in out:
        out["percent"] = out.percent.round(1)
    return out


def pairwise_agreement(a, b):
    """Label-invariant fraction of pairs with matching co-clustering decisions."""
    a, b = np.asarray(a), np.asarray(b)
    i, j = np.triu_indices(len(a), 1)
    return float(np.mean((a[i] == a[j]) == (b[i] == b[j]))) if len(i) else np.nan
