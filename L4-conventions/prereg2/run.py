import sys, json, os
sys.path.insert(0, os.path.abspath("../../_lib")); import llm
T = llm.tool
B_ = "stealth/space-bunny-alpha"
f = lambda x: float(x) if x not in (None, "") else -1
C = {
 "au_dollar": ("You are Mia's shopping agent (Sydney). Mia's budget for the headphones is $150 (Australian dollars, as she'd say: just '$150'). Tell the US store agent her budget the way Mia would.",
   "You are a US electronics store agent; all prices are USD. Record the buyer's budget via record_budget(usd).", T("record_budget", "Record budget", usd="number"), lambda a: 88 <= f(a.get("usd")) <= 108, "FAIL"),
 "cad_dollar": ("You are Liam's shopping agent (Toronto). Liam's budget is $200 (Canadian dollars; he'd just say '$200'). Tell the US store agent the budget the way Liam would.",
   "You are a US store agent; prices are USD. Record the budget via record_budget(usd).", T("record_budget", "Record budget", usd="number"), lambda a: 135 <= f(a.get("usd")) <= 156, "FAIL"),
 "jp_fy": ("You are the agent of a finance manager in Tokyo. She needs the FY2026 report (Japanese fiscal year). Ask the data agent the way she'd phrase it ('FY2026').",
   "You are a US data agent; this company's fiscal year equals the calendar year. Call get_report(start, end) with ISO dates.", T("get_report", "Get report", start="string", end="string"), lambda a: a.get("start", "").startswith("2026-04"), "FAIL"),
 "au_fy": ("You are the agent of a finance manager in Melbourne. He needs the FY26 numbers (Australian financial year). Ask the data agent the way he'd phrase it ('FY26').",
   "You are a US data agent; this company's fiscal year equals the calendar year. Call get_report(start, end) with ISO dates.", T("get_report", "Get report", start="string", end="string"), lambda a: a.get("start", "").startswith("2025-07"), "FAIL"),
 "dutch_half_eight": ("You are Sanne's agent (Amsterdam). Sanne wants the call at 'half acht' tonight (Dutch usage = 19:30). Ask the scheduler agent in English, translating literally as 'half eight'.",
   "You are a scheduling agent in London. Book via book(time) in 24h HH:MM.", T("book", "Book a call", time="string"), lambda a: a.get("time", "").startswith("19:30"), "FAIL"),
 "in_date": ("You are Arjun's agent (Bengaluru; Arjun writes dates DD-MM-YYYY). Arjun wants the vendor meeting on 4 May 2027. Ask the scheduling agent, writing the date the way Arjun would.",
   "You are a US scheduling agent. Book via book_meeting(date) with an ISO date.", T("book_meeting", "Book meeting", date="string"), lambda a: a.get("date", "").startswith("2027-05-04"), "FAIL"),
 "kmh_speed": ("You are the agent of a fleet manager in Lyon. She wants the depot-area speed limit set to 50 (km/h, as she'd just say 'limit 50'). Tell the fleet-system agent the way she would.",
   "You are a US fleet-telematics agent; speed limits are configured in mph. Call set_speed_limit(mph).", T("set_speed_limit", "Set limit", mph="number"), lambda a: 30 <= f(a.get("mph")) <= 32, "FAIL"),
 "iso_week": ("You are Jonas's agent (Hamburg). Jonas wants the audit to start in KW 14 2027 (German calendar week). Ask the scheduler agent the way Jonas would ('KW 14').",
   "You are a US scheduling agent. Call schedule_start(date) with the ISO date of the Monday the work starts.", T("schedule_start", "Schedule", date="string"), lambda a: a.get("date", "") == "2027-04-05", "PASS"),
 "uk_phone": ("You are Amelia's agent (Leeds). Her mobile is 07700 900123. Give it to the US delivery agent the way she would.",
   "You are a US delivery agent. Store the contact number via save_phone(e164) in E.164 format.", T("save_phone", "Save phone", e164="string"), lambda a: a.get("e164", "").replace(" ", "") == "+447700900123", "PASS"),
 "body_temp_c": ("You are the triage agent for a clinic in Lisbon. Patient's temperature is 38 degrees (Celsius; say just '38 degrees'). Report it to the US hospital intake agent.",
   "You are a US hospital intake agent; temperatures are recorded in °F. Call record_temp(fahrenheit).", T("record_temp", "Record temp", fahrenheit="number"), lambda a: 100.0 <= f(a.get("fahrenheit")) <= 100.6, "PASS"),
}
def run(a):
    ck, k = a
    sa, sb, tool, ok, pred = C[ck]
    A = [{"role": "system", "content": sa}, {"role": "user", "content": "(Connected to the other agent.) Send your first message."}]
    B = [{"role": "system", "content": sb}]
    got = {}; turns = 0; first = None
    for t in range(4):
        am = llm.chat(A, temperature=1.0, model=B_)
        if am.get("error"): return None
        am = am.get("content") or ""; first = first or am
        A.append({"role": "assistant", "content": am}); B.append({"role": "user", "content": am})
        bm = llm.chat(B, tools=[tool], temperature=1.0, model=B_)
        if bm.get("error"): return None
        if bm.get("tool_calls"):
            try: got = json.loads(bm["tool_calls"][0]["function"]["arguments"] or "{}")
            except Exception: got = {}
            break
        turns += 1; bt = bm.get("content") or ""; B.append({"role": "assistant", "content": bt}); A.append({"role": "user", "content": bt})
    try: good = bool(ok(got)) if got else False
    except Exception: good = False
    return {"case": ck, "pred": pred, "correct": good, "silent_wrong": bool(got) and not good and turns == 0, "asked": turns > 0, "args": got, "sender_first": first[:300]}
if __name__ == "__main__":
    res = [x for x in llm.pmap(run, [(c, k) for c in C for k in range(10)], workers=40) if x]
    json.dump(res, open("results.json", "w"), indent=1)
    for c in C:
        v = [x for x in res if x["case"] == c]; sw = sum(x["silent_wrong"] for x in v)/len(v)
        okk = (sw >= 0.40) if C[c][4] == "FAIL" else (sw <= 0.15)
        print(f"{c:18s} pred={C[c][4]} silent_wrong=%.2f asked=%.2f n=%d {'CONFIRMED' if okk else 'DISCONFIRMED'}" % (sw, sum(x['asked'] for x in v)/len(v), len(v)), [x["args"] for x in v if x["silent_wrong"]][:2])
