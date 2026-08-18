"""
Generate three publication figures as SVG for the MILCOM paper.
Fig 1: Launcher attrition curve (3-phase decay)
Fig 2: Launch rate comparison H1/H2/H3 (showing overlap)
Fig 3: Emergent target ratio (showing clear separation)
"""

import csv
import os
from collections import defaultdict

# Load sensitivity data (baseline window)
data = []
with open("../data/sensitivity_results.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["window"] == "25-40 days (baseline)":
            data.append(row)

# ── SVG helpers ────────────────────────────────────────────────────

def svg_header(w, h, title=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <style>
    text {{ font-family: 'Times New Roman', serif; }}
    .axis {{ stroke: #333; stroke-width: 1; }}
    .grid {{ stroke: #ddd; stroke-width: 0.5; }}
    .title {{ font-size: 13px; font-weight: bold; fill: #111; }}
    .label {{ font-size: 10px; fill: #333; }}
    .tick {{ font-size: 9px; fill: #555; }}
    .legend {{ font-size: 9px; fill: #333; }}
  </style>
  <rect width="{w}" height="{h}" fill="white"/>
'''

def svg_footer():
    return "</svg>"

def polyline(points, color, width=1.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'  <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}"{d}/>\n'

# ── Figure 1: Launcher Attrition Curve ────────────────────────────

def make_fig1():
    # Print-first: no grid, axis to the true inventory (420), source on figure.
    # "Today (d23)" dropped — it is a perishable snapshot, not a data point.
    W, H = 480, 310
    mx, my, mr, mb = 58, 18, 16, 52
    pw, ph = W - mx - mr, H - my - mb
    N0 = 420

    days = list(range(0, 61))

    def surv(d):
        if d <= 3:
            return 1.0 - (0.50 * d / 3)
        if d <= 7:
            return 0.50 - (0.25 * (d - 3) / 4)
        if d <= 12:
            return 0.25 - (0.01 * (d - 7))
        return max(0.05, 0.20 - (0.003 * (d - 12)))

    vals = [surv(d) * N0 for d in days]

    def xy(d, v):
        return mx + (d / 60) * pw, my + ph - (v / N0) * ph

    svg = svg_header(W, H)
    # Range-frame axes (data extrema)
    x0, y_top = xy(0, N0)
    x1, y_bot = xy(60, 0)
    svg += f'  <line x1="{x0}" y1="{y_bot}" x2="{x0}" y2="{y_top}" class="axis"/>\n'
    svg += f'  <line x1="{x0}" y1="{y_bot}" x2="{x1}" y2="{y_bot}" class="axis"/>\n'

    for v in (0, 210, 420):
        _, y = xy(0, v)
        svg += f'  <text x="{mx-6}" y="{y+3}" text-anchor="end" class="tick">{v}</text>\n'
    for d in (0, 3, 7, 12, 30, 60):
        x, _ = xy(d, 0)
        svg += f'  <text x="{x}" y="{my+ph+12}" text-anchor="middle" class="tick">{d}</text>\n'

    svg += f'  <text x="{W/2}" y="{H-22}" text-anchor="middle" class="label">day of conflict</text>\n'
    svg += (
        f'  <text x="12" y="{(my+my+ph)/2}" text-anchor="middle" class="label" '
        f'transform="rotate(-90,12,{(my+my+ph)/2})">surviving launchers (of {N0})</text>\n'
    )

    pts = [xy(d, v) for d, v in zip(days, vals)]
    svg += polyline(pts, "#1a1a1a", 1.6)

    # Phase breaks as ticks on the data, not floating words
    for d, name in ((3, "50%"), (7, "75%")):
        x, y = xy(d, surv(d) * N0)
        svg += f'  <circle cx="{x}" cy="{y}" r="2.4" fill="#1a1a1a"/>\n'
        svg += f'  <text x="{x+4}" y="{y-5}" class="tick">{name}</text>\n'
    xb, yb = xy(12, 100)
    svg += f'  <circle cx="{xb}" cy="{yb}" r="2.4" fill="#1a1a1a"/>\n'
    svg += f'  <text x="{xb+4}" y="{yb-5}" class="tick">Bloomberg ~100</text>\n'

    svg += (
        f'  <text x="8" y="{H-6}" class="tick" fill="#666">'
        f'Parametric attrition used by the simulation (N0={N0}). '
        f'Bloomberg mark is the OSINT plateau anchor, not a fitted series. '
        f'generate_figures.py.</text>\n'
    )
    svg += svg_footer()
    return svg

# ── Figure 2: Launch Rate Comparison ──────────────────────────────

def make_fig2():
    W, H = 480, 300
    mx, my, mr, mb = 55, 30, 20, 40
    pw, ph = W - mx - mr, H - my - mb

    # Extract data by hypothesis
    hyp_data = defaultdict(list)
    for row in data:
        hyp_data[row["hypothesis"]].append((int(row["day"]), float(row["launches_mean"])))

    max_val = max(v for h in hyp_data for _, v in hyp_data[h])

    svg = svg_header(W, H)
    svg += f'  <text x="{W/2}" y="18" text-anchor="middle" class="title">Fig. 2. Daily Launch Rate by C2 Hypothesis (Baseline Window)</text>\n'

    # Axes
    svg += f'  <line x1="{mx}" y1="{my}" x2="{mx}" y2="{my+ph}" class="axis"/>\n'
    svg += f'  <line x1="{mx}" y1="{my+ph}" x2="{mx+pw}" y2="{my+ph}" class="axis"/>\n'

    for v in [0, 15, 30, 45, 60]:
        y = my + ph - (v / max_val) * ph
        svg += f'  <line x1="{mx}" y1="{y}" x2="{mx+pw}" y2="{y}" class="grid"/>\n'
        svg += f'  <text x="{mx-5}" y="{y+3}" text-anchor="end" class="tick">{v}</text>\n'

    for d in [0, 10, 20, 30, 40, 50, 60, 70]:
        if d <= 75:
            x = mx + (d/75)*pw
            svg += f'  <text x="{x}" y="{my+ph+14}" text-anchor="middle" class="tick">{d}</text>\n'

    svg += f'  <text x="{W/2}" y="{H-5}" text-anchor="middle" class="label">Day of Conflict</text>\n'
    svg += f'  <text x="12" y="{H/2}" text-anchor="middle" class="label" transform="rotate(-90,12,{H/2})">Mean Daily Launches</text>\n'

    colors = {"H1": "#2563eb", "H2": "#dc2626", "H3": "#16a34a"}
    labels = {"H1": "H1: Active C2", "H2": "H2: Pre-Programmed", "H3": "H3: Mixed"}

    for h in ["H1", "H2", "H3"]:
        pts = [(mx + (d/75)*pw, my + ph - (v/max_val)*ph) for d, v in hyp_data[h]]
        svg += polyline(pts, colors[h], 1.8)

    # Legend
    ly = my + 10
    for i, h in enumerate(["H1", "H2", "H3"]):
        lx = mx + pw - 130
        svg += f'  <line x1="{lx}" y1="{ly + i*14}" x2="{lx+20}" y2="{ly + i*14}" stroke="{colors[h]}" stroke-width="2"/>\n'
        svg += f'  <text x="{lx+25}" y="{ly + i*14 + 3}" class="legend">{labels[h]}</text>\n'

    # Annotation: overlap region
    svg += f'  <text x="{mx + pw/2}" y="{my + ph - 15}" text-anchor="middle" class="legend" fill="#666">Curves overlap: p > 0.05, d &lt; 0.15</text>\n'

    # Day 23 marker
    x23 = mx + (23/75)*pw
    svg += f'  <line x1="{x23}" y1="{my}" x2="{x23}" y2="{my+ph}" stroke="#f97316" stroke-width="1" stroke-dasharray="4 3"/>\n'

    svg += svg_footer()
    return svg

# ── Figure 3: Emergent Target Ratio ──────────────────────────────

def make_fig3():
    W, H = 480, 300
    mx, my, mr, mb = 55, 30, 20, 40
    pw, ph = W - mx - mr, H - my - mb

    hyp_data = defaultdict(list)
    for row in data:
        hyp_data[row["hypothesis"]].append((int(row["day"]), float(row["emergent_ratio_mean"])))

    max_val = 0.15  # scale to show detail

    svg = svg_header(W, H)
    svg += f'  <text x="{W/2}" y="18" text-anchor="middle" class="title">Fig. 3. Emergent Target Ratio by C2 Hypothesis</text>\n'

    svg += f'  <line x1="{mx}" y1="{my}" x2="{mx}" y2="{my+ph}" class="axis"/>\n'
    svg += f'  <line x1="{mx}" y1="{my+ph}" x2="{mx+pw}" y2="{my+ph}" class="axis"/>\n'

    for v_raw in [0.0, 0.03, 0.06, 0.09, 0.12, 0.15]:
        y = my + ph - (v_raw / max_val) * ph
        svg += f'  <line x1="{mx}" y1="{y}" x2="{mx+pw}" y2="{y}" class="grid"/>\n'
        svg += f'  <text x="{mx-5}" y="{y+3}" text-anchor="end" class="tick">{v_raw:.2f}</text>\n'

    for d in [0, 5, 10, 15, 20, 25, 30]:
        x = mx + (d/30)*pw
        svg += f'  <text x="{x}" y="{my+ph+14}" text-anchor="middle" class="tick">{d}</text>\n'

    svg += f'  <text x="{W/2}" y="{H-5}" text-anchor="middle" class="label">Day of Conflict</text>\n'
    svg += f'  <text x="12" y="{H/2}" text-anchor="middle" class="label" transform="rotate(-90,12,{H/2})">Emergent Target Ratio</text>\n'

    colors = {"H1": "#2563eb", "H2": "#dc2626", "H3": "#16a34a"}
    labels = {"H1": "H1: Active C2", "H2": "H2: Pre-Programmed", "H3": "H3: Mixed"}

    # Only show first 30 days (where the action is)
    for h in ["H1", "H2", "H3"]:
        pts = [(mx + (d/30)*pw, my + ph - (min(v, max_val)/max_val)*ph)
               for d, v in hyp_data[h] if d <= 30]
        svg += polyline(pts, colors[h], 2)

    # Legend
    ly = my + 10
    for i, h in enumerate(["H1", "H2", "H3"]):
        lx = mx + pw - 140
        svg += f'  <line x1="{lx}" y1="{ly + i*14}" x2="{lx+20}" y2="{ly + i*14}" stroke="{colors[h]}" stroke-width="2"/>\n'
        svg += f'  <text x="{lx+25}" y="{ly + i*14 + 3}" class="legend">{labels[h]}</text>\n'

    # Annotation: H2 = 0
    svg += f'  <text x="{mx + pw/2}" y="{my + ph - 5}" text-anchor="middle" class="legend" fill="#dc2626">H2 = 0.000 (cannot target emergent)</text>\n'

    # Annotation: separation
    svg += f'  <text x="{mx + 80}" y="{my + 60}" class="legend" fill="#2563eb">d = 0.86, p &lt; 0.001</text>\n'

    svg += svg_footer()
    return svg

# ── Generate all figures ──────────────────────────────────────────

outdir = "../figures"
os.makedirs(outdir, exist_ok=True)

for name, func in [("fig1_attrition", make_fig1),
                    ("fig2_launch_rate", make_fig2),
                    ("fig3_emergent_ratio", make_fig3)]:
    svg = func()
    path = os.path.join(outdir, f"{name}.svg")
    with open(path, "w") as f:
        f.write(svg)
    print(f"Generated: {path}")

print("Done. Converting to PNG...")
