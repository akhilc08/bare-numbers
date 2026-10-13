#!/bin/zsh
cd "$(dirname "$0")"
python3 run_frontier.py opus opus 6 3 > log_opus_opus.txt 2>&1 &
python3 run_frontier.py sonnet sonnet 6 3 > log_sonnet_sonnet.txt 2>&1 &
python3 run_frontier.py haiku haiku 6 3 > log_haiku_haiku.txt 2>&1 &
python3 run_frontier.py claude-fable-5-1 claude-fable-5-1 6 3 > log_fable_fable.txt 2>&1 &
python3 run_frontier.py sonnet gpt-6.1-sol 3 2 > log_sonnet_gpt.txt 2>&1 &
python3 run_frontier.py gpt-6.1-sol opus 3 2 > log_gpt_opus.txt 2>&1 &
wait
