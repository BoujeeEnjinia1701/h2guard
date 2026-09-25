"""H2Guard concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. The back wall of a small lab room lies in the XZ plane with its inside face
at Y = 0; equipment sits at negative Y. Ceiling height 2,600 mm, floor at Z = 0.
Grey parts are context (room, bench, gas cylinder, supply line, cable runs, person) and are not
in the BOM. Colored parts carry the BOM line number used in bom/bom.csv and the exploded view.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Sphere, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, human_figure, _render

ROOT = Path(__file__).resolve().parents[2]
CEIL = 2600.0
WALL_T = 100.0


def tube(a, b, r):
    """Round tube between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def path(points, r):
    s = None
    for p, q in zip(points, points[1:]):
        t = tube(p, q, r)
        s = t if s is None else s + t
    return s


# ---------------- context (grey, no BOM number) ----------------
back_wall = Pos(1800, WALL_T / 2, CEIL / 2) * Box(3600, WALL_T, CEIL)
side_wall = Pos(-WALL_T / 2, -800 + WALL_T / 2, CEIL / 2) * Box(WALL_T, 1600 + WALL_T, CEIL)
floor = Pos(1800, -800, -15) * Box(3600, 1600, 30)
outlet = Pos(2980, -12, 320) * Box(80, 24, 120)                     # mains outlet
room = back_wall + side_wall + floor + outlet

bench = Pos(1900, -325, 880) * Box(1200, 650, 40)
for bx in (1340, 2460):
    for by in (-620, -30):
        bench = bench + Pos(bx, by, 430) * Box(40, 40, 860)
apparatus = Pos(1625, -300, 1025) * Box(350, 300, 250)             # e.g. a small electrolyzer or fuel cell rig
bench = bench + apparatus

CYL = (650.0, -170.0)                                              # small hydrogen cylinder with regulator
cylinder = (Pos(CYL[0], CYL[1], 450) * Cylinder(90, 900) + Pos(CYL[0], CYL[1], 900) * Sphere(90)
            + Pos(CYL[0], CYL[1], 1010) * Cylinder(18, 60) + Pos(CYL[0], CYL[1], 1060) * Box(70, 60, 50)
            + Pos(CYL[0], -45, 700) * Box(200, 90, 20))            # wall restraint strap

supply = path([(CYL[0], CYL[1], 1085), (CYL[0], CYL[1], 1300), (1600, CYL[1], 1300),
               (1600, -300, 1300), (1600, -300, 1150)], 6)

# ---------------- H2Guard parts ----------------
# 1 Detector head enclosure, 110 x 80 x 90 mm, on the wall directly above the source, top 85 mm below the ceiling
HX, HZ = 1625.0, 2470.0
head_c = (HX, -40.0, HZ)
head = Pos(*head_c) * (Box(110, 80, 90) - Box(104, 74, 84))
for dx in (-22, 22):
    head = head - Pos(HX + dx, -40, HZ - 44) * Cylinder(13, 12)    # two sensor ports in the floor of the box
head = head + Pos(HX, -40, HZ + 50) * Box(40, 80, 10)              # cable gland boss
# 2 Catalytic hydrogen sensor on a carrier board, over the left port
cat = Pos(HX - 22, -40, HZ - 32) * Cylinder(10, 17) + Pos(HX, -40, HZ - 20) * Box(96, 66, 2)
# 3 MOS early-warning hydrogen sensor over the right port
mos = Pos(HX + 22, -40, HZ - 36) * Cylinder(4.6, 8) + Pos(HX + 22, -40, HZ - 31) * Cylinder(6, 2)
# 4 Sintered stainless flame arrestor discs in both ports, plus a drip skirt
arrest = (Pos(HX - 22, -40, HZ - 44) * Cylinder(12.5, 5) + Pos(HX + 22, -40, HZ - 44) * Cylinder(12.5, 5)
          + Pos(HX, -40, HZ - 52) * (Box(116, 86, 12) - Box(108, 78, 14)))

# 5 to 7 Controller at chest height, well below the ceiling layer
CX, CZ = 2760.0, 1400.0
ctrl_body = Pos(CX, -47, CZ) * (Box(200, 90, 250) - Pos(0, -3, 0) * Box(192, 88, 242))
board = (Pos(CX, -8, CZ) * Box(176, 3, 220)
         + Pos(CX - 50, -18, CZ + 60) * Box(40, 18, 40)                    # MCU module
         + Pos(CX + 40, -24, CZ + 50) * Box(28, 30, 20) + Pos(CX + 40, -24, CZ + 10) * Box(28, 30, 20)  # relay and driver blocks
         + Pos(CX, -16, CZ - 90) * Box(150, 14, 18))                       # terminal strip
panel = (Pos(CX, -94, CZ) * Box(200, 4, 250)
         + Pos(CX, -98, CZ + 60) * Box(90, 4, 45)                          # display
         + Pos(CX - 50, -104, CZ - 40) * Rot(90, 0, 0) * Cylinder(12, 16)  # key-switch reset
         + Pos(CX + 10, -100, CZ - 40) * Rot(90, 0, 0) * Cylinder(9, 8)    # test button
         + Pos(CX + 55, -100, CZ - 40) * Box(40, 6, 12))                   # status LEDs
# 8 Certified 24 V DC power supply brick on the floor next to the outlet
psu = Pos(2850, -110, 20) * Box(160, 70, 40)
# 9 Exhaust fan: grille on the inside face at high level, 150 mm fan housing through the wall
FX, FZ = 2200.0, 2400.0
fan = (Pos(FX, -6, FZ) * Box(240, 12, 240) - Pos(FX, -6, FZ) * Rot(90, 0, 0) * Cylinder(80, 14)
       + Pos(FX, WALL_T / 2 + 20, FZ) * Rot(90, 0, 0) * Cylinder(90, WALL_T + 40)
       + Pos(FX, -4, FZ) * Rot(90, 0, 0) * Cylinder(30, 8))
# 10 Low-level make-up air grille, far side of the room
inlet = Pos(300, -6, 180) * Box(300, 12, 160)
# 11 Normally closed solenoid valve on the supply line (energize to open)
VX = 950.0
valve = (Pos(VX, CYL[1], 1300) * Box(60, 45, 45) + Pos(VX, CYL[1], 1352) * Cylinder(22, 60)
         + Pos(VX, CYL[1], 1392) * Box(30, 30, 20))
# 12 Sounder and beacon, high on the wall near the room door
BX, BZ = 3060.0, 2150.0
beacon = (Pos(BX, -25, BZ) * Box(100, 50, 100) + Pos(BX, -80, BZ) * Rot(90, 0, 0) * Cylinder(38, 60)
          + Pos(BX, -110, BZ) * Sphere(38))

# Cable runs (context): trunk under the ceiling, drops to each device, then down to the controller
TR = 2560.0
cables = (path([(VX, -10, 1415), (VX, -10, TR), (2700, -10, TR), (2700, -10, CZ + 125)], 5)
          + path([(HX, -10, HZ + 55), (HX, -10, TR)], 5)
          + path([(FX, -10, FZ + 120), (FX, -10, TR)], 5)
          + path([(BX - 50, -10, BZ), (2700, -10, BZ)], 5)
          + path([(VX, CYL[1] + 20, 1400), (VX, -10, 1415)], 5)
          + path([(2850, -110, 40), (2850, -60, 120), (2850, -60, CZ - 125)], 4)
          + path([(2930, -110, 20), (2980, -30, 300)], 4))

ORANGE, TEAL = "#C2410C", "#0F766E"
parts = [
    Part("Detector head enclosure", head, "#F59E0B", 1),
    Part("Catalytic H2 sensor, 0 to 100 % LFL", cat, TEAL, 2),
    Part("MOS H2 sensor, early warning", mos, "#0EA5E9", 3),
    Part("Flame arrestor discs and drip skirt", arrest, "#94A3B8", 4),
    Part("Controller enclosure", ctrl_body, "#D1D5DB", 5),
    Part("Controller board, independent trip", board, "#115E59", 6),
    Part("Front panel: display, key reset, test", panel, "#374151", 7),
    Part("24 V DC supply, certified", psu, "#1F2937", 8),
    Part("Exhaust fan, 150 mm, high level", fan, "#2563EB", 9),
    Part("Make-up air grille, low level", inlet, "#93C5FD", 10),
    Part("NC solenoid valve, 24 V DC", valve, "#D4A017", 11),
    Part("Sounder and beacon", beacon, "#DC2626", 12),
]

# Exploded view: a compact kit-of-parts layout (targets are part centers, mm)
targets = {
    1: (150, -40, 1150), 2: (110, -40, 1040), 3: (190, -40, 1040), 4: (150, -40, 950),
    12: (150, -120, 720), 8: (150, -150, 480), 11: (150, -120, 250),
    5: (650, -47, 900), 6: (650, -260, 900), 7: (650, -470, 900),
    9: (650, -40, 470), 10: (650, -40, 170),
}
for p in parts:
    c = p.shape.bounding_box().center()
    tx, ty, tz = targets[p.bom]
    p.explode = (tx - c.X, ty - c.Y, tz - c.Z)

context = [
    human_figure(1750, x=3450, y=-420, z=0),
    Part("Room, bench and test apparatus (context)", room + bench, "#E5E7EB"),
    Part("Hydrogen cylinder, regulator and supply line (context)", cylinder + supply, "#9CA3AF"),
    Part("Cable runs (context)", cables, "#6B7280"),
]

flow = {
    "title": "detect, decide, act chain for the design leak (estimates, 30 m3 room)",
    "stages": [("Leak at the source", "5 L/min H2\n(design case)"),
               ("Rises to ceiling layer", "1 % vol in about 7 min\nif unventilated (est.)"),
               ("Detector head", "t90 30 s or less\n(target, unverified)"),
               ("Controller trip", "at 25 % LFL, latched;\nunder 1 s (est.)"),
               ("NC valve closes", "under 1 s; supply\nstopped (est.)"),
               ("Fan on boost", "300 m3/h, 10 air\nchanges per hour (est.)")],
}

KEY_FIGURES = ["Warn at 10 % LFL (0.4 % vol H2); trip at 25 % LFL (1.0 % vol)",
               "Leak to valve closed about 35 s (estimate)",
               "Exhaust 150 m3/h continuous, 300 m3/h boost (30 m3 room)",
               "Fail-safe: NC valve closes on power loss, fault or fan failure",
               "24 V DC build; mains only inside a certified supply",
               "Parts about $240 (indicative); budget $180"]

render_all(
    parts, project="H2Guard", title="Leak detector and interlock concept", dwg_no="HGD-DWG-010",
    key_figures=KEY_FIGURES,
    date="2026-09-25", cut=False, scale_figure=False, context=context, flow=flow,
)

# Hero again with a clearer note (the kit lists context part names, which is long here)
_render(parts + context, ROOT / "media" / "hero.png", title="H2Guard",
        note="Grey figure: 1.75 m person for scale. Grey room, bench, gas cylinder, supply line and cable runs are context, not in the BOM.")

# Blueprint again with the room, bench and cylinder in the orthographic views, so the device heights
# (fan and head under the ceiling, make-up air low, controller at chest height) read against the room.
from build123d import Compound
from drawing import Sheet, project_views
room_ctx = [c for c in context if not c.name.startswith("Person")]
md = ROOT / "media"
views = project_views(Compound(children=[p.shape for p in parts + room_ctx]), md / "_views")
views["iso"] = project_views(Compound(children=[p.shape for p in parts + context]), md / "_views_fig")["iso"]
sheet = Sheet(project="H2Guard", title="Leak detector and interlock concept", dwg_no="HGD-DWG-010", rev="P1",
              author="Amish Chadha", date="2026-09-25", theme="blueprint",
              material="Massing model for concept communication; room, bench and cylinder are context",
              revisions=[("P1", "Concept sheet", "2026-09-25", "AC")])
sheet.add_ortho(views)
sheet.add_svg(views["iso"], 276, 32, 140, 118, label="Isometric view",
              sublabel="Not to scale; figure is a 1.75 m person")
sheet.add_notes("Key figures", KEY_FIGURES, x=276, y=168, width=140)
sheet.save(md / "concept-blueprint")

# Cutaway: detector head and controller, each cut on a vertical plane normal to X and seen from -X.
# The head is moved beside the controller for this view; the cut passes through the catalytic sensor
# and through the controller's MCU module.
def cut_x(shape, x0):
    bb = shape.bounding_box()
    big = 4 * max(bb.size.X, bb.size.Y, bb.size.Z) + 10
    c = bb.center()
    return shape & (Pos(x0 + big / 2, c.Y, c.Z) * Box(big, big, big))


near = []
for p in parts:
    if p.bom in (1, 2, 4):
        sh = cut_x(p.shape, HX - 22)
        near.append(Part(p.name, Pos(CX - HX, -330, CZ + 60 - HZ) * sh, p.color, p.bom))
    elif p.bom in (5, 6, 7):
        near.append(Part(p.name, cut_x(p.shape, CX - 50), p.color, p.bom))
_render(near, ROOT / "media" / "cutaway.png", azim=180, elev=15, labels=True,
        title="H2Guard: section through detector head (right) and controller (left)",
        note="Head shown beside the controller; installed just under the ceiling. MOS sensor (3) is behind the cut plane.")

# Clean up renderer scratch folders
import shutil
for d in (ROOT / "media").glob("_views*"):
    shutil.rmtree(d, ignore_errors=True)
