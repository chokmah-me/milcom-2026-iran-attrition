"""
generate_phase2_figure.py — Fig. 1 for the Phase II short paper.
Two panels, primary window (72h):
  (a) discrimination r (H1 vs H2) vs connectivity: launch rate (blind) vs
      attribution correlation D_win (sharp). The core contrast.
  (b) mean attribution correlation D_win by hypothesis vs connectivity.
Re-runs the grid (~30s) so the figure and the report never drift.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import phase2_runner as R

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.linewidth": 0.8,
    "figure.dpi": 150,
})

W = 3  # primary window
per, _ = R.run_grid()
cs = R.C_RES_SWEEP

r_lr = [R.discriminate(per, W, c, "lr")[0] for c in cs]
r_dw = [R.discriminate(per, W, c, "d_win")[0] for c in cs]
h1 = [R._mean(per[(W, c, "H1")]["d_win"]) for c in cs]
h2 = [R._mean(per[(W, c, "H2")]["d_win"]) for c in cs]
h3 = [R._mean(per[(W, c, "H3")]["d_win"]) for c in cs]

fig, (axA, axB) = plt.subplots(1, 2, figsize=(9.2, 3.9))

# Panel A: the contrast
axA.axhline(0, color="0.7", lw=0.6, zorder=0)
axA.plot(cs, r_dw, "o-", color="black", lw=1.8, ms=6,
         label="Attribution correlation")
axA.plot(cs, r_lr, "s--", color="0.55", lw=1.6, ms=6,
         label="Launch rate")
axA.set_ylim(-0.15, 1.08)
axA.set_xlim(0.15, 0.70)
axA.set_xticks(cs)
axA.set_xlabel("Reconstituted C2 connectivity")
axA.set_ylabel("H1 vs H2 discrimination (rank-biserial r)")
axA.set_title("(a) Same runs, two metrics")
axA.legend(loc="center right", frameon=False, fontsize=9)
axA.annotate("p < 0.001", (0.20, r_dw[0]), textcoords="offset points",
             xytext=(6, -12), fontsize=8, color="black")
axA.annotate("p > 0.05 (null)", (0.35, r_lr[1]), textcoords="offset points",
             xytext=(-4, 10), fontsize=8, color="0.4")

# Panel B: by-hypothesis signal
axB.plot(cs, h1, "o-", color="black", lw=1.8, ms=6, label="H1 active C2")
axB.plot(cs, h3, "^-", color="0.4", lw=1.6, ms=6, label="H3 mixed")
axB.plot(cs, h2, "s:", color="0.6", lw=1.6, ms=6, label="H2 pre-programmed")
axB.axhline(0.64, color="0.3", lw=0.9, ls="-.")
axB.annotate("empirical Stream B (0.64)", (0.155, 0.64),
             textcoords="offset points", xytext=(2, 4), fontsize=8, color="0.3")
axB.set_ylim(0, 0.72)
axB.set_xlim(0.15, 0.70)
axB.set_xticks(cs)
axB.set_xlabel("Reconstituted C2 connectivity")
axB.set_ylabel("Attribution correlation (in-window, D_win)")
axB.set_title("(b) Signal by hypothesis")
axB.legend(loc="upper left", frameon=False, fontsize=9)

fig.tight_layout()
for ext in ("png", "pdf"):
    fig.savefig(f"../figures/phase2_fig1_discrimination.{ext}", bbox_inches="tight")
print("wrote figures/phase2_fig1_discrimination.png/.pdf")
