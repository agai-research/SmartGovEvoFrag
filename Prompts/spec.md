# HyFragComp — Full Prototype, Dataset, Baselines, Experiments and Colab Notebooks

> Attachments: `HyFragComp.tex` (paper), `tikz.tex` (TikZ figures), `DATASET_SCHEMA.md` and `HyFragComp_BREADY_BE_Dataset_v2_JSON_CSV.zip` (seed dataset), `ZMethod1.pdf` (Bucchiarone et al., context-aware fragment composition), `ZMethod2.pdf` (Lu et al., case-based reasoning with semantic + graph-structural similarity).
> Read PART 0 first: it lists what the attachments contain, the gaps you must close, and the inconsistencies to resolve without asking.

---

## PART 0 — Role, objective and how to read the attachments

**Role.** Act as a senior researcher, an expert in python programming, LARGE LANGUAGE MODELS, retrieval augmented generation, GraphRAG, GNNs, hypergraph neural networks, scientific visualization, AllSet framework encoder, workflow management (BPMN, workflow nets) and service computing, Google Colab and research-oriented GitHub repositories.

**Study the sources deeply.**
1. Deeply analyze and understand the HyFragComp approach described in `HyFragComp.tex`: problem formulation (Definitions 1–8, Eqs. for freshness, difference Δ, objective, lifting, match score, alignment, promotion benefit, utility), the AllSet-based structural encoder (Eqs. for PMA_T / MLP_E / PMA_H / PMA_O / MLP_V, dual embedding), Algorithm 1 (reuse planning), Algorithm 2 (anchored delta recomposition), Algorithm 3 (cascading invalidation), frequency-gated promotion, privacy/explanation measures, the smart-governance scenario and the experimental specification.
2. Analyze the TikZ figures in `tikz.tex`, because they provide additional information about the implemented architecture, processing pipeline, components, data structures, interactions, and algorithms. In particular:
   - Figure "hypergraph before/after update": entry fragment F1 → AND-hyperedge e1 → {F2, F3, F4} → XOR-hyperedge e2 → variant group {F5, F7} → terminal F6; after a regulatory update a new fragment (biometric enrollment) is inserted between document collection and the XOR merge, and the memory layer promotes {F2,F3,F4} into composite C1 linked by a dashed derivation hyperedge d1. This is the unit test for insertion + promotion + derivation.
   - Commented "pipeline" figure (stages 1–8): Input request → Abstraction (c_cur, PII masking) → Decomposition (c_int, c_pln → goal hypergraph A⁺(P)) → Structural encoding (AllSet: z^G(g), z^G(P)) → Similarity search (ANN recall with q = e_T ⊕ z^G(P)) → Sub-goal alignment (Hungarian, threshold θ_m) → Formal re-validation (V1–V5) → three branches per sub-goal: REUSE / SWITCH (variant guard γ true, sibling substituted) / RECOMPOSE (delta GraphRAG) → composed workflow W* and explanation X(W*). It also shows the memory/knowledge space K⁺: HNSW vector indexes Z_G (sub-goals) and Z (fragments), fragment hypergraph H, ephemeral tier C_e.
   - Commented "architecture" figure: request path, reuse path and lifecycle path (frequency sketch → promotion gate; change monitor → cascading invalidation) around the shared space K⁺; audit log; model layer M (one LLM, eight role configurations).
   - AllSet figure: tail-set aggregation → two-way messages (PMA_H to heads, PMA_O to tails) → node update repeated L times → outputs z^str(F_i) = W h^(L), fused into Z; same encoder for sub-goals into Z_G.
3. Use `ZMethod1.pdf` and `ZMethod2.pdf` to implement the two external baselines completely (details in PART 7).
4. Use `DATASET_SCHEMA.md` and the zip to build the dataset (PART 5).

**The primary objective is: "Implement a complete prototype of the approach defined in the attached file."** The implemented HyFragComp prototype must take advantage of various tools, libraries, and other related technologies you judge necessary to cover HyFragComp functionalities as described in the Experimental validation section. The implementation must cover all the steps in the approach, strictly respect the approach's steps (minor improvements on equations, parameters, etc. are allowed), and implement all the algorithms. Do not replace the scientific approach with a different architecture simply because another implementation would be easier. Do not replace the models or mechanisms used in the original approach; do not include other mechanisms or novel models; use the formulation in the paper and apply minor adjustments if and only if necessary.

**Gaps and inconsistencies in the sources — resolve them yourself, without major changes, and record each resolution only in `implementation report.docx`:**

| # | Issue found in the sources | Resolution to apply |
|---|---|---|
| G1 | Section `\ref{sec:prototype}` is empty in `HyFragComp.tex` (its content sits in `implementation-gmail.tex`, not attached). | Write `Implementation.tex` from scratch, from the code you actually built (PART 9). |
| G2 | The base-framework beam score η(f \| Ω, G) is cited but never defined. | Define η explicitly (coverage gain over G^Δ, dual-embedding similarity to the sub-goal, compatibility margin, normalized cost), with its weights in the config; document it in `Implementation.tex`. |
| G3 | Cost terms c_cmp, c_reu, c_rev, the observed update rate λ_f and the threshold u_eager ("to be calibrated") are undefined. | c_cmp / c_reu / c_rev: measured cost counters (LLM tokens and latency for composing; predicate evaluations and latency for reusing and re-verifying), expressed in one normalized cost unit. λ_f: exponentially weighted observed update rate per fragment. u_eager: calibrated as a percentile (config, default 0.75) of Utility(y) over promoted composites on a validation stream; never a literal constant in code. |
| G4 | Table `tab:parameters` lost its Greek symbols; it cites Eq. 14/15 that do not exist (the match score and alignment are Eq. `eq:match`, `eq:align`). | Reconstruct: m→θ_m, reuse-ratio threshold→ρ_min, K_a, k, k_u, R→R_max, h, B_w, repair rounds→ε_max, W_s, e→τ_e, u_eager, (λ1,λ2,λ3). Also add the parameters the paper uses but the table omits: fusion weight α, encoder depth L / dimensions, ANN per-sub-goal budget K, similarity floor θ_sim, η weights, HNSW parameters. |
| G5 | The scenario is internally inconsistent (see PART 6): ρ is 3/5 in the text and 4/5 elsewhere; "four of five sub-goals matched above θ_m" contradicts the score 0.71 < 0.75; record c_s vs c_17 differ in φ; F4 appears in R without a covering sub-goal; the variant switch is attributed to (V2) although guard evaluation is not one of V1–V5. | Use the corrected scenario of PART 6. Evaluate the guard γ as part of (V4) (guard/role/temporal compatibility) and document it. |
| G6 | `tikz.tex` names the new biometric fragment F8, which collides with F8 "Company-name reservation" of the full repository figure; it also ends the residence lane at F6 while the full figure continues F6 → F14; it uses `\subfigure[...]{}` (package `subfigure`) while the paper loads `subcaption`. | Rename the new fragment (e.g., F18) in the repository and tests; in any LaTeX you write, use the `subfigure` *environment* of `subcaption`. |
| G7 | Experiment E4/E9 uses 4 reuse-ratio buckets, but every figure needs ≥ 5 x-axis values. | Use 5 buckets: [3–4], [5–6], [7–9], [10–13], [14–18]. |
| G8 | The paper's Hungarian remark assumes q ≤ 10, while experiments use \|G\| up to 18. | Keep the exact Hungarian solver (still negligible cost at q = 18); report alignment latency. |
| G9 | Instruction text mentions "smart educational datasets"; the paper's domain is smart governance. | Use smart-governance / public-administration knowledge wherever data must be completed. |
| G10 | The paper says "eleven experiments in nine series"; figure labels are e1–e10 and table e11. | Use the mapping of PART 8. |
| G11 | Retrieval, matching and checks are deterministic; c_ret appears in the role list but in no reuse-path stage. | Configure c_ret as a role; invoke it only for query reformulation in the scratch (base) pipeline; the reuse path makes zero c_ret calls. |

---

## PART 1 — Deliverables and repository layout

All the generated files (python scripts, json files, ipynb, docx, md, tex, figures, logs) must be downloaded as a single zip file (`HyFragComp.zip`), and the entire implementation must be organized using folders and sub-folders and saved in a root folder called **`HyFragComp`**. Organize the python files and scripts into subfolders: `HyFragComp`, `Data`, `Test`, etc. Use meaningful and short names for the different files; avoid long names. Suggested layout (you may rename, add or organize files):

```
HyFragComp/
├── README.md                     # description, figure of the whole approach, environment, configuration guide
├── HyFragComp.py                 # (i) runs the prototype on a request (CLI + importable)
├── hypergraph.py                 # (ii) builds the fragment hypergraph from the dataset
├── main-exp.py                   # (iii) builds experiment instances and dispatches experiment scripts
├── requirements.txt, environment.md
├── configs/                      # yaml: default.yaml (Table of parameters), one override file per experiment
├── Prompts/prompts.json          # multiple realistic test requests (PART 6)
├── HyFragComp/                   # prototype package (no experiment code inside)
│   ├── roles.py llm.py           # one LLM, eight role configurations, backends
│   ├── model.py                  # fragment, hyperedge, goal hypergraph, record dataclasses
│   ├── allset.py train_enc.py    # structural encoder + offline training
│   ├── index.py                  # HNSW indexes Z, Z_G with metadata filters
│   ├── request.py                # curator / interpreter / planner, template, goal hypergraph
│   ├── graphrag.py               # vector + structural retrieval, hyperedge expansion, ranking, context assembly
│   ├── match.py reuse.py         # alignment (Hungarian), difference Δ, V1–V5, variant switch, reuse plan
│   ├── delta.py verify.py        # anchored beam recomposition, C1–C5, soundness, repair
│   ├── memory.py promote.py      # ephemeral tier, count-min sketch, regions, lifting, promotion
│   ├── invalid.py explain.py     # cascading invalidation, witnesses, privacy
│   └── viz.py                    # BPMN-style workflow drawing
├── Baselines/                    # scratch.py whole.py cbr.py cafc.py (+ shared interface)
├── Data/                         # build scripts, raw/, derived/, instances/ (json)
├── Exp/                          # one script per experiment: e1.py … e11.py, oracle.py, plots.py, stats.py
├── Test/                         # first_test.py (dedicated graph + user queries), unit tests
├── results/                      # raw/, agg/, figs/, tables/, logs/
├── notebooks/                    # Colab notebooks (PART 10)
└── docs/                         # Implementation.tex, Results.tex, Dataset.tex, Dataset.docx, implementation report.docx, figures
```

The implementation must be structured as a set of python files, as well as other file formats (yaml, json, md, tex, docx, ipynb). A main file must be defined to call the rest of the scripts. Create different main files: (i) `HyFragComp.py` to run the prototype; (ii) `hypergraph.py` that constructs the graphs by accessing the dataset and eventually calling other python files or libraries; (iii) `main-exp.py`, the main file that constructs the different instances needed in the experiments and dispatches the experiment scripts; feel free to rename, add or organize these files. The implementation must allow accessing the datasets and processing the data (e.g., the hypergraph construction script has direct access to the dataset); for the graph construction and other data structures use the necessary python libraries, and populate the graphs from the datasets used in the approach.

Rules for the layout:
- Do not mix the prototype implementation with the experiments' scripts.
- Avoid wrong paths to the different files (e.g., when accessing a .json file or when calling a python file): resolve every path from the project root with `pathlib`; add a path self-check at start-up.
- `main-exp.py` and the other hyphenated entry points are executed as scripts; keep importable modules underscore-free and short.
- Do not neglect execution logs: structured JSON-lines logs per run (request id, stage timings, decisions, rejected candidates with the failed check, LLM role calls with tokens and latency, witnesses).

---

## PART 2 — Coding and file-content rules

- The python scripts, json files, ipynb, docx and md files must not contain needless text (e.g., guidelines, reasons for not using a tool). That text belongs only in a separate file `implementation report.docx` that summarizes the faced issues (problem invoking a tool, problem transforming or extracting data, parameter adjustments, scenario corrections, analytic fallbacks, etc.).
- The code (variable names, function names) must look humanized; all generated code must be minimal and error-free.
- Add short human-like comments in each python script to allow others to understand the code and execution logic. Comments only illustrate key implementation steps. Never write comments such as "We chose this because…", "This implementation is simpler…", "The paper was ambiguous…", "We could not use library X…", "This is a workaround…". Such explanations belong in `implementation report.docx`.
- The source code must be free of syntax errors and must be verified and correctly executed (run `python -m py_compile` on every file, run the test suite, run every experiment script at least in a smoke profile). No placeholders (below).
- Do not hardcode hyperparameters: every parameter comes from `configs/*.yaml` or the CLI; a experiment script reads its sweep values from its config.
- Use the verbs "build", "create", "construct" instead of "generate" in code, files and docs.
- Avoid long file names. Use consistent naming for methods in code, results and figures: `ours`, `whole`, `scratch`, `cbr`, `cafc`.

### NO PLACEHOLDERS
The following are explicitly prohibited: `return random.random()`, `return 0.8`, `return True`; hardcoded final workflow; hardcoded experimental ranking; hardcoded metric values; dummy embeddings; dummy GraphRAG; dummy AllSet; dummy LLM output; empty baseline implementations; incomplete plots; artificial performance improvements. Do not replace an algorithm with a simple random function, constant value, hardcoded result, or superficial placeholder. Do not provide generic, simplistic or superficial implementations. Randomness is allowed only to construct data and to initialize/train models, always through seeded generators.

---

## PART 3 — Prototype specification (component by component)

The implementation must respect the following, taken from the paper and figures. Items marked *(config)* are parameters.

### 3.1 One LLM, eight role configurations
- The paper specifies one underlying LLM specialized through role configurations (prompts + decoding settings), not separate models. Preserve this principle. Implement the role configurations for: `c_int` interpreter, `c_pln` planner, `c_ret` retriever (where applicable, G11), `c_sel` selector, `c_com` composer, `c_ver` verifier, `c_exp` explainer, `c_cur` curator. These are configurations/prompts for the same underlying LLM, not unrelated independent models, unless the implementation environment absolutely requires a documented fallback.
- One `LLM` object with swappable backends: (a) local open instruction model through `transformers` (4-bit quantization or vLLM when a GPU exists; a small instruct model on CPU otherwise), (b) hosted API selected through environment variables. All roles share the loaded model; a role = system prompt + output JSON schema + decoding settings *(config)* (e.g., temperature 0 for `c_ver`, `c_sel`, `c_int`, `c_pln`).
- The LLM components must actually be callable: first inspect the execution environment (GPU, network allowlist, installed packages), choose the backend, and run a start-up self-test that calls every role once. Outputs are parsed against JSON schemas with bounded retries; every retry counts as an LLM call.
- Call policy (defaults, *(config)*): `c_cur` 1 per request; `c_int` 1; `c_pln` 1; `c_sel` 1 per sub-goal in G^Δ; `c_com` 1 per delta recomposition; `c_ver` 1 per repair round (the checks themselves are deterministic and decide acceptance); `c_exp` 1; `c_cur` also verbalizes each promoted composite. Retrieval, matching, compatibility checks, validity checks and dependency traversal are deterministic computations, never LLM calls.
- Count and log LLM calls, input/output tokens and latency per role.

### 3.2 Data model
- Smart workflow fragment `f = (id, δ, B=(T_f,C_f), pre, post, σ=(I_f,O_f), rol, θ, τ)` with type τ ∈ {ENT, INT, TER, VAR}; extended with validity window ν = [ν⁻, ν⁺), revision counter rev, kind κ ∈ {atm, cmp}, support set supp for composites, level ℓ(f). Pre/post are sets of typed atoms (with a small subsumption hierarchy) so that entailment ⊨ is decidable by closure; signatures are typed data items; roles are role sets; θ holds statutory delays/deadlines as interval constraints.
- Directed hypergraph `H = (F, E, π)` with hyperedge `e = (tail, head)`, pattern π ∈ {SEQ, AND, XOR, LOOP} plus DER (derivation hyperedges form a DAG and never enable execution). XOR carries a guard γ(e) evaluated on the context; LOOP carries a guard and a bounded iteration limit. Enabling condition of f: OR over hyperedges with f in head of AND over tail completion. Composition outside a rule is forbidden. Library: `networkx` for graph algorithms plus a dedicated `Hypergraph` class (incidence matrices as `scipy.sparse`).
- Substitutability `f' ⊑ f`: pre(f) ⊨ pre(f'), post(f') ⊨ post(f), I_{f'} ⊆ I_f, O_f ⊆ O_{f'}, rol(f) ⊆ rol(f'), θ(f) ⊨ θ(f'), f' inherits hyperedges.
- Goal hypergraph `A⁺(P) = (G, E_G, π_G)` with E_G = {(pred(g), {g})}, π_G = SEQ if |pred| = 1 else AND; each sub-goal carries an end state ω(g) and typed slots s(g). Template `T = α(P̂)` replaces literal slot values by their types and contains no identifier, name, date or amount.
- Composition record `c = (T_c, W_c, φ_c, ς_c, ν_c, n_c, U_c, ttl_c, scope_c)` as a materialized view; freshness predicate `fresh(c,t) ⇔ t ∈ ν_c ∧ ∀f ∈ F_c: f_t ⊑ f_{ς_c(f)}` (and the licensing hyperedges still exist with the same pattern and guard).

### 3.3 Structural encoder (AllSet) — a real neural encoder
- Implement an actual neural structural encoder (AllSet) rather than a placeholder; if you need more details on AllSet ask me to attach the PDF of this encoder. Implement in PyTorch (optionally `torch_geometric`/scatter utilities): PMA (attention pooling with learned seeds, Set-Transformer style), pattern embeddings ε_π, and the layer equations of the paper exactly: `m_e = PMA_T({h_u : u ∈ tail(e)})`, `h_e = MLP_E([m_e ‖ ε_π(e)])`, `a_v = PMA_H({h_e : v ∈ head(e)})`, `b_v = PMA_O({h_e : v ∈ tail(e)})`, `h_v^(l+1) = LN(h_v^(l) + MLP_V([a_v ‖ b_v]))`; separate parameters for PMA_H and PMA_O; h^(0) = Sentence-BERT-style embedding of the description δ(v) (or of the sub-goal text); z^str(v) = W h^(L); dual embedding `z(f) = normalize(α z^sem ⊕ (1−α) z^str)` after projecting both parts to the same dimension; prompt-level vector `z^G(P) = PMA_G({h_g^(L)})`.
- One shared encoder for fragment hypergraph and goal hypergraphs. Variable-size tail/head sets are handled with padding masks or segment softmax.
- Offline training by masked hyperedge completion with an InfoNCE loss (mask a tail or head member, recover it against in-batch and hard negatives); train/validation split by hyperedges; no test request leaks into training; checkpoint and loss curve saved. Inductive use: a promoted composite is encoded by one forward pass over its neighborhood, without retraining.
- Report sanity metrics (hit@k of masked completion) in the logs; the encoder must be demonstrably trained before any experiment uses it.

### 3.4 Memory and indexes
- Two HNSW indexes (`hnswlib` or `faiss`): `Z` for fragments (including composites), `Z_G` for sub-goal patterns of every record and promoted composite with a pointer to φ_c(g). Every query carries metadata filters: t ∈ ν, scope, tier, status (implement as a filter callback or an over-fetch + exact filter that is verified to return K results when they exist).
- Ephemeral tier `C_e`: bounded capacity, TTL τ_e on the simulated clock, hit counter refresh, requester set U_c, record shared only when |U_c| ≥ k_u. Permanent tier = composite fragments and their DER/lifted hyperedges in H.
- Simulated clock: every request has `(P, D, t, u)`; validity windows, regulatory dates, TTL and ticks use this clock, not wall-clock.

### 3.5 Request path
`c_cur.Abstract` → template T (with a deterministic PII detector that rejects a template still containing personal literals) → `c_int` (clarified prompt P̂) → `c_pln.Decompose` → `LiftPlan` to A⁺(P) with ω(g), slots and hyperedges → AllSet encode → q = e_T ⊕ z^G(P).

### 3.6 GraphRAG (Algorithm 2, lines 5–6, and Section "Reuse-aware composition approach")
GraphRAG must be implemented as a real retrieval process. It must combine: vector/semantic retrieval; structural retrieval; hypergraph traversal; neighborhood expansion; compatibility filtering; candidate ranking; workflow-oriented context assembly. The implementation must not merely retrieve text chunks. The GraphRAG process must operate on the fragment hypergraph and respect the hyperedge semantics:
1. ANN over `Z` with the dual embedding (semantic + AllSet structural) under filters t ∈ ν(f), status = valid → seed set S (budget K).
2. `Expand(S, H, h)`: backward to tails, forward to heads and tail completion up to depth h; AND needs the whole tail, XOR selects the head member by guard γ(e) on the context, LOOP re-enables only while the guard holds, DER edges are traversed for provenance only. Keep only hyperedges whose tail is contained in the current fragments and touches the frontier ∂Ω (anchored retrieval).
3. Compatibility filtering with χ_fun (post entails pre), χ_dat (data available), χ_rol (role transition authorized), χ_tmp (temporal constraints jointly satisfiable), implemented as separate predicate functions with evaluation counters.
4. Ranking by η.
5. Context assembly: serialize the surviving candidate sub-hypergraph (fragments with pre/post/roles, hyperedges with pattern and guard, anchor/frontier, rejections with reason) into the context handed to `c_sel` / `c_com`.

### 3.7 Matching, difference and re-validation (Algorithm 1)
- Recall: ANN on `Z_G` with q, filters t ∈ ν_c, scope ∈ {u, shared}, status = valid, budget K_a.
- Alignment: m(g,g') = λ1 cos(e_g, e_g') + λ2 cos(z^G(g), z^G(g')) + λ3·1_slot(g,g') with Σλ = 1; ψ* by the exact Hungarian method (`scipy.optimize.linear_sum_assignment`): maximize the sum of scores where scores below θ_m are zeroed, then drop zero-score pairs. Anchor record c* = argmax s(c) with s(c) = Σm/|G|; unmatched sub-goals are looked up individually in `Z_G` and may come from other records.
- Difference Δ = (G⁼, G⁺, G⁻, E⁺, E⁻) computed in O(|E_G|) by hyperedge mapping (same pattern required for E⁼); reuse ratio ρ = |G⁼|/|G|.
- Per matched sub-goal in ≺-order, checks (V1) validity, (V2) freshness (substitutable revision + licensing hyperedges persist), (V3) entailment (post(R_g) ⊨ ω(g); pre(R_g) ⊆ ctx(P̂) ∪ post(R^{<g})), (V4) compatibility (χ_rol, χ_tmp between R_g and R^{<g}; plus guard consistency), (V5) scope. On failure try **variant switch**: if a member of a variant group has guard false and a sibling with guard true exists under the same XOR hyperedge, substitute and re-check; otherwise add g to G^Δ and record the failed check.
- Mode: full if G^Δ = ∅ ∧ E⁺ = E⁻ = ∅; partial if ρ ≥ ρ_min; scratch otherwise (R = ∅, G^Δ = G, ξ = ∅). Junctions J between R and the rest; witnesses ξ.

### 3.8 Delta recomposition with incremental verification (Algorithm 2)
- Beam of partial compositions Ω starting from Ω₀ = (R, C_c|_R); pick the ≺-minimal uncovered sub-goal; GraphRAG candidates; XOR guard selection; extend only if all four χ hold for every tail member; record rejections; keep top-B_w by η (gain computed over G^Δ only); stop on full coverage or beam exhaustion (FAIL → scratch fallback).
- Incremental verification: only junctions and new connections are checked for (C3)/(C4) (count predicate evaluations: 4·|C^Δ| vs 4·|C|); (C5) soundness on the unfolding where each retained region is abstracted to its verified body; up to ε_max repair rounds with `c_ver.Repair` (bridge a missing rule, add synchronization), re-checked deterministically each round.

### 3.9 Feasibility checks (C1–C5)
(C1) coverage of every sub-goal; (C2) connectivity from a unique entry; (C3) pairwise compatibility of every connection; (C4) conformance of every connection to a composition rule; (C5) soundness of the workflow-net unfolding (option to complete, proper completion, no dead transitions). Implement the unfolding (AND = synchronizing transition, XOR = exclusive choice per guard, LOOP = bounded re-entry, SEQ = place chain) and the soundness test with `pm4py`'s workflow-net tools when installable, otherwise an own reachability/coverability procedure on the bounded net.

### 3.10 Two-tier memory: frequency-gated promotion
- Every verified composition → record in `C_e`; a hit refreshes it, increments n_c and adds the requester to U_c.
- Admissible region: connected, convex, hyperedge-closed, 2 ≤ |R| ≤ R_max; candidate regions grown greedily from frontier fragments (O(|F(W*)|·R_max) candidates per composition); signature s(R) = canonical hash of sorted fragment ids and typed hyperedges.
- Frequency by a **count-min sketch** (implement it; counters halved every W_s requests) and distinct requesters |U_s|. Promote when `n̂(s) ≥ k ∧ |U_s| ≥ k_u ∧ B(R) > 0`, with `B(R) = n̂(s)(c_cmp(R) − c_reu(R)) − Σ_{f∈R} λ_f c_rev(R)`.
- Lifting: pre(f_R) = ∪pre − internal post; post, rol, signatures, `ν(f_R) = ∩ν(f)`, supp(f_R) = R; add DER hyperedge d = (R, {f_R}) and lifted incoming/outgoing hyperedges of the same pattern; keep original hyperedges; verbalize with `c_cur`; encode with one AllSet forward pass; insert into `H`, `Z`, and `Z_G`.

### 3.11 Cascading invalidation (Algorithm 3)
Events: `update(f→f')`, `withdraw(f)`, `regulation(Φ_reg, t*)`, `tick(t)` (priority queue Q_ν by ν⁺, `heapq`). Substitutable update → rebind stamps and recompute windows only. Otherwise BFS backward over DER hyperedges to collect dependents D(f); mark suspect by increasing level ℓ; eager `Revalidate` when `Utility(y) = n̂(s(y))(c_cmp − c_reu) ≥ u_eager`, lazy at next access otherwise; records in `C_e` are marked suspect through their stamps. `Revalidate`: windows, χ on connections incident to the changed members, soundness; on failure targeted repair by Algorithm 2; on failure eviction (fragment, DER and lifted hyperedges, index entries) which cascades. Count predicate evaluations per event.

### 3.12 Explanation and privacy
- `c_exp` produces a symbolic, human-readable explanation X(W*); each sub-goal carries a witness: pseudonymous record id, the three components of the match score, status (reuse / switch / new), validity evidence (t, ν), stamps, junction witnesses, memory tier, failed-check reason.
- Privacy: template abstraction + PII detector; private-until-|U_c| ≥ k_u; shared records hold only fragment identifiers and typed slots; shared and private hits follow the same code path with latency padding as an option *(config)*; the padding is switched off in the experiments that report latency and switched on in a dedicated unit test that verifies equalization.

### 3.13 Final composition and visualization
- The final composition must be represented explicitly (JSON): ordered workflow elements; fragment identifiers; hyperedge relationships (pattern, tail, head); conditions/guards where applicable; inputs/outputs; reused elements; newly composed elements; switched elements; junctions; verification status (C1–C5 each, soundness, repair rounds); witnesses.
- The final workflow/application composition must be produced from the appropriate inputs (never hardcoded) and visualized as a BPMN-style scheme (start/end events, task boxes colored reused / switched / new, AND "+" and XOR "×" gateways, loop marker, guards on gateway outgoing flows) or at least a clear directed process graph. Export PNG and SVG (Graphviz when available, `matplotlib` fallback). Also visualize the goal hypergraph and the alignment (reuse/switch/new per sub-goal), as in the paper's partial-reuse example.

### 3.14 Run interface and output
`HyFragComp.py` takes as input the required data: a fragment hypergraph file (JSON), a request file or inline text (`prompt, context, time, requester`), the config, and the memory state; it returns a clear output in the terminal and in an output file (JSON + a short Markdown report + the BPMN figure): mode, ρ, per-sub-goal decisions, LLM calls and latency per stage, verification status, explanation. Use the appropriate format for the user query and the graph to run the prototype correctly (`Prompts/prompts.json`, `Data/instances/*.json`).

If the implementation logic of the approach risks to affect the approach's behavior and good performance, make some adjustment to preserve high performance and high solution quality of our approach compared to other methods. In case of an unrealistic step in an algorithm, you can apply a minor adjustment; no major modification is allowed.

---

## PART 4 — Parameters (Table `tab:parameters`, reconstructed)

Keep every value in `configs/default.yaml`; ranges drive the sensitivity sweeps. Feel free to adjust the settings of this table.

| Symbol | Description | Range | Default |
|---|---|---|---|
| θ_m | Sub-goal match threshold | [0.5, 0.95] | 0.75 |
| ρ_min | Reuse-ratio threshold for partial mode | [0.2, 0.8] | 0.5 |
| K_a | ANN candidate budget (recall) | [5, 50] | 10 |
| k | Promotion frequency threshold | [1, 10] | 3 |
| k_u | Requester-diversity threshold | [1, 10] | 3 |
| R_max | Maximum admissible region size | [2, 10] | 6 |
| h | Hyperedge expansion depth | [1, 4] | 2 |
| B_w | Beam width | [1, 20] | 5 |
| ε_max | Maximum repair rounds | [1, 5] | 3 |
| W_s | Count-min halving window (requests) | [100, 10000] | 1000 |
| τ_e | Ephemeral time-to-live (days) | [1, 30] | 7 |
| u_eager | Eager re-validation threshold | cost units | calibrated (G3) |
| λ1, λ2, λ3 | Match-score weights | [0, 1] each, Σ = 1 | 0.5, 0.3, 0.2 |
| α | Dual-embedding fusion weight | [0, 1] | chosen on a validation split |
| L, d | Encoder depth / hidden size | — | chosen on a validation split |
| K, θ_sim | ANN budget per sub-goal / similarity floor in Algorithm 2 | — | config |
| default \|F\| | Repository size (fragments incl. composites) | 100 … 50 000 | 1000 |

Tune only on a validation split of the data (never on the requests that produce the reported results) and give the baselines the same tuning budget.

---

## PART 5 — Dataset

Use the attached `HyFragComp_BREADY_BE_Dataset_v2_JSON_CSV.zip` and `DATASET_SCHEMA.md` as the seed: it is complete for what it contains — 50 economies, 18 services, 9 resources, 7 requirements, 5 constraints, 16 fragments, 17 hyperedges, 250 single-sentence requests, 150 reference composition records, 150 change scenarios, 2 200 relevance labels, and scale sets of 10–50 economies — and it keeps raw (B-READY scores), derived and synthetic parts separate with provenance. If the attached datasets are complete you can use them rather than creating new datasets; but they are **not sufficient for the experiments** (they lack pre/post-conditions, data signatures, roles, temporal constraints, guards, goal hypergraphs, requester populations, regulatory events, residence-permit procedures, multi-sub-goal requests of 3–18 goals, long prompts, repositories of up to tens of thousands of fragments, and update/staleness streams). Complete them as follows, keeping the canonical files unchanged and storing everything new as derived data with provenance tags (`source`, `derived`, `synthetic_controlled`).

The dataset needed in the implementation must be created from the public datasets mentioned in the paper (the World Bank B-READY 2024 Business Entry data in the zip is the public source for the company-creation lane). If necessary, construct the missing data to provide a complete data set for the experiments; if you are unable to extract data from datasets available online, you can construct all (or part) of the required data from your own knowledge of smart-governance procedures (residence permit, company creation), labeled as constructed.

Create the required Python scripts (in `Data/`) to: access available public datasets (local zip, plus download when the network allowlist permits); parse them; normalize them; transform them into the required format; construct service/fragment descriptions; construct workflow information; construct prompts; construct hypergraphs; construct composition records; create experiment-specific instances. Avoid terms like "generate"; say "build", "create" or "construct".

The dataset must cover all required information, including as appropriate: services; fragments; composite fragments; resources; descriptions; preconditions; postconditions; data signatures; roles; temporal constraints; hyperedges; guards; workflows; requests/prompts; goal hypergraphs; composition records; requester information; validity windows; revisions; regulatory events.

Do not add relations to the graph and the main dataset unless needed; limit the relations to those defined in the paper (SEQ, AND, XOR, LOOP, DER). Do not construct needless data that is not included in the experiments.

**Construction rules**
1. `Data/build_base.py`: from the zip build the base repository — map B-READY Business Entry services/fragments (F01–F16 of the zip) to the company-creation lane (name reservation, statutes/legal form, capital deposit, fee payment, commercial-register entry, tax-ID/social affiliation, with the loop on rejection) and construct the residence-permit lane of the paper's Figure (F1–F7, F14, C1, e1–e12, d1) plus the fragments the scenario needs (F2r renewal eligibility, F16 contract check, F17 work-permit check, the new regulatory fragment renamed per G6). Each fragment gets pre/post atoms, I/O signature, roles, temporal constraints, guard on variant groups, validity window and revision, with fields following `DATASET_SCHEMA.md` §6 plus the extensions.
2. QoS proxies and economy context come from the B-READY pillar scores (`economy_service_context.json`); keep provenance.
3. `Data/build_scale.py`: construct repositories of arbitrary size by controlled variant families (scope, revision, procedure variant) over a controlled vocabulary of actions × objects × qualifiers drawn from the B-READY taxonomy — descriptions must be meaningful text, so embeddings and ground-truth relevance come from the construction logic (family id, equivalence classes), never from any method's output.
4. `Data/build_requests.py`: requests with known sub-goal structure (|G| from 3 to 18), known paraphrase mapping to stored sub-goals (ground-truth alignment), controlled prompt-pair overlap (0–100 %), controlled word length (10–160 words with filler circumstances that do not add sub-goals), requester populations (|U| and Zipf-like recurrence), and timestamps.
5. `Data/build_events.py`: update/withdraw/regulation/tick streams with controlled update rates and staleness rates (fraction of fragments expired or revised non-substitutably: 0–75 %).
6. `Data/build_records.py`: composition records (ground-truth feasible compositions verified by the oracle) for pre-populating memory.
7. Instance builders (`Data/inst_*.py`, or one parametrized script) that cut the dataset into experiment-specific instances, saved as `.json` under `Data/instances/`, with parameters for: number of services; number of fragments; workflow sizes; graph densities (hyperedge-to-fragment ratio, tail/head sizes); thresholds; requester populations; update rates; staleness rates; overlap; prompt length; request volume. Save the main dataset and its instances (a part of the dataset specific to an experiment) in the form of `.json` files, plus a `manifest.json` with counts and checksums.
8. A validation script asserts schema validity, DAG-ness of DER edges, window consistency, and that ground truth is independent of method outputs.

**Prompts file** `Prompts/prompts.json`: multiple realistic test requests, each with requester pseudonym, timestamp, context D, and an `expected_branch` used only by the tests. Include: first residence-permit requests; renewal requests; priority requests; requests with additional sub-goals; company-creation requests; requests designed to trigger partial reuse; requests designed to trigger scratch composition; requests designed to trigger variant switching; requests designed to test stale fragments; requests designed to test regulatory changes. Do not merely vary one word: the prompts must exercise different branches of the HyFragComp pipeline (full, partial, scratch, switch, V1–V5 rejection of each type, scope rejection, composite attachment, promotion trigger, invalidation).

---

## PART 6 — Smart-governance scenario (reproduce explicitly, corrected)

The smart-governance scenario in the paper must be implemented explicitly: at minimum reproduce the paper's illustrative scenario, and correct it in case of inconsistencies. Use this corrected version as the reference test (qualitative outcomes are asserted; scores are computed by the code, never hardcoded — calibrate the *constructed repository*, not the algorithm, so the outcomes appear):

- **Repository:** the paper's hypergraph (14 fragments F1–F14, composite C1 with DER d1 on {F2,F3,F4}, hyperedges e1…e12), plus F2r, F16, F17 and the regulatory fragment (renamed, G6).
- **Stored record c_17** (first long-stay student permit): φ(g1)={F2}, φ(g2)={F3}, φ(g3)={F5,F4}, φ(g4)={F6}.
- **Request (21-09-2026):** renew a permit as a priority case, upload documents, validate a new employment contract, be notified by SMS. Five sub-goals: g^c_1 renewal eligibility, g^c_2 dossier documents, g^c_3 contract validation, g^c_4 priority appointment (with fee enabling), g^c_5 submission + SMS notice; e_a = ({g^c_1,g^c_2,g^c_3},{g^c_4}) and a SEQ edge to g^c_5.
- **Expected decisions:** g^c_2 ↔ g_2 reuse F3; g^c_5 ↔ g_4 reuse F6 with slot channel := SMS; g^c_4 ↔ g_3 re-validated, guard priority_status true → variant switch F5 → F7 (fee fragment F4 retained with it); g^c_1 aligns below θ_m and the composite C1 fails (V3) because pre(F2) requires that no valid permit is held; g^c_3 has no match. Retained: 3 of 5 → ρ = 3/5 ≥ ρ_min → mode partial; G^Δ = {g^c_1, g^c_3}. Algorithm 2 anchors on R = {F1, F3, F4, F6} (+F7): for g^c_1 candidates F2r and F2 → F2 rejected by χ_fun, F2r kept; for g^c_3 candidates F16 and F17 → F17 rejected by χ_rol, F16 kept; junction checks run only on the four connections touching F2r and F16.
- **Change events:** (i) finance act, fee schedule from 01-01-2027, F4′ ⊑ F4 → stamps and ν(C1) rebound, nothing invalidated; (ii) decree adds a mandatory document, F3′ with I_{F3′} ⊄ I_{F3} → not substitutable, D(F3) = {C1}, records containing F3 suspect; at next access (V) χ_dat fails on F3′ → e2, repair adds a bridging fragment (C1 gets a new revision); with no bridge C1 is evicted and requests fall back to e1–e2.
- Implement it as `Test/first_test.py` (below) and as a unit test with assertions on mode, ρ, G^Δ, switches, rejections and invalidation outcomes.

**First-test script.** Besides the scripts devoted to the experiments, create a distinct first-test script `Test/first_test.py` that allows me to test the prototype HyFragComp using a dedicated graph (the scenario repository) and a set of user queries (`Prompts/prompts.json`). It prints a clear terminal output per query (mode, ρ, decisions, calls, latency, verification, explanation), saves JSON results, and saves BPMN-style figures.

---

## PART 7 — Compared methods (five conditions, complete implementations)

All methods run on identical data, identical request streams, identical simulated clock, identical LLM backend and decoding settings, identical embedding models, identical oracle, and identical fallback rule: every method must return a workflow for every request; when its own mechanism fails it falls back to the shared scratch composer and the extra LLM calls are counted. Implement the baselines and methods for the experimental comparison. Do not provide generic, simple, or lightweight implementations of these methods; they must be complete and reach a sufficient level of detail, following `ZMethod1.pdf` and `ZMethod2.pdf`. Each baseline has a script file that is executable and free of errors, and a Colab notebook.

1. **`ours`** — full HyFragComp.
2. **`scratch`** — scratch-only: the base pipeline without memory: c_int, c_pln, c_ret (query reformulation), full GraphRAG over H for every sub-goal, c_sel, c_com, deterministic checks, c_ver repairs, c_exp. No reuse.
3. **`whole`** — whole-record reuse only (internal ablation): HyFragComp with delta recomposition (Algorithm 2) disabled: a request either reuses a matched record in full (still with V1–V5 so that the benefit isolated is granularity, not verification) or falls back to scratch composition; no sub-goal-level recombination. This isolates the benefit of reuse at sub-goal granularity (RQ1–RQ2) from the benefit of reuse at all.
4. **`nore` (re-validation disabled ablation, E1 only)** — HyFragComp without V1–V5 (and without variant switch checks): matched sub-goals are reused as aligned. Its results must differ from `ours` (verify; if identical, the experiment or implementation is wrong).
5. **`cbr` — Case-based composition (Lu et al., ZMethod2)**: a knowledge-graph case-based reasoning method that retrieves and recommends a whole composed case by a weighted fusion of semantic (DeBERTa, TF-IDF, SimHash) and graph-structural (maximum common subgraph) similarity, with no sub-goal decomposition, no formal re-validation, and no notion of staleness. Implement completely:
   - Case knowledge graph: case nodes, attribute entities, inter-case relations as triples (id, study area/economy, service type, parameters, capabilities, inputs, outputs, examples, name, description, code, weight, tags), four-layer ontology (semantic concept → logical service feature → atomic functional mechanism → property); store in `networkx` (a Neo4j backend is optional); here a case = a composition record, with its workflow as the case graph.
   - Query processing in the paper's dual path: (i) structured conversion of the request into a triple-form query graph, (ii) semantic parsing to keywords and text features; import the query graph into the case graph.
   - Semantic similarity: `Sim_attr = β1·Sim_DeBERTa + β2·Sim_TF-IDF + β3·Sim_SimHash` — DeBERTa embeddings (e.g., `microsoft/deberta-v3-base`, mean pooling, cosine), TF-IDF with TF = n_ij/Σn_kj and IDF = log(|D|/|{j: t_i ∈ d_j}|) implemented or via scikit-learn, SimHash as a 64-bit fingerprint with Hamming-based similarity (implement it).
   - Structural similarity: maximum common (connected) subgraph `Sim(G1,G2) = 2|g| / (|G1|+|G2|)` with `g = mcs(G1,G2)` — implement an exact MCS (e.g., via the modular-product graph + maximum clique, or a McGregor-style backtracking with pruning) over nodes+edges; structural normalization of case graphs before matching.
   - Fusion: `Sim = α·Sim_attr + (1−α)·Sim_stru`, i.e. `Sim = αβ1·S_DeBERTa + αβ2·S_TF + αβ3·S_SimHash + (1−α)·S_MCS`. Weights by the **Analytic Hierarchy Process**: build the pairwise matrix over (S1 DeBERTa, S2 SimHash, S3 TF-IDF, S4 MCS) = [[1,3,5,7],[1/3,1,2,5],[1/5,1/2,1,3],[1/7,1/5,1/3,1]], column-normalize, row-sum, normalize to weights (paper: DeBERTa 0.57, SimHash 0.24, TF-IDF 0.13, MCS 0.06), compute λ_max (paper: 4.07809), CI = (λ_max − n)/(n−1) (0.02603), RI = 0.90, CR = CI/RI (0.0289 < 0.1) and assert the consistency test in code; derive α = sum of the three semantic weights and β_i by renormalization.
   - Similar-case identification threshold 0.8 (paper's ablation setting); recommend the case with highest fused similarity as the whole solution (adapted only by slot rebinding); no staleness check; below threshold → scratch fallback.
6. **`cafc` — Context-aware fragment composition (Bucchiarone et al., ZMethod1)**: an AI-planning-based framework that composes process fragments against an explicit context model and repairs a running composition when context preconditions are violated. Implement completely:
   - Fragments as deterministic labelled transition systems `f = ⟨S, s⁰, I, O, R⟩` with controllable (`!`) and uncontrollable (`?`) actions, built from each fragment's body (request/reply activities, abstract activities with goals).
   - Context properties `p = ⟨L, l⁰, E, T⟩` (state transition systems with events), context `C = {p1…pn}` with disjoint event sets; context formulas as disjunctions of conjunctions of states. Map the domain: permit status, priority_status, fee paid, documents complete, validity-window state and revision state of each fragment, regulatory status, etc.
   - Annotations `ω = ⟨P, E, G⟩` (precondition formula, effect event, goal formula) from the fragments' pre/post/ω (precondition ↔ pre, effect ↔ post event, goal ↔ end state of the abstract activity).
   - Grounding (Def. 7–8): replace event-labelled transitions by action-labelled transitions with guards; grounded context Σ_C as synchronous product; execution domain Σ_F as asynchronous product of fragments; context-aware execution domain Σ_CF; Domain Builder pruning of unreachable configurations and irrelevant fragments.
   - Planner: strong planning, backward fixpoint of the paper's Fig. 10 — `StrongPreImage` (controllable actions leading into S; uncontrollable actions with all outcomes in S), `PruneStates`, termination when initial states are covered or no new states appear; output the state-action table (consistent solution executor) and derive the executable process by forward analysis; translate to a workflow (hyperedge-conformant ordering).
   - Requirements: goal context formula built from the sub-goal end states ω(g); the sub-goal decomposition itself comes from the shared `c_int`/`c_pln` calls (counted).
   - Change handling: when an exogenous event violates a context precondition (fragment expired/revised/withdrawn, regulatory status change), repair by re-running the Adaptation Manager pipeline (Domain Builder → Translator → Planner → Translator) on the updated context to refine/replace the broken abstract activity; count transitions/predicates evaluated; if the planner fails (no fragment covers a goal) fall back to shared scratch composition (LLM).
   - It performs no memory reuse of past compositions and has no substitutability test, no derivation hypergraph and no promotion; it is the closest pre-LLM analogue of context-triggered repair (RQ4).

Every baseline reports the same measures through the same interface (`serve(request) → result` + `handle(event)`), so the same experiment script drives all methods. The results of the ablated variants must not be identical, and if it is the case repeat the experiments or adjust their implementation.

---

## PART 8 — Experiments

For each experiment write the necessary python scripts that allow parsing the corresponding dataset or data file. The experiments must be identical to those in the attached approach (`HyFragComp.tex`). Define a script for each test series or experiment (`Exp/e1.py` … `Exp/e11.py`); in this script the appropriate dataset or data file (instance of the main created dataset) is accessed to execute the script of the test case and record the results. The scripts must be strictly aligned with the approach and the paper content; use the exact numbers of objects (e.g., hyperedge size, number of fragments, etc.) and other hyper-parameters, as described in the experiments and the settings table. If necessary apply minor modifications on the parameters and variables used in the experiments. Do not mix the prototype implementation with the experiments' scripts.

### 8.1 Mapping to the paper (labels used in `Results.tex`)

| Exp. | Section label | Independent variable(s) (x-axis, ≥ 5 values) | Measures | Methods | Figure / table |
|---|---|---|---|---|---|
| E1 | `sec:revalidation` | staleness rate {0,10,25,50,75} % | incorrect-reuse rate, mean latency (ms) | `ours`, `nore` (+ `whole`, `cbr`, `cafc` where defined; `scratch` as zero-reuse reference) | `fig:e1` |
| E2 | `sec:cost-reduction` | reuse strategy (5 methods), \|F\| = 1000, θ_m = 0.75 | mean LLM calls / request, mean latency (ms) (+ tokens, calls per role) | all five | `fig:e2` |
| E3 | `sec:granularity` | prompt-pair overlap {0,20,40,60,80,100} % | reuse ratio ρ, # sub-goals recomposed from scratch | `ours` vs `whole` (+ others where defined) | `fig:e3` |
| E4 | `sec:complexity-sensitivity` | \|G\| ∈ {3,5,8,12,18} | alignment precision, recall, alignment latency (ms) | `ours` (+ `cbr` as whole-case alignment baseline, `whole`) | `fig:e4` |
| E9 | same section | sub-goal bucket {[3–4],[5–6],[7–9],[10–13],[14–18]} (G7) | distribution of ρ | `ours`, `whole` (+ others where defined) | `fig:e9` |
| E8 | `sec:request-length` | prompt length (words) {10,20,40,80,160} | # decomposed sub-goals \|G\|, planner-role decomposition latency | `ours` (shared planner role, + all methods' decomposition for comparison) | `fig:e8` |
| E5 | `sec:repository-growth` | requests served {100,500,1000,5000,10000} | % sub-goals covered by existing fragments vs new composition | all five | `fig:e5` |
| E7 | same section | \|F\| ∈ {100,500,1000,5000,10000,50000} (if 50 000 is infeasible use 20 000 and document it) | end-to-end latency, reuse ratio | all five | `fig:e7` |
| E6 | `sec:stage-latency` | pipeline stage (abstraction, structural encoding, recall+alignment, re-validation, delta recomposition, verification, explanation) × \|G\| ∈ {3,5,8,12,18} × mode {full, partial, scratch}; B_w = 5, ε_max = 3 | mean latency per stage (ms) | `ours` (+ stage subsets of the others where they exist) | `fig:e6` |
| E10 | `sec:workflow-correctness` | method × \|G\| ∈ {3,5,8,12,18}; ε_max = 3, θ_m = 0.75 | fraction of requests satisfying (C1)–(C5), mean repair rounds | all five | `fig:e10` |
| E11 | `sec:comparative-summary` | none (default configuration) | LLM calls, latency, ρ, correctness rate, invalidation cost (predicate evaluations per event) | all five | `tab:e11` |

Held parameters per series are as stated in the paper (e.g., E1: θ_m = 0.75, k = k_u = 3; E3: ρ_min = 0.5; E4: K_a = 10; E5/E7: k = k_u = 3, R_max = 6; E6: B_w = 5, ε_max = 3; E10: ε_max = 3). All experiments should be conducted for all the compared methods wherever the measure is defined for that method; where the paper specifies only internal conditions (E1, E3) keep them as the primary curves and add the other methods as extra curves when meaningful. The service-space-size sweep (|S| ∈ {100,250,500,1000,1500,2000}) given as the example structure below is not a separate series of the paper; use it only if a service-space experiment is added to the paper.

### 8.2 Experimental protocol
- Every experiment must be actually executed. For each experiment do all or part of the following operations: load the appropriate dataset instance; initialize the required method; run HyFragComp; run every baseline; run all required LLM calls; record execution statistics; repeat the complete experiment five times; calculate the mean; preserve raw results; save aggregated results; create figures; create tables; create logs.
- **ALL THE EXPERIMENTS MUST BE RUN 5 times and the average results are reported** (seeds 0–4, each run rebuilding stochastic instance parts, retraining nothing from the test split); report mean ± standard deviation and a 95 % confidence interval. The LLM calls or agents invocations and the runs for the different compared methods must all be run to generate the experimental results.
- The results of an executed test case or experiment must be saved in a dedicated file (e.g., json): `results/raw/<exp>/<method>/run_<i>.json` (all per-request records), `results/agg/<exp>.json` (mean, std, CI, n), `results/tables/<exp>_*.csv|.tex`, `results/figs/<exp>_*.png|.pdf`, `results/logs/<exp>_run<i>.log`.
- **Execution tiers** (so that long streams stay executable while every claim stays measured): (a) request sets of E2, E4, E6, E8, E10, E11 and the quality/correctness measures run with real LLM calls on every request; (b) for the long streams of E5/E7 (up to 10 000 requests and 50 000 fragments) all non-LLM computation (ANN, Hungarian, re-validation, beam search, soundness, promotion, invalidation) runs for real on every request, while LLM latency is taken from per-role latency/token models calibrated on measured calls from the same run (the calibration data and the "calibrated" flag are stored with the results). If an LLM/API/model cannot be executed, give near-to-reality analytic results based on the conventional behavior of the adopted technique, labeled `analytic` in every JSON/table/figure caption and in `implementation report.docx`, never presented as measured and never fabricated.
- **Oracle.** The judge of (C1)–(C5), incorrect reuse and alignment correctness is a separate `Exp/oracle.py` computed from the full hypergraph state at time t and from construction-time ground truth; no method grades itself.
- **Instrumentation:** wall-clock stage timers (`time.perf_counter`), LLM call counters per role, predicate-evaluation counters (χ_fun, χ_dat, χ_rol, χ_tmp, V1–V5, soundness steps) per request and per event, memory growth (records, composites, index sizes).
- **Integrity of the "HyFragComp must win" goal.** If the experimental results show that the main approach (HyFragComp) does not perform well and produce bad results, adjust its algorithms so they boost HyFragComp and return better measures compared to the rest of approaches; the ultimate goal is to prove that HyFragComp is the best among all compared methods, and this is an implementation priority. Permitted adjustments: minor changes inside the paper's formulation (η weights, α, λ_i, encoder size/training length, candidate budgets, cost-model constants, thresholds) selected on a validation split, with the same tuning budget granted to every baseline; fixing implementation defects; improving the instance construction when it is unrealistic. Not permitted: changing data/ground truth after seeing test results, hardcoding outcomes, weakening a baseline, or selecting seeds. If a metric still favors a baseline after legitimate tuning, keep the measured value and describe it in the interpretation text and in `implementation report.docx`.

### 8.2b Tuning protocol (how HyFragComp is boosted without bias)

Run this protocol before any reported experiment; it implements the "boost HyFragComp" priority above. Script: `Exp/tune.py`; outputs: `configs/tuned_<method>.yaml`, `results/tuning/<method>_trials.json`.

1. **Splits.** Build three disjoint request/instance splits from the same construction scripts: `train` (encoder training, record pre-population), `val` (all tuning and failure analysis), `test` (the reported experiments). Disjoint by request family and by construction seed; tuning seeds (100–104) differ from reporting seeds (0–4). A second, untouched `test2` split is kept in reserve for a final confirmation run.
2. **Objective.** Tune on `val` with a constrained objective: maximize the oracle correctness rate (C1–C5) first; among configurations within 1 point of the best correctness, minimize mean LLM calls, then latency; reuse ratio is reported, not optimized. The objective is identical for every method.
3. **Budget and method.** The same number of trials *(config, default 60)*, the same wall-clock cap and the same search algorithm (staged coordinate search over the groups below, then TPE/random search via `optuna` inside the best region) for every method, each on its own parameters. Every trial is logged (config, val metrics, seed, duration).
4. **Search space for `ours`** (ranges from PART 4; nothing outside the paper's mechanisms):
   - encoder: L, hidden size, α, number of negatives, hard-negative ratio, epochs, learning rate, temperature of InfoNCE;
   - matching: λ1–λ3 on the simplex, θ_m, ρ_min, K_a, per-sub-goal K, θ_sim;
   - recomposition: η weights, h, B_w, ε_max;
   - memory: k, k_u, R_max, W_s, τ_e, the u_eager percentile, cost-model constants for c_cmp / c_reu / c_rev, EWMA factor of λ_f;
   - role prompts shared by all methods (few-shot examples, JSON schema strictness, decoding settings), tuned once on `val` and then frozen for everyone, so no method gets better prompts than another;
   - HNSW M / efConstruction / efSearch (quality–latency trade-off).
5. **Search space for baselines.** `scratch`: K, h, B_w, η weights. `whole`: θ_m, K_a, V-check settings. `nore`: same as `ours` minus V1–V5. `cbr`: α, β_i, the 0.8 similarity threshold (AHP weights kept as the reference setting and compared against tuned ones), MCS size cap. `cafc`: pruning aggressiveness, context-property granularity, replanning scope.
6. **Failure-driven fixes.** After each tuning stage, analyze `val` failures per method: rejections by check (V1–V5, χ_*), misaligned sub-goals, rejected-but-correct candidates, soundness failures, LLM JSON-parse retries. Fix implementation defects and unrealistic instance construction found this way; any code change re-triggers tuning of every affected method so the comparison stays equal.
7. **Stopping rule.** Stop when the best val objective improves by less than 0.5 % over 15 consecutive trials, or the trial/wall-clock budget is spent, whichever is first.
8. **Freeze and lock.** Write the chosen configs with a SHA-256 hash and the commit/state of the code; the experiment scripts refuse to run on `test` if the hash does not match. The `test` split is unlocked once; results are never used to re-tune. If a final check on `test2` disagrees with `test`, report both.
9. **Reporting.** Include the tuned values, the trial counts per method, a sensitivity analysis (one-at-a-time sweeps around the optimum on `val`) and, in `implementation report.docx`, every metric where a baseline still leads after tuning.

### 8.3 Figures and tables
- For each experiment, create at least three types of COMPLETE figures to record the compared results. Each figure must be complete (legends, axis labels, units, error bars). Avoid placing captions within figures and limit this to subsections only, if needed. Text in the figures must be large and readable (≥ 14 pt tick labels, ≥ 16 pt axis labels). Avoid heatmap figures. In the experiments' figures, the number of values in the x-axis should be at least five.
- Do not create incomplete graphics: no figure with a missing plot or bar or legend entry — e.g. a figure comparing 4 approaches with curves has 4 curves, not 3 or 2. Enforce in `Exp/plots.py` an assertion that the plotted series equal the declared method list; keep one fixed color/marker/linestyle per method across all figures (colorblind-safe palette).
- Use different chart templates across experiments: multi-series line chart, stacked bar chart, grouped bar chart, line chart with confidence band, box/violin plot, CDF, scatter/bubble, radar. Suggested chart types: E1 line (incorrect-reuse), grouped bar (latency), stacked bar (outcomes: reused / switched / recomposed / rejected by V1–V5); E2 grouped bar (calls), bar with error bars (latency), stacked bar (calls per role), cumulative-cost line over the stream; E3 line (ρ), grouped bar (recomposed sub-goals), stacked bar (retained/switched/new); E4 line (precision/recall/F1), bar (latency); E9 box/violin and CDF of ρ per bucket; E8 line (|G| vs words), bar (latency), scatter (decomposed vs true |G|); E5 stacked bar (covered vs new), line (promoted composites over time); E7 log-scale line (latency), line (ρ); E6 stacked bars by stage per mode (2 × 3 layout); E10 line (correctness vs |G|), grouped bar (repair rounds), stacked bar (defect type C1–C5); E11 radar and bubble chart next to `tab:e11`.
- Use clear and readable colors for high-quality figures; use different layouts (2 × 2 four subfigures, 1 × 4 in one row, 2 × 3 six subfigures with three per row, a single figure …).
- Tables record complementary measures (not the same measures as the figures), with the same row/column structure as in `Results.tex`.
- Statistical significance (in `Exp/stats.py`): paired comparisons of `ours` against each baseline — per-request paired tests pooled over requests within each run plus run-level means (n = 5 runs; do not claim run-level Wilcoxon significance below its attainable p-value), effect sizes (Cohen's d), bootstrap confidence intervals; export a table.

---

## PART 9 — Written outputs

1. **`README.md`**: describes HyFragComp and its components, the implementation structure and organization, the execution environment for reproducibility (python version, packages, GPU/CPU, LLM backend, seeds, expected run times), the configuration guidelines (every parameter of PART 4, profiles `smoke` and `full`, how to run `HyFragComp.py`, `Test/first_test.py`, `main-exp.py --exp e1 … e11 --runs 5`, how to rebuild the dataset and instances) so other researchers can reuse or reproduce the implementation in a GitHub repository. Include a figure representing the whole approach (build it with a script from the pipeline/architecture of the paper; store PNG + SVG in `docs/`; optionally add a Mermaid diagram).
2. **`docs/Implementation.tex`**: contains only an adjusted and improved version of Section `\ref{sec:prototype}` (use `\label{sec:prototype}`; elsarticle style; subsections: environment and libraries, LLM layer and role configurations, structural encoder and training, indexes and memory, request path, GraphRAG, matching and re-validation, delta recomposition and verification, promotion and invalidation, explanation and privacy, visualization), written from the code actually built, with tables of parameters and the η definition (G2). Feel free to adjust this section if needed.
3. **`docs/Results.tex`**: follows the same structure as the subsection `\subsection{Results}` of `HyFragComp.tex` (one `\subsubsection` per series with the same titles and labels as PART 8.1; the description paragraphs currently in the experimental specification are kept and extended with the recorded results). After conducting all the experiments and recording the results, include them in tables and figures (python figures), followed by (i) a text (at least two consistent and complete paragraphs) describing the observed results, including approaches' names and examples of recorded values or comparisons; (ii) a text interpreting the results and justifying them by mentioning the approaches' execution logic. Use rich figures and tables with different layouts (`subcaption` environments). Template for each series, e.g. `\subsubsection{Impact of service-space size}`:

   ```latex
   \subsubsection{Impact of service-space size}
   \label{sec:service-space}
   This series assesses end-to-end scalability as the number of candidate services increases while preserving the same task distribution. To do so, we varied |S| ∈ {100, 250, 500, 1000, 1500, 2000}; |R|=500; η_g=30%; π_T=25%; workflow size=4 goals. The following measures are recorded in Table \ref{tab:....} and Figure \ref{fig:....}.
   \begin{figure*}[!t]
       \centering
       \includegraphics[width=\linewidth]{[Produced Figure].png}
   \caption{.......}
   \label{fig:....}
   \end{figure*}
   % [relevant tables recording complementary measures, not the same measures as in the figure]
   % [paragraph presenting the observed results: compared methods, some recorded values, performance order]
   % [paragraph interpreting the results: why an approach outperforms the others or performs badly]
   ```
   where `[Produced Figure].png` is the figure produced for the corresponding experiment after running the implemented methods.
4. **`docs/Dataset.docx` and `docs/Dataset.tex`**: a complete summary of the dataset information (number of services, resources, fragments, composites, hyperedges per pattern, requests, goal hypergraphs, records, events, per-instance sizes, provenance) and the recorded results as a set of tables having the same structure (lines and columns) as those of `Results.tex`.
5. **`implementation report.docx`**: the only place for the summary of the faced issues (tool invocation problems, data extraction/transformation problems, parameter adjustments, scenario corrections G1–G11, analytic fallbacks, environment limits, anything where a result favors a baseline).
6. Everything bundled in one `HyFragComp.zip`.

---

## PART 10 — Google Colab notebooks

Once generated, use all the created files (python file, dataset scripts, experiments scripts, etc.) to create multiple `.ipynb` (Google Colab Notebooks) files. These Colab notebooks will be used later to: (i) run the entire prototype on examples of inputs and data and in one click, (ii) run all the experiments and display their results in the form of python figures and in the form of tables (similar to the paper figures). Each notebook starts with a setup cell (unzip/clone the repository, `pip install -r requirements.txt`, GPU check, LLM backend selection through Colab secrets or environment variables, `smoke`/`full` profile switch). Feel free to follow or adjust these examples:
- `00_quickstart.ipynb`: one-click run of the prototype on the scenario and on `Prompts/prompts.json`, with the BPMN-style figures and explanations displayed.
- `01_data_report.ipynb`: detailed report on the constructed data, statistical significance, results interpretation and justification.
- `02_exp_all.ipynb` (and optionally one notebook per series): run an experiment on all the baseline methods, record results (including mean and standard deviation) in json, and display a direct python figure or table in the same notebook.
- One notebook for each baseline (`scratch`, `whole`, `cbr`, `cafc`) and one for `ours`.
- If needed, notebooks may include text cells for explainability. Execute each notebook end-to-end at least in the `smoke` profile (`jupyter nbconvert --execute`) before delivery.

---

## PART 11 — Delivery checklist (verify before finishing)

1. Every `.py` compiles; the unit tests and `Test/first_test.py` pass; each experiment script runs end-to-end in the `smoke` profile and then in the `full` profile with 5 runs.
2. A static check finds none of the prohibited patterns (constant returns, `random` in decision paths, hardcoded results, dummy encoders or LLM outputs) and no comments of the forbidden kind.
3. The AllSet encoder is trained (loss curve logged), the LLM start-up self-test calls all eight roles, GraphRAG runs the five stages, and the BPMN-style figure is produced from the composed workflow.
4. Results of `ours` and the ablations differ; each figure has the declared number of series and ≥ 5 x values; no heatmaps; ≥ 3 complete figures per experiment; the aggregated JSON exposes mean, std, CI and n = 5.
5. Paths and file names are valid from a fresh checkout; the README commands run as written.
6. `Implementation.tex`, `Results.tex`, `Dataset.tex/docx`, `implementation report.docx`, the notebooks and `HyFragComp.zip` are all present.
