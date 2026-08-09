# Leg 2 Retro-Audit: Coalition-Action Datebook and Coincidence Probability
Date: 2026-08-07

## Purpose
Per the leverage-map recommendation: check whether Leg 2's three clean 1s (B5, B6, B9) sat inside dense local provocation clusters. Compute the 72-hour coincidence probability for each.

## Coalition-action datebook, April 8 – June 28, 2026

Sources: Wikipedia (2026 Strait of Hormuz crisis, 7 May 2026 strikes), OAN, ABC News MOU-collapse timeline, Al Jazeera.

| date | US/coalition action | target | source |
|------|---------------------|--------|--------|
| 2026-04-12 | US naval blockade declared (Strait of Hormuz) | shipping enforcement, no kinetic strike | multiple |
| 2026-05-04 | US disables Gambia-flagged Lian Star tanker (Hellfire, disabling fire) | tanker departing Bandar Abbas | Wikipedia (Hormuz crisis) |
| 2026-05-07 | US strikes on southern Iran and Tehran | military sites, response to Iranian targeting of USS Truxtun/Peralta/Mason | Wikipedia (7 May 2026 strikes); B5 antecedent = the destroyer transit itself |
| 2026-05-27 | US strike on Iranian site "threatening forces in strait" | unclear target, southern Iran | Bloomberg via coding table B6 |
| 2026-06-02 | US Hellfire disables tanker to Kharg Island | tanker, naval enforcement | coding table B7 (coalition action) |
| 2026-06-07 | IDF strikes southern Beirut | Lebanon, not Iran directly | Britannica |
| 2026-06-25 | Iran drone strike on ship in Strait (first MOU violation); US retaliatory strikes on 5 Iranian targets | missile/drone storage, coastal radar, Sirik area | OAN; ABC timeline |
| 2026-06-26 | CENTCOM strikes on Iranian military targets | infrastructure linked to missile/drone capabilities, Qeshm Island, southern coastline | Wikipedia (Hormuz crisis); CENTCOM |
| 2026-06-27 | US strikes on Iranian ISR/comms/AD/drone/minelayer sites | multiple sites near Strait | coding table B9 antecedent |

**Total discrete coalition kinetic actions in the 82-day window: ~8** (excluding the blockade declaration and the Beirut strike which is Israel/Lebanon, not Iran). That is roughly one action per 10 days. The 72-hour window covers 3 days. At one action per 10 days, the probability of a random 72-hour window containing at least one antecedent is roughly 3/10 = 0.30.

## Coincidence analysis for the three clean 1s

### B5 (May 7, destroyers)
**Antecedent:** The three destroyers (Truxtun, Peralta, Mason) transiting the Strait ARE the target. Iran frames as "reciprocal action."

- 72h window before May 7: May 4-7.
- Coalition actions in window: May 4 (Lian Star disable) and May 7 (US strikes on Iran, which are themselves the response to B5).
- **This is a degenerate case.** The provocation and the target are identical (the transiting force). The May 4 Lian Star action is a separate event 3 days prior. The May 7 strikes are concurrent/reactive to B5, not antecedent to it.
- **Coincidence probability: not applicable.** B5 is not a retargeting event; it's a direct engagement of a transiting force. The physical match is identity, not selection. B5's coding as 1 is robust against the saturation critique because there is nothing to coincidentally match; the provocation IS the target.

### B6 (May 30, Ali Al Salem Fateh-110)
**Antecedent:** US strike on Iranian site "threatening forces in strait" on May 27. Iran: "targeted the base responsible for the previous day's attack."

- 72h window before May 30: May 27-30.
- Coalition actions in window: May 27 (US strike on Iranian site).
- **ONE action in the window.** No other coalition kinetic action in the datebook between May 4 and May 27 (23-day gap). The provocation environment is sparse.
- Number of candidate antecedent origin bases: 1 (the strike on May 27 came from a specific platform/base; Iran identifies Ali Al Salem as "the base responsible").
- Number of possible Iranian targets: ~8-10 US-linked bases in theater.
- Coincidence probability (chance that Iran hits the specific antecedent base out of ~8-10 options): ~0.10-0.125.
- **Combined probability (antecedent exists AND hits correct base by chance):** One action in a 23-day sparse period, then chance match = effectively low. B6's coding as 1 is the strongest in the dataset. The reviewer attack surface is small.

### B9 (June 28, Ali Al Salem + Bahrain)
**Antecedent:** US strikes June 27 on Iranian ISR/comms/AD/drone/minelayer sites.

- 72h window before June 28: June 25-28.
- Coalition actions in window: June 25 (US strikes on 5 Iranian targets after drone-on-ship), June 26 (CENTCOM strikes on Qeshm Island/southern coast), June 27 (US strikes on ISR/comms/AD).
- **THREE actions in the window.** This is the most exposed of the three 1s. The June 25-27 period was a tit-for-tat exchange (Iran hit ship, US hit Iran, Iran hit another ship, US hit Iran again). The provocation environment is locally dense.
- Number of candidate antecedent origin bases: at least 2-3 (carrier + possibly Ali Al Salem or Bahrain-based assets).
- Coincidence probability: with 3 antecedents over 3 days, the window is saturated. The chance-match probability for hitting Ali Al Salem specifically is still ~0.10-0.125 if random, but the existence of an antecedent within 72h is certain (probability 1.0).
- **B9 is partially exposed to the saturation critique.** The coding as 1 rests entirely on the specificity of Iran's framing ("response to US strikes that violated ceasefire") and the physical match (Ali Al Salem hosts forces conducting the June 27 strikes). The framing is strong, but a reviewer could argue that with three antecedents in 72 hours, the match is less informative than B6's single-antecedent case.

## Summary

| Event | Antecedents in 72h window | Local provocation density | Coincidence probability | Coding robustness |
|-------|--------------------------|--------------------------|------------------------|-------------------|
| B5 | 1 (degenerate: target=provocation) | sparse (1 other in window) | n/a (identity, not selection) | Strong |
| B6 | 1 | very sparse (23-day gap before) | ~0.10-0.125 | Strongest |
| B9 | 3 | locally dense (tit-for-tat cluster) | ~0.30 for antecedent existence; ~0.10-0.125 for specific-base match | Partially exposed |

## Recommendation

B6 carries the most evidential weight. B5 is structurally different (identity match, not selection). B9 is the weakest of the three but still holds: the physical-match specificity (Iran named "the base responsible") and the framing specificity reduce the coincidence explanation, even in a locally dense antecedent environment.

The Phase II paper should note B9's exposure in a sentence: "B9 occurs in a locally dense provocation cluster (three coalition actions in 72 hours), making its physical match less informative than B6's (one action in 23 days). The coding rests on Iran's specific framing rather than the temporal match alone."

No re-coding recommended. All three 1s survive the audit. B6 is the spine. B9 is the weakest link but holds.
