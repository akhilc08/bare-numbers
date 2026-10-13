# Prior work: silent convention mismatch between agents (subagent search, 2026-10-03; citations checked)

## Grounding and clarification
- **Grounding Gaps in LM Generations** (Shaikh et al., NAACL 2024, 2024.naacl-long.348). LLMs are "presumptive grounders". This is our theoretical frame; they study one model with a human, without locale.
- **AmbigQA** (2004.10645) and **CLAMBER** (2405.12063, ACL 2024). The ambiguity there is *visible*; ours is invisible from the receiver's own convention.
- **ClarEval** (2603.00187); **ClarifyCodeBench** (2607.00711), where units and precision ambiguities are resolved *best*, a useful contrast because those are visible.
- **Implicit Intelligence** (2602.20424). Unstated requirements; no locale.
- **Talk is Cheap, Communication is Hard** (2605.01750). Grounding failures between agents in negotiation; the closest agent-to-agent framing, without locale.
- **Illusion of Alignment** (2608.08210). Hidden disagreement behind consensus; a conceptual cousin.

## Reliability of multi-agent communication
- **Beyond Message Passing** (2604.02369). A survey of 18 protocols with little support for clarification or context alignment. Use as motivation.
- **Facts Without Rules** (2608.29028). The value survives and the frame is dropped (privacy). A parallel to ours.
- **Faithful, Not Corrective** (2607.09678). Relay fidelity; our failure is faithful transmission followed by misdecoding.
- **SovereignNegotiation-Bench** (2607.02814). Same principal-agent setting; no conventions.

## Cultural and locale knowledge
- **CAPRI: LLMs Infer Cultural Context but Fail to Apply It** (2606.17688). **The most important single-agent precedent** (recognised conventions not applied); single model and user, no agent-to-agent communication, no clarification measure.
- **WorldBench** (2609.01056), **Terminal-Bench-LILT** (2608.28641), **CASA** (2410.23252), **CulturalBench** (2410.02677), **BLEnD** (2406.09948). Single locale or knowledge QA.

## Date, unit and time-zone ambiguity
- **Numerical Localisation in LLM Translations** (2608.05232). Translation task; a prompt fix helps.
- **DateLogicQA** (2412.13377); **GeoTemp** (2506.03984).

## Verdict
**Novel, moderately strong.** No prior paper puts two agents from different locales in conversation and measures silent reinterpretation, or the visible vs hidden-ambiguity split.
- Frame it as **agent-to-agent pragmatics** (faithful sender, silent decoding by the receiver in its own locale), not as cultural knowledge.
- Stress that a locale visible in a source name is decoded correctly, and that sender style matters.

**Position against:** Shaikh 2024, CAPRI 2026, Beyond Message Passing, Talk is Cheap (plus Facts Without Rules).

## Suggested expansion (~30 conventions, locales US/UK/DE/FR/JP/IN/BR/AU)
- **Numbers:** decimal comma, thousands dot, lakh/crore ("2,50,000"), long-scale "milliard".
- **Dates and times:** DD.MM, Japanese era, ISO week "KW 14", week start, 12h/24h, "viertel acht", "half seven", "next/this Friday", "fortnight", "bank holiday".
- **Units:** stone, UK vs US pint/gallon/fl oz, AU tbsp = 20 ml, gas mark, km/miles, clothing and shoe sizes, A4/Letter.
- **Money:** fiscal years (JP/IN Apr–Mar, AU Jul–Jun), "$" meaning AUD, VAT/GST-inclusive prices, tipping.
- **Spatial:** floor numbering, "ground floor", phone formats; JP address order.
- **Controls:** no-reinterpretation cases, and cases that are visible but conflicting.
