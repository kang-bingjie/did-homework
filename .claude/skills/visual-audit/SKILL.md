---
name: visual-audit
description: Perform adversarial visual audit of Quarto or Beamer slides checking for overflow, font consistency, box fatigue, and layout issues.
argument-hint: "[QMD or TEX filename]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Visual Audit of Slide Deck

Perform a thorough visual layout audit of a slide deck.

## Steps

1. **Read the slide file** specified in `$ARGUMENTS`

2. **For Quarto (.qmd) files:**
   - Render with `quarto render Quarto/$ARGUMENTS`
   - Open in browser to inspect each slide

3. **For Beamer (.tex) files:**
   - Compile and check for overfull hbox warnings

4. **Audit every slide for:**

   **OVERFLOW:** Content exceeding slide boundaries
   **FONT CONSISTENCY:** Inline font-size overrides, inconsistent sizes
   **BOX FATIGUE:** 2+ colored boxes on one slide, wrong box types
   **SPACING:** Missing negative margins, missing fig-align
   **LAYOUT:** Missing transitions, missing framing sentences, semantic colors
   **IMAGE RESOLUTION:** All PNG images must be ≥2000px wide. Check with `sips -g pixelWidth`. If any image is below threshold, re-convert from source PDF using PyMuPDF at ≥600 DPI
   **IMAGE SIZING:** Images must NOT have inline `width="xx%"` attributes — CSS in `ruc-theme.scss` handles sizing via `max-width: 85%` + `max-height: 65vh`. Flag any image with a width attribute as it will override CSS and break aspect ratio
   **CHINESE TYPOGRAPHY:** No ASCII straight double quotes `"` in Chinese text context. Must use directional quotes `""` (U+201C/U+201D). Reference: quarto-formatting Rule 2 & Rule 3
   **PYTHON FIGURE CHINESE RENDERING:** When the file contains `eval: true` Python code blocks that generate matplotlib/seaborn figures with Chinese text (axis labels, titles, legends, annotations), verify:
   - A hidden matplotlib setup cell exists **after the YAML header and before any content**, containing `plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']` and `plt.rcParams['axes.unicode_minus'] = False`
   - The setup cell uses `#| echo: false` and `#| output: false` so it does not appear on slides
   - **All** Python code blocks that call `plt.xlabel()`, `plt.ylabel()`, `plt.title()`, `plt.legend()`, `ax.set_xlabel()`, `ax.set_ylabel()`, `ax.set_title()`, or `ax.legend()` with Chinese text are covered by the setup cell (it must appear before them)
   - No later code block re-imports matplotlib and resets `rcParams` without re-applying the Chinese font config
   - If the setup cell is missing or incomplete, flag as **CRITICAL** — Chinese labels will render as blank boxes (□□□)

5. **Produce a report** organized by slide with severity and recommendations

6. **Follow the spacing-first principle:**
   1. Reduce vertical spacing with negative margins
   2. Consolidate lists
   3. Move displayed equations inline
   4. Reduce image/SVG size
   5. Last resort: font size reduction (never below 0.85em)
