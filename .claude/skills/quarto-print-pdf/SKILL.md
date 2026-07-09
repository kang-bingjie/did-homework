---
name: quarto-print-pdf
description: Render Quarto RevealJS slides and print them to a real PDF using the reliable local-HTTP + Chrome headless workflow. Use this skill whenever the user asks to render slides, print Quarto slides to PDF, export RevealJS to PDF, create a PDF from a .qmd slide deck, or when direct file:///?print-pdf output creates a blank or tiny PDF.
---

# Quarto Print PDF

Use this skill to turn a Quarto RevealJS `.qmd` slide deck into both HTML and a valid PDF. This workflow is designed for this repository's slide decks, where direct `file://...?...print-pdf` printing can produce a blank 1-page PDF because Chrome may not load RevealJS assets and scripts correctly from local file paths.

## When To Use

Use this skill when the user asks for any of the following:

- render Quarto slides
- print slides to PDF
- export RevealJS slides to PDF
- create a PDF from a `.qmd` deck
- fix a blank/tiny PDF from Quarto/RevealJS
- produce a shareable PDF copy of lecture slides

## Expected Input

A path to a Quarto RevealJS `.qmd` file, usually relative to the repository root, for example:

```text
InvitedLectures/AI-For-Research/day1/day1_am.qmd
```

## Output

Create these files beside the `.qmd` input:

```text
<deck>.html
<deck>.pdf
```

Report the final PDF path, file size, page count when available, and any fallback used.

## Required Tools

- `quarto`
- Python 3, for `python3 -m http.server`
- Google Chrome at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` on macOS
- Optional: `pdfinfo` for page-count validation

If Chrome is not available at that path, locate it with `command -v google-chrome`, `command -v chromium`, or common macOS app paths before failing.

## Workflow

1. Render the `.qmd` normally first:

   ```bash
   quarto render '<deck>.qmd'
   ```

2. Confirm the `.html` file exists beside the `.qmd`.

3. Start a temporary HTTP server from the repository root or another parent directory that contains the `.qmd` deck and all referenced relative assets:

   ```bash
   python3 -m http.server <free-port>
   ```

   Use an available local port such as `8765`, `8766`, etc. Run this as a background/async process because it must stay alive while Chrome prints. In this repository, serving from the deck directory can break paths like `../../../ruc-theme.scss`; serving from the repository root avoids those 404s.

4. Print with Chrome headless from the HTTP URL, not `file://`:

   ```bash
   '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
     --headless=new \
     --disable-gpu \
     --no-sandbox \
     --run-all-compositor-stages-before-draw \
     --virtual-time-budget=10000 \
     --print-to-pdf='<absolute-output-pdf-path>' \
   'http://127.0.0.1:<port>/<path-from-server-root-to-deck>.html?print-pdf'
   ```

5. Validate that the PDF is real:

   ```bash
   file '<deck>.pdf'
   ls -lh '<deck>.pdf'
   pdfinfo '<deck>.pdf' | grep -E 'Pages|Page size'
   ```

   A tiny PDF around 1 KB or a PDF with only one blank page usually means Chrome printed before RevealJS loaded, or the deck was served through `file://`. Re-run through local HTTP.

6. Stop the temporary HTTP server.

## Preferred Script

Use the bundled helper script for repeatable execution:

```bash
python3 .claude/skills/quarto-print-pdf/scripts/print_quarto_pdf.py '<deck>.qmd'
```

The script renders the deck, serves the deck directory over local HTTP, prints with Chrome headless, validates the PDF, and shuts down the server.

## Important Notes

- Do not rely on `quarto render <deck>.qmd --to revealjs-pdf` alone. In this environment it may only regenerate a print-styled HTML file and not produce a `.pdf`.
- Do not rely on `file://...?...print-pdf` when the resulting PDF is tiny or blank.
- Serve from the repository root when decks reference parent-level theme files such as `../../../ruc-theme.scss`.
- If a deck is outside the current working directory, serve from the nearest common parent directory and use a URL path that reaches the HTML file.
- Always report whether the PDF was validated and whether a local HTTP server was used.

## Example

Input:

```bash
python3 .claude/skills/quarto-print-pdf/scripts/print_quarto_pdf.py 'InvitedLectures/AI-For-Research/day1/day1_am.qmd'
```

Expected result:

```text
Rendered HTML: InvitedLectures/AI-For-Research/day1/day1_am.html
Printed PDF: InvitedLectures/AI-For-Research/day1/day1_am.pdf
PDF size: 1.1M
Pages: 42
Temporary server stopped
```
