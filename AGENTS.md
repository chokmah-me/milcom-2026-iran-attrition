# AGENTS.md — milcom-2026-iran-attrition

Companion sim and data for the v4 launcher-attrition paper and Phase II residual-force observability paper. Stdlib only. Thin MC gates are not the full publication grids.

## Commands

```powershell
python verify_milcom_claims.py
python verify_phase2_claims.py
```

Full v4 Workstream A grid (publication-scale, slower):

```powershell
cd simulation
python workstream_a_runner.py
```

## Work rules

- Exit 0 on the verify scripts means the load-bearing thin MC still holds.
- Do not change locked data tables, published figures, or minted PDFs without the user's explicit word.
- Phase II headline is the observable discrimination gap; do not treat sim numbers as field measurements.

## Pointers

- `README.md` — papers, DOIs, reproduce
- `claim-manifest.json` — both gates
- `ZENODO.md` — concept vs version
- `simulation/` — runners
