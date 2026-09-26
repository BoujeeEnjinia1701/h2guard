---
doc_id: HGD-DDR-002
title: H2Guard recommendations accepted
project: H2Guard
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the review recommendations accepted by Amish on 2026-09-25 and what changed in the repo
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below with a recommendation is decided by Amish, 2026-09-25: go with recommendation. Items without a recommendation remain proposed, awaiting Amish.

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." The items concerned are those in `docs/REVIEW.md` (TRL 2 and TRL 3 sessions) and in HGD-DDR-001 that were marked "Proposed, awaiting Amish" or "Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review" and that carried a recommendation. Where a recommendation offered several options, the recommended option is the decision. Work stays at TRL 3; TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` and HGD-DDR-001.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 1 | D1 to D9 of HGD-DDR-001 (sensor pair, set points, normally closed valve, continuous ventilation with boost, inventory rule, key reset and one head per room, university teaching lab as first users, independent hardware trip, 24 V DC) | As recommended | Status wording in HGD-DDR-001, HGD-PRB-001, HGD-PRC-001 and HGD-REQ-001; no design change |
| 2 | Budget (TRL 2 item 1 and HGD-DDR-001 O1) | Option (a) of the TRL 3 review: $265, covering the TRL 3 kit including the fan and make-up grille. The TRL 2 figure of $250 was superseded by this later recommendation | `budget_usd` 180 to 265; R14 target $265; R14 from not met ($264 against $180, +47 %) to met on paper ($1 margin) |
| 3 | Timed escalation from warning to trip | Option (a): close the valve when a warning is held for 5 min, latched as a trip | R3 restated; firmware rule added to HGD-PRC-001; HGD-CAL-001 v0.2 F7 and F8: off-axis design leak closed at 5.6 min, 28 L released, room about 1.9 % LFL; GA note on HGD-DWG-001 Rev P2 |
| 4 | Head placement rule | Adopt: head directly above each likely leak point, second head where leak points are far apart; the horizontal offset limit is set at TRL 4 | R1 restated; HGD-CAL-001 E7 gives the plume radius at the ports (141 mm) as the paper basis; GA note on HGD-DWG-001 Rev P2. Setting the offset limit by test is TRL 4 work, decided but on hold |
| 5 | R13 scope | Option (b): the fan and grille wall openings are builder's work outside the 4 h target | R13 restated; status from not met (6.0 h) to at risk (4.1 h, 5 min over) |
| 6 | H2Bench to reflect the inventory rule (D5) | Adopt | Cross-repo action listed in `docs/REVIEW.md`; H2Bench not edited |

No pitch or problem rewording was recommended, so `project.yaml` and the README keep their pitch and problem text. No part was added or resized, so the model geometry, STEP and STL files and the BOM lines are unchanged; the drawing changes only in its notes.

*Table 2. Items still open, proposed, awaiting Amish (no recommendation was made).*

| # | Item |
| --- | --- |
| O2 | Oxygen depletion monitoring when inert gas cylinders share the room |
| O3 | Where the set points and the inventory rule come from in each country the first users are in |
| O4 | How airflow is proven: tachometer only, or a differential pressure switch |
| O5 | Low-cost solenoid valve or a certified gas valve |
| O6 | Whether a full-span bump test trips the system (proof test with a key reset) or a lower span gas is used; no recommendation until the cup delivery factor is known |
| O7 | A second interlock output (dry contact) for H2Bench's bench supply; raised as an interface point, with no recommendation |

## Consequences

- Requirement status (HGD-CAL-001 v0.2): 0 not met, 3 at risk (R4, R7, R13), 1 not verifiable at TRL 3 (R1), 7 met on paper, 4 met by design. Before: 2 not met, 2 at risk, 1 not verifiable, 6 met on paper, 4 met by design.
- Documents revised: HGD-PRB-001 v0.4, HGD-PRC-001 v0.4, HGD-REQ-001 v0.4, HGD-CAL-001 v0.2, HGD-DDR-001 v0.2, HGD-DWG-001 Rev P2.
- The timed escalation is a firmware rule and does not share the independence of the comparator trip (R6). Writing that firmware beyond a labeled sketch is TRL 4 work and is on hold.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building, testing, purchasing or firmware work.
