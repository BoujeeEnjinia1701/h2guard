# H2Guard

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Hydrogen · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $180 USD · **Difficulty:** 3 of 5

A hydrogen leak detector and ventilation interlock for small labs, workshops and electrolyzer rooms: it senses hydrogen near the ceiling, runs a fan and cuts the supply when readings rise.

## Concept rationale

Detection plus automatic ventilation and shutoff is the basic safety chain for any hydrogen space; making it open and cheap removes a barrier to learning with hydrogen safely.

## Burning platform

Hydrogen is being promoted for teaching and small-scale use faster than safe practice is spreading to the people handling it.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. The hydrogen economy is a Design Molecule research area with no open project yet; safety comes before any rig.

## Problem

Small hydrogen setups in schools and startups often have no gas detection or interlock because commercial systems are priced for industrial plants.

## Concept

A hydrogen leak detector and ventilation interlock for small labs, workshops and electrolyzer rooms: it senses hydrogen near the ceiling, runs a fan and cuts the supply when readings rise.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Catalytic or thermal conductivity hydrogen sensor
- Controller with relay outputs
- Ventilation fan, spark-free
- Normally closed solenoid valve on the supply
- Alarm sounder and beacon
- Wall enclosure

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Hydrogen is flammable across a wide concentration range. This is a research prototype and not a certified gas detection system; use certified equipment for any real installation.

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

A project of the [Design Molecule](https://designmolecule.com) lab. Gap-filling areas set.
