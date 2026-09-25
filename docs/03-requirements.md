---
doc_id: HGD-REQ-001
title: H2Guard requirements
project: H2Guard
doc_type: Requirements
version: "0.2"
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
---

# H2Guard requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be checked by calculation at TRL 3 and revised after sessions with the first users. Status is judged against the first-order estimates in HGD-PRC-001. Two requirements are **not met** by the current concept (R12 and R14), and several are met by design only and still unverified.

Table 1. Requirements. LFL is the lower flammability limit of hydrogen in air, taken as 4.0 % by volume, so 10 % LFL is 0.4 % vol and 25 % LFL is 1.0 % vol.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Measure hydrogen at the high point of the room | 0 to 100 % LFL (0 to 4 % vol), resolution 1 % LFL or better; head within 0.3 m of the ceiling above the likely leak source | Sensor datasheet review; installation rule in the precis | Met by selection (catalytic sensor), unverified |
| R2 | Warn early | At 10 % LFL (0.4 % vol): fan to boost, amber light, intermittent sounder; self-clearing | Set point and logic review | Met by design |
| R3 | Trip and shut off the supply | At 25 % LFL (1.0 % vol): valve closed, fan on boost, continuous sounder and beacon; latched until reset with a key and the reading is below 10 % LFL | Set point and logic review | Met by design |
| R4 | Respond fast enough | Sensor t90 of 30 s or less; alarm within 60 s of a step to 1.1 % vol (twice t90, following the ISO 26142 test approach); valve closed within 2 s of the trip | Datasheets, then a bench test at TRL 4 | **Unverified:** catalytic sensor t90 not yet confirmed from a datasheet; estimate about 35 s from leak reaching the head to valve closed |
| R5 | Fail safe | The supply is closed within 2 s of any of: loss of 24 V power, sensor open or short circuit, heater failure, controller watchdog timeout, fan stopped (no tachometer pulses for 10 s) | Failure modes and effects analysis (FMEA) | Met by design (normally closed valve, energize to open); FMEA not yet done |
| R6 | Trip without firmware | A hardware comparator on the catalytic sensor bridge removes valve power at the trip level even if the microcontroller has stopped | Circuit review | Met by design, unverified |
| R7 | Ventilate the room | Continuous exhaust at high level of 5 air changes per hour or more (150 m3/h for the 30 m3 reference room); boost of 10 air changes per hour or more; make-up air at low level on the far side | Fan curve against duct and grille losses | Met on free-air fan rating; **unverified** with duct losses |
| R8 | Keep the design leak below the trip level | With the design leak of 5 L/min and continuous ventilation, the well-mixed room stays below 10 % LFL | First-order dilution calculation | Met by estimate: about 5 % LFL well mixed; local ceiling values may be several times higher |
| R9 | Limit what can leak | Hydrogen inventory that could be released into the room is 1 % of room volume or less at atmospheric pressure (300 L for 30 m3), unless a flow restrictor limits release to the design leak | Installation rule and host project review | Rule proposed; applies to the gas system, not to H2Guard hardware |
| R10 | Alert people | Sounder 85 dB(A) or more at 1 m and a red beacon visible from the room entrance | Component ratings | Met by selection (about 90 dB at 1 m), unverified |
| R11 | Keep mains out of the self-built parts | All self-built wiring 24 V DC; mains only inside a certified power supply; power draw 60 W or less | Design review | Met by design (about 21 W normal, about 29 W in alarm, estimates) |
| R12 | Be checkable in use | Bump test with 1 % vol hydrogen span gas through a test cap in 2 min or less; self-test button runs the alarm, fan boost and valve close; event log of readings, warnings, trips and resets kept for 90 days or more | Design review | **Not met:** no test cap or gas port is designed yet; log and self-test by design |
| R13 | Install simply | Mounted and wired by one person with hand tools in 4 h or less, excluding the gas fitting, which a competent person makes | Installation walk-through at TRL 4 | Unverified |
| R14 | Stay within the concept budget | Parts $180 or less | Priced BOM | **Not met:** about $239 (indicative); budget change proposed, awaiting Amish |
| R15 | Avoid adding ignition sources in the ceiling layer | Fan never switched on in a flammable mixture (runs continuously); controller, relays and power supply mounted at least 1 m below the ceiling; sensor ports behind sintered flame arrestors | Design review | Met by layout; **not certified** for hazardous areas, and the catalytic element runs hot |

## Assumptions

- Reference room: 4 x 3 x 2.5 m (30 m3), one door, general ventilation unknown and taken as zero.
- Design leak: 5 L/min of hydrogen, representing a failed fitting downstream of a regulator with a flow restrictor. A small electrolyzer of about 100 W makes only about 0.4 L/min (see the precis), so this covers it with margin. A failed regulator on an unrestricted cylinder can release far more, and H2Guard does not protect against that (R9).
- Hydrogen collects first in a layer under the ceiling. The first-order numbers use a 0.3 m layer and treat it as well mixed; real plumes are more concentrated near the source.
- Set points follow common practice for hydrogen detection (warning at 10 % LFL, shutdown at 25 % LFL); ISO 26142 describes alarm levels at 25 % or 50 % LFL. The choice of set points is proposed, awaiting Amish.
- Budget: the $180 in `project.yaml` covers H2Guard hardware only, not the gas system, span gas or installation labor.
