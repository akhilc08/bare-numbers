# Preregistration #2: false-friend theory (written 2026-10-03 BEFORE running run.py)
**Refined theory (after prereg #1):** silent misreading occurs when the sender's expression is valid AND plausible in the receiver's convention, AND its ambiguity isn't commonly known. Otherwise the receiver converts or asks.
**Prediction:** space→space baseline silent-wrong ≥ 40% for FAIL and ≤ 15% for PASS.

| case | sender meaning | receiver convention | prediction |
|---|---|---|---|
| au_dollar | "$150" = AUD 150 (~USD 98) | US store, USD | FAIL |
| cad_dollar | "$200" = CAD 200 (~USD 146) | US store, USD | FAIL |
| jp_fy | Japanese "FY2026" = Apr 2026–Mar 2027 | US company, calendar FY | FAIL |
| au_fy | Australian "FY26" = Jul 2025–Jun 2026 | US company, calendar FY | FAIL |
| dutch_half_eight | Dutch "half acht" said as "half eight" = 19:30 | London scheduler (UK "half eight" = 20:30) | FAIL |
| in_date | Indian "04-05-2027" = 4 May 2027 | US MM-DD | FAIL |
| kmh_speed | "limit 50" meaning 50 km/h | US fleet system in mph | FAIL |
| iso_week | German "KW 14 2027" | US scheduler (ISO date) | PASS |
| uk_phone | UK mobile "07700 900123" | US system requiring E.164 | PASS |
| body_temp_c | "38 degrees" (patient fever, Celsius) | US nurse system in °F | PASS |
