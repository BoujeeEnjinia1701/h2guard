---
doc_id: HGD-DEC-001
title: H2Guard design decisions register
project: H2Guard
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the build plan; open decisions gathered from the review note and the decision records; budget treated as a value-engineering target
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Amish approved the recommendations for open decisions 1 to 12 (HGD-DDR-003 accepted; head on a ceiling drop rod); moved to decisions made
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Decisions carried into the model, BOM and calculations; value engineering re-priced (USD 411); items to confirm for the drop rod, pressure switch and dry-contact relay
---

# H2Guard design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The catalytic sensor's response time (t90), power and hydrogen output, from its datasheet | R4 assumes a t90 of 30 s; R1's 1 % LFL resolution needs the output | HGD-CAL-001, F3 |
| 2 | The sensor can is about 20 mm across and 17 mm tall | The standoff length sets its 2.2 mm gap above the disc | HGD-DDR-003, P4 |
| 3 | The head box has its lid on a 110 x 90 face | The ports, gland and drop rod hole assume it | HGD-DDR-003, P3 |
| 4 | The controller box's boss spacing and corner fixing holes | They set the mounting plate holes and the wall screws | HGD-DDR-003, P6, P8 |
| 5 | The fan's body fits a 200 mm sleeve (about 180 mm across or less) and has fixing holes in its inlet face | The fan plate holds it by those holes | HGD-DDR-003, P10 |
| 6 | The fan's curve gives at least 300 m³/h against about 60 Pa | R7 rests on an assumed curve | HGD-CAL-001, G3 |
| 7 | The valve has two tapped holes underneath, 36 mm apart, and is rated for hydrogen with a stated seat leak rate | The bracket holes; the leaking-seat fault in Table 4 of HGD-CAL-001 | HGD-DDR-003, P11; HGD-DDR-001, O5 |
| 8 | The pressure switch can be set to about 3 Pa (a low-range air switch) | The fan inlet tap gives only 5.7 Pa at the continuous flow; a common 20 Pa minimum switch would prove flow only on boost | HGD-CAL-001, G6; decision 6 |
| 9 | The floor flange, pipe nipple and conduit locknuts share one 1/2 in thread, and the ceiling takes the flange screws | The drop rod holds the head over the apparatus | HGD-CAL-001, E7; decision 2 |
| 10 | The dry-contact relay's contact rating suits H2Bench's supply cut-off circuit | H2Bench switches its own supply through it | Decision 9 |

## Value engineering

Value-engineering target: USD 265. Estimated cost of the constructable design: USD 411 (USD 146 over the target). The estimate comes from the 21-line bill of materials at indicative prices; the target is `budget_usd`, a hypothetical control target, not a limit. Two options are priced with quantity 0 and are not in the total: the oxygen sensor (USD 110) and the fan with its motor outside the air stream (USD 450, in place of the USD 55 fan). Main cost drivers and savings worth trying:

- The largest lines are the hydrogen-rated valve (USD 95), the exhaust fan with its grille, sleeve, shutter and hood (USD 55), the catalytic sensor (USD 35), the pressure switch and tubing (USD 30) and the controller modules (USD 25). Together they are about 60 % of the cost.
- Making the design constructable added USD 25: the made brackets and plates (USD 14), the 200 mm wall sleeve (USD 5), standoffs, screws and epoxy (USD 4) and the cup's push-in fitting and tube clips (USD 2).
- The decisions of 2026-10-02 added USD 122: the hydrogen-rated valve (USD 65 more than the brass valve), the pressure switch and tubing (USD 30), the ceiling drop rod (USD 11), the dry-contact relay and terminal (USD 6), the clear-lid controller box (USD 5) and more cable (USD 5).
- Savings worth trying: a printed controller mounting plate in place of aluminium sheet (about USD 3); buying the fan as a kit with its own shutter and hood; one combined controller board at TRL 4 in place of separate bought modules; and, where the room already has mechanical extract at high level, using it in place of the kit fan and grille (USD 63), which would bring the kit to about USD 348; and the brass valve at USD 30, if its maker states hydrogen compatibility and a seat leak rating and it passes the seat leak proof test (USD 65 less).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 to D9: catalytic plus metal oxide sensors (certified sensor as the upgrade); set points 10 % and 25 % LFL; normally closed valve; continuous ventilation with boost; inventory rule (R9); key-switch reset and one head per room; a university teaching lab first; independent hardware trip; 24 V DC with a certified supply | Amish: "i accept all your recommendations, go with them across all repos." | HGD-DDR-001, HGD-DDR-002 |
| 2026-09-25 | Budget figure USD 265, now treated as the value-engineering target | Amish, same instruction; on 2026-10-01: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | HGD-DDR-002 |
| 2026-09-25 | Timed escalation: a warning held 5 min closes the valve and latches | Amish, same instruction | HGD-DDR-002 |
| 2026-09-25 | Head placement rule: a head directly above each likely leak point; offset limit set by test at TRL 4 | Amish, same instruction | HGD-DDR-002 |
| 2026-09-25 | R13 scope: the fan and grille wall openings are builder's work | Amish, same instruction | HGD-DDR-002 |
| 2026-09-25 | H2Bench to reflect the inventory rule | Amish, same instruction | HGD-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; keep open decisions out of the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | HGD-DDR-003 (changes accepted on 2026-10-02, below) |
| 2026-10-02 | Design for construction accepted: the changes P1 to P11, as made; the head position is settled separately (decision 2) | Amish: "i approve your recommendations for all 555 open decisions." | HGD-DDR-003, Table 1 |
| 2026-10-02 | The head hangs from the ceiling on a drop rod directly over the apparatus; wall mounting is allowed only if the TRL 4 plume test shows a trip at the wall position (the wall position puts the ports 260 mm from the apparatus centre against a plume radius of about 141 mm) | Amish: "i approve your recommendations for all 555 open decisions." | HGD-DDR-003, A1 |
| 2026-10-02 | Fan motor in the sleeve accepted for the supervised teaching prototype; any room used without close supervision gets a fan with its motor outside the air stream | Amish: "i approve your recommendations for all 555 open decisions." | HGD-DDR-003, A2 |
| 2026-10-02 | An oxygen sensor is added, as a standard kit option, whenever inert gas cylinders share the room | Amish: "i approve your recommendations for all 555 open decisions." | HGD-DDR-001, O2 |
| 2026-10-02 | Set points and the inventory rule come from the stricter of the national code and ISO 26142, and from the host institution's safety office where its rules are stricter; 10 % and 25 % LFL stay the defaults | Amish: "i approve your recommendations for all 555 open decisions." | HGD-DDR-001, O3 |
| 2026-10-02 | A differential pressure switch at the fan proves airflow | Amish: "i approve your recommendations for all 555 open decisions." | HGD-DDR-001, O4 |
| 2026-10-02 | The valve is rated for hydrogen with a stated seat leak rate; the low-cost brass valve is accepted only if its maker states hydrogen compatibility and a seat leak rating and it passes a seat leak proof test at TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | HGD-DDR-001, O5 |
| 2026-10-02 | The 1 % full-span bump test trips the system, as planned; the pass level is set once the cup delivery factor is measured | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-25 |
| 2026-10-02 | A dry-contact relay output that opens on a trip or loss of power is added, for H2Bench to cut its own supply | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-25 |
| 2026-10-02 | The render layout is kept, with a caption saying the head and valve are drawn beside the controller | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, item 1 |
| 2026-10-02 | A clear-lid IP65 controller box, added to the BOM at its next revision | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, item 2 |
| 2026-10-02 | Leaving the fan, grille, sounder, beacon and supply out of the product renders accepted | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, item 3 |
