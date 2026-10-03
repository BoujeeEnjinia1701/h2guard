"""H2Guard general arrangement sheet HGD-DWG-001, Rev P5 (TRL 3, constructable design).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/HGD-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept blueprint in media/ is HGD-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, build_parts, context, derived  # noqa: E402

DATE = "2026-09-25"
DATE4 = "2026-10-01"
DATE5 = "2026-10-02"


def safe_project_views(part, workdir, line_weight=0.35, names=("front", "top", "right", "iso")):
    """Same views as drawing.project_views, edge by edge, so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X - d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name in names:
        origin, up = setups[name]
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    dl = 11                                       # room the kit leaves for overall dimensions (drawing.add_ortho)
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.0, 400, INK, "middle", mono=True)}</g>']


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.0, 400, INK, "middle", mono=True)]


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 1.9, 400, INK, anchor)]


def main():
    from build123d import Compound
    D = derived(P)
    S = build_parts(P)
    C = context(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = Compound(children=list(S.values()) + [C["room"], C["bench"], C["store"]])
    views = safe_project_views(asm, work, names=("front", "top", "right"))
    head = Compound(children=[S[k] for k in ("head", "cat", "mos", "arrest", "drop")])
    hv = safe_project_views(head, work / "head", names=("iso",))
    bb = asm.bounding_box()
    s = Sheet(project="H2Guard", title="General arrangement in the 30 m3 reference room", dwg_no="HGD-DWG-001", rev="P5",
              author="Amish Chadha", date=DATE5, scale=None, theme="technical",
              material="Bought-in parts per bom/bom.csv; room, bench and gas store are context. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Notes: head placement rule, timed escalation (DDR-002)", DATE, "AC"),
                         ("P3", "Layout and labels tidied", DATE, "AC"),
                         ("P4", "Design for construction (DDR-003): brackets, plates, sleeve", DATE4, "AC"),
                         ("P5", "Head on ceiling drop rod; pressure switch; O2 option (DEC-001)", DATE5, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    rx, ry, rz = P["room"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    z0 = Z(0)
    xl = X(bb.min.X) - 13
    heights = [(D["port_face"], f"{D['port_face']:.0f} sensor ports"),
               (P["beacon_z"], f"{P['beacon_z']:.0f} beacon"), (D["ctrl_top"], f"{D['ctrl_top']:.0f} controller top"),
               (D["src_z"], f"{D['src_z']:.0f} leak source")]
    for i, (zz, label) in enumerate(heights):
        xd = xl - 5 * (i + 1)
        L += [ext(X(bb.min.X), Z(zz), xd - 1, Z(zz))]
        L += dim_v(xd, Z(zz), z0, label)
    L += leader(X(P["app_x"]), Z(D["head_z"]), X(P["app_x"]) - 2, Z(rz) - 6, "1-4, 17 HEAD ON DROP ROD OVER SOURCE", "end")
    L += leader(X(P["dps_x"]), Z(P["dps_z"]), X(1760), Z(rz) - 11, "18 PRESSURE SWITCH")
    L += leader(X(P["o2_x"]), Z(P["o2_z"] - 80), X(2620), Z(420), "20 O2 SENSOR (OPTION)")
    L += leader(X(P["fan_x"]), Z(P["fan_z"]), X(P["fan_x"]) + 6, Z(rz) - 6, f"9 EXHAUST FAN, CENTER {P['fan_z']:.0f}")
    L += leader(X(P["ctrl_x"] - 60), Z(P["ctrl_z"] + 60), X(3400), Z(1250), "5-7 CONTROLLER, 15 TEST PORT", "end")
    L += leader(X(P["valve_x"]), Z(P["supply_z"]), X(P["valve_x"]) + 8, Z(P["supply_z"] + 280), "11 NC VALVE ON SUPPLY")
    L += leader(X(P["store_x"]), Z(1000), X(150), Z(rz) - 3, "GAS STORE (CONTEXT)")
    L += leader(X(P["psu_x"]), Z(40), X(4150), Z(650), "8 SUPPLY", "end")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    L += dim_h(Xt(0), Xt(rx), Yt(-ry) - 6, f"{rx:,.0f}")
    L += dim_v(Xt(rx) + 10, Yt(0), Yt(-ry), f"{ry:,.0f}", side=1)
    L += leader(Xt(P["fan_x"]), Yt(0), Xt(P["fan_x"]) + 8, Yt(-500), f"FAN AT X {P['fan_x']:.0f}")
    L += leader(Xt(0), Yt(P["inlet_y"]), Xt(700), Yt(P["inlet_y"] + 200), f"10 MAKE-UP AIR, Z {P['inlet_z']:.0f}")

    # right view (from +X): -Y to the left... looking along -X, +Y appears to the right
    x, y, w, h = c["right"]
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    Yr = lambda my: x + (my - bb.min.Y) * k
    L += dim_v(Yr(-ry) - 4, Zr(P["inlet_z"] + P["inlet"][1] / 2), Zr(0), f"{P['inlet_z'] + P['inlet'][1] / 2:.0f}")
    L += leader(Yr(-ry / 2), Zr(P["inlet_z"]), Yr(-ry / 2) + 4, Zr(700), "10 GRILLE")

    s._layers += L
    s.add_svg(hv["iso"], 276, 42, 140, 60, label="Detector head on its drop rod, items 1 to 4 and 17",
              sublabel="Not to scale; ports and bump test cup face down")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Room {rx:.0f} x {ry:.0f} x {rz:.0f} ({D['room_m3']:.0f} m3); leak source {D['src_z']:.0f} above floor",
        f"Head {P['head'][0]:.0f} x {P['head'][1]:.0f} x {P['head'][2]:.0f} on drop rod; ports {D['port_below_ceiling']:.0f} below ceiling, {D['plume_rise']:,.0f} above source",
        f"Arrestor discs {P['disc'][0]:.0f} x {P['disc'][1]:.0f}; sensor {D['sensor_gap']:.1f} behind disc",
        f"Bump cup {P['cup'][0]:.0f} x {P['cup'][1]:.0f} x {P['cup'][2]:.0f} ({D['cup_ml']:.0f} mL); tube 4 OD, {D['tube_run']:,.0f} run",
        f"Controller {P['ctrl'][0]:.0f} x {P['ctrl'][2]:.0f} x {P['ctrl'][1]:.0f}; top {D['ctrl_below_ceiling']:,.0f} below ceiling",
        f"Fan 150 spigots, body in a {P['sleeve'][0]:.0f} wall sleeve; grille top {D['fan_below_ceiling']:.0f} below ceiling",
        f"Make-up grille {P['inlet'][0]:.0f} x {P['inlet'][1]:.0f} on far wall, center {P['inlet_z']:.0f}",
        "Valve 1/4 in NC, hydrogen rated, on a wall bracket; gas fitting by others",
        f"Ports {D['port_offset']:.0f} from apparatus centre (plume radius 141)",
        f"Pressure switch at fan; O2 cell {D['o2_cell_z']:,.0f} above floor (option)",
        "Warning held 5 min closes valve and latches (firmware, DDR-002)",
        "Third-angle; front view from -Y (room side); HGD-CAL-001",
    ], x=276, y=118, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "HGD-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
