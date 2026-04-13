"""
workstream_a_runner.py — v3 Magazine Discipline Experiment
============================================================
Runs the full Workstream A grid and reports Mann-Whitney U tests
on H1-vs-H2 launch-rate discrimination under each (attrition profile,
rationing mode) combination.

Grid (900 runs):
  3 hypotheses x 3 attrition profiles x 2 rationing modes x 50 seeds
  Baseline expiry window only (25-40 days).

Headline question:
  Under the v3_realistic attrition curve with coordinated magazine
  discipline, does launch-rate still fail to discriminate H1 from H2?
  If YES (p > 0.05, r < 0.15), the v3 paper's magazine-discipline
  conjecture is vindicated and the abstract/VI-D/conclusion hedges
  can be tightened.
  If NO (p < 0.05), the finding flips: magazine discipline does NOT
  mask C2 differences, and the paper needs a different reframe.
"""

import math
import os
import csv
from collections import defaultdict

from c2_core import run_single

# ── Grid specification ─────────────────────────────────────────────

ATTRITION_PROFILES = ["v1_original", "v3_realistic", "v3_front_loaded", "v3_plateau_high"]
RATIONING_MODES = ["off", "individual", "coordinated"]
HYPOTHESES = ["H1", "H2", "H3"]
EXPIRY_WINDOW = (25, 40)  # baseline
N_RUNS = 50
DAYS = 40  # run through d39 ceasefire

# v1 reference point uses v1 rationing, not the new modes
V1_REFERENCE = ("v1_original", "v1")

# ── Statistical tests (reused from statistical_tests.py pattern) ───

def cohens_d(a, b):
    if not a or not b: return 0.0
    ma, mb = sum(a)/len(a), sum(b)/len(b)
    sa = math.sqrt(sum((x-ma)**2 for x in a)/max(len(a)-1,1))
    sb = math.sqrt(sum((x-mb)**2 for x in b)/max(len(b)-1,1))
    sp = math.sqrt((sa**2 + sb**2) / 2)
    return abs(ma - mb) / sp if sp > 0 else 0.0

def _norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def mann_whitney_u(a, b):
    """Returns (U, z, p, rank_biserial)."""
    if not a or not b:
        return 0, 0, 1.0, 0.0
    combined = [(v, 'a') for v in a] + [(v, 'b') for v in b]
    combined.sort(key=lambda x: x[0])
    # Tie-corrected ranks
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

    r1 = sum(x[2] for x in ranked if x[1] == 'a')
    n1, n2 = len(a), len(b)
    u1 = r1 - n1*(n1+1)/2
    u2 = n1*n2 - u1
    mu = n1*n2/2
    sigma = math.sqrt(n1*n2*(n1+n2+1)/12)
    z = (u1 - mu) / sigma if sigma > 0 else 0
    p = 2 * (1 - _norm_cdf(abs(z)))
    # Rank-biserial correlation: 1 - 2U / (n1*n2)
    r_rb = 1 - (2 * min(u1, u2)) / (n1 * n2) if n1*n2 > 0 else 0.0
    return u1, z, p, r_rb

# ── Runner ─────────────────────────────────────────────────────────

def run_grid():
    """Execute full grid. Returns dict keyed by (profile, mode, hypothesis)."""
    results = {}
    total_combos = len(ATTRITION_PROFILES) * len(RATIONING_MODES) * len(HYPOTHESES)
    combos_done = 0

    print(f"Running {total_combos} combinations x {N_RUNS} seeds = "
          f"{total_combos * N_RUNS} total runs...")

    for profile in ATTRITION_PROFILES:
        for mode in RATIONING_MODES:
            for hyp in HYPOTHESES:
                # Per-run daily launch series; we'll aggregate to phases
                per_run_launches_by_day = defaultdict(list)
                per_run_emergent_by_day = defaultdict(list)
                for run in range(N_RUNS):
                    seed = hash((profile, mode, hyp, run, "wsA")) % 2**31
                    daily = run_single(hyp, EXPIRY_WINDOW,
                                       seed=seed, days=DAYS,
                                       attrition_profile=profile,
                                       rationing_mode=mode)
                    for d in daily:
                        per_run_launches_by_day[d["day"]].append(d["launches"])
                        per_run_emergent_by_day[d["day"]].append(d["emergent_ratio"])
                results[(profile, mode, hyp)] = {
                    "launches_by_day": dict(per_run_launches_by_day),
                    "emergent_by_day": dict(per_run_emergent_by_day),
                }
                combos_done += 1
                print(f"  [{combos_done}/{total_combos}] {profile:18s} {mode:12s} {hyp}")

    # Also run the v1 reference point (v1_original + v1 rationing)
    print(f"  [reference] v1_original  v1           (H1,H2,H3)")
    for hyp in HYPOTHESES:
        per_run_launches_by_day = defaultdict(list)
        per_run_emergent_by_day = defaultdict(list)
        for run in range(N_RUNS):
            seed = hash(("v1_original", "v1", hyp, run, "wsA")) % 2**31
            daily = run_single(hyp, EXPIRY_WINDOW,
                               seed=seed, days=DAYS,
                               attrition_profile="v1_original",
                               rationing_mode="v1")
            for d in daily:
                per_run_launches_by_day[d["day"]].append(d["launches"])
                per_run_emergent_by_day[d["day"]].append(d["emergent_ratio"])
        results[("v1_original", "v1", hyp)] = {
            "launches_by_day": dict(per_run_launches_by_day),
            "emergent_by_day": dict(per_run_emergent_by_day),
        }

    return results

def compute_discrimination(results, metric_key):
    """
    For each (profile, mode), compute H1-vs-H2, H1-vs-H3, H2-vs-H3
    Mann-Whitney U tests on early-phase (d0-9) aggregated metric values.
    """
    phases = [("early", range(0, 10)),
              ("mid", range(10, 25)),
              ("late", range(25, 40))]

    discrim_rows = []

    # All (profile, mode) combinations present in results
    combos = sorted({(p, m) for (p, m, h) in results.keys()})

    for profile, mode in combos:
        for phase_name, day_range in phases:
            for pair_a, pair_b in [("H1","H2"), ("H1","H3"), ("H2","H3")]:
                vals_a = []
                vals_b = []
                for d in day_range:
                    vals_a.extend(results[(profile, mode, pair_a)][metric_key].get(d, []))
                    vals_b.extend(results[(profile, mode, pair_b)][metric_key].get(d, []))
                d_eff = cohens_d(vals_a, vals_b)
                u, z, p, r_rb = mann_whitney_u(vals_a, vals_b)
                discrim_rows.append({
                    "profile": profile,
                    "rationing": mode,
                    "phase": phase_name,
                    "comparison": f"{pair_a}_vs_{pair_b}",
                    "n_a": len(vals_a),
                    "n_b": len(vals_b),
                    "cohens_d": round(d_eff, 4),
                    "rank_biserial_r": round(r_rb, 4),
                    "z": round(z, 4),
                    "p": round(p, 6),
                    "significant_at_0.05": p < 0.05,
                })
    return discrim_rows

def format_report(launch_rows, emergent_rows):
    lines = []
    lines.append("=" * 90)
    lines.append("WORKSTREAM A: MAGAZINE DISCIPLINE DISCRIMINATION ANALYSIS")
    lines.append("=" * 90)
    lines.append("")
    lines.append(f"Grid: {N_RUNS} runs x {len(HYPOTHESES)} hypotheses x "
                 f"{len(ATTRITION_PROFILES)} profiles x {len(RATIONING_MODES)} modes")
    lines.append(f"Expiry window: {EXPIRY_WINDOW} (baseline only)")
    lines.append(f"Campaign length: {DAYS} days (through April 8 ceasefire)")
    lines.append("")
    lines.append("Headline question: under v3_realistic + coordinated rationing,")
    lines.append("does launch rate discriminate H1 from H2?")
    lines.append("")

    # Launch-rate discrimination table
    lines.append("-" * 90)
    lines.append("LAUNCH RATE DISCRIMINATION (Mann-Whitney U, rank-biserial r)")
    lines.append("-" * 90)
    lines.append(f"{'profile':<18} {'rationing':<14} {'phase':<6} {'comparison':<12} "
                 f"{'r':>8} {'p':>9} {'sig':>6}")
    for row in launch_rows:
        sig_marker = ("***" if row["p"] < 0.001 else
                      "**"  if row["p"] < 0.01 else
                      "*"   if row["p"] < 0.05 else "ns")
        lines.append(f"{row['profile']:<18} {row['rationing']:<14} "
                     f"{row['phase']:<6} {row['comparison']:<12} "
                     f"{row['rank_biserial_r']:>8.3f} {row['p']:>9.4f} {sig_marker:>6}")
    lines.append("")

    # Emergent-ratio discrimination table (spot check only: H1 vs H2 early)
    lines.append("-" * 90)
    lines.append("EMERGENT TARGET RATIO DISCRIMINATION (spot check: early phase H1 vs H2)")
    lines.append("-" * 90)
    lines.append(f"{'profile':<18} {'rationing':<14} "
                 f"{'r':>8} {'p':>9} {'sig':>6}")
    for row in emergent_rows:
        if row["phase"] != "early" or row["comparison"] != "H1_vs_H2":
            continue
        sig_marker = ("***" if row["p"] < 0.001 else
                      "**"  if row["p"] < 0.01 else
                      "*"   if row["p"] < 0.05 else "ns")
        lines.append(f"{row['profile']:<18} {row['rationing']:<14} "
                     f"{row['rank_biserial_r']:>8.3f} {row['p']:>9.4f} {sig_marker:>6}")
    lines.append("")

    # Headline extract
    lines.append("=" * 90)
    lines.append("HEADLINE FINDING")
    lines.append("=" * 90)
    headline = [r for r in launch_rows
                if r["profile"] == "v3_realistic"
                and r["rationing"] == "coordinated"
                and r["comparison"] == "H1_vs_H2"]
    for r in headline:
        verdict = "MASKED (null result holds)" if r["p"] > 0.05 else "DISCRIMINATED"
        lines.append(f"  v3_realistic + coordinated, {r['phase']:6s} phase: "
                     f"p={r['p']:.4f}, r={r['rank_biserial_r']:+.3f}  -> {verdict}")
    lines.append("")

    # Compare to v1 baseline
    v1_baseline = [r for r in launch_rows
                   if r["profile"] == "v1_original"
                   and r["rationing"] == "v1"
                   and r["comparison"] == "H1_vs_H2"
                   and r["phase"] == "early"]
    if v1_baseline:
        r = v1_baseline[0]
        lines.append(f"  v1 reference (early H1_vs_H2): p={r['p']:.4f}, "
                     f"r={r['rank_biserial_r']:+.3f}")
        lines.append("  (should reproduce the paper's v1 null result)")
    lines.append("")

    return "\n".join(lines)

# ── Main ───────────────────────────────────────────────────────────

def main():
    outdir = "../data_v3"
    os.makedirs(outdir, exist_ok=True)

    results = run_grid()

    print("\nComputing discrimination statistics...")
    launch_rows = compute_discrimination(results, "launches_by_day")
    emergent_rows = compute_discrimination(results, "emergent_by_day")

    # Write CSVs
    for name, rows in [("wsA_launch_discrimination", launch_rows),
                        ("wsA_emergent_discrimination", emergent_rows)]:
        path = os.path.join(outdir, f"{name}.csv")
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"  CSV: {path}")

    # Write report
    report = format_report(launch_rows, emergent_rows)
    report_path = os.path.join(outdir, "wsA_report.txt")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"  Report: {report_path}\n")
    print(report)

if __name__ == "__main__":
    main()
