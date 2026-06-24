#!/usr/bin/env python3
"""
Interactive weekly-meeting logger.

Usage:  python log_meeting.py
Asks you what happened, then appends timestamped entries to
  weekly_meeting/<YYYY-MM-DD>/tasks.md
  weekly_meeting/<YYYY-MM-DD>/progress.md
  weekly_meeting/<YYYY-MM-DD>/potential_exploration.md

Multi-line input: enter blank line to finish a section.
Skip a section by entering a blank line immediately.
"""

from datetime import date, datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent / "weekly_meeting"

SECTIONS = [
    ("tasks.md",                 "Tasks",                 "Task list for the week"),
    ("progress.md",              "Progress",              "Experimental progress / results"),
    ("potential_exploration.md", "Potential Exploration", "Key issues & potential explanations"),
]


def read_block(prompt: str) -> str:
    """Read multi-line input until a blank line. Returns stripped block."""
    print(f"\n--- {prompt} (blank line to finish, or blank now to skip) ---")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def append_entry(path: Path, title: str, description: str, body: str, stamp: str, is_new: bool):
    with path.open("a", encoding="utf-8") as f:
        if is_new:
            f.write(f"# {title}\n\n> {description}\n\n")
        f.write(f"## {stamp}\n\n{body}\n\n")


def main():
    today = date.today().isoformat()           # YYYY-MM-DD (ISO-8601)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    folder = ROOT / today
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "images").mkdir(exist_ok=True)

    print(f"📓 Logging meeting for {today}")
    print(f"   → {folder}")

    wrote_any = False
    for filename, title, description in SECTIONS:
        body = read_block(title)
        if not body:
            print(f"   (skipped {filename})")
            continue
        path = folder / filename
        is_new = not path.exists()
        append_entry(path, title, description, body, stamp, is_new)
        print(f"   ✓ wrote to {path.relative_to(ROOT.parent)}")
        wrote_any = True

    if not wrote_any:
        print("\nNothing entered — no files written.")
        sys.exit(0)

    print(f"\n✅ Done. Timestamp: {stamp}")


if __name__ == "__main__":
    main()