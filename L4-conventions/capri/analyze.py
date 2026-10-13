import json, collections, random, re, sys
sys.argv = sys.argv[:1]
from run import conv_unit, spec
R = [r for r in json.load(open("results.json")) if not r["error"]]
PAT = {"C": r"°\s?C|celsius", "F": r"°\s?F|fahrenheit", "kmh": r"km/h|kph|kmh|kilomet", "mph": r"mph|miles per hour",
       "km": r"\bkm\b|kilomet", "mi": r"\bmi\b|\bmiles?\b", "sqm": r"m²|\bm2\b|sq\.?\s?m\b|square met|sqm", "sqft": r"sq\.?\s?ft|square f|ft²|sqft",
       "CNY": r"yuan|RMB|CNY|元", "EUR": r"€|euro|EUR", "GBP": r"£|pound|GBP", "KRW": r"₩|\bwon\b|KRW", "JPY": r"\byen\b|JPY|円",
       "INR": r"₹|rupee|INR|\bRs\.?", "BRL": r"R\$|rea(l|is)\b|BRL", "ILS": r"₪|shekel|NIS|ILS", "USD": r"(?<!R)\$|dollar|USD"}
UNITS = {"temperature": ["C", "F"], "speed": ["kmh", "mph"], "distance": ["km", "mi"], "size": ["sqm", "sqft"],
         "price": ["CNY", "EUR", "GBP", "KRW", "JPY", "INR", "BRL", "ILS", "USD"]}
def sender_unit(r):
    t = r["sender_first"]; own = conv_unit(r["concept"], r["culture"])
    hits = {u for u in UNITS[r["concept"]] if re.search(PAT[u], t, re.I if u not in ("EUR","GBP","KRW","JPY","INR","BRL","ILS","USD","CNY") else 0)}
    if not hits: return "bare"
    if len(hits) > 1: return "hedged"
    return "own" if own in hits else "wrong"
for r in R:
    if r["cond"] != "direct": r["sender_unit"] = sender_unit(r)
def ci(v, B=2000):
    if not v: return (0, 0, 0)
    rng = random.Random(0); m = sum(v) / len(v)
    bs = sorted(sum(rng.choice(v) for _ in v) / len(v) for _ in range(B))
    return m, bs[int(.025 * B)], bs[int(.975 * B)]
def row(name, v, keys=("correct", "silent_wrong", "asked")):
    print(f"{name:34s}", "  ".join("%s=%.2f[%.2f,%.2f]" % ((k,) + ci([float(r[k]) for r in v])) for k in keys), f"n={len(v)}")
print("== implicit CAPRI cues, cross-convention receiver")
for c in ["direct", "none", "card", "card+resolver"]:
    row(c, [r for r in R if r["kind"] == "implicit" and not r["same"] and r["cond"] == c])
print("\n== by concept (correct): direct / none / card / card+resolver")
for k in ["temperature", "speed", "distance", "size", "price"]:
    print(f"  {k:12s}", *["%.2f" % ci([float(r['correct']) for r in R if r['kind'] == 'implicit' and not r['same'] and r['cond'] == c and r['concept'] == k])[0] for c in ["direct", "none", "card", "card+resolver"]])
print("\n== by culture (correct): direct / none / card / card+resolver")
for k in sorted({r["culture"] for r in R if r["kind"] == "implicit"}):
    print(f"  {k:12s}", *["%.2f" % ci([float(r['correct']) for r in R if r['kind'] == 'implicit' and not r['same'] and r['cond'] == c and r['culture'] == k])[0] for c in ["direct", "none", "card", "card+resolver"]])
print("\n== where the relay breaks: sender's first message states principal's unit (own) / a wrong unit / both (hedged) / none (bare)")
for c in ["none", "card", "card+resolver"]:
    v = [r for r in R if r["kind"] == "implicit" and not r["same"] and r["cond"] == c]
    print(f" {c}: share", {k: round(n / len(v), 2) for k, n in collections.Counter(r["sender_unit"] for r in v).most_common()})
    for su in ["own", "wrong", "hedged", "bare"]:
        w = [r for r in v if r["sender_unit"] == su]
        if w: row(f"   sender={su}", w)
print("\n== same-convention controls (correct = no conversion)")
for c in ["none", "card+resolver"]:
    row(c, [r for r in R if r["same"] and r["cond"] == c])
try:
    N = [r for r in json.load(open("results_neutral.json")) if not r["error"]]
    print("\n== CAPRI neutral (no cues; value given metric-style, US receiver). correct = metric reading")
    for c in ["direct", "none"]:
        v = [r for r in N if r["cond"] == c]
        for r in v:
            if c != "direct": r["sender_unit"] = sender_unit(r)
        row(c, v)
        if c != "direct": print("   sender unit:", dict(collections.Counter(r["sender_unit"] for r in v)))
except FileNotFoundError: pass
