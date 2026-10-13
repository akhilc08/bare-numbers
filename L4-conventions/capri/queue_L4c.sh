#!/bin/zsh
# Resume the review must-fix cells cut off by the CLI session limit (2026-10-05). Order (2026-10-07, after the
# side-chat plan): cross-model pairs, Haiku explicit cells (headline: explicit units -> confident errors),
# non-oracle same-convention controls, then the Sonnet typed/hybrid cells.
# run_ablation.py skips completed (file, cond, same, sender, receiver) rows, so this is safe to re-run.
# CLI aliases resolved 2026-10-07: haiku=claude-haiku-4-5-20251001, sonnet=claude-sonnet-5, opus=claude-opus-5-5.
cd "$(dirname "$0")"
export OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-unused-claude-cli-only}  # llm.py needs a key at import; these runs use the CLI only
python3 run_ablation.py opus haiku "none,explicit+card+resolver,explicit+inferred+resolver" --amb --step 2 --workers 4
python3 run_ablation.py haiku opus "none,explicit+card+resolver,explicit+inferred+resolver" --amb --step 2 --workers 4
python3 run_ablation.py haiku haiku "explicit,explicit+inferred+resolver,explicit+inferred+resolver+hybrid,typed,none" --amb --step 2 --workers 4
python3 run_ablation.py opus opus "none,explicit+card+resolver,explicit+inferred+resolver,explicit+inferred+resolver+hybrid" --amb --same --workers 4
python3 run_ablation.py sonnet sonnet "explicit+inferred+resolver+hybrid" --amb --same --workers 4
python3 run_ablation.py sonnet sonnet "typed,inferred+resolver+hybrid,explicit+inferred+resolver+hybrid,explicit+card+resolver,none" --amb --workers 4
