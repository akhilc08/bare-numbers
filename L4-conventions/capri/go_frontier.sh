#!/bin/zsh
cd "$(dirname "$0")"
python3 run_claude.py opus 2 direct,none,card+resolver,explicit+card+resolver 4 > log_frontier_opus.txt 2>&1 &
python3 run_claude.py haiku 2 direct,none,card+resolver,explicit+card+resolver 4 > log_frontier_haiku.txt 2>&1 &
python3 run_claude.py claude-fable-5-1 2 direct,none,card+resolver,explicit+card+resolver 4 > log_frontier_fable.txt 2>&1 &
python3 run_claude.py gpt-6.1-sol 6 direct,none 2 > log_frontier_gpt.txt 2>&1 &
wait
