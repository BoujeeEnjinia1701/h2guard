"""H2Guard sizing calculations, HGD-CAL-001 v0.1 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Every number quoted in docs/04-calcs/01-sizing.md is printed here, tagged [A1], [B2] and so on.
The script imports PARAMS and derived() from cad/src/model.py, so the room, mounting heights,
sensor cavity, bump test cup and tube are those of the model and of drawing HGD-DWG-001.
It also reads bom/bom.csv and budget_usd in project.yaml. First-principles estimates only.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)
OUT = []


def say(tag, text):
    line = f"[{tag}] {text}"
    OUT.append(line)
    print(line)


# ---------------- constants and assumptions ----------------
LFL = 4.0                 # % vol, hydrogen in air
WARN, TRIP = 0.10 * LFL, 0.25 * LFL
T = 293.15                # K, 20 °C
R = 8.314                 # J/(mol K)
VM = R * T / 101325 * 1000   # L/mol at 20 °C, 1 atm
F = 96485.0
RHO_AIR, RHO_H2 = 1.204, 0.0838   # kg/m3 at 20 °C, 1 atm
G = 9.81
ROOM = D["room_m3"]       # m3
LEAK = 5.0                # L/min design leak
VENT, BOOST = 150.0, 300.0          # m3/h, R7 targets for the 30 m3 room
BUDGET_REC = 250.0                  # $ recommended in the TRL 2 review, awaiting Amish

say("A1", f"LFL {LFL:.1f} % vol; warning 10 % LFL = {WARN:.2f} % vol; trip 25 % LFL = {TRIP:.2f} % vol; molar volume {VM:.2f} L/mol at 20 °C")
say("A2", f"Reference room {ROOM:.1f} m3, ceiling {D['ceiling_m2']:.1f} m2, height {P['room'][2]:.0f} mm")

# ---------------- B. sources and inventory ----------------
# B1 electrolyzer (Faraday): 100 W stack at 1.9 V per cell
stack_w, v_cell = 100.0, 1.9
IN = stack_w / v_cell                         # A x cells
n = IN / (2 * F)
q_el = n * VM * 60
say("B1", f"100 W PEM stack at {v_cell} V/cell: I x N = {IN:.1f} A, {n * 1e4:.2f} x 10^-4 mol/s, {q_el:.2f} L/min; design leak {LEAK:.0f} L/min is {LEAK / q_el:.0f} times this")
# B2 inventory rule: whole inventory mixed into the room stays at or below 25 % LFL
inv_l = ROOM * 1000 * TRIP / 100
inv_g = inv_l / VM * 2.016
say("B2", f"Inventory limit (1 % of room volume): {inv_l:.0f} L at 1 atm, {inv_g:.1f} g")
# B3 examples: H2Bench 2 L tank at 300 kPa gauge (its REVIEW), a 10 L cylinder at 200 bar (Z = 1.13)
h2b = 2.0 * (300 + 101.3) / 101.3
cyl_mol = 200e5 * 0.010 / (1.13 * R * T)
cyl_l = cyl_mol * VM
say("B3", f"H2Bench 2 L tank at 300 kPa gauge: {h2b:.1f} L ({100 * h2b / inv_l:.1f} % of the limit); 10 L cylinder at 200 bar: {cyl_l / 1000:.2f} m3, {cyl_l / inv_l:.1f} times the limit")
# B4 flow restrictor that limits a full-bore failure to the design leak (choked orifice)
gam, Rs, Cd = 1.41, 4124.0, 0.8
p0 = 11e5                                         # 10 bar gauge upstream
mdot = LEAK / 60 / 1000 * RHO_H2                  # kg/s
flux = Cd * p0 * math.sqrt(gam / (Rs * T)) * (2 / (gam + 1)) ** ((gam + 1) / (2 * (gam - 1)))
d_or = math.sqrt(4 * mdot / flux / math.pi) * 1000
p0b = 4e5
d_or3 = math.sqrt(4 * mdot / (flux * p0b / p0) / math.pi) * 1000
say("B4", f"Restrictor for {LEAK:.0f} L/min: orifice {d_or:.2f} mm at 10 bar gauge, {d_or3:.2f} mm at 3 bar gauge (choked, Cd {Cd})")

# ---------------- C. build-up without ventilation ----------------
layer_m3 = D["ceiling_m2"] * 0.3
say("C1", f"Ceiling layer 0.3 m x {D['ceiling_m2']:.0f} m2 = {layer_m3:.1f} m3")
rows = []
for name, c in (("10 % LFL", WARN), ("25 % LFL", TRIP), ("100 % LFL", LFL)):
    vl = layer_m3 * 1000 * c / 100
    vr = ROOM * 1000 * c / 100
    rows.append((name, vl, vl / LEAK, vr / LEAK))
    say("C2", f"{name}: layer needs {vl:.0f} L, {vl / LEAK:.1f} min at {LEAK:.0f} L/min; whole room {vr:.0f} L, {vr / LEAK:.0f} min")

# ---------------- D. dilution with ventilation ----------------
def mixed(q_lpm, vent_m3h):
    v = vent_m3h * 1000 / 60
    return 100 * q_lpm / (v + q_lpm)

c_v, c_b, c_el = mixed(LEAK, VENT), mixed(LEAK, BOOST), mixed(q_el, VENT)
say("D1", f"Steady well-mixed (and exhaust) concentration, {LEAK:.0f} L/min: {c_v:.3f} % vol ({100 * c_v / LFL:.1f} % LFL) at {VENT:.0f} m3/h; "
    f"{c_b:.3f} % vol ({100 * c_b / LFL:.1f} % LFL) at {BOOST:.0f} m3/h; electrolyzer case {c_el:.4f} % vol")
ach = VENT / ROOM
tau_min = 60 / ach
say("D2", f"{ach:.1f} air changes per hour; time constant {tau_min:.0f} min; 95 % of steady state after {3 * tau_min:.0f} min")
# with high-level exhaust and low-level make-up air, the upper layer at steady state is at the exhaust concentration
say("D3", f"High-level exhaust: at steady state all hydrogen leaves through the fan, so the upper layer settles at the exhaust value, {c_v:.2f} % vol ({100 * c_v / LFL:.1f} % LFL)")
# the plume flow at the ceiling versus the exhaust flow sets whether a layer interface forms in the room
alpha = 0.10
Q = LEAK / 60 / 1000                             # m3/s
B = G * (RHO_AIR - RHO_H2) / RHO_AIR * Q        # buoyancy flux, m4/s3
k_q = 6 * alpha / 5 * (9 * alpha / 10) ** (1 / 3) * math.pi ** (2 / 3)
k_w = 5 / (6 * alpha) * (9 * alpha / 10) ** (1 / 3) * math.pi ** (-1 / 3)
z_int = (VENT / 3600 / (k_q * B ** (1 / 3))) ** 0.6
say("D4", f"Plume flow equals {VENT:.0f} m3/h exhaust {z_int:.2f} m above the source; source to ceiling is {D['src_to_ceiling'] / 1000:.2f} m, "
    "so the plume reaches the ceiling before it carries the exhaust flow and the upper layer extends down to about source height")

# ---------------- E. plume at the detector head ----------------
z = D["plume_rise"] / 1000
qp = k_q * B ** (1 / 3) * z ** (5 / 3)
c_mean = 100 * Q / qp
c_axis = 2 * c_mean
w = k_w * B ** (1 / 3) * z ** (-1 / 3)
t_rise = 0.75 * z ** (4 / 3) / (k_w * B ** (1 / 3))
say("E1", f"Buoyancy flux {B * 1e4:.2f} x 10^-4 m4/s3; plume rise to the sensor ports {z:.3f} m")
say("E2", f"Plume flow at the head {qp * 1000:.1f} L/s; mean {c_mean:.2f} % vol ({100 * c_mean / LFL:.0f} % LFL); on the axis about {c_axis:.2f} % vol ({100 * c_axis / LFL:.0f} % LFL)")
say("E3", f"Plume velocity at the head {w:.2f} m/s; rise time {t_rise:.1f} s")
warn_ok = 100 * c_mean / LFL >= 10
trip_ok = 100 * c_axis / LFL >= 25
say("E4", f"Head reading with the fan running: layer {100 * c_v / LFL:.0f} % LFL plus plume {100 * c_mean / LFL:.0f} to {100 * c_axis / LFL:.0f} % LFL; "
    f"plume mean {'above' if warn_ok else 'below'} the warning, plume axis {'above' if trip_ok else 'below'} the trip")
# leak sizes that reach the trip on the plume axis at the head
q_trip = (TRIP / 100 / 2 * k_q * z ** (5 / 3) * (G * (RHO_AIR - RHO_H2) / RHO_AIR) ** (1 / 3)) ** 1.5 * 60000
q_warn = (WARN / 100 * k_q * z ** (5 / 3) * (G * (RHO_AIR - RHO_H2) / RHO_AIR) ** (1 / 3)) ** 1.5 * 60000
say("E5", f"Leak that brings the plume axis at the head to 25 % LFL: {q_trip:.1f} L/min; plume mean to 10 % LFL: {q_warn:.1f} L/min")
# plume flow scales with alpha^(4/3), so the head concentration scales with alpha^(-4/3)
f_lo, f_hi = (0.10 / 0.12) ** (4 / 3), (0.10 / 0.08) ** (4 / 3)
say("E6", f"Entrainment coefficient 0.08 to 0.12 instead of 0.10: head values x{f_lo:.2f} to x{f_hi:.2f}, axis {100 * c_axis * f_lo / LFL:.0f} to {100 * c_axis * f_hi / LFL:.0f} % LFL")

# ---------------- F. response time chain (R4, R5) ----------------
D_h2 = 0.61e-4 * (T / 273.15) ** 1.75          # m2/s, H2 in air
eps, tort = 0.40, 3.0
d_eff = D_h2 * eps / tort
dd, dt = P["disc"]
A_disc = math.pi / 4 * (dd / 1000) ** 2
L = dt / 1000
t_slab = L ** 2 / d_eff
Gc = d_eff * A_disc / L
V_cav = D["sensor_cavity_ml"] * 1e-6
t_cav = 2.303 * V_cav / Gc
t_arr = t_slab + t_cav
say("F1", f"Arrestor disc {dd:.0f} x {dt:.0f} mm, porosity {eps}, tortuosity {tort}: D_eff {d_eff * 1e6:.1f} x 10^-6 m2/s; slab {t_slab:.2f} s; "
    f"cavity {D['sensor_cavity_ml']:.2f} mL behind it, 90 % in {t_cav:.2f} s; total {t_arr:.1f} s")
L5 = 0.005
t_arr_trl2 = L5 ** 2 / d_eff + 2.303 * (math.pi / 4 * (dd / 1000) ** 2 * 0.015) / (d_eff * A_disc / L5)
say("F2", f"TRL 2 arrangement (5 mm disc, sensor 15 mm behind it): {t_arr_trl2:.0f} s")
t90_sensor = 30.0          # target, unconfirmed
t_comp, t_relay, t_valve = 0.05, 0.02, 0.10
t_total = t_rise + t_arr + t90_sensor + t_comp + t_relay + t_valve
say("F3", f"Leak to valve closed: rise {t_rise:.1f} + arrestor {t_arr:.1f} + sensor t90 {t90_sensor:.0f} (assumed) + comparator {t_comp} + relay {t_relay} + valve {t_valve} = {t_total:.1f} s")
say("F4", f"Trip to valve closed {t_comp + t_relay + t_valve:.2f} s (R4 limit 2 s); alarm within {t_arr + t90_sensor:.0f} s of a step at the head (R4 limit 60 s)")
rel = LEAK * t_total / 60
line_l = math.pi / 4 * 4.3 ** 2 * 3000 / 1e6 * (11 / 1.013)
say("F5", f"Released before closing: {rel:.1f} L at {LEAK:.0f} L/min; plus downstream line (3 m of 4.3 mm bore at 10 bar gauge) {line_l:.2f} L")
wd = 1.0
say("F6", f"Fault to valve closed: watchdog {wd:.1f} s + relay + valve = {wd + t_relay + t_valve:.2f} s; sensor open or short via comparator {t_comp + t_relay + t_valve:.2f} s; "
    f"fan stop detected at 10 s then {t_relay + t_valve:.2f} s (R5 limit 2 s after detection)")

# ---------------- G. fan and duct system (R7) ----------------
d = P["fan_d"] / 1000
A = math.pi / 4 * d ** 2
K_exh = {"inside grille": 0.7, "sleeve friction": 0.03 * D["sleeve_len"] / 1000 / d, "backdraft shutter": 1.2, "weather hood and exit": 1.5}
iw, ih = P["inlet"]
A_in = iw * ih / 1e6 * 0.5
K_in = 2.0


def sys_dp(q_m3h):
    v = q_m3h / 3600 / A
    vi = q_m3h / 3600 / A_in
    return sum(K_exh.values()) * 0.5 * RHO_AIR * v ** 2 + K_in * 0.5 * RHO_AIR * vi ** 2


Ksum = sum(K_exh.values())
say("G1", f"Duct velocity at {VENT:.0f} m3/h: {VENT / 3600 / A:.2f} m/s; exhaust side K {Ksum:.2f}; make-up grille free area {A_in:.3f} m2, K {K_in}")
say("G2", f"System pressure drop: {sys_dp(VENT):.1f} Pa at {VENT:.0f} m3/h; {sys_dp(BOOST):.1f} Pa at {BOOST:.0f} m3/h (room runs slightly below ambient)")
kq = sys_dp(VENT) / VENT ** 2


def op_point(qmax, p0):
    # fan p = p0 (1 - (q/qmax)^2) at full speed; system p = kq q^2
    return math.sqrt(p0 / (kq + p0 / qmax ** 2))


fans = {"TRL 2 spec (axial, 300 m3/h free air, 100 Pa shut-off, assumed)": (300.0, 100.0),
        "TRL 3 spec (mixed flow, 450 m3/h free air, 200 Pa shut-off, assumed)": (450.0, 200.0)}
q_ops = {}
for name, (qm, p0) in fans.items():
    q = op_point(qm, p0)
    q_ops[name] = q
    say("G3", f"{name}: full speed {q:.0f} m3/h ({q / ROOM:.1f} air changes per hour), {100 * (q / BOOST - 1):+.0f} % against the {BOOST:.0f} m3/h boost")
q_new = list(q_ops.values())[1]
s_cont = VENT / q_new
P_fan_full = 35.0
p_fan_cont = P_fan_full * s_cont ** 3 + 1.0
say("G4", f"Continuous {VENT:.0f} m3/h at {100 * s_cont:.0f} % speed; fan power about {p_fan_cont:.1f} W continuous, {P_fan_full + 1:.0f} W on boost (35 W rated input assumed)")
say("G5", f"Room depression at boost {sys_dp(q_new) - sum(K_exh.values()) * 0.5 * RHO_AIR * (q_new / 3600 / A) ** 2:.1f} Pa across the make-up grille")

# ---------------- H. power (R11) ----------------
cat_w, mos_w, ctl_w, valve_w, alarm_w = 0.5, 0.28, 0.5, 8.0, 3.0
states = {
    "Normal": cat_w + mos_w + ctl_w + valve_w + p_fan_cont,
    "Warning (valve open, fan boost, sounder)": cat_w + mos_w + ctl_w + valve_w + P_fan_full + 1 + alarm_w,
    "Trip (valve closed, fan boost, alarm)": cat_w + mos_w + ctl_w + P_fan_full + 1 + alarm_w,
}
for k_, v_ in states.items():
    say("H1", f"{k_}: {v_:.1f} W")
pmax = max(states.values())
say("H2", f"Peak {pmax:.1f} W against the 60 W supply: margin x{60 / pmax:.2f}; valve coil heat {valve_w:.0f} W continuous; energy in normal state {states['Normal'] * 24 / 1000:.2f} kWh/day")

# ---------------- J. bump test and log (R12) ----------------
q_span = 1.0            # L/min
cup = D["cup_ml"]
t_tube = D["tube_ml"] / 1000 / q_span * 60
t_cup = 5 * cup / 1000 / q_span * 60
t_bump = t_tube + t_cup + t90_sensor + t_arr
gas_per = q_span * (t_bump + 15) / 60
cyl_span = 34.0
say("J1", f"Bump test at {q_span:.1f} L/min: tube {D['tube_run'] / 1000:.2f} m, {D['tube_ml']:.1f} mL, delay {t_tube:.1f} s; cup {cup:.0f} mL, five volumes in {t_cup:.0f} s; "
    f"reading settles after about {t_bump:.0f} s (R12 limit 120 s)")
say("J2", f"Span gas {gas_per:.2f} L per test (with 15 s margin); a 34 L disposable cylinder gives about {cyl_span / gas_per:.0f} tests")
rec_b, per_min = 16, 1
log_mb = 90 * 24 * 60 * per_min * rec_b / 1e6
say("J3", f"Log: one {rec_b} B record per minute for 90 days = {log_mb:.2f} MB, plus events; needs a board with 4 MB flash or more")

# ---------------- K. alarm level (R10) ----------------
for r_m in (1, 3, 5):
    say("K1", f"Sounder 90 dB at 1 m: {90 - 20 * math.log10(r_m):.0f} dB at {r_m} m (free field)")
diag = math.sqrt((P["room"][0] / 1000) ** 2 + (P["room"][1] / 1000) ** 2)
say("K2", f"Farthest point in the room {diag:.1f} m: {90 - 20 * math.log10(diag):.0f} dB, {90 - 20 * math.log10(diag) - 60:.0f} dB above a 60 dB lab background")

# ---------------- L. ignition sources and placement (R1, R15) ----------------
say("L1", f"Sensor ports {D['port_below_ceiling']:.0f} mm below the ceiling (R1: 300 mm or less); fan grille top {D['fan_below_ceiling']:.0f} mm below the ceiling")
say("L2", f"Controller top {D['ctrl_below_ceiling']:.0f} mm below the ceiling (R15: 1000 mm or more); beacon top {D['beacon_below_ceiling']:.0f} mm; supply on the floor")

# ---------------- M. installation time (R13) ----------------
tasks = [("Plan and mark out", 20), ("Detector head bracket and head", 30), ("Core drill 160 mm through the wall; sleeve, fan and hood", 90),
         ("Opening and make-up air grille", 60), ("Controller", 25), ("Sounder and beacon", 15), ("Power supply", 5),
         ("15 m of cable in surface conduit", 60), ("Bump test tube and port", 20), ("Valve coil connection (gas fitting by others)", 10),
         ("Commissioning: test button and first bump test", 25)]
t_all = sum(t for _, t in tasks)
t_nowall = t_all - 90 - 60 + 20 + 15
say("M1", f"Installation estimate {t_all} min ({t_all / 60:.1f} h) with both wall openings; {t_nowall} min ({t_nowall / 60:.1f} h) if the openings are made by others (R13 limit 240 min)")

# ---------------- N. cost (R14) ----------------
bom = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
total = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in bom)
budget = None
for line in (ROOT / "project.yaml").read_text().splitlines():
    if line.startswith("budget_usd:"):
        budget = float(line.split(":")[1].split("#")[0])
fan_grille = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in bom if r["item"].split()[0] in ("9", "10"))
say("N1", f"BOM {len(bom)} lines, total ${total:.2f}; budget_usd ${budget:.0f}: {100 * (total / budget - 1):+.0f} %; recommended ${BUDGET_REC:.0f} (awaiting Amish): {total - BUDGET_REC:+.2f}")
say("N2", f"Without the fan and make-up grille (${fan_grille:.2f}): ${total - fan_grille:.2f}")

(Path(__file__).parent / "results.txt").write_text("\n".join(OUT) + "\n")
