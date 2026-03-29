# Phase 1: Foundation and Meta - Research

**Researched:** 2026-03-29
**Domain:** Python static site generator refactoring -- header parsing, meta descriptions, code quality
**Confidence:** HIGH

## Summary

This phase refactors the core `_parse_post()` method in `blogmaker.py` to use loop-based header parsing instead of index-based line access, adds auto-generated meta descriptions to every post, fixes code quality issues (bare except, string-based image detection), and adds comprehensive edge-case tests. The entire scope is within a single ~283-line Python file and its test files.

The codebase is small, well-understood, and has zero external dependencies beyond `markdown2` and `jinja2`. All 15 existing posts follow a consistent format: `Date:` on line 1, optional `# Title` on line 2, then content. One post (`how-athletics-shape-your-best-self.md`) uses an ordinal suffix (`May 11th`) which the existing ordinal-stripping logic already handles. No posts currently have cover images (all return `cover_image=None`). The template plumbing for `{{ description }}` already exists in `base.html` and `page.html` -- it just receives `None` today.

**Primary recommendation:** Refactor header parser first (it unblocks Phase 2's Draft/Tags headers), then add meta description extraction, then fix code quality issues -- all with tests written before implementation changes.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Parse headers as `Key: Value` lines until the first blank line or first `# ` heading. This replaces the current index-based approach (`lines[0]` for Date, `lines[1]` for Title).
- **D-02:** The parser must be backward-compatible -- all 15 existing posts must build identically before and after the refactor.
- **D-03:** Supported headers for now: `Date:`, `Draft:`, `Tags:`. Title remains extracted from the first `# ` heading after the header block.
- **D-04:** Extract description from raw markdown text (not rendered HTML). Strip markdown syntax (links, images, bold, italic, code) to get plain text, then truncate to ~160 characters at a word boundary.
- **D-05:** Populate the existing `description` parameter in template render calls (currently `None`). Templates already have `{{ description }}` plumbing.
- **D-06:** Replace string-based image detection with a regex pattern matching `![alt](url)`. Only standard inline image syntax -- no reference-style images (not used in any existing post).
- **D-07:** Replace bare `except:` in `_load_cache()` with `except (json.JSONDecodeError, IOError):`.

### Claude's Discretion
- Exact regex pattern for image extraction
- How to strip markdown syntax from description text (regex vs simple replacements)
- Test structure and organization within test files

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| QUAL-01 | Fix bare `except:` to specific exception types | Direct code change at line 50 of blogmaker.py; change to `except (json.JSONDecodeError, IOError):` per D-07 |
| QUAL-02 | Replace string-based image extraction with regex | Rewrite `_extract_cover_image()` using regex per D-06; pattern and edge cases documented below |
| QUAL-03 | Refactor header parser from index-based to loop-based | Rewrite `_parse_post()` header section per D-01/D-03; architecture pattern documented below |
| QUAL-04 | Add tests for cover image extraction edge cases | Test cases documented in Pitfalls section; no existing posts have cover images so this is pure edge-case testing |
| QUAL-05 | Add tests for date parsing edge cases | Ordinal suffixes, invalid formats, missing dates; one real post uses ordinals (`May 11th`) |
| META-01 | Auto-generate description from first ~160 chars of post markdown content | New `_extract_description()` method; markdown stripping approach documented below |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.x (system) | Runtime | Already in use |
| markdown2 | (installed) | Markdown to HTML | Already a project dependency |
| jinja2 | (installed) | Template rendering | Already a project dependency |
| re (stdlib) | N/A | Regex for image extraction and markdown stripping | No new dependency needed |
| json (stdlib) | N/A | Cache file loading (for exception type fix) | Already imported |

### Supporting
No new libraries needed. This phase uses only Python stdlib `re` module (already imported in test_quality.py, needs import in blogmaker.py).

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Regex markdown stripping | `markdown2` then strip HTML | More fragile, more complex -- D-04 explicitly says use raw markdown |
| Custom header parser | YAML frontmatter (`---` delimited) | Would change post format, violate D-01's `Key: Value` approach |

## Architecture Patterns

### Current Code Structure (relevant sections)

```
blogmaker.py (283 lines)
  Line 44-51:  _load_cache()     -- bare except to fix (QUAL-01)
  Line 62-118: _parse_post()     -- header parser to refactor (QUAL-03)
  Line 120-141: _extract_cover_image() -- string-based to regex (QUAL-02)
  Line 208-215: build() render   -- description=None to populate (META-01)

tests/
  test_build.py   -- 6 existing tests, extend for new edge cases
  test_quality.py -- quality checks (HTML size, accessibility, etc.)
```

### Pattern 1: Loop-Based Header Parser
**What:** Replace index-based `lines[0]`/`lines[1]` access with a loop that consumes `Key: Value` lines until hitting a blank line, `# ` heading, or non-header line.
**When to use:** Always -- this is the D-01 locked decision.
**Example:**
```python
# Parse header block: Key: Value lines until blank line or heading
headers = {}
i = 0
while i < len(lines):
    line = lines[i].strip()
    if not line or line.startswith('#'):
        break
    if ':' in line:
        key, _, value = line.partition(':')
        key = key.strip().lower()
        headers[key] = value.strip()
        i += 1
    else:
        break

# Extract known headers with defaults
date_str = headers.get('date')
if not date_str:
    print(f"Warning: {filepath.name} missing date header")
    return None

# Parse title from first # heading (if present)
if i < len(lines) and lines[i].strip().startswith('# '):
    title = lines[i].strip()[2:].strip()
    i += 1
else:
    title = filepath.stem.replace('-', ' ').title()

start_line = i
```

**Critical detail:** The `partition(':')` approach handles values that contain colons (e.g., a future `Source: https://example.com`). The `split(':', 1)` approach from ARCHITECTURE.md also works. Both are safe.

**Critical detail:** `Draft:` and `Tags:` headers are parsed here for future use by Phase 2 but are NOT consumed in Phase 1's rendering. Store them in the post dict with defaults (`draft=False`, `tags=[]`) so the dict shape is forward-compatible.

### Pattern 2: Markdown-to-Plain-Text Description Extraction
**What:** Strip markdown syntax from raw content, take first ~160 chars at word boundary.
**When to use:** For every post and page during parsing.
**Example:**
```python
import re

def _extract_description(self, markdown_text: str) -> str:
    """Extract plain text description from markdown, ~160 chars."""
    text = markdown_text

    # Remove images: ![alt](url)
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', text)
    # Remove links but keep text: [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove bold/italic markers
    text = re.sub(r'[*_]{1,3}', '', text)
    # Remove strikethrough
    text = re.sub(r'~~', '', text)
    # Remove headings markers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove blockquote markers
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    # Remove code blocks (fenced)
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Truncate at ~160 chars on word boundary
    if len(text) <= 160:
        return text
    truncated = text[:160].rsplit(' ', 1)[0]
    return truncated.rstrip('.,;:!? ') + '...'
```

**Edge cases from actual posts:**
- `orchestrators.md` starts with a blockquote -- must strip `>` marker
- `the-complexity-tax.md` uses strikethrough `~~business~~` and italic `_making things simple_`
- `from-late-night-conversations...md` has links in the first sentence
- `in-defense-of-attention.md` starts with italic `*Attention*`
- `humanity-deserves-better...md` has a very short first paragraph (45 chars) -- should still produce a valid description by including subsequent text
- `the-agentic-middle-layer...md` has no blank line between title and first content paragraph

**Fallback:** If extracted description is empty or under 50 chars after stripping, fall back to the site-wide description from CONFIG.

### Pattern 3: Regex Image Extraction
**What:** Replace string manipulation with a proper regex for `![alt](url)`.
**Example:**
```python
import re

_IMAGE_RE = re.compile(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$')

def _extract_cover_image(self, lines, slug):
    cover_image = None
    filtered_lines = []

    for line in lines:
        match = _IMAGE_RE.match(line.strip())
        if match and cover_image is None:
            image_path = match.group(2)
            if image_path.startswith('http'):
                cover_image = image_path
            elif image_path.startswith('/'):
                cover_image = image_path
            else:
                cover_image = f"/{image_path}"
            continue
        filtered_lines.append(line)

    return cover_image, filtered_lines
```

**Why this regex:** `^!\[([^\]]*)\]\(([^)]+)\)\s*$` matches the full line as a standalone image (anchored with `^...$`). Group 1 captures alt text (allows empty), group 2 captures URL. The `\s*$` allows trailing whitespace. This handles edge cases the string-based approach misses: alt text containing `](` would confuse the current `find('](')` approach.

### Anti-Patterns to Avoid
- **Index-based line access:** Do not use `lines[0]`, `lines[1]` for header parsing. The whole point of QUAL-03 is to eliminate this fragility.
- **HTML-based description extraction:** Do not convert markdown to HTML then strip tags. Work from raw markdown per D-04.
- **Modifying post file format:** All 15 posts must build identically without any file changes (D-02).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Markdown syntax stripping | Full markdown parser | Simple regex chain on raw text | Only need to strip ~6 syntax types for description text; a full parser is overkill |
| Date parsing | Custom date parser | `datetime.strptime` with existing format + ordinal stripping | Already works for all 15 posts |

## Common Pitfalls

### Pitfall 1: Ordinal Suffix Stripping Is Greedy
**What goes wrong:** The current ordinal stripping replaces ALL occurrences of `st`, `nd`, `rd`, `th` in the date string. `Date: 2025 Mar 03` would have `Mar` become `Ma` because `r` + `d` is not the issue but `th` in month names like `Month` could be affected. Currently this works because `strptime` format `%b` uses 3-letter abbreviations and none end in `st`/`nd`/`rd`/`th`.
**Why it happens:** `str.replace()` replaces everywhere, not just at the end of the day number.
**How to avoid:** Keep the current approach (it works for all real posts), but consider using a regex `r'\d+(st|nd|rd|th)'` replacement for correctness. Test with all 12 month abbreviations to verify none are mangled.
**Warning signs:** A month abbreviation like "August" would break if used in full-form dates (but `%b` format prevents this).

### Pitfall 2: Header Parser Stops Too Early or Too Late
**What goes wrong:** The loop-based parser might consume a line that looks like a header but is actually content (e.g., a line like `Note: this is important` in the post body), or stop too early if there is a blank line between headers.
**Why it happens:** Ambiguity between `Key: Value` header syntax and natural English prose containing colons.
**How to avoid:** Only recognize KNOWN header keys (`date`, `draft`, `tags`). Any unrecognized key stops header parsing. Alternatively, stop at the first blank line unconditionally -- all current posts have headers immediately followed by the `# Title` line with no blank line separator.
**Warning signs:** A post whose first paragraph starts with a word followed by a colon would be misinterpreted as a header.

### Pitfall 3: Description Extraction Gets Empty String
**What goes wrong:** Posts that start with only images, code blocks, or headings (no plain text in first ~160 chars after stripping) produce an empty description.
**Why it happens:** All non-text markdown elements are stripped, and nothing remains.
**How to avoid:** Fall back to CONFIG["site_description"] when extracted text is under 50 chars. Test with a synthetic post that starts with a code block.

### Pitfall 4: Backward Compatibility Regression
**What goes wrong:** After refactoring `_parse_post()`, the generated HTML differs from the pre-refactor output for one or more of the 15 posts.
**Why it happens:** Subtle differences in where `start_line` is set, or whitespace handling in the new parser.
**How to avoid:** Before making any changes, capture the current output of all 15 posts as baseline. After refactoring, compare. The test should assert byte-for-byte identical output (or at minimum, identical rendered content).
**Warning signs:** A post that has unusual whitespace between the date line and title line.

### Pitfall 5: `_parse_page()` Left Inconsistent
**What goes wrong:** `_parse_post()` gets a description but `_parse_page()` does not, leaving pages with `description=None` still.
**Why it happens:** Forgetting that pages also pass `description=None` to template render (line 239).
**How to avoid:** Apply `_extract_description()` to pages too. The about page (`pages/about.md`) should also get a description.

## Code Examples

### Existing Post Dict Shape (to preserve)
```python
# Source: blogmaker.py _parse_post() return, line 103-114
{
    'title': str,
    'slug': str,
    'filename': str,
    'date': str,         # formatted: "2025 Oct 12"
    'iso_date': str,     # ISO 8601
    'date_obj': datetime,
    'content': str,      # rendered HTML
    'cover_image': str,  # URL or None
    'filepath': str,
    'hash': str,         # SHA256[:16]
}
```

### Extended Post Dict Shape (after this phase)
```python
{
    # ... all existing fields unchanged ...
    'description': str,  # NEW: plain text ~160 chars
    'tags': list,        # NEW: [] for now (parsed but unused until Phase 2)
    'draft': bool,       # NEW: False for now (parsed but unused until Phase 2)
}
```

### Bare Except Fix
```python
# Source: blogmaker.py line 50
# Before:
except:
    return {}

# After:
except (json.JSONDecodeError, IOError):
    return {}
```

### Test Pattern for Backward Compatibility
```python
def test_all_existing_posts_parse_identically():
    """Snapshot test: all 15 posts produce same HTML before and after refactor."""
    # Capture baseline before refactor (run once, save expected output)
    # After refactor, compare against baseline
    for filepath in sorted(Path('posts').glob('*.md')):
        post = builder._parse_post(filepath)
        assert post is not None, f"{filepath.name} failed to parse"
        # Compare title, date, content, cover_image against known values
```

### Test Cases for Image Extraction (QUAL-04)
```python
# Edge cases to test:
# 1. Standard image: ![alt](path/to/image.jpg)
# 2. Image with empty alt: ![](image.jpg)
# 3. Image with complex alt containing special chars: ![photo [1]](image.jpg)
# 4. Inline image (not standalone line): text ![img](url) more text -- should NOT match
# 5. Multiple images: first becomes cover, rest stay in content
# 6. No images: returns None, all lines preserved
# 7. HTTP URL image: ![alt](https://example.com/img.jpg)
# 8. Image with spaces in path: ![alt](path/my image.jpg)
```

### Test Cases for Date Parsing (QUAL-05)
```python
# Edge cases to test:
# 1. Standard date: "Date: 2025 Oct 12" -- passes
# 2. Ordinal suffix: "Date: 2025 May 11th" -- passes (existing handling)
# 3. Other ordinals: "Date: 2025 Jan 1st", "Date: 2025 Feb 2nd", "Date: 2025 Mar 3rd"
# 4. Invalid date: "Date: not-a-date" -- returns None
# 5. Missing date line: no "Date:" prefix -- returns None
# 6. Malformed date: "Date: 2025 13 01" -- returns None (invalid month)
# 7. Empty date value: "Date: " -- returns None
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Index-based header parsing (`lines[0]`, `lines[1]`) | Loop-based `Key: Value` parsing | This phase | Enables arbitrary header fields in Phase 2 |
| String-based image detection (`startswith('![')`, `find('](')`) | Regex `^!\[([^\]]*)\]\(([^)]+)\)\s*$` | This phase | Handles edge cases in alt text, is more explicit |
| `description=None` in all render calls | Auto-generated from markdown content | This phase | SEO improvement, fills existing template plumbing |
| Bare `except:` in `_load_cache` | `except (json.JSONDecodeError, IOError):` | This phase | Code quality, prevents swallowing unexpected errors |

## Validation Architecture

> Skipped per config: `workflow.nyquist_validation` is `false`.

## Project Constraints (from CLAUDE.md)

The following directives from CLAUDE.md are relevant to this phase:

1. **Test-first workflow:** "ALWAYS start by writing a test to reproduce the problem" -- tests for each requirement before implementation.
2. **Run tests:** `python3 tests/test_quality.py && python3 tests/test_build.py` -- must pass after all changes.
3. **Compile check:** `python3 -m py_compile blogmaker.py` -- must pass before declaring complete.
4. **Simplicity:** "ALWAYS choose simplicity over complexity" -- no over-engineering the header parser.
5. **DRY:** Share `_extract_description()` between `_parse_post()` and `_parse_page()`.
6. **No backwards compat maintenance:** "NEVER try to maintain backwards compatibility when making changes" -- however D-02 explicitly requires identical output for existing posts, which takes precedence as a user decision.
7. **Tests in `tests/` folder:** Never inline in source files.
8. **Conventional commits:** `feat:`, `fix:`, `test:`, `refactor:` etc.
9. **No co-authored-by lines** in commit messages.
10. **Only 2 dependencies:** `markdown2` and `jinja2`. No new packages.

## Sources

### Primary (HIGH confidence)
- Direct codebase analysis: `blogmaker.py` (283 lines), all 15 posts examined, templates inspected
- `.planning/research/ARCHITECTURE.md` -- header parser design, component boundaries
- `.planning/research/PITFALLS.md` -- Pitfall 4 (meta description artifacts), Pitfall 10 (header format conflicts)
- `.planning/phases/01-foundation-and-meta/01-CONTEXT.md` -- locked decisions D-01 through D-07

### Secondary (MEDIUM confidence)
- Python `re` module documentation -- regex syntax for image/markdown patterns (standard, well-known)

### Tertiary (LOW confidence)
- None -- this phase is entirely within the existing codebase with no external library research needed.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new libraries, only stdlib `re`
- Architecture: HIGH -- single-file refactor in well-understood codebase, all 15 posts verified
- Pitfalls: HIGH -- edge cases identified from actual post content analysis

**Research date:** 2026-03-29
**Valid until:** Indefinite -- codebase-internal refactoring with no external dependency concerns
