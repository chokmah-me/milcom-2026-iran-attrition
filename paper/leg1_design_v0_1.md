# Phase II Leg 1 Design — Simulation of Attribution Correlation Under Low Attrition
Locked before coding. Version 0.1. Companion to `codebook_v0_1.md` (Leg 2, empirical).

## 0. What Leg 1 tests, and why it is not a v4 rerun

v4 already showed the emergent target ratio discriminates H1 from H2 in the residual-force
regime (Table V: r = 0.706 under `v3_realistic`, stronger than v1). So "a C2 discriminator
becomes visible at low attrition" is, for the emergent ratio, already established. Leg 1 does
not re-derive that.

The emergent ratio is unobservable (a collection requirement). Attribution correlation is its
observable proxy: did Iran strike the specific asset that just provoked it, within a window.
The sim question is the gap:

> How much discriminating power survives the move from the full emergent target ratio
> (unobservable) to the source-specific, windowed attribution-correlation proxy (observable)?

That gap is the contribution. The empirical Stream B ≈ 0.64 is interpretable as H1-consistent
**only if** the sim shows the proxy keeps real power. If the proxy collapses toward the
launch-rate null, the 0.64 cannot carry H1, and per Leg 2 codebook §6 that is reported as
evidence against H1-observability, not explained away.

## 1. Provocation mechanic

A provocation is a discrete timed event with a source identity: `P = (t_p, S, value, W)`.
It spawns a fresh emergent target `S` (`active_since = t_p`, elevated `value`) that reuses the
existing target machinery in `c2_core.py`. After the window `W`, `S`'s value decays back down
so late strikes on it stop counting.

Response is handled by the existing `cell_decide` dispatch, unchanged:
- **H1** (connected): value-sorts available targets; `S` is high-value and now available, so it
  tends to fire at `S` soon after `t_p`. High correlation, short latency.
- **H2**: `_pick_pre_auth` draws only from pre-war packages. `S` is post-initiation, never in a
  pre-war list, so H2 structurally cannot hit it. Correlation ≈ 0.
- **H3**: connected cells adapt with p = 0.65; lands between, graded by connectivity.

**Caveat to state in paper:** H2 = 0 by construction is the same artifact v4 flagged for the
emergent ratio. It is arguably correct here (a pre-programmed force cannot retaliate against a
novel provoker, which is exactly why Stream A ≈ 0.0), but it inflates r and must be labeled.

## 2. In-sim metric, and mapping to existing machinery

Attribution correlation is a strict subset of the emergent ratio:
`emergent_ratio()` counts `active_since > 0`; attribution correlation additionally requires
`target_id == S` and `0 <= day - t_p <= W`. Therefore r(attribution) ≤ r(emergent) always, and
the gap is the reported quantity.

**Denominator: report both (decision locked).**
- `D_all`  = correlated / all residual-phase strikes. Matches the empirical 4.5/7 construction.
- `D_win`  = correlated / strikes fired while a provocation window is active. Pure response
  rate, drops standing-fire dilution.
- Both computed per run, both fed to the stat harness. Primary chosen after inspecting
  stability across seeds.

**Latency** falls out for free: `day - t_p` per correlated strike gives the sim analog of the
empirical ~24h median (codebook §5). One mechanic, two metrics that both map back to Leg 2.

## 3. Regime parameters

| Parameter | Value | Note |
|---|---|---|
| Attrition profile | new `phase2_residual`: ~0.42 start, slow drift to ~0.38 over 60d | past the acute phase, near-flat; not the declining `v3_realistic` |
| Sim window | 60 days | residual/post-acute segment |
| Base fire tempo | throttled hard; standing cadence low, H1 response provocation-gated | the real new mechanic; standing fire must not swamp the signal |
| Provocations | 6–10 over the window, cadence roughly matching coalition actions | calibrated to regime realism, NOT to the empirical event count (that would be circular) |
| Window W | 3 days (72h) primary; 2 days (48h) robustness | mirrors codebook §3 |
| Connectivity c_res | **swept**: {0.20, 0.35, 0.50, 0.65} | decision locked; see §4 |
| Seeds | 50 to match v4; 200 for the headline to tighten CIs at low tempo | |
| Hypotheses | H1, H2, H3 | unchanged rulesets |

## 4. Two additive wrappers (rulesets otherwise unchanged)

Target-selection dispatch (H1 value-sort / H2 pre_auth / H3 mix) is reused verbatim. Two hooks
are added, both defaulting to v1 behavior so `run_single` parity is preserved:

1. **Residual connectivity.** `compute_connectivity` floors near 0.05 by late campaign; in a
   reconstituted-C2 regime that would collapse H1 into H2 and leave nothing to discriminate.
   Add a steady-state connectivity parameter `c_res` and **sweep it** rather than pick one
   value. Reporting r vs c_res shows exactly how much the H1/H2 separation depends on the
   reconstitution assumption, turning the load-bearing assumption into a labeled curve.
2. **Provocation-gated tempo.** Low standing cadence plus provocation-triggered response
   (§1, §3).

## 5. Statistical posture (carries v4 discipline)

- Mann-Whitney U; rank-biserial r primary effect size; Cohen's d in parens.
- Pairs: H1 vs H2 (primary), H1 vs H3, H2 vs H3.
- Proper N via seeds. This is where the inferential work lives; Leg 2 stays descriptive.
- Report `r(attribution)` alongside `r(emergent)` from the same runs so the gap is explicit.

## 6. Pre-registered read (lock before running)

- **Proxy retains power** if r(attribution, H1 vs H2) stays near r(emergent) (~0.7 band):
  the observable proxy works, empirical Stream B ≈ 0.64 is interpretable as H1-consistent.
- **Proxy collapses** if r(attribution) falls toward the launch-rate null (r < ~0.1): the
  observable proxy is uninformative; the empirical number cannot discriminate H1 from H2;
  report as a negative result against H1-observability. Do not widen W or cherry-pick c_res
  to rescue it.
- The reported "gap" is `r(attribution) / r(emergent)`, pre-committed as the headline number.

## 7. What Leg 1 is NOT doing

- Not touching the validated H1/H2/H3 target-selection logic.
- Not re-running the v4 magazine-discipline grid.
- Not claiming a discriminator "emerges" (v4 already has that). Only measuring proxy fidelity.
- Not calibrating provocation count to the empirical log (circular).

## 8. Build plan (next session)

- Extend `simulation/c2_core.py`: `phase2_residual` profile, `c_res` connectivity hook,
  provocation registry + spawn, provocation-gated tempo. All additive; v1 parity test must
  still pass bit-for-bit.
- New `simulation/phase2_runner.py` (mirrors `workstream_a_runner.py`): grid over
  {hypothesis × c_res × W} × seeds; compute `D_all`, `D_win`, latency, emergent ratio;
  write report + CSVs to `data_phase2/`.
