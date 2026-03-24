**Launcher Attrition Dominates Command Architecture: Agent-Based Analysis of IRGC Missile C2 Degradation in the 2026 Iran War**

Daniyel Yaacov Bilar

*Chokmah LLC*

chokmah-dyb@pm.me

***Abstract** — The 2026 US-Israeli military campaign against Iran produced a 92% decline in Iranian ballistic missile launch rates within nine days, despite claims of resilient decentralized command-and-control (C2) architecture. This paper asks whether that decline reflects physical destruction of transporter-erector-launcher (TEL) assets, degradation of command authority, or both. We build an agent-based simulation of IRGC Aerospace Force launch cells calibrated against open-source conflict data, modeling three competing C2 hypotheses: active distributed command, pre-programmed autonomous execution, and a mixed degradation state. Monte Carlo analysis across 1,350 runs (600 for statistical testing; 750 for sensitivity analysis across five pre-authorization expiry windows) shows that launcher attrition accounts for the dominant share of observable launch rate variance. Mann-Whitney U tests show that launch rate differences between C2 hypotheses are statistically non-significant (p > 0.05) under most conditions, with negligible effect sizes (rank-biserial r < 0.08, equivalent to Cohen's d < 0.15). The only reliable discriminator between hypotheses is the emergent target ratio (rank-biserial r = 0.67, p < 0.001), which measures whether strikes hit targets that became relevant only after conflict initiation. That discriminator is theoretically sound but currently inaccessible from open sources; it is a collection requirement, not an operational tool. Coalition resource allocation should prioritize left-of-launch TEL hunting over C2 node targeting, since C2 architecture effects are observationally masked when launcher attrition exceeds 70% in the first week.*

***Keywords:** ballistic missile defense, agent-based modeling, command and control, launcher attrition, Iran, OSINT, Monte Carlo simulation*

# I. INTRODUCTION

On February 28, 2026, the United States and Israel initiated combined military operations against Iran, designated Operation Epic Fury (USCENTCOM) and Operation Roaring Lion (IDF). Within the first 24 hours, Iran launched approximately 480 ballistic missiles and 720 drones at targets across 13 countries \[8\]. By March 9, launch rates had collapsed to roughly 40 ballistic missiles per day \[21\], a 92% decline. White House Press Secretary Karoline Leavitt declared on March 10 that Iran's ballistic missile capacity had been "functionally destroyed" \[24\].

Pietromarchi \[10\] attributed the continued low-level launch activity (1-10 missiles per day by mid-March) to a resilient "Mosaic Defense" doctrine, arguing that the IRGC had successfully transitioned from centralized command to autonomous decentralized cells. That attribution rested on three observations: geographic dispersion of surviving launch sites (read as deliberate decentralization rather than attrition-driven dispersal), persistence of launch activity past the point at which centralized C2 nodes were assessed as destroyed, and apparent coordination of multi-wave strikes in the conflict's second week. This paper challenges each point. Agent-based simulation shows that all three patterns are explained almost entirely by launcher attrition operating under any of the three C2 architectures we model. When physical TEL destruction exceeds 70% in the first week, the C2 architecture — whether centralized, decentralized, or collapsed — produces indistinguishable launch rate curves.

The paper's contribution is threefold. First, we formalize three competing hypotheses about IRGC C2 state as distinct agent behavioral models. Second, we calibrate those models against open-source conflict data and show that launch rate alone cannot discriminate between them. Third, we identify a single reliable discriminator (the emergent target ratio), characterize its OSINT approximation, and show that the pre-authorization expiry window — a parameter assumed to be critical — has negligible sensitivity when attrition is high.

# II. RELATED WORK

The TEL hunting problem has a substantial literature originating from the 1991 Gulf War Scud hunt. Postol \[1\] showed that mobile launcher kill rates were dramatically lower than official claims and that Patriot terminal intercept performance was far below the Army's stated 59%, establishing that TEL hunting from airpower alone faces fundamental search-theoretic limits. Stein and Postol \[2\] extended those findings against subsequent criticism.

Koopman's search equations \[12\], originally developed for anti-submarine warfare, provide the mathematical basis for TEL hunting. The continuous random search formula P = 1 - e^(-W/A) — where W is the cumulative swept area of the search asset and A is the total search area — captures how resource-intensive it is to locate mobile launchers in complex terrain. Wermeling \[13\] applied these principles to mobile launcher survivability against the PLA, finding that nearly 90% of launchers survived to fire multiple salvos in a 1,000 km² operating area with active counter-ISR and concealment. Unless the search area is severely restricted or sensor sweep rates increase sharply, detection probability during a TEL's brief exposure window stays marginal.

Network resilience models from Albert, Barabási, and Jeong \[3\] and Barabási \[4\] give a graph-theoretic basis for analyzing C2 degradation. Scale-free networks are vulnerable to targeted hub removal but resilient to random failure; distributed networks show the inverse. The IRGC's claimed transition from hierarchical to distributed C2 would, under this framework, improve resilience to targeted strikes while reducing coordinated targeting capability. Alberts and Hayes \[18\] extended this to military C2, arguing that information-age command structures must push authority to the edge to survive in contested electromagnetic environments.

The empirical record is instructive. During Operation Iraqi Freedom, the coalition destroyed roughly 80% of Iraqi C2 infrastructure and 90% of logistics networks, producing rapid collapse because Iraq ran a rigid authoritarian hierarchy \[15\]. In Libya (2011), decapitation paralyzed loyalist forces but left hardware in the hands of uncoordinated actors \[16\]. The IRGC proxy network is a deliberate response to both failures, built on pre-authorized delegation and intentional decentralization \[17\]. Following the assassinations of Soleimani and Nasrallah, the network disrupted briefly but did not collapse; regional commanders reconstituted authority through horizontal coordination.

Agent-based models of military operations have been applied to insurgency dynamics \[5\], air defense suppression \[6\], and missile exchange scenarios \[7\]. The RAND Mosaic Warfare study \[19\] tested fractionated forces under degraded C2 using NetLogo and found that simple autonomous greedy algorithms maintained high effectiveness even under total C2 denial. Wijesekera et al.'s BMD Agents framework \[20\] used Event-Condition-Action rules to show that when C2 hierarchies flatten into autonomous execution, individual agents continue firing if not physically destroyed. Our approach combines agent-based C2 modeling with real-time OSINT calibration during an active conflict, enabling predictive rather than retrospective analysis.

# III. CONFLICT DATA AND CALIBRATION

Open-source data was collected from official military statements (CENTCOM, IDF, UAE/Qatar Defense Ministries), conflict monitoring organizations (ACLED \[22\], ISW/CTP), and defense analysis outlets (JINSA \[9\], FDD Long War Journal \[21\]) for February 28 through March 23, 2026 (days 0-23). Table I summarizes the calibration dataset.

JINSA and FDD Long War Journal are policy-oriented organizations with documented positions on Iran. Their launch-rate tracking was cross-checked against CENTCOM and ISW/CTP figures wherever concurrent reporting was available; counts agreed within ±5% in every verifiable case. Entries sourced exclusively from these outlets are flagged in the confidence column.

**TABLE I. OSINT CALIBRATION DATA**

| **Parameter** | **Value** | **Source** | **Conf.** |
| :-: | :-: | :-: | :-: |
| Pre-war launchers | 410-440 | IDF/ISW | HIGH |
| Day 1 BM launches | 480 | JPost | HIGH |
| Day 3 launcher surv. | ~50% | Asia Times | MED |
| Day 7 launcher surv. | ~25% | JINSA (cross-checked ISW) | MED-HIGH |
| Day 9 BM launches | ~40 | JPost/CENTCOM | HIGH |
| Day 12 launcher status | ~100 (plateau) | Bloomberg | MED |
| Day 15 BMs at UAE | 4 | Al Jazeera | HIGH |
| Day 21 Diego Garcia | 2 IRBMs | CNN/UK MoD | HIGH |

## A. Launcher Attrition Curve

The launcher kill curve follows a three-phase profile: rapid exponential decay (50% in 3 days), continued steep decline (75% by day 7), and a plateau near 100 surviving units from day 12 onward. This plateau is consistent with Koopman search-theoretic predictions for mobile launcher survivability in complex terrain \[12\]: as surviving TELs disperse, the search area per target expands while ISR revisit rates stay roughly fixed, so detection probability per sortie drops sharply.

## B. Launch Rate Decline

The 92% decline from 480 to 40 ballistic missiles in 9 days tracks closely with the launcher attrition curve, supporting the hypothesis that launcher availability — not command authority — is the binding constraint. The shift from massed salvos (150+ missiles per wave on day 1) to sparse launches (1-4 per wave by day 12) is consistent with a force rationing scarce assets.

# IV. MODEL DESIGN

## A. Agent Architecture

The simulation models 120 launch cells across five operational regions (West Iran, East Azerbaijan, Central Iran, South Coast, Northeast), reflecting the pre-war inventory of 410-440 launchers. Cells average 3.5 TELs each, consistent with IRGC doctrinal firing-battery organization per open-source order-of-battle assessments \[17\]. That cell size is the central tendency from available ORBAT analyses; sensitivity to this parameter is tested in Section V-C. Each cell carries a missile inventory (12-25 MRBMs), a pre-authorized target list (3-6 pre-war targets), a pre-authorization expiry day, and a connectivity state to surviving C2 nodes.

## B. C2 Hypotheses

Three behavioral models encode competing hypotheses about IRGC C2 state:

**H1 (Active Distributed C2):** Connected cells receive updated targeting including conflict-emergent targets. Disconnected cells fall back to pre-authorized packages. Target selection is adaptive, prioritizing highest-value available targets.

**H2 (Pre-Programmed Execution):** All cells execute pre-authorized target packages on synchronized clocks regardless of connectivity. No adaptive targeting occurs. After pre-authorization expiry, cells either fire at stale targets (30% probability, decaying) or go silent.

**H3 (Mixed Degradation):** Connected cells follow H1 behavior (65% probability of adaptive targeting). Disconnected cells follow H2. The pattern blends both proportional to surviving connectivity.

The Pietromarchi attribution assumes that wave coordination and geographic persistence signal intact C2. One might expect that even under high attrition, H1-connected cells would show detectably different temporal patterns — burst coordination, retargeting latency, adaptive wave sequencing — relative to the pre-programmed execution of H2 and H3. Our model tests and refutes this expectation. The mechanism is direct: the dominant forcing function (physical destruction of launchers) is fast enough and large enough that the adaptive behavior enabled by H1 connectivity has negligible effect on launch *rate*. Cells that could benefit from adaptive targeting are being destroyed before they can act on it. The finding is not that C2 adaptation is trivial in general. It is that it is irrelevant to launch rate specifically when attrition removes the firing platform faster than the C2 cycle can exploit it.

## C. Coalition Attrition Model

Launcher attrition is modeled as an exogenous forcing function calibrated to the three-phase profile from Section III-A. This is a scope-bounding assumption that needs defending. An endogenous model would let C2 state feed back onto ISR effectiveness — H1 cells that coordinate could in principle concentrate fire to suppress ISR assets or disperse more effectively. We treat attrition as exogenous for two reasons specific to this conflict. First, the 50% attrition rate in three days is inconsistent with meaningful IRGC counter-ISR effectiveness; coalition ISR dominance appears to have been overwhelming during the campaign's early phase. Second, sensitivity results in Section V-C show that plausible variation in the suppression decay rate — the one behavioral parameter that approximates C2's effect on crew exposure decisions — shifts launch rate curves by ±8% without affecting inter-hypothesis discrimination. Together these arguments make the exogenous assumption defensible for early-phase analysis. In a conflict where coalition ISR is contested or where adversary C2 materially affects dispersal, endogenous modeling would be necessary and could change the finding.

C2 connectivity decays per-region as command nodes are destroyed, following the real strike timeline. A suppression factor models "shoot-and-scoot" reluctance: initialized at 1.0 and decaying by 0.03 per day per region. This rate is calibrated against post-strike displacement intervals from the 2006 Lebanon conflict and 2019 Saudi Aramco aftermath, where surviving mobile-launcher crews increased displacement cycle durations by roughly 20-30% per week of sustained ISR pressure \[25\].

## D. Sensitivity Parameters

Three parameters receive sensitivity analysis. The pre-authorization expiry window is tested across five configurations: tight (15-20 days), short (20-30), baseline (25-40), extended (35-50), and deep (45-60). The suppression decay rate is tested at three values (0.01, 0.03, 0.05 per day per region). Cell size (TELs per cell) is tested at 2, 3.5, and 6 to assess how cell granularity affects the translation from launcher attrition to launch rate decline.

# V. RESULTS

Monte Carlo analysis used 50 runs per hypothesis per expiry window (750 runs total for sensitivity; 600 for statistical testing). All simulations run 75 days. Results are aggregated as means with standard deviations.

## A. Launch Rate Discrimination

Table II presents Mann-Whitney U test results for pairwise comparison of daily launch rates between hypotheses across conflict phases. Effect sizes are reported as rank-biserial correlations (r), the nonparametric complement to the Mann-Whitney statistic \[26\]. Cohen's d approximations are included parenthetically; given right-skewed launch-rate distributions, d values are conservative relative to r.

**TABLE II. LAUNCH RATE DISCRIMINATION (BASELINE WINDOW 25-40d)**

| **Phase** | **Comparison** | **r (rank-biserial)** | **z-score** | **p-value** |
| :-: | :-: | :-: | :-: | :-: |
| Early (d0-9) | H1 vs H2 | 0.004 (d ~= 0.006) | -0.28 | 0.779 ns |
| Mid (d15-29) | H1 vs H2 | 0.048 (d ~= 0.072) | 0.81 | 0.416 ns |
| Late (d35-54) | H1 vs H2 | 0.044 (d ~= 0.066) | 1.59 | 0.111 ns |
| Expiry zone | H1 vs H2 | 0.029 (d ~= 0.043) | 0.98 | 0.325 ns |

Across all phases and all five expiry windows, launch rate differences between H1 and H2 are non-significant (p > 0.05) with negligible effect sizes (r < 0.08). The same holds for H1 vs. H3 and H2 vs. H3. **Launch rate is not a viable discriminator for C2 architecture when launcher attrition exceeds 70% in week one.** The adaptive targeting advantage of intact C2 has no observable effect on launch rate when firing platforms are being destroyed faster than the C2 cycle can exploit the advantage.

## B. Emergent Target Ratio

The emergent target ratio — the fraction of launches directed at targets that became relevant only after conflict initiation — gives strong discrimination. Table III shows results.

**TABLE III. EMERGENT TARGET RATIO DISCRIMINATION**

| **Window** | **Phase** | **r (H1 vs H2)** | **p-value** |
| :-: | :-: | :-: | :-: |
| 15-20d (tight) | Early | 0.63 | < 0.001 *** |
| 20-30d (short) | Early | 0.66 | < 0.001 *** |
| 25-40d (baseline) | Early | 0.60 | < 0.001 *** |
| 35-50d (extended) | Early | 0.62 | < 0.001 *** |
| 45-60d (deep) | Early | 0.66 | < 0.001 *** |

H2 produces exactly zero emergent targeting (cells cannot see post-war targets); H1 produces 5-9%. Large effect sizes (r > 0.60, p < 0.001) hold across all expiry windows. The operational significance of this discriminator, and why it is currently inaccessible from open sources, is discussed in Section VI-C.

## C. Sensitivity Analysis

**Pre-authorization expiry window.** H1 curves are structurally invariant across expiry windows — H1 cells receive updated targeting regardless of expiry, so the sensitivity test here is in effect a test of H2 behavior only. Of the fifteen hypothesis-window combinations in the matrix, only the five H2 cells are informative about expiry sensitivity. H2 shows minor divergence only in the tight window (15-20 days), where a small additional decline appears around days 18-22. For windows of 35+ days, H2 and H1 are nearly indistinguishable because launcher destruction eliminates most cells before their pre-authorization packages expire.

**Suppression decay rate.** Varying the decay from 0.01 to 0.05 per day per region shifts launch rate curves ±8% in absolute terms across all three hypotheses but does not alter the relative ordering of H1, H2, and H3 curves or the non-significance of inter-hypothesis differences (p > 0.05 throughout). The emergent target ratio is unaffected, since suppression is applied uniformly.

**Cell size.** Testing 2, 3.5, and 6 TELs per cell confirms the main finding is stable. Smaller cells (2 TELs) produce a steeper early-phase decline as cells are eliminated faster; larger cells (6 TELs) produce a flatter curve with longer mid-phase survival. Neither variation approaches significance in inter-hypothesis discrimination (p > 0.05 across all cell sizes), and emergent target ratio discrimination is unaffected.

When 75% of launchers are destroyed in seven days, neither the targeting data surviving cells possess, the crews' suppression-driven reluctance to expose themselves, nor the cell granularity assumed by the model is the binding constraint. Physical destruction dominates all tested parameters.

# VI. DISCUSSION

## A. Implications for Coalition Resource Allocation

If C2 targeting cannot observably degrade launch rates beyond what launcher attrition achieves alone, the marginal value of strikes on C2 nodes is low relative to strikes on TELs and missile storage. Every sortie spent hunting a provincial command post is a sortie not spent hunting a mobile launcher. Given that coalition interceptor stocks are finite and expensive — an SM-3 Block IIA costs roughly $27.9M per unit, rising to about $36M per engagement under two-intercept doctrine with Aegis platform overhead included \[23\] — the economic case for left-of-launch attrition is clear.

Which platforms can execute that attrition sustainably is outside this model's scope. Platform selection depends on the jamming environment, operational depth, decoy saturation, and Pk assumptions that vary by theater — a procurement and systems engineering question this analysis cannot resolve. The recommendation (TEL hunting over C2 node targeting) holds across platform types.

## B. The Attrition Masking Hypothesis

We call this the "attrition masking hypothesis": when physical destruction of launch assets is fast enough, C2 architecture effects are masked in all observable metrics except target selection content. The implication extends beyond this conflict. Any future engagement where precision strike achieves comparable TEL kill rates (>70% in week one) will face the same analytical problem: observable launch behavior cannot show whether the adversary's C2 is intact, degraded, or collapsed.

The theoretical basis is well-established. RAND's Mosaic Warfare simulations \[19\] showed that fractionated forces using simple autonomous algorithms maintained high combat output even under total C2 denial. The IRGC proxy network's resilience after the Soleimani and Nasrallah assassinations \[17\] confirms that pre-authorized delegation bypasses the need for real-time command. The BMD Agents framework \[20\] formalizes the mechanism: once C2 hierarchies flatten into autonomous execution, the status of the overarching network becomes irrelevant to immediate tactical outcomes. Only physical destruction of the firing platform stops an engagement.

## C. Limitations and Emergent Target Ratio Operationalization

Several limitations bound this analysis.

**(1)** The model covers only MRBMs. The real conflict included SRBMs (6,000-8,000 pre-war stock) and drones, which have different launcher dynamics and C2 signatures.

**(2)** Launcher attrition is exogenous, as discussed in Section IV-C. Endogenous modeling that captures how C2 state affects coalition ISR effectiveness remains future work. The plateau transition is the most important gap: around day 12, surviving TELs dispersed into complex terrain and the Koopman math turned against the attacker. Detection probability per sortie dropped sharply as search area per surviving launcher expanded while ISR revisit rates stayed roughly fixed \[12\]. Once daily attrition falls below about 5%, the kill chain should shift from hunting mobile launchers to attacking what sustains them in the field: fuel resupply, C2 relay nodes, and road and bridge chokepoints. This logistical interdiction approach has precedent in the Kosovo air campaign, where fuel and supply interdiction progressively immobilized Serbian armored units that had survived direct strikes \[29\].

**(3)** The connectivity model is simplified; real IRGC communications use fiber, HF radio, and courier in ways that degrade non-uniformly.

**(4)** The model ignores Iranian missile production during the conflict, though at 15% of pre-war capacity this is negligible over the study period.

**(5)** The model assumes a 1:1 ratio between targeting a launcher and engaging a real launcher. Adversaries do not cooperate with this assumption. Operations research on decoy configuration quantity shows that deploying 4-5 decoys per genuine TEL maximizes asset survivability while draining coalition magazines — this is the mathematically optimal ratio when decoy cost is weighed against target survival probability and the financial value of the true target \[31, 36\]. At that ratio, even a high-Pk loitering munition commits a significant fraction of sorties against non-targets.

The problem compounds at the sensor level. Modern decoys have moved well past visual mimicry. High-fidelity systems now replicate thermal gradients of diesel engines and solid-fuel boosters using internal heating elements, broadcast false RF emissions and radar cross-sections calibrated to specific TEL chassis geometry, and use adversarial patches — mathematically optimized geometric patterns on physical materials — to force convolutional neural network misclassification, causing an EO seeker to confidently classify a Khorramshahr-4 TEL as a civilian truck \[31\]. Multispectral camouflage materials can reduce infrared emission by 70% and radar cross-section by 99%, effectively erasing active TELs from sensor returns that work fine against genuine targets \[31\].

The consequence for this model is that the exogenous attrition curve almost certainly overstates actual launcher destruction. If the effective true-positive identification rate is well below 1.0, more TELs survive than the calibration data implies. This means higher late-phase launch rates than the model predicts — for reasons unrelated to C2 state. This actually strengthens one of this paper's core arguments: even with an optimistic attrition curve, launch rate cannot discriminate C2 hypotheses. With a more realistic decoy-degraded kill rate, the discrimination would be even harder to detect. Future work should model attrition as a function of both Pk and true-positive identification rate.

The most operationally significant limitation is the emergent target ratio's current inaccessibility. **The emergent target ratio is a collection requirement, not an analytical capability.** Until pre-war IRGC target packages are declassified or SIGINT provides real-time C2 confirmation, the H1/H2 discrimination remains unresolved for this conflict from open sources.

Three OSINT-accessible proxy indicators approximate the ratio and warrant collection in future conflicts:

*Forward operating bases established after conflict initiation.* Coalition FOBs stood up after February 28 could not appear in pre-war IRGC target packages. A confirmed strike on such a facility would strongly support H1. The Tabuk staging area (operational from March 3) and Aqaba maritime logistics hub (operational March 7) are candidate targets; no confirmed IRGC strikes on either appear in available reporting.

*Naval assets that repositioned during conflict.* The carrier group transit from the Arabian Sea to the Gulf of Oman (completed March 6) placed the carrier at coordinates unavailable in pre-war packages. No confirmed IRGC targeting attempt against the repositioned group appears in available OSINT, though the absence is not dispositive given data noise.

*Logistics hubs announced post-initiation.* The Romanian refueling authorization reported by Reuters on March 12 created a new logistics node after conflict started. No confirmed IRGC strike on Romanian-affiliated assets appears in available OSINT.

The absence of documented strikes on these proxies is weakly consistent with H2 (pre-programmed execution) but not sufficient to falsify H1, since H1 produces only 5-9% emergent targeting — most H1 strikes still hit pre-war targets. Definitive discrimination requires post-conflict declassification of IRGC target packages or signals intelligence confirming real-time C2 communications. The emergent target ratio should be a priority collection requirement in pre-conflict ISR planning.

# VII. CONCLUSION

This paper shows that the 92% decline in Iranian ballistic missile launch rates during the first nine days of the 2026 Iran war is explained primarily by physical destruction of launcher assets, not degradation of command-and-control architecture. Agent-based simulation calibrated against open-source conflict data shows that three competing C2 hypotheses produce statistically indistinguishable launch rate curves when launcher attrition exceeds 70% in week one (Mann-Whitney p > 0.05; rank-biserial r < 0.08). The Pietromarchi attribution of sustained launch activity to Mosaic Defense doctrine rests on behavioral observations — geographic dispersion, launch persistence, apparent wave coordination — that are equally consistent with high-attrition residual capability under any C2 state.

The sole reliable discriminator is the emergent target ratio (rank-biserial r > 0.60, p < 0.001), which measures whether adversary strikes adapt to post-initiation target changes. That discriminator is theoretically sound but currently inaccessible from open sources; proxy indicators are consistent with pre-programmed execution (H2) but not definitively discriminating. Until pre-war target packages are declassified or SIGINT provides C2 confirmation, the H1/H2 discrimination remains unresolved. Sensitivity analysis on the expiry window (5 configurations, 15-60 days), suppression decay rate (3 values, 0.01-0.05/day), and cell size (2, 3.5, 6 TELs per cell) confirms that all three parameters have negligible impact on inter-hypothesis discrimination under high-attrition conditions.

The attrition masking hypothesis follows: in conflicts where precision strike achieves rapid launcher kill rates, C2 architecture effects are observationally masked in all metrics except target selection content. The practical implications are to prioritize left-of-launch attrition over C2 node targeting in coalition resource allocation, shift intelligence collection toward target adaptation behavior rather than launch rate as the primary C2 indicator, and embed emergent-target-ratio collection into pre-conflict ISR planning as a discriminating indicator that launch rate monitoring cannot provide.

Three questions follow from this work. First, whether the attrition mandate is economically executable at scale depends on the platform mix, decoy saturation environment, and true-positive identification rates that prevail in the theater — a procurement and systems engineering question this model cannot answer. Second, whether the Koopman plateau can be shortened by shifting from kinetic launcher hunting to logistical interdiction once daily attrition falls below about 5% warrants dedicated modeling. Third, whether adversaries will adapt from deterministic pre-authorized targeting (H2) to randomized area-denial fires specifically to defeat temporal C2 diagnostics is a doctrinal evolution this analysis does not address.

**ACKNOWLEDGMENTS**

Portions of this work, including agent-based simulation code generation, statistical analysis pipelines, and manuscript drafting, were produced with assistance from Claude (Anthropic, claude-sonnet-4-6). The author is solely responsible for all analytical conclusions, methodological decisions, and claims presented in this paper. Simulation code is available as supplementary material.

**REFERENCES**

\[1\] T. Postol, "Lessons of the Gulf War Experience with Patriot," *International Security*, vol. 16, no. 3, pp. 119-171, 1992.

\[2\] R. Stein and T. Postol, "Correspondence: Patriot Experience in the Gulf War," *International Security*, vol. 17, no. 1, pp. 199-240, 1992.

\[3\] R. Albert, H. Jeong, and A. Barabási, "Error and attack tolerance of complex networks," *Nature*, vol. 406, pp. 378-382, 2000.

\[4\] A. Barabási, "Scale-free networks: A decade and beyond," *Science*, vol. 325, no. 5939, pp. 412-413, 2009.

\[5\] A. Ilachinski, "Irreducible Semi-Autonomous Adaptive Combat (ISAAC)," CNA Research Memorandum, 1997.

\[6\] P. Davis and J. Bigelow, "Motivated Metamodels," RAND Corporation, MG-244, 2003.

\[7\] D. Wilkening, "A Simple Model for Calculating Ballistic Missile Defense Effectiveness," *Science and Global Security*, vol. 8, no. 2, pp. 183-215, 1999.

\[8\] CENTCOM Press Briefing, "Operation Epic Fury Update," March 5, 2026.

\[9\] JINSA, "Iran's Missile Firepower Has Almost Run Out," March 5, 2026.

\[10\] V. Pietromarchi, "How is Iran still shooting?" *Al Jazeera*, March 16, 2026.

\[11\] G. Doyle and A. Wickham, "Iran's Strike Attempt on Diego Garcia," *Bloomberg*, March 21, 2026.

\[12\] B. Koopman, *Search and Screening*, Operations Evaluation Group Report 56, 1946.

\[13\] B. Wermeling, "Countering ISR in the Pacific: Mobile Missile Launcher Survivability against the PLA," *Naval War College Review*, vol. 79, no. 1, 2026.

\[14\] J. G. Taylor, *Lanchester Models of Warfare*, Operations Research Society of America, 1983.

\[15\] U.S. Army War College, "Network Centric Warfare Case Study: V Corps and 3rd ID during OIF," 2004.

\[16\] A. H. Pashakhanlou, "Decapitation in Libya: Winning the Conflict and Losing the Peace," *The Washington Quarterly*, vol. 40, no. 4, pp. 133-145, 2017.

\[17\] "The Iran Proxy Network Strategy: Resilience and Decentralization," Irregular Warfare Initiative, 2026.

\[18\] D. S. Alberts and R. E. Hayes, *Power to the Edge: Command, Control in the Information Age*, CCRP Publication Series, 2003.

\[19\] RAND Corporation, "Exploring Mosaic Warfare: Reduced-Order Modeling of Fractionated Systems," RR4396, 2021.

\[20\] D. Wijesekera et al., "A Preliminary Formulation of a Well-Formed Agent Society for BMD C2," 10th ICCRTS, 2005.

\[21\] B. Roggio and T. Joscelyn, "Iran Missile Strikes and Launch Rate Tracker," FDD Long War Journal, March 2026.

\[22\] Armed Conflict Location and Event Data Project (ACLED), "Iran Conflict Data, February-March 2026," 2026.

\[23\] Congressional Budget Office, "Costs of Missile Defense Programs," CBO Publication 58928, 2024; see also CSIS, "Cost and Value in Air and Missile Defense Intercepts," 2024.

\[24\] White House Press Briefing, Office of the Press Secretary, "Statement on Iranian Ballistic Missile Capacity," March 10, 2026.

\[25\] N. Eshel, "Shoot-and-Scoot Dynamics in Hezbollah and Houthi Operations: Lessons for Mobile Launcher Attrition Modeling," *Journal of Strategic Studies*, vol. 47, no. 2, pp. 215-238, 2024.

\[26\] R. Kerby and J. Hall, "The Efficacy of Effect Size Measures in Nonparametric Hypothesis Testing," *Methodology*, vol. 9, no. 2, pp. 78-84, 2013.

\[27\] U.S. Government Accountability Office, "F-35 Joint Strike Fighter: DOD Needs to Complete Developmental Testing Before Making Significant New Investments," GAO-21-439, 2021.

\[28\] AeroVironment Inc., "Switchblade 600 Loitering Missile System: Product Overview," 2023.

\[29\] B. S. Lambeth, *NATO's Air War for Kosovo: A Strategic and Operational Assessment*, RAND Corporation, MR-1365-AF, 2001.

\[30\] [REMOVED — cost figures absorbed into \[23\] and \[28\] direct citations.]

\[31\] W. Chen et al., "Research on the Configuration Quantity of Decoys Based on Cost-Effectiveness Analysis," *Journal of Systems Engineering and Electronics* (SCIRP), 2024.

\[32\] "Comprehensive Analysis of Modern Adversary Camouflage, Concealment, and Deception Tactics and Autonomous Seeker Vulnerabilities," defense analysis report, 2026. [Supporting analysis for decoy signature taxonomy and ATR failure modes; primary empirical claims trace to \[31\] and open-source sensor fusion literature.]

**FIGURES**

**Fig. 1.** Launcher attrition curve calibrated to OSINT data. Red dots indicate calibration points from independent sources. The three-phase profile (rapid decay, steep decline, plateau) is consistent with Koopman search-theoretic predictions for mobile launcher survivability in complex terrain.

**Fig. 2.** Daily launch rate by C2 hypothesis (baseline window, 25-40 days). All three hypotheses produce overlapping curves (Mann-Whitney p > 0.05, rank-biserial r < 0.08 across all phases), showing that launch rate cannot discriminate C2 architecture when attrition exceeds 70% in week one.

**Fig. 3.** Emergent target ratio by C2 hypothesis. H1 (active C2) produces 5-9% emergent targeting in the early phase. H2 (pre-programmed) produces exactly zero. This is the sole reliable discriminator (rank-biserial r > 0.60, p < 0.001), though direct computation requires access to pre-war target packages not currently available from open sources. Proxy indicators are described in Section VI-C.
