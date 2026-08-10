# Claim-holds brief — milcom-2026-iran-attrition

## Status
**Verified** (thin Monte Carlo gates) — re-run 2026-08-10 via `computational-claim-gate`

## Claims

| id | command | exit | notes |
|----|---------|------|-------|
| `milcom-magazine-null` | `python verify_milcom_claims.py` | 0 | ~1.2s; n_runs=20 |
| `milcom-phase2-observability` | `python verify_phase2_claims.py` | 0 | ~1.1s; n_seeds=20 |

### Observed — magazine-discipline (v4 stack)

| check | result |
|-------|--------|
| Smoke H1/H2/H3 | valid daily series; launches > 0; attrition 120→21 |
| v3_realistic + coordinated early H1_vs_H2 | null (p > 0.05, r < 0.25) |
| v1_original + v1 early H1_vs_H2 | null (p > 0.05, r < 0.25) |

### Observed — Phase II (2026-08-10T01:55Z)

| check | result |
|-------|--------|
| Residual LR null @ c_res 0.20 / 0.50 / 0.65 | all p > 0.05, \|r\| < 0.35 |
| D_win H1>H2 @ same cells | all p ≈ 0, r ≥ 0.955 |
| Leg 3 dense coding null (p_frame=1, p_attr=0.5, 1/day) | rate 0.582 ∈ [0.55, 0.72] |

## Seeds / env / platform

- Magazine gate: `hash((profile, mode, hyp, run, "wsA")) % 2**31`; n=20; days=40
- Phase II gate: shared prov schedule per seed as `phase2_runner`; n_seeds=20; W=3; c_res ⊂ {0.20,0.50,0.65}
- Stdlib only

## Not checked here

- Full Workstream A grid (4×3×50) / published **107/108**
- Full Phase II 200-seed × full c_res × W∈{2,3} grid
- Empirical Leg 2/3 coding tables / observed Stream B 0.500 H_ceiling as a *sim* output
- Figure regeneration

## Evidence

- `results/milcom_claim_verify.json`
- `results/phase2_claim_verify.json`
- `results/claim_verify_meta.json` / `claim_verify_out.txt`
- `claim-manifest.json`

## Residual risk

Thin n can flap effect-size bands (magazine gate has seen one r-band miss in-session). Green gates do **not** replace publication grids: `workstream_a_runner.py`, `phase2_runner.py`.
