#!/bin/zsh
# EXPERIMENT_PLAN.md B + C (2026-10-08): Sonnet reruns and gap fills, pinned model IDs.
# Both runners skip completed rows, so the loop re-runs the whole queue until no session-limit errors remain.
cd "$(dirname "$0")"
export OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-unused-claude-cli-only}  # llm.py needs a key at import; these runs use the CLI only
S=claude-sonnet-5; O=claude-opus-5-5; H=claude-haiku-4-5-20251001
INJ="inject:bare,inject:own,inject:wrong,inject:hedged"
FACT="none,explicit,card,resolver,generic,inferred+resolver,explicit+inferred+resolver,explicit+card+resolver"
SAME="none,explicit+card+resolver,explicit+inferred+resolver"
queue() {
  # B: Sonnet reruns
  python3 run_claude.py $S 2 direct,none,card+resolver,explicit+card+resolver 4
  python3 run_ablation.py $S $S "$INJ" --amb --step 2 --workers 4
  python3 run_ablation.py $S $S "$FACT" --amb --step 2 --workers 4
  python3 run_ablation.py $S $S "$SAME" --amb --same --step 2 --workers 4
  # C: gap fills (cross pairs keep the alias names of their existing rows; Opus/Haiku drift-checked stable)
  python3 run_ablation.py opus haiku "none,explicit+card+resolver,explicit+inferred+resolver" --amb --step 2 --workers 4
  python3 run_ablation.py haiku opus "none,explicit+card+resolver,explicit+inferred+resolver" --amb --step 2 --workers 4
  python3 run_ablation.py $H $H "$FACT" --amb --step 2 --workers 4
  python3 run_ablation.py $O $O "$SAME" --amb --same --workers 4
}
# a pass needs another try only if rows written during it hit the session limit (old failed rows stay in the files)
F=(results_ablation.jsonl results_frontier_$S.jsonl); touch $F
newhits() { local h=0; for k in 1 2; do h=$((h + $(tail -n +$((${n0[$k]} + 1)) ${F[$k]} | grep -c "session limit"))); done; echo $h; }
for i in {1..12}; do
  n0=($(wc -l < ${F[1]}) $(wc -l < ${F[2]})); queue
  hits=$(newhits)
  if [ "$hits" -eq 0 ]; then echo "queue complete (pass $i)"; break; fi
  echo "pass $i: $hits session-limit errors; sleeping 45 min"; sleep 2700
done
