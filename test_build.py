#!/usr/bin/env python3
"""
test_build.py — Tests the build_page function by regenerating rice.html
and comparing with the original.
"""
import difflib
import sys
from pathlib import Path

from build_page import build_page

# Read original rice.html
orig_path = Path(__file__).parent / "rice.html"
with open(orig_path, "r", encoding="utf-8") as f:
    orig_lines = f.readlines()

# ---- Extract page-specific values from rice.html ----

# Title (line 7, 0-indexed: 6)
title = "Indian Rice Export — Basmati & Non-Basmati | APEDA Registered | Radiance Overseas"

# Description (line 8, 0-indexed: 7)
description = "Buy bulk Indian rice — 1121 Basmati, Pusa Basmati, IR64 Parboiled, Sona Masoori, Swarna. APEDA registered exporter from India. EU Organic, India Organic. MOQ 25 MT. 30+ countries."

# Keywords (line 9, 0-indexed: 8)
keywords = "basmati rice export india,indian rice exporter,1121 basmati rice india,IR64 parboiled rice export,sona masoori rice export,APEDA rice exporter,non-basmati rice india export"

# Canonical / OG_URL filename
canonical = "rice.html"

# PAGE_SCHEMA: lines 34-36 (0-indexed: 33-35), the CollectionPage + FAQPage scripts
# (after the Organization schema which stays hardcoded)
page_schema = "".join(orig_lines[33:36])

# page_css: lines 629-720 (0-indexed: 628-719)
page_css = "".join(orig_lines[628:720])

# body_content: lines 721-1044 (0-indexed: 720-1043)
body_content = "".join(orig_lines[720:1044])

# ---- Build the page ----
rebuilt = build_page(
    title=title,
    description=description,
    keywords=keywords,
    canonical=canonical,
    page_schema=page_schema,
    page_css=page_css,
    body_content=body_content,
)

# Write to /tmp/rice_rebuilt.html
output_path = Path("/tmp/rice_rebuilt.html")
output_path.write_text(rebuilt, encoding="utf-8")
print(f"Rebuilt page written to: {output_path}")

# ---- Compare ----
orig_text = orig_path.read_text(encoding="utf-8")
rebuilt_lines = rebuilt.splitlines(keepends=True)
orig_lines_clean = orig_text.splitlines(keepends=True)

diff = list(difflib.unified_diff(
    orig_lines_clean,
    rebuilt_lines,
    fromfile="rice.html (original)",
    tofile="rice_rebuilt.html",
    lineterm="",
))

if not diff:
    print("\nRESULT: PERFECT MATCH — rebuilt is identical to original!")
else:
    print(f"\nRESULT: {len(diff)} diff lines found. First 80 diff lines:")
    print("\n".join(diff[:80]))

    # Count matching lines
    matcher = difflib.SequenceMatcher(None, orig_lines_clean, rebuilt_lines)
    ratio = matcher.ratio()
    print(f"\nSimilarity ratio: {ratio:.4f} ({ratio*100:.2f}%)")
