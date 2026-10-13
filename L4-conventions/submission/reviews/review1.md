# Review 1 (independent ARR-style reviewer agent, 2026-10-04, on interim for_review.md)
Scores: Soundness 2.5, Excitement 2.5, Overall 2.5 (borderline Findings), confidence 4. Theme fit: yes.
Odds as is: Main 5% / Findings 22% / Reject 73%. With must-fixes: 15 / 40 / 45.

Weaknesses (ranked) and remedies:
- W1 (must) Fix uses the ORACLE locale in the card and a prompt that names the failure; CAPRI paper (arXiv:2606.17688) already shows explicit/sequential prompting closes the infer-vs-apply gap. → card from sender-inferred locale; generic-caution prompt control; full factorial (explicit-only, card-only, resolver-only).
- W2 (must) "Both sides complementary" contradicted: Haiku worse with explicit+card+resolver than card+resolver; Opus card+resolver weak. → factorial with per-model effects; inspect Haiku explicit traces.
- W3 (must) Asking counted as failure. → report safe rate (correct+asked); headline silent-wrong; justify when asking is unnecessary.
- W4 (must) Harness confound (CLI system prompts, default temps, transcript rendering, GPT different harness). → raw-API replication on ambiguous subset, temp 0, native multi-turn. [Note: our CLI runs fully replace the system prompt and disable built-in tools; must state this.]
- W5 (must) Small n, naive stats, abstract/appendix mismatch. → all items, 3 seeds, bootstrap clustered by culture×concept, McNemar; regenerate numbers.
- W6 (must) Same-convention controls small and imperfect (0.62–0.80). → enlarge; report over-conversion vs asking.
- W7 (nice) One template per concept, unit exposed in tool signature. → 3–5 paraphrases; unit only in description; one realistic multi-step task.
- W8 (nice) Same model both sides; GPT lacks fix conditions; no open-weight. → cross-model pairs; open-weight model; complete GPT.
- W9 (must) Cites unreported anonymous-model analysis. → redo sender first-message coding on reported models.

Prior work to cite/contrast: CAPRI paper (Miao, Zhu & Shwartz 2026, arXiv:2606.17688); "Faithful, Not Corrective" (arXiv:2607.09678, relays propagate errors); MAST (Cemri et al. 2025; verify the 37% figure); NUMCoT (arXiv:2406.02864; report conversion accuracy when unit known); A2A agent cards have no locale field.

## Actions taken (2026-10-04)
- W1/W2/W6/W7/W8: capri/run_ablation.py + go_ablation.sh (Opus & Sonnet factorial on all ambiguous items incl. inferred-locale card and generic control; enlarged same-convention controls; Opus↔Haiku cross pairs; unit-in-description variant; GPT fix conditions).
- W8/W4 (partial): open-weight Ling-3.1-flash via native multi-turn chat API (capri/run_or.py).
- W3/W5/W9: analysis (safe rate, clustered CIs, McNemar, sender first-message coding) in capri/analyze_frontier.py.
