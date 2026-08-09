# Leg 3 Coding Tables — v0.2 (post-author-review)
# Window: July 7 – August 6, 2026 (pre-reg locked, DOI stamped)
# Codebook: Phase II codebook v0.1, applied without modification
# Protocol: stream and provocation_antecedent coded before attribution_correlated

---

## COALITION-ACTION DATEBOOK (antecedent reference for Stream B coding)

Every dated US/coalition strike on Iran, July 7 – Aug 6. Used to populate provocation_antecedent fields.

| day | date | US action | targets | source |
|-----|------|-----------|---------|--------|
| 1 | 2026-07-07 | 80+ target strike package | anti-ship missile sites, coastal radar, AD, 60+ IRGC fast attack craft | CENTCOM release; ABC News |
| 2 | 2026-07-08 | Night 2 strikes | continued coastal/maritime targets | CENTCOM; CNN |
| 3 | 2026-07-09 | Night 3 | Hormuz coastline targets | CENTCOM; The National |
| 4 | 2026-07-10 | Night 4 | continued | CENTCOM |
| 5 | 2026-07-11 | Night 5 ("third round this week") | commercial shipping response | CENTCOM release |
| 6 | 2026-07-12 | Night 6 (one-way attack sea drones, first use) | dozens of targets, multiple locations | CENTCOM release; Al Jazeera |
| 7 | 2026-07-13 | Night 7 | continued | CENTCOM |
| 8 | 2026-07-14 | Night 8 | continued | CENTCOM |
| 9 | 2026-07-15 | Night 9 | Greater Tunb Island coastal defense | CENTCOM; CBS |
| 10 | 2026-07-16 | Night 10 (inland expansion) | Chah Bahar port surveillance tower, Iranshahr (~200km inland), targets around Tehran, Semnan | CENTCOM; Euronews; Al Jazeera |
| 11 | 2026-07-17 | Night 11 | continued | CENTCOM |
| 12 | 2026-07-18 | Night 12 (8th consecutive per CENTCOM numbering) | at Commander in Chief's direction | CENTCOM release |
| 13 | 2026-07-19 | Night 13 (9th consecutive) | Darkhovin nuclear plant struck, Hormozgan/Khuzestan provinces; "punish" IRGC for Jordan KIAs | CENTCOM release; Al Jazeera; AEOI |
| 14 | 2026-07-20 | Night 14 | continued | CENTCOM release |
| 15 | 2026-07-21 | Night 15 | continued | CENTCOM |
| 16 | 2026-07-22 | Night 16 (12th consecutive) | continued | CENTCOM release |
| 17 | 2026-07-23 | Night 17 (13th consecutive) | military command centers, drone storage, communications | CENTCOM release; MilitarySpot |
| — | 2026-07-24 to 07-27 | Reduced/paused (not confirmed, no CENTCOM release found) | — | gap in CENTCOM releases |
| 18 | 2026-07-29 | "Heavy wave" | IRGC targets, response to July 28 Iranian attacks on US forces | CENTCOM release |
| 19 | 2026-07-30 | Continued | southern Iran military sites, Khuzestan/Hormozgan/Fars/Bushehr | CTP July 30 report |
| — | 2026-07-31 | Unclear if strikes occurred | — | no CENTCOM release found |
| — | 2026-08-01 | Trump cancels planned major campaign | cancelled late Aug 1 after Gulf state request | CNN; CBS |
| — | 2026-08-02 to 08-06 | NO STRIKES (six consecutive nights) | — | GlobalSecurity OPREP Day 159 |

**Summary:** 17-19 confirmed US strike nights in the 31-day window (July 7-Aug 6). Effectively nightly through July 23, brief gap July 24-28, one heavy wave July 29-30, then lull Aug 1-6. The 72-hour antecedent window is open for every Iranian strike from July 7 through roughly Aug 2 (72h after last confirmed July 30 strike).

---

## STREAM B — Coalition / Gulf-state targets (PRIMARY)

Coding protocol followed per codebook sec.7: stream and provocation_antecedent coded first. Each distinct named target in a 24-hour salvo is one event per codebook sec.1.

| id | date | iran_target | target_class | munition | provocation_antecedent | antecedent_date | latency_h | iran_framing | attrib | outcome | antecedent_unattributable | coder_note |
|----|------|-------------|--------------|----------|------------------------|-----------------|-----------|--------------|--------|---------|--------------------------|------------|
| L3-B1a | 2026-07-08 | Ali Al Salem AB, Kuwait | us_base | BM+drone | US July 7 80+ target strike | 2026-07-07 | ~24 | IRGC: "first phase of punitive response" (IRNA) | 1 | partial | no (Ali Al Salem hosts coalition forces that operate in Strait) | IRGC explicitly links to July 7 strikes. Target is a named US basing asset. Physical match: Ali Al Salem supports Strait ops. 3+ sources (CENTCOM, Al Jazeera, JNS, IranWire). |
| L3-B1b | 2026-07-08 | Port Salman / US Fifth Fleet, Bahrain | us_base | BM+drone | US July 7 strikes | 2026-07-07 | ~24 | IRGC: same "first phase" statement | 1 | partial | no (5th Fleet is identifiable actor) | Same salvo as B1a. 5th Fleet is the specific naval command conducting Strait ops. Physical+framing match. |
| L3-B2a | 2026-07-09 | Kuwait (Patriot AD system) | us_base | drone | US July 8 strikes | 2026-07-08 | ~24 | Iranian Army: "continuation of operations against US bases, retaliation for strikes" (state TV) | 0.5 | intercepted | yes (antecedent = carrier/standoff, not the Patriot battery) | Target is AD asset, not the antecedent actor. Framing explicit but generic "US bases." Ceiling 0.5 per antecedent_unattributable. |
| L3-B2b | 2026-07-09 | Qatar (early warning site) | gulf_state_terr | drone | US July 8 strikes | 2026-07-08 | ~24 | Iranian Army: same statement | 0.5 | unknown | yes | Qatar hosts US forces but is not the antecedent actor. Generic framing. |
| L3-B2c | 2026-07-09 | Bahrain (fuel storage, US forces) | us_base | drone | US July 8 strikes | 2026-07-08 | ~24 | Iranian Army: same statement | 0.5 | partial | yes | Host-state target, not the specific antecedent platform. |
| L3-B2d | 2026-07-09 | Azraq AB, Jordan | us_base | ~10 BM | US July 8 strikes | 2026-07-08 | ~24 | IRGC: "second phase of retaliation" (The National) | 1 | intercepted (Jordan shot down 8) | no (Azraq hosts US strike aircraft that fly Iran missions) | IRGC explicitly names this "second phase." Azraq hosts F-15s/F-16s used in strikes. Physical match: the base's aircraft plausibly flew July 8 sorties. 3+ sources (The National, Jordan military, IRGC via IRNA). |
| L3-B3a | 2026-07-12 | Bahrain (Sheikh Isa AB + Juffair) | us_base | BM+drone | US July 11-12 strikes | 2026-07-11 | ~24 | IRGC: "latest phase of retaliation" targeting "installations and infrastructure of the aggressive US army" (Sepah News) | 0.5 | intercepted | yes (antecedent = carrier/standoff) | Broad target set, explicit framing, but physical match is to host basing, not specific antecedent platform. |
| L3-B3b | 2026-07-12 | Kuwait (HIMARS base) | us_base | mixed | US July 11-12 | 2026-07-11 | ~24 | IRGC: claimed "setting fire to two HIMARS launchers" (Al Jazeera) | 0.5 | claimed damage | yes | HIMARS is a US weapons system, but not the platform that struck Iran. |
| L3-B3c | 2026-07-12 | Jordan (Prince Hassan AB) | us_base | BM+drone | US July 11-12 | 2026-07-11 | ~24 | IRGC: targeted with missiles and drones, claimed fuel depot fires (Al Jazeera) | 0.5 | partial (Jordan intercepted 4 missiles) | partial (Prince Hassan hosts US forces, may host strike aircraft) | Similar to B2d but weaker physical match (Prince Hassan less clearly the origin of antecedent strikes than Azraq). |
| L3-B3d | 2026-07-12 | Oman (FPS radar + vessel detection radar) | gulf_state_terr | mixed | US July 11-12 | 2026-07-11 | ~24 | IRGC: claimed "destroyed" (Al Jazeera) | 0 | claimed destroyed | yes | Oman is not conducting strikes on Iran. This is a deterrence/denial target, not retaliation for a specific action. IRGC framing is generic. |
| L3-B3e | 2026-07-12 | commercial ship (Strait) | shipping | unknown | US naval ops | — | — | none specific | 0 | unknown | n/a | Part of broader Strait enforcement/disruption. No specific antecedent named. |
| L3-B4a | 2026-07-16 | Isa AB, Bahrain (radar + fuel pumping) | us_base | BM+drone | US July 15 Greater Tunb / July 16 Tehran-area strikes | 2026-07-15 | ~24 | IRGC: destroyed radar and fuel infrastructure "in response to US crimes" (IRNA via JNS) | 0.5 | claimed destroyed | yes | Framing explicit but generic ("US crimes"). Not tied to a specific antecedent base. |
| L3-B4b | 2026-07-16 | Azraq AB, Jordan (C2 center + F-35 hangar) | us_base | BM | US July 15-16 | 2026-07-15 | ~24 | IRGC: response to "American attack near a children's cancer hospital in Iran" (Euronews) | 0.5 | claimed damage | no (Azraq hosts strike aircraft) | DOWNGRADED (v0.2, author review): framing names an antecedent action but is emotive/propaganda-adjacent ("children's cancer hospital"), not a precise operational linkage. Physical match present (Azraq hosts strike aircraft). Azraq saturation flag applies. Ceiling 0.5. |
| L3-B5 | 2026-07-18 | Jordan (kills 2 US troops) | us_base | BM+drone | US July 17-18 strikes | 2026-07-17 | ~24 | IRGC framing not found in searched sources for this specific event | 0.5 | hit (2 KIA) | partial | Deadliest single event in window. No specific IRGC attribution statement found in my sources. Physical match (Jordan base hosting US forces), but without framing, ceiling 0.5. |
| L3-B6a | 2026-07-19 | Kuwait (Camp al-Adiri ammo depot + Ali Al Salem AD radars) | us_base | mixed | US July 18-19 (Darkhovin + Hormozgan/Khuzestan) | 2026-07-18 | ~24 | IRGC: "heavy blows" to US bases; Army: targeted "Camp al-Adiri" and "Ali Al Salem AD radars" (Al Jazeera) | 0.5 | partial | yes (Darkhovin struck from standoff) | IRGC framing generic ("heavy blows"). Named targets but not tied to specific antecedent platform. |
| L3-B6b | 2026-07-19 | Kuwait (power/water plant) | gulf_infra | mixed | US July 18-19 | 2026-07-18 | ~24 | IRGC general retaliation framing | 0 | hit (fire) | n/a | Civilian infrastructure. Not a US military target. IRGC framing does not link to specific antecedent. Host-state pressure target. |
| L3-B6c | 2026-07-19 | Jordan (shot down 3 of 4 missiles) | us_base | BM | US July 18-19 (punish IRGC for Jordan KIAs) | 2026-07-18 | ~24 | part of same IRGC "heavy blows" statement | 0.5 | intercepted | partial | CENTCOM framed July 19 strikes as "punishing" IRGC for Jordan KIAs, creating a clean retaliatory chain. But the IRGC framing is generic. |
| L3-B7a | 2026-07-21 | Bahrain (Muharraq + Riffa, AD/radar) | us_base | drone | US July 20 strikes | 2026-07-20 | ~24 | IRGC: "Operation Nasr 24" (IranWire) | 0.5 | partial | yes | Named operation but targets are host-state AD, not antecedent actor. |
| L3-B7b | 2026-07-21 | Jordan (Azraq AB, missile defense radar + "F-15 destroyed") | us_base | BM | US July 20 | 2026-07-20 | ~24 | IRGC: Nasr 24 continues | 1 | claimed (Jordan/US deny) | no (Azraq hosts strike aircraft) | Azraq repeatedly targeted and repeatedly linked to IRGC retaliatory framing. F-15s at Azraq fly Iran missions. Physical match + named operation. 3+ sources (IranWire, Xinhua, Iran International). |
| L3-B7c | 2026-07-21 | Kuwait (Ahmad al-Jaber + Ali Al Salem) | us_base | mixed | US July 20 | 2026-07-20 | ~24 | IRGC+Army: targeted "early-warning radar, Patriot, PFS-117" (Xinhua) | 0.5 | partial | yes | Detailed target list but not tied to specific antecedent platform. |
| ~~L3-B7d~~ | ~~2026-07-21~~ | ~~Bahrain (Amazon data center)~~ | ~~gulf_infra~~ | ~~CM~~ | — | — | — | — | EXCLUDED | — | — | EXCLUDED (v0.2, author review): non-military commercial target. Removed from construct. Logged for completeness only. |
| L3-B7e | 2026-07-21 | Erbil (Patriot + espionage balloon) | us_base | mixed | US July 20 | 2026-07-20 | ~24 | IRGC: "surprise operations" (Xinhua) | 0 | claimed | yes | KRI target, not linked to specific antecedent. Distinct from Stream A (this is US military assets in Erbil, not Kurdish opposition camps). |
| L3-B8a | 2026-07-24 | Kuwait (Ali Al Salem, ammo depot) | us_base | drone ("advanced ultra-heavy kamikaze") | US July 23 (13th consecutive) | 2026-07-23 | ~24 | IRGC: "in response to US crimes" (Xinhua/Tasnim) | 0.5 | claimed | yes | Generic framing, not tied to specific antecedent. |
| L3-B8b | 2026-07-24 | Jordan (Azraq AB, "crushing attack") | us_base | BM | US July 23 | 2026-07-23 | ~24 | IRGC: "crushing attack" causing "significant damage to fighter aircraft" (Xinhua) | 0.5 | claimed (US/Jordan deny) | no (Azraq hosts strike aircraft) | Physical match present but framing not tied to specific antecedent action. |
| L3-B8c | 2026-07-24 | Bahrain (continued) | us_base | mixed | US July 23 | 2026-07-23 | ~24 | IRGC: confirmed strikes (Iran International) | 0.5 | unknown | yes | Confirmed by Iran International, IRGC, and Bahrain MoI. Generic framing. |
| L3-B9 | 2026-07-28 | US forces (location unclear) | us_base | BM+drone | US July 24-27 activity (reduced) | 2026-07-27? | unclear | not found in searched sources | 0 | "attempted" per CENTCOM | unknown | Known only from CENTCOM July 29 release referencing "yesterday's attempted missile attacks on US forces." No IRGC statement found. Antecedent unclear (US strikes may have paused July 24-27). |
| L3-B10a | 2026-07-30 | Jordan (Muwaffaq Salti AB) | us_base | BM | US July 29 "heavy wave" | 2026-07-29 | ~24 | IRGC: claimed attack to help Jordanian people "liberate" from "American occupiers"; also framed as response to US strikes (CTP July 30) | 1 | unknown | no (Muwaffaq Salti hosts US drones/aircraft) | UPGRADED (v0.2, author review): Muwaffaq Salti hosts US strike aircraft and drones conducting Iran sorties. Physical match to antecedent. IRGC framing is political in tone but explicitly retaliatory in substance ("in response to" US strikes per CTP analysis). Latency ~24h. Azraq-adjacent flag: Jordan basing repeatedly targeted. 3+ sources (CTP, Al Jazeera, JPost). |
| L3-B10b | 2026-07-30 | Kuwait (Ahmad Al-Jaber AB) | us_base | drone | US July 29 | 2026-07-29 | ~24 | Iranian Army: "retaliation for recent US strikes" (Tasnim via Al Jazeera) | 0.5 | partial | yes | Generic "recent US strikes" framing. Not the specific antecedent platform. |
| L3-B11a | 2026-07-31 | Kuwait (Ali Al Salem, ammo + comms) | us_base | drone | US July 29-30 | 2026-07-29 | ~48 | Iranian Army via IRIB: targeted "ammunition stores and communication assets" | 0.5 | claimed | yes | Generic framing. |
| L3-B11b | 2026-07-31 | Jordan (Muwaffaq Salti AB) | us_base | drone | US July 29-30 | 2026-07-29 | ~48 | Army via IRIB: targeted "US military assets" | 0.5 | claimed | yes | Generic framing, not tied to specific strike. |
| L3-B11c | 2026-07-31 | Bahrain (Sheikh Isa AB, hangars+fuel+comms) | us_base | drone | US July 29-30 | 2026-07-29 | ~48 | Army via IRIB (JPost) | 0.5 | claimed | yes | Same pattern: named targets, generic framing. |
| L3-B12 | 2026-08-01 | Kuwait (dawn drone wave) | us_base | drone | US July 29-30 (last confirmed strikes) | 2026-07-29 | ~72 | not found | 0 | intercepted | unknown | Last Iranian attack before lull. No IRGC statement found in sources. At edge of 72h window. |
| — | 2026-08-02 to 08-06 | NO IRANIAN ATTACKS | — | — | — | — | — | — | — | — | Six consecutive nights at zero per GlobalSecurity OPREP. |

**Stream B count (v0.2):** 26 construct-coded events (L3-B1a through L3-B12, excluding B7d per author review).
- attribution_correlated = 1: L3-B1a, L3-B1b, L3-B2d, L3-B7b, L3-B10a = **5 events**
- attribution_correlated = 0.5: L3-B2a, B2b, B2c, B3a, B3b, B3c, B4a, B4b, B5, B6a, B6c, B7a, B7c, B8a, B8b, B8c, B10b, B11a, B11b, B11c = **20 events**
- attribution_correlated = 0: L3-B3d, B3e, B6b, B7e, B9, B12 = **6 events**

**Stream B raw attribution correlation rate** = (5 x 1 + 20 x 0.5 + 6 x 0) / 26 = 15/26 = **0.577**

**antecedent_unattributable ceiling count:** 15 of 26 events flagged (57.7%). Majority of Stream B events are ceiling-limited because Iran cannot identify or reach the carrier/standoff platforms that delivered the antecedent strikes. This triggers the falsification table row: "More than half of Stream B events flagged antecedent_unattributable: deflation dominates."

**v0.2 changes from v0.1:**
- B4b downgraded 1 to 0.5 (propaganda-adjacent framing, not precise operational linkage)
- B7d excluded (non-military commercial target, Amazon data center)
- B10a upgraded 0.5 to 1 (Muwaffaq Salti hosts US strike aircraft; framing retaliatory in substance despite political tone)
- B5 held at 0.5 pending IRGC framing verification
- Net effect on rate: 0.556 to 0.577 (still inside null band 0.55-0.72)

---

## STREAM A — Kurdish opposition targets (CONTROL)

Coded at representative resolution per Leg 2 practice. Sources: Washington Kurdish Institute July 2026 digest, FDD, KHRN, Hengaw, JPost.

| id | date | iran_target | target_class | munition | antecedent | antecedent_date | iran_framing | attrib | coder_note |
|----|------|-------------|--------------|----------|------------|-----------------|--------------|--------|------------|
| L3-A1 | 2026-07-02 | PDKI, Piranshahr (Qazqapan area) | opposition_camp | ground clash | none (standing target) | — | none attributable; PDKI announced, Iran silent | 0 | Ground clash, not airstrike. Included for completeness. 6 PDKI killed. |
| L3-A2 | 2026-07-13 | PAK camps | opposition_camp | 3 drones | none (standing target) | — | Press TV July 15: "separatist" framing (standing counter-opposition) | 0 | Fixed target, years-long pattern. Iran does NOT link to any US action despite nightly US strikes ongoing. |
| L3-A3 | 2026-07-17 | Komala (Zargwezila camp, Sulaymaniyah) | opposition_camp | missile | none (standing target) | — | UNCLAIMED. Iran did not claim responsibility. Komala confirmed, KHRN confirmed. | 0 | Deadliest single Kurdish strike in window (9 killed, 3 wounded). US struck Iran on July 14, 15, 16, 17. 72h window SATURATED with antecedents. Iran STILL did not claim or frame as retaliation. This is the framing-asymmetry finding in action. |
| L3-A4 | 2026-07-20 | Komala HQ (Alana Valley, Erbil/Choman) + Surdash camp | opposition_camp | missile + drone | none (standing target) | — | none attributable; attacked day after burying July 17 dead | 0 | Two separate locations struck in one night. Iran silent. US struck Iran July 19-20. Antecedents available. Iran does not use them. |
| L3-A5 | ~2026-07-20 | PAK camps | opposition_camp | drone | none | — | PAK alleges white phosphorus (JPost). Iran silent. | 0 | Unverified WP allegation. Iran makes no statement. |

**Stream A raw attribution correlation rate** = 0/5 = **0.0**

**Framing asymmetry finding:** In the July 7-Aug 6 window, the US struck Iran on at least 17 nights. Every Stream A event falls within 72 hours of at least one US strike. Yet Iran claimed ZERO Kurdish strikes as retaliation and made no framing statements linking them to US actions. The asymmetry is total: Iran frames every Gulf strike (Stream B) as retaliation while leaving every Kurdish strike (Stream A) unclaimed. This is the pre-reg Section 4a item (4) finding.

**Implication for the gap construction:** Because framing is withheld from Stream A entirely, Stream A cannot measure the framing inflation that inflates Stream B. The B-minus-A gap equals the raw B rate (0.577 - 0.0 = 0.577). The gap construction does not control for the confound as designed. The null band comparison (pre-reg Section 4a item 3) is the binding control: raw Stream B rate 0.577 falls INSIDE the simulated null band of 0.55-0.72. H_ceiling is the result.

---

## CONSTRUCT COMPUTATION (v0.2, post-author-review)

### Raw rates
- Stream B attribution correlation: **0.577** (26 events; B7d excluded)
- Stream A attribution correlation: **0.0** (5 events)
- B minus A gap: **0.577**

### v0.2 changes from v0.1
- B4b downgraded 1 to 0.5 (propaganda-adjacent framing, not precise operational linkage)
- B7d excluded (non-military commercial target, Amazon data center)
- B10a upgraded 0.5 to 1 (Muwaffaq Salti hosts US strike aircraft; framing retaliatory in substance)
- B5 held at 0.5 pending IRGC framing verification
- Net effect on rate: 0.556 to 0.577 (still inside null band 0.55-0.72)

### Against pre-registered hypotheses

**Primary metric: strict-novelty rate.**

Pre-war IRGC target packages (v4 simulation): Ali Al Salem, Arifjan, Al Udeid, Juffair, Muharraq, Incirlik, Dhahran, UAE bases, Nevatim, Ramon, Dimona, Tel Nof, Haifa, Diego Garcia, Shaybah.

Targets in Leg 3 NOT on that list: Azraq AB, Muwaffaq Salti AB, Prince Hassan AB (all Jordan), Ahmad Al-Jaber AB (Kuwait), Oman radar sites, Kuwait power/water plant. Jordan is the strongest novelty case: no pre-war IRGC targeting of Jordan is documented in OSINT.

Events hitting novel targets: ~12 of 26 = **~0.46**. Exceeds H_persist threshold of 0.10.

**This number is unreliable and the paper does not claim H_persist on this basis.** The v4 simulation models 14 pre-war targets; the real IRGC database is unknown. "Not in the documented list" may reflect documentation gaps. Report as suggestive only.

### Pre-registered assessment table

| Test | Value | Threshold | Result |
|------|-------|-----------|--------|
| Raw Stream B rate | 0.577 | 0.55-0.72 null band | INSIDE null band |
| Raw Stream B rate vs upper bound | 0.577 | > 0.72 | NOT exceeded |
| B minus A gap | 0.577 | -- | Equals raw B (framing asymmetry total) |
| Strict-novelty rate | ~0.46 (LOW CONFIDENCE) | >= 0.10 for H_persist | Exceeds IF trusted; not claimed |
| Stream A raw rate | 0.0 | > 0.40 for construct failure | NOT triggered |
| antecedent_unattributable | 15/26 = 58% | > 50% for deflation flag | TRIGGERED |

### Azraq / Jordan robustness check

Azraq AB appears in 4 events: B2d (1), B4b (0.5), B7b (1), B8b (0.5). Three of five 1s depend on Jordan basing (B2d and B7b at Azraq, B10a at Muwaffaq Salti). If a reviewer argues repeated targeting of the same base is a standing pattern rather than adaptive retargeting, the 1s thin out.

**Without Azraq events (22 events):**
- 1s: B1a, B1b, B10a = 3
- 0.5s: 16 events
- 0s: 3 events
- Rate = (3 + 8) / 22 = **0.500** (below null band lower bound of 0.55)

**Without ALL Jordan events (removed: B2d, B3c, B4b, B5, B6c, B7b, B8b, B10a, B11b = 9 events; remaining = 17):**
- 1s: B1a, B1b = 2
- 0.5s: 12 events
- 0s: 3 events
- Rate = (2 + 6) / 17 = **0.471** (below null band)

**Interpretation:** the finding is Jordan-sensitive. Without Jordan basing, the rate drops below the null band, which would push toward H_collapse. This is a structural feature of the July war: Jordan absorbed the bulk of IRGC retaliatory fire because its bases (Azraq, Muwaffaq Salti) host the US strike aircraft conducting Iran sorties and are within IRGC missile range. The geographic concentration is consistent with adaptive selection of the most accessible antecedent platforms, but it also means the finding's base is narrow. Report transparently.

### Headline result (v0.2)

**H_ceiling confirmed on the raw construct.** Stream B rate (0.577) is inside the pre-registered null band. A pre-programmed force scores this by coincidence under daily provocation. The construct cannot discriminate H1 from H2 in the dense-provocation regime.

**The framing asymmetry is the cleanest finding.** Iran claims all Gulf strikes as retaliation and claims zero Kurdish strikes as retaliation, even when identical 72-hour antecedents are available. This asymmetry is total and selective.

**Strict-novelty is suggestive but not dispositive.** The rate (~0.46) exceeds H_persist but the metric is low-confidence. The paper does not claim H_persist.

**The signal is Jordan-concentrated.** Removing Jordan events drops the rate below the null band. IRGC retaliatory targeting in July was geographically focused on the US strike platforms it could reach. Consistent with adaptive selection, but a narrow base.

### Latency (the five 1s)
L3-B1a: ~24h, L3-B1b: ~24h, L3-B2d: ~24h, L3-B7b: ~24h, L3-B10a: ~24h
Median: ~24h. Identical to Leg 2.

---

## REMAINING OPEN DECISION (v0.2)

**L3-B5 (July 18, 2 US KIA): held at 0.5 pending IRGC framing verification.** Check Press TV / IRNA / Sepah News archives for July 18-19. If IRGC claimed it as retaliation for a specific strike, upgrade to 1 (deadliest event in window, physical match to Jordan basing present). If no framing found after primary-source check, lock at 0.5.
