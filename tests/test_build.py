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


def test_header_parser_extracts_date():
    """Header parser extracts Date from 'Date: 2025 Jan 01' line."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "date-test.md").write_text("Date: 2025 Jan 01\n# Date Test\nContent.")
        builder = BlogBuilder(config)
        post = builder._parse_post(posts / "date-test.md")
        assert post is not None, "Post should parse successfully"
        assert post['date'] == "2025 Jan 01", f"Date should be '2025 Jan 01', got '{post['date']}'"
        print("✓ Header parser extracts date correctly!")


def test_header_parser_extracts_title():
    """Header parser extracts Title from '# My Title' line after headers."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "title-test.md").write_text("Date: 2025 Jan 01\n# My Custom Title\nContent.")
        builder = BlogBuilder(config)
        post = builder._parse_post(posts / "title-test.md")
        assert post is not None, "Post should parse successfully"
        assert post['title'] == "My Custom Title", f"Title should be 'My Custom Title', got '{post['title']}'"
        print("✓ Header parser extracts title correctly!")


def test_header_parser_no_title_uses_filename():
    """Header parser uses filename as title when no # heading present."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "my-post-name.md").write_text("Date: 2025 Jan 01\n\nContent without title heading.")
        builder = BlogBuilder(config)
        post = builder._parse_post(posts / "my-post-name.md")
        assert post is not None, "Post should parse successfully"
        assert post['title'] == "My Post Name", f"Title should be 'My Post Name', got '{post['title']}'"
        print("✓ Header parser uses filename as title when no heading!")


def test_header_parser_stops_at_blank_line():
    """Header parser stops at blank line between headers and content."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "blank-line.md").write_text("Date: 2025 Jan 01\n\n# Title After Blank\nContent.")
        builder = BlogBuilder(config)
        post = builder._parse_post(posts / "blank-line.md")
        assert post is not None, "Post should parse successfully"
        assert post['title'] == "Title After Blank", f"Title should be 'Title After Blank', got '{post['title']}'"
        print("✓ Header parser stops at blank line!")


def test_header_parser_stops_at_heading():
    """Header parser stops at '# ' heading line."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "heading-stop.md").write_text("Date: 2025 Jan 01\n# Direct Title\nContent here.")
        builder = BlogBuilder(config)
        post = builder._parse_post(posts / "heading-stop.md")
        assert post is not None, "Post should parse successfully"
        assert post['title'] == "Direct Title", f"Title should be 'Direct Title', got '{post['title']}'"
        print("✓ Header parser stops at heading!")


def test_post_dict_has_draft_and_tags():
    """Post dict includes draft (False) and tags ([]) for forward compatibility."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "forward-compat.md").write_text("Date: 2025 Jan 01\n# Forward Compat\nContent.")
        builder = BlogBuilder(config)
        post = builder._parse_post(posts / "forward-compat.md")
        assert post is not None, "Post should parse successfully"
        assert 'draft' in post, "Post dict should have 'draft' key"
        assert post['draft'] is False, f"draft should be False, got {post['draft']}"
        assert 'tags' in post, "Post dict should have 'tags' key"
        assert post['tags'] == [], f"tags should be [], got {post['tags']}"
        print("✓ Post dict has draft and tags fields!")


def test_all_existing_posts_parse():
    """All 15 existing posts parse successfully."""
    config = {
        "site_url": "https://0xpili.xyz",
        "site_title": "0xpili",
        "site_description": "Test",
        "author": "0xpili",
        "templates_dir": "templates",
        "posts_dir": "posts",
        "output_dir": "docs",
        "cache_file": ".build_cache.json",
        "date_format": "%Y %b %d",
    }
    builder = BlogBuilder(config)
    posts_path = Path(config["posts_dir"])
    post_files = sorted(posts_path.glob("*.md"))
    assert len(post_files) >= 15, f"Expected at least 15 posts, found {len(post_files)}"
    for filepath in post_files:
        post = builder._parse_post(filepath)
        assert post is not None, f"{filepath.name} failed to parse"
        assert post['title'], f"{filepath.name} has empty title"
        assert post['date'], f"{filepath.name} has empty date"
    print(f"✓ All {len(post_files)} existing posts parse successfully!")


if __name__ == "__main__":
    test_blog_builds_successfully()
    test_incremental_build()
    test_missing_date_skipped()
    test_post_sorting()
    test_header_parser_extracts_date()
    test_header_parser_extracts_title()
    test_header_parser_no_title_uses_filename()
    test_header_parser_stops_at_blank_line()
    test_header_parser_stops_at_heading()
    test_post_dict_has_draft_and_tags()
    test_all_existing_posts_parse()
    print("\n🏴‍☠️ All build tests passed! ARR!")