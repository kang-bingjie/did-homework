---
name: pdf-to-md
description: Convert PDF documents to Markdown using pandoc with configurable extraction options.
---

# pdf-to-md

Convert PDF files to clean Markdown using pandoc. Useful for extracting text from academic papers, lecture notes, and research documents for further editing or inclusion in Quarto/Markdown workflows.

## When to Use

- Extract text from a PDF paper to quote or summarize it in lecture slides
- Convert scanned or exported PDF notes into editable Markdown
- Prepare PDF content for inclusion in a Quarto project or documentation
- Batch-convert multiple PDFs in a directory

## Requirements

- **pandoc** must be installed (`brew install pandoc` on macOS, or download from pandoc.org)
- For scanned/image-based PDFs, OCR pre-processing (e.g., `ocrmypdf`) is recommended before using this skill

## Basic Usage

### Single File

```bash
pandoc input.pdf -t markdown -o output.md
```

### Preserve Formatting (Headers, Lists, Tables)

```bash
pandoc input.pdf -t markdown --wrap=none --extract-media=./media -o output.md
```

### Batch Convert All PDFs in a Directory

```bash
for f in *.pdf; do pandoc "$f" -t markdown -o "${f%.pdf}.md"; done
```

## Common Options

| Option | Description |
|--------|-------------|
| `-t markdown` | Target format (required) |
| `-o file.md` | Output file path |
| `--wrap=none` | Disable line-wrapping for cleaner diffs |
| `--extract-media=DIR` | Extract embedded images to a directory |
| `--standalone` | Produce a full document with metadata |
| `--from pdf` | Explicitly specify input format |

## Tips

- **Text-based PDFs** (exported from Word/LaTeX): pandoc extraction is usually high-quality.
- **Scanned PDFs**: Run `ocrmypdf input.pdf output_ocr.pdf` first, then apply this skill.
- **Tables**: pandoc may approximate complex tables; review the Markdown output.
- **Math**: Inline LaTeX math often survives conversion but may need cleanup.

## After Conversion

Review the generated `.md` file for:
1. Broken tables or lists
2. Missing images (use `--extract-media` to preserve them)
3. Garbled math or special characters
4. Header level consistency

## Example Workflow

```bash
# 1. Convert a single paper
pandoc Carlson_Burbano_2026.pdf -t markdown --wrap=none -o Carlson_Burbano_2026.md

# 2. Review and clean up
# Open the .md file and fix any formatting issues

# 3. Move to your project
mv Carlson_Burbano_2026.md ./2026Spring/LectureNotes/references/
```
