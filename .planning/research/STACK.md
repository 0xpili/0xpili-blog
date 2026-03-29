# Technology Stack

**Project:** 0xpili Blog Improvements (Meta Descriptions, RSS, Drafts, Tags)
**Researched:** 2026-03-29

## Constraint: No New Dependencies

The project explicitly forbids new dependencies. The entire stack is Python stdlib + markdown2 + jinja2. Every recommendation below uses only these. This is not a limitation — it is the correct choice for a blog that aims to run for decades.

## Recommended Stack

### RSS Feed Generation

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| `xml.etree.ElementTree` | stdlib | Generate RSS 2.0 XML | Built into Python, handles XML escaping correctly, no string concatenation bugs. Produces well-formed XML every time. |

**Use RSS 2.0, not Atom.** Rationale: RSS 2.0 is simpler to generate, universally supported by all feed readers, and the blog's content (plain articles with titles, dates, descriptions) has zero need for Atom's extra complexity (content type labeling, extensible namespaces). The RSS 2.0 spec has been stable since 2009 — perfect for a "built for decades" blog.

**Required RSS 2.0 elements:**
- Channel: `title`, `link`, `description` (all already in CONFIG)
- Items: `title`, `link`, `description`, `pubDate`, `guid`
- Optional but recommended: `lastBuildDate`, `language`, `generator`

**Implementation approach:** Generate `docs/feed.xml` during build using `ElementTree.SubElement()` to construct the tree, then `ElementTree.write()` to output. ~30-40 lines of code.

**Confidence:** HIGH — stdlib, stable spec, straightforward implementation.

### Meta Description Generation

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| `re` module | stdlib | Strip markdown syntax from first paragraph | Simpler and faster than html.parser for this narrow use case. No HTML parsing needed — we strip markdown *before* conversion. |
| Jinja2 template | existing | Render `<meta name="description">` | Templates already have `{{ description }}` placeholders passing `None`. Just needs real values. |

**Approach:** Extract description from the raw markdown content (post first paragraph), not from HTML output. This avoids needing to strip HTML tags entirely.

Algorithm:
1. After extracting title and before markdown-to-HTML conversion, find first non-empty paragraph of text
2. Strip markdown syntax (links, bold, italic, images) with regex
3. Truncate to 155 characters at a word boundary
4. Pass to template as `description`

**Why not strip from HTML?** Would require `html.parser` subclass (~15 lines of boilerplate) to strip tags after conversion. Working with raw markdown is simpler — a few `re.sub()` calls handle `[text](url)` -> `text`, `**bold**` -> `bold`, `![alt](src)` -> empty, etc.

**Why 155 characters?** Google truncates meta descriptions at ~155-160 characters. Truncating at 155 with a word boundary keeps descriptions clean in search results.

**Confidence:** HIGH — trivial string manipulation, templates already wired up.

### Draft Support

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| String parsing | stdlib | Parse `Draft: true` header | Consistent with existing `Date:` header pattern. No new parsing complexity. |

**Approach:** Add optional `Draft: true` header line after `Date:` line. During `_parse_post()`, check for this header and skip the post when building for production.

Post format becomes:
```
Date: 2025 Oct 12
Draft: true
# My Work In Progress

Content...
```

**Why a header, not a filename convention (e.g., `_draft-post.md`)?** Headers are explicit, visible in the file, and consistent with the existing `Date:` header pattern. Filename conventions are fragile (easy to forget the underscore) and would require changing the glob pattern.

**Why not a `drafts/` directory?** Would require a second directory scan, changes to the build cache key scheme, and creates ambiguity about when to move files between directories. A header field is simpler.

**Confidence:** HIGH — 3-5 lines of code in `_parse_post()`.

### Tags/Categories

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| String parsing | stdlib | Parse `Tags: crypto, ai, philosophy` header | Comma-separated list, trivial to parse with `str.split(',')`. |
| Jinja2 template | existing | Render tag links on posts and optionally on index | Already using Jinja2 for all rendering. |

**Approach:** Add optional `Tags:` header. Parse as comma-separated, stripped, lowercased strings. Store in post dict. Pass to templates.

Post format:
```
Date: 2025 Oct 12
Tags: crypto, ai, defi
# My Post

Content...
```

**Phase 1 (this milestone):** Parse tags, display on posts, include in RSS feed categories. No tag index pages yet — that is a separate feature with its own template.

**Why comma-separated, not YAML frontmatter?** The blog uses a dead-simple header format (`Key: Value` lines). YAML frontmatter (`---` delimited blocks) would require a YAML parser or regex complexity and is philosophically misaligned with this blog's minimalism. Comma-separated values in a single line are sufficient for tags.

**Confidence:** HIGH — simple string parsing.

### Post Header Parsing (Unified)

The current `_parse_post()` parses headers ad-hoc (checks `lines[0]` for Date, `lines[1]` for title). Adding Draft and Tags headers means this should be refactored into a generic header parser.

**Recommended pattern:**
```python
def _parse_headers(self, lines: List[str]) -> Tuple[Dict[str, str], int]:
    """Parse Key: Value headers until first non-header line.
    Returns (headers_dict, content_start_line)."""
    headers = {}
    for i, line in enumerate(lines):
        if ':' in line and not line.startswith('#'):
            key, _, value = line.partition(':')
            key = key.strip().lower()
            if key in ('date', 'draft', 'tags'):
                headers[key] = value.strip()
                continue
        return headers, i
    return headers, len(lines)
```

This is ~10 lines, handles any number of headers, and makes future headers (e.g., `Author:`, `Slug:`) trivial to add.

**Confidence:** HIGH — straightforward refactor.

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Feed format | RSS 2.0 via `xml.etree` | Atom 1.0 | Unnecessary complexity for this use case. Atom's advantages (content typing, namespaces) are irrelevant for a plain blog. |
| Feed format | RSS 2.0 via `xml.etree` | Hand-written XML string | Fragile. Fails on special characters (`&`, `<`, `>`) in post titles/descriptions. ElementTree handles escaping automatically. |
| Feed library | `xml.etree.ElementTree` | `rfeed`, `feedgen`, `PyRSS2Gen` | Violates no-new-dependencies constraint. Also, these libraries are overkill — the blog needs ~30 lines of XML generation. |
| Meta description | Strip from raw markdown | Strip from HTML output | Requires html.parser subclass boilerplate. Working with markdown source is simpler. |
| Meta description | Auto-generate from content | Manual `Description:` header | Adds friction to writing. Auto-generation from first paragraph works for 95% of blog posts. Can add optional override header later. |
| Draft support | `Draft: true` header | `_filename.md` convention | Filename conventions are invisible, easy to forget, and inconsistent with existing header pattern. |
| Draft support | `Draft: true` header | Separate `drafts/` directory | Adds directory management complexity, cache key changes, and file-moving workflow. |
| Tags format | Comma-separated header | YAML frontmatter | Would need YAML parser or complex regex. Overkill for a flat list of strings. |
| Header parsing | Generic `Key: Value` parser | Continue ad-hoc per-line checks | Current approach doesn't scale. Adding 2 more headers to ad-hoc parsing creates brittle index math. |

## What NOT to Use

| Technology | Why Not |
|------------|---------|
| `feedgen` / `rfeed` / `PyRSS2Gen` | New dependencies. The stdlib handles RSS generation fine. |
| `PyYAML` / `python-frontmatter` | New dependencies. Comma-separated headers are sufficient. |
| `BeautifulSoup` | New dependency. Not needed for text extraction from markdown. |
| `lxml` | New dependency. `xml.etree.ElementTree` is sufficient. |
| Jinja2 for RSS template | While technically possible, XML generation via string templates is fragile and hard to validate. `ElementTree` is the right tool for XML. |
| JSON Feed | Low adoption compared to RSS 2.0. Not worth supporting. |

## No Installation Required

```bash
# Nothing new to install. All features use:
# - Python stdlib (xml.etree.ElementTree, re, html)
# - Existing deps: markdown2, jinja2
pip install markdown2 jinja2  # already installed
```

## Sources

- [RSS 2.0 Specification (Current)](https://www.rssboard.org/rss-specification) — RSS 2.0 required elements, channel and item structure
- [W3C RSS 2.0 Specification](https://validator.w3.org/feed/docs/rss2.html) — Feed validation requirements
- [Python xml.etree.ElementTree Documentation](https://docs.python.org/3/library/xml.etree.elementtree.html) — Stdlib XML generation API
- [Python html.parser Documentation](https://docs.python.org/3/library/html.parser.html) — Stdlib HTML parsing (considered, not recommended)
- [SEO Guide for Static Site Generators](https://buttercms.com/blog/a-complete-dead-simple-guide-to-seo-for-static-site-generators/) — Meta description best practices
- [Atom vs RSS Discussion](https://danielmiessler.com/blog/atom-rss-why-we-should-just-call-them-feeds-instead-of-rss-feeds) — Feed format comparison
