# Zenodo paper description — Phase II v0.2

**Published**

| Role | DOI / URL |
|------|-----------|
| Concept | https://doi.org/10.5281/zenodo.21865793 |
| Version (v0.2) | https://doi.org/10.5281/zenodo.21865794 |
| Record | https://zenodo.org/records/21865794 |
| OSF mirror | https://osf.io/c8rgz/ (10.17605/OSF.IO/C8RGZ) |

**Title:** Below the Masking Threshold: Observable Command-and-Control Discrimination in a Residual IRGC Missile Force

**Creators:** Bilar, Daniyel Yaacov (Chokmah LLC; ORCID 0000-0002-9040-6914)

**Version:** 0.2

**License:** CC-BY-4.0

**Resource type:** publication / preprint

**Upload:** `PHASE2_C2_Observability_REL_FIXED.pdf` only (no software zip)

**Keywords:** command and control; attribution correlation; residual force; launcher attrition; ballistic missile defense; IRGC; Iran; agent-based modeling; OSINT; MILCOM

---

## Deposit description body (paste into Zenodo)

**1. Artifact claim.**  
This deposit is the Phase II companion preprint (v0.2 PDF): an empirical-and-simulation argument that, in a residual IRGC missile force after high week-one attrition, an open-source *attribution-correlation* proxy can discriminate active from pre-programmed C2 under sparse provocation—and that dense provocation saturates that proxy (H_ceiling).

**2. Problem / scientific context.**  
The parent study found that under high launcher attrition, daily launch rate cannot distinguish C2 architectures; only the emergent target ratio discriminates, and it is unobservable from open sources (paper concept DOI [10.5281/zenodo.19210451](https://doi.org/10.5281/zenodo.19210451); version [10.5281/zenodo.19558494](https://doi.org/10.5281/zenodo.19558494)). Phase II tests both sides of the residual-force boundary that finding implies: low attrition with sparse provocation (April–June 2026 skirmish window) versus low attrition with dense provocation after fighting resumed in July 2026.

**3. Contents (this deposit).**  
- Single PDF: Phase II manuscript v0.2 (`PHASE2_C2_Observability_REL_FIXED.pdf`).  
- Not in this deposit: simulation code, CSV outputs, or figure source scripts (those live under the **software** concept DOI [10.5281/zenodo.19210120](https://doi.org/10.5281/zenodo.19210120)).

**4. How to reproduce (prose + pointer to software).**  
The PDF is not executable. Load-bearing simulation and coding artifacts are in the companion repository [chokmah-me/milcom-2026-iran-attrition](https://github.com/chokmah-me/milcom-2026-iran-attrition) under the software concept. Minimal software-side checks: `python verify_milcom_claims.py` (magazine-discipline null gate for the parent stack); Phase II grid via `simulation/phase2_runner.py`; Leg 3 null floor via `simulation/leg3_null_sim.py`. Pre-registration for Leg 3 is stamped at [10.5281/zenodo.21443990](https://doi.org/10.5281/zenodo.21443990).

**5. Relation to software / dual concept.**  
Paper concept (this record’s concept, once minted) ≠ software concept `10.5281/zenodo.19210120`. Leg 1 = residual-force ABM with provocation-response (`phase2_runner.py` / `c2_core.py`); Leg 2 = pre-registered coding tables and retro-audit; Leg 3 = dense-provocation coding plus null simulation. This PDF states claims and tables; the software concept holds runnable code and locked data products.

**6. Limitations / non-claims.**  
- Leg 2 Stream B rests on a small event count; no inferential test is claimed on the empirical rate alone.  
- Attribution correlation is a **proxy** for adaptive targeting, not equivalence to the emergent target ratio.  
- Near-perfect simulation separation at high connectivity reflects pure behavioral archetypes (H1/H2), not guaranteed real-world discrimination.  
- Under dense July provocation, the construct hits H_ceiling and is **not** offered as a standing C2 indicator.  
- Not a claim of MILCOM acceptance; not a targeting doctrine attribution of any named unit beyond the stated coding protocol; not a weapons-employment recommendation.

**7. This version (v0.2 scientific delta).**  
Adds Leg 3 out-of-sample test under resumed hostilities (Section VI), Leg 2 retro-audit of coincidence structure for the three clean Stream B events, H_ceiling interpretation (saturation plus unattributable-antecedent deflation), and count-corrected release narrative. Not a changelog of repository commits.

**8. Citation.**  
Cite the Phase II **paper concept DOI** (always latest PDF) once minted; pin this PDF with the **version DOI**. Cite the parent argument at paper concept `10.5281/zenodo.19210451`. Cite runnable code at software concept `10.5281/zenodo.19210120`.

---

## Related identifiers (for Zenodo metadata)

| Relation | Identifier | Scheme |
|----------|------------|--------|
| references | 10.5281/zenodo.19558494 | doi |
| references | 10.5281/zenodo.19210451 | doi |
| isSupplementedBy | 10.5281/zenodo.19210120 | doi |
| references | 10.5281/zenodo.21443990 | doi |
| isSupplementTo | https://github.com/chokmah-me/milcom-2026-iran-attrition | url |

| isIdenticalTo | 10.17605/OSF.IO/C8RGZ | doi |

## AI utilization (notes field)

Produced with AI assistance (Claude / Anthropic for code extension, pipelines, drafting). Author solely responsible for claims and final judgments. No AI system is a co-author.

## CRE self-check

- [x] Objection-first non-claims (proxy, small-n, H_ceiling, no standing indicator)
- [x] Dual concept OK (PDF-only paper deposit)
- [x] Body ≠ git log
- [x] Parent cite prefers paper DOI `19558494` / concept `19210451` (FIXED PDF body still cites code DOI in [1] — residual for optional v0.2.1)
- [x] Mint/OSF are external gates after this draft
