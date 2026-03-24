# milcom-2026-iran-attrition

Companion code and data for:

> Daniyel Yaacov Bilar. "Launcher Attrition Dominates Command Architecture: Agent-Based Analysis of IRGC Missile C2 Degradation in the 2026 Iran War." *MILCOM 2026* (submitted).

**Author:** Daniyel Yaacov Bilar, Chokmah LLC  
**Contact:** chokmah-dyb@pm.me  
**DOI:** *(assigned by Zenodo on release)*  
**License:** Code: MIT. Paper and data: CC-BY 4.0. See [LICENSE](LICENSE) and [LICENSE-DATA](LICENSE-DATA).

---

## What this repo contains

```
simulation/         Python simulation code (stdlib only, no dependencies)
figures/            Publication SVG figures (Figs 1-3)
artifacts/          Interactive JSX dashboards for browser exploration
data/               Pre-computed CSV results and plain-text reports
paper/              Paper manuscript (v8)
```

---

## Requirements

Python 3.8 or later. No external dependencies. The entire simulation stack uses Python's standard library only: `random`, `math`, `csv`, `json`, `os`, `collections`, `dataclasses`.

---

## Reproducing the results

Run from the `simulation/` directory.

**Step 1. Base agent-based simulation (3 hypotheses, Monte Carlo)**

```bash
cd simulation
python c2_degradation_sim.py --runs 50 --days 75 --outdir ../data
```

This writes `c2_simulation_results.csv` and `c2_simulation_report.txt` to `data/`.

**Step 2. Sensitivity analysis (5 pre-authorization expiry windows)**

```bash
python sensitivity_analysis.py
```

Writes `sensitivity_results.csv` and `sensitivity_report.txt` to `data/`.

**Step 3. Statistical tests (Mann-Whitney U, Cohen's d)**

```bash
python statistical_tests.py
```

Writes `statistical_analysis.txt` to `data/`.

**Step 4. Regenerate SVG figures**

```bash
python generate_figures.py
```

Reads `../data/sensitivity_results.csv`, writes SVGs to `../figures/`.

Pre-computed outputs for all steps are already in `data/` and `figures/` if you want to skip re-running the simulation.

---

## Key results

| Finding | Value |
|---|---|
| Launch rate H1 vs H2, early phase | p = 0.779, r = 0.004 (ns) |
| Launch rate H1 vs H2, all phases | p > 0.05, r < 0.08 (ns) |
| Emergent target ratio H1 vs H2, early | p < 0.001, d = 0.78-0.86 (large) |
| Strongest discriminator | Emergent target ratio (all windows) |
| Sensitivity to expiry window | Negligible under 70%+ attrition in week 1 |

The central finding: **launch rate cannot distinguish C2 hypothesis when launcher attrition exceeds 70% in week one.** The emergent target ratio is the only reliable discriminator, but is currently inaccessible from open sources.

---

## Interactive artifacts

`artifacts/c2_simulation_dashboard.jsx` and `artifacts/sensitivity_dashboard.jsx` are self-contained React components that render the simulation results interactively. They can be loaded in any React environment or on Claude.ai.

---

## Simulation design

The simulation models 120 IRGC launch cells across five operational regions (West Iran, East Azerbaijan, Central Iran, South Coast, Northeast), reflecting an estimated pre-war inventory of 410-440 launchers at ~3.5 TELs per cell. Three competing C2 hypotheses are modeled:

- **H1 (Active Distributed C2):** Connected cells receive updated targeting including conflict-emergent targets.
- **H2 (Pre-Programmed Execution):** Cells execute pre-authorized target packages on synchronized clocks regardless of connectivity.
- **H3 (Mixed Degradation):** Connected cells follow H1 behavior; disconnected cells follow H2.

Launcher attrition is calibrated as an exogenous three-phase curve against open-source conflict data: 50% in 3 days, 75% by day 7, plateau near 100 surviving units from day 12. Monte Carlo analysis runs 50 seeds per hypothesis per expiry window (1,350 runs total).

---

## Citation

```bibtex
@inproceedings{bilar2026launcher,
  title     = {Launcher Attrition Dominates Command Architecture:
               Agent-Based Analysis of {IRGC} Missile {C2} Degradation
               in the 2026 Iran War},
  author    = {Bilar, Daniyel Yaacov},
  booktitle = {Proceedings of MILCOM 2026},
  year      = {2026},
  note      = {Submitted},
  doi       = {}
}
```

---

## Acknowledgments

Portions of the simulation code, statistical analysis pipelines, and manuscript drafting were produced with assistance from Claude (Anthropic, claude-sonnet-4-6). The author is solely responsible for all analytical conclusions, methodological decisions, and claims.
