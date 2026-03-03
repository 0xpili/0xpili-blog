#!/usr/bin/env python3

import os
import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blogmaker import BlogBuilder


def _make_config(tmpdir):
    """Create a test config pointing at temp directories."""
    test_posts = Path(tmpdir) / "posts"
    test_templates = Path(tmpdir) / "templates"
    test_output = Path(tmpdir) / "docs"

    test_posts.mkdir(exist_ok=True)
    test_templates.mkdir(exist_ok=True)

    for template in ["base.html", "index.html", "404.html"]:
        src = Path("templates") / template
        if src.exists():
            shutil.copy(src, test_templates / template)

    return {
        "site_url": "https://example.com",
        "site_title": "Test Blog",
        "site_description": "A test blog.",
        "author": "tester",
        "templates_dir": str(test_templates),
        "posts_dir": str(test_posts),
        "output_dir": str(test_output),
        "cache_file": str(Path(tmpdir) / ".build_cache.json"),
        "date_format": "%Y %b %d",
    }


def test_blog_builds_successfully():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])

        (posts / "test-post.md").write_text("""Date: 2025 Jan 01
# Test Post
This is a test.""")

        BlogBuilder(config).build()

        assert (output / "index.html").exists(), "Index not generated"
        assert (output / "404.html").exists(), "404 page not generated"
        assert (output / "test-post.html").exists(), "Post not generated"

        index_content = (output / "index.html").read_text()
        assert "Test Post" in index_content, "Post not listed in index"

        post_content = (output / "test-post.html").read_text()
        assert "This is a test." in post_content, "Post content not rendered"

        print("✓ Blog builds successfully!")


def test_incremental_build():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])

        (posts / "post-one.md").write_text("""Date: 2025 Jan 01
# Post One
First post.""")

        BlogBuilder(config).build()
        first_mtime = (output / "post-one.html").stat().st_mtime

        # Build again — post should be unchanged (cache hit)
        BlogBuilder(config).build()
        second_mtime = (output / "post-one.html").stat().st_mtime
        assert first_mtime == second_mtime, "Unchanged post was rebuilt (cache miss)"

        # Modify post — should trigger rebuild
        (posts / "post-one.md").write_text("""Date: 2025 Jan 01
# Post One
Updated content.""")

        BlogBuilder(config).build()
        third_mtime = (output / "post-one.html").stat().st_mtime
        assert third_mtime > first_mtime, "Modified post was not rebuilt"

        updated_content = (output / "post-one.html").read_text()
        assert "Updated content." in updated_content, "Updated content not in output"

        print("✓ Incremental builds work correctly!")


def test_missing_date_skipped():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])

        (posts / "no-date.md").write_text("""# No Date Post
This post has no date header.""")

        (posts / "valid-post.md").write_text("""Date: 2025 Feb 01
# Valid Post
This one is fine.""")

        BlogBuilder(config).build()

        assert not (output / "no-date.html").exists(), "Post without date should be skipped"
        assert (output / "valid-post.html").exists(), "Valid post should be generated"

        print("✓ Posts without date header are skipped!")


def test_post_sorting():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])

        (posts / "older.md").write_text("""Date: 2025 Jan 01
# Older Post
Old content.""")

        (posts / "newer.md").write_text("""Date: 2025 Dec 15
# Newer Post
New content.""")

        BlogBuilder(config).build()

        index_content = (output / "index.html").read_text()
        newer_pos = index_content.find("Newer Post")
        older_pos = index_content.find("Older Post")
        assert newer_pos < older_pos, "Newer post should appear before older post in index"

        print("✓ Posts are sorted newest-first!")


if __name__ == "__main__":
    test_blog_builds_successfully()
    test_incremental_build()
    test_missing_date_skipped()
    test_post_sorting()
    print("\n🏴‍☠️ All build tests passed! ARR!")