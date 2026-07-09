---
name: wav-to-text
description: 将 .wav 音频文件转录为文字并生成 Markdown 文件。使用 OpenAI Whisper 实现高精度语音识别，支持中文、英文等多语言。适用于讲座录音、会议记录、访谈等场景。
argument-hint: "<.wav 文件路径或目录路径> [选项]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Run", "Task"]
---

# WAV 转文字 (Speech-to-Text)

使用 OpenAI Whisper 将 `.wav` 音频文件转录为文字，输出结构化的 Markdown 文件（含完整文本、分段时间戳、SRT 字幕格式）。

## 安装依赖

首次使用需要安装 Whisper：

```bash
pip install openai-whisper
```

如果安装缓慢，可使用国内镜像：

```bash
pip install openai-whisper -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> **注意**：Whisper 需要 `ffmpeg`，macOS 上可通过 `brew install ffmpeg` 安装。

## 使用方法

### 基本用法

```bash
# 转录单个文件（使用 base 模型，自动检测语言）
python .claude/skills/wav-to-text/scripts/wav_to_text.py  lecture.wav

# 指定输出目录
python .claude/skills/wav-to-text/scripts/wav_to_text.py  lecture.wav -o ./transcripts

# 指定模型和语言
python .claude/skills/wav-to-text/scripts/wav_to_text.py  lecture.wav --model small --lang zh

# 批量处理整个目录
python .claude/skills/wav-to-text/scripts/wav_to_text.py  ./audio_folder --model medium

# 显示详细转录过程
python .claude/skills/wav-to-text/scripts/wav_to_text.py  lecture.wav --verbose
```

### 可用模型

| 模型 | 速度 | 精度 | 推荐场景 |
|------|------|------|---------|
| `tiny` | ⚡⚡⚡⚡⚡ | ★★☆ | 快速预览 |
| `base` | ⚡⚡⚡⚡ | ★★★☆ | **默认，日常推荐** |
| `small` | ⚡⚡⚡ | ★★★★ | 较高质量 |
| `medium` | ⚡⚡ | ★★★★★ | 高质量转录 |
| `large` | ⚡ | ★★★★★★ | 最高精度（需 GPU） |
| `turbo` | ⚡⚡⚡ | ★★★★★ | large 精度 + 更快速度 |

### 语言选项

- `zh` — 中文（普通话）
- `en` — English
- `ja` — 日本語
- 不指定则自动检测

## 输出文件格式

生成 Markdown 文件 `{原文件名}_transcript.md`，包含：

1. **YAML 元数据** — 文件信息、模型参数、处理时间
2. **完整文本** — 纯文本全文
3. **分段文本（含时间戳）** — 表格格式，每段带起止时间
4. **SRT 字幕格式** — 可直接导入视频编辑软件

### 示例输出结构

```markdown
---
title: "语音转文字 — lecture.wav"
source_file: "lecture.wav"
model: "whisper-base"
language: "zh"
duration_seconds: 1860.5
---

# 语音转文字: lecture.wav

## 完整文本

大家好，今天我们来讨论...

## 分段文本（含时间戳）

| 时间 | 文本 |
|------|------|
| 00:00:00.000 | 大家好，今天我们来讨论... |

## SRT 字幕格式

```srt
1
00:00:00,000 --> 00:00:05,320
大家好，今天我们来讨论...
```
```

## 工作流

1. **转录** → 运行脚本生成 Markdown
2. **审阅** → 检查转录质量，修正识别错误
3. **应用** → 将文本用于讲义整理、笔记生成、字幕制作等

## 注意事项

- **长音频**：Whisper 自动处理长音频，无需分割
- **音频质量**：清晰的录音效果更好（建议采样率 16kHz+）
- **GPU 加速**：如有 NVIDIA GPU 会自动使用，大幅提升速度
- **文件格式**：当前仅支持 `.wav` 格式。其他格式（`.mp3`, `.m4a` 等）请先用 `ffmpeg` 转换：
  ```bash
  ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav
  ```
