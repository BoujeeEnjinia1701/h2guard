---
doc_id: HGD-PRB-001
title: H2Guard problem statement
project: H2Guard
doc_type: Problem statement
version: "0.7"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (problem, users, context, constraints, out of scope, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; open questions resolved by HGD-DDR-001 marked as adopted for TRL 3 pending Amish's review; cost figure from HGD-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); budget $265; resolved questions marked as decided
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Stronger sources
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Cost constraint restated against the value-engineering target after the design for construction (HGD-DDR-003)
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: O2 and O3 decided by Amish on 2026-10-02 (HGD-DEC-001)
---

# H2Guard problem statement

Small hydrogen setups in schools, university teaching labs, makerspaces and startups often have no gas detection or supply interlock, because commercial fixed detection systems are specified, priced and installed for industrial plants. H2Guard is an open, low-cost leak detector and ventilation interlock for one small room: it senses hydrogen at the ceiling, keeps the room ventilated, shuts the hydrogen supply when readings rise and fails safe when anything goes wrong. It is a research and teaching prototype, not a certified gas detection system.

## The problem

Hydrogen behaves differently from the gases most small labs are used to. It is flammable in air from about 4 % to 74 % by volume, and the energy needed to ignite it (about 0.02 mJ) is very low; it is also buoyant and diffuses quickly, so it escapes safely outdoors but collects under a ceiling in a poorly ventilated room ([US DOE hydrogen safety fact sheet](https://www1.eere.energy.gov/hydrogenandfuelcells/pdfs/h2_safety_fsheet.pdf)). It is invisible and odorless, so a person will not notice a leak.

Hydrogen use is spreading to smaller and less specialized users. Installed water electrolysis capacity reached about 2 GW in 2024 ([IEA, Global Hydrogen Review 2025](https://www.iea.org/reports/global-hydrogen-review-2025/executive-summary)), national programs are funding skills training (for example India's National Green Hydrogen Mission, [PIB, 2023](https://www.pib.gov.in/PressReleasePage.aspx?PRID=1888547)), and teaching benches such as the lab's own H2Bench put electrolyzers and fuel cells in ordinary classrooms.

Laboratory accidents show what happens when detection, grounding and supply control are missing. In March 2016 a hydrogen and oxygen gas mixture in an ungrounded 49 L tank exploded in a University of Hawaii lab; a postdoctoral researcher lost an arm, and the state regulator cited the university for 15 violations with $115,500 in fines ([C&EN, 2016](https://cen.acs.org/articles/94/web/2016/09/University-Hawaii-fined-115500-lab.html)), later settled at nine violations and $69,300 ([Honolulu Star-Advertiser, 2016](https://www.staradvertiser.com/2016/10/07/breaking-news/state-agrees-to-reduced-violations-fines-in-uh-lab-explosion/)). In May 2019 a hydrogen tank used by a fuel cell company at a technopark in Gangneung, South Korea, exploded, killing two people and injuring six ([Korea Herald, 2019](https://www.koreaherald.com/article/2006624)). An analysis of 576 statistically relevant events in the European hydrogen incident database found organizational and human factors in a large share of them ([Wen et al., 2022](https://www.sciencedirect.com/science/article/pii/S0360319922012976)), which argues for automatic safeguards that do not depend on a person noticing.

The gap for small users is threefold:

- **Cost and scale.** Fixed gas detection systems are sold as engineered packages for plants. A single certified hydrogen sensing element can cost about $249 on its own ([GasLab listing for the NevadaNano MPS sensor](https://gaslab.com/products/flammable-gas-sensor-nevada-nano-mps)), before the controller, valve, fan, alarm and installation.
- **Detection without action.** Where small labs do buy a detector, it is often a stand-alone alarm. Nothing closes the supply or increases ventilation, and nothing stops the gas flowing when the detector is unpowered or faulty.
- **No open reference.** There is no widely used open design that a teacher or a startup engineer can read, build, test and understand. Closed units hide their set points and failure behavior.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Secondary school or college science teacher | A detector and interlock for a hydrogen demonstration or H2Bench, which students can also learn from | Classroom or prep room, 20 to 60 m3, mains power, no gas engineer on site |
| University teaching lab technician | Protection for several student benches with small electrolyzers and fuel cells | Teaching lab with general ventilation, supervised sessions |
| Early-stage hydrogen startup | Interim protection for a small test room before a certified system is installed | Rented workshop or unit, small cylinders or electrolyzer output, limited budget |
| Makerspace or hackerspace | A clear rule set and hardware for members experimenting with electrolysis | Shared room, variable supervision |
| Analytical lab switching gas chromatography carrier gas to hydrogen | Room-level leak detection near a hydrogen generator | Existing lab, mechanical ventilation |
| Vocational trainer | A teaching unit for hydrogen safety: detection, set points, interlocks, bump tests | Training workshops for technicians |

## Operating environment

- Indoor room of about 20 to 60 m3 with a ceiling height of 2.4 to 3.5 m. The reference room for first-order numbers is 30 m3 (4 x 3 x 2.5 m).
- Hydrogen source: an electrolyzer of up to about 100 W, a metal hydride canister, or a small cylinder with a regulator and a flow restrictor. Pressure after the regulator 0 to 10 bar.
- Ambient 5 to 40 °C, 10 to 90 % relative humidity, non-condensing. Possible silicone, solvent or alcohol vapors from other lab work, which can poison or confuse some sensors.
- Mains power available (100 to 240 V, 50 or 60 Hz); outages possible.

## Constraints

- Garage-buildable prototype. Value-engineering target USD 265 (`project.yaml`, a hypothetical control target, not a limit), raised from USD 180 when Amish accepted the recommendation on 2026-09-25 (HGD-DDR-002). Estimated cost of the constructable design: USD 289, USD 24 over the target (HGD-CAL-001 v0.3).
- All self-built wiring is extra-low voltage (24 V DC). Mains is used only inside a certified power supply.
- Fail-safe by design: loss of power, a sensor fault or a controller fault must leave the hydrogen supply closed.
- Parts off the shelf where possible, with open firmware and published set points.
- Must not be presented as a certified gas detection system. It is a research and teaching prototype, and a real installation should use certified equipment.

## Out of scope

- Industrial or commercial installations, hydrogen refuelling stations, rooms classified as hazardous areas (ATEX or IECEx zones, NEC Class I divisions) and any use as the sole safeguard where a certified system is required.
- High-pressure storage indoors beyond the inventory limit proposed in the precis.
- Detection of other gases (oxygen depletion, carbon monoxide) except as a later option.
- Design of the gas system itself (regulator, tubing, flow restrictor), which belongs to the host project, for example H2Bench.

## Prior work

- **Standards.** ISO 26142:2010 covers performance of hydrogen detection apparatus for stationary applications ([ISO](https://www.iso.org/standard/52319.html)); it asks for a response time (t90) under 30 s, with alarms typically set at 25 % or 50 % of the lower flammability limit ([HySafe paper on sensor response time, 2017](https://hysafe.info/uploads/papers/2017/211.pdf)). NFPA 2, the Hydrogen Technologies Code, governs hydrogen installations in the United States ([NFPA](https://www.nfpa.org/product/nfpa-2-hydrogen-technologies-code/p0002code)). H2Guard uses these as design references only; it does not claim compliance.
- **Sensing elements.** Catalytic sensors burn the gas on a heated catalyst and read 0 to 100 % LFL; Figaro offers hydrogen-capable catalytic sensors such as the TGS6812 for stationary fuel cell leak detection ([Figaro, 2025](https://www.sensor-test.de/assets/Fairs/2025/ProductNews/PDFs/Figaro-Engineering-hydrogen-sensors-and-their-applications.pdf)). Metal oxide sensors such as the TGS2616 detect about 30 to 3,000 ppm hydrogen with reduced alcohol interference ([Figaro TGS2616-C00](https://www.figarosensor.com/product/docs/tgs2616-c00_product%20information(fusa)rev02.pdf)). Certified molecular property spectrometer sensors report 0 to 100 % LEL with t90 under 20 s and claim immunity to poisoning ([NevadaNano](https://nevadanano.com/mps-hydrogen-gas-sensor/)).
- **Incident learning.** The European HIAD 2.0 database and its analyses ([Wen et al., 2022](https://www.sciencedirect.com/science/article/pii/S0360319922012976)) and the University of Hawaii investigation ([UH report, 2016](http://www.hawaii.edu/news/wp-content/uploads/2016/07/Report-2-University-of-Hawaii.pdf)) supply the failure cases the concept is checked against.
- **Open designs.** A brief search found hobby hydrogen alarm projects built on single metal oxide sensors, but no documented open design that combines detection, ventilation and a fail-safe supply interlock. This has not been verified exhaustively.

## Open questions

Decided by Amish, 2026-09-25: go with recommendation (HGD-DDR-001 and HGD-DDR-002):

- First users: a university teaching lab first (D7).
- Sensor baseline: catalytic plus metal oxide pair, with the certified sensing element documented as the upgrade (D1).
- Inventory limit: 1 % of room volume at atmospheric pressure, or a flow restrictor, as a condition for H2Bench and other lab projects (D5).

Decided by Amish on 2026-10-02 (HGD-DEC-001):

- Oxygen depletion (O2): an oxygen sensor is added, as a standard kit option, whenever inert gas cylinders share the room.
- Set points and the inventory rule (O3): from the stricter of the national code and ISO 26142, and from the host institution's safety office where its rules are stricter; 10 % and 25 % LFL stay the defaults.
