"""H2Guard concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Main dimensions and interfaces only; not for fabrication.

Coordinates as in model.py: back wall inside face at Y = 0, room toward negative Y, side wall
inside face at X = 0, floor at Z = 0, ceiling at 2,500 mm. Grey parts are context (room,
bench, gas store, supply line, cable runs, bump test tube, person) and are not in the BOM
except where noted. Colored parts carry the BOM line number used in bom/bom.csv.
Figures quoted on the media come from docs/04-calcs/sizing.py (HGD-CAL-001).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Pos, Compound  # noqa: E402
from concept import Part, render_all, human_figure, _render  # noqa: E402
from model import PARAMS as P, build_parts, context, bump_kit, derived  # noqa: E402

D = derived(P)
from model import build_components  # noqa: E402
CC = build_components(P)
S = build_parts(P, comps=CC)
C = context(P)
port, run = bump_kit(P, comps=CC)

TEAL = "#0F766E"
spec = [("head", "Detector head enclosure", "#F59E0B", 1),
        ("cat", "Catalytic H2 sensor, 0 to 100 % LFL", TEAL, 2),
        ("mos", "MOS H2 sensor, early warning", "#0EA5E9", 3),
        ("arrest", "Flame arrestors and bump test cup", "#94A3B8", 4),
        ("ctrl", "Controller enclosure", "#D1D5DB", 5),
        ("board", "Controller board, series trip relay", "#115E59", 6),
        ("panel", "Front panel: display, key reset, test", "#374151", 7),
        ("psu", "24 V DC supply, certified", "#1F2937", 8),
        ("fan", "Exhaust fan, 150 mm mixed flow", "#2563EB", 9),
        ("inlet", "Make-up air grille, low level", "#93C5FD", 10),
        ("valve", "NC solenoid valve, 24 V DC", "#D4A017", 11),
        ("beacon", "Sounder and beacon", "#DC2626", 12)]
parts = [Part(name, S[key], color, bom) for key, name, color, bom in spec]
parts.append(Part("Bump test port (tube shown grey)", port, "#7C3AED", 15))

# Exploded view: a compact kit-of-parts layout (targets are part centers, mm)
targets = {
    1: (150, -40, 1150), 2: (80, -40, 1030), 3: (220, -40, 1030), 4: (150, -40, 920),
    12: (150, -120, 700), 8: (150, -150, 470), 11: (150, -120, 250),
    5: (650, -47, 900), 6: (650, -260, 900), 7: (650, -470, 900), 15: (380, -700, 1150),
    9: (700, -40, 470), 10: (700, -40, 150),
}
for p in parts:
    c = p.shape.bounding_box().center()
    tx, ty, tz = targets[p.bom]
    p.explode = (tx - c.X, ty - c.Y, tz - c.Z)

ctx = [
    human_figure(1750, x=2900, y=-2000, z=0),
    Part("Room, bench and test apparatus (context)", C["room"] + C["bench"], "#E5E7EB"),
    Part("Gas store with regulator and restrictor, supply line (context)", C["store"], "#9CA3AF"),
    Part("Cable runs and bump test tube (context)", C["cables"] + run, "#6B7280"),
]

R = {}
for line in (ROOT / "docs" / "04-calcs" / "results.txt").read_text().splitlines():
    R[line[1:line.index("]")]] = line
flow = {
    "title": "detect, decide, act chain for the design leak (HGD-CAL-001 estimates, 30 m3 room)",
    "stages": [("Leak at the source", "5 L/min H2\n(design case)"),
               ("Plume to the head", "4.0 s; 15 % LFL mean,\n30 % on axis (est.)"),
               ("Arrestor and sensor", "1.5 s + t90 30 s\n(t90 assumed)"),
               ("Comparator trip", "at 25 % LFL, latched\nin hardware; 0.05 s"),
               ("NC valve closes", "0.17 s trip to closed;\n35.7 s from leak (est.)"),
               ("Fan on boost", "347 m3/h, 11.6 air\nchanges per hour (est.)")],
}

KEY_FIGURES = ["Warn at 10 % LFL (0.4 % vol H2); trip at 25 % LFL (1.0 % vol)",
               "Leak to valve closed 35.7 s with t90 30 s assumed (HGD-CAL-001)",
               "Exhaust 150 m3/h continuous, 347 m3/h boost; room 5 % LFL",
               "Fail-safe: NC valve, series hardware trip relay, 1 s watchdog",
               "24 V DC build; mains only inside a certified supply",
               "Warning held 5 min also closes the valve (DDR-002)",
               "Estimated cost USD 289; value-engineering target USD 265"]

render_all(
    parts, project="H2Guard", title="Leak detector and interlock concept", dwg_no="HGD-DWG-010",
    key_figures=KEY_FIGURES, date="2026-10-01", cut=False, scale_figure=False, context=ctx, flow=flow,
)

# Hero again with a clearer note (the kit lists every context part name, which is long here)
_render(parts + ctx, ROOT / "media" / "hero.png", title="H2Guard",
        note="Grey figure: 1.75 m person for scale. Grey room, bench, gas store, supply line, cables and bump test tube are context.")

# Blueprint again with the room, bench and store in the orthographic views, so the device heights
# (fan and head under the ceiling, make-up air low, controller at chest height) read against the room.
from drawing import Sheet, project_views  # noqa: E402
room_ctx = [c for c in ctx if not c.name.startswith("Person")]
md = ROOT / "media"
views = project_views(Compound(children=[p.shape for p in parts + room_ctx]), md / "_views")
views["iso"] = project_views(Compound(children=[p.shape for p in parts + ctx]), md / "_views_fig")["iso"]
sheet = Sheet(project="H2Guard", title="Leak detector and interlock concept", dwg_no="HGD-DWG-010", rev="P4",
              author="Amish Chadha", date="2026-10-01", theme="blueprint",
              material="Built from cad/src/model.py; room, bench and gas store are context. GA is HGD-DWG-001",
              revisions=[("P1", "Concept sheet", "2026-09-25", "AC"), ("P2", "From the TRL 3 parametric model", "2026-09-25", "AC"),
                         ("P3", "Key figures after DDR-002", "2026-09-25", "AC"),
                         ("P4", "Constructable design (DDR-003)", "2026-10-01", "AC")])
sheet.add_ortho(views)
sheet.add_svg(views["iso"], 276, 32, 140, 118, label="Isometric view",
              sublabel="Not to scale; figure is a 1.75 m person")
sheet.add_notes("Key figures", KEY_FIGURES, x=276, y=168, width=140)
sheet.save(md / "concept-blueprint")


# Cutaway: detector head and controller, each cut on a vertical plane normal to X and seen from -X.
# The kit's cutaway_parts cuts near the origin only, so the cut is done here. The head is moved
# beside the controller for this view; the cut passes through the catalytic sensor and the MCU module.
def cut_x(shape, x0):
    bb = shape.bounding_box()
    big = 4 * max(bb.size.X, bb.size.Y, bb.size.Z) + 10
    c = bb.center()
    return shape & (Pos(x0 + big / 2, c.Y, c.Z) * Box(big, big, big))


HX, HZ = P["app_x"], D["head_z"]
CX, CZ = P["ctrl_x"], P["ctrl_z"]
near = []
for p in parts:
    if p.bom in (1, 2, 4):
        sh = cut_x(p.shape, HX - P["port_dx"])
        near.append(Part(p.name, Pos(CX - HX, -330, CZ + 60 - HZ) * sh, p.color, p.bom))
    elif p.bom in (5, 6, 7):
        near.append(Part(p.name, cut_x(p.shape, CX - 50), p.color, p.bom))
_render(near, md / "cutaway.png", azim=180, elev=15, labels=True,
        title="H2Guard: section through detector head (right) and controller (left)",
        note="Head shown beside the controller; installed with its ports 175 mm below the ceiling. MOS sensor (3) is behind the cut plane.")

for d in md.glob("_views*"):
    shutil.rmtree(d, ignore_errors=True)
print("media refreshed")
