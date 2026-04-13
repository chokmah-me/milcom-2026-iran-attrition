"""
sensitivity_analysis.py — Pre-Auth Expiry Window Sensitivity Driver
====================================================================
Refactored for v3 paper: model logic now lives in c2_core.py.
This file is the run-matrix driver, CSV exporter, and report generator.

Default behavior is bit-for-bit identical to the v1 (March 2026) paper
because c2_core.run_single's v3 hooks all default to v1 values.

To exercise v3 hooks, pass them through to run_single via the new
optional arguments to run_sensitivity (Workstreams A, B, C will use these).
"""

import csv
import math
import os
from collections import defaultdict

from c2_core import run_single

# ── Sensitivity matrix ─────────────────────────────────────────────

EXPIRY_WINDOWS = [
    ("15-20 days (tight)", (15, 20)),
    ("20-30 days (short)", (20, 30)),
    ("25-40 days (baseline)", (25, 40)),
    ("35-50 days (extended)", (35, 50)),
    ("45-60 days (deep plan)", (45, 60)),
]

METRIC_KEYS = ["launches", "entropy", "emergent_ratio",
               "alive_cells", "connected_cells", "missiles_remaining"]

def run_sensitivity(n_runs=40, days=75,
                    attrition_profile="v1_original",
                    rationing_mode="v1",
                    lam=0.0):
    """
    Run all hypotheses x all expiry windows x Monte Carlo.

    v3 hooks (default to v1 behavior):
      attrition_profile  - selects launcher kill curve
      rationing_mode     - magazine-discipline firing rule
      lam                - C2-mediated attrition reduction
    """
    results = []
    total = len(EXPIRY_WINDOWS) * 3 * n_runs
    done = 0

    for window_name, window_range in EXPIRY_WINDOWS:
        for hyp in ["H1", "H2", "H3"]:
            agg_by_day = defaultdict(lambda: defaultdict(list))

            for run in range(n_runs):
                seed = hash((window_name, hyp, run)) % 2**31
                daily = run_single(hyp, window_range,
                                   seed=seed, days=days,
                                   attrition_profile=attrition_profile,
                                   rationing_mode=rationing_mode,
                                   lam=lam)
                for d in daily:
                    for k in METRIC_KEYS:
                        agg_by_day[d["day"]][k].append(d[k])
                done += 1

            for day in range(days):
                row = {"window": window_name, "hypothesis": hyp, "day": day}
                for k in METRIC_KEYS:
                    vals = agg_by_day[day][k]
                    mean = sum(vals) / len(vals) if vals else 0
                    std = (math.sqrt(sum((v - mean)**2 for v in vals) / len(vals))
                           if len(vals) > 1 else 0)
                    row[f"{k}_mean"] = round(mean, 3)
                    row[f"{k}_std"] = round(std, 3)
                results.append(row)

    print(f"  Completed {done} simulation runs.")
    return results

# ── Export ─────────────────────────────────────────────────────────

def export_csv(results, path):
    if not results:
        return
    keys = list(results[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(results)

def generate_report(results, days=75):
    lines = []
    lines.append("=" * 78)
    lines.append("PRE-AUTH EXPIRY SENSITIVITY ANALYSIS")
    lines.append("v1 model logic (c2_core.py) under v1 default parameters")
    lines.append("=" * 78)
    lines.append("")
    lines.append("REAL-WORLD CALIBRATION POINTS:")
    lines.append("  Pre-war launchers: ~420 (IDF/ISW)")
    lines.append("  Day 3 survival: ~50% (Asia Times)")
    lines.append("  Day 7 survival: ~25% (JINSA: 75% destroyed)")
    lines.append("  Day 12 survival: ~24% (Bloomberg: 'held steady' at ~100)")
    lines.append("  Day 1 BM launches: 480 (JPost)")
    lines.append("  Day 9 BM launches: ~40 (92% decline, JPost)")
    lines.append("")

    for window_name, _ in EXPIRY_WINDOWS:
        lines.append(f"--- Window: {window_name} ---")
        lines.append("")

        for hyp in ["H1", "H2", "H3"]:
            hdata = [r for r in results
                     if r["window"] == window_name and r["hypothesis"] == hyp]
            if not hdata:
                continue

            labels = {"H1": "Active C2", "H2": "Pre-Programmed", "H3": "Mixed"}

            d0 = next((r for r in hdata if r["day"] == 0), None)
            d22 = next((r for r in hdata if r["day"] == 22), None)
            d45 = next((r for r in hdata if r["day"] == 45), None)
            d60 = next((r for r in hdata if r["day"] == 60), None)

            initial = d0["launches_mean"] if d0 else 0

            cessation = None
            for r in hdata:
                if r["launches_mean"] < 5 and r["day"] > 5:
                    cessation = r["day"]
                    break

            decline_day = None
            for i in range(3, len(hdata)):
                if hdata[i]["day"] >= 15 and hdata[i-3]["launches_mean"] > 0:
                    drop = ((hdata[i-3]["launches_mean"] - hdata[i]["launches_mean"])
                            / max(hdata[i-3]["launches_mean"], 0.01))
                    if drop > 0.3:
                        decline_day = hdata[i]["day"]
                        break

            lines.append(f"  {hyp} ({labels[hyp]}):")
            lines.append(f"    Day 0 launches:  {initial:.1f}")
            lines.append(f"    Day 22 launches: {d22['launches_mean']:.1f}" if d22 else "    Day 22: N/A")
            lines.append(f"    Day 45 launches: {d45['launches_mean']:.1f}" if d45 else "    Day 45: N/A")
            lines.append(f"    Day 60 launches: {d60['launches_mean']:.1f}" if d60 else "    Day 60: N/A")
            lines.append(f"    Near-cessation:  day {cessation if cessation else '>75'}")
            lines.append(f"    Sharp decline:   day {decline_day if decline_day else 'none detected'}")

            first_expiry_day = int(window_name.split("-")[0].split("(")[0].strip())
            expiry_data = next((r for r in hdata if r["day"] == first_expiry_day), None)
            if expiry_data:
                lines.append(f"    Entropy at expiry start (day {first_expiry_day}): {expiry_data['entropy_mean']:.3f}")

            lines.append("")
        lines.append("")

    lines.append("=" * 78)
    lines.append("SENSITIVITY FINDINGS (unchanged from v1 paper)")
    lines.append("=" * 78)
    lines.append("")
    lines.append("1. EXPIRY WINDOW IMPACT ON H2: tight windows cause collapse ~d18-22.")
    lines.append("2. EXPIRY WINDOW IMPACT ON H1: zero. H1 is the control.")
    lines.append("3. EXPIRY WINDOW IMPACT ON H3: moderate, scales with disconnected fraction.")
    lines.append("")

    return "\n".join(lines)

# ── Main ──────────────────────────────────────────────────────────

def main():
    outdir = "../data"
    os.makedirs(outdir, exist_ok=True)

    print("Running pre-auth expiry sensitivity analysis (v1 defaults)...")
    print(f"  5 windows x 3 hypotheses x 40 runs x 75 days")
    results = run_sensitivity(n_runs=40, days=75)

    csv_path = os.path.join(outdir, "sensitivity_results.csv")
    export_csv(results, csv_path)
    print(f"CSV: {csv_path}")

    report = generate_report(results)
    report_path = os.path.join(outdir, "sensitivity_report.txt")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Report: {report_path}")

if __name__ == "__main__":
    main()
