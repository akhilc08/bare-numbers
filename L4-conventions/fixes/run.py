"""L4 method: protocol-level locale metadata (agent-card style) vs prompt fix vs both, on the hardest conventions."""
import sys, json, os, importlib.util, collections
sys.path.insert(0, os.path.abspath("../../_lib")); import llm
def load(p):
    s = importlib.util.spec_from_file_location(p.replace("/", "_"), p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
M1 = load("../run.py"); M2 = load("../prereg/run.py"); M3 = load("../prereg2/run.py")
B_ = "stealth/space-bunny-alpha"
CASES = {"uk_first_floor": (M1.C, "London, United Kingdom"), "uk_date": (M1.C, "London, United Kingdom"), "half_six_de": (M1.C, "Berlin, Germany"),
         "uk_pint_recipe": (M2.C, "Manchester, United Kingdom"), "de_ground_floor_one": (M2.C, "Munich, Germany"),
         "cad_dollar": (M3.C, "Toronto, Canada"), "kmh_speed": (M3.C, "Lyon, France"), "in_date": (M3.C, "Bengaluru, India"), "body_temp_c": (M3.C, "Lisbon, Portugal")}
RA = " Note: the other agent's principal may follow different regional conventions (dates, floors, sizes, fiscal years, time expressions, units, currency). Resolve them correctly or confirm before acting."
def run(a):
    ck, cond, k = a
    C, loc = CASES[ck]; t = C[ck]; sa, sb, tool, ok = t[0], t[1], t[2], t[3]
    if cond in ("locale_card", "card+prompt"): sb += f"\n\n[Agent card of the counterpart] principal_locale: {loc}"
    if cond in ("prompt", "card+prompt"): sb += RA
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
CONDS = ["baseline", "locale_card", "prompt", "card+prompt"]
res = [x for x in llm.pmap(run, [(c, d, k) for c in CASES for d in CONDS for k in range(8)], workers=40) if x]
json.dump(res, open("results.json", "w"), indent=1)
print("case".ljust(20), *[d.ljust(13) for d in CONDS])
for c in CASES: print(c.ljust(20), *[("%.2f" % (sum(x["correct"] for x in res if x["case"] == c and x["cond"] == d)/max(1, sum(1 for x in res if x["case"] == c and x["cond"] == d)))).ljust(13) for d in CONDS])
print("MEAN".ljust(20), *[("%.2f" % (sum(x["correct"] for x in res if x["cond"] == d)/sum(1 for x in res if x["cond"] == d))).ljust(13) for d in CONDS])
print("asked".ljust(20), *[("%.2f" % (sum(x["asked"] for x in res if x["cond"] == d)/sum(1 for x in res if x["cond"] == d))).ljust(13) for d in CONDS])
