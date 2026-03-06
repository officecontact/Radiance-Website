#!/usr/bin/env python3
"""
build_page.py — Assembles full HTML pages from shared partials + page-specific content.
"""
from pathlib import Path

SHARED_DIR = Path(__file__).parent / "shared"

def _read(filename):
    return (SHARED_DIR / filename).read_text(encoding="utf-8")

def build_page(
    title: str,
    description: str,
    keywords: str,
    canonical: str,       # just the filename, e.g. "rice.html"
    page_schema: str,     # raw <script type="application/ld+json">...</script> blocks
    page_css: str,        # raw <style>...</style> block for page-specific CSS
    body_content: str,    # everything between nav_js and footer
) -> str:
    """
    Assembles a complete HTML page from shared partials + page-specific content.
    Returns the full HTML string.
    """
    DOMAIN = "https://www.radianceoverseas.com"

    head = _read("head_common.html")
    head = head.replace("{{TITLE}}", title)
    head = head.replace("{{DESCRIPTION}}", description)
    head = head.replace("{{KEYWORDS}}", keywords)
    head = head.replace("{{CANONICAL}}", f"{DOMAIN}/{canonical}")
    head = head.replace("{{OG_TITLE}}", title)
    head = head.replace("{{OG_DESC}}", description)
    head = head.replace("{{OG_URL}}", f"{DOMAIN}/{canonical}")
    head = head.replace("{{PAGE_SCHEMA}}", page_schema)

    parts = [
        head,
        "<body>\n",
        _read("topbar.html"),
        _read("nav.html"),
        _read("mobile_drawer.html"),
        _read("nav_js.html"),
        page_css,
        body_content,
        _read("footer.html"),
        _read("whatsapp_float.html"),
        _read("scripts.html"),
    ]
    return "".join(parts)
