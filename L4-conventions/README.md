# L4: Bare Numbers Between Agents (start here)

**Target:** NAACL 2027 theme track ("Language as a Medium for Agentic Communication"), ARR deadline **Oct 12, 2026**. Last updated Oct 8.

## The paper in one paragraph
A personal agent delegates a request to another organisation's agent, for example "my budget is 300,000" from a Korean user to a US store's agent. The number arrives intact; its unit doesn't. The data and answer key come from **CAPRI** (Miao, Zhu & Shwartz 2026): conversations where the user's culture shows only through implicit cues.

**Claims:**
1. Single agents and plain relays fail: the number is copied, the convention is lost.
2. The sender's message decides the outcome. Shown by swapping in fixed sender messages.
3. The standard fix, telling the sender to state units (CAPRI's own recommendation), backfires next to receiver-side safeguards. It suppresses the sender's doubt, and the forced guess often defaults to US units.
4. **Main claim:** a grounding protocol beats published baselines on a delegation evaluation built on CAPRI, on accuracy and safety together.
   - The sender cites the cue and sends value, unit, locale and confidence, and asks its principal when unsure.
   - The receiver cross-checks the unit against the locale.
   - The receiver reads back the converted value, and the sender confirms.

**Hard rule:** no self-built evaluation cases. CAPRI's conversations, cues and unit key are the data; the request templates and values are a fixed test setting.

## Status at a glance
| | What | Status |
|---|---|---|
| Literature review | 5 research notes + report, 19 key papers | ✅ `lit_review/`, `papers/` |
| Claims 1–3 | 6 models (Opus, Sonnet, Haiku, Fable, GPT-6.1, Ling), Oct 3–5 | ✅ clean data in `capri/results_*` |
| Mechanism analyses | doubt suppression, wrong-unit assertions, number fidelity | ✅ `capri/analysis_messages.txt` |
| Method + simulated principal | `capri/run_e2e.py`, frozen at commit `41fe4f2` | ✅ |
| Held-out test split | 168 CAPRI chats from scaffolds unseen in development | ✅ `capri/heldout.json` |
| **E1 method pilot** (development set) | Opus + Sonnet, 12 conditions, 2,016 runs | ✅ `capri/analysis_e2e_dev.txt` |
| **E2 held-out test** (the main result) | Opus, Sonnet, Haiku × 9 conditions + same-unit controls, ~5,300 runs | ⏳ **co-author to run** |
| B–G follow-ups | Sonnet reruns, gap fills, sender-only probe, Fable/GPT, repeat runs, ~6,000 runs | ⏳ co-author, after E2 |
| Paper draft | outline below | ⏳ not started |

## What's next, in order
1. **Co-author: start the remaining runs today.** One command; see [`CO_AUTHOR_RUN.md`](CO_AUTHOR_RUN.md).
   - It runs E2 first, then the follow-ups, and sleeps through usage limits.
   - At ~1,500 runs/day on Robert's plan, E2 alone would take 3–4 days. A larger plan should be faster, but **E2 is the critical path for Oct 12**.
   - The pipeline already runs E2 before anything else.
2. **Write the paper in parallel.** Sections 1–5 below can be drafted now from finished results. Section 6 waits for E2.
3. **When E2 is done:** run `cd capri && python3 analyze_e2e.py --split heldout --file results_e2e_coauthor.jsonl` and decide the headline. See "Open question for the headline" below.
4. **Decisions needed (co-author + Robert):**
   - **Number grid:** varying request values per concept from external sources. Does a pre-committed grid count as self-built? It is not needed for Oct 12.
   - **Hand-labeling (optional):** 150 sender messages, ~1 h, `capri/annotation/sheet.csv`. It validates the message classifier used in the mechanism analyses. The main claim doesn't depend on it.
   - **Ling, the open-weight model (optional):** needs the OpenRouter key restored (small cost).

## Results so far
### E1 method pilot (development set; correct / silently wrong; 84 items per cell; `capri/analysis_e2e_dev.txt`)
| Condition | Opus 5.5 | Sonnet 5 |
|---|---|---|
| **Method** (ground + cross-check + read-back) | **96% / 1%** | **100% / 0%** |
| Hybrid confidence channel | 95% / 0% | 96% / 2% |
| Explicit + inferred locale + resolver | 92% / 0% | 95% / 5% |
| Explicit units (CAPRI's explicit prompting) | 82% / 0% | 95% / 5% |
| Typed JSON (mandatory unit field) | 75% / 0% | 80% / 17% |
| CAPRI's own fix (Pragmatic CoT) | 64% / 35% | 74% / 26% |
| Receiver asks when unsure (Matsnev 2026) | 71% / 21% | 55% / 42% |
| Plain relay | 65% / 35% | 60% / 40% |
| Ablation: grounding only | 85% / 0% | 99% / 0% |
| Ablation: no grounding (cross-check + read-back) | 93% / 0% | 81% / 18% |

**Settled:**
- The method beats CAPRI's fix, the plain relay, Matsnev and typed JSON by large, significant margins.
- CAPRI's published fix does not carry over to delegation: it leaves 26–35% silent errors.

**Open question for the headline:**
- Against the two strongest baselines the method ties on accuracy.
- On cost-weighted utility (questions and escalations to the human are costed) it wins on Sonnet. It loses on Opus to the hybrid, which escalates less.
- E2 decides whether the claim is "beats all baselines" or "matches the best at lower cost on some models".

### Mechanism, from the clean Oct 3–5 runs (`capri/analysis_messages.txt`)
- **Number intact, meaning lost.** Senders copy the number verbatim 99–100% of the time, yet plain relays are correct only 12–30% of the time. This answers the closest prior work, *Faithful, Not Corrective*.
- **Explicit-unit prompts suppress doubt.** Senders admitting they don't know the unit: Opus 33% → 2–3%, Fable 23% → 0%, Ling 31% → 11%.
- **Suppressed doubt becomes wrong-unit assertions.** Opus ~10%, Haiku 42%. These end silently wrong ~100% of the time, even when the receiver's agent card shows the right country.
- **Plausibility acts on the sender.** Under explicit prompts, Opus never asserts a wrong currency when the budget would be absurd in dollars (0/18), but does when it would be plausible (7/36). Small n.

## Paper outline (draft narrative)
1. **Problem.** Delegation across organisations; protocols carry no unit or locale. A2A has no locale field, and MCP's locale proposal was closed unmerged. Mars Climate Orbiter as the analogy.
2. **Single agents fail.** This replicates CAPRI's infer-but-don't-apply finding in tool calls: 0–5% correct.
3. **Where it's lost.** The number is copied verbatim; injected sender messages decide the outcome.
4. **The standard fix backfires.** Explicitness suppresses doubt, the forced guess defaults to US units, and receivers trust stated units.
5. **Method.** Ground, cross-check, read back. Each step targets a measured failure.
6. **Evaluation.** End-to-end with a simulated principal, cost-weighted scoring and a held-out CAPRI split. *(Waits for E2.)*
7. **Analysis.** Step ablations (from E1), same-unit controls, cross-model pairs, per-model behaviour such as Opus refusing FX conversion.
8. **Limitations.** Harness (see below), fixed templates, three ambiguous concepts.

Related work, novelty threats and positioning lines are in `lit_review/report.md`.

## Caveats a reviewer will ask about
- **Harness.** Since ~Oct 6 the subscription CLI injects the logged-in account's email, today's date and an environment section into every run, even with the system prompt replaced (`capri/QUARANTINE.md`).
  - The Oct 3–5 runs predate this.
  - Newer runs add a note telling agents to ignore it.
  - Comparisons between conditions within one account are valid, so whole stages run on one account. Absolute US-default rates come from the Oct 3–5 data.
- **Sonnet's old rows** (Oct 3–5, `sonnet` alias) come from an unknown model version. New Sonnet runs use the pinned `claude-sonnet-5`.
- **Other limitations:** one request template per concept; price bands depend on exchange rates (±12%); dialogues are rendered as transcripts for the CLI (no native multi-turn).

## Where things are
| Path | What |
|---|---|
| `EXPERIMENT_PLAN.md` | Detailed plan, setup decisions, change log |
| `CO_AUTHOR_RUN.md` | How to run the remaining experiments on your plan |
| `lit_review/report.md`, `lit_review/notes/` | Literature review |
| `papers/` | 19 key related papers (PDF) with an index |
| `submission/` | Earlier draft (`for_review.md`) and three mock reviews |
| `capri/run_e2e.py` | Method, baselines, simulated principal (E1, E2, F, G) |
| `capri/run_ablation.py`, `run_claude.py` | Original conditions (claims 1–3; B, C) |
| `capri/run_probe.py` | Sender-only probe (D) |
| `capri/pipeline.sh`, `harness_env.sh` | Stage-selectable runner; harness setup |
| `capri/analyze_e2e.py`, `analyze_messages.py`, `analyze_frontier.py` | Analyses |
| `capri/results_*.jsonl` | Raw results (`*_coauthor` = co-author's account) |
| `capri/quarantine_*` | Runs excluded from analysis (reasons in `QUARANTINE.md`) |
| `run.py`, `prereg*/`, `fixes/`, `v3/`, `results.md` | **Old "Lost in Convention" work on hand-built cases. Not used** (no-self-built rule) |
