---
doc_id: HGD-DDR-001
title: H2Guard TRL 2 review decisions
project: H2Guard
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted for TRL 3 work under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); D1 to D9 and O1 decided, O2 to O5 still open
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: O2 to O5 decided by Amish on 2026-10-02 (recommendations approved, HGD-DEC-001)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** items D1 to D9 and O1 decided by Amish, 2026-09-25: go with recommendation (see HGD-DDR-002); items O2 to O5 were decided by Amish on 2026-10-02 (recommendations approved, HGD-DEC-001).

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish", and the design precis HGD-PRC-001 v0.2 listed eight key design choices, each with options and a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this batch item by item. Every item that carries a recommendation is therefore adopted as recommended for TRL 3 work, open for his review; items without a recommendation, and the budget figure, stay open.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in HGD-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted for TRL 3 work, decided by Amish on 2026-09-25.*

| # | Item | Adopted choice | Status |
| --- | --- | --- | --- |
| D1 | Sensor baseline | Option (a): catalytic sensor for the trip plus a metal oxide sensor for early warning (about $50 of sensors), with a certified molecular property spectrometer sensor documented as the upgrade for any room used without close supervision | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Set points | Warning at 10 % LFL (0.4 % vol), trip at 25 % LFL (1.0 % vol) | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Supply valve | Normally closed, energize to open, rather than a latching or motorized valve | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Ventilation | Continuous exhaust with a boost, rather than a fan that starts on alarm | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Inventory rule (R9) | Hydrogen that could be released into the room is 1 % of room volume or less at atmospheric pressure, or a flow restrictor limits release to the design leak; a condition for H2Bench and any other lab project using H2Guard. H2Bench is asked, through the review note, to reflect it | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Reset and coverage | Key-switch reset; one detector head per room as the base kit, with a second head as an option for beamed or pocketed ceilings | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | First users | A university teaching lab first, because supervision and a technician are in place | Decided by Amish, 2026-09-25: go with recommendation |
| D8 | Independent hardware trip | A comparator trip beside the microcontroller; kept as the core of the design | Decided by Amish, 2026-09-25: go with recommendation |
| D9 | Supply voltage | 24 V DC throughout, from a certified plug-in supply | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items left open at v0.1. O1 was decided on 2026-09-25 and O2 to O5 on 2026-10-02.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Budget. The TRL 2 review recommended raising `budget_usd` from $180 to $250. `budget_usd` is not changed. HGD-CAL-001 puts the parts at $264, over both figures, so the review note asks Amish to choose again. Recommendation: $265, covering the TRL 3 kit including the fan. | Decided by Amish, 2026-09-25: go with recommendation ($265; see HGD-DDR-002) |
| O2 | Oxygen depletion monitoring when inert gas cylinders share the room. No recommendation was made. | Decided by Amish, 2026-10-02 (recommendation approved, HGD-DEC-001): an oxygen sensor is added, as a standard kit option, whenever inert gas cylinders share the room |
| O3 | Where the set points and the inventory rule come from in each country the first users are in. No recommendation was made. | Decided by Amish, 2026-10-02 (recommendation approved, HGD-DEC-001): set points and the inventory rule come from the stricter of the national code and ISO 26142, and from the host institution's safety office where stricter; 10 % and 25 % LFL stay the defaults |
| O4 | How airflow is proven: tachometer only, or a differential pressure switch. No recommendation was made; HGD-CAL-001 Table 4 shows a blocked duct is not detected with the tachometer alone. | Decided by Amish, 2026-10-02 (recommendation approved, HGD-DEC-001): a differential pressure switch at the fan proves airflow |
| O5 | Low-cost solenoid valve or a certified gas valve, pending the hydrogen compatibility and seat leak rating. No recommendation was made. | Decided by Amish, 2026-10-02 (recommendation approved, HGD-DEC-001): a valve rated for hydrogen with a stated seat leak rate; the low-cost brass valve only if its maker states hydrogen compatibility and a seat leak rating and it passes a seat leak proof test at TRL 4 |

## Consequences

- `project.yaml`: only the TRL fields change. `budget_usd` stays at $180 (O1). No pitch or problem rewording was recommended, so none was applied.
- HGD-PRB-001, HGD-PRC-001 and HGD-REQ-001 are revised to v0.3. The key design choices in the precis are no longer "proposed"; they are adopted for TRL 3 work pending Amish's review. R9 becomes an adopted installation rule. No requirement target is relaxed or redefined by these items.
- The TRL 3 calculations (HGD-CAL-001) led to three changes within the adopted choices: a larger mixed-flow fan so the boost is reached against the duct losses (D4), thinner flame arrestor discs with the sensors close behind them, and a bump test cup, tube and port for R12. They raise the parts cost from $239 to $264.
- New proposals from HGD-CAL-001 (a timed escalation from warning to trip, a head placement rule, a redefinition of R13, a revised budget figure) are listed in `docs/REVIEW.md` and await Amish; this record does not adopt them.
- On 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos." HGD-DDR-002 records the result: D1 to D9 and O1 are decided, and the new proposals are decided where they carried a recommendation.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
