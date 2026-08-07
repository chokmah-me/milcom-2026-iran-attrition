# Changelog

All notable changes to this companion repository are documented here.

## [Unreleased] — 2026-08-07

### Added

- **Computational claim gate** for magazine-discipline null and sim smoke:
  - `verify_milcom_claims.py` — thin Monte Carlo harness (n_runs=20, days=40)
  - `claim-manifest.json` — `cd-claim-gate/v1` claim `milcom-magazine-null`
  - `results/` evidence: `claim_verify_meta.json`, `claim_verify_out.txt`,
    `milcom_claim_verify.json`, `claim-holds-brief.md`
- README **Quickstart** (verify-before full Workstream A) and structure tree entries
- This CHANGELOG

### Notes

- Gate checks H1–H3 smoke plus early-phase H1_vs_H2 null under
  `v3_realistic`/`coordinated` and the v1 reference — **not** a substitute for
  the full Workstream A grid or the published 107/108 null count
- Non-claims and residual risk: `results/claim-holds-brief.md`
- Re-run: `python verify_milcom_claims.py` or
  `verify_claim_project.py --project .` from computational-claim-gate
