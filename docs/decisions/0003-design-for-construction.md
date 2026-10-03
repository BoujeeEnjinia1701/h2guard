---
doc_id: HGD-DDR-003
title: H2Guard design for construction
project: H2Guard
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish; A1 decided as a ceiling drop rod (changed recommendation) and A2 accepted for the supervised prototype only
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Consequences updated after the approved follow-ups were carried into the model, drawings, build plan, calculations and appearance model
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Table 1 and the recommendations for A1 and A2 in Table 3 as written for the register on 2026-10-01 (HGD-DEC-001): A1 was changed from the wall mounting proposed here to a ceiling drop rod, and A2 was sharpened. Every change in Table 1 was made under Amish's 2026-09-30 instruction to make the design physically buildable. Nothing in Table 1 changes what H2Guard does, its pitch or its safety case. The cost is reported against the value-engineering target (Table 2) and needs no decision.

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model (`cad/src/model.py`) showed what H2Guard does and where each part goes in the room, but several parts were shapes that could not be made, fitted or held as drawn. Checking the model with build123d (intersections, distances and clearances between parts) found the problems P1 to P11 below.

The changes keep what the system does: the same room, the same detector head size and mounting height with the ports 175 mm below the ceiling, the same sensors, arrestor discs, sensor gap, bump test cup volume, controller, fan air path, valve, sounder and beacon, power supply and set points. `cad/src/model.py` now builds each part a maker handles, with its fixings, and runs 127 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch without overlapping, parts that must stay apart keep the stated clearance, no two parts overlap, and every part bears on the wall, floor or a neighbour. All 127 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The bump test cup's 2 mm top plate covered both sensor ports completely (2,118 mm³ of plastic across the openings), so no gas could reach the sensors. | Two 22 mm openings in the cup's top plate, in line with the ports. | Restores the gas path. The cup volume used in the calculations (114 mL) already assumed a top plate, so it is unchanged. |
| P2 | The 25 mm arrestor discs sat in 26 mm ports with nothing to hold them: they would drop through. | Ports drilled 22 mm; each disc rests on the 1.5 mm ledge this leaves on the inside of the floor and is bonded round its edge with a bead of two-part epoxy (never silicone, which poisons catalytic sensors). | The disc stays where the calculations put it (on the floor, 2.2 mm below the sensor can), so the 1.5 s arrestor lag [F1] is unchanged, and the bonded edge stops gas bypassing the disc. |
| P3 | A wall plate fused to the back of the head cut 2.5 mm into the box's inside (21,840 mm³ of overlap), and the head had no fixing to the wall. | Wall plate removed. The head box is a stock box with its lid on the room-side face; two M4 screws with wall plugs go through its back wall from inside. | Uses what a stock box offers; the head's size and position are unchanged. |
| P4 | The sensor carrier board and the cup had no fixing. | Four 22 mm M3 female standoffs on the floor of the head. Four M3 screws come up through the cup's top plate and the head floor into the standoffs; the board sits on the standoffs on four more M3 screws. | One set of standoffs holds both the cup and the board, and the standoff length sets the 22 mm floor-to-board gap that gives the 2.2 mm sensor gap. |
| P5 | The cup's gas nozzle was a solid stub with no way to connect the 4 mm tube. | A printed boss on the cup's side, tapped M5, with a straight push-in fitting for 4 mm tube. | A standard pneumatic fitting; the tube pushes in and pulls out with the collet. |
| P6 | The controller board floated 4.5 mm off the box's back wall with no fixing, and the modules cut 0.5 mm into it. | A 2 mm aluminium mounting plate on the box's four moulded bosses, four M4 self-tapping screws; each module on M3 screws and 6 mm nylon standoffs. | Stock IP65 boxes have these bosses; the modules can be bought and fitted without a laid-out circuit board, which is TRL 4 work. |
| P7 | The front panel floated 4 mm in front of an open-fronted box. | The panel is the box's own lid, cut for the display window, key switch, test button and three lights; each part is held through its hole by its nut or screws. | The lid closes on the box's gasket with the panel parts in it. |
| P8 | The controller had no cable entries and no wall fixing. | Five M16 cable glands (four in the top for the head, fan, valve and beacon cables, one in the bottom for the supply lead) and four screws through the box's corner fixing holes. | Keeps the box sealed; cables arrive from the trunking above and the supply from the floor below. |
| P9 | The bump test port overlapped a solid block that stood in for its bracket, and the tube did not start at the port. | A 40 mm length of 30 x 30 x 3 mm aluminium angle on the wall 35 mm left of the controller, with the bulkhead port pointing down through its flat leg (cap underneath, push-fit on top); the tube rises from the port and runs on the wall in seven saddle clips. | Span gas is connected from below at chest height, and the tube follows the wall to the head as in the concept (2.72 m instead of 2.69 m [J1]). |
| P10 | The fan was drawn as a 146 mm motor floating inside the 150 mm sleeve with no support, although the fan specified has a body about 170 mm across; the sleeve also cut into the inside grille. | A 200 mm wall sleeve takes the 170 mm fan body. A 3 mm aluminium fan plate on the inside wall face holds the fan by four screws into its inlet face; the inside grille screws to the plate; the backdraft shutter fits on the fan's outlet spigot and the weather hood screws to the outside wall by four tabs. | The air still passes through the fan's 150 mm spigots, so the duct losses and the 347 m³/h boost [G3] are unchanged. The wall opening grows from about 160 to 206 mm; it is builder's work, already outside R13. |
| P11 | The solenoid valve hung in mid-air 148 mm from the wall, and the supply line passed straight through its body (4,222 mm³ of overlap). | A bracket bent from 40 x 5 mm aluminium flat bar: a 132 mm leg on the wall on two M6 screws with plugs, and a 200 mm arm under the valve, which is held by two M5 screws into the tapped holes under its body. The supply line now ends at the valve's two ports. | Supports the valve independently of the gas line, so the gas fitter's joints carry no load. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| BOM | Lines 1, 2, 4, 5, 6, 7, 9, 11, 14 and 15 re-specified; line 9 (larger sleeve) +USD 5, line 14 (standoffs, screws, epoxy) +USD 4, line 15 (push-in fitting, clips) +USD 2; new line 16, made brackets and plates, USD 14. | Parts added for construction. |
| Cost | Value-engineering target USD 265 (`budget_usd`, unchanged). Estimated cost of the constructable design USD 289, USD 24 over the target [N1]. R14 is reported against the target. | The concept left out brackets, plates and fixings. |
| Installation | 255 min (4.2 h) with the wall openings as builder's work, 15 min over R13's 4 h (it was 5 min over) [M1]; R13 stays at risk. | Ten more minutes to fix the valve bracket. |
| Bump test | Tube 2.72 m, 13.3 mL; the reading still settles in about 67 s [J1]. | Tube route follows the bracket and clips. |
| Calculation note | HGD-CAL-001 v0.3; HGD-REQ-001 v0.5 (R13, R14 status). No other figure changed. | Follows the model. |
| Drawings and media | HGD-DWG-001 Rev P4; making sketches HGD-DWG-101 to 109 added; concept blueprint HGD-DWG-010 Rev P4; concept media and STEP and STL files regenerated. | Follows the model. |

*Table 3. Proposed for Amish; decided on 2026-10-02 as shown under each recommendation.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The head is mounted on the back wall above the bench, so its ports sit 110 mm horizontally from the back edge of the apparatus and 260 mm from its centre, against a plume radius of about 141 mm at the ports [E7]. This touches the head placement rule, which is part of the safety case. | (a) keep the wall mounting and set the offset limit by test at TRL 4, as decided; (b) hang the head from the ceiling directly over the apparatus on a drop rod. | (a) for the prototype, since the offset limit is already a TRL 4 test; revisit if the test shows the offset matters. Changed in the recommendation to Amish and decided on 2026-10-02: (b), the head hangs from the ceiling on a drop rod directly over the apparatus; wall mounting only if the TRL 4 plume test shows a trip at the wall position. At the wall position the design leak would only warn, and the valve would wait for the 5 min escalation with about 28 L released. |
| A2 | The fan motor now sits inside the wall sleeve rather than partly in the room. The safety case already notes the motor is in the exhaust stream and not rated for hazardous areas. | (a) accept; (b) specify a fan with the motor outside the air stream (a belt or external-rotor design). | (a); no change to the ignition-source argument, which relies on continuous running. Decided on 2026-10-02: (a) for the supervised teaching prototype; (b) for any room used without close supervision, since the argument rests on supervision. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan HGD-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`), and the design decisions register HGD-DEC-001 indexes the decisions.
- With A1 decided as (b), the model, drawings, build plan and calculation E7 were updated to the ceiling drop rod on 2026-10-02 (`docs/REVIEW.md`, approved follow-ups carried out).
- Requirement status after the decisions of 2026-10-02: 1 not met on estimate (R13), 2 at risk (R4, R7), 1 not verifiable at TRL 3 (R1), 6 met on paper, 4 met by design, and R14 over the value-engineering target by USD 146 (HGD-CAL-001 v0.4).
- The appearance model `cad/src/product_model.py` was updated to the constructable design on 2026-10-02 and its render scenes exported; the photoreal renders, `media/card.png` and `media/social-preview.png` are to be regenerated from them on Amish's Mac, where Blender is.
- The box, fan and valve are chosen at TRL 4. The head box lid face, the controller box bosses and corner holes, the fan's inlet-face fixing holes and the valve's tapped mounting holes must be checked then, and the made parts drilled to suit.
