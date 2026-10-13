# Bare Numbers Between Agents: Where Delegated Agent Communication Loses Conventions

*Working submission summary for internal review (v3, after reviews 1–2). Target: NAACL 2027 (ARR October 2026), theme track "Language as a Medium for Agentic Communication". Long paper. Every number is copied from Appendix A (capri/analyze_frontier.py); all numbers refer to the ambiguous subset (speed/distance/price) unless stated; model coverage is given per claim.*

## Abstract (draft)
When a personal agent delegates a request to another organisation's agent, quantities cross convention boundaries (a Korean user's budget of "300,000", a German user's speed alert of "100"). CAPRI (Miao, Zhu & Shwartz 2026) showed that models infer a user's culture from implicit cues but fail to apply it; we ask where, in an agent-to-agent exchange, the convention is lost and which side of the channel should carry it. Each CAPRI conversation becomes the principal's history with their own agent, followed by a bare-number request carried out through a counterpart agent whose tool uses another convention. Across six models (Claude Opus/Sonnet/Haiku/Fable, GPT-6.1, open-weight Ling-3.1), a single agent holding the tool converts on 0–5% of items, silently acting on the wrong value 46–96% of the time; a plain relay is correct on 10–30%. The receiver's outcome is set by the sender's message: counterfactually replacing it (4 receivers) with a bare number gives 0% correct (32–96% silently wrong), with a wrong unit 0% (70–100% silently wrong), with the principal's unit 43–80% (0% silently wrong, the rest ask). In a factorial ablation on all 168 ambiguous items (Opus, Sonnet), sender explicitness is the largest single lever (61–67%) versus receiver metadata alone (card 11–22%, resolver 15–21%) and a length-matched generic caution prompt (5–10%); a fully non-oracle protocol — the sender infers the locale, states units, and publishes its inferred locale for the receiver to resolve against — reaches 73–84%, close to the oracle-locale bound (72–89%). But explicitness trades safety for accuracy: senders infer the locale wrongly ~30% of the time, and stating units turns receiver questions into confident actions (Sonnet silent-wrong 3% with receiver-side resolution vs 20–23% with sender explicitness). Two channel designs move along this frontier: a typed message with a mandatory unit field (Opus: 62% correct, 3% silently wrong) and a hybrid in which the sender attaches a confidence and the receiver asks when it is low (Opus: 65% correct, 1% silently wrong, vs 84%/7% without it). Explicit protocols also over-convert same-convention requests (Sonnet 18%), a cost we report.

## 1. Claims (coverage)
1. **Tool-unit anchoring (replication of CAPRI's infer-vs-apply gap in a tool setting; motivation, not novelty).** Direct: 0–5% correct on all 6 models.
2. **The sender's message determines the outcome (interventional).** Counterfactual message injection on Opus, Sonnet, Haiku, Fable receivers (84 items each). Observationally in plain relays, bare first messages are followed by 0–3% correct for all 6 models.
3. **Sender explicitness is the strongest lever; receiver metadata helps conditionally; generic caution does nothing.** Full factorial on 168 items for Sonnet; Opus cells n=111–143 (completing).
4. **A non-oracle protocol approaches the oracle** (Opus 84% vs 86% within the ablation; Sonnet 73% vs 72% main run).
5. **Accuracy–safety trade-off.** Explicitness raises silent errors; typed and hybrid channels reduce them at an accuracy cost; protocols over-convert same-convention requests (Sonnet 18% non-oracle and oracle; Opus/others: oracle 0–10%).

## 2. Setup
- **Data.** CAPRI implicit-cue conversations (CC BY 4.0): temperature, speed, distance, size, price × 10 cultures; Iran-price excluded. CAPRI's unit key defines the principal's convention. Main conditions: every second item (141 per model; 84 ambiguous). Ablations: all 168 ambiguous items. Injection: every second ambiguous item (84).
- **Task.** CAPRI's final image question removed; one templated bare-number instruction per concept; receiver's tool takes the other convention and its prompt states its locale.
- **Metrics.** correct; **silent wrong** (acted wrongly without asking; headline harm); **safe** (correct or asked). 95% CIs: bootstrap clustered by culture×concept; paired exact McNemar between conditions on the same items.
- **Conditions.** direct; plain relay (≤4 rounds); factorial tokens explicit / card (oracle locale) / inferred (sender's own inferred locale in its card) / resolver / generic (length-matched caution) / typed (JSON with mandatory unit) / hybrid (sender confidence; receiver asks if unit missing or confidence low); inject:{bare, own, wrong, hedged} (receiver sees a fixed sender message).
- **Sender-message coding.** Deterministic regex coder over unit/currency patterns (own / wrong / hedged / bare); validation on a hand-checked sample pending.
- **Models / harness.** Claude via Claude Code CLI headless (system prompt fully replaced, built-in tools disabled; history rendered as a transcript); GPT-6.1 via Codex CLI (direct/relay only, quota); Ling-3.1-flash (open-weight) via native chat API with true multi-turn messages (harness check: same pattern).

## 3. Results
Appendix A: per model main conditions + same-convention controls + paired tests + first-message analysis; per sender→receiver pair the factorial ablation, typed/hybrid, injection and inferred-locale accuracy.

## 4. Limitations
- One template per concept; three ambiguous concepts; price is FX-based (bands ±12%).
- Claude/GPT multi-turn rendered as a transcript; native-API replication only for Ling. GPT has two conditions.
- Opus typed/hybrid cells and Sonnet typed/hybrid are still completing; cross-model pairs (Opus↔Haiku) queued.
- Prior work: CAPRI (infer-vs-apply; explicit prompting), Faithful-Not-Corrective (arXiv:2607.09678; relays propagate errors — wrong-unit unrecoverability is expected), Generalization across Measurement Systems (arXiv:2506.02591), NUMCoT (arXiv:2406.02864), MAST, A2A agent cards (no locale field).

## Appendix A: live results (capri/analyze_frontier.py, 2026-10-05 07:43)
```

== claude-fable-5-1 (errors=0)  (n ok=644)
  condition                      AMBIGUOUS correct      silent wrong           safe(correct|asked)    n   | all items correct
  direct                         0.00 [0.00,0.00]       0.46 [0.32,0.61]       0.54 [0.39,0.68]        84 | 0.28 [0.17,0.40] n=141
  none                           0.30 [0.18,0.42]       0.32 [0.19,0.48]       0.68 [0.54,0.81]        84 | 0.57 [0.45,0.70] n=141
  card+resolver                  0.83 [0.73,0.92]       0.10 [0.04,0.17]       0.90 [0.83,0.96]        84 | 0.89 [0.83,0.95] n=141
  explicit+card+resolver         0.89 [0.81,0.96]       0.11 [0.04,0.19]       0.89 [0.81,0.96]        84 | 0.94 [0.89,0.98] n=141
  same-convention control explicit+card+resolver   correct=1.00 [1.00,1.00] over-converted/wrong=0.00 asked=0.00 n=40
  same-convention control none                     correct=0.93 [0.82,1.00] over-converted/wrong=0.03 asked=0.12 n=40
    direct -> none: +25 / -0 of 84 paired items, exact p=5.96e-08
    none -> card+resolver: +46 / -1 of 84 paired items, exact p=6.82e-13
    none -> explicit+card+resolver: +50 / -0 of 84 paired items, exact p=1.78e-15
    plain relay, sender's first message: {'hedged': '0.38 (correct 0.25)', 'bare': '0.31 (correct 0.00)', 'own': '0.26 (correct 0.77)', 'wrong': '0.05 (correct 0.00)'}

== gpt-6.1-sol (errors=0)  (n ok=107)
  condition                      AMBIGUOUS correct      silent wrong           safe(correct|asked)    n   | all items correct
  direct                         0.00 [0.00,0.00]       0.57 [0.39,0.75]       0.43 [0.25,0.61]        28 | 0.21 [0.11,0.34] n=47
  none                           0.14 [0.04,0.29]       0.39 [0.21,0.57]       0.61 [0.43,0.79]        28 | 0.45 [0.30,0.60] n=47
  same-convention control none                     correct=0.62 [0.38,0.85] over-converted/wrong=0.00 asked=0.38 n=13
    direct -> none: +4 / -0 of 28 paired items, exact p=0.125
    none vs card+resolver: no discordant pairs (n=0)
    none vs explicit+card+resolver: no discordant pairs (n=0)
    plain relay, sender's first message: {'hedged': '0.46 (correct 0.08)', 'bare': '0.43 (correct 0.00)', 'own': '0.11 (correct 1.00)'}

== haiku (errors=0)  (n ok=644)
  condition                      AMBIGUOUS correct      silent wrong           safe(correct|asked)    n   | all items correct
  direct                         0.00 [0.00,0.00]       0.82 [0.71,0.92]       0.18 [0.08,0.29]        84 | 0.07 [0.02,0.13] n=141
  none                           0.13 [0.05,0.24]       0.64 [0.51,0.76]       0.36 [0.24,0.49]        84 | 0.45 [0.33,0.58] n=141
  card+resolver                  0.63 [0.48,0.79]       0.02 [0.00,0.06]       0.98 [0.94,1.00]        84 | 0.77 [0.66,0.87] n=141
  explicit+card+resolver         0.45 [0.31,0.61]       0.27 [0.15,0.40]       0.73 [0.60,0.85]        84 | 0.65 [0.53,0.77] n=141
  same-convention control explicit+card+resolver   correct=0.75 [0.62,0.88] over-converted/wrong=0.10 asked=0.20 n=40
  same-convention control none                     correct=0.78 [0.62,0.90] over-converted/wrong=0.07 asked=0.17 n=40
    direct -> none: +11 / -0 of 84 paired items, exact p=0.000977
    none -> card+resolver: +45 / -3 of 84 paired items, exact p=1.31e-10
    none -> explicit+card+resolver: +31 / -4 of 84 paired items, exact p=3.47e-06
    plain relay, sender's first message: {'bare': '0.61 (correct 0.00)', 'own': '0.19 (correct 0.62)', 'wrong': '0.12 (correct 0.00)', 'hedged': '0.08 (correct 0.14)'}

== ling-3.1-flash (errors=15)  (n ok=629)
  condition                      AMBIGUOUS correct      silent wrong           safe(correct|asked)    n   | all items correct
  direct                         0.00 [0.00,0.00]       0.96 [0.92,1.00]       0.04 [0.00,0.08]        84 | 0.11 [0.05,0.18] n=141
  none                           0.12 [0.04,0.21]       0.55 [0.39,0.69]       0.45 [0.32,0.61]        84 | 0.42 [0.30,0.54] n=141
  card+resolver                  0.90 [0.85,0.95]       0.00 [0.00,0.00]       0.98 [0.94,1.00]        83 | 0.92 [0.87,0.96] n=140
  explicit+card+resolver         0.92 [0.86,0.97]       0.00 [0.00,0.00]       1.00 [1.00,1.00]        75 | 0.95 [0.91,0.98] n=129
  same-convention control explicit+card+resolver   correct=0.95 [0.87,1.00] over-converted/wrong=0.03 asked=0.03 n=38
  same-convention control none                     correct=0.93 [0.82,1.00] over-converted/wrong=0.00 asked=0.17 n=40
    direct -> none: +10 / -0 of 84 paired items, exact p=0.00195
    none -> card+resolver: +65 / -0 of 83 paired items, exact p=5.42e-20
    none -> explicit+card+resolver: +59 / -0 of 75 paired items, exact p=3.47e-18
    plain relay, sender's first message: {'bare': '0.46 (correct 0.03)', 'hedged': '0.37 (correct 0.00)', 'own': '0.17 (correct 0.64)'}

== opus (errors=0)  (n ok=644)
  condition                      AMBIGUOUS correct      silent wrong           safe(correct|asked)    n   | all items correct
  direct                         0.05 [0.00,0.12]       0.76 [0.62,0.87]       0.24 [0.13,0.38]        84 | 0.35 [0.23,0.48] n=141
  none                           0.18 [0.08,0.29]       0.26 [0.13,0.42]       0.74 [0.58,0.87]        84 | 0.51 [0.38,0.64] n=141
  card+resolver                  0.40 [0.27,0.54]       0.01 [0.00,0.04]       0.99 [0.96,1.00]        84 | 0.65 [0.53,0.76] n=141
  explicit+card+resolver         0.89 [0.82,0.95]       0.08 [0.04,0.14]       0.92 [0.86,0.96]        84 | 0.94 [0.89,0.97] n=141
  same-convention control explicit+card+resolver   correct=0.95 [0.88,1.00] over-converted/wrong=0.05 asked=0.00 n=40
  same-convention control none                     correct=0.80 [0.68,0.93] over-converted/wrong=0.05 asked=0.28 n=40
    direct -> none: +13 / -2 of 84 paired items, exact p=0.00739
    none -> card+resolver: +24 / -5 of 84 paired items, exact p=0.000546
    none -> explicit+card+resolver: +60 / -0 of 84 paired items, exact p=1.73e-18
    plain relay, sender's first message: {'hedged': '0.44 (correct 0.08)', 'bare': '0.31 (correct 0.00)', 'own': '0.24 (correct 0.60)', 'wrong': '0.01 (correct 0.00)'}

== sonnet (errors=7)  (n ok=637)
  condition                      AMBIGUOUS correct      silent wrong           safe(correct|asked)    n   | all items correct
  direct                         0.00 [0.00,0.00]       0.93 [0.86,0.98]       0.07 [0.02,0.14]        84 | 0.25 [0.13,0.38] n=141
  none                           0.10 [0.02,0.20]       0.28 [0.15,0.43]       0.72 [0.57,0.85]        82 | 0.40 [0.27,0.51] n=139
  card+resolver                  0.52 [0.37,0.68]       0.00 [0.00,0.00]       1.00 [1.00,1.00]        82 | 0.68 [0.57,0.79] n=139
  explicit+card+resolver         0.72 [0.60,0.84]       0.19 [0.10,0.31]       0.81 [0.69,0.90]        83 | 0.83 [0.75,0.91] n=138
  same-convention control explicit+card+resolver   correct=0.93 [0.82,1.00] over-converted/wrong=0.07 asked=0.00 n=40
  same-convention control none                     correct=0.80 [0.68,0.93] over-converted/wrong=0.00 asked=0.23 n=40
    direct -> none: +8 / -0 of 82 paired items, exact p=0.00781
    none -> card+resolver: +34 / -1 of 80 paired items, exact p=2.1e-09
    none -> explicit+card+resolver: +50 / -0 of 81 paired items, exact p=1.78e-15
    plain relay, sender's first message: {'hedged': '0.46 (correct 0.05)', 'bare': '0.35 (correct 0.00)', 'own': '0.18 (correct 0.40)'}

== ABLATION sender=claude-fable-5-1 receiver=claude-fable-5-1 (errors in file=0)  (n ok=336)
  condition                      AMBIGUOUS correct      silent wrong           safe(correct|asked)    n   | all items correct
  inject:bare                    0.00 [0.00,0.00]       0.35 [0.20,0.50]       0.65 [0.50,0.81]        84 | 0.00 [0.00,0.00] n=84
  inject:hedged                  0.00 [0.00,0.00]       0.00 [0.00,0.00]       1.00 [1.00,1.00]        84 | 0.00 [0.00,0.00] n=84
  inject:own                     0.69 [0.51,0.86]       0.00 [0.00,0.00]       1.00 [1.00,1.00]        84 | 0.69 [0.51,0.86] n=84
  inject:wrong                   0.00 [0.00,0.00]       0.98 [0.94,1.00]       0.02 [0.00,0.06]        84 | 0.00 [0.00,0.00] n=84

== ABLATION sender=haiku receiver=haiku (errors in file=0)  (n ok=336)
  condition                      AMBIGUOUS correct      silent wrong           safe(correct|asked)    n   | all items correct
  inject:bare                    0.00 [0.00,0.00]       0.55 [0.39,0.70]       0.45 [0.30,0.61]        84 | 0.00 [0.00,0.00] n=84
  inject:hedged                  0.00 [0.00,0.00]       0.05 [0.00,0.11]       0.95 [0.89,1.00]        84 | 0.00 [0.00,0.00] n=84
  inject:own                     0.43 [0.26,0.58]       0.00 [0.00,0.00]       1.00 [1.00,1.00]        84 | 0.43 [0.26,0.58] n=84
  inject:wrong                   0.00 [0.00,0.00]       0.70 [0.56,0.82]       0.30 [0.18,0.44]        84 | 0.00 [0.00,0.00] n=84

== ABLATION sender=opus receiver=opus (errors in file=0)  (n ok=1737)
  condition                      AMBIGUOUS correct      silent wrong           safe(correct|asked)    n   | all items correct
  card                           0.22 [0.12,0.33]       0.03 [0.01,0.06]       0.97 [0.94,0.99]       142 | 0.22 [0.12,0.33] n=142
  explicit                       0.67 [0.52,0.80]       0.09 [0.04,0.14]       0.91 [0.86,0.96]       136 | 0.67 [0.52,0.80] n=136
  explicit+card+resolver         0.87 [0.78,0.94]       0.08 [0.03,0.15]       0.92 [0.85,0.97]       112 | 0.87 [0.78,0.94] n=112
  explicit+inferred+resolver     0.84 [0.74,0.92]       0.07 [0.03,0.12]       0.93 [0.88,0.97]       139 | 0.84 [0.74,0.92] n=139
  explicit+inferred+resolver+hybrid 0.66 [0.54,0.77]       0.01 [0.00,0.03]       0.99 [0.97,1.00]       108 | 0.66 [0.54,0.77] n=108
  generic                        0.10 [0.04,0.18]       0.15 [0.05,0.26]       0.85 [0.74,0.95]       144 | 0.10 [0.04,0.18] n=144
  inferred+resolver              0.50 [0.39,0.61]       0.03 [0.01,0.06]       0.97 [0.94,0.99]       135 | 0.50 [0.39,0.61] n=135
  inferred+resolver+hybrid       0.30 [0.21,0.40]       0.03 [0.00,0.06]       0.97 [0.94,1.00]       116 | 0.30 [0.21,0.40] n=116
  inject:bare                    0.00 [0.00,0.00]       0.77 [0.63,0.89]       0.23 [0.11,0.37]        84 | 0.00 [0.00,0.00] n=84
  inject:hedged                  0.29 [0.14,0.46]       0.04 [0.00,0.11]       0.96 [0.89,1.00]        84 | 0.29 [0.14,0.46] n=84
  inject:own                     0.80 [0.67,0.92]       0.00 [0.00,0.00]       1.00 [1.00,1.00]        84 | 0.80 [0.67,0.92] n=84
  inject:wrong                   0.00 [0.00,0.00]       1.00 [1.00,1.00]       0.00 [0.00,0.00]        84 | 0.00 [0.00,0.00] n=84
  none                           0.15 [0.06,0.26]       0.32 [0.19,0.49]       0.68 [0.51,0.81]       114 | 0.15 [0.06,0.26] n=114
  resolver                       0.22 [0.12,0.33]       0.03 [0.00,0.07]       0.97 [0.93,1.00]       141 | 0.22 [0.12,0.33] n=141
  typed                          0.62 [0.49,0.74]       0.03 [0.00,0.06]       0.96 [0.93,0.99]       114 | 0.62 [0.49,0.74] n=114
    sender-inferred locale correct: 0.71 (n=498)

== ABLATION sender=sonnet receiver=sonnet (errors in file=0)  (n ok=1530)
  condition                      AMBIGUOUS correct      silent wrong           safe(correct|asked)    n   | all items correct
  card                           0.11 [0.04,0.20]       0.11 [0.05,0.19]       0.89 [0.81,0.95]       168 | 0.11 [0.04,0.20] n=168
  explicit                       0.61 [0.49,0.72]       0.23 [0.15,0.32]       0.77 [0.68,0.85]       168 | 0.61 [0.49,0.72] n=168
  explicit+inferred+resolver     0.73 [0.63,0.82]       0.20 [0.12,0.27]       0.80 [0.73,0.88]       168 | 0.73 [0.63,0.82] n=168
  generic                        0.05 [0.01,0.14]       0.17 [0.07,0.29]       0.83 [0.71,0.93]       168 | 0.05 [0.01,0.14] n=168
  inferred+resolver              0.45 [0.32,0.60]       0.03 [0.01,0.05]       0.97 [0.95,0.99]       168 | 0.45 [0.32,0.60] n=168
  inject:bare                    0.00 [0.00,0.00]       0.96 [0.90,1.00]       0.04 [0.00,0.10]        84 | 0.00 [0.00,0.00] n=84
  inject:hedged                  0.21 [0.08,0.36]       0.07 [0.01,0.17]       0.93 [0.83,0.99]        84 | 0.21 [0.08,0.36] n=84
  inject:own                     0.71 [0.55,0.87]       0.00 [0.00,0.00]       1.00 [1.00,1.00]        84 | 0.71 [0.55,0.87] n=84
  inject:wrong                   0.00 [0.00,0.00]       1.00 [1.00,1.00]       0.00 [0.00,0.00]        84 | 0.00 [0.00,0.00] n=84
  resolver                       0.15 [0.06,0.26]       0.03 [0.01,0.05]       0.97 [0.95,0.99]       168 | 0.15 [0.06,0.26] n=168
  same-convention control explicit+card+resolver   correct=0.75 [0.63,0.88] over-converted/wrong=0.19 asked=0.07 n=57
  same-convention control explicit+inferred+resolver correct=0.78 [0.67,0.89] over-converted/wrong=0.17 asked=0.05 n=63
  same-convention control none                     correct=0.76 [0.62,0.88] over-converted/wrong=0.00 asked=0.29 n=66
    sender-inferred locale correct: 0.70 (n=399)
```
