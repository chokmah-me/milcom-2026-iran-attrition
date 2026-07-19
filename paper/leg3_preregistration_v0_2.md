# Phase II Leg 3 Pre-Registration -- Out-of-Sample Test Under Resumed Hostilities
Locked before data collection. Version 0.2. Date: 2026-07-19.
(v0.1 -> v0.2, same day, before lock: incorporated the simulated coding-scheme null and the Stream A framing-asymmetry finding. Both discovered during pre-lock feasibility checks; documented here rather than in an addendum because no data has been coded.)

**Author:** Daniyel Yaacov Bilar, Chokmah LLC, chokmah-dyb@pm.me

---

## 0. Purpose

Leg 2 found attribution correlation ~0.64 in Stream B (coalition/Gulf-state targets) during the low-attrition residual-force regime (April 8 - June 28, 2026). The Phase II paper argues this is consistent with an H1-like adaptive C2 signature becoming observable once attrition stops swamping the signal.

On July 7, 2026, the June 17 MOU collapsed and major combat operations resumed. The conflict has returned to high-tempo, multi-target exchanges with seven consecutive nights of US strikes and IRGC multi-country retaliation as of July 18.

Leg 3 tests whether any adaptive-targeting signal survives the regime shift back toward acute operations. Pre-lock feasibility work (Section 4a) already established that the raw attribution-correlation construct saturates under dense provocation, so the test runs on saturation-resistant quantities, and the saturation finding is itself a pre-registered result.

## 1. Hypothesis

The simulated null (Section 4a) shows the raw attribution-correlation rate cannot carry the test in the dense regime. Hypotheses are therefore stated on two saturation-resistant quantities:

**Primary: strict-novelty rate.** The fraction of Stream B events striking an asset absent from documented pre-war Iranian target sets (the codebook Section 5 target-novelty flag, elevated from exploratory to primary). A pre-programmed force structurally cannot strike targets that were not in its packages; coincidence cannot inflate this the way it inflates antecedent matching. This is the empirical analog of the v4 paper's emergent target ratio, and Leg 3's honest headline is that the analysis is forced back onto it.

**Secondary: excess over the null band.** Raw Stream B attribution correlation compared against the pre-registered simulated null band of 0.55-0.72. Only a rate above 0.72 counts as any evidence of adaptivity beyond coincidence-plus-framing; anything inside or below the band is uninformative on the raw construct.

**H_persist:** strict-novelty rate at or above 0.10 (at least one in ten July strikes hits a genuinely novel asset), OR raw Stream B rate above 0.72. Adaptive targeting observable despite saturation.

**H_collapse:** strict-novelty rate below 0.05 AND raw rate inside or below the null band. Nothing observable survives the regime shift; the sparse window was necessary.

**H_ceiling (new, and now the expected outcome):** the construct itself saturates as the null sim predicts, and the paper's contribution becomes the boundary result: attribution correlation is a usable OSINT C2 discriminator only below a provocation-density threshold. The null simulation quantifies that threshold.

Thresholds (0.05, 0.10, 0.72) fixed now, not adjusted post hoc.

## 2. Coding window

**Start:** July 7, 2026 (CENTCOM 80+ target strike package, first major post-MOU escalation).
**End:** The earlier of (a) a new ceasefire or MOU taking effect, or (b) August 6, 2026 (30 days from start). No other trigger. In particular, the window does NOT close when coding begins; tying the window to author behavior would let the author (consciously or not) time the cutoff to favorable news. Coding may begin before the window closes, but events through the locked end date must be coded regardless of what they show.

## 3. Codebook

Leg 3 uses the Phase II codebook v0.1 without modification. All definitions, coding levels, anti-gaming rules, field schemas, and coder protocols from the locked codebook apply identically.

Specifically:
- Unit of analysis: retaliatory strike event, one per distinct named target per 24-hour salvo.
- Attribution correlation levels: 1, 0.5, 0 per codebook Section 3.
- 72-hour antecedent window: fixed, not widened.
- Iranian framing requirement: attributable IRGC/state-media/official statement, not analyst speculation.
- Two-source minimum for any attribution_correlated=1.
- Maritime enforcement exclusion: pure blockade enforcement (seizures, inspections) is excluded from the primary construct, same as Leg 2's B2/B3 treatment. Offensive strikes on commercial shipping by Iran ARE included (same as Leg 2's B8 treatment).
- Ambiguity defaults down.

One addition: commercial-vessel targeting by Iran requires a judgment call on whether the target is a coalition/Gulf-state asset (Stream B eligible) or a neutral commercial vessel (not Stream B eligible by the existing schema). **Rule:** A commercial vessel flagged to a US-allied Gulf state (UAE, Saudi, Kuwaiti, Qatari, Bahraini registry) is Stream B eligible. A vessel flagged to a neutral state (e.g., Marshall Islands, Panama, Thailand) is logged but excluded from the primary construct unless Iran's framing explicitly links the strike to a specific coalition action. This mirrors the codebook's requirement that both physical antecedent match AND Iranian framing must hold for a 1.

## 4. Streams

**Stream B extension (primary).** All Iranian offensive strikes against US bases, US naval vessels, Gulf-state territory/infrastructure, and Gulf-flagged commercial shipping in the July 7+ window.

**Stream A IS extended, and its role changes.** In Leg 2 the Kurdish-opposition control anchored the low end of the scale (~0.0) in a sparse-provocation environment. In Leg 3 it becomes the instrument for measuring the dense-provocation confound (Section 4a). Kurdish camps are a fixed target set by construction: any rise in measured Stream A attribution correlation during the July window cannot reflect genuine adaptive targeting. It can only reflect (i) coincidental 72-hour antecedent availability under near-daily coalition strikes, and (ii) the IRGC's now-systematic retaliation framing. The Stream A July rate is therefore a direct estimate of pure framing-and-coincidence inflation, and the quantity of interest is the **Stream B minus Stream A gap**, not the raw Stream B rate. Stream A coding stays at representative resolution (as in Leg 2), but every Stream A event in the window with an available 72-hour antecedent and IRGC framing must be coded under the identical rules applied to Stream B, with no special skepticism applied to A that is not applied to B.

**No Stream C.** The maritime/Strait-specific events are coded as Stream B, not a separate stream. The codebook's target_class enum already includes `shipping` and `gulf_infra`. Adding a separate stream would fragment the comparison with Leg 2.

## 4a. The dense-provocation base-rate problem (central design issue)

Leg 2's 0.64 was measured in a sparse-provocation regime. Coalition actions against Iran between April 8 and June 28 were rare, discrete, dated events. A strike landing within 72 hours of one, on the asset that conducted it, carried real information: the coincidence probability was low.

The July regime breaks that. The US has struck Iran every night since July 7. The 72-hour antecedent window is now permanently open. Any Iranian strike on any US-linked target will have a dated antecedent within 72 hours, mechanically. And IRGC framing has become systematic: numbered "response phases" attached to nearly every operation. Under these conditions, a purely pre-programmed force (H2) firing its standing pre-war target list on a fixed schedule would score high on attribution correlation by coincidence alone. The construct's null expectation is no longer near zero, and the Leg 2 baseline of 0.64 is not directly comparable to any Leg 3 raw rate.

The confound also cuts the other way. Many July coalition strikes are delivered by carrier aviation, standoff munitions, and drones whose originating platform Iran cannot identify or reach. For those events the "specific antecedent actor" requirement of codebook Section 3 may be structurally unsatisfiable: Iran physically cannot strike the carrier that launched last night's sortie if it cannot find it, so strict coding pushes those events to 0.5 regardless of how adaptive the targeting actually is. Inflation from antecedent saturation and deflation from unattributable antecedents operate simultaneously. Neither can be assumed to dominate.

Two pre-registered controls:

**(1) Stream A as the inflation gauge.** See Section 4. The Stream A July rate estimates pure framing-and-coincidence inflation on a target set known to be fixed. The primary Leg 3 quantity is the Stream B minus Stream A gap, reported alongside both raw rates. In Leg 2 this gap was 0.64 - 0.0 = 0.64. The Leg 3 hypotheses (Section 1) are evaluated on the gap, not the raw Stream B rate.

**(2) Antecedent-specificity strictness is held fixed.** The temptation under antecedent saturation is to relax "the specific coalition asset that conducted the action" to "any US-linked target," which would flood the 1 bin. The codebook definition is applied exactly as written. Where the antecedent action came from an unattributable platform (carrier aviation, standoff), the event cannot be coded 1 on physical-match grounds and takes a ceiling of 0.5; this is recorded in coder_note as `antecedent_unattributable` so the deflation effect can be counted, not just suspected. The count of ceiling-limited events is reported in the results.

**(3) Simulated null band (added in v0.2, replaces the gap as primary control).** A Monte Carlo of the coding scheme itself (leg3_null_sim.py, stdlib, 1,000 events per cell) asked: what does a purely pre-programmed force firing at a fixed standing list score on this construct when provocations occur daily and framing is universal? Answer: 0.55 to 0.72 across plausible parameters (framing probability 1.0, antecedent attributability 0.3 to 0.7, 1 to 2 provocations per day). The mechanism is structural: framing alone earns 0.5 per event under codebook Section 3, and with daily provocations originating from the same basing set Iran strikes, chance physical matches supply the rest.

Two consequences. First, Leg 2's Stream B rate of 0.64 sits inside this dense-regime null band. The raw construct cannot discriminate H1 from H2 under continuous provocation. This is itself a pre-registered finding: the attribution-correlation proxy has a tempo ceiling, and the sparse-provocation window of April-June was a necessary condition for its Leg 2 usefulness. Second, the H_persist / H_collapse test cannot run on the raw rate. It runs on the two saturation-resistant quantities defined below.

**(4) Stream A repurposed (supersedes the inflation-gauge role from v0.1).** Feasibility checks found Iran does not frame its Kurdish-camp strikes as retaliation (the July 17 Komala strike that killed nine went unclaimed), while framing every Gulf strike. Because framing behavior differs by stream, Stream A cannot measure the framing floor for Stream B, and the B-minus-A gap does not correct the saturation. Stream A is still coded, but its role is to document the framing asymmetry itself: a regime that selectively performs attribution for one audience and withholds it for another is evidence about the propaganda function of framing, which bears directly on the attribution-laundering threat (Section 7 item 4).

No post-hoc correction beyond these. If these controls prove inadequate, that is reported as a limitation, not patched.

## 5. Statistical posture

Same as Leg 2: **no inferential test on the empirical stream.** N will be small (expected 10-25 events based on current tempo, but this is a guess and does not constrain the analysis). The paper reports proportions and distributions descriptively. Comparison with Leg 2 is qualitative. The simulated null band is a fixed reference, not a fitted model; no inferential claim is made against it.

The hypothesis thresholds in Section 1 are descriptive benchmarks, not significance thresholds. "H_persist confirmed" means the observed rate is at or above 0.50; it does not mean a p-value was computed.

If N exceeds 30, a sensitivity analysis comparing the July rate to the April-June rate using a permutation test is permitted as exploratory, flagged as post hoc, and does not replace the descriptive comparison.

## 6. Simulation prediction (qualitative, no new runs)

The v4 paper's model predicts that under high-attrition conditions (>70% week-one kill rate), attribution correlation should be harder to detect because attrition masks C2 behavioral differences. The Phase II Leg 1 simulation found that attribution correlation separates sharply even under low attrition.

The qualitative prediction for Leg 3: if the July regime restores something close to the v4 paper's attrition conditions for the relevant launcher population, attribution correlation should fall. If the July regime is operationally different enough (maritime focus, fixed coastal targets, different C2 architecture) that the v4 model's predictions do not transfer, attribution correlation may not fall, and the result is not a clean test of the v4 boundary.

**No new simulation runs are pre-registered for Leg 3.** The c2_core.py model covers land-based MRBM cells, not coastal anti-ship infrastructure. Extending the simulation to the maritime domain would require a separate model design, which is a separate pre-registration. If a Leg 3 simulation is wanted after the empirical results are in, it is pre-registered then, not retroactively justified by the empirical findings.

## 7. Threats to validity specific to Leg 3

In addition to all threats listed in codebook Section 8:

1. **Domain shift.** The July target set (Strait shipping, coastal infrastructure, Gulf-state desalination/power plants) is different from the April-June target set (US bases, US naval vessels). Attribution correlation measured on a different target population may not be comparable to Leg 2's 0.64.

2. **Escalation bias / antecedent saturation.** This is the central confound and is handled structurally, not just noted: see Section 4a. The gap construction (B minus A) and the `antecedent_unattributable` ceiling flag are the pre-registered controls.

3. **Fog of war.** Active high-tempo fighting produces more conflicting reports, more contested attributions, and shorter timelines for source verification. Coding quality may be lower than Leg 2. The two-source minimum for any 1 and the ambiguity-defaults-down rule are the primary controls.

4. **Attribution laundering at scale.** The IRGC has formalized its retaliatory framing (numbered "response phases" in official statements; one tracker source names the July campaign "Operation Nasr 2," but that name is thinly sourced and should be verified before use in the paper). This suggests institutional investment in appearing adaptive. The more systematic the framing, the harder it is to distinguish genuine reactive targeting from propaganda overlaid on pre-planned targeting. This threat was flagged in codebook Section 8 item 2 but is more acute in Leg 3.

5. **Survivorship of the coding scheme.** The codebook was designed for a low-tempo, small-N observational log. At 15-25 events it may encounter edge cases the rules do not cleanly cover. Any edge case that requires a judgment call not anticipated by the codebook is documented in a Leg 3 build-notes addendum, coded conservatively, and flagged for a second pass.

## 8. Falsification table

| Observation | Threshold | Interpretation |
|---|---|---|
| Strict-novelty rate >= 0.10 | Primary | H_persist. Adaptive targeting visible through the saturation-resistant channel. |
| Strict-novelty rate < 0.05 and raw rate inside/below null band (0.55-0.72) | Primary + secondary | H_collapse. No adaptive signal survives the regime shift. |
| Raw Stream B rate > 0.72 | Above null upper bound | Weak supporting evidence for H_persist; interpret only alongside novelty rate, never alone. |
| Raw Stream B rate 0.55-0.72 | Inside null band | Uninformative on the raw construct, as pre-registered. Confirms H_ceiling. |
| Stream A framing asymmetry persists (Gulf strikes framed, Kurdish strikes unclaimed) | Qualitative | Supports the propaganda-function reading of framing; strengthens the attribution-laundering caveat on all framed events. |
| More than half of Stream B events flagged `antecedent_unattributable` | Deflation count | Strict physical match unsatisfiable in a standoff environment; construct limitation, reported. |
| Fewer than 5 construct-coded Stream B events | N floor | No result. Report raw data. Legitimate outcome. |

## 9. Deviations

Any deviation from this pre-registration is documented in a dated build-notes addendum (leg3_build_notes_v0_1.md), not retroactively edited into this document. The pre-registration is immutable once the first July event is coded.

## 10. What this leg does NOT do

- Does not extend or modify Leg 2 coding tables.
- Does not run new simulations in c2_core.py.
- Does not make inferential statistical claims on empirical data.
- Does not retroactively adjust the codebook.
- Does not claim to test the v4 paper's launch-rate discrimination finding (different target population, no simulation leg).

It tests one thing: whether the attribution-correlation signal that appeared in the low-attrition window survives the return to high-tempo operations, or whether it was a product of the quiet period that revealed it.
