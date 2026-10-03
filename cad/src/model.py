"""H2Guard parametric model (build123d), TRL 3, constructable design (HGD-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    runs the constructability checks (contacts, clearances, overlaps)

Exports:
    h2guard-assembly.step / .stl   every H2Guard part in place in the 30 m3 reference room
    detector-head.step / .stl      detector head with sensors, flame arrestors, bump test cup and ceiling drop rod
    controller.step / .stl         controller enclosure, mounting plate, modules, dry-contact relay, lid and front panel
    exhaust-fan.step / .stl        fan plate, fan, wall sleeve, inside grille, shutter, weather hood and pressure switch

Axes: the back wall of the reference room lies in the XZ plane with its inside face at
Y = 0; the room extends to negative Y. The side wall with the make-up air grille is at X = 0
(inside face). Floor at Z = 0, ceiling at Z = room[2]. Units are mm.

build_components() returns every part a maker handles (made, drilled or bought, with the
fixings that hold them), so the build plan pictures (cad/src/build_plan_media.py) and the
checks work part by part. build_parts() fuses them by BOM line for the concept media.
The same PARAMS feed docs/04-calcs/sizing.py (HGD-CAL-001) and the drawing HGD-DWG-001
(cad/src/sheets.py). Grey context (room, bench, apparatus, gas store, supply line, cables)
is built by context() and is not in the BOM. Not for fabrication.
"""
import math
import sys
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # reference room: 4 x 3 x 2.5 m = 30 m3 (HGD-REQ-001 assumptions)
    "room": (4000.0, 3000.0, 2500.0), "wall_t": 150.0,
    # context: bench and the apparatus whose fittings are the likely leak source
    "bench": (1200.0, 650.0, 900.0), "bench_x": 2000.0,
    "apparatus": (350.0, 300.0, 250.0), "app_x": 1700.0, "app_y": -300.0,   # apparatus centre (its fittings are the leak point)
    # 1 detector head enclosure (outer, lid included), wall thickness, gap from ceiling to top of the head;
    # the head hangs on the ceiling drop rod with its ports directly over the apparatus (HGD-DEC-001, decision 2)
    "head": (110.0, 80.0, 90.0), "head_wall": 3.0, "head_ceiling_gap": 85.0, "head_y": -300.0,
    "port_d": 22.0, "port_dx": 22.0,          # two sensor ports in the floor; the 25 mm disc rests on the 1.5 mm ledge
    "gland_dx": -38.0,                        # head cable gland, offset from the drop rod in the top of the head
    # 17 ceiling drop rod: 1/2 in steel pipe nipple (OD, wall, length) in a 1/2 in floor flange used as the ceiling plate
    "drop_pipe": (21.3, 2.8, 89.0), "drop_flange": (80.0, 5.0, 32.0, 15.0), "drop_pcd": 60.0, "drop_nut": (30.0, 4.0),
    # 2 catalytic sensor can, 3 MOS sensor can
    "cat": (20.0, 17.0), "mos": (9.2, 8.0),
    # 4 flame arrestor discs (sintered stainless) and the drip skirt that doubles as the bump test cup
    "disc": (25.0, 2.0), "cup": (96.0, 66.0, 22.0), "cup_wall": 2.0,
    "board_gap": 22.0,                        # head floor (inside) to underside of the sensor carrier board = standoff length
    "sensor_board": (100.0, 70.0, 1.6), "standoff_xy": (40.0, 25.0),
    # 5 controller enclosure; center height keeps its top at least 1 m below the ceiling
    "ctrl": (200.0, 90.0, 250.0), "ctrl_x": 3300.0, "ctrl_z": 1350.0, "ctrl_lid_t": 4.0,
    "boss_xz": (80.0, 100.0),                 # moulded bosses inside the controller back wall
    "mplate": (176.0, 220.0, 2.0),            # controller mounting plate (aluminium)
    # 8 power supply on the floor by the mains outlet
    "psu": (160.0, 70.0, 40.0), "psu_x": 3450.0,
    # 9 exhaust fan: 150 mm spigots, body in a 200 mm wall sleeve, held by the fan plate on the inside wall
    "fan_x": 2600.0, "fan_z": 2300.0, "fan_d": 150.0, "grille": (240.0, 12.0),
    "fan_body": (170.0, 110.0), "hood": (220.0, 220.0, 160.0),
    "sleeve": (200.0, 4.0), "fan_plate": (240.0, 3.0),
    # 10 make-up air grille, low on the side wall on the far side of the room from the fan
    "inlet": (300.0, 160.0), "inlet_y": -1500.0, "inlet_z": 200.0,
    # 11 normally closed solenoid valve on the supply line, on a bent flat-bar bracket
    "valve_x": 950.0, "valve": (60.0, 45.0, 45.0), "coil": (44.0, 60.0), "valve_bar": (40.0, 5.0),
    # 12 sounder and beacon by the door, top at least 0.3 m below the ceiling
    "beacon_x": 3800.0, "beacon_z": 2000.0,
    # 15 bump test port on an angle bracket beside the controller, 4 mm tube up to the cup
    "tube_od": 4.0, "tube_id": 2.5, "test_x": 3165.0, "test_z": 1250.0,
    # 18 differential pressure switch beside the fan; its low port is tubed to a static tap in the fan inlet
    "dps_x": 2370.0, "dps_z": 2330.0, "dps": (85.0, 55.0, 85.0), "dp_tube": (6.0, 4.0), "dp_tap_dz": -62.0,
    # 20 oxygen sensor option (inert gas cylinders in the room): transmitter on the back wall, cell at breathing height
    "o2_x": 2850.0, "o2_z": 1560.0, "o2_box": (80.0, 55.0, 110.0), "o2_cell": (30.0, 25.0),
    # context: small gas store with regulator and flow restrictor (gas system, not H2Guard)
    "store_x": 650.0, "store_y": -170.0, "supply_z": 1300.0,
}


def tube_points(p=PARAMS):
    """Centre line of the bump test tube: test port, up the wall, along the wall under the ceiling,
    out across the ceiling to the head on its drop rod, down to the cup."""
    rz = p["room"][2]
    tx, tz = p["test_x"], p["test_z"]
    hx, hy = p["app_x"], p["head_y"]
    port_face = rz - p["head_ceiling_gap"] - p["head"][2]
    nz = port_face - p["cup"][2] / 2 + 1          # nozzle height on the cup side
    xe = hx + p["cup"][0] / 2 + 20                # end of the push-in fitting
    xr = xe + 17                                  # vertical run beside the head
    run_z = rz - 60
    cz = rz - p["tube_od"]                        # run on the ceiling, held by ceiling clips
    return [(tx, -18, tz + 20), (tx, -18, tz + 40), (tx, -2, tz + 60), (tx, -2, run_z), (xr, -2, run_z),
            (xr, -2, cz), (xr, hy, cz), (xr, hy, nz), (xe, hy, nz)]


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
    pts = tube_points(p)
    tube_run = sum(math.dist(a, c) for a, c in zip(pts, pts[1:]))
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
        # horizontal distance from the centre of the two sensor ports to the apparatus centre (the leak point)
        "port_offset": math.hypot(p["app_x"] - p["app_x"], p["head_y"] - p["app_y"]),
        "drop_visible": p["head_ceiling_gap"] - p["drop_flange"][1] - p["drop_flange"][3] - p["drop_nut"][1],
        "ctrl_top": ctrl_top, "ctrl_below_ceiling": rz - ctrl_top,
        "fan_top": p["fan_z"] + p["grille"][0] / 2, "fan_below_ceiling": rz - p["fan_z"] - p["grille"][0] / 2,
        "beacon_top": p["beacon_z"] + 50.0, "beacon_below_ceiling": rz - p["beacon_z"] - 50.0,
        "sleeve_len": p["wall_t"] + 40.0,     # 150 mm air path through the fan and its spigots
        "tube_run": tube_run, "tube_ml": math.pi / 4 * p["tube_id"] ** 2 * tube_run / 1e3,
        "fan_to_inlet_x": p["fan_x"],
        "o2_cell_z": p["o2_z"] - p["o2_box"][2] / 2 - p["o2_cell"][1] / 2,
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


def xcyl(x, y, z, r, h):
    """Cylinder with its axis along X."""
    b = _b3d()
    return b.Pos(x, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, h)


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


def path(points, r, joints=False):
    b = _b3d()
    s = fuse(tube(a, c, r) for a, c in zip(points, points[1:]))
    if joints:
        s = fuse([s] + [b.Pos(*q) * b.Sphere(r) for q in points[1:-1]])
    return s


def _clip(pt, along, r):
    """Saddle clip for the 4 mm tube on the wall: 8 mm along the run, 10 across, 6 deep, tube bore cut out."""
    x, y, z = pt
    if along == "x":
        c = box(x, -3, z, 8, 6, 10) - xcyl(x, y, z, r, 10)
    else:
        c = box(x, -3, z, 10, 6, 8) - zcyl(x, y, z, r, 10)
    return c


def _cclip(pt, r, rz):
    """Ceiling clip for the 4 mm tube running along Y: 8 mm along the run, 10 across, 6 deep, bore cut out."""
    x, y, z = pt
    return box(x, y, rz - 3, 10, 8, 6) - ycyl(x, y, z, r, 10)


def build_components(p=PARAMS):
    """Every part a maker handles, by name: {key: solid}. Fixings are grouped with the part they hold."""
    b = _b3d()
    D = derived(p)
    rz = p["room"][2]
    C = {}

    # ---- 1 detector head: bought box with its lid on the room-side face, drilled, hung on the drop rod
    hx, hy, hz = p["app_x"], p["head_y"], D["head_z"]
    hw, hd, hh = p["head"]
    t = p["head_wall"]
    pf = D["port_face"]
    top = hz + hh / 2
    fl = pf + t                                   # inside face of the floor
    y0 = hy + hd / 2                              # back face of the box (the lid face is at y0 - hd)
    gx = hx + p["gland_dx"]
    # cavity runs from the open front (lid face) back to the inside of the back wall
    body = box(hx, y0 - (hd - t) / 2, hz, hw, hd - t, hh) - box(hx, y0 + (-(hd - t) - 0.01 - t) / 2, hz, hw - 2 * t, hd - 2 * t + 0.01, hh - 2 * t)
    for dx in (-p["port_dx"], p["port_dx"]):
        body = body - zcyl(hx + dx, hy, pf + t / 2, p["port_d"] / 2, t + 2)
    po, pw_, pl_ = p["drop_pipe"]
    body = body - zcyl(hx, hy, top - t / 2, po / 2 + 0.2, t + 2)              # drop rod hole in the top, centred
    body = body - zcyl(gx, hy, top - t / 2, 8.1, t + 2)                      # gland hole in the top
    sx, sy = p["standoff_xy"]
    so = [(hx + i * sx, hy + j * sy) for i in (-1, 1) for j in (-1, 1)]
    for x, y in so:
        body = body - zcyl(x, y, pf + t / 2, 1.7, t + 2)                     # holes for the standoff screws
    C["head_body"] = body
    C["head_lid"] = box(hx, y0 - hd + t / 2, hz, hw, t, hh)
    C["head_gland"] = zcyl(gx, hy, top + 6, 9, 12) + zcyl(gx, hy, top - t - 2, 10.5, 4) + zcyl(gx, hy, top - t / 2, 8.0, t)

    # ---- 17 ceiling drop rod: floor flange screwed to the ceiling, pipe nipple, locknuts either side of the head top
    fd, ft, hubd, hubh = p["drop_flange"]
    fl_ = zcyl(hx, hy, rz - ft / 2, fd / 2, ft) + (zcyl(hx, hy, rz - ft - hubh / 2, hubd / 2, hubh) - zcyl(hx, hy, rz - ft - hubh / 2, po / 2 + 0.05, hubh + 0.01))
    pcd = p["drop_pcd"] / 2
    fsc_ = [(hx + pcd * math.cos(math.radians(a)), hy + pcd * math.sin(math.radians(a))) for a in (90, 210, 330)]
    for x, y in fsc_:
        fl_ = fl_ - zcyl(x, y, rz - ft / 2, 2.75, ft + 2)
    C["drop_flange"] = fl_
    C["drop_rod"] = zcyl(hx, hy, rz - ft - pl_ / 2, po / 2, pl_) - zcyl(hx, hy, rz - ft - pl_ / 2, po / 2 - pw_, pl_ + 1)
    nd, nt = p["drop_nut"]
    C["drop_nuts"] = ((zcyl(hx, hy, top + nt / 2, nd / 2, nt) - zcyl(hx, hy, top + nt / 2, po / 2 + 0.03, nt + 1))
                      + (zcyl(hx, hy, top - t - nt / 2, nd / 2, nt) - zcyl(hx, hy, top - t - nt / 2, po / 2 + 0.03, nt + 1)))
    C["drop_screws"] = fuse(zcyl(x, y, rz - ft - 1.75, 4.5, 3.5) + zcyl(x, y, rz - ft + 20, 2.5, 40) for x, y in fsc_)

    # ---- 4 flame arrestor discs, bonded on the floor over each port (they rest on the 1.5 mm ledge)
    dd, dt = p["disc"]
    C["discs"] = fuse(zcyl(hx + dx, hy, fl + dt / 2, dd / 2, dt) for dx in (-p["port_dx"], p["port_dx"]))

    # ---- standoffs: four M3 x 22 female standoffs; the cup screws come up from below into them
    bz = fl + p["board_gap"]                      # underside of the sensor board
    C["standoffs"] = fuse(zcyl(x, y, fl + p["board_gap"] / 2, 3.0, p["board_gap"]) - zcyl(x, y, fl + p["board_gap"] / 2, 1.6, p["board_gap"] + 1) for x, y in so)

    # ---- 2, 3 sensor carrier board with the catalytic and MOS sensors under it
    bw_, bd_, bt_ = p["sensor_board"]
    board = box(hx, hy, bz + bt_ / 2, bw_, bd_, bt_)
    for x, y in so:
        board = board - zcyl(x, y, bz + bt_ / 2, 1.6, bt_ + 1)
    board = board + box(hx + 30, hy + 12, bz + bt_ + 4, 16, 12, 8) + box(hx, hy + 20, bz + bt_ + 5, 30, 10, 10)  # regulator, cable terminal
    cd_, ch_ = p["cat"]
    cat = zcyl(hx - p["port_dx"], hy, bz - ch_ / 2 - 0.8, cd_ / 2, ch_) + zcyl(hx - p["port_dx"], hy, bz - 0.4, 4, 0.8)
    md_, mh_ = p["mos"]
    mos = zcyl(hx + p["port_dx"], hy, bz - mh_ / 2 - 0.8, md_ / 2, mh_) + zcyl(hx + p["port_dx"], hy, bz - 0.4, 3, 0.8)
    C["sensor_board"] = board
    C["cat"] = cat
    C["mos"] = mos
    C["board_screws"] = fuse(zcyl(x, y, bz + bt_ + 1, 2.75, 2) + zcyl(x, y, bz + bt_ / 2 - 2.0, 1.5, bt_ + 4) for x, y in so)

    # ---- 4 bump test cup (printed): skirt with a 2 mm top plate, port openings, a side boss for the push-in fitting
    cx_, cy_, cz_ = p["cup"]
    w = p["cup_wall"]
    cup = box(hx, hy, pf - cz_ / 2, cx_, cy_, cz_) - box(hx, hy, pf - w - (cz_ - w) / 2 - 0.005, cx_ - 2 * w, cy_ - 2 * w, cz_ - w + 0.01)
    for dx in (-p["port_dx"], p["port_dx"]):
        cup = cup - zcyl(hx + dx, hy, pf - w / 2, p["port_d"] / 2, w + 2)
    for x, y in so:
        cup = cup - zcyl(x, y, pf - w / 2, 1.7, w + 2)
    nz = pf - cz_ / 2 + 1
    bx0 = hx + cx_ / 2
    cup = cup + xcyl(bx0 + 4 - w, hy, nz, 5, 8 + w)                            # boss, 8 mm proud of the side
    cup = cup - xcyl(bx0 - 2, hy, nz, 1.25, 12) - xcyl(bx0 + 5, hy, nz, 2.1, 6.01)   # gas way and M5 tapped hole
    C["cup"] = cup
    C["cup_screws"] = fuse(zcyl(x, y, pf - w - 1, 2.75, 2) + zcyl(x, y, pf - w + 6.5, 1.5, 13) for x, y in so)
    C["cup_fitting"] = xcyl(bx0 + 9, hy, nz, 4.5, 4) + xcyl(bx0 + 15.5, hy, nz, 4.0, 9) + xcyl(bx0 + 5, hy, nz, 2.1, 6)

    # ---- 5 controller enclosure: bought IP65 box, back on the wall, lid on the front; moulded bosses inside
    cw, cd, ch = p["ctrl"]
    cxx, czz = p["ctrl_x"], p["ctrl_z"]
    lt = p["ctrl_lid_t"]
    dep = cd - lt                                 # body depth 86
    ct = 3.0
    cb = box(cxx, -dep / 2, czz, cw, dep, ch) - box(cxx, (-dep - 0.01 - ct) / 2, czz, cw - 2 * ct, dep - ct + 0.01, ch - 2 * ct)
    bxo, bzo = p["boss_xz"]
    for i in (-1, 1):
        for j in (-1, 1):
            cb = cb + (ycyl(cxx + i * bxo, -ct - 3.5, czz + j * bzo, 4, 7) - ycyl(cxx + i * bxo, -ct - 3.5, czz + j * bzo, 1.4, 7.01))
    gl_top = [cxx - 60, cxx - 20, cxx + 20, cxx + 60]
    for gx in gl_top:
        cb = cb - zcyl(gx, -45, czz + ch / 2 - ct / 2, 8.1, ct + 2)
    gl_bot = [cxx - 60, cxx - 20, cxx + 20, cxx + 60]   # oxygen sensor, pressure switch, dry-contact output, supply lead
    for gx in gl_bot:
        cb = cb - zcyl(gx, -45, czz - ch / 2 + ct / 2, 8.1, ct + 2)
    wsx = [(cxx + i * 85, czz + j * 110) for i in (-1, 1) for j in (-1, 1)]
    for x, z in wsx:
        cb = cb - ycyl(x, -ct / 2, z, 2.2, ct + 2)
    C["ctrl_body"] = cb
    glands = fuse(zcyl(gx, -45, czz + ch / 2 + 7.5, 9, 15) + zcyl(gx, -45, czz + ch / 2 - ct / 2, 8.0, ct)
                  + zcyl(gx, -45, czz + ch / 2 - ct - 2, 10.5, 4) for gx in gl_top)
    glands = glands + fuse(zcyl(gx, -45, czz - ch / 2 - 7.5, 9, 15) + zcyl(gx, -45, czz - ch / 2 + ct / 2, 8.0, ct)
                           + zcyl(gx, -45, czz - ch / 2 + ct + 2, 10.5, 4) for gx in gl_bot)
    C["ctrl_glands"] = glands
    C["ctrl_screws"] = fuse(ycyl(x, -ct - 1.5, z, 4, 3) + ycyl(x, 13.5, z, 2.0, 33) for x, z in wsx)

    # ---- 7 lid with the front panel cut-outs, and the panel parts fitted through it
    ly = -dep - lt / 2
    lid = box(cxx, ly, czz, cw, lt, ch)
    lid = lid - box(cxx - 40, ly, czz + 60, 60, lt + 2, 30)                # display window
    lid = lid - ycyl(cxx - 50, ly, czz - 40, 9.6, lt + 2)                  # key switch
    lid = lid - ycyl(cxx + 10, ly, czz - 40, 8.1, lt + 2)                  # test button
    for lx in (45, 60, 75):
        lid = lid - ycyl(cxx + lx, ly, czz - 40, 2.6, lt + 2)              # status lights
    C["ctrl_lid"] = lid
    fy = -dep - lt                                # front face of the lid (-90)
    panel = (box(cxx - 40, -dep + 3, czz + 60, 70, 6, 40) + box(cxx - 40, -dep - lt / 2, czz + 60, 58, lt, 28)        # display module and glass
             + ycyl(cxx - 50, fy - 1, czz - 40, 12, 2) + ycyl(cxx - 50, fy + 15, czz - 40, 9.5, 30) + ycyl(cxx - 50, -dep + 1.5, czz - 40, 12, 3)  # key switch
             + ycyl(cxx + 10, fy - 1, czz - 40, 10, 2) + ycyl(cxx + 10, fy + 10, czz - 40, 8.0, 20) + ycyl(cxx + 10, -dep + 1.5, czz - 40, 10, 3))  # button
    for lx in (45, 60, 75):
        panel = panel + ycyl(cxx + lx, fy - 1, czz - 40, 4, 2) + ycyl(cxx + lx, fy + 5, czz - 40, 2.5, 10)
    C["panel_parts"] = panel

    # ---- 6 controller mounting plate (2 mm aluminium) on the four bosses, with the modules on standoffs
    pw, ph, pt = p["mplate"]
    py0 = -ct - 7                                 # front face of the bosses (-10)
    plate = box(cxx, py0 - pt / 2, czz, pw, pt, ph)
    for i in (-1, 1):
        for j in (-1, 1):
            plate = plate - ycyl(cxx + i * bxo, py0 - pt / 2, czz + j * bzo, 2.2, pt + 1)
    C["mplate"] = plate
    C["mplate_screws"] = fuse(ycyl(cxx + i * bxo, py0 - pt - 1, czz + j * bzo, 3.5, 2) + ycyl(cxx + i * bxo, py0 - pt / 2 + 3, czz + j * bzo, 1.4, pt + 6)
                              for i in (-1, 1) for j in (-1, 1))
    pf_ = py0 - pt                                # plate front face (-12)
    mods = None
    # (centre x, centre z, board w, board h, block w, block depth, block h)
    for mx, mz, mw, mh, kw, kd, kh in ((cxx - 45, czz + 75, 52, 24, 40, 6, 18),       # microcontroller module
                                       (cxx - 40, czz + 15, 80, 50, 60, 10, 30),       # trip board: comparator, latch, bridge supply
                                       (cxx + 45, czz + 70, 50, 40, 40, 15, 19),       # relay module: series trip relay, fan relay
                                       (cxx + 45, czz + 15, 40, 40, 20, 8, 20)):       # valve and alarm driver
        m = box(mx, pf_ - 6 - 0.8, mz, mw, 1.6, mh) + box(mx, pf_ - 7.6 - kd / 2, mz, kw, kd, kh)
        for sxo in (-1, 1):
            m = m + ycyl(mx + sxo * (mw / 2 - 4), pf_ - 3, mz, 2.5, 6)
        mods = m if mods is None else mods + m
    mods = mods + box(cxx, pf_ - 7, czz - 80, 150, 14, 18)                    # terminal strip
    C["modules"] = mods
    # ---- 19 dry-contact output: relay module (opens on a trip or loss of power) with its 2-way output terminal
    rx_, rz_ = cxx + 45, czz - 38
    dr = box(rx_, pf_ - 6 - 0.8, rz_, 44, 1.6, 34) + box(rx_ - 6, pf_ - 7.6 - 7.5, rz_ + 2, 20, 15, 16) \
        + box(rx_ + 14, pf_ - 7.6 - 5, rz_ + 2, 10, 10, 12)
    for sxo in (-1, 1):
        dr = dr + ycyl(rx_ + sxo * 18, pf_ - 3, rz_, 2.5, 6)
    C["dry_relay"] = dr

    # ---- 8 power supply brick on the floor by the outlet
    pw8, pd8, ph8 = p["psu"]
    C["psu"] = box(p["psu_x"], -110, ph8 / 2, pw8, pd8, ph8)

    # ---- 9 exhaust fan: fan plate on the wall, fan body in the 200 mm sleeve, grille over the plate, shutter and hood outside
    fx, fz = p["fan_x"], p["fan_z"]
    gs, gt = p["grille"]
    fr = p["fan_d"] / 2
    ps, pth = p["fan_plate"]
    wt = p["wall_t"]
    fp = box(fx, -pth / 2, fz, ps, pth, ps) - ycyl(fx, -pth / 2, fz, fr + 1, pth + 2)
    fsc = [(fx + i * 56.6, fz + j * 56.6) for i in (-1, 1) for j in (-1, 1)]
    wsc = [(fx + i * 105, fz + j * 105) for i in (-1, 1) for j in (-1, 1)]
    gsc = [(fx, fz + 110), (fx, fz - 110), (fx + 110, fz), (fx - 110, fz)]
    for x, z in fsc + wsc:
        fp = fp - ycyl(x, -pth / 2, z, 2.2, pth + 2)
    for x, z in gsc:
        fp = fp - ycyl(x, -pth / 2, z, 1.65, pth + 2)
    C["fan_plate"] = fp
    fbd, fbl = p["fan_body"]
    fan = (ycyl(fx, -pth / 2, fz, fr, pth) - ycyl(fx, -pth / 2, fz, fr - 1.5, pth + 1))                 # inlet spigot lip in the plate hole
    fan = fan + ycyl(fx, fbl / 2, fz, fbd / 2, fbl)                                                     # body
    fan = fan + (ycyl(fx, fbl + (wt + 2 - fbl) / 2, fz, fr, wt + 2 - fbl) - ycyl(fx, fbl + (wt + 2 - fbl) / 2, fz, fr - 1.5, wt + 3 - fbl))  # outlet spigot to 152
    for x, z in fsc:
        fan = fan - ycyl(x, 5, fz + (z - fz), 1.65, 10.01)                                              # tapped holes in the inlet face
    C["fan"] = fan
    so_, st_ = p["sleeve"]
    C["sleeve"] = ycyl(fx, wt / 2, fz, so_ / 2, wt) - ycyl(fx, wt / 2, fz, so_ / 2 - st_, wt + 1)
    gr = box(fx, -pth - gt / 2, fz, gs, gt, gs) - ycyl(fx, -pth - gt / 2, fz, fr, gt + 2)
    gr = gr + fuse(box(fx, -pth - gt / 2, fz + dz, 2 * fr, 3, 4) for dz in (-50, -25, 0, 25, 50))
    for x, z in gsc:
        gr = gr - ycyl(x, -pth - gt / 2, z, 2.2, gt + 2)
    C["grille"] = gr
    C["fan_screws"] = (fuse(ycyl(x, 3.5 - pth, z, 1.6, 7) for x, z in fsc)                              # countersunk, flush with the plate
                       + fuse(ycyl(x, 20 - pth, z, 2.0, 40) for x, z in wsc)                          # wall screws, flush, into plugs
                       + fuse(ycyl(x, -pth - gt - 1, z, 4, 2) + ycyl(x, -pth - gt / 2, z, 1.6, gt + pth) for x, z in gsc))
    C["shutter"] = (ycyl(fx, wt + 2 + 5, fz, fr + 4, 10) - ycyl(fx, wt + 2 + 5, fz, fr - 1.5, 11)) + ycyl(fx, wt + 2 + 5, fz, fr - 1.5, 1)
    hwid, hdep, hht = p["hood"]
    hood_y = wt + hdep / 2
    hood = box(fx, hood_y, fz + 20, hwid, hdep, hht) - box(fx, hood_y - 3, fz + 20 - 20, hwid - 6, hdep, hht)
    for i in (-1, 1):
        for zz in (fz + 100, fz - 60):
            hood = hood + (box(fx + i * (hwid / 2 + 10), wt + 1.5, zz, 20, 3, 20) - ycyl(fx + i * (hwid / 2 + 10), wt + 1.5, zz, 2.2, 4))
    C["hood"] = hood

    # ---- 10 make-up air grille on the side wall (inside face X = 0), low level
    iw, ih = p["inlet"]
    C["inlet"] = box(6, p["inlet_y"], p["inlet_z"], 12, iw, ih) - box(6, p["inlet_y"], p["inlet_z"], 14, iw - 30, ih - 30) \
        + fuse(box(6, p["inlet_y"], p["inlet_z"] + dz, 4, iw - 30, 3) for dz in (-40, -15, 10, 35))

    # ---- 11 normally closed solenoid valve on the bent flat-bar bracket
    vx, vy, vz = p["valve_x"], p["store_y"], p["supply_z"]
    vw, vd, vh = p["valve"]
    cr, cl = p["coil"]
    vb = (box(vx, vy, vz, vw, vd, vh) + zcyl(vx, vy, vz + vh / 2 + cl / 2, cr / 2, cl)
          + box(vx, vy, vz + vh / 2 + cl + 10, 30, 30, 20)
          + tube((vx - vw / 2 - 12, vy, vz), (vx + vw / 2 + 12, vy, vz), 7))
    for dy in (-18, 18):
        vb = vb - zcyl(vx, vy + dy, vz - vh / 2 + 4, 2.0, 8.01)                 # M5 tapped holes in the body underside
    C["valve"] = vb
    bw2, bt2 = p["valve_bar"]
    arm_z = vz - vh / 2 - bt2 / 2
    reach = -vy + 30                              # wall to 30 mm past the valve centre
    leg_bot = arm_z - 130
    br = box(vx, -reach / 2, arm_z, bw2, reach, bt2) + box(vx, -bt2 / 2, (leg_bot + arm_z + bt2 / 2) / 2, bw2, bt2, arm_z + bt2 / 2 - leg_bot)
    for dy in (-18, 18):
        br = br - zcyl(vx, vy + dy, arm_z, 2.75, bt2 + 2)
    for zz in (leg_bot + 25, leg_bot + 80):
        br = br - ycyl(vx, -bt2 / 2, zz, 3.3, bt2 + 2)
    C["valve_bracket"] = br
    C["valve_screws"] = (fuse(zcyl(vx, vy + dy, arm_z - bt2 / 2 - 2, 4.5, 4) + zcyl(vx, vy + dy, arm_z + 2.5, 2.0, bt2 + 5) for dy in (-18, 18))
                         + fuse(ycyl(vx, -bt2 - 2, zz, 5.5, 4) + ycyl(vx, 20 - bt2, zz, 3.0, 40) for zz in (leg_bot + 25, leg_bot + 80)))

    # ---- 12 sounder and beacon by the door
    bx, bzb = p["beacon_x"], p["beacon_z"]
    C["beacon"] = box(bx, -25, bzb, 100, 50, 100) + ycyl(bx, -80, bzb, 38, 60) + b.Pos(bx, -110, bzb) * b.Sphere(38)

    # ---- 18 differential pressure switch on the wall left of the fan; low port tubed to a static tap in the fan inlet
    dx_, dz_ = p["dps_x"], p["dps_z"]
    dw, dd_, dh = p["dps"]
    dyc = -dd_ / 2
    dbot = dz_ - dh / 2
    C["dp_switch"] = (box(dx_, dyc, dz_, dw, dd_, dh) + ycyl(dx_, -dd_ - 3, dz_ + 10, 14, 6)          # body and set-point knob
                      + zcyl(dx_ + 15, dyc, dbot - 6, 3, 12) + zcyl(dx_ - 15, dyc, dbot - 4, 3, 8)    # low port (tubed), high port (open)
                      - fuse(ycyl(dx_ + i * 30, -2, dz_ + 30, 2.2, 5) + ycyl(dx_ + i * 30, -6.05, dz_ + 30, 4.3, 4.1) for i in (-1, 1)))
    C["dp_screws"] = fuse(ycyl(dx_ + i * 30, -5.5, dz_ + 30, 4, 3) + ycyl(dx_ + i * 30, 12.5, dz_ + 30, 2.0, 33) for i in (-1, 1))
    tz_ = p["fan_z"] + p["dp_tap_dz"]
    to_, ti_ = p["dp_tube"]
    C["dp_tube"] = path([(dx_ + 15, dyc, dbot - 12), (dx_ + 15, dyc, tz_), (p["fan_x"], dyc, tz_),
                         (p["fan_x"], -p["fan_plate"][1] - 3, tz_)], to_ / 2, joints=True)

    # ---- 20 oxygen sensor option: transmitter box on the back wall, cell facing down at breathing height
    ox, oz = p["o2_x"], p["o2_z"]
    ow, od, oh = p["o2_box"]
    cdia, clen = p["o2_cell"]
    C["o2_box"] = (box(ox, -od / 2, oz, ow, od, oh) + zcyl(ox, -od / 2, oz - oh / 2 - clen / 2, cdia / 2, clen)
                   + zcyl(ox + 25, -od / 2, oz + oh / 2 + 6, 7, 12)                                   # cable gland on top
                   - fuse(ycyl(ox, -2, oz + i * 40, 2.2, 5) + ycyl(ox, -6.05, oz + i * 40, 4.3, 4.1) for i in (-1, 1)))
    C["o2_screws"] = fuse(ycyl(ox, -5.5, oz + i * 40, 4, 3) + ycyl(ox, 12.5, oz + i * 40, 2.0, 33) for i in (-1, 1))

    # ---- 15 bump test port on its angle bracket, tube and clips
    tx, tz = p["test_x"], p["test_z"]
    ang = box(tx, -15, tz - 1.5, 40, 30, 3) + box(tx, -1.5, tz + 12, 40, 3, 30)     # 30 x 30 x 3 angle, 40 long
    ang = ang - zcyl(tx, -18, tz - 1.5, 6.25, 5)
    for dx in (-10, 10):
        ang = ang - ycyl(tx + dx, -1.5, tz + 16, 2.2, 5)
    C["test_bracket"] = ang
    C["test_bracket_screws"] = fuse(ycyl(tx + dx, -4.5, tz + 16, 4, 3) + ycyl(tx + dx, 13.5, tz + 16, 2.0, 33) for dx in (-10, 10))
    C["test_port"] = (zcyl(tx, -18, tz - 3 - 7.5, 8, 15) + zcyl(tx, -18, tz - 3 - 15 - 7.5, 9, 15)     # body hex and dust cap below the leg
                      + zcyl(tx, -18, tz - 1.5, 6.0, 3) + zcyl(tx, -18, tz + 2.5, 8, 5) + zcyl(tx, -18, tz + 12.5, 5.5, 15))
    r = p["tube_od"] / 2
    pts = tube_points(p)
    C["tube"] = path(pts, r, joints=True)
    clips = [((tx, -2, z), "z") for z in (1500.0, 1900.0, 2300.0)]
    clips += [((x, -2, rz - 60), "x") for x in (2000.0, 2350.0, 2850.0)]
    C["clips"] = fuse(_clip(q, a, r) for q, a in clips)
    C["ceil_clips"] = fuse(_cclip((pts[5][0], y, pts[5][2]), r, rz) for y in (-80.0, hy + 60))
    return C


# BOM line of each component (lines 13 and 14 are cable and hardware; 16 is the made brackets and plates;
# 17 drop rod, 18 pressure switch, 19 dry-contact output, 20 oxygen sensor option; 21 is the alternative fan, not modelled)
COMPONENT_BOM = {
    "head_body": 1, "head_lid": 1, "head_gland": 1, "discs": 4, "standoffs": 14,
    "drop_flange": 17, "drop_rod": 17, "drop_nuts": 17, "drop_screws": 17,
    "dp_switch": 18, "dp_tube": 18, "dp_screws": 18, "dry_relay": 19, "o2_box": 20, "o2_screws": 20, "ceil_clips": 15,
    "sensor_board": 2, "cat": 2, "mos": 3, "board_screws": 14, "cup": 4, "cup_screws": 14, "cup_fitting": 15,
    "ctrl_body": 5, "ctrl_glands": 5, "ctrl_screws": 14, "ctrl_lid": 5, "panel_parts": 7, "mplate": 16,
    "mplate_screws": 14, "modules": 6, "psu": 8, "fan_plate": 16, "fan": 9, "sleeve": 9, "grille": 9,
    "fan_screws": 14, "shutter": 9, "hood": 9, "inlet": 10, "valve": 11, "valve_bracket": 16, "valve_screws": 14,
    "beacon": 12, "test_bracket": 16, "test_bracket_screws": 14, "test_port": 15, "tube": 15, "clips": 15,
}

# concept-media groups (one coloured part per BOM line, as before)
GROUPS = {
    "head": ["head_body", "head_lid", "head_gland"], "cat": ["sensor_board", "cat", "standoffs"], "mos": ["mos"],
    "arrest": ["discs", "cup"], "ctrl": ["ctrl_body", "ctrl_lid", "ctrl_glands"], "board": ["mplate", "modules", "dry_relay"],
    "panel": ["panel_parts"], "psu": ["psu"], "fan": ["fan_plate", "fan", "sleeve", "grille", "shutter", "hood"],
    "inlet": ["inlet"], "valve": ["valve", "valve_bracket"], "beacon": ["beacon"],
    "bump": ["test_bracket", "test_port", "cup_fitting", "tube", "clips", "ceil_clips"],
    "drop": ["drop_flange", "drop_rod", "drop_nuts"], "dps": ["dp_switch", "dp_tube"], "o2": ["o2_box"],
}


def build_parts(p=PARAMS, comps=None):
    """Return {key: solid} for the H2Guard parts by BOM line (lines 1 to 12, 15, 17, 18 and 20), fixings left out."""
    C = comps or build_components(p)
    return {k: fuse(C[n] for n in names) for k, names in GROUPS.items()}


def bump_kit(p=PARAMS, comps=None):
    """BOM line 15 as (test port on its bracket, tube with its clips)."""
    C = comps or build_components(p)
    return C["test_bracket"] + C["test_port"], C["tube"] + C["clips"] + C["ceil_clips"] + C["cup_fitting"]


BOM_ORDER = [("head", 1), ("cat", 2), ("mos", 3), ("arrest", 4), ("ctrl", 5), ("board", 6), ("panel", 7),
             ("psu", 8), ("fan", 9), ("inlet", 10), ("valve", 11), ("beacon", 12), ("bump", 15),
             ("drop", 17), ("dps", 18), ("o2", 20)]


def context(p=PARAMS):
    """Grey context, not in the BOM: {name: solid} for room, bench and apparatus, gas store and supply, cables."""
    b = _b3d()
    D = derived(p)
    rx, ry, rz = p["room"]
    wt = p["wall_t"]
    back = box(rx / 2, wt / 2, rz / 2, rx, wt, rz)
    back = back - ycyl(p["fan_x"], wt / 2, p["fan_z"], p["sleeve"][0] / 2 + 3, wt + 2)
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
    bench = bench + box(p["app_x"], p["app_y"], bh + ah / 2, aw, ad, ah)
    sx, sy = p["store_x"], p["store_y"]
    store = (zcyl(sx, sy, 450, 90, 900) + b.Pos(sx, sy, 900) * b.Sphere(90) + zcyl(sx, sy, 1010, 18, 60)
             + box(sx, sy, 1060, 70, 60, 50) + box(sx, -45, 700, 200, 90, 20))
    sz = p["supply_z"]
    vx, vw = p["valve_x"], p["valve"][0]
    supply = (path([(sx, sy, 1085), (sx, sy, sz), (vx - vw / 2 - 12, sy, sz)], 4)
              + path([(vx + vw / 2 + 12, sy, sz), (p["app_x"] - 100, sy, sz), (p["app_x"] - 100, sy, D["src_z"] - 20)], 4))
    tr = rz - 40
    cx, cz = p["ctrl_x"], p["ctrl_z"]
    ch = p["ctrl"][2]
    top = D["head_z"] + p["head"][2] / 2
    gx, hy = p["app_x"] + p["gland_dx"], p["head_y"]
    ox, oz = p["o2_x"], p["o2_z"] + p["o2_box"][2] / 2
    cables = (path([(p["valve_x"], -10, sz + 110), (p["valve_x"], -10, tr), (cx + 60, -10, tr), (cx + 60, -10, cz + ch / 2 + 30), (cx + 60, -45, cz + ch / 2 + 15)], 5)
              + path([(gx, hy, top + 12), (gx, hy, rz - 6), (gx, -6, rz - 6), (gx, -10, tr)], 5)
              + path([(p["dps_x"] - 30, -10, p["dps_z"] + p["dps"][2] / 2), (p["dps_x"] - 30, -10, tr)], 4)
              + path([(ox + 25, -27.5, oz + 12), (ox + 25, -27.5, oz + 40), (ox + 25, -10, oz + 40), (ox + 25, -10, 1150),
                      (cx - 60, -10, 1150), (cx - 60, -45, cz - ch / 2 - 15)], 4)
              + path([(cx - 20, -45, cz - ch / 2 - 15), (cx - 20, -10, cz - ch / 2 - 40), (cx - 20, -10, 1100), (p["dps_x"] - 60, -10, 1100),
                      (p["dps_x"] - 60, -10, tr)], 4)
              + path([(p["fan_x"], -10, p["fan_z"] + 130), (p["fan_x"], -10, tr)], 5)
              + path([(p["beacon_x"], -10, p["beacon_z"] + 50), (p["beacon_x"], -10, tr)], 5)
              + path([(p["valve_x"], p["store_y"] + 20, sz + 100), (p["valve_x"], -10, sz + 110)], 5)
              + path([(p["psu_x"], -110, 40), (p["psu_x"], -60, 120), (cx + 60, -60, 120), (cx + 60, -60, cz - ch / 2 - 30), (cx + 60, -45, cz - ch / 2 - 15)], 4)
              + path([(p["psu_x"] + 80, -110, 20), (p["psu_x"] + 120, -30, 300)], 4))
    return {"room": back + side + floor + outlet, "bench": bench, "store": store + supply, "cables": cables}


def assembly(p=PARAMS, with_room=False):
    b = _b3d()
    parts = build_parts(p)
    kids = list(parts.values())
    if with_room:
        kids += list(context(p).values())
    return b.Compound(children=kids)


# ----------------------------------------------------------------- constructability checks
CONTACTS = [  # (a, b): faces must touch (distance under 0.05 mm) without overlapping
    ("head_lid", "head_body"), ("discs", "head_body"), ("standoffs", "head_body"), ("sensor_board", "standoffs"),
    ("cat", "sensor_board"), ("mos", "sensor_board"), ("cup", "head_body"), ("cup_screws", "cup"),
    ("board_screws", "sensor_board"), ("head_gland", "head_body"),
    ("drop_rod", "drop_flange"), ("drop_nuts", "drop_rod"), ("drop_nuts", "head_body"), ("drop_screws", "drop_flange"),
    ("dp_screws", "dp_switch"), ("dp_tube", "dp_switch"), ("o2_screws", "o2_box"), ("dry_relay", "mplate"),
    ("ceil_clips", "tube"),
    ("cup_fitting", "cup"), ("tube", "cup_fitting"),
    ("ctrl_lid", "ctrl_body"), ("mplate", "ctrl_body"), ("modules", "mplate"), ("panel_parts", "ctrl_lid"),
    ("ctrl_glands", "ctrl_body"), ("ctrl_screws", "ctrl_body"), ("mplate_screws", "mplate"),
    ("test_port", "test_bracket"), ("tube", "test_port"), ("clips", "tube"), ("test_bracket_screws", "test_bracket"),
    ("fan", "fan_plate"), ("grille", "fan_plate"), ("shutter", "fan"), ("fan_screws", "fan_plate"),
    ("valve", "valve_bracket"), ("valve_screws", "valve_bracket"),
]
CLEAR = [  # (a, b, minimum gap mm)
    ("cat", "discs", 2.0), ("fan", "sleeve", 5.0), ("shutter", "hood", 1.0), ("tube", "head_body", 10.0),
    ("tube", "ctrl_body", 10.0), ("tube", "grille", 10.0), ("tube", "fan_plate", 10.0), ("test_port", "ctrl_body", 10.0),
    ("modules", "panel_parts", 5.0), ("ctrl_glands", "modules", 5.0), ("valve", "tube", 100.0),
    ("cup_screws", "discs", 2.0), ("standoffs", "cat", 2.0), ("standoffs", "mos", 2.0),
    ("drop_rod", "sensor_board", 20.0), ("drop_nuts", "head_gland", 5.0), ("tube", "drop_flange", 20.0), ("tube", "drop_nuts", 20.0),
    ("dp_tube", "fan", 2.0), ("dp_tube", "grille", 2.0), ("dp_tube", "fan_plate", 2.0), ("dp_switch", "fan_plate", 50.0),
    ("dp_switch", "clips", 20.0), ("dp_switch", "tube", 20.0), ("dry_relay", "panel_parts", 5.0), ("dry_relay", "modules", 5.0),
    ("ctrl_glands", "dry_relay", 5.0), ("o2_box", "tube", 100.0), ("o2_box", "test_port", 100.0),
]
WALL_ITEMS = {  # parts that bear on the room: back wall (y = 0), side wall (x = 0), floor (z = 0)
    "ctrl_body": "y", "fan_plate": "y", "test_bracket": "y", "valve_bracket": "y", "beacon": "y",
    "clips": "y", "inlet": "x", "psu": "z", "sleeve": "y", "hood": "y150", "dp_switch": "y", "o2_box": "y",
    "drop_flange": "c", "ceil_clips": "c",
}


def check(p=PARAMS, verbose=True):
    """Constructability checks on build_components(). Returns (passed, failed) lists of strings."""
    C = build_components(p)
    ok, bad = [], []
    D = derived(p)

    def ivol(x, y):
        try:
            r = x & y
            return 0.0 if r is None else r.volume
        except Exception:
            return 0.0

    def rec(good, text):
        (ok if good else bad).append(text)

    for a, b_ in CONTACTS:
        d = C[a].distance_to(C[b_])
        v = ivol(C[a], C[b_])
        rec(d < 0.05 and v < 0.5, f"contact {a} / {b_}: gap {d:.2f} mm, overlap {v:.2f} mm3")
    for a, b_, g in CLEAR:
        d = C[a].distance_to(C[b_])
        rec(d >= g, f"clearance {a} / {b_}: {d:.1f} mm (at least {g:g})")
    keys = list(C)
    bbs = {k: C[k].bounding_box() for k in keys}
    for i, a in enumerate(keys):
        for b_ in keys[i + 1:]:
            A, B = bbs[a], bbs[b_]
            if A.min.X > B.max.X or B.min.X > A.max.X or A.min.Y > B.max.Y or B.min.Y > A.max.Y or A.min.Z > B.max.Z or B.min.Z > A.max.Z:
                continue
            v = ivol(C[a], C[b_])
            rec(v < 0.5, f"no overlap {a} / {b_}: {v:.2f} mm3")
    wt = p["wall_t"]
    for k, face in WALL_ITEMS.items():
        bb = bbs[k]
        if face == "y":
            good = abs(bb.max.Y) < 0.05 or (bb.min.Y < 0.05 and bb.max.Y > -0.05)
        elif face == "y150":
            good = abs(bb.min.Y - wt) < 0.05
        elif face == "x":
            good = abs(bb.min.X) < 0.05
        elif face == "c":
            good = abs(bb.max.Z - p["room"][2]) < 0.05
        else:
            good = abs(bb.min.Z) < 0.05
        rec(good, f"bears on the room ({face}): {k}")
    rec(D["port_offset"] < 1.0, f"head ports over the apparatus centre: offset {D['port_offset']:.0f} mm")
    rec(D["port_below_ceiling"] <= 300.0, f"sensor ports {D['port_below_ceiling']:.0f} mm below the ceiling (300 or less)")
    rec(1400.0 <= D["o2_cell_z"] <= 1700.0, f"oxygen cell at breathing height: {D['o2_cell_z']:.0f} mm")
    if verbose:
        for t in bad:
            print("FAIL", t)
        print(f"{len(ok)} checks pass, {len(bad)} fail")
    return ok, bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        _, bad = check()
        sys.exit(1 if bad else 0)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    CC = build_components()
    P = build_parts(comps=CC)
    groups = {
        "h2guard-assembly": list(CC.values()),
        "detector-head": [CC[k] for k in ("head_body", "head_lid", "head_gland", "discs", "standoffs", "sensor_board", "cat", "mos",
                                          "board_screws", "cup", "cup_screws", "cup_fitting", "drop_flange", "drop_rod", "drop_nuts",
                                          "drop_screws")],
        "controller": [CC[k] for k in ("ctrl_body", "ctrl_lid", "ctrl_glands", "mplate", "mplate_screws", "modules", "dry_relay",
                                       "panel_parts")],
        "exhaust-fan": [CC[k] for k in ("fan_plate", "fan", "sleeve", "grille", "fan_screws", "shutter", "hood", "dp_switch",
                                        "dp_tube", "dp_screws")],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"room {D['room_m3']:.1f} m3; sensor ports {D['port_below_ceiling']:.0f} mm below the ceiling, {D['port_offset']:.0f} mm from the apparatus centre; "
          f"leak source {D['src_z']:.0f} mm above the floor, {D['plume_rise']:.0f} mm below the ports")
    print(f"controller top {D['ctrl_below_ceiling']:.0f} mm below the ceiling; fan grille top {D['fan_below_ceiling']:.0f} mm; "
          f"beacon top {D['beacon_below_ceiling']:.0f} mm")
    print(f"bump test cup {D['cup_ml']:.0f} mL; tube {D['tube_run']:.0f} mm, {D['tube_ml']:.1f} mL")
