# Running the remaining L4 experiments on your own Claude plan

You need macOS or Linux with zsh, `python3` (standard library only) and Claude Code logged in to **your** plan. No API key is needed.

1. Get the code:
   ```bash
   git pull
   cd experiments/good-ideas/L4-conventions/capri
   claude --version          # Robert's runs used 2.1.281; note yours
   ```
2. **Start it from a plain terminal, not from inside a Claude Code or agent session.** A child `claude -p` started by an agent inherits that agent's context.
   ```bash
   source harness_env.sh && RESULTS_TAG=_coauthor STAGES="E2 B C D F G" ./pipeline.sh
   ```
   - It runs the held-out test (E2), then the Sonnet reruns (B), gap fills (C), sender-only probe (D), Fable/GPT (F) and repeat runs (G). See `EXPERIMENT_PLAN.md`.
   - When your usage limit hits, it sleeps 30 minutes and resumes by itself. Leave the terminal open.
3. Keep the machine awake (second terminal tab):
   ```bash
   caffeinate -is -w $(pgrep -f "[p]ipeline.sh" | head -1)
   ```
4. Check progress: `tail capri/logs/pipeline_coauthor.log`
5. Commit and push your results whenever convenient (they never overwrite Robert's):
   ```bash
   git add capri/results_*_coauthor.jsonl capri/logs && git commit -m "L4: co-author runs" && git push
   ```

## Why the tag matters
The subscription CLI injects the logged-in account's email and today's date into every run, so your runs and Robert's are slightly different harness contexts. Run **whole stages** on one account: every condition and every model of the held-out test comes from you. Never mix accounts within one results table. Don't edit the scripts. If your plan lacks a model (e.g., Fable), that step fails and the pipeline moves on.
