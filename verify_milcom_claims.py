#!/usr/bin/env python3
"""
Computational claim gate for milcom-2026-iran-attrition.

Load-bearing *simulation* claims (thin MC, not the full 50-run × grid paper run):
  1. Smoke: H1/H2/H3 produce valid daily series with positive launch activity.
  2. Magazine-discipline null (v4 / Workstream A headline): under
     attrition_profile=v3_realistic + rationing_mode=coordinated, early-phase
     launch totals do not discriminate H1 from H2 (p > 0.05, small effect).
  3. v1 reference null: v1_original + rationing_mode=v1 also fails to
     discriminate H1 from H2 on the same early metric (paper baseline).

Non-claims: full 4×3 grid × 50 seeds; 107/108 null count across all cells;
phase2 observability suite; figure regeneration.

Exit 0 iff all checks pass. Prints why each check fails.
"""

from __future__ import annotations

import json
import math
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SIM = ROOT / "simulation"
sys.path.insert(0, str(SIM))

from c2_core import run_single  # noqa: E402

# ---------------------------------------------------------------------------
# Gate policy
# ---------------------------------------------------------------------------
N_RUNS = 20  # paper workstream uses 50
DAYS = 40
EXPIRY = (25, 40)
EARLY = range(0, 10)

# Null-result policy (matches paper framing: fail to reject H0 at α=0.05,
# and rank-biserial effect stays small). Thin-N is noisier → allow r < 0.25.
P_NULL_MIN = 0.05
R_NULL_MAX = 0.25

RESULTS = ROOT / "results"


def _fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def _ok(msg: str) -> None:
    print(f"OK:   {msg}")


def cohens_d(a, b):
    if not a or not b:
        return 0.0
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    sa = math.sqrt(sum((x - ma) ** 2 for x in a) / max(len(a) - 1, 1))
    sb = math.sqrt(sum((x - mb) ** 2 for x in b) / max(len(b) - 1, 1))
    sp = math.sqrt((sa ** 2 + sb ** 2) / 2)
    return abs(ma - mb) / sp if sp > 0 else 0.0


def mann_whitney_u(a, b):
    """Returns (U, z, p, rank_biserial) — same pattern as workstream_a_runner."""
    if not a or not b:
        return 0, 0, 1.0, 0.0
    combined = [(v, "a") for v in a] + [(v, "b") for v in b]
    combined.sort(key=lambda x: x[0])
    ranked = []
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + j + 1) / 2
        for k in range(i, j):
            ranked.append((combined[k][0], combined[k][1], avg_rank))
        i = j
    r1 = sum(x[2] for x in ranked if x[1] == "a")
    n1, n2 = len(a), len(b)
    u1 = r1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    mu = n1 * n2 / 2
    sigma = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    z = (u1 - mu) / sigma if sigma > 0 else 0
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    r_rb = 1 - (2 * min(u1, u2)) / (n1 * n2) if n1 * n2 > 0 else 0.0
    return u1, z, p, r_rb


def early_launch_totals(profile: str, mode: str, hyp: str, n_runs: int) -> list[float]:
    """One sample per MC run: sum of launches on days 0..9 (early phase)."""
    vals = []
    for run in range(n_runs):
        seed = hash((profile, mode, hyp, run, "wsA")) % (2 ** 31)
        daily = run_single(
            hyp,
            EXPIRY,
            seed=seed,
            days=DAYS,
            attrition_profile=profile,
            rationing_mode=mode,
        )
        vals.append(float(sum(d["launches"] for d in daily if d["day"] in EARLY)))
    return vals


def check_smoke() -> dict:
    """API + basic dynamics invariants."""
    report = {"runs": []}
    for hyp in ("H1", "H2", "H3"):
        daily = run_single(hyp, EXPIRY, seed=0, days=20)
        if not daily:
            _fail(f"{hyp}: empty daily series")
        keys = set(daily[0].keys())
        need = {"day", "launches", "emergent_ratio", "alive_cells"}
        if not need.issubset(keys):
            _fail(f"{hyp}: missing keys {need - keys}")
        total = sum(d["launches"] for d in daily)
        if total <= 0:
            _fail(f"{hyp}: zero total launches over 20 days")
        alive0 = daily[0]["alive_cells"]
        alive_last = daily[-1]["alive_cells"]
        if alive0 <= 0:
            _fail(f"{hyp}: no alive cells at day 0")
        # Attrition should not increase force size
        if alive_last > alive0 + 1e-9:
            _fail(f"{hyp}: alive_cells rose {alive0} -> {alive_last}")
        report["runs"].append(
            {
                "hypothesis": hyp,
                "days": len(daily),
                "total_launches": total,
                "alive0": alive0,
                "alive_last": alive_last,
            }
        )
        _ok(
            f"smoke {hyp}: launches={total} alive {alive0}->{alive_last} "
            f"over {len(daily)} days"
        )
    report["ok"] = True
    return report


def check_null_pair(profile: str, mode: str, label: str) -> dict:
    h1 = early_launch_totals(profile, mode, "H1", N_RUNS)
    h2 = early_launch_totals(profile, mode, "H2", N_RUNS)
    u, z, p, r_rb = mann_whitney_u(h1, h2)
    d = cohens_d(h1, h2)
    mean1, mean2 = sum(h1) / len(h1), sum(h2) / len(h2)

    print(
        f"[{label}] {profile}+{mode} early H1_vs_H2: "
        f"n={N_RUNS} p={p:.4f} r={r_rb:.4f} d={d:.4f} "
        f"mean H1={mean1:.1f} H2={mean2:.1f}"
    )

    if p <= P_NULL_MIN:
        _fail(
            f"{label}: expected null (p > {P_NULL_MIN}) but p={p:.4f} — "
            f"launch rate discriminates H1 from H2 under {profile}/{mode}"
        )
    _ok(f"{label}: p={p:.4f} > {P_NULL_MIN} (null holds)")

    if r_rb >= R_NULL_MAX:
        _fail(
            f"{label}: rank-biserial r={r_rb:.4f} >= {R_NULL_MAX} "
            f"(effect not small enough for thin-gate null)"
        )
    _ok(f"{label}: |effect| r={r_rb:.4f} < {R_NULL_MAX}")

    return {
        "ok": True,
        "label": label,
        "profile": profile,
        "rationing": mode,
        "n_runs": N_RUNS,
        "phase": "early_days_0_9_sum",
        "comparison": "H1_vs_H2",
        "p": p,
        "rank_biserial_r": r_rb,
        "cohens_d": d,
        "mean_h1": mean1,
        "mean_h2": mean2,
        "policy": {"p_null_min": P_NULL_MIN, "r_null_max": R_NULL_MAX},
    }


def main() -> int:
    print("verify_milcom_claims.py — computational claim gate (thin MC)")
    print(f"n_runs={N_RUNS} days={DAYS} (paper workstream uses 50 runs)")
    print("non-claims: full grid null count 107/108; phase2; figures")
    print()

    t0 = time.perf_counter()
    smoke = check_smoke()
    print()
    null_v3 = check_null_pair("v3_realistic", "coordinated", "magazine-discipline")
    print()
    null_v1 = check_null_pair("v1_original", "v1", "v1-reference")
    elapsed = time.perf_counter() - t0

    RESULTS.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "milcom-claim-verify/v1",
        "ok": True,
        "elapsed_sec": round(elapsed, 3),
        "smoke": smoke,
        "null_magazine_discipline": null_v3,
        "null_v1_reference": null_v1,
    }
    out = RESULTS / "milcom_claim_verify.json"
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
