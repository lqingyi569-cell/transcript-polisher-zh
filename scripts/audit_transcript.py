#!/usr/bin/env python3
"""Audit information retention and structure in revised Chinese transcripts."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from docx import Document


ROLE_RE = re.compile(r"^【([^】]+)】")
CHINESE_RE = re.compile(r"[\u3400-\u9fff]")
SUSPICIOUS = (
    "转写存疑",
    "没有没有",
    "然后然后",
    "就是就是",
    "对对对",
    "这个这个",
)


def load(path: Path):
    if path.suffix.lower() == ".docx":
        doc = Document(path)
        paragraph_objects = [p for p in doc.paragraphs if p.text.strip()]
        paragraphs = [p.text.strip() for p in paragraph_objects]
        headings = [
            p.text.strip()
            for p in paragraph_objects
            if p.style.name.startswith("Heading")
        ]
    else:
        paragraphs = [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        headings = [
            line.lstrip("#").strip()
            for line in paragraphs
            if line.startswith("#")
        ]
    chars = sum(len(CHINESE_RE.findall(text)) for text in paragraphs)
    roles: dict[str, int] = {}
    for text in paragraphs:
        match = ROLE_RE.match(text)
        if match:
            role = match.group(1)
            roles[role] = roles.get(role, 0) + 1
    suspicious = [
        (index + 1, token, text)
        for index, text in enumerate(paragraphs)
        for token in SUSPICIOUS
        if token in text
    ]
    return {
        "paragraphs": paragraphs,
        "chars": chars,
        "headings": headings,
        "roles": roles,
        "suspicious": suspicious,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    args = parser.parse_args()

    original = load(args.original)
    revised = load(args.revised)
    ratio = revised["chars"] / original["chars"] if original["chars"] else 0

    print(f"Original Chinese chars: {original['chars']}")
    print(f"Revised Chinese chars:  {revised['chars']}")
    print(f"Retention ratio:        {ratio:.1%}")
    print(f"Original paragraphs:    {len(original['paragraphs'])}")
    print(f"Revised paragraphs:     {len(revised['paragraphs'])}")
    print(f"Original headings:      {len(original['headings'])}")
    print(f"Revised headings:       {len(revised['headings'])}")
    print(f"Revised role labels:    {revised['roles']}")

    missing = [h for h in original["headings"] if h not in revised["headings"]]
    if missing:
        print("Missing headings:")
        for heading in missing:
            print(f"  - {heading}")

    if ratio < 0.5:
        print("WARNING: retention is below 50%; the revision may be a summary.")
    elif ratio < 0.65:
        print("NOTE: retention is below the default 65% target; review omissions.")
    elif ratio > 1.05:
        print("NOTE: revision is longer than source; check for unsupported expansion.")

    if revised["suspicious"]:
        print("Suspicious text:")
        for line, token, text in revised["suspicious"][:20]:
            print(f"  paragraph {line}: {token}: {text[:100]}")
    else:
        print("No configured suspicious tokens found.")


if __name__ == "__main__":
    main()
