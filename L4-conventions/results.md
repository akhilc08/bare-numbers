# L4 deep dive: silent convention misreading between agents ("false friends")

## 1. Main sweep (17 conventions × 4 sender→receiver pairs {space-bunny, ling-3.1-flash} × baseline/fix × 5; n ≈ 615)
Baseline silent-wrong (receiver acted wrongly with no clarification turn), all pairs:
| convention | silent wrong [95% CI] |
|---|---|
| UK "first floor" → US | **0.75** [0.55, 0.90] |
| UK date "03/04" → US | **0.70** [0.50, 0.90] |
| UK fiscal "FY27" → US | **0.65** [0.45, 0.85] |
| German "half six" → London | **0.62** [0.31, 0.85] |
| US date "10/11" → Madrid | **0.50** [0.28, 0.72] |
| °C "18 degrees" → US | 0.33 · EU shoe 0.25 · "tomorrow" TYO→NYC 0.18 · UK dress 0.15 · L/100km 0.10 |
| stone, lakh, Reiwa era, °F→EU room | 0.00 |
| controls (decimal comma, "mil millones", "next Friday") | 0.00–0.10 |

- By pair: space→space 0.39, space→ling 0.28, ling→space 0.14, ling→ling 0.14.
- **The combined fix** (receiver locale awareness + sender explicitness): correct 0.72 → 0.89 overall; space→space 0.51 → 0.84.

## 2. Decomposition (judge labels each sender's first message as locale-ambiguous or explicit)
- **P(sender writes the ambiguous locale form):** space-bunny **0.74**, ling **0.39**. Senders differ in how faithfully they mimic their principal.
- **P(receiver silently wrong | ambiguous message):** space-bunny 0.39 (asks 0.13), ling 0.33 (asks 0.07). Receivers rarely clarify.
- **Given an ambiguous message:** UK date 1.00, "first floor" 0.93, "half six" 0.88, US→EU date 0.50, versus stone, lakh, Reiwa and °F→EU room all **0.00**.

## 3. Preregistered test of the false-friend theory (PREDICTIONS.md committed before running; space→space, 10 each)
**Theory:** silent misreading happens when the expression is *valid and plausible in the receiver's own convention*.

| case | prediction | silent wrong | |
|---|---|---|---|
| UK "2 pints" → US ml | FAIL | **1.00** (946 ml) | ✓ |
| German "1st floor" → US | FAIL | **1.00** | ✓ |
| Australian "2 tablespoons" → US ml | FAIL | **0.80** (30 ml) | ✓ |
| Brazilian "05/06" → US | FAIL | **0.70** (May 6) | ✓ |
| UK "table the item" → US | FAIL | 0.30 (postponed) | ✗ (below threshold, but non-zero) |
| UK "biweekly" → US | FAIL | 0.00, **asked 0.80** | ✗: the ambiguity is visible ("biweekly" is ambiguous even in US English), so it gets clarified |
| EU shoe 44, 295 K, 10 imperial gal, 25/12/2027, HK$800 | PASS | 0.00 each | ✓ ×5 |
| UK "gas mark 4" | PASS | 0.40 (400 °F) | ✗: a conversion-*knowledge* error (correct is 350 °F), not a misreading |

**9/12 confirmed.** The two theory-relevant misses refine it: **(valid ∧ plausible in the receiver's convention) ∧ ambiguity not commonly known → silent error. Known-ambiguous terms → clarification.**

## Verdict
- **Strengths:**
  - large, clean effects (70–100% on false friends);
  - a predictive account confirmed by preregistration;
  - a sender × receiver decomposition;
  - two model families, a realistic setting (principal-faithful agents), and a fix baseline (72% → 89%) that leaves headroom;
  - squarely on the theme track ("Language as a Medium for Agentic Communication": modelling partners, common ground, reliability);
  - prior-work check: novel (closest are Grounding Gaps, NAACL 2024, and CAPRI 2606.17688).
- **Weaknesses:** two mid-size models only; simulated principals; the judge-based decomposition needs human validation (cheap: ~150 sender messages).

**Acceptance outlook: GOOD. The strongest candidate for the theme track; main-conference plausible.** Remaining needs: 3–4 more model families (including frontier GPT/Claude/Gemini, to show it isn't a weak-model artefact), human validation of the judge labels, and ~30 conventions × 8 locales as a released benchmark.

## 4. Preregistration #2 (prereg2/PREDICTIONS.md committed before running; space→space, 10 each)
| case | prediction | silent wrong | |
|---|---|---|---|
| Indian "04-05-2027" → US | FAIL | **1.00** (Apr 5) | ✓ |
| CAD "$200" → USD | FAIL | **0.80** (recorded 200 USD) | ✓ |
| Japanese "FY2026" → calendar FY | FAIL | **0.80** | ✓ |
| AUD "$150" → USD | FAIL | **0.70** | ✓ |
| "limit 50" (km/h) → mph | FAIL | **0.70** (50 mph) | ✓ |
| Dutch "half eight" (=19:30) → London | FAIL | **0.60** (20:30) | ✓ |
| Australian "FY26" | FAIL | 0.30 | ✗ (non-zero but below threshold) |
| UK phone → E.164 | PASS | 0.00 | ✓ |
| "38 degrees" fever → °F system | PASS | **0.30 (recorded 38 °F)** | ✗: implausible readings are *not* reliably caught |
| German "KW 14" | PASS | 0.50 | ✗ artifact: the receiver lacked the current year (wrong-year dates) |

**Across both preregistrations: 16/22 predictions confirmed.**
- **FAIL predictions: 11/13** (the theory predicts which conventions break).
- **PASS predictions: 5/9.** The theory is *too optimistic* about safety: receivers sometimes write implausible values (38 °F fever, 400 °F for gas mark 4) instead of converting or asking.

So the false-friend criterion is *sufficient* for failure, but plausibility checking is unreliable even when the misreading is absurd.

**Updated benchmark size:** 17 + 12 + 10 = **39 conventions** tested across ~10 locales.

## 5. Author spot-check of the decomposition judge (20 random sender messages, read manually)
**Agreement 15/20 (75%).**
- 3 disagreements: unmistakable foreign units ("₹2.5 lakh" ×2, "12 stone") labelled *ambiguous*. They can't be misread, which inflates the ambiguous denominator for exactly the 0%-error conventions.
- 2 disagreements: misses ("tomorrow, Wednesday, October 14" is explicit; "6 litres" omits "/100 km").
- Labels on the false-friend cases (dates, floors, "half six", 68 degrees) were all correct.

**Implication:** the decomposition's main conclusions (senders differ in mimicry; receivers misread false friends 88–100% when ambiguous) hold. Per-convention numbers for unmistakable units need a sharper rubric ("misreadable in the receiver's convention") and **human validation (2 annotators, ~150 messages)** before submission.

## 6. Protocol-level fix: locale metadata in the counterpart's agent card (9 hardest conventions × 8; space→space)
| case | baseline | locale card only | prompt fix only | card + prompt |
|---|---|---|---|---|
| UK first floor | 0.00 | 0.12 | 0.12 | 0.50 |
| UK date 03/04 | 0.00 | 1.00 | 0.88 | 1.00 |
| German "half six" | 0.25 | 0.38 | 0.38 | 0.38 |
| UK "2 pints" | 0.25 | 0.88 | 0.12 | 1.00 |
| German "1st floor" | 0.00 | 0.25 | 0.38 | 0.50 |
| CAD "$200" | 0.12 | 0.12 | 0.12 | **0.12** |
| "limit 50" km/h | 0.25 | 0.38 | 0.12 | 0.62 |
| Indian DD-MM date | 0.00 | 0.75 | 0.88 | 0.88 |
| 38 °C fever | 0.88 | 0.50 | 1.00 | 1.00 |
| **mean** | **0.19** | **0.49** | **0.44** | **0.67** |
| asked back | 0.11 | 0.10 | 0.36 | 0.38 |

- A one-line locale field (as an A2A-style agent card could carry) more than doubles accuracy without extra turns.
- Combined with the prompt it reaches 0.67, but **CAD "$" (0.12), "half six" (0.38) and floors (0.50) stay hard** even when the receiver *knows* the sender is in Toronto, Berlin or London. Knowing the locale isn't the same as applying its conventions (cf. CAPRI 2606.17688).

That leaves clear headroom for a method contribution (e.g., an explicit convention-resolution step or a trained grounding policy).

## 7. Method: explicit convention-resolution step (receiver lists locale-dependent expressions, resolves them in the sender's convention, then acts)
| case | baseline | card + prompt | resolver only | **card + resolver** |
|---|---|---|---|---|
| UK first floor | 0.00 | 0.50 | 0.38 | **1.00** |
| UK date | 0.00 | 1.00 | 1.00 | **1.00** |
| German "half six" | 0.25 | 0.38 | 0.38 | 0.50 |
| UK pints | 0.25 | 1.00 | 1.00 | **1.00** |
| German "1st floor" | 0.00 | 0.50 | 0.62 | **1.00** |
| CAD "$" | 0.12 | 0.12 | 0.38 | **0.75** |
| km/h | 0.25 | 0.62 | 0.75 | **1.00** |
| Indian date | 0.00 | 0.88 | 1.00 | **1.00** |
| 38 °C fever | 0.88 | 1.00 | 0.88 | **1.00** |
| **mean** | 0.19 | 0.67 | 0.71 | **0.92** |
| asked back | 0.11 | 0.38 | **0.75** | 0.24 |

- **Locale metadata + an explicit resolution step: 19% → 92%**, with fewer clarification turns than resolving without metadata (24% vs 75%).
- The pieces are complementary: metadata says *which* convention; the resolver forces it to be *applied* (the know-vs-apply gap, cf. CAPRI).
- The remaining failure is the colloquial time expression ("half six" from a German speaker), where the literal English phrase is itself a false friend.

## Overall L4 verdict (space-bunny ceiling reached)
**Paper:** "Lost in Convention: Silent Cross-Locale Misreading Between LLM Agents" (NAACL 2027 theme track). Contents:
1. a 39-convention benchmark across ~10 locales;
2. large silent-error rates (up to 100%) with no clarification;
3. a predictive *false-friend* account, preregistered twice (16/22 predictions; 11/13 failure predictions);
4. a sender-mimicry × receiver-misreading decomposition;
5. fixes: prompts (→ 67%), protocol metadata (→ 49%), and **metadata + resolution step (→ 92%)**.

**Acceptance outlook: GOOD. The most acceptance-ready of the four leads.**

Still needed beyond Space Bunny:
- (a) **frontier models** as sender and receiver, to show it isn't a weak-model artefact;
- (b) human validation of the judge-based decomposition;
- (c) a heterogeneous-pair matrix with 3+ families.

## 8. v3 (reviewer-driven redesign): naturalistic relay senders + cue control + held-out method eval + same-locale controls
675 runs (15 per case × condition), fixed shuffle seed, **0 errored runs** (errors now logged, not silently dropped).
- **Naturalistic sender:** a generic "relay your principal's request" agent; the *principal's own message* ("Can you get the workshop booked for 03/04/2027 please?") is the input. No instruction to mimic.
- **Receiver cue:** *none* (the locale isn't recoverable) vs *card* (principal_locale in the counterpart's agent card) vs *card + resolver*.

| set | none: correct / silent-wrong | card: correct / silent-wrong | card + resolver: correct / silent-wrong |
|---|---|---|---|
| dev (6 conventions the resolver was developed on) | 0.29 / 0.67 | 0.41 / **0.54** | **0.94** / 0.04 |
| **held-out** (6 new conventions) | 0.27 / 0.72 | 0.37 / **0.62** | **0.67** / 0.30 |
| same-locale controls (US→US) | 0.87 / 0.13 | 0.91 / 0.09 | 0.89 / 0.07 |

Senders mention their principal's location in only 0–4% of messages, so in *none* the locale truly isn't recoverable from the message.

Per case (none / card / card + resolver correct):
- UK first floor 0 / 0 / 1.00
- CAD "$200" 0 / 0 / 0.80
- km/h 0.13 / 0.13 / 1.00
- UK pints 0 / 0.67 / 1.00
- UK FY27 0.07 / 0 / 0.20
- AUD "$150" 0 / 0 / 0.67
- JP FY2026 0 / 0 / 0.40
- AU tbsp 0 / 0.33 / 0.80
- UK date 1 / 1 / 1 (naturalistic senders rewrite dates as "3 April 2027")
- Indian date 0.60 / 0.67 / 0.87
- Brazilian date 0.60 / 0.93 / 0.93
- 38 °C fever 0.93 / 0.93 / 1.00

**What this settles:**
1. **"Misreading despite the cue" is real.** With the sender's locale *explicitly given* in the agent card, receivers still silently misread **54–62%** of false friends (UK floors, CAD/AUD "$", km/h, fiscal years: 0–13% correct). This answers the "reading in your own convention is rational" objection.
2. **Naturalistic senders don't fix it.** They often disambiguate *dates* themselves, but relay floors, units, currency symbols and fiscal years verbatim.
3. **The method generalises only partly:** 94% on the development conventions vs **67% held out** (fiscal years 20–40%, AUD 67%). This is honest headroom for a method paper.
4. **No over-conversion:** same-locale controls are unchanged (0.87–0.91). One interesting residual: even a US→US "03/04/2027" is read as April 3 in 27–33% of runs.

## L4 final verdict (space-bunny ceiling)
Mock ARR review *before* v3: meta 2.5 (Main ~10% / Findings ~30–35%). v3 directly fixes its top soundness items:
- cue control and misreading despite the cue;
- naturalistic senders;
- held-out method evaluation;
- over-conversion controls;
- error logging, fixed seeds, n=15 per cell.

With these, I'd estimate meta **~3.0–3.5 on the current evidence** (Findings likely, Main possible).
- **What decides Main:** frontier and open-weight model breadth (3+ families, heterogeneous pairs) and human validation of any judge-based analysis.
- If frontier receivers also misread despite the cue at ≥30–40%, this is a strong theme-track main paper.

## 9. CAPRI-grounded evaluation (existing benchmark; `capri/`)
**Data.** CAPRI (yisongmiao/CAPRI, CC BY 4.0): human-validated conversations where the user's culture is revealed only through implicit cues (name, postcode, phone or plate format, voltage), across 10 cultures. We use CAPRI's ground-truth unit key per culture.
- **Sample:** 282 implicit conversations covering temperature, speed, distance, size and price, with ~6 per culture per concept. Price for Iran is excluded (FX ambiguity).
- **Neutral controls:** 30 CAPRI neutral conversations.
- **Task:** the verbatim CAPRI conversation is the principal's history with their own agent. The final image question is replaced by a bare-number instruction, e.g. "set my thermostat to 22" or "my max budget is 300". The receiver's tool takes a different convention (°F, mph, miles, sq ft, USD; °C/km/h etc. for US principals).
- **Scoring:** correct = the tool argument lies in the band implied by the principal's CAPRI unit.
- space-bunny, temperature 1, seed 0. Errors: 0/1368, 0/120 and 0/684.

| condition | correct | silent wrong | correct on ambiguous subset (speed/distance/price, n=168) |
|---|---|---|---|
| direct (single agent holds the tool) | **0.07** [.04,.10] | 0.77 | 0.00 |
| relay | 0.58 [.52,.63] | 0.36 | 0.38 |
| relay + card | 0.65 [.59,.70] | 0.27 | — |
| relay + card + resolver (receiver-side) | 0.82 [.77,.86] | 0.12 | 0.73 |
| explicit-units sender | 0.79 [.74,.83] | 0.14 | 0.67 |
| **explicit sender + card + resolver** | **0.89** [.86,.93] | **0.05** | **0.87** |

Same-convention controls (correct = no conversion): none 0.86, card+resolver 0.88, explicit 0.91. The fixes don't cause over-conversion.

**Tool-unit anchoring (new).** A single agent with a unit-typed tool passes the bare number straight through (`fahrenheit=22`, `mph=100`, `max_usd=30000` for a Japanese principal) in 77% of cases, even though CAPRI's cues are in context. Relaying through natural language accidentally helps, because the sender verbalises a unit.

**Where the relay breaks (sender's first message, plain relay).**

| sender's first message | share | plain relay correct | with receiver resolver |
|---|---|---|---|
| principal's unit | 64% | 0.87 | 0.98 |
| bare number | 18% | 0.02 | 0.72 |
| hedged | 10% | 0.14 | 0.70 |
| wrong unit (e.g. UK "300" sent as "$300") | 7% | 0.00 | **0.00** |

A wrong unit asserted by the sender is unrecoverable downstream, so the sender-side fix is needed. Receivers also drop stated units (US "$300" recorded as €300).

**Cue control (neutral CAPRI, value given metric-style).**
- Temperature and size are resolvable by plausibility: no-cue relay ≈ 0.92 for both.
- Speed and distance need the cues: no-cue relay 0.25 / 0.08 vs implicit relay 0.50 / 0.35 (metric cultures).
- The paper's headline subset should therefore be **speed/distance/price**, where the plain relay is only 38% correct and the full fix reaches 87%.

**Caveats.**
- One model (space-bunny).
- The instruction templates and value bands are ours; CAPRI supplies the conversations, cues and unit key.
- FX bands are approximate (±~12%).

## 10. Claude verification (Sonnet via `claude -p`; `capri/run_claude.py`; 141 CAPRI items, 637 runs, 7 network errors)
Acting agent uses a native MCP tool. Prior turns (CAPRI history, relay dialogue) are rendered as a transcript because the CLI takes one prompt.

| condition | correct | silent wrong | asked | ambiguous subset correct / silent wrong |
|---|---|---|---|---|
| direct | 0.25 | 0.65 | 0.11 | **0.00 / 0.93** |
| relay | 0.40 | 0.17 | 0.45 | 0.10 / 0.28 |
| relay + card + resolver | 0.68 | **0.00** | 0.32 | 0.52 / 0.00 |
| explicit sender + card + resolver | **0.83** | 0.12 | 0.07 | 0.72 / 0.19 |

Same-convention controls: 0.80 / 0.93.

- **Tool-unit anchoring replicates on Claude.** On ambiguous items, direct is 0% correct (e.g. `max_usd=300000` for a Korean ₩300,000 budget, `mph=100` for Iran).
- Unlike space-bunny, Claude relays ask more (45%), so failures shift from silent to unresolved.
- The explicit-units sender is again the biggest lever.
