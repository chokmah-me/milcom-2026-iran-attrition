# Paper ↔ software bridge — Phase II (Below the Masking Threshold)

| Role | Identifier | Notes |
|------|------------|-------|
| Phase II paper concept DOI | [10.5281/zenodo.21865793](https://doi.org/10.5281/zenodo.21865793) | Always-latest Phase II PDF |
| Phase II paper version DOI (v0.3) | [10.5281/zenodo.21926014](https://doi.org/10.5281/zenodo.21926014) | This FIXED PDF |
| Parent (v4) paper concept DOI | [10.5281/zenodo.19210451](https://doi.org/10.5281/zenodo.19210451) | *Launcher Attrition Dominates…* always-latest |
| Parent (v4) paper version DOI | [10.5281/zenodo.19558494](https://doi.org/10.5281/zenodo.19558494) | v4.0 PDF |
| Software concept DOI | [10.5281/zenodo.19210120](https://doi.org/10.5281/zenodo.19210120) | Always-latest code/data companion |
| Software version DOI (current) | [10.5281/zenodo.21925910](https://doi.org/10.5281/zenodo.21925910) | v0.6.1 GitHub–Zenodo |

## Relation paragraph

Phase II is a **companion paper** to the v4 attrition-masking result: it tests whether an *observable* proxy (attribution correlation) can discriminate C2 architecture in a residual-force, low-attrition regime, and whether dense provocation saturates that proxy (Leg 3). The **PDF** is the scholarly argument (Legs 1–3). The **software concept** holds the executable model extension (`simulation/phase2_runner.py`, `leg3_null_sim.py`, `c2_core.py` residual profile), pre-computed outputs (`data_phase2/`), figures (`figures/phase2_fig1_*`), and pre-registration tables under `paper/leg3_*`. Paper PDF and software zip are **distinct Zenodo concepts** and must not be co-deposited as one concept.

## Dual-concept check

- [x] Paper and software are not described as one Zenodo concept
- [x] README should cite concept DOIs for “latest” where intended (post-mint release-sync)
- [x] Phase II PDF deposit will not include the code zip
- [x] Software chain already under concept `19210120`; Phase II paper is a **new** paper concept
