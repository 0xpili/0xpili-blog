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

    for template in ["base.html", "page.html", "index.html", "404.html"]:
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


# --- Image Extraction Edge-Case Tests (QUAL-04) ---


def _make_builder(tmpdir):
    """Create a minimal BlogBuilder for unit testing methods directly."""
    config = _make_config(tmpdir)
    return BlogBuilder(config), config


def test_cover_image_standard():
    """Standard image ![alt](path/to/image.jpg) extracts as cover image."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        lines = ["Date: 2025 Jan 01", "# Title", "Some text", "![photo](images/photo.jpg)", "More text"]
        cover, filtered = builder._extract_cover_image(lines, "test")
        assert cover == "/images/photo.jpg", f"Expected '/images/photo.jpg', got '{cover}'"
        assert "![photo](images/photo.jpg)" not in [l.strip() for l in filtered], "Cover image line should be removed"
        print("✓ Cover image standard extraction works!")


def test_cover_image_empty_alt():
    """Image with empty alt text ![](image.jpg) extracts correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        lines = ["![](image.jpg)"]
        cover, filtered = builder._extract_cover_image(lines, "test")
        assert cover is not None, "Cover image should be extracted even with empty alt"
        assert cover == "/image.jpg", f"Expected '/image.jpg', got '{cover}'"
        print("✓ Cover image with empty alt works!")


def test_cover_image_inline_not_extracted():
    """Inline image within text (not standalone line) is NOT extracted."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        lines = ["Check this ![img](url.jpg) in text"]
        cover, filtered = builder._extract_cover_image(lines, "test")
        assert cover is None, "Inline image should NOT be extracted as cover"
        assert len(filtered) == 1, "Line should be preserved"
        print("✓ Inline image not extracted as cover!")


def test_cover_image_multiple_first_wins():
    """Multiple standalone images -- first becomes cover, rest stay in content."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        lines = ["![first](first.jpg)", "Some text", "![second](second.jpg)"]
        cover, filtered = builder._extract_cover_image(lines, "test")
        assert cover == "/first.jpg", f"First image should be cover, got '{cover}'"
        # Second image should remain in filtered lines
        remaining = [l.strip() for l in filtered]
        assert "![second](second.jpg)" in remaining, "Second image should stay in content"
        assert "![first](first.jpg)" not in remaining, "First image should be removed"
        print("✓ Multiple images: first wins, rest preserved!")


def test_cover_image_none_when_no_images():
    """No images -- returns None, all lines preserved."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        lines = ["Line one", "Line two", "Line three"]
        cover, filtered = builder._extract_cover_image(lines, "test")
        assert cover is None, "Should be None when no images"
        assert len(filtered) == 3, f"All lines should be preserved, got {len(filtered)}"
        print("✓ No images returns None!")


def test_cover_image_http_url():
    """HTTP URL image uses URL as-is (no / prefix)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        lines = ["![alt](https://example.com/img.jpg)"]
        cover, filtered = builder._extract_cover_image(lines, "test")
        assert cover == "https://example.com/img.jpg", f"Expected full URL, got '{cover}'"
        print("✓ HTTP URL image preserved as-is!")


def test_cover_image_relative_path_prefixed():
    """Relative image path gets '/' prefix."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        lines = ["![alt](images/photo.jpg)"]
        cover, filtered = builder._extract_cover_image(lines, "test")
        assert cover.startswith("/"), f"Relative path should start with '/', got '{cover}'"
        assert cover == "/images/photo.jpg", f"Expected '/images/photo.jpg', got '{cover}'"
        print("✓ Relative path gets / prefix!")


# --- Date Parsing Edge-Case Tests (QUAL-05) ---


def test_date_parsing_standard():
    """Standard date 'Date: 2025 Oct 12' parses correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "standard-date.md").write_text("Date: 2025 Oct 12\n# Standard Date\nContent.")
        post = builder._parse_post(posts / "standard-date.md")
        assert post is not None, "Standard date should parse"
        assert post['date'] == "2025 Oct 12", f"Expected '2025 Oct 12', got '{post['date']}'"
        print("✓ Standard date parses correctly!")


def test_date_parsing_ordinal_th():
    """Ordinal suffix 'Date: 2025 May 11th' parses correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "ordinal-th.md").write_text("Date: 2025 May 11th\n# Ordinal Test\nContent.")
        post = builder._parse_post(posts / "ordinal-th.md")
        assert post is not None, "Ordinal th should parse"
        assert post['date'] == "2025 May 11", f"Expected '2025 May 11', got '{post['date']}'"
        print("✓ Ordinal th parses correctly!")


def test_date_parsing_ordinal_st():
    """Ordinal suffix 'Date: 2025 Jan 1st' parses correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "ordinal-st.md").write_text("Date: 2025 Jan 1st\n# Ordinal St\nContent.")
        post = builder._parse_post(posts / "ordinal-st.md")
        assert post is not None, "Ordinal st should parse"
        assert post['date'] == "2025 Jan 01", f"Expected '2025 Jan 01', got '{post['date']}'"
        print("✓ Ordinal st parses correctly!")


def test_date_parsing_ordinal_nd():
    """Ordinal suffix 'Date: 2025 Feb 2nd' parses correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "ordinal-nd.md").write_text("Date: 2025 Feb 2nd\n# Ordinal Nd\nContent.")
        post = builder._parse_post(posts / "ordinal-nd.md")
        assert post is not None, "Ordinal nd should parse"
        assert post['date'] == "2025 Feb 02", f"Expected '2025 Feb 02', got '{post['date']}'"
        print("✓ Ordinal nd parses correctly!")


def test_date_parsing_ordinal_rd():
    """Ordinal suffix 'Date: 2025 Mar 3rd' parses correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "ordinal-rd.md").write_text("Date: 2025 Mar 3rd\n# Ordinal Rd\nContent.")
        post = builder._parse_post(posts / "ordinal-rd.md")
        assert post is not None, "Ordinal rd should parse"
        assert post['date'] == "2025 Mar 03", f"Expected '2025 Mar 03', got '{post['date']}'"
        print("✓ Ordinal rd parses correctly!")


def test_date_missing_returns_none():
    """Post without Date: header returns None."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "no-date.md").write_text("# No Date Here\nJust content.")
        post = builder._parse_post(posts / "no-date.md")
        assert post is None, "Missing date should return None"
        print("✓ Missing date returns None!")


def test_date_invalid_returns_none():
    """Invalid date format 'Date: not-a-date' returns None."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "bad-date.md").write_text("Date: not-a-date\n# Bad Date\nContent.")
        post = builder._parse_post(posts / "bad-date.md")
        assert post is None, "Invalid date should return None"
        print("✓ Invalid date returns None!")


# --- Header Parser Edge-Case Tests ---


def test_header_parser_unknown_key_stops_parsing():
    """Unknown header key stops header parsing -- date after it is not found."""
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "unknown-key.md").write_text("Note: something\nDate: 2025 Jan 01\n# Title\nContent.")
        post = builder._parse_post(posts / "unknown-key.md")
        assert post is None, "Unknown key before Date should stop parsing, returning None"
        print("✓ Unknown header key stops parsing!")


# --- Description Extraction Tests (META-01) ---


def test_description_strips_images():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        result = builder._extract_description("![photo](img.jpg) Some text here that is long enough to not trigger the fallback threshold for short content")
        assert "img.jpg" not in result
        assert "Some text here" in result
        print("✓ Description strips images!")


def test_description_strips_links_keeps_text():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        result = builder._extract_description("Check out [this link](https://example.com) for more details about the topic we are discussing in this paragraph")
        assert "https://example.com" not in result
        assert "this link" in result
        print("✓ Description strips links, keeps text!")


def test_description_strips_bold_italic():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        result = builder._extract_description("This is **bold** and *italic* and ~~struck~~ text in a paragraph that is long enough to pass the threshold")
        assert "**" not in result
        assert "~~" not in result
        assert "bold" in result and "italic" in result and "struck" in result
        print("✓ Description strips bold/italic/strikethrough!")


def test_description_strips_headings_blockquotes():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        result = builder._extract_description("## Heading\n> A quote from someone notable\nNormal text that continues the paragraph with enough content to pass threshold")
        assert "#" not in result
        assert ">" not in result
        assert "Heading" in result and "A quote" in result
        print("✓ Description strips headings and blockquotes!")


def test_description_strips_code():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        result = builder._extract_description("Use `print()` or:\n```python\ncode\n```\nMore text follows here with enough content to pass the minimum threshold for descriptions")
        assert "```" not in result
        assert "`" not in result
        assert "More text" in result
        print("✓ Description strips code!")


def test_description_truncates_at_word_boundary():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        long_text = "word " * 50
        result = builder._extract_description(long_text)
        assert result.endswith("...")
        assert len(result) <= 165
        print("✓ Description truncates at word boundary!")


def test_description_short_text_no_truncation():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        text = "Short text here that is meaningful enough to use and passes the minimum threshold easily."
        result = builder._extract_description(text)
        assert not result.endswith("...")
        assert "Short text here" in result
        print("✓ Short description not truncated!")


def test_description_empty_falls_back():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        result = builder._extract_description("")
        assert result == builder.config["site_description"]
        print("✓ Empty content falls back to site description!")


def test_description_real_post_content():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        text = """## The Future of Agents

> "The most important thing is to have smart people."

Building **autonomous agents** requires understanding [orchestration](https://example.com/orch) patterns.

```python
def run_agent():
    pass
```

The key insight is that agents need both ~~simple~~ *sophisticated* tooling and clear goals."""
        result = builder._extract_description(text)
        assert "#" not in result
        assert "**" not in result
        assert "```" not in result
        assert "example.com" not in result
        assert "orchestration" in result
        print("✓ Description handles real post content!")


def test_built_post_has_meta_description():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "desc-test.md").write_text("Date: 2025 Jan 01\n# Description Test Post\nThis is my test post about interesting topics that should appear in the meta description tag.")
        BlogBuilder(config).build()
        post_html = (output / "desc-test.html").read_text()
        assert 'meta name="description"' in post_html
        assert "interesting topics" in post_html
        print("✓ Built post has meta description!")


def test_built_page_has_meta_description():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        config["pages_dir"] = str(Path(tmpdir) / "pages")
        pages = Path(config["pages_dir"])
        pages.mkdir()
        output = Path(config["output_dir"])
        (pages / "about.md").write_text("# About Me\nI write about technology, privacy, and the human condition. This is my personal blog where I share thoughts.")
        BlogBuilder(config).build()
        page_html = (output / "about.html").read_text()
        assert 'meta name="description"' in page_html
        assert "technology" in page_html
        print("✓ Built page has meta description!")


# --- Draft Support Tests (DRFT-01, DRFT-02) ---


def test_draft_post_excluded_from_output():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "secret-draft.md").write_text("Date: 2025 Mar 01\nDraft: true\n# Secret Draft\nThis should not be published.")
        BlogBuilder(config).build()
        assert not (output / "secret-draft.html").exists()
        print("✓ Draft post excluded from output!")


def test_draft_case_insensitive():
    for value in ["true", "True", "TRUE"]:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = _make_config(tmpdir)
            posts = Path(config["posts_dir"])
            output = Path(config["output_dir"])
            (posts / "draft-post.md").write_text(f"Date: 2025 Mar 01\nDraft: {value}\n# Draft {value}\nContent.")
            BlogBuilder(config).build()
            assert not (output / "draft-post.html").exists()
    print("✓ Draft case-insensitive parsing works!")


def test_draft_excluded_from_index():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "published.md").write_text("Date: 2025 Mar 01\n# Published Post\nVisible content.")
        (posts / "hidden-draft.md").write_text("Date: 2025 Mar 02\nDraft: true\n# Hidden Draft\nSecret content.")
        BlogBuilder(config).build()
        index_content = (output / "index.html").read_text()
        assert "Published Post" in index_content
        assert "Hidden Draft" not in index_content
        print("✓ Draft post excluded from index!")


def test_non_draft_builds_normally():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "normal-post.md").write_text("Date: 2025 Mar 01\n# Normal Post\nRegular content.")
        BlogBuilder(config).build()
        assert (output / "normal-post.html").exists()
        print("✓ Non-draft post builds normally!")


def test_stale_draft_cleanup():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "evolving-post.md").write_text("Date: 2025 Mar 01\n# Evolving Post\nPublished content.")
        BlogBuilder(config).build()
        assert (output / "evolving-post.html").exists()
        (posts / "evolving-post.md").write_text("Date: 2025 Mar 01\nDraft: true\n# Evolving Post\nNow a draft.")
        BlogBuilder(config).build()
        assert not (output / "evolving-post.html").exists()
        print("✓ Stale draft cleanup works!")


# --- Tag System Tests (TAGS-01, TAGS-02, TAGS-03) ---


def test_tag_parsing_from_header():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "tagged.md").write_text("Date: 2025 Jan 01\nTags: crypto, ai\n# Tagged Post\nContent.")
        post = builder._parse_post(posts / "tagged.md")
        assert post['tags'] == ['crypto', 'ai']
        print("✓ Tags parsed from header!")


def test_tag_whitespace_and_case():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "messy-tags.md").write_text("Date: 2025 Jan 01\nTags:  Crypto , AI , Philosophy \n# Messy Tags\nContent.")
        post = builder._parse_post(posts / "messy-tags.md")
        assert post['tags'] == ['crypto', 'ai', 'philosophy']
        print("✓ Tags whitespace-trimmed and lowercased!")


def test_no_tags_empty_list():
    with tempfile.TemporaryDirectory() as tmpdir:
        builder, config = _make_builder(tmpdir)
        posts = Path(config["posts_dir"])
        (posts / "no-tags.md").write_text("Date: 2025 Jan 01\n# No Tags\nContent.")
        post = builder._parse_post(posts / "no-tags.md")
        assert post['tags'] == []
        print("✓ No tags header gives empty list!")


def test_tags_displayed_on_post():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "tagged-post.md").write_text("Date: 2025 Jan 01\nTags: crypto, ai\n# Tagged Post\nSome content here.")
        BlogBuilder(config).build()
        post_html = (output / "tagged-post.html").read_text()
        assert "tag-crypto.html" in post_html
        assert "tag-ai.html" in post_html
        print("✓ Tags displayed on post page!")


def test_tag_index_pages_generated():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "post1.md").write_text("Date: 2025 Jan 01\nTags: crypto\n# Crypto Post\nAbout crypto.")
        (posts / "post2.md").write_text("Date: 2025 Feb 01\nTags: crypto, ai\n# Both Post\nAbout both.")
        BlogBuilder(config).build()
        assert (output / "tag-crypto.html").exists()
        assert (output / "tag-ai.html").exists()
        crypto_page = (output / "tag-crypto.html").read_text()
        assert "Posts tagged: crypto" in crypto_page
        assert "Crypto Post" in crypto_page
        assert "Both Post" in crypto_page
        ai_page = (output / "tag-ai.html").read_text()
        assert "Both Post" in ai_page
        assert "Crypto Post" not in ai_page
        print("✓ Tag index pages generated correctly!")


def test_tag_pages_exclude_drafts():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "pub.md").write_text("Date: 2025 Jan 01\nTags: crypto\n# Published\nContent.")
        (posts / "draft.md").write_text("Date: 2025 Feb 01\nTags: crypto\nDraft: true\n# Draft\nSecret.")
        BlogBuilder(config).build()
        crypto_page = (output / "tag-crypto.html").read_text()
        assert "Published" in crypto_page
        assert "Draft" not in crypto_page
        print("✓ Tag pages exclude drafts!")


def test_stale_tag_pages_cleaned():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "post.md").write_text("Date: 2025 Jan 01\nTags: crypto\n# Post\nContent.")
        BlogBuilder(config).build()
        assert (output / "tag-crypto.html").exists()
        (posts / "post.md").write_text("Date: 2025 Jan 01\nTags: ai\n# Post\nContent.")
        BlogBuilder(config).build()
        assert not (output / "tag-crypto.html").exists()
        assert (output / "tag-ai.html").exists()
        print("✓ Stale tag pages cleaned up!")


def test_tag_pages_sorted_newest_first():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "older.md").write_text("Date: 2025 Jan 01\nTags: crypto\n# Older Post\nContent.")
        (posts / "newer.md").write_text("Date: 2025 Mar 01\nTags: crypto\n# Newer Post\nContent.")
        BlogBuilder(config).build()
        crypto_page = (output / "tag-crypto.html").read_text()
        newer_pos = crypto_page.find("Newer Post")
        older_pos = crypto_page.find("Older Post")
        assert newer_pos < older_pos
        print("✓ Tag pages sorted newest-first!")


# --- RSS Feed Tests (RSS-01) ---


def test_rss_feed_generated():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "post1.md").write_text("Date: 2025 Jan 01\n# First Post\nSome content about the first post that is long enough to generate a proper description for the feed.")
        (posts / "post2.md").write_text("Date: 2025 Feb 01\n# Second Post\nMore content about the second post that is also long enough to generate a proper description.")
        BlogBuilder(config).build()
        assert (output / "feed.xml").exists()
        print("✓ RSS feed.xml generated!")


def test_rss_feed_valid_xml():
    import xml.etree.ElementTree as ET
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "post1.md").write_text("Date: 2025 Jan 01\n# XML Test Post\nContent that is long enough for description generation in the RSS feed items.")
        BlogBuilder(config).build()
        tree = ET.parse(output / "feed.xml")
        root = tree.getroot()
        assert root.tag == "rss"
        assert root.get("version") == "2.0"
        channel = root.find("channel")
        assert channel is not None
        assert channel.find("title").text == config["site_title"]
        items = channel.findall("item")
        assert len(items) == 1
        assert items[0].find("title").text == "XML Test Post"
        assert items[0].find("link") is not None
        assert items[0].find("description") is not None
        assert items[0].find("pubDate") is not None
        print("✓ RSS feed is valid XML with correct structure!")


def test_rss_feed_excludes_drafts():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "pub.md").write_text("Date: 2025 Jan 01\n# Published RSS\nContent for the RSS feed that is long enough for proper descriptions.")
        (posts / "draft.md").write_text("Date: 2025 Feb 01\nDraft: true\n# Draft RSS\nSecret content that should not appear.")
        BlogBuilder(config).build()
        feed_content = (output / "feed.xml").read_text()
        assert "Published RSS" in feed_content
        assert "Draft RSS" not in feed_content
        print("✓ RSS feed excludes drafts!")


def test_rss_feed_has_rfc822_dates():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])
        (posts / "dated.md").write_text("Date: 2025 Mar 15\n# Dated Post\nContent for testing RFC 822 date format in the RSS feed items.")
        BlogBuilder(config).build()
        feed_content = (output / "feed.xml").read_text()
        assert "Sat, 15 Mar 2025" in feed_content
        print("✓ RSS feed has RFC 822 dates!")


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
    # Image extraction edge cases (QUAL-04)
    test_cover_image_standard()
    test_cover_image_empty_alt()
    test_cover_image_inline_not_extracted()
    test_cover_image_multiple_first_wins()
    test_cover_image_none_when_no_images()
    test_cover_image_http_url()
    test_cover_image_relative_path_prefixed()
    # Date parsing edge cases (QUAL-05)
    test_date_parsing_standard()
    test_date_parsing_ordinal_th()
    test_date_parsing_ordinal_st()
    test_date_parsing_ordinal_nd()
    test_date_parsing_ordinal_rd()
    test_date_missing_returns_none()
    test_date_invalid_returns_none()
    # Header parser edge cases
    test_header_parser_unknown_key_stops_parsing()
    # Description extraction (META-01)
    test_description_strips_images()
    test_description_strips_links_keeps_text()
    test_description_strips_bold_italic()
    test_description_strips_headings_blockquotes()
    test_description_strips_code()
    test_description_truncates_at_word_boundary()
    test_description_short_text_no_truncation()
    test_description_empty_falls_back()
    test_description_real_post_content()
    test_built_post_has_meta_description()
    test_built_page_has_meta_description()
    # Draft support (DRFT-01, DRFT-02)
    test_draft_post_excluded_from_output()
    test_draft_case_insensitive()
    test_draft_excluded_from_index()
    test_non_draft_builds_normally()
    test_stale_draft_cleanup()
    # Tag system (TAGS-01, TAGS-02, TAGS-03)
    test_tag_parsing_from_header()
    test_tag_whitespace_and_case()
    test_no_tags_empty_list()
    test_tags_displayed_on_post()
    test_tag_index_pages_generated()
    test_tag_pages_exclude_drafts()
    test_stale_tag_pages_cleaned()
    test_tag_pages_sorted_newest_first()
    # RSS feed (RSS-01)
    test_rss_feed_generated()
    test_rss_feed_valid_xml()
    test_rss_feed_excludes_drafts()
    test_rss_feed_has_rfc822_dates()
    print("\n🏴‍☠️ All build tests passed! ARR!")