"""H2Guard parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    h2guard-assembly.step / .stl   every H2Guard part in place in the 30 m3 reference room
    detector-head.step / .stl      detector head with sensors, flame arrestors and bump test cup
    controller.step / .stl         controller enclosure, board, front panel and bump test port
    exhaust-fan.step / .stl        inside grille, wall sleeve with fan, weather hood

Axes: the back wall of the reference room lies in the XZ plane with its inside face at
Y = 0; the room extends to negative Y. The side wall with the make-up air grille is at X = 0
(inside face). Floor at Z = 0, ceiling at Z = room[2]. Units are mm.
Main dimensions and interfaces only: device envelopes, mounting heights, sensor ports,
bump test cup and tube, fan sleeve, valve ports. Not fabrication detail; not for
fabrication. The same PARAMS feed docs/04-calcs/sizing.py (HGD-CAL-001) and the drawing
HGD-DWG-001 (cad/src/sheets.py). Grey context (room, bench, apparatus, gas store, supply
line, cables) is built by context() and is not in the BOM.
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # reference room: 4 x 3 x 2.5 m = 30 m3 (HGD-REQ-001 assumptions)
    "room": (4000.0, 3000.0, 2500.0), "wall_t": 150.0,
    # context: bench and the apparatus whose fittings are the likely leak source
    "bench": (1200.0, 650.0, 900.0), "bench_x": 2000.0,
    "apparatus": (350.0, 300.0, 250.0), "app_x": 1700.0,
    # 1 detector head enclosure (outer), wall thickness, gap from ceiling to top of the head
    "head": (110.0, 80.0, 90.0), "head_wall": 3.0, "head_ceiling_gap": 85.0, "head_y": -40.0,
    "port_d": 26.0, "port_dx": 22.0,          # two sensor ports in the floor of the head
    # 2 catalytic sensor can, 3 MOS sensor can
    "cat": (20.0, 17.0), "mos": (9.2, 8.0),
    # 4 flame arrestor discs (sintered stainless) and the drip skirt that doubles as the bump test cup
    "disc": (25.0, 2.0), "cup": (96.0, 66.0, 22.0), "cup_wall": 2.0,
    "board_gap": 22.0,                        # head floor (inside) to underside of the sensor carrier board
    # 5 controller enclosure; center height keeps its top at least 1 m below the ceiling
    "ctrl": (200.0, 90.0, 250.0), "ctrl_x": 3300.0, "ctrl_z": 1350.0,
    # 8 power supply on the floor by the mains outlet
    "psu": (160.0, 70.0, 40.0), "psu_x": 3450.0,
    # 9 exhaust fan: inside grille, 150 mm duct sleeve through the wall, weather hood
    "fan_x": 2600.0, "fan_z": 2300.0, "fan_d": 150.0, "grille": (240.0, 12.0),
    "fan_body": (170.0, 110.0), "hood": (220.0, 220.0, 160.0),
    # 10 make-up air grille, low on the side wall on the far side of the room from the fan
    "inlet": (300.0, 160.0), "inlet_y": -1500.0, "inlet_z": 200.0,
    # 11 normally closed solenoid valve on the supply line
    "valve_x": 950.0, "valve": (60.0, 45.0, 45.0), "coil": (44.0, 60.0),
    # 12 sounder and beacon by the door, top at least 0.3 m below the ceiling
    "beacon_x": 3800.0, "beacon_z": 2000.0,
    # 15 bump test port at the controller and 4 mm tube up to the cup
    "tube_od": 4.0, "tube_id": 2.5,
    # context: small gas store with regulator and flow restrictor (gas system, not H2Guard)
    "store_x": 650.0, "store_y": -170.0, "supply_z": 1300.0,
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    rx, ry, rz = p["room"]
    hw, hd, hh = p["head"]
    head_z = rz - p["head_ceiling_gap"] - hh / 2
    port_face = head_z - hh / 2                               # underside of the head, where gas enters
    cup_bot = port_face - p["cup"][2]
    bw, bd, bh = p["bench"]
    src_z = bh + p["apparatus"][2]                            # top of the apparatus: leak source height
    cw, cd, ch = p["ctrl"]
    ctrl_top = p["ctrl_z"] + ch / 2
    # bump test tube: up beside the controller, along under the ceiling, down to the cup nozzle (as bump_kit)
    tube_run = ((rz - 60 - (p["ctrl_z"] - 45)) + abs((p["ctrl_x"] - cw / 2 - 20) - (p["app_x"] + p["cup"][0] / 2 + 10))
                + (rz - 60 - (port_face - 8)) + abs(-25 - p["head_y"]))
    cupx, cupy, cupz = p["cup"]
    t = p["cup_wall"]
    return {
        "room_m3": rx * ry * rz / 1e9, "ceiling_m2": rx * ry / 1e6,
        "head_z": head_z, "port_face": port_face, "port_below_ceiling": rz - port_face,
        "cup_bot": cup_bot,
        # gap between the top of the arrestor disc and the sensor can, and the gas cavity it makes
        "sensor_gap": p["board_gap"] - 0.8 - p["cat"][1] - p["disc"][1],
        "sensor_cavity_ml": math.pi / 4 * p["disc"][0] ** 2 * (p["board_gap"] - 0.8 - p["cat"][1] - p["disc"][1]) / 1e3,
        "cup_ml": (cupx - 2 * t) * (cupy - 2 * t) * (cupz - t) / 1e3,
        "src_z": src_z, "plume_rise": port_face - src_z, "src_to_ceiling": rz - src_z,
        "ctrl_top": ctrl_top, "ctrl_below_ceiling": rz - ctrl_top,
        "fan_top": p["fan_z"] + p["grille"][0] / 2, "fan_below_ceiling": rz - p["fan_z"] - p["grille"][0] / 2,
        "beacon_top": p["beacon_z"] + 50.0, "beacon_below_ceiling": rz - p["beacon_z"] - 50.0,
        "sleeve_len": p["wall_t"] + 40.0,
        "tube_run": tube_run, "tube_ml": math.pi / 4 * p["tube_id"] ** 2 * tube_run / 1e3,
        "fan_to_inlet_x": p["fan_x"],
    }


def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def zcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def ycyl(x, y, z, r, h):
    """Cylinder with its axis along Y."""
    b = _b3d()
    return b.Pos(x, y, z) * b.Rot(90, 0, 0) * b.Cylinder(r, h)


def tube(a, c, r):
    b = _b3d()
    a, c = b.Vector(*a), b.Vector(*c)
    d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def path(points, r):
    return fuse(tube(a, c, r) for a, c in zip(points, points[1:]))


def build_parts(p=PARAMS):
    """Return {key: solid} for the H2Guard parts (BOM lines 1 to 12 and 15)."""
    b = _b3d()
    D = derived(p)
    rx, ry, rz = p["room"]
    parts = {}

    # 1 Detector head: open-bottom box body with two ports in its floor and a cable gland on top
    hx, hy, hz = p["app_x"], p["head_y"], D["head_z"]
    hw, hd, hh = p["head"]
    t = p["head_wall"]
    body = box(hx, hy, hz, hw, hd, hh) - box(hx, hy, hz, hw - 2 * t, hd - 2 * t, hh - 2 * t)
    for dx in (-p["port_dx"], p["port_dx"]):
        body = body - zcyl(hx + dx, hy, hz - hh / 2 + t / 2, p["port_d"] / 2, t + 2)
    body = body + zcyl(hx, hy, hz + hh / 2 + 6, 9, 12)                      # cable gland
    body = body + box(hx, -t / 2 - 2, hz, hw + 30, 4, hh)                   # wall plate
    parts["head"] = body
    # 2 Catalytic sensor can over the left port on a carrier board; 3 MOS sensor over the right port
    cd_, ch_ = p["cat"]
    board = box(hx, hy, hz - hh / 2 + t + p["board_gap"], hw - 2 * t - 4, hd - 2 * t - 4, 1.6)
    parts["cat"] = zcyl(hx - p["port_dx"], hy, hz - hh / 2 + t + p["board_gap"] - ch_ / 2 - 0.8, cd_ / 2, ch_) + board
    md_, mh_ = p["mos"]
    parts["mos"] = zcyl(hx + p["port_dx"], hy, hz - hh / 2 + t + p["board_gap"] - mh_ / 2 - 0.8, md_ / 2, mh_)
    # 4 Flame arrestor discs in both ports, and the drip skirt that forms the bump test cup
    dd, dt = p["disc"]
    discs = fuse(zcyl(hx + dx, hy, hz - hh / 2 + t + dt / 2, dd / 2, dt) for dx in (-p["port_dx"], p["port_dx"]))
    cx_, cy_, cz_ = p["cup"]
    w = p["cup_wall"]
    cup = box(hx, hy, D["port_face"] - cz_ / 2, cx_, cy_, cz_) - box(hx, hy, D["port_face"] - cz_ / 2 - w / 2, cx_ - 2 * w, cy_ - 2 * w, cz_ - w + 0.01)
    cup = cup + tube((hx + cx_ / 2 - 1, hy, D["port_face"] - 8), (hx + cx_ / 2 + 10, hy, D["port_face"] - 8), 3)   # gas nozzle
    parts["arrest"] = discs + cup

    # 5 Controller enclosure (open front), 6 board inside, 7 front panel
    cw, cd, ch = p["ctrl"]
    cxx, czz = p["ctrl_x"], p["ctrl_z"]
    parts["ctrl"] = box(cxx, -cd / 2 + 2, czz, cw, cd - 4, ch) - box(cxx, -cd / 2, czz, cw - 6, cd - 4, ch - 6)
    parts["board"] = (box(cxx, -8, czz, cw - 24, 3, ch - 30)
                      + box(cxx - 50, -18, czz + 60, 40, 18, 40)        # MCU module
                      + box(cxx + 40, -24, czz + 50, 28, 30, 20)        # comparator trip relay
                      + box(cxx + 40, -24, czz + 10, 28, 30, 20)        # valve and fan drivers
                      + box(cxx, -16, czz - 90, 150, 14, 18))           # terminal strip
    parts["panel"] = (box(cxx, -cd - 2, czz, cw, 4, ch)
                      + box(cxx, -cd - 6, czz + 60, 90, 4, 45)          # display
                      + ycyl(cxx - 50, -cd - 12, czz - 40, 12, 16)      # key-switch reset
                      + ycyl(cxx + 10, -cd - 8, czz - 40, 9, 8)         # test button
                      + box(cxx + 55, -cd - 7, czz - 40, 40, 6, 12))    # status lights
    # 8 Power supply brick on the floor by the outlet
    pw, pd, ph = p["psu"]
    parts["psu"] = box(p["psu_x"], -110, ph / 2, pw, pd, ph)

    # 9 Exhaust fan: inside grille, sleeve with the fan through the wall, weather hood outside
    fx, fz = p["fan_x"], p["fan_z"]
    gs, gt = p["grille"]
    fr = p["fan_d"] / 2
    grille = box(fx, -gt / 2, fz, gs, gt, gs) - ycyl(fx, -gt / 2, fz, fr, gt + 2)
    grille = grille + fuse(box(fx, -gt / 2, fz + dz, 2 * fr, 3, 4) for dz in (-50, -25, 0, 25, 50))
    sl = D["sleeve_len"]
    sleeve = ycyl(fx, sl / 2 - 20, fz, fr + 3, sl) - ycyl(fx, sl / 2 - 20, fz, fr, sl + 2)
    fb_d, fb_l = p["fan_body"]
    motor = ycyl(fx, p["wall_t"] / 2, fz, fb_d / 2 - 12, fb_l) + ycyl(fx, p["wall_t"] / 2, fz, 30, fb_l + 10)
    hwid, hdep, hht = p["hood"]
    hood_y = p["wall_t"] + hdep / 2
    hood = (box(fx, hood_y, fz + 20, hwid, hdep, hht) - box(fx, hood_y - 3, fz + 20 - 20, hwid - 6, hdep, hht))
    parts["fan"] = grille + sleeve + motor + hood

    # 10 Make-up air grille on the side wall (inside face X = 0), low level
    iw, ih = p["inlet"]
    parts["inlet"] = box(6, p["inlet_y"], p["inlet_z"], 12, iw, ih) - box(6, p["inlet_y"], p["inlet_z"], 14, iw - 30, ih - 30) \
        + fuse(box(6, p["inlet_y"], p["inlet_z"] + dz, 4, iw - 30, 3) for dz in (-40, -15, 10, 35))

    # 11 Normally closed solenoid valve: brass body with 1/4 in ports, coil and connector
    vx, vy, vz = p["valve_x"], p["store_y"], p["supply_z"]
    vw, vd, vh = p["valve"]
    cr, cl = p["coil"]
    parts["valve"] = (box(vx, vy, vz, vw, vd, vh) + zcyl(vx, vy, vz + vh / 2 + cl / 2, cr / 2, cl)
                      + box(vx, vy, vz + vh / 2 + cl + 10, 30, 30, 20)
                      + tube((vx - vw / 2 - 12, vy, vz), (vx + vw / 2 + 12, vy, vz), 7))
    # 12 Sounder and beacon by the door
    bx, bz = p["beacon_x"], p["beacon_z"]
    parts["beacon"] = box(bx, -25, bz, 100, 50, 100) + ycyl(bx, -80, bz, 38, 60)
    b_ = _b3d()
    parts["beacon"] = parts["beacon"] + b_.Pos(bx, -110, bz) * b_.Sphere(38)

    # 15 Bump test kit: bulkhead test port with cap beside the controller, 4 mm tube up to the cup nozzle
    port, run = bump_kit(p)
    parts["bump"] = port + run
    return parts


def bump_kit(p=PARAMS):
    """BOM line 15 as (test port, tube run); the media show the tube with the cable runs."""
    D = derived(p)
    cw, cd, ch = p["ctrl"]
    cxx, czz = p["ctrl_x"], p["ctrl_z"]
    hx, hy = p["app_x"], p["head_y"]
    cx_ = p["cup"][0]
    rz = p["room"][2]
    port = ycyl(cxx - cw / 2 - 20, -40, czz - 60, 8, 30) + ycyl(cxx - cw / 2 - 20, -60, czz - 60, 10, 10)
    port = port + box(cxx - cw / 2 - 10, -20, czz - 60, 20, 40, 30)
    r = p["tube_od"] / 2
    nz = D["port_face"] - 8
    run = path([(cxx - cw / 2 - 20, -25, czz - 45), (cxx - cw / 2 - 20, -25, rz - 60),
                (hx + cx_ / 2 + 10, -25, rz - 60), (hx + cx_ / 2 + 10, -25, nz),
                (hx + cx_ / 2 + 10, hy, nz)], r)
    return port, run


BOM_ORDER = [("head", 1), ("cat", 2), ("mos", 3), ("arrest", 4), ("ctrl", 5), ("board", 6), ("panel", 7),
             ("psu", 8), ("fan", 9), ("inlet", 10), ("valve", 11), ("beacon", 12), ("bump", 15)]


def context(p=PARAMS):
    """Grey context, not in the BOM: {name: solid} for room, bench and apparatus, gas store and supply, cables."""
    b = _b3d()
    D = derived(p)
    rx, ry, rz = p["room"]
    wt = p["wall_t"]
    back = box(rx / 2, wt / 2, rz / 2, rx, wt, rz)
    back = back - ycyl(p["fan_x"], wt / 2, p["fan_z"], p["fan_d"] / 2 + 3, wt + 2)
    side = box(-wt / 2, -ry / 2 + wt / 2, rz / 2, wt, ry + wt, rz)
    side = side - box(-wt / 2, p["inlet_y"], p["inlet_z"], wt + 2, p["inlet"][0] - 30, p["inlet"][1] - 30)
    floor = box(rx / 2, -ry / 2, -15, rx, ry, 30)
    outlet = box(p["psu_x"] + 120, -12, 320, 80, 24, 120)
    bw, bd, bh = p["bench"]
    bench = box(p["bench_x"], -bd / 2, bh - 20, bw, bd, 40)
    for dx in (-bw / 2 + 40, bw / 2 - 40):
        for dy in (-bd + 30, -30):
            bench = bench + box(p["bench_x"] + dx, dy, (bh - 40) / 2, 40, 40, bh - 40)
    aw, ad, ah = p["apparatus"]
    bench = bench + box(p["app_x"], -ad / 2 - 150, bh + ah / 2, aw, ad, ah)
    sx, sy = p["store_x"], p["store_y"]
    store = (zcyl(sx, sy, 450, 90, 900) + b.Pos(sx, sy, 900) * b.Sphere(90) + zcyl(sx, sy, 1010, 18, 60)
             + box(sx, sy, 1060, 70, 60, 50) + box(sx, -45, 700, 200, 90, 20))
    sz = p["supply_z"]
    supply = path([(sx, sy, 1085), (sx, sy, sz), (p["app_x"] - 100, sy, sz), (p["app_x"] - 100, sy, D["src_z"] - 20)], 4)
    tr = rz - 40
    cx, cz = p["ctrl_x"], p["ctrl_z"]
    cables = (path([(p["valve_x"], -10, sz + 110), (p["valve_x"], -10, tr), (cx + 60, -10, tr), (cx + 60, -10, cz + 125)], 5)
              + path([(p["app_x"], -10, D["head_z"] + 57), (p["app_x"], -10, tr)], 5)
              + path([(p["fan_x"], -10, p["fan_z"] + 130), (p["fan_x"], -10, tr)], 5)
              + path([(p["beacon_x"], -10, p["beacon_z"] + 50), (p["beacon_x"], -10, tr)], 5)
              + path([(p["valve_x"], p["store_y"] + 20, sz + 100), (p["valve_x"], -10, sz + 110)], 5)
              + path([(p["psu_x"], -110, 40), (p["psu_x"], -60, 120), (cx + 60, -60, 120), (cx + 60, -60, cz - 125)], 4)
              + path([(p["psu_x"] + 80, -110, 20), (p["psu_x"] + 120, -30, 300)], 4))
    return {"room": back + side + floor + outlet, "bench": bench, "store": store + supply, "cables": cables}


def assembly(p=PARAMS, with_room=False):
    b = _b3d()
    parts = build_parts(p)
    kids = list(parts.values())
    if with_room:
        kids += list(context(p).values())
    return b.Compound(children=kids)


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    P = build_parts()
    groups = {
        "h2guard-assembly": list(P.values()),
        "detector-head": [P[k] for k in ("head", "cat", "mos", "arrest")],
        "controller": [P[k] for k in ("ctrl", "board", "panel")],
        "exhaust-fan": [P["fan"]],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"))
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"room {D['room_m3']:.1f} m3; sensor ports {D['port_below_ceiling']:.0f} mm below the ceiling; "
          f"leak source {D['src_z']:.0f} mm above the floor, {D['plume_rise']:.0f} mm below the ports")
    print(f"controller top {D['ctrl_below_ceiling']:.0f} mm below the ceiling; fan grille top {D['fan_below_ceiling']:.0f} mm; "
          f"beacon top {D['beacon_below_ceiling']:.0f} mm")
    print(f"bump test cup {D['cup_ml']:.0f} mL; tube {D['tube_run']:.0f} mm, {D['tube_ml']:.1f} mL")
