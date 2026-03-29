# Architecture Patterns

**Domain:** Static site generator feature expansion
**Researched:** 2026-03-29

## Current Architecture

The engine is a single-class `BlogBuilder` (~283 lines) with this data flow:

```
posts/*.md  -->  _parse_post()  -->  post dict  -->  template.render()  -->  docs/*.html
pages/*.md  -->  _parse_page()  -->  page dict  -->  template.render()  -->  docs/*.html
                                     [all posts] -->  index_template     -->  docs/index.html
```

The post dict is the central data structure. Every feature in this milestone adds data to the post dict, consumes the post dict, or filters which post dicts reach output. This is the key architectural insight: the post dict is the integration point.

### Current Post Dict Shape

```python
{
    'title': str,           # From first # heading or filename
    'slug': str,            # Filename stem, lowercased
    'filename': str,        # Same as slug
    'date': str,            # Formatted date string
    'iso_date': str,        # ISO 8601 date
    'date_obj': datetime,   # Python datetime (for sorting)
    'content': str,         # Rendered HTML
    'cover_image': str,     # First standalone image URL or None
    'filepath': str,        # Source file path (for cache)
    'hash': str,            # SHA256 hash (for cache)
}
```

## Recommended Architecture

Keep the single-class design. These features do not warrant extracting services, registries, or plugin systems. Each feature maps cleanly to either (a) a new field on the post dict, (b) a filtering step before rendering, or (c) a new output artifact. The BlogBuilder class remains the single owner of the build pipeline.

### Extended Post Dict Shape (After All Features)

```python
{
    # ... existing fields unchanged ...
    'description': str,     # NEW: first ~160 chars of plain text (meta descriptions)
    'tags': list[str],      # NEW: parsed from Tags: header line
    'draft': bool,          # NEW: parsed from Draft: header line
}
```

### Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| `_parse_post()` | Parse markdown, extract ALL metadata (date, title, description, tags, draft status), convert to HTML | Returns post dict to `build()` |
| `build()` | Orchestrate: parse all posts, filter drafts, render posts, render index, generate RSS | Calls all other methods, passes post dicts |
| `_extract_description()` | Extract first ~160 chars of plain text from markdown content (strip markdown syntax) | Called by `_parse_post()`, result stored in post dict |
| `_generate_rss()` | Generate RSS XML from sorted post list | Called by `build()` after posts are sorted, writes `docs/feed.xml` |
| `_extract_cover_image()` | Extract first standalone image (existing) | Called by `_parse_post()`, unchanged |
| Templates | Consume post dict fields for rendering | Receive post dict fields as template variables |

### Data Flow (After All Features)

```
posts/*.md
    |
    v
_parse_post()
    |-- parses Date: header (existing)
    |-- parses Draft: header (NEW - line 2 if present)
    |-- parses Tags: header (NEW - line 3 if present)
    |-- extracts # Title (existing)
    |-- extracts cover image (existing)
    |-- extracts description from first paragraph (NEW)
    |-- converts markdown to HTML (existing)
    |-- returns post dict with all fields
    |
    v
build()
    |-- collects all post dicts
    |-- FILTERS out draft=True posts (NEW)
    |-- sorts by date (existing)
    |-- renders each post HTML via base.html (existing, now passes description + tags)
    |-- renders index.html (existing, receives filtered+sorted posts)
    |-- generates feed.xml (NEW)
    |-- saves cache (existing)
    |
    v
docs/
    |-- *.html (post pages, with meta description tags)
    |-- index.html (no drafts listed)
    |-- feed.xml (NEW, no drafts included)
```

## Integration Details Per Feature

### 1. Meta Descriptions

**Where it lives:** New `_extract_description()` method on BlogBuilder, called inside `_parse_post()`.

**Implementation approach:** Strip markdown syntax from the content text (before HTML conversion), take the first ~160 characters, break at the last word boundary. This operates on the raw markdown content string, not the HTML output, because stripping HTML tags is fragile and unnecessary when you already have the source markdown.

**Template integration:** `base.html` already has the plumbing:
```html
<meta name="description" content="{{ description or 'Thoughtful writings...' }}">
```
Currently `description=None` is passed in the render call (line 215 of blogmaker.py). Change to `description=post['description']`. Same for `page.html`.

**No new dependencies.** Simple string processing with stdlib `re` to strip markdown links, images, bold, italic markers.

**Build order dependency:** None. Can be implemented first or in parallel with any other feature.

### 2. Draft Filtering

**Where it lives:** Parsing in `_parse_post()`, filtering in `build()`.

**Post format extension:**
```markdown
Date: 2026 Mar 29
Draft: true
# My Unfinished Post
```

The `Draft:` header is optional. When absent, `draft` defaults to `False`. This follows the existing pattern of the `Date:` header as a simple `Key: Value` line.

**Parsing approach:** After parsing the `Date:` line (line index 0), check if the next line starts with `Draft:`. If so, parse the value (`true`/`yes`/`1` = draft), and shift the `start_line` index forward by one. This same index-shifting pattern must also account for the `Tags:` header, so both optional headers should be parsed in a single pass through the header block.

**Filtering approach:** In `build()`, after collecting all post dicts, filter before rendering:
```python
posts = [p for p in posts if not p.get('draft', False)]
```

Draft posts are excluded from: individual HTML output, index listing, and RSS feed. They are NOT excluded from cache tracking (so the cache knows about them and rebuilds correctly when draft status changes).

**Build order dependency:** Should be implemented before RSS, since RSS must also respect draft filtering.

### 3. Tags

**Where it lives:** Parsing in `_parse_post()`, display in templates.

**Post format extension:**
```markdown
Date: 2026 Mar 29
Tags: crypto, privacy, philosophy
# My Post Title
```

The `Tags:` header is optional. When absent, `tags` defaults to `[]`. Comma-separated, stripped of whitespace.

**Parsing approach:** Parse in the same header block pass as Draft. The header block is lines 1+ (after Date:) until the first `# ` heading or a line that does not match `Key: Value` pattern.

**Template integration:** Add a tag display in the `.meta` div of `base.html`:
```html
<div class="meta">
  {{ date }}
  {% if tags %}
  <span class="tags">{% for tag in tags %}{{ tag }}{% if not loop.last %}, {% endif %}{% endfor %}</span>
  {% endif %}
</div>
```

Tags are purely display in this milestone. No tag index pages, no filtering by tag. This is explicitly kept simple -- tag index pages would add significant template and routing complexity for marginal value at 15 posts. If the blog grows past 50+ posts, tag pages become worth the cost.

**Build order dependency:** Can be implemented in parallel with meta descriptions. Should come before or alongside draft filtering since they share the header parsing logic.

### 4. RSS Feed Generation

**Where it lives:** New `_generate_rss()` method on BlogBuilder, called at the end of `build()`.

**Implementation approach:** Generate RSS 2.0 XML using Python's `xml.etree.ElementTree` (stdlib, no new dependency). The method receives the sorted, draft-filtered post list and writes `docs/feed.xml`.

**RSS structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>0xpili</title>
    <link>https://0xpili.xyz</link>
    <description>Thoughtful writings...</description>
    <atom:link href="https://0xpili.xyz/feed.xml" rel="self" type="application/rss+xml"/>
    <item>
      <title>Post Title</title>
      <link>https://0xpili.xyz/post-slug.html</link>
      <guid>https://0xpili.xyz/post-slug.html</guid>
      <pubDate>RFC 822 date</pubDate>
      <description>Meta description or first 160 chars</description>
    </item>
  </channel>
</rss>
```

**Template integration:** Add RSS autodiscovery `<link>` to both `base.html` and `index.html` `<head>`:
```html
<link rel="alternate" type="application/rss+xml" title="0xpili" href="/feed.xml">
```

**Feed content:** Use the `description` field (from meta descriptions feature) as the `<description>` for each item. This creates a direct dependency on meta descriptions being implemented first.

**Build order dependency:** Depends on meta descriptions (for item descriptions) and draft filtering (to exclude drafts). Implement last.

### 5. Code Quality Fixes (Bare Except, Image Parsing, Tests)

**Where they live:** Inline fixes to existing methods.

**Bare except (line 50):** Change `except:` to `except (json.JSONDecodeError, IOError):` in `_load_cache()`.

**Image extraction:** Replace string-based parsing in `_extract_cover_image()` with a regex:
```python
import re
IMAGE_RE = re.compile(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$')
```
This handles edge cases the current string parsing misses (e.g., alt text containing `](`).

**These have no dependencies on other features and can be done first or in parallel.**

## Header Parsing Design

The most architecturally significant change is extending the header block parser in `_parse_post()`. Currently it reads exactly one line (Date:) and optionally a second line (# Title). The new design reads a variable-length header block:

```python
# Parse header block
i = 0
date_str = lines[i].replace('Date:', '').strip()  # Line 0: Date (required)
i += 1

draft = False
tags = []

# Parse optional headers until we hit title or content
while i < len(lines):
    line = lines[i].strip()
    if line.startswith('Draft:'):
        draft = line.split(':', 1)[1].strip().lower() in ('true', 'yes', '1')
        i += 1
    elif line.startswith('Tags:'):
        tags = [t.strip() for t in line.split(':', 1)[1].split(',') if t.strip()]
        i += 1
    else:
        break  # Not a header line, stop

# Parse title
if i < len(lines) and lines[i].startswith('# '):
    title = lines[i][2:].strip()
    i += 1
else:
    title = filepath.stem.replace('-', ' ').title()

start_line = i
```

This is a clean extension of the existing pattern. The while loop consumes known header keys, stops at the first unrecognized line, then title parsing proceeds as before. New headers can be added in the future by adding `elif` branches.

## Patterns to Follow

### Pattern: Enrich-Then-Filter-Then-Render
The build pipeline should follow a strict order:
1. **Parse** all posts (enrich post dicts with all metadata)
2. **Filter** (remove drafts)
3. **Sort** (by date, descending)
4. **Render** (HTML pages, index, RSS)

This ordering means every renderer receives clean, complete, filtered data. No renderer needs to check draft status. No renderer needs to handle missing fields.

### Pattern: Optional Headers with Defaults
Every new header field must have a sensible default so existing posts build without modification:
- `Draft:` absent = `False`
- `Tags:` absent = `[]`
- `description` is always auto-generated, never a header field

### Pattern: Cache Awareness for New Fields
When a post's tags or draft status change, the post must rebuild. The current cache keys on the SHA256 hash of the entire file, so any content change (including header changes) already triggers a rebuild. No cache logic changes needed.

## Anti-Patterns to Avoid

### Anti-Pattern: Separate Metadata Files
Do NOT store post metadata in a separate YAML/JSON file. The single-file post format (metadata headers + markdown content) is the blog's strength. Everything about a post lives in one `.md` file.

### Anti-Pattern: Tag Index Pages (in this milestone)
Do NOT build tag index pages (e.g., `/tags/crypto.html`). At 15 posts, tag navigation adds complexity without reader value. Tags should be display-only metadata in this phase.

### Anti-Pattern: Full HTML in RSS
Do NOT include full post HTML in RSS `<description>`. It balloons feed size and creates a maintenance burden (relative URLs, image paths). Use the short text description.

### Anti-Pattern: Extracting Description from HTML
Do NOT run the markdown-to-HTML conversion first and then strip HTML tags to get the description. Work from the raw markdown source -- it is simpler and avoids edge cases with HTML entities and nested tags.

## Suggested Build Order (Dependencies)

```
Phase 1 (parallel, no dependencies):
  |-- Code quality fixes (bare except, image regex)
  |-- Meta descriptions (_extract_description)
  |-- Header parsing refactor (Draft: + Tags: support)

Phase 2 (depends on Phase 1):
  |-- Draft filtering in build() (needs header parsing)
  |-- Tag display in templates (needs header parsing)

Phase 3 (depends on Phase 1 + Phase 2):
  |-- RSS feed generation (needs meta descriptions + draft filtering)
  |-- RSS link in templates
```

The critical path is: header parsing refactor --> draft filtering --> RSS. Meta descriptions can proceed independently until RSS needs them.

## Scalability Considerations

| Concern | At 15 posts (now) | At 100 posts | At 1000 posts |
|---------|-------------------|--------------|---------------|
| Build time | <1s, non-issue | <2s with incremental | May need parallel parsing |
| RSS feed size | ~5KB | ~30KB | Paginate or limit to latest 50 |
| Tag management | Display only | Consider tag index pages | Tag index pages + tag counts |
| Draft management | Header flag sufficient | Header flag sufficient | Consider drafts directory |
| Description extraction | Regex strip per post | Still fine | Still fine |

At the current scale of 15 posts, none of these features introduce performance concerns. The incremental build cache already handles the "only rebuild changed posts" optimization.

## Sources

- Current codebase analysis (blogmaker.py, templates, PROJECT.md) -- PRIMARY
- RSS 2.0 specification (cyber.harvard.edu/rss/rss.html) -- for feed format
- Python xml.etree.ElementTree stdlib documentation -- for RSS generation approach
- Confidence: HIGH -- this is an architecture analysis of an existing, well-understood codebase with straightforward feature additions
