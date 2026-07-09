#!/usr/bin/env python3
"""
wav_to_text.py — 将 .wav 音频文件转录为文字并生成 Markdown 文件

依赖:
    pip install openai-whisper

用法:
    python wav_to_text.py <音频文件.wav>
    python wav_to_text.py <音频文件.wav> -o 输出目录
    python wav_to_text.py <音频文件.wav> --model large  (默认: base)
    python wav_to_text.py <文件夹路径>                   (批量处理)
    python wav_to_text.py <音频文件.wav> --lang en       (指定语言)
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path


def format_timestamp(seconds: float) -> str:
    """将秒数转换为 SRT/VTT 风格的时间戳"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def format_srt_time(seconds: float) -> str:
    """SRT 格式时间戳"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def transcribe_file(
    audio_path: Path,
    model_size: str = "base",
    language: str | None = None,
    output_dir: Path | None = None,
    verbose: bool = False,
) -> Path | None:
    """转录单个音频文件并生成 Markdown 文件"""

    import whisper

    if not audio_path.exists():
        print(f"❌ 文件不存在: {audio_path}")
        return None

    print(f"\n{'='*60}")
    print(f"🎤 正在转录: {audio_path.name}")
    print(f"📦 模型: whisper-{model_size}")
    print(f"{'='*60}")

    # 加载模型
    print("⏳ 加载模型中...")
    model = whisper.load_model(model_size)

    # 准备转录参数
    transcribe_opts = {"verbose": verbose}
    if language:
        transcribe_opts["language"] = language

    # 执行转录
    print("⏳ 转录中...")
    start_time = time.time()
    result = model.transcribe(str(audio_path), **transcribe_opts)
    elapsed = time.time() - start_time

    # 获取音频时长（秒）
    audio_duration = result.get("duration", 0)

    print(f"✅ 转录完成！耗时: {elapsed:.1f}s | 音频时长: {audio_duration:.1f}s")
    print(f"   ⚡ 实时因子: {elapsed / audio_duration:.2f}x" if audio_duration > 0 else "")

    # 确定输出目录
    if output_dir is None:
        output_dir = audio_path.parent
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 输出文件路径
    output_name = audio_path.stem
    md_path = output_dir / f"{output_name}_transcript.md"

    # 检测语言（如果未指定）
    detected_lang = result.get("language", language or "unknown")

    # 生成 Markdown 内容
    lines = []
    lines.append("---")
    lines.append(f'title: "语音转文字 — {audio_path.name}"')
    lines.append(f"date: \"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\"")
    lines.append(f"source_file: \"{audio_path.name}\"")
    lines.append(f"source_path: \"{audio_path.resolve()}\"")
    lines.append(f"model: \"whisper-{model_size}\"")
    lines.append(f"language: \"{detected_lang}\"")
    lines.append(f"duration_seconds: {audio_duration:.1f}")
    lines.append(f"processing_time_seconds: {elapsed:.1f}")
    lines.append("---")
    lines.append("")
    lines.append(f"# 语音转文字: {audio_path.name}")
    lines.append("")
    lines.append(f"- **音频文件**: `{audio_path.name}`")
    lines.append(f"- **转录模型**: whisper-{model_size}")
    lines.append(f"- **检测语言**: {detected_lang}")
    lines.append(f"- **音频时长**: {audio_duration:.1f} 秒 ({audio_duration / 60:.1f} 分钟)")
    lines.append(f"- **处理耗时**: {elapsed:.1f} 秒")
    lines.append(f"- **转录时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # 完整文本
    full_text = result.get("text", "").strip()
    if full_text:
        lines.append("## 完整文本")
        lines.append("")
        lines.append(full_text)
        lines.append("")

    # 带时间戳的逐段文本
    segments = result.get("segments", [])
    if segments:
        lines.append("## 分段文本（含时间戳）")
        lines.append("")
        lines.append("| 时间 | 文本 |")
        lines.append("|------|------|")
        for seg in segments:
            ts = format_timestamp(seg["start"])
            text = seg["text"].strip()
            if text:
                lines.append(f"| {ts} | {text} |")
        lines.append("")

        # SRT 格式
        lines.append("## SRT 字幕格式")
        lines.append("")
        lines.append("```srt")
        for i, seg in enumerate(segments, 1):
            start = format_srt_time(seg["start"])
            end = format_srt_time(seg["end"])
            text = seg["text"].strip()
            if text:
                lines.append(f"{i}")
                lines.append(f"{start} --> {end}")
                lines.append(f"{text}")
                lines.append("")
        lines.append("```")

    # 写入文件
    md_content = "\n".join(lines)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"📄 已保存: {md_path}")
    return md_path


def find_wav_files(directory: Path) -> list[Path]:
    """递归查找目录下所有 .wav 文件"""
    return sorted(directory.rglob("*.wav"))


def main():
    parser = argparse.ArgumentParser(
        description="将 .wav 音频文件转录为文字并生成 Markdown 文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s lecture.wav
  %(prog)s lecture.wav -o ./transcripts
  %(prog)s lecture.wav --model large
  %(prog)s ./audio_folder --model small --lang zh
  %(prog)s lecture.wav --model base --verbose
        """,
    )
    parser.add_argument("input", help=".wav 文件路径或包含 .wav 文件的目录")
    parser.add_argument("-o", "--output", help="输出目录（默认: 音频文件所在目录）")
    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large", "turbo"],
        help="Whisper 模型大小（默认: base）",
    )
    parser.add_argument(
        "--lang", "--language",
        dest="language",
        default=None,
        help="指定语言（如 zh, en, ja）。不指定则自动检测。",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="显示详细转录过程"
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    # 收集需要处理的文件
    if input_path.is_dir():
        wav_files = find_wav_files(input_path)
        if not wav_files:
            print(f"❌ 目录中未找到 .wav 文件: {input_path}")
            sys.exit(1)
        print(f"📂 在目录中找到 {len(wav_files)} 个 .wav 文件")
    elif input_path.is_file():
        if input_path.suffix.lower() != ".wav":
            print(f"❌ 输入文件不是 .wav 格式: {input_path}")
            print("   请提供 .wav 文件，或先使用格式转换工具（如 ffmpeg）转换。")
            sys.exit(1)
        wav_files = [input_path]
    else:
        print(f"❌ 路径不存在: {input_path}")
        sys.exit(1)

    # 解析输出目录
    output_dir = Path(args.output) if args.output else None

    # 逐文件转录
    success_count = 0
    for wav_file in wav_files:
        try:
            result_path = transcribe_file(
                audio_path=wav_file,
                model_size=args.model,
                language=args.language,
                output_dir=output_dir,
                verbose=args.verbose,
            )
            if result_path:
                success_count += 1
        except ImportError:
            print("\n❌ 缺少依赖。请安装 openai-whisper:")
            print("   pip install openai-whisper")
            print("\n   如果安装缓慢，可以使用国内镜像:")
            print("   pip install openai-whisper -i https://pypi.tuna.tsinghua.edu.cn/simple")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ 转录失败 [{wav_file.name}]: {e}")

    # 总结
    print(f"\n{'='*60}")
    print(f"🎯 处理完成: {success_count}/{len(wav_files)} 个文件成功")
    if success_count > 0:
        print(f"📁 输出位置: {output_dir or wav_files[0].parent}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
