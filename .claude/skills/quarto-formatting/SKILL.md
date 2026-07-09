---
name: quarto-formatting
description: Quarto RevealJS slide formatting conventions. Box styles (.concept-box, .example-box, .warning-box, callouts), typography rules, and visual consistency for academic slides.
argument-hint: "[QMD filename]"
user-invocable: true
---
# Quarto RevealJS Formatting Conventions

## Custom Box Styles

### Box Types and Usage

| Class                | Use Case                  | Color Theme      |
| -------------------- | ------------------------- | ---------------- |
| `.concept-box`     | Key theoretical concepts  | Blue left border |
| `.example-box`     | Worked examples, cases    | Gold left border |
| `.warning-box`     | Common pitfalls, cautions | Red left border  |
| `.callout-note`    | Information callouts      | Blue left border |
| `.callout-warning` | Warning callouts          | Red left border  |
| `.callout-tip`     | Tips and hints            | Gold left border |

### Box Content Formatting Rules

**CRITICAL: Follow these exactly for visual consistency.**

#### Rule 1: No Colons After Box Titles

```markdown
# GOOD:
::: {.concept-box}
**核心概念**

- 要点1
- 要点2
:::

# BAD (colon after title):
::: {.concept-box}
**核心概念**：

- 要点1
- 要点2
:::
```

**Why**: The title spans the full div width. A colon at the end creates an awkward line break.

#### Rule 2: Use Italics (Not Bold) for Emphasis Inside Boxes

```markdown
# GOOD:
::: {.concept-box}
**随机变量 (Random Variable)**

分为：
- *离散型*：取值可数
- *连续型*：取值不可数
:::

# BAD:
::: {.concept-box}
**随机变量 (Random Variable)**:

分为：
- **离散型**：取值可数
- **连续型**：取值不可数
:::
```

**Why**: Bold inside colored boxes creates visual clutter. Italics provide emphasis while maintaining clean aesthetics.

#### Rule 3: Box Title Format

- Use a single line with bold for the box title
- Do not add a colon after the title
- Leave a blank line after the title
- Use regular text or italics in the body, not bold
- Then add content

```markdown
::: {.example-box}
**直观理解**

抛硬币次数越多，正面比例越接近 50%
:::
```

### Complete Examples

**Concept Box:**

```markdown
::: {.concept-box}
**条件期望函数 (CEF)**

在给定 $X=x$ 的条件下，$Y$ 的期望：
$$E[Y|X=x]$$

*关键性质*：$E[\varepsilon|X] = 0$
:::
```

**Warning Box:**

```markdown
::: {.warning-box}
**常见错误**

用预测的方法做因果推断，或用因果的方法做预测，都会导致错误结论！
:::
```

**Example Box:**

```markdown
::: {.example-box}
**例子：教育与收入**

回归显示每多受一年教育，收入增加 8%。但这不一定是因果效应，因为：
1. *能力偏误*：能力强的人既爱学习又能赚钱
2. *家庭背景*：富裕家庭的孩子教育更多
:::
```

## Code Block Formatting

### Code Font Size Rule

**Use `font-size: 1em` for all code blocks** to ensure readability on projection screens:

```markdown
# GOOD:
::: {style="font-size: 1em;"}
```{python}
import numpy as np
```

:::

# BAD (too small):

::: {style="font-size: 0.78em;"}

```{python}
import numpy as np
```

:::

```

**Why**: Smaller font sizes (0.75em, 0.78em) are hard to read in lecture halls. Use 1em for consistent readability.

### Python Code
```markdown
::: {style="font-size: 1em;"}
```{python}
#| echo: true
#| eval: false
import numpy as np
```

:::

```

**Note**: For display-only code (not executable), use `python.reticulate: false` chunk option to prevent reticulate errors.

### R Code
```markdown
::: {style="font-size: 1em;"}
```{r}
#| echo: true
#| eval: false
library(dplyr)
```

:::

```

## Chinese Typography Rules

### Quotation Marks (引号)

**CRITICAL: Distinguish Chinese and English quotation marks correctly.**

#### Rule 1: Chinese text always uses full-width curved quotation marks

- For Chinese double quotes, use opening “ and closing ”
- For Chinese single quotes, use opening ‘ and closing ’
- Do not use straight ASCII quotes inside Chinese sentences

```markdown
# GOOD:
这就是“后门准则”的核心思想。
他说：“这是一个‘局部平均处理效应’的问题。”

# BAD (straight ASCII double quotes):
这就是"后门准则"的核心思想。

# BAD (straight ASCII single quotes):
这就是'后门准则'的核心思想。
```

#### Rule 2: English text uses standard English quotation marks

- For English double quotes, use opening " and closing "
- For English single quotes, use opening ' and closing '
- Do not replace English quotes with Chinese full-width quotes when the sentence itself is English

```markdown
# GOOD:
The key idea is "conditional independence."
She called this a 'natural experiment.'

# BAD:
The key idea is "conditional independence."
She called this a 'natural experiment.'
```

#### Rule 3: Ensure the opening and closing direction is correct

- Chinese double quotes: left opening ", right closing "
- Chinese single quotes: left opening ', right closing '
- English quotes follow the same directional rule within English text

```markdown
# GOOD:
"工具变量"
'排他性约束'

# BAD (reversed direction):
"工具变量"
'排他性约束'
```

**Why**: Correct quotation marks are part of professional Chinese and English typography. Mixed or reversed quotes look unpolished and are especially noticeable in lecture slides.

#### Rule 4: Automated Quote Verification and Fixing

**CRITICAL: The Edit tool cannot distinguish ASCII straight quotes (U+0022) from curly quotes (U+201C/U+201D) due to Unicode normalization. Attempting to replace straight quotes with curly quotes via Edit will silently report "no changes." Always use the Python script below instead.**

**Verification** — check actual byte values with `hexdump`:

```bash
sed -n 'Np' file.qmd | hexdump -C | head -5
```

- ASCII straight quote `"` = byte `22`
- Left curly `\u201c` = bytes `e2 80 9c`
- Right curly `\u201d` = bytes `e2 80 9d`

**Automated Fix Script** — when straight quotes are found in Chinese prose, run this Python script (NOT the Edit tool):

```python
python3 << 'PYEOF'
path = 'TARGET_FILE.qmd'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_yaml = False
yaml_seen = 0
in_code = False
changed = 0
result = []

for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == '---' and yaml_seen < 2:
        yaml_seen += 1
        in_yaml = (yaml_seen == 1)
        result.append(line)
        continue
    if in_yaml:
        result.append(line)
        continue
    if stripped.startswith('```{python}') or stripped.startswith('```{r}'):
        in_code = True
        result.append(line)
        continue
    if in_code and stripped == '```':
        in_code = False
        result.append(line)
        continue
    if in_code:
        result.append(line)
        continue
    if stripped.startswith('#|'):
        result.append(line)
        continue
    if '"' in line:
        new_line = ''
        quote_open = False
        for ch in line:
            if ch == '"':
                if not quote_open:
                    new_line += '\u201c'
                    quote_open = True
                else:
                    new_line += '\u201d'
                    quote_open = False
                changed += 1
            else:
                new_line += ch
        result.append(new_line)
    else:
        result.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(result)
print(f"Replaced {changed} ASCII double quotes with curly quotes")
PYEOF
```

This script preserves:

- YAML frontmatter (between `---` delimiters)
- Code blocks (```` ```{python} ... ``` ````)
- Quarto cell options (`#|` lines)

And correctly pairs quotes: odd occurrence = opening `\u201c`, even = closing `\u201d`.

**Post-fix verification** — confirm zero remaining ASCII quotes in prose:

```python
python3 << 'PYEOF'
path = 'TARGET_FILE.qmd'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
in_yaml = False; yaml_seen = 0; in_code = False
for i, line in enumerate(lines, 1):
    s = line.strip()
    if s == '---' and yaml_seen < 2: yaml_seen += 1; in_yaml = (yaml_seen == 1); continue
    if in_yaml: continue
    if s.startswith('```{python}') or s.startswith('```{r}'): in_code = True; continue
    if in_code and s == '```': in_code = False; continue
    if in_code or s.startswith('#|'): continue
    if '"' in line: print(f"Line {i}: {line.rstrip()}")
print("--- Done (lines above still have ASCII quotes, if any) ---")
PYEOF
```

### Chinese Punctuation Spacing

- Use full-width Chinese punctuation (，。！？：；）
- No spaces around Chinese punctuation
- Exception: Use half-width space between Chinese and English/numbers

```markdown
# GOOD:
控制变量$X$后，我们可以识别因果效应

# BAD (missing space around math):
控制变量 $X$ 后，我们可以识别因果效应
```

## Math Formatting

- Use `$...$` for inline math
- Use `$$...$$` for display math
- Use `html-math-method: katex` in YAML for best RevealJS compatibility

## YAML Header Template

```yaml
---
title: "课程标题"
subtitle: "第X讲：副标题"
author: "作者名"
institute: "机构名"
date: "YYYY-MM-DD"
format:
  revealjs:
    theme: [default, ruc-theme.scss]
    css: ruc-theme.scss
    slide-number: true
    code-fold: false
    width: 1400
    height: 788
    toc: true
    toc-depth: 1
execute:
  echo: true
  warning: false
  message: false
  eval: false
lang: zh
html-math-method: katex
---
```

## List Spacing Rule

**CRITICAL: Every Markdown list MUST have a blank line before the first list item to render correctly.**

### Inside Box Environments

When a list follows text inside a box, ALWAYS add a blank line:

```markdown
# GOOD:
::: {.example-box}
**关键发现**

所有后门路径都经过家庭收入$I$！

- 路径1：$D \leftarrow I \rightarrow Y$
- 路径2：$D \leftarrow PE \rightarrow I \rightarrow Y$
:::

# BAD (no blank line before list):
::: {.example-box}
**关键发现**

所有后门路径都经过家庭收入$I$！
- 路径1：$D \leftarrow I \rightarrow Y$
- 路径2：$D \leftarrow PE \rightarrow I \rightarrow Y$
:::
```

### Common Patterns to Fix

```markdown
# Text ending with colon - needs blank line after colon:
控制$I$相当于：

- 在$I$的每个水平内比较
- 剥离$I$造成的相关性

# Section headers followed by lists:
**步骤1：朴素回归**

- 估计结果有偏
- 包含后门路径偏误
```

**Why**: Without the blank line, RevealJS renders lists as inline text instead of proper bullet points.

### Applies Everywhere

This rule applies in all Markdown and Quarto contexts, not only inside boxes:

- regular slide body text
- text after equations
- text after bold lead-ins such as `**步骤1**`
- text after Chinese colons such as `分为：`

```markdown
# GOOD:
*本节课目标*

- 理解匹配法的基本原理
- 掌握倾向得分匹配(PSM)的实现

# BAD:
*本节课目标*
- 理解匹配法的基本原理
- 掌握倾向得分匹配(PSM)的实现
```

### Enforcement Note

When editing `.md` or `.qmd` files, check every newly introduced list and insert the blank line immediately before the first bullet or numbered item.

## Pause (Incremental Reveal) Spacing Rule

**CRITICAL: `. . .` pauses MUST have blank lines above AND below.**

```markdown
# GOOD:
内容第一段

. . .

内容第二段（点击后显示）

# BAD (no blank line after):
内容第一段

. . .
内容第二段

# BAD (no blank lines):
内容第一段
. . .
内容第二段
```

**Why**: Without proper spacing, `. . .` may not render correctly as an incremental reveal, or may cause layout issues.

## Python Output Layout Rule

**CRITICAL: If a Python chunk produces both tabular/text output and a figure, do NOT keep them on the same slide. Split them into separate slides.**

### Required Pattern

- Slide 1: coefficients, summary table, printed statistics, or console output
- Slide 2: figure only
- The figure slide should usually use `#| echo: false`
- Increase `fig-width` and `fig-height` on the figure slide so the chart can fully occupy the slide

```markdown
## 倾向得分估计

::: {style="font-size: 0.75em;"}
```{python}
#| echo: true
#| eval: true
#| output: true

print(coef_df.to_string(index=False))
print(summary_stats)
```

:::

## 倾向得分分布图

```{python}
#| echo: false
#| eval: true
#| fig-width: 10
#| fig-height: 5.8

plt.show()
```

```

### Why This Matters

- RevealJS often compresses or clips figures when text/table output shares the same slide
- Table output becomes unreadable when competing with a chart for vertical space
- Splitting slides makes both the table and the figure legible during projection

### Preferred Defaults

- Keep table or console output inside a styled code/output slide
- Put the visualization on a dedicated follow-up slide with no printed table output
- Move summary statistics out of the figure chunk when necessary

## Enabling Executable Python Code Cells

To execute Python code during rendering (not just display):

### Required Packages

```bash
pip install jupyter-cache ipykernel numpy pandas matplotlib scipy statsmodels
```

### YAML Configuration

```yaml
---
title: "Your Title"
# ... other options ...
execute:
  echo: true
  warning: false
  message: false
  eval: true      # IMPORTANT: must be true to execute
  cache: true     # Cache results for faster re-renders
jupyter: python3  # IMPORTANT: specifies which kernel to use
---
```

### Project-Level Configuration

Create `_quarto.yml` in your Quarto directory:

```yaml
project:
  type: default

jupyter:
  kernel: python3

execute:
  freeze: auto  # Re-render only when source changes
  cache: true
```

### Code Block Syntax

```markdown
# GOOD (executable):
```{python}
#| echo: true
#| eval: true
import numpy as np
print("This will execute and show output!")
```

# BAD (not executable):

```{.python}
#| echo: false
#| eval: false
import numpy as np
```

```

### Critical Requirements

1. Use `{python}` NOT `{.python}` for code blocks
2. Use `{r}` NOT `{.r}` for R code blocks
3. Set `#| eval: true` in each chunk (or globally)
4. Add `jupyter: python3` to YAML
5. Install `jupyter-cache` for caching

### Troubleshooting

**Error: `.conda environment not activated`**

- Solution: Add `jupyter: python3` to YAML header and `_quarto.yml`

**Error: `jupyter-cache package is required`**

- Solution: Run `pip install jupyter-cache`

**Error: `No kernel found`**

- Solution: Ensure `ipykernel` is installed: `pip install ipykernel`
- Verify kernel is available: `python3 -m ipykernel --version`

**Code shows but doesn't execute (no output)**

- Check: Use `{python}` not `{.python}`
- Check: Set `#| eval: true` not `false`
- Check: Set global `execute: eval: true`

## Website Navigation Update Protocol

**CRITICAL: When adding new lectures, update `_quarto.yml` in THREE places.**

### Step 1: Add to Render List

```yaml
project:
  render:
    # ... existing lectures ...
    - Quarto/lecture03_dags.html
    - Quarto/lecture03_dags_notes.html
```

### Step 2: Add to Navbar Dropdown

```yaml
website:
  navbar:
    left:
      - text: "讲义"
        menu:
          # ... existing lectures ...
          - text: "第三讲：有向无环图"
            file: Quarto/lecture03_dags.html
          - text: "第三讲：详细讲义"
            file: Quarto/lecture03_dags_notes.html
```

### Step 3: Add to Sidebar

```yaml
website:
  sidebar:
    - title: "课程资料"
      contents:
        - section: "讲义"
          contents:
            # ... existing lectures ...
            - text: "第三讲：有向无环图"
              file: Quarto/lecture03_dags.html
            - text: "第三讲：详细讲义"
              file: Quarto/lecture03_dags_notes.html
```

### Step 4: Verify and Deploy

```bash
# Preview locally
quarto preview

# Render entire site
quarto render

# Commit and push
git add _quarto.yml docs/
git commit -m "feat: Add Lecture N to navigation"
git push origin main
```

**Why this matters**: The sidebar navigation is the primary way students access lecture materials. Missing updates here make content discoverable only through direct links.

## Checklist Before Committing

- [ ] No `**bold**` inside concept/example/warning boxes (use `*italics*`)
- [ ] No colons after box titles (causes display issues)
- [ ] Lists have blank line before first item (inside AND outside boxes)
- [ ] `. . .` pauses have blank lines above AND below
- [ ] Chinese quotes use full-width curved quotation marks `"` `"` (not straight quotes `"`)
- [ ] **Updated `_quarto.yml` navigation (3 places: render, navbar, sidebar)**
- [ ] For executable Python: `jupyter: python3` in YAML
- [ ] For display-only Python: `python.reticulate: false` chunk option
- [ ] Code font size is 1em (for readability on projection screens)
- [ ] Math renders correctly with KaTeX
- [ ] Mermaid diagrams have proper font configuration
