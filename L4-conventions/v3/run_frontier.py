"""L4 v3 on frontier models: same cases/conditions/checkers as run.py, sender and receiver set independently
(heterogeneous pairs). Claude via `claude -p` (receiver tool served natively by mock_mcp.py), OpenAI via `codex exec`.
The CLIs take one prompt, so the dialogue so far is rendered as a transcript each turn (as in capri/run_claude.py).
Usage: python run_frontier.py SENDER RECEIVER [REPS] [WORKERS]; results append to results_frontier.jsonl (resumable)."""
import sys, json, os, random, threading
sys.path.insert(0, os.path.abspath("../../_lib")); import llm, claude_mcp, codex_mcp
from run import C, RESOLVE, SENDER
OUT = "results_frontier.jsonl"; LOCK = threading.Lock()
B = lambda m: codex_mcp if m.startswith("gpt") else claude_mcp
render = lambda dlg, me, other: "\n".join(f"{me if r == 'me' else other}: {t}" for r, t in dlg)


def run(a):
    ck, cond, k, sm, rm = a
    p, msg, sb, tool, ok, dev = C[ck]
    sb = sb + " Today is 2026-10-03."
    loc = p.split("(")[1].split(";")[0].rstrip(")")
    if cond in ("card", "card+resolver"): sb += f"\n\n[Agent card of the counterpart] principal_locale: {loc}"
    if cond == "card+resolver": sb += "\n\n" + RESOLVE
    sa = SENDER.format(p=p) + " Reply with only the message text to send to the other agent."
    who = p.split(" (")[0]
    base = {"case": ck, "set": "dev" if dev is True else ("heldout" if dev is False else "control"), "cond": cond, "k": k, "sender": sm, "receiver": rm}
    dlg, got, turns, first = [], {}, 0, None  # dlg entries: ("A"|"B", text)
    for _ in range(4):
        hist = "\n".join(f"{'You' if r == 'A' else 'Other agent'}: {t}" for r, t in dlg)
        pa = f"[From {who}]: {msg}\n\n(You are connected to the other agent.)\n" + (f"[Dialogue with the other agent so far]\n{hist}\n\n" if dlg else "") + \
             ("Write your next message to the other agent." if dlg else "Send your first message to it.")
        ra = B(sm).episode(sa, pa, model=sm, max_turns=2)
        if ra["error"] or not ra["text"].strip(): return dict(base, error=(ra["error"] or "empty sender")[:300])
        am = ra["text"].strip(); first = first or am; dlg.append(("A", am))
        hist = "\n".join(f"{'Other agent' if r == 'A' else 'You'}: {t}" for r, t in dlg)
        rb = B(rm).episode(sb, f"[Conversation with the other agent]\n{hist}\n\nRespond to the other agent, or use your tool to act.", [tool], model=rm, max_turns=4)
        if rb["error"] and not rb["calls"]: return dict(base, error=rb["error"][:300])
        if rb["calls"]:
            got = rb["calls"][0]["arguments"]; break
        turns += 1; dlg.append(("B", rb["text"].strip()))
    try: good = bool(ok(got)) if got else False
    except Exception: good = False
    locale_in_msg = any(w.lower() in (first or "").lower() for w in [loc.split(",")[0], loc.split(",")[-1].strip()])
    return dict(base, error=None, correct=good, acted=bool(got), asked=turns > 0, silent_wrong=bool(got) and not good and turns == 0,
                sender_mentions_locale=locale_in_msg, sender_first=(first or "")[:400], args=got)


def logged(a):
    r = run(a)
    with LOCK, open(OUT, "a") as fh: fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return r


if __name__ == "__main__":
    sm, rm = sys.argv[1], sys.argv[2]
    reps = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            x = json.loads(l)
            if not x.get("error"): done.add((x["case"], x["cond"], x["k"], x["sender"], x["receiver"]))
    jobs = [(c, d, k, sm, rm) for c in C for d in ["none", "card", "card+resolver"] for k in range(reps) if (c, d, k, sm, rm) not in done]
    random.Random(0).shuffle(jobs)
    print(sm, "->", rm, len(jobs), "jobs", flush=True)
    res = llm.pmap(logged, jobs, workers=workers)
    print("errors:", sum(bool(r.get("error")) for r in res), "of", len(res), flush=True)
