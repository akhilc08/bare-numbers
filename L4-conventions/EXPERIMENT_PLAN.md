# L4 experiment plan (2026-10-08)

**Main claim.** On a delegation evaluation built on CAPRI, a grounding protocol beats published methods on accuracy and safety at once.

**Supporting claims.**
1. Single agents and plain relays fail.
2. The sender's message decides the outcome.
3. Telling senders to state units backfires next to receiver-side fixes. It suppresses the sender's doubt, and the forced guess defaults to US units.

## Setup decisions (object if you disagree)
- **Data.** From CAPRI: the conversations, culture labels and unit key. Ours, as before: the request templates, values and acceptance bands.
- **Exclusions.**
  - Iranian prices: official and market exchange rates differ about 10×.
  - Temperature and size serve as controls only.
  - CAPRI has no UK distance chats at all (864 = 96 scaffolds × 9 cultures), so its odd "km" key entry for UK distance is never used.
- **Development / held-out split.**
  - Development set: the 168 items used so far.
  - Test set: 168 new CAPRI chats (6 per culture × concept, fixed seed) from the full release, drawn only from conversation scaffolds never used in the development set (`capri/make_split.py` → `capri/heldout.json`).
  - The method and analysis are committed to git before the test run.
- **Models.** Pinned IDs: `claude-opus-5-5`, `claude-sonnet-5`, `claude-haiku-4-5-20251001`, plus `claude-fable-5-1` and GPT-6.1 (Codex CLI) if quota allows.
  - Harness: headless Claude Code CLI (`claude -p`), system prompt replaced, built-in tools off.
  - No paid API.
- **Harness problem found Oct 8 (see `capri/QUARANTINE.md`).** The subscription CLI now injects a user-context block into every `claude -p` run, even with the system prompt replaced: the account email (a US university address), today's date and an environment section naming the model.
  - Runs launched from inside an agent session also inherit that session's environment, and runs started inside the repo also get the project memory.
  - The US email is a confound for a study of US-default units. 0 of 5,019 rows from Oct 3–5 mention it; 14 of ~500 rows from Oct 7–8 do.
  - `--bare` removes the block but needs a paid API key.
  - **Fix used:** every run is launched from a plain terminal with `source capri/harness_env.sh`. That clears inherited agent variables and adds a note telling every agent that any email, date or environment details belong to the test setup. Episodes run in a temp folder (no project memory).
  - All 2,562 rows written Oct 7–8 are quarantined, not used.
- **Decision (Robert, Oct 8): run on the subscription anyway, launched from a headless terminal.** The verification failed: Sonnet was silently wrong on 33% of items vs 0% on the same items Oct 4–5, and 5 runs mentioned the email. A paid API key was declined.
  - Consequences for the paper:
    - Comparisons *between conditions* within the new runs are valid, because the injected block is identical in every run. The method-vs-baselines claim rests on these.
    - Absolute "US-default" rates in the new runs are confounded by the US email. The mechanism claim leans on the clean Oct 3–5 data.
    - The new runs are reported as a separate harness, and the injected block is stated as a limitation.
  - The note was strengthened to say the email belongs to the operator and must not be used.
- **Sonnet drift: not established.** The Oct 8 "Sonnet changed" result (3% → 53% silent errors) was measured under the contaminated harness. A verification rerun with the fix decides whether the Oct 4–5 Sonnet results are usable. Pass if silent errors are at most 15% and no agent mentions the email. Opus and Haiku looked stable even under contamination.
- **Held for the co-author.** Varying request values per concept and matching requests to each chat's object. The open question is whether a pre-committed value grid counts as self-built.

## Experiments
Run order overnight: harness verification → E1 → E2 → B → C → D → F → extra repeats of E2 (reliability). The method claim goes first because it is the main claim. The method is frozen and committed before E1, and E2 uses the same frozen version, so the held-out result is not tuned.

| | What | Size (episodes) |
|---|---|---|
| A | **Free analyses of existing logs.** Fix the sender-message coder (unit stated first vs conversion gloss). Six mutually exclusive outcomes. Number-copied vs value-correct table. Sender doubt analysis. Plausibility on the sender side. A 150-message sheet for **human validation (both authors, ~1 h)**. | 0 |
| B | **Sonnet reruns (pinned).** Direct / relay main table, message injection, explicitness factorial, same-unit controls. | ~1,300 |
| C | **Gap fills.** Haiku explicitness cells, Opus same-unit controls for explicit protocols, Opus↔Haiku cross pairs. | ~1,000 |
| D | **Mechanism tests.** Sender-only probe ("what unit does your principal mean?", no counterpart). Principal states the unit ("₩300,000"), separating inference from conversion. | ~750 |
| E1 | **Method pilot (development set).** Opus and Sonnet × 11 conditions (7 baselines, full method, 3 ablations) × 84 items. One revision allowed, then frozen and committed. | ~1,850 |
| E2 | **Method test (held-out).** Opus, Sonnet, Haiku × method + 7 baselines × 168 items, plus same-unit controls. | ~4,800 |
| F | **Optional breadth.** Fable and GPT-6.1 on method vs best baselines (held-out subset). Open-weight Ling-3.1 only if the OpenRouter key is restored (priced before running). | small |

### Log of changes after the plan was written
- **Oct 8, 02:24.** Asking the sender to "write your reasoning" tripped Opus 5.5's reasoning-extraction safeguard: 14 refusals in the first 45 runs, all in the pcot and ground conditions. The scratch part is now a short "NOTES:" line, and only the message is sent. This is the freeze point for all overnight runs (commit `41fe4f2`). The 16 rows written under the old wording are set aside.

### E: method vs baselines
**Setup.** End-to-end with a simulated principal (`capri/run_e2e.py`). It knows its own value and unit, answers only questions about the unit or what the number means, and can be reached through the sender (at most 2 escalations per episode).
- The task deliberately gives no booking references. A smoke test showed agents looping on logistics, so all conditions tell both agents the booking is already handled. Every condition gets the same principal access and the same logistics line.

**Baselines.**
- Plain relay.
- State units (CAPRI's explicit prompting).
- Pragmatic CoT sender (CAPRI's fix).
- Typed JSON with a mandatory unit field.
- Receiver asks when its own uncertainty ≥ 0.5 (Matsnev 2026).
- Hybrid confidence channel.
- Best current combination (explicit + inferred locale + resolver).

**Method.**
1. The sender grounds. It cites the cue and sends value, unit, locale tag and confidence, and asks its principal when unsure.
2. The receiver cross-checks the unit against the locale and against plausibility.
3. The receiver reads back the converted value, and the sender confirms.

Ablations remove one step each.

**Metrics.**
- Six outcomes: correct; silently wrong; asked → correct; asked → wrong; unnecessary ask on a same-unit control; gave up.
- Agent turns, and escalations to the principal.
- Cost-weighted utility swept over question costs.
- Regret against "ask only when the unit actually mismatches".

## Not running
- CAPRI's own image task (secondary at most).
- Native-API replication: paid, so transcript rendering stays a stated limitation.
- Latent channels or training.

## Budget
About 10,000 episodes on the Claude subscription across several session windows. Runs auto-resume after session-limit resets.

Priority order means a partial finish still supports the paper: A–D cover claims 1–3; E is the method claim.
