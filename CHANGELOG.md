# Changelog

All notable changes to this companion repository are documented here.

## [Unreleased] — 2026-08-10

### Added

- **Phase II claim gate** `verify_phase2_claims.py` (claim id `milcom-phase2-observability`):
  thin MC residual LR-null + D_win discrimination + Leg 3 coding null band
- `claim-manifest.json` now lists both magazine-null and phase2-observability
- `results/phase2_claim_verify.json`; claim-holds brief updated

### Notes

- Publication augment (CRE / release-sync) does **not** own sim gates — see skill yield to
  `computational-claim-gate`. Phase II had no gate entry until this change.

## [Phase II paper v0.2] — 2026-08-09

### Added

- **Phase II preprint** deposited (PDF-only paper concept, separate from software):
  - Concept DOI: [10.5281/zenodo.21865793](https://doi.org/10.5281/zenodo.21865793)
  - Version DOI: [10.5281/zenodo.21865794](https://doi.org/10.5281/zenodo.21865794)
  - File: `paper/PHASE2_C2_Observability_REL_FIXED.pdf`
  - OSF mirror: [osf.io/c8rgz](https://osf.io/c8rgz/) ([10.17605/OSF.IO/C8RGZ](https://doi.org/10.17605/OSF.IO/C8RGZ))
- Deposit craft (Chokmah Research Engine): `paper/ZENODO-PAPER-DESCRIPTION.md`,
  `paper/PAPER-SOFTWARE-BRIDGE.md`
- Repo DOI map: `ZENODO.md`
- Citation surfaces updated: `CITATION.cff` (preferred-citation → Phase II concept),
  README Phase II badges/bibtex, `paper/README.md`

### Scientific content (paper v0.2)

- Legs 1–3: residual-force ABM + sparse-window coding + July OOS / H_ceiling
- Leg 2 retro-audit; count-corrected FIXED release

### Notes

- Paper concept ≠ software concept (`19210120`). Do not co-deposit PDF + zip.
- Parent v4 paper remains [10.5281/zenodo.19558494](https://doi.org/10.5281/zenodo.19558494).

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
