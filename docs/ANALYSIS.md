# Phase 3 — Comparative Analysis Memo

Date: 2026-11-16. Basis: `coding_sheet_final.csv` (the adjudicated final sheet,
24 incidents), read together with `claims_coderA.csv` and `claims_coderB.csv` for
supporting detail, `coding_guide.md` v2 for definitions, and `ADJUDICATION.md` for
the Phase 2c decisions. **Every number in this memo was recomputed from the final
sheet for this phase; the coder A and coder B sheets were not used for any count.**
The machine-readable counts behind this memo are in `analysis_counts.csv` (one row
per counted item: category, item, count, denominator).

Conventions used below, per Coding Guide v2: a field "carries reported content" when
its cell is a source-backed summary; `reported absent` means a source (or, for
Fallon, the structural facts under rule R10) establishes that the thing did not
happen; `n/a` in `recovery_operations` is the R8 value for operations that were
never interrupted (or, for Fallon, never existed). "Not reported" always means the
sources found were silent, never that the thing did not happen.

## 1. Sample summary

- **24 incidents, 6 per year** by dataset year: 2020: 6, 2021: 6, 2022: 6, 2023: 6.
  The even split is a property of the selection rule (six per year), not a finding
  about attack frequency. The sheet's year is the dataset year; Section 5 notes
  several rows where the attack itself happened in a different year than the
  dataset date suggests.
- **Ransomware confirmation (guide v2): 24 of 24 coded `yes`.** No row in the final
  sheet is coded `no` or `unclear`, so after adjudication the confirmation variable
  carries no variance; the information sits in two caveats:
  - **Geisinger** is `yes` at the vendor level only (rule R1): the encrypted
    organization was Geisinger's printing and mailing vendor OneTouchPoint, and no
    source reports encryption at, or disruption to, Geisinger itself.
  - **Tallahassee Memorial Healthcare** is `yes` under rule R2: TMH itself never
    used the word ransomware (it said "IT security issue"), and the `yes` rests on
    sources with direct knowledge describing a suspected ransomware attack, with no
    source contradicting it.
  Both rows were coded `unclear` by one coder in Phase 2 and were resolved to `yes`
  by adjudication; the caveats above are recorded in the rows' notes.
- **The 24 rows cover 23 distinct attack events.** Virginia Mason Franciscan Health
  and Immanuel Medical Center are two division-level rows of the same parent
  CommonSpirit Health incident (access September 16 to October 3, 2022). Counts in
  this memo are per row, as coded; readers should keep the shared event in mind for
  the 2022 rows.
- **Reporting strength.** The final sheet contains no coded reporting-strength
  variable, so no strength distribution is reported as a coded result. As a derived
  completeness check (computed from the final sheet for this memo only), the number
  of the six analytic fields coded `not reported` per incident distributes as:
  0 fields not reported: 7 incidents; 1: 3 incidents; 2: 5 incidents; 3: 2
  incidents; 4: 5 incidents; 5: 2 incidents. The two thinnest rows are Harvard Eye
  Associates and Eye Center of Northern Colorado, each with only one analytic field
  carrying reported content (a vendor-level technical event and a notification
  timeline, respectively). The two richest rows by service labels are Manchester
  Memorial and Rockville General Hospital (12 service labels) and Sky Lakes Medical
  Center (10 service labels).

## 2. Service-to-workflow disruption table

One row per service in the guide v2 taxonomy. "Coded disrupted" counts incidents
whose final `services_affected` cell carries that label. "Not coded" is 24 minus
that count; it decomposes into rows where other services were coded but not this
one (19 rows have at least one service coded), the 4 rows where the services field
as a whole is `not reported` (MultiCare, Harvard Eye Associates, Geisinger, Eye
Center of Northern Colorado), and the 1 row where it is `reported absent` (Fallon
Ambulance Services). A service not being coded means the reporting did not tie that
service to the incident; it does not mean the service was unaffected.

| Service | Workflow it supports | Coded disrupted (of 24) | Not coded (of 24) | Downstream operational effects reported in the same incidents |
|---|---|---|---|---|
| EHR/clinical records | Clinical documentation and patient chart access during care | 10 | 14 (9 with other services coded, 4 field not reported, 1 field reported absent) | The widest range in the sample. Sky Lakes: all hospital systems offline, major downtime roughly three weeks. Tallahassee: network offline, EMS diversion, non-emergency surgeries and outpatient procedures cancelled, 13 days of IT downtime. Manchester Memorial and Rockville General: emergency departments closed and patients diverted, elective surgeries and outpatient appointments suspended. Virginia Mason Franciscan Health: appointments cancelled or rescheduled, patient portal suspended. Immanuel Medical Center: appointments rescheduled, some surgeries delayed. Brookside: records deleted and the practice closed permanently. Saint Francis (Ferguson Medical Group): all data including medical records inaccessible, services described as disrupted, no specific cancellations reported. Dickingson County: EHR offline with considerable disruption, but the emergency department and nearly all care stayed open, no diversion. Personal Touch: the organization's own notice reports no downtime; inaccessibility of records and disrupted care appear only as a flagged class-action allegation (rule R12). Ascension Coastal Cardiology: operational effect reported absent for current care; only pre-October 2021 legacy records were encrypted. |
| general IT systems (unspecified) | Not specifiable from the reporting; the label exists (rule R6) for "some systems encrypted or disrupted, none named" | 6 | 18 (13, 4, 1) | Effects range from none to severe, which is the point of the label: Colosseum Dental reports more than 100 Benelux practices closed for days; Victory Health Partners reports the clinic system shut down with no care-delivery effect reported; Hampton-Newport News CSB reports technical disruptions with no specific service-delivery effect found; Barlow Respiratory Hospital and Clinical Hospital No.1 CF Witting both report the operational effect absent (care not interrupted); Suncoast Skin Solutions reports no operational effect at all. |
| scheduling/appointments | Appointment booking, registration, admissions scheduling | 5 | 19 (14, 4, 1) | Brookside: schedules deleted with the records, contributing to the permanent closure. Virginia Mason Franciscan Health and Immanuel: appointments cancelled or rescheduled. Tallahassee: non-emergency appointments rescheduled. Manchester Memorial and Rockville General: outpatient appointments suspended and several outpatient services closed until further notice. |
| billing/administrative | Billing, coding, insurance verification, payroll, general office systems | 5 | 19 (14, 4, 1) | Cheyenne Regional: the payroll/timekeeping outage mis-paid more than 2,000 employees (about 55% overpaid, about 45% underpaid) and some HR systems stayed down for months; no patient-care effect reported. Manchester Memorial and Rockville General: the hospitals could not bill properly for about six weeks, could not pay supply vendors or receive Medicaid reimbursements, and Connecticut provided $7 million in support. Vilnius Psychiatric Hospital: employees' administrative functions were limited. Sky Lakes: accounting, billing and email were lower restoration priorities and took longer to restore. Brookside: payment information deleted with the records. |
| imaging/radiology | Diagnostic imaging ordering and viewing (PACS), radiology reading | 4 | 20 (15, 4, 1) | Sky Lakes: PACS down for days, diagnostic imaging curtailed, radiologists read studies on modality consoles and burned images to CDs. Virginia Mason Franciscan Health: a patient reported waiting about two weeks for MRI results and three hours after an X-ray. Manchester Memorial and Rockville General: outpatient medical imaging closed with the other outpatient services. Vilnius Psychiatric Hospital: certain radiology services could not be provided (the only service-level evidence in that row comes from a 2025 Lithuanian regulator decision). |
| surgery/procedures | Operating-room and procedure scheduling and performance | 4 | 20 (15, 4, 1) | Tallahassee: all non-emergency surgical and outpatient procedures cancelled, still cancelled on February 6, 2023, resuming only on a limited basis before February 15. Manchester Memorial and Rockville General: elective surgeries suspended, closed until further notice. Immanuel (CHI Health): some surgeries delayed, including a colonoscopy cancelled on arrival. Sky Lakes: some procedures shut down and computer-controlled cancer treatments could not be offered. |
| laboratory | Lab ordering and results workflows | 3 | 21 (16, 4, 1) | Coded only inside the three widest outages (Sky Lakes, Tallahassee, Manchester Memorial and Rockville General); in Manchester, outpatient blood draws were among the suspended services. No incident in the sample reports a laboratory-specific effect separate from the general outage. |
| communications | Phone systems, email, internal messaging, patient portals | 3 | 21 (16, 4, 1) | Virginia Mason Franciscan Health: patient portal access suspended. Manchester Memorial and Rockville General: a temporary phone system had to be set up for patients to reach providers. Sky Lakes: communications were part of the all-systems outage (extra bandwidth was donated by a local telecom). |
| pharmacy | Medication dispensing, pharmacy systems, e-prescribing | 2 | 22 (17, 4, 1) | Coded only where downtime artifacts were reported (rule R5): Sky Lakes ran pharmacy on downtime procedures (barcode scanning out, paper prescription pads) while already-filled prescriptions remained available; Tallahassee used paper prescription pads as part of its paper documentation. Pharmacy's low count reflects what reporting mentions, not evidence that medication workflows were untouched elsewhere. |
| emergency care/patient diversion | Emergency department intake and ambulance routing | 2 | 22 (17, 4, 1) | Tallahassee: EMS patients diverted, accepting only Level 1 traumas from the immediate service area plus stroke and heart-attack patients; some diversion still in place on February 8, 2023. Manchester Memorial and Rockville General: both emergency departments closed for much of August 3, 2023 and patients were diverted to nearby centers; the departments reopened late the same day. Note the near-misses the coding excludes: Sky Lakes and Dickingson County both kept emergency care open with diversion explicitly not reported for them, and diversion reported for MercyOne in the CommonSpirit incident is not coded to the Virginia Mason row. |
| other (specify) | Varies by specification | 3 incidents carry `other` labels (8 labels total) | 21 | Sky Lakes: other (radiation oncology), other (cardiology), other (supply chain system) inside its all-systems outage; radiation oncology was restored as a named milestone on November 9, 2020. Manchester Memorial and Rockville General: other (wound healing center), other (urgent care center), other (women's wellness center), other (outpatient physical therapy), all closed until further notice. Spine & Disc Medical Center: other (organization website), the only coded service in that row; the website was unreachable for a few days and no care-delivery effect was reported. |

Reading of the table: the EHR is the most frequently coded disrupted service
(10 of 24), and the incidents where it is coded include every large care-delivery
outage in the sample. The second-largest category is not a clinical service at all
but the residual `general IT systems (unspecified)` label (6 of 24), which measures
a reporting habit (notices that name no systems) rather than a workflow. Below the
EHR, scheduling and billing/administrative (5 each) are coded more often than any
other named clinical service, and the services closest to the bedside after the EHR
(imaging and surgery/procedures, 4 each; laboratory and communications, 3 each;
pharmacy and emergency diversion, 2 each) are coded mainly when an outage was wide
enough for reporting to enumerate services at all.

## 3. Recovery comparison

The three recovery sub-fields are reported very unevenly across the 24 incidents:

| Recovery sub-field | Reported content | Reported absent | n/a (R8) | Not reported |
|---|---|---|---|---|
| Technical restoration | 11 | 1 (Brookside) | 0 | 12 |
| Operations resumed | 6 | 1 (Brookside) | 6 | 11 |
| Continuing limitations | 18 | 0 | 0 | 6 |

Continuing limitations are the most-reported recovery fact in the sample
(18 of 24), ahead of technical restoration (11 of 24), and an operations-resumption
milestone is the least-reported (6 of 24). Two cautions attach to the operations
count. First, 6 further rows carry the R8 `n/a` value (MultiCare, Barlow, Witting,
Ascension, Geisinger, Fallon), meaning operations were never interrupted or never
existed, so there was nothing to resume; those rows are answers, not gaps. Second,
one of the 6 content cells (Dickingson County) reports that routine care was
maintained throughout and explicitly notes that no separate resumption milestone
was reported, and one (Sky Lakes) documents a single service's resumption
(radiation oncology, November 9, 2020) while stating that no source gives a general
return-to-normal date. Brookside is the only incident coded `reported absent` on
both restoration and resumption: the files could not be recovered and the practice
closed instead of resuming.

**What the continuing limitations consist of.** Grouping the 18 rows that report
limitations (a row can fall in more than one group; 22 group assignments across
18 rows):

- **Notification and data tails: 11 of 18** (MultiCare, Suncoast Skin Solutions,
  Barlow, Ascension, Virginia Mason Franciscan Health, Immanuel, Tallahassee,
  Vilnius Psychiatric Hospital, Fallon, Eye Center of Northern Colorado,
  Hampton-Newport News CSB). The dominant pattern: the clinical/technical story
  ends long before the breach process does. Individual identification and
  notification were still pending, in preparation, or running in stages months
  after the incident in MultiCare (notification in preparation February-March
  2021), Suncoast (letters began November 28, 2022), Barlow (determinations into
  February-March 2022), Fallon (review completed December 27, 2023, roughly eight
  months after detection), Eye Center of Northern Colorado (notification from June
  2024, about a year after the June 2023 detection) and Hampton-Newport News CSB
  (notifications mailed around January 11, 2024, roughly two months after
  discovery). Vilnius also records about 48,000 files published.
- **Permanent data loss: 4 of 18** (Saint Francis, Sky Lakes, Brookside, Ascension).
  Saint Francis permanently lost Ferguson Medical Group records for services
  between September 20 and December 31, 2018 plus all scanned documentation; Sky
  Lakes permanently lost 140 archived images of 1.5 million; Brookside lost all
  patient files when the ransom was refused; Ascension's legacy EMR data remained
  encrypted and inaccessible, so the organization could not determine exactly what
  information was affected.
- **Prolonged service limits: 5 of 18** (Sky Lakes, Dickingson County, Virginia
  Mason Franciscan Health, Tallahassee, Manchester Memorial and Rockville
  General). Sky Lakes reports full organizational recovery taking about seven
  months with support systems restored later and elective services still cut back
  in mid-November 2020; Dickingson County still had about 5% of systems
  outstanding on November 19, 2020 with full recovery expected by year-end;
  Virginia Mason's restoration was partial and phased (only some records systems
  back by October 17, 2022); Tallahassee expected continuing hurdles and patient
  delays after its February 15, 2023 return to standard operations; Manchester's
  billing function stayed impaired for about six weeks with payment problems
  persisting after systems returned.
- **Other: 2 of 18** (Colosseum Dental, Cheyenne Regional). Colosseum's attackers
  had deleted backups before encrypting, which reporting says left no option but
  to pay, and whether data leaked was uncertain; Cheyenne was still recovering
  employee overpayments at the March 26, 2022 report, offering extended repayment
  options.

**Dated milestones.** A minority of rows carry enough dates for a rough timeline
statement. No averages are computed; the sample's dating problems (Section 5) do
not support them.

- **Sky Lakes Medical Center:** attack October 26-27, 2020 (sheet date October 27);
  some servers back by November 6; radiation oncology restored November 9; Epic EHR
  and a fully operational PACS restored November 23; full organizational recovery
  about seven months. Major downtime lasted roughly three weeks as coded.
- **Tallahassee Memorial Healthcare:** IT taken offline February 2, 2023; clinical
  practices resumed seeing patients with limited surgeries on February 6; EMS
  intake increased gradually from February 8; full restoration and return to
  standard operations announced February 15, 2023; total IT downtime 13 days per
  TMH.
- **Manchester Memorial and Rockville General Hospital (ECHN):** emergency
  departments closed and reopened on August 3, 2023; recovery progress on critical
  systems reported August 18; computers back online across the network by
  September 19; operations largely normal for patients by mid-September; billing
  impaired about six weeks.
- **Dickingson County Healthcare System:** attack October 17, 2020; recovery
  reported complete just shy of one month, while a November 19, 2020 update still
  reported about 5% of systems outstanding and full recovery expected by year-end
  (the tension between the two statements is recorded in the sheet).
- **Virginia Mason Franciscan Health:** onset October 3, 2022 (unauthorized access
  September 16 to October 3); some patient records systems back online by October
  17, 2022; patient breach letters sent December 1, 2022.
- **Cheyenne Regional Medical Center (Kronos/UKG):** the vendor outage began
  December 11, 2021; the vendor completed its first restoration phase on January
  22, 2022 and was fully functional in early March 2022; paycheck reconciliation
  began once access returned. The sheet's incident date (March 26, 2022) is the
  newspaper article date and falls after most of this timeline.
- **Colosseum Dental:** practices closed for days from August 7, 2022; most of the
  120 Netherlands practices were reported open again during the week of August 8,
  2022.
- **Immanuel Medical Center (CHI Health):** onset October 3, 2022; CHI Health
  announced on October 18, 2022 that restoration of the systems taken offline was
  in process; no completion date is coded.

## 4. Workarounds

A workaround is reported in **11 of 24** incidents and is `not reported` in **13 of
24**, making it, with recovery_operations, one of the two least-reported fields.
Classifying the 11 reported cells by type (an incident can carry more than one
type; 13 type assignments across 11 incidents):

- **Paper and manual downtime procedures: 6 of 11** (Sky Lakes: paper records,
  runners carrying paper and spreadsheets between departments, copper-line fax
  machines, studies read on modality consoles and burned to CDs; Dickingson County:
  manual procedures and paper copies under established contingency procedures;
  Witting: continuity through offline registers; Virginia Mason Franciscan Health:
  a makeshift paper system of record keeping at St. Anthony Hospital; Tallahassee:
  paper forms, prescription pads and handwritten notes under its downtime
  procedures; Manchester Memorial and Rockville General: paper record-keeping).
- **Transfers, diversion or referral to partner or outside providers: 3 of 11**
  (Brookside: referrals to other providers after the records were destroyed;
  Colosseum Dental: dental emergencies temporarily accommodated by colleagues
  outside the group; Tallahassee: EMS patient flow coordinated with HCA Florida
  Capital Hospital and Leon County EMS, with patients routed to HCA).
- **Manual financial processes: 1 of 11** (Cheyenne Regional: departments manually
  input data and the payroll department manually processed paychecks over five pay
  cycles under a contingency plan).
- **Other: 3 assignments across 3 incidents** (Barlow: a generic statement that the
  hospital operated under its emergency procedures; Immanuel: a parent-level
  CommonSpirit statement that facilities followed existing outage protocols, with
  no Immanuel-specific measure reported; Brookside: the physicians stayed at the
  office for a few weeks seeing patients who showed up, without records).

Two coding notes matter for interpretation. Victory Health Partners is not counted:
paper charts were that clinic's standing practice, not an incident workaround, and
the sheet says so. And where an organization simply closed or turned patients away
with no continuity measure, the guide codes the closure as an operational effect
and the workaround as `not reported`, so the 13 `not reported` cells include cases
(Colosseum's practice closures are coded as effect, with only the emergency
arrangement counted as workaround) where the absence of a workaround is itself part
of the story the sources tell.

## 5. Reporting gaps

Per-field status across the 24 incidents:

| Field | Reported content | Reported absent | n/a | Not reported |
|---|---|---|---|---|
| services_affected | 19 | 1 | 0 | 4 |
| operational_effect | 15 | 6 | 0 | 3 |
| workaround | 11 | 0 | 0 | 13 |
| recovery_technical | 11 | 1 | 0 | 12 |
| recovery_operations | 6 | 1 | 6 | 11 |
| recovery_limitations | 18 | 0 | 0 | 6 |

The structural reasons the evidence notes and the final sheet's notes identify for
these gaps:

1. **Vendor-mediated incidents report data impact without care impact.** In 4 of
   the 6 vendor-mediated rows (Section 6), no disrupted service at the named
   organization is reported at all, because the public record for those rows is
   breach-notification material: affected-individual counts, data types,
   notification dates. The record documents a data event, not an operations event.
2. **Breach-notice language names no systems.** Six rows needed the residual
   `general IT systems (unspecified)` label because the sources say "certain
   systems" were encrypted or disrupted without naming any (Suncoast, Barlow,
   Witting, Victory, Colosseum, Hampton-Newport News CSB). Service-level analysis
   is impossible for those rows from the public record as it stands.
3. **Dataset dates are often not attack dates.** The sheet keeps dataset dates per
   guide §6, but the notes record that the dataset date is an article date
   (Geisinger, August 2, 2022, for an April 2022 vendor encryption; Cheyenne,
   March 26, 2022; Hampton-Newport News CSB, November 25, 2023), a notification or
   investigation-conclusion date (Fallon, December 27, 2023), a leak-site listing
   date (Vilnius, August 19, 2023, for a July 27, 2023 breach; Eye Center of
   Northern Colorado, July 11, 2023, for May-June 2023 access), or a settlement
   article date (Saint Francis, November 4, 2020, for a September 21, 2019
   attack). Brookside's underlying event is a spring 2019 incident entirely
   (adjudicated under rule R3). Any year-based reading of the sample has to carry
   this caveat.
4. **Recovery is reported asymmetrically.** Sources describe technical restoration
   and, even more, what stayed broken (limitations in 18 of 24) far more readily
   than the moment normal operations resumed (6 of 24). Part of the asymmetry is
   also a coding-rule effect that should be disclosed: under rule R9, parent-level
   CommonSpirit recovery statements that did not explicitly cover the division
   were moved out of the recovery fields of the Virginia Mason and Immanuel rows
   into their notes.
5. **Single-source sparsity.** Spine & Disc Medical Center rests on a single source
   (DataBreaches.Net) with no organization statement found; its row codes one
   service (the organization's website) and nothing else. Geisinger's row is
   similarly thin for the named organization: one dataset source, with all detail
   at the vendor level.

## 6. Vendor-mediated pattern

**6 of 24 incidents are vendor-mediated**: the organization attacked was a vendor,
host, or business associate of the named organization, not the named organization
itself. They are Personal Touch Home Aides (cloud host Crossroads Technologies),
MultiCare (IT vendor Netgain Technology, through Woodcreek Provider Services),
Harvard Eye Associates (online data storage vendor), Geisinger (printing and
mailing vendor OneTouchPoint), Cheyenne Regional Medical Center (payroll vendor
Kronos/UKG) and Eye Center of Northern Colorado (management company and business
associate Panorama Eyecare). The remaining 18 rows are direct incidents at the named
organization (including Fallon, whose breached system was its own retained archive,
and the two CommonSpirit division rows, whose attacker hit the parent, not a
vendor).

Field-by-field contrast (reported content, of the group size):

| Field | Vendor-mediated (of 6) | Direct (of 18) |
|---|---|---|
| services_affected | 2 | 17 (plus 1 reported absent: Fallon) |
| operational_effect | 2 | 13 (plus 4 reported absent) |
| workaround | 1 | 10 |
| recovery_technical | 3 | 8 (plus 1 reported absent: Brookside) |
| recovery_operations | 1 | 5 (plus 1 reported absent: Brookside) |
| recovery_limitations | 3 | 15 |

How the reporting differs:

- **Services and effects mostly vanish.** Services are `not reported` in 4 of 6
  vendor rows and in 0 of 18 direct rows. The operational effect is `reported
  absent` in 2 of 6 vendor rows on the strength of explicit no-impact statements
  (MultiCare: the breach was isolated to a vendor archive server and the primary
  EMR database was not affected; Geisinger: OneTouchPoint's filed statement that
  its business customers' systems were not impacted), and `not reported` in the
  other 2 data-only rows (Harvard Eye, Eye Center). The two vendor rows with a
  coded effect are the exceptions that mark the boundary of the pattern: Personal
  Touch, where the ransomed host itself ran the organization's cloud EHR (effect
  detail still rests on a flagged lawsuit allegation), and Cheyenne, where the
  vendor's payroll system was a workflow the hospital used daily, producing the
  sample's only fully documented administrative outage.
- **What recovery exists sits at the vendor.** All 3 vendor rows with technical
  restoration content describe events at the vendor, not at the named
  organization: MultiCare's stolen data was returned after a ransom paid on the
  vendor side (copy received January 18, 2021); Harvard Eye's vendor paid a ransom
  and the hackers returned the data; Cheyenne's timeline is Kronos's restoration
  phases. No vendor row reports a technical restoration at the named organization,
  because none was reported to have lost one.
- **Limitations reduce to the data tail.** The 3 vendor rows with limitations
  (MultiCare, Cheyenne, Eye Center) report notification preparation, overpayment
  recovery, and a year-long notification delay respectively; none reports a
  continuing clinical limitation.
- **Workarounds are almost absent from vendor reporting** (1 of 6, Cheyenne's
  manual payroll), against 10 of 18 direct rows. Where the vendor's system was not
  part of daily care or operations at the named organization, there was no
  workaround to report; where it was (payroll), the workaround looks exactly like
  a direct incident's.

In short: for vendor-mediated incidents the public record is a breach record
(what data, how many people, when they were told, what the vendor did), while for
direct incidents it is, at least in the better-reported rows, an operations record
(what stopped, how care continued, what came back, what stayed broken). Any
comparison of disruption or recovery across the full 24 that ignores this split
would mistake a difference in reporting for a difference in impact.

## 7. Traceability note

Every count above was recomputed from `coding_sheet_final.csv` for this memo and
is reproduced in `analysis_counts.csv`. Free-text summaries name the incidents they
summarize, and each summarized cell can be checked against the final sheet and,
behind it, against the claim rows in `claims_coderA.csv` and `claims_coderB.csv`.
Two derived items are labeled as derived rather than coded: the field-completeness
distribution in Section 1 and the workaround-type and limitation-group
classifications in Sections 3 and 4, which classify the final sheet's coded text
and name every incident assigned to each class.
