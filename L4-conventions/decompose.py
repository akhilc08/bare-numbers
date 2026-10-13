"""Decompose silent errors: P(sender writes locale-ambiguous form) x P(receiver misreads | ambiguous)."""
import sys, json, os, collections
sys.path.insert(0, os.path.abspath("../_lib")); import llm
R = json.load(open("results.json"))
R = [r for r in R if r["cond"] == "baseline" and not r["case"].startswith("control")]
MEANING = {"uk_date": "3 April 2027", "us_date_to_eu": "11 October 2027", "uk_first_floor": "the UK first floor (= US 2nd floor)", "half_six_de": "17:30 (German 'halb sechs')",
           "tomorrow_tz": "Wednesday 2026-10-14 (Tokyo's tomorrow)", "celsius_to_us": "18 °C", "fahrenheit_to_eu": "68 °F", "eu_shoe": "EU shoe size 39", "uk_dress": "UK dress size 12",
           "uk_fy": "UK fiscal year Apr 2026–Mar 2027", "fuel_l100": "6 L/100 km", "stone": "12 stone", "lakh": "2.5 lakh = 250,000 INR", "reiwa": "Reiwa 5 = 2023"}
def lab(r):
    j = llm.judge_json(f"A sender agent meant: {MEANING[r['case']]}.\nIts first message:\n{r['sender_first']}\n\nDoes the message express this value ONLY in a locale-specific form that someone from another country could plausibly misread (e.g. '03/04', 'first floor', 'half six', 'size 39', 'FY27', '18 degrees', 'tomorrow' with no timezone), WITHOUT an explicit disambiguation (spelled-out month, ISO date, unit system, 'UK sizing', timezone, conversion)? " + '{"ambiguous": bool}')
    return {**r, "ambiguous": bool(j.get("ambiguous"))}
L = llm.pmap(lab, R, workers=40)
json.dump(L, open("decomposed.json", "w"), indent=1)
by = collections.defaultdict(list)
for r in L: by[r["pair"].split("->")[0]].append(r)
print("P(sender writes ambiguous form) by sender model:")
for s, v in by.items(): print("  ", s, "%.2f n=%d" % (sum(x["ambiguous"] for x in v)/len(v), len(v)))
by = collections.defaultdict(list)
for r in L:
    if r["ambiguous"]: by[r["pair"].split("->")[1]].append(r)
print("P(receiver silently wrong | ambiguous message) by receiver model:")
for s, v in by.items(): print("  ", s, "%.2f  asked=%.2f n=%d" % (sum(x["silent_wrong"] for x in v)/len(v), sum(x["asked"] for x in v)/len(v), len(v)))
amb = [r for r in L if r["ambiguous"]]; clear = [r for r in L if not r["ambiguous"]]
print("silent_wrong | ambiguous=%.2f (n=%d)   | explicit=%.2f (n=%d)" % (sum(x["silent_wrong"] for x in amb)/len(amb), len(amb), sum(x["silent_wrong"] for x in clear)/max(1,len(clear)), len(clear)))
by = collections.defaultdict(list)
for r in amb: by[r["case"]].append(r["silent_wrong"])
print("P(silent wrong | ambiguous) by convention:"); [print("  ", k, "%.2f n=%d" % (sum(v)/len(v), len(v))) for k, v in sorted(by.items(), key=lambda x: -sum(x[1])/len(x[1]))]
