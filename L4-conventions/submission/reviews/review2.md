# Review 2 (fresh ARR-style reviewer agent, theme track, 2026-10-04, on draft v2)
Scores: Soundness 2.5, Excitement 2.5, Overall 2.5, confidence 4; theme fit good. Odds: Main 7 / Findings 28 / Reject 65; with must-fixes 18 / 47 / 35.

- W1 (must) Text contradicts appendix (Opus direct 0.05 not 0; relay 9–28% not 5–39%; ablation ranges; oracle range omits Haiku 0.39; "six models" overreach; non-oracle only Opus/Sonnet). → generate every number from scripts; state model/item coverage per claim.
- W2 (must) On silent-wrong, explicitness is WORSE (Sonnet card+resolver 0.00 → explicit+card+resolver 0.19; Haiku 0.02→0.30): explicitness turns asks into confident actions, ~30% sender inferences wrong. → reframe as accuracy–safety trade-off; hybrid ask-on-low-confidence protocol; cost-weighted utility.
- W3 (must) Sender-message claim observational/post-treatment; "bare → 0%" near-definitional; wrong-unit n≈11. → counterfactual message injection (bare/own/wrong/hedged) on the receiver.
- W4 (must) Ablation incomplete & unpaired; oracle cell from different items. → same 172 items for all cells incl. oracle; McNemar; Haiku + non-Anthropic sender; cross-model pairs.
- W5 (must) Missing typed-schema baseline (mandatory unit field). 
- W6 (must) Same-convention control untested for the non-oracle protocol.
- W7 (must) Message coder validity (it is a deterministic regex coder — say so; validate on a sample); per-concept results (price = FX).
- W8 (nice) One template per concept; Ling n small; Claude transcript rendering.
Prior work to add: "On Generalization across Measurement Systems" (arXiv:2506.02591); agent ToM / interlocutor awareness (EMNLP 2025); adaptive ToM coordination (arXiv:2603.16264). "Faithful, Not Corrective" makes wrong-unit unrecoverability expected.

## Actions (2026-10-04)
- W2/W3/W4/W5/W6: run_ablation.py gained inject:{bare,own,wrong,hedged}, typed, hybrid; queue_L4b.sh runs injection on 4 receivers, typed/hybrid/oracle/none on the same items for Opus/Sonnet, non-oracle same-convention controls, Haiku cells.
- First observation: typed JSON with mandatory unit → Haiku sender fills the wrong unit ("1200 USD" for a Brazilian principal): the bottleneck is sender inference, not channel format.
