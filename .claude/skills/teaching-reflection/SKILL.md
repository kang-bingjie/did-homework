---
name: teaching-reflection
description: |
  Analyze a teaching transcript against lecture slides/notes to produce a comprehensive
  reflection covering knowledge accuracy, pedagogical effectiveness, and insight extraction.
  Feeds improvements back into slides, knowledge base, and persistent teaching memory.
  Use after each teaching session with a transcript.
argument-hint: "WN transcript_path [--skip-interview] [--focus knowledge|pedagogy|insights]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Agent", "AskUserQuestion", "Task"]
---

# Teaching Reflection

Comprehensive post-teaching analysis that compares what you *planned* (slides/notes) with what you *actually said* (transcript), then generates actionable improvements.

This skill is for the 经济与商务实证研究方法 (RMEB) course — an 8-week course covering empirical research methods in economics and business.

---

## Non-Negotiable Constraints

1. **Transcript alignment must complete before parallel review** — reviewers need the alignment map
2. **Factual errors are CRITICAL severity** — always flagged first in recommendations
3. **Teaching memory is append-only** — never delete entries, only update status
4. **Patches require user approval** — never auto-edit slides or notes
5. **KB updates require user approval** — never auto-modify knowledge base
6. **Scores are transparent** — every deduction cites specific transcript evidence
7. **Chinese-language output** — all reports, questions, and patches in Chinese

---

## Phase 0: Intake

### Parse Arguments

Extract from `$ARGUMENTS`:

1. **Week number** — e.g., `W03` → resolve to files
2. **Transcript path** — path to `.md` or `.txt` file
3. **Flags:**
   - `--skip-interview` → set SKIP_INTERVIEW=true
   - `--focus knowledge|pedagogy|insights` → set FOCUS_LENS

### Resolve Files

```
Slides:  2026Spring/LectureNotes/WN_*.qmd (NOT *_notes.qmd)
Notes:   2026Spring/LectureNotes/WN_*_notes.qmd (may not exist — that's OK)
KB:      .claude/rules/knowledge-base-rmeb.md
Memory:  .claude/rules/teaching-memory.md
```

If slides file not found, STOP and ask the user to confirm the week number.

### Read All Inputs

Read these files in parallel:

1. Slides QMD (full file)
2. Notes QMD (full file, if exists)
3. Transcript (full file)
4. Teaching memory (full file, if exists — may be empty for first reflection)
5. Knowledge base (full file)

---

## Phase 1: Alignment (Sequential — Must Complete Before Phase 2)

Launch the **transcript-aligner** agent with:

- Slides QMD content
- Notes QMD content (if available)
- Transcript content

**Agent prompt must include:**

> You are the transcript-aligner agent. Align this teaching transcript to the lecture slides.
>
> **Slides file:** [path]
> **Notes file:** [path or "N/A"]
> **Transcript file:** [path]
>
> Read all three files, then produce the alignment map following your agent protocol.
> Save the alignment map to: `quality_reports/teaching_reflections/WN_YYYY-MM-DD_alignment.md`

**GATE:** Wait for alignment to complete. Read the alignment map output before proceeding.

---

## Phase 2: Parallel Review (3 Agents Simultaneously)

Launch all three agents in parallel, each receiving the alignment map:

### Agent A: Knowledge Teaching Reviewer

> You are the knowledge-teaching-reviewer agent. Review this teaching session for knowledge quality.
>
> **Alignment map:** [path to alignment map from Phase 1]
> **Slides:** [path]
> **Notes:** [path or "N/A"]
> **Transcript:** [path]
> **Knowledge base:** .claude/rules/knowledge-base-rmeb.md
>
> Read all files and the alignment map, then produce your knowledge review following your agent protocol.

### Agent B: Pedagogy Teaching Reviewer

> You are the pedagogy-teaching-reviewer agent. Review this teaching session for pedagogical effectiveness.
>
> **Alignment map:** [path to alignment map from Phase 1]
> **Slides:** [path]
> **Transcript:** [path]
>
> Read all files and the alignment map, then produce your pedagogy review following your agent protocol.

### Agent C: Insight Extractor

> You are the insight-extractor agent. Evaluate all deviations from this teaching session.
>
> **Alignment map:** [path to alignment map from Phase 1]
> **Slides:** [path]
> **Notes:** [path or "N/A"]
> **Transcript:** [path]
>
> Read all files and the alignment map, then produce your insight extraction following your agent protocol.

**If `--focus` flag is set:** Still run all 3 agents, but when synthesizing (Phase 3), weight the focused lens at 2x in the overall score.

**GATE:** Wait for all 3 agents to complete before proceeding.

---

## Phase 3: Synthesis

Merge the outputs of all 3 agents into a unified reflection. Read all agent outputs.

### Compute Scores

**Per-dimension scores (0-100):**

| Dimension | Weight | Source |
| --------- | ------ | ------ |
| Knowledge accuracy | 25% | Knowledge reviewer |
| Logical reasoning | 20% | Knowledge reviewer |
| Pedagogical effectiveness | 25% | Pedagogy reviewer |
| Content coverage | 15% | Alignment map |
| Innovation value | 10% | Insight extractor |
| Time efficiency | 5% | Insight extractor |

If `--focus` is set, double the weight of the focused area and re-normalize.

**Overall score:** Weighted average of all dimensions.

**Score interpretation:**

| Score | Rating |
| ----- | ------ |
| 90-100 | Excellent |
| 80-89 | Good |
| 70-79 | Adequate |
| 60-69 | Needs Work |
| <60 | Concerning |

### Identify Cross-Cutting Themes

From all 3 reports, identify:

- **Recurring strengths** — patterns that appear across sections
- **Recurring growth areas** — issues that appear across sections
- **Connections between dimensions** — e.g., pacing issue causing knowledge gap

### Rank Recommendations

Merge all agent recommendations into a single priority list:

1. CRITICAL knowledge issues first (factual errors)
2. HIGH-value insights to preserve (don't lose the gold)
3. Major pedagogical improvements
4. Minor refinements

---

## Phase 4: Socratic Interview (Optional)

**Skip if `--skip-interview` flag is set.**

Generate 3-5 targeted questions based on Phase 3 findings. Use these triggers:

| Trigger | Question Pattern |
| ------- | --------------- |
| Significant deviation | "你在[X]处花了N分钟讲了slides里没有的[Y]，是什么让你想到这个的？" |
| Skipped section | "你跳过了[section]，这是有意为之还是时间限制？" |
| Explanation differs from notes | "你对[Z]的解释和讲义不同。你更喜欢哪个版本？" |
| Engagement peak | "你讲[W]时似乎特别投入。是什么让这部分有效？" |
| Factual issue | "你说了[statement]。现在回想，这个表述准确吗？" |
| Always (final) | "如果重新来过，最想改变的一件事是什么？" |

Present questions one at a time using `AskUserQuestion`. Record each answer.

---

## Phase 5: Output Generation

### 5.1 Write Reflection Report

Save to: `quality_reports/teaching_reflections/WN_YYYY-MM-DD_reflection.md`

Structure:

```markdown
# 教学反思: 第N周 — [标题]
**日期:** YYYY-MM-DD
**总体评分:** XX/100 (评级)

## 评分摘要
| 维度 | 分数 | 关键发现 |
| ---- | ---- | -------- |
| 知识准确性 | XX | [一句话] |
| 逻辑推理 | XX | [一句话] |
| 教学有效性 | XX | [一句话] |
| 内容覆盖率 | XX% | [覆盖/总计] |
| 创新价值 | XX | [N个洞见, M个偏题] |
| 时间效率 | XX% | [有效偏离占比] |

## 逐节分析
[Section-by-section from all 3 agents, integrated]

## 跨维度主题
### 优势
### 改进方向

## 洞见清单
[From insight extractor]

## 教师反思 (来自苏格拉底式访谈)
[Q&A pairs if interview was conducted]

## 优先建议
1. [最高优先级]
2. [第二优先级]
3. [第三优先级]

## 与历史讲座对比
[From teaching memory, if available]
```

### 5.2 Generate Patches

Save to: `quality_reports/teaching_reflections/WN_YYYY-MM-DD_patches.md`

For each actionable finding:

- **Slide patches:** Content to add/edit in the QMD (with exact location)
- **Notes patches:** Content to add/edit in the notes QMD
- **Each patch includes:** file, location, action (ADD/EDIT/DELETE), rationale, proposed content

Mark all patches as `PENDING USER APPROVAL`.

Present the patches to the user and ask which ones to apply.

### 5.3 Update Teaching Memory

Read the current `.claude/rules/teaching-memory.md` (or initialize if first reflection).

**Append (never overwrite):**

- New row in Week History table
- New entries in Best Improvised Content (if any HIGH-value insights)
- New entries in Knowledge Corrections Log (if any factual errors found)
- New entries in Effective Teaching Techniques (if any standout moments)
- New entries in Techniques to Avoid (if any patterns to stop)
- Update Instructor Profile strengths/growth areas if patterns are confirmed across 2+ weeks
- Update Growth Trajectory with latest scores

### 5.4 Propose KB Updates (If Applicable)

If the insight extractor or knowledge reviewer found content that should update the knowledge base:

- New methods or concepts discussed (add to knowledge base)
- New empirical application discussed (add to applications database)
- New anti-pattern identified (add to anti-patterns)

Present each proposed KB update to the user for approval before making changes.

---

## Post-Completion

1. **Present summary to user:** Overall score, top 3 strengths, top 3 growth areas, patches awaiting approval
2. **Log session:** Write session log to `quality_reports/session_logs/`
3. **Remind about patches:** "N个修改建议待审批，运行时我会逐一展示。"

---

## First-Time Initialization

If this is the first time `/teaching-reflection` is run (teaching-memory.md doesn't exist):

1. Initialize `.claude/rules/teaching-memory.md` with the empty template
2. Create `quality_reports/teaching_reflections/` directory
3. Note in the report: "这是首次教学反思，尚无历史数据可供对比。"
4. Note: This is an 8-week course, so the growth trajectory tracks progress across 8 weeks of teaching.
