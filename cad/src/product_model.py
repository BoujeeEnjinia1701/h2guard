"""H2Guard product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: filleted detector head with a parting line, label,
cable gland, drip skirt bump test cup, sintered arrestor discs and the two sensor cans on their
carrier board; an IP65 controller box with a lid frame, a clear polycarbonate window over the
board and the series trip and fan interlock relays, lid screws, glands, an OLED readout, a
key-switch reset, a teal test button and a lit green status light; the capped bump test port and
its tube; and the normally closed solenoid valve on the supply line. Context is a compact section
of back wall and ceiling with surface conduit and the supply pipe and clips.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
A research and teaching prototype, not a certified gas detection system.

Every main dimension, mounting height and interface comes from PARAMS, derived(), build_parts()
and bump_kit() in model.py. Axes as model.py: back wall inside face at Y = 0 with the room
toward -Y, floor at Z = 0, ceiling at Z = room[2]. The controller is at its model.py position.
For a compact product render the detector head (with a short section of ceiling) and the valve
are shown on their own wall panels beside the controller (HEAD_AT, VALVE_AT below), so the head
is drawn lower than installed: in the room its ports are 175 mm below the ceiling and the
controller top is at least 1 m below the ceiling, as model.py and HGD-DWG-001 give. All sizes,
offsets from the wall and the head-to-ceiling gap are unchanged. See docs/REVIEW.md, session
2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, derived

TITLE = "H2Guard: hydrogen leak detector and ventilation interlock"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 20, "az": -50,
     "note": "Product render from the front right and above (about 20 deg elevation); detector head under a "
             "ceiling section at left with the shut-off valve below it, controller at right with the relays "
             "behind its clear window and the green status light lit. Panels are not at installed heights"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): detector head, sensors, "
             "arrestor discs and test cup; controller box, board with trip and fan interlock relays, lid, "
             "window and controls; bump test port; solenoid valve"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 14, "az": -62,
     "note": "Detail from the front right, slightly above (about 14 deg elevation): detector head (top) and "
             "controller (bottom) without the room; relays behind the clear window, green status light lit"},
]

# Render layout (not the installed layout). The head panel stands beside the controller panel;
# the head keeps its 85 mm gap below the ceiling of its own panel.
HEAD_AT = (2990.0, 1680.0)     # head centre X and the underside of its ceiling section, Z
VALVE_AT = (2990.0, 1330.0)    # valve centre X and pipe centre Z (Y stays at store_y)
PANEL_Z0 = 1150.0              # bottom of both context panels
HEAD_PANEL_W = 220.0
CTRL_PANEL = (3140.0, 3460.0, 1560.0)   # x0, x1, top Z of the controller panel
CEIL_DEPTH = 140.0             # ceiling section projects this far into the room (-Y)

# Colours (restrained product palette; kit accent)
C_SHELL = "#E9EAEC"
C_SHELL2 = "#C9CDD3"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_WINDOW = "#DCEBF5"
C_METAL = "#B8BEC6"
C_SINTER = "#8E949B"
C_BRASS = "#C9A227"
C_PCB = "#166534"
C_CHIP = "#111827"
C_RELAY = "#1E3A5F"
C_TERM = "#2E7D5B"
C_LED_G = "#22C55E"
C_LED_A = "#6E5315"
C_LED_R = "#5E1C1C"
C_OLED = "#5EEAD4"
C_LABEL = "#F4F4F2"
C_TUBE = "#EDEDEA"
C_WALL = "#E3E1DC"
C_CEIL = "#ECEBE7"
C_CONDUIT = "#D5D7DA"
C_PIPE = "#AEB4BB"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _front(s):
    return s.faces().sort_by(Axis.Y)[0].edges()


def _back(s):
    return s.faces().sort_by(Axis.Y)[-1].edges()


def _hex_x(x, y, z, af, length):
    """Hex prism along X (across flats `af`)."""
    return Pos(x - length / 2, y, z) * extrude(Plane.YZ * RegularPolygon(af / 1.732, 6), amount=length)


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def product_parts(P=PARAMS):
    D = derived(P)
    rz = P["room"][2]
    Pv = dict(P, app_x=HEAD_AT[0], valve_x=VALVE_AT[0], supply_z=VALVE_AT[1])
    dzh = HEAD_AT[1] - rz                              # head drawn this far below its installed height
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ detector head (BOM 1 to 4)
    hx, hy, hz = Pv["app_x"], P["head_y"], D["head_z"] + dzh
    hw, hd, hh = P["head"]
    t = P["head_wall"]
    pf = D["port_face"] + dzh
    EH = (0, -90, 0)                                    # head explode: forward off the wall plate
    outer = _box(hx, hy, hz, hw, hd, hh)
    outer = _fillet_try(outer, _edges_par(outer, Axis.Z), [8.0, 6.0, 4.0])
    outer = _fillet_try(outer, _front(outer), [4.0, 3.0, 2.0])
    housing = outer - _box(hx, hy, hz, hw - 2 * t, hd - 2 * t, hh - 2 * t)
    for dx in (-P["port_dx"], P["port_dx"]):
        housing -= _zcyl(hx + dx, hy, pf + t / 2, P["port_d"] / 2, t + 2)
    # parting line between the base and the front cover
    ring = _box(hx, hy, hz, hw + 2, hd + 2, 0.8) - _box(hx, hy, hz, hw - 1.2, hd - 1.2, 2)
    housing -= Pos(0, 0, 18.0) * ring
    add("Detector head housing", housing, C_SHELL, "plastic", 1, "shell", EH)

    plate = _box(hx, -t / 2 - 2, hz, hw + 30, 4, hh)
    plate = _fillet_try(plate, _edges_par(plate, Axis.Y), [6.0, 4.0])
    plate -= outer
    add("Detector head wall plate", plate, C_SHELL2, "plastic", 1, "shell", (0, 0, 0))
    screws = None
    for sx in (-1, 1):
        s = _ycyl(hx + sx * (hw / 2 + 8), -6.3, hz, 3.0, 1.6)
        s = _fillet_try(s, _front(s), [0.6, 0.3])
        s -= _box(hx + sx * (hw / 2 + 8), -7.2, hz, 3.6, 1.0, 0.8)
        screws = s if screws is None else screws + s
    add("Wall plate screws", screws, C_METAL, "metal", 14, "shell", (0, -30, 0))

    gz = hz + hh / 2
    gland = _hex_z(hx, hy, gz + 2.5, 20.0, 5.0) + _zcyl(hx, hy, gz + 8.0, 8.0, 6.0)
    gland += Pos(hx, hy, gz + 11.0) * Sphere(7.0) & _box(hx, hy, gz + 14, 20, 20, 6)
    add("Head cable gland", gland, C_DARK, "plastic", 1, "shell", (0, -90, 70))

    # front label and accent band (thin raised parts)
    fy = hy - hd / 2
    band = _box(hx, fy - 0.2, hz + 30, hw - 18, 0.4, 5)
    add("Head accent band", band, C_ACCENT, "painted", 1, "shell", (0, -130, 0))
    lab = _box(hx, fy - 0.2, hz - 2, 58, 0.4, 26)
    add("Head label", lab, C_LABEL, "paper", 14, "shell", (0, -130, 0))
    ink = _box(hx - 18, fy - 0.5, hz + 3, 14, 0.3, 10) + _box(hx + 7, fy - 0.5, hz + 6, 28, 0.3, 3) \
        + _box(hx + 3, fy - 0.5, hz, 20, 0.3, 2) + _box(hx, fy - 0.5, hz - 10, 48, 0.3, 2)
    add("Head label print", ink, C_DARK, "paper", 14, "shell", (0, -130, 0))

    # sensors on their carrier board (BOM 2, 3)
    ES = (0, -90, -80)
    bz = pf + t + P["board_gap"]
    carrier = _box(hx, hy, bz, hw - 2 * t - 4, hd - 2 * t - 4, 1.6)
    add("Sensor carrier board", carrier, C_PCB, "plastic", 2, "internal", ES)
    cd_, ch_ = P["cat"]
    cat = _zcyl(hx - P["port_dx"], hy, bz - ch_ / 2 - 0.8, cd_ / 2, ch_)
    cat = _fillet_try(cat, _bottom(cat), [1.0, 0.5])
    add("Catalytic H2 sensor can", cat, C_METAL, "metal", 2, "internal", ES)
    md_, mh_ = P["mos"]
    mos = _zcyl(hx + P["port_dx"], hy, bz - mh_ / 2 - 0.8, md_ / 2, mh_)
    mos = _fillet_try(mos, _bottom(mos), [0.6, 0.3])
    add("MOS H2 sensor can", mos, C_METAL, "metal", 3, "internal", ES)
    comps = _box(hx, hy + 12, bz + 1.6, 12, 8, 1.6) + _box(hx - 2, hy - 14, bz + 1.4, 8, 5, 1.2) \
        + _box(hx + 30, hy + 20, bz + 3.8, 12, 6, 6)
    add("Sensor board components", comps, C_CHIP, "plastic", 2, "internal", ES)

    # arrestor discs (BOM 4), in the ports as model.py
    dd, dt = P["disc"]
    discs = None
    for dx in (-P["port_dx"], P["port_dx"]):
        d = _zcyl(hx + dx, hy, pf + t / 2 + dt / 2 - t / 2, dd / 2, dt)
        discs = d if discs is None else discs + d
    add("Sintered arrestor discs", discs, C_SINTER, "metal", 4, "internal", (0, -90, -125))

    # drip skirt that forms the bump test cup (BOM 4), with its gas nozzle
    cx_, cy_, cz_ = P["cup"]
    w = P["cup_wall"]
    skirt = _box(hx, hy, pf - cz_ / 2, cx_, cy_, cz_)
    skirt = _fillet_try(skirt, _edges_par(skirt, Axis.Z), [6.0, 4.0])
    skirt = _fillet_try(skirt, _bottom(skirt), [1.5, 1.0])
    inner = _box(hx, hy, pf - cz_ / 2 - w / 2, cx_ - 2 * w, cy_ - 2 * w, cz_ - w + 0.01)
    inner = _fillet_try(inner, _edges_par(inner, Axis.Z), [4.0, 2.0])
    skirt -= inner
    skirt += _box(hx, hy, pf + 1.0, cx_ + 2, cy_ + 2, 2.0) - _box(hx, hy, pf + 1.0, cx_ - 2 * w, cy_ - 2 * w, 3)
    nz = pf - 8
    nozzle = _xcyl(hx + cx_ / 2 + 4.5, hy, nz, 3.0, 11.0) + _xcyl(hx + cx_ / 2 + 8.0, hy, nz, 3.6, 2.0)
    skirt += nozzle
    skirt -= _xcyl(hx + cx_ / 2 + 4, hy, nz, 1.3, 16.0)
    add("Drip skirt and bump test cup", skirt, C_DARK, "plastic", 4, "shell", (0, -90, -185))

    # ------------------------------------------------------------ controller (BOM 5 to 7)
    cw, cd, ch = P["ctrl"]
    cxx, czz = P["ctrl_x"], P["ctrl_z"]
    body_o = _box(cxx, -cd / 2 + 2, czz, cw, cd - 4, ch)         # y -86 .. 0, as model.py
    body_o = _fillet_try(body_o, _edges_par(body_o, Axis.Y), [8.0, 6.0, 4.0])
    body_o = _fillet_try(body_o, _back(body_o), [2.0, 1.0])
    body = body_o - _box(cxx, -cd / 2, czz, cw - 6, cd - 4, ch - 6)
    # mounting ribs on the sides (texture) and a lid step
    for sx in (-1, 1):
        for dz in (-80, -40, 0, 40, 80):
            body -= _box(cxx + sx * cw / 2, -46, czz + dz, 1.6, 60, 2.0)
    add("Controller enclosure", body, C_SHELL, "plastic", 5, "shell", (0, 0, 0))

    ly0, ly1 = -cd - 4, -cd + 4                                    # lid y -94 .. -86
    lid_o = _box(cxx, (ly0 + ly1) / 2, czz, cw, ly1 - ly0, ch)
    lid_o = _fillet_try(lid_o, _edges_par(lid_o, Axis.Y), [8.0, 6.0, 4.0])
    lid_o = _fillet_try(lid_o, _front(lid_o), [2.5, 1.5, 1.0])
    ww, wh = cw - 36, ch - 40
    wz = czz - 4
    lid = lid_o - _box(cxx, (ly0 + ly1) / 2, wz, ww, 20, wh)
    lid -= _box(cxx, ly1 - 0.5, czz, cw - 6, 1.2, ch - 6) - _box(cxx, ly1 - 0.5, czz, cw - 8, 2, ch - 8)
    add("Controller lid frame", lid, C_SHELL2, "plastic", 5, "shell", (0, -320, 0))

    # clear polycarbonate window, cut round the front panel parts (BOM 7)
    pane = _box(cxx, -91, wz, ww + 4, 2.0, wh + 4)
    holes = (_box(cxx, -91, czz + 60, 92, 6, 47) + _ycyl(cxx - 50, -91, czz - 40, 12.5, 6)
             + _ycyl(cxx + 10, -91, czz - 40, 9.5, 6) + _box(cxx + 55, -91, czz - 40, 42, 6, 14))
    pane -= holes
    add("Clear polycarbonate window", pane, C_WINDOW, "clear", 5, "shell", (0, -320, 0))

    lscr = None
    for sx in (-1, 1):
        for sz in (-1, 1):
            s = _ycyl(cxx + sx * (cw / 2 - 9), ly0 - 0.6, czz + sz * (ch / 2 - 9), 3.4, 1.2)
            s = _fillet_try(s, _front(s), [0.5, 0.3])
            s -= _box(cxx + sx * (cw / 2 - 9), ly0 - 1.2, czz + sz * (ch / 2 - 9), 4.0, 1.0, 0.8)
            lscr = s if lscr is None else lscr + s
    add("Lid screws", lscr, C_METAL, "metal", 14, "shell", (0, -380, 0))

    lab = _box(cxx, ly0 - 0.2, czz + ch / 2 - 11, 64, 0.4, 7)
    add("Controller name plate", lab, C_ACCENT, "painted", 7, "shell", (0, -360, 0))

    # front panel: OLED module, key-switch reset, test button, status lights (BOM 7)
    EP = (0, -400, 0)
    oled = _box(cxx, -cd - 6, czz + 60, 90, 4, 45)
    oled = _fillet_try(oled, _edges_par(oled, Axis.Y), [3.0, 2.0])
    oled = _fillet_try(oled, _front(oled), [0.8, 0.5])
    oled -= _box(cxx, -cd - 8, czz + 62, 72, 1.0, 30)
    add("OLED display bezel", oled, C_BLACK, "plastic", 7, "shell", EP)
    glass = _box(cxx, -cd - 7.3, czz + 62, 72, 0.6, 30)
    add("OLED display glass", glass, "#0E1216", "screen", 7, "shell", EP)
    yy = -cd - 7.75
    readout = (_box(cxx - 14, yy, czz + 67, 34, 0.3, 11) + _box(cxx + 20, yy, czz + 69, 16, 0.3, 4)
               + _box(cxx + 20, yy, czz + 63, 16, 0.3, 2) + _box(cxx, yy, czz + 53, 60, 0.3, 3))
    add("OLED readout (lit)", readout, C_OLED, "emissive", 7, "shell", EP)

    kx, kz = cxx - 50, czz - 40
    kb = _ycyl(kx, -cd - 5, kz, 12.0, 6.0)
    kb = _fillet_try(kb, _front(kb), [1.5, 1.0])
    kb -= _ycyl(kx, -cd - 7, kz, 7.5, 4.0)
    add("Key switch bezel", kb, C_METAL, "metal", 7, "shell", EP)
    core = _ycyl(kx, -cd - 5.5, kz, 7.3, 5.0) - _box(kx, -cd - 8.2, kz, 1.6, 2.0, 7.0)
    add("Key switch cylinder", core, "#9A9FA6", "metal", 7, "shell", EP)

    bx_, bz_ = cxx + 10, czz - 40
    bb = _ycyl(bx_, -cd - 4.5, bz_, 9.0, 1.8) - _ycyl(bx_, -cd - 4.5, bz_, 6.6, 3.0)
    add("Test button bezel", bb, C_DARK, "plastic", 7, "shell", EP)
    btn = _ycyl(bx_, -cd - 6.5, bz_, 6.3, 5.0)
    btn = _fillet_try(btn, _front(btn), [1.2, 0.8])
    add("Test button", btn, C_ACCENT, "plastic", 7, "shell", EP)

    lx, lz = cxx + 55, czz - 40
    strip = _box(lx, -cd - 5, lz, 40, 2.0, 12)
    strip = _fillet_try(strip, _edges_par(strip, Axis.Y), [2.0, 1.0])
    add("Status light housing", strip, C_BLACK, "plastic", 7, "shell", EP)
    for k, (col, mat, nm) in enumerate([(C_LED_G, "emissive", "Status light, green (lit)"),
                                        (C_LED_A, "plastic", "Status light, amber"),
                                        (C_LED_R, "plastic", "Status light, red")]):
        dome = _ycyl(lx - 12 + 12 * k, -cd - 6.5, lz, 3.4, 1.4) + Pos(lx - 12 + 12 * k, -cd - 7.2, lz) * Sphere(3.0)
        dome &= _box(lx - 12 + 12 * k, -cd - 7.0, lz, 8, 4.0, 8)
        add(nm, dome, col, mat, 7, "shell", EP)

    # controller board with relays (BOM 6), same envelopes as model.py
    EB = (0, -180, 0)
    pcb = _box(cxx, -8, czz, cw - 24, 3, ch - 30)
    pcb = _fillet_try(pcb, _edges_par(pcb, Axis.Y), [3.0, 2.0])
    add("Controller board PCB", pcb, C_PCB, "plastic", 6, "internal", EB)
    mcu = _box(cxx - 50, -12, czz + 60, 40, 6, 40) + _box(cxx - 50, -18.5, czz + 64, 30, 7, 26)
    add("Microcontroller module", mcu, C_CHIP, "plastic", 6, "internal", EB)
    shield = _box(cxx - 50, -22.5, czz + 64, 30, 1.0, 26)
    add("Microcontroller shield can", shield, C_METAL, "metal", 6, "internal", EB)
    relay = _box(cxx + 40, -24, czz + 50, 28, 30, 20)
    relay = _fillet_try(relay, relay.edges(), [1.2, 0.6])
    add("Series trip relay", relay, C_RELAY, "plastic", 6, "internal", EB)
    frelay = _box(cxx + 40, -24, czz + 10, 28, 30, 20)
    frelay = _fillet_try(frelay, frelay.edges(), [1.2, 0.6])
    add("Fan interlock relay and valve driver", frelay, C_RELAY, "plastic", 6, "internal", EB)
    rlab = _box(cxx + 40, -39.2, czz + 50, 18, 0.4, 10) + _box(cxx + 40, -39.2, czz + 10, 18, 0.4, 10)
    add("Relay labels", rlab, C_LABEL, "paper", 6, "internal", EB)
    term = _box(cxx, -16, czz - 90, 150, 14, 18)
    for k in range(10):
        term -= _box(cxx - 67.5 + 15 * k, -23.5, czz - 86, 6, 2.0, 5)
    add("Terminal strip", term, C_TERM, "plastic", 6, "internal", EB)
    tscr = None
    for k in range(10):
        s = _ycyl(cxx - 67.5 + 15 * k, -23.4, czz - 96, 2.2, 1.0)
        tscr = s if tscr is None else tscr + s
    add("Terminal screws", tscr, C_METAL, "metal", 6, "internal", EB)
    caps = _zcyl(cxx - 5, -18, czz + 20, 5.0, 14) + _zcyl(cxx - 5, -18, czz - 10, 4.0, 10) \
        + _box(cxx - 55, -11, czz - 20, 14, 3, 14) + _box(cxx - 55, -11, czz + 5, 10, 2, 10)
    add("Board components", caps, C_CHIP, "plastic", 6, "internal", EB)

    # cable glands on the controller (BOM 5)
    gl = None
    for x, y, z, sgn in [(cxx - 60, -45, czz - ch / 2, -1), (cxx, -45, czz - ch / 2, -1),
                         (cxx + 60, -10 - 12, czz + ch / 2, 1)]:
        g = _hex_z(x, y, z + sgn * 2.5, 22.0, 5.0) + _zcyl(x, y, z + sgn * 9.0, 9.0, 8.0)
        g = _fillet_try(g, (_bottom(g) if sgn < 0 else _top(g)), [2.0, 1.0])
        gl = g if gl is None else gl + g
    add("Controller cable glands", gl, C_DARK, "plastic", 5, "shell", (0, 0, 0))

    # bump test port beside the controller (BOM 15), from model.py bump_kit
    port_x, port_z = cxx - cw / 2 - 20, czz - 60
    brk = _box(cxx - cw / 2 - 10, -20, port_z, 20, 40, 30)
    brk = _fillet_try(brk, _edges_par(brk, Axis.Y), [2.0, 1.0])
    add("Test port bracket", brk, C_SHELL2, "plastic", 15, "shell", (-60, 0, 0))
    bulk = _ycyl(port_x, -40, port_z, 8, 30)
    bulk += Pos(port_x, -44, port_z) * Rot(90, 0, 0) * extrude(RegularPolygon(10.4, 6), amount=4)
    add("Bump test port body", bulk, C_METAL, "metal", 15, "shell", (-60, -60, 0))
    cap = _ycyl(port_x, -60, port_z, 10, 10)
    cap = _fillet_try(cap, _front(cap), [2.5, 1.5])
    add("Bump test port dust cap", cap, C_ACCENT, "rubber", 15, "shell", (-60, -110, 0))

    # ------------------------------------------------------------ solenoid valve (BOM 11)
    vx, vy, vz = Pv["valve_x"], P["store_y"], P["supply_z"]
    vw, vd, vh = P["valve"]
    cr, cl = P["coil"]
    vb = _box(vx, vy, vz, vw, vd, vh)
    vb = _fillet_try(vb, vb.edges(), [3.0, 2.0, 1.0])
    add("Solenoid valve body (brass)", vb, C_BRASS, "metal", 11, "accessory", (-230, 0, -40))
    stubs = _xcyl(vx, vy, vz, 7, vw + 24)
    stubs += _hex_x(vx - vw / 2 - 8, vy, vz, 17.0, 8.0) + _hex_x(vx + vw / 2 + 8, vy, vz, 17.0, 8.0)
    add("Valve port fittings", stubs, C_BRASS, "metal", 11, "accessory", (-230, 0, -40))
    coil = _zcyl(vx, vy, vz + vh / 2 + cl / 2, cr / 2, cl)
    coil = _fillet_try(coil, coil.edges(), [3.0, 2.0])
    add("Valve coil (24 V DC)", coil, C_BLACK, "plastic", 11, "accessory", (-230, 0, 70))
    clab = Pos(vx, vy, vz + vh / 2 + cl / 2) * (Cylinder(cr / 2 + 0.3, 22) - Cylinder(cr / 2 - 1, 24))
    clab &= _box(vx, vy - cr / 2, vz + vh / 2 + cl / 2, cr * 0.8, cr, 30)
    add("Valve coil label", clab, C_LABEL, "paper", 11, "accessory", (-230, 0, 70))
    con = _box(vx, vy, vz + vh / 2 + cl + 10, 30, 30, 20)
    con = _fillet_try(con, con.edges(), [2.0, 1.0])
    con += _zcyl(vx, vy, vz + vh / 2 + cl + 21.0, 3.2, 2.0)
    add("Valve coil connector", con, C_DARK, "plastic", 11, "accessory", (-230, 0, 140))

    # ------------------------------------------------------------ context (not in the BOM)
    wt = P["wall_t"]
    z0 = PANEL_Z0
    zc = HEAD_AT[1]
    hp0, hp1 = hx - HEAD_PANEL_W / 2, hx + HEAD_PANEL_W / 2
    cp0, cp1, cpt = CTRL_PANEL
    wall = _box(hx, wt / 2, (z0 + zc) / 2, HEAD_PANEL_W, wt, zc - z0)
    wall += _box((cp0 + cp1) / 2, wt / 2, (z0 + cpt) / 2, cp1 - cp0, wt, cpt - z0)
    add("Wall panels (painted plaster)", wall, C_WALL, "paper", None, "context", (0, 0, 0))
    ceil = _box(hx, (wt - CEIL_DEPTH) / 2, zc + 20, HEAD_PANEL_W, wt + CEIL_DEPTH, 40)
    add("Ceiling section", ceil, C_CEIL, "paper", None, "context", (0, 0, 0))

    r_c = 6.0
    cone = vz + vh / 2 + cl + 22
    conduit = _pipe([(hx, hy, gz + 13), (hx, hy, zc + 1)], 4.0)
    conduit += _pipe([(vx, vy, cone), (vx, vy, cone + 20), (vx, -10, cone + 20), (vx, -10, z0 + 1)], r_c)
    conduit += _pipe([(cxx + 60, -22, czz + ch / 2 + 13), (cxx + 60, -22, cpt - 1)], r_c)
    conduit += _pipe([(cxx - 60, -45, czz - ch / 2 - 13), (cxx - 60, -45, z0 + 1)], r_c)
    conduit += _pipe([(cxx, -45, czz - ch / 2 - 13), (cxx, -45, z0 + 1)], r_c)
    add("Surface conduit and cables", conduit, C_CONDUIT, "plastic", 13, "context", (0, 0, 0))

    rt = P["tube_od"] / 2
    nx = hx + P["cup"][0] / 2 + 10
    run = _pipe([(port_x, -25, port_z + 15), (port_x, -25, cpt - 1)], rt)
    run += _pipe([(nx, hy, nz), (nx, -25, nz), (nx, -25, zc - 1)], rt)
    add("Bump test tube (4 mm)", run, C_TUBE, "plastic", 15, "context", (0, 0, 0))

    sup = _pipe([(hp0 + 1, vy, vz), (vx - vw / 2 - 12, vy, vz)], 4.0)
    sup += _pipe([(vx + vw / 2 + 12, vy, vz), (hp1 - 40, vy, vz), (hp1 - 40, vy, z0 + 1)], 4.0)
    add("Hydrogen supply line (stainless)", sup, C_PIPE, "metal", None, "context", (0, 0, 0))
    pclip = None
    for (x, z) in [(hp0 + 25, vz), (hp1 - 40, vz - 90)]:
        c = _box(x, vy / 2, z, 12, abs(vy), 10) + _xcyl(x, vy, z, 7.0, 12) - _xcyl(x, vy, z, 4.0, 14)
        pclip = c if pclip is None else pclip + c
    add("Pipe stand-off clips", pclip, C_METAL, "metal", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
