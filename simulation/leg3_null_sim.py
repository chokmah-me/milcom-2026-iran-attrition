"""
leg3_null_sim.py -- Simulated null for the Leg 3 attribution-correlation
construct under dense provocation. Stdlib only.

Question: what does a PURELY PRE-PROGRAMMED (H2) force score on the
codebook's attribution_correlated construct, by coincidence, when
coalition provocations occur daily and IRGC framing is universal?

Model of the CODING SCHEME, not the ABM:
- H2 fires at a fixed standing target list (n_targets US-linked sites),
  choosing uniformly at random each strike day (matches _pick_pre_auth).
- Coalition provocations occur every day (dense regime). Each provocation
  is attributable to a specific basing asset with prob p_attr (carrier /
  standoff strikes are unattributable); if attributable, the origin is
  drawn from the same n_targets sites (the bases doing the striking are
  the bases being struck -- true in the July regime).
- Framing: IRGC frames the strike as retaliation with prob p_frame.
- Coding per codebook sec.3:
    1   if framing AND an attributable provocation in prior 72h whose
        origin == the struck target
    0.5 if framing XOR clean physical match (incl. unattributable antecedent)
    0   if neither
"""
import random, statistics

def run(n_events=1000, n_targets=8, p_attr=0.5, p_frame=1.0, window=3,
        provocations_per_day=1.0, seed=1):
    rng = random.Random(seed)
    scores = []
    for _ in range(n_events):
        struck = rng.randrange(n_targets)
        # provocations in prior 72h
        n_prov = 0
        match = False
        for d in range(window):
            k = int(provocations_per_day) + (1 if rng.random() < provocations_per_day % 1 else 0)
            for _ in range(k):
                n_prov += 1
                if rng.random() < p_attr and rng.randrange(n_targets) == struck:
                    match = True
        framed = rng.random() < p_frame
        if framed and match:
            scores.append(1.0)
        elif framed or match:
            scores.append(0.5)
        else:
            scores.append(0.0)
    return statistics.mean(scores)

print(f"{'p_frame':>8} {'p_attr':>7} {'prov/day':>9} {'null rate':>10}")
for p_frame in (1.0, 0.8, 0.5):
    for p_attr in (0.7, 0.5, 0.3):
        for ppd in (1.0, 2.0):
            r = run(p_frame=p_frame, p_attr=p_attr, provocations_per_day=ppd)
            print(f"{p_frame:>8} {p_attr:>7} {ppd:>9} {r:>10.3f}")

# Leg 2 sparse-regime reference: provocations rare (~1 per 2 weeks)
print("\nSparse regime (Leg 2 conditions, ~1 provocation/14d, framing 0.8):")
r = run(p_frame=0.8, p_attr=0.7, provocations_per_day=1/14)
print(f"  null rate = {r:.3f}")
