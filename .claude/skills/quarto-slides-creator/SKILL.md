---
name: quarto-slides-creator
description: >
  Create new Quarto revealjs lecture slides or detailed lecture notes for the 经济与商务实证研究方法 (RMEB) course.
  Two modes: (1) slides mode — brainstorm → approve → generate slides → visual audit;
  (2) notes mode — expand existing slides into a comprehensive HTML lecture notes document with
  full derivations, code demos, visualizations, and extended case studies.
  Use this skill whenever the user wants to create a new lecture, build new slides, add a new week's
  content, or says "创建讲义", "新建lecture", "写slides", "做PPT", "create lecture", or any variant.
  Also triggers for "第N周" creation requests. For notes, triggers on "创建notes", "写notes",
  "详细讲义", "lecture notes", "创建讲义笔记", "补充讲义" or any variant.
  ALWAYS use this skill for new slide or notes creation — never create Quarto slides/notes from scratch without it.
argument-hint: "[Lecture topic or week number] [--notes]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
---
# Quarto Slides Creator

Create pedagogically excellent Quarto revealjs lecture slides — or detailed HTML lecture notes — for the 经济与商务实证研究方法 course.

**This is a collaborative process. The instructor drives the vision; Claude is a thinking partner.**

## Mode Selection

This skill operates in two modes. Determine the mode from the user's request:

| Mode                       | Trigger phrases                                                      | Output                                |
| -------------------------- | -------------------------------------------------------------------- | ------------------------------------- |
| **slides** (default) | "创建讲义", "写slides", "新建lecture", "第N周"                       | `WN_topic.qmd` (revealjs)           |
| **notes**            | "创建notes", "写notes", "详细讲义", "lecture notes",`--notes` flag | `WN_topic_notes.qmd` (HTML article) |

### Notes Mode Prerequisites (CRITICAL)

**NEVER create notes without an existing slides file.** Follow this decision tree:

1. Check if `2026Spring/LectureNotes/WN_*.qmd` (slides, NOT notes) exists
2. **If slides exist** → proceed to Notes Workflow (Phase N0–N4 below)
3. **If slides do NOT exist** → inform the user and ask:

   > "该讲的 slides 尚未创建。Notes 必须基于 slides 生成以确保内容一致。是否先创建 slides？"
   >

   - If user confirms → run the full Slides Workflow (Phase 0–5) first
   - After slides are created → **GATE: wait for user to review and approve slides**
   - Only after user approves slides → proceed to Notes Workflow

---

# SLIDES WORKFLOW

## CONSTRAINTS (Non-Negotiable)

1. **Read syllabus.qmd FIRST** — confirm topic, week number, and reading materials
2. **Read the previous lecture** to ensure continuity (review slide + preview alignment)
3. Motivation before formalism — real-world example or question before every definition
4. Worked example within 2 slides of every new concept
5. Max 2 colored boxes per slide (concept/example/warning)
6. No colons after box titles — write `**核心概念**` not `**核心概念：**`
7. Use *italics* (not **bold**) for emphasis inside colored boxes
8. Blank line after box title, blank line before every list
9. `. . .` (incremental reveal) needs blank lines ABOVE and BELOW
10. No --- to seperate slides if the next slides is started with  a new section #[title]
11. Code blocks always use `font-size: 1em` — never smaller
12. Chinese typography: full-width quotes ""''、，。！？ and half-width space between CJK and Latin
    - **中文双引号必须使用方向正确的：左侧 “(unicode U+201C))，右侧”（ unicode U+201D），严禁使用 ASCII 直引号 `""`**
    - 参考 `quarto-formatting` 技能的 Rule 2（英文文本用英文引号）和 Rule 3（中文引号方向必须正确）
13. Work in sections of 5-8 slides — share outline for feedback before bulk generation
14. All citations must be verifiable — no invented references
15. **PDF→PNG 图片转换**：使用 PyMuPDF (`fitz`) 以 ≥600 DPI 渲染，确保输出 PNG 像素宽度 ≥2000px。严禁使用 `sips` 仅修改 DPI 元数据而不增加实际像素
16. **图片尺寸**：**不要在 QMD 中设置 `width="85%"`**——Quarto 会生成内联 `style="width:85%"` 导致与 CSS `max-height` 冲突而破坏宽高比。由 `ruc-theme.scss` 通过 `max-width: 85%` + `max-height: 65vh` 统一控制
17. **图片语法**：slides 中 Mermaid PNG 须用 `:::{.intro-mermaid}` 包裹，notes 用 `![caption](path){#fig-label}`，均不加 width 属性
18. **Python 图片中文显示**：由于 slides 默认 `eval: true`，所有含 Python 图表且图表有中文标签的 slides 必须在 YAML header 之后、所有内容之前插入一个隐藏的 matplotlib 中文字体配置 setup cell（`#| echo: false` + `#| output: false`），配置 `plt.rcParams['font.sans-serif']` 等参数。否则中文标签将显示为空白方块
19. **Mermaid 图必须预渲染为 PNG**：不要在 QMD 中使用内联 Mermaid 代码块（`` ```{mermaid} ``），因为显示比例不可控。正确做法：将 `.mmd` 源文件渲染为 PNG 后以图片方式插入。完整流程见下方"Mermaid 图渲染规范"

---

## WORKFLOW

### Phase 0: Intake & Context

1. Read `syllabus.qmd` — locate the target week, topic, and assigned readings
2. Read the previous lecture's last slides (本讲要点 + 下节课预告) for continuity
3. Read `quarto-formatting/SKILL.md` for formatting rules (MANDATORY)
4. State the lecture topic, pedagogical goal, and key concepts to the user
5. **GATE: User confirms topic scope before proceeding**

### Phase 1: Content Research & Brainstorm

1. Identify core concepts from the syllabus reading materials
2. Search for classic empirical examples and case studies for the topic
3. Plan the narrative arc:
   - Opening: 上节课回顾 (review previous lecture)
   - Body: 3-4 major sections with section dividers
   - Closing: 本讲要点 + 下节课预告
4. Propose an outline with:
   - Section titles (will become `{background-color="#AE0B2A"}` dividers)
   - Key concepts per section
   - Empirical cases / applications
   - Where to place Python code demonstrations
   - Estimated slide count per section
5. **GATE: User approves outline before Phase 2**

### Phase 2: Generate Slides

Follow this structure precisely:

#### YAML Header (copy verbatim, update only title/subtitle/date)

```yaml
---
title: "经济与商务实证研究方法"
subtitle: "第N周：[TITLE]——[SUBTITLE]"
author: "陈志远"
institute: "中国人民大学商学院"
date: "YYYY-MM-DD"
format:
  revealjs:
    theme: [default, ruc-theme.scss]
    css: ruc-theme.scss
    slide-number: true
    progress: true
    code-fold: false
    code-tools: true
    highlight-style: github
    pdf-separate-fragments: false
    width: 1400
    height: 788
    margin: 0.05
    transition: slide
    background-transition: fade
    toc: true
    toc-depth: 1
    chalkboard:
      buttons: true
    preview-links: auto
    mermaid:
      theme: default
      flowchart:
        useMaxWidth: true
        htmlLabels: true
        nodeSpacing: 70
        rankSpacing: 90
        diagramPadding: 20
      themeCSS: |
        .label text,
        .nodeLabel,
        .edgeLabel,
        .edgeLabel p,
        .cluster-label text {
          font-size: 28px !important;
          font-family: "Source Han Sans SC", "Noto Sans CJK SC", "WenQuanYi Micro Hei", sans-serif !important;
          font-weight: 600 !important;
        }
      themeVariables:
        fontSize: 32px
        fontFamily: "Source Han Sans SC, Noto Sans CJK SC, WenQuanYi Micro Hei, sans-serif"
        fontWeight: 600
  beamer:
    pdf-engine: xelatex
    include-in-header:
      text: |
        \usepackage[UTF8]{ctex}
        \usetheme{Madrid}
        \usecolortheme{default}
execute:
  echo: true
  warning: false
  message: false
  eval: true
  cache: false
lang: zh
html-math-method: katex
---
```

#### Matplotlib Chinese Font Setup Cell (MANDATORY when Python figures contain Chinese labels)

Since slides default to `eval: true`, any slide deck containing Python code that generates figures with Chinese labels **MUST** have this hidden setup cell placed immediately after the YAML `---` closing line, before any slide content:

````markdown
```{python}
#| echo: false
#| output: false
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150

np.random.seed(42)
```
````

> **Why this is mandatory:** Without this setup cell, matplotlib defaults to a font that cannot render CJK characters, causing Chinese axis labels, titles, and legends to display as empty boxes (□□□). This cell sets the font fallback chain globally for all subsequent Python code cells in the document.

#### Mermaid 图渲染规范

**绝不在 QMD 中使用内联 Mermaid 代码块**（`` ```{mermaid} ``）。内联 Mermaid 在 RevealJS 中的显示比例不可控，经常出现溢出、字体渲染异常、或图表过小等问题。

**正确流程：**

1. **创建 `.mmd` 源文件**：保存到 `2026Spring/LectureNotes/diagrams/WN/` 目录
2. **使用 `mmdc` 渲染为 PNG**：

   ```bash
   mmdc -i diagram.mmd -o diagram.png -s 4 --backgroundColor white
   ```

   - `-s 4`：4 倍缩放，确保高分辨率
   - `--backgroundColor white`：白色背景，避免透明背景在浅色 slides 上显示异常
   - 渲染后检查：`sips -g pixelWidth diagram.png`，确保宽度 ≥ 2000px
3. **在 QMD 中以图片方式插入**：

   ```markdown
   :::{.intro-mermaid}
   ![](diagrams/W2/ai_tools_landscape.png){fig-align="center"}
   :::
   ```

   - **必须使用 `:::{.intro-mermaid}` 包裹**——该 CSS 类提供 `width: 100%`、`max-height: 78vh` 和居中对齐
   - **不加 `width` 属性**——由 `ruc-theme.scss` 的 CSS 统一控制尺寸
4. **验证**：Quarto render 后检查图片是否清晰、比例正确、无溢出

> **Why**: 内联 Mermaid 的渲染依赖浏览器端 JavaScript，字体大小、节点间距、子图比例均不可精确控制。预渲染为 PNG 后，图片作为静态资源加载，显示效果完全可预测。

#### Slide Structure Patterns

**Opening Review Slide:**

```markdown
## 上节课回顾

::: {.concept-box}
**核心概念**

- *关键概念1*：简要描述
- *关键概念2*：$formula$ 的含义
- *关键概念3*：方法要点
:::

. . .

*本节课目标*

- 目标1
- 目标2
- 目标3
```

**Section Divider:**

```markdown
# 节标题 {background-color="#AE0B2A"}
```

**Concept Introduction Slide:**

```markdown
## 概念标题

::: {.concept-box}
**概念名称**

概念的精确定义或核心思想。
:::

. . .

*直观理解*

- 用日常语言解释
- 类比或比喻
```

**Example/Case Study Slide:**

```markdown
## 案例标题

::: {.example-box}
**案例名称**

案例背景和研究设计要点。
:::

. . .

**结果**

关键发现的简述。
```

**Warning/Limitation Slide:**

```markdown
## 局限性标题

::: {.warning-box}
**警告要点**

需要注意的关键限制或陷阱。
:::

. . .

*实践建议*

- 应对方案1
- 应对方案2
```

**Python Code Slide:**

```markdown
## Python实现：标题

::: {style="font-size: 1em;"}
```{python}
#| echo: true
#| eval: true
#| output: true

import numpy as np
import pandas as pd
# ... code here ...
```

:::

```

**Comparison Table Slide:**
```markdown
## 比较标题

| 方法 | 核心假设 | 适用场景 |
|:---|:---|:---|
| *方法A* | 假设描述 | 场景描述 |
| *方法B* | 假设描述 | 场景描述 |
```

**Summary Slides (split into two if >5 items):**

```markdown
## 本讲要点（一）

::: {.concept-box}

1. *要点标题*
   - 子要点说明

2. *要点标题*
   - 子要点说明

:::

## 本讲要点（二）

::: {.concept-box}

3. *要点标题*
   - 子要点说明

4. *要点标题*
   - 子要点说明

:::
```

**Tool Recommendation Slide (side-by-side columns):**

```markdown
## 推荐工具

:::: {.columns}

::: {.column width="50%"}
::: {.callout-tip}
**Python**

- `package1`：用途
- `package2`：用途
:::
:::

::: {.column width="50%"}
::: {.callout-tip}
**R**

- `package1`：用途
- `package2`：用途
:::
:::

::::
```

**Next Lecture Preview:**

```markdown
## 下节课预告

**第N+1周：[TITLE]**

- 预告要点1
- 预告要点2
- 预告要点3

. . .

::: {.concept-box}
*核心思想*

一句话概括下节课的核心。
:::
```

**References Section:**

```markdown
# 参考文献

- Author1 (Year). Title. Journal, Volume(Issue), Pages.
- Author2 (Year). Title. Publisher.
```

#### Writing Guidelines

1. **Narrative flow**: Each section follows 动机 → 定义 → 直觉 → 公式 → 案例 → 局限
2. **Progressive reveal**: Use `. . .` to build arguments gradually
3. **Bilingual terms**: First mention includes English in parentheses, e.g., 双重差分法（Difference-in-Differences, DiD）
4. **Math notation**: Use KaTeX-compatible LaTeX; long formulas use `aligned` environment
5. **Diagrams**: Pre-render Mermaid to PNG, wrap in `:::{.intro-mermaid}` div. See "Mermaid 图渲染规范" for full syntax.
6. **Slide density**: Aim for 25-40 slides per lecture; each slide should make ONE point
7. **Box variety**: Alternate between concept-box (blue), example-box (gold), warning-box (red) — avoid repeating the same type on consecutive slides

### Phase 3: Self-Audit

After generating all slides, run these checks automatically:

```
[ ] YAML header matches template exactly (except title/subtitle/date)
[ ] 上节课回顾 opens with concept-box reviewing prior lecture
[ ] Every section has a {background-color="#AE0B2A"} divider
[ ] No colons after box titles
[ ] No **bold** inside boxes (use *italics*)
[ ] Blank line before every list
[ ] Blank line above AND below every `. . .`
[ ] No --- before level-1 header (indicated by a single #)
[ ] Code blocks use font-size: 1em
[ ] Chinese quotes “” ‘’(not ASCII "")
[ ] Half-width space between CJK and Latin/numbers
[ ] Max 2 colored boxes per slide
[ ] 本讲要点 split if >5 items
[ ] 下节课预告 matches syllabus next topic
[ ] All Python code uses {python} not {.python}
[ ] If Python figures with Chinese labels exist → matplotlib setup cell present after YAML header
[ ] References are real and verifiable
[ ] Estimated total: 25-40 slides
```

### Phase 4: Visual Audit

After self-audit passes, invoke the `visual-audit` skill on the generated file to catch overflow, font inconsistency, box fatigue, and layout issues.

### Phase 5: Website Integration

After the lecture file is finalized:

1. Update `_quarto.yml` in THREE places (render list, navbar, sidebar)
2. Render the full site with `quarto render`
3. Verify the new lecture appears in navigation

---

## Box Type Quick Reference

| Box             | CSS Class            | Color  | Use For                                           |
| --------------- | -------------------- | ------ | ------------------------------------------------- |
| Concept         | `.concept-box`     | Blue   | Definitions, core ideas, formal statements        |
| Example         | `.example-box`     | Gold   | Case studies, empirical examples, worked problems |
| Warning         | `.warning-box`     | Red    | Limitations, pitfalls, common mistakes            |
| Note            | `.callout-note`    | Blue   | Supplementary info, asides                        |
| Tip             | `.callout-tip`     | Green  | Software tools, practical advice                  |
| Warning callout | `.callout-warning` | Orange | Cautions (lighter than warning-box)               |

---

## Common Pitfalls (from session logs)

These mistakes have been caught repeatedly — avoid them:

1. **Colons after box titles** — WRONG: `**核心概念：**` → RIGHT: `**核心概念**`
2. **Bold inside boxes** — WRONG: `**要点**` inside box → RIGHT: `*要点*`
3. **Small code font** — WRONG: `font-size: 0.75em` → RIGHT: `font-size: 1em`
4. **ASCII quotes in Chinese** — WRONG: `"example"` → RIGHT: `"example"`。必须使用方向正确的中文双引号 `""`（U+201C/U+201D），参考 quarto-formatting Rule 2 & Rule 3。**注意：Edit 工具无法区分 ASCII 直引号和弯引号（Unicode 正规化问题），必须使用 quarto-formatting Rule 4 中的 Python 脚本进行自动替换和验证**
5. **Missing blank line before list** — every list needs a blank line above it
6. **Orphan `. . .`** after images — remove stray incremental markers
7. **Dense summary slides** — split 本讲要点 into 两页 if more than 5 items
8. **Too many boxes on one slide** — max 2; move extras to a new slide
9. **Low-res PDF→PNG** — WRONG: `sips -s dpiWidth 300` (only tags metadata) → RIGHT: use PyMuPDF `fitz` at ≥600 DPI (actual pixel rendering ≥2000px wide)
10. **Inconsistent image widths** — WRONG: inline `width="85%"` in QMD (creates forced inline style) → RIGHT: no width attribute, let CSS `max-width: 85%` handle sizing
11. **Distorted images** — WRONG: inline `width` + CSS `max-height` conflict → RIGHT: use only CSS `max-width` + `max-height` + `height: auto` + `width: auto !important`
12. **Inline Mermaid code blocks** — WRONG: `` ```{mermaid} `` in QMD → RIGHT: pre-render `.mmd` to PNG with `mmdc -s 4`, wrap with `:::{.intro-mermaid}`, insert as `![](diagrams/WN/file.png){fig-align="center"}`

---

## Post-Creation Checklist

```
[ ] Lecture compiles: quarto render 2026Spring/LectureNotes/WN_topic.qmd
[ ] No content overflow on any slide
[ ] All equations render (KaTeX)
[ ] All diagrams/images display
[ ] All images ≥2000px wide (check with: sips -g pixelWidth diagrams/WN/*.png)
[ ] No inline Mermaid code blocks (grep for "```{mermaid}" — must be 0 matches)
[ ] All Mermaid diagrams are pre-rendered PNG in diagrams/WN/ directory
[ ] Every Mermaid PNG is wrapped with `:::{.intro-mermaid}` div (no bare `![]()` references)
[ ] No image has inline width="xx%" attribute (CSS handles sizing via ruc-theme.scss)
[ ] No ASCII straight quotes in Chinese text — run quarto-formatting Rule 4 Python script to auto-fix (Edit tool CANNOT fix quotes due to Unicode normalization)
[ ] Python code cells execute correctly
[ ] Python-generated figures display Chinese labels correctly (no □□□ blank boxes)
[ ] Matplotlib Chinese font setup cell present (if Python figures contain Chinese labels)
[ ] Formatting self-audit passes (Phase 3)
[ ] Visual audit passes (Phase 4)
[ ] _quarto.yml updated (Phase 5)
[ ] Session log written to quality_reports/session_logs/
```

---

# NOTES WORKFLOW

## Notes Constraints (Non-Negotiable)

1. **Notes MUST be based on an existing slides file** — never create notes without slides
2. **Content must be consistent** with the slides — same structure, same notation, same examples
3. Notes EXPAND on slides; they do not contradict or reorganize the narrative
4. All Python code in notes must use `eval: true` with actual executable code
5. Include a matplotlib Chinese font setup block at the top
6. Use `#` / `##` / `###` heading hierarchy (not `##` slides-style)
7. No incremental reveals (`. . .`) — notes are a continuous document
8. No `{background-color}` section dividers — use regular `#` headings
9. No `.concept-box` / `.example-box` / `.warning-box` — use `.callout-note/warning/tip` instead
10. Chinese typography rules still apply (full-width quotes, punctuation, CJK-Latin spacing)

---

## Phase N0: Pre-Check & Intake

1. **Locate the slides file**: Find `2026Spring/LectureNotes/WN_*.qmd` (not `*_notes.qmd`)
   - If not found → STOP, ask user to create slides first (see Mode Selection above)
2. **Read the slides file** completely to extract:
   - All sections and their topics
   - All formulas and notation
   - All empirical cases and examples
   - All Python code blocks
   - References list
3. **Read `quarto-formatting/SKILL.md`** for formatting rules

## Phase N1: Expansion Plan

Analyze the slides and generate an **expansion checklist** showing what will be added. Present this to the user for approval.

The checklist should cover these expansion categories:

| Category              | What to expand                                            | Example                                      |
| --------------------- | --------------------------------------------------------- | -------------------------------------------- |
| **数学推导**    | Brief formula → full derivation with steps               | DiD estimator derivation, FE demeaning proof |
| **直觉解释**    | Bullet point → paragraph explanation                     | Why parallel trends matters                  |
| **案例拓展**    | Case name + result → full story + context + data         | Card & Krueger background, data details      |
| **Python 演示** | Slide code snippet → full executable demo with plots     | DiD simulation with visualization            |
| **R 对照**      | (often absent in slides) → add R equivalent              | fixest, did package examples                 |
| **图表可视化**  | Static diagram reference → matplotlib/plotly code        | Event study plot, DiD diagram                |
| **补充材料**    | (absent in slides) → literature context, further reading | Related papers, extensions                   |
| **课后思考**    | (absent in slides) → reflection questions                | 2-3 open-ended questions                     |

**Output format** — present to user like this:

```
📋 Notes 扩展清单 — 第N周：[TITLE]

基于 slides 内容，计划在以下方面进行扩展：

1. [数学推导] 固定效应去均值化的完整推导过程
2. [数学推导] DiD 估计量与 TWFE 的等价性证明
3. [案例拓展] Card & Krueger (1994) 完整研究背景与数据描述
4. [案例拓展] California Proposition 99 合成控制的详细过程
5. [Python 演示] DiD 模拟：完整数据生成 + 估计 + 可视化
6. [Python 演示] 事件研究图的绘制代码
7. [R 对照] 使用 fixest 包进行面板回归
8. [图表可视化] 平行趋势检验的可视化
9. [补充材料] 现代 DiD 文献综述
10. [课后思考] 3道反思题

是否确认？可以增删调整。
```

**GATE: User approves expansion plan before Phase N2**

## Phase N2: Generate Notes

### YAML Header Template (copy verbatim, update title/subtitle/date)

```yaml
---
title: "经济与商务实证研究方法 - 第N周：[TITLE]"
subtitle: "[SUBTITLE]：完整讲义"
author: "陈志远"
institute: "中国人民大学商学院"
date: "YYYY-MM-DD"
format:
  html:
    theme: cosmo
    css: lecture-notes.css
    html-math-method: mathml
    toc: true
    toc-depth: 3
    number-sections: true
    code-fold: false
    code-tools: true
    highlight-style: github
    self-contained: true
    embed-resources: true
    page-layout: article
execute:
  echo: true
  warning: false
  message: false
  eval: true
  cache: false
  fig-width: 10
  fig-height: 6
  dpi: 150
lang: zh
jupyter: python3
---
```

### Setup Code Block (MUST be first code cell)

````markdown
```{python}
#| echo: false
#| output: false
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Set up matplotlib for Chinese display
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150

# Set random seed for reproducibility
np.random.seed(42)
```
````

### Notes Structure Patterns

**Follow the slides section order exactly**, but expand as planned:

```markdown
# 引言 {#sec-intro}

[Bridge from previous lecture — what we learned, why this lecture follows]

## 上节课回顾

[Expanded paragraph version of the slides' review box]

# 第一部分：[Section Title] {#sec-part1}

## [Concept Name]

[Full paragraph explanation — motivation, context, why it matters]

### [Sub-topic]

[Detailed derivation or extended explanation]

$$
\begin{aligned}
...step-by-step derivation...
\end{aligned}
$$

### 直观理解

[Extended intuition with analogies and examples]

### Python 实现

```{python}
#| code-fold: show
#| code-summary: "点击查看完整代码"
#| fig-cap: "图标题"
#| fig-width: 12
#| fig-height: 8

# Full executable code with visualization
```

### R 语言对照

```{r}
#| eval: true
#| echo: true

# R equivalent code
```

```

**Summary Section:**

```markdown
# 总结 {#sec-summary}

## 本讲要点回顾

### 1. [Topic]
- [Extended summary point]

### 2. [Topic]
- [Extended summary point]

## 关键公式汇总

| 概念 | 公式 | 说明 |
|:---|:---|:---|
| ... | $...$ | ... |

## 下一讲预告

**第N+1周：[TITLE]**

[Brief paragraph about what comes next and why]

## 课后思考

1. **在你的研究领域**，[open-ended reflection question]
2. **[Topic]**：[analytical question]
3. **[Topic]**：[critical thinking question]
```

**Ending:**

```markdown
---

**联系方式**

- 邮箱：chenzhiyuan@rmbs.ruc.edu.cn
- 办公室：919
- Office Hours：邮件或微信预约

*本讲义基于 [source books/papers] 整理而成。*
```

### Writing Guidelines (Notes-Specific)

1. **Prose over bullets**: Notes use full paragraphs, not just bullet lists
2. **Show your work**: Include derivation steps, not just final formulas
3. **Code tells a story**: Each code block should build on the previous one; add narrative between blocks
4. **Visualization matters**: Every major concept should have an accompanying plot
5. **Dual-language code**: Include both Python and R where appropriate
6. **Cross-references**: Use `{#sec-label}` and `@sec-label` for internal links
7. **Figure captions**: Use `#| fig-cap:` for all figures
8. **Code folding**: Use `#| code-fold: show` with `#| code-summary:` for long code blocks
9. **Target length**: 500-800 lines; longer than slides but not exhaustive

## Phase N3: Self-Audit (Notes)

```
[ ] YAML header uses html format with theme: cosmo
[ ] Setup code block is first cell (matplotlib Chinese fonts)
[ ] All Python code uses {python} not {.python} and eval: true
[ ] Section structure mirrors slides order
[ ] No .concept-box / .example-box / .warning-box (use callouts)
[ ] No `. . .` incremental reveals
[ ] No {background-color} dividers
[ ] Chinese quotes (run quarto-formatting Rule 4 Python script to auto-fix — Edit tool CANNOT fix this)
[ ] All formulas from slides are preserved (notation consistency)
[ ] Expansion items from Phase N1 checklist are all addressed
[ ] 课后思考 section with 2-3 questions
[ ] 联系方式 at the end
[ ] References match slides' references (plus any additions)
[ ] File named: WN_topic_notes.qmd
```

## Phase N4: Render & Website Integration

1. Render the notes: `quarto render 2026Spring/LectureNotes/WN_topic_notes.qmd`
2. Update `_quarto.yml` in THREE places (render list, navbar as "第N周：详细讲义", sidebar)
3. Verify rendering — all code executes, all plots display

---

## Notes Post-Creation Checklist

```
[ ] Notes compile: quarto render 2026Spring/LectureNotes/WN_topic_notes.qmd
[ ] All Python code executes and produces output
[ ] All plots render with Chinese labels
[ ] All equations display correctly (MathML)
[ ] Content is consistent with slides (no contradictions)
[ ] Expansion checklist items all addressed
[ ] _quarto.yml updated
[ ] Session log written to quality_reports/session_logs/
```
