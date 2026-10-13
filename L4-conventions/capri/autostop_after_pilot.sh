#!/bin/zsh
# Stops master_L4.sh as soon as it finishes the method pilot (E1) and starts the held-out test (E2), which the co-author
# runs on his own account (CO_AUTHOR_RUN.md). Any held-out rows written from this account in the gap are set aside.
cd "$(dirname "$0")"
until grep -q "E2_claude-opus-5-5: pass 1" logs/master.log; do sleep 5; done
pkill -f "[m]aster_L4.sh"; sleep 2; pkill -f "[r]un_e2e.py claude-opus-5-5 claude-opus-5-5"; sleep 3
python3 - <<'EOF'
import json
rows = [json.loads(l) for l in open("results_e2e.jsonl")]
held = [x for x in rows if x.get("split") == "heldout"]
if held:
    with open("quarantine_heldout_from_robert_account.jsonl", "a") as fh:
        fh.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in held)
with open("results_e2e.jsonl", "w") as fh:
    fh.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in rows if x.get("split") != "heldout")
print("set aside", len(held), "held-out rows written from this account")
EOF
echo "[$(date '+%F %T')] auto-stop: pilot (E1) done; stopped before E2 (co-author runs E2 onward)" | tee -a logs/master.log
