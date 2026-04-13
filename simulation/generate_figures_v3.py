"""
generate_figures_v3.py — Figures 4 and 5 for paper v3.1
=========================================================
Fig 4: Attrition profile comparison (v1_original vs three v3 profiles)
       with post-conflict IC data points overlaid.
Fig 5: Launch rate under v3_realistic + coordinated rationing.
       Three overlapping H1/H2/H3 curves with ±1 sigma bands.

Style-matched to v1 Figs 1-3 (Times New Roman, same color palette,
same margin conventions).
"""

import csv
import os
from collections import defaultdict

# Style constants matching generate_figures.py
COLORS = {
    "H1": "#2563eb",
    "H2": "#dc2626",
    "H3": "#16a34a",
    "v1_original": "#6b7280",       # gray (reference/invalidated)
    "v3_realistic": "#2563eb",      # blue (headline profile)
    "v3_front_loaded": "#d97706",   # amber
    "v3_plateau_high": "#16a34a",   # green
}

def svg_header(w, h):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <style>
    text {{ font-family: 'Times New Roman', serif; }}
    .axis {{ stroke: #333; stroke-width: 1; }}
    .grid {{ stroke: #ddd; stroke-width: 0.5; }}
    .title {{ font-size: 13px; font-weight: bold; fill: #111; }}
    .label {{ font-size: 10px; fill: #333; }}
    .tick {{ font-size: 9px; fill: #555; }}
    .legend {{ font-size: 9px; fill: #333; }}
    .annot {{ font-size: 9px; fill: #666; font-style: italic; }}
  </style>
  <rect width="{w}" height="{h}" fill="white"/>
'''

def svg_footer():
    return "</svg>"

def polyline(points, color, width=1.8, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'  <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}"{d}/>\n'

def filled_band(upper_pts, lower_pts, color, opacity=0.15):
    """Shaded ±sigma band between two polylines."""
    pts = upper_pts + list(reversed(lower_pts))
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'  <polygon points="{pts_str}" fill="{color}" fill-opacity="{opacity}" stroke="none"/>\n'

# ── Fig 4: attrition profiles ─────────────────────────────────────

def make_fig4():
    # Pull attrition formulas directly from c2_core so this stays in sync
    import sys
    sys.path.insert(0, ".")
    from c2_core import compute_launcher_attrition

    W, H = 520, 320
    mx, my, mr, mb = 60, 35, 130, 45  # extra right margin for legend
    pw, ph = W - mx - mr, H - my - mb

    days = list(range(0, 45))
    profiles = [
        ("v1_original", "v1 (invalidated): 75% kill by d7", "4 2"),
        ("v3_realistic", "v3 realistic: ~45% at ceasefire", ""),
        ("v3_front_loaded", "v3 front-loaded: fast early", "2 2"),
        ("v3_plateau_high", "v3 plateau high: early drop", "6 3"),
    ]

    # y-axis: survival fraction 0 to 1
    svg = svg_header(W, H)
    svg += f'  <text x="{W/2}" y="20" text-anchor="middle" class="title">Fig. 4. Launcher Survival Under v1 vs v3 Attrition Profiles</text>\n'

    # Axes
    svg += f'  <line x1="{mx}" y1="{my}" x2="{mx}" y2="{my+ph}" class="axis"/>\n'
    svg += f'  <line x1="{mx}" y1="{my+ph}" x2="{mx+pw}" y2="{my+ph}" class="axis"/>\n'

    # Y grid + ticks (survival fraction)
    for v in [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]:
        y = my + ph - v * ph
        svg += f'  <line x1="{mx}" y1="{y:.1f}" x2="{mx+pw}" y2="{y:.1f}" class="grid"/>\n'
        svg += f'  <text x="{mx-5}" y="{y+3:.1f}" text-anchor="end" class="tick">{v:.1f}</text>\n'

    # X ticks
    for d in [0, 7, 14, 21, 28, 35, 39]:
        x = mx + (d/44)*pw
        svg += f'  <text x="{x:.1f}" y="{my+ph+14}" text-anchor="middle" class="tick">{d}</text>\n'

    svg += f'  <text x="{mx+pw/2:.1f}" y="{H-8}" text-anchor="middle" class="label">Day of Conflict</text>\n'
    svg += f'  <text x="14" y="{my+ph/2:.1f}" text-anchor="middle" class="label" transform="rotate(-90,14,{my+ph/2:.1f})">Fraction Surviving</text>\n'

    # Profile lines
    for prof_name, label, dash in profiles:
        vals = [compute_launcher_attrition(d, prof_name) for d in days]
        pts = [(mx + (d/44)*pw, my + ph - v*ph) for d, v in zip(days, vals)]
        svg += polyline(pts, COLORS[prof_name], 2, dash)

    # Post-conflict IC data points at d39
    # CNN: ~50% survival (0.50), AJC: ~40% survival (0.40)
    x39 = mx + (39/44)*pw
    y_cnn = my + ph - 0.50*ph
    y_ajc = my + ph - 0.40*ph
    svg += f'  <circle cx="{x39:.1f}" cy="{y_cnn:.1f}" r="4" fill="#111" stroke="white" stroke-width="1.5"/>\n'
    svg += f'  <circle cx="{x39:.1f}" cy="{y_ajc:.1f}" r="4" fill="#111" stroke="white" stroke-width="1.5"/>\n'
    svg += f'  <text x="{x39-6:.1f}" y="{y_cnn+3:.1f}" text-anchor="end" class="tick" fill="#111">CNN ~50%</text>\n'
    svg += f'  <text x="{x39-6:.1f}" y="{y_ajc+3:.1f}" text-anchor="end" class="tick" fill="#111">AJC ~40%</text>\n'

    # Ceasefire marker
    svg += f'  <line x1="{x39:.1f}" y1="{my}" x2="{x39:.1f}" y2="{my+ph}" stroke="#f97316" stroke-width="1" stroke-dasharray="4 3"/>\n'
    svg += f'  <text x="{x39+3:.1f}" y="{my+14}" class="tick" fill="#f97316">Ceasefire</text>\n'

    # Legend (right margin)
    lx = mx + pw + 10
    ly = my + 20
    for i, (prof_name, label, dash) in enumerate(profiles):
        yy = ly + i*22
        da = f' stroke-dasharray="{dash}"' if dash else ""
        svg += f'  <line x1="{lx}" y1="{yy}" x2="{lx+18}" y2="{yy}" stroke="{COLORS[prof_name]}" stroke-width="2"{da}/>\n'
        # Split label across two lines if long
        parts = label.split(": ")
        svg += f'  <text x="{lx+22}" y="{yy+2}" class="legend">{parts[0]}</text>\n'
        if len(parts) > 1:
            svg += f'  <text x="{lx+22}" y="{yy+12}" class="legend" fill="#666">{parts[1]}</text>\n'

    # IC data legend
    yy_ic = ly + 4*22 + 8
    svg += f'  <circle cx="{lx+9}" cy="{yy_ic}" r="3.5" fill="#111"/>\n'
    svg += f'  <text x="{lx+22}" y="{yy_ic+2}" class="legend">post-conflict IC</text>\n'

    svg += svg_footer()
    return svg

# ── Fig 5: launch rate under v3_realistic + coordinated ───────────

def make_fig5():
    # Load timeseries
    rows = []
    with open("../data_v3/wsA_daily_timeseries.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["profile"] == "v3_realistic" and row["rationing"] == "coordinated":
                rows.append({
                    "hypothesis": row["hypothesis"],
                    "day": int(row["day"]),
                    "mean": float(row["launches_mean"]),
                    "std": float(row["launches_std"]),
                })

    # Group by hypothesis
    by_hyp = defaultdict(list)
    for r in rows:
        by_hyp[r["hypothesis"]].append(r)
    for h in by_hyp:
        by_hyp[h].sort(key=lambda x: x["day"])

    # Determine max y for scaling
    max_y = max(r["mean"] + r["std"] for r in rows) * 1.1

    W, H = 520, 320
    mx, my, mr, mb = 60, 35, 130, 45
    pw, ph = W - mx - mr, H - my - mb

    max_day = 39

    svg = svg_header(W, H)
    svg += f'  <text x="{W/2}" y="20" text-anchor="middle" class="title">Fig. 5. Launch Rate Under v3 Realistic Attrition + Coordinated Rationing</text>\n'

    # Axes
    svg += f'  <line x1="{mx}" y1="{my}" x2="{mx}" y2="{my+ph}" class="axis"/>\n'
    svg += f'  <line x1="{mx}" y1="{my+ph}" x2="{mx+pw}" y2="{my+ph}" class="axis"/>\n'

    # Y grid/ticks
    y_ticks = [0, 10, 20, 30, 40, 50, 60]
    for v in y_ticks:
        if v > max_y:
            continue
        y = my + ph - (v / max_y) * ph
        svg += f'  <line x1="{mx}" y1="{y:.1f}" x2="{mx+pw}" y2="{y:.1f}" class="grid"/>\n'
        svg += f'  <text x="{mx-5}" y="{y+3:.1f}" text-anchor="end" class="tick">{v}</text>\n'

    # X ticks
    for d in [0, 7, 14, 21, 28, 35, 39]:
        x = mx + (d/max_day)*pw
        svg += f'  <text x="{x:.1f}" y="{my+ph+14}" text-anchor="middle" class="tick">{d}</text>\n'

    svg += f'  <text x="{mx+pw/2:.1f}" y="{H-8}" text-anchor="middle" class="label">Day of Conflict</text>\n'
    svg += f'  <text x="14" y="{my+ph/2:.1f}" text-anchor="middle" class="label" transform="rotate(-90,14,{my+ph/2:.1f})">Mean Daily Launches</text>\n'

    # Plot ±1 sigma bands first (so lines render on top)
    for hyp in ["H1", "H2", "H3"]:
        series = by_hyp[hyp]
        upper = [(mx + (r["day"]/max_day)*pw,
                  my + ph - min(r["mean"]+r["std"], max_y)/max_y * ph)
                 for r in series]
        lower = [(mx + (r["day"]/max_day)*pw,
                  my + ph - max(r["mean"]-r["std"], 0)/max_y * ph)
                 for r in series]
        svg += filled_band(upper, lower, COLORS[hyp], opacity=0.12)

    # Mean lines
    for hyp in ["H1", "H2", "H3"]:
        series = by_hyp[hyp]
        pts = [(mx + (r["day"]/max_day)*pw,
                my + ph - (r["mean"]/max_y)*ph)
               for r in series]
        svg += polyline(pts, COLORS[hyp], 2.0)

    # Legend
    lx = mx + pw + 10
    ly = my + 20
    labels = {"H1": "H1: Active C2", "H2": "H2: Pre-Programmed", "H3": "H3: Mixed"}
    for i, hyp in enumerate(["H1", "H2", "H3"]):
        yy = ly + i*18
        svg += f'  <line x1="{lx}" y1="{yy}" x2="{lx+18}" y2="{yy}" stroke="{COLORS[hyp]}" stroke-width="2"/>\n'
        svg += f'  <text x="{lx+22}" y="{yy+2}" class="legend">{labels[hyp]}</text>\n'

    # Annotation: null result
    annot_y = ly + 3*18 + 15
    svg += f'  <text x="{lx}" y="{annot_y}" class="annot">All phases:</text>\n'
    svg += f'  <text x="{lx}" y="{annot_y+12}" class="annot">p &gt; 0.05</text>\n'
    svg += f'  <text x="{lx}" y="{annot_y+24}" class="annot">r &lt; 0.07</text>\n'
    svg += f'  <text x="{lx}" y="{annot_y+44}" class="annot">N=50 seeds</text>\n'
    svg += f'  <text x="{lx}" y="{annot_y+56}" class="annot">per curve</text>\n'

    # Ceasefire marker
    x39 = mx + (39/max_day)*pw
    svg += f'  <line x1="{x39:.1f}" y1="{my}" x2="{x39:.1f}" y2="{my+ph}" stroke="#f97316" stroke-width="1" stroke-dasharray="4 3"/>\n'
    svg += f'  <text x="{x39-3:.1f}" y="{my+14}" text-anchor="end" class="tick" fill="#f97316">Ceasefire</text>\n'

    svg += svg_footer()
    return svg

# ── Run ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    outdir = "../figures"
    os.makedirs(outdir, exist_ok=True)

    for name, func in [("fig4_attrition_profiles", make_fig4),
                        ("fig5_v3_launch_rate", make_fig5)]:
        svg = func()
        path = os.path.join(outdir, f"{name}.svg")
        with open(path, "w") as f:
            f.write(svg)
        print(f"Generated: {path}")

    print("Done.")
