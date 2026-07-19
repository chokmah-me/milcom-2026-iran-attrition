# v4 Paper Build Notes -- July 2026 Addendum

**Paper:** dyb-2026g-IranWar-Launcher-Agents_v4-2.md
**Zenodo version DOI:** 10.5281/zenodo.19558036
**Date of this note:** 2026-07-19
**Author:** Daniyel Yaacov Bilar, Chokmah LLC

---

## What happened

The April 8 ceasefire held through late April (extended indefinitely), then was formalized in a 14-point Memorandum of Understanding signed June 17 in Islamabad. The MOU ended the US naval blockade, reopened the Strait of Hormuz, and started a 60-day negotiation window. The Strait's status was the core sticking point: the MOU said Iran would use "its best efforts for safe passage" for 60 days, without ruling out future Iranian "service fees." Iran read this as continued sovereignty over the waterway; the US read it as a path to full reopening.

The MOU collapsed. On June 25, Iran launched a drone strike against a ship in the Strait. The US interpreted this as a violation and struck five Iranian targets. Iran retaliated against Ali Al Salem AB (Kuwait) and the US Fifth Fleet (Bahrain) on June 28 (already coded as B9 in Phase II Leg 2). A second tit-for-tat cycle followed immediately.

On July 7, Iran struck three commercial vessels in the Strait. CENTCOM responded with a major 80+ target strike package: anti-ship missile sites, coastal radar, air defense systems, and 60+ IRGC fast attack craft. The US rescinded Iran's oil sanction waiver. Trump declared the ceasefire "over" at the NATO summit on July 8 and notified Congress that "limited" military action had resumed. CENTCOM reimposed the naval blockade.

Since July 7, the conflict has returned to near-original-campaign intensity:
- Seven consecutive nights of US strikes on Iran (through July 17).
- IRGC multi-country retaliatory strikes against US assets in Kuwait, Bahrain, Qatar, Jordan, Oman, and Syria, framed as "Operation Nasr 2."
- Two US service members killed in Jordan on July 18, one missing. Total US KIA now 16.
- Iran's Health Ministry reports 35+ killed, 300+ injured since fighting resumed.
- 50,000+ US military personnel deployed in theater.
- CENTCOM strikes have expanded inland (Iranshahr, ~200km from coast) and hit maritime surveillance infrastructure (Chah Bahar port tower).

Sources: ABC News timeline (2026-07-09), CNN liveblog (2026-07-13, 2026-07-16, 2026-07-18), Al Jazeera (2026-07-16, 2026-07-17), CENTCOM official releases (2026-07-12, 2026-07-15), Stars and Stripes (2026-07-18), CBS News (2026-07-17), RFE/RL (2026-07-09), The National (2026-07-09, 2026-07-18), HSToday/Windward maritime assessment (2026-07-07).

## What this means for the v4 paper

### Nothing changes in the statistical findings

The v4 paper's simulation results (Tables II-V, Figures 1-5) are scoped to the Feb 28 - Apr 8 campaign window. The Monte Carlo runs, the Mann-Whitney tests, the attrition-masking null result, and the emergent target ratio discrimination all stand as published. The post-conflict re-simulation (Section V-D) was calibrated to ceasefire-day IC reporting and tested three attrition profiles against three magazine-discipline rules. None of this is affected by subsequent events.

### The framing needs a note

The paper's abstract says "A ceasefire took effect on April 8, 2026, ending major combat operations after 40 days." Section I says the same. Section VI-D treats the ceasefire as a terminal boundary. These statements were accurate at publication (v4.0, April 13; v4.2, April 15). They are now incomplete. The April 8 ceasefire did not end the war; it paused it. Major combat operations resumed on July 7, 2026.

**Recommendation:** Add a dated footnote to the next version (v4.3 or v5) at the first mention of the ceasefire:

> *Post-publication note (July 19, 2026): The April 8 ceasefire was formalized in a June 17 MOU but collapsed after Iranian strikes on commercial shipping in the Strait of Hormuz. Major combat operations resumed July 7, 2026. The paper's simulation results are scoped to the Feb 28 - Apr 8 window and are unaffected. See Phase II build notes for implications.*

Do NOT retroactively edit the body text. The paper was honest about its data cutoff at every version; a dated footnote preserves that discipline.

### One finding gains empirical weight

Section IV-C flagged the exogenous-attrition assumption as "less defensible for weeks four and five" due to US aircraft losses. The July events strengthen that flag considerably. CENTCOM's July strike packages are explicitly targeting Iran's ability to threaten shipping, i.e. the coalition is now fighting to restore ISR dominance it lost. The C2-ISR feedback loop the paper flagged as "empirically motivated, not just a theoretical hedge" is now the central operational dynamic of the resumed conflict. Endogenous modeling of this feedback is no longer future work for academic completeness; it is the binding question for any model of the current phase.

### One limitation sharpens

Section VI-C limitation (1) noted the model covers only MRBMs. The July fighting is overwhelmingly anti-ship missiles, coastal defense systems, fast attack craft, and drones. A different launcher population with different C2 signatures. The MRBM TEL-hunting model in c2_core.py does not cover this target set. Any extension to the current phase would need a separate model, not a parameter change.

---

## Action items

1. **v4.3 footnote:** Draft and add the post-publication note above. Do not change locked body text.
2. **Phase II implications:** Documented separately in phase2_build_notes_july2026.md.
3. **Leg 3 pre-registration:** Filed as leg3_preregistration_v0_1.md (locked before any July data is coded).
4. **No code changes to c2_core.py.** The current model does not cover the maritime/anti-ship domain. Any new simulation work is a separate effort.
