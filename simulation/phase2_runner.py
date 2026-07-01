"""
phase2_runner.py — Phase II Leg 1 discrimination runner
=======================================================
Mirrors workstream_a_runner.py. Extends the canonical ABM (c2_core.py) into
the low-attrition residual-force regime and measures whether the OBSERVABLE
attribution-correlation proxy separates H1 (adaptive) from H2 (pre-programmed),
and how much discriminating power it keeps relative to the full (unobservable)
emergent target ratio.

Design is locked in leg1_design_v0_1.md. Key pre-registered choices:
  - Both denominators reported (D_all matches empirical 4.5/7; D_win is the
    pure response rate). Primary chosen after inspecting stability.
  - Connectivity c_res is SWEPT, not fixed, so the reconstituted-C2 assumption
    is a labeled curve.
  - Headline number is the GAP = r(attribution) / r(emergent).

Stats are stdlib-only (Mann-Whitney U with tie-corrected normal approximation,
rank-biserial r as the primary effect size, Cohen's d in parens), matching the
v4 posture and the "no external dependencies" constraint.
"""

import math
import random
import time
import csv
from collections import defaultdict

import c2_core as m

# ── Grid parameters ────────────────────────────────────────────────
N_SEEDS      = 200
SIM_DAYS     = 60
PRE_AUTH     = (25, 40)
N_PROV       = 8
PROV_VALUE   = 1.2            # salience premium above max pre-war value (0.95)
P_STANDING   = 0.5           # fraction of provokers that are pre-war targets
C_RES_SWEEP  = [0.20, 0.35, 0.50, 0.65]
W_SWEEP      = [3, 2]          # 72h primary, 48h robustness
HYPS         = ["H1", "H2", "H3"]

# Emergent target set is fixed by construction. Base emergent tids come from
# build_targets; NOVEL provocation sources are added per run. Standing
# provokers are pre-war targets (active_since 0) and are NOT emergent.
_BASE = m.build_targets()
EMERGENT_BASE = {tid for tid, t in _BASE.items() if t.active_since > 0}
PRE_WAR = [(tid, t.value) for tid, t in _BASE.items() if t.active_since == 0]


# ── Stdlib statistics ──────────────────────────────────────────────
def _normal_cdf(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _mean(v):
    return sum(v) / len(v) if v else 0.0


def _var(v):
    if len(v) < 2:
        return 0.0
    mu = _mean(v)
    return sum((x - mu) ** 2 for x in v) / (len(v) - 1)


def cohen_d(x, y):
    nx, ny = len(x), len(y)
    sp2 = ((nx - 1) * _var(x) + (ny - 1) * _var(y)) / max(nx + ny - 2, 1)
    sp = math.sqrt(sp2)
    return (_mean(x) - _mean(y)) / sp if sp > 0 else 0.0


def mann_whitney(x, y):
    """
    Two-sided Mann-Whitney U with tie-corrected normal approximation.
    Returns (rank_biserial_r, z, p). r is signed positive when x tends to
    exceed y (i.e. r > 0 means H1 > H2 on the metric). Handles the all-equal
    degenerate case (returns r=0, p=1).
    """
    n1, n2 = len(x), len(y)
    n = n1 + n2
    if n1 == 0 or n2 == 0:
        return 0.0, 0.0, 1.0

    combined = sorted([(v, 0) for v in x] + [(v, 1) for v in y],
                      key=lambda t: t[0])
    # average ranks with tie handling
    ranks = [0.0] * n
    tie_terms = 0.0
    i = 0
    while i < n:
        j = i
        while j + 1 < n and combined[j + 1][0] == combined[i][0]:
            j += 1
        avg = (i + j + 2) / 2.0  # ranks are 1-based: (i+1..j+1) averaged
        for k in range(i, j + 1):
            ranks[k] = avg
        t = j - i + 1
        if t > 1:
            tie_terms += t ** 3 - t
        i = j + 1

    R1 = sum(ranks[k] for k in range(n) if combined[k][1] == 0)
    U1 = R1 - n1 * (n1 + 1) / 2.0
    U2 = n1 * n2 - U1

    # rank-biserial, signed for x (H1) vs y (H2)
    r = 2.0 * U1 / (n1 * n2) - 1.0

    mu = n1 * n2 / 2.0
    if n < 2:
        return r, 0.0, 1.0
    sigma2 = (n1 * n2 / 12.0) * ((n + 1) - tie_terms / (n * (n - 1)))
    if sigma2 <= 0:
        # all tied -> no separation
        return 0.0, 0.0, 1.0
    U = min(U1, U2)
    # continuity correction
    z = (U - mu + 0.5) / math.sqrt(sigma2) if U < mu else (U - mu - 0.5) / math.sqrt(sigma2)
    p = 2.0 * (1.0 - _normal_cdf(abs(z)))
    return r, z, min(p, 1.0)


# ── Grid execution ─────────────────────────────────────────────────
def run_grid():
    t0 = time.time()
    # per_run[(W, c_res, hyp)] = {"d_all":[], "d_win":[], "emr":[], "lat":[], "nl":[]}
    per_run = defaultdict(lambda: {"d_all": [], "d_win": [], "emr": [],
                                   "lat": [], "nl": [], "lr": []})

    for W in W_SWEEP:
        for seed in range(N_SEEDS):
            # provocation schedule shared across all hyps and all c_res for
            # this (W, seed): built from an independent rng.
            prov_rng = random.Random(10_000 * W + seed)
            provs, ptargets = m.build_provocations(prov_rng, N_PROV, W,
                                                   SIM_DAYS, PROV_VALUE,
                                                   PRE_WAR, P_STANDING)
            novel_tids = {pr["S"] for pr in provs if pr["kind"] == "novel"}
            emergent_tids = EMERGENT_BASE | novel_tids

            for c_res in C_RES_SWEEP:
                for hyp in HYPS:
                    _, log, _ = m.run_single(
                        hyp, PRE_AUTH, seed=seed, days=SIM_DAYS,
                        attrition_profile="phase2_residual",
                        tempo_mode="phase2", residual_p=c_res,
                        provocations=provs, prov_targets=None,
                        prov_value=PROV_VALUE, return_log=True)
                    d_all, d_win, lat = m.attribution_correlation(log, provs, W)
                    emr = m.overall_emergent_ratio(log, emergent_tids)
                    cell = per_run[(W, c_res, hyp)]
                    cell["d_all"].append(d_all)
                    cell["d_win"].append(d_win)
                    cell["emr"].append(emr)
                    cell["lat"].extend(lat)
                    cell["nl"].append(len(log))
                    cell["lr"].append(len(log) / SIM_DAYS)  # mean daily launch rate

    elapsed = time.time() - t0
    return per_run, elapsed


def discriminate(per_run, W, c_res, metric):
    x = per_run[(W, c_res, "H1")][metric]
    y = per_run[(W, c_res, "H2")][metric]
    r, z, p = mann_whitney(x, y)
    d = cohen_d(x, y)
    return r, p, d, _mean(x), _mean(y)


def _median(v):
    if not v:
        return None
    s = sorted(v)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


# ── Reporting ──────────────────────────────────────────────────────
def write_report(per_run, elapsed, path_txt, path_csv):
    lines = []
    lines.append("PHASE II LEG 1 — ATTRITION-CORRELATION DISCRIMINATION")
    lines.append("=" * 68)
    lines.append(f"seeds={N_SEEDS}  days={SIM_DAYS}  n_prov={N_PROV}  "
                 f"prov_value={PROV_VALUE}  runtime={elapsed:.1f}s")
    lines.append("Metric: H1 (adaptive) vs H2 (pre-programmed). "
                 "r = rank-biserial (+ means H1>H2).")
    lines.append("D_all = correlated/all strikes ; D_win = correlated/in-window strikes")
    lines.append("EMR = full emergent ratio (unobservable v4-style comparator). "
                 "CTX = r(D_all) vs r(EMR): observable proxy vs unobservable ceiling (not a strict ratio).")
    lines.append("")

    rows = []
    for W in W_SWEEP:
        tag = "PRIMARY (72h)" if W == 3 else "ROBUSTNESS (48h)"
        lines.append(f"--- WINDOW W={W}d  {tag} ---")
        lines.append(f"{'c_res':>6} | {'r(LR)':>7} {'p(LR)':>7} | "
                     f"{'r(D_all)':>9} {'p':>7} {'d':>6} | {'r(D_win)':>9} | "
                     f"{'r(EMR)':>7} | {'H1 Dall':>7} {'H2':>5} {'H3':>6} | {'lat':>4}")
        for c_res in C_RES_SWEEP:
            r_lr, p_lr, d_lr, _, _ = discriminate(per_run, W, c_res, "lr")
            r_all, p_all, d_all, m1_all, m2_all = discriminate(per_run, W, c_res, "d_all")
            r_win, p_win, d_win, m1_win, m2_win = discriminate(per_run, W, c_res, "d_win")
            r_emr, p_emr, d_emr, m1_emr, m2_emr = discriminate(per_run, W, c_res, "emr")
            m3_all = _mean(per_run[(W, c_res, "H3")]["d_all"])
            lat_med = _median(per_run[(W, c_res, "H1")]["lat"])
            lines.append(
                f"{c_res:>6.2f} | {r_lr:>7.3f} {p_lr:>7.3f} | "
                f"{r_all:>9.3f} {p_all:>7.4f} {d_all:>6.2f} | {r_win:>9.3f} | "
                f"{r_emr:>7.3f} | {m1_all:>7.3f} {m2_all:>5.2f} {m3_all:>6.3f} | "
                f"{(lat_med if lat_med is not None else 0):>4.1f}")
            rows.append({
                "W": W, "c_res": c_res,
                "r_LR": round(r_lr, 4), "p_LR": round(p_lr, 5),
                "r_D_all": round(r_all, 4), "p_D_all": round(p_all, 5),
                "d_D_all": round(d_all, 3),
                "r_D_win": round(r_win, 4), "p_D_win": round(p_win, 5),
                "r_EMR": round(r_emr, 4), "p_EMR": round(p_emr, 5),
                "mean_H1_D_all": round(m1_all, 4),
                "mean_H2_D_all": round(m2_all, 4),
                "mean_H3_D_all": round(m3_all, 4),
                "lat_median_days": lat_med if lat_med is not None else "",
            })
        lines.append("")

    lines.append("READ:")
    lines.append("  r(LR): launch-rate discrimination H1 vs H2 on the SAME runs. Near 0 / p>0.05")
    lines.append("    reproduces the v4 null: launch volume is blind to C2 state here too.")
    lines.append("  r(D_all): the observable attribution-correlation proxy. High + p<0.001 means")
    lines.append("    the discriminator that launch rate cannot see becomes sharp once attrition")
    lines.append("    stops swamping targeting. The LR-vs-D_all contrast on identical runs is the")
    lines.append("    paper's core result.")
    lines.append("  r(EMR): the v4-style full emergent ratio (unobservable ceiling), for context.")
    lines.append("  H2 D_all > 0 is the coincidence floor (standing provokers, codebook §8).")
    lines.append("  Separation is near-complete because H1/H2 are idealized archetypes; the real")
    lines.append("  force is a mixture (cf. H3, and empirical Stream B ~0.64).")

    report = "\n".join(lines)
    with open(path_txt, "w") as f:
        f.write(report + "\n")
    with open(path_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return report


if __name__ == "__main__":
    per_run, elapsed = run_grid()
    report = write_report(per_run, elapsed,
                          "../data_phase2/phase2_discrimination.txt",
                          "../data_phase2/phase2_discrimination.csv")
    print(report)
