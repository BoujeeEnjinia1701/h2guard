---
doc_id: HGD-PRC-001
title: H2Guard design precis
project: H2Guard
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, components, first-order numbers, design choices, safety, media)
---

# H2Guard design precis

H2Guard protects one small room where hydrogen is used. A detector head at the ceiling carries a catalytic sensor that reads 0 to 100 % of the lower flammability limit (LFL) and a metal oxide sensor for early warning. A wall controller at chest height keeps a 150 mm exhaust fan running at high level, holds a normally closed solenoid valve on the hydrogen supply open only while all is well, and drives a sounder and beacon. At 10 % LFL it warns and boosts the fan; at 25 % LFL it closes the valve and latches the alarm. Loss of power, a sensor fault, a stopped fan or a crashed controller all close the valve, and a hardware comparator can trip the valve without the firmware. First-order numbers suggest the valve closes about 35 s after hydrogen reaches the head, continuous ventilation keeps the 5 L/min design leak at about 5 % LFL in a well-mixed 30 m3 room, and the parts cost about $239 against a $180 budget. H2Guard is a research and teaching prototype, not a certified gas detection system.

![Hero render](../media/hero.png)

*Figure 1. H2Guard in a 30 m3 teaching room, with a 1.75 m person for scale. Detector head (orange) above the bench, exhaust fan (blue) high on the wall, make-up air grille low on the far side, solenoid valve (gold) on the supply line, controller and beacon near the room entrance. Grey parts are context. Massing model.*

## How it works

1. **Sense.** Hydrogen rises and collects under the ceiling. The detector head sits at the high point directly above the likely leak source, within 0.3 m of the ceiling. The catalytic sensor measures 0 to 100 % LFL and sets the warning and trip. The metal oxide sensor responds from about 30 ppm and shows small, slow leaks as a trend long before the catalytic reading moves; it never trips the system alone, because humidity and other vapors affect it.
2. **Decide.** The controller reads both sensors. The microcontroller handles set points, display, logging and self-test. In parallel, a hardware window comparator watches the catalytic sensor bridge: above the trip level, or if the bridge reads open or shorted, it removes power from the valve directly.
3. **Act.**
   - **Normal:** fan at continuous speed, valve energized (open), green light.
   - **Warning, 10 % LFL (0.4 % vol):** fan to boost, amber light, intermittent sounder. Clears itself when the reading falls.
   - **Trip, 25 % LFL (1.0 % vol):** valve de-energized (closed), fan on boost, continuous sounder and red beacon. Latched: the supply stays closed until someone turns the reset key and the reading is below 10 % LFL.
   - **Fault:** any loss of 24 V power, sensor fault, heater failure, watchdog timeout or fan stop (no tachometer pulses for 10 s) closes the valve and shows the fault.
4. **Ventilate.** The fan runs all the time, so it is never switched on in a flammable mixture, and so no gas can flow unless the room is being ventilated. Make-up air enters through a low grille on the far side of the room, sweeping the room toward the high exhaust.
5. **Record and test.** The controller logs readings, warnings, trips, faults and resets. A test button runs the sounder, beacon, fan boost and valve close. A bump test with certified 1 % vol hydrogen span gas checks the sensor response (the gas port is not yet designed, see Open questions).

![Detect, decide, act chain](../media/flow.png)

*Figure 2. Detect, decide and act chain for the design leak in the 30 m3 reference room. All values are estimates; the sensor t90 is a target not yet confirmed from a datasheet.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 3.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Detector head enclosure | ABS or polycarbonate box, about 110 x 80 x 90 mm, two sensor ports facing down | Ceiling or high wall mount above the source |
| 2 | Catalytic hydrogen sensor | Catalytic (pellistor) sensor with hydrogen response, 0 to 100 % LFL, for example Figaro TGS6812 | Primary trip sensor; needs oxygen and can be poisoned by silicones |
| 3 | Metal oxide hydrogen sensor | About 30 to 3,000 ppm, for example Figaro TGS2616-C00 | Early warning and trend only |
| 4 | Flame arrestor discs and drip skirt | Sintered stainless discs in the sensor ports | Keeps flame from the hot sensor element inside the head; not a certified flameproof assembly |
| 5 | Controller enclosure | IP65 polycarbonate wall box, about 200 x 250 x 90 mm | At chest height, at least 1 m below the ceiling |
| 6 | Controller board | RP2040-class microcontroller; hardware comparator trip; drivers for valve, fan and alarm; tachometer input; event log | Firmware beyond a labeled sketch is TRL 4 work |
| 7 | Front panel | OLED display, key-switch reset, test button, status lights | The key keeps students from clearing a trip |
| 8 | 24 V DC power supply | Certified plug-in supply, 24 V, 60 W | Only mains part; bought certified |
| 9 | Exhaust fan | 150 mm brushless DC duct fan, 24 V, about 300 m3/h free air, tachometer | High on the wall near the ceiling; runs continuously |
| 10 | Make-up air grille | Low-level wall grille with insect mesh | Far side of the room from the fan |
| 11 | Normally closed solenoid valve | 1/4 in, brass, FKM seals, 24 V DC, 0 to 10 bar | After the regulator; closes on loss of power |
| 12 | Sounder and beacon | 24 V, about 90 dB at 1 m, red flashing | At the room entrance |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view of the H2Guard parts with BOM numbers. Cabling (BOM line 13) and fixings (line 14) are not shown.*

![Cutaway](../media/cutaway.png)

*Figure 4. Sections through the controller (left) and the detector head (right), each cut on a vertical plane and seen from the side. The head section passes through the catalytic sensor and its flame arrestor disc. The head is drawn beside the controller for this view.*

The blueprint concept sheet ([PDF](../media/concept-blueprint.pdf)) shows the arrangement in plan and elevation with the key figures, and the [interactive 3D model](../media/viewer.html) shows the parts in place.

## First-order numbers

All values are estimates for the concept, to be checked by calculation at TRL 3.

**Hydrogen made by a small electrolyzer.** Faraday's law gives the production rate as n = I x N / (2F), where I x N is the stack current times the number of cells. A 100 W PEM stack at about 1.9 V per cell gives I x N of about 53 A, so n is about 2.7 x 10^-4 mol/s, or about 0.4 L/min at 20 °C (24.1 L/mol). Even a total leak of the full output of an H2Bench-sized electrolyzer is well below the 5 L/min design leak.

**How fast a ceiling layer builds up.** In the 30 m3 reference room, take a 0.3 m layer under the 12 m2 ceiling (3.6 m3), well mixed and unventilated.

Table 2. Time to reach set points with a 5 L/min leak, no ventilation (estimates).

| Level | Hydrogen needed in the layer | Time at 5 L/min | Whole room well mixed |
| --- | --- | --- | --- |
| 10 % LFL (0.4 % vol) | about 14 L | about 3 min | about 24 min |
| 25 % LFL (1.0 % vol) | about 36 L | about 7 min | about 60 min |
| 100 % LFL (4 % vol) | about 144 L | about 29 min | about 4 h |

A plume directly above the leak reaches these levels sooner than the layer average, which is why the head goes directly above the source.

**Dilution by the fan.** With 150 m3/h (2,500 L/min, 5 air changes per hour) of continuous exhaust, the steady well-mixed concentration for a 5 L/min leak is 5 / 2,505, about 0.20 % vol or 5 % LFL. On boost (300 m3/h) it falls to about 0.10 % vol. Stratification can make the ceiling layer several times richer than the room average; with a factor of 5 the head would read about 25 % LFL, which is the trip point. So continuous ventilation alone keeps the room well below the LFL for the design leak, and the interlock stops the source if it does not. For the 0.4 L/min electrolyzer case the mixed value is about 0.016 % vol.

**Time from leak to valve closed.** Transport from the source to the head: a few seconds for a buoyant plume 1.4 m below the ceiling (estimate, up to 5 s). Sensor t90: 30 s target (not yet confirmed for the chosen catalytic sensor). Comparator and driver: under 0.1 s. Valve closing: under 1 s (typical for small direct-acting solenoid valves, to be confirmed). Total about 35 s, within the R4 limit of 60 s. About 3 L of hydrogen escapes at 5 L/min in that time, plus the gas held in the supply line downstream of the valve (under 1 L for a few meters of small tubing at 10 bar).

**Inventory limit.** If the whole inventory leaks and mixes into the room, it stays below 25 % LFL only if it is 1 % of the room volume or less: 300 L at atmospheric pressure (about 25 g) for 30 m3. A 10 L cylinder at 200 bar holds about 1.7 m3, more than five times this, so an unrestricted cylinder is outside what H2Guard can protect; a metal hydride canister or low-pressure store of a few hundred liters, as planned for H2Bench, is inside it. This rule is proposed for R9.

**Power budget (estimates).** Normal: catalytic sensor about 0.5 W, metal oxide sensor about 0.3 W, controller and display about 0.5 W, valve coil held open about 8 W, fan at continuous speed about 12 W, total about 21 W. Alarm: valve off, fan boost about 25 W, beacon and sounder about 3 W, total about 29 W. The 60 W supply leaves a margin of about two.

**Cost.** About $239 in indicative parts prices (`bom/bom.csv`), about 33 % over the $180 budget. Without the fan and grille (about $43), which some rooms already have in another form, the detector, controller, valve, alarm and cabling (lines 1 to 8 and 11 to 14) come to about $196, still over budget.

## Key design choices

All choices below are proposed, awaiting Amish.

1. **Catalytic sensor for the trip, metal oxide sensor for early warning.** Options: (a) catalytic plus metal oxide (about $50 of sensors); (b) a certified molecular property spectrometer sensor (about $249, t90 under 20 s, poisoning resistant, [NevadaNano](https://nevadanano.com/mps-hydrogen-gas-sensor/)); (c) metal oxide only (cheapest, but its range ends at about 0.3 % vol and it drifts with humidity). Recommendation: (a) for the teaching prototype, with (b) documented as the upgrade for any room used without close supervision.
2. **Normally closed valve, energize to open.** Fail-safe on power loss, at the cost of about 8 W of coil power all the time. A latching or motorized valve would save power but would not close when the power fails. Recommendation: normally closed.
3. **Independent hardware trip.** A comparator trip beside the microcontroller, so a firmware bug cannot hold the valve open. Recommendation: keep; it is the core of the design.
4. **Continuous ventilation with a boost, rather than a fan that starts on alarm.** Avoids switching a motor on in a flammable mixture and proves airflow before gas can flow. Recommendation: continuous.
5. **Set points 10 % LFL (warn) and 25 % LFL (trip).** More conservative than the 25 % and 50 % levels often used in industry. Recommendation: keep for teaching use, where people are close to the source.
6. **24 V DC throughout, with a certified plug-in supply.** Keeps mains out of the self-built parts. Recommendation: keep.
7. **Key-switch reset.** Stops students from clearing a trip without a supervisor. Recommendation: keep.
8. **One detector head per room.** A second head is needed if the ceiling has beams or pockets that could trap gas away from the first head. Recommendation: one head as the base kit, with a second head as an option.

## Relation to other lab projects

- **H2Bench** is the first host. Its README states that it is "Protected by H2Guard", and its gas system (electrolyzer, low-pressure store, regulator and tubing) is where the valve and any flow restrictor go. The inventory rule (R9) would apply to H2Bench's storage.
- H2Guard does not use a SwapCell pack or any lithium cell.

## Safety

> **Safety:** Hydrogen is flammable in air from about 4 % to 74 % by volume and ignites with very little energy. H2Guard is a research and teaching prototype, not a certified gas detection system, and it must not be the only safeguard in any room where codes or insurers require certified detection. Use certified equipment for any real installation.

> **Safety:** The parts are not certified for hazardous areas. The catalytic sensor element runs hot, and the fan motor, relays and supply are possible ignition sources. The design limits this by keeping the controller and supply low on the wall, running the fan continuously and fitting flame arrestors to the sensor ports, but it does not remove the risk.

> **Safety:** The design leak assumes a flow restrictor. A failed regulator on an unrestricted high-pressure cylinder can release gas far faster than the fan can remove it. Keep inventories within the proposed limit, and have gas fittings made and leak-tested by a competent person.

> **Safety:** Catalytic sensors need oxygen and can be poisoned by silicones, sulfur compounds and some solvents, which makes them read low without warning. Bump test before each teaching session and after any exposure to these vapors, and replace the sensor when it fails a bump test.

> **Safety:** Mains power enters only through a certified plug-in supply. Do not open it or wire mains inside the controller.

## Open questions for TRL 3

- Confirm t90, power and poisoning behavior of the chosen catalytic sensor from its datasheet, and whether it responds to hydrogen well enough across 0 to 100 % LFL.
- Design a bump test cap and gas port for the detector head (R12, not yet met), and decide how span gas is supplied. CalRig might host a hydrogen span check; that is for CalRig to decide.
- Check the fan against duct, grille and weather hood losses, and decide how airflow is proven (tachometer only, or a differential pressure switch).
- Carry out a failure modes and effects analysis of the trip chain, including a welded relay contact, a stuck valve and a blocked sensor port.
- Hydrogen compatibility and leak rating of low-cost solenoid valves, or whether a certified gas valve is needed.
- Where set points and the inventory rule come from for each country the first users are in.
- Whether the parts cost can be brought to $180, or the budget should change (proposed, awaiting Amish).
