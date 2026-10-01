#!/usr/bin/env python3

import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blogmaker import BlogBuilder
from test_build import _make_config

_HTML_LINK_RE = re.compile(r'href="/[^"]*\.html"')


def _build_sample(tmpdir) -> Path:
    config = _make_config(tmpdir)
    pages = Path(tmpdir) / "pages"
    pages.mkdir()
    config["pages_dir"] = str(pages)
    (Path(config["posts_dir"]) / "sample.md").write_text(
        "Date: 2025 Jan 01\nTags: life\n\n# Sample\n\nBody with a [link](https://example.com).")
    (pages / "about.md").write_text("# About\n\nAbout me.")
    BlogBuilder(config).build()
    return Path(config["output_dir"])


def test_every_page_has_home_header_and_footer():
    with tempfile.TemporaryDirectory() as tmpdir:
        output = _build_sample(tmpdir)
        for name in ["sample.html", "about.html", "index.html", "tag-life.html"]:
            html = (output / name).read_text()
            header = re.search(r"<header>.*?</header>", html, re.DOTALL)
            assert header and 'href="/"' in header.group(0), f"{name}: missing home link in header"
            assert 'href="/about"' in header.group(0), f"{name}: missing about link in header"
            footer = re.search(r"<footer>.*?</footer>", html, re.DOTALL)
            assert footer and 'href="/feed.xml"' in footer.group(0), f"{name}: missing footer"
        print("✓ Every page shares the header and footer!")


def test_internal_links_are_clean():
    with tempfile.TemporaryDirectory() as tmpdir:
        output = _build_sample(tmpdir)
        for html_file in output.glob("*.html"):
            links = _HTML_LINK_RE.findall(html_file.read_text())
            assert not links, f"{html_file.name}: .html links {links}"
        index = (output / "index.html").read_text()
        assert 'href="/sample"' in index, "Index should link to /sample"
        print("✓ Internal links are clean!")


def test_no_javascript_and_system_theme():
    with tempfile.TemporaryDirectory() as tmpdir:
        output = _build_sample(tmpdir)
        for html_file in output.glob("*.html"):
            html = html_file.read_text()
            assert "<script" not in html, f"{html_file.name}: has JavaScript"
            assert "data-theme" not in html, f"{html_file.name}: has manual theme"
            assert "prefers-color-scheme:dark" in html, f"{html_file.name}: no dark mode"
        print("✓ No JavaScript, theme follows the system!")


def test_template_change_rebuilds_unchanged_posts():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        post = Path(config["posts_dir"]) / "steady.md"
        post.write_text("Date: 2025 Jan 01\n\n# Steady\n\nUnchanged.")
        BlogBuilder(config).build()

        layout = Path(config["templates_dir"]) / "layout.html"
        layout.write_text(layout.read_text().replace("</body>", "<!-- v2 --></body>"))
        BlogBuilder(config).build()

        html = (Path(config["output_dir"]) / "steady.html").read_text()
        assert "<!-- v2 -->" in html, "Template change did not rebuild unchanged post"
        print("✓ Template changes rebuild unchanged posts!")


if __name__ == "__main__":
    test_every_page_has_home_header_and_footer()
    test_internal_links_are_clean()
    test_no_javascript_and_system_theme()
    test_template_change_rebuilds_unchanged_posts()
    print("\n🏴‍☠️ All layout tests passed! ARR!")
