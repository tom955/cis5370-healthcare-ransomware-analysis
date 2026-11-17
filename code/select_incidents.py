#!/usr/bin/env python3
"""
CIS 5370 Final Project - Stage 1: Incident Selection.

Reproducible selection of 24 healthcare ransomware incidents from the
Ransomware Decade dataset, version 1.0.0 (Zenodo record 15571866,
DOI 10.5281/zenodo.15571866; Sarabi et al., USENIX Security 2025).

Assignment rule implemented literally:
  1. Filter records to sector = Healthcare and incident-date in 2020-2023.
  2. Keep incidents involving a healthcare DELIVERY organization (hospital,
     health system, clinic, or similar care provider). Exclude insurers,
     pharmaceutical companies and technology vendors, unless the attacked
     organization itself delivers care.
  3. Within each year, sort eligible records by the SHA-256 hash of the uuid
     and select the first six (24 total).
  4. Replace an ineligible or duplicate record with the next record in that
     year's order, documenting the reason (see exclusion_log.csv).

Conventions (documented in RUN_NOTES.md):
  * Hash input: the uuid string exactly as stored in incidents.csv
    (lowercase, hyphenated), encoded as UTF-8. Sort key: the lowercase hex
    digest, ascending (lexicographic order = numeric order for fixed-length
    lowercase hex).
  * The eligibility review below covers the first 16 records of each year's
    hash order, which is more than the selection window needs in every year
    (windows close at positions 7, 6, 6 and 9). The script walks the full
    ordered list, so applying the calls in order and taking the first six
    eligible records is exactly the assignment's "sort eligible, take six,
    replace ineligible with next" rule.
  * Records whose organization type is genuinely unclear are marked
    "borderline". A borderline record inside the selection window is counted
    PROVISIONALLY eligible so the pipeline yields a concrete set of 24; every
    such case is flagged in the outputs and in RUN_NOTES.md for adjudication,
    together with the alternate pick that would replace it.

Eligibility calls were made from the dataset's own fields first (victim name
and the source articles stored in the detailed records in incidents.zip),
with quick web checks where the dataset did not say what an organization is
(JDC Healthcare Management, GlobeMed). Each call carries a one-line reason.

Inputs : ../dataset/incidents.csv  (dataset v1.0.0, sha256
         fd1d6eec47fac2fa8fd4baee87e98d56c5ae1e84987cf0d0f62a848004858dd3)
Outputs: ../outputs/selected_24.csv
         ../outputs/exclusion_log.csv
         ../outputs/candidates_by_year.csv
"""

import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
DATASET_CSV = BASE / "dataset" / "incidents.csv"
OUT_DIR = BASE / "outputs"

YEARS = [2020, 2021, 2022, 2023]
PICKS_PER_YEAR = 6
REVIEW_DEPTH = 16  # eligibility calls are provided for the first 16 per year

# ---------------------------------------------------------------------------
# Eligibility review: uuid -> (expected victim name, call, one-line reason)
# call in {"eligible", "ineligible", "borderline"}
# ---------------------------------------------------------------------------
ELIGIBILITY = {
    # ---------------- 2020 ----------------
    "5b6c33a5-90b9-5c49-af92-6d951039f2fb": ("Dr Reddy's Laboratories", "ineligible",
        "Pharmaceutical manufacturer; the assignment explicitly excludes pharmaceutical companies."),
    "b738108b-d8a1-54fc-bfa1-10dcb7858798": ("Personal Touch Home Aides Inc.", "borderline",
        "Home-care agency group (incl. a hospice entity): aides and nurses deliver hands-on care in patients' homes, but it is not a facility-based provider; flagged for adjudication, counted provisionally eligible."),
    "0747a98d-683a-5978-a4c4-8a9325efb5cc": ("Saint Francis Healthcare System", "eligible",
        "Hospital-based health system."),
    "0d33d1d1-93b3-5718-a636-1ad3d624c3b1": ("Sky Lakes Medical Center", "eligible",
        "Hospital."),
    "65739b44-ba4b-55e6-adcf-9946d0250c58": ("Brookside Surgery Center", "eligible",
        "Ambulatory surgery center."),
    "8c8bbe06-c660-52ef-a1ce-dcbd703d2d80": ("Dickingson County Healthcare System", "eligible",
        "Hospital/health system (dataset spelling; Dickinson County Healthcare System, Michigan)."),
    "83929382-81b0-5145-be6a-3657a71457be": ("MultiCare", "eligible",
        "Health system."),
    "185e8dd6-991e-54bc-976b-51b38cdc95c6": ("Valley Health System", "eligible",
        "Health system."),
    "a5717644-e55f-5427-a841-15248af60295": ("Laura Lynn", "ineligible",
        "Children's hospice, but the ransomware attack hit its vendor Blackbaud; the hospice's own systems were not attacked (vendor incident)."),
    "6c3bf601-b8fa-5532-98ea-eea16fb52d58": ("Miltenyi Biotec", "ineligible",
        "Biotechnology / cell-therapy technology company; not a care provider."),
    "5ab5149c-c9d0-5962-87cf-2b5f3a374e42": ("Samaritan Health", "eligible",
        "Health system."),
    "0a58bf26-77e9-57c4-afc0-6d0b8f44b657": ("Alamance Skin Center", "eligible",
        "Dermatology clinic."),
    "6715daa3-0ee2-5652-a4b4-a982cfdb966a": ("Dyras Dental", "eligible",
        "Dental practice."),
    "8134faf2-eaa6-50ab-a694-0ede1aa40e94": ("Jordan Health Center", "eligible",
        "Community health center."),
    "b213ebda-a7a1-5261-9b5b-6e11f62ee829": ("Bristol Myers Squibb", "ineligible",
        "Pharmaceutical company; explicitly excluded."),
    "6012e13f-c148-5aed-a47a-01d14ca07458": ("Centre for Addiction and Mental Health", "eligible",
        "Psychiatric teaching hospital (Toronto)."),
    # ---------------- 2021 ----------------
    "c2da29fb-cd17-54e8-b342-247f1fbe8e81": ("Spine & Disc Medical Center", "eligible",
        "Specialty medical clinic."),
    "cde24666-afbd-5f4f-ba05-ce4bf5cc8552": ("Suncoast Skin Solutions", "eligible",
        "Dermatology practice."),
    "3fd94ece-1c20-589c-84c7-89e98f469c62": ("Barlow Respiratory Hospital", "eligible",
        "Hospital."),
    "891edebd-60de-5b75-963e-8595468ba5b7": ("Harvard Eye Associates", "eligible",
        "Ophthalmology practice."),
    "0a4acd88-393b-5613-8f83-6d8baab57cc7": ("Clinical Hospital No.1 CF Witting", "eligible",
        "Clinical hospital (Bucharest); sources describe a Phobos attack on the hospital's own servers."),
    "c211f5b3-cac4-555c-8664-bfcfa7d3c4df": ("Victory Health Partners", "eligible",
        "Medical clinic (Mobile, AL); source states ransomware infected the clinic's own computer system."),
    "d1f8a660-cad6-5111-a0a6-fb2a398a036d": ("Siegfried", "ineligible",
        "Pharmaceutical manufacturing company (CDMO); not a care provider."),
    "be725069-3053-53fb-92b4-4a55c8a741ff": ("Altona Clinic", "eligible",
        "Medical clinic (Altona, Manitoba)."),
    "1fbe975f-0fd6-5416-a686-1ab7adfaa5d8": ("Memorial Health System", "eligible",
        "Health system."),
    "9ce867a5-9961-5164-b644-2efcbe06b115": ("Coastal Family Health Center", "eligible",
        "Community health center."),
    "f34efccd-79c4-5af9-8cb5-4667419bf120": ("Newberry County Memorial Hospital", "eligible",
        "Hospital."),
    "8e2ae1c3-1362-5470-8a0a-81d853d8a8f3": ("JDC Healthcare Management", "borderline",
        "Legal entity is a dental support/management organization, but it operates Jefferson Dental's clinics and is listed as a practice with ~190 providers; outside the selection window either way."),
    "5c47e493-f87b-5cc4-91c7-ea6a8ac53684": ("Pierre Fabre", "ineligible",
        "Pharmaceutical company; explicitly excluded."),
    "1e5c75a7-18db-5280-aac4-5651e3f6ed85": ("Meddi Laboratório", "borderline",
        "Diagnostic laboratory (Brazil) hit by Avaddon; performs medical testing but does not treat patients; outside the selection window either way."),
    "6fbd1ba0-3d57-58c4-bc5d-00a2c8f6e722": ("Medatixx", "ineligible",
        "Practice-management / EHR software company (Germany); technology vendor."),
    "914726ed-6509-5104-868f-670b2f197642": ("GlobeMed", "ineligible",
        "Healthcare benefits management company / third-party administrator for payers (GlobeMed Saudi); does not deliver care."),
    # ---------------- 2022 ----------------
    "f3ebaca0-3852-5c94-95ad-0c1a0521a160": ("Ascension St. Vincent's Coastal Cardiology", "eligible",
        "Cardiology practice within Ascension."),
    "24a436e5-3906-53e5-a7e4-72b54644c76b": ("Virginia Mason Franciscan Health", "eligible",
        "Health system."),
    "ad922c08-7271-57b3-9d9f-eafdb89f28c6": ("Colosseum Dental", "eligible",
        "Dental care provider chain (Europe)."),
    "23b34f06-1da0-5932-a4b0-d0ab5035e984": ("Geisinger", "eligible",
        "Health system."),
    "1402a8cf-c5f3-5722-81de-919e2fead13f": ("Immanuel Medical Center", "eligible",
        "Hospital."),
    "3642d9b2-1854-5563-a3e6-b95c702d89b5": ("Cheyenne Regional Medical Center", "eligible",
        "Hospital."),
    "9ba8e0ed-810b-54e6-adf9-b231aaaf20a0": ("Austin-Travis County EMS", "ineligible",
        "EMS agency whose only source documents impact from the Kronos/UKG vendor ransomware attack; the ransomware target was its payroll vendor, not the agency's own systems."),
    "7dfb3771-6f06-5665-8674-bfc76a30ee88": ("Medibank", "ineligible",
        "Private health insurer (Australia); the assignment explicitly excludes insurers."),
    "a1d65e0c-780c-5058-aa14-ee1629f4346b": ("Aesthetic Dermatology Associates", "eligible",
        "Dermatology practice."),
    "4514512c-68a0-5559-9470-9e6c23829964": ("SERV Behavioral Health System", "eligible",
        "Behavioral health care provider."),
    "59468e88-7ed1-5961-9fab-3b43dd5b7803": ("GHT Coeur Grand Est Hospitals and Health Care group", "eligible",
        "Public hospital group (France)."),
    "c7bdcb58-f128-53ae-81a1-f1b3f3981252": ("Avamere Health", "eligible",
        "Skilled nursing / post-acute care provider."),
    "6b1dc55a-b742-57a2-b486-fcaca81bb132": ("OakBend Medical Center", "eligible",
        "Hospital."),
    "f1f1aa17-c1f9-5a93-9772-18ac4bcc6929": ("Physiotherapy Board of New Zealand", "ineligible",
        "Professional regulatory/licensing board; does not deliver care."),
    "33f07ed2-535e-5955-971b-7ae9da65f1ee": ("Associated Eye Care Partners", "ineligible",
        "Eye-care management organization whose data was exposed through its vendor Netgain's ransomware incident; its own systems were not the ransomware target."),
    "dce89301-2f70-5be0-85c1-48bcf96eec42": ("Yuma Regional Medical Center", "eligible",
        "Hospital."),
    # ---------------- 2023 ----------------
    "35830ddf-5352-5112-a0e1-b574579928e1": ("Varian Medical Systems", "ineligible",
        "Medical technology / device company; technology vendor, not a care provider."),
    "ac32b272-21a3-5127-848d-f3cb339ac701": ("Tallahassee Memorial Healthcare", "eligible",
        "Hospital / health system."),
    "b93ce527-3dee-528b-8d74-fc16d6a28f4e": ("TransForm Shared Service Organization", "ineligible",
        "Hospital-owned shared-services organization providing IT and supply-chain services to member hospitals; it does not itself deliver care. Consequential call (hash position 3), flagged in RUN_NOTES.md."),
    "95cbd9a6-5b5c-5a78-a7b9-eed31acb0611": ("Manchester Memorial and Rockville General Hospital", "eligible",
        "Hospitals (ECHN, Connecticut)."),
    "ac66e373-5173-53d5-abc0-8edb44f4a848": ("Republican Vilnius Psychiatric Hospital", "eligible",
        "Psychiatric hospital (Lithuania)."),
    "1162cb73-89dd-5c18-8b00-006c15d3f685": ("Fallon Ambulance Services", "borderline",
        "Ambulance/EMS company (medical transport with EMT/paramedic care), but it had ceased operations in Dec 2022 and the breached system was a retained data archive; flagged for adjudication, counted provisionally eligible."),
    "a9ee5c33-ec88-5b94-ba78-838f4c70495b": ("Eye Center of Northern Colorado", "eligible",
        "Eye care clinic."),
    "122bbd07-f441-5dbb-af7d-4a1a9896debe": ("Hawaii Medical Service Association", "ineligible",
        "Health insurer (Blue Cross Blue Shield of Hawaii); explicitly excluded."),
    "3f6dece3-52cf-5c1a-b303-20aa047d95f7": ("Hampton-Newport News CSB", "eligible",
        "Public community services board that directly provides behavioral health care."),
    "145bc094-1b32-50c9-93e6-aa696a3d0f23": ("Methodist Family Health", "eligible",
        "Behavioral health care provider (Arkansas)."),
    "e5b60cc2-d9f5-5973-b93d-ba318b3f2853": ("Fredericksburg Foot & Ankle Center", "eligible",
        "Podiatry clinic."),
    "0395a37f-ff4a-59fb-ac03-376b065b9937": ("Katholische Hospitalvereinigung Ostwestfalen", "eligible",
        "Catholic hospital association operating hospitals (Germany)."),
    "68fba7f4-5532-5463-b668-41f9223add42": ("Waterbury Health", "eligible",
        "Health system."),
    "e22c9142-03fe-5f9d-96df-21c9bf4d35ef": ("Proliance Surgeons", "eligible",
        "Physician surgical practice group."),
    "7eb00270-e6c1-5df6-acb7-4e204c5786e6": ("Michael Garron Hospital", "eligible",
        "Hospital (Toronto)."),
    "f28279fe-c5d8-5731-842a-079d8538a469": ("Arizona Liver Health", "eligible",
        "Specialty liver clinic."),
}


def sha256_of_uuid(uuid_str: str) -> str:
    """SHA-256 hex digest of the uuid string exactly as stored in the CSV."""
    return hashlib.sha256(uuid_str.encode("utf-8")).hexdigest()


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATASET_CSV, dtype=str, keep_default_na=False)
    total_records = len(df)
    assert df["uuid"].is_unique, "dataset contains duplicate uuids"

    # --- Step 1: sector + date filter -------------------------------------
    df["parsed_date"] = pd.to_datetime(df["incident-date"], errors="coerce")
    assert df["parsed_date"].notna().all(), "unparseable incident-date values"
    healthcare = df[df["sector"] == "Healthcare"]
    filtered = healthcare[
        (healthcare["parsed_date"].dt.year >= YEARS[0])
        & (healthcare["parsed_date"].dt.year <= YEARS[-1])
    ].copy()
    filtered["year"] = filtered["parsed_date"].dt.year

    print(f"total records in incidents.csv : {total_records}")
    print(f"sector = Healthcare            : {len(healthcare)}")
    print(f"Healthcare and 2020-2023       : {len(filtered)}")
    for y in YEARS:
        print(f"  {y}: {(filtered['year'] == y).sum()}")

    # duplicate check inside the filtered set (same victim + same date)
    dup_mask = filtered.duplicated(subset=["victim", "incident-date"], keep=False)
    print(f"victim+date duplicates in set  : {int(dup_mask.sum())}")

    # --- Step 2: hash order ------------------------------------------------
    filtered["sha256_of_uuid"] = filtered["uuid"].map(sha256_of_uuid)
    assert filtered["sha256_of_uuid"].is_unique, "hash collision in filtered set"
    filtered = filtered.sort_values(
        ["year", "sha256_of_uuid"], kind="mergesort"
    ).reset_index(drop=True)

    # --- Step 3: eligibility review + selection ----------------------------
    candidate_rows, selected_rows, exclusion_rows = [], [], []
    for year in YEARS:
        sub = filtered[filtered["year"] == year].reset_index(drop=True)
        picks = 0
        window_closed_at = None
        for pos, row in sub.iterrows():
            rank = pos + 1
            entry = ELIGIBILITY.get(row["uuid"])
            if rank <= REVIEW_DEPTH:
                if entry is None:
                    raise SystemExit(
                        f"Missing eligibility call for top-{REVIEW_DEPTH} record "
                        f"{row['uuid']} ({row['victim']}, {year})"
                    )
                expected_name, call, reason = entry
                assert row["victim"] == expected_name, (
                    f"Victim name mismatch for {row['uuid']}: dataset has "
                    f"{row['victim']!r}, review table has {expected_name!r}"
                )
            else:
                call, reason = None, None

            if picks < PICKS_PER_YEAR:
                if call is None:
                    raise SystemExit(
                        f"Selection window for {year} extends past the reviewed "
                        f"top {REVIEW_DEPTH}; extend ELIGIBILITY before running."
                    )
                selected = call in ("eligible", "borderline")
                if selected:
                    picks += 1
                    if picks == PICKS_PER_YEAR:
                        window_closed_at = rank
                    selected_rows.append({
                        "uuid": row["uuid"],
                        "organization": row["victim"],
                        "incident_date": row["incident-date"],
                        "year": int(year),
                        "sha256_of_uuid": row["sha256_of_uuid"],
                        "hash_rank_in_year": rank,
                        "eligibility_call": call,
                        "provisional": "yes" if call == "borderline" else "no",
                        "source_fields_relied_on": (
                            "victim; sector; incident-date; sources "
                            "(detailed record in incidents.zip)"
                        ),
                    })
                else:
                    exclusion_rows.append({
                        "year": int(year),
                        "hash_rank_in_year": rank,
                        "uuid": row["uuid"],
                        "organization": row["victim"],
                        "incident_date": row["incident-date"],
                        "sha256_of_uuid": row["sha256_of_uuid"],
                        "reason": reason,
                    })
            else:
                selected = False

            if rank <= REVIEW_DEPTH:
                candidate_rows.append({
                    "year": int(year),
                    "hash_rank": rank,
                    "uuid": row["uuid"],
                    "organization": row["victim"],
                    "incident_date": row["incident-date"],
                    "sha256_of_uuid": row["sha256_of_uuid"],
                    "eligibility_call": call,
                    "reason": reason,
                    # both flags are recomputed cleanly after the loop
                    "selected": "no",
                    "in_selection_window": "no",
                })
        print(f"{year}: window closed at hash rank {window_closed_at}, "
              f"picks = {picks}")
        assert picks == PICKS_PER_YEAR, f"{year}: got {picks} picks"

    # fix the 'selected' flag in candidates (recompute cleanly)
    selected_uuids = {r["uuid"] for r in selected_rows}
    last_window_rank = {}
    for r in exclusion_rows:
        last_window_rank[r["year"]] = max(last_window_rank.get(r["year"], 0), r["hash_rank_in_year"])
    for r in selected_rows:
        last_window_rank[r["year"]] = max(last_window_rank.get(r["year"], 0), r["hash_rank_in_year"])
    for r in candidate_rows:
        r["selected"] = "yes" if r["uuid"] in selected_uuids else "no"
        r["in_selection_window"] = "yes" if r["hash_rank"] <= last_window_rank.get(r["year"], 0) else "no"

    selected_df = pd.DataFrame(selected_rows).sort_values(
        ["year", "hash_rank_in_year"]
    )
    exclusion_df = pd.DataFrame(exclusion_rows).sort_values(
        ["year", "hash_rank_in_year"]
    )
    candidates_df = pd.DataFrame(candidate_rows).sort_values(
        ["year", "hash_rank"]
    )

    # --- Sanity checks ------------------------------------------------------
    assert len(selected_df) == PICKS_PER_YEAR * len(YEARS), "not 24 selected"
    for y in YEARS:
        assert (selected_df["year"] == y).sum() == PICKS_PER_YEAR, f"{y} != 6"
    assert selected_df["uuid"].is_unique, "duplicate incident selected"
    assert set(selected_df["eligibility_call"]) <= {"eligible", "borderline"}

    selected_df.drop(columns=["hash_rank_in_year"]).to_csv(
        OUT_DIR / "selected_24.csv", index=False
    )
    exclusion_df.to_csv(OUT_DIR / "exclusion_log.csv", index=False)
    candidates_df.to_csv(OUT_DIR / "candidates_by_year.csv", index=False)

    print(f"\nselected total: {len(selected_df)} "
          f"(borderline/provisional: "
          f"{(selected_df['eligibility_call'] == 'borderline').sum()})")
    print(f"exclusions logged: {len(exclusion_df)}")
    print("outputs written to", OUT_DIR)
    return 0


if __name__ == "__main__":
    sys.exit(main())
