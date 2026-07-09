#!/usr/bin/env python3
"""
Pre-Compact State Preservation Hook

Fires before context compaction to save current session state.
Writes state to a session-scoped JSON file that post-compact-restore.py
reads after compaction to help Claude resume seamlessly.

Hook Event: PreCompact
Returns: Exit code 0 (always allow compaction to proceed)
"""

import json
import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# Colors for terminal output
CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
NC = "\033[0m"


def get_session_dir() -> Path:
    """Get the session directory for storing state files."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return Path.home() / ".claude" / "sessions" / "default"

    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:8]
    session_dir = Path.home() / ".claude" / "sessions" / project_hash
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def find_active_plan(project_dir: str) -> dict | None:
    """Find the most recent plan file and extract its status."""
    plans_dir = Path(project_dir) / "quality_reports" / "plans"
    if not plans_dir.exists():
        return None

    plan_files = sorted(
        plans_dir.glob("*.md"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not plan_files:
        return None

    latest_plan = plan_files[0]
    content = latest_plan.read_text()

    status = "unknown"
    if "COMPLETED" in content.upper():
        status = "completed"
    elif "APPROVED" in content.upper():
        status = "in_progress"
    elif "DRAFT" in content.upper():
        status = "draft"

    current_task = None
    for line in content.split("\n"):
        if "- [ ]" in line:
            current_task = line.replace("- [ ]", "").strip()
            break

    return {
        "plan_path": str(latest_plan),
        "plan_name": latest_plan.name,
        "status": status,
        "current_task": current_task,
    }


def find_recent_session_log(project_dir: str) -> str | None:
    """Find the most recent session log path."""
    logs_dir = Path(project_dir) / "quality_reports" / "session_logs"
    if not logs_dir.exists():
        return None

    log_files = sorted(
        logs_dir.glob("*.md"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    return str(log_files[0]) if log_files else None


def main():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    session_dir = get_session_dir()

    state = {
        "timestamp": datetime.now().isoformat(),
        "project_dir": project_dir,
    }

    # Capture active plan info
    plan_info = find_active_plan(project_dir) if project_dir else None
    if plan_info:
        state["plan_path"] = plan_info["plan_path"]
        state["plan_status"] = plan_info["status"]
        state["current_task"] = plan_info.get("current_task")

    # Capture recent session log
    session_log = find_recent_session_log(project_dir) if project_dir else None
    if session_log:
        state["session_log"] = session_log

    # Write state file for post-compact-restore.py to read
    state_file = session_dir / "pre-compact-state.json"
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    # Print reminder to stdout
    print(f"\n{CYAN}[Pre-Compact]{NC} State saved to {state_file}")
    if plan_info:
        print(f"  Plan: {plan_info['plan_name']} ({plan_info['status']})")
        if plan_info.get("current_task"):
            print(f"  Next task: {plan_info['current_task']}")

    # Exit 0 to allow compaction to proceed
    sys.exit(0)


if __name__ == "__main__":
    main()
