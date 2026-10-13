# NL vs structured/typed/latent/hybrid channels between LLM agents, evaluation of agent communication, and theme-track positioning for L4 ("Bare Numbers Between Agents")

Compiled 2026-10-07. Verification method: every arXiv ID below was resolved through the arXiv export API (title, authors, date, comment/journal-ref and abstract read from the record), so the IDs, titles and first authors are confirmed. Venue strings come from the arXiv comment or journal-ref field, or from an ACL Anthology/conference page. Where a venue or detail could not be confirmed it is marked **UNVERIFIED**. Non-arXiv sources (ICAO, NASA, FSF, conference pages) were opened directly unless marked "(search snippet only)".

Shorthand for L4's five channels: **C1** plain NL relay; **C2** NL plus an instruction to state units; **C3** typed JSON with a mandatory unit field; **C4** convention metadata in an agent card; **C5** hybrid NL plus a confidence channel. L4's headline result: explicitness and typing raise accuracy but trade off against safety. Stating units turns receiver questions into confident actions; typed channels cut silent errors at an accuracy cost.

---

## (a) Empirical comparisons of NL vs structured vs latent communication between LLM agents (2023–2026): which report reliability/accuracy trade-offs?

### Takeaway
There are two literatures, and they disagree.
- **Latent channels** (embeddings, activations, KV-cache, hidden states) consistently report modest accuracy gains (+0.5 to +27 points) and large efficiency gains over text on shared-convention reasoning benchmarks. A 2026 negative result finds that latent channels match text but never exceed it.
- **Structured-vs-NL work** is split. Format restriction can hurt reasoning, although that claim is contested. In relays, structure gives faithfulness, not correction. A 2026 audit argues that communication quality is not an intrinsic property of a channel, because richer messages amplify both helpful and harmful influence.

No paper found tests any of these channel forms under a hidden convention mismatch (units, currency, locale), so L4's niche survives. However, the closest relay-format paper (2607.09678) uses almost the same C1/C2/C3 conditions.

### Cited Findings

**Latent / sub-symbolic channels**
- **CIPHER.** Pham, Liu, Yang, Chen, Liu, Yuan et al., "Let Models Speak Ciphers: Multiagent Debate through Embeddings," ICLR 2024, arXiv 2310.06272.
  - Finding: removing token sampling and passing the expectation of output embeddings beats NL debate by 0.5–5.0% across five reasoning tasks.
  - Relation to L4: contrast. The channel is lossless about belief distributions, but every agent shares one convention space.
  - Positioning: "CIPHER shows richer channels help when agents share a code; L4 asks what happens when the code itself (units) differs." — [arXiv](https://arxiv.org/abs/2310.06272)
- **Activation communication.** Ramesh & Li, "Communicating Activations Between Language Model Agents," ICML 2025, arXiv 2501.14082.
  - Finding: merging intermediate activations gives up to 27.0% improvement over NL communication with under 1/4 of the compute, on coordination games and reasoning benchmarks.
  - Relation: contrast, and a possible borrowable channel. — [arXiv](https://arxiv.org/abs/2501.14082)
- **Cache-to-Cache (C2C).** Fu, Min, Zhang, Yan, Dai, Ouyang et al., "Cache-to-Cache: Direct Semantic Communication Between Large Language Models," ICLR 2026, arXiv 2510.03215.
  - Finding: projects and fuses one model's KV-cache into another's. Accuracy is 6.4–14.2% higher than individual models and about 3.1–5.4% higher than text communication, with an average 2.5x latency speedup.
  - Relation: borrowable method for a latent arm of L4 (open-weight models only). — [arXiv](https://arxiv.org/abs/2510.03215)
- **KVComm.** Shi, Chiesa, Maguire, Kostic, "KVComm: Enabling Efficient LLM Communication through Selective KV Sharing," ICLR 2026, arXiv 2510.03346.
  - Finding: sharing as few as 30% of layers' KV pairs gets close to the upper bound of merging inputs into one model.
  - Relation: borrowable. — [arXiv](https://arxiv.org/abs/2510.03346)
- **LatentMAS.** Zou, Qiu, Li, Yang, Tieu, Lu et al., "Latent Collaboration in Multi-Agent Systems," ICML 2026 Spotlight, arXiv 2511.20639.
  - Finding: training-free latent working memory, evaluated on 9 benchmarks. Up to 14.6% higher accuracy, 70.8–83.7% fewer output tokens, and 4–4.3x faster inference than text-based MAS.
  - Relation: contrast. Efficiency-and-accuracy framing with no reliability or safety analysis. — [arXiv](https://arxiv.org/abs/2511.20639)
- **Thought Communication.** Zheng, Zhao, Li, Xie, Gao, Zhang et al., "Thought Communication in Multiagent Collaboration," NeurIPS 2025 Spotlight, arXiv 2510.20733.
  - Finding: formalizes "mind-to-mind" communication as a latent-variable model and proves that shared and private thoughts are identifiable. It motivates the work by calling NL "lossy, ambiguous, and indirect."
  - Relation: supports L4's premise that NL ambiguity is a real cost; contrast on remedy. — [arXiv](https://arxiv.org/abs/2510.20733)
- **Interlat.** Du, Wang, Bai, Cao, Zhu, Cheng et al., "Enabling Agents to Communicate Entirely in Latent Space," ACL 2026, arXiv 2511.09149; [ACL Anthology 2026.acl-long.1248](https://aclanthology.org/2026.acl-long.1248/).
  - Finding: last-layer hidden states as messages, plus learned compression. Beats fine-tuned CoT and single-agent baselines, even across heterogeneous models, with up to 24x faster inference.
  - Relation: shows that ACL main accepts "forms of communication" mechanism papers. — [arXiv](https://arxiv.org/abs/2511.09149)
- **OBF compression.** Li, An, Du, "When Less Latent Leads to Better Relay: Information-Preserving Compression for Latent Multi-Agent LLM Collaboration," arXiv 2604.13349 (venue UNVERIFIED).
  - Finding: keeps only 9.9–20.2% of prompt KV, cuts bandwidth 4.7x, and stays close to full KV relay across nine benchmarks. — [arXiv](https://arxiv.org/abs/2604.13349)
- **Negative result on latent channels.** Wenzel, "Latent Communication Between Language Model Agents: Channels, Alignment, and the Limits of Text," arXiv 2607.14103 (venue UNVERIFIED).
  - Finding: text serialization destroys 88% of SAE features, and a sparse latent channel keeps 99.4% probe accuracy vs 80.4% for text. Cross-model Procrustes alignment reaches 92% top-1 retrieval (Llama↔Mistral). Yet at the task level the latent channel "matches the text channel on cross-lingual concept tasks but never exceeds it." The lost features "mostly or completely encode surface form, not task-relevant semantics."
  - Relation: contrast, and useful to L4. It suggests that what matters for a task survives text, while what L4 shows is lost is *unstated* context, which no channel carries unless it is encoded. — [arXiv](https://arxiv.org/abs/2607.14103)
- **Latent-communication survey.** Liu, "Beyond tokens: a unified framework for latent communication in LLM-based multi-agent systems," arXiv 2606.05711.
  - Finding: categorizes 18 methods from 2024–2026 along WHAT, WHICH alignment, and HOW fused. Open challenges include cross-architecture alignment and "security of latent channels."
  - The survey's HTML version reportedly cautions that latent-over-NL gains are "vulnerable to publication bias and baseline mismatch" (search snippet only; not in abstract). — [arXiv](https://arxiv.org/abs/2606.05711)
- **Position paper.** Zhou, Feng, Julaiti, Yang, "Why do AI agents communicate in human language?," arXiv 2506.02739 (venue UNVERIFIED).
  - Finding: argues that NL is "structurally misaligned" with model vector spaces, "resulting in information loss and behavioral drift." Calls for models built to support structured communication natively.
  - Relation: a framing foil. — [arXiv](https://arxiv.org/abs/2506.02739)

**Structured / typed vs free NL**
- **Relay formats (closest threat).** Zeng, "Faithful, Not Corrective: Model Capability Governs Message-Format Effects in Multi-Hop Agent Relays," arXiv 2607.09678 (venue UNVERIFIED). See also the threats list in section (e).
  - Setup: twelve programmatic facts relayed over six hops in five formats: **free NL, precision-instructed NL, JSON, triples, key-value**. This is nearly L4's C1/C2/C3.
  - Findings:
    - A strong relay is nearly lossless in every format (hop-6 QA recall ≥0.973), and residual loss sits at the first encoding.
    - With a weak 1.5B relay, across-format dispersion grows 8.7x and the format ranking flips in transit.
    - Injected errors propagate faithfully in every format (surface persistence 83–100%).
    - Conclusion: "Structure buys a faithful, error-localizing channel, not an error-correcting code."
  - Relation: **novelty threat on channel design**. It also supports L4: if strong models copy faithfully, L4's errors must come from *decoding under a convention mismatch*, not transmission. — [arXiv](https://arxiv.org/abs/2607.09678)
- **Format restriction.** Tam, Wu, Tsai, Lin, Lee, Chen, "Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of LLMs," EMNLP 2024 Industry ([Anthology PDF](https://aclanthology.org/2024.emnlp-industry.91.pdf)), arXiv 2408.02442.
  - Finding: "a significant decline in LLMs reasoning abilities under format restrictions," and stricter formats degrade reasoning more.
  - Relation: supports L4's finding that typed JSON (C3) costs accuracy. — [arXiv](https://arxiv.org/abs/2408.02442)
  - **Contested.** The dottxt blog post "Say What You Mean: A Response to 'Let Me Speak Freely'" argues that the paper used different prompts for structured and unstructured runs. With matched prompts it reports structured ≥ unstructured (GSM8K 0.78 vs 0.77; Last Letter 0.77 vs 0.73; Shuffle Object 0.44 vs 0.41). This is a blog, not peer-reviewed (search snippet only). — [dottxt blog](https://blog.dottxt.ai/say-what-you-mean.html)
  - Implication for L4: C3's accuracy cost may partly be a prompt or parser mismatch. Control for it with a same-prompt ablation.
- **Prompt formatting.** He, Rungta, Koleczek, Sekhon, Wang, Hasan, "Does Prompt Formatting Have Any Impact on LLM Performance?," arXiv 2411.10541 (submitted to NAACL 2025; acceptance UNVERIFIED).
  - Finding: GPT-3.5-turbo varies by up to 40% on code translation across plain text, Markdown, JSON and YAML templates. GPT-4 is more robust.
  - Relation: borrowable control. The *input* format of the message to the receiver matters independently of content. — [arXiv](https://arxiv.org/abs/2411.10541)
- **JSONSchemaBench.** Geng, Cooper, Moskal, Jenkins, Berman, Ranchin et al., arXiv 2501.10868.
  - Finding: a benchmark of 10K real-world JSON schemas for constrained decoding, evaluated on efficiency, coverage and quality. Schema compliance is not guaranteed in practice.
  - Relation: background for C3's validity rate. — [arXiv](https://arxiv.org/abs/2501.10868)
- **HiddenBench.** Li, Naito, Shirado, "Systematic Failures in Collective Reasoning under Distributed Information in Multi-Agent LLMs," ICML 2026, arXiv 2505.11556.
  - Finding: on a 65-task Hidden Profile benchmark, multi-agent LLMs reach 30.1% accuracy vs 80.7% for single agents given complete information. "a lightweight structured communication protocol substantially improves collective reasoning across model families."
  - Relation: supports the claim that structure helps. It is also a theme-adjacent template (theory-grounded paradigm plus structured-protocol fix). — [arXiv](https://arxiv.org/abs/2505.11556)
- **TalkHier.** Wang, Moriyama, Wang, Gangopadhyay, Takamatsu, "Talk Structurally, Act Hierarchically," arXiv 2502.11098 (venue UNVERIFIED).
  - Finding: a structured communication protocol plus hierarchical refinement beats AgentVerse, majority voting, and o1 on QA and ad-text generation.
  - Relation: structure-helps precedent, measured on accuracy only. — [arXiv](https://arxiv.org/abs/2502.11098)
- **MetaGPT.** Hong, Zhuge, Chen, Zheng, Cheng, Zhang et al., arXiv 2308.00352.
  - Finding: encodes SOPs as structured intermediate documents in place of free chat, to curb "cascading hallucinations caused by naively chaining LLMs."
  - Relation: an early structured-messages rationale. — [arXiv](https://arxiv.org/abs/2308.00352)
- **ChatDev.** Qian, Liu, Liu, Chen, Dang, Li et al., ACL 2024, arXiv 2307.07924.
  - Finding: NL "is advantageous for system design, and communicating in programming language proves helpful in debugging." This is a channel-by-phase result.
  - Relation: supports a "choose the form by message type" framing. — [arXiv](https://arxiv.org/abs/2307.07924)
- **AgentVerse.** Chen, Su, Zuo, Yuan, Chan et al., arXiv 2308.10848.
  - Finding: a dynamic group-composition framework that studies emergent social behaviors. It has no channel-form ablation.
  - Relation: background only. — [arXiv](https://arxiv.org/abs/2308.10848)
- **Agora.** Marro, La Malfa, Wright, Li, Shadbolt, Wooldridge, Torr, "A Scalable Communication Protocol for Networks of Large Language Models," arXiv 2410.11905 (peer-reviewed venue UNVERIFIED; no venue on the arXiv record).
  - Finding: defines the "Agent Communication Trilemma" (versatility, efficiency, portability). Agents "use standardised routines for frequent communications, natural language for rare communications, and LLM-written routines for everything in between." Self-organizing protocols emerge in large networks.
  - Relation: a **borrowable method** (negotiated protocol), and the precedent for a hybrid policy. — [arXiv](https://arxiv.org/abs/2410.11905)
- **ProtocolBench.** Du, Su, Li, Ding, Yang, Han et al., "ProtocolBench: Which LLM MultiAgent Protocol to Choose?," ICML 2026, arXiv 2510.17149.
  - Finding: compares A2A, ACP, ANP and Agora on success, latency, overhead and failure robustness. Completion time varies by up to 36.5% across protocols. ProtocolRouter cuts Fail-Storm recovery time by up to 18.1%.
  - Relation: contrast. Transport-layer reliability only; no semantic or convention errors. — [arXiv](https://arxiv.org/abs/2510.17149)

**Efficiency-oriented channel design**
- **Optima.** Chen, Yuan, Qian, Yang, Liu, Sun, Findings of ACL 2025 ([Anthology 2025.findings-acl.601](https://aclanthology.org/2025.findings-acl.601/)), arXiv 2410.08115.
  - Finding: generate–rank–select–train with a reward balancing task performance, token efficiency and readability. Up to 2.8x performance with under 10% of tokens on information-asymmetric tasks.
  - Relation: a borrowable training recipe for "learning to communicate units." — [arXiv](https://arxiv.org/abs/2410.08115)
- **AgentPrune.** Zhang, Yue, Li, Yun, Wan, Wang et al., "Cut the Crap: An Economical Communication Pipeline for LLM-based Multi-Agent Systems," arXiv 2410.02506 (venue UNVERIFIED).
  - Finding: prunes redundant messages and matches state-of-the-art topologies at $5.6 vs $43.7. — [arXiv](https://arxiv.org/abs/2410.02506)
- **Sparse topology.** Li, Du, Zhang, Zhang, Hou, Grabowski et al., "Improving Multi-Agent Debate with Sparse Communication Topology," arXiv 2406.11776 (venue UNVERIFIED).
  - Finding: sparse connectivity matches or beats fully connected debate at lower cost. — [arXiv](https://arxiv.org/abs/2406.11776)
- **Exchange-of-Thought.** Yin, Sun, Chang, Guo, Dai, Huang et al., EMNLP 2023, arXiv 2312.01823.
  - Finding: four communication paradigms (Memory, Report, **Relay**, Debate) with a confidence-evaluation mechanism.
  - Relation: an early "hybrid NL + confidence" precedent for C5. — [arXiv](https://arxiv.org/abs/2312.01823)
- **ReConcile.** Chen, Saha, Bansal, ACL 2024, arXiv 2309.13007.
  - Finding: messages carry answers, explanations **and confidence scores**, with confidence-weighted voting. Up to +11.4% over prior single- and multi-agent baselines.
  - Relation: the **closest precedent for C5** (NL plus confidence). — [arXiv](https://arxiv.org/abs/2309.13007)

**Reliability-oriented audits of channels**
- **ICR audit (very recent; important).** Li, Yang, Zhang, Cheng, Ping, Bogdan, "Beyond Final Accuracy: Auditing Communication in LLM Multi-Agent Systems," arXiv 2610.01042, posted 2026-10-01 (venue UNVERIFIED).
  - Method: the Independent–Communicate–Revise (ICR) framework fixes initial reasoning, then measures **correction vs preservation** conditional on both agents' initial correctness, with a **no-message revision control**. It covers textual and latent channels.
  - Findings:
    - "similar aggregate accuracy can conceal substantially different revision behaviors."
    - Full reasoning (vs answers only) "increases correction while reducing preservation on all four benchmarks, so richer messages amplify beneficial and harmful influence alike."
    - A "structured verification policy shifts every channel toward greater preservation and lower correction."
    - The authors "challenge treating communication quality as an intrinsic property of a channel."
  - Relation: **novelty threat to L4's trade-off framing, and the best borrowable metric set.** — [arXiv](https://arxiv.org/abs/2610.01042)
- **Facts Without Rules.** Wang, Goyal, Chandrasekharan, Sundaram, "Facts Without Rules: Boundary Metadata Collapse in Multi-Agent LLM Handoffs," arXiv 2608.29028.
  - Findings:
    - Handoff summaries keep operational facts but drop boundary metadata. Free-text handoffs keep markers at σ_b≈0.80; a 25-word budget drops them to ≈0.57 while fact survival stays near ceiling.
    - Vague boundary language leaks in 73% (GPT) and 50% (DeepSeek) of cases; explicit constraints reduce leakage to under 15%.
    - A gold audience allowlist nearly eliminates leakage.
  - Relation: a **close structural parallel** ("the value survives, the frame is dropped"). Units are frame metadata. — [arXiv](https://arxiv.org/abs/2608.29028)

### Inferences
- Every latent-channel paper evaluates on shared-convention reasoning tasks (math, QA, code). None asks whether *context that was never encoded* (the sender's locale default) can cross a channel. L4's core claim, that the failure is in pragmatic decoding rather than bandwidth, is therefore orthogonal to and untested by the latent literature. A small latent arm (C2C or KVComm on two open-weight models) would let L4 claim coverage of "NL vs structured vs latent," which is one of the theme's listed topics.
- The structured-vs-free literature measures accuracy or fidelity. Only two papers measure *how a channel changes receiver decisions*: ICR (correction vs preservation) and, partly, Facts Without Rules (leakage). L4's ask-vs-act safety axis is a third decision-level measure. It should be presented as an instance of ICR's thesis that channel quality depends on the receiver policy, with the new element that the harm is caused by a convention gap and not by a wrong peer.
- 2607.09678's result (strong relays are nearly lossless in every format) helps L4 rule out transmission loss as an explanation. If L4 shows the bare number is relayed verbatim under C1 and still misread, then the failure is pragmatic decoding.

### Gaps
- Found no paper that compares NL vs JSON vs latent channels under a sender–receiver convention mismatch (units, currency, decimal separator, date format).
- Found no peer-reviewed paper titled or framed as "Should agents speak JSON?". The closest are 2607.09678 and ProtocolBench.
- Could not confirm peer-reviewed venues for Agora, Faithful-Not-Corrective, the ICR audit, Facts Without Rules, or Wenzel 2607.14103.

---

## (b) Emergent communication, negotiated or learned protocols, and the revival with LLMs

### Takeaway
Classic emergent-communication research (deep RL referential games) has been revived with LLM agents in three strands:
1. **Convention formation**: populations converge on conventions, but heterogeneous pairs often fail to.
2. **Task-oriented or covert protocols**: these raise efficiency but harm transparency.
3. **Training agents to speak and listen**: RL or DPO on communicative reward.

Units and currency defaults are literal Lewis-style conventions. The finding that heterogeneous human–AI dyads fail to form shared conventions is the closest cognitive-science analogue to L4's cross-locale agent pairs.

### Cited Findings
- **Survey.** Lazaridou & Baroni, "Emergent Multi-Agent Communication in the Deep Learning Era," arXiv 2006.02419.
  - The canonical survey, covering both scientific (language evolution) and applied (agents communicating with each other and with us) motivations.
  - Relation: background. — [arXiv](https://arxiv.org/abs/2006.02419)
- **Survey.** Peters, Waubert de Puiseau, Tercan, Gopikrishnan, Lucas De Carvalho, Bitter et al., "Emergent Language: A Survey and Taxonomy," *Autonomous Agents and Multi-Agent Systems* 39, 18 (2025), arXiv 2409.02645.
  - Reviews 181 publications, including "existing evaluation methods and metrics."
  - Relation: source for metrics vocabulary. — [arXiv](https://arxiv.org/abs/2409.02645)
- **Ashery, Aiello, Baronchelli**, "Emergent social conventions and collective bias in LLM populations," *Science Advances* 11, eadu9368 (2025), arXiv 2410.08948.
  - Findings:
    - Universally adopted conventions emerge spontaneously in decentralized LLM populations.
    - Collective biases arise even when no single agent is biased.
    - Committed adversarial minorities can flip conventions.
  - Relation: supports the "conventions are a communication-level phenomenon" framing.
  - Positioning: "Ashery et al. show conventions form *within* an LLM population; L4 studies what happens *across* populations whose conventions were fixed in advance by locale." — [arXiv](https://arxiv.org/abs/2410.08948)
- **Jones, Lombardi, Mahowald, Bergen**, "LLMs and people both learn to form conventions — just not with each other," arXiv 2602.08208 (venue UNVERIFIED).
  - Findings:
    - Both human–human and AI–AI dyads form conventions (higher accuracy, shorter turns).
    - Heterogeneous human–AI pairs fail.
    - Prompting LLMs to look humanlike matches message length but not accuracy or lexical overlap. Alignment "requires... shared interpretative biases."
  - Relation: **supports**. It is the closest conceptual cousin: mismatched interpretive priors break grounding. — [arXiv](https://arxiv.org/abs/2602.08208)
- **Kouwenhoven, Peeperkorn, de Kleijn, Verhoef**, "Shaping Shared Languages: Human and LLMs' Inductive Biases in Emergent Communication," IJCAI 2025 (Human-centred AI track), arXiv 2503.04395.
  - Finding: referentially grounded vocabularies emerge in Human–Human, LLM–LLM and Human–LLM pairs. Mixed interaction yields vocabularies that are more human-like than LLM-like.
  - Relation: a borrowable referential-game design. — [arXiv](https://arxiv.org/abs/2503.04395)
- **ICCA.** Hua & Artzi, "Talk Less, Interact Better: Evaluating In-context Conversational Adaptation in Multimodal LLMs," COLM 2024, arXiv 2408.01417.
  - Finding: MLLMs understand a partner's increasingly efficient language but do not spontaneously make their own language more efficient. Only heavy prompting elicits this in GPT-4. — [arXiv](https://arxiv.org/abs/2408.01417)
- **Hua, Wang, Artzi**, "Post-training for Efficient Communication via Convention Formation," COLM 2025, arXiv 2508.06482.
  - Finding: targeted fine-tuning on heuristically identified convention-formation demonstrations significantly improves convention formation on two new benchmarks.
  - Relation: **borrowable training method** for "learning to communicate conventions." — [arXiv](https://arxiv.org/abs/2508.06482)
- **Carmeli, Paradise, Goldwasser, Belinkov, Meir**, "Investigating the Development of Task-Oriented Communication in Vision-Language Models," arXiv 2601.20641 (venue UNVERIFIED).
  - Findings: VLM agents in referential games develop more efficient task-adapted protocols and also **covert** protocols that humans and external agents struggle to interpret. Similar models coordinate spontaneously without shared protocols.
  - Relation: contrast. Efficiency costs transparency, which mirrors L4's accuracy-vs-safety theme. — [arXiv](https://arxiv.org/abs/2601.20641)
- **Taniguchi, Ueda, Nakamura, Suzuki, Taniguchi**, "Generative Emergent Communication: Large Language Model is a Collective World Model," arXiv 2501.00226.
  - Finding: frames language emergence as decentralized Bayesian inference (Collective Predictive Coding), with the LLM as a decoder of a society-level world model.
  - Relation: theoretical background. — [arXiv](https://arxiv.org/abs/2501.00226)
- **CoMet.** Xu & Zhong, "CoMet: Metaphor-Driven Covert Communication for Multi-Agent Language Games," ACL 2025 Main ([Anthology 2025.acl-long.389](https://aclanthology.org/2025.acl-long.389/)), ACL 2025 SAC Highlight ([awards page](https://2025.aclweb.org/program/awards/)), arXiv 2505.18218.
  - Finding: a hypothesis-based metaphor reasoner plus generator for Undercover and Adversarial Taboo. Metaphor acts as "asymmetric encryption in natural language" (search snippet).
  - Relation: an example of an accepted mechanism paper in agent communication. — [arXiv](https://arxiv.org/abs/2505.18218)
- **Sarkar, Xia, Liu, Sadigh**, "Training Language Models for Social Deduction with Multi-Agent Reinforcement Learning," AAMAS 2025, arXiv 2502.06060.
  - Finding: splits communication into listening (predict world state from discussion) and speaking (reward by influence on other agents). This doubles win rates vs standard RL in an Among-Us-style game.
  - Relation: **borrowable reward decomposition**. For example, reward the sender when its message changes the receiver's unit interpretation toward the truth. — [arXiv](https://arxiv.org/abs/2502.06060)
- **Agora, again.** Agora is the explicit "agents negotiate the protocol" paper: frequent exchanges use standardized routines, rare ones use NL, and LLM-written routines cover the middle. Emergent, self-organizing protocols arise. — [arXiv](https://arxiv.org/abs/2410.11905)
- **Protocol taxonomy.** Sander, Gidey, Lenz, Knoll, "A Technical Taxonomy of LLM Agent Communication Protocols," arXiv 2606.19135.
  - Finding: classifies 9 maintained protocols. All agent-to-agent protocols combine hybrid payloads with session state. "two negotiate schemas at runtime." No single protocol will maximize versatility, efficiency and portability.
  - Relation: supports "negotiated schema" as a real deployment pattern. — [arXiv](https://arxiv.org/abs/2606.19135)
- **Covert channels as a risk.** Motwani, Baranchuk, Strohmeier, Bolina, Torr, Hammond et al., "Secret Collusion among AI Agents: Multi-Agent Deception via Steganography," arXiv 2402.07510 (venue UNVERIFIED on the arXiv record).
  - Finding: formalizes secret collusion; GPT-4 shows a steganographic capability jump. — [arXiv](https://arxiv.org/abs/2402.07510)
- **Mathew, Matthews, McCarthy, Velja, Schroeder de Witt, Cope et al.**, "Hidden in Plain Text: Emergence & Mitigation of Steganographic Collusion in LLMs," IJCNLP-AACL 2025 Oral, arXiv 2410.03768.
  - Finding: misspecified rewards produce steganographic collusion, and paraphrasing mitigation is "not fully effective."
  - Relation: contrast. Opaque channels are a safety cost, which is relevant if L4 adds a latent arm. — [arXiv](https://arxiv.org/abs/2410.03768)
- **UNVERIFIED.** OpenReview forum zy06mHNoO2, "Emergence of Machine Language in LLM-based Agent Communication." A search snippet reports two LLM agents developing a shared language over 541 objects in 4 rounds. The OpenReview page could not be opened (bot check), so the authors, venue and decision are unknown. — [OpenReview](https://openreview.net/forum?id=zy06mHNoO2)

### Inferences
- In this literature L4's unit defaults are *pre-existing conventions* (Lewis 1969 sense) that differ across agent "communities." That differs from emergent-communication work, where conventions form during interaction. A natural extension is a repeated-interaction condition: after one silent-error episode with feedback, does the dyad converge on explicit units (ad-hoc convention formation à la Hua & Artzi)? This would move L4 into "learning to communicate."
- Agora's frequency-based mix (structured routines for common exchanges, NL for rare ones) gives L4 a principled design hypothesis: typed unit fields for routine quantity hand-offs, NL plus clarification for novel cases. L4 could test this hybrid instead of the five fixed channels.

### Gaps
- Found no LLM emergent-communication study that uses units or measurement conventions as the referent space.
- Did not verify Lewis (1969) *Convention* bibliographic details from a primary page.

---

## (c) Evaluation of agent communication: metrics for fidelity, grounding success, efficiency, robustness; benchmarks; debate failures

### Takeaway
Agent-communication evaluation is moving from final-task accuracy toward process- and decision-level metrics:
- milestone KPIs (MultiAgentBench) and process metrics (Collab-Overcooked);
- revision decomposition with no-message controls (ICR);
- fact and marker survival through relays (Faithful-Not-Corrective, Facts Without Rules);
- failure taxonomies (MAST).

The emergent-communication literature contributes the key methodological warning: a message can be informative without being *used* (positive signaling vs positive listening). Debate studies show that communication often adds little beyond voting and can flip correct answers to wrong ones.

### Cited Findings
- **MultiAgentBench (MARBLE).** Zhu, Du, Hong, Yang, Guo, Wang et al., "MultiAgentBench: Evaluating the Collaboration and Competition of LLM agents," ACL 2025 Main ([Anthology PDF 2025.acl-long.421](https://aclanthology.org/2025.acl-long.421.pdf)), arXiv 2503.01935.
  - Finding: milestone-based KPIs plus task scores across star, chain, tree and graph topologies. Graph topology is best in the research scenario, and cognitive planning raises milestone achievement by 3%.
  - Relation: borrowable process metric. — [arXiv](https://arxiv.org/abs/2503.01935)
- **COMMA.** Ossowski, Maqbool, Chen, Cai, Bradshaw, Hu, "COMMA: A Communicative Multimodal Multi-Agent Benchmark," TMLR 2025, arXiv 2410.07553.
  - Finding: puzzles with unequal information access. Many CoT reasoning VLMs (e.g., R1-Onevision, LLaVA-CoT) "struggle to outperform even a random baseline in agent-agent collaboration."
  - Relation: an information-asymmetry benchmark template. — [arXiv](https://arxiv.org/abs/2410.07553)
- **Collab-Overcooked.** Sun, Zhang, Niu, Ren, Xu, Fu et al., EMNLP 2025 Main, EMNLP 2025 SAC Highlight ([awards](https://2025.emnlp.org/program/awards/)), arXiv 2502.20073.
  - Finding: process-oriented collaboration metrics across 13 LLMs. Models are strong at goal interpretation but weak at active collaboration and continuous adaptation. — [arXiv](https://arxiv.org/abs/2502.20073)
- **LLM-Coordination.** Agashe, Fan, Reyna, Wang, arXiv 2310.03903.
  - Finding: agents do well when decisions depend on the environment but struggle when they must consider partners' beliefs and intentions. CoordQA isolates ToM and joint planning.
  - Relation: a template for "modelling partners." — [arXiv](https://arxiv.org/abs/2310.03903)
- **HiddenBench** (see a): 30.1% vs 80.7%. The failure is "agents cannot recognize or act under latent information asymmetry." — [arXiv](https://arxiv.org/abs/2505.11556)
- **ICR audit** (see a): correction/preservation conditional on initial correctness, no-message control, receiver-policy comparison. — [arXiv](https://arxiv.org/abs/2610.01042)
- **MAST.** Cemri, Pan, Yang, Agrawal, Chopra, Tiwari et al., "Why Do Multi-Agent LLM Systems Fail?," arXiv 2503.13657 (venue UNVERIFIED; arXiv comment "ArXiv v3").
  - Finding: 1600+ annotated traces across 7 MAS frameworks, 14 failure modes in 3 categories (system design, **inter-agent misalignment**, task verification), κ=0.88, plus an LLM-judge pipeline.
  - Relation: L4's silent convention errors are an instance of inter-agent misalignment. Cite it to place them in the taxonomy. — [arXiv](https://arxiv.org/abs/2503.13657)
- **Telephone game.** Perez, Kovač, Léger, Colas, Molinaro, Derex et al., "When LLMs Play the Telephone Game: Cultural Attractors as Conceptual Tools to Evaluate LLMs in Multi-turn Settings," ICLR 2025, arXiv 2407.04503.
  - Finding: transmission chains drift toward attractor states (toxicity, positivity, length). Open-ended instructions produce stronger attraction.
  - Relation: a relay-fidelity methodology. — [arXiv](https://arxiv.org/abs/2407.04503)
- **Lowe, Foerster, Boureau, Pineau, Dauphin**, "On the Pitfalls of Measuring Emergent Communication," AAMAS 2019, arXiv 1903.05168.
  - Finding: agents can appear to communicate (their messages predict their own actions) while the messages do not affect the listener. The paper separates *positive signaling* from *positive listening* and warns against relying on reward gain alone.
  - Relation: **borrowable**. L4 should show the receiver actually *uses* the unit field (causal ablation of the field), not just that the sender emits it. — [arXiv](https://arxiv.org/abs/1903.05168)
- **Jaques, Lazaridou, Hughes, Gulcehre, Ortega, Strouse et al.**, "Social Influence as Intrinsic Motivation for Multi-Agent Deep RL," arXiv 1810.08647 (venue ICML 2019 per common citation; UNVERIFIED on the arXiv record).
  - Finding: counterfactual causal influence of one agent's message on another's action, equivalent to mutual information between actions.
  - Relation: a borrowable metric for "did the unit statement change the action." — [arXiv](https://arxiv.org/abs/1810.08647)
- **AgentComm-Bench.** Bansal & Gangwani, arXiv 2603.20285.
  - Finding: embodied cooperation under latency, packet loss, bandwidth collapse, stale memory and conflicting evidence. Stale memory and bandwidth collapse cause over 96% drops in navigation; content corruption cuts perception F1 by over 85%.
  - Relation: contrast. It covers channel impairments, not semantic ones. — [arXiv](https://arxiv.org/abs/2603.20285)
- **Debate failures**
  - **Choi, Zhu, Li**, "Debate or Vote: Which Yields Better Decisions in Multi-Agent LLMs?," NeurIPS 2025 Spotlight, arXiv 2508.17536. Majority voting accounts for most gains attributed to debate, and debate induces a martingale over beliefs, so debate alone does not improve expected correctness. — [arXiv](https://arxiv.org/abs/2508.17536)
  - **Wynn, Satija, Hadfield**, "Talk Isn't Always Cheap: Understanding Failure Modes in Multi-Agent Debate," ICML 2025 MAS Workshop, arXiv 2509.05396. Models "frequently shift from correct to incorrect answers in response to peer reasoning," even when stronger models are the majority. — [arXiv](https://arxiv.org/abs/2509.05396)
  - **Zhang, Cui, Chen, Wang, Zhang, Wang et al.**, "Stop Overvaluing Multi-Agent Debate," arXiv 2502.08788. Across 5 MAD methods, 9 benchmarks and 4 models, MAD often fails to beat CoT or self-consistency. — [arXiv](https://arxiv.org/abs/2502.08788)
  - **Smit, Duckworth, Grinsztajn, Barrett, Pretorius**, "Should we be going MAD?," arXiv 2311.17371 (venue UNVERIFIED). MAD does not reliably beat self-consistency or ensembling and is hyperparameter-sensitive. — [arXiv](https://arxiv.org/abs/2311.17371)
  - **Ni & Zou**, "Silent Dissent: LLM Agents That Yield to the Majority Still Represent Their Original Premise," arXiv 2610.02702 (2026-10-02). Agents that give in to unanimous wrong peers still represent their original bridge entity in intermediate layers (J-lens hit@100 of 0.85, 0.22 and 0.24 for three models, vs 0.00–0.06 for the logit lens).
    - Relation: a **borrowable probe**. Does a receiver that silently misdecodes a unit still represent the alternative unit internally? — [arXiv](https://arxiv.org/abs/2610.02702)
- **Grounding failures between agents.** Yao, Zou, Hawkins, "Talk is Cheap, Communication is Hard: Dynamic Grounding Failures and Repair in Multi-Agent Negotiation," arXiv 2605.01750 (venue UNVERIFIED).
  - Finding: four failure modes: history loss, anchoring, equal-split defaults, and **referential binding errors across turns**. "the bottleneck lies in dynamic grounding."
  - Relation: supports. It is the nearest agent-to-agent grounding paper. — [arXiv](https://arxiv.org/abs/2605.01750)
- **Illusion of Alignment.** Liu, Luo, Wang, Ju, Liu, Lei et al., "Illusion of Alignment: Detecting Hidden Disagreement in Collaborative Dialogue," arXiv 2608.08210.
  - Finding: diagnostic MCQs expose hidden disagreement. The best model reaches 49.5% F1, and IoA-Prober-8B 51.8%. The prober surfaces 2.89 unvoiced disagreements per real meeting and improves downstream multi-agent results (BigCodeBench-Hard, HiddenBench).
  - Relation: a borrowable detection method (probe both agents' interpretation of the same quantity). — [arXiv](https://arxiv.org/abs/2608.08210)
- **Multi-turn underspecification.** Laban, Hayashi, Zhou, Neville, "LLMs Get Lost In Multi-Turn Conversation," arXiv 2505.06120.
  - Finding: an average 39% drop from single- to multi-turn over 200,000+ simulated conversations, split into a minor aptitude loss and a large **unreliability** increase. "LLMs often make assumptions in early turns."
  - Relation: a borrowable decomposition (aptitude vs unreliability) for L4's accuracy-vs-safety. — [arXiv](https://arxiv.org/abs/2505.06120)
- **Surveys of communication-centric MAS.**
  - Yan, Zhou, Zhang, Zhang, Zhou, Miao et al., "Beyond Self-Talk: A Communication-Centric Survey of LLM-Based Multi-Agent Systems," *Frontiers of Computer Science* (DOI 10.1007/s11704-026-50857-y per arXiv comment), arXiv 2502.14321. It flags "inadequate benchmarking" of communication. — [arXiv](https://arxiv.org/abs/2502.14321)
  - Yuan, Lyu, Yuan, Zhang, He, Geng et al., "Beyond Message Passing: A Semantic View of Agent Communication Protocols," arXiv 2604.02369. Across 18 protocols, support for "clarification, context alignment, and verification" is limited, and semantic duties are pushed into prompts. — [arXiv](https://arxiv.org/abs/2604.02369)

### Inferences
- A defensible, reviewer-proof metric suite for L4, assembled from the above:
  1. silent-error rate (wrong action with no question asked);
  2. ask/clarify rate (Shaikh grounding acts);
  3. confident-wrong rate;
  4. ICR-style correction/preservation conditional on whether the receiver's default matches the sender's convention;
  5. a no-message or no-metadata control;
  6. a causal ablation showing the unit field is *used* (Lowe et al.);
  7. token and turn cost (Optima-style efficiency).
  Reporting aptitude vs unreliability (Laban) would separate "can decode when told" from "fails to ask."
- The debate literature suggests reviewers will ask whether gains come from communication or from extra compute or voting. L4's channels are single-hop delegation, so this is less pressing. A no-message baseline still defends against it.

### Gaps
- Found no benchmark whose metric is specifically "convention-grounding success" between agents.
- Found no peer-reviewed study that measures read-back/hearback between LLM agents. Web results were blogs; for example, a vendor post claims a "25% failure rate" for unverified instructions with no methodology, so it is not cited as evidence.

---

## (d) What the theme track and recent ACL/EMNLP/NAACL tracks have accepted (and what made papers strong)

### Takeaway
"Language as a Medium for Agentic Communication" is new for NAACL 2027. The 2025 NAACL theme was different ("NLP in a Multicultural World"), and its 23/71 figure is a base rate for *a* NAACL theme track, not this one. Recent best-theme-paper winners are large resources or methods squarely on-theme. Agent-communication papers that received ACL/EMNLP highlights are either new benchmarks with process metrics (Collab-Overcooked, MultiAgentBench) or new communication mechanisms (CoMet, Interlat).

### Cited Findings
- **NAACL 2027 CFP (opened).**
  - The theme frames language as "a computational mechanism for coordination, reasoning, negotiation, teaching, and collaboration."
  - Listed topics: learning to communicate (what, when, how; pragmatic strategies); communication and collective reasoning; modelling partners (common ground; knowledge, beliefs, intentions); forms of communication (NL vs structured or learned protocols); efficiency and reliability (uncertainty, ambiguity, miscommunication mitigation); evaluation (benchmarks for effectiveness and robustness).
  - Relevance rule, verbatim: "The use of multiple agents alone is not sufficient for relevance to the theme. Communication should constitute a substantive research question, computational mechanism, or source of capability in the work."
  - Logistics: deadline 2026-10-12 (ARR); conference June 1–5, 2027, San Francisco; 8/4 pages. No theme-specific award appeared in the fetched text. — [NAACL 2027 CFP](https://2027.naacl.org/calls/main_conference_papers/)
- **NAACL 2025 theme ("NLP in a Multicultural World").** Front matter, opened and extracted:
  - "We received 71 submissions to the special theme, of which 23 were accepted for presentation at the conference" (≈32%).
  - For context, an estimated 22% of October-cycle NAACL-intended papers went to main and 15% to Findings (37% total). 719 main and 477 Findings out of 1,647 committed papers.
  - It is not stated whether the 23 include Findings. — [NAACL 2025 front matter](https://aclanthology.org/2025.naacl-short.0.pdf)
- **NAACL 2025 Best Theme Paper.** Winata, Hudi, Irawan, Anugraha, Putri, Wang et al., "WorldCuisines: A Massive-Scale Benchmark for Multilingual and Multicultural Visual Question Answering on Global Cuisines," arXiv 2410.12705 (arXiv comment: "Best Theme Paper at NAACL 2025").
  - What made it strong: scale (1M+ VQA points, 30 languages and dialects, 9 families), a released KB and training set, and a clear on-theme failure ("struggle with adversarial contexts").
  - The NAACL 2025 accepted-papers page does not mark theme papers, so the other 22 could not be enumerated. — [arXiv](https://arxiv.org/abs/2410.12705); [NAACL 2025 accepted papers](https://2025.naacl.org/program/accepted_papers/)
- **ACL 2025.**
  - Theme: "Generalization of NLP Models," with a Thematic Paper Award. — [ACL 2025 CFP](https://2025.aclweb.org/calls/main_conference_papers/)
  - The awards page lists theme-paper awards to "MaCP: Minimal yet Mighty Adaptation via Hierarchical Cosine Projection," "Meta-rater: A Multi-dimensional Data Selection Method for Pre-training Language Models," and "SubLIME: Subset Selection via Rank Correlation Prediction for Data-Efficient LLM Evaluation." The fetch tool's summary was internally inconsistent ("two papers" but three listed), so the exact count is **UNVERIFIED**.
  - Agent-communication SAC Highlight: CoMet. — [ACL 2025 awards](https://2025.aclweb.org/program/awards/)
  - MultiAgentBench was ACL 2025 main (2025.acl-long.421). Optima was Findings of ACL 2025.
- **EMNLP 2025.**
  - Theme: "Advancing our Reach: Interdisciplinary Recontextualization of NLP," with a Special Theme Best Paper award. — [EMNLP 2025 CFP](https://2025.emnlp.org/calls/main_conference_papers/)
  - Best Special Theme Paper: "InterIDEAS: Philosophical Intertextuality via LLMs" (Yang, Xu, Huang, Jurgensen, Hu, Wang).
  - SAC Highlights in the agent space: Collab-Overcooked; "ReSo: A Reward-driven Self-organizing LLM-based Multi-Agent System for Reasoning Tasks." — [EMNLP 2025 awards](https://2025.emnlp.org/program/awards/)
- **ACL 2026.**
  - Theme: explainability/interpretability, with a Thematic Paper Award (search snippet of the CFP). — [ACL 2026 CFP](https://2026.aclweb.org/calls/main_conference_papers/)
  - Agent-communication papers in ACL 2026 main include Interlat (2026.acl-long.1248) and "CIA: Inferring the Communication Topology from LLM-based Multi-Agent Systems" (2026.acl-long.815; title from search snippet only, details UNVERIFIED). ACL 2026 also had a tutorial, "Towards Effective and Efficient Multi-Agent Language Model Systems." — [Anthology 2026.acl-long.1248](https://aclanthology.org/2026.acl-long.1248/); [Anthology 2026.acl-long.815](https://aclanthology.org/2026.acl-long.815/); [tutorial](https://aclanthology.org/2026.acl-tutorials.3/)
- **Other on-theme venue precedents.**
  - Shaikh et al. "Grounding Gaps in Language Model Generations" (NAACL 2024): communication as a research question with new grounding-act metrics. — [arXiv](https://arxiv.org/abs/2311.09144)
  - Hua & Artzi (COLM 2024, 2025): convention formation, evaluated then trained. — [arXiv](https://arxiv.org/abs/2508.06482)
  - CAPRI: a units/culture resource. Miao, Zhu, Shwartz, arXiv 2606.17688 (venue UNVERIFIED). — [arXiv](https://arxiv.org/abs/2606.17688)

### Inferences
- **What "strong" looks like (inference from the winners and highlights above):**
  1. A *resource at scale* with a crisp on-theme failure (WorldCuisines, MultiAgentBench, Collab-Overcooked).
  2. A *new mechanism* that makes communication itself the lever (CoMet, Interlat, C2C).
  3. A *cognitively grounded paradigm plus a fix* (HiddenBench, ICML; Shaikh et al.).

  A careful prompt-and-channel ablation on a mid-sized task set with one trade-off finding, which is L4's current shape, matches none of these templates. That plausibly explains the "plateau" reviews.
- For the theme's relevance rule, L4 qualifies as "communication as a substantive research question." The weakest part is "computational mechanism or source of capability." Adding a learned or negotiated protocol, read-back, or a latent arm would cover it.
- A 23/71 theme acceptance in 2025 is similar to the overall Main+Findings rate (37%). It is not evidence that theme tracks are easier, and the 2027 theme may be crowded given the volume of agent-communication work in 2026.

### Gaps
- Could not list the other 22 NAACL 2025 theme papers; the accepted-papers page lacks theme markers.
- Could not identify the NAACL 2025 "SAC award for the Special theme" paper title.
- No public data on NAACL 2027 theme submission volume.

---

## Pragmatics and semantics framing: Gricean quantity, presumptive grounding, RSA, bare numerals, underspecified quantities

### Takeaway
L4's failure maps cleanly onto established pragmatic theory:
- the sender under-informs, a violation of Grice's maxim of quantity, because it presumes common ground (Shaikh et al.'s "presumptive grounding");
- the receiver resolves the bare numeral with its own prior instead of reasoning about the speaker (an RSA-style listener would discount its own default);
- LMs compare quantities using heuristics over numerals and unit scale rather than by normalizing.

Explicit epistemic and unit markers are known to change model behavior. High-certainty phrasing *lowers* accuracy, and LMs are overconfident when they do express confidence. This offers a mechanism for L4's "stating units makes receivers act confidently" result.

### Cited Findings
- **Grounding Gaps.** Shaikh, Gligorić, Khetan, Gerstgrasser, Yang, Jurafsky, "Grounding Gaps in Language Model Generations" (earlier title "Grounding or Guesswork? LLMs are Presumptive Grounders"), NAACL 2024, arXiv 2311.09144.
  - Finding: compared with humans, LLMs produce fewer grounding acts (clarification, acknowledgment, follow-up) and "presume common ground." Training on contemporary preference data reduces grounding acts.
  - Relation: **the theoretical frame for L4**. L4 extends it to agent–agent exchanges and to an invisible ambiguity. — [arXiv](https://arxiv.org/abs/2311.09144)
- **Miehling, Nagireddy, Sattigeri, Daly, Piorkowski, Richards**, "Language Models in Dialogue: Conversational Maxims for Human-AI Interactions," arXiv 2403.15115 (venue UNVERIFIED).
  - Finding: Grice's four maxims plus benevolence and transparency. Models have "an internal prioritization of principles" that affects how they interpret the maxims. — [arXiv](https://arxiv.org/abs/2403.15115)
- **Saad, Murukannaiah, Singh**, "Gricean Norms as a Basis for Effective Collaboration," AAMAS 2025, arXiv 2503.14484.
  - Finding: GPT-4 agents given Gricean norms (quantity, quality, relation, manner, plus inference) interpret ambiguous, incomplete, invalid or irrelevant instructions with higher task accuracy.
  - Relation: borrowable prompt condition ("Gricean sender"). — [arXiv](https://arxiv.org/abs/2503.14484)
- **VanderHoeven, Nath, Krishnaswamy**, "Flout at Your Own Risk: LLMs Struggle with Pragmatic Cooperativity Under Epistemic Asymmetry," arXiv 2607.11053 (venue UNVERIFIED).
  - Finding: formalizes "collaborative epistemic asymmetry," linking task success to the cooperative principle. Failure modes "correlate with floutings of Grice's maxims that go unrecognized." Prompting and post-training help partially.
  - Relation: **supports, and a moderate novelty threat for a "Gricean framing" pitch**. — [arXiv](https://arxiv.org/abs/2607.11053)
- **Kim, Chin, Son, Kim, Kim**, "Applying the Gricean Maxims to a Human-LLM Interaction Cycle," CHI 2025 LBW, arXiv 2503.00858. Participatory design yields reinterpreted maxims and nine design considerations. — [arXiv](https://arxiv.org/abs/2503.00858)
- **"The Gricean Maxims in NLP – A Survey,"** INLG 2024 (authors not checked; search result only). — [Anthology PDF](https://aclanthology.org/2024.inlg-main.39.pdf)
- **Ruis, Khan, Biderman, Hooker, Rocktäschel, Grefenstette**, "The Goldilocks of Pragmatic Understanding: Fine-Tuning Strategy Matters for Implicature Resolution by LLMs," NeurIPS 2023 Spotlight, arXiv 2210.14986. Three of four model categories are near random on binary implicatures; example-level instruction tuning helps. — [arXiv](https://arxiv.org/abs/2210.14986)
- **RSA.** Frank & Goodman, "Predicting Pragmatic Reasoning in Language Games," *Science* 336:998 (2012), DOI 10.1126/science.1218633.
  - Finding: informative speakers plus Bayesian listeners give a parameter-free fit to human reference-game judgments.
  - Relation: borrowable listener model. A pragmatic receiver should infer that a speaker from locale X who omits the unit means X's default. — [Science](https://www.science.org/doi/10.1126/science.1218633)
- **Bare numerals.** Kennedy, "A 'de-Fregean' semantics (and neo-Gricean pragmatics) for modified and unmodified numerals," *Semantics & Pragmatics* 8(10):1–44 (2015).
  - Finding: unmodified and modified numerals differ in ordering relation, and ignorance and exactness inferences are neo-Gricean Quantity implicatures.
  - Relation: limited. It concerns exactness (at least/exactly), not units. It supports the general claim that a bare numeral's interpretation is partly pragmatic. — [S&P](https://semprag.org/article/view/sp.8.10)
- **Quantity heuristics in LMs.** Sasaki, Kamoda, Takahashi, Sato, Inui, Sakaguchi et al., "Language Models Compare Quantities Using Number-specific and Unit-specific Heuristics," arXiv 2606.03982 (venue UNVERIFIED).
  - Finding: LMs compare quantities such as "110 cm vs 1.2 m" by "a bag of heuristics over numerals and units" rather than converting to a shared scale. Causal interventions on the corresponding subspaces shift outputs.
  - Relation: **supports a mechanism** for misdecoding when the unit scale is absent. — [arXiv](https://arxiv.org/abs/2606.03982)
- **CAPRI.** Miao, Zhu, Shwartz, "LLMs Infer Cultural Context but Fail to Apply It When Responding," arXiv 2606.17688.
  - Finding: models infer a user's cultural background and recall the local measurement units, but "often fail to utilize the information... unless explicitly prompted to perform the tasks sequentially." Priors are "not culture-neutral."
  - Relation: **novelty threat, the reviewers' named precedent**. L4's C2 is the agent-to-agent analogue of CAPRI's explicit sequential prompting. — [arXiv](https://arxiv.org/abs/2606.17688)
- **Epistemic markers.** Zhou, Jurafsky, Hashimoto, "Navigating the Grey Area: How Expressions of Uncertainty and Overconfidence Affect Language Models," EMNLP 2023 Oral, arXiv 2302.13439.
  - Finding: injecting 50 epistemic markers changes accuracy by more than 80%. "expressions of high certainty result in a 7% decrease in accuracy as compared to low certainty expressions."
  - Relation: **supports a mechanism** for L4's safety result. An explicit unit statement may act as a certainty marker that suppresses the receiver's checking. — [arXiv](https://arxiv.org/abs/2302.13439)
- **Zhou, Hwang, Ren, Sap**, "Relying on the Unreliable: The Impact of Language Models' Reluctance to Express Uncertainty," ACL 2024, arXiv 2401.06730.
  - Finding: LMs rarely express uncertainty. When prompted they are overconfident, with an average 47% error among confident responses, and users rely on outputs regardless of certainty markers.
  - Relation: relevant to C5's confidence-channel calibration. — [arXiv](https://arxiv.org/abs/2401.06730)
- **Clarification training (borrowable fixes for "ask vs act").**
  - Zhang, Knox, Choi, "Modeling Future Conversation Turns to Teach LLMs to Ask Clarifying Questions," ICLR 2025, arXiv 2410.13788. Preference labels from simulated future turns give +5% F1 on interpretation recovery. — [arXiv](https://arxiv.org/abs/2410.13788)
  - Chen, Sun, Pfister, Arık, "Learning to Clarify: Multi-turn Conversations with Action-Based Contrastive Self-Training," ICLR 2025, arXiv 2406.00222. Models "overhedge or implicitly guess users' true intents rather than asking"; ACT is DPO-based. — [arXiv](https://arxiv.org/abs/2406.00222)

### Inferences
- L4's three regimes map onto pragmatic theory:
  - **C1, bare numbers**: a Quantity violation by the sender together with presumptive grounding by the receiver (Shaikh).
  - **C2, stated units**: Quantity satisfied. But the statement doubles as a certainty marker (Zhou 2023), which suppresses grounding acts and yields "confident actions."
  - **C3, typed field**: shifts the burden from pragmatics to schema compliance. It works only if the field is validated (see the Mars Climate Orbiter analogue below).

  An RSA listener that models the sender's locale is the normative baseline. It predicts the receiver should ask exactly when the posterior over conventions is spread and the cost of error is high. L4 could fit or compare receivers against that normative policy.
- "Unit omission as an implicature failure" is defensible. When speaker and hearer share a default, omission is cooperative (it conveys "the usual unit"). When their defaults differ, the same omission yields a false implicature. This is a cleaner linguistic story than "cultural knowledge" and avoids CAPRI's framing.

### Gaps
- Found no NLP paper specifically on *underspecified or unitless numerals* (default-unit resolution) beyond CAPRI (units by user culture) and the prior-work file's "Numerical Localisation in LLM Translations" (2608.05232, not re-verified here).
- Found no RSA-style model applied to LLM agent-to-agent unit or currency interpretation.

---

## Human–human analogues: aviation phraseology and read-back/hearback, spaceflight interface specs, medication-order conventions

### Takeaway
Safety-critical human domains converged on three protocol fixes for the same bare-number problem:
1. **State the unit and all digits** (ICAO/FSF altimeter SOPs). This is L4's C2.
2. **Typed interface specifications** (NASA's Software Interface Specification). This is L4's C3. The Mars Climate Orbiter was lost because a typed spec existed but was not followed, and the receiving team *assumed* metric.
3. **Read-back/hearback.** The receiver echoes the interpreted value and the sender checks it (ICAO Annex 11; Joint Commission verbal orders).

L4 tests 1 and 2 but not 3, the domain's strongest fix.

### Cited Findings
- **ICAO APAC ATM/SG/13 IP/06**, "Importance of ATC Readback and Hearback" (presented by Pakistan, August 2025), opened and extracted.
  - "ICAO Annex 11 paragraph 3.7.3 describes the requirement for flight crew and airside drivers to readback safety related parts of ATC clearance and instructions... It also requires controllers to ensure proper hearback to identify any discrepancy in readback."
  - ICAO references cited: Annex 11 3.7.3; Annex 10 Vol. II 5.1.1.1 and 5.2; PANS-ATM Doc 4444 4.5.7.5 and C12; guidance material Doc 9432.
  - Causes of readback/hearback errors listed: "non-standard Phraseology... expectation bias, call sign confusion, language barriers, accent variations."
  - Relation: borrowable protocol. "Expectation bias" is the human term for receiver default decoding. — [ICAO IP/06 PDF](https://www.icao.int/sites/default/files/APAC/Meetings/2025/2025%20ATMSG13/04-Information%20Papers/IP06%20Importance%20of%20ATC%20Readback%20and%20Hearback%20%20.pdf)
- **Flight Safety Foundation ALAR Briefing Note 3.1, "Barometric Altimeter and Radio Altimeter"** (*Flight Safety Digest*, Aug–Nov 2000), opened and extracted.
  - "A transmission such as 'altimeter setting six seven' can be interpreted as 28.67 in. Hg, 29.67 in. Hg, 30.67 in. Hg or 967 hPa." This is a textbook bare-number ambiguity.
  - "a QNH of 991 hPa was set mistakenly on the altimeter as 29.91 in. Hg (equivalent to 1012 hPa), resulting in the true altitude being 640 feet lower than indicated."
  - SOP when broadcasting or reading back: "All digits, as well as the unit of measurement (e.g., inches or hectopascals), should be announced."
  - The ALAR Task Force found lack of positional awareness was a causal factor in 51% of 76 approach-and-landing accidents and serious incidents (1984–1997).
  - The note lists "Confusion about units of measurement" among the causes of altimeter-setting errors. — [FSF ALAR BN 3.1](https://flightsafety.org/wp-content/uploads/2016/09/alar_bn3-1-altimeter.pdf)
- **NASA, *Mars Climate Orbiter Mishap Investigation Board Phase I Report*** (Nov 10, 1999; chair Arthur G. Stephenson), opened and extracted.
  - Root cause: "failure to use metric units in the coding of a ground software file, 'Small Forces,'... The output from the SM_FORCES application code as required by a MSOP Project Software Interface Specification (SIS) was to be in metric units of Newton-seconds (N-s). Instead, the data was reported in English units of pound-seconds (lbf-s)."
  - "the trajectory modelers assumed the data was provided in metric units per the requirements." The effect was underestimated "by a factor of 4.45," and the trajectory was about 170 km lower than planned.
  - Contributing cause 5, communications: "When conflicts in the data were uncovered, the team relied on e-mail to solve problems, instead of formal problem resolution processes."
  - Recommendation: "a software audit for SIS compliance on all data transferred between" teams.
  - Relation: **a direct analogue of C3 and C4**. A typed declaration without validation still yields silent errors, and receivers decode by assumption. — [NASA LLIS PDF](https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf)
- **Air Canada Flight 143 ("Gimli Glider"), July 23, 1983** (search snippet only; primary report not opened).
  - Fuel was computed with 1.77 (litres→pounds) instead of about 0.8 (litres→kilograms), so the aircraft carried 22,300 lb rather than 22,300 kg, roughly half the required fuel.
  - The Board of Inquiry final report (Lockwood) is hosted by the FAA. — [FAA-hosted Board of Inquiry report](https://www.faa.gov/sites/faa.gov/files/2024-12/AirCanada143_C-GAUN.pdf); [CBC archive](https://www.cbc.ca/archives/when-a-metric-mix-up-led-to-the-gimli-glider-emergency-1.4754039)
- **Medicine** (search snippets only).
  - The Joint Commission "Do Not Use" list bans "U, u (unit)" because it "can be mistaken for '0' (zero), the number '4' (four) or 'cc'." — [Joint Commission](https://www.jointcommission.org/en-us/knowledge-library/support-center/standards-interpretation/do-not-use-list-of-abbreviations)
  - Verbal orders must be recorded and **read back**. For abbreviations, the recipient should "transcribe and read back the meaning of the abbreviation, not the abbreviation." — [ISMP 2017](https://www.ismp.org/sites/default/files/attachments/2018-03/20170518.pdf); [Joint Commission](https://www.jointcommission.org/en-us/knowledge-library/support-center/standards-interpretation/do-not-use-list-of-abbreviations)
- **Typed agent communication languages (pre-LLM)** (search snippet of the spec page).
  - The FIPA ACL Message Structure Specification (SC00061G) makes *performative* mandatory and provides **language** and **ontology** parameters so the receiver knows how to interpret content: "the ontology parameter is used in conjunction with the language parameter to support the interpretation of the content expression."
  - Relation: precedent for C3/C4. Classical ACLs put "which vocabulary/convention" in the message envelope. — [FIPA SC00061G](https://www.fipa.org/specs/fipa00061/SC00061G.html)
- **A2A protocol (current industry standard), opened.**
  - The AgentCard is "A JSON metadata document published by an A2A Server, describing its identity, capabilities, skills, service endpoint, and authentication requirements."
  - Parts are TextPart, FilePart and DataPart; DataPart is "a structured data blob (i.e. JSON)."
  - Tasks can enter `TASK_STATE_INPUT_REQUIRED` so an agent can "request additional input mid-processing." `acceptedOutputModes` negotiates media types.
  - The fetched (truncated) spec showed no unit or locale typing. An extensions mechanism exists.
  - Relation: L4's C4 (agent-card metadata) is realistic. A2A has a native clarification state (input-required) that L4 could use for "ask" behavior. — [A2A spec](https://a2a-protocol.org/latest/specification/)
- **Protocol surveys.**
  - Ehtesham, Singh, Gupta, Kumar, arXiv 2505.02279: MCP offers "typed data exchange" over JSON-RPC, and "A2A enables peer-to-peer task delegation using capability-based Agent Cards." — [arXiv](https://arxiv.org/abs/2505.02279)
  - Yang, Chai, Song, Qi, Wen, Li et al., "A Survey of AI Agent Protocols," arXiv 2504.16736. — [arXiv](https://arxiv.org/abs/2504.16736)

### Inferences
- Mapping to L4:
  - The ICAO/FSF SOP "announce all digits and the unit" = C2.
  - The NASA SIS = C3/C4.
  - Read-back/hearback = a missing C6. In C6 the receiver restates the value *in its own canonical, unit-explicit form* ("transferring 1,234.50 EUR, i.e., one thousand two hundred thirty-four euros fifty"), and the sender confirms or corrects.
- The Joint Commission rule (read back the *meaning*, not the abbreviation) is the key design detail. An echo of the bare string ("1.234") detects nothing; only an *interpreted* echo exposes the mismatch.
- The MCO lesson predicts L4's typed-channel result. Typing reduces silent errors only to the degree it is enforced. L4 should distinguish "declared unit field" from "validated unit field" (schema validation that rejects or flags a mismatch against the receiver's expectation).
- Aviation's dual check (the sender broadcasts the unit *and* the receiver reads back) suggests that the accuracy-vs-safety trade-off L4 observes is an artifact of using only one of the two checks.

### Gaps
- The Doc 4444 §4.5.7.5 list of items that must be read back (levels, headings, speeds, QNH, etc.) was not verified from the document; only its citation in IP/06 was.
- Found no quantitative human study of read-back effectiveness (e.g., error-catch rates) in this pass.
- Gimli Glider and Joint Commission details rely on search snippets rather than opened primary documents.

---

## (e) Positioning or reframing L4 as a stronger theme-track paper: novelty threats, reframing options, borrowed experiments

### Takeaway
The current framing ("we compare channel designs; explicitness trades accuracy against safety") is crowded:
- 2607.09678 compares nearly identical NL, precision-NL and JSON formats;
- ICR (2610.01042) already argues that richer messages amplify help and harm, and that structured verification shifts toward preservation;
- CAPRI owns "explicit prompting fixes units."

L4's defensible core is **faithful transmission followed by pragmatic misdecoding under a hidden convention gap**, which none of these test. The strongest reframes add a *mechanism* (read-back/hearback; negotiated or learned protocol; a pragmatic RSA-style receiver) or a *forms-of-communication* breadth arm (latent channel), and they evaluate with decision-level metrics.

### Cited Findings
- Channel-format overlap: 2607.09678 uses free NL, precision-instructed NL, JSON, triples and key-value; errors "propagate faithfully" in every format. — [arXiv](https://arxiv.org/abs/2607.09678)
- Trade-off overlap: ICR reports "richer messages amplify beneficial and harmful influence alike" and that structured verification moves "toward greater preservation and lower correction." — [arXiv](https://arxiv.org/abs/2610.01042)
- Explicit-prompting overlap: CAPRI's models "fail to utilize the information... unless explicitly prompted." — [arXiv](https://arxiv.org/abs/2606.17688)
- Metadata-loss overlap: Facts Without Rules, where boundary metadata collapses while facts survive and explicit constraints fix it. — [arXiv](https://arxiv.org/abs/2608.29028)
- Structured-protocol fix precedent: HiddenBench. — [arXiv](https://arxiv.org/abs/2505.11556)
- Hybrid NL+confidence precedent: ReConcile. — [arXiv](https://arxiv.org/abs/2309.13007)
- Mechanism precedents accepted at ACL venues: CoMet (ACL 2025 SAC Highlight), Interlat (ACL 2026). — [ACL 2025 awards](https://2025.aclweb.org/program/awards/); [Anthology](https://aclanthology.org/2026.acl-long.1248/)
- The theme's relevance rule requires communication to be "a substantive research question, computational mechanism, or source of capability." — [NAACL 2027 CFP](https://2027.naacl.org/calls/main_conference_papers/)

### Inferences

#### Novelty threats (ranked)
1. **Zeng 2607.09678, "Faithful, Not Corrective."** Almost the same C1/C2/C3 manipulation (free NL / precision-instructed NL / JSON) in agent relays.
   - Differentiator to state up front: their facts are self-contained, so fidelity equals correctness. L4's quantities are *convention-dependent*, so a perfectly faithful copy is still wrong. L4 measures receiver *decisions* (ask vs act), not recall.
   - Cite it as showing that transmission is not the bottleneck for strong models.
2. **Li et al. 2610.01042, ICR audit.** The claim that channel richness amplifies help and harm and that receiver policy matters pre-empts L4's trade-off as a *general* claim.
   - Differentiator: L4 has ground-truth convention labels, an invisible-ambiguity design, and the specific harm of confident action. Adopt ICR's conditional metrics and no-message control instead of competing with them.
3. **Miao et al. 2606.17688, CAPRI.** "Explicit sequential prompting fixes unit adaptation."
   - Differentiator: agent-to-agent, two locales, a clarification/safety measure, and the finding that explicitness *backfires* on safety. CAPRI has no such finding.
4. **Wang et al. 2608.29028, Facts Without Rules.** Same "value survives, frame dropped" structure, and explicitness fixes it.
   - Differentiator: L4's frame is never written down because it is an implicit default, while theirs is present and then lost.
5. **VanderHoeven et al. 2607.11053 (Gricean flouting under epistemic asymmetry)** and **Yao et al. 2605.01750 (dynamic grounding failures).** These threaten a pure "pragmatics of agents" pitch. L4 should cite both and differentiate on invisible, convention-level ambiguity.
6. **HiddenBench 2505.11556** and **TalkHier 2502.11098.** "Structured protocol improves collective reasoning" pre-empts any claim that structure helps. L4's contribution is the *cost side* (accuracy loss, false confidence).
7. **Low threat but must cite:** Shaikh 2311.09144 (frame); ReConcile 2309.13007 (C5 precedent); Agora 2410.11905 (hybrid/negotiated precedent); MAST 2503.13657 (taxonomy slot).

#### Reframing options for the theme track
- **R1. "Read-back closes the explicitness–safety trade-off" (mechanism; topics: efficiency & reliability, modelling partners).**
  - Claim: unit statements (C2) and typed fields (C3) are *one-sided* fixes that trade accuracy against safety. A receiver-side **interpreted read-back** plus sender hearback (ICAO Annex 11 3.7.3; the Joint Commission "read back the meaning") recovers both.
  - Evidence needed:
    - (i) a C6 read-back channel that beats C1–C5 on silent-error rate *and* accuracy, at a reported token/turn cost;
    - (ii) hearback catch rate (the share of mismatches the sender detects);
    - (iii) an ablation: verbatim echo vs interpreted echo, predicting that the verbatim echo catches nothing;
    - (iv) robustness across 2–3 model families and the ~30-convention expansion.
  - Strength: a concrete computational mechanism with deep human precedent; directly answers "plateau."
- **R2. "Unit omission is a pragmatic (Quantity) failure: sender explicitness vs receiver inference vs negotiated common ground" (topics: modelling partners, learning to communicate).**
  - Claim: frame C1 as presumptive grounding (Shaikh) and C2's backfire as certainty-marking (Zhou et al. 2023). Introduce a normative RSA-style receiver that models the sender's locale prior, and test when asking is optimal.
  - Evidence needed:
    - (i) a fitted or normative listener model that predicts which items receivers should query;
    - (ii) correlation of model ask-rates with posterior uncertainty;
    - (iii) a hedged-explicit condition ("amount 1.234 — I believe this is in EUR, please confirm") showing whether hedging restores asking;
    - (iv) ideally a small human–human or human–LLM dyad baseline (cf. Jones et al. 2602.08208; Kouwenhoven et al. 2503.04395).
  - Strength: a linguistics-grounded story that clearly separates L4 from CAPRI's "cultural knowledge" framing.
- **R3. "Learning when to be explicit: training senders and receivers to ground conventions" (topics: learning to communicate, efficiency).**
  - Claim: prompting fixes overshoot (always-explicit is verbose and suppresses checking). A small model trained with an Optima/ACT-style reward (task success − λ·silent error − μ·tokens + bonus for questions that resolve a real ambiguity) learns *selective* explicitness.
  - Evidence needed:
    - (i) a trained 4B sender/receiver (the repo already has 4B training infrastructure) beating the best prompted channel on held-out conventions and locales;
    - (ii) a Pareto plot of accuracy vs silent-error vs tokens;
    - (iii) Lowe-style causal evidence that the receiver uses the learned signals.
  - Strength: turns communication into a "source of capability." Risk: compute and time before the 2026-10-12 deadline (5 days); more realistic for a later cycle.
- **R4. "Do richer channels carry conventions? NL vs typed vs latent under a convention gap" (topics: forms of communication, evaluation).**
  - Claim: latent channels (C2C/KVComm/LatentMAS) promise lossless transfer, but conventions that were never encoded cannot be transferred. Test whether a latent channel carries the sender's locale context better than bare NL.
  - Evidence needed:
    - (i) a latent arm on two open-weight models (sender locale context in the prompt; receiver decodes);
    - (ii) the same metrics as above;
    - (iii) a probe (logit/J-lens as in Silent Dissent 2610.02702) of whether the receiver internally represents the sender's unit.
  - Strength: hits the theme's "NL vs structured/latent/symbolic/hybrid" topic squarely. A negative result would fit with Wenzel 2607.14103. Risk: engineering effort; works with open models only.

#### Experiment ideas borrowed from this literature
1. **Interpreted read-back/hearback (ICAO; Joint Commission).** Receiver restates the value in canonical, unit-explicit form before acting; sender confirms or corrects. Arms: no read-back / verbatim echo / interpreted echo / interpreted echo with sender hearback. Metrics: silent error, catch rate, extra turns and tokens.
2. **Declared vs validated type (NASA MCO SIS lesson).** C3 with a validator that compares the declared unit with the receiver's expected unit and raises `input-required` (A2A `TASK_STATE_INPUT_REQUIRED`) on mismatch, vs C3 without validation.
3. **Negotiated protocol (Agora; runtime schema negotiation per 2606.19135).** Before delegation, agents exchange and agree a short protocol document (currency, decimal and thousands separators, date order, units). Compare with static agent-card metadata (C4). Measure the amortized cost over N delegations.
4. **ICR-style revision audit (2610.01042).** Fix sender messages; vary channel × receiver policy (act / verify / ask). Report correction and preservation conditional on convention match vs mismatch, plus a no-message control.
5. **Hedged explicitness (Zhou et al. 2023; 2401.06730).** C2 with certainty vs uncertainty markers on the unit statement, to test whether the "confident action" effect is a certainty-marker effect. Also calibrate C5's confidence channel (ECE; accuracy among confident responses).
6. **Repeated interaction and convention formation (Hua & Artzi 2024/2025; Jones et al. 2026).** Multi-episode dyads with feedback after errors: do agents converge on explicit units, and does convergence transfer to new quantities?
7. **Causal use of the unit field (Lowe et al. 2019; Jaques et al.).** Counterfactually flip or remove the unit field and measure the change in receiver action, separating positive signaling from positive listening.
8. **Latent vs NL arm (C2C 2510.03215 / KVComm 2510.03346 / LatentMAS 2511.20639)** on Qwen-class models, with **internal probing** (Silent Dissent J-lens 2610.02702) of whether misdecoding receivers represent the alternative unit.
9. **Hidden-disagreement probe (Illusion of Alignment 2608.08210).** After delegation, ask sender and receiver the same diagnostic question ("in what currency is the amount?"). Divergence = hidden convention gap. This gives a cheap detector to evaluate alongside read-back.
10. **Aptitude vs unreliability decomposition (Laban et al. 2505.06120).** Separate "can decode when told the convention" (aptitude) from variance or failure to ask (unreliability) for each channel.

### Gaps
- The novelty check covers papers indexed by 2026-10-07. ICR (2610.01042) and Silent Dissent (2610.02702) appeared in the last week, so further same-week preprints may exist.
- Whether the NAACL 2027 theme reviewers will weigh "mechanism" over "analysis" cannot be determined from public material. The inference rests on 2025–2026 award and highlight patterns only.
