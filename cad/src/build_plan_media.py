"""H2Guard prototype build plan pictures (HGD-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
With no argument it draws everything. A single picture can be drawn with, for example,
"steps:4" or "sheets:103" or "joints:2", which keeps memory low. Every picture is drawn from
cad/src/model.py (build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/HGD-DWG-101 to 110        making sketches for the made and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, context, box, ycyl, xcyl, zcyl  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
DATE2 = "2026-10-02"
D = derived(P)
C = build_components(P)

COL = {"head_body": "#F59E0B", "discs": "#64748B", "standoffs": "#A16207", "cup": "#94A3B8", "sensor_board": "#0F766E",
       "head_lid": "#FCD34D", "ctrl_body": "#D1D5DB", "ctrl_glands": "#1F2937", "mplate": "#94A3B8", "modules": "#115E59",
       "ctrl_lid": "#E5E7EB", "panel_parts": "#374151", "test_bracket": "#1D4ED8", "test_port": "#7C3AED",
       "fan_plate": "#0E7490", "fan": "#2563EB", "sleeve": "#9CA3AF", "grille": "#E5E7EB", "hood": "#6B7280",
       "inlet": "#93C5FD", "valve_bracket": "#B45309", "valve": "#D4A017", "beacon": "#DC2626", "psu": "#1F2937",
       "tube": "#7C3AED", "bolt": "#111827", "wall": "#E7E5E4", "drop": "#78716C", "dps": "#0891B2", "o2": "#65A30D",
       "dry_relay": "#1E3A8A"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


S = lambda *ks: _fuse([C[k] for k in ks])  # noqa: E731


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def win(sh, x0, x1, y0, y1, z0, z1):
    import build123d as b
    r = sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))
    return r


def wall_patch(x0, x1, z0, z1, t=20):
    """A piece of the back wall for orientation (its room face at Y = 0)."""
    return part("Wall", box((x0 + x1) / 2, t / 2, (z0 + z1) / 2, x1 - x0, t, z1 - z0), COL["wall"])


HX, HY, HZ = P["app_x"], P["head_y"], D["head_z"]
CX, CZ = P["ctrl_x"], P["ctrl_z"]
FX, FZ = P["fan_x"], P["fan_z"]
TX, TZ = P["test_x"], P["test_z"]
VX, VY, VZ = P["valve_x"], P["store_y"], P["supply_z"]


# ----------------------------------------------------------------- named parts, in build order
def short_tube():
    """The tube drawn short for the overview, with its eight clips in a row."""
    import build123d as b
    t = xcyl(0, 0, 0, 2, 340)
    clips = _fuse(b.Pos(-140 + 40 * i, 0, -12) * (box(0, 0, 0, 8, 6, 10) - xcyl(0, 0, 0, 2, 10)) for i in range(8))
    return t + clips


def made():
    import build123d as b
    inlet = b.Pos(0, 0, 0) * b.Rot(0, 0, 90) * b.Pos(-6, -P["inlet_y"], -P["inlet_z"]) * C["inlet"]
    return [
        part("Detector head box, drilled", C["head_body"], COL["head_body"]),
        part("Flame arrestor discs (2)", C["discs"], COL["discs"]),
        part("Standoffs and M3 screws (4 + 8)", S("standoffs", "cup_screws", "board_screws"), COL["standoffs"]),
        part("Bump test cup, printed, with push-in fitting", S("cup", "cup_fitting"), COL["cup"]),
        part("Sensor board with both sensors", S("sensor_board", "cat", "mos"), COL["sensor_board"]),
        part("Head lid and cable gland", S("head_lid", "head_gland"), COL["head_lid"]),
        part("Ceiling drop rod: flange, pipe, locknuts", S("drop_flange", "drop_rod", "drop_nuts", "drop_screws"), COL["drop"]),
        part("Controller box, drilled, with 8 glands", S("ctrl_body", "ctrl_glands"), COL["ctrl_body"]),
        part("Controller mounting plate", S("mplate", "mplate_screws"), COL["mplate"]),
        part("Controller modules, dry-contact relay, terminals", S("modules", "dry_relay"), COL["modules"]),
        part("Controller lid with front panel parts", S("ctrl_lid", "panel_parts"), "#CBD5E1"),
        part("Test port bracket and test port", S("test_bracket", "test_port"), COL["test_bracket"]),
        part("Fan plate", C["fan_plate"], COL["fan_plate"]),
        part("Exhaust fan", C["fan"], COL["fan"]),
        part("Wall sleeve, 200 mm", C["sleeve"], COL["sleeve"]),
        part("Inside grille", C["grille"], COL["grille"]),
        part("Backdraft shutter and weather hood", S("shutter", "hood"), COL["hood"]),
        part("Pressure switch and its tube", S("dp_switch", "dp_tube", "dp_screws"), COL["dps"]),
        part("Make-up air grille", inlet, COL["inlet"]),
        part("Valve bracket", C["valve_bracket"], COL["valve_bracket"]),
        part("Normally closed solenoid valve", C["valve"], COL["valve"]),
        part("Sounder and beacon", C["beacon"], COL["beacon"]),
        part("Oxygen sensor (option)", S("o2_box", "o2_screws"), COL["o2"]),
        part("Bump test tube (drawn short) and clips", short_tube(), COL["tube"]),
        part("24 V power supply", C["psu"], COL["psu"]),
    ]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    targets = [(0, 0, 1400), (0, 0, 1290), (0, 0, 1225), (0, 0, 1130), (0, 0, 1520), (0, -170, 1400), (0, 0, 1680),
               (470, 0, 1350), (470, -190, 1350), (470, -360, 1350), (470, -560, 1350), (720, 0, 1680),
               (980, -130, 1380), (1000, 60, 1360), (1020, 330, 1340), (960, -330, 1400), (1040, 720, 1320), (1060, 0, 1700),
               (0, 0, 820), (420, 0, 760), (420, 0, 950), (750, 0, 850), (750, 0, 1100), (420, 0, 560), (1000, 0, 800)]
    for p, t in zip(M, targets):
        c = p.shape.bounding_box().center()
        p.explode = (t[0] - c.X, t[1] - c.Y, t[2] - c.Z)
    return bv.overview(M, OUT / "overview.png", "H2Guard prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front left and above; sizes to scale with each other",
                       elev=18, azim=-60, size=(11, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    base = dict(project="H2Guard", date=DATE)
    out = []
    want = lambda n: only is None or n == only  # noqa: E731
    head_n = [part("Head", S("head_lid", "discs", "cup", "sensor_board", "cat", "mos", "standoffs"), "#999")]

    if want(101):
        hb = C["head_body"]
        c = hb.bounding_box().center()
        flip = b.Rot(180, 0, 0) * b.Pos(-c.X, -c.Y, -c.Z) * hb
        out.append(bv.component_sheet(
            part("Detector head box", hb, COL["head_body"]), [part("Head parts", S("discs", "cup", "sensor_board", "cat", "mos", "standoffs", "head_gland"), "#999")],
            dwg_no="HGD-DWG-101", title="H2Guard detector head box: drilling sketch", rev="P2", revisions=[("P1", "Making sketch for the prototype build plan", DATE, "AC"), ("P2", "Drop rod hole in the top; gland moved; back holes removed", DATE2, "AC")],
            material="Bought ABS or polycarbonate box 110 x 80 x 90 mm, lid on the 110 x 90 face", view_shape=flip, inset_view=(22, -60),
            notes=["Drawn upside down: the top view shows the floor (the face with the ports).",
                   "Floor: two 22 mm sensor ports, 22 mm each side of the centre, on the",
                   "  centre line front to back. The 25 mm discs rest on the 1.5 mm ledge.",
                   "Floor: four 3.4 mm holes for the standoff screws, 40 mm each side of",
                   "  centre and 25 mm each side of the front-to-back centre line.",
                   "Top: one 21.7 mm hole at the centre for the drop rod, and one",
                   "  16.2 mm hole 38 mm left of it for the M16 cable gland.",
                   "No holes in the back: the box hangs from the drop rod.",
                   "Tape the faces, pilot drill 3 mm, open the ports with a step drill.",
                   "  Deburr; clean with water only (solvent residue poisons the sensor).",
                   "Check: a disc laid on each port covers it with an even ledge all round."],
            **{**base, "date": DATE2}))

    if want(102):
        sb = S("sensor_board", "cat", "mos")
        c = sb.bounding_box().center()
        out.append(bv.component_sheet(
            part("Sensor board", sb, COL["sensor_board"]), [part("Head", S("head_body", "standoffs", "discs"), "#999")],
            dwg_no="HGD-DWG-102", title="H2Guard sensor board with both sensors: making sketch",
            material="Prototype board 100 x 70 x 1.6 mm; bought sensors", view_shape=b.Pos(-c.X, -c.Y, -c.Z) * sb, inset_view=(15, -60),
            notes=["Cut prototype board to 100 x 70 mm. Drill four 3.2 mm holes 10 mm in",
                   "  from each end and 10 mm in from the long edges (80 x 50 mm apart).",
                   "Solder the catalytic sensor under the board, centred 28 mm from the",
                   "  left end; the MOS sensor under it 28 mm from the right end, both on",
                   "  the long centre line. They must sit over the two ports.",
                   "Seat each sensor with 0.8 mm under its body: the catalytic can's face",
                   "  then sits 2.2 mm above its disc. Use a 0.8 mm shim while soldering.",
                   "On top: the bridge supply and heater regulator and a 4-way terminal",
                   "  for the cable (24 V, 0 V, catalytic output, MOS output).",
                   "No flux cleaner or silicone near the sensors: both poison them.",
                   "Check: the four holes line up with the standoffs in the box."],
            **base))

    if want(103):
        cup = S("cup", "cup_fitting")
        c = C["cup"].bounding_box().center()
        out.append(bv.component_sheet(
            part("Bump test cup", cup, COL["cup"]), [part("Head", S("head_body", "head_lid", "head_gland"), "#999")],
            dwg_no="HGD-DWG-103", title="H2Guard bump test cup (drip skirt): making sketch",
            material="PETG, 3D printed, 4 perimeters, 40 % infill", view_shape=b.Pos(-c.X, -c.Y, -c.Z) * C["cup"], inset_view=(-25, -60),
            notes=["Print 96 x 66 x 22 mm, walls and top plate 2 mm, open at the bottom.",
                   "Print it top plate down on the bed; no supports needed.",
                   "Top plate: two 22 mm openings 22 mm each side of centre, to line up",
                   "  with the ports; four 3.4 mm holes at 80 x 50 mm for the screws.",
                   "Right side: a 10 mm boss standing 8 mm proud, its centre 10 mm below",
                   "  the top plate; a 2.5 mm gas way through it into the cup.",
                   "Tap the boss M5 6 mm deep (drill 4.2) for the push-in fitting.",
                   "Inside volume about 114 mL; it is the bump test cup.",
                   "Fit: the four M3 screws that hold the standoffs pass up through the",
                   "  top plate, so the cup is held flat under the head floor.",
                   "Check: the openings sit over the ports; the fitting does not leak."],
            **base))

    if want(104):
        cb = S("ctrl_body", "ctrl_glands")
        c = C["ctrl_body"].bounding_box().center()
        out.append(bv.component_sheet(
            part("Controller box", cb, COL["ctrl_body"]), [part("Plate and modules", S("mplate", "modules"), "#999"),
                                                            wall_patch(CX - 260, CX + 220, CZ - 200, CZ + 200)],
            dwg_no="HGD-DWG-104", title="H2Guard controller box: drilling sketch", rev="P2", revisions=[("P1", "Making sketch for the prototype build plan", DATE, "AC"), ("P2", "Clear-lid box; four glands in the bottom", DATE2, "AC")],
            material="Bought IP65 polycarbonate wall box 200 x 250 x 90 mm, clear lid", view_shape=b.Pos(-c.X, -c.Y, -c.Z) * C["ctrl_body"], inset_view=(20, -55),
            notes=["Top face: four 16.2 mm gland holes, 45 mm in from the back face,",
                   "  20 and 60 mm each side of the centre (40 mm apart).",
                   "Bottom face: four 16.2 mm holes 45 mm in from the back, 20 and",
                   "  60 mm each side of the centre: oxygen sensor, pressure switch,",
                   "  dry-contact output and supply lead, from left to right.",
                   "Back: use the box's own corner fixing holes, outside the seal",
                   "  (about 170 x 220 mm apart here; follow the box you buy).",
                   "Inside the back: four moulded bosses, 160 x 200 mm apart, carry the",
                   "  mounting plate; check them on your box before drilling the plate.",
                   "Tape, pilot 3 mm, step drill slowly, deburr. No solvents.",
                   "Fit an M16 gland in each hole, nut inside, seal outside.",
                   "Check: each gland seal sits flat; nothing cracks round a hole."],
            **{**base, "date": DATE2}))

    if want(105):
        ld = S("ctrl_lid", "panel_parts")
        c = C["ctrl_lid"].bounding_box().center()
        out.append(bv.component_sheet(
            part("Controller lid", ld, COL["panel_parts"]), [part("Box", S("ctrl_body", "ctrl_glands", "mplate", "modules"), "#999")],
            dwg_no="HGD-DWG-105", title="H2Guard controller lid with the front panel: making sketch",
            material="Lid of the bought box, 4 mm polycarbonate; bought panel parts", view_shape=b.Pos(-c.X, -c.Y, -c.Z) * C["ctrl_lid"], inset_view=(15, -40),
            notes=["Measured from the lid centre, seen from the front.",
                   "Display window 60 x 30 mm, centred 40 mm left and 60 mm up:",
                   "  drill the corners 6 mm, cut between, file to the line.",
                   "Key switch: 19.2 mm hole, 50 mm left, 40 mm down.",
                   "Test button: 16.2 mm hole, 10 mm right, 40 mm down.",
                   "Status lights: three 5.2 mm holes, 45, 60 and 75 mm right, 40 down.",
                   "Display module behind the window on four M2.5 screws; the glass",
                   "  sits in the window. Key switch and button: nut behind the lid.",
                   "Lights in bezels: green (normal), amber (warning), red (trip).",
                   "Label the key 'RESET' and the button 'TEST'.",
                   "Check: the lid still closes on its gasket with every part fitted."],
            **base))

    if want(106):
        mp = C["mplate"]
        c = mp.bounding_box().center()
        out.append(bv.component_sheet(
            part("Mounting plate", mp, COL["mplate"]), [part("Box and modules", S("ctrl_body", "modules", "dry_relay"), "#999")],
            dwg_no="HGD-DWG-106", title="H2Guard controller mounting plate: making sketch", rev="P2", revisions=[("P1", "Making sketch for the prototype build plan", DATE, "AC"), ("P2", "Dry-contact relay added below the driver", DATE2, "AC")],
            material="Aluminium sheet 2 mm, 5052 or 6061 class", view_shape=b.Pos(-c.X, -c.Y, -c.Z) * mp, inset_view=(15, -50),
            notes=["Cut 176 x 220 mm from 2 mm aluminium sheet; round the corners.",
                   "Four 4.4 mm holes at the box's bosses: 80 mm each side of the",
                   "  centre across, 100 mm each side up and down (measure your box).",
                   "Lay the modules on it as the inset and step 5 show: microcontroller",
                   "  upper left, trip board below it, relays upper right, driver below,",
                   "  dry-contact relay below that (45 right, 38 down), terminal strip",
                   "  along the bottom, 80 mm below centre.",
                   "Mark each module's holes through the module; drill 3.2 mm for",
                   "  M3 screws on 6 mm nylon standoffs.",
                   "Deburr both faces so no chip can short a module.",
                   "Fit: four M4 x 10 self-tapping screws into the bosses.",
                   "Check: flat within 0.5 mm; the plate sits on all four bosses."],
            **{**base, "date": DATE2}))

    if want(107):
        tb = S("test_bracket", "test_port")
        c = C["test_bracket"].bounding_box().center()
        out.append(bv.component_sheet(
            part("Test port bracket", tb, COL["test_bracket"]), [part("Controller", S("ctrl_body", "ctrl_lid", "panel_parts", "ctrl_glands"), "#999"),
                                                                  part("Tube", win(C["tube"], TX - 20, TX + 20, -30, 0, TZ, TZ + 200), "#999")],
            dwg_no="HGD-DWG-107", title="H2Guard bump test port bracket: making sketch",
            material="Aluminium equal angle 30 x 30 x 3 mm", view_shape=b.Pos(-c.X, -c.Y, -c.Z) * C["test_bracket"], inset_view=(20, -125),
            notes=["Cut 40 mm of 30 x 30 x 3 mm angle; square and deburr the ends.",
                   "Upright leg (goes on the wall): two 4.4 mm holes 10 mm each side",
                   "  of centre, 19 mm up from the underside of the flat leg.",
                   "Flat leg (stands out from the wall): one 12.5 mm hole at mid-length,",
                   "  18 mm out from the wall face, for the bulkhead test port.",
                   "Fit the port from below, nut on top, dust cap pointing down.",
                   "Fit: two M4 screws with wall plugs, 35 mm left of the controller,",
                   "  flat leg 1,250 mm above the floor.",
                   "The 4 mm tube pushes into the top of the port and runs up the wall.",
                   "Check: the port is square to the leg and the cap comes off by hand."],
            **base))

    if want(108):
        fp = C["fan_plate"]
        c = fp.bounding_box().center()
        out.append(bv.component_sheet(
            part("Fan plate", fp, COL["fan_plate"]), [part("Fan, sleeve and hood", S("fan", "sleeve", "hood", "shutter"), "#999")],
            dwg_no="HGD-DWG-108", title="H2Guard fan plate: making sketch",
            material="Aluminium sheet 3 mm, 5052 or 6061 class", view_shape=b.Pos(-c.X, -c.Y, -c.Z) * fp, inset_view=(18, -45),
            notes=["Cut 240 x 240 mm from 3 mm aluminium sheet; round the corners.",
                   "Centre hole 152 mm for the fan's inlet: drill a ring of holes inside",
                   "  the line, cut out, file to the line (or use a 152 mm hole saw).",
                   "Fan screws: four 4.4 mm holes on an 80 mm radius at 45 degrees,",
                   "  countersunk from the front; match them to the fan you buy.",
                   "Wall screws: four 4.4 mm holes 105 mm each side of centre at the",
                   "  corners, countersunk from the front.",
                   "Grille screws: four holes tapped M4 (drill 3.3) 110 mm from centre",
                   "  on the centre lines, top, bottom, left and right.",
                   "Fit: fan body flat on the back of the plate; plate flat on the wall",
                   "  over the 200 mm sleeve; grille over the plate.",
                   "Check: the fan screws pull the fan face flat onto the plate."],
            **base))

    if want(109):
        vb = C["valve_bracket"]
        c = vb.bounding_box().center()
        out.append(bv.component_sheet(
            part("Valve bracket", S("valve_bracket"), COL["valve_bracket"]), [part("Valve", C["valve"], "#999"),
                                                                             wall_patch(VX - 200, VX + 200, VZ - 200, VZ + 150)],
            dwg_no="HGD-DWG-109", title="H2Guard valve bracket: making sketch",
            material="Aluminium flat bar 40 x 5 mm, 6082 class", view_shape=b.Pos(-c.X, -c.Y, -c.Z) * vb, inset_view=(20, -50),
            notes=["Cut 330 mm of 40 x 5 mm flat bar. Bend 90 degrees in the vice to",
                   "  an L, measured outside the bend: a 132 mm upright leg on the",
                   "  wall and a 200 mm arm standing out from it.",
                   "Upright leg: two 6.6 mm holes on the centre line, 25 and 80 mm up",
                   "  from its bottom end, for M6 screws with wall plugs.",
                   "Arm: two 5.5 mm holes on the bar's centre line, 152 and 188 mm",
                   "  out from the wall face (36 mm apart), for the valve screws.",
                   "Match these two holes to the tapped holes under the valve you buy.",
                   "Fit: arm level, 1,272 mm above the floor; valve on top on two M5",
                   "  screws from below. The gas fitter connects the valve ports.",
                   "Check: the arm is level and does not flex when the valve is pushed."],
            **base))

    if want(110):
        dr = S("drop_flange", "drop_rod", "drop_nuts", "drop_screws")
        c = dr.bounding_box().center()
        ceil_ = part("Ceiling", box(HX, HY, P["room"][2] + 15, 300, 260, 30), COL["wall"])
        out.append(bv.component_sheet(
            part("Ceiling drop rod", dr, COL["drop"]), [part("Detector head", S("head_body", "head_lid", "cup", "head_gland"), "#999"), ceil_],
            dwg_no="HGD-DWG-110", title="H2Guard ceiling drop rod and ceiling plate: making sketch",
            material="Bought: 1/2 in malleable iron floor flange, 1/2 in steel pipe nipple, two conduit locknuts",
            view_shape=b.Pos(-c.X, -c.Y, -c.Z) * dr, inset_view=(12, -60),
            notes=["Ceiling plate: a 1/2 in floor flange about 80 mm across. Drill or",
                   "  open three 5.5 mm holes on a 60 mm circle if it has none.",
                   "Rod: a 1/2 in steel pipe nipple, 89 mm long, 21.3 mm across,",
                   "  threaded at both ends. Screw it hand tight into the flange.",
                   "Run one locknut up the rod so its underside is 85 mm below the",
                   "  flange's ceiling face: the head top sits on it, 85 mm down.",
                   "Fit: flange on the ceiling directly over the apparatus centre",
                   "  (plumb line), three M5 x 40 screws into ceiling plugs.",
                   "The rod goes up through the 21.7 mm hole in the head top; the",
                   "  second locknut goes on inside, through the open front.",
                   "Check: ports 175 mm below the ceiling, over the apparatus; the",
                   "  head does not turn when pushed by hand."],
            **{**base, "date": DATE2}))
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []
    want = lambda n: only is None or n == only  # noqa: E731
    pf = D["port_face"]
    if want(1):
        bx = (HX - 52, HX + 6, HY, 0, pf - 24, pf + 50)
        out.append(bv.joint([
            part("Head box floor and wall", win(C["head_body"], *bx), COL["head_body"]),
            part("Arrestor disc on the ledge", win(C["discs"], *bx), COL["discs"]),
            part("Catalytic sensor, 2.2 mm above", win(C["cat"], *bx), COL["sensor_board"]),
            part("Sensor board", win(C["sensor_board"], *bx), "#14B8A6"),
            part("Cup top plate, opening under the port", win(C["cup"], *bx), COL["cup"])],
            OUT / "joint-01.png", "Joint 1: arrestor disc, port and catalytic sensor (head cut open)",
            subtitle="Cut through the left port, seen from the front. Gas passes the cup opening, the port and the disc to the sensor",
            elev=6, azim=-90, size=(8, 6)))
    if want(2):
        yy = HY + P["standoff_xy"][1]
        bx = (HX - 62, HX - 20, yy, 0, pf - 24, pf + 40)
        out.append(bv.joint([
            part("Head box floor", win(C["head_body"], *bx), COL["head_body"]),
            part("Standoff, 22 mm", win(C["standoffs"], *bx), COL["standoffs"]),
            part("Cup screw from below", win(C["cup_screws"], *bx), COL["bolt"]),
            part("Board screw from above", win(C["board_screws"], *bx), "#4B5563"),
            part("Sensor board", win(C["sensor_board"], *bx), COL["sensor_board"]),
            part("Bump test cup", win(C["cup"], *bx), COL["cup"])],
            OUT / "joint-02.png", "Joint 2: one standoff holds the cup and the sensor board",
            subtitle="Cut through a standoff, seen from the front. The screw from below clamps the cup to the floor",
            elev=6, azim=-90, size=(8, 6)))
    if want(3):
        nz = pf - P["cup"][2] / 2 + 1
        bx = (HX + 30, HX + 95, HY - 30, 0, nz - 20, pf + 45)
        out.append(bv.joint([
            part("Bump test cup and boss", win(C["cup"], *bx), COL["cup"]),
            part("M5 push-in fitting", win(C["cup_fitting"], *bx), COL["bolt"]),
            part("4 mm tube from the test port", win(C["tube"], *bx), COL["tube"]),
            part("Head box (above the cup)", win(C["head_body"], HX + 30, HX + 95, HY - 30, 0, pf, pf + 12), COL["head_body"])],
            OUT / "joint-03.png", "Joint 3: the tube at the cup",
            subtitle="Seen from the front right and below. The tube pushes into the fitting; the fitting screws into the boss",
            elev=-15, azim=-40, size=(8, 6)))
    if want(4):
        x0 = CX - 50
        bx = (CX - 105, x0, -95, 1, CZ - 130, CZ + 135)
        out.append(bv.joint([
            part("Box with its glands", win(S("ctrl_body", "ctrl_glands"), *bx), COL["ctrl_body"]),
            part("Moulded boss and M4 screw", win(C["mplate_screws"], *bx), COL["bolt"]),
            part("Mounting plate", win(C["mplate"], *bx), COL["mplate"]),
            part("Modules on standoffs", win(C["modules"], *bx), COL["modules"]),
            part("Lid", win(C["ctrl_lid"], *bx), "#CBD5E1"),
            part("Display and key switch", win(C["panel_parts"], *bx), COL["panel_parts"])],
            OUT / "joint-04.png", "Joint 4: controller cut open through the key switch",
            subtitle="Seen from the right. Plate on the bosses at the back, modules on standoffs, panel parts in the lid at the front",
            elev=8, azim=-3, size=(8, 6)))
    if want(5):
        bx = (TX - 40, TX + 40, -45, 1, TZ - 40, TZ + 70)
        out.append(bv.joint([
            wall_patch(TX - 40, TX + 40, TZ - 40, TZ + 70),
            part("Test port bracket", win(C["test_bracket"], *bx), COL["test_bracket"]),
            part("Bulkhead test port, cap down", win(C["test_port"], *bx), COL["test_port"]),
            part("M4 wall screws", win(C["test_bracket_screws"], *bx), COL["bolt"]),
            part("4 mm tube", win(C["tube"], *bx), "#A78BFA")],
            OUT / "joint-05.png", "Joint 5: bump test port on its bracket",
            subtitle="Seen from the front left. The port goes up through the flat leg; the tube pushes into its top",
            elev=20, azim=-55, size=(8, 6)))
    if want(6):
        bx = (FX - 140, FX, -25, 320, FZ - 130, FZ + 140)
        wall = context(P)["room"]
        out.append(bv.joint([
            part("Wall and 200 mm sleeve (cut)", win(wall, FX - 140, FX, 0, 150, FZ - 140, FZ + 140) + win(C["sleeve"], *bx), COL["wall"]),
            part("Inside grille on the fan plate", win(S("grille", "fan_plate"), *bx), COL["fan_plate"]),
            part("Fan, body in the sleeve", win(C["fan"], *bx), COL["fan"]),
            part("Shutter and weather hood (outside)", win(S("shutter", "hood"), *bx), COL["hood"])],
            OUT / "joint-06.png", "Joint 6: exhaust fan in the wall (cut through the fan's axis)",
            subtitle="Seen from the right and a little from outside; the room is on the left. The fan plate holds the fan",
            elev=18, azim=25, size=(8, 6)))
    if want(7):
        st = context(P)["store"]
        bx = (VX - 110, VX + 110, -230, 1, VZ - 175, VZ + 125)
        out.append(bv.joint([
            part("Valve bracket", win(C["valve_bracket"], *bx), COL["valve_bracket"]),
            part("Solenoid valve", win(C["valve"], *bx), COL["valve"]),
            part("M5 screws from below; M6 wall screws", win(C["valve_screws"], *bx), COL["bolt"]),
            part("Supply line (gas fitter)", win(st, *bx), "#9CA3AF")],
            OUT / "joint-07.png", "Joint 7: valve on its bracket",
            subtitle="Seen from the front left and below. Two screws up through the arm into the valve body",
            elev=-12, azim=-50, size=(8, 6)))
    if want(8):
        rz = P["room"][2]
        bx = (HX - 60, HX + 60, HY, HY + 60, rz - 110, rz + 30)
        ceil_ = box(HX, HY + 30, rz + 15, 120, 60, 30)
        out.append(bv.joint([
            part("Ceiling", ceil_, COL["wall"]),
            part("Floor flange (ceiling plate) and screws", win(S("drop_flange", "drop_screws"), *bx), COL["drop"]),
            part("Pipe nipple, 89 mm", win(C["drop_rod"], *bx), "#A8A29E"),
            part("Locknuts above and below the head top", win(C["drop_nuts"], *bx), COL["bolt"]),
            part("Head box top", win(C["head_body"], *bx), COL["head_body"]),
            part("Cable gland", win(C["head_gland"], *bx), "#374151")],
            OUT / "joint-08.png", "Joint 8: the head on its ceiling drop rod (cut through the rod)",
            subtitle="Seen from the front. The rod screws into the flange; two locknuts clamp the head top between them",
            elev=8, azim=-90, size=(8, 6)))
    if want(9):
        bx = (FX - 260, FX + 40, -60, 20, FZ - 110, FZ + 90)
        out.append(bv.joint([
            wall_patch(FX - 280, FX + 60, FZ - 120, FZ + 100),
            part("Pressure switch", win(S("dp_switch", "dp_screws"), *bx), COL["dps"]),
            part("6 mm tube to the fan inlet tap", win(C["dp_tube"], *bx), "#22D3EE"),
            part("Inside grille and fan plate", win(S("grille", "fan_plate"), *bx), "#CBD5E1"),
            part("Fan inlet", win(C["fan"], *bx), COL["fan"])],
            OUT / "joint-09.png", "Joint 9: pressure switch and its tap in the fan inlet",
            subtitle="Seen from the front left. The low port's tube ends just inside the grille; the high port is open to the room",
            elev=15, azim=-60, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    out = []
    want = lambda n: only is None or n == only  # noqa: E731

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    hb = part("Head box", C["head_body"], COL["head_body"])
    st(1, [hb], [mv(part("Arrestor discs", C["discs"], COL["discs"]), (0, -130, 25))], "arrestor discs into the head",
       "Through the open front; each disc on its port ledge with a bead of two-part epoxy round its edge. No silicone",
       elev=35, azim=-60, label_done=True)
    hd = [hb, part("Discs", C["discs"], COL["discs"])]
    st(2, hd, [mv(part("Standoffs (4), from inside", C["standoffs"], COL["standoffs"]), (0, 0, 60)),
               mv(part("Bump test cup with fitting", S("cup", "cup_fitting"), COL["cup"]), (0, 0, -60)),
               mv(part("M3 screws from below", C["cup_screws"], COL["bolt"]), (0, 0, -110))],
       "standoffs and bump test cup", "Hold each standoff inside; screw up through the cup and the floor into it. Seen from below",
       elev=-28, azim=-60, label_done=False)
    hd2 = hd + [part("Cup and standoffs", S("cup", "cup_fitting", "standoffs", "cup_screws"), COL["cup"])]
    st(3, hd2, [mv(part("Sensor board with sensors", S("sensor_board", "cat", "mos", "board_screws"), COL["sensor_board"]), (0, -110, 0)),
                mv(part("M16 cable gland", C["head_gland"], COL["bolt"]), (0, 0, 60))],
       "sensor board and cable gland", "Board in through the open front onto the standoffs, four M3 screws; gland in the top, nut inside",
       elev=20, azim=-60, label_done=False)
    head_all = part("Detector head", S("head_body", "discs", "cup", "cup_fitting", "standoffs", "cup_screws", "sensor_board", "cat", "mos", "head_gland"), COL["head_body"])
    import build123d as b
    rz_ = P["room"][2]
    ceil = part("Ceiling", box(HX, HY, rz_ + 10, 320, 260, 20), COL["wall"])
    inner_nut = C["drop_nuts"] & box(HX, HY, D["head_z"] + P["head"][2] / 2 - P["head_wall"] - 2, 40, 40, 4.2)
    outer = S("drop_flange", "drop_rod", "drop_screws") + (C["drop_nuts"] - inner_nut)
    st(4, [part("Drop rod and top locknut, on the ceiling", outer, COL["drop"])],
       [mv(head_all, (0, 0, -150)), mv(part("Inner locknut, through the open front", inner_nut, COL["bolt"]), (0, -160, -40)),
        mv(part("Lid, fitted after the cable is wired", C["head_lid"], "#FCD34D"), (0, -260, -150))],
       "detector head onto the ceiling drop rod", "Seen from below. Flange screwed to the ceiling over the apparatus first; push the head up onto the rod and fit the inner locknut",
       context=[ceil], elev=-14, azim=-55, label_done=True)
    cbox = part("Controller box with glands", S("ctrl_body", "ctrl_glands"), COL["ctrl_body"])
    st(5, [part("Controller box", C["ctrl_body"], COL["ctrl_body"])],
       [mv(part("Glands (4 top, 4 bottom)", C["ctrl_glands"], COL["ctrl_glands"]), (0, -40, 70)),
        mv(part("Mounting plate with modules and dry-contact relay", S("mplate", "modules", "dry_relay", "mplate_screws"), COL["modules"]), (0, -170, 0))],
       "glands and mounting plate into the controller box",
       "Modules fitted to the plate on the bench first; plate on the four bosses with four M4 screws",
       elev=18, azim=-50, label_done=False)
    st(6, [part("Lid", C["ctrl_lid"], COL["ctrl_lid"])], [mv(part("Display, key switch, button and lights", C["panel_parts"], COL["panel_parts"]), (0, 70, 0))],
       "front panel parts into the lid", "Seen from behind: display on four M2.5 screws; key switch, button and lights through their holes, nuts behind the lid",
       elev=15, azim=125, label_done=True)
    wallc = wall_patch(TX - 120, CX + 160, CZ - 200, CZ + 200)
    cfull = part("Controller with plate and modules", S("ctrl_body", "ctrl_glands", "mplate", "modules"), COL["ctrl_body"])
    st(7, [], [mv(cfull, (0, -150, 0)), mv(part("Test port bracket and port", S("test_bracket", "test_port"), COL["test_bracket"]), (0, -110, 0))],
       "controller and test port bracket onto the wall", "Seen from the front left. Controller top 1,475 mm above the floor, four screws; bracket 35 mm to its left, two M4 screws",
       context=[wallc], elev=15, azim=-125, label_done=False)
    st(8, [part("Fan plate", C["fan_plate"], COL["fan_plate"])], [mv(part("Exhaust fan", C["fan"], COL["fan"]), (0, 150, 0))],
       "fan onto the fan plate", "On the bench. Fan inlet face flat on the back of the plate; four M4 countersunk screws from the front",
       elev=15, azim=40, label_done=True)
    wall_cut = part("Wall (cut away round the opening)", win(context(P)["room"], FX - 300, FX + 300, 0, 150, FZ - 300, FZ + 190), COL["wall"])
    st(9, [], [mv(part("Wall sleeve, 200 mm", C["sleeve"], COL["sleeve"]), (0, -300, 0)),
               mv(part("Fan plate with fan", S("fan_plate", "fan"), COL["fan"]), (0, -520, 0))],
       "sleeve and fan into the wall", "Sleeve flush with both wall faces; fan into the sleeve, plate flat on the wall, four screws with plugs",
       context=[wall_cut], elev=12, azim=-50, label_done=False)
    st(10, [part("Fan plate with fan and sleeve", S("fan_plate", "fan", "sleeve"), COL["fan"])],
       [mv(part("Inside grille, four M4 screws into the plate", C["grille"], "#CBD5E1"), (0, -120, 0)),
        mv(part("Shutter on the outlet; hood outside", S("shutter", "hood"), COL["hood"]), (0, 260, 0))],
       "grille, shutter and weather hood", "Grille on the room side; shutter on the fan outlet and hood on four screws on the outside face",
       context=[wall_cut], elev=12, azim=-50, label_done=False)
    import build123d as b
    wall_side = part("Side wall", b.Pos(-10, P["inlet_y"], P["inlet_z"]) * b.Box(20, 500, 400), COL["wall"])
    wallp = wall_patch(P["dps_x"] - 120, FX + 160, FZ - 180, FZ + 140)
    st(11, [part("Fan plate, fan and grille", S("fan_plate", "fan", "grille"), COL["fan"])],
       [mv(part("Pressure switch, two screws with plugs", S("dp_switch", "dp_screws"), COL["dps"]), (0, -150, 0)),
        mv(part("6 mm tube from the low port into the fan inlet", C["dp_tube"], "#22D3EE"), (0, -90, -60))],
       "pressure switch and its tube", "Switch on the wall left of the fan, ports down; the tube's end sits just inside the grille, in the fan inlet",
       context=[wallp], elev=12, azim=-50, label_done=True)
    st(12, [], [mv(part("Make-up air grille", C["inlet"], COL["inlet"]), (160, 0, 0))], "make-up air grille",
       "Low on the far side wall over the builder's opening, mesh on; four screws with plugs",
       context=[wall_side], elev=15, azim=-30, label_done=False)
    wallv = wall_patch(VX - 200, VX + 200, VZ - 220, VZ + 160)
    st(13, [], [mv(part("Valve bracket, M6 screws and plugs", S("valve_bracket"), COL["valve_bracket"]), (0, -120, 0)),
                mv(part("Solenoid valve, two M5 screws from below", C["valve"], COL["valve"]), (0, 0, 110))],
       "valve bracket and valve", "Arm level, 1,272 mm up; the gas fitter then connects the valve into the supply after the regulator",
       context=[wallv], elev=15, azim=-55, label_done=False)
    psu_near = part("24 V power supply, on the floor by the outlet", b.Pos(0, 0, 0) * C["psu"], COL["psu"])
    wallb = wall_patch(P["beacon_x"] - 160, P["beacon_x"] + 160, P["beacon_z"] - 160, P["beacon_z"] + 160)
    wallo = wall_patch(P["o2_x"] - 160, P["o2_x"] + 160, P["o2_z"] - 200, P["o2_z"] + 160)
    st(15, [], [mv(part("Oxygen sensor, cell down, two screws with plugs", S("o2_box", "o2_screws"), COL["o2"]), (0, -150, 0))],
       "oxygen sensor (only where inert gas cylinders share the room)", "Cell at breathing height, about 1,480 mm above the floor; cable through the gland on top to the controller",
       context=[wallo], elev=12, azim=-55, label_done=False)
    st(14, [], [mv(part("Sounder and beacon by the door", C["beacon"], COL["beacon"]), (0, -150, 0))],
       "sounder, beacon and power supply", "Beacon top 450 mm below the ceiling, two screws with plugs. The certified 24 V supply just stands on the floor by the outlet",
       context=[wallb], elev=12, azim=-55, label_done=False)
    wallt = wall_patch(HX - 100, TX + 100, CZ - 200, P["room"][2])
    ceilt = part("Ceiling (cut back)", box((HX + TX) / 2, -170, rz_ + 10, TX - HX + 200, 340, 20), COL["wall"], alpha=0.35)
    st(16, [part("Detector head on its drop rod", S("head_body", "cup", "head_lid", "drop_flange", "drop_rod", "drop_nuts"), COL["head_body"]), part("Controller", S("ctrl_body", "ctrl_lid", "ctrl_glands"), COL["ctrl_body"]),
            part("Test port", S("test_bracket", "test_port"), COL["test_bracket"]), part("Fan", S("fan_plate", "grille"), COL["fan"])],
       [mv(part("4 mm tube, six wall clips, two ceiling clips", S("tube", "clips", "ceil_clips"), COL["tube"]), (0, -150, 0))],
       "bump test tube and clips", "Tube from the top of the test port, up the wall, along under the ceiling, across the ceiling to the head and down into the cup fitting",
       context=[wallt, ceilt], elev=14, azim=-62, label_done=False)
    st(17, [part("Controller box", S("ctrl_body", "ctrl_glands", "mplate", "modules", "dry_relay"), COL["ctrl_body"])],
       [mv(part("Lid with the front panel", S("ctrl_lid", "panel_parts"), COL["panel_parts"]), (0, -150, 0))],
       "wire up and close the lids", "Cables through the glands to the terminal strip, as the wiring diagram; lid on its gasket; same for the head lid",
       context=[wall_patch(CX - 160, CX + 160, CZ - 180, CZ + 180)], elev=15, azim=-50, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 8.4), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 84); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 82, "H2Guard prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 78.6, "Bought modules and a hand-wired trip board; no circuit board is laid out. Stranded copper; ferrules on every screw terminal. All circuits 24 V DC or lower.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/h2guard", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((30, 12), 56, 49, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(31.5, 59.8, "In the controller box, on the mounting plate", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, BLK = "#B91C1C", "#1D4ED8", "#6B7280", "#111827"
    blk(3, 44, 17, 12, "24 V supply", "certified plug-in,\n60 W, mains inside it", "#1F2937")
    blk(3, 22, 17, 14, "Detector head", "sensor board: bridge\nsupply, MOS heater,\nboth sensors", "#F59E0B")
    blk(34, 44, 22, 12, "Trip board", "fuse 3 A, 5 V supply,\ncomparator and latch", "#0F766E")
    blk(60, 44, 22, 12, "Microcontroller", "RP2040 class, 4 MB\nflash, watchdog 1 s", "#115E59")
    blk(34, 24, 22, 13, "Relay modules", "series trip relay, fan\nboost relay; dry-contact\nrelay (held when healthy)", "#0F766E")
    blk(60, 24, 22, 13, "Driver module", "valve switch,\nsounder, beacon", "#0F766E")
    blk(34, 13.5, 48, 4, "", "", "#7C3AED")
    ax.text(58, 15.5, "Terminal strip: fan, valve, sounder, beacon and dry-contact cables land here", ha="center", va="center", fontsize=8, fontweight="bold", color=INK)
    blk(99, 46, 18, 11, "Exhaust fan", "24 V EC; PWM in,\ntachometer out", "#2563EB")
    blk(99, 31, 18, 11, "Solenoid valve", "normally closed,\n24 V, 8 W coil", "#D4A017")
    blk(99, 16, 18, 11, "Sounder, beacon", "24 V, red", "#DC2626")
    blk(62, 3.5, 20, 6.5, "Front panel", "display, key, test, lights", "#374151")
    blk(3, 63, 19, 11, "Oxygen sensor", "option; 4 to 20 mA,\n24 V, breathing height", "#65A30D")
    blk(99, 63, 18, 11, "Pressure switch", "at the fan; contact\ncloses on airflow", "#0891B2")
    blk(99, 4, 18, 8.5, "H2Bench supply", "dry contact: opens on\ntrip or power loss", "#1E3A8A")
    wire([(11.5, 44), (11.5, 40), (28, 40), (28, 50), (34, 50)], RED); lab(12.3, 41.5, "24 V lead, 1.0 mm²,\nbottom gland", RED)
    wire([(56, 50), (60, 50)], RED, 1.2); lab(58, 52.4, "5 V", RED, "center")
    wire([(20, 29), (30, 29), (30, 46), (34, 46)], BLU); lab(20.5, 31.6, "4-core 0.5 mm²: 24 V,\n0 V, CAT out, MOS out", BLU)
    wire([(45, 44), (45, 37)], GRY, 1.4); lab(45.6, 40.5, "trip line\n(hardware)", GRY)
    wire([(71, 44), (71, 37)], GRY, 1.4); lab(71.6, 40.5, "valve, alarm,\nboost commands", GRY)
    wire([(56, 30.5), (60, 30.5)], RED, 2.0); lab(58, 33, "relay in\nseries", RED, "center")
    wire([(45, 24), (45, 17.5)], RED, 1.2); wire([(71, 24), (71, 17.5)], RED, 1.2)
    wire([(82, 15.5), (90, 15.5), (90, 51), (99, 51)], RED); lab(90.6, 53, "4-core 0.5 mm²", RED)
    wire([(82, 15.5), (92, 15.5), (92, 36), (99, 36)], RED); lab(92.6, 38.2, "2-core 0.75 mm²", RED)
    wire([(82, 15.5), (99, 21)], RED); lab(88, 20.5, "4-core 0.5 mm²", RED)
    wire([(82, 6.75), (84.5, 6.75), (84.5, 47), (82, 47)], GRY, 1.2); lab(85.3, 8.5, "ribbon to the\nmicrocontroller", GRY)
    wire([(22, 68.5), (26, 68.5), (26, 53), (34, 53)], "#65A30D"); lab(27, 66.5, "2-core 0.5 mm², 4 to 20 mA, bottom gland,\nto the trip board and microcontroller", "#65A30D")
    wire([(99, 68.5), (87.5, 68.5), (87.5, 52), (82, 52)], "#0891B2"); lab(88.2, 60.5, "2-core 0.5 mm²,\nbottom gland; no airflow\nfor 10 s closes the valve", "#0891B2")
    wire([(82, 14.5), (96, 14.5), (96, 8), (99, 8)], "#1E3A8A"); lab(86, 12.4, "2-core, volt-free", "#1E3A8A")
    ax.text(2, 7.5, "Valve power passes through the relay contact (opened by the hardware latch)\nand then the driver's switch: either one opening closes the valve.",
            fontsize=7.4, color="#B45309", fontweight="bold", va="center")
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        name, _, n = w.partition(":")
        r = fns[name](int(n)) if n else fns[name]()
        print(w, "->", r)
