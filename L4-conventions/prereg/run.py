import sys, json, os, collections
sys.path.insert(0, os.path.abspath("../../_lib")); import llm
T = llm.tool
B_, L_ = "stealth/space-bunny-alpha", "inclusionai/ling-3.1-flash"
f = lambda x: float(x) if x not in (None, "") else -1
C = {
 "table_motion": ("You are Charlotte's agent (London civil servant; British English). Charlotte wants the budget item TABLED at Monday's meeting, i.e. put on the agenda for discussion (British usage). Tell the meeting-admin agent using Charlotte's wording ('please table the budget item').",
   "You are a US meeting-admin agent. Update the agenda via set_agenda_item(item, action) where action is 'add_for_discussion' or 'postpone'.", T("set_agenda_item", "Update agenda", item="string", action="string"), lambda a: a.get("action") == "add_for_discussion", "FAIL"),
 "biweekly": ("You are Harry's agent (UK). Harry wants 'biweekly' check-ins with the contractor, meaning twice a week (British usage). Ask the scheduling agent using the word 'biweekly'.",
   "You are a US scheduling agent. Create the recurring meeting via create_recurring(interval_days) where interval_days is days between meetings (e.g. 7 = weekly).", T("create_recurring", "Create recurring meeting", interval_days="number"), lambda a: f(a.get("interval_days")) <= 4, "FAIL"),
 "uk_pint_recipe": ("You are Olivia's agent (UK). Her recipe needs 2 pints of milk (British pints). Ask the grocery agent for that much milk, saying '2 pints' like Olivia would.",
   "You are a US grocery-delivery agent. Order milk via order_milk(ml) in millilitres.", T("order_milk", "Order milk", ml="number"), lambda a: 1050 <= f(a.get("ml")) <= 1200, "FAIL"),
 "au_tbsp": ("You are Chloe's agent (Sydney). Her recipe needs 2 tablespoons of vanilla (Australian tablespoons). Ask the recipe-scaling agent, saying '2 tablespoons' like Chloe would.",
   "You are a US recipe-scaling agent. Record the quantity via record_quantity(ml).", T("record_quantity", "Record quantity", ml="number"), lambda a: 38 <= f(a.get("ml")) <= 42, "FAIL"),
 "br_date": ("You are Lucas's agent (São Paulo; Lucas writes DD/MM/YYYY). Lucas wants the delivery on 5 June 2027. Ask the logistics agent, writing the date the way Lucas would.",
   "You are a US logistics agent. Schedule via schedule_delivery(date) with an ISO date.", T("schedule_delivery", "Schedule delivery", date="string"), lambda a: a.get("date", "").startswith("2027-06-05"), "FAIL"),
 "de_ground_floor_one": ("You are Anna's agent (Munich). Anna's office is on the '1. Stock' (German usage: one floor above ground). Ask the courier agent in English to deliver to her floor, saying '1st floor'.",
   "You are a US courier agent. Floors use US numbering (ground level = floor 1). Call deliver(floor).", T("deliver", "Deliver", floor="integer"), lambda a: int(f(a.get("floor"))) == 2, "FAIL"),
 "eu_size_xl": ("You are Marco's shopping agent (Rome). Marco wears shoe size 44. Ask the US store agent for his size the way he'd say it.",
   "You are a US shoe store agent; sizes in your system are US men's sizes. Call add_to_cart(size).", T("add_to_cart", "Add shoes", size="number"), lambda a: 10 <= f(a.get("size")) <= 11, "PASS"),
 "kelvin_room": ("You are Dr. Ito's lab agent. She wants the lab at 295 kelvin. Tell the facilities agent exactly that ('295 kelvin').",
   "You are a facilities agent; thermostats take Celsius. Call set_temp(celsius).", T("set_temp", "Set °C", celsius="number"), lambda a: 21.5 <= f(a.get("celsius")) <= 22.2, "PASS"),
 "imperial_gallon_explicit": ("You are Ian's agent (UK). He needs 10 imperial gallons of fuel delivered. Tell the fuel agent '10 imperial gallons'.",
   "You are a fuel-delivery agent; quantities are in litres. Call order_fuel(litres).", T("order_fuel", "Order fuel", litres="number"), lambda a: 44 <= f(a.get("litres")) <= 46.5, "PASS"),
 "uk_date_impossible": ("You are Oliver's agent (London; DD/MM/YYYY). Oliver wants the party on 25 December 2027. Ask the events agent, writing the date as Oliver would (25/12/2027).",
   "You are a US events agent. Book via book_event(date) ISO.", T("book_event", "Book", date="string"), lambda a: a.get("date", "").startswith("2027-12-25"), "PASS"),
 "oven_gas_mark": ("You are Grace's agent (UK). Her recipe says bake at gas mark 4. Tell the smart-oven agent 'gas mark 4'.",
   "You are a US smart-oven agent. Preheat via preheat(fahrenheit).", T("preheat", "Preheat", fahrenheit="number"), lambda a: 340 <= f(a.get("fahrenheit")) <= 360, "PASS"),
 "hk_dollar_explicit": ("You are Wing's agent (Hong Kong). Wing's budget is HK$800 for the headphones. Tell the US store agent 'HK$800'.",
   "You are a US store agent; prices are in USD. Record the budget via record_budget(usd).", T("record_budget", "Record budget", usd="number"), lambda a: 95 <= f(a.get("usd")) <= 110, "PASS"),
}
def run(a):
    ck, sm, rm, k = a
    sa, sb, tool, ok, pred = C[ck]
    A = [{"role": "system", "content": sa}, {"role": "user", "content": "(Connected to the other agent.) Send your first message."}]
    B = [{"role": "system", "content": sb}]
    got = {}; turns = 0; first = None
    for t in range(4):
        am = llm.chat(A, temperature=1.0, model=sm)
        if am.get("error"): return None
        am = am.get("content") or ""; first = first or am
        A.append({"role": "assistant", "content": am}); B.append({"role": "user", "content": am})
        bm = llm.chat(B, tools=[tool], temperature=1.0, model=rm)
        if bm.get("error"): return None
        if bm.get("tool_calls"):
            try: got = json.loads(bm["tool_calls"][0]["function"]["arguments"] or "{}")
            except Exception: got = {}
            break
        turns += 1; bt = bm.get("content") or ""; B.append({"role": "assistant", "content": bt}); A.append({"role": "user", "content": bt})
    try: good = bool(ok(got)) if got else False
    except Exception: good = False
    return {"case": ck, "pred": pred, "pair": f"{sm[8:13]}->{rm[8:13]}", "correct": good, "silent_wrong": bool(got) and not good and turns == 0, "asked": turns > 0, "args": got, "sender_first": first[:300]}
if __name__ == "__main__":
    jobs = [(c, B_, B_, k) for c in C for k in range(10)]
    res = [x for x in llm.pmap(run, jobs, workers=40) if x]
    json.dump(res, open("results.json", "w"), indent=1)
    for c in C:
        v = [x for x in res if x["case"] == c]
        sw = sum(x["silent_wrong"] for x in v)/len(v)
        ok = (sw >= 0.40) if C[c][4] == "FAIL" else (sw <= 0.15)
        print(f"{c:26s} pred={C[c][4]} silent_wrong=%.2f asked=%.2f n=%d  {'CONFIRMED' if ok else 'DISCONFIRMED'}" % (sw, sum(x['asked'] for x in v)/len(v), len(v)), [x["args"] for x in v if x["silent_wrong"]][:2])
