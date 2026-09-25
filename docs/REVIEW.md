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
