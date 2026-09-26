# H2Guard

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Hydrogen · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $265 USD · **Difficulty:** 3 of 5

A hydrogen leak detector and ventilation interlock for small labs, workshops and electrolyzer rooms: it senses hydrogen near the ceiling, runs a fan and cuts the supply when readings rise.

![H2Guard concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement HGD-DWG-001 (PDF)](cad/drawings/HGD-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Detection, ventilation and automatic shutoff form the basic safety chain for any room where hydrogen is used, and each link has to work when the others fail. H2Guard puts that chain in one small kit: a ceiling detector head with a catalytic sensor for the trip and a metal oxide sensor for early warning, a continuously running exhaust fan, and a normally closed valve that holds the supply open only while the controller, the sensors and the fan are all healthy. A hardware comparator can close the valve without the firmware, so a software bug cannot keep gas flowing.

It is open and garage-buildable because the people now starting to use hydrogen, teachers, technicians and small startups, need to see how a safety system decides, not just trust a sealed box. Every set point and failure response is written down, the self-built parts run on 24 V DC from a certified supply, and the parts are off the shelf. It is a teaching and research prototype, not a certified gas detection system, and the documents say where it falls short of one.

## Burning platform

Hydrogen is moving into classrooms, startups and small labs faster than safe practice is reaching them. Installed water electrolysis capacity reached about 2 GW in 2024, with more than 1 GW added in the first seven months of 2025 ([IEA, Global Hydrogen Review 2025](https://www.iea.org/reports/global-hydrogen-review-2025/executive-summary)). The gas is flammable in air from about 4 % to 74 % by volume, ignites with about 0.02 mJ, and collects under ceilings in poorly ventilated rooms ([US DOE](https://www1.eere.energy.gov/hydrogenandfuelcells/pdfs/h2_safety_fsheet.pdf)).

Small-scale accidents show the cost of missing safeguards. In 2016 a hydrogen and oxygen mixture exploded in a University of Hawaii lab, costing a researcher an arm and the university a $115,500 fine for 15 violations ([C&EN](https://cen.acs.org/articles/94/web/2016/09/University-Hawaii-fined-115500-lab.html)). In 2019 a hydrogen tank used by a fuel cell company at a technopark in Gangneung, South Korea, exploded, killing two people and injuring six ([Korea Herald](https://www.koreaherald.com/article/2006624)). An analysis of the European HIAD 2.0 incident database found organizational factors in about half of the relevant events ([Wen et al., 2022](https://www.sciencedirect.com/science/article/pii/S0360319922012976)), which is the case for safeguards that act automatically.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Education | Protection and teaching aid for school and university hydrogen demonstrations, including the lab's H2Bench |
| Hydrogen and fuel cell startups | Interim protection for a small test room before a certified system is installed |
| Analytical laboratories | Room-level leak detection near hydrogen generators used as gas chromatography carrier gas |
| Materials handling and backup power | Monitoring battery charging rooms, where US rules require ventilation for gases from charging batteries ([OSHA 1910.178(g)(2)](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.178)), and small fuel cell backup rooms |
| Vocational training | Hands-on teaching of set points, interlocks and bump testing for hydrogen technicians |
| Makerspaces | A clear rule set and hardware for members experimenting with electrolysis |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| United States | The 2016 University of Hawaii explosion led to 15 violations and a $115,500 fine ([C&EN](https://cen.acs.org/articles/94/web/2016/09/University-Hawaii-fined-115500-lab.html)); many teaching labs handle small gas quantities without fixed detection |
| South Korea | A hydrogen tank explosion at a Gangneung technopark in 2019 killed two visitors from venture businesses and research groups ([Korea Herald](https://www.koreaherald.com/article/2006624)) |
| European Union | The EU hydrogen strategy aims for at least 40 GW of renewable hydrogen electrolyzers by 2030 ([European Commission, COM(2020) 301](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52020DC0301)), which needs many trained technicians |
| China | Holds 65 % of the world's installed and committed electrolyzer capacity ([IEA](https://www.iea.org/reports/global-hydrogen-review-2025/executive-summary)), with a large and growing training need |
| India | The National Green Hydrogen Mission targets at least 5 Mt per year of green hydrogen by 2030 and includes a skills program ([PIB, 2023](https://www.pib.gov.in/PressReleasePage.aspx?PRID=1888547)); colleges and startups need low-cost lab safety |
| Namibia and southern Africa | Namibia runs a national green hydrogen program ([Namibia Green Hydrogen Programme](https://gh2namibia.com/)); local colleges training for it may lack budgets for industrial detection |

## What sparked the idea

The idea traces back to the New London School explosion in Texas on March 18, 1937. Gas from a faulty connection on a cheap residue gas line collected unnoticed in a nearly closed space beneath the school and exploded, killing about 298 students and teachers; the most important result was a state law requiring a distinctive malodorant in commercial and industrial gas so that people could smell a leak ([Texas State Historical Association, Handbook of Texas](https://www.tshaonline.org/handbook/entries/new-london-school-explosion)). That fix does not carry over to hydrogen. It is colorless and odorless, and there are no known odorants light enough to travel with it, so by the time an odorant could be smelled the gas may already be above its flammability limit ([OSHA](https://www.osha.gov/green-jobs/hydrogen/fire-explosion)). A room that uses hydrogen therefore needs what the nose cannot give it: an electronic detector at the ceiling, where the gas collects, tied to ventilation and a valve that shuts the supply without waiting for a person to notice. H2Guard is that chain, sized for the classrooms and small labs now taking up hydrogen.

## Problem

Small hydrogen setups in schools and startups often have no gas detection or interlock because commercial systems are priced for industrial plants.

Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

A detector head at the ceiling above the hydrogen source measures 0 to 100 % of the lower flammability limit (LFL). A wall controller keeps an exhaust fan running and holds a normally closed valve on the supply open. At 10 % LFL it warns and boosts the fan; at 25 % LFL it closes the valve, sounds the alarm and latches until a key reset. Power loss, sensor faults, a stopped fan or a crashed controller also close the valve, and a hardware comparator trip works without the firmware. The TRL 3 calculations give 35.7 s from a 5 L/min leak to the valve closing (with an assumed 30 s sensor response), and about 5 % LFL in the 30 m3 reference room with the fan running. They also show that the design leak trips the system at once only if the detector head is on the plume axis above the leak. Two rules accepted by Amish cover the rest: a warning held for 5 min also closes the valve (about 5.6 min for the design leak off the axis), and a head goes directly above each likely leak point.

Full design precis: [docs/02-concept.md](docs/02-concept.md) · Requirements: [docs/03-requirements.md](docs/03-requirements.md) · Calculations: [docs/04-calcs/01-sizing.md](docs/04-calcs/01-sizing.md) · Decisions: [DDR-001](docs/decisions/0001-trl2-review-decisions.md), [DDR-002](docs/decisions/0002-recommendations-accepted.md)

## Key components

- Detector head with a catalytic hydrogen sensor (0 to 100 % LFL) and a metal oxide early-warning sensor, behind thin sintered flame arrestors, with a drip skirt that doubles as a bump test cup
- Controller with an independent hardware trip (latched comparator and series relay), display, key-switch reset, event log and a bump test gas port
- Certified 24 V DC power supply
- 150 mm mixed-flow exhaust fan at high level, running continuously, and a low-level make-up air grille
- Normally closed 24 V DC solenoid valve on the supply
- Sounder and beacon

The priced bill of materials is in [bom/bom.csv](bom/bom.csv). Parts come to $264 (indicative prices), within the $265 budget that Amish set on 2026-09-25 when he accepted the review recommendations; see the [review note](docs/REVIEW.md). The parametric model is `cad/src/model.py`, with STEP and STL exports in `cad/step/` and `cad/stl/`.

## Safety

> Hydrogen is flammable in air from about 4 % to 74 % by volume. This is a research and teaching prototype and not a certified gas detection system; use certified equipment for any real installation. Its parts are not rated for hazardous areas. It protects only against small, flow-limited leaks; keep hydrogen inventories small, and have gas fittings made and leak-tested by a competent person. Mains power enters only through a certified supply.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (HGD-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `HGD-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
