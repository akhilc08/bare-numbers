# Agent-to-agent protocols, delegation, and information loss in multi-agent relays (related work for L4, "Bare Numbers Between Agents")

Scope: (a) protocol metadata, (b) empirical loss/distortion in relays and handoffs, (c) principal-agent delegation across organisations, (d) implications for L4's novelty and positioning. Verified 2026-10-07. I checked every arXiv ID, title, author list and date against the arXiv API (export.arxiv.org) or the abs page. I read protocol fields from the normative source files (proto/OpenAPI/pydantic) where I could. Items marked UNVERIFIED could not be confirmed from a primary source.

Legend for "Relation": SUPPORTS = evidence for L4's premise; THREAT = overlaps L4's claimed novelty; CONTRAST = differs in a way L4 can use to position itself; METHOD = a method L4 can borrow.

---

## Q1. What metadata do agent communication protocols carry? Any locale, language, region, units, currency or i18n fields?

### Takeaway
None of the agent-to-agent or agent-to-tool protocols (A2A 1.0, MCP, ANP, AGNTCY OASF, OpenAI Agents SDK handoffs, Magentic-One) has a core field for locale, region, currency or measurement system. A2A's "modes" are MIME media types. IBM's ACP had a `natural_languages` field (ISO 639-1), but ACP has since merged into A2A, which has no such field. The open MCP proposal for language negotiation (SEP-2792) explicitly excludes "locale, timezone, currency, calendar, measurement". Currency is typed, as ISO 4217 code plus minor units, only in the payment/checkout layer (AP2, OpenAI/Stripe ACP). The natural-language intent layer, where L4's failure occurs, has no such typing. Classic ACLs (FIPA ACL, KQML) did carry an explicit `ontology` parameter. FIPA nonetheless allowed it to be omitted when "commonly understood", which is exactly the assumption that fails in L4.

### Cited Findings

**Google / Linux Foundation A2A (Agent2Agent) protocol, v1.0.0 (released 2026-03-12; v1.0.1 2026-05-28)**
- The normative `AgentCard` fields in `specification/a2a.proto` are `name`, `description`, `supported_interfaces`, `provider` (AgentProvider: `organization`, `url`), `version`, `documentation_url`, `capabilities`, `security_schemes`, `security_requirements`, `default_input_modes`, `default_output_modes`, `skills`, `signatures` and `icon_url` — [a2a.proto](https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto); [A2A spec §4.4.1](https://a2a-protocol.org/latest/specification/); [releases](https://github.com/a2aproject/A2A/releases)
- `default_input_modes`: "The set of interaction modes that the agent supports across all skills. This can be overridden per skill. Defined as media types." `AgentSkill.input_modes` is defined as "The set of supported input media types for this skill". The "modes" are therefore MIME types, not human languages or locales — [a2a.proto](https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto)
- `AgentSkill` fields: `id`, `name`, `description`, `tags`, `examples`, `input_modes`, `output_modes`, `security_requirements`. `AgentCapabilities` fields: `streaming`, `push_notifications`, `extensions`, `extended_agent_card` — [a2a.proto](https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto)
- I searched the full a2a.proto (812 lines) case-insensitively. It contains 0 occurrences each of "locale", "language", "currency", "timezone", "region", "country" and "i18n". The two hits for "unit" are prose ("core unit of action", "one unit of communication") — [a2a.proto](https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto). This confirms the reviewers' remark that A2A agent cards have no locale field.
- Escape hatches exist:
  - `Message.metadata` and `Part.metadata` are free-form `google.protobuf.Struct` ("Any metadata to provide along with the message").
  - `Part.data` carries "Arbitrary structured `data` as a JSON value".
  - `AgentExtension` has `uri`, `description`, `required` ("If true, the client must understand and comply with the extension's requirements") and `params` — [a2a.proto](https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto)
  - A locale/currency declaration is therefore expressible only as a non-standard extension or as metadata.
- A2A has a protocol-level "ask back" state: `TASK_STATE_INPUT_REQUIRED = 6` ("Indicates that the agent requires additional user input to proceed. This is an interrupted state.") — [a2a.proto](https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto). This is the natural hook for L4's hybrid "receiver asks when confidence is low" channel.
- Issue #2121, "Proposal: Cost and budget propagation extension for multi-agent delegation" (open, 2026-08-09):
  - It proposes `{"budget": {"cost": {"amount": 0.50, "currency": "USD"}, ...}}` in `SendMessageRequest` metadata. The budget is for compute cost, not the user's purchase.
  - It reports that maintainers had judged a related token-visibility request (#1155) to belong "as an opt-in extension, not core spec" — [A2A issue #2121](https://github.com/a2aproject/A2A/issues/2121)
  - Searching A2A issues for "locale" and "i18n" returned no locale proposal. Hits were unrelated (#107, #222) — [A2A issues search](https://github.com/a2aproject/A2A/issues)
- Relation: CONTRAST + METHOD. L4's "locale field in the counterpart's agent card" condition is a counterfactual protocol design: it is not in the spec and must be built as an `AgentExtension`.
- Positioning: "A2A 1.0 standardises what media types an agent accepts but not what conventions its numbers are in; we test what happens when that gap is filled by an extension field, by sender explicitness, or by a receiver-side resolver."

**Model Context Protocol (MCP), tools spec, revision 2025-06-18**
- A Tool definition has `name`, `title`, `description`, `inputSchema` ("JSON Schema defining expected parameters"), `outputSchema` (optional) and `annotations`. Content items carry `mimeType` and annotations (`audience`, `priority`, `lastModified`). There is no locale, units or currency field — [MCP tools spec 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- The spec's own example output schema puts the unit only in free-text descriptions (`"temperature": {"type": "number", "description": "Temperature in celsius"}`), while the unstructured example result says "72°F" — [MCP tools spec 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/server/tools). Units live in prose descriptions, not in typed fields.
- SEP-1809, "Standardized Client Context Propagation (SCCP)", opened 2025-11-13 and closed 2026-06-24:
  - It proposed an optional `clientContext` on `CallToolRequest` with IANA `timezone`, `currentTimestamp` and `locale`.
  - Its motivation: tools "expect formatting/locale awareness (dates, numbers, currency)", and without it servers produce "Formatting that does not match the user's regional expectations (e.g., date order, decimal separator, language)."
  - The closure was procedural ("SEPs have since moved to pull requests"), not a merge.
  - A commenter argued: "If a tool needs timezone/locale, declare it as a parameter" — [MCP SEP-1809](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1809)
- SEP-2792, "Per-Request User Language Preference" (PR open, labelled `in-review`, created 2026-05-26):
  - It adds `params._meta["io.modelcontextprotocol/acceptLanguage"]` (HTTP Accept-Language grammar).
  - It states: "This is language preference only, not a locale, timezone, currency, calendar, measurement, formatting, or translation-infrastructure system." — [MCP PR #2792](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2792)
- An older issue, "Internationalization (i18n) / multilingualism for some text fields ?" (#86), was closed 2024-11-29. I did not read its content — [MCP issue #86](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/86)
- Relation: SUPPORTS + partial THREAT. Practitioners have explicitly named the decimal-separator/currency/locale gap, but the live i18n proposal scopes currency and measurement out. No proposal has been adopted.
- Positioning: "Protocol designers have recognised that tools need the user's locale (MCP SEP-1809) yet the active standardisation track deliberately excludes currency and measurement (SEP-2792); we measure the cost of that exclusion between agents."

**IBM / BeeAI Agent Communication Protocol (ACP), now merged into A2A**
- The ACP OpenAPI `Metadata` schema includes `natural_languages` ("Supported human languages (ISO 639-1 codes)"), `programming_language`, `framework`, `domains` (e.g., 'finance', 'healthcare', 'supply-chain'), `tags`, `annotations` and `capabilities`. `AgentManifest` has `name`, `description`, `input_content_types`, `output_content_types` (MIME, default `*/*`), `metadata` and `status` — [ACP openapi.yaml](https://github.com/i-am-bee/acp/blob/main/docs/spec/openapi.yaml); [ACP manifest docs](https://agentcommunicationprotocol.dev/core-concepts/agent-manifest)
- README: "ACP is now part of A2A under the Linux Foundation!" The GitHub repo is archived (last push 2025-08-25) — [i-am-bee/acp](https://github.com/i-am-bee/acp)
- Relation: CONTRAST. The one mainstream protocol with a human-language field had language only (no region, currency or units), and it was absorbed into A2A, which has none.

**Agent Network Protocol (ANP), Agent Description Protocol spec**
- Agent Description fields: `protocolType`, `protocolVersion`, `type`, `url`, `name`, `did`, `owner`, `description`, `created`, `securityDefinitions`, `security`, `Infomations` [sic], `interfaces`, `proof`. There is no language, locale or currency field at the agent level.
- Product descriptions reuse schema.org and can carry `"priceCurrency": "CNY"` and `audience.geographicArea` — [ANP Agent Description spec](https://github.com/agent-network-protocol/AgentNetworkProtocol/blob/main/07-anp-agent-description-protocol-specification.md)
- Relation: CONTRAST. Currency appears only on product offers via schema.org (data-level), not as a declared convention of the agent or its tools.

**AGNTCY Open Agentic Schema Framework (OASF)**
- OASF records describe skills, domains, modules/extensions, `schema_version`, `authors` and `created_at` — [OASF docs](https://docs.agntcy.org/oasf/open-agentic-schema-framework/); [agntcy/oasf](https://github.com/agntcy/oasf)
- A GitHub code search of `agntcy/oasf` found:
  - "locale" only in `server/priv/data/words.txt`;
  - "currency" only in a `cryptocurrency` domain file;
  - "language" only in language-model modules and skills.
  
  This suggests there is no locale or currency descriptor (search not exhaustive) — [agntcy/oasf](https://github.com/agntcy/oasf)

**OpenAI Agents SDK, handoffs**
- `handoff()` parameters: `agent`, `tool_name_override`, `tool_description_override`, `on_handoff`, `input_type`, `input_filter`, `is_enabled`, `nest_handoff_history`.
- By default the receiver "takes over the conversation, and gets to see the entire previous conversation history".
- `input_type` is for "a small piece of model-generated metadata such as `reason`, `language`, `priority`, or `summary`" (a Pydantic schema validated as JSON) — [OpenAI Agents SDK handoffs](https://openai.github.io/openai-agents-python/handoffs/)
- Relation: CONTRAST + METHOD. Intra-organisation handoffs pass the full history, so the sender's locale context travels with them. Cross-organisation A2A delegation passes only the message, which is L4's setting. `input_type` is a ready-made mechanism for L4's "typed JSON with mandatory unit field" condition.

**Microsoft Magentic-One / AutoGen**
- The Orchestrator keeps a Task Ledger ("given or verified facts, facts to look up, facts to derive, and educated guesses") and a Progress Ledger, and directs sub-agents in natural language. No message-level convention metadata is described — [Magentic-One, arXiv:2411.04468](https://arxiv.org/abs/2411.04468); [AutoGen Magentic-One docs](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/magentic-one.html)

**Payment/commerce-layer protocols: where currency *is* typed**
- AP2 (Agent Payments Protocol, Google). `IntentMandate` (pydantic model) fields are `user_cart_confirmation_required`, `natural_language_description` ("generated by the shopping agent, and confirmed by the user", e.g., "High top, old school, red basketball shoes"), `merchants`, `skus`, `requires_refundability` and `intent_expiry`. **There is no amount or currency field**, so a budget lives only in the NL description — [AP2 mandate.py](https://github.com/google-agentic-commerce/AP2/blob/main/code/sdk/python/ap2/models/mandate.py)
- The newer AP2 SDK's generated open payment mandate has typed constraints:
  - `AmountRange`: `currency` "ISO4217 Alpha-3 currency code.", `max` "Maximum allowed amount in minor (cents) unit of currency."
  - `Budget`: `max: float` "Maximum amount for the budget.", `currency` ISO4217.
  - `Amount`: "Amount in minor units, according to the ISO-4217 spec" — [AP2 open_payment_mandate.py](https://github.com/google-agentic-commerce/AP2/blob/main/code/sdk/python/ap2/sdk/generated/open_payment_mandate.py); [AP2 amount.py](https://github.com/google-agentic-commerce/AP2/blob/main/code/sdk/python/ap2/sdk/generated/types/amount.py)
- OpenAI/Stripe Agentic Commerce Protocol checkout spec:
  - `currency` must "follow the ISO 4217 standard in lower case".
  - Amounts are "Integer representing total amount in minor units".
  - The `Accept-Language` request header carries "The preferred locale for content like messages and errors" (e.g., `en-US`) — [ACP Agentic Checkout Spec](https://developers.openai.com/commerce/specs/checkout)
- Typed minor units bring their own convention layer. Stripe: "enter 1099 to charge 10.99 USD… Enter 10 to charge 10 JPY (or any other zero-decimal currency)". ISK and UGX "transitioned to a zero-decimal currency, but backward compatibility requires you to represent it as a two-decimal value" — [Stripe currencies](https://docs.stripe.com/currencies)
- Relation: THREAT (to the typed-message condition only) + CONTRAST. Industry's answer at the payment layer is exactly L4's "typed JSON with mandatory unit field". L4's contribution is to show (i) the failure happens upstream, in NL delegation, before any mandate exists, and (ii) how much of the typed-field benefit transfers to agent-to-agent NL messages.

**Classic agent communication languages: explicit ontology fields**
- FIPA ACL Message Structure Specification, SC00061G (Standard, 2002/12/03):
  - It defines 13 parameters. `language`, `encoding` and `ontology` form the "Description of Content" category.
  - §2.4.3: `ontology` "Denotes the ontology(s) used to give a meaning to the symbols in the content expression." Notes: "In many situations, the ontology parameter will be commonly understood by the agent community and so this message parameter may be omitted."
  - §2.4.1: `language` "may be omitted if the agent receiving the message can be assumed to know the language of the content expression."
  - §2: "Some parameters of the message might be omitted when their value can be deduced by the context of the conversation. However, FIPA does not specify any mechanism to handle such conditions, therefore those implementations that omit some message parameters are not guaranteed to interoperate with each other."
  - A receiver that cannot process a parameter "can reply with the appropriate not-understood message" — [FIPA SC00061G](http://www.fipa.org/specs/fipa00061/SC00061G.html) (fipa.org returned 403 to the fetcher; text verified from a mirror PDF: [mirror](https://ppgia.pucpr.br/~fabricio/ftp/Aulas/Mestrado/AS/Aula3/SC00061G_FIPA_ACL.pdf))
- KQML message envelope (Finin et al., 1994): optional `:language` and `:ontology` arguments. Canonical example: `(ask-one :content (PRICE IBM ?price) :receiver stock-server :language LPROLOG :ontology NYSE-TICKS)` — [UMBC KQML paper §3.3](https://research.cs.umbc.edu/kqml/papers/kqml-acl-html/section3.3.html). The ontology name pins down what "price" means, including its units.
- Gruber & Olsen, "An Ontology for Engineering Mathematics" (KR'94): a shared ontology of physical quantities, dimensions and units of measure, designed "explicitly for knowledge sharing" between agents — [Gruber](https://tomgruber.org/writing/an-ontology-for-engineering-mathematics/)
- Relation: CONTRAST (historical). Symbolic ACLs carried an explicit, nameable ontology slot, and even FIPA recognised that omitting it breaks interoperability. LLM-era protocols dropped the slot because the "content language" became natural language.
- Positioning: "FIPA ACL let agents name the ontology that gives meaning to their symbols, and warned that omitted parameters 'are not guaranteed to interoperate'; LLM-era protocols replaced the ontology slot with natural language, and we measure what that costs for bare numbers."

**Motivating analogy (non-LLM)**
- Mars Climate Orbiter (1999). Root cause: "failure to use metric units in the coding of a ground software file, 'Small Forces'". The interface document required metric, and "the trajectory modelers assumed the data was provided in metric units" — [NASA LLIS lesson 641](https://llis.nasa.gov/lesson/641). This is a two-organisation, interface-spec convention mismatch, structurally the same as L4.

### Inferences
- The gap is structural. Protocols type the *transport* (MIME, JSON-RPC, signatures) and, in commerce, the *settlement amount*. The *intent* layer (NL request, `natural_language_description`, A2A text Part) is untyped. L4 targets exactly the layer every protocol leaves to NL.
- A2A's `INPUT_REQUIRED` state and FIPA's `not-understood` are the protocol analogues of L4's "receiver asks" channel. Citing both makes the hybrid condition look like a principled protocol design rather than prompt engineering.
- Typing does not eliminate conventions; it moves them. Minor-unit exponents (USD 2 vs JPY 0; ISK/UGX legacy two-decimal) are a second convention layer. In AP2's generated SDK, `AmountRange.max` is explicitly in minor units while `Budget.max` is a float with no unit statement. This is my reading of the field descriptions, not a reported bug.

### Gaps
- I checked the MCP spec revision 2025-06-18 tools page only; later revisions (e.g., 2025-11-25) were not checked for `_meta` locale additions.
- I did not read the content of MCP issue #86 (i18n) or A2A issue #1694 ("Add 'limitations' field to AgentCard").
- The OASF check was a GitHub code search, not a full schema read (schema.oasf.agntcy.org did not resolve).
- AutoGen core message types (beyond Magentic-One) were not inspected.
- KQML venue (Finin et al., CIKM 1994) is from secondary listings; UNVERIFIED as to the exact venue.

---

## Q2. Do surveys of agent protocols discuss semantic, unit or locale interoperability?

### Takeaway
The surveys acknowledge a "semantic layer" gap: protocols do not ensure agents *interpret* messages the same way. None of them, as far as their abstracts and the sections I read show, discusses units, currency or locale conventions. "Beyond Message Passing" is the best motivating citation. It finds clarification and context-alignment support weak, rates only A2A, Agora and PXP as supporting clarification, and pushes semantic responsibility into prompts.

### Cited Findings
- **Yuan et al., "Beyond Message Passing: A Semantic View of Agent Communication Protocols"**, arXiv:2604.02369 (v1 2026-03-30, v3 2026-04-13), 14 authors (Dun Yuan … Xue Liu).
  - It organises protocols into communication, syntactic and semantic layers and analyses 18 protocols.
  - Most "offer limited protocol-level mechanisms for clarification, context alignment, and verification. As a result, semantic responsibilities are often pushed into prompts, wrappers, or application-specific orchestration logic" — [arXiv:2604.02369](https://arxiv.org/abs/2604.02369)
  - The 18 protocols: MCP, agents.json, Agent Protocol, ACP-AGNTCY, ACP-IBM, ACP-AgentUnion, ACN, A2A, Agora, LOKA, ANP, Coral, AITP, LMOS, CrowdES, SPPs, PXP, WAP.
  - "many protocols help agents exchange messages correctly without ensuring they interpret them in the same way".
  - MCP is "weak at the semantic layer". In Table 1 only A2A, Agora and PXP get ✓ for clarification.
  - KQML/FIPA-ACL are mentioned only historically, for "brittleness and engineering overhead" — [HTML v3](https://arxiv.org/html/2604.02369v3). From an automated read of the HTML; I found no locale, units or currency discussion.
  - Relation: SUPPORTS (motivation).
  - Positioning: "Yuan et al. argue that protocols transport messages without guaranteeing shared interpretation; we give a concrete, measurable instance — numeric conventions — and test protocol-level fixes."
- **Ehtesham, Singh, Gupta, Kumar, "A survey of agent interoperability protocols: MCP, ACP, A2A, and ANP"**, arXiv:2505.02279 (v1 2025-05-04, v2 2025-05-23).
  - It characterises MCP (JSON-RPC, typed tool invocation), ACP (REST, multipart), A2A (Agent Cards, task outsourcing) and ANP (DIDs, JSON-LD), and proposes a phased adoption roadmap — [arXiv:2505.02279](https://arxiv.org/abs/2505.02279)
  - Relation: background.
- **Yang et al., "A Survey of AI Agent Protocols"**, arXiv:2504.16736 (v1 2025-04-23, v3 2025-06-21), 14 authors.
  - It proposes a two-way classification: context-oriented vs inter-agent, and general-purpose vs domain-specific.
  - It compares protocols on security, scalability and latency, and lists future needs: "adaptability, privacy preservation, and group-based interaction" — [arXiv:2504.16736](https://arxiv.org/abs/2504.16736)
  - Relation: background. The abstract does not mention semantics or locale.
- **Sander, Gidey, Lenz, Knoll, "A Technical Taxonomy of LLM Agent Communication Protocols"**, arXiv:2606.19135 (2026-06-17).
  - It covers nine protocols on five dimensions: counterparty, payload, interaction state, discovery mechanism, schema flexibility.
  - "two negotiate schemas at runtime".
  - The open gaps it names are "privacy and policy enforcement" — [arXiv:2606.19135](https://arxiv.org/abs/2606.19135)
  - Relation: CONTRAST. Its "schema flexibility" dimension is syntactic, not convention-level.

### Inferences
- L4 can claim to supply the first *empirical* measurement of a semantic-layer failure that these surveys diagnose only qualitatively.
- Runtime schema negotiation (Sander et al.; Agora in Yuan et al.) is a possible extra baseline: agents negotiate a message schema before exchange. It would be a stronger form of L4's typed condition.

### Gaps
- I did not read the full text of 2505.02279 or 2504.16736 for any passage on ontologies, units or locale; the claims above rest on abstracts.
- I found no 2025–2026 survey that explicitly discusses currency, measurement or locale interoperability for LLM agents.

---

## Q3. Empirical studies of information loss and distortion in relays, handoffs and multi-agent pipelines

### Takeaway
Relay studies converge on one picture. Explicit facts (including numbers and budgets) survive hops well with strong models. What gets lost is *metadata that governs interpretation*: privacy boundaries, hedges, and (L4's case) units. Relays faithfully propagate whatever errors they receive and do not correct them. Failure-taxonomy work (MAST) names "fail to ask for clarification" and "information withholding" as inter-agent failure modes but has no cross-organisation or locale cases. Failure-attribution work shows LLM judges cannot reliably assign blame, which motivates L4's counterfactual-injection design.

### Cited Findings
- **Sicheng Zeng, "Faithful, Not Corrective: Model Capability Governs Message-Format Effects in Multi-Hop Agent Relays"**, arXiv:2607.09678 (v1 2026-06-12, v2 2026-09-17), single author, no venue listed — [arXiv:2607.09678](https://arxiv.org/abs/2607.09678)
  - Design: 12 synthetic facts relayed over six hops in five formats (free NL, precision-instructed NL, JSON, triples, key-value), with two capability tiers.
    - The strong relay is DeepSeek-v4-flash; the weak relay is Qwen2.5-1.5B-Instruct, 4-bit.
    - Fact types include quantities such as deadlines, ports, canary percentages, versions and **budgets**, in three domains: software migration, incident response, logistics — [HTML v2](https://arxiv.org/html/2607.09678v2)
  - Results:
    - Strong relays keep "hop-6 QA recall ≥ 0.973" in every format.
    - For weak models the format effect "grows by a factor of 8.7 (CI 5.3–15.5)".
    - Cognitive load raises generation cost 24–53% with minimal fidelity change.
    - Injected errors show "surface persistence 83–100%" with no cross-fact cascade — [arXiv:2607.09678](https://arxiv.org/abs/2607.09678)
  - Injection protocol: at hop 3's output, one owner name is replaced across all surface occurrences with a plausible absent name, and the chain forks into clean and injected arms. 164/200 chains (82%) were successfully injected. Thesis: "Structure is a faithful, error-localizing channel, not an error-correcting code." — [HTML v2](https://arxiv.org/html/2607.09678v2)
  - Relation: THREAT (reviewer-flagged) + METHOD (fork-at-hop counterfactual injection).
  - Difference from L4: Zeng's errors are *corruptions of the message content*. In L4 the message can be perfectly faithful ("300,000" survives verbatim) and the loss happens because the *decoding frame* (currency) was never encoded and the receiver substitutes its own default. Zeng's facts are synthetic and convention-free, so this failure is invisible to his QA-recall metric: string recall of "300,000" would score 1.0.
  - Positioning: "Zeng shows relays are faithful but not corrective with respect to content errors; we show that faithful relays can still fail when the error is not in the content but in an unstated convention, and we localise whether the sender omitted it or the receiver misdecoded it."
- **Wang, Goyal, Chandrasekharan, Sundaram, "Facts Without Rules: Boundary Metadata Collapse in Multi-Agent LLM Handoffs"**, arXiv:2608.29028 (2026-08-29), no venue listed — [arXiv:2608.29028](https://arxiv.org/abs/2608.29028)
  - Abstract (verbatim numbers): "summary collapse" means summaries "preferentially preserve operational facts while weakening the boundary metadata that governs how those facts may be used".
    - Marker survival is scored by a human-validated judge (κ = 0.74).
    - Boundary-marker and operational-fact survival are "nearly uncorrelated (Pearson r near zero)".
    - Uncompressed handoffs give σ_b ≈ 0.80; a 25-word budget drops σ_b to ≈ 0.57 "while operational-fact survival stays near ceiling".
    - "vague languages leak in 73% of GPT and 50% of DeepSeek cases, while explicit constraints reduce leakage to under 15%".
    - "a gold-derived audience allowlist nearly eliminates leakage" (GPT-5-mini, DeepSeek-R1-32B, Qwen3-32B).
  - From an automated read of the HTML (treat per-model figures as needing a check against the PDF):
    - 36 scenarios across 7 domains × 4 handoff surfaces (explicit summary, forwarding, memory replay, report writing).
    - Conditions include free text, compressed, preserve-markers instruction, sectioned template and structured schema.
    - A corrupted typed allowlist restores leakage to about 44/48 — [HTML](https://arxiv.org/html/2608.29028)
    - The HTML-derived per-model baselines (σ_b ≈ 0.95 GPT / 0.88 DeepSeek) differ from the abstract's pooled ≈ 0.80. I have not reconciled these; cite the abstract.
  - Relation: THREAT (closest mechanistic parallel) + METHOD. The "value survives, governing metadata dropped" pattern and the "typed field fixes it" result both parallel L4's typed-unit condition.
  - Difference: their metadata is *present* upstream and lost under compression (a transmission loss). L4's convention is usually *never written*: it is implicit in the sender's locale and supplied by the receiver's default. The domain also differs: privacy norms versus decoding a value.
  - Positioning: "Wang et al. show governing metadata is shed in handoffs; for numbers the governing metadata is the unit, which senders often never write, so L4 isolates omission (sender) from misdecoding (receiver) rather than compression loss."
- **Perez, Kovač, Léger, Colas, Molinaro, Derex, Oudeyer, Moulin-Frier, "When LLMs Play the Telephone Game: Cultural Attractors as Conceptual Tools to Evaluate LLMs in Multi-turn Settings"**, ICLR 2025, arXiv:2407.04503 (v4 2026-01-29) — [arXiv:2407.04503](https://arxiv.org/abs/2407.04503)
  - Transmission chains drift toward "attractors" in toxicity, positivity, difficulty and length.
  - "more open-ended instructions lead to stronger attraction effects"; toxicity attracts more strongly than length.
  - Relation: CONTRAST. That work studies gradual, many-hop drift of text properties; L4 studies a discrete, single-hop flip of meaning with exact ground truth.
  - Positioning: "Telephone-game studies measure cumulative drift; L4 shows one hop suffices to flip a number's meaning by orders of magnitude."
- **Cemri, Pan, Yang, Agrawal, Chopra, Tiwari, Keutzer, Parameswaran, Klein, Ramchandran, Zaharia, Gonzalez, Stoica, "Why Do Multi-Agent LLM Systems Fail?"**, NeurIPS 2025 Datasets & Benchmarks Track, arXiv:2503.13657 (v3 2025-10-26) — [arXiv:2503.13657](https://arxiv.org/abs/2503.13657); [NeurIPS 2025 poster](https://neurips.cc/virtual/2025/poster/121528); [NeurIPS proceedings PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/b1041e52d3be19f0a9bc491657488e4a-Paper-Datasets_and_Benchmarks_Track.pdf)
  - MAST has 14 failure modes in 3 categories, derived from 150 traces with κ = 0.88.
  - The v3 abstract cites "1600+ annotated traces across 7 popular MAS frameworks"; the NeurIPS listing describes "MAD … 1000+ annotated traces" (version difference) — [arXiv](https://arxiv.org/abs/2503.13657); [NeurIPS search snippet](https://neurips.cc/virtual/2025/poster/121528)
  - v3 per-mode prevalence:
    - FC1: FM-1.1 disobey task spec 11.8%, FM-1.2 disobey role 1.5%, FM-1.3 step repetition 15.7%, FM-1.4 loss of conversation history 2.80%, FM-1.5 unaware of termination 12.4%.
    - **FC2 Inter-agent misalignment:** FM-2.1 conversation reset 2.20%, **FM-2.2 fail to ask for clarification 6.80%**, FM-2.3 task derailment 7.40%, **FM-2.4 information withholding 0.85%**, FM-2.5 ignored other agent's input 1.90%, FM-2.6 reasoning-action mismatch 13.2%.
    - FC3: FM-3.1 premature termination 6.20%, FM-3.2 no/incomplete verification 8.20%, FM-3.3 incorrect verification 9.10% — [HTML v3](https://arxiv.org/html/2503.13657v3)
    - Summing the v3 rows gives FC1 ≈ 44.2%, FC2 ≈ 32.4%, FC3 ≈ 23.5% (my computation from [HTML v3](https://arxiv.org/html/2503.13657v3)). A web-search summary attributed category shares of ~41.8% (specification) and ~36.9% (inter-agent misalignment) to an earlier version. UNVERIFIED: I could not tie these to a primary source; do not cite them.
  - Definitions: FM-2.2 "Inability to request additional information when faced with unclear or incomplete data, potentially resulting in incorrect actions"; FM-2.4 "Failure to share or communicate important data or insights that an agent possess and could impact decision-making of other agents if shared." — [HTML v3](https://arxiv.org/html/2503.13657v3)
  - Relation: SUPPORTS + METHOD (shared vocabulary for failure labels). L4's failure is FM-2.4 on the sender side (the convention is withheld because the sender assumes it is shared) and FM-2.2 on the receiver side (it does not ask).
  - Contrast: MAST traces are single-developer systems (ChatDev, MetaGPT, etc.). There are no cross-organisation agents and no locale.
  - Positioning: "MAST's inter-agent misalignment category names the symptoms; L4 provides a controlled, ground-truthed instance in which the two symptoms are separable by counterfactual injection."
- **Zhang, Yin, Zhang, Liu, Han, Zhang, Li, Wang, Wang, Chen, Wu, "Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems" (Who&When)**, ICML 2025 Spotlight, arXiv:2505.00212 — [arXiv:2505.00212](https://arxiv.org/abs/2505.00212); [ICML 2025 poster](https://icml.cc/virtual/2025/poster/45823)
  - The dataset covers 127 MAS.
  - The best method reaches "53.5% accuracy in identifying failure-responsible agents but only 14.2% in pinpointing failure steps"; o1 and R1 do not reach practical usability.
  - Relation: METHOD + SUPPORTS. LLM-judge blame assignment is unreliable, which justifies L4's counterfactual injection as ground-truth attribution of sender vs receiver.
- **Zhang et al., "AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?"**, arXiv:2509.03312 (2025-09-03) — [arXiv:2509.03312](https://arxiv.org/abs/2509.03312)
  - It annotates failed trajectories "via counterfactual replay and programmed fault injection".
  - Reasoning LLMs' attribution accuracy is "generally below 10%".
  - AgenTracer-8B beats Gemini-2.5-Pro and Claude-4-Sonnet by up to 18.18% on Who&When.
  - Relation: METHOD (counterfactual replay is L4's core design; cite as precedent).
- **West et al., "Abduct, Act, Predict: Scaffolding Causal Inference for Automated Failure Attribution in Multi-Agent Systems" (A2P)**, arXiv:2509.10401 — [arXiv:2509.10401](https://arxiv.org/abs/2509.10401)
  - Prior attribution methods have step-level accuracy "below 17%".
  - A2P frames attribution as counterfactual: "determine if correcting a single action would have actually averted the task failure".
  - Relation: METHOD (conceptual precedent for "minimal corrective intervention" = L4's message swap).
- **Jia, Deng, Chen, Wang, Zheng, "MAS-FIRE: Fault Injection and Reliability Evaluation for LLM-Based Multi-Agent Systems"**, arXiv:2602.19843 (2026-02-23) — [arXiv:2602.19843](https://arxiv.org/abs/2602.19843)
  - MAS "are prone to semantic failures (e.g., hallucinations, misinterpreted instructions, and reasoning drift) that propagate silently without raising runtime exceptions".
  - It defines 15 fault types, injected via "prompt modification, response rewriting, and message routing manipulation".
  - "stronger foundation models do not uniformly improve robustness".
  - Relation: METHOD ("response rewriting" = L4's message injection) + SUPPORTS ("silent" semantic failures).
- **Srinivasan, "Modality-Native Routing in Agent-to-Agent Networks: A Multimodal A2A Protocol Extension"**, arXiv:2604.12213 (2026-04-14) — [arXiv:2604.12213](https://arxiv.org/abs/2604.12213)
  - An A2A extension that reads Agent Card capability declarations gives 52% vs 32% task accuracy (McNemar p = 0.006).
  - A keyword-matching ablation erases the gap ("36% vs. 36%"): "protocol-level routing must be paired with capable agent-level reasoning".
  - Relation: METHOD + SUPPORTS. It is a precedent for evaluating an A2A Agent Card extension, and for the finding that a card field helps only if the receiver reasons with it.
- **Mehta, "Confident and Wrong: Silent Semantic Failures in Coding Agents"**, arXiv:2603.25764 — [arXiv:2603.25764](https://arxiv.org/abs/2603.25764)
  - Completion and correctness diverge (GPT-5 submits on 100% of runs and resolves 44%).
  - "silent semantic failure" covers 80% of Llama 4's and 68% of GPT-5's failing runs, and is invisible to completion and consistency monitoring.
  - Relation: SUPPORTS (terminology: L4's receiver confidently records `max_usd=300000`).

### Inferences
- Together, Zeng (values survive), Wang et al. (governing metadata does not) and L4 (the governing unit is often never sent) form a coherent progression. L4 should cite them as complementary layers: content fidelity, then metadata fidelity, then convention grounding.
- L4's counterfactual message injection is methodologically closest to Zeng's hop-3 fork and AgenTracer's counterfactual replay. L4 differs by swapping *semantically equivalent-but-explicit* sender messages rather than inserting errors. That isolates the receiver's decoding policy.

### Gaps
- I did not verify the exact Facts Without Rules per-model figures against the PDF; the HTML summary and abstract numbers differ.
- I found no relay study whose fact set includes values with locale-dependent units or currencies.
- The MAST category-level percentages for the NeurIPS camera-ready were not directly confirmed.

---

## Q4. LLM agents acting for principals with other organisations' agents: settings and reported failure modes

### Takeaway
A fast-growing 2025–2026 literature puts a user-owned agent against counterpart agents of other organisations: consumer vs merchant, buyer vs seller, platform-mediated booking. The reported failures are about strategy and loyalty: disclosure of reservation values, injection susceptibility, anchoring and first-proposal bias, overspending, misaligned speech acts and grounding breakdowns. None studies a mismatch of *conventions* (currency, units, number formats) between principal-side and counterpart-side agents, although several report "overspending" or budget violations without diagnosing a mechanism.

### Cited Findings
- **Dylan Zongmin Liu, "SovereignNegotiation-Bench: Evaluating User-Owned Personal Agents In Delegated Bargaining Under Privacy, Consent, Evidence, And Institutional Pressure"**, arXiv:2607.02814 (v1 2026-07-02, v2 2026-10-01), single author — [arXiv:2607.02814](https://arxiv.org/abs/2607.02814)
  - Setting: five agency-law duties (loyalty, obedience, confidentiality, candor, diligence) checked deterministically on logs, over 1,764 paired scenarios, 18 domains and 7 counterparty tactics.
  - Rule-based agents reach 92% faithful success; open-weight models range from 6% to 75%.
  - Models disclose reservation values in 2–80% of episodes and follow counterparty-injected instructions in 5–57%.
  - 48% of pooled agreements breach at least one duty. "single disclosed sentences" take surplus from 0.70 to 0.00.
  - Relation: CONTRAST + METHOD (deterministic duty checks on structured actions; L4's "obedience" = honour the budget in the principal's currency).
  - Positioning: "SovereignNegotiation-Bench tests whether a delegate is loyal; L4 tests whether a loyal delegate is *understood*."
- **Dylan Zongmin Liu, "SovereignPA-Bench: Evaluating User-Owned Personal Agents under Evolving Intent, Platform Mediation, and Consent Constraints"**, arXiv:2607.05363 (v2 2026-10-01) — [arXiv:2607.05363](https://arxiv.org/abs/2607.05363)
  - Scale: 1,920 booking and 288 cancellation scenarios, with one-factor variants including "ambiguous intent".
  - "every question the agent asks is labelled necessary or unnecessary, so faithfulness and user burden are measured separately".
  - Results across 17 open-weight models:
    - Success ranges from 2% to 82%.
    - "More faithful models ask fewer unnecessary questions, not more (Spearman rho = -0.67)".
    - "in 184 of 440 failed obstructed cancellations the agent told the user it had succeeded".
    - Checklists or a structural firewall raise success by at most 9 points.
  - Relation: METHOD. Necessary/unnecessary question labelling is exactly what L4's hybrid "ask when confidence is low" condition needs for measuring over-asking on shared-convention controls.
- **Yao, Zou, Hawkins, "Talk is Cheap, Communication is Hard: Dynamic Grounding Failures and Repair in Multi-Agent Negotiation"**, arXiv:2605.01750 (v2 2026-05-12) — [arXiv:2605.01750](https://arxiv.org/abs/2605.01750)
  - "agent dyads consistently fail" to reach Pareto-optimal allocations that individuals can find.
  - Four failure modes: "(1) loss of shared interaction history, (2) stubborn anchoring to early proposals, (3) defaulting to equal splits over reward-maximizing coordination, and (4) referential binding errors across turns".
  - "the bottleneck lies in dynamic grounding".
  - Relation: SUPPORTS + CONTRAST. This is the closest grounding framing. L4's failure is a grounding failure that *never triggers repair*, because neither party perceives a breakdown: the number is well-formed under both conventions.
  - Positioning: "Yao et al. study grounding breakdowns agents could notice and repair; L4 studies breakdowns that are invisible from inside the receiver's convention, so repair must be designed into the channel."
- **Bansal et al. (24 authors, Microsoft), "Magentic Marketplace: An Open-Source Environment for Studying Agentic Markets"**, arXiv:2510.25779 (2025-10-27) — [arXiv:2510.25779](https://arxiv.org/abs/2510.25779); [code](https://github.com/microsoft/multi-agent-marketplace)
  - Setting: a two-sided market with Assistant agents for consumers and Service agents for businesses.
  - "frontier models can approach optimal welfare — but only under ideal search conditions"; performance "deteriorates significantly as scale increases".
  - "severe first-proposal bias, creating 10-30x advantages for response speed over quality"; manipulation vulnerability is also studied.
  - Relation: METHOD (cross-organisation consumer/business topology; an open-source testbed L4 could plug its convention scenarios into).
- **Zhu, Sun, Nian, South, Pentland, Pei, "The Automated but Risky Game: Modeling and Benchmarking Agent-to-Agent Negotiations and Transactions in Consumer Markets"**, arXiv:2506.00073 (v4 2025-09-20) — [arXiv:2506.00073](https://arxiv.org/abs/2506.00073)
  - Both consumers and merchants delegate to agents.
  - "AI-mediated deal-making is an inherently imbalanced game"; "behavioral anomalies in LLMs can result in financial losses for both consumers and merchants, such as overspending or accepting unreasonable deals".
  - Relation: SUPPORTS. Budget violations are a known agent-commerce risk, and L4 supplies one concrete, cross-locale mechanism for "overspending".
- **Liu, Gu, Song, "AgenticPay: A Multi-Agent LLM Negotiation System for Buyer-Seller Transactions"**, arXiv:2602.06008 (2026-02-05) — [arXiv:2602.06008](https://arxiv.org/abs/2602.06008)
  - It has over 110 tasks from bilateral bargaining to many-to-many markets, with "structured action extraction and metrics for feasibility, efficiency, and welfare".
  - Relation: METHOD (structured action extraction from NL negotiation).
- **Bianchi, Chia, Yuksekgonul, Tagliabue, Jurafsky, Zou, "How Well Can LLMs Negotiate? NegotiationArena Platform and Analysis"**, arXiv:2402.05863 (2024-02-08) — [arXiv:2402.05863](https://arxiv.org/abs/2402.05863)
  - Section "Behaviors Change When Denominations Change": scaling all values by a constant X shows that "as we scale up all resources and beliefs, the portion of the money ($100X) the object is sold for decreases" — [HTML](https://arxiv.org/html/2402.05863)
  - The venue (ICML 2024) is UNVERIFIED; the fetch showed only an "ICML" keyword.
  - Relation: CONTRAST (minor THREAT). LLM agents are sensitive to number magnitude, but within a shared currency; no cross-convention decoding.
  - Positioning: "NegotiationArena shows outcomes shift with numeric scale; L4 shows the scale itself can be silently reinterpreted across agents."
- **Liang, Xu, "When LLM Agents Negotiate: Private Information and Dynamic Bargaining in Supply Chains"**, arXiv:2608.07538 (2026-07-29) — [arXiv:2608.07538](https://arxiv.org/abs/2608.07538)
  - Scale: 9,840 LLM-to-LLM negotiations across nine models from OpenAI, Google and Alibaba.
  - Agents agree in 98.9% of negotiations and capture 95.4% of first-best surplus. They average 2.98 rounds against the benchmark's 1.25, and the delay erodes 21–34% of surplus.
  - Baseline-tier models accept individually irrational contracts in 19.2% of cases, versus 0.0–0.6% for mid-tier and flagship models.
  - Self-play buyer shares are 40% (OpenAI), 50% (Google) and 70% (Qwen); "Reversing which provider sells moves the division by 7-18" points.
  - Relation: METHOD (cross-provider sender × receiver matrix with role reversal; L4's "different organisation" can be operationalised as a different provider).
- **Li, Petersson, Acquisti, Bakker, "Emergent Misaligned Communication in Long-Horizon Multi-Agent LLM Commerce"**, arXiv:2608.14825 (v3 2026-08-21) — [arXiv:2608.14825](https://arxiv.org/abs/2608.14825)
  - Data: 2,583 inter-agent emails from 20 one-year runs of Vending-Bench Arena, with 13 frontier LLMs.
  - 12.6% of emails are misaligned (false claims, manipulation, collusion, threats), in all 20 runs and 74.7% of agent-runs.
  - Receiving a misaligned email raises the odds of a misaligned reply 1.65×; low inventory raises them 1.58×.
  - Relation: CONTRAST. Those are *strategic* falsehoods between separate principals. L4's are *honest* miscommunications, so they cannot be addressed by deception detection.
- **Li et al., "ComboShoppingBench: Evaluating LLM Agents for Budget-Constrained Basket Shopping with Coupons"**, arXiv:2608.09282 (2026-08-10) — [arXiv:2608.09282](https://arxiv.org/abs/2608.09282)
  - Budgets are phrased as a cap, a fuzzy target ("around … N CNY") or a band. This detail comes from a search snippet of the HTML, not my own read.
  - Relation: CONTRAST (single-agent and single-currency budget phrasing; L4 adds the cross-agent and cross-currency dimension).

### Inferences
- Every cross-organisation benchmark above assumes both agents share one currency and number convention, usually USD or CNY implicitly. L4 can point out that this assumption is baked into the benchmarks themselves, so convention-mismatch failures would be invisible in them.
- "Overspending" (Zhu et al.) and "irrational contracts" (Liang & Xu) are measured outcomes without a mechanism. L4 can position itself as a *mechanistic* study of one route to such outcomes.

### Gaps
- I did not locate a "consumer-agent vs business-agent" study that varies the user's country or locale. Searched via arXiv API: `abs:locale AND abs:agents AND abs:LLM`, `abs:currency AND abs:"multi-agent" AND abs:LLM`, `abs:"cross-cultural" AND abs:"agent-to-agent"` (no hits for the last).
- The "Talk is Cheap" paper's numerical results were not in the abstract and were not extracted.

---

## Q5. Hidden disagreement and convention formation (Illusion of Alignment and similar)

### Takeaway
Hidden-disagreement work shows that apparent agreement routinely masks divergent assumptions, and that targeted diagnostic probes can surface them. Convention-formation work shows that alignment depends on shared interpretive biases. Both support L4's framing that convention loss is invisible to the participants.

### Cited Findings
- **Liu, Luo, Wang, Ju, Liu, Lei, Lai, Li, Liu, "Illusion of Alignment: Detecting Hidden Disagreement in Collaborative Dialogue"**, arXiv:2608.08210 (2026-08-08) — [arXiv:2608.08210](https://arxiv.org/abs/2608.08210)
  - Collaborative dialogue often ends in "apparent agreement while participants still differ on goals, assumptions, or execution plans" (a real-user study of 18 meetings).
  - Method: "diagnostic multiple-choice questions whose divergent answers across participants provide direct behavioral evidence of hidden disagreement".
  - IoA-Prober-8B reaches 51.8% F1 on IoA-Suite and finds 2.89 unvoiced hidden disagreements per meeting. Pairing it with agents improves BigCodeBench-Hard and HiddenBench.
  - Relation: SUPPORTS + METHOD (probe both agents with "Which currency is the budget in?" after the exchange to detect hidden misalignment before the tool call).
  - Positioning: "Illusion of Alignment detects hidden divergence in human meetings; L4 exhibits a sharp, ground-truthed case between agents where the divergent assumption is a numeric convention."
- **Jones, Lombardi, Mahowald, Bergen, "LLMs and people both learn to form conventions — just not with each other"**, arXiv:2602.08208 (2026-02-09) — [arXiv:2602.08208](https://arxiv.org/abs/2602.08208)
  - Same-type pairs (human-human, AI-AI) converge, "increasing the accuracy and consistency of their turns while decreasing their length". Mixed human-AI pairs lag even when length is matched.
  - "effective conversational alignment requires shared interpretative biases".
  - Relation: SUPPORTS. Cross-locale agent pairs are a case of non-shared interpretive priors, even when both agents are the same model with different system contexts.
- **Buscemi et al., "When Numbers Start Talking: Implicit Numerical Coordination Among LLM-Based Agents"**, arXiv:2601.03846 (v2 2026-04-19) — [arXiv:2601.03846](https://arxiv.org/abs/2601.03846)
  - A game-theoretic study of covert signalling via numbers in actions.
  - Relation: tangential; it is about numbers as strategic signals, not decoding conventions.

### Inferences
- L4's hybrid channel (sender attaches confidence, receiver asks when it is low) can be framed as an *online* hidden-disagreement detector. IoA-style post-hoc probes give an upper bound on how much misalignment is detectable.

### Gaps
- HiddenBench (cited inside Illusion of Alignment) was not looked up independently.

---

## Novelty threats (ranked)

### Takeaway
After targeted searches (arXiv API queries combining locale/currency/unit/convention with agent/multi-agent/agent-to-agent; GitHub issue searches on A2A, MCP and ANP), I found **no paper that studies unit, currency or locale mismatch between LLM agents**. The closest threats are (1) relay-fidelity and handoff-metadata papers that share L4's "faithful transmission, lost meaning" structure, (2) protocol-community proposals that already name the locale/currency gap, and (3) payment protocols that already implement the typed-currency fix.

### Cited Findings
1. **Faithful, Not Corrective (arXiv:2607.09678). HIGH; reviewer-flagged.**
   - Overlap: the relay-fidelity framing, format comparison (NL vs JSON vs key-value) and counterfactual error injection — [arXiv:2607.09678](https://arxiv.org/abs/2607.09678)
   - Defence: Zeng's facts are convention-free synthetic values, and his injected errors are content corruptions. L4's errors arise *without* any content corruption, from an implicit decoding frame. Under Zeng's string-recall metric, L4's failing messages would score as perfect.
   - Concretely, L4 should report a "string fidelity vs semantic fidelity" table: the number survives verbatim (≈100%), but the decoded value is wrong in X% of cases.
2. **Facts Without Rules (arXiv:2608.29028). HIGH.**
   - Overlap: "operational value survives, governing metadata collapses"; typed fields fix it — [arXiv:2608.29028](https://arxiv.org/abs/2608.29028)
   - Defence: theirs is a privacy and compression loss of markers *present upstream*. L4's convention is typically *absent upstream*, and the counterfactual design attributes the loss to sender omission vs receiver default.
   - L4 should also test their corrupted-typed-field stress test, to show whether receivers over-trust a structured unit field.
3. **LLMs Infer Cultural Context but Fail to Apply It When Responding (Miao, Zhu, Shwartz; arXiv:2606.17688). MEDIUM.**
   - A single-agent precedent for "recognised but not applied" — [arXiv:2606.17688](https://arxiv.org/abs/2606.17688)
   - The arXiv title does not contain "CAPRI". The existing L4 prior-work notes call it "CAPRI"; check the paper body for the benchmark name before citing it that way (UNVERIFIED).
4. **Protocol proposals naming the gap. MEDIUM, for the claim that "nobody has noticed".**
   - MCP SEP-1809 explicitly motivates locale with "dates, numbers, currency" and "decimal separator" — [SEP-1809](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1809)
   - A2A #2121 adds currency-tagged budgets for compute cost — [A2A #2121](https://github.com/a2aproject/A2A/issues/2121)
   - Defence: these are unmerged engineering proposals with no measurement. SEP-2792, the live i18n track, excludes currency and measurement — [PR #2792](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2792)
   - Cite them as evidence the problem is real and unsolved.
5. **Payment protocols with ISO 4217 typed amounts (AP2, OpenAI/Stripe ACP). MEDIUM, for the typed-message condition.**
   - Typed currency plus minor units is already industry practice at checkout — [AP2 open_payment_mandate.py](https://github.com/google-agentic-commerce/AP2/blob/main/code/sdk/python/ap2/sdk/generated/open_payment_mandate.py); [ACP checkout spec](https://developers.openai.com/commerce/specs/checkout)
   - Defence: AP2's `IntentMandate` carries intent only as `natural_language_description`, with no amount field — [AP2 mandate.py](https://github.com/google-agentic-commerce/AP2/blob/main/code/sdk/python/ap2/models/mandate.py). The L4 failure occurs before a typed mandate exists. L4 tests whether the typed fix transfers to agent-to-agent NL delegation.
6. **NegotiationArena denomination scaling (arXiv:2402.05863). LOW.**
   - Shows magnitude sensitivity within one currency, not reinterpretation — [HTML](https://arxiv.org/html/2402.05863)
7. **MAST FM-2.2 / FM-2.4 (arXiv:2503.13657). LOW.**
   - Generic categories without a convention instance — [HTML v3](https://arxiv.org/html/2503.13657v3)

### Inferences
- The defensible novelty claim, narrowed: *"first controlled measurement of convention loss across organisational agent boundaries, with counterfactual attribution to sender omission vs receiver misdecoding, and a comparison of protocol-level channel designs (card field, typed unit field, resolver, confidence-gated asking) that existing protocols lack or scope out."*
- Frame L4 as the third layer in a fidelity stack, so that 2607.09678 and 2608.29028 become support rather than threats:
  - content fidelity (Zeng 2026);
  - governing-metadata fidelity (Wang et al. 2026);
  - convention grounding (L4).

### Gaps
- The arXiv API's relevance search is keyword-based. Papers using different vocabulary (e.g., "cultural pragmatics between agents", "localization drift") may have been missed. I did not search the ACL Anthology or OpenReview directly for 2026 venue papers.
- Google Scholar was not queried.

---

## Experiment ideas borrowed from this literature

### Takeaway
The literature supplies concrete, citable designs for L4: fork-at-hop counterfactual injection, string-vs-semantic fidelity metrics, marker-survival under compression budgets, corrupted-typed-field stress tests, necessary/unnecessary question labelling, cross-provider role-reversal matrices, receiver ablations for protocol fields, post-hoc divergence probes, and spec-compliant A2A/MCP implementations of the locale field.

### Cited Findings
- **Fork-at-hop counterfactual injection with clean and injected arms** (Zeng): fork each episode at the sender message and swap in an explicit-convention variant or a stripped variant. Report how many chains were injected successfully, as Zeng does (164/200) — [HTML v2](https://arxiv.org/html/2607.09678v2). Cite AgenTracer's "counterfactual replay and programmed fault injection" as precedent — [arXiv:2509.03312](https://arxiv.org/abs/2509.03312)
- **String recall vs QA recall** (Zeng): add a "verbatim survival of the number" metric alongside "decoded value correct" to show faithful-but-wrong decoding — [HTML v2](https://arxiv.org/html/2607.09678v2)
- **Convention-marker survival σ_c under compression budgets** (Wang et al.'s σ_b): measure whether "₩"/"KRW"/"won" survives when the sender summarises under 25- and 40-word caps, and whether survival is uncorrelated with value survival (their Pearson r ≈ 0) — [arXiv:2608.29028](https://arxiv.org/abs/2608.29028)
- **Corrupted typed-field stress test** (Wang et al.: a corrupted allowlist restores leakage to about baseline): give the typed JSON a wrong `unit` and see whether receivers follow the field over contradicting NL context. This tests over-trust in structure — [HTML](https://arxiv.org/html/2608.29028)
- **Rule-based receiver ablation** (Srinivasan's keyword-matching ablation, 36% vs 36%): replace the LLM receiver with a deterministic reader of the Agent Card locale field. This separates the value of the protocol field from the value of receiver reasoning — [arXiv:2604.12213](https://arxiv.org/abs/2604.12213)
- **Necessary vs unnecessary question labelling** (SovereignPA-Bench): for the hybrid condition, label every receiver question. Report ask rate on shared-convention controls (over-asking) and the success–burden correlation (their ρ = −0.67) — [arXiv:2607.05363](https://arxiv.org/abs/2607.05363)
- **Deterministic duty checks on structured actions** (SovereignNegotiation-Bench): score "obedience" as tool-call argument equals the principal's budget converted correctly, computed from logs with no LLM judge — [arXiv:2607.02814](https://arxiv.org/abs/2607.02814)
- **Cross-provider sender × receiver matrix with role reversal** (Liang & Xu, a 7–18 point shift on role reversal): operationalise "another organisation" as another model provider and report asymmetries — [arXiv:2608.07538](https://arxiv.org/abs/2608.07538)
- **Post-exchange divergence probe** (Illusion of Alignment): ask sender and receiver the same multiple-choice question ("300,000 is in: KRW / USD / …"). Divergence rate is a cheap detector, and it can be compared with the hybrid channel's online asking — [arXiv:2608.08210](https://arxiv.org/abs/2608.08210)
- **MAST labels for comparability**: tag L4 failures as FM-2.4 (sender withholds convention) or FM-2.2 (receiver fails to ask), using the released MAST annotator — [arXiv:2503.13657](https://arxiv.org/abs/2503.13657)
- **LLM-judge attribution baseline** (Who&When: 53.5% agent-level accuracy): give Who&When-style judges L4 traces and compare their sender/receiver blame with L4's counterfactual ground truth. This shows why injection is needed — [arXiv:2505.00212](https://arxiv.org/abs/2505.00212)
- **Spec-compliant protocol-field implementations**:
  - Implement the card condition as an A2A `AgentExtension` (`uri`, `required: true`, `params: {locale, currency, measurement_system}`) and the per-message variant in `Message.metadata`.
  - Implement the ask condition via `TASK_STATE_INPUT_REQUIRED` — [a2a.proto](https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto)
  - Mirror it for MCP with SEP-1809's `clientContext.locale`, or `_meta` per SEP-2792 — [SEP-1809](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1809); [PR #2792](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2792)
  - Use OpenAI Agents SDK `input_type` for the typed-message condition — [handoffs](https://openai.github.io/openai-agents-python/handoffs/)
- **Typed-amount minor-unit probe** (AP2/ACP/Stripe): in the typed condition, use the industry schema (ISO 4217 code plus integer minor units). Test zero-decimal currencies (Stripe: "Enter 10 to charge 10 JPY") and legacy cases (ISK/UGX) to show that typing moves the convention problem to the minor-unit exponent rather than removing it — [Stripe currencies](https://docs.stripe.com/currencies); [AP2 amount.py](https://github.com/google-agentic-commerce/AP2/blob/main/code/sdk/python/ap2/sdk/generated/types/amount.py)
- **Plug into an existing cross-organisation market**: run L4 scenarios inside Magentic Marketplace (Assistant vs Service agents) to show the failure in a third-party testbed — [microsoft/multi-agent-marketplace](https://github.com/microsoft/multi-agent-marketplace)

### Inferences
- The two cheapest, highest-value additions for the ARR resubmission:
  - the string-vs-semantic fidelity table, which directly neutralises the "close to Faithful, Not Corrective" critique;
  - the rule-based-receiver ablation on the agent-card field, which explains *why* the card field does or does not help.
- The minor-unit probe would let L4 argue that the typed-field fix is necessary but not sufficient, a more interesting result than "JSON helps".

### Gaps
- KRW's zero-decimal status is not quoted explicitly on the Stripe page I fetched. Its minimum-charge table lists "50 KRW" with no decimals; verify against the ISO 4217 table before using KRW in the minor-unit probe.
- Magentic Marketplace's support for custom per-agent locale context was not checked in its code.
