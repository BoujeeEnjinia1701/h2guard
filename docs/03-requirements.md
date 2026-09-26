---
doc_id: HGD-REQ-001
title: H2Guard requirements
project: H2Guard
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from HGD-CAL-001; set points and inventory rule adopted for TRL 3 per HGD-DDR-001 (pending Amish's review); R6 names the series relay and hardware latch; R12 names the bump test cup and port
---

# H2Guard requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be revised after sessions with the first users. At TRL 3 each requirement is checked by calculation in HGD-CAL-001 against the design in HGD-PRC-001 v0.3 and the model in `cad/src/model.py`. Two requirements are **not met**: R14 (cost, $264 against $180) and R13 (installation, about 6 h against 4 h). R4 and R7 are at risk, and R1 cannot be verified without sensor data. No target was relaxed or redefined at TRL 3. The set points (R2, R3) and the inventory rule (R9) are adopted for TRL 3 work under Amish's 2026-09-25 instruction, open for his review (HGD-DDR-001, D2 and D5).

Table 1. Requirements. LFL is the lower flammability limit of hydrogen in air, taken as 4.0 % by volume, so 10 % LFL is 0.4 % vol and 25 % LFL is 1.0 % vol. Tags in brackets refer to lines of HGD-CAL-001.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (HGD-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Measure hydrogen at the high point of the room | 0 to 100 % LFL (0 to 4 % vol), resolution 1 % LFL or better; head within 0.3 m of the ceiling above the likely leak source | Sensor datasheet review; installation rule in the precis | **Not verifiable at TRL 3:** resolution needs sensor data; placement met (ports 175 mm below the ceiling [L1]) |
| R2 | Warn early | At 10 % LFL (0.4 % vol): fan to boost, amber light, intermittent sounder; self-clearing | Set point and logic review | Met on paper: design leak plume at the head about 15 % LFL [E2] |
| R3 | Trip and shut off the supply | At 25 % LFL (1.0 % vol): valve closed, fan on boost, continuous sounder and beacon; latched until reset with a key and the reading is below 10 % LFL | Set point and logic review | Met by design; the design leak reaches the trip only on the plume axis (about 30 % LFL [E2]); off the axis it warns only |
| R4 | Respond fast enough | Sensor t90 of 30 s or less; alarm within 60 s of a step to 1.1 % vol (twice t90, following the ISO 26142 test approach); valve closed within 2 s of the trip | Datasheets, then a bench test at TRL 4 | **At risk:** 35.7 s leak to valve closed with an assumed 30 s t90; 0.17 s trip to valve closed [F3, F4] |
| R5 | Fail safe | The supply is closed within 2 s of any of: loss of 24 V power, sensor open or short circuit, heater failure, controller watchdog timeout, fan stopped (no tachometer pulses for 10 s) | Failure modes and effects analysis (FMEA) | Met on paper: worst listed fault 1.12 s [F6]; the first-pass FMEA finds four dangerous undetected faults outside this list |
| R6 | Trip without firmware | A hardware comparator on the catalytic sensor bridge, with its own latch, opens a relay in series with the microcontroller's valve switch at the trip level, even if the microcontroller has stopped | Circuit review | Met by design (block diagram level) |
| R7 | Ventilate the room | Continuous exhaust at high level of 5 air changes per hour or more (150 m3/h for the 30 m3 reference room); boost of 10 air changes per hour or more; make-up air at low level on the far side | Fan curve against duct and grille losses | **At risk:** 347 m3/h boost with the re-specified fan on an assumed curve; the TRL 2 fan gave 237 m3/h [G3] |
| R8 | Keep the design leak below the trip level | With the design leak of 5 L/min and continuous ventilation, the well-mixed room stays below 10 % LFL | First-order dilution calculation | Met on paper: 5.0 % LFL well mixed and in the upper layer [D1, D3] |
| R9 | Limit what can leak | Hydrogen inventory that could be released into the room is 1 % of room volume or less at atmospheric pressure (300 L for 30 m3), unless a flow restrictor limits release to the design leak | Installation rule and host project review | Met by design as an installation rule; H2Bench's tank is 2.6 % of the limit; a 0.13 mm orifice at 10 bar gauge limits a failure to 5 L/min [B3, B4] |
| R10 | Alert people | Sounder 85 dB(A) or more at 1 m and a red beacon visible from the room entrance | Component ratings | Met on paper: 90 dB at 1 m, 76 dB at 5 m [K2] |
| R11 | Keep mains out of the self-built parts | All self-built wiring 24 V DC; mains only inside a certified power supply; power draw 60 W or less | Design review | Met on paper: 48.3 W peak in the warning state [H2] |
| R12 | Be checkable in use | Bump test with 1 % vol hydrogen span gas through the test port and head cup in 2 min or less; self-test button runs the alarm, fan boost and valve close; event log of readings, warnings, trips and resets kept for 90 days or more | Design review | Met on paper: bump reading settles in about 67 s [J1]; log 2.07 MB in 4 MB of flash [J3]; cup delivery factor unknown |
| R13 | Install simply | Mounted and wired by one person with hand tools in 4 h or less, excluding the gas fitting, which a competent person makes | Task time estimate; walk-through at TRL 4 | **Not met** on estimate: 6.0 h, or 4.1 h if the wall openings are made by others [M1] |
| R14 | Stay within the concept budget | Parts $180 or less (`budget_usd`) | Priced BOM | **Not met:** $264.00 [N1]; also over the $250 recommended at TRL 2 (proposed, awaiting Amish) |
| R15 | Avoid adding ignition sources in the ceiling layer | Fan never switched on in a flammable mixture (runs continuously); controller, relays and power supply mounted at least 1 m below the ceiling; sensor ports behind sintered flame arrestors | Design review | Met by design: controller top 1,025 mm below the ceiling [L2]; **not certified** for hazardous areas, and the catalytic element runs hot |

## Assumptions

- Reference room: 4 x 3 x 2.5 m (30 m3), one door, general ventilation unknown and taken as zero.
- Design leak: 5 L/min of hydrogen, representing a failed fitting downstream of a regulator with a flow restrictor. A small electrolyzer of about 100 W makes only about 0.39 L/min (HGD-CAL-001, B1), so this covers it with margin. A failed regulator on an unrestricted cylinder can release far more, and H2Guard does not protect against that (R9).
- Hydrogen rises from the leak as a buoyant plume and collects under the ceiling. HGD-CAL-001 uses plume theory for the head and a well-mixed or displacement model for the room.
- Set points follow common practice for hydrogen detection (warning at 10 % LFL, shutdown at 25 % LFL); ISO 26142 describes alarm levels at 25 % or 50 % LFL. The set points are adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review (HGD-DDR-001, D2).
- Budget: the $180 in `project.yaml` covers H2Guard hardware only, not the gas system, span gas or installation labor. A figure of $250 was recommended at TRL 2 and awaits Amish (HGD-DDR-001, O1).
