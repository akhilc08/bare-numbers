# Preregistered predictions: false-friend theory of silent convention errors
Written 2026-10-03 BEFORE running `run.py`; committed before results exist.

**Theory:** a receiver agent silently misreads a sender's convention when the expression is (1) valid in the receiver's own convention and (2) yields a plausible value there ("false friend"). When the receiver-convention reading is implausible, or the expression carries an unmistakably foreign marker, the receiver converts or asks.

**Prediction:** silent-wrong rate ≥ 40% for every PREDICTED-FAIL case, and ≤ 15% for every PREDICTED-PASS case (baseline, space-bunny → space-bunny).

| case | sender meaning | receiver's convention | prediction |
|---|---|---|---|
| table_motion | UK "table the budget item" = put it on the agenda to discuss now | US: "table" = postpone or remove | FAIL |
| biweekly | UK "biweekly check-ins" = twice a week | US: biweekly = every two weeks | FAIL |
| uk_pint_recipe | UK "2 pints of milk" for a recipe (1136 ml) | US pint 473 ml → 946 ml | FAIL |
| au_tbsp | Australian "2 tablespoons" (40 ml) | US tbsp 15 ml → 30 ml | FAIL |
| br_date | Brazilian "05/06" (5 June) | US MM/DD → May 6 | FAIL |
| de_ground_floor_one | German "1. Stock" said as "1st floor" (= US 2nd floor) | US floor numbering | FAIL |
| eu_size_xl | EU shoe size 44 to US store | US sizes ≤ ~15 (implausible) | PASS |
| kelvin_room | sender says "set the lab to 295 kelvin" (explicit) | Celsius thermostat | PASS |
| imperial_gallon_explicit | "10 imperial gallons" (explicit marker) | US liters system | PASS |
| uk_date_impossible | UK "25/12/2027" (day > 12, so the US reading is impossible) | US MM/DD | PASS |
| oven_gas_mark | UK "gas mark 4" | US oven in °F | PASS |
| hk_dollar_explicit | "HK$800" | USD system | PASS |
