#!/bin/zsh
# Rebuild submission/for_review.md = draft + live numbers from the CAPRI frontier result files
cd "$(dirname "$0")/.."
{ cat submission/draft.md; echo; echo "## Appendix A: live results (capri/analyze_frontier.py, $(date '+%Y-%m-%d %H:%M'))"; echo '```'; (cd capri && python3 analyze_frontier.py); echo '```'; } > submission/for_review.md
