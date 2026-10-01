# Review note: H2Guard

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (HGD-PRB-001 v0.2): problem with cited hydrogen properties, adoption figures and incidents; users; operating environment; constraints; out of scope; prior work (ISO 26142, NFPA 2, sensor types, HIAD 2.0); open questions. There was no co-design checklist to keep.
- `docs/03-requirements.md` (HGD-REQ-001 v0.2): 15 measurable requirements (R1 to R15) with targets, verification method and status at TRL 2, plus assumptions.
- `docs/02-concept.md` (HGD-PRC-001 v0.2): how it works, 12 numbered components, first-order numbers (electrolyzer output, ceiling layer build-up, dilution, response time, inventory limit, power, cost), eight design choices, relation to H2Bench, safety, open questions.
- `cad/src/concept_media.py`: massing model of a 30 m3 class teaching room with the 12 H2Guard parts colored and numbered, and grey context (room, bench, apparatus, small cylinder, supply line, cable runs, 1.75 m person).
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg` (orthographic views include the room outline so heights read correctly), `model.glb` and `viewer.html`, `exploded.png` (compact kit-of-parts layout with BOM callouts), `cutaway.png` (sections through controller and detector head), `flow.png` (detect, decide, act chain with estimated values). Temporary `_views` folders removed.
- `bom/bom.csv`: 14 lines with indicative prices, lines 1 to 12 matching the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; Concept rationale, Burning platform, By industry and By country or region tables, and What sparked the idea expanded with cited figures; Concept, Key components and Safety brought in line with the precis.
- `docs/pdf/`: branded PDFs of the three controlled documents.

`project.yaml` is unchanged: the pitch and problem still match the numbers found.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Warning and trip set points | 10 % LFL (0.4 % vol) and 25 % LFL (1.0 % vol) | R2, R3 by design |
| Hydrogen from a 100 W electrolyzer | about 0.4 L/min | Design leak 5 L/min covers it |
| Ceiling layer (0.3 m) to 25 % LFL, 5 L/min, no ventilation | about 7 min (whole room mixed: about 60 min) | |
| Well-mixed concentration, 5 L/min leak, 150 m3/h exhaust | about 0.20 % vol (5 % LFL) | R8 met by estimate |
| Leak reaching head to valve closed | about 35 s (sensor t90 30 s assumed) | R4 unverified |
| Hydrogen released before the valve closes | about 3 L | |
| Inventory limit for a 30 m3 room | 300 L at atmospheric pressure (about 25 g) | R9 proposed |
| Power | about 21 W normal, 29 W in alarm | R11 met |
| Parts cost | about $239 (about $196 without fan and grille) | **R14 not met** |

Requirements not met or unverified:

- **R14 (cost) not met:** about $239 against $180.
- **R12 (bump test in use) not met:** no test cap or span gas port is designed yet.
- **R4 unverified:** the t90 of the proposed catalytic sensor has not been confirmed from a datasheet.
- **R7 unverified:** fan rated about 300 m3/h in free air; duct, grille and hood losses not yet checked.
- **R15 not certified:** layout avoids ignition sources in the ceiling layer, but no part is rated for hazardous areas.
- R5 and R6 (fail-safe and hardware trip) are met by design only; no FMEA yet.

### Proposed, awaiting Amish

Status update 2026-09-25: items 1 to 8 are decided by Amish, 2026-09-25: go with recommendation (HGD-DDR-001, HGD-DDR-002). For item 1 the later TRL 3 recommendation ($265) superseded the $250 figure.

1. **Budget.** Options: (a) raise `budget_usd` to $250; (b) treat the fan and grille as site ventilation outside the kit, giving about $196, still over; (c) drop the metal oxide sensor and use a cheaper enclosure and valve to approach $180, losing early warning. Recommendation: (a). `project.yaml` is unchanged. Decided by Amish, 2026-09-25: go with recommendation, as revised at TRL 3 to $265.
2. **Sensor baseline.** Options: (a) catalytic plus metal oxide pair (about $50); (b) certified MPS sensor (about $249, total about $440); (c) metal oxide only. Recommendation: (a) for supervised teaching, with (b) documented as the upgrade. Decided by Amish, 2026-09-25: go with recommendation.
3. **Set points** of 10 % LFL warning and 25 % LFL trip, more conservative than the 25 % and 50 % levels common in industry. Recommendation: keep. Decided by Amish, 2026-09-25: go with recommendation.
4. **Normally closed valve, energize to open**, rather than a latching or motorized valve. Recommendation: keep. Decided by Amish, 2026-09-25: go with recommendation.
5. **Continuous ventilation with boost**, rather than a fan that starts on alarm. Recommendation: keep. Decided by Amish, 2026-09-25: go with recommendation.
6. **Inventory rule (R9):** 1 % of room volume at atmospheric pressure, or a flow restrictor sized to the design leak, as a condition for H2Bench and any other lab project using H2Guard. Recommendation: adopt, and ask H2Bench to reflect it. Decided by Amish, 2026-09-25: go with recommendation.
7. **Key-switch reset and one detector head per room** as the base kit, with a second head as an option. Decided by Amish, 2026-09-25: go with recommendation.
8. **First users:** a school science department running H2Bench, a university teaching lab or a startup. Recommendation: a university teaching lab first, because supervision and a technician are in place. Decided by Amish, 2026-09-25: go with recommendation.

### Safety concerns

- It is a teaching prototype, not certified detection; the documents say this plainly, but a low-cost kit invites use as the only safeguard.
- Ignition sources: the catalytic element runs hot, and the fan motor and relays are not rated for flammable atmospheres.
- An unrestricted high-pressure cylinder can overwhelm any small fan; the inventory rule and flow restrictor are essential.
- Catalytic sensors are poisoned by silicones and some solvents and then read low; bump testing is needed, and the means of doing it is not designed yet.
- Mains appears only inside a certified plug-in supply.

### Problems and notes

- The kit's `cutaway_parts` places its cutter box at X = 0, Z = 0, so it misses parts far from the origin. `concept_media.py` therefore cuts the head and controller with its own function. This may affect other repos with large scenes; worth fixing in the kit.
- `render_all` was run with `cut=False` and `scale_figure=False` (the person is added as a context part so it stands clear of the wall); the hero and blueprint are then re-rendered in the script with clearer notes and room context in the orthographic views.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- Suggestion only: CalRig could add a hydrogen span gas check; that is CalRig's decision.

### Recommended next step

Review this note and the media, then decide items 1, 2 and 6. If approved, run `/advance-trl3` to confirm the sensor data, calculate the ventilation with duct losses, write the FMEA of the trip chain, design the bump test port and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the H2Guard TRL 2 points item by item, so every item with a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (HGD-DDR-001 v0.1, status proposed): nine items adopted as recommended for TRL 3, open for Amish's review (D1 to D9), and five items left open (O1 to O5), including the budget figure.
- `docs/04-calcs/01-sizing.md` (HGD-CAL-001 v0.1) and `docs/04-calcs/sizing.py` (writes `docs/04-calcs/results.txt`): sources and inventory, flow restrictor sizing, build-up, dilution, the plume at the detector head, arrestor lag, the response and fault chain, fan and duct losses, power, bump test and log, alarm level, placement, installation time, cost, and a first-pass FMEA of the trip chain, with a status for every requirement. The script imports the model's parameters and reads the BOM and `project.yaml`.
- `cad/src/model.py`: parametric build123d model of all H2Guard parts in the 30 m3 reference room (head with ports, sensors, arrestors and bump test cup; controller, board and panel; supply; fan with grille, sleeve and hood; make-up grille; valve; beacon; bump test port and tube) plus grey context. Exports `cad/step/` and `cad/stl/` for `h2guard-assembly`, `detector-head`, `controller` and `exhaust-fan`.
- `cad/src/sheets.py` and `cad/drawings/HGD-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:50, with mounting heights, a detector head detail and interface notes, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". HGD-DWG-001 was free because the concept blueprint is HGD-DWG-010 (now Rev P2 from the model).
- `bom/bom.csv` (15 lines, all priced with a supplier type, $264.00) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered and every image checked (the person was moved clear of the controller and callout 15 clear of the panel). Temporary `_views` folders removed.
- HGD-PRB-001, HGD-PRC-001 and HGD-REQ-001 revised to v0.3; `README.md` (TRL 3, cost, findings, links) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

Design changes the calculations required, within the adopted choices: the exhaust fan is re-specified from a 300 m3/h axial fan (237 m3/h against the losses) to a 450 m3/h mixed-flow EC fan (347 m3/h); the arrestor discs are 2 mm instead of 5 mm with the sensors about 2 mm behind them (lag 1.5 s instead of about 21 s); a bump test cup, tube and capped port are added (R12); the comparator trip now has a hardware latch and a relay in series with the microcontroller's valve switch; the board needs 4 MB of flash for the 90-day log; the reference room in the model is the 4 x 3 x 2.5 m room of the requirements (the TRL 2 media used a 2.6 m ceiling).

### Requirement status (HGD-CAL-001, Table 5)

2 not met, 2 at risk, 1 not verifiable at TRL 3, 6 met on paper, 4 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R14 Cost | **Not met** | $264.00 against $180; also $14 over the $250 recommended at TRL 2 |
| R13 Installation | **Not met** on estimate | 6.0 h (4 h limit); 4.1 h if the wall openings are made by others |
| R4 Response | At risk | 35.7 s leak to valve closed with an assumed 30 s t90; 0.17 s trip to closed |
| R7 Ventilation | At risk | 347 m3/h boost on an assumed fan curve (target 300); the TRL 2 fan gave 237 |
| R1 Measurement | Not verifiable at TRL 3 | Resolution needs sensor data; ports 175 mm below the ceiling |
| R2, R5, R8, R10, R11, R12 | Met on paper | Plume 15 % LFL at the head; worst listed fault 1.12 s; room 5.0 % LFL; 76 dB at 5 m; 48.3 W peak; bump test 67 s |
| R3, R6, R9, R15 | Met by design | Latched trip; series hardware relay; 300 L inventory rule (H2Bench 2.6 % of it); controller 1,025 mm below the ceiling |

Key numbers: electrolyzer 0.39 L/min; design leak plume at the head about 15 % LFL mean and 30 % LFL on the axis; 3.0 L released before the valve closes; restrictor orifice 0.13 mm at 10 bar gauge; 13.1 W normal power.

### Decisions recorded (HGD-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: D1 catalytic plus metal oxide sensors, certified sensor as the upgrade; D2 set points 10 % and 25 % LFL; D3 normally closed valve; D4 continuous ventilation with boost; D5 inventory rule (R9); D6 key-switch reset and one head per room, second head optional; D7 a university teaching lab as first users; D8 independent hardware trip; D9 24 V DC with a certified supply. No pitch or problem rewording was recommended, so none was applied.

### Still awaiting Amish

1. **O1, budget.** The TRL 2 recommendation was to raise `budget_usd` to $250; `budget_usd` is unchanged at $180. The priced BOM is $264, over both. Options: (a) $265, covering the TRL 3 kit; (b) $250 with the fan and grille treated as site ventilation ($206 kit); (c) keep $180 and accept R14 not met. Recommendation: (a), because the fan is part of the safety function. Decided by Amish, 2026-09-25: go with recommendation ($265).
2. **O2 to O5.** Oxygen depletion monitoring; set points and inventory rules per country; airflow proving (tachometer only or a differential pressure switch); low-cost or certified gas valve. No recommendations were made. Still proposed, awaiting Amish.
3. **New, timed escalation.** The design leak trips the system only on the plume axis; beside it, or for leaks under about 3.8 L/min, the head warns without closing the supply (HGD-CAL-001, E). Options: (a) close the valve when a warning persists for 5 min; (b) lower the trip to 20 % LFL; (c) accept warning-only for small leaks. Recommendation: (a). Decided by Amish, 2026-09-25: go with recommendation; applied (see the session below).
4. **New, head placement rule.** Keep the head directly above each likely leak point, within a horizontal distance to be set from the plume width, with a second head where leak points are far apart. Recommendation: adopt with the distance set at TRL 4. Decided by Amish, 2026-09-25: go with recommendation; rule applied, distance on hold with TRL 4.
5. **New, R13 scope.** Options: (a) keep 4 h including the wall openings (not met); (b) exclude the fan and grille openings as builder's work (4.1 h, at risk). Recommendation: (b). Decided by Amish, 2026-09-25: go with recommendation; applied.
6. **New, bump test and trip.** A full-span 1 % vol bump test trips the system. Options: (a) keep, as a proof test of the whole chain, with a key reset after each test; (b) use a lower span gas, for example 0.5 % vol. No recommendation until the cup delivery factor is known. Still proposed, awaiting Amish.

### Cross-repo notes

- H2Guard does not depend on FieldNode, CellGuard, MotionCore, ThermaCart, TwinKit or CalRig, so no shared interface applies. CalRig hosting a hydrogen span check remains a suggestion for CalRig.
- H2Bench (host project, read only): its review lists an H2Guard interlock that cuts its bench power supply and closes its tank solenoid, with set point and response time undefined. H2Guard now defines both (25 % LFL; 0.17 s trip to closed) but has one 24 V valve output. A second output, a dry contact for the bench supply, is not in the design; this is an interface point for Amish and H2Bench, not edited here. H2Bench's 7.9 L inventory is within the adopted R9 rule.

### Safety concerns

- False reassurance: a low-cost kit invites use as the only safeguard. The documents say it is a research and teaching prototype, not a certified gas detection system.
- Small or off-axis leaks can hold the head in the warning band with the supply open (new proposal 3).
- Four dangerous undetected faults (HGD-CAL-001, Table 4): blocked duct with the fan turning, poisoned sensor, blocked port and a leaking valve seat. Bump tests cover two; airflow proving and a valve proof test are not designed.
- Ignition sources: the catalytic element runs hot and no part is rated for hazardous areas; the fan motor sits in the exhaust stream.
- An unrestricted high-pressure cylinder overwhelms the fan; the restrictor and inventory rule are essential. Mains appears only inside a certified supply.

### Gaps and notes

- Citations: WebSearch was exhausted. A WebFetch of the Figaro TGS6812 product page was not approved in time; the cited Figaro 2025 overview PDF was fetched and says only that the TGS6812 detects hydrogen up to 100 % LEL with a "fast response", so the sensor t90, power and output remain unconfirmed. No other citation was flagged as unchecked at TRL 2.
- Assumptions only tests can settle: sensor t90 and sensitivity, fan curve, duct losses, plume axis factor and cup delivery factor. Installation times are judgment.
- The exploded view's MOS sensor (3) is too small to see at that scale; its callout marks its position.
- The kit's cutaway cuts only near the origin; `concept_media.py` keeps its own cut function (as at TRL 2). Worth fixing in the kit.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. No test, build, purchasing or firmware material exists.

### Recommended next step

Review HGD-DDR-001 and decide O1 and the four new proposals, above all the timed escalation (item 3), which changes how the system responds to small leaks. TRL 4 is on hold by Amish's instruction; nothing further should be built or tested. For reference only, TRL 4 would need: sensor datasheet confirmation and a bench test of t90 and resolution; a fan curve test against the real duct and grille; a measured bump cup delivery factor; a lab-built controller with the hardware trip exercised against every fault in Table 4; a TST report with `environment: lab`; and build log entries.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now decided by Amish, 2026-09-25: go with recommendation. The record is `docs/decisions/0002-recommendations-accepted.md` (HGD-DDR-002 v0.1); HGD-DDR-001 is revised to v0.2 with D1 to D9 and O1 marked decided.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| Budget (TRL 2 item 1, O1) | $265, covering the TRL 3 kit with fan and grille | `budget_usd` 180; R14 not met, $264 is +47 % | `budget_usd` 265; R14 met on paper, $1 margin |
| Timed escalation | A warning held 5 min closes the valve and latches (firmware rule) | Off-axis design leak warned but never closed the supply | Valve closed at 5.6 min, 28 L released (9 % of the R9 limit), room about 1.9 % LFL [F7, F8]; R3 restated |
| Head placement rule | Head directly above each likely leak point; second head where leak points are far apart; offset limit at TRL 4 | Rule proposed only | R1 restated; plume radius 141 mm at the ports as the paper basis [E7]; offset limit on hold with TRL 4 |
| R13 scope | Fan and grille wall openings are builder's work | Target included openings: 6.0 h, not met | Target excludes them: 4.1 h, at risk (5 min over) |
| D1 to D9 | As recommended (sensor pair, set points, NC valve, continuous ventilation, inventory rule, key reset and one head, university teaching lab first, hardware trip, 24 V DC) | Adopted for TRL 3, open for review | Decided; wording only |
| H2Bench to reflect the inventory rule | Adopt | Asked through the review note | Listed below as a cross-repo action |

Files changed: `project.yaml` (budget, evidence list), `README.md` (budget, concept, key components, decisions links, What sparked the idea), HGD-PRB-001 v0.4, HGD-PRC-001 v0.4, HGD-REQ-001 v0.4, HGD-CAL-001 v0.2 (`sizing.py` adds E7, F7 and F8 and reads the new budget; `results.txt` regenerated), HGD-DDR-001 v0.2, new HGD-DDR-002, `bom/bom-notes.md`, HGD-DWG-001 Rev P1 to P2 (two new notes: placement rule and timed escalation), concept blueprint HGD-DWG-010 Rev P2 to P3 (key figures). No part was added or resized, so `bom/bom.csv` ($264.00) and the model geometry are unchanged; `cad/src/model.py` was re-run and STEP and STL re-exported. No pitch or problem rewording was recommended.

All PDFs, drawings and media were regenerated so that no generated file still shows the old personal domain. `README.md` "What sparked the idea" now traces the design to the 1937 New London School explosion and the odorization law that followed, since hydrogen cannot be odorized (OSHA); the earlier text about a portfolio review was removed.

### Requirement status now (HGD-CAL-001 v0.2, Table 5)

0 not met, 3 at risk, 1 not verifiable at TRL 3, 7 met on paper, 4 met by design (before: 2 not met, 2 at risk, 1, 6, 4).

| ID | Status | Key number |
| --- | --- | --- |
| R13 Installation | At risk | 4.1 h against 4 h, wall openings excluded |
| R4 Response | At risk | 35.7 s leak to valve closed with an assumed 30 s t90 |
| R7 Ventilation | At risk | 347 m3/h boost on an assumed fan curve |
| R1 Measurement | Not verifiable at TRL 3 | Resolution needs sensor data; placement rule adopted |
| R2, R5, R8, R10, R11, R12, R14 | Met on paper | R14: $264.00 against $265 |
| R3, R6, R9, R15 | Met by design | R3 now includes the 5 min escalation |

### Still awaiting Amish (no recommendation was made)

- O2 oxygen depletion monitoring; O3 source of set points and inventory rule per country; O4 airflow proving (tachometer or differential pressure switch); O5 low-cost or certified gas valve.
- Whether a full-span bump test trips the system or a lower span gas is used (no recommendation until the cup delivery factor is known).
- A second interlock output (dry contact) for H2Bench's bench supply (interface point, no recommendation).

### Cross-repo actions

- **H2Bench:** reflect the decided R9 inventory rule (1 % of room volume at atmospheric pressure, or a flow restrictor sized to 5 L/min) in its gas system documents. Its 7.9 L tank is already within the rule. H2Bench was not edited.

### Safety

- The timed escalation is a firmware rule and is not independent like the comparator trip; a leak below about 2.7 L/min at the head gives no warning and is not escalated.
- The other safety concerns of the TRL 3 session stand: false reassurance from a low-cost kit, four dangerous undetected faults, ignition sources, and the need for the inventory rule or a restrictor.

### TRL 4

TRL 4 remains on hold by Amish's instruction. `trl: 3` and `trl_target: 3` are unchanged. Setting the head offset limit by test, the escalation firmware beyond a sketch, and all build, test and purchasing work are decided where recommended but not started.

## Session 2026-09-26: sources strengthened

Every README link in the four rationale sections was re-fetched with WebFetch and checked against its claim.

- **Namibia row:** the link to the Namibia Green Hydrogen Programme site loads and confirms a government program, but the row's second clause (local colleges may lack budgets for industrial detection) had no source. It was replaced with the NUST vice-chancellor's warning of a talent gap of up to 130,000 workers by 2040 (*The Namibian*, 21 September 2025) and NUST's own IGNITE GH2 page (685 graduates and 40 instructors). The row label is now "Namibia."
- **University of Hawaii fine (Burning platform, United States row and HGD-PRB-001):** C&EN alone replaced by C&EN plus the *Honolulu Star-Advertiser* (7 October 2016), which also reports that the 15 violations and $115,500 were later settled at nine violations and $69,300. The uncited clause "many teaching labs handle small gas quantities without fixed detection" was removed from the United States row. HGD-PRB-001 moved to v0.5.
- Confirmed unchanged: IEA Global Hydrogen Review 2025, US DOE hydrogen safety fact sheet, Korea Herald (Gangneung, 2019), Wen et al. (2022), OSHA 1910.178(g)(2), EU hydrogen strategy COM(2020) 301 (40 GW by 2030), PIB (National Green Hydrogen Mission), Texas State Historical Association (New London, 1937) and OSHA hydrogen fire and explosion page.
- No budget change.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was added

`cad/src/product_model.py` exposes `product_parts()` (53 parts: 28 shell, 14 internal, 5 accessory, 6 context), `TITLE` and `RENDER_VIEWS` (hero, exploded and a detail view of the head and controller without context). It reuses PARAMS and derived() from `cad/src/model.py`; every part size, the head-to-ceiling gap, the offsets from the wall and the controller position are as model.py. It adds:

- Detector head: filleted housing with a parting line, wall plate and screws, cable gland, teal accent band and a printed label, the catalytic and MOS sensor cans on their carrier board, the sintered arrestor discs, and the filleted drip skirt and bump test cup with its nozzle.
- Controller: filleted IP65 box with side ribs, a lid frame with a clear polycarbonate window over the board, four lid screws, a teal name plate, cable glands, an OLED display with a lit readout, the key-switch reset, a teal test button and three status lights with the green one lit.
- Controller board: PCB, microcontroller module with its shield can, the series trip relay and the fan interlock relay and valve driver (in the model.py envelopes, with labels), terminal strip and screws.
- Bump test port with bracket and teal dust cap; the 4 mm tube.
- Normally closed solenoid valve: brass body with hex port fittings, coil with a label, and the coil connector.
- Context (not in the BOM): two wall panels, a ceiling section over the head, surface conduit, the hydrogen supply pipe and its stand-off clips.

`README.md` now shows `media/render-hero.png` and links `media/render-exploded.png`; the orchestrator produces both files.

### Differences from model.py (Proposed, awaiting Amish)

1. **Render layout of the head and valve.** In the reference room the head is 1.6 m and the valve 2.35 m from the controller along the wall, and the head ports are about 1.15 m above the controller top. At that spacing each device is too small in a product render. The appearance model therefore shows the head, with its own ceiling section, on a separate wall panel beside the controller panel, drawn 820 mm lower than installed, and the valve on the head panel below it. The head keeps its 85 mm gap to its ceiling and all sizes are unchanged. Proposed, awaiting Amish. Recommendation: keep this as a render-only layout, with the hero caption saying the panels are not at installed heights (the view note does); the installed heights stay as in model.py and HGD-DWG-001 (ports 175 mm below the ceiling, controller top at least 1 m below it). Option: render the true room layout instead, accepting small devices.
2. **Clear window in the controller lid.** BOM line 5 specifies an IP65 polycarbonate wall box without saying whether the lid is clear. The appearance model uses a lid frame with a clear polycarbonate window so the board and relays show, which suits a teaching prototype. Proposed, awaiting Amish. Recommendation: adopt a clear-lid IP65 box (common and similar in price) and add "clear lid" to BOM line 5 at the next BOM revision; it was not edited now.
3. **Omitted parts.** The exhaust fan, make-up air grille, sounder and beacon and power supply (BOM lines 8, 9, 10, 12) are not in the appearance model, to keep the render compact; they remain in model.py and the concept media. Proposed, awaiting Amish. Recommendation: accept for the product renders.
4. **Fixings and label detail.** Screws, glands, labels and the conduit are appearance detail, with BOM lines 13 and 14 for cable and hardware; no new BOM lines are implied.

### Status

This is an appearance model only: no tolerances, no fabrication detail, nothing past TRL 3. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold. model.py, the BOM and the other documents were not edited.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: design for construction and prototype build plan (kit 1.7.0)

Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, `CLAUDE.md`). On 2026-09-30 Amish asked for an illustrated build plan in every repo and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The changes below were made under that instruction to make the design physically buildable; they are recorded in HGD-DDR-003 (status Draft) and are open for his review. None changes what H2Guard does, its pitch or its safety case.

### Design changes made for construction

`cad/src/model.py` now builds every part a maker handles, with its fixings, and runs 127 constructability checks (`python cad/src/model.py --check`, all pass).

1. Bump test cup: its solid top covered both sensor ports; two 22 mm openings added over the ports.
2. Arrestor discs: 25 mm discs in 26 mm ports would fall through; ports now 22 mm, discs rest on the ledge and are bonded with two-part epoxy (no silicone).
3. Detector head: the fused wall plate cut into the box and nothing held it; the plate is gone and two M4 screws through the back hold the stock box, lid facing the room.
4. Sensor board and cup: no fixing; four 22 mm M3 standoffs, screwed from below through the cup and from above through the board.
5. Cup nozzle: a solid stub; now an M5 push-in fitting for the 4 mm tube in a printed boss.
6. Controller board: floating, with modules cutting into it; now a 2 mm aluminium mounting plate on the box's four bosses with modules on 6 mm nylon standoffs.
7. Front panel: floating in front of an open box; now the box's own lid, cut for the display, key switch, button and lights.
8. Controller: five M16 cable glands and four corner wall screws added.
9. Bump test port: overlapped a solid block; now a 30 x 30 x 3 mm aluminium angle bracket with the port pointing down, and seven tube clips.
10. Exhaust fan: a 170 mm fan drawn as a 146 mm motor floating in a 150 mm sleeve; now a 200 mm sleeve with the fan held by a 3 mm aluminium fan plate on the inside wall, the grille screwed to the plate, shutter on the outlet spigot and a hood with fixing tabs. The air path is still 150 mm, so the fan delivery is unchanged.
11. Solenoid valve: hung in mid-air with the supply pipe through its body; now on a bent 40 x 5 mm flat-bar bracket with two M5 screws.

Knock-on: BOM lines 1, 2, 4, 5, 6, 7, 9, 11, 14 and 15 re-specified and line 16 (made brackets and plates) added. Re-run calculations (HGD-CAL-001 v0.3): bump test tube 2.72 m, reading still settles in about 67 s [J1]; installation 4.2 h, 15 min over R13 (still at risk) [M1]; estimated cost USD 289.00 against the USD 265 value-engineering target, USD 24 over [N1]. HGD-REQ-001 v0.5, HGD-PRC-001 v0.5, HGD-PRB-001 v0.6 and `bom/bom-notes.md` updated.

### What was added or regenerated

- `docs/05-build-plan.md` (HGD-BLD-001 v0.1) with `cad/src/build_plan_media.py`: overview, nine making sketches (`cad/drawings/HGD-DWG-101` to `109`), seven joint close-ups, fifteen assembly step pictures and a block-level wiring diagram in `docs/05-build-plan/`.
- `docs/06-design-decisions.md` (HGD-DEC-001 v0.1): 12 open decisions, 7 items to confirm when parts are bought, a value engineering section, and the decisions made.
- `docs/decisions/0003-design-for-construction.md` (HGD-DDR-003 v0.1, Draft).
- `cad/drawings/HGD-DWG-001` Rev P4; concept blueprint HGD-DWG-010 Rev P4; `media/hero.png`, `exploded.png`, `cutaway.png`, `flow.png`, `model.glb`, `viewer.html`; STEP and STL in `cad/step/` and `cad/stl/`.
- `project.yaml`: `design_state: constructable`, the three new documents in `trl_evidence`; `budget_usd` unchanged. `README.md`: links line, cost wording and a "Building the prototype" section.

### Proposed, awaiting Amish

- Accept the changes above (HGD-DDR-003, Table 1). Recommendation: accept.
- A1: the head stays on the back wall, 110 mm from the apparatus's back edge and 260 mm from its centre, against a plume radius of about 141 mm; the offset limit is a TRL 4 test. Recommendation: keep the wall mounting.
- A2: the fan motor now sits inside the wall sleeve in the exhaust stream. Recommendation: accept.
- All other open items are listed in the design decisions register.

### Stale media

The photoreal renders (`media/render-*.png`, made on Amish's Mac and not in this copy), `media/card.png` and `media/social-preview.png` show the concept head, controller and valve without the new brackets, fan plate and larger sleeve, and should be regenerated on the Mac. `cad/src/product_model.py` reads the new 22 mm port size from `model.py` but does not yet model the new brackets and plates.

### Safety

No new hazard is introduced. The build plan adds safety stops before power, before gas reaches the valve, before the first bump test and before hydrogen is used, and keeps silicone and solvents away from the sensors. The earlier concerns stand: false reassurance from a low-cost kit, undetected blocked ducts and leaking valve seats, ignition sources, and the need for the inventory rule or a restrictor.

### Recommended next step

Amish reviews HGD-DDR-003 and the register. TRL 4 (building and testing to the plan) remains on hold.
