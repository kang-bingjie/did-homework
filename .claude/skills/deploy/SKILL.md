---
name: deploy
description: Render Quarto slides and sync to docs/ for GitHub Pages deployment. Use when deploying lecture slides after making changes.
disable-model-invocation: true
argument-hint: "[WeekN or 'all']"
allowed-tools: ["Read", "Bash"]
---

# Deploy Slides to GitHub Pages

Render Quarto slides and sync all files to `docs/` for GitHub Pages deployment.

## Steps

1. **Run the sync script:**
   - If `$ARGUMENTS` is provided (e.g., "Week3"): `./scripts/sync_to_docs.sh $ARGUMENTS`
   - If no argument: `./scripts/sync_to_docs.sh` (syncs all weeks)

2. **Verify deployment:**
   - Check that HTML files exist in `docs/2026Spring/LectureNotes/`
   - Check that `_files/` directories were copied (RevealJS assets)
   - Check that `docs/2026Spring/LectureNotes/diagrams/` was synced

3. **Verify interactive charts** (if applicable):
   - Grep rendered HTML for interactive widget count
   - Confirm count matches expected

4. **Verify TikZ SVGs** (if applicable):
   - Check that all referenced SVG files exist in `docs/2026Spring/LectureNotes/diagrams/WN/`

5. **Open in browser** for visual verification:
   - `open docs/2026Spring/LectureNotes/WN_Name.html`
   - Confirm slides render, images display, navigation works

6. **Report results** to the user

## Website

- GitHub Pages: `zhiyuanryanchen.github.io/rmeb-website`
- Repository: `zhiyuanryanchen/rmeb-website`
- Course: 经济与商务实证研究方法

## What the sync script does:

- Renders all `.qmd` files in `2026Spring/LectureNotes/` (skips `*_backup*` files)
- Copies HTML and `_files/` directories to `docs/2026Spring/LectureNotes/`
- Syncs `2026Spring/LectureNotes/diagrams/` to `docs/2026Spring/LectureNotes/diagrams/` using rsync
