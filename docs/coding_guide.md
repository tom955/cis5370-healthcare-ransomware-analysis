# Coding Guide v2 — Healthcare Ransomware Disruption and Recovery (Stage 2/3)

Version 1, written 2026-11-16, before coding began. Version 2, revised 2026-11-16 after the
independent double-coding comparison (assignment stage 3): adjudication rules R1–R12 were
added to the relevant sections, and the changes are listed in the v2 changelog at the bottom
of this file, never as silent edits.

## 1. Purpose and unit of analysis

The unit of analysis is **one incident**: one row of the selected 24 (one uuid in
`selected_24.csv`). For each incident we code what public reporting says about how the
ransomware event disrupted healthcare services, how the organization kept care going, and
how it recovered. We code **reported** facts only. The study question is what public
reports show, so the reporting itself — including its gaps — is the data.

## 2. Sources

For each incident, coders use, in this order:

1. **The dataset's detailed record** for the incident (inside `incidents.zip`): the source
   article texts and source list the dataset itself collected. These are usually the
   earliest reports and often the only ones for small organizations.
2. **Public sources found by the coder**: the affected organization's own statements,
   press releases, or patient notices; reputable news coverage (local news is often the
   most detailed for small hospitals); HHS OCR breach portal records and state
   attorney-general breach notices when relevant (these confirm dates and record counts
   but rarely describe disruption).

Public records only. No hospital systems, no patient records, no malware samples are
accessed (per the assignment's threat model). If a source is behind a hard paywall and
cannot be read, note it in the evidence notes and do not code from its headline alone
unless the visible text supports the specific claim.

**Retrospectives vs. contemporaneous sources (R11).** Later retrospective accounts (for
example, a hospital IT director's interview or conference talk a year or more after the
incident) may supply mechanism and workaround detail that contemporaneous reporting lacks,
and may be coded for that detail. When a retrospective conflicts with contemporaneous
sources on dates or counts, the contemporaneous sources govern, and the conflict is logged
in notes with both figures stated. (Origin: the Sky Lakes PC and server counts, where the
IS director's retrospective figures of more than 2,500 PCs and 600 servers taken down
differ from contemporaneous November 2020 reporting of about 2,000 computers replaced and
568 servers.)

## 3. Fields coded for each incident

### 3.1 ransomware_confirmed — `yes` / `no` / `unclear`

- `yes`: at least one source states the incident was ransomware (the word "ransomware",
  a named ransomware group, ransom demand, or encrypted systems described as ransomware
  by the organization, law enforcement, or a reputable outlet).
- `no`: sources describe a different kind of incident (e.g., pure data theft with no
  encryption, or an explicitly non-ransomware outage).
- `unclear`: sources say only "cyberattack", "security incident", "network outage", or
  similar, and nothing found confirms ransomware specifically.

A breach notice that lists "unauthorized access" without more does **not** by itself make
this `yes`. Verifying ransomware vs. an unspecified cyberattack is one of the assignment's
named technical challenges, so this field is coded conservatively.

**Vendor incidents (R1).** `ransomware_confirmed` describes the attack event behind the
dataset record, not only the named organization's own experience. When the attacked system
belonged to the organization's vendor, code `yes` if the vendor attack is confirmed as
ransomware, and state in notes that confirmation is at the vendor level (e.g., Geisinger:
ransomware confirmed at its printing/mailing vendor OneTouchPoint). Victim-level impact is
coded in the other fields, never in this one: a customer whose own systems were not
impacted is not coded `unclear` merely because the encryption happened at its vendor.

**Hedged confirmation (R2).** Code `yes` when at least one credible source with direct
knowledge describes the incident as ransomware and no source contradicts it, even if the
reporting hedges ("suspected", "apparent", "hallmarks") and even if the victim
organization itself never used the word. In that case add a confirmation note in notes
stating that the victim never confirmed ransomware itself (e.g., Tallahassee Memorial,
which said only "IT security issue" / "cyberattack"). If sources conflict on whether
ransomware was used, or the only descriptions are unattributed speculation, code `unclear`.

### 3.2 services_affected — fixed taxonomy, multiple values allowed

Code every service the reporting says was disrupted, degraded, or taken offline. Use
exactly these labels, separated by `; `:

| Label | Means |
|---|---|
| EHR/clinical records | Electronic health/medical record system, patient chart access, clinical documentation |
| imaging/radiology | PACS, X-ray/CT/MRI scheduling or viewing, radiology reading |
| laboratory | Lab ordering or results (in-house or reference lab workflows) |
| pharmacy | Medication dispensing, pharmacy systems, e-prescribing |
| scheduling/appointments | Appointment booking, registration, admissions scheduling |
| emergency care/patient diversion | Emergency department closure, ambulance diversion, patients sent elsewhere for urgent care |
| surgery/procedures | Cancelled or postponed operations or procedures, cath lab, endoscopy, etc. |
| communications | Phone systems, email, internal messaging, patient portals used for communication |
| billing/administrative | Billing, coding, insurance verification, payroll, general IT/office systems |
| general IT systems (unspecified) | Reporting says systems were encrypted, disrupted or taken offline but names no specific system (added in v2, rule R6) |
| other (specify) | Anything else, with a short specification in parentheses, e.g. `other (radiation oncology planning)` |

Only code a service when a source ties it to this incident. Do not code a service just
because the organization has one (every hospital has a lab; the question is whether the
reporting says the lab was affected).

**Access is not disruption (R4).** Code a service only when reporting says it was
disrupted, unavailable, encrypted or taken offline. Unauthorized access to, or
exfiltration from, a system does **not** by itself code that service; the data impact is
recorded in notes and in the claims sheet instead. (Origin: Barlow Respiratory Hospital,
where the EHR was reported accessed/breached and data exfiltrated, but no source reported
clinicians losing EHR access, while the hospital stated care was never interrupted; the
EHR label was removed and the generic IT disruption in the hospital's own letter was coded
under the R6 label.) One refinement for vendor-hosted systems: when the ransomed system is
the vendor host that itself runs the victim's service (for example, a cloud-hosted EHR),
the service may be coded because the hosted service itself was the encrypted system; note
that the coding is vendor-mediated.

**Pharmacy downtime procedures (R5).** Code `pharmacy` when the normal pharmacy workflow
is reported down or replaced by downtime procedures (paper prescription pads in place of
an electronic process, barcode scanning out), even when medication delivery continued by
workaround. A statement that already-filled prescriptions remained available is a
continuity fact, not evidence that pharmacy was unaffected. (Origin: Sky Lakes and
Tallahassee Memorial.)

**Generic systems and closures (R6).** Use `general IT systems (unspecified)` for
"some systems encrypted / disrupted, none named" reporting, instead of forcing such cases
into `other (specify)` or into `billing/administrative`. An organization or practice
closing is an operational-effect outcome, coded in `operational_effect`; it is never a
service label.

### 3.3 operational_effect — free text, source-backed

What happened to care delivery as a result: appointment or procedure cancellations,
patient diversion, delays, services reduced or closed, downtime duration when reported.
Write a short factual summary built only from sourced claims. Duration is coded when a
source states it ("systems were down for three days"); do not estimate durations from
article publication dates.

### 3.4 workaround — free text, source-backed

What the organization used to keep care going: downtime procedures, paper charting and
paper orders, manual registration, transferring patients, sending work to partner or
sister facilities, bringing in outside IT/forensics help **for care continuity** (pure
investigation steps are not workarounds unless they restored service). If reporting
describes the organization simply closing or turning patients away with no continuity
measure, code the closure under operational_effect and code workaround as `not reported`
unless a source explicitly says no workaround was used.

### 3.5 recovery_milestones — three separate sub-fields

Reports use "systems restored" and "operations resumed" loosely, so the three are coded
separately, each with dates when reported:

- **recovery_technical**: technical restoration — systems rebuilt, network back online,
  EHR accessible again, vendor declaring containment/restoration of IT.
- **recovery_operations**: operations resumed — appointments, surgeries, admissions, or
  the ED back to normal or near-normal operation.
- **recovery_limitations**: continuing limitations after resumption — backlogs being
  cleared, some systems still down, delayed billing, breach notification still pending,
  services restored in phases.

A single source sentence can feed more than one sub-field ("the EHR came back Tuesday
and clinics reopened Wednesday, though billing is still manual"). Code each part where it
belongs. If a source says only "operations have returned to normal" with no technical
detail, that is recovery_operations, and recovery_technical is `not reported` unless
another source covers it.

**Response language is not restoration (R7).** Generic response boilerplate — "we promptly
took steps to secure our systems", "we engaged outside cybersecurity experts", "our
systems are now secure" — is containment/response, not a technical-restoration milestone.
`recovery_technical` requires a statement that systems were restored, rebuilt or brought
back online (a ransom-paid return of stolen data, or a vendor's dated restoration of the
affected system, is a concrete recovery event and may be coded, framed at the level where
it happened). If only boilerplate exists, code `recovery_technical` as `not reported` and
note the response statement in notes. (Origin: the Hampton-Newport News CSB, Fallon and
Panorama Eyecare/Eye Center of Northern Colorado rows, where Coder A had coded boilerplate
as recovery_technical.)

**Operations that never stopped (R8).** When `operational_effect` is `reported absent`
because care was never interrupted, code `recovery_operations` as
`n/a - operations not interrupted` instead of `not reported`: there was nothing to resume,
and the sheet should say so rather than imply the resumption is merely unreported. For an
organization that had ceased operating before the incident, code
`n/a - no active operations` (Fallon).

**Parent-company statements (R9).** When the coded organization is a division or facility
of a parent that suffered the incident, a parent company's statement may fill the
division's recovery fields only when it explicitly covers the affected division or
facility (for example, a division-level announcement, or a breach notice addressed to that
division's patients). A system-wide parent statement that does not name or clearly cover
the division is recorded in notes, flagged as parent-level, and is not coded in the
division's recovery fields. (Origin: the CommonSpirit rows — Virginia Mason Franciscan
Health and Immanuel Medical Center.)

**Scope of recovery_limitations (clarified in adjudication).** The breach-notification
process is coded in `recovery_limitations` when the coded organization (or its parent,
acting for it) ran that process for this incident — including for rows where the
organization itself had no service disruption but did have a documented notification arc
(e.g., Fallon). A vendor's notification process covering many unrelated customers is not
coded in a customer row's limitations (e.g., Geisinger); record it in notes instead.

### 3.6 notes — conflicts, traps, coder remarks

Record here: conflicting accounts or dates across sources (state both, do not silently
pick one); ambiguity in the reporting; identity traps (similar organization names,
vendor-vs-victim confusion, a breach notice for a different incident at the same
organization); and anything a second coder should double-check.

**Identity conflicts between the dataset record and wider coverage (R3).** When the
dataset's source and other coverage appear to describe the same event under a different
organization name or date, adjudicate identity on the distinctive facts: if the unique
details match (ransom amount, what was deleted or encrypted, investigative involvement,
city) and no separate second incident can be found, treat them as the same incident. Keep
the dataset date and organization name in the sheet (per §6), record both dates and the
name difference in notes, and keep the claims sourced to the wider coverage. (Origin:
Brookside — the dataset's January 2020 "Brookside Surgery Center" item and the spring 2019
"Brookside ENT and Hearing Center" coverage share the $6,500 demand, the deletion of all
records after refusal, and the FBI investigation, and were adjudicated the same incident.)

## 4. The key rule: reported / not reported / reported absent

Every coded value is exactly one of three kinds:

1. **Reported**: a source states it. The claim goes in `claims_coderA.csv` with its URL
   and supporting text.
2. **not reported**: the sources found are silent on the field. Code the field value as
   `not reported`. Silence is a finding about reporting, not about the incident.
3. **reported absent**: a source explicitly says the thing did **not** happen or there
   was no impact (e.g., "no patient care was affected", "the emergency department
   remained open"). Code it as `reported absent` and add the claim with its source.

Never infer absence from silence. Never upgrade "not reported" because an effect "must
have" happened. Never exclude, merge, or thin out an incident because its reporting is
sparse — sparse rows are part of the results (the assignment requires reporting missing
information alongside observed patterns).

**Structural absence (R10).** `reported absent` normally requires an explicit statement
that the thing did not happen. There is one structural exception: when sourced facts
establish that there was nothing for the effect to act on — the organization had ceased
operations before the incident and the compromised system was a retained archive — code
`reported absent` on that structural basis, and state the basis and the sourcing facts in
notes. (Origin: Fallon Ambulance Services, which closed in December 2022, months before
the February–April 2023 intrusion into its retained data archive.)

In the coding sheet, a field with a mix (some services reported affected, others never
mentioned) is coded with the reported values; the unmentioned ones are simply absent
from the list, and the evidence notes record that they were not reported. The
`reported absent` wording is used in a field when the explicit-denial is the coded value
for that field (most often operational_effect, recovery fields, or workaround).

## 5. Claims discipline

Every individual claim in the coding sheet must be traceable to one row of the claims
sheet: incident uuid, field, value, source URL, a short supporting quote or close
paraphrase, and source type (`organization statement`, `news`, `dataset article`,
`official record`). A coding-sheet cell may summarize several claims. If a cell's content
cannot be pointed to claims rows, it does not belong in the sheet.

Quotes must be real: copied or closely paraphrased from the source at that URL. Do not
write a supporting text that is stronger than the source (e.g., source says "some
appointments were rescheduled" — do not paraphrase as "appointments were cancelled").

**Lawsuit allegations (R12).** Class-action complaints and reporting that relays their
allegations are usable only flagged as allegations. An allegation is never the sole basis
for a `services_affected` or `operational_effect` value: if the only source for a
disruption claim is a lawsuit, the cell states the sourced facts and presents the
disruption claim explicitly as an allegation. (Origin: Personal Touch Home Aides, where
the only source for records being inaccessible and care being disrupted was the Booker v.
Personal Touch class action.)

## 6. Dates

Use the date the source gives for the event it describes (discovery date, downtime start,
restoration date). The dataset's `incident-date` is the coding sheet's incident date.
Where sources disagree on a date, record both in notes with their sources; the sheet
keeps the dataset date.

## 7. Workflow per incident

1. Open the dataset record; read every article text and list every source URL.
2. Search for the organization's own statement and at least one independent news source;
   check HHS OCR / state AG records when the incident involves a US provider and a data
   breach is reported.
3. Draft claims rows first, then fill the coding sheet from the claims (not the other
   way around).
4. Write the evidence-notes entry: sources found and used, what is missing, conflicts
   and traps.
5. Mark any field you are unsure about in notes for the second coder, rather than
   forcing a call.

## 8. Changelog

- v1 (2026-11-16): initial guide, written before Coder A coding.
- v2 (2026-11-16): revised after the independent double-coding comparison (assignment
  stage 3). Coder B independently coded 6 of the 24 incidents (Brookside, Sky Lakes,
  Barlow, Geisinger, Tallahassee, Fallon); the cell-by-cell comparison produced 34
  differing cells plus 1 rationale disagreement (see `disagreement_log.csv` and
  `ADJUDICATION.md`). The comparison changed the guide as follows:
  - **R1 (§3.1)** — vendor incidents: `ransomware_confirmed` describes the attack event
    behind the record. The two coders split on Geisinger (unclear vs. yes) because v1 did
    not say whether confirmation attaches to the vendor attack or the customer's own
    systems; v2 attaches it to the event, with the vendor level noted.
  - **R2 (§3.1)** — hedged confirmation: the coders split on Tallahassee (unclear vs. yes)
    because v1's "code conservatively" instruction collided with its reputable-outlet
    test when every outlet hedged and the victim never confirmed. v2 sets the threshold
    (one credible source with direct knowledge, no contradiction) and requires a caveat
    note when the victim never used the word.
  - **R3 (§3.6)** — identity adjudication: both coders independently concluded the
    dataset's 2020 "Brookside Surgery Center" item and the 2019 "Brookside ENT and Hearing
    Center" coverage were the same incident, but v1 gave no test for merging conflicting
    identity/date records; v2 adds the distinctive-facts test.
  - **R4 (§3.2)** — access vs. disruption: both coders coded Barlow's EHR, on different
    stated bases, from reporting that described access and breach but no downtime. v2
    states that access/exfiltration alone never codes a service, with a vendor-hosted
    refinement (Personal Touch).
  - **R5 (§3.2)** — pharmacy: Coder B coded pharmacy at Sky Lakes and Tallahassee from
    downtime artifacts (barcode scanning out, paper prescription pads) that Coder A had
    treated as continuity evidence. v2 codes pharmacy when the workflow is down or on
    downtime procedures, even if delivery continued by workaround.
  - **R6 (§3.2)** — new taxonomy label `general IT systems (unspecified)` for
    "some systems encrypted, none named" reporting (both coders had flagged the missing
    generic label; Coder A had used three different forced `other (...)` formulations),
    and a statement that an organization closing is an operational effect, not a service.
  - **R7 (§3.5)** — recovery boilerplate: Coder A had coded "we secured our systems and
    engaged experts" statements as `recovery_technical` (Hampton, Fallon,
    Panorama/Eye Center); Coder B coded the same pattern as containment and left the
    field not reported. v2 requires a restoration statement for `recovery_technical`.
  - **R8 (§3.5)** — operations never interrupted: v1 had no value for "nothing to resume"
    (both coders left `recovery_operations` as `not reported` for never-interrupted rows,
    which reads as missing data). v2 adds `n/a - operations not interrupted` and
    `n/a - no active operations`.
  - **R9 (§3.5)** — parent statements: Coder A used CommonSpirit parent-level recovery
    statements in the Virginia Mason and Immanuel rows with in-cell flags, but v1 did not
    say when a parent statement may stand in for a division. v2 allows it only when the
    statement explicitly covers the division/facility; otherwise it is notes-only.
  - **R10 (§4)** — structural reported absence: Coder B coded Fallon's
    `operational_effect` as reported absent on structural grounds and flagged that it
    stretched v1's explicit-denial definition; Coder A did the same for services. v2
    admits the structural basis when the facts are sourced and stated in notes.
  - **R11 (§2)** — retrospectives: the richest Sky Lakes detail came from the IS
    director's retrospective accounts, whose PC/server counts conflict with
    contemporaneous reporting; v1 gave no weighting rule. v2 lets retrospectives supply
    mechanism/workaround detail but gives contemporaneous sources the dates and counts.
  - **R12 (§5)** — lawsuit allegations: Coder A's Personal Touch disruption coding rested
    on a class-action allegation, which v1's source list neither admitted nor excluded.
    v2 admits allegations only flagged as such, never as the sole basis for a services or
    effect value.
  - **Clarification (§3.5)** — scope of `recovery_limitations`: the coders split on
    Fallon (notification timeline coded vs. notes-only) because v1 did not say whether
    recovery fields presuppose a disruption at the coded organization. v2 codes the
    notification process as a limitation when the coded organization (or its parent for
    it) ran it, and keeps a multi-customer vendor's process in notes.
  - No v1 rule was deleted; v2 adds rules and one taxonomy label. The final coding sheet
    (`coding_sheet_final.csv`) applies R1–R12 to the six double-coded rows and sweeps
    R4–R9 and R12 across the remaining 18 rows wherever the same patterns occur.
