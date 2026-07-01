"""
c2_core.py — Canonical IRGC C2 Degradation Model
=================================================
Extracted from sensitivity_analysis.py (v1, March 2026 paper) and refactored
for v3 paper extensions.

This module is the single source of truth for the agent-based model.
sensitivity_analysis.py imports from here; the older c2_degradation_sim.py
is a vestigial v0 prototype and is NOT used by this module.

v3 extension hooks (all default to v1 behavior when unspecified):
  - attrition_profile:  selects a launcher kill curve. Default "v1_original"
                        reproduces the March-23 paper's 50%-by-d3, 75%-by-d7,
                        plateau curve. New profiles for the v3 paper land here.
  - rationing_mode:     controls the magazine-discipline firing rule.
                        "v1" reproduces v1's hardcoded day-block rationing.
                        Workstream A will add "off", "individual", "coordinated".
  - lam:                C2-mediated survival advantage (Workstream B).
                        0.0 reproduces v1's exogenous attrition.

v1 reference: Daniyel Yaacov Bilar, "Launcher Attrition Dominates Command
Architecture," Zenodo 10.5281/zenodo.19547033 (v2, April 2026).
"""

import random
import math
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional

# ── Data Structures ────────────────────────────────────────────────

@dataclass
class Target:
    id: str
    value: float
    active_since: int    # day the target became relevant (0 = pre-war)
    mobile: bool = False

@dataclass
class Cell:
    id: str
    region: str
    pre_auth_targets: list
    pre_auth_expiry: int
    missiles: int = 20
    initial_missiles: int = 20      # v3 hook: needed for magazine_factor
    alive: bool = True
    connected_to_hq: bool = True
    total_launches: int = 0
    suppressed: bool = False        # crew "shoot-and-scoot" reluctance flag

# ── Network: regions and cell counts ───────────────────────────────

REGIONS = ["west_iran", "east_azerbaijan", "central_iran", "south_coast", "northeast"]
# Pre-war ~420 launchers; 120 cells × ~3.5 TELs avg
REGION_CELL_COUNTS = [30, 25, 28, 20, 17]  # 120 cells total

# ── Phase II tempo constants (residual low-attrition regime) ────────
# Standing cadence is deliberately low so standing fire does not swamp the
# provocation-response signal. A connected adaptive cell inside a provocation
# window fires at P2_RESPONSE. Suppression scales fire prob by the same
# 0.15/0.45 ratio the acute model uses.
P2_STANDING = 0.03
# (P2_RESPONSE removed: tempo is exogenous and flat across hypotheses.)
P2_SUPPRESS_FACTOR = 0.15 / 0.45
# Probability an adaptive, connected cell actually retaliates against the
# current provoker in an open window (vs firing at standing targets). Adaptive
# does not mean always-retaliate; this keeps H1 off a degenerate perfect score
# and produces realistic per-run variance. H3 adaptive cells retaliate at
# P2_RETAL_Q * 0.65 (the v4 mixed-adaptation fraction).
P2_RETAL_Q = 0.65

# ── Target set ─────────────────────────────────────────────────────

def build_targets():
    targets = {}
    pre_war = [
        ("T_nevatim", 0.9, 0), ("T_ramon", 0.8, 0), ("T_dimona", 0.95, 0),
        ("T_tel_nof", 0.7, 0), ("T_haifa", 0.5, 0), ("T_dhahran", 0.7, 0),
        ("T_aludeid", 0.85, 0), ("T_arifjan", 0.7, 0), ("T_muharraq", 0.5, 0),
        ("T_juffair", 0.6, 0), ("T_incirlik", 0.6, 0), ("T_diego", 0.6, 0),
        ("T_shaybah", 0.5, 0), ("T_uae_bases", 0.65, 0),
    ]
    for tid, val, day in pre_war:
        targets[tid] = Target(tid, val, day)

    emergent = [
        ("T_fob_alpha", 0.6, 5), ("T_fob_bravo", 0.5, 8),
        ("T_logistics_hub", 0.7, 12, True), ("T_carrier_group", 0.9, 3, True),
        ("T_awacs_orbit", 0.8, 1, True), ("T_b1_corridor", 0.75, 4),
        ("T_tanker_orbit", 0.6, 6, True), ("T_cyp_akrotiri", 0.4, 2),
    ]
    for e in emergent:
        tid, val, day = e[0], e[1], e[2]
        mob = e[3] if len(e) > 3 else False
        targets[tid] = Target(tid, val, day, mob)
    return targets

def build_cells(rng, pre_auth_expiry_range):
    """Build cells with configurable pre-auth expiry window."""
    cells = {}
    targets = build_targets()
    pre_war_tids = [t for t, v in targets.items() if v.active_since == 0]

    for ri, region in enumerate(REGIONS):
        for ci in range(REGION_CELL_COUNTS[ri]):
            cid = f"cell_{region}_{ci}"
            pa_count = rng.randint(3, 6)
            pa_targets = rng.sample(pre_war_tids, min(pa_count, len(pre_war_tids)))

            lo, hi = pre_auth_expiry_range
            pa_expiry = rng.randint(lo, hi)

            missiles = rng.randint(12, 25)

            cells[cid] = Cell(
                id=cid, region=region,
                pre_auth_targets=pa_targets,
                pre_auth_expiry=pa_expiry,
                missiles=missiles,
                initial_missiles=missiles,   # v3: lock initial for magazine_factor
            )
    return cells, targets

# ── Launcher attrition profiles ────────────────────────────────────

def compute_launcher_attrition(day, profile="v1_original"):
    """
    Returns the fraction of cells that should still be alive on `day`.
    `apply_attrition_to_cells` uses this to drive probabilistic kills.

    Profiles:
      "v1_original": March-23 paper calibration. 50% by d3, 75% by d7,
                     ~20% plateau, slow grind to ~5%.
      Workstream A will add v3_realistic, v3_front_loaded, etc.
    """
    if profile == "v1_original":
        if day <= 3:
            return 1.0 - (0.50 * day / 3)
        elif day <= 7:
            return 0.50 - (0.25 * (day - 3) / 4)
        elif day <= 12:
            return 0.25 - (0.01 * (day - 7))
        else:
            return max(0.05, 0.20 - (0.003 * (day - 12)))

    if profile == "v3_realistic":
        # Post-conflict IC reporting: ~50% survival at d39 (ceasefire).
        # Shape: slower early kill than v1, smooth decline, plateau ~45-50%.
        if day <= 7:
            # ~20% destroyed by d7 (vs v1's 75%)
            return 1.0 - (0.20 * day / 7)
        elif day <= 20:
            # linear decline to ~55% by d20
            return 0.80 - (0.25 * (day - 7) / 13)
        elif day <= 39:
            # slow grind to ~45% at ceasefire
            return 0.55 - (0.10 * (day - 20) / 19)
        else:
            return max(0.40, 0.45 - (0.002 * (day - 39)))

    if profile == "v3_front_loaded":
        # Fast early kill (closer to v1 in week one) but plateau higher.
        # Lands at ~45% at d39.
        if day <= 3:
            return 1.0 - (0.30 * day / 3)
        elif day <= 10:
            return 0.70 - (0.20 * (day - 3) / 7)
        elif day <= 25:
            return 0.50 - (0.05 * (day - 10) / 15)
        elif day <= 39:
            return 0.45 - (0.03 * (day - 25) / 14)
        else:
            return max(0.38, 0.42 - (0.002 * (day - 39)))

    if profile == "v3_plateau_high":
        # Steeper initial drop, very early plateau. Lands at ~50%.
        if day <= 5:
            return 1.0 - (0.40 * day / 5)
        elif day <= 12:
            return 0.60 - (0.08 * (day - 5) / 7)
        else:
            return max(0.48, 0.52 - (0.001 * (day - 12)))

    if profile == "phase2_residual":
        # Phase II low-attrition residual-force regime. The acute-attrition
        # phase is already over: the force starts at the ~42% ceasefire
        # survival estimate and drifts down slowly (near-flat), never
        # swamping the target-selection signal. Floor at 36%.
        return max(0.36, 0.42 - 0.0007 * day)

    raise ValueError(f"Unknown attrition profile: {profile}")

def apply_attrition_to_cells(cells, day, rng,
                              profile="v1_original",
                              lam=0.0):
    """
    Kill cells probabilistically to match the target survival fraction.
    
    v3 hook: `lam` is the C2-mediated survival advantage. lam=0 reproduces
    v1's purely exogenous attrition. Workstream B will populate this.
    Currently a no-op for lam>0; the parameter is plumbed through but the
    dampening logic is deferred to Workstream B to keep this refactor
    behavior-preserving.
    """
    alive = [c for c in cells.values() if c.alive]
    if not alive:
        return

    target_survival = compute_launcher_attrition(day, profile=profile)
    total_cells = len(cells)
    target_alive = max(1, int(total_cells * target_survival))
    current_alive = len(alive)

    to_kill = max(0, current_alive - target_alive)
    if to_kill > 0:
        victims = rng.sample(alive, min(to_kill, len(alive)))
        for v in victims:
            v.alive = False

    # Suppression: surviving cells become cautious as the campaign drags
    for c in cells.values():
        if c.alive and day >= 3:
            c.suppressed = rng.random() < min(0.4, 0.05 * day)

# ── C2 connectivity model ─────────────────────────────────────────

def compute_connectivity(day, region, rng, residual_p=None):
    """
    Per-region probability that a cell still has C2 contact today.
    Supreme HQ destroyed day 0; sector commands hit days 3-7;
    provincial nodes degraded progressively.

    Phase II hook: `residual_p` overrides the campaign decay with a flat
    reconstituted-C2 connection probability, uniform across regions. This
    models a residual force that has re-established horizontal C2 past the
    acute phase. It is the paper's load-bearing assumption and is SWEPT
    (not fixed) by phase2_runner. residual_p=None reproduces v1 behavior.
    """
    if residual_p is not None:
        return rng.random() < residual_p

    base_p = {
        "west_iran": 0.9,
        "east_azerbaijan": 0.85,
        "central_iran": 0.8,
        "south_coast": 0.75,
        "northeast": 0.7,
    }
    p = base_p.get(region, 0.8)

    if day == 0:
        p *= 0.3
    elif day <= 3:
        p *= 0.4
    elif day <= 7:
        p *= 0.25
    elif day <= 14:
        p *= 0.15
    else:
        p *= max(0.05, 0.15 - 0.005 * (day - 14))

    return rng.random() < p

# ── Magazine discipline (v3 Workstream A) ──────────────────────────

def magazine_fire_probability(cell, force_state, rationing_mode, base=0.45):
    """
    Compute the per-day firing probability under v3 magazine discipline.

    Modes:
      "off"          - no rationing beyond the base rate (ceiling test)
      "individual"   - each cell rations based only on its own magazine
      "coordinated"  - cells ration using both own magazine AND force-wide
                       scarcity signal (the H1-like coordination mechanism)

    The v1 mode is handled separately in cell_decide and does not go through
    this function.
    """
    if rationing_mode == "off":
        return base

    # Magazine factor: sigmoid centered at 30% remaining.
    # At 100% full: factor ~1.0. At 30% remaining: 0.5. At 10% remaining: ~0.1.
    mag_frac = cell.missiles / max(cell.initial_missiles, 1)
    mag_factor = 1.0 / (1.0 + math.exp(-12 * (mag_frac - 0.30)))

    if rationing_mode == "individual":
        return base * mag_factor

    if rationing_mode == "coordinated":
        # Force-wide scarcity signal: as the force depletes, surviving cells
        # husband their magazines more aggressively. Floors at 0.3 so a
        # fully-depleted force still fires occasionally (matches the 20-45
        # BM/day late-phase observed in VI-D).
        force_frac = force_state["alive_cells"] / max(force_state["initial_cells"], 1)
        scarcity_factor = 0.3 + 0.7 * force_frac
        return base * mag_factor * scarcity_factor

    raise ValueError(f"Unknown rationing_mode: {rationing_mode}")

# ── Cell launch decision ───────────────────────────────────────────

def cell_decide(cell, day, targets, hypothesis, connected, rng,
                rationing_mode="v1",
                force_state=None,
                tempo_mode="v1",
                active_provocations=None):
    """
    Returns target_id or None.

    v3 hook: rationing_mode + force_state are the magazine-discipline plumbing
    for Workstream A. "v1" reproduces the original day-block rationing
    (no magazine sigmoid, no force-wide signal). Workstream A will add
    "off", "individual", "coordinated".

    Phase II hook: tempo_mode="phase2" replaces the acute-campaign fire gate
    with a low standing cadence. When an adaptive cell (H1/H3) is connected and
    a provocation window is open, it retaliates directly against a current provoker
    with probability P2_RETAL_Q
    (`active_provocations` is the list of open provoker ids); otherwise it falls
    through to the UNCHANGED hypothesis dispatch. Fire rate is flat and exogenous,
    so only targeting differs by hypothesis. tempo_mode="v1" reproduces v1 exactly.
    """
    if not cell.alive or cell.missiles <= 0:
        return None

    if tempo_mode == "phase2":
        # Tempo is held EXOGENOUS and equal across hypotheses: every cell fires
        # at the same low standing rate regardless of C2 state. This mirrors the
        # v4 modeling philosophy (C2 changes WHAT is hit, not HOW MUCH), so
        # launch volume cannot by construction discriminate the hypotheses; only
        # target selection can. What connectivity gates is RETARGETING, not rate.
        p_fire = P2_STANDING
        if cell.suppressed:
            p_fire *= P2_SUPPRESS_FACTOR
        if rng.random() > p_fire:
            return None
        if active_provocations and connected and hypothesis in ("H1", "H3"):
            q = P2_RETAL_Q if hypothesis == "H1" else P2_RETAL_Q * 0.65
            if rng.random() < q:
                # deliberate retaliation against a currently-open provoker
                return rng.choice(active_provocations)
        # non-retaliating fire: same selection logic, but guarantee a launch so
        # volume stays exogenous and equal across hypotheses.
        tid = _select_target(cell, day, targets, hypothesis, connected, rng)
        if tid is None:
            tid = _phase2_fallback(cell, targets, rng)
        return tid
    else:
        base_fire_prob = 0.45 if not cell.suppressed else 0.15

        if rationing_mode == "v1":
            if rng.random() > base_fire_prob:
                return None
            # Original day-block rationing
            if day < 3:
                pass
            elif day < 10:
                if rng.random() > 0.6:
                    return None
            else:
                if rng.random() > 0.4:
                    return None
        else:
            # v3 magazine discipline: single probabilistic gate, no day-blocks.
            # Suppression still modulates the base rate.
            p_fire = magazine_fire_probability(
                cell, force_state, rationing_mode,
                base=(0.45 if not cell.suppressed else 0.15),
            )
            if rng.random() > p_fire:
                return None

    # Hypothesis dispatch
    return _select_target(cell, day, targets, hypothesis, connected, rng)


def _select_target(cell, day, targets, hypothesis, connected, rng):
    """The v1/v3 target-selection dispatch, unchanged. Extracted so the Phase II
    path can reuse it verbatim and then apply a guaranteed-launch fallback."""
    if hypothesis == "H1":
        if connected:
            available = [t for t in targets.values() if t.active_since <= day]
            available.sort(key=lambda t: t.value + rng.gauss(0, 0.15), reverse=True)
            return available[0].id if available else None
        else:
            return _pick_pre_auth(cell, day, rng)
    elif hypothesis == "H2":
        return _pick_pre_auth(cell, day, rng)
    elif hypothesis == "H3":
        if connected and rng.random() < 0.65:
            available = [t for t in targets.values() if t.active_since <= day]
            available.sort(key=lambda t: t.value + rng.gauss(0, 0.15), reverse=True)
            return available[0].id if available else None
        return _pick_pre_auth(cell, day, rng)
    return None


def _phase2_fallback(cell, targets, rng):
    """Guarantee a launch once the flat fire gate has fired, so launch VOLUME is
    exogenous and equal across hypotheses (only targeting differs). A residual
    pre-programmed force keeps firing its list rather than going silent."""
    if cell.pre_auth_targets:
        return rng.choice(cell.pre_auth_targets)
    prewar = [t.id for t in targets.values() if t.active_since == 0]
    return rng.choice(prewar) if prewar else None

def _pick_pre_auth(cell, day, rng):
    if day > cell.pre_auth_expiry:
        days_past = day - cell.pre_auth_expiry
        desperation_p = max(0.05, 0.35 - 0.02 * days_past)
        if rng.random() > desperation_p:
            return None
    if not cell.pre_auth_targets:
        return None
    return rng.choice(cell.pre_auth_targets)

# ── Metrics ────────────────────────────────────────────────────────

def target_entropy(launches):
    if not launches:
        return 0.0
    counts = defaultdict(int)
    for t in launches:
        counts[t] += 1
    n = len(launches)
    return -sum((c/n) * math.log2(c/n) for c in counts.values())

def emergent_ratio(launches, targets):
    if not launches:
        return 0.0
    return sum(1 for t in launches
               if targets.get(t) and targets[t].active_since > 0) / len(launches)

# ── Phase II: provocations and attribution correlation ─────────────

def build_provocations(rng, n_prov, window_days, sim_days, prov_value,
                       pre_war, p_standing=0.5):
    """
    Build a provocation schedule for one run. Each provocation is a coalition
    action with a source asset S that Iran may retaliate against within
    [t_p, t_p + W].

    Two kinds, mixed by p_standing (this is what makes the metric informative
    rather than circular):
      "novel"    : a fresh post-initiation asset (new deployment). Not in any
                   pre-war package, so H2 CANNOT strike it. Spawns an emergent
                   Target (active_since = t_p).
      "standing" : the provoker is an existing pre-war target (e.g. a base that
                   was always on the list and just conducted a strike). H2 can
                   hit it by coincidence through its normal pre-auth firing;
                   H1 hits it more via adaptive retargeting. This is the
                   attribution-laundering / coincidence floor of codebook §8.

    `pre_war` is a list of (tid, value) for the pre-war target set. Provocation
    salience (prov_value) is set above the max pre-war value so an adaptive,
    connected cell prioritizes the provoker while its window is open.

    Returns (provocations, prov_targets):
      provocations: list of {"t_p","S","W","kind","base_value"}
      prov_targets: {S: Target}   (novel provokers only)
    Call with an rng seeded independently of hypothesis so the schedule is
    shared across H1/H2/H3 for a matched comparison.
    """
    provs, ptargets = [], {}
    lo = 5
    hi = max(lo + 1, sim_days - window_days - 2)
    pre_war_tids = [tid for tid, _ in pre_war]
    for i in range(n_prov):
        frac = (i + 0.5) / n_prov
        base = lo + frac * (hi - lo)
        t_p = int(round(base + rng.uniform(-2.0, 2.0)))
        t_p = max(1, min(sim_days - 1, t_p))
        if rng.random() < p_standing:
            tid = rng.choice(pre_war_tids)
            base_value = dict(pre_war)[tid]
            provs.append({"t_p": t_p, "S": tid, "W": window_days,
                          "kind": "standing", "base_value": base_value})
        else:
            S = f"T_prov_{i}"
            provs.append({"t_p": t_p, "S": S, "W": window_days,
                          "kind": "novel", "base_value": 0.0})
            ptargets[S] = Target(S, prov_value, t_p, mobile=True)
    return provs, ptargets


def attribution_correlation(launch_log, provocations, window_days):
    """
    In-sim analog of the empirical attribution-correlation construct.

    A launch is attribution-correlated if it strikes the specific provocation
    source S within [t_p, t_p + W]. Returns two rates (both reported, primary
    chosen later) plus the latency list:
      d_all : correlated / all residual-phase launches   (matches empirical 4.5/7)
      d_win : correlated / launches fired while any window is open (response rate)
      latencies : (day - t_p) for each correlated launch  (sim analog of ~24h median)
    """
    total = len(launch_log)
    correlated = 0
    windowed_total = 0
    latencies = []
    for (day, tid) in launch_log:
        in_window = False
        matched = False
        for pr in provocations:
            if pr["t_p"] <= day <= pr["t_p"] + window_days:
                in_window = True
                if tid == pr["S"]:
                    matched = True
                    latencies.append(day - pr["t_p"])
        if in_window:
            windowed_total += 1
        if matched:
            correlated += 1
    d_all = correlated / total if total else 0.0
    d_win = correlated / windowed_total if windowed_total else 0.0
    return d_all, d_win, latencies


def overall_emergent_ratio(launch_log, emergent_tids):
    """Fraction of all launches that hit any emergent target (active_since>0).
    This is the full v4 emergent-ratio signal; attribution correlation is its
    observable subset. The ratio of the two effect sizes is the paper's gap."""
    if not launch_log:
        return 0.0
    return sum(1 for (_, tid) in launch_log if tid in emergent_tids) / len(launch_log)


# ── Single-run driver ──────────────────────────────────────────────

def run_single(hypothesis, pre_auth_range, seed=42, days=75,
               attrition_profile="v1_original",
               rationing_mode="v1",
               lam=0.0,
               tempo_mode="v1",
               residual_p=None,
               provocations=None,
               prov_targets=None,
               prov_value=1.0,
               return_log=False):
    """
    One Monte Carlo run.

    v1 call sites that pass only (hypothesis, pre_auth_range, seed, days) get
    bit-for-bit identical results to the original sensitivity_analysis.py
    because all v3 hooks default to "v1" / "v1_original" / 0.0.

    Phase II params (all default to no-op so v1/v3 parity is preserved):
      tempo_mode    "phase2" enables provocation-gated low tempo.
      residual_p    flat reconstituted connectivity (swept); None = v1 decay.
      provocations  schedule from build_provocations(); shared across hypotheses.
      prov_targets  the provocation Target objects, merged into the target set.
      prov_value    salience premium for an open provocation window.
      return_log    if True, also return (launch_log, provocations).
    """
    rng = random.Random(seed)
    cells, targets = build_cells(rng, pre_auth_range)
    if prov_targets:
        targets.update(prov_targets)
    daily = []
    launch_log = []

    for day in range(days):
        apply_attrition_to_cells(cells, day, rng,
                                  profile=attrition_profile,
                                  lam=lam)

        # v3 hook: force_state for coordinated rationing (Workstream A)
        alive_now = sum(1 for c in cells.values() if c.alive)
        force_state = {
            "alive_cells": alive_now,
            "initial_cells": len(cells),
        }

        # Phase II: list provoker ids whose window is open today.
        active_provocations = None
        if provocations:
            open_ids = [pr["S"] for pr in provocations
                        if pr["t_p"] <= day <= pr["t_p"] + pr["W"]]
            active_provocations = open_ids if open_ids else None

        all_launches = []
        region_counts = defaultdict(int)

        for cid, cell in cells.items():
            connected = compute_connectivity(day, cell.region, rng,
                                             residual_p=residual_p)
            cell.connected_to_hq = connected
            tid = cell_decide(cell, day, targets, hypothesis, connected, rng,
                              rationing_mode=rationing_mode,
                              force_state=force_state,
                              tempo_mode=tempo_mode,
                              active_provocations=active_provocations)
            if tid:
                cell.missiles -= 1
                cell.total_launches += 1
                all_launches.append(tid)
                launch_log.append((day, tid))
                region_counts[cell.region] += 1

        alive_n = sum(1 for c in cells.values() if c.alive)
        conn_n = sum(1 for c in cells.values() if c.alive and c.connected_to_hq)
        missiles_left = sum(c.missiles for c in cells.values() if c.alive)

        daily.append({
            "day": day,
            "launches": len(all_launches),
            "alive_cells": alive_n,
            "connected_cells": conn_n,
            "missiles_remaining": missiles_left,
            "entropy": round(target_entropy(all_launches), 4),
            "emergent_ratio": round(emergent_ratio(all_launches, targets), 4),
        })
    if return_log:
        return daily, launch_log, provocations
    return daily
