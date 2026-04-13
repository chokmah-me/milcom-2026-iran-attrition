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

def compute_connectivity(day, region, rng):
    """
    Per-region probability that a cell still has C2 contact today.
    Supreme HQ destroyed day 0; sector commands hit days 3-7;
    provincial nodes degraded progressively.
    """
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
                force_state=None):
    """
    Returns target_id or None.

    v3 hook: rationing_mode + force_state are the magazine-discipline plumbing
    for Workstream A. "v1" reproduces the original day-block rationing
    (no magazine sigmoid, no force-wide signal). Workstream A will add
    "off", "individual", "coordinated".
    """
    if not cell.alive or cell.missiles <= 0:
        return None

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

# ── Single-run driver ──────────────────────────────────────────────

def run_single(hypothesis, pre_auth_range, seed=42, days=75,
               attrition_profile="v1_original",
               rationing_mode="v1",
               lam=0.0):
    """
    One Monte Carlo run.

    v1 call sites that pass only (hypothesis, pre_auth_range, seed, days) get
    bit-for-bit identical results to the original sensitivity_analysis.py
    because all v3 hooks default to "v1" / "v1_original" / 0.0.
    """
    rng = random.Random(seed)
    cells, targets = build_cells(rng, pre_auth_range)
    daily = []

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

        all_launches = []
        region_counts = defaultdict(int)

        for cid, cell in cells.items():
            connected = compute_connectivity(day, cell.region, rng)
            cell.connected_to_hq = connected
            tid = cell_decide(cell, day, targets, hypothesis, connected, rng,
                              rationing_mode=rationing_mode,
                              force_state=force_state)
            if tid:
                cell.missiles -= 1
                cell.total_launches += 1
                all_launches.append(tid)
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
    return daily
