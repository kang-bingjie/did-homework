#!/usr/bin/env python3
"""Render a Quarto RevealJS deck and print it to PDF via local HTTP + Chrome."""

from __future__ import annotations

import argparse
import contextlib
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


DEFAULT_CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def find_chrome(explicit: str | None = None) -> str:
    candidates = []
    if explicit:
        candidates.append(explicit)
    candidates.extend(DEFAULT_CHROME_PATHS)

    for candidate in candidates:
        if Path(candidate).exists():
            return candidate

    for name in ("google-chrome", "chromium", "chrome"):
        resolved = shutil.which(name)
        if resolved:
            return resolved

    raise RuntimeError(
        "Chrome/Chromium not found. Install Google Chrome or pass --chrome /path/to/chrome."
    )


def start_server_on_available_port(
    directory: Path,
    preferred_port: int | None,
    start: int = 8765,
    max_tries: int = 50,
) -> tuple[subprocess.Popen[str], int]:
    ports = [preferred_port] if preferred_port else list(range(start, start + max_tries))
    last_error: Exception | None = None
    for port in ports:
        if port is None:
            continue
        if not is_port_available(port):
            last_error = OSError(f"port {port} is already in use")
            continue
        process = subprocess.Popen(
            ["python3", "-m", "http.server", str(port), "--bind", "127.0.0.1"],
            cwd=directory,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        time.sleep(0.2)
        if process.poll() is None:
            return process, port
        output = process.stdout.read() if process.stdout else ""
        last_error = RuntimeError(output.strip() or f"server exited on port {port}")
        if preferred_port:
            break
    raise RuntimeError(f"Could not start local HTTP server: {last_error}")


def is_port_available(port: int) -> bool:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
        return True


def wait_until_ready(url: str, timeout_seconds: float = 5.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1.0) as response:
                if 200 <= response.status < 400:
                    return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
        time.sleep(0.1)
    raise RuntimeError(f"Local HTTP server did not become ready for {url}: {last_error}")


def pdf_info(pdf_path: Path) -> str:
    file_result = run(["file", str(pdf_path)])
    info = [file_result.stdout.strip()]

    if shutil.which("pdfinfo"):
        pdfinfo_result = run(["pdfinfo", str(pdf_path)])
        selected = [
            line
            for line in pdfinfo_result.stdout.splitlines()
            if line.startswith("Pages:") or line.startswith("Page size:")
        ]
        info.extend(selected)
    else:
        info.append("pdfinfo not found; skipped page-count validation")

    return "\n".join(info)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Quarto RevealJS slides and print them to PDF."
    )
    parser.add_argument("qmd", help="Path to the Quarto .qmd slide deck")
    parser.add_argument("--chrome", help="Path to Chrome/Chromium executable")
    parser.add_argument("--port", type=int, help="Local HTTP port to use")
    parser.add_argument(
        "--virtual-time-budget",
        type=int,
        default=10000,
        help="Chrome virtual time budget in milliseconds",
    )
    args = parser.parse_args()

    qmd_path = Path(args.qmd).expanduser().resolve()
    if not qmd_path.exists():
        raise FileNotFoundError(qmd_path)
    if qmd_path.suffix.lower() != ".qmd":
        raise ValueError(f"Expected a .qmd file, got: {qmd_path}")

    deck_dir = qmd_path.parent
    html_path = qmd_path.with_suffix(".html")
    pdf_path = qmd_path.with_suffix(".pdf")
    serve_root = Path.cwd().resolve()
    try:
        html_url_path = html_path.relative_to(serve_root).as_posix()
    except ValueError:
        serve_root = deck_dir
        html_url_path = html_path.name

    print(f"Rendering interactive HTML: {qmd_path}")
    render_result = run(["quarto", "render", str(qmd_path)])
    print(render_result.stdout)

    if not html_path.exists():
        raise RuntimeError(f"Expected rendered HTML not found: {html_path}")

    chrome = find_chrome(args.chrome)
    server, port = start_server_on_available_port(serve_root, args.port)
    url = f"http://127.0.0.1:{port}/{html_url_path}?print-pdf"

    try:
        print(f"Printing via local HTTP: {url}")
        wait_until_ready(url)
        print_result = run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--run-all-compositor-stages-before-draw",
                f"--virtual-time-budget={args.virtual_time_budget}",
                f"--print-to-pdf={pdf_path}",
                url,
            ]
        )
        if print_result.stdout.strip():
            print(print_result.stdout)
    finally:
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=3)
        print("Temporary HTTP server stopped")

    if not pdf_path.exists():
        raise RuntimeError(f"Expected PDF not found: {pdf_path}")
    if pdf_path.stat().st_size < 10_000:
        raise RuntimeError(
            f"PDF is suspiciously small ({pdf_path.stat().st_size} bytes): {pdf_path}"
        )

    print("PDF validation:")
    print(pdf_info(pdf_path))
    print(f"Rendered HTML: {html_path}")
    print(f"Printed PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
