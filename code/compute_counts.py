#!/usr/bin/env python3
"""
CIS 5370 Final Project - Phase 3: reproduce the analysis counts.

Reads data/coding_sheet_final.csv (the adjudicated final coding sheet,
24 incidents) and recomputes every count published in
data/analysis_counts.csv, then compares the two and reports any mismatch.

What is computed directly from the sheet:
  * sample size by year, ransomware confirmation counts
  * per-service disrupted / not-coded counts from services_affected
  * per-field status counts (reported content / not reported /
    reported absent / n/a) for the six analytic fields
  * recovery three-way counts, workaround and limitation totals
  * vendor-mediated vs direct field-content counts, and the per-incident
    count of fields coded "not reported"

Three classifications are analyst judgments documented in docs/ANALYSIS.md,
which names every incident assigned to each class. They are encoded here
verbatim from that memo (Sections 3, 4 and 6) so the published counts stay
reproducible; the script validates that every named organization exists in
the sheet and carries reported content in the relevant field.

Field status rule (Coding Guide v2): a cell equal to "not reported" is
not reported; a cell starting with "reported absent" is reported absent;
a cell starting with "n/a" is the R8 not-applicable value; anything else
is reported content backed by a source.

Usage: python3 code/compute_counts.py
Exit code 0 means the recomputed counts match data/analysis_counts.csv.
"""

import sys
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
SHEET_CSV = BASE / "data" / "coding_sheet_final.csv"
COUNTS_CSV = BASE / "data" / "analysis_counts.csv"

FIELDS = [
    "services_affected",
    "operational_effect",
    "workaround",
    "recovery_technical",
    "recovery_operations",
    "recovery_limitations",
]

TAXONOMY = [
    "EHR/clinical records",
    "imaging/radiology",
    "laboratory",
    "pharmacy",
    "scheduling/appointments",
    "emergency care/patient diversion",
    "surgery/procedures",
    "communications",
    "billing/administrative",
    "general IT systems (unspecified)",
]

# Vendor-mediated incidents, docs/ANALYSIS.md Section 6: the organization
# attacked was a vendor, host or business associate of the named
# organization (Crossroads, Netgain, a storage vendor, OneTouchPoint,
# Kronos/UKG and Panorama Eyecare respectively).
VENDOR_MEDIATED = {
    "Personal Touch Home Aides Inc.",
    "MultiCare",
    "Harvard Eye Associates",
    "Geisinger",
    "Cheyenne Regional Medical Center",
    "Eye Center of Northern Colorado",
}

# Workaround types, docs/ANALYSIS.md Section 4 (13 assignments, 11 rows).
WORKAROUND_TYPES = [
    ("paper/manual downtime procedures", {
        "Sky Lakes Medical Center",
        "Dickingson County Healthcare System",
        "Clinical Hospital No.1 CF Witting",
        "Virginia Mason Franciscan Health",
        "Tallahassee Memorial Healthcare",
        "Manchester Memorial and Rockville General Hospital",
    }),
    ("transfers/diversion/referral to partner or outside providers", {
        "Brookside Surgery Center",
        "Colosseum Dental",
        "Tallahassee Memorial Healthcare",
    }),
    ("manual financial processes", {
        "Cheyenne Regional Medical Center",
    }),
    ("other", {
        "Barlow Respiratory Hospital",
        "Immanuel Medical Center",
        "Brookside Surgery Center",
    }),
]

# Continuing-limitation groups, docs/ANALYSIS.md Section 3 (22 assignments,
# 18 rows; a row can fall in more than one group).
LIMITATION_GROUPS = [
    ("notification/data tails", {
        "MultiCare",
        "Suncoast Skin Solutions",
        "Barlow Respiratory Hospital",
        "Ascension St. Vincent's Coastal Cardiology",
        "Virginia Mason Franciscan Health",
        "Immanuel Medical Center",
        "Tallahassee Memorial Healthcare",
        "Republican Vilnius Psychiatric Hospital",
        "Fallon Ambulance Services",
        "Eye Center of Northern Colorado",
        "Hampton-Newport News CSB",
    }),
    ("permanent data loss", {
        "Saint Francis Healthcare System",
        "Sky Lakes Medical Center",
        "Brookside Surgery Center",
        "Ascension St. Vincent's Coastal Cardiology",
    }),
    ("prolonged service limits", {
        "Sky Lakes Medical Center",
        "Dickingson County Healthcare System",
        "Virginia Mason Franciscan Health",
        "Tallahassee Memorial Healthcare",
        "Manchester Memorial and Rockville General Hospital",
    }),
    ("other", {
        "Colosseum Dental",
        "Cheyenne Regional Medical Center",
    }),
]


def status(value):
    v = str(value).strip()
    if v == "not reported":
        return "not reported"
    if v.startswith("reported absent"):
        return "reported absent"
    if v.startswith("n/a"):
        return "n/a"
    return "reported content"


def service_labels(value):
    v = str(value).strip()
    if status(v) != "reported content":
        return []
    return [part.strip() for part in v.split(";") if part.strip()]


def main():
    df = pd.read_csv(SHEET_CSV, dtype=str, keep_default_na=False)
    n = len(df)
    rows = []  # (category, item, count, denominator)

    def add(category, item, count, denominator):
        rows.append((category, item, int(count), int(denominator)))

    # Sample by year and confirmation.
    for year in sorted(df["year"].unique()):
        add("sample_by_year", year, (df["year"] == year).sum(), n)
    for value in sorted(df["ransomware_confirmed"].unique()):
        add("ransomware_confirmed", value,
            (df["ransomware_confirmed"] == value).sum(), n)

    # Services: named taxonomy labels, then "other (specify)" labels.
    labels_per_row = [service_labels(v) for v in df["services_affected"]]
    for label in TAXONOMY:
        c = sum(1 for labels in labels_per_row if label in labels)
        add("service_disrupted", label, c, n)
        add("service_not_coded", label, n - c, n)
    other_labels = sorted({
        lab for labels in labels_per_row for lab in labels
        if lab.startswith("other (")
    })
    for label in other_labels:
        c = sum(1 for labels in labels_per_row if label in labels)
        add("service_disrupted_other_spec", label, c, n)

    # Services field status as a whole.
    svc_status = [status(v) for v in df["services_affected"]]
    add("services_field_status", "not reported",
        svc_status.count("not reported"), n)
    add("services_field_status", "reported absent",
        svc_status.count("reported absent"), n)
    add("services_field_status", "at least one service coded",
        svc_status.count("reported content"), n)

    # Per-field status for the six analytic fields.
    field_status = {}
    for field in FIELDS:
        sts = [status(v) for v in df[field]]
        field_status[field] = sts
        add(f"field_status:{field}", "reported content",
            sts.count("reported content"), n)
        add(f"field_status:{field}", "not reported",
            sts.count("not reported"), n)
        if sts.count("reported absent"):
            add(f"field_status:{field}", "reported absent",
                sts.count("reported absent"), n)
        if sts.count("n/a"):
            add(f"field_status:{field}", "n/a", sts.count("n/a"), n)

    # Recovery three-way reported-content counts.
    for field in ["recovery_technical", "recovery_operations",
                  "recovery_limitations"]:
        add("recovery_reported_content", field,
            field_status[field].count("reported content"), n)

    # Workarounds: totals and type classification.
    wa_content_orgs = {
        org for org, st in zip(df["organization"], field_status["workaround"])
        if st == "reported content"
    }
    for type_name, orgs in WORKAROUND_TYPES:
        missing = orgs - set(df["organization"])
        if missing:
            raise SystemExit(f"workaround type '{type_name}': organizations "
                             f"not in sheet: {sorted(missing)}")
        not_content = orgs - wa_content_orgs
        if not_content:
            raise SystemExit(f"workaround type '{type_name}': organizations "
                             f"without workaround content: {sorted(not_content)}")
        add("workaround_type", type_name, len(orgs), len(wa_content_orgs))
    add("workaround", "any workaround reported", len(wa_content_orgs), n)
    add("workaround", "not reported",
        field_status["workaround"].count("not reported"), n)

    # Continuing limitations: totals and group classification.
    lim_content_orgs = {
        org for org, st in zip(df["organization"],
                               field_status["recovery_limitations"])
        if st == "reported content"
    }
    for group_name, orgs in LIMITATION_GROUPS:
        missing = orgs - set(df["organization"])
        if missing:
            raise SystemExit(f"limitation group '{group_name}': organizations "
                             f"not in sheet: {sorted(missing)}")
        not_content = orgs - lim_content_orgs
        if not_content:
            raise SystemExit(f"limitation group '{group_name}': organizations "
                             f"without limitation content: {sorted(not_content)}")
        add("limitation_group", group_name, len(orgs), len(lim_content_orgs))
    add("recovery_limitations", "any limitation reported",
        len(lim_content_orgs), n)
    add("recovery_limitations", "not reported",
        field_status["recovery_limitations"].count("not reported"), n)

    # Vendor-mediated vs direct.
    is_vendor = df["organization"].isin(VENDOR_MEDIATED)
    add("vendor_mediated", "vendor-mediated incidents", is_vendor.sum(), n)
    add("vendor_mediated", "direct incidents", (~is_vendor).sum(), n)
    for field in FIELDS:
        sts = field_status[field]
        v = sum(1 for s, flag in zip(sts, is_vendor)
                if flag and s == "reported content")
        d = sum(1 for s, flag in zip(sts, is_vendor)
                if not flag and s == "reported content")
        add("vendor_field_content", f"{field} content (vendor)", v,
            int(is_vendor.sum()))
        add("direct_field_content", f"{field} content (direct)", d,
            int((~is_vendor).sum()))

    # Derived completeness: fields coded "not reported" per incident.
    per_row = [0] * n
    for field in FIELDS:
        for i, s in enumerate(field_status[field]):
            if s == "not reported":
                per_row[i] += 1
    for k in sorted(set(per_row)):
        add("derived_fields_not_reported_per_incident",
            f"{k} of 6 fields not reported", per_row.count(k), n)

    computed = pd.DataFrame(
        rows, columns=["category", "item", "count", "denominator"])
    # keep_default_na=False matters here: the published item label for the
    # not-applicable status is the literal string "n/a", which pandas would
    # otherwise parse as a missing value.
    published = pd.read_csv(COUNTS_CSV, keep_default_na=False)

    if computed.equals(published):
        print(f"MATCH: all {len(published)} counts in "
              f"{COUNTS_CSV.name} reproduced from {SHEET_CSV.name}.")
        return 0

    merged = published.merge(
        computed, on=["category", "item"], how="outer",
        suffixes=("_published", "_computed"), indicator=True)
    bad = merged[
        (merged["_merge"] != "both")
        | (merged["count_published"] != merged["count_computed"])
        | (merged["denominator_published"] != merged["denominator_computed"])
    ]
    print("MISMATCH between recomputed counts and analysis_counts.csv:")
    print(bad.to_string(index=False))
    return 1


if __name__ == "__main__":
    sys.exit(main())
