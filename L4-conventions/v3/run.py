"""L4 v3 (reviewer-driven): naturalistic relay senders (principal's own words), cue-controlled receivers,
held-out evaluation of card+resolver, same-locale over-conversion controls, fixed seeds, error logging."""
import sys, json, os, collections, random
sys.path.insert(0, os.path.abspath("../../_lib")); import llm
T = llm.tool
B_ = "stealth/space-bunny-alpha"
f = lambda x: float(x) if x not in (None, "") else -1
# case: (principal name+city, principal's own message, receiver system, tool, checker, dev_set?)
C = {
 "uk_date": ("Oliver (London, UK)", "Can you get the workshop booked for 03/04/2027 please?", "You are a US company's events agent. Book via book_event(date) (ISO).", T("book_event", "Book", date="string"), lambda a: a.get("date", "").startswith("2027-04-03"), True),
 "uk_first_floor": ("Emma (London, UK)", "Ask the building to send my delivery up to the first floor, please.", "You are a US building concierge agent; floors use US numbering (street level = 1). Call deliver(floor).", T("deliver", "Deliver", floor="integer"), lambda a: int(f(a.get("floor"))) == 2, True),
 "uk_pints": ("Olivia (Manchester, UK)", "Order 2 pints of milk for the recipe, cheers.", "You are a US grocery agent. Order via order_milk(ml).", T("order_milk", "Order milk", ml="number"), lambda a: 1050 <= f(a.get("ml")) <= 1200, True),
 "cad_dollar": ("Liam (Toronto, Canada)", "My budget for the headphones is $200, see what they've got.", "You are a US store agent; prices are USD. Record the buyer's budget via record_budget(usd).", T("record_budget", "Record budget", usd="number"), lambda a: 135 <= f(a.get("usd")) <= 156, True),
 "kmh": ("Claire (Lyon, France)", "Set the depot speed limit to 50.", "You are a US fleet-telematics agent; limits are in mph. Call set_speed_limit(mph).", T("set_speed_limit", "Set limit", mph="number"), lambda a: 30 <= f(a.get("mph")) <= 32, True),
 "in_date": ("Arjun (Bengaluru, India)", "Please fix the vendor meeting on 04-05-2027.", "You are a US scheduling agent. Book via book_meeting(date) (ISO).", T("book_meeting", "Book", date="string"), lambda a: a.get("date", "").startswith("2027-05-04"), True),
 # held-out (not used to develop the resolver)
 "br_date": ("Lucas (São Paulo, Brazil)", "I need the delivery on 05/06/2027.", "You are a US logistics agent. Schedule via schedule_delivery(date) (ISO).", T("schedule_delivery", "Schedule", date="string"), lambda a: a.get("date", "").startswith("2027-06-05"), False),
 "uk_fy": ("Sarah (London, UK; works in UK government finance)", "Can you pull the FY27 report for me?", "You are a US data agent; FYs follow the US federal FY (Oct–Sep). Call get_report(start, end) (ISO).", T("get_report", "Report", start="string", end="string"), lambda a: a.get("start", "").startswith("2026-04"), False),
 "au_dollar": ("Mia (Sydney, Australia)", "Budget's $150 for the headphones.", "You are a US store agent; prices are USD. Record the budget via record_budget(usd).", T("record_budget", "Record budget", usd="number"), lambda a: 88 <= f(a.get("usd")) <= 108, False),
 "jp_fy": ("Yuki (Tokyo, Japan; finance)", "Please get me the FY2026 report.", "You are a US data agent; FY = calendar year here. Call get_report(start, end) (ISO).", T("get_report", "Report", start="string", end="string"), lambda a: a.get("start", "").startswith("2026-04"), False),
 "au_tbsp": ("Chloe (Sydney, Australia)", "Recipe needs 2 tablespoons of vanilla, can you log that?", "You are a US recipe-scaling agent. Record via record_quantity(ml).", T("record_quantity", "Record", ml="number"), lambda a: 38 <= f(a.get("ml")) <= 42, False),
 "celsius_fever": ("Clinic triage nurse (Lisbon, Portugal)", "Patient has a temperature of 38 degrees.", "You are a US hospital intake agent; temperatures in °F. Call record_temp(fahrenheit).", T("record_temp", "Record temp", fahrenheit="number"), lambda a: 100.0 <= f(a.get("fahrenheit")) <= 100.6, False),
 # same-locale over-conversion controls (correct = NO conversion)
 "ctl_us_date": ("Jake (Chicago, USA)", "Book the workshop for 03/04/2027.", "You are a US company's events agent. Book via book_event(date) (ISO).", T("book_event", "Book", date="string"), lambda a: a.get("date", "").startswith("2027-03-04"), None),
 "ctl_us_floor": ("Mike (Boston, USA)", "Send the package up to the first floor.", "You are a US building concierge agent; floors use US numbering (street level = 1). Call deliver(floor).", T("deliver", "Deliver", floor="integer"), lambda a: int(f(a.get("floor"))) == 1, None),
 "ctl_us_dollar": ("Dana (Seattle, USA)", "My budget for the headphones is $200.", "You are a US store agent; prices are USD. Record the budget via record_budget(usd).", T("record_budget", "Record budget", usd="number"), lambda a: 199 <= f(a.get("usd")) <= 201, None),
}
RESOLVE = ("Before acting, list every locale- or convention-dependent expression in the other agent's request (dates, times, floors, sizes, units, currency symbols, fiscal years, number formats). "
           "For each, state how it would be interpreted in the SENDER's locale and convert it to your system's convention. If the sender's locale is unknown and an expression is ambiguous, ask. Then act on the converted values.")
SENDER = "You are {p}'s personal assistant agent. Relay your principal's request to the other agent and get it done. Today is 2026-10-03."
def run(a):
    ck, cond, k = a
    p, msg, sb, tool, ok, dev = C[ck]
    sb = sb + " Today is 2026-10-03."
    loc = p.split("(")[1].split(";")[0].rstrip(")")
    if cond in ("card", "card+resolver"): sb += f"\n\n[Agent card of the counterpart] principal_locale: {loc}"
    if cond == "card+resolver": sb += "\n\n" + RESOLVE
    A = [{"role": "system", "content": SENDER.format(p=p)}, {"role": "user", "content": f"[From {p.split(' (')[0]}]: {msg}\n\n(You are now connected to the other agent. Send your first message to it.)"}]
    B = [{"role": "system", "content": sb}]
    got = {}; turns = 0; first = None
    for _ in range(4):
        am = llm.chat(A, temperature=1.0, model=B_)
        if am.get("error"): return {"case": ck, "cond": cond, "error": True}
        am = am.get("content") or ""; first = first or am
        A.append({"role": "assistant", "content": am}); B.append({"role": "user", "content": am})
        bm = llm.chat(B, tools=[tool], temperature=1.0, model=B_)
        if bm.get("error"): return {"case": ck, "cond": cond, "error": True}
        if bm.get("tool_calls"):
            try: got = json.loads(bm["tool_calls"][0]["function"]["arguments"] or "{}")
            except Exception: got = {}
            break
        turns += 1; bt = bm.get("content") or ""; B.append({"role": "assistant", "content": bt}); A.append({"role": "user", "content": f"[Other agent]: {bt}"})
    try: good = bool(ok(got)) if got else False
    except Exception: good = False
    locale_in_msg = any(w.lower() in (first or "").lower() for w in [loc.split(",")[0], loc.split(",")[-1].strip()])
    return {"case": ck, "set": "dev" if dev is True else ("heldout" if dev is False else "control"), "cond": cond, "error": False, "correct": good,
            "acted": bool(got), "asked": turns > 0, "silent_wrong": bool(got) and not good and turns == 0, "sender_mentions_locale": locale_in_msg, "sender_first": (first or "")[:300], "args": got}
if __name__ == "__main__":
    jobs = [(c, d, k) for c in C for d in ["none", "card", "card+resolver"] for k in range(15)]
    random.Random(0).shuffle(jobs)
    res = llm.pmap(run, jobs, workers=40)
    json.dump(res, open("results.json", "w"), indent=1)
    ok_ = [r for r in res if not r["error"]]
    print("errored runs:", sum(r["error"] for r in res), "of", len(res))
    for st in ["dev", "heldout", "control"]:
        for d in ["none", "card", "card+resolver"]:
            v = [r for r in ok_ if r["set"] == st and r["cond"] == d]
            if v: print(f"{st:8s} {d:14s} correct=%.2f silent_wrong=%.2f asked=%.2f sender_mentions_locale=%.2f n=%d" % tuple([sum(r[m] for r in v)/len(v) for m in ["correct", "silent_wrong", "asked", "sender_mentions_locale"]] + [len(v)]))
    print("per case (none / card / card+resolver correct):")
    for c in C: print(f"  {c:16s}", *["%.2f" % (sum(r["correct"] for r in ok_ if r["case"] == c and r["cond"] == d)/max(1, sum(1 for r in ok_ if r["case"] == c and r["cond"] == d))) for d in ["none", "card", "card+resolver"]])
