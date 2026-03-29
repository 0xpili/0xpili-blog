# Coding Conventions

**Analysis Date:** 2026-03-29

## Naming Patterns

**Files:**
- Python modules: lowercase with underscores (`blogmaker.py`, `test_build.py`, `test_quality.py`)
- Markdown posts: lowercase with hyphens (`agentfi.md`, `hiring-is-broken.md`, `crypto-without-privacy-is-half-finished.md`)
- HTML output: lowercase slug format from filename stem, hyphens for spacing

**Functions:**
- Snake case: `_parse_post()`, `_extract_cover_image()`, `_needs_rebuild()`, `_load_cache()`
- Leading underscore for private methods: `_file_hash()`, `_save_cache()`
- Test functions prefixed with `test_`: `test_blog_builds_successfully()`, `test_incremental_build()`
- Helper functions prefixed with underscore in tests: `_make_config()`

**Variables:**
- Snake case for all variables: `html_file`, `date_str`, `cover_image`, `posts_path`
- Configuration constants: `CONFIG` (all caps), nested dicts with string keys
- Loop variables use descriptive names: `for filepath in posts_path.glob("*.md"):`

**Types:**
- Type hints on function signatures: `def _parse_post(self, filepath: Path) -> Optional[Dict]:`
- Use `Optional`, `Dict`, `List`, `Tuple` from `typing` module
- Return type annotations always specified in method signatures
- Parameter types always annotated

## Code Style

**Formatting:**
- Python 3 style (modern)
- 4-space indentation
- No auto-formatter configured (rely on manual adherence)
- No linter configuration file (style is by convention)
- Whitespace: blank lines between method definitions in classes (single blank line)
- Line length: observed ~100 chars typical, no hard limit enforced

**Linting:**
- No linter configured (no `.eslintrc`, `.pylintrc`, or `setup.cfg`)
- No formatter configured (no `.prettierrc` or `black.toml`)
- Style enforced by convention and code review

## Import Organization

**Order:**
1. Standard library imports (`os`, `sys`, `json`, `hashlib`, `http.server`, `socketserver`)
2. Third-party imports (`markdown2`, `jinja2`)
3. Local imports (`from blogmaker import BlogBuilder`, `from pathlib import Path`)

**Path Aliases:**
- No path aliases used
- Direct imports: `from pathlib import Path`, `from typing import Dict, List, Optional, Tuple`
- Relative imports in tests: `sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))` to enable `from blogmaker import BlogBuilder`

**Examples from codebase:**
```python
# blogmaker.py
import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

try:
    import markdown2
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    print("Error: Required dependencies not found.")
    sys.exit(1)
```

## Error Handling

**Patterns:**
- Graceful degradation: Missing cache returns empty dict (`except: return {}`)
- Try-except with specific exception types: `except ValueError:`, `except ImportError:`
- Bare `except:` used sparingly (cache loading fallback)
- Print warnings to stdout for non-fatal issues: `print(f"Warning: {filepath.name} missing date header")`
- Print errors with context: `print(f"Error parsing {filepath.name}: {e}")`
- Silent failures acceptable for unchanged posts (cache hit): prints informational message instead
- System exit on critical failures: `sys.exit(1)` when dependencies missing

**Examples:**
```python
# Specific exception handling
try:
    date_obj = datetime.strptime(clean_date, self.config["date_format"])
except ValueError:
    print(f"Warning: Invalid date format in {filepath.name}: {date_str}")
    return None

# Graceful fallback for non-critical failures
def _load_cache(self) -> Dict[str, str]:
    cache_path = Path(self.config["cache_file"])
    if cache_path.exists():
        try:
            with open(cache_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

# Build continues with partial success
try:
    html = post_template.render(...)
    output_file.write_text(html, encoding='utf-8')
    print(f"  ✓ {post['title']}")
except Exception as e:
    print(f"  ✗ Error building {post['title']}: {e}")
    # Build continues with next post
```

## Logging

**Framework:** No dedicated logging framework; uses `print()` for all output

**Patterns:**
- Informational messages: `print("Building blog...")`, `print(f"  ✓ {post['title']}")`
- Warnings: `print(f"Warning: {filepath.name} missing date header")`
- Errors: `print(f"Error parsing {filepath.name}: {e}")`
- Indented output for nested progress: `print(f"  ✓ Index page")`
- Test output uses checkmarks and symbols: `print("✓ Blog builds successfully!")`, `print("❌ Quality issues found:")`
- Progress tracking with status symbols: `✓` (success), `✗` (error), `-` (unchanged), `🏴‍☠️` (festive)

**Test output examples from `test_quality.py`:**
```python
print("❌ Quality issues found:")
for error in errors:
    print(f"  - {error}")

print("✓ HTML quality: Excellent")
print("🏆 All quality tests passed!")
```

## Comments

**When to Comment:**
- Comments are minimal — code is self-documenting
- No docstrings observed in source code
- Inline comments used sparingly for non-obvious logic
- Regex pattern comment in test: `# The inline theme-toggle script is intentional — match it so we can allow it`

**JSDoc/TSDoc:**
- Not used (Python project, no TypeScript)
- Type hints preferred over doc comments for parameter documentation

**Example of minimal comment:**
```python
# Size budgets account for ~8KB of inlined CSS per page
if html_file.name == "index.html" and size_kb > 10:
    errors.append(f"{html_file.name}: Too large ({size_kb:.1f}KB, limit 10KB)")
```

## Function Design

**Size:** Methods typically 5-40 lines, favoring conciseness
- `_file_hash()`: 4 lines
- `_extract_cover_image()`: 18 lines
- `_parse_post()`: 57 lines (larger, complex logic)
- `build()`: 90 lines (orchestration method, longest in codebase)

**Parameters:**
- Keep to 2-3 parameters max
- Use dict unpacking when passing multiple config values: `self.config["key"]`
- Single responsibility: `_parse_post()` does one thing — parse markdown + extract metadata

**Return Values:**
- Explicit return type hints always present
- Return `None` for failure cases gracefully: `return None` instead of raising
- Return dicts or typed objects: `return { 'title': title, 'slug': slug, ... }`
- Return tuples for multiple values: `Tuple[Optional[str], List[str]]`

**Examples:**
```python
def _file_hash(self, filepath: Path) -> str:
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]

def _needs_rebuild(self, post: Dict) -> bool:
    cached_hash = self.cache.get(post['filepath'])
    output_file = Path(self.config["output_dir"]) / f"{post['slug']}.html"
    return cached_hash != post['hash'] or not output_file.exists()

def _extract_cover_image(self, lines: List[str], slug: str) -> Tuple[Optional[str], List[str]]:
    cover_image = None
    filtered_lines = []
    # ... logic ...
    return cover_image, filtered_lines
```

## Module Design

**Exports:**
- `BlogBuilder` class is main public export from `blogmaker.py`
- `CONFIG` dict is mutable and can be overridden via environment variables before instantiation
- `main()` function is entry point when run directly: `if __name__ == "__main__": main()`

**Class Structure:**
- Single public method: `build()` — orchestrates entire build process
- All other methods private (prefixed with `_`): `_load_cache()`, `_parse_post()`, etc.
- Constructor takes config dict, initializes cache and Jinja environment
- No inheritance or mixins used (simple, single-purpose class)

**File Organization:**
- No barrel files or re-exports
- Each test file is standalone with helper functions (e.g., `_make_config()`)
- Tests import directly from `blogmaker`: `from blogmaker import BlogBuilder`

**Configuration as Dictionary:**
```python
CONFIG = {
    "site_url": "https://0xpili.xyz",
    "site_title": "0xpili",
    "author": "0xpili",
    "templates_dir": "templates",
    "posts_dir": "posts",
    "pages_dir": "pages",
    "output_dir": "docs",
    "cache_file": ".build_cache.json",
    "date_format": "%Y %b %d",
}

# Overridden by environment variables before instantiation
for key in CONFIG:
    env_key = f"BLOG_{key.upper()}"
    if env_key in os.environ:
        CONFIG[key] = os.environ[env_key]
```

---

*Convention analysis: 2026-03-29*
