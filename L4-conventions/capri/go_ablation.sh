#!/bin/zsh
# Review-1 must-fixes, in priority order. Ambiguous subset (speed/distance/price), all items.
cd "$(dirname "$0")"
F="explicit,card,resolver,generic,inferred+resolver,explicit+inferred+resolver"
for m in opus sonnet; do
  ( python3 run_ablation.py $m $m "$F" --amb --workers 2
    python3 run_ablation.py $m $m "none,explicit+inferred+resolver,explicit+card+resolver" --amb --same --workers 2 ) > log_ablation_$m.txt 2>&1 &
done
wait
( python3 run_ablation.py opus haiku "none,explicit+card+resolver,explicit+inferred+resolver" --amb --step 2 --workers 2 &
  python3 run_ablation.py haiku opus "none,explicit+card+resolver,explicit+inferred+resolver" --amb --step 2 --workers 2 &
  python3 run_ablation.py opus opus "desc+direct,desc+none" --amb --step 2 --workers 2 &
  wait ) > log_ablation_p2.txt 2>&1
python3 run_ablation.py gpt-6.1-sol gpt-6.1-sol "explicit+card+resolver,explicit+inferred+resolver" --amb --step 3 --workers 2 > log_ablation_gpt.txt 2>&1
