---
paths:
  - "Quarto/**/*.qmd"
  - "Quarto/diagrams/**"
---

# Image Quality & Typography Rules

## Rule 1: PDF→PNG 高分辨率转换

**严禁使用 `sips` 转换 PDF 为 PNG** — `sips` 仅修改 DPI 元数据标签，不增加实际像素数量，导致图片在投影和 Retina 屏幕上模糊。

**正确方法**：使用 PyMuPDF (`fitz`) 以 ≥600 DPI 实际渲染：

```python
import fitz
doc = fitz.open("source.pdf")
page = doc[0]
zoom = 600 / 72.0  # 600 DPI (fitz 默认 72 DPI)
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat, alpha=False)
pix.save("output.png")
```

**验证标准**：输出 PNG 像素宽度 ≥ 2000px。使用 `sips -g pixelWidth file.png` 检查。

## Rule 2: 图片尺寸与宽高比

- **不要在 QMD 中设置 `width="85%"`** — Quarto 会将其渲染为内联 `style="width:85%"`，当 CSS 同时有 `max-height` 限制时会破坏宽高比
- **由 CSS 统一控制**：`ruc-theme.scss` 中通过 `max-width: 85%` + `max-height: 65vh` + `height: auto` + `width: auto !important` 实现等比例缩放
- **Slides 语法**：`![](diagrams/lectureNN/image.png){fig-align="center"}`（不加 width）
- **Notes 语法**：`![标题](diagrams/lectureNN/image.png){#fig-label}`（不加 width）
- 浏览器会在 `max-width` 和 `max-height` 两个约束中取更严的那个，同时自动保持原始宽高比

## Rule 3: 中文引号（参考 quarto-formatting Rule 2 & Rule 3）

- **中文文本中的双引号**：必须使用方向正确的 `""` (U+201C / U+201D)
- **严禁**：在中文语境中使用 ASCII 直引号 `""`（U+0022）
- **英文文本中的引号**：使用英文引号 `""`
- **检查方法**：扫描所有含 CJK 字符的行，排除代码块、YAML 头和 HTML 属性后，不应包含 ASCII 直引号 `"`

### 快速检查脚本

```python
import re
with open("file.qmd") as f:
    for i, line in enumerate(f, 1):
        if re.search(r'[\u4e00-\u9fff]', line) and '"' in line:
            # 排除属性内的引号后检查
            clean = re.sub(r'\{[^}]*\}', '', line)
            clean = re.sub(r'[a-zA-Z_-]+=("[^"]*")', '', clean)
            if '"' in clean:
                print(f"L{i}: {line.rstrip()}")
```
