---
doc_id: HGD-DEC-001
title: H2Guard design decisions register
project: H2Guard
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the build plan; open decisions gathered from the review note and the decision records; budget treated as a value-engineering target
---

# H2Guard design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes P1 to P11 (cup openings, disc ledge and epoxy, head and controller fixings, standoffs, push-in fitting, mounting plate, lid as front panel, glands, test port bracket, 200 mm fan sleeve with fan plate, valve bracket) | Accept; change any one | Accept all | Every made part and assembly step | HGD-DDR-003, Table 1 |
| 2 | Head mounting: on the back wall above the bench (ports 110 mm from the apparatus's back edge, 260 mm from its centre) or hung from the ceiling directly over the apparatus | (a) wall mounting, offset limit set by test at TRL 4; (b) ceiling drop rod | (a) | Head position and step 4 | HGD-DDR-003, A1 |
| 3 | Fan motor inside the wall sleeve, in the exhaust stream | (a) accept; (b) a fan with its motor outside the air stream | (a) | Fan choice | HGD-DDR-003, A2 |
| 4 | Oxygen depletion monitoring when inert gas cylinders share the room | Add an oxygen sensor; leave to the site | None yet | A third sensor and cable if added | HGD-DDR-001, O2 |
| 5 | Where the set points and the inventory rule come from in each country of the first users | National codes; ISO 26142; the user's own rules | None yet | Trip board threshold, firmware set points | HGD-DDR-001, O3 |
| 6 | How airflow is proven | Tachometer only (as built); add a differential pressure switch | None yet; a blocked duct is not detected with the tachometer alone | A pressure switch and tubing at the fan if added | HGD-DDR-001, O4 |
| 7 | Low-cost solenoid valve or a certified gas valve | Low-cost brass valve (as built); certified gas valve at several times the price | None yet, pending the valve's hydrogen compatibility and seat leak rating | Valve and its bracket holes | HGD-DDR-001, O5 |
| 8 | Whether a full-span bump test trips the system or a lower span gas is used | 1 % hydrogen, tripping the system as a proof test (as planned); about 0.5 % without a trip | None until the cup delivery factor is measured | First checks and safety stop S4 | Review note, 2026-09-25 |
| 9 | A second interlock output (dry contact) for H2Bench's bench supply | Add a relay output; leave H2Bench to switch from the valve signal | None yet (interface point with H2Bench) | A relay and terminal on the mounting plate if added | Review note, 2026-09-25 |
| 10 | Render-only layout of the head and valve beside the controller in the product renders | Keep the render layout with a caption; render the true room layout | Keep, with the caption | None (renders only) | Review note, 2026-09-26, item 1 |
| 11 | Clear window in the controller lid | Clear-lid IP65 box; opaque lid as now specified | Clear-lid box, added to the BOM at its next revision | Controller box choice | Review note, 2026-09-26, item 2 |
| 12 | Fan, make-up grille, sounder, beacon and supply left out of the product renders | Accept; add them | Accept | None (renders only) | Review note, 2026-09-26, item 3 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The catalytic sensor's response time (t90), power and hydrogen output, from its datasheet | R4 assumes a t90 of 30 s; R1's 1 % LFL resolution needs the output | HGD-CAL-001, F3 |
| 2 | The sensor can is about 20 mm across and 17 mm tall | The standoff length sets its 2.2 mm gap above the disc | HGD-DDR-003, P4 |
| 3 | The head box has its lid on a 110 x 90 face | The ports, gland and wall holes assume it | HGD-DDR-003, P3 |
| 4 | The controller box's boss spacing and corner fixing holes | They set the mounting plate holes and the wall screws | HGD-DDR-003, P6, P8 |
| 5 | The fan's body fits a 200 mm sleeve (about 180 mm across or less) and has fixing holes in its inlet face | The fan plate holds it by those holes | HGD-DDR-003, P10 |
| 6 | The fan's curve gives at least 300 m³/h against about 60 Pa | R7 rests on an assumed curve | HGD-CAL-001, G3 |
| 7 | The valve has two tapped holes underneath, 36 mm apart, and is rated for hydrogen with a stated seat leak rate | The bracket holes; the leaking-seat fault in Table 4 of HGD-CAL-001 | HGD-DDR-003, P11; HGD-DDR-001, O5 |

## Value engineering

Value-engineering target: USD 265 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 289 (USD 24 over the target), from the 16-line bill of materials at indicative prices. Main cost drivers and savings worth trying:

- The largest lines are the exhaust fan with its grille, sleeve, shutter and hood (USD 55), the catalytic sensor (USD 35), the solenoid valve (USD 30) and the controller modules (USD 25). Together they are about half the cost.
- Making the design constructable added USD 25: the made brackets and plates (USD 14), the 200 mm wall sleeve (USD 5), standoffs, screws and epoxy (USD 4) and the cup's push-in fitting and tube clips (USD 2).
- Savings worth trying: a printed controller mounting plate in place of aluminium sheet (about USD 3); buying the fan as a kit with its own shutter and hood; one combined controller board at TRL 4 in place of separate bought modules; and, where the room already has mechanical extract at high level, using it in place of the kit fan and grille (USD 63), which would bring the kit to about USD 226.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 to D9: catalytic plus metal oxide sensors (certified sensor as the upgrade); set points 10 % and 25 % LFL; normally closed valve; continuous ventilation with boost; inventory rule (R9); key-switch reset and one head per room; a university teaching lab first; independent hardware trip; 24 V DC with a certified supply | Amish: "i accept all your recommendations, go with them across all repos." | HGD-DDR-001, HGD-DDR-002 |
| 2026-09-25 | Budget figure USD 265, now treated as the value-engineering target | Amish, same instruction; on 2026-10-01: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | HGD-DDR-002 |
| 2026-09-25 | Timed escalation: a warning held 5 min closes the valve and latches | Amish, same instruction | HGD-DDR-002 |
| 2026-09-25 | Head placement rule: a head directly above each likely leak point; offset limit set by test at TRL 4 | Amish, same instruction | HGD-DDR-002 |
| 2026-09-25 | R13 scope: the fan and grille wall openings are builder's work | Amish, same instruction | HGD-DDR-002 |
| 2026-09-25 | H2Bench to reflect the inventory rule | Amish, same instruction | HGD-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; keep open decisions out of the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | HGD-DDR-003 (changes open for review, open decision 1) |
