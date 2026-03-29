# Testing Patterns

**Analysis Date:** 2026-03-29

## Test Framework

**Runner:**
- Python 3 built-in unittest-style (no external test runner framework)
- Tests are plain Python scripts executed directly with `python3`
- No pytest, unittest module imports, or nose — just raw functions with assertions

**Assertion Library:**
- Python built-in `assert` statements
- No external assertion library (pytest, nose, unittest.TestCase)
- Format: `assert condition, "error message"`

**Run Commands:**
```bash
python3 tests/test_quality.py      # Run quality checks (HTML, performance, accessibility)
python3 tests/test_build.py        # Run build system tests (parsing, caching, rendering)
python3 tests/test_quality.py && python3 tests/test_build.py  # Run all tests
```

## Test File Organization

**Location:**
- Co-located in `tests/` directory
- Separate from source code (`blogmaker.py` stays in project root)
- Two primary test files: `test_quality.py`, `test_build.py`

**Naming:**
- `test_*.py` convention for test files
- `test_function_name()` for test functions
- Helper functions prefixed with underscore: `_make_config()`

**Structure:**
```
tests/
├── test_build.py      # BlogBuilder functionality tests
└── test_quality.py    # HTML output quality checks
```

## Test Structure

**Suite Organization:**

From `test_build.py`:
```python
if __name__ == "__main__":
    test_blog_builds_successfully()
    test_incremental_build()
    test_missing_date_skipped()
    test_post_sorting()
    test_about_page_generated()
    test_pages_without_date_header()
    print("\n🏴‍☠️ All build tests passed! ARR!")
```

From `test_quality.py`:
```python
def main():
    print("Running quality tests...\n")

    results = [
        test_html_quality(),
        test_performance(),
        test_accessibility(),
    ]

    if all(results):
        print("\n🏆 All quality tests passed!")
    else:
        print("\n⚠️  Some tests failed. Fix issues and run again.")
        sys.exit(1)
```

**Patterns:**
- **Setup:** Create temporary directories and configs before each test
- **Execution:** Build blog or check output with test data
- **Assertion:** Use `assert condition, "message"` to validate
- **Teardown:** Automatic via `tempfile.TemporaryDirectory()` context manager
- **Reporting:** Print success/failure messages, exit with `sys.exit(1)` on failure

## Mocking

**Framework:** No mocking framework (no unittest.mock, pytest-mock, etc.)

**Patterns:**
- Use real temporary directories instead of mocks: `tempfile.TemporaryDirectory()`
- Copy real template files into test environment: `shutil.copy(src, test_templates / template)`
- Create minimal test data in-memory: write test markdown files to temp dirs
- No stubbing or patching — tests use actual `BlogBuilder` class

**Example from `test_build.py`:**
```python
def _make_config(tmpdir):
    """Create a test config pointing at temp directories."""
    test_posts = Path(tmpdir) / "posts"
    test_templates = Path(tmpdir) / "templates"
    test_output = Path(tmpdir) / "docs"

    test_posts.mkdir(exist_ok=True)
    test_templates.mkdir(exist_ok=True)

    # Copy real templates into test environment
    for template in ["base.html", "index.html", "404.html", "page.html"]:
        src = Path("templates") / template
        if src.exists():
            shutil.copy(src, test_templates / template)

    return {
        "site_url": "https://example.com",
        "site_title": "Test Blog",
        # ... rest of config ...
    }
```

**What to Mock:**
- Nothing — tests use real files and real `BlogBuilder`

**What NOT to Mock:**
- Template rendering (use real Jinja2)
- File I/O (use real temp directories)
- Markdown parsing (use real markdown2)

## Fixtures and Factories

**Test Data:**
```python
# Test post fixture pattern
(posts / "test-post.md").write_text("""Date: 2025 Jan 01
# Test Post
This is a test.""")

# Test configuration factory
def _make_config(tmpdir):
    # ... creates complete test config dict ...
    return {
        "site_url": "https://example.com",
        "site_title": "Test Blog",
        "site_description": "A test blog.",
        "author": "tester",
        "templates_dir": str(test_templates),
        "posts_dir": str(test_posts),
        "pages_dir": str(Path(tmpdir) / "pages"),
        "output_dir": str(test_output),
        "cache_file": str(Path(tmpdir) / ".build_cache.json"),
        "date_format": "%Y %b %d",
    }
```

**Location:**
- Helper functions in same test file: `_make_config()` defined in `test_build.py`
- Test data created inline within test functions using `Path.write_text()`
- No separate fixtures directory or external data files

## Coverage

**Requirements:** No coverage enforcement (no `.coveragerc`, no CI coverage gates)

**View Coverage:** Not automated — manual inspection only

## Test Types

**Unit Tests:**
- Scope: Individual methods and functions of `BlogBuilder` class
- Approach: Test in isolation with minimal dependencies
- Examples: `test_blog_builds_successfully()`, `test_incremental_build()`, `test_missing_date_skipped()`
- Use real code paths, not mocks

**Integration Tests:**
- Scope: Full blog build pipeline with real Jinja2 and markdown2
- Approach: Use temporary filesystem, real templates, actual rendering
- Examples: `test_about_page_generated()`, `test_pages_without_date_header()`
- Validates end-to-end workflow

**Quality Tests:**
- Scope: Generated HTML output validation
- Approach: Check file sizes, HTML structure, accessibility, performance
- Examples: `test_html_quality()`, `test_performance()`, `test_accessibility()`
- Non-functional test suite (checks attributes of output, not input/output mapping)

**E2E Tests:**
- Not explicitly separated — integration tests serve this purpose
- Full blog builds from markdown to HTML with real dependencies

## Common Patterns

**Async Testing:**
- Not applicable (Python 3 synchronous code, no async/await)

**Error Testing:**
```python
def test_missing_date_skipped():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])

        # Create post without required Date header
        (posts / "no-date.md").write_text("""# No Date Post
This post has no date header.""")

        # Create valid post
        (posts / "valid-post.md").write_text("""Date: 2025 Feb 01
# Valid Post
This one is fine.""")

        BlogBuilder(config).build()

        # Assert invalid post was skipped
        assert not (output / "no-date.html").exists(), "Post without date should be skipped"
        # Assert valid post was built
        assert (output / "valid-post.html").exists(), "Valid post should be generated"

        print("✓ Posts without date header are skipped!")
```

**File Existence Testing:**
```python
def test_blog_builds_successfully():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])

        (posts / "test-post.md").write_text("""Date: 2025 Jan 01
# Test Post
This is a test.""")

        BlogBuilder(config).build()

        # Assert output files exist
        assert (output / "index.html").exists(), "Index not generated"
        assert (output / "404.html").exists(), "404 page not generated"
        assert (output / "test-post.html").exists(), "Post not generated"

        # Assert content correctness
        index_content = (output / "index.html").read_text()
        assert "Test Post" in index_content, "Post not listed in index"

        post_content = (output / "test-post.html").read_text()
        assert "This is a test." in post_content, "Post content not rendered"

        print("✓ Blog builds successfully!")
```

**Incremental Build Testing (Cache Behavior):**
```python
def test_incremental_build():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _make_config(tmpdir)
        posts = Path(config["posts_dir"])
        output = Path(config["output_dir"])

        (posts / "post-one.md").write_text("""Date: 2025 Jan 01
# Post One
First post.""")

        # First build
        BlogBuilder(config).build()
        first_mtime = (output / "post-one.html").stat().st_mtime

        # Second build — file should not be touched if content unchanged
        BlogBuilder(config).build()
        second_mtime = (output / "post-one.html").stat().st_mtime
        assert first_mtime == second_mtime, "Unchanged post was rebuilt (cache miss)"

        # Modify content and rebuild
        (posts / "post-one.md").write_text("""Date: 2025 Jan 01
# Post One
Updated content.""")

        BlogBuilder(config).build()
        third_mtime = (output / "post-one.html").stat().st_mtime
        assert third_mtime > first_mtime, "Modified post was not rebuilt"

        # Assert updated content in output
        updated_content = (output / "post-one.html").read_text()
        assert "Updated content." in updated_content, "Updated content not in output"

        print("✓ Incremental builds work correctly!")
```

**Ordering/Sorting Test:**
```python
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
```

**Quality Metrics Testing:**
```python
def test_html_quality():
    docs = Path("docs")
    if not docs.exists():
        print("Run 'python3 blogmaker.py' first")
        return False

    errors = []

    for html_file in docs.glob("*.html"):
        content = html_file.read_text()

        # Check for forbidden patterns
        if "fonts.googleapis.com" in content:
            errors.append(f"{html_file.name}: External font dependency")

        if 'style="' in content:
            errors.append(f"{html_file.name}: Inline styles found")

        # Check size budgets
        size_kb = html_file.stat().st_size / 1024
        if html_file.name == "index.html" and size_kb > 10:
            errors.append(f"{html_file.name}: Too large ({size_kb:.1f}KB, limit 10KB)")
        elif html_file.name == "404.html" and size_kb > 3:
            errors.append(f"{html_file.name}: Too large ({size_kb:.1f}KB, limit 3KB)")
        elif size_kb > 25:
            errors.append(f"{html_file.name}: Too large ({size_kb:.1f}KB, limit 25KB)")

        # Check accessibility requirements
        if "<meta name=\"viewport\"" not in content:
            errors.append(f"{html_file.name}: Missing viewport meta")

    if errors:
        print("❌ Quality issues found:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✓ HTML quality: Excellent")
        return True
```

---

*Testing analysis: 2026-03-29*
