# Phase II Build Notes -- July 2026 Addendum

**Paper:** PHASE2_C2_Observability_DRAFT_v0-1.md
**Date of this note:** 2026-07-19
**Author:** Daniyel Yaacov Bilar, Chokmah LLC

---

## Context

Leg 2 (empirical coding) was locked with a June 28 cutoff. Stream B attribution correlation was 0.64 (n=7 construct-coded events, 3 clean 1s). Stream A control was ~0.0. Leg 1 (simulation) showed attribution correlation separates sharply (r = 0.93-1.00, p < 0.001) while launch rate does not, confirming the Phase II boundary-condition hypothesis: when attrition stops swamping the signal, adaptive targeting becomes observable through attribution correlation.

The low-attrition residual-force regime that defined Leg 2's empirical window ended on July 7, 2026.

## What happened (summary)

The June 17 MOU formalized the April 8 ceasefire, ended the US naval blockade, and reopened the Strait of Hormuz. The Strait's status was disputed from day one: Iran claimed continued sovereignty, the US demanded full reopening. The MOU collapsed through a series of escalating violations:

- June 25: Iran drone strike on ship in Strait (first MOU violation).
- June 25-28: Tit-for-tat exchange. Iran hits Kuwait/Bahrain (coded as B9/B9b in Leg 2, the last events in the locked window).
- July 7: Iran strikes three commercial vessels. US responds with 80+ target strike package (anti-ship missiles, coastal radar, AD, 60+ IRGC fast attack craft). US rescinds oil sanction waiver. Trump declares ceasefire "over."
- July 8-18: Seven consecutive nights of US strikes on Iran. IRGC multi-country retaliation ("Operation Nasr 2") hitting US assets in Kuwait, Bahrain, Qatar, Jordan, Oman, Syria. Two US troops killed in Jordan (July 18), total US KIA now 16. Iran Health Ministry: 35+ killed, 300+ injured since July 7.

Sources: see v4_build_notes_july2026.md for full citation list.

## Implications for Phase II

### Leg 2 findings are unaffected

The coding window (Apr 8 - Jun 28) and all construct values are locked. The three clean attribution_correlated=1 events (B5: May 7 destroyer exchange, B6: May 30 Ali Al Salem Fateh-110, B9: June 28 Kuwait/Bahrain response) stand as coded. The headline read (attribution correlation ~0.64, consistent with H1-like adaptive signature in low-attrition conditions) is a correct description of that window.

### The regime has changed

The Phase II paper's central claim is that attribution correlation becomes observable "when launch volume is small and attrition is not swamping the signal" (codebook Section 0). That condition held from April 8 through early July. It no longer holds. The July 7+ fighting is high-tempo, multi-target, multi-country, with explicit IRGC escalation ("Operation Nasr 2," "80 distinct strike packages"). This is closer to the v4 paper's acute-attrition regime than to the Phase II paper's low-attrition regime, though the target set is different (maritime/anti-ship vs. MRBM TELs).

The Phase II paper should note this regime change in its discussion section, framed as: "The low-attrition window the paper studies was bounded. The conditions that made attribution correlation observable were temporary."

### The July events are a natural out-of-sample test

This is the interesting part. The July 7-18 events include multiple cases that look like textbook attribution_correlated=1 candidates under the existing codebook:

**Base-rate warning before reading the candidate list.** The descriptions below make several events "look like 1 candidates." Treat that language with suspicion. Under near-daily US strikes, every Iranian action has an antecedent within 72 hours by construction, and IRGC framing is now attached to everything. The apparent strength of these candidates is partly an artifact of antecedent saturation. This is the central design issue of Leg 3 (pre-reg Section 4a), handled by evaluating the Stream B minus Stream A gap rather than raw rates.

**Candidate events (NOT YET CODED, flagged from news search only):**

1. **July 8, IRGC strikes on Ali Al Salem + Port Salman.** IRGC statement: "first phase of punitive response" to US July 7 strikes. Targets: the specific US bases that support Strait operations. Physical match + framing match. Latency: ~24h. Looks like a strong 1 candidate.

2. **July 9, IRGC drone attacks on Kuwait/Qatar/Bahrain.** Iran Army statement: targeted Patriot system in Kuwait, early warning in Qatar, fuel tanks in Bahrain "in retaliation for US strikes earlier the same day." Physical match is diffuse (host-state infrastructure, not the specific antecedent actor). Framing is explicit. Looks like 0.5-1 range depending on target specificity.

3. **July 9, IRGC fires ~10 BMs at Azraq/Jordan.** IRGC: "second phase of retaliation." Jordan intercepts 8. Latency: ~24h from July 8 US strikes. Physical match: Azraq hosts US forces. Framing: explicit. Looks like a 1 candidate.

4. **July 12, broadest single-night IRGC attack.** BMs + drones at Qatar, Kuwait, Bahrain, Jordan, Oman, plus commercial ship. IRGC framing: explicit attrition campaign. Multiple antecedent US strikes. This is a multi-target salvo; under codebook Section 1, each named target is a separate event.

5. **July 13, IRGC claims strike on al-Tanf, Syria.** Stated as retaliation for US strikes in Iranshahr. Physical match: al-Tanf is a US base. Complication: US says it vacated al-Tanf in February. If the base is empty, the physical match is questionable. Needs verification.

6. **July 15, IRGC claims strikes on US bases in Kuwait, Jordan, Bahrain.** After CENTCOM strikes on Greater Tunb Island coastal defense. Explicit retaliation framing.

7. **July 18, Iranian BM/drone attack kills 2 US troops in Jordan.** CENTCOM confirms. Part of seventh consecutive night of exchanges. IRGC framing not yet available at time of this note.

**The test question:** Does the Stream B minus Stream A attribution-correlation gap (0.64 in Leg 2) survive the return to high-tempo operations, or does it collapse toward zero once the inflation floor measured by Stream A is subtracted?

If it persists: the adaptive C2 signature is strong enough to show through even under resumed high-tempo conditions. This would modify the v4 paper's attrition-masking hypothesis, suggesting that once an adversary has shifted to an adaptive mode, the attrition mask has a ceiling, not total coverage.

If it collapses: the v4 paper's boundary condition is confirmed. Attribution correlation was observable only because the low-attrition window created space for it.

Either result is informative. Neither invalidates Phase II's locked findings. But the test needs to be pre-registered before any coding happens. See leg3_preregistration_v0_1.md.

### Simulation gap

The c2_core.py model covers land-based MRBM TEL cells with five operational regions inside Iran. The July fighting is primarily maritime: anti-ship missile sites, coastal radar networks, fast attack craft, and Strait-control infrastructure. A different launcher population, different C2 architecture (coastal defense is likely more centralized than dispersed MRBM cells), different attrition dynamics (the US is hunting fixed coastal installations, not mobile TELs). The Koopman search-theoretic framework that grounded the v4 model's attrition plateau does not apply the same way to fixed coastal sites.

Leg 1's simulation cannot be extended to the July regime without a separate model. Leg 3 is therefore empirical-only, with qualitative predictions from the existing simulation stated in the pre-reg. If a Leg 3 simulation is warranted, it is a separate effort requiring its own model design.

### One new data point for the paper's argument

The July events provide a data point the Phase II paper's discussion section should note (without coding, since it's outside the locked window): the IRGC's attribution framing has become more explicit and more systematic over time. "Operation Nasr 2" is a named retaliatory operation with numbered strike phases. Compare this to the May-June events, where framing was present but less formalized. If the IRGC is deliberately performing attribution for propaganda purposes, that is a threat to validity the codebook flagged (Section 8, item 2: "attribution laundering"). The July events may help calibrate how much weight to put on that threat.

---

## Action items

1. **Add regime-change note to Phase II draft discussion section.** One paragraph, post-Leg-2 framing.
2. **Lock Leg 3 pre-registration** (leg3_preregistration_v0_1.md) before any July data is coded.
3. **Do not retroactively edit Leg 2 coding tables.** The June 28 cutoff stands.
4. **Do not extend c2_core.py to the maritime domain.** Separate model if needed.
