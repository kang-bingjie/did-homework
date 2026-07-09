---
paths:
  - "**/*.qmd"
  - "**/*.md"
---

# Chinese Typography: Quotation Marks

**This rule is enforced on every write or edit to any `.qmd` or `.md` file.**

## The Non-Negotiable Rule

Chinese text MUST use **directional curved quotes**. ASCII straight quotes inside Chinese sentences are always wrong.

| Correct | Wrong | Unicode |
|:---|:---|:---|
| `"左引号"` | `"左引号"` | U+201C / U+201D |
| `'左引号'` | `'左引号'` | U+2018 / U+2019 |

## Application by Context

### Chinese sentence — use Chinese curved quotes

```
✓  这就是"后门准则"的核心思想。
✓  他说："这是一个'局部平均处理效应'的问题。"

✗  这就是"后门准则"的核心思想。
✗  这就是'后门准则'的核心思想。
```

### English sentence — use English directional quotes (same characters, same rule)

```
✓  The key idea is "conditional independence."
✓  She called this a 'natural experiment.'

✗  The key idea is "conditional independence."
```

### YAML frontmatter — ASCII `"` is correct YAML syntax, leave unchanged

```yaml
title: "经济与商务实证研究方法"   ← correct, this is YAML, not prose
```

### Code blocks — no change; use whatever the language requires

```python
label = "处理组"   # ← ASCII quotes inside code are correct Python syntax
```

## Direction Matters

The opening quote opens to the RIGHT (`"` `'`) and the closing quote opens to the LEFT (`"` `'`). Reversed direction is wrong:

```
✗  "工具变量"   ← reversed: right-open then right-close
✓  "工具变量"   ← correct: left-open then right-close
```

## Common Error Patterns to Catch Before Saving

1. **Typing shortcut output**: most keyboards produce `"…"` (straight) — always replace with `"…"` in Chinese prose
2. **Copy-paste from code editors**: code editors often insert straight quotes — check after pasting
3. **Inside callout/box titles**: these are still prose, apply the same rule
4. **Inside LaTeX math mode `$...$`**: math mode content is exempt (LaTeX handles its own quoting)
5. **Markdown link titles** `[text](url "title")`: use ASCII quotes in URL/link syntax per Markdown spec

## Quick Reference — Characters to Use

Copy-paste as needed:

- Chinese double open: `"`  (U+201C  LEFT DOUBLE QUOTATION MARK)
- Chinese double close: `"`  (U+201D  RIGHT DOUBLE QUOTATION MARK)
- Chinese single open: `'`  (U+2018  LEFT SINGLE QUOTATION MARK)
- Chinese single close: `'`  (U+2019  RIGHT SINGLE QUOTATION MARK)

## Bulk Fix Script

When copy-pasting from older files or the web, straight quotes often contaminate `.qmd`/`.md` prose. Use this Python snippet to batch-replace straight quotes with curved ones, while **preserving** YAML frontmatter, code blocks, and HTML attributes:

```python
import re

with open('file.qmd', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_yaml = False
in_code = False
yaml_done = False

for line in lines:
    s = line.strip()
    if s == '---' and not yaml_done:
        in_yaml = not in_yaml
        if not in_yaml: yaml_done = True
        new_lines.append(line); continue
    if in_yaml: new_lines.append(line); continue
    if s.startswith('```'):
        in_code = not in_code
        new_lines.append(line); continue
    if in_code: new_lines.append(line); continue
    if 'style=' in line or 'fig-alt=' in line:
        new_lines.append(line); continue

    new_line = line
    # Paired straight double quotes → curved
    new_line = re.sub(r'"([^"]{2,})"', lambda m: '“' + m.group(1) + '”', new_line)
    # Paired straight single quotes → curved
    new_line = re.sub(r"'([^']{2,})'", lambda m: '‘' + m.group(1) + '’', new_line)
    new_lines.append(new_line)

with open('file.qmd', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
```

**Key points:**
- Only processes paired quotes (`"text"`, `'text'`) to avoid breaking contractions and code
- Skips YAML, fenced code blocks, and HTML attribute lines
- Requires manual review after running — not a fully hands-off replacement
