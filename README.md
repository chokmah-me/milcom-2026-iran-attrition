# milcom-2026-iran-attrition

Companion code and data for two related papers:

> **v4.** Daniyel Yaacov Bilar. "Launcher Attrition Dominates Command Architecture: Agent-Based Analysis of IRGC Missile C2 Degradation in the 2026 Iran War."

> **Phase II.** Daniyel Yaacov Bilar. "Below the Masking Threshold: Observable Command-and-Control Discrimination in a Residual IRGC Missile Force."

**Author:** Daniyel Yaacov Bilar, Chokmah LLC  
**Contact:** chokmah-dyb@pm.me  

| Surface | DOI |
|---------|-----|
| **Phase II paper concept** (always latest PDF) | [10.5281/zenodo.21865793](https://doi.org/10.5281/zenodo.21865793) |
| Phase II paper v0.3 (this PDF) | [10.5281/zenodo.21926014](https://doi.org/10.5281/zenodo.21926014) |
| Phase II OSF mirror | [osf.io/c8rgz](https://osf.io/c8rgz/) ([10.17605/OSF.IO/C8RGZ](https://doi.org/10.17605/OSF.IO/C8RGZ)) |
| v4 paper version | [10.5281/zenodo.19558494](https://doi.org/10.5281/zenodo.19558494) |
| Software concept (always latest code) | [10.5281/zenodo.19210120](https://doi.org/10.5281/zenodo.19210120) |

Full concept vs version map: [ZENODO.md](ZENODO.md).

**License:** Code: MIT. Paper and data: CC-BY 4.0. See [LICENSE](LICENSE) and [LICENSE-DATA](LICENSE-DATA).

**Claim gates:** `python verify_milcom_claims.py` (v4 magazine-discipline null) and `python verify_phase2_claims.py` (Phase II residual LR-null + D_win discrimination + Leg3 null band). Or `verify_claim_project.py --project .` for both via `claim-manifest.json`. See [Computational claim gate](#computational-claim-gate-thin-mc).

---

## What this repo contains

```
simulation/              Python simulation code (stdlib only, no dependencies)
verify_milcom_claims.py  Computational claim gate (thin MC)
claim-manifest.json      Claim-gate manifest (cd-claim-gate/v1)
results/                 Gate evidence + claim-holds brief
figures/                 Publication figures (v4 SVGs + Phase II)
artifacts/               Interactive JSX dashboards for browser exploration
data/                    Pre-computed CSV results and plain-text reports
data_phase2/             Phase II discrimination outputs
paper/                   Phase II FIXED PDF/source + coding tables + deposit craft
ZENODO.md                Paper/software concept vs version DOI map
CHANGELOG.md
```

---

## Requirements

Python 3.8 or later. No external dependencies. The entire simulation stack uses Python's standard library only: `random`, `math`, `csv`, `json`, `os`, `collections`, `dataclasses`.

---

## Quickstart

```bash
git clone https://github.com/chokmah-me/milcom-2026-iran-attrition
cd milcom-2026-iran-attrition

# 1) Claim gates first (~3s total): v4 magazine null + Phase II observability
#    Exit 0 = load-bearing thin MC still holds (not full paper grids)
python verify_milcom_claims.py
python verify_phase2_claims.py
# Or both via computational-claim-gate:
# python path/to/computational-claim-gate/scripts/verify_claim_project.py --project .

# 2) Full v4 Workstream A grid (~1 min) — publication-scale null table
cd simulation
python workstream_a_runner.py
```

Pre-computed `data/` and `figures/` are already in the tree if you only need archived outputs. Full step-by-step reproduce: [Reproducing the results](#reproducing-the-results).

---

## Computational claim gate (thin MC)

**What it is.** Fast, seeded harnesses that re-run *load-bearing simulation* claims and fail with a clear reason if they break. Prefer after edits to `c2_core.py`, attrition/rationing, residual tempo, or provocation mechanics.

### Claim A — `milcom-magazine-null` (`verify_milcom_claims.py`, n_runs=20)

- H1/H2/H3 smoke: valid series; launches > 0; attrition reduces force size
- **Magazine-discipline null:** early launches do not discriminate H1 from H2 under `v3_realistic` + `coordinated`
- **v1 reference null:** same for `v1_original` + rationing `v1`

### Claim B — `milcom-phase2-observability` (`verify_phase2_claims.py`, n_seeds=20)

- **Residual launch-rate null** at c_res ∈ {0.20, 0.50, 0.65}, W=3 (72h)
- **D_win attribution discrimination:** H1 > H2 with large rank-biserial r on the same runs
- **Leg 3 coding-scheme null band:** dense-provocation coincidence rate ∈ [0.55, 0.72] for the locked reference cell

**Not checked:** full Workstream A 4×3×50 / 107/108; full Phase II 200-seed grid; empirical coding tables; figure regeneration. Policy: `results/claim-holds-brief.md`.

```bash
python verify_milcom_claims.py
python verify_phase2_claims.py
python path/to/computational-claim-gate/scripts/verify_claim_project.py --project .
```

Manifest: `claim-manifest.json`.

---

## Reproducing the results

The claim gate above is the **fast** check. Steps below regenerate publication artifacts.

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

Writes `statistical_analysis.txt` and `statistical_results.json` to `data/`.

**Step 4. Regenerate SVG figures**

```bash
python generate_figures.py
```

Reads `../data/sensitivity_results.csv`, writes SVGs to `../figures/`.

Pre-computed outputs for all steps are already in `data/` and `figures/` if you want to skip re-running the simulation.

---

## v4.0: Magazine-Discipline Validation (April 13, 2026)

Paper version 4.0 adds Section V-D, validating the magazine-discipline
conjecture from v2/v3 via a 1,800-run re-simulation under post-conflict
attrition profiles. The null result on launch-rate discrimination is
reproduced in 107 of 108 tests.

### Running the v4 experiment

```bash
cd simulation
python workstream_a_runner.py    # ~1 min, writes data_v3/wsA_*
python generate_figures_v3.py    # writes figures/fig4_*.svg, fig5_*.svg
```

`workstream_a_runner.py` must run before `generate_figures_v3.py`
(Fig. 5 reads from `wsA_daily_timeseries.csv`).

### What's new in c2_core.py

Three new attrition profiles calibrated to 40-50% survival at the
April 8 ceasefire:

- `v1_original` — March 23 calibration (invalidated by post-conflict IC)
- `v3_realistic` — gradual decline, 45% at d39
- `v3_front_loaded` — fast early kill, plateau at 42%
- `v3_plateau_high` — steep initial drop, 49% plateau

Three magazine-discipline rationing modes:

- `off` — no rationing beyond base firing rate
- `individual` — per-cell sigmoid gate on magazine depletion
- `coordinated` — adds force-wide scarcity signal

`run_single` accepts both as keyword arguments. Defaults (`v1_original`,
`v1`) reproduce v1 paper output bit-for-bit.

### v4 headline results

| Finding | Value |
|---|---|
| Launch rate H1 vs H2, v3_realistic + coordinated, early | p = 0.92, r = +0.004 (ns) |
| Launch rate H1 vs H2, all phases under v3_realistic | 9 of 9 tests p > 0.05 |
| Full grid null: 4 profiles x 3 modes x 3 phases x 3 pairs | 107 of 108 ns |
| Emergent target ratio H1 vs H2, v3_realistic | r = 0.706, p < 0.001 |
| v1 reference reproduction | matches published null |

### Verifying the refactor didn't break v1

```bash
cd simulation
python sensitivity_analysis.py
diff ../data/sensitivity_results.csv ../data/sensitivity_results_v1_archive.csv
```

Should produce no output. If you didn't archive `sensitivity_results.csv`
before applying the refactor, check out the v1.0 tag and regenerate:

```bash
git checkout v1.0 -- simulation/
python simulation/sensitivity_analysis.py   # writes v1 CSV
git checkout main -- simulation/
python simulation/sensitivity_analysis.py   # writes v4 CSV (same content)
```

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

Two simulation configurations are provided. The **base simulation** (`c2_degradation_sim.py`) models 85 launch cells across five geographic regions (East Azerbaijan, Lorestan, Kermanshah, Isfahan, Hormozgan) and runs 30 Monte Carlo seeds per hypothesis by default. The **sensitivity analysis** (`sensitivity_analysis.py`) uses a calibrated 120-cell model across five operational regions (West Iran, East Azerbaijan, Central Iran, South Coast, Northeast), reflecting an estimated pre-war inventory of 410-440 launchers at ~3.5 TELs per cell. Three competing C2 hypotheses are modeled in both:

- **H1 (Active Distributed C2):** Connected cells receive updated targeting including conflict-emergent targets.
- **H2 (Pre-Programmed Execution):** Cells execute pre-authorized target packages on synchronized clocks regardless of connectivity.
- **H3 (Mixed Degradation):** Connected cells follow H1 behavior; disconnected cells follow H2.

Launcher attrition is calibrated as an exogenous three-phase curve against open-source conflict data: 50% in 3 days, 75% by day 7, plateau near 100 surviving units from day 12. The sensitivity analysis runs 40 seeds per hypothesis per expiry window (600 runs total across 5 windows).

---

## Citation

**Phase II paper** (prefer concept DOI for always-latest PDF):

```bibtex
@article{bilar2026masking,
  title   = {Below the Masking Threshold: Observable Command-and-Control
             Discrimination in a Residual {IRGC} Missile Force},
  author  = {Bilar, Daniyel Yaacov},
  year    = {2026},
  version = {0.2},
  doi     = {10.5281/zenodo.21865793},
  note    = {Version pin: 10.5281/zenodo.21926014; OSF mirror 10.17605/OSF.IO/C8RGZ}
}
```

**Parent (v4) paper:**

```bibtex
@inproceedings{bilar2026launcher,
  title     = {Launcher Attrition Dominates Command Architecture:
               Agent-Based Analysis of {IRGC} Missile {C2} Degradation
               in the 2026 Iran War},
  author    = {Bilar, Daniyel Yaacov},
  booktitle = {Proceedings of MILCOM 2026},
  year      = {2026},
  note      = {Submitted},
  doi       = {10.5281/zenodo.19558494}
}
```

**Software concept:** `10.5281/zenodo.19210120`. See [ZENODO.md](ZENODO.md) and [CITATION.cff](CITATION.cff).

---

## Acknowledgments

Portions of the simulation code, statistical analysis pipelines, and manuscript drafting were produced with assistance from Claude (Anthropic, claude-sonnet-4-6). The author is solely responsible for all analytical conclusions, methodological decisions, and claims.
