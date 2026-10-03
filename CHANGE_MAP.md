# Change map — PS2 revision

> 本文件是完整的回应清单（R1–R17）。论文 Appendix D 只保留四种反馈来源的留空栏位（课堂反馈、同学评审、
> Han Zhang 讨论、我们提交的评审），**不再逐条收录**张老师 PS1 正式评审的 R1–R8；那八条的完整回应记在
> 本文件里（下表 R1–R8），随时可核对。
> 来源分组：R1–R8 张老师 PS1 正式评审 · R9–R10 课堂反馈 · R11–R13 peer reviewers · R14–R15 Han Zhang ·
> R16–R17 你们自己写的两份评审（个人工作）。

Reviewer point → author response → changed artifact → remaining limitation.
Status tags: `done` · `in progress` · `planned`.

| # | Source | Point raised | Decision and reason | Change made | Evidence (file / section) | Remaining limitation | Status |
|---|---|---|---|---|---|---|---|
| R1 | Prof. Luyao Zhang, formal PS1 review (2026-09-25) | Put a legible strategic representation in the paper itself; the README must show the same representation. | Accepted — the model is a normal-form 2×2, so the matrix belongs in the paper and in the README. | Table 1 (four decisions, payoffs, private/social ranks); same matrix added to `README.md`. | `README.md`, PS2 §2 Table 1 | none | done |
| R2 | Prof. Luyao Zhang, formal PS1 review | State the game type precisely (static/dynamic, simultaneous/sequential, complete/incomplete vs imperfect information). | Accepted, adapted — the PS2 model has no hidden action, so it is static, simultaneous-move, complete information. | One sentence in §2 states timing and information structure explicitly. | PS2 §2; `README.md` | none | in progress |
| R3 | Prof. Luyao Zhang, formal PS1 review | Use the solution concept implied by the structure; show strategies and deviation checks. | Accepted — dominant strategies and Nash equilibrium for a static 2×2. | Dominant strategy at k = 0 and the equilibrium cell per rule; deviation check in `verify_k.py`. | `verify_k.py`; PS2 §2 | SPNE/PBE only if the release decision becomes sequential | in progress |
| R4 | Prof. Luyao Zhang, formal PS1 review | Computational verification must match the model (course-tool benchmark, not a generic tutorial). | Accepted, partly planned — the symbolic and zero-dependency checks are model-aligned; a course-tool benchmark was missing. | Planned: `benchmark_nashpy.py` rebuilding the same four payoffs as a normal form (dominance, pure and mixed equilibrium) with saved output. | `benchmark_nashpy.py` (planned); `k_formula.ipynb`; `verify_k.py` | self-contained all-pay auction solver | planned |
| R5 | Prof. Luyao Zhang, formal PS1 review | Innovation Studio evidence: record benchmark, literature boundary, overturning condition, limitation. | Accepted as planned — relevant module: Auction Design (all-pay auctions), plus Static Games for the 2×2. | Planned: run the Studio module and export the result with a short reflection. | Appendix C of PS2 (planned) | not yet run | planned |
| R6 | Prof. Luyao Zhang, formal PS1 review | Release traceability: cite the exact tested commit; expose inputs, parameters, seeds, code, saved outputs, checks, dependencies, one reproduction entry point. | Accepted — the reported table must be reproducible from the paper alone. | Appendix A lists the level constants; README lists setup, dependencies, run order, parameters, expected output and the exact commit; all artifacts cite the same repository and commit. | PS2 Appendices A–B; `code/distill_sim.py`; `code/fresh_run_output.txt`; `README.md` | pinned `requirements.txt` | in progress |
| R7 | Prof. Luyao Zhang, formal PS1 review | The GitHub release must be the team repository inside the course organization, cited by organization URL plus commit. | Accepted — PS1 pointed at a personal fork; PS2 uses the organization repository with member work merged by pull request. | Canonical release: `https://github.com/dku-comsci-econ206-Autumn2026/PS2-FP4-CapabilityTransfer`, cited with its exact commit everywhere. | repository URL + commit in `README.md`, PS2 PDF, notebook, Space | none | in progress |
| R8 | Prof. Luyao Zhang, formal PS1 review | Visual/release gates: R4, body ≥10 pt, labels ≥9 pt, references 7.5–8 pt; one semantic palette with hex codes; vector export; grayscale and colour-vision-deficiency check. | Accepted — manuscript re-laid out for R4 at the required type sizes. | R4 layout with required point sizes; single palette defined once and documented; vector figures. | PS2 PDF (R4); `main.tex` palette block | grayscale / CVD check | in progress |
| R9 | Prof. Luyao Zhang, in-class feedback (date: TBD) | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** |
| R10 | Prof. Luyao Zhang, in-class feedback | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** |
| R11 | Student peer reviewer **[FILL: full name]** | **[FILL: comment]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** |
| R12 | Student peer reviewer **[FILL: full name]** | **[FILL: comment]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** |
| R13 | Student peer reviewer **[FILL: full name]** | **[FILL: comment]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** |
| R14 | Han Zhang (Liberata; Duke Ph.D. candidate) | **[FILL: comment, e.g. the market-share point]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** |
| R15 | Han Zhang (Liberata; Duke Ph.D. candidate) | **[FILL: comment]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** | **[FILL]** |

## How to fill a row

1. **Point raised** — one sentence, as close to the original wording as possible.
2. **Decision and reason** — accept / adapt / decline, plus why.
3. **Change made** — what actually changed in the model, argument, code, figure, interface or interpretation. If nothing has changed yet, write `Planned:` and say what will change.
4. **Evidence** — the exact location: PS2 PDF page + section, repository file + commit, Space link if relevant.
5. **Remaining limitation** — what still needs testing, tagged `planned`.
