# milcom-2026-iran-attrition system catalog

## c2-degradation-sim — agent-based C2 degradation pipeline

- **owner:** Daniyel Yaacov Bilar (Chokmah LLC) — chokmah-dyb@pm.me
- **status:** active
- **purpose:** Agent-based Monte Carlo simulation discriminating three hypotheses (H1 active distributed C2, H2 pre-programmed execution, H3 mixed degradation) for IRGC missile C2 under launcher attrition; produces the paper's quantitative results, sensitivity analysis, statistical tests, and figures.
- **inputs:** CLI args `--runs`, `--days`, `--outdir` (no external/network data — self-contained). Downstream steps read prior steps' CSVs from `data/` (e.g. `generate_figures.py` reads `data/sensitivity_results.csv`).
- **outputs:** `data/c2_simulation_results.csv` + `c2_simulation_report.txt`; `data/sensitivity_results.csv` + `sensitivity_report.txt`; `data/statistical_analysis.txt` + `statistical_results.json`; `figures/*.svg`.
- **dependencies:** Python 3.8+, **standard library only** (`random`, `math`, `csv`, `json`, `os`, `collections`, `dataclasses`). `c2_degradation_sim.py` depends on `c2_core.py`; figure step depends on the sensitivity step's output.
- **credentials/permissions:** none — fully offline, no secrets, no network calls.
- **failure modes:** The 4-step reproduction is **order-dependent** — running `generate_figures.py` / `statistical_tests.py` before their upstream CSVs exist → `FileNotFoundError`. Monte Carlo is stochastic; low `--runs` gives unstable statistics (paper used `--runs 50 --days 75`).
- **test_evidence:** Ran `python c2_degradation_sim.py --runs 5 --days 20 --outdir <scratch>` on 2026-07-19 → produced `c2_simulation_results.csv` + `c2_simulation_report.txt` as expected (executability confirmed, scratch dir, repo `data/` untouched). Committed reference outputs live in `data/`. Code DOI 10.5281/zenodo.19558036 (v4.0).
- **last_validated:** 2026-07-19
- **confidence:** fresh

Full 4-step reproduction runbook is in [README.md](README.md); build notes in `paper/`.

Decision note (2026-07-19): this session validated **executability** with reduced params
only (`--runs 5 --days 20`), not a full reproduction of the paper's headline numbers
(`--runs 50 --days 75`). `last_validated` reflects "confirmed runnable today," not
"re-derived every published figure." Related extensions in the same `simulation/` dir —
Phase 2 (`phase2_runner.py`, `workstream_a_runner.py`) and Leg 3 (`leg3_null_sim.py`,
committed today) — get their own entries once they stabilize.

## _legacy_v0_prototype.py — v0 prototype simulator

- **owner:** Daniyel Yaacov Bilar (Chokmah LLC)
- **status:** retired
- **purpose:** (historical) First-generation prototype of the C2 degradation simulator.
- **inputs:** n/a — not part of any current reproduction path.
- **outputs:** n/a
- **dependencies:** Python stdlib (historical).
- **credentials/permissions:** none.
- **failure modes:** n/a — not maintained; do not use for results.
- **test_evidence:** none — superseded, not exercised.
- **last_validated:** n/a (retired)
- **confidence:** unknown

Retired 2026-07-19 — self-declares `DEPRECATED: v0 prototype. Not used by v1/v4 results.
See c2_core.py.` Superseded by `c2_core.py` + `c2_degradation_sim.py`. Kept in-repo for
provenance, not deleted — but explicitly marked dead so it stops reading as a live system.
