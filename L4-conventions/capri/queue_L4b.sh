#!/bin/zsh
# Review-2 must-fixes (3 workers; runs alongside go_ablation.sh and queue.sh to stay under the process cap)
cd "$(dirname "$0")"
INJ="inject:bare,inject:own,inject:wrong,inject:hedged"
for m in opus sonnet haiku claude-fable-5-1; do python3 run_ablation.py $m $m "$INJ" --amb --step 2 --workers 3; done
for m in opus sonnet; do
  python3 run_ablation.py $m $m "typed,inferred+resolver+hybrid,explicit+inferred+resolver+hybrid,explicit+card+resolver,none" --amb --workers 3
  python3 run_ablation.py $m $m "explicit+inferred+resolver+hybrid" --amb --same --workers 3
done
python3 run_ablation.py haiku haiku "explicit,explicit+inferred+resolver,explicit+inferred+resolver+hybrid,typed,none" --amb --step 2 --workers 3
