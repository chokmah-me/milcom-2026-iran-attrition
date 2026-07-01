<p class="hebrew-epigraph" dir="rtl" lang="he">אִם יִרְצֶה הַשֵּׁם</p>

<!-- DATE PLACEHOLDER: Hebrew-calendar date for the session date (Gregorian 1 July 2026).
     Per house convention the Hebrew date is not guessed. Replace with the confirmed string, e.g.:
     <p class="hebrew-date" dir="rtl" lang="he">ט״ז בְּתַמּוּז תשפ״ו</p> -->

# Below the Masking Threshold: Observable Command-and-Control Discrimination in a Residual IRGC Missile Force

Daniyel Yaacov Bilar, Chokmah LLC, chokmah-dyb@pm.me
ORCID: [0000-0002-9040-6914](https://orcid.org/0000-0002-9040-6914)

Version 0.1, prerelease for review. Companion to the v4 attrition-masking paper [1].

## Abstract

A prior agent-based study of the 2026 Iran war found that when launcher attrition exceeds about 70 percent in week one, the daily ballistic-missile launch rate cannot tell an active distributed command-and-control (C2) architecture from a pre-programmed one; only the emergent target ratio discriminates, and that quantity is not available from open sources. This paper tests the other side of that boundary. During the April to June 2026 ceasefire period the surviving Iranian force operated at low tempo and low attrition, the regime in which target selection should stop being swamped by launcher losses. We ask whether an observable discriminator appears there. The discriminator we use is attribution correlation: whether Iran strikes the specific coalition asset that just provoked it, within a fixed window, and says so. A pre-registered coding of the skirmish period gives a Stream B (coalition and Gulf-state targets) attribution correlation near 0.64 against a fixed-target control near 0.0, but the event count is too small to carry an inferential test. To supply the statistics, we extend the canonical model into a residual-force regime with a provocation-response mechanic and run 200 Monte Carlo seeds across a connectivity sweep. On identical runs, launch-rate discrimination between the two architectures stays null (rank-biserial r near 0, p greater than 0.05) while attribution correlation separates them sharply (r from 0.83 to 1.00, p less than 0.001), with a short response latency of one to two days. The discriminator that launch rate cannot see becomes sharp once attrition stops masking targeting. The signal is observable, unlike the emergent target ratio it proxies, which makes it a candidate collection target rather than only a modeling construct.

## I. Introduction

The 2026 US-Israeli campaign against Iran cut Iranian ballistic-missile launch rates by about 92 percent in nine days. A prior agent-based model (ABM) asked whether that fall reflected physical destruction of transporter-erector-launcher (TEL) assets or degradation of command authority, and concluded that launcher attrition explained the dominant share of the launch-rate variance [1]. The same work established a boundary. When week-one attrition is high, three competing C2 hypotheses (active distributed command, pre-programmed autonomous execution, and a mixed state) produce launch-rate curves that are statistically indistinguishable. The only reliable discriminator was the emergent target ratio, the fraction of strikes aimed at targets that became relevant only after the war began. That ratio needs pre-war target packages to compute, so it is a collection requirement, not an open-source measurement.

The boundary has two sides. The v4 paper characterized the high-attrition side, where targeting information is present in the surviving cells but the cells are destroyed before they can act on it. The low-attrition side was named but not tested: once a residual force operates past the acute-attrition phase, does its target selection become observably adaptive?

The April to June 2026 ceasefire period is that regime. Independent US intelligence reporting placed launcher survival at 40 to 50 percent at the April 8 ceasefire, roughly double the model's original assumption [1], and Iranian activity continued at low tempo through the following months. Attrition was no longer fast enough to swamp behavior. If target selection carries a C2 signature, this is where it should surface.

The signature we test is not the emergent target ratio, which stays unobservable, but a weaker observable proxy for it: attribution correlation. An event is attribution-correlated when Iran strikes the specific coalition asset that conducted an identifiable action against it within a fixed window, and Iranian framing links the strike to that action. Attribution correlation captures reactive retargeting. It is not the full adaptive-targeting construct, and the substitution is stated as a limitation, not smuggled in as equivalence.

Two legs make the argument. The empirical leg codes the skirmish period under a pre-registered protocol and reports the attribution-correlation rate. The event count is small by construction, so it carries no inferential test. The simulation leg extends the canonical ABM into the residual-force regime, adds a provocation-response mechanic, and runs enough Monte Carlo seeds to carry the statistics that the empirical record cannot. The two are compared qualitatively.

## II. The Prior Result

The v4 model represents 120 launch cells across five regions, each with a missile inventory, a pre-authorized target list, a pre-authorization expiry day, and a connectivity state to surviving C2 nodes [1]. Three behavioral rulesets encode the hypotheses. H1 (active distributed C2): connected cells receive updated targeting including conflict-emergent targets and prioritize the highest-value available target; disconnected cells fall back to pre-authorized packages. H2 (pre-programmed execution): all cells fire pre-authorized packages regardless of connectivity, and produce no emergent targeting. H3 (mixed): connected cells follow H1 with probability 0.65, otherwise H2.

Two findings from that work set up this one. First, across all phases and five pre-authorization windows, launch-rate differences between H1 and H2 were non-significant (Mann-Whitney U, p greater than 0.05; rank-biserial r less than 0.08). Launch rate is blind to C2 state under high attrition. Second, the emergent target ratio discriminated strongly (r greater than 0.60, p less than 0.001), and a post-conflict re-simulation under realistic 40 to 50 percent survival found the discriminator grew stronger in the residual-force regime, not weaker (r rising from 0.356 to 0.706) [1]. The re-simulation did not, however, connect the emergent ratio to anything an analyst could observe. That gap is what this paper addresses.

## III. Empirical Leg: Coding the Skirmish Period

The empirical leg is a pre-registered coding study of Iranian and Iran-attributed strikes from April to late June 2026. The unit is a retaliatory strike event: one discrete offensive action against a coalition, Gulf-state, or opposition target, bounded in time and target. A multi-target salvo is one event per distinct named target. Purely defensive maritime actions that enforce the strait blockade are logged separately and excluded from the construct.

Events are stratified into two streams before any construct is coded. Stream B, the primary stream, holds coalition and Gulf-state targets: US bases, US naval vessels, and Gulf-state territory and infrastructure. Coalition actions there create new, dated, attributable provocations, so adaptive targeting is testable. Stream A, the control, holds Iranian strikes on Kurdish opposition camps in Iraq, a target set Iran has struck for years. Stream A is a fixed-target baseline expected to show near-zero attribution correlation by construction, and it anchors the low end of the scale.

The construct is attribution correlation, coded 0, 0.5, or 1. A 1 requires both a physical match (the target is the specific asset that acted against Iran within 72 hours) and attributable Iranian framing (a statement from the IRGC, Iranian state media, or a named official linking the strike to that action). A physical match without framing, or framing without a dated antecedent, is 0.5. A standing target with no dated antecedent is 0. The 72-hour window is fixed and not re-tuned; a 48-hour robustness value is declared. Ambiguity defaults down.

Coding the skirmish period gives a Stream B attribution-correlation rate near 0.64 across seven construct events, against a Stream A control near 0.0. The Stream B signal rests on three clean events: the May 7 destroyer exchange, the May 27 to 28 Fateh-110 strike on Ali Al Salem Air Base after that base conducted the prior US strike, and the June 28 Kuwait and Bahrain salvo after US strikes on Iranian sites. Response latency across the three is short, on the order of a day. The event count is small, so no inferential test is claimed on it. The honest reading is that a consistent pattern of attribution-correlated retaliation exists in the low-attrition regime; three events cannot establish that the regime is adaptive. Supplying the statistics is the job of the simulation leg.

## IV. Simulation Leg: Design

The simulation extends the canonical model (`c2_core.py`) into the residual-force regime. The extension is additive: a bit-for-bit parity test against the original module reproduces all v1 and v3 behavior across 192 configurations, so nothing in the prior pipeline moves.

**Residual attrition.** A new attrition profile starts at about 42 percent launcher survival and drifts down slowly to about 38 percent over 60 days, holding the force past the acute-attrition phase. About 50 of the 120 cells survive.

**Provocation-response mechanic.** A provocation is a discrete timed event with a source asset and a response window. Half the provocations are new post-initiation assets, which a pre-programmed force has no package for and cannot strike. Half are standing pre-war targets, which a pre-programmed force can strike by coincidence through its normal firing. The standing half gives H2 a realistic non-zero coincidence floor and keeps the comparison from being decided by construction. When an adaptive cell (H1 or H3) is connected and a provocation window is open, it retaliates directly against the provoker with probability 0.65. H3 retaliates at that probability scaled by its 0.65 mixed-adaptation fraction. H2 never retaliates; it fires its standing list.

**Exogenous tempo.** Fire rate is held flat and equal across hypotheses. Every cell fires at the same low standing rate regardless of C2 state, and a fired shot always produces a launch. C2 state changes what is struck, never how much. This mirrors the v4 modeling choice and makes launch volume unable to discriminate the hypotheses by construction, so any launch-rate separation would be an artifact and its absence is a check, not an assumption.

**In-simulation metric.** Attribution correlation is the fraction of launches that strike a provocation source inside its window. We report two denominators. D_all divides by all launches over the 60 days, matching the empirical whole-period construction. D_win divides by launches fired while a provocation window is open, the pure response rate. D_win is the direct analog of the empirical construct (of the strikes fired during a provocation window, how many hit the provoker), so it is the primary reported metric; D_all is the conservative whole-period figure. The window is 3 days (72 hours) primary and 2 days (48 hours) for robustness. Response latency is recorded per correlated strike.

**Connectivity sweep.** The residual force is assumed to have re-established a flat, reconstituted C2 connectivity. That assumption carries weight, so it is swept rather than fixed, across connectivity levels of 0.20, 0.35, 0.50, and 0.65. Reporting discrimination across the sweep shows how far the result depends on the reconstitution assumption.

Each condition runs 200 Monte Carlo seeds. The provocation schedule is shared across hypotheses for a given seed and window, so the three rulesets see the same provocations and differ only in response. Discrimination between H1 and H2 uses the Mann-Whitney U test with a tie-corrected normal approximation, rank-biserial r as the primary effect size, and Cohen's d reported alongside. The stack is Python standard library only, and the grid runs in about 30 seconds.

## V. Results

The result is a contrast on identical runs. Table I reports H1 versus H2 discrimination at the primary 72-hour window across the connectivity sweep, for launch rate and for attribution correlation.

TABLE I. H1 vs H2 DISCRIMINATION, PRIMARY WINDOW (72h), 200 SEEDS

| Connectivity | r (launch rate) | p | r (D_win) | p | H1 D_win | H2 floor | H3 D_win |
|---|---|---|---|---|---|---|---|
| 0.20 | 0.001 | 0.98 | 0.934 | < 0.001 | 0.174 | 0.034 | 0.113 |
| 0.35 | -0.054 | 0.35 | 0.994 | < 0.001 | 0.249 | 0.034 | 0.176 |
| 0.50 | -0.008 | 0.90 | 1.000 | < 0.001 | 0.348 | 0.034 | 0.240 |
| 0.65 | 0.036 | 0.53 | 1.000 | < 0.001 | 0.434 | 0.034 | 0.303 |

Launch-rate discrimination is null at every connectivity level (p greater than 0.05), reproducing the v4 launch-rate finding inside the residual regime. Attribution correlation separates the two architectures at every level (p less than 0.001; Cohen's d from about 2.5 at the lowest connectivity to about 5 at the highest). Fig. 1 shows the contrast in panel (a) and the by-hypothesis signal in panel (b).

The connectivity sweep sets magnitude, not the qualitative result. H1 in-window attribution correlation rises from 0.17 to 0.43 as reconstituted connectivity rises from 0.20 to 0.65, and H3 tracks below it (0.11 to 0.30), while the H2 coincidence floor holds near 0.034. Even at the lowest connectivity, where an adaptive force is in contact only one time in five, the proxy still separates H1 from H2 (r equal to 0.934, p less than 0.001). The 48-hour robustness window reproduces the pattern: launch rate stays null, and attribution correlation stays significant at every level (r from 0.837 to 1.000, all p less than 0.001), with a shorter one-day median latency. Response latency in the simulation is one to two days across the sweep, matching the roughly one-day latency of the three clean empirical events.

## VI. Discussion

The finding is a boundary flip. Under high attrition, launch rate and target selection are both blind or unavailable, and C2 architecture is masked. Under the residual-force regime, launch rate is still blind, but an observable proxy for target selection separates the architectures cleanly. The discriminator that the v4 paper could name only as an unobservable collection requirement has an observable counterpart once attrition stops masking targeting.

**Comparison to the empirical record.** The simulation and the coding study measure the same construct and agree in direction. Iran, in the skirmish period, struck the specific provoker within a short window and framed it as retaliation, at a Stream B rate near 0.64 against a fixed-target control near 0.0. In simulation, an adaptive force produces exactly this pattern while a pre-programmed force cannot, and the response latency matches. The comparison is qualitative and bounded. The empirical 0.64 sits above the simulated H1 in-window rate (0.43 at the highest connectivity) because the empirical denominator counts only construct-coded events, a more selective population than every in-window launch in the simulation. The levels are not meant to coincide; the direction and the separability are the claim. The empirical Stream B, read against the simulation, is consistent with an adaptive-leaning residual force, not with pure pre-programmed execution.

**What would falsify this.** The simulation is falsifiable in the same spirit as its parent. If launch rate had separated the hypotheses, the exogenous-tempo construction would be wrong and the null check would have failed; it did not. If attribution correlation had collapsed toward the launch-rate null once the H2 coincidence floor was admitted, the proxy would carry no signal and the empirical 0.64 could not discriminate; it did not. The empirical leg carries its own falsification discipline: a low Stream B rate would have been reported as evidence against observable adaptation, not explained away.

**Limitations.** Three bound the result. First, attribution correlation is a proxy. It captures reactive retargeting, not the full adaptive-targeting construct; a force could be adaptive without striking the exact provoker, and a force could claim precise retaliation for propaganda even when targeting was pre-planned. The coding protocol requires both a physical antecedent match and attributable framing to limit the second failure, but the proxy is weaker than the emergent ratio it stands in for. Second, the near-complete separation at higher connectivity (r at or near 1.0) reflects idealized behavioral archetypes. H1 and H2 are pure types; a real force is a mixture, which is what H3 models and what the empirical 0.64 reflects. The simulation shows the discriminator works, not that real-world discrimination is perfect. Third, the reconstituted-connectivity assumption is swept, not measured. The result holds across the swept range, but the true residual connectivity of the IRGC in this period is not known from open sources.

**Collection implication.** Attribution correlation is observable where the emergent target ratio is not. It needs only dated coalition actions, dated Iranian strikes, and attributable Iranian framing, all of which appear in open reporting. That makes it a candidate indicator for the low-attrition regime, to be collected and coded during a campaign rather than reconstructed after declassification. It does not replace the emergent target ratio as the theoretically sound discriminator; it is the observable shadow the emergent ratio casts when a residual force retaliates against fresh provocations.

## VII. Conclusion

The 2026 campaign left a residual Iranian missile force operating at low tempo and moderate attrition through the ceasefire period. In that regime, the launch rate remains blind to command-and-control state, as it was under high attrition, but target selection does not. A pre-registered coding of the skirmish period finds Iranian retaliation correlated with specific coalition provocations at a Stream B rate near 0.64 against a fixed-target control near 0.0, on an event count too small to test. A residual-force simulation, run at proper Monte Carlo scale on identical runs, reproduces the launch-rate null and shows that an observable attribution-correlation proxy separates an active from a pre-programmed architecture at every connectivity level tested, with a response latency that matches the empirical events. The masking that hides C2 architecture under high attrition lifts for target selection once attrition falls, and it lifts for a quantity an analyst can actually see.

## AI Utilization Statement

This work was produced with AI assistance. The author used Claude (Anthropic) for simulation code extension, statistical pipeline construction, figure generation, and manuscript drafting. All substantive claims, analytical decisions, and final editorial judgments were made by the author. AI-generated content was reviewed and corrected by the author before inclusion. No AI system is listed as a co-author.

Affiliation: Chokmah LLC, Norwich, VT. Contact: chokmah-dyb@pm.me.

## References

[1] D. Y. Bilar, "Launcher Attrition Dominates Command Architecture: Agent-Based Analysis of IRGC Missile C2 Degradation in the 2026 Iran War," Zenodo, 2026. doi: 10.5281/zenodo.19558036. [Online]. Available: https://doi.org/10.5281/zenodo.19558036

<!-- REFERENCE NOTE (prerelease): the empirical event sources for Section III
     (CENTCOM, ISW/CTP, JINSA, CNN via the Soufan Center, and the Iranian
     state-media framing statements) are documented per event in the companion
     coding tables and codebook. They need the standard primary-source
     verification pass and IEEE formatting before submission, and are omitted
     here rather than listed unverified. -->
