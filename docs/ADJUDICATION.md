# Adjudication — Phase 2c (Stage 3): Comparison, Resolutions, Guide v2, Final Sheet

Date: 2026-11-16. Inputs: `coding_sheet_coderA.csv` (24 rows), `claims_coderA.csv`,
`EVIDENCE_NOTES_A.md`; `coding_sheet_coderB.csv` (6 rows), `claims_coderB.csv`,
`EVIDENCE_NOTES_B.md`; `coding_guide.md` v1. Outputs of this phase:
`disagreement_log.csv` (35 rows), `coding_guide.md` v2, `coding_sheet_final.csv`
(24 rows). The claims files were not edited.

Coder B independently double-coded 6 incidents: Brookside Surgery Center, Sky Lakes
Medical Center, Barlow Respiratory Hospital, Geisinger, Tallahassee Memorial Healthcare,
Fallon Ambulance Services. All 11 data columns were compared cell by cell for those 6
rows (66 cells). The adjudication rulings R1–R12 (issued with this phase) were applied
as final; where a ruling was silent, the v1 guide's own definitions (§3.5, §4) governed.

## 1. Disagreement counts

34 of 66 cells differed, plus 1 rationale disagreement (a cell whose value matched but
whose stated basis differed materially). 32 cells were identical, including all 18
organization/year/incident_date cells (both coders copied them from `selected_24.csv`).

| Field | Differing cells (of 6) | Rows involved |
|---|---|---|
| ransomware_confirmed | 2 | Geisinger, Tallahassee |
| services_affected | 4 (+1 rationale) | Sky Lakes, Barlow (+rationale), Tallahassee, Fallon |
| operational_effect | 6 | all six (5 of 6 agree at code level; most differences are wording/coverage) |
| workaround | 4 | Brookside, Sky Lakes, Barlow (cosmetic only), Tallahassee |
| recovery_technical | 4 | Brookside, Sky Lakes, Tallahassee, Fallon |
| recovery_operations | 3 | Brookside, Sky Lakes, Tallahassee |
| recovery_limitations | 5 | Brookside, Sky Lakes, Barlow, Tallahassee, Fallon |
| notes | 6 | all six (expected: each coder recorded conflicts in their own words) |

Closed-value agreement: ransomware_confirmed agreed in 4 of 6 rows; services_affected
sets were identical in 2 of 6 rows (Brookside, Geisinger); operational_effect agreed at
code level (reported content / reported absent / not reported) in 5 of 6 rows. Most
free-text differences were coverage and wording, not substance; the substantive forks
were confirmation at vendor/hedged incidents (Geisinger, Tallahassee), the access-vs-
disruption question (Barlow), pharmacy (Sky Lakes, Tallahassee), the recovery-field
scope questions (Brookside, Sky Lakes, Fallon), and the Brookside identity question.

## 2. How the rulings resolved the disagreements

- **R1 (vendor confirmation)** resolved Geisinger `ransomware_confirmed`: final `yes`
  (Coder B), confirmed at the vendor (OneTouchPoint) level and noted as such. Coder A's
  `unclear` rested on reading confirmation as the customer's own experience; R1 attaches
  confirmation to the attack event behind the record.
- **R2 (hedged confirmation)** resolved Tallahassee `ransomware_confirmed`: final `yes`
  (Coder B) with the caveat in notes that TMH itself never used the word ransomware.
- **R3 (identity)** resolved the Brookside identity conflict and, with it, Brookside's
  `operational_effect` and `workaround`: the 2019-sourced facts are coded directly
  (Coder B's approach). See §3 below.
- **R4 (access vs. disruption)** resolved Barlow `services_affected` against both
  coders' EHR coding (see the rationale disagreement below) and confirmed the
  Personal Touch vendor-hosted refinement in the sweep.
- **R5 (pharmacy)** resolved Sky Lakes and Tallahassee `services_affected`: pharmacy
  coded in both (Coder B), because the pharmacy workflow ran on downtime procedures
  (barcode scanning out and pads exhausted at Sky Lakes; paper prescription pads
  replacing an electronic process at Tallahassee).
- **R6 (taxonomy)** supplied the label `general IT systems (unspecified)`, applied to
  Barlow's generic IT disruption and swept to Suncoast, Witting, Victory, Hampton and
  Colosseum; Colosseum's "practices closed" service label was removed because closure
  is an operational-effect outcome, not a service.
- **R7 (recovery boilerplate)** resolved Fallon `recovery_technical` for Coder B
  (`not reported`) and removed Coder A's boilerplate-based cells at Hampton and
  Panorama/Eye Center in the sweep.
- **R8 (operations never interrupted)** changed no disputed cell (the coders agreed on
  `not reported` in the affected cells) but changed three agreed cells in the six rows
  (Barlow, Geisinger, Fallon `recovery_operations`) and three rows in the sweep
  (MultiCare, Witting, Ascension).
- **R9 (parent statements)** was applied to the two CommonSpirit division rows in the
  sweep (VMFH, Immanuel); see §4.
- **R10 (structural absence)** resolved Fallon `services_affected` for Coder A
  (`reported absent`, structural basis stated in notes).
- **R11 (retrospectives)** resolved the Sky Lakes count conflict (contemporaneous
  November 2020 figures govern; the IS director's retrospective figures are recorded
  in notes) and the Tallahassee restoration date (TMH's own February 15, 2023
  announcement governs over the February 23 report date Coder A used).
- **R12 (lawsuit allegations)** drove the Personal Touch `operational_effect` rewrite
  in the sweep (see §4).

Disagreements resolved under the v1 guide's own definitions rather than R1–R12:
Brookside `recovery_technical` and `recovery_operations` (final `reported absent`,
Coder B — sources explicitly state the files could not be recovered and the practice
closed instead of resuming; guide §4), Brookside `recovery_limitations` (Coder A's
content retained — permanent data loss is a continuing limitation under §3.5), Sky
Lakes `recovery_operations` (Coder A's November 9 radiation-oncology resumption
adopted as an operations milestone under §3.5, with Coder B's no-return-to-normal
caution stated in the cell), Fallon `recovery_limitations` (Coder A's content retained
under §3.5, which lists "breach notification still pending" as a limitation), and
Geisinger `operational_effect` (Coder B's `reported absent`, on OTP's filed statement
that its business customers' systems were not impacted; guide §4). The remaining
differing cells were editorial merges of source-backed text (both coders' claim-backed
content unioned) or wording-only differences (Barlow `workaround` differed only by an
article and a trailing period).

The one rationale disagreement: **Barlow's EHR**. Both coders coded
`EHR/clinical records`, but Coder A's stated basis was access/breach reporting
(expressly not an outage) while Coder B's was that the named system was involved and
its files encrypted/exfiltrated. Under R4 neither basis codes the service — no source
reports EHR downtime, and the sources that mention encryption do not tie it to the EHR
itself — so the label was removed, the breach is documented in notes, and the generic
IT disruption in the hospital's own AG letter is coded under the R6 label.

## 3. The Brookside decision (R3)

The dataset record (CBS Detroit, January 23, 2020) names "Brookside Surgery Center,
Battle Creek"; all richer coverage (spring 2019: WWMT via Nelson Hardiman, HIPAA
Journal, Health IT Answers, Becker's) names "Brookside ENT and Hearing Center",
Battle Creek. Both coders independently reached the same conclusion, and adjudication
confirms it: **these are the same incident.** The distinctive facts match uniquely —
the $6,500 ransom demand, deletion of all patient records, appointment schedules and
payment information after the owners refused to pay, data deleted but not shared, and
the FBI investigation — and no separate January 2020 Brookside incident exists in any
source either coder found. The final sheet keeps the dataset date (2020-01-23) and the
dataset organization name per guide §6, records both dates and the name difference in
notes, and keeps the 2019-sourced claims (services, closure on April 30, 2019, the
walk-in workaround, the permanent loss). The practical consequence: Brookside's row is
a full row (the only incident in the 24 where the attack ended the organization)
rather than the near-empty row the dataset's single 2020 item would have produced.

## 4. Swept changes outside the six double-coded rows

`coding_sheet_final.csv` starts from Coder A's 24 rows. Beyond the six double-coded
rows (31 cells changed there, including the three R8 applications in §5), the v2 rules
were swept across the other 18 rows wherever the same patterns occur — 19 cells in 11
rows:

| Organization | Field | Change | Rule |
|---|---|---|---|
| Personal Touch Home Aides | operational_effect | Rewritten: sourced facts stated (vendor ransomware notified Dec 1, 2019; org notice reports no downtime); the records-inaccessible/care-disrupted claim now presented explicitly as a flagged class-action allegation | R12 |
| Personal Touch Home Aides | notes | Adjudication note appended: EHR code is vendor-mediated (the ransomed host ran the cloud EHR); the allegation flag stated | R4, R12 |
| MultiCare | recovery_operations | `not reported` → `n/a - operations not interrupted` | R8 |
| Suncoast Skin Solutions | services_affected | `other (some systems encrypted; specific systems not named)` → `general IT systems (unspecified)` | R6 |
| Clinical Hospital No.1 CF Witting | services_affected | `other (hospital servers/data encrypted; specific clinical systems not named)` → `general IT systems (unspecified)` | R6 |
| Clinical Hospital No.1 CF Witting | recovery_operations | `not reported` → `n/a - operations not interrupted` | R8 |
| Victory Health Partners | services_affected | `other (clinic computer system shut down after detection)` → `general IT systems (unspecified)` (the shutdown itself remains stated in operational_effect) | R6 |
| Ascension St. Vincent's Coastal Cardiology | recovery_operations | `not reported` → `n/a - operations not interrupted` | R8 |
| Virginia Mason Franciscan Health | recovery_limitations | Parent-level clause removed ("at parent level, as of Nov. 9 not all EHR systems and patient portals were back online"); division-sourced content retained | R9 |
| Virginia Mason Franciscan Health | notes | The Nov. 9 parent-level statement recorded here, flagged as not explicitly covering VMFH | R9 |
| Colosseum Dental | services_affected | `other (dental practice operations - practices closed)` → `general IT systems (unspecified)` (systems held hostage, none named; the closures remain in operational_effect) | R6 |
| Immanuel Medical Center | recovery_technical | Parent-level clause removed ("at parent level, by Nov. 10 the majority of impacted hospitals/clinics had EHR access again"); the CHI Health (division) October 18 restoration statement retained | R9 |
| Immanuel Medical Center | recovery_limitations | Parent-level Nov. 10 portal-scheduling clause removed; breach-notification content retained | R9 |
| Immanuel Medical Center | notes | The Nov. 10 parent-level statement recorded here, flagged as not explicitly covering Immanuel | R9 |
| Eye Center of Northern Colorado | recovery_technical | Panorama's "experts engaged / all systems now secure" statement removed → `not reported` | R7 |
| Eye Center of Northern Colorado | notes | Adjudication note appended recording the R7 basis | R7 |
| Hampton-Newport News CSB | services_affected | `other (certain computer systems disrupted; ...)` → `general IT systems (unspecified)` | R6 |
| Hampton-Newport News CSB | recovery_technical | "Took steps to secure its systems and engaged outside experts" removed → `not reported` | R7 |
| Hampton-Newport News CSB | notes | Adjudication note appended recording the R7 basis | R7 |

Note on the VMFH recovery_technical cell: it also contains a CommonSpirit statement
("systems were returned to the network once secured, with additional security and
monitoring tools"), but that statement comes from the CommonSpirit breach notice
addressed to VMFH's own patients (quoted by TechTarget), so it explicitly covers the
division and is retained under R9.

## 5. Rule-driven changes to cells the coders agreed on

Three cells inside the six double-coded rows changed although A and B agreed, because
R8 supplies a value v1 lacked:

- Barlow `recovery_operations`: `not reported` → `n/a - operations not interrupted`.
- Geisinger `recovery_operations`: `not reported` → `n/a - operations not interrupted`
  (operational_effect is `reported absent` and Geisinger care was never interrupted;
  see the flag in §7).
- Fallon `recovery_operations`: `not reported` → `n/a - no active operations`.

## 6. Claims-backing notes (claims files untouched, per instructions)

Where a rule change removed or reframed a final cell, the supporting claim rows remain
in the claims files; their status is recorded here rather than edited there:

- Fallon `recovery_technical` (R7): the claims_coderA row sourced to SafetyDetectives
  ("took steps to secure the data storage archive and initiated a comprehensive
  investigation") no longer backs any coding-sheet cell.
- Hampton `recovery_technical` (R7): the claims_coderA row sourced to HNNCSB's own
  statement (securing systems, engaging experts) no longer backs a cell; the fact is
  acknowledged in the final notes.
- Eye Center `recovery_technical` (R7): the claims_coderA row sourced to HIPAA Journal
  (Panorama: experts engaged, "all of its systems and networks are now secure") no
  longer backs a cell; acknowledged in the final notes.
- Barlow `services_affected` (R4): the EHR access/breach claim rows in both claims
  files now back the notes documentation of the breach, not a services value. The
  final `general IT systems (unspecified)` value is backed by the CA AG letter text in
  claims_coderA ("an incident that disrupted the operations of our IT systems") and
  Becker's "affecting several IT systems" claim.
- VMFH `recovery_limitations` and Immanuel `recovery_technical`/`recovery_limitations`
  (R9): the parent-level claim rows (Fierce Healthcare; TechTarget, Nov. 10) now back
  the notes statements instead of recovery cells.
- Personal Touch `operational_effect` (R12): the ClassAction.org claim row now backs
  an explicitly flagged allegation statement inside the cell, not a factual assertion.

## 7. Flagged for the lead

**No disagreement was left unresolved.** All 35 logged disagreements were resolved
under R1–R12 or under the v1 guide's own definitions (§3.5, §4), as recorded in
`disagreement_log.csv`. The following judgment calls were resolved with stated
reasoning but are flagged so the lead can revisit them with full visibility:

1. **Fallon `recovery_limitations`** — resolved for Coder A under guide §3.5 (which
   lists "breach notification still pending" as a limitation). Coder B's narrower
   reading — that recovery fields presuppose a disruption at the coded organization,
   which would also move this content to notes — is reasonable and is the single most
   contestable scope call in the phase. The v2 guide now states the adopted convention
   (§3.5 clarification).
2. **Sky Lakes `recovery_operations`** — resolved under §3.5 by treating the November 9
   radiation-oncology resumption as an operations milestone. Coder B's stricter
   reading (no operations milestone without a stated return-to-normal for appointments,
   surgeries or admissions) is recorded in the log; the final cell states the caveat.
3. **Geisinger `recovery_operations` (R8 application)** — R8's condition is met
   literally, but Geisinger is a vendor row where Coder B deliberately left every
   recovery field `not reported` ("no Geisinger disruption to recover from"). The
   `n/a` value was applied for consistency with the other never-interrupted rows;
   flagged for confirmation.
4. **Personal Touch `services_affected` (closest call in the sweep)** — `EHR/clinical
   records` was retained under R4's vendor-hosted refinement: the ransomed Crossroads
   host itself ran Personal Touch's cloud-based EHR, so the hosted service was the
   encrypted system. The only source describing the records as inaccessible is the
   class-action allegation (now flagged in the effect cell under R12). If the lead
   reads R4 strictly, the alternative is `not reported` with the hosted-EHR facts in
   notes.
5. **Vendor ransom-paid data returns retained under R7** — MultiCare, Harvard Eye
   Associates and Colosseum Dental keep `recovery_technical` cells describing a ransom
   payment followed by return of the stolen data (Colosseum: the organization's
   estimate that it had all data back). These were judged concrete, dated recovery
   events rather than generic "we secured our systems" boilerplate, and the cells are
   framed at the vendor level where applicable. Under the strictest reading of R7
   (restored/rebuilt/back online only) they would move to notes; flagged as borderline.

## 8. Guide v2 changelog summary

`coding_guide.md` is now v2 (2026-11-16). R1–R12 were added as explicit rules in the
relevant sections (§2: R11; §3.1: R1, R2; §3.2: R4, R5, R6 plus the new taxonomy label;
§3.5: R7, R8, R9 and the recovery_limitations scope clarification; §3.6: R3; §4: R10;
§5: R12), each with its originating incident. The §8 changelog entry in the guide lists
what the double-coding comparison changed and why, rule by rule. No v1 rule was
deleted. The final sheet was produced under v2 and differs from Coder A's sheet in 50
cells (31 in the six double-coded rows, 19 in the sweep), each traceable to
`disagreement_log.csv` (for the six) or to the table in §4 above (for the sweep).

## 8. Lead confirmation of the flagged judgment calls (2026-11-16)

All five calls flagged in section 7 are CONFIRMED as resolved:

1. Fallon recovery_limitations: A's notification timeline stays in limitations. Breach-notification tails are coded as continuing limitations consistently across the sample (Barlow, Suncoast, Eye Center); Fallon is not singled out.
2. Sky Lakes recovery_operations: A's dated service-level resumption (Nov 9, radiation oncology) counts as an operations-resumed milestone under the guide's definition, with B's no-full-return-to-normal caveat kept in the cell.
3. Geisinger recovery_operations: the R8 n/a value stands. OTP's filed statement says customer operations were not impacted, so there was no resumption to report.
4. Personal Touch services: the EHR label is RETAINED with the vendor-mediated note. The hosted EHR the agency's staff use to deliver care was disrupted by the vendor incident; treating vendor-hosted and on-premise systems differently for the same functional loss would distort the sample.
5. Vendor ransom-paid data-return cells (MultiCare, Harvard Eye, Colosseum): retained as technical milestones. R7 targets generic response boilerplate; a dated ransom payment followed by data return is a concrete restoration event.

Phase 2 is closed. The final coding sheet and Coding Guide v2 are the basis for the analysis phase.
