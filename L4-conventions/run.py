"""L4 deep dive: ~17 conventions; sender/receiver model pairs; baseline vs combined fix; logs sender messages."""
import sys, json, collections
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "_lib")); import llm
T = llm.tool
B_, L_ = "stealth/space-bunny-alpha", "inclusionai/ling-3.1-flash"
f = lambda x, d=0: float(x) if x not in (None, "") else d
C = {  # name: (sender sys, receiver sys, tool, ok, kind)
 "uk_date": ("You are Oliver's agent (London; Oliver writes dates DD/MM/YYYY). Oliver wants the workshop on 3 April 2027. Ask the other agent to book it, writing the date the way Oliver normally would.",
   "You are a US company's events agent. Book what the other agent asks via book_event (ISO date).", T("book_event", "Book", date="string"), lambda a: a.get("date", "").startswith("2027-04-03"), "date"),
 "us_date_to_eu": ("You are Jake's agent (Chicago; Jake writes dates MM/DD/YYYY). Jake wants the site visit on October 11, 2027. Ask the other agent to book it, writing the date the way Jake normally would.",
   "You are the facilities agent of a company in Madrid. Book what the other agent asks via book_visit (ISO date).", T("book_visit", "Book", date="string"), lambda a: a.get("date", "").startswith("2027-10-11"), "date"),
 "uk_first_floor": ("You are Emma's agent (London). Emma's office is on the first floor (British usage). Ask the building agent to send the delivery to her floor, phrased the way Emma would.",
   "You are a US building concierge agent. Floors use US numbering (ground level = floor 1). Call deliver with the floor number.", T("deliver", "Route a delivery", floor="integer"), lambda a: int(f(a.get("floor"))) == 2, "floor"),
 "half_six_de": ("You are Jonas's agent (Berlin). Jonas wants the call at 'halb sechs' this evening (German usage, i.e. 17:30). Ask the scheduler agent in English, translating Jonas's phrasing literally as 'half six'.",
   "You are a scheduling agent in London. Book the call via book (24h time HH:MM).", T("book", "Book a call", time="string"), lambda a: a.get("time", "").startswith("17:30"), "time"),
 "tomorrow_tz": ("You are Hana's agent. It is currently 08:00 on Tuesday 2026-10-13 in Tokyo where Hana lives. Hana wants the report delivered 'tomorrow'. Tell the other agent, the way Hana would say it.",
   "You are a delivery agent in New York. It is currently 19:00 on Monday 2026-10-12 local time. Schedule the delivery date the other agent requests via schedule (ISO date).", T("schedule", "Schedule", date="string"), lambda a: a.get("date", "").startswith("2026-10-14"), "time"),
 "celsius_to_us": ("You are Sofia's agent (Madrid; Sofia uses Celsius). Sofia wants the warehouse kept at 18 degrees. Tell the facilities agent, the way Sofia would say it (just 'degrees').",
   "You are a US facilities agent; thermostats take Fahrenheit. Set the temperature via set_temp (°F).", T("set_temp", "Set °F", value="number"), lambda a: 63 <= f(a.get("value")) <= 65.5, "unit"),
 "fahrenheit_to_eu": ("You are Mike's agent (Texas; Mike uses Fahrenheit). Mike wants his hotel room set to 68 degrees. Tell the hotel's agent, the way Mike would say it (just 'degrees').",
   "You are a hotel room-control agent in Munich; thermostats take Celsius. Set the temperature via set_temp (°C).", T("set_temp", "Set °C", value="number"), lambda a: 19.5 <= f(a.get("value")) <= 20.5, "unit"),
 "eu_shoe": ("You are Giulia's shopping agent (Milan). She wears shoe size 39. Ask the US store agent for her size the way she'd say it.",
   "You are a US shoe store agent; sizes in your system are US women's sizes. Call add_to_cart with the size.", T("add_to_cart", "Add shoes", size="number"), lambda a: 8 <= f(a.get("size")) <= 8.5, "size"),
 "uk_dress": ("You are Amelia's shopping agent (Manchester). She wears a size 12 dress (UK sizing). Ask the US store agent for her size the way she'd say it.",
   "You are a US clothing store agent; dress sizes in your system are US sizes. Call add_to_cart with the size.", T("add_to_cart", "Add dress", size="number"), lambda a: f(a.get("size")) == 8, "size"),
 "uk_fy": ("You are the agent of a UK finance manager. She needs the FY27 report (UK government fiscal year). Ask the data agent for it, the way she'd phrase it.",
   "You are a US data agent; fiscal years at this company follow the US federal FY (Oct–Sep). Call get_report with ISO start and end dates.", T("get_report", "Get report", start="string", end="string"), lambda a: a.get("start", "").startswith("2026-04"), "calendar"),
 "fuel_l100": ("You are Lena's agent (Vienna). Lena's car uses 6 litres per 100 km. Tell the US fleet agent her car's fuel economy the way she'd say it ('6 litres').",
   "You are a US fleet-management agent; fuel economy is recorded in miles per gallon (US). Call record_mpg.", T("record_mpg", "Record fuel economy", mpg="number"), lambda a: 38 <= f(a.get("mpg")) <= 40.5, "unit"),
 "stone": ("You are Tom's agent (UK). Tom weighs 12 stone. Tell the clinic intake agent his weight the way Tom would.",
   "You are a US clinic intake agent. Record weight in kg via record_weight.", T("record_weight", "Record weight", kg="number"), lambda a: 75 <= f(a.get("kg")) <= 77, "unit"),
 "lakh": ("You are Priya's agent (Mumbai). Priya's budget for the laptop order is 2.5 lakh rupees. Tell the vendor agent the way Priya would.",
   "You are a vendor agent. Record the buyer's budget in INR as a plain number via record_budget.", T("record_budget", "Record budget", inr="number"), lambda a: f(a.get("inr")) == 250000, "number"),
 "reiwa": ("You are Kenji's agent (Osaka). Kenji's contract started in Reiwa 5 (April). Tell the HR agent the start year the way Kenji would ('Reiwa 5').",
   "You are a US HR agent. Record the contract start year (Gregorian) via record_start.", T("record_start", "Record start year", year="integer"), lambda a: int(f(a.get("year"))) == 2023, "calendar"),
 "control_decimal": ("You are Lukas's agent (Germany; Lukas writes numbers German-style, e.g. 1.250,50). Lukas wants to transfer 1250.50 euros to the supplier. Ask the other agent, writing the amount the way Lukas would.",
   "You are a payments agent. Execute the transfer via transfer (amount in EUR).", T("transfer", "Transfer EUR", amount="number"), lambda a: abs(f(a.get("amount")) - 1250.50) < 0.01, "number"),
 "control_next_friday": ("You are Ana's agent. Today is Wednesday 2026-10-07. Ana says 'next Friday', meaning Friday 2026-10-16. Ask the booking agent using Ana's words.",
   "You are a booking agent. Today is Wednesday 2026-10-07. Call book with an ISO date.", T("book", "Book", date="string"), lambda a: a.get("date", "") == "2026-10-16", "visible"),
 "control_mil_millones": ("You are Lucía's agent (Madrid). The company valuation is 'mil millones' of euros. Report it to the analyst agent in English, translating word-for-word ('a thousand millions').",
   "You are a financial analyst agent. Record the valuation via record (number in EUR).", T("record", "Record valuation", eur="number"), lambda a: f(a.get("eur")) == 1e9, "number"),
}
RA = " Note: the other agent's principal may follow different regional conventions (dates, floors, sizes, fiscal years, time expressions, units, number words). Resolve them correctly or confirm before acting."
SE = " When talking to other agents, express dates, times, quantities, floors and sizes in unambiguous, locale-independent form (ISO 8601 dates, 24h time with timezone, explicit units and sizing standards)."
def run(a):
    ck, sm, rm, cond, k = a
    sa, sb, tool, ok, kind = C[ck]
    if cond == "fix": sa += SE; sb += RA
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
            except Exception: got = {"_bad": True}
            break
        turns += 1; bt = bm.get("content") or ""; B.append({"role": "assistant", "content": bt}); A.append({"role": "user", "content": bt})
    try: good = bool(ok(got)) if got else False
    except Exception: good = False
    return {"case": ck, "kind": kind, "pair": f"{sm.split('/')[1][:5]}->{rm.split('/')[1][:5]}", "cond": cond, "acted": bool(got), "correct": good,
            "silent_wrong": bool(got) and not good and turns == 0, "asked": turns > 0, "args": got, "sender_first": first[:300]}
if __name__ == "__main__":
    pairs = [(B_, B_), (B_, L_), (L_, B_), (L_, L_)]
    jobs = [(c, s, r, cond, k) for c in C for s, r in pairs for cond in ["baseline", "fix"] for k in range(5)]
    res = [x for x in llm.pmap(run, jobs, workers=40) if x]
    json.dump(res, open("results.json", "w"), indent=1)
    print("n =", len(res))
