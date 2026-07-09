---
name: lecture-post
description: >
  Deploy rendered lecture slides and notes to the course website (GitHub Pages) and Gitee repository.
  Handles file copying WITH attachments (_files/ folders), _quarto.yml updates (render list, navbar, sidebar),
  index.qmd announcement updates, git commit & push, and Gitee sync.
  Use when the user says "部署", "发布", "deploy", "post lecture", "上传课件", "推送到网站",
  "同步到Gitee", "lecture-post", or any variant indicating deployment of finished lecture materials.
  ALWAYS use this skill for deployment — never manually copy files without it.
argument-hint: "week N"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
---
# Lecture Deployment Workflow

Deploy rendered lecture slides and companion notes to the course website (GitHub Pages) and Gitee student repository.

## Key Facts

| Item              | Value                                                        |
| ----------------- | ------------------------------------------------------------ |
| Website repo      | `zhiyuanryanchen/empirical-methods` (GitHub Pages)         |
| Gitee repo        | `econ-research-methods/` (local), `gitee.com/zhiyuanryanchen/econ-research-methods.git` (remote) |
| Gitee branch      | `master`                                                   |
| Gitee lecture dir  | `econ-research-methods/2026Spring/`                       |
| Source dir        | `2026Spring/LectureNotes/`                                 |
| Website output    | `docs/2026Spring/LectureNotes/`                            |
| Website config    | `_quarto.yml` (top-level)                                  |
| Homepage source   | `index.qmd`                                                |

## Critical Rule: Attachments Must Travel With HTMLs

Quarto renders two types of HTML output:

| Type                           | Format                    | Self-contained?                           | `_files/` folder needed?                                         |
| ------------------------------ | ------------------------- | ----------------------------------------- | ------------------------------------------------------------------ |
| **Slides** (revealjs)    | `WN_{topic}.html`       | **NO**                              | **YES** — contains `libs/revealjs/`, `figure-revealjs/` |
| **Notes** (html article) | `WN_{topic}_notes.html` | **YES** (`embed-resources: true`) | **NO** — images are base64-embedded                         |

**Slides HTML files CANNOT display without their `_files/` folder.** Every copy operation for slides must include the corresponding `_files/` directory. Notes are self-contained and do not need `_files/`.

### Diagrams Folder (CRITICAL — often missed)

Slides may reference static images via `![](diagrams/WN/image.png)` or `![](diagrams/mermaid/file.svg)`. These paths are **relative to the HTML file**, NOT inside `_files/`.

The source folder is `2026Spring/LectureNotes/diagrams/` and contains:

- `diagrams/W03/` — DAG PNGs for Week 3
- `diagrams/W06/` — Panel/DiD images for Week 6
- `diagrams/mermaid/` — Mermaid SVGs
- (new week subfolders may be added over time)

**The entire `diagrams/` folder MUST be synced to `docs/2026Spring/LectureNotes/diagrams/` and the Gitee repo.** This is a one-time copy per new diagram subfolder, but always verify during deployment.

---

## Usage

User invokes with week number: `/lecture-post week 3`

## Step 0: Identify Lecture Files

1. Extract week number from user input (e.g., "3")
2. List matching files:
   ```bash
   ls 2026Spring/LectureNotes/W0{N}_*.qmd 2026Spring/LectureNotes/W{N}_*.qmd 2>/dev/null
   ```
3. Identify topic from filename (e.g., `W03_panel_did.qmd` → topic is `panel_did`)
4. Set variables:
   - `{N}` — week number (e.g., `03`)
   - `{topic}` — topic slug from filename (e.g., `panel_did`)
   - `{TITLE}` — Chinese display title (extract from QMD `title:` field)
5. Confirm with user: "找到第{N}周：{TITLE}，确认部署吗？"

## Step 1: Verify Rendered Files Exist

```bash
# Required files
ls -lh 2026Spring/LectureNotes/W{N}_{topic}.html          # slides HTML
ls -lh 2026Spring/LectureNotes/W{N}_{topic}_notes.html    # notes HTML
ls -d  2026Spring/LectureNotes/W{N}_{topic}_files/        # slides attachments (REQUIRED)

# Source files (for Gitee)
ls 2026Spring/LectureNotes/W{N}_{topic}.qmd
ls 2026Spring/LectureNotes/W{N}_{topic}_notes.qmd
```

**If slides HTML or `_files/` folder is missing:**

```bash
cd 2026Spring/LectureNotes && export QUARTO_PYTHON='/Users/happyhome/anaconda3/bin/python3'
quarto render W{N}_{topic}.qmd
```

**If notes HTML is missing:**

```bash
# Notes must be rendered from OUTSIDE the LectureNotes/ project directory
export QUARTO_PYTHON='/Users/happyhome/anaconda3/bin/python3'
quarto render 2026Spring/LectureNotes/W{N}_{topic}_notes.qmd --to html
```

After rendering, re-verify all files exist before proceeding.

## Step 2: Deploy to Course Website (`docs/2026Spring/LectureNotes/`)

```bash
DOCS="docs/2026Spring/LectureNotes"

# ── Slides: copy HTML + _files/ folder ──
cp 2026Spring/LectureNotes/W{N}_{topic}.html "$DOCS/"
cp -R 2026Spring/LectureNotes/W{N}_{topic}_files "$DOCS/W{N}_{topic}_files"

# ── Notes: copy HTML only (self-contained) ──
cp 2026Spring/LectureNotes/W{N}_{topic}_notes.html "$DOCS/"

# ── Diagrams: sync the entire diagrams/ folder ──
cp -R 2026Spring/LectureNotes/diagrams "$DOCS/diagrams" 2>/dev/null || \
  rsync -a 2026Spring/LectureNotes/diagrams/ "$DOCS/diagrams/"

# ── Optional: copy QMD sources for reference ──
cp 2026Spring/LectureNotes/W{N}_{topic}.qmd "$DOCS/"
cp 2026Spring/LectureNotes/W{N}_{topic}_notes.qmd "$DOCS/"
```

## Step 3: Update `_quarto.yml` (3 locations)

Edit the **top-level** `_quarto.yml`.

### Location 1: `render` list

```yaml
    - 2026Spring/LectureNotes/W{N}_{topic}.html
    - 2026Spring/LectureNotes/W{N}_{topic}_notes.html
```

### Location 2: `navbar` menu

```yaml
          - text: "第{N}周：{TITLE}"
            file: 2026Spring/LectureNotes/W{N}_{topic}.html
          - text: "第{N}周：详细讲义"
            file: 2026Spring/LectureNotes/W{N}_{topic}_notes.html
```

### Location 3: `sidebar` contents

```yaml
            - text: "第{N}周：{TITLE}"
              file: 2026Spring/LectureNotes/W{N}_{topic}.html
            - text: "第{N}周：详细讲义"
              file: 2026Spring/LectureNotes/W{N}_{topic}_notes.html
```

## Step 4: Update `index.qmd` Announcement

```markdown
**YYYY-MM-DD**

第{N}周课件和详细讲义已发布！

📊 [查看第{N}周课件](2026Spring/LectureNotes/W{N}_{topic}.html)

📖 [查看第{N}周详细讲义](2026Spring/LectureNotes/W{N}_{topic}_notes.html)

---
```

## Step 5: Commit and Push Course Website

```bash
git add _quarto.yml index.qmd
git add docs/2026Spring/LectureNotes/W{N}_{topic}.html
git add docs/2026Spring/LectureNotes/W{N}_{topic}_notes.html
git add docs/2026Spring/LectureNotes/W{N}_{topic}_files/
git add docs/2026Spring/LectureNotes/diagrams/
git commit -m "feat: Deploy 第{N}周 {TITLE}"
git push origin main
```

## Step 6: Deploy QMD Sources to Gitee

Copy QMD source files (and their diagram dependencies) to the Gitee student repository so students can access the source and render locally.

```bash
GITEE="econ-research-methods/2026Spring"

# ── Create LectureNotes dir if needed ──
mkdir -p "$GITEE/LectureNotes"

# ── Copy QMD source files ──
cp 2026Spring/LectureNotes/W{N}_{topic}.qmd "$GITEE/LectureNotes/"
cp 2026Spring/LectureNotes/W{N}_{topic}_notes.qmd "$GITEE/LectureNotes/"

# ── Copy diagrams referenced by QMDs ──
if [ -d "2026Spring/LectureNotes/diagrams/W{N}" ]; then
  mkdir -p "$GITEE/LectureNotes/diagrams/W{N}"
  cp -R "2026Spring/LectureNotes/diagrams/W{N}/" "$GITEE/LectureNotes/diagrams/W{N}/"
fi

# ── Copy theme files if not already present (needed for local rendering) ──
cp -n ruc-theme.scss "$GITEE/" 2>/dev/null || true
cp -n lecture-notes.css "$GITEE/" 2>/dev/null || true
```

### Commit and Push to Gitee

```bash
cd econ-research-methods
git add 2026Spring/
git add ruc-theme.scss lecture-notes.css 2>/dev/null || true
git commit -m "feat: 第{N}周 {TITLE} 课件源文件"
git push origin master
cd ..
```

**Note:** Gitee repo uses branch `master` (not `main`). Always verify with `git branch --show-current` before pushing.

## Step 7: Post-Deployment Verification

```bash
# Verify _quarto.yml has the new lecture (3 locations)
grep -c "W{N}_{topic}" _quarto.yml
# → Should appear in render, navbar, and sidebar.

# Verify Gitee files
ls econ-research-methods/2026Spring/LectureNotes/W{N}_*.qmd
```

### Deployment Checklist

```
[ ] Slides HTML copied to docs/2026Spring/LectureNotes/
[ ] Slides _files/ folder copied to docs/2026Spring/LectureNotes/
[ ] diagrams/ folder synced to docs/2026Spring/LectureNotes/diagrams/
[ ] Notes HTML copied to docs/2026Spring/LectureNotes/
[ ] _quarto.yml updated: render list
[ ] _quarto.yml updated: navbar menu
[ ] _quarto.yml updated: sidebar contents
[ ] index.qmd updated with announcement
[ ] GitHub Pages repo committed and pushed
[ ] QMD source files copied to econ-research-methods/2026Spring/LectureNotes/
[ ] Diagram assets copied to econ-research-methods/2026Spring/LectureNotes/diagrams/
[ ] Theme files (ruc-theme.scss, lecture-notes.css) present in Gitee repo
[ ] Gitee repo committed and pushed to master
[ ] Slides display correctly when opened locally
```
