"""L4 method: explicit convention-resolution step before acting (receiver-side), with and without the locale card."""
import sys, json, os, importlib.util
sys.path.insert(0, os.path.abspath("../../_lib")); import llm
src = open("run.py").read().split("CONDS =")[0]; exec(src)
RESOLVE = ("Before acting, list every locale- or convention-dependent expression in the other agent's request (dates, times, floors, sizes, units, "
           "currency symbols, fiscal years, number formats). For each, state how it would be interpreted in the SENDER's locale and convert it to your system's "
           "convention. If the sender's locale is unknown and an expression is ambiguous, ask. Then act on the converted values.")
def run2(a):
    ck, cond, k = a
    C, loc = CASES[ck]; t = C[ck]; sa, sb, tool, ok = t[0], t[1], t[2], t[3]
    if "card" in cond: sb += f"\n\n[Agent card of the counterpart] principal_locale: {loc}"
    if "resolver" in cond: sb += "\n\n" + RESOLVE
    A = [{"role": "system", "content": sa}, {"role": "user", "content": "(Connected to the other agent.) Send your first message."}]
    B = [{"role": "system", "content": sb}]
    got = {}; turns = 0
    for _ in range(4):
        am = llm.chat(A, temperature=1.0, model=B_)
        if am.get("error"): return None
        am = am.get("content") or ""; A.append({"role": "assistant", "content": am}); B.append({"role": "user", "content": am})
        bm = llm.chat(B, tools=[tool], temperature=1.0, model=B_)
        if bm.get("error"): return None
        if bm.get("tool_calls"):
            try: got = json.loads(bm["tool_calls"][0]["function"]["arguments"] or "{}")
            except Exception: got = {}
            break
        turns += 1; bt = bm.get("content") or ""; B.append({"role": "assistant", "content": bt}); A.append({"role": "user", "content": bt})
    try: good = bool(ok(got)) if got else False
    except Exception: good = False
    return {"case": ck, "cond": cond, "correct": good, "asked": turns > 0}
CONDS2 = ["resolver", "card+resolver"]
res = [x for x in llm.pmap(run2, [(c, d, k) for c in CASES for d in CONDS2 for k in range(8)], workers=40) if x]
json.dump(res, open("results_resolver.json", "w"), indent=1)
print("case".ljust(20), *[d.ljust(14) for d in CONDS2])
for c in CASES: print(c.ljust(20), *[("%.2f" % (sum(x["correct"] for x in res if x["case"] == c and x["cond"] == d)/max(1, sum(1 for x in res if x["case"] == c and x["cond"] == d)))).ljust(14) for d in CONDS2])
print("MEAN".ljust(20), *[("%.2f" % (sum(x["correct"] for x in res if x["cond"] == d)/sum(1 for x in res if x["cond"] == d))).ljust(14) for d in CONDS2])
print("asked".ljust(20), *[("%.2f" % (sum(x["asked"] for x in res if x["cond"] == d)/sum(1 for x in res if x["cond"] == d))).ljust(14) for d in CONDS2])
