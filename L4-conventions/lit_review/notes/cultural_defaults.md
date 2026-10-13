# Cultural defaults and the "infer-but-don't-apply" gap: related work for the L4 paper ("Bare Numbers Between Agents")

Scope: prior work on (a) inferring a culture versus applying it, (b) US, Western and English default biases in conventions and values, (c) generalization across locales and measurement systems, (d) what each implies for L4's novelty and framing. Searched 2026-10-07. Every arXiv ID below was opened on its arXiv abs or HTML page, or on its ACL Anthology page, unless it is marked UNVERIFIED. Where a fetched page and an arXiv ID disagree on a date, I say so.

How each entry is laid out: **Citation**, ID/URL. *Finding.* **Relation to L4.** Positioning sentence ("Pos:").

---

## Q1. CAPRI (Miao, Zhu & Shwartz 2026): tasks, models, cultures, findings, fix, what it did not study, follow-ups

### Takeaway
CAPRI is the direct single-agent precursor of L4. Nine open or small VLMs infer the user's country from implicit cues almost perfectly, but they lag in answering with local units unless a two-step "Pragmatic CoT" makes them name the country first. Two of its results matter most for L4. On culture-neutral conversations, models default to the US as the country but to **metric** units; currency is the exception, where USD dominates (98% for Gemini). And CAPRI never studies agents, tools, relays, clarification or frontier closed models. As of 2026-10-07, Semantic Scholar indexes **zero** papers citing it.

### Cited Findings
- **Citation:** Yisong Miao, Jian Zhu, Vered Shwartz. "LLMs Infer Cultural Context but Fail to Apply It When Responding." arXiv:2606.17688, submitted 16 Jun 2026. The comments field reads "9 pages, 7 figures, 2 tables (24 pages with appendices)" and names no venue; the dataset card's BibTeX is `@misc`. [arXiv abs](https://arxiv.org/abs/2606.17688); [code/data](https://github.com/YisongMiao/CAPRI)
- **Abstract claim:** "models can infer cultural background and recall relevant conventions, but often fail to utilize the information to adapt their answers to the relevant cultural conventions, unless explicitly prompted to perform the tasks sequentially". It also says priors "are not culture-neutral, sometimes aligning with the model's country of origin." — [arXiv abs](https://arxiv.org/abs/2606.17688)
- **Tasks:**
  - Task 1 is background inference (BG): predict the user's country, or "unknown".
  - Task 2, the primary task, is VQA: answer an image question in the user's local units.
  - Objective dimensions: temperature, distance, speed, size and price, each with a ground-truth unit key per culture.
  - Subjective dimensions: time expressions and quantifiers.
  - Size: 172 images, 516 scaffolds, 4,992 implicit and 516 neutral conversations. — [CAPRI dataset card (local copy of repo README)](https://github.com/YisongMiao/CAPRI)
- **Cultures (10):** Brazil, China, France, India, Iran, Israel, Japan, South Korea, UK, US. — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **Models:**
  - Listed in the HTML: Llama-3.2-11B-Vision-Instruct; Qwen3-VL-8B/32B in Instruct and Thinking variants; Gemma-4-E2B/E4B/31B-it; Gemini-3.1-Flash-Lite.
  - The extraction tool also called these "seven" models while listing nine, so the exact count needs checking in the paper.
  - **No GPT or Claude models, and no frontier-scale closed model apart from Gemini Flash-Lite.** — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **Cues:** names ("James" for the US, "Zhang Wei" for China), phone-number formats, postal codes, shopping platforms (Fnac, Flipkart, Coupang), news sources, electrical standards and dates. — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **Six cue levels:** Null, Neutral, ImplicitCue1, ImplicitCue2, ImplicitFull and ExplicitFull ("I am from [country]"). — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **Main gap (verbatim):**
  - "with just one cultural cue (from Neutral to ImplicitCue1), background prediction jumps sharply from near zero to around 80%, while the VQA task rises much more slowly."
  - Under ImplicitFull, "background prediction is almost perfect, while the VQA task still lags behind."
  - Under ExplicitFull, "the gap narrows for all models except LLaMA."
  - The HTML text gives no per-model unit-accuracy numbers; they appear to be in figures. — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **The fix ("Pragmatic CoT"):**
  - A two-step JSON output: Step 1 is "Reason about the user's background, ending with 'This user is from [country].' or '[unknown]'"; Step 2 answers the question.
  - "Pragmatic CoT improves VQA performance substantially, matching or exceeding the background inference task."
  - Plain CoT also helps, but less.
  - "larger models close the gap between BG and VQA more effectively under Pragmatic CoT" (RQ3, scaling). — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **Neutral-conversation priors (RQ4), verbatim:**
  - "models default to the US for country, yet prefer the metric system (which the US does not use) for measurement units."
  - Price is "an exception, where the dollar dominates (98% for Gemini, other models similar)."
  - On BG, Qwen-32B picks the US on 94% of neutral conversations. — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **Corpus frequencies (infini-gram):**
  - "USD" gets 113M hits, about double all other tested currencies combined (58M).
  - Distance and temperature run about 60% metric; speed about 70% imperial; size roughly equal. — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **Country-of-origin priors (subjective dimensions):**
  - "China is the closest to Qwen-32B's prior", while the US is "the most alien culture for Qwen-32B".
  - Gemini-3.1 places China as most alien under explicit cues. — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **Limitations the authors state:** only 10 countries; English-only data ("introduces a language prior"); country used as a proxy for culture. — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **What CAPRI does not study** (none of these appear in the paper): agent-to-agent communication, tool or function calls, actions that have consequences, asking clarification questions, sender/receiver roles, typed protocols, or frontier closed models (GPT, Claude). — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **Follow-ups:**
  - The Semantic Scholar citations endpoint for arXiv:2606.17688 returned an empty list on 2026-10-07. — [Semantic Scholar API](https://api.semanticscholar.org/graph/v1/paper/arXiv:2606.17688/citations)
  - An automated review (Pith) criticises the abstract for missing sample sizes and statistical tests, and the work for being "narrowly focused on numeric and temporal expressions". — [Pith review](https://pith.science/paper/2606.17688)
- **Relation to L4:** strong support and the closest precedent. L4's "direct" condition (0–5% correct) replicates CAPRI's gap in a tool-action setting; the draft already frames it as "replication ... motivation, not novelty".
- **Pos:** "CAPRI shows that a single model infers a user's culture but does not apply it when answering; we show that the same gap, moved into an agent-to-agent channel, turns into silent wrong actions, and that the convention must be carried by the sender's message rather than recovered by the receiver."

### Inferences
- **CAPRI's metric-unit prior cuts against a simple story that "models default to US units."** CAPRI's own neutral-prompt priors are metric for distance, temperature and size. So L4 senders asserting "5 miles (about 8 km)" for an Iranian user are probably **not** a global imperial prior.
  - The more likely mechanism is **anchoring to the counterpart's or tool's convention**: in L4 the receiver's prompt states its locale, and its tool uses the other convention.
  - "1,500 USD" for a Chinese user, by contrast, matches the documented USD prior (CAPRI 98%; Bui et al. 80%, see Q3).
  - L4 should keep the two apart and report them separately: currency follows a global-default mechanism, while length and speed follow a counterpart-anchoring mechanism.
- **CAPRI's fix (name the country first, then act) is a natural baseline for L4's sender.** L4's "inferred" condition, where the sender infers the locale and publishes it, is the agentic analogue.
  - L4's finding that sender explicitness trades safety for accuracy (questions from the receiver become confident wrong actions) is new relative to CAPRI. CAPRI has no receiver and no option to ask.
- **L4 extends the gap to frontier closed models** (Claude Opus/Sonnet/Haiku/Fable, GPT-6.1). CAPRI's largest models were Qwen3-VL-32B, Gemma-4-31B and Gemini-3.1-Flash-Lite. This is a concrete scope extension L4 can claim.
- **The zero citations suggest L4 may be the first follow-up to build on CAPRI.** Say "builds on" rather than "first to".

### Gaps
- Per-model numeric unit-accuracy values (from the figures) could not be extracted from the HTML.
- Whether CAPRI reports US units chosen for non-US users under implicit cues (the error L4 sees) is not stated in the extracted text.
- Google Scholar "cited by" could not be queried from this environment. Only Semantic Scholar was checked.
- No peer-reviewed venue is listed for CAPRI as of the fetch. One search snippet said "October 2026", but that is unverified and probably wrong.

---

## Q2. Evidence that LLMs default to US/Anglo conventions and values when culture is unstated or only implicit

### Takeaway
There is strong, recent, peer-reviewed evidence of US-locale defaults in factual answers. LocQA (ACL 2026) finds US answers at 50% of outputs against 26% in the data, with the bias **amplified by instruction tuning**. Defaults extend to American English (AmE favoured in all 6 pretraining corpora and 21 post-training datasets), to US-like values and opinions (alignment increases US similarity), and to Western entities. For **units specifically**, the evidence is mixed. USD is a robust default (80–98%). Length and temperature defaults are metric in neutral contexts, but imperial when the subject of the question is located in the US. I found no published paper documenting °F or MM/DD defaults for non-US users with numbers.

### Cited Findings
- **LocQA.**
  - **Citation:** Guy Mor-Lan, Omer Goldman, Matan Eyal, Adi Mayrav Gilady, Sivan Eiger, Idan Szpektor, Avinatan Hassidim, Yossi Matias, Reut Tsarfaty. "Location Not Found: Exposing Implicit Local and Global Biases in Multilingual LLMs." ACL 2026 (main). arXiv:2604.19292. [arXiv](https://arxiv.org/abs/2604.19292); [ACL Anthology 2026.acl-long.1344](https://aclanthology.org/2026.acl-long.1344/); [data](https://github.com/google-research-datasets/locqa/)
  - *Finding:*
    - LocQA has 2,156 locale-ambiguous questions in 12 languages, on laws, dates and measurements.
    - Average global US bias B_US is 0.24 across 32 models: US answers make up 50% of outputs against 26% in the data. It ranges from about 0 (Falcon 3) to 0.42 (Grok 4).
    - The bias **increases after instruction tuning** in every family tested (Gemma 3, Qwen, OLMo-3, Falcon 3, Granite 3).
    - US-centric errors are typed as Intrusion 17.5%, Selection 8.7% and Erasure 6.5%. — [arXiv HTML](https://arxiv.org/html/2604.19292v1)
  - **Relation:** supports. It is the best citation for a "US default under locale ambiguity" that alignment makes worse.
  - **Pos:** "LocQA shows instruction-tuned models resolve locale-ambiguous questions toward the US; L4 shows the same resolution happens when an agent *writes* a unit for its principal, and that it is acted on downstream."
- **American English as the default.**
  - **Citation:** Mir Tafseer Nayeem, Davood Rafiei. "How Does 'English (US)' Become the Default? Triangulating Structural Bias Towards American English Across the LLM Pipeline." arXiv:2604.04204 (v1 5 Apr 2026, rev. 28 Sep 2026; no venue listed). [arXiv](https://arxiv.org/abs/2604.04204)
  - *Finding:*
    - They build 1,813 AmE/BrE matched pairs and the DiAlign measure.
    - "AmE is consistently favored across all six audited pretraining corpora and 21 post-training datasets".
    - AmE is cheaper for tokenizers and models to predict.
    - British-English prompting shifts but "does not consistently eliminate" the AmE default. — [arXiv](https://arxiv.org/abs/2604.04204); [summary](https://awesomepapers.io/machine-learning/papers/hf2604.04204)
  - **Relation:** supports. It gives the structural reason "writing in English" pulls toward US conventions.
  - **Pos:** "English output itself is structurally US-defaulted (Nayeem & Rafiei 2026); L4's senders write English messages to receivers, which is exactly where US units leak in."
- **Alignment and global representation.**
  - **Citation:** Michael J. Ryan, William Held, Diyi Yang. "Unintended Impacts of LLM Alignment on Global Representation." ACL 2024 (main). arXiv:2402.15018. [arXiv](https://arxiv.org/abs/2402.15018); [ACL Anthology 2024.acl-long.853](https://aclanthology.org/2024.acl-long.853/)
  - *Finding:*
    - RLHF/DPO alignment raises the similarity of model opinions to US opinions relative to China, Jordan and Nigeria, and creates disparities across English dialects.
    - The Starling reward model "rates 99.4% of all other countries more negatively than the USA." — [arXiv](https://arxiv.org/abs/2402.15018); figure via [arXiv HTML search snippet](https://arxiv.org/html/2402.15018v2)
  - **Relation:** supports, and suggests a mechanism: preference tuning pushes toward the US.
  - **Pos:** "Alignment is known to shift models toward US perspectives (Ryan et al. 2024; Mor-Lan et al. 2026); L4 tests whether this extends to the units an agent asserts on a user's behalf."
- **Cultural values.**
  - **Citation:** Yan Tao, Olga Viberg, Ryan S. Baker, René F. Kizilcec. "Cultural Bias and Cultural Alignment of Large Language Models." *PNAS Nexus* 3(9), Sept 2024. arXiv:2311.14096. [arXiv](https://arxiv.org/abs/2311.14096)
  - *Finding:* GPT-3 through GPT-4o "exhibit cultural values resembling English-speaking and Protestant European countries". Cultural prompting improves alignment for 71–81% of countries for GPT-4, 4-turbo and 4o. — [arXiv](https://arxiv.org/abs/2311.14096)
  - **Relation:** supports a Western default. Its fix (state the culture) parallels L4's oracle-locale card.
  - **Pos:** "As with cultural prompting for values (Tao et al. 2024), telling the agent the locale helps; L4's question is who in a multi-agent channel should know and state it."
- **WEIRD psychology.**
  - **Citation:** Mohammad Atari, Mona J. Xue, Peter S. Park, Damián Blasi, Joseph Henrich. "Which Humans?" PsyArXiv preprint, Sept 2023. [OSF/PsyArXiv 5b26t](https://osf.io/preprints/psyarxiv/5b26t)
  - *Finding:* LLM responses on psychological measures most resemble WEIRD populations, and similarity falls with cultural distance from the US (r = −.70). — [OSF](https://osf.io/preprints/psyarxiv/5b26t)
  - **Relation:** background citation for the "WEIRD default". It covers values, not conventions.
  - **Pos:** one clause in the intro: "LLMs mirror WEIRD populations (Atari et al. 2023)".
- **Western entities in Arabic.**
  - **Citation:** Tarek Naous, Michael J. Ryan, Alan Ritter, Wei Xu. "Having Beer after Prayer? Measuring Cultural Bias in Large Language Models." ACL 2024 (main), pp. 16366–16393; Best Social Impact Paper. arXiv:2305.14456. [ACL Anthology 2024.acl-long.862](https://aclanthology.org/2024.acl-long.862/); [arXiv](https://arxiv.org/abs/2305.14456)
  - *Finding:* in CAMeL (628 prompts, 20,368 entities, 8 types), 16 LMs favour Western entities even in Arabic contexts and show an "inability to appropriately adapt to Arab cultural contexts". — [arXiv](https://arxiv.org/abs/2305.14456)
  - **Relation:** supports (Western default even when the context signals non-Western).
  - **Pos:** "Western defaults persist even when the context marks a non-Western user (Naous et al. 2024); L4 measures the same for units in agent messages."
- **Measurement-system defaults:** Bui et al., ACL 2025, report USD as the default 80% of the time (details under Q3). — [arXiv HTML](https://arxiv.org/html/2506.02591v1)
- **CAPRI neutral prior:** country defaults to the US, units default to metric, and price to USD at 98% for Gemini (details under Q1). — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
- **Survey framing:** CAPRI's related work groups the Western-centrism evidence as Hershcovich et al. 2022, Cao et al. 2023 and Durmus et al. 2024. These are cited by CAPRI and their IDs were not opened here (UNVERIFIED). — [CAPRI HTML](https://arxiv.org/html/2606.17688v1)
- **Date order:** DateLogicQA (NAACL 2025 SRW) benchmarks temporal and date-format biases. I saw only the title and anchor, not the content, so it is UNVERIFIED for numbers. It is probably covered by the parallel date-ambiguity note. — [ACL Anthology 2025.naacl-srw.32](https://aclanthology.org/2025.naacl-srw.32.pdf)

### Inferences
- The literature supports "US default" robustly for **locale-dependent facts** (LocQA), **English variety** (Nayeem & Rafiei), **values and opinions** (Ryan; Tao; Atari) and **currency** (CAPRI; Bui). For **length, speed and temperature in neutral prompts** it does *not* support a US default (CAPRI: metric). L4's wording should be specific, e.g.: "currency defaults to USD, consistent with prior work; distance and speed are asserted in the counterpart's (US) units, which prior neutral-prompt priors do not predict."
- LocQA's "alignment tax" makes a testable prediction for L4: instruction-tuned senders should assert US units more than base models. L4 can test this only with an open-weight sender (e.g., Ling or a Qwen base/instruct pair).
- LocQA's Intrusion/Selection/Erasure taxonomy maps directly onto L4 sender messages:
  - Intrusion: adding a US gloss ("5 km (3.1 miles)").
  - Selection: choosing USD over CNY.
  - Erasure: replacing km with miles.

### Gaps
- I found no peer-reviewed paper with numbers on °F or MM/DD defaults for non-US users in generation. CAPRI covers temperature, but its neutral prior is metric (°C). The date-order evidence (DateLogicQA) was not opened.
- I found no paper measuring US-unit defaults in English *agent-to-agent* messages.
- The Hershcovich 2022, Cao 2023 and Durmus 2024 IDs were not opened (UNVERIFIED).

---

## Q3. "On Generalization across Measurement Systems" (arXiv:2506.02591) and other work on robustness to measurement systems

### Takeaway
Bui et al. (ACL 2025) show that models default to the dominant system in the data: USD for 80% of currency answers, and units tied to the **location of the entity being asked about**, so 73% imperial for US city distances and 100% metric for German, Japanese, Russian and Chinese cities. Accuracy is unstable across systems. CoT fixes part of this at 2–3× the test-time compute, which the authors frame as a cost charged to underrepresented cultures. Follow-ups show LLM answers change under unit-converted or reformatted but numerically equivalent inputs.

### Cited Findings
- **Bui et al.**
  - **Citation:** Minh Duc Bui, Kyung Eun Park, Goran Glavaš, Fabian David Schmidt, Katharina von der Wense. "On Generalization across Measurement Systems: LLMs Entail More Test-Time Compute for Underrepresented Cultures." ACL 2025 (Long), pp. 21262–21276, DOI 10.18653/v1/2025.acl-long.1032. arXiv:2506.02591. [arXiv](https://arxiv.org/abs/2506.02591); [ACL Anthology](https://aclanthology.org/2025.acl-long.1032/)
  - *Models:* seven open models: Qwen2.5 (72B, 7B), Llama 3.3 and 3.1 (70B-class, 8B; the extraction said "72B" for Llama, which is not a real size), Aya Expanse (32B, 8B). Prompts are English, and the location is given via cities or countries rather than as the user's culture. — [arXiv HTML](https://arxiv.org/html/2506.02591v1)
  - *Findings (verbatim):*
    - "For fiscal data, LLMs predominantly default to using USD (80% on average), and almost exclusively rely on either USD or local currency (17% on average)."
    - "distances in Germany, Japan, Russia and China are reported solely in the metric system, whereas, for city distances in the USA, 73% are expressed in the imperial system."
    - "For weight measurements, LLMs strictly employ either the imperial or metric system, in line with the data context."
    - "Sequential incur a cost up to 199% of the cost without reasoning, whereas CoT on average increases the test-time compute cost to 300% for currency conversions and around 200% for weight and length system conversions." — [arXiv HTML](https://arxiv.org/html/2506.02591v1)
    - An extracted summary also said accuracy is about 34% worse for currencies of low-income countries. That figure was not quoted verbatim; treat it as UNVERIFIED.
  - **Relation:** supports (default to the dominant system) and contrasts. Their defaults are conditioned on the *entity's* location, not the *user's*. L4's conflict is user locale against counterpart locale.
  - **Pos:** "Bui et al. (2025) show models answer in the system of the place being discussed and default to USD for money; L4 isolates a different axis — the *principal's* locale versus the *counterpart's* — and shows the counterpart wins in the sender's message."
- **NUMCoT.**
  - **Citation:** Ancheng Xu, Minghuan Tan, Lei Wang, Min Yang, Ruifeng Xu. "NUMCoT: Numerals and Units of Measurement in Chain-of-Thought Reasoning using Large Language Models." Findings of ACL 2024. arXiv:2406.02864. [arXiv](https://arxiv.org/abs/2406.02864)
  - *Finding:* perturbing numerals and units (including ancient Chinese units) makes math problems markedly harder; LLMs struggle with "handling numeral and measurement conversions." — [arXiv](https://arxiv.org/abs/2406.02864)
  - **Relation:** contrast. It is about conversion skill. L4 failures are about *whether* to convert, not how; models convert correctly once a unit is stated.
  - **Pos:** "Unlike conversion-skill benchmarks (NUMCoT), L4's failures occur even though every model converts correctly when told the unit."
- **Same Quantity, Different Answer.**
  - **Citation:** Ephraim Atta-Duncan. "Same Quantity, Different Answer: Numerical Representation Invariance in Language Models." arXiv:2609.25009. The fetched page gives the submission date as 27 Jul 2026, which conflicts with the 2609 prefix; check this. [arXiv](https://arxiv.org/abs/2609.25009)
  - *Finding:* 3,600 exact-rational problems and 8,600 prompts across five transformations, one of them "exactly converted unit", on five open-weight models. Mistral Small 4 scores 0.699 on unit-converted inputs, with 265 errors that are off by exact powers of ten. — [arXiv](https://arxiv.org/abs/2609.25009)
  - **Relation:** contrast/background (representation invariance).
  - **Pos:** footnote only.
- **Scripts and formats.**
  - **Citation:** Varshini Reddy, Craig W. Schmidt, Seth Ebner, Adam Wiemerslage, Yuval Pinter, Chris Tanner. "The Effect of Scripts and Formats on LLM Numeracy." arXiv:2601.15251 (21 Jan 2026). [arXiv](https://arxiv.org/abs/2601.15251)
  - *Finding:* numeracy "drops substantially when numerical inputs are rendered in underrepresented scripts or formats," and targeted prompting "can greatly narrow this gap." — [arXiv](https://arxiv.org/abs/2601.15251)
  - **Relation:** borrowable for L4's planned decimal-comma and lakh/crore expansion (not confirmed to be covered in the paper).
  - **Pos:** "Format-induced numeracy drops (Reddy et al. 2026) are a separate failure; L4 holds format fixed and varies the unit convention only."
- **Other citers of Bui et al.** (from Semantic Scholar; titles only, abstracts not opened, UNVERIFIED): arXiv:2606.03982 "Language Models Compare Quantities Using Number-specific and Unit-specific Heuristics"; arXiv:2609.22494 (CultureMINE survey, verified: NLP+CSS workshop 2026, 375+ papers surveyed, no mention of units in the abstract). — [Semantic Scholar API](https://api.semanticscholar.org/graph/v1/paper/arXiv:2506.02591/citations); [arXiv 2609.22494](https://arxiv.org/abs/2609.22494)
- **Recipe adaptation.**
  - **Citation:** Yong Cao et al. "Cultural Adaptation of Recipes." TACL 2024 (2024.tacl-1.5). arXiv:2310.17353. The full author list was not opened (UNVERIFIED). [ACL Anthology](https://aclanthology.org/2024.tacl-1.5/); [arXiv](https://arxiv.org/abs/2310.17353)
  - *Finding:* adapting Chinese↔English recipes requires changes to "style, ingredients, measurement units, tools, techniques, and action order". GPT-4 adapts Chinese→English well but lags humans on English→Chinese. — [MIT Press TACL](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00634/119279/Cultural-Adaptation-of-Recipes)
  - **Relation:** contrast. There the target culture is *explicit* in the task; in L4 it is implicit and must be inferred.
  - **Pos:** "In cultural adaptation tasks the target culture is given (Cao et al. 2024); in delegation it must be inferred by one agent and transmitted to another."
- **Real-world motivation:** the Mars Climate Orbiter was lost in 1999 because one team's software output pound-force-seconds while the interface specification and the consuming software expected newton-seconds. It is a canonical case of a silent unit mismatch between organisations. — [NASA JPL](https://www.jpl.nasa.gov/missions/mars-climate-orbiter/); [Wikipedia summary](https://en.wikipedia.org/wiki/Mars_Climate_Orbiter)

### Inferences
- **Bui et al.'s location-conditioned defaults suggest a specific confound for L4.** If a CAPRI conversation mentions a US entity, or the receiver is US-located, the sender may pick imperial units because of the discussed location rather than a global US prior. This should be controlled (see Experiment ideas).
- **Bui et al.'s compute-cost framing transfers directly.** L4's explicit and typed protocols add tokens and rounds. Reporting the extra tokens per culture would let L4 say whether non-US principals "pay more" for correct delegation.
- **Every measurement-system paper found is single-agent QA.** None studies a unit *asserted in a message* and then acted on by another agent.

### Gaps
- Bui et al.'s exact per-model and per-system accuracy deltas (MAPD) were not reliably extracted; the "34% worse" figure is UNVERIFIED.
- I found no measurement-system paper that conditions on the user's culture inferred from implicit cues, other than CAPRI.

---

## Q4. Implicit personalization and demographic inference from conversation: do models act on what they infer?

### Takeaway
Models infer user attributes from implicit text very well: up to 85% top-1 on location, income and sex from Reddit profiles. They also form internal "user models". *Whether* they act on these inferences depends on the task. For values and decisions they do act on them, often harmfully (dialect prejudice; implicit personalization of recommendations). For pragmatics and conventions they mostly do not: about one fifth of the explicit-instruction shift is recovered under implicit cues (Nasim et al.), and CAPRI shows the same for units. This asymmetry ("acts on stereotypes, not on conventions") is a useful framing hook for L4.

### Cited Findings
- **Implicit personalization.**
  - **Citation:** Zhijing Jin, Nils Heil, Jiarui Liu, Shehzaad Dhuliawala, Yahang Qi, Bernhard Schölkopf, Rada Mihalcea, Mrinmaya Sachan. "Implicit Personalization in Language Models: A Systematic Study." Findings of EMNLP 2024. arXiv:2405.14808. [arXiv](https://arxiv.org/abs/2405.14808); [ACL Anthology 2024.findings-emnlp.717](https://aclanthology.org/2024.findings-emnlp.717/)
  - *Finding:* defines Implicit Personalization (IP) as "language models inferring a user's background from the implicit cues in the input prompts and tailoring the response based on this inference". Formalises it with a structural causal model and "indirect intervention", and gives a moral-reasoning framework for when IP is appropriate. — [arXiv](https://arxiv.org/abs/2405.14808)
  - **Relation:** framing to borrow. L4's failure is *missing* implicit personalization where it is clearly appropriate (unit choice), followed by transmitting the unpersonalized value.
  - **Pos:** "Implicit personalization (Jin et al. 2024) is usually studied as a risk; L4 is a case where IP is required and absent, and the absence propagates across agents."
- **Locating and controlling IP.**
  - **Citation:** Yueru Yan, Siqi Wu, Thai Le. "Locating and Controlling Implicit Personalization in Large Language Models." arXiv:2608.11735 (12 Aug 2026; no venue listed). [arXiv](https://arxiv.org/abs/2608.11735)
  - *Finding:*
    - Matched cued and neutral conversations across five LLMs; a localized activation signal tracks shifts in recommendations (r up to 0.87).
    - Cue signals combine roughly additively inside the model, but output changes do not.
    - Ablating the signal suppresses a cue's influence "often more effectively than asking the model to ignore demographics via prompting". — [arXiv](https://arxiv.org/abs/2608.11735)
  - **Relation:** borrowable method (matched cued and neutral conversations, which CAPRI provides; activation probing).
  - **Pos:** "Implicit cues are represented internally and causally steer outputs (Yan et al. 2026); L4's behavioral probe shows the locale is recoverable, so the failure is in its use, not its encoding."
- **User-model dashboard.**
  - **Citation:** Yida Chen, Aoyu Wu, Trevor DePodesta, Catherine Yeh, Kenneth Li, Nicholas Castillo Marin, Oam Patel, Jan Riecke, Shivam Raval, Olivia Seow, Martin Wattenberg, Fernanda Viégas. "Designing a Dashboard for Transparency and Control of Conversational AI." arXiv:2406.07882 (2024). [arXiv](https://arxiv.org/abs/2406.07882)
  - *Finding:* from an open LLM's internal state "we can extract data related to a user's age, gender, educational level, and socioeconomic status", and steering that internal user model changes behavior. — [arXiv](https://arxiv.org/abs/2406.07882)
  - **Relation:** supports "inferred but latent". The method (a linear probe for user country) could strengthen L4's probe with an open-weight sender.
  - **Pos:** "Models maintain internal user models (Chen et al. 2024); L4 asks whether such a model's locale field is ever written into an outgoing agent message."
- **Inference from text.**
  - **Citation:** Robin Staab, Mark Vero, Mislav Balunović, Martin Vechev. "Beyond Memorization: Violating Privacy Via Inference with Large Language Models." arXiv:2310.07298 (v1 Oct 2023, rev. May 2024). ICLR 2024 per my knowledge; the venue was not shown on the page (UNVERIFIED). [arXiv](https://arxiv.org/abs/2310.07298)
  - *Finding:* LLMs infer location, income, sex and other attributes from real Reddit text with "up to 85% top-1 and 95% top-3 accuracy", 100× cheaper and 240× faster than humans. — [arXiv](https://arxiv.org/abs/2310.07298)
  - **Relation:** supports the "infer" half. Contrast with L4's ~30% wrong locale inference by senders, likely because CAPRI cues are sparse.
  - **Pos:** "Locale inference from implicit text is a known LLM strength (Staab et al. 2024), so failures to apply it are not failures of perception."
- **Dialect prejudice.**
  - **Citation:** Valentin Hofmann, Pratyusha Ria Kalluri, Dan Jurafsky, Sharese King. "AI generates covertly racist decisions about people based on their dialect." *Nature* 633, 147–154 (2024). arXiv:2403.00742 (preprint title "Dialect prejudice predicts AI decisions about people's character, employability, and criminality"). [Nature](https://www.nature.com/articles/s41586-024-07856-5); [arXiv](https://arxiv.org/abs/2403.00742)
  - *Finding:* given African American English, models are "more likely to suggest that speakers of African American English be assigned less prestigious jobs, be convicted of crimes, and be sentenced to death". Human-feedback training does not remove this covert bias. — [arXiv](https://arxiv.org/abs/2403.00742)
  - **Relation:** contrast. Models *do* act on implicit cues when the action is a social judgement, so "infer but don't apply" is selective.
  - **Pos:** "Implicit cues can drive model decisions strongly (Hofmann et al. 2024); conventions are a case where the cue is perceived yet ignored."
- **Implicit pragmatic adaptation.**
  - **Citation:** Mehwish Nasim, Sanjeevan Selvaganapathy, Neel Ganapathi Sabhahit, Marie Griesbach, Pranav Bhandari, Janina Lütke Stockdiek, Lennart Schäpermeier, Usman Naseem, Christian Grimme. "Do LLMs Use Cultural Knowledge Without Being Told? A Multilingual Evaluation of Implicit Pragmatic Adaptation." arXiv:2604.17718 (20 Apr 2026; no venue listed). [arXiv](https://arxiv.org/abs/2604.17718)
  - *Finding:*
    - English, German, Hindi, Nepali and Urdu; 12 pragmatic features; three prompt types (neutral, explicit cultural instruction, implicit situational cue).
    - Pragmatic Context Sensitivity (PCS) is the fraction of the neutral→explicit shift that reappears under neutral→implicit. Models recover about **one fifth**: authority cues 0.299, individual-versus-group framing 0.120.
    - Hindi vs Urdu shows no difference (t=0.96, p=0.339), which suggests responses to linguistic form rather than to culture. — [arXiv](https://arxiv.org/abs/2604.17718)
  - **Relation:** supports. It is an independent replication of infer-but-don't-apply in pragmatics, and its PCS metric is borrowable.
  - **Pos:** "Implicit cultural cues recover only ~20% of the adaptation that explicit instructions produce (Nasim et al. 2026); L4 finds an analogous ratio for units in agent messages."

### Inferences
- **The literature gives L4 an asymmetry to name.** Models act on implicit cues for stereotyped *judgements* (Hofmann; Jin) but not for *conventions and pragmatics* (CAPRI; Nasim). A plausible explanation (untested) is that conventions are "formatting" that RLHF-trained writers fill with the dominant default, while judgements draw on associations.
- **L4's behavioral probe can be strengthened.** It currently asks the model for the user's country. Chen et al. and Yan et al. show internal probes and steering on open models. A linear probe on Ling or a Qwen sender would make "identifies but does not apply" mechanistic rather than behavioral.
- **L4's ~30% wrong locale inference by senders is worse than Staab's 85% top-1.** The likely cause is CAPRI's deliberately weak cues (one or two per conversation). L4 should cite CAPRI's own BG numbers (about 80% after one cue, near-perfect at ImplicitFull) for comparison.

### Gaps
- No paper found tests implicit personalization in *messages to another agent*, or whether inferred user attributes are passed on.
- Jin et al.'s case studies were not extracted in detail. The abstract alone does not say whether they include locale or units.

---

## Q5. Cultural benchmarks, one line each: do they measure application of conventions in actions, and which is closest to L4?

### Takeaway
None of the listed benchmarks measures a locale convention applied inside a tool action delegated between agents. The closest on *conventions* are CAPRI (units, single-agent answer) and Numerical Localisation (times, numbers and dates in translation). The closest on *agentic action* are WorldBench (culturally grounded sandbox workflows) and CASA (web agents and norms). LocQA is closest on *US default under ambiguity*.

### Cited Findings
- **CulturalBench.**
  - **Citation:** Yu Ying Chiu, Liwei Jiang, Bill Yuchen Lin, Chan Young Park, Shuyue Stella Li, Sahithya Ravi, Mehar Bhatia, Maria Antoniak, Yulia Tsvetkov, Vered Shwartz, Yejin Choi. "CulturalBench: A Robust, Diverse, and Challenging Cultural Benchmark by Human-AI CulturalTeaming." ACL 2025 (main). arXiv:2410.02677. [arXiv](https://arxiv.org/abs/2410.02677)
  - *Finding:* knowledge QA only: 1,696 questions, 45 regions, 17 topics; humans 92.4%, frontier LMs 28.7–61.5%; weakest on North African, South American and Middle Eastern content. **No application or actions.**
  - **Relation:** contrast, as the "knowledge" side of knowledge-vs-application.
  - **Pos:** "Knowledge benchmarks (CulturalBench, BLEnD) test whether models know conventions; L4 tests whether agents use them."
- **BLEnD.**
  - **Citation:** Junho Myung, Nayeon Lee, Yi Zhou, Jiho Jin, Rifki Afina Putri, Dimosthenis Antypas, Hsuvas Borkakoty, Eunsu Kim, Carla Perez-Almendros, Abinew Ali Ayele, Víctor Gutiérrez-Basulto, Yazmín Ibáñez-García, Hwaran Lee, Shamsuddeen Hassan Muhammad, Kiwoong Park, Anar Sabuhi Rzayev, Nina White, Seid Muhie Yimam, Mohammad Taher Pilehvar, Nedjma Ousidhoum, Jose Camacho-Collados, Alice Oh. "BLEnD: A Benchmark for LLMs on Everyday Knowledge in Diverse Cultures and Languages." NeurIPS 2024 Datasets & Benchmarks. arXiv:2406.09948. [arXiv](https://arxiv.org/abs/2406.09948)
  - *Finding:* everyday-knowledge QA: 52.6k QA pairs, 16 countries, 13 languages; GPT-4 shows a gap of up to 57.34% between well- and under-represented cultures. **No actions.**
  - **Relation:** contrast (knowledge).
  - **Pos:** as above.
- **CASA.**
  - **Citation:** Haoyi Qiu, Alexander R. Fabbri, Divyansh Agarwal, Kung-Hsiang Huang, Sarah Tan, Nanyun Peng, Chien-Sheng Wu. "Evaluating Cultural and Social Awareness of LLM Web Agents." Findings of NAACL 2025. arXiv:2410.23252. [arXiv](https://arxiv.org/abs/2410.23252)
  - *Finding:* web agents (online shopping, social forums) must detect and handle norm-violating user queries; agents show "less than 10% awareness coverage and over 40% violation rates". **Actions: yes. Conventions or units: no.**
  - **Relation:** contrast/borrowable (agentic cultural evaluation, "awareness coverage" metric).
  - **Pos:** "CASA evaluates whether web agents respect cultural *norms*; L4 evaluates whether delegating agents preserve cultural *conventions* across an organisational boundary."
- **WorldBench.**
  - **Citation:** Leonardo Ranaldi, Sherrie Shen, Jushi Kai, Alexandra Birch. "WorldBench: Culturally Grounded Benchmark for Multilingual Agents." arXiv:2609.01056 (1 Sep 2026; no venue listed). [arXiv](https://arxiv.org/abs/2609.01056)
  - *Finding:* 1,600 persona-grounded everyday workflows in 7 languages and 8 cultures, with agents acting through structured sandbox actions. Frontier models reach 49.2% Constrained Task Success, with large gaps between correctness and environment preservation. **Actions: yes. Whether locale conventions are tested: not stated in the abstract.**
  - **Relation:** **potential partial novelty threat.** It is the closest agentic cultural benchmark; single-agent, and the culture is persona-given (probably explicit).
  - **Pos:** "WorldBench grounds single agents in a culture's workflows; L4 asks what survives when a culture-aware agent hands a number to an agent grounded in a different culture."
- **Terminal-Bench-LILT.**
  - **Citation:** Yunsu Kim, Kaden Uhlig, Ashwin Purohit, Milind Agarwal, Patrick Simianer, Anil Arslan, Kiarash Mokhtari, Thomas Zenkel, Johannes Mosig, Gabriel Bretschner, Shamik Bose, Joern Wuebker, John DeNero. "Terminal-Bench-LILT: Multilingual Agentic Coding Benchmark Grounded in Language, Region, and Culture." arXiv:2608.28641 (11 Aug 2026). [arXiv](https://arxiv.org/abs/2608.28641)
  - *Finding:* 300 coding tasks in 10 languages (ar, cs, de, es, hi, ja, ko, sr, tr, zh) on "internationalization, encoding, text normalization, and cultural conventions." **Actions: yes (code). Locale is explicit in the task. Which conventions: not enumerated in the abstract.**
  - **Relation:** contrast. Conventions appear as code requirements, not as an implicit principal's intent.
  - **Pos:** "i18n coding benchmarks (Terminal-Bench-LILT) test whether agents implement locale conventions when asked; L4 tests whether they infer and transmit them when not asked."
- **Numerical Localisation.**
  - **Citation:** Patrizia Kaye. "Analysis of Numerical Localisation in LLM Translations." arXiv:2608.05232 (5 Aug 2026; 13 pp.; no venue listed). [arXiv](https://arxiv.org/abs/2608.05232)
  - *Finding:* five LLMs translating text must *localise* times, numbers and dates rather than translate them. Of three strategies, "embedding the localisation principles into the prompt context provided a statistically significant improvement."
  - **Relation:** closest on the *convention* object, with a prompt fix that parallels L4's explicitness instruction. The target locale is given and there is no action.
  - **Pos:** "Localisation in translation improves when principles are in the prompt (Kaye 2026); in delegation the analogous instruction ('state units explicitly') raises accuracy but imports the sender's US default."
- **LocQA** (see Q2): locale-ambiguous QA; measures the US default, not actions. Closest on the *default* phenomenon. — [arXiv](https://arxiv.org/abs/2604.19292)
- **NormAd.**
  - **Citation:** Abhinav Rao, Akhila Yerukola, Vishwa Shah, Katharina Reinecke, Maarten Sap. "NormAd: A Framework for Measuring the Cultural Adaptability of Large Language Models." NAACL 2025. arXiv:2404.12464. [arXiv](https://arxiv.org/abs/2404.12464); [ACL Anthology PDF](https://aclanthology.org/2025.naacl-long.120.pdf)
  - *Finding:* 2.6k etiquette situations from 75 countries. Even with the relevant norm given, top models score under 82% against humans above 95%. With only abstract values and the country, they fall below 60% against humans above 90%. Performance is stronger for English-centric cultures.
  - **Relation:** supports (adaptation degrades as context becomes implicit). Its graded context levels are borrowable.
  - **Pos:** "As context becomes less explicit, cultural adaptation degrades (NormAd); L4's sender sees the most implicit level and must still write an explicit unit."

### Inferences
- **Ranking by closeness to L4:**
  1. CAPRI (same data, same gap, single agent);
  2. LocQA (US default under ambiguity, alignment amplifies it);
  3. Numerical Localisation (convention conversion, prompt fix);
  4. WorldBench and CASA (cultural agent actions, no convention transfer);
  5. Terminal-Bench-LILT (explicit i18n in code);
  6. CulturalBench and BLEnD (knowledge only).
- **A 2×2 framing table works well in L4's related work.** Rows: knowledge vs application. Columns: single agent vs multi-agent. Every prior benchmark sits in the single-agent column; L4 fills the multi-agent × application cell.

### Gaps
- The WorldBench and Terminal-Bench-LILT full texts were not opened, so it is unconfirmed whether they include unit, currency or date conventions in actions. **Check WorldBench before submission; it is the one most likely to overlap.**
- Whether CASA states the user's culture explicitly in queries was not verified.

---

## Q6. Knowledge vs application ("knowing-doing gap") as a general frame L4 can cite

### Takeaway
"Knowing-doing gap" is an established term for LLM agents. Schmied et al. (ICLR 2026) report correct rationales 87% of the time against optimal actions 21% of the time in decision tasks. In cultural NLP the same split appears for taboos (CulShield, the "Knowledge-Behavior Gap"), norms (NormAd), pragmatics (Nasim et al.) and units (CAPRI). L4 can adopt the term, and its new contribution is that the gap is *distributed across agents*: one agent knows, another acts.

### Cited Findings
- **Greedy agents.**
  - **Citation:** Thomas Schmied, Jörg Bornschein, Jordi Grau-Moya, Markus Wulfmeier, Razvan Pascanu. "LLMs are Greedy Agents: Effects of RL Fine-tuning on Decision-Making Abilities." arXiv:2504.16078 (22 Apr 2025). ICLR 2026 per the ML Anthology listing. [arXiv](https://arxiv.org/abs/2504.16078); [ML Anthology](https://mlanthology.org/iclr/2026/schmied2026iclr-llms/)
  - *Finding:*
    - It names three failure modes: greediness, frequency bias, and the **knowing-doing gap**, "the inability to effectively act on knowledge present in the model".
    - RL fine-tuning on self-generated rationales narrows the gap.
    - The 27B model produced correct rationales 87% of the time but chose the optimal action only 21% of the time. These two numbers come from the arXiv HTML via a search snippet and should be checked against the PDF. — [arXiv](https://arxiv.org/abs/2504.16078); [arXiv HTML](https://arxiv.org/html/2504.16078v1)
  - **Relation:** general frame (supports).
  - **Pos:** "L4 is a knowing-doing gap (Schmied et al. 2026) split across two agents: the sender knows the principal's locale, the receiver acts."
- **CulShield.**
  - **Citation:** Ying He, Sihang Jiang, Xingzhou Chen, Zhouhong Gu, Yiwei Gu, Minggui He, Shimin Tao, Hongxia Ma, Yanghua Xiao. "The 'Knowledge-Behavior Gap' in Cultural Taboo Safety of Large Language Models." arXiv:2608.12341. The fetched page reported 3 Jun 2026, which conflicts with the 2608 prefix; check this. [arXiv](https://arxiv.org/abs/2608.12341)
  - *Finding:* the CulShield benchmark covers 2,020+ taboos across 77 countries and territories; "models often fail to apply known taboos during interaction" (tested models include GPT-4o-mini and Gemini-2.5-pro). — [arXiv](https://arxiv.org/abs/2608.12341)
  - **Relation:** supports. The same gap appears in safety, which shows it is general.
  - **Pos:** "The knowledge–behavior gap recurs across cultural domains (taboos: He et al. 2026; norms: Rao et al. 2025; units: Miao et al. 2026)."
- **NormAd** (see Q5) and **Nasim et al.** (see Q4) are further cultural instances. — [NormAd](https://arxiv.org/abs/2404.12464); [Nasim et al.](https://arxiv.org/abs/2604.17718)
- **CAPRI's own framing:** "CAPRI thus disentangles *knowing* a user's culture from *acting on it*" (dataset card); its abstract calls for "narrowing the gap between cultural knowledge and culturally adaptive language generation". — [CAPRI GitHub](https://github.com/YisongMiao/CAPRI); [arXiv](https://arxiv.org/abs/2606.17688)
- **STOCKTAKE.** "STOCKTAKE: Measuring the Gap Between Perception and Action in LLM Agents with a Fair Oracle." arXiv:2607.13618. The title was seen on arXiv HTML; authors and venue were not opened (UNVERIFIED). A possible general agent frame. — [arXiv HTML](https://arxiv.org/html/2607.13618)

### Inferences
- **Recommended framing:** "infer-but-don't-apply" (CAPRI) is a cultural instance of the knowing-doing gap (Schmied). L4 shows that in multi-agent delegation the gap becomes a **knowledge-location problem**: the agent that knows the convention is not the one that acts. Sender explicitness moves the knowledge into the message, but the sender's English-writing default can corrupt it. This connects CAPRI, Schmied and the US-default literature in one line.

### Gaps
- Schmied et al.'s 87%/21% figures were not seen verbatim on the abs page.
- STOCKTAKE's authors and contents were not verified.

---

## Novelty threats (prior work showing sender-side or agent-side US-default unit anchoring)

### Takeaway
I found **no published or arXiv paper (to 2026-10-07)** showing that an agent writing to another agent asserts US units for a non-US principal, or measuring how conventions get lost in agent-to-agent delegation. The real threats are partial:
- CAPRI owns "infer-but-don't-apply for units" in single-agent answers.
- LocQA, Bui et al. and CAPRI's price prior own "models default to US/USD".
- WorldBench and CASA own "cultural evaluation of acting agents".
- White et al. own "agents from different cultures communicating" (in a game).

L4's defensible novelty is the *channel*: where the convention is lost, which side should carry it, and the accuracy/safety trade-off of sender explicitness.

### Cited Findings
- **Threat 1, CAPRI (high, for claim 1 only).** It already shows the infer-vs-apply gap for the same units on the same data, with a sequential-prompting fix. L4's draft correctly labels the direct condition a replication. — [arXiv](https://arxiv.org/abs/2606.17688)
- **Threat 2, US default in outputs (medium, for the "senders assert US units" finding).**
  - LocQA: the US is chosen for 50% of answers against 26% in the data, and the bias rises with instruction tuning. — [arXiv HTML](https://arxiv.org/html/2604.19292v1)
  - Bui et al.: USD is the default for 80% of currency answers. — [arXiv HTML](https://arxiv.org/html/2506.02591v1)
  - CAPRI: USD for 98% of price answers in neutral contexts. — [arXiv HTML](https://arxiv.org/html/2606.17688v1)
  - Implication: "1,500 USD for a Chinese user" is *predicted* by prior work. Present it as consistent with prior work, not as a discovery.
- **Mitigation: imperial units are not predicted by prior work.** CAPRI reports that in neutral contexts models "prefer the metric system (which the US does not use)". Bui et al. find imperial only when the *entity* is in the US. L4 senders asserting **miles** for an Iranian user is therefore not explained by the known priors. That makes it the more novel half of the US-unit finding, possibly explained by anchoring to the counterpart or tool. — [CAPRI HTML](https://arxiv.org/html/2606.17688v1); [Bui HTML](https://arxiv.org/html/2506.02591v1)
- **Threat 3, cross-cultural communication between agents (low).**
  - **Citation:** Isadora White, Sashrika Pandey, Michelle Pan. "Communicate to Play: Pragmatic Reasoning for Efficient Cross-Cultural Communication in Codenames." Findings of EMNLP 2024. arXiv:2408.04900. [ACL Anthology 2024.findings-emnlp.711](https://aclanthology.org/2024.findings-emnlp.711/); [arXiv](https://arxiv.org/abs/2408.04900)
  - *Finding:* culturally induced differences in common ground cause pragmatic failures between simulated players. RSA+C3 infers the partner's sociocultural context from interaction and improves collaboration.
  - **Relation:** the closest "agents from different cultures communicate" precedent, and a contrast: a game with word associations, not tool-executed quantities. It is also borrowable, since inferring the partner's culture from the interaction could become a receiver-side strategy.
  - **Pos:** "Cross-cultural common-ground failures have been modelled between game-playing agents (White et al. 2024); L4 studies them between delegating agents whose messages are executed by tools."
- **Threat 4, agentic cultural benchmarks (low to medium).** WorldBench (sandbox actions in 8 cultures; the abstract does not say whether conventions are tested) and CASA (norms, not units) are both single-agent. — [WorldBench](https://arxiv.org/abs/2609.01056); [CASA](https://arxiv.org/abs/2410.23252)
- **Threat 5, multi-agent relay and grounding work.** Faithful-Not-Corrective (arXiv:2607.09678) and Talk is Cheap (arXiv:2605.01750) appear in L4's existing prior_work.md. They are outside this note's scope and not re-verified here (cross-reference the parallel note).
- **Searches that returned nothing relevant:** "LLM agent tool call locale mismatch currency units date format", "locale-aware LLM agents user locale inference function calling units currency", "LLM agents negotiation booking assume USD currency default non-US users". Results were tool-failure benchmarks (ToolFailBench, FinToolBench, AgentIF) and negotiation-language papers, none about convention transfer. — [ToolFailBench](https://arxiv.org/html/2607.04686); [Language of Bargaining](https://arxiv.org/html/2601.04387)

### Inferences
- **Claim to make:** "first study of convention loss in agent-to-agent delegation, and of which side of the channel should carry the principal's locale".
- **Claims to avoid:** "first to show LLMs default to USD" (Bui, CAPRI) and "first to show infer-but-don't-apply" (CAPRI).
- **Strongest single novel empirical hook from this literature view:** under an explicitness instruction, senders assert the *counterpart's* units for the principal, against the metric prior prior work documents. If confirmed by a receiver-locale swap (see below), this is "counterpart anchoring", a multi-agent-specific failure no single-agent paper can show.

### Gaps
- WorldBench and Terminal-Bench-LILT full texts were not checked for unit or currency conventions in actions.
- Google Scholar was not searchable here; very recent (Sept–Oct 2026) arXiv postings might be missed by web search.

---

## Experiment ideas borrowed from this literature

### Takeaway
The cheapest high-value additions are three, in order:
1. A **receiver-locale swap**, to separate counterpart anchoring from a US prior.
2. CAPRI's **cue ladder** on the sender, using CAPRI's existing conversation variants.
3. A **Pragmatic-CoT sender baseline**, a direct comparison to CAPRI's fix.

Further options: LocQA's base-vs-instruct test, Nasim's recovery-ratio metric, Bui's per-culture token-cost reporting, and a linear-probe or steering version of the locale probe on the open-weight sender.

### Cited Findings
- **Receiver-locale swap (from Bui et al.'s finding that units follow the location of the entity).** Keep the principal fixed (e.g., Iran) and vary the receiver's locale: US/imperial, UK (mixed: miles for roads, metric elsewhere) and JP/metric with a different currency.
  - If "miles" appears only with US receivers, the cause is counterpart anchoring.
  - If it appears regardless, the cause is a global English/US default.
  - Basis: Bui et al. show units follow the discussed location, and CAPRI shows a metric prior in neutral contexts. — [Bui HTML](https://arxiv.org/html/2506.02591v1); [CAPRI HTML](https://arxiv.org/html/2606.17688v1)
- **CAPRI cue ladder for the sender.** Run explicit-sender conditions on Neutral, ImplicitCue1, ImplicitCue2, ImplicitFull and ExplicitFull variants, which ship with CAPRI, then plot sender inferred-locale accuracy against correct-unit assertion. This shows whether the explicitness trade-off shrinks as cues accumulate. — [CAPRI HTML](https://arxiv.org/html/2606.17688v1)
- **Pragmatic-CoT sender.** Have the sender output "This user is from X" and then the message (CAPRI's two-step JSON). Compare it with L4's "inferred" and "explicit" conditions so that L4 can say it beats or matches the published fix. — [CAPRI HTML](https://arxiv.org/html/2606.17688v1)
- **Base vs instruct ("alignment tax").** With an open-weight sender pair (base and instruct), test whether instruction tuning increases US-unit assertion, as LocQA found for the US-locale bias. — [LocQA HTML](https://arxiv.org/html/2604.19292v1)
- **Implicit recovery ratio (Nasim et al.'s PCS).** Report (implicit-sender correct − bare relay) / (oracle-locale correct − bare relay). Values near 0.2 would match Nasim's ~one-fifth. — [arXiv](https://arxiv.org/abs/2604.17718)
- **Per-culture cost (Bui et al.).** Report tokens and rounds per correctly delegated item by principal culture, to test whether non-US principals need more compute or more clarification turns for the same accuracy. — [Bui HTML](https://arxiv.org/html/2506.02591v1)
- **Error typing (LocQA).** Classify wrong sender messages as Intrusion (an added US gloss), Selection (the US unit chosen) or Erasure (the principal's unit replaced). — [LocQA HTML](https://arxiv.org/html/2604.19292v1)
- **Internal locale probe and steering (Chen et al.; Yan et al.).** On the open-weight sender:
  - Train a linear probe for the principal's country on hidden states at message-writing time; it should be decodable even when the message uses US units.
  - Optionally steer the locale direction, to test whether that fixes the unit without any prompt change. — [Chen et al.](https://arxiv.org/abs/2406.07882); [Yan et al.](https://arxiv.org/abs/2608.11735)
- **Graded explicitness of the principal's context (NormAd).** Add a level where the principal's culture is stated but its convention is not ("I'm from Iran"), between implicit cues and an oracle unit. It separates inference failure from application failure. — [NormAd](https://arxiv.org/abs/2404.12464)
- **Entity-location confound control (Bui et al.).** Write templates where the principal's country differs from the location of the thing being discussed, for example an Iranian user setting a speed alert for a US road trip. This tests whether senders follow the principal or the entity. — [Bui HTML](https://arxiv.org/html/2506.02591v1)
- **Partner-culture inference by the receiver (White et al.'s RSA+C3).** A receiver strategy that infers the sender's or principal's culture from the message itself (name, formatting) before acting, compared with asking a question. — [ACL Anthology](https://aclanthology.org/2024.findings-emnlp.711/)
- **Magnitude of silent errors.** Report the size of the error, not just its rate. For example, 5 mi against 5 km is a factor of about 1.61, while KRW against USD is roughly 1,000× or more. This follows Bui et al.'s MAPD-style error reporting and the powers-of-ten error analysis in Atta-Duncan 2026. — [Bui ACL](https://aclanthology.org/2025.acl-long.1032/); [Atta-Duncan](https://arxiv.org/abs/2609.25009)

### Inferences
- The receiver-locale swap is the single most important addition for novelty. It turns "senders say US units", which is partly predicted by prior work, into "senders anchor on the counterpart", which is multi-agent-specific and unexplained by any single-agent prior.
- The cue ladder and the Pragmatic-CoT baseline reuse CAPRI assets already in the repo (`experiments/good-ideas/L4-conventions/capri/`), so they cost only API calls.

### Gaps
- It was not checked whether L4 currently uses only ImplicitFull conversations. The draft says "CAPRI implicit-cue conversations" without naming the variant.
- The KRW/USD magnitude above is illustrative and depends on the exchange rate L4's tool uses.
