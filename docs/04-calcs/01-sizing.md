---
doc_id: HGD-CAL-001
title: H2Guard sizing calculations
project: H2Guard
doc_type: Calculation note
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (sources and inventory, build-up, dilution, plume at the head, response chain, arrestor lag, fan and duct system, power, bump test, alarm level, placement, installation time, cost, trip chain FMEA)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); budget $265, R13 scope, timed escalation (F7, F8) and head placement basis (E7) added; status table updated
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Design for construction (HGD-DDR-003); bump test tube run, installation time and cost re-run; budget treated as a value-engineering target
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: Decisions of 2026-10-02 carried in (HGD-DEC-001); head on a ceiling drop rod over the apparatus (E7, R1 placement), pressure switch airflow proving (G6, F6, Table 4), hydrogen-rated valve, dry-contact output and oxygen sensor option (H1 to H3), tripping bump test, installation time and cost re-run (M1, N1 to N3)
---

# H2Guard sizing calculations

On paper, H2Guard meets ten of its fifteen requirements (six by calculation, four by design), has two at risk, one not met on its estimate and one that cannot be verified at TRL 3, and the cost (R14) is reported against the value-engineering target. Amish accepted the review recommendations on 2026-09-25 (HGD-DDR-002) and decided the remaining open decisions on 2026-10-02 (HGD-DEC-001); this version carries those decisions into the design. **Cost:** Value-engineering target: USD 265. Estimated cost of the constructable design: USD 411 (USD 146 over the target). The hydrogen-rated valve (USD 65 more than the brass valve), the pressure switch, the drop rod, the dry-contact output, the clear-lid box and more cable account for the increase from USD 289. **R13 (installation) is not met on the estimate**: with the wall openings builder's work outside the target, the estimate is 5.0 h against 4 h, after the drop rod, the pressure switch and their cables were added. R4 (response time) is at risk because the catalytic sensor's t90 is still an assumed 30 s, and R7 (ventilation) is at risk because the fan curve is assumed. R1's resolution cannot be checked without sensor data. The calculations changed three parts of the TRL 2 concept: the 300 m3/h axial fan cannot deliver the 300 m3/h boost against the duct and grille losses (237 m3/h), so it is re-specified as a 450 m3/h mixed-flow fan; the 5 mm flame arrestor disc with the sensor 15 mm behind it would add about 21 s of diffusion lag, so the disc is 2 mm thick with the sensor about 2 mm behind it (1.5 s); and a bump test cup, tube and port are added so that R12 can be met. The design leak trips the system at once only if the detector head sits on the plume axis; off the axis the head sees about 15 % LFL and warns. The head now hangs from the ceiling on a drop rod with its ports directly over the apparatus, so the port offset is zero (Section E). The accepted timed escalation now closes the supply when a warning is held for 5 min, at about 5.6 min for the off-axis design leak with 28 L released (Section F). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [E2], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that a room is safe, and H2Guard is a research and teaching prototype, not a certified gas detection system. Hydrogen is flammable in air from about 4 % to 74 % by volume. See HGD-PRC-001, Safety.

## Scope and method

The note checks every requirement in HGD-REQ-001 v0.7 against the design in HGD-PRC-001 v0.7 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and derived dimensions, so the room, mounting heights, sensor cavity, bump test cup and tube are those in the STEP files and in drawing HGD-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.txt`.

The design case is the 30 m3 reference room (4 x 3 x 2.5 m) with a 5 L/min hydrogen leak from fittings on the bench apparatus, 1,150 mm above the floor, with the detector head directly above it.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Hydrogen | LFL 4.0 % vol; 20 °C, 1 atm; molar volume 24.05 L/mol; density 0.0838 kg/m3 (air 1.204) | US DOE fact sheet cited in HGD-PRB-001; ideal gas |
| Leak | 5 L/min design leak downstream of a flow restrictor; point source at the top of the apparatus | HGD-REQ-001 |
| Plume | Morton, Taylor and Turner point-source plume, top-hat entrainment coefficient 0.10 (0.08 to 0.12 checked); axis value twice the top-hat mean; leak momentum and non-Boussinesq effects near the source ignored | Textbook plume theory; the factor of two is an assumption |
| Ventilation | Exhaust at high level, make-up air at low level on the far side; general ventilation of the room taken as zero | HGD-REQ-001 |
| Airflow proving | Static tap in the fan inlet, just inside the grille: depression is the grille loss plus one velocity head (K 1.7 on the 150 mm duct velocity); switch set at half the continuous-flow value | First principles; to confirm at TRL 4 |
| Duct losses | Loss coefficients on the 150 mm duct velocity: inside grille 0.7, backdraft shutter 1.2, weather hood with exit 1.5, sleeve friction factor 0.03; make-up grille K 2.0 on 50 % free area | Handbook ranges; to confirm with the chosen parts |
| Fan curves | Quadratic, p = p0 (1 - (Q/Qmax)^2). TRL 2 axial fan: Qmax 300 m3/h, p0 100 Pa. TRL 3 mixed-flow fan: Qmax 450 m3/h, p0 200 Pa, 35 W input at full speed; power scales with speed cubed | Typical 150 mm fans; no datasheet chosen yet |
| Sensor | Catalytic sensor t90 30 s (target, not confirmed); power 0.5 W; MOS sensor 0.28 W | TRL 2 figures; the Figaro page fetched on 2026-09-25 says only "fast response" |
| Arrestor | Sintered stainless disc, porosity 0.40, tortuosity 3; hydrogen diffusivity in air 0.61 cm2/s at 0 °C, scaled by T^1.75 | Handbook values |
| Trip chain | Comparator 0.05 s, relay drop-out 0.02 s, valve closing 0.10 s with a Zener clamp on the coil; watchdog 1.0 s | Typical small parts; to confirm |
| Other loads | Controller and display 0.5 W; valve coil 8 W; sounder and beacon 3 W; dry-contact relay coil 0.4 W while healthy; oxygen transmitter option 0.5 W | TRL 2 figures; typical small relay and 4 to 20 mA loop |
| Bump test | Span gas 1 % vol hydrogen at 1.0 L/min; cup flushed by five volumes; 34 L disposable cylinder | Common practice; cup delivery factor not known |
| Installation | Task times in Section M are estimates for one competent person with hand tools and a core drill | Judgment; to confirm in use |

## A. Set points

- Warning at 10 % LFL is 0.40 % vol; trip at 25 % LFL is 1.00 % vol [A1]. The reference room is 30.0 m3 with a 12.0 m2 ceiling [A2].

## B. Sources and inventory (R8, R9)

- **Electrolyzer.** A 100 W PEM stack at 1.9 V per cell makes 2.73 x 10^-4 mol/s, 0.39 L/min. The 5 L/min design leak is 13 times this [B1].
- **Inventory limit.** One percent of the room volume is 300 L at 1 atm, 25.1 g of hydrogen [B2]. H2Bench's 2 L tank at 300 kPa gauge holds 7.9 L, 2.6 % of the limit; a 10 L cylinder at 200 bar holds 1.75 m3, 5.8 times the limit [B3].
- **Flow restrictor.** A choked orifice of 0.13 mm at 10 bar gauge, or 0.21 mm at 3 bar gauge, limits a full-bore failure downstream to the design leak [B4]. This sizes the restrictor in the gas system; it is not H2Guard hardware.

## C. Build-up without ventilation

*Table 2. Time to reach the set points with a 5 L/min leak and no ventilation [C1, C2].*

| Level | Ceiling layer 0.3 m (3.6 m3) | Time | Whole room mixed | Time |
| --- | --- | --- | --- | --- |
| 10 % LFL | 14 L | 2.9 min | 120 L | 24 min |
| 25 % LFL | 36 L | 7.2 min | 300 L | 60 min |
| 100 % LFL | 144 L | 28.8 min | 1,200 L | 240 min |

The TRL 2 figures stand.

## D. Dilution with ventilation (R8)

- **Well mixed.** At 150 m3/h the steady concentration for the design leak is 0.200 % vol (5.0 % LFL); at 300 m3/h it is 0.100 % vol (2.5 % LFL). The electrolyzer case gives 0.0157 % vol [D1]. The room time constant at 5 air changes per hour is 12 min [D2].
- **Stratified.** With exhaust at high level, all the hydrogen leaves through the fan at steady state, so the upper layer settles at the exhaust value, 5.0 % LFL [D3]. The plume would carry the full exhaust flow only 2.28 m above the source, and the ceiling is 1.35 m above it, so no clean interface forms: the room above source height is at about the exhaust value [D4]. The TRL 2 worry that the ceiling layer could be five times richer than the room average does not hold at steady state; it does hold near the plume (Section E) and in the first minutes of a leak.

## E. Plume at the detector head (R2, R3)

- **Plume.** The design leak has a buoyancy flux of 7.61 x 10^-4 m4/s3; the sensor ports are 1.175 m above the source [E1]. At the head the plume carries 13.8 L/s of mixture at a mean of 0.60 % vol (15 % LFL), and about 1.21 % vol (30 % LFL) on its axis [E2]. It rises at 0.22 m/s and takes 4.0 s to reach the head [E3].
- **What the head sees.** A head on the plume axis reads above the trip; a head beside the axis reads about the mean and warns but does not trip [E4]. Leaks of 3.8 L/min or more reach 25 % LFL on the axis; leaks of 2.7 L/min or more bring the plume mean to 10 % LFL [E5]. An entrainment coefficient between 0.08 and 0.12 moves the axis value to between 24 and 41 % LFL [E6]. The plume's top-hat radius at the ports is about 141 mm. On the ceiling drop rod the centre of the two ports is 0 mm from the apparatus centre, inside the plume; at the former wall position it was 260 mm away, outside it [E7].
- **Consequence.** For the design leak with the fan running, the room stays at about 5 % LFL (R8 met), but whether the supply closes depends on the head being on the plume axis. A smaller leak, or a leak from a fitting away from the head, is warned but not stopped by the set points alone. Amish accepted two remedies on 2026-09-25 (HGD-DDR-002): a timed escalation that closes the valve when a warning is held for 5 min (Section F, [F7]), and a placement rule that keeps the head directly above each likely leak point, with a second head where leak points are far apart. On 2026-10-02 Amish decided that the head hangs from the ceiling on a drop rod directly over the apparatus (HGD-DEC-001, decision 2); the model now places it there, with its ports 175 mm below the ceiling [E7, L1]. The horizontal offset limit for other rooms is to be set at TRL 4 from a measured plume width; the 141 mm radius above is the paper basis.

## F. Response chain (R4, R5, R6)

- **Flame arrestor lag.** A 25 x 2 mm sintered disc has an effective diffusivity of 9.2 x 10^-6 m2/s and a slab time of 0.43 s. The 1.08 mL cavity between disc and sensor can reaches 90 % in 1.10 s, 1.5 s in all [F1]. The TRL 2 arrangement, a 5 mm disc with the sensor 15 mm behind it, would have added about 21 s [F2], using most of the R4 budget, so the disc is thinned and the sensor moved close to it (`PARAMS["disc"]`, `PARAMS["board_gap"]`).
- **Leak to valve closed.** Rise 4.0 s, arrestor 1.5 s, sensor t90 30 s (assumed), comparator, relay and valve 0.17 s: 35.7 s [F3]. Trip to valve closed is 0.17 s against the 2 s limit, and the alarm follows a step at the head within 32 s against the 60 s limit [F4].
- **Gas released.** About 3.0 L escapes at 5 L/min before the valve closes, plus 0.47 L held in 3 m of 4.3 mm bore line at 10 bar gauge downstream of it [F5]. Both are 1 % of the inventory limit or less.
- **Faults.** A watchdog timeout closes the valve in 1.12 s; a sensor open or short circuit through the comparator in 0.17 s; a stopped fan, once detected after 10 s without tachometer pulses, in 0.12 s; and loss of airflow, once the pressure switch has not proved flow for 10 s with the fan running (fan stopped, duct blocked or shutter stuck), in 0.12 s [F6]. Loss of 24 V closes the valve as the coil current decays.
- **Timed escalation (HGD-DDR-002).** A warning held for 300 s closes the valve through the microcontroller and latches like a trip. For the off-axis design leak the warning comes at 35.5 s and the valve closes at 336 s (5.6 min), with 28 L released, 9 % of the R9 inventory limit; at the 2.7 L/min warning threshold leak about 15 L is released [F7]. With the fan running the well-mixed room is at about 1.9 % LFL at that moment, against a steady 5.0 % LFL [F8]. The rule is a firmware rule, so it does not share the independence of the comparator trip (R6); leaks below 2.7 L/min at the head give no warning and are not escalated [F8].

## G. Fan and duct system (R7)

- **Losses.** At 150 m3/h the duct velocity is 2.36 m/s; the exhaust side has a total loss coefficient of 3.44, and the make-up grille has 0.024 m2 of free area [G1]. The system needs 15.1 Pa at 150 m3/h and 60.5 Pa at 300 m3/h [G2].
- **TRL 2 fan fails the boost.** A 150 mm axial fan rated 300 m3/h in free air meets the losses at 237 m3/h, 7.9 air changes per hour, 21 % short of the boost target. A fan rated at the target flow in free air can never deliver it through a real duct [G3].
- **Re-specified fan.** A 150 mm mixed-flow EC fan of about 450 m3/h free air and 200 Pa shut-off gives 347 m3/h at full speed, 11.6 air changes per hour, 16 % above the boost target [G3]. The continuous 150 m3/h needs 43 % speed and about 3.8 W; boost takes about 36 W [G4]. At boost the room runs about 19 Pa below ambient across the make-up grille [G5], which a door undercut will relieve in practice. R7 stays at risk until a real fan curve is used.
- **Airflow proving (HGD-DEC-001, decision 6).** A differential pressure switch beside the fan has its low port tubed to a static tap in the fan inlet, just inside the grille, and its high port open to the room. The tap sees about 5.7 Pa at the continuous 150 m3/h and 30.5 Pa at full speed; with no flow, whatever the cause, it falls to about 0 Pa. A set point of 2.8 Pa, half the continuous value, is reached at about 106 m3/h [G6]. The switch must have a low range; the set point is confirmed when the switch is bought and by test at TRL 4. When the fan is running and the switch has not proved flow for 10 s, the microcontroller closes the valve and latches, as for a stopped fan [F6].

## H. Power (R11)

*Table 3. Power by state [H1].*

| State | Power |
| --- | --- |
| Normal (valve open, fan continuous, dry-contact relay held) | 13.5 W |
| Warning (valve open, fan boost, intermittent sounder) | 48.7 W |
| Trip (valve closed, fan boost, sounder and beacon; dry-contact relay released) | 40.3 W |

The peak of 48.7 W leaves a margin of 1.23 on the 60 W supply; the valve coil dissipates 8 W continuously, and the normal state uses 0.32 kWh per day [H2]. With the oxygen sensor option the peak is 49.2 W, margin 1.22 [H3]. The pressure switch draws no power. The TRL 2 figures (21 W normal, 29 W alarm) are replaced: normal falls because the larger fan runs slower, and the warning state now counts the valve and fan boost together.

## J. Bump test and log (R12)

- **Bump test.** Span gas at 1.0 L/min passes through 3.11 m of tube (15.3 mL, 0.9 s), now run across the ceiling to the head on its drop rod, into the 114 mL cup under the head, which five volumes flush in 34 s; with the arrestor and the assumed sensor t90 the reading settles after about 67 s, within the 120 s limit [J1]. Each test uses 1.36 L of span gas, so a 34 L disposable cylinder gives about 25 tests [J2]. The cup is open at the bottom, so the concentration the sensor sees is lower than the span gas by an unknown delivery factor; the pass level must be set when that factor is measured.
- **Trip during the test.** Span gas of 1 % vol equals the trip level, so a bump test that reaches full span trips the system. This proves the whole chain; the valve then needs a key reset. Amish decided on 2026-10-02 to keep the tripping test (HGD-DEC-001, decision 8). The pass level is set when the cup delivery factor is measured at TRL 4.
- **Log.** One 16 B record per minute for 90 days is 2.07 MB plus events, so the board needs 4 MB of flash or more [J3]. The BOM now says so.

## K. Alarm level (R10)

- A sounder of 90 dB at 1 m gives 80 dB at 3 m and 76 dB at 5 m in free field [K1]. The farthest point of the room is 5.0 m away, where the sounder is 16 dB above a 60 dB lab background [K2].

## L. Placement and ignition sources (R1, R15)

- The sensor ports are 175 mm below the ceiling (R1: 300 mm or less); the fan grille's top is 80 mm below it [L1].
- The controller's top is 1,025 mm below the ceiling (R15: 1,000 mm or more), the beacon's top 450 mm, and the power supply is on the floor [L2].
- The arrestor pore size of 50 µm or less is well below the maximum experimental safe gap for hydrogen, about 0.3 mm (IEC group IIC; value to be checked against IEC 60079-20-1). The catalytic element runs hot, and no part is rated for hazardous areas.

## M. Installation time (R13)

The estimate is 415 min (6.9 h) with both wall openings made on the day, and 300 min (5.0 h) if a builder makes them beforehand [M1]. The 206 mm core through the wall for the fan sleeve (90 min) and the make-up air opening (60 min) dominate. Under HGD-DDR-002 the fan and grille wall openings are builder's work outside the R13 target, so the 5.0 h figure applies: 60 min over the 4 h target on a judgment estimate, so R13 is not met on the estimate. The decisions of 2026-10-02 added 45 min: the ceiling drop rod (5 min more than the wall fixing), the pressure switch and its tube (15 min), 7 m more cable (20 min) and the ceiling clips for the test tube (5 min). The valve bracket added for construction (HGD-DDR-003) adds 10 min; the made parts (brackets, plates, the drilled boxes and the printed cup) are bench work before installation and are not counted.

## N. Cost (R14)

Value-engineering target: USD 265. Estimated cost of the constructable design: USD 411 (USD 146 over the target) [N1]. The target is `budget_usd`, a hypothetical control target, not a spending limit. The 21-line BOM has two priced options with quantity 0 that are not in the total: the oxygen sensor (line 20, USD 110) and the fan with its motor outside the air stream (line 21, USD 450, in place of line 9); with the oxygen sensor the kit is USD 521 [N3]. Without the fan and make-up grille (USD 63) the kit is USD 348 [N2], a different scope from the target. The decisions of 2026-10-02 added USD 122: the hydrogen-rated valve (USD 65 more), the pressure switch and tubing (USD 30), the ceiling drop rod (USD 11), the dry-contact relay and terminal (USD 6), the clear-lid controller box (USD 5) and more cable (USD 5). The TRL 3 changes added USD 15 (larger fan), USD 9 (bump test port and tube) and USD 1 (arrestor and cup) against the TRL 2 total of USD 239; the design for construction (HGD-DDR-003) added USD 25 more: the made brackets and plates (USD 14), the 200 mm wall sleeve (USD 5), standoffs, screws and epoxy (USD 4) and the cup's push-in fitting and tube clips (USD 2). The prices are indicative.

## P. Failure modes of the trip chain (R5, R6)

*Table 4. Failure modes and effects of the trip chain (first pass).*

| Failure | Effect | Detected by | Result |
| --- | --- | --- | --- |
| Loss of 24 V | Valve coil de-energized | Inherent | Safe: valve closes |
| Microcontroller stops | Valve MOSFET off or watchdog reset | 1 s watchdog | Safe: valve closes [F6] |
| Firmware bug holds valve MOSFET on | Comparator relay in series still opens at trip | Comparator | Safe for gas above the trip |
| Comparator relay contact welds | MOSFET in series still opens on firmware trip | Test button (proof test) | Safe while firmware runs; latent single fault |
| Valve MOSFET fails short | Comparator relay in series still opens | Test button | Safe; latent single fault |
| Sensor open or short, heater failure | Bridge outside the comparator window | Comparator | Safe: valve closes [F6] |
| Fan stops | No tachometer pulses; no airflow at the pressure switch | Controller, 10 s | Safe: valve closes [F6] |
| Duct blocked, shutter stuck, fan running | Tachometer still pulses; the fan inlet depression falls to about 0 Pa | Pressure switch, 10 s [G6] | Safe: valve closes [F6] |
| Pressure switch contact welds closed | Airflow shown as proved | Proof test: block the inlet tap at commissioning and at each bump test | Safe while the fan runs; latent single fault |
| Sensor poisoned (silicones, sulfur) | Reads low | Bump test only | **Dangerous, undetected** between tests |
| Port blocked (dust, paint, cap left on) | Reads low | Bump test only | **Dangerous, undetected** between tests |
| Valve seat leaks or sticks open | Supply not stopped | Not detected | **Dangerous, undetected**: covered by the valve's stated hydrogen rating and seat leak rate and by the seat leak proof test at TRL 4 |
| Dry-contact relay contact welds | H2Bench supply not cut by H2Guard | Test button (proof test) | H2Guard's own valve still closes; latent single fault |

R5's listed faults all close the valve within 2 s, and R6 holds because the comparator's relay sits in series with the microcontroller's valve switch. Three dangerous faults remain undetected in operation. Two (sensor poisoned, port blocked) are covered by the bump test before each session. The pressure switch (HGD-DEC-001, decision 6) moves the blocked duct and the stuck shutter from dangerous undetected to detected. The leaking valve seat stays a dangerous undetected fault: it is covered by the valve's stated hydrogen rating and seat leak rate (BOM line 11, decision 7) and by a seat leak proof test, which is TRL 4 work.

## Results against every requirement

*Table 5. Requirement status from this note.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R13 | Install simply | 5.0 h with the wall openings as builder's work; 6.9 h with them [M1] | 4 h, wall openings excluded (HGD-DDR-002) | **Not met on estimate** (60 min over; was at risk at v0.3) |
| R4 | Respond fast enough | 35.7 s leak to valve closed with t90 assumed 30 s; 0.17 s trip to closed [F3, F4] | t90 30 s or less; alarm 60 s; valve 2 s | **At risk** (t90 unconfirmed) |
| R7 | Ventilate the room | 347 m3/h boost, 150 m3/h continuous at 43 % speed; TRL 2 fan 237 m3/h [G3, G4] | 150 m3/h; boost 300 m3/h | **At risk** (fan curve assumed) |
| R1 | Measure at the high point | Ports 175 mm below the ceiling [L1], on the drop rod 0 mm from the apparatus centre, inside the 141 mm plume radius [E7]; 0 to 100 % LFL by selection | 0 to 100 % LFL, 1 % LFL resolution, within 0.3 m of the ceiling, directly above each likely leak point | **Not verifiable at TRL 3** (resolution needs sensor data); placement met on the drop rod (at v0.3 the wall position, 260 mm off, did not meet it) |
| R2 | Warn early | Design leak plume at the head 15 % LFL mean [E2] | Warn at 10 % LFL | Met on paper |
| R5 | Fail safe | 1.12 s worst listed fault to closed, airflow loss included [F6] | 2 s | Met on paper; three dangerous undetected faults (Table 4) |
| R8 | Keep the design leak below the trip | 5.0 % LFL well mixed and in the upper layer [D1, D3] | Below 10 % LFL | Met on paper |
| R10 | Alert people | 76 dB at 5 m, 16 dB over background [K2] | 85 dB(A) at 1 m; beacon visible | Met on paper |
| R11 | Keep mains out; 60 W or less | 48.7 W peak; 49.2 W with the oxygen sensor [H2, H3] | 60 W | Met on paper (the line 21 fan, if mains powered, is wired by an electrician through a certified contactor) |
| R12 | Be checkable in use | Bump test 67 s [J1]; log 2.07 MB in 4 MB [J3] | 2 min; 90 days | Met on paper (cup delivery factor unknown; pass level set at TRL 4) |
| R14 | Cost against the value-engineering target | USD 411 [N1] | USD 265 value-engineering target (`budget_usd`, HGD-DDR-002) | Over the value-engineering target by USD 146 (indicative prices) |
| R3 | Trip and shut off | Logic and latch; design leak 30 % LFL on the plume axis [E2]; off the axis the 5 min escalation closes the valve at 5.6 min [F7] | Trip at 25 % LFL or a warning held 5 min, key reset | Met by design (escalation is a firmware rule) |
| R6 | Trip without firmware | Comparator relay in series with the valve MOSFET, hardware latch | Independent of the microcontroller | Met by design |
| R9 | Limit what can leak | 300 L limit; H2Bench tank 2.6 % of it; 0.13 mm restrictor [B2 to B4] | 1 % of room volume or restrictor | Met by design (installation rule) |
| R15 | Avoid ignition sources in the ceiling layer | Controller 1,025 mm below the ceiling; continuous fan; 50 µm arrestors [L2] | 1 m; arrestors; continuous fan | Met by design; not certified |

Counts: 1 not met on estimate (R13), 2 at risk, 1 not verifiable at TRL 3, 6 met on paper, 4 met by design, and R14 over the value-engineering target by USD 146. At v0.3 they were 0 not met, 3 at risk (R13 among them) and R14 over the target by USD 24; R1's placement was recorded as met although the wall position did not meet it. At v0.2 R14 was met on paper (USD 264). At v0.1 they were 2 not met (R13, R14), 2 at risk, 1 not verifiable, 6 met on paper and 4 met by design.

## Checks against the TRL 2 figures

| TRL 2 claim (HGD-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| Electrolyzer about 0.4 L/min | 0.39 L/min | Stands |
| Layer to 25 % LFL about 7 min; room about 60 min | 7.2 min; 60 min | Stands |
| About 5 % LFL well mixed at 150 m3/h | 5.0 % LFL | Stands |
| Ceiling layer could be five times the room average and trip | At steady state the layer is at the exhaust value; the plume at the head is 15 to 30 % LFL | Precis updated |
| Transport to the head up to 5 s | 4.0 s | Stands |
| Leak to valve closed about 35 s | 35.7 s, but only with the arrestor changed; 55 s with the TRL 2 arrestor | Arrestor changed, precis updated |
| Fan about 300 m3/h free air meets the 300 m3/h boost | 237 m3/h | Fan re-specified, precis and BOM updated |
| About 3 L released; under 1 L in the line | 3.0 L; 0.47 L | Stands |
| Inventory limit 300 L, about 25 g; cylinder more than five times | 300 L, 25.1 g; 5.8 times | Stands |
| Power about 21 W normal, 29 W alarm | 13.5 W normal, 48.7 W warning, 40.3 W trip | Precis updated |
| Parts about $239 | $264.00 | Precis, README and BOM notes updated |
