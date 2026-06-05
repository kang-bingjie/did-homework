# Prompt Cards

这些 prompt 用于现场演示。建议逐张打开，不要一次性把所有任务交给 AI。

## 1. 项目体检

风险等级：低

```text
请先阅读这个项目的 README、scripts、notebooks/digital_stata_did.ipynb、notebooks/digital_matlab_model.ipynb、notebooks/research_memo.ipynb 和 paper/main.tex。请不要修改文件。
告诉我：运行顺序是什么？每一步应该生成什么输出？有哪些潜在失败点？
```

## 2. 数据诊断

风险等级：低

```text
请检查 data/raw/digital_transformation_firm_panel.csv 的变量、缺失值和企业面板结构。
输出一段简短诊断：企业数、年份数、处理组数量、是否存在重复 firm_id-year。
```

## 3. 修复分析脚本

风险等级：中

```text
请检查 scripts/analyze_did.py 是否能从 data/raw/digital_transformation_firm_panel.csv 生成 output/python_did_results.csv、output/digital_parallel_trends.png 和 output/demo_summary.md。
如果不能，只做最小修改。修改后运行脚本并汇报验证结果。
```

## 4. Stata-MCP / fallback

风险等级：中

```text
请用 Stata 跑一个 DID 回归：log_tfp 对 digital，加入 firm_id 和 year 固定效应，标准误聚类到 firm_id。
同时输出事前平行趋势事件研究和 2018 年虚假处理的安慰剂检验。如果 Stata-MCP 不可用，请检查 scripts/run_stata_did.do 是否能作为 fallback 脚本。
```

## 5. Matlab-MCP / fallback

风险等级：低

```text
请检查 scripts/matlab_power_simulation.m 的输出逻辑。它应生成 output/matlab_theory_estimates.csv、output/matlab_productivity_surface.csv 和 output/matlab_theory_model.png。
如果 Matlab-MCP 不可用，只说明手动运行方式，不要修改系统配置。
```

## 6. 结果段落

风险等级：高

```text
请根据 output/stata_did_results.csv、output/stata_placebo_results.csv、output/digital_event_study.png 和 output/matlab_theory_estimates.csv 改写 notebooks/research_memo.ipynb 中的结果段落。
要求：说明数据是合成的，不能推出真实企业数字化转型结论；不要虚构文献；保留 DID 估计对象、聚类标准误、平行趋势和安慰剂检验说明。
```

## 7. LaTeX 正式写作

风险等级：高

```text
请把 notebook 中的结果段落改写成论文风格的 LaTeX 小节，放入 paper/main.tex 的 Result Summary 部分。
要求：保留模型设定、聚类标准误说明、平行趋势/安慰剂检验、Matlab 理论机制和合成数据限制；不要虚构文献；不要改变估计对象。
```

## 8. 审计日志

风险等级：低

```text
请根据本次修改更新 audit-log.md。每条记录包括：工具、任务、接受的输出、拒绝或修改的输出、验证方式。
```

## 9. 双语经济学论文写作

风险等级：高

```text
请基于当前 demo-project 的 notebooks、output 和 paper 文件，完成一套“数字化转型与企业生产率”的经济学论文写作示范。请先阅读 README.md、notebooks/digital_stata_did.ipynb、notebooks/digital_matlab_model.ipynb、notebooks/research_memo.ipynb、output/stata_did_results.csv、output/stata_event_study.csv、output/stata_placebo_results.csv、output/matlab_theory_estimates.csv、output/matlab_productivity_surface.csv、output/digital_parallel_trends.png、output/stata_event_study_ci.png、output/matlab_theory_model.png、paper/main.tex 和 audit-log.md。

任务目标：分别创建或更新 paper/main_zh.tex 和 paper/main_en.tex，生成中文论文版式和英文论文版式。两篇论文都必须包含标题页、摘要、关键词、引言、文献综述、数据与变量、实证策略、主要结果、动态效应与识别检查、安慰剂检验、理论机制、讨论与局限、结论、参考文献、AI 写作与复现审计附录。

必须使用 output 中的真实数值：DID 主估计 digital 对 log_tfp 的系数约 0.1209，企业层面聚类标准误约 0.0047；placebo_digital_2018 系数约 0.0015，p 值约 0.835；事件研究中处理前相对年份 -4、-3、-2 的系数接近 0，处理后系数逐步上升；Matlab 理论模型中 phi_hat 约 0.8659，平均模型收益约 0.1209，AI 采用率约 0.8197。

中文论文使用适合中文编译的 LaTeX 方案，例如 ctexart；英文论文使用标准 article 论文版式。两篇论文都要插入并解释 output/digital_parallel_trends.png、output/stata_event_study_ci.png 或 output/digital_event_study.png、output/matlab_theory_model.png。

请创建或更新 paper/references.bib。所有引用必须经过核查，不得虚构文献。优先使用 DOI、Crossref、期刊官网、出版社页面或本地文献库核查作者、年份、标题、期刊和 DOI。无法核查的文献不要引用，只能在正文注释中标记 citation needed after verification。

请确保 LaTeX 编译正确。从 demo-project 根目录运行：latexmk -xelatex -outdir=paper -interaction=nonstopmode -halt-on-error paper/main_zh.tex；latexmk -xelatex -outdir=paper -interaction=nonstopmode -halt-on-error paper/main_en.tex。若编译失败，请根据 log 修复，直到生成 paper/main_zh.pdf 和 paper/main_en.pdf。

请更新 audit-log.md，记录本次 AI 写作和复现审计：输入材料、接受的输出、拒绝或修改的输出、关键写作决策摘要、文献核查方式、LaTeX 编译命令和结果、研究者判断。不要记录或要求暴露隐藏 chain-of-thought，只记录可审计的写作过程、决策摘要、验证证据和人工判断。

写作边界：本项目使用合成数据，所有文字必须明确说明结果只用于展示研究工作流，不能解释为真实企业数字化转型的因果证据；不得改变估计对象；必须保留企业固定效应、年份固定效应、控制变量和企业层面聚类标准误的说明；平行趋势和安慰剂检验只是识别诊断，不是识别假设的证明；Matlab 理论模型只能作为机制示范，不能声称已经结构估计真实企业行为。

完成后汇报新增或修改文件、两个 PDF 是否成功生成、使用了哪些 output 数值、引用了哪些已核查文献、audit-log.md 中新增了什么记录，以及仍需人工确认的限制。
```

## Bad Prompt vs Better Prompt

### Bad

```text
帮我做一下 DID 分析。
```

### Better

```text
请用 data/raw/digital_transformation_firm_panel.csv 估计 log_tfp ~ digital + firm FE + year FE，标准误聚类到 firm_id。
请输出 stata_did_results.csv、事件研究和平行趋势图，并解释这是合成数据演示，不能当作真实企业数字化转型结论。
```
