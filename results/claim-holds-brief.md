# Claim-holds brief — milcom-2026-iran-attrition

## Status
**Verified** (thin Monte Carlo gate)

## Claims

| id | command | exit | notes |
|----|---------|------|-------|
| `milcom-magazine-null` | `python verify_milcom_claims.py` | 0 | ~2s; n_runs=20 |

### Observed (gate run)

| check | result |
|-------|--------|
| Smoke H1/H2/H3 | valid daily series; launches > 0; attrition reduces alive cells |
| v3_realistic + coordinated early H1_vs_H2 | p≈0.73, r≈0.07 (null) |
| v1_original + v1 early H1_vs_H2 | p≈0.96, r≈0.01 (null) |

Policy: null requires p > 0.05 and rank-biserial r < 0.25.

## Seeds / env / platform

- Seeds: `hash((profile, mode, hyp, run, "wsA")) % 2**31` (same pattern as `workstream_a_runner.py`)
- n_runs (gate): **20** (paper workstream: **50**)
- Days: 40; early metric: sum of launches on days 0–9
- Stdlib only (`c2_core.run_single`)

## Not checked here

- Full Workstream A grid (4 profiles × 3 modes × 50 seeds)
- Published **107/108** null-count across all tests
- Phase 2 discrimination suite
- Figure regeneration / sensitivity CSV bit-identity
- Statistical tests on emergent-ratio as headline

## Evidence

- `results/claim_verify_meta.json`
- `results/claim_verify_out.txt`
- `results/milcom_claim_verify.json`
- `claim-manifest.json`

## Residual risk

Thin n_runs can fluctuate p-values; bands are deliberately loose on effect size. A green gate does **not** re-prove the full v4 grid — re-run `simulation/workstream_a_runner.py` for publication artifacts.
