#!/usr/bin/env python3
"""
Computational claim gate — Phase II (residual-force C2 observability).

Load-bearing *simulation* claims (thin MC, not paper's 200-seed full grid):
  1. Residual-regime launch-rate null: under phase2_residual + phase2 tempo,
     early/window-matched launch totals do not discriminate H1 from H2
     (p > 0.05, |r| small) at swept residual connectivity.
  2. Attribution-correlation discrimination: D_win (primary 72h window)
     separates H1 from H2 sharply (p < 0.05, rank-biserial r above floor)
     on the same runs.

Also: Leg 3 coding-scheme null floor sanity (stdlib coincidence model) —
dense-provocation pre-programmed rate lands in the paper's 0.55–0.72 band
for the locked reference cell (p_frame=1, p_attr=0.5, 1 prov/day).

Non-claims: full 200-seed × c_res × W grid; empirical coding tables; H_ceiling
rate 0.500 as a sim output; figure regeneration.

Exit 0 iff all checks pass. Prints why each check fails.
"""

from __future__ import annotations

import json
import math
import random
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SIM = ROOT / "simulation"
sys.path.insert(0, str(SIM))

import c2_core as m  # noqa: E402
import leg3_null_sim as leg3  # noqa: E402

# ---------------------------------------------------------------------------
# Gate policy (thin MC)
# ---------------------------------------------------------------------------
N_SEEDS = 20  # paper Leg 1 uses 200
SIM_DAYS = 60
PRE_AUTH = (25, 40)
N_PROV = 8
PROV_VALUE = 1.2
P_STANDING = 0.5
W_PRIMARY = 3  # 72h
C_RES_GATE = [0.20, 0.50, 0.65]  # low / mid / high of paper sweep (skip one for speed)

# Launch-rate null (same spirit as v4 thin gate)
P_LR_NULL_MIN = 0.05
R_LR_NULL_MAX = 0.35  # slightly looser than 0.25 — residual tempo + thin N

# Attribution discrimination (D_win)
P_ATTR_MAX = 0.05
R_ATTR_MIN = 0.50  # paper cells are ~0.83–1.0; thin N still well above 0.5

# Leg 3 null band (paper §VI)
LEG3_NULL_LO = 0.55
LEG3_NULL_HI = 0.72

RESULTS = ROOT / "results"

_BASE = m.build_targets()
PRE_WAR = [(tid, t.value) for tid, t in _BASE.items() if t.active_since == 0]


def _fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def _ok(msg: str) -> None:
    print(f"OK:   {msg}")


def _normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def mann_whitney(x, y):
    """Signed rank-biserial r (x>y → r>0), two-sided p. Same posture as phase2_runner."""
    n1, n2 = len(x), len(y)
    n = n1 + n2
    if n1 == 0 or n2 == 0:
        return 0.0, 1.0
    combined = sorted([(v, 0) for v in x] + [(v, 1) for v in y], key=lambda t: t[0])
    ranks = [0.0] * n
    tie_terms = 0.0
    i = 0
    while i < n:
        j = i
        while j + 1 < n and combined[j + 1][0] == combined[i][0]:
            j += 1
        avg = (i + j + 2) / 2.0
        for k in range(i, j + 1):
            ranks[k] = avg
        t = j - i + 1
        if t > 1:
            tie_terms += t**3 - t
        i = j + 1
    R1 = sum(ranks[k] for k in range(n) if combined[k][1] == 0)
    U1 = R1 - n1 * (n1 + 1) / 2.0
    r = 2.0 * U1 / (n1 * n2) - 1.0
    mu = n1 * n2 / 2.0
    sigma2 = (n1 * n2 / 12.0) * ((n + 1) - tie_terms / (n * (n - 1))) if n > 1 else 0.0
    if sigma2 <= 0:
        return 0.0, 1.0
    U = min(U1, n1 * n2 - U1)
    z = (U - mu + 0.5) / math.sqrt(sigma2) if U < mu else (U - mu - 0.5) / math.sqrt(sigma2)
    p = 2.0 * (1.0 - _normal_cdf(abs(z)))
    return r, min(p, 1.0)


def run_thin_grid():
    """Shared provocations across hyps; thin seeds × selected c_res; W=3 only."""
    per = defaultdict(lambda: {"d_win": [], "lr": []})
    for seed in range(N_SEEDS):
        prov_rng = random.Random(10_000 * W_PRIMARY + seed)
        provs, _ = m.build_provocations(
            prov_rng, N_PROV, W_PRIMARY, SIM_DAYS, PROV_VALUE, PRE_WAR, P_STANDING
        )
        for c_res in C_RES_GATE:
            for hyp in ("H1", "H2"):
                _, log, _ = m.run_single(
                    hyp,
                    PRE_AUTH,
                    seed=seed,
                    days=SIM_DAYS,
                    attrition_profile="phase2_residual",
                    tempo_mode="phase2",
                    residual_p=c_res,
                    provocations=provs,
                    prov_targets=None,
                    prov_value=PROV_VALUE,
                    return_log=True,
                )
                d_all, d_win, lat = m.attribution_correlation(log, provs, W_PRIMARY)
                cell = per[(c_res, hyp)]
                cell["d_win"].append(d_win)
                cell["lr"].append(len(log) / SIM_DAYS)
    return per


def check_leg1_thin(per) -> dict:
    cells = []
    for c_res in C_RES_GATE:
        h1_lr = per[(c_res, "H1")]["lr"]
        h2_lr = per[(c_res, "H2")]["lr"]
        h1_w = per[(c_res, "H1")]["d_win"]
        h2_w = per[(c_res, "H2")]["d_win"]
        r_lr, p_lr = mann_whitney(h1_lr, h2_lr)
        r_win, p_win = mann_whitney(h1_w, h2_w)
        mean_h1 = sum(h1_w) / len(h1_w)
        mean_h2 = sum(h2_w) / len(h2_w)
        print(
            f"[phase2 c_res={c_res:.2f}] "
            f"LR: p={p_lr:.4f} r={r_lr:.4f} | "
            f"D_win: p={p_win:.4f} r={r_win:.4f} "
            f"mean H1={mean_h1:.3f} H2={mean_h2:.3f}"
        )

        if p_lr <= P_LR_NULL_MIN:
            _fail(
                f"c_res={c_res}: launch-rate expected null (p>{P_LR_NULL_MIN}) "
                f"but p={p_lr:.4f}"
            )
        if abs(r_lr) >= R_LR_NULL_MAX:
            _fail(
                f"c_res={c_res}: launch-rate |r|={abs(r_lr):.4f} >= {R_LR_NULL_MAX} "
                f"(thin-gate null band)"
            )
        _ok(f"c_res={c_res}: launch-rate null p={p_lr:.4f} |r|={abs(r_lr):.4f}")

        if p_win >= P_ATTR_MAX:
            _fail(
                f"c_res={c_res}: D_win expected discrimination (p<{P_ATTR_MAX}) "
                f"but p={p_win:.4f}"
            )
        if r_win < R_ATTR_MIN:
            _fail(
                f"c_res={c_res}: D_win r={r_win:.4f} < {R_ATTR_MIN} "
                f"(attribution proxy should separate H1>H2)"
            )
        _ok(f"c_res={c_res}: D_win discrimination p={p_win:.4f} r={r_win:.4f}")

        cells.append(
            {
                "c_res": c_res,
                "n_seeds": N_SEEDS,
                "W": W_PRIMARY,
                "launch_rate": {"p": p_lr, "rank_biserial_r": r_lr, "ok": True},
                "d_win": {
                    "p": p_win,
                    "rank_biserial_r": r_win,
                    "mean_h1": mean_h1,
                    "mean_h2": mean_h2,
                    "ok": True,
                },
            }
        )
    return {
        "ok": True,
        "policy": {
            "p_lr_null_min": P_LR_NULL_MIN,
            "r_lr_null_max": R_LR_NULL_MAX,
            "p_attr_max": P_ATTR_MAX,
            "r_attr_min": R_ATTR_MIN,
        },
        "cells": cells,
    }


def check_leg3_null_band() -> dict:
    """Coding-scheme coincidence floor under dense provocation (not ABM)."""
    rate = leg3.run(
        n_events=1000,
        n_targets=8,
        p_attr=0.5,
        p_frame=1.0,
        window=3,
        provocations_per_day=1.0,
        seed=1,
    )
    print(f"[leg3-null] dense p_frame=1 p_attr=0.5 1/day → rate={rate:.3f}")
    if rate < LEG3_NULL_LO or rate > LEG3_NULL_HI:
        _fail(
            f"leg3 null rate {rate:.3f} outside paper band "
            f"[{LEG3_NULL_LO}, {LEG3_NULL_HI}]"
        )
    _ok(f"leg3 null rate {rate:.3f} in [{LEG3_NULL_LO}, {LEG3_NULL_HI}]")
    return {
        "ok": True,
        "rate": rate,
        "band": [LEG3_NULL_LO, LEG3_NULL_HI],
        "params": {
            "p_frame": 1.0,
            "p_attr": 0.5,
            "provocations_per_day": 1.0,
            "n_events": 1000,
            "seed": 1,
        },
    }


def main() -> int:
    print("verify_phase2_claims.py — Phase II computational claim gate (thin MC)")
    print(
        f"n_seeds={N_SEEDS} days={SIM_DAYS} W={W_PRIMARY} "
        f"c_res={C_RES_GATE} (paper Leg1 uses 200 seeds × full sweep)"
    )
    print("non-claims: full grid; empirical coding; H_ceiling 0.500 as sim output")
    print()

    t0 = time.perf_counter()
    per = run_thin_grid()
    print()
    leg1 = check_leg1_thin(per)
    print()
    leg3_rep = check_leg3_null_band()
    elapsed = time.perf_counter() - t0

    RESULTS.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "milcom-phase2-claim-verify/v1",
        "ok": True,
        "elapsed_sec": round(elapsed, 3),
        "leg1_thin": leg1,
        "leg3_null_band": leg3_rep,
    }
    out = RESULTS / "phase2_claim_verify.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print()
    print(f"wrote {out}  elapsed={elapsed:.1f}s")
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError:
        raise SystemExit(1)
