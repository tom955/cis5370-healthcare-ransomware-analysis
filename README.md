# Analyzing Healthcare Ransomware Disruption and Recovery

CIS 5370 Principles of Cybersecurity, final project.

## Project purpose

This project studies what public reports actually show about how ransomware
disrupts healthcare services, how the affected organizations recover, and
what the public record leaves unclear. It builds a small, carefully verified
sample of 24 healthcare ransomware incidents from 2020 to 2023 and codes each
one against the same set of questions: which services were disrupted, what
the operational effect was, what workaround the organization used, and what
recovery looked like, split into technical restoration, resumption of
operations, and limitations that continued after systems came back.

## Description

The sample comes from the Ransomware Decade dataset (version 1.0.0). The
selection follows a fixed rule so anyone can reproduce it: take the
healthcare records dated 2020 to 2023, keep the ones where the attacked
organization itself delivers care (hospitals, health systems, clinics and
similar providers, not insurers, pharmaceutical companies or technology
vendors), sort each year's records by the SHA-256 hash of the record uuid,
and take the first six per year.

Each selected incident was then verified and coded from public sources: the
source articles stored in the dataset, organization statements, reputable
news coverage, and official records such as HHS OCR breach entries. Every
coded claim carries a source. A field is coded "not reported" when the
sources are silent, which is kept separate from "reported absent," where a
source states that the thing did not happen. Two coders independently coded
six of the incidents, the disagreements were compared and adjudicated, and
the coding guide was revised to version 2 before the analysis was run. The
project does not estimate how often these effects occur across all
healthcare ransomware attacks, and it does not infer patient harm from
missing or indirect evidence.

## Threat model

The threat actor is a ransomware operator (in some incidents working through
an affiliate or an initial access broker) who gains access to a healthcare
delivery organization's systems, or to a vendor that hosts its systems or
data, and encrypts systems or data and typically also steals data for
extortion. The study starts after that point. It examines the reported
effects on care delivery and operations and the reported recovery. It does
not reconstruct initial access methods that were not publicly disclosed, and
it uses public records only: no hospital systems, no patient records, and no
malware samples are involved.

## Setup

- Python 3.10 or newer, with pandas.
- The dataset is not included in this repository. Download it from the
  authors' official artifact on Zenodo:
  - Record: https://zenodo.org/records/15571866
  - DOI: 10.5281/zenodo.15571866
  - Version: 1.0.0 (the only version listed on the record)
  - Paper: Sarabi, Huang, Wang, Karir and Liu, "The Ransomware Decade: The
    Creation of a Fine-Grained Dataset and a Longitudinal Study," USENIX
    Security 2025.
- Download these three files into a folder named `dataset` in the
  repository root (the folder is listed in .gitignore, so the files stay
  local):
  - `incidents.csv`
  - `incidents.zip`
  - `schema.json`
- Verify the downloads before running anything. The MD5 checksums published
  in the Zenodo record are:
  - incidents.csv: 0937ce926fae9da1b901ebb8f8b27c3c
  - incidents.zip: de2420cf705c8d98de5c8b30c3b60998
  - schema.json: 4d85b5bf4cab1cc4c1025e3bb947c4fd
- The SHA-256 values we computed locally for the same files are:
  - incidents.csv: fd1d6eec47fac2fa8fd4baee87e98d56c5ae1e84987cf0d0f62a848004858dd3
  - incidents.zip: 516422b83ceb011572b915c4f81f6e0b116917cdbda65949abada4ececace27d
  - schema.json: 107f072ab36b7e21dc768373dbf5f6610e504abc64374b7fcd80a34cdb6271bc

## How to run the experiments

1. Selection. With the dataset files in `dataset/` as described above, run:

   ```
   python3 code/select_incidents.py
   ```

   The script filters the dataset, applies the eligibility calls documented
   in its header, walks each year's hash order, and writes
   `outputs/selected_24.csv`, `outputs/exclusion_log.csv` and
   `outputs/candidates_by_year.csv`. The committed copies of the selection
   outputs are in `data/`. Re-running the script reproduces
   `selected_24.csv` and `candidates_by_year.csv` exactly; the committed
   `exclusion_log.csv` is the script output plus one adjudication note
   added later to the TransForm row (see `docs/ADJUDICATION.md`).

2. Analysis counts. Run:

   ```
   python3 code/compute_counts.py
   ```

   The script reads `data/coding_sheet_final.csv`, recomputes every count in
   `data/analysis_counts.csv`, and prints MATCH if all counts reproduce. It
   exits with a nonzero status and prints the differing rows if they do not.

## Expected results

- Selection: 24 incidents, exactly 6 per year for 2020, 2021, 2022 and 2023,
  with 4 records skipped inside the selection windows and documented in
  `data/exclusion_log.csv`.
- Counts: `code/compute_counts.py` reports a full match against
  `data/analysis_counts.csv` (88 count rows).

## Results

The full analysis is in `docs/ANALYSIS.md`. The headline findings:

- The EHR and clinical records are the most frequently coded disrupted
  service (10 of 24 incidents). The next largest category is a residual one,
  "general IT systems (unspecified)" (6 of 24), which appears when breach
  notices say systems were affected without naming any.
- Recovery is reported unevenly. Continuing limitations are the most
  reported recovery fact (18 of 24), ahead of technical restoration
  (11 of 24), and an operations-resumption milestone is the least reported
  (6 of 24). The limitations are dominated by breach notification and data
  tails that run for months after the clinical story ends.
- Workarounds are not reported in 13 of 24 incidents. Where they are
  reported, paper and manual downtime procedures are the most common type.
- 6 of the 24 incidents are vendor-mediated: the attacked organization was a
  vendor or business associate of the named healthcare organization. In
  those rows the public record is mostly a breach record (what data, how
  many people, when they were told), while direct incidents more often have
  an operations record (what stopped, how care continued, what came back).
- Two coders agreed on most closed values in the double-coded sample; the
  disagreements and how they were resolved are in `docs/ADJUDICATION.md`,
  and the coding rules they produced are in `docs/coding_guide.md`
  (version 2).

## Repository layout

- `code/select_incidents.py`: reproducible incident selection (stage 1).
- `code/compute_counts.py`: recomputes and verifies the analysis counts.
- `data/selected_24.csv`: the 24 selected incidents.
- `data/exclusion_log.csv`: records skipped inside the selection windows,
  with reasons.
- `data/coding_sheet_final.csv`: the adjudicated final coding sheet.
- `data/analysis_counts.csv`: the counts behind the analysis memo.
- `docs/coding_guide.md`: the coding guide, version 2.
- `docs/ADJUDICATION.md`: double-coding disagreements and their resolution.
- `docs/ANALYSIS.md`: the comparative analysis memo.

## Contributors

Tomas Ortiz Lara, Dario Castillo, and Ethan Choi (Group 4).
