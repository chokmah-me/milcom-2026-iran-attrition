# Phase II Leg 1 Build Notes — Deviations from Pre-Registration
Version 0.1. Companion to `leg1_design_v0_1.md` (pre-registered) and
`codebook_v0_1.md` (Leg 2). The design spec is left unchanged as the
pre-registration record. This file documents where the build departed from it
and why. All three departures were forced by results, not preference, and each
is stated in the paper as a deviation.

## Summary

The runner and extended `c2_core.py` build cleanly (30s, 200 seeds, stdlib
only) and pass a bit-for-bit v1/v3 parity test (0 mismatches across 192 configs:
3 hypotheses x 4 seeds x 4 attrition profiles x 4 rationing modes). The Phase II
extension is purely additive.

Headline (72h window): on identical runs, launch-rate discrimination H1 vs H2 is
null (r ~ 0, p > 0.05 at every connectivity level) while attribution-correlation
discrimination is sharp (r = 0.93 to 1.00, p < 0.001). Same simulation, two
metrics: launch volume is blind to C2 state, target selection is not.

## Deviation 1 — Attribution correlation is not a strict subset of the emergent ratio

**Pre-registered (design §2):** attribution correlation was framed as a strict
subset of the v4 emergent target ratio, with the headline being the "gap"
r(attribution) / r(emergent).

**What happened:** modeling every provoker as a novel post-initiation asset made
H2 structurally incapable of ever hitting a provoker. H2 attribution correlation
was exactly 0 for every seed, H1 was reliably positive, so rank-biserial pegged
at exactly 1.000 across the whole grid. That is circular: the model was built so
H2 cannot produce the signal, then "found" the signal separates H1 from H2
perfectly. No gradient, nothing learned.

**Fix:** provokers are a mix (50/50) of novel assets and standing pre-war
targets. A standing provoker is an existing target (e.g. a base that was always
on the list and just conducted a strike), which H2 can hit by coincidence
through normal pre-authorized firing. This gives H2 a real, small coincidence
floor (~0.02) and makes the metric informative. It also matches the codebook's
own §8 position that attribution correlation is a distinct, overlapping
construct that captures reactive retargeting, not a subset of emergent
targeting. The "gap" ratio is dropped as not meaningful. The emergent ratio is
still reported per run as an unobservable-ceiling comparator, but not as a
denominator.

## Deviation 2 — The result is the launch-rate-vs-attribution contrast, not attribution alone

**Pre-registered (design §0):** measure whether the observable proxy separates
H1 from H2 in the residual regime.

**What happened:** v4 already established that a discriminator (the emergent
ratio) exists in the residual regime. Reporting only that attribution
correlation separates H1 from H2 risks re-deriving v4's Table V. The
non-circular contribution is showing, on the same runs, that launch rate stays
null while the observable proxy separates.

**Fix:** launch-rate discrimination H1 vs H2 was added to the runner and is
computed on the identical runs that produce the attribution result. It comes out
null (r ~ 0, p > 0.05) at every connectivity level, reproducing the v4
launch-rate finding inside the Phase II regime. The paper's core claim is the
LR-vs-attribution contrast on identical runs, which also defuses the "the model
separates everything" objection: the model demonstrably produces a null on
launch rate.

## Deviation 3 — Tempo held flat and exogenous across hypotheses

**Pre-registered (design §4):** a provocation-gated tempo, where an adaptive
cell fires at an elevated rate when it sees a provocation.

**What happened:** an elevated response rate for H1/H3 made adaptive cells fire
more than pre-programmed cells, so launch volume itself discriminated the
hypotheses (r(LR) rose to 0.4 to 0.9). That contradicts the v4 thesis that C2
state changes what is hit, not how much, and would have made launch rate a valid
discriminator by construction.

**Fix:** every cell fires at the same low standing rate regardless of C2 state.
Connectivity gates only retargeting (whether an adaptive, connected cell
redirects its fire to the current provoker), never the fire rate. To keep volume
equal, a gated fire always yields a launch: a residual pre-programmed force keeps
firing its list rather than going silent on pre-auth expiry (the acute-phase
silence mechanic is suppressed in the phase2 tempo path only). This holds launch
volume exogenous and equal across hypotheses, mirroring v4's modeling
philosophy, so launch rate is null by design and only targeting carries C2
information.

## Two caveats to carry into the writeup

1. **Near-complete separation at high connectivity.** r(D_all) reaches 1.000 at
   c_res >= 0.50 because H1 and H2 are idealized behavioral archetypes. The real
   force is a mixture, which is what H3 models (graded, r and mean between H1 and
   H2) and what the empirical Stream B ~0.64 reflects. The paper should not read
   r = 1.0 as a claim that real-world discrimination is perfect.

2. **D_win, not D_all, is the comparator to Stream B.** H1 D_all sits at 0.09 to
   0.22 because its denominator is all 60 days of standing fire, most of it
   outside any provocation window. The empirical 4.5/7 counted only construct
   events, which are response-window events. D_win (correlated / in-window
   strikes) is the like-for-like comparator. Both are reported per the locked
   decision; D_win is the honest match to the empirical level, D_all is the
   conservative whole-campaign rate.

## Parameters as built (for the methods section)

- Attrition profile `phase2_residual`: ~42% survival at day 0, near-flat drift to
  ~38% by day 60 (floor 36%). Past the acute phase.
- 120 cells, ~50 surviving. 60-day window. Pre-auth expiry (25, 40).
- Flat standing fire rate P2_STANDING = 0.03; suppression factor 0.333.
- Retaliation probability P2_RETAL_Q = 0.65 (H1); H3 uses 0.65 x 0.65.
- 8 provocations per run, 50% standing / 50% novel. Salience premium 1.2.
- Connectivity c_res swept over {0.20, 0.35, 0.50, 0.65}.
- Window W: 3 days primary, 2 days robustness.
- 200 seeds. Provocation schedule shared across hypotheses per (W, seed).
- Stats: Mann-Whitney U, tie-corrected normal approximation, rank-biserial r
  primary, Cohen's d reported. Stdlib only.
