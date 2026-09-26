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

1. **Budget.** Options: (a) raise `budget_usd` to $250; (b) treat the fan and grille as site ventilation outside the kit, giving about $196, still over; (c) drop the metal oxide sensor and use a cheaper enclosure and valve to approach $180, losing early warning. Recommendation: (a). `project.yaml` is unchanged.
2. **Sensor baseline.** Options: (a) catalytic plus metal oxide pair (about $50); (b) certified MPS sensor (about $249, total about $440); (c) metal oxide only. Recommendation: (a) for supervised teaching, with (b) documented as the upgrade.
3. **Set points** of 10 % LFL warning and 25 % LFL trip, more conservative than the 25 % and 50 % levels common in industry. Recommendation: keep.
4. **Normally closed valve, energize to open**, rather than a latching or motorized valve. Recommendation: keep.
5. **Continuous ventilation with boost**, rather than a fan that starts on alarm. Recommendation: keep.
6. **Inventory rule (R9):** 1 % of room volume at atmospheric pressure, or a flow restrictor sized to the design leak, as a condition for H2Bench and any other lab project using H2Guard. Recommendation: adopt, and ask H2Bench to reflect it.
7. **Key-switch reset and one detector head per room** as the base kit, with a second head as an option.
8. **First users:** a school science department running H2Bench, a university teaching lab or a startup. Recommendation: a university teaching lab first, because supervision and a technician are in place.

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

1. **O1, budget.** The TRL 2 recommendation was to raise `budget_usd` to $250; `budget_usd` is unchanged at $180. The priced BOM is $264, over both. Options: (a) $265, covering the TRL 3 kit; (b) $250 with the fan and grille treated as site ventilation ($206 kit); (c) keep $180 and accept R14 not met. Recommendation: (a), because the fan is part of the safety function.
2. **O2 to O5.** Oxygen depletion monitoring; set points and inventory rules per country; airflow proving (tachometer only or a differential pressure switch); low-cost or certified gas valve. No recommendations were made.
3. **New, timed escalation.** The design leak trips the system only on the plume axis; beside it, or for leaks under about 3.8 L/min, the head warns without closing the supply (HGD-CAL-001, E). Options: (a) close the valve when a warning persists for 5 min; (b) lower the trip to 20 % LFL; (c) accept warning-only for small leaks. Recommendation: (a). Not applied.
4. **New, head placement rule.** Keep the head directly above each likely leak point, within a horizontal distance to be set from the plume width, with a second head where leak points are far apart. Recommendation: adopt with the distance set at TRL 4. Not applied.
5. **New, R13 scope.** Options: (a) keep 4 h including the wall openings (not met); (b) exclude the fan and grille openings as builder's work (4.1 h, at risk). Recommendation: (b). Not applied.
6. **New, bump test and trip.** A full-span 1 % vol bump test trips the system. Options: (a) keep, as a proof test of the whole chain, with a key reset after each test; (b) use a lower span gas, for example 0.5 % vol. No recommendation until the cup delivery factor is known.

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
