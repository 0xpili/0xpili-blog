# Phase 2: Drafts and Tags - Research

**Researched:** 2026-03-29
**Domain:** Python static site generator -- draft filtering and tag taxonomy
**Confidence:** HIGH

## Summary

Phase 2 adds two features to `blogmaker.py`: draft post exclusion and a tag system with per-tag index pages. The existing codebase is exceptionally well-prepared -- Phase 1 already added `draft` and `tags` keys to the known_headers allowlist (line 104) and initialized them in the post dict (lines 175-176). The work is connecting parsed header values to filtering logic and template rendering.

Draft support requires: (1) populating `draft` from the parsed header, (2) filtering drafts from the build pipeline (no HTML generation, no index listing), and (3) cleaning up stale HTML when a published post becomes a draft. Tag support requires: (1) parsing comma-separated tags from the header, (2) displaying linked tags on post pages, (3) generating per-tag index pages using the existing index template pattern.

**Primary recommendation:** Implement drafts first (simpler, no template changes beyond filtering), then tags (builds on draft-aware post list). Both features touch `_parse_post()` and `build()` in blogmaker.py, plus templates.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Parse `Draft: true` from header block using the existing loop-based parser. Case-insensitive value matching (`true`, `True`, `TRUE` all work).
- **D-02:** Draft posts are excluded from: HTML output generation, index page post list, and future RSS feed. The post dict already has `draft: False` -- populate from header.
- **D-03:** If a previously published post becomes a draft, delete its stale HTML output file from `docs/`.
- **D-04:** Parse `Tags: crypto, ai, philosophy` from header block. Comma-separated, whitespace-trimmed, lowercased for consistency.
- **D-05:** Display tags on individual post pages as comma-separated linked text (links point to tag index pages). Style consistent with blog's minimal aesthetic.
- **D-06:** Generate per-tag index pages at `docs/tag-{name}.html` (flat structure, no subdirectory).
- **D-07:** Tag index pages reuse the index.html template pattern with a heading like "Posts tagged: crypto". List only non-draft posts with that tag, sorted newest-first.

### Claude's Discretion
- Exact CSS styling for tag links on post pages
- Whether to add tags to the index.html post listing (not required, but allowed if it fits)
- Tag normalization edge cases (hyphens, special chars)

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.

</user_constraints>

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DRFT-01 | Support `Draft: true` header field to exclude posts from build output | Header parser already recognizes 'draft' key; populate boolean from parsed value with case-insensitive check |
| DRFT-02 | Draft posts excluded from index page, RSS feed, and HTML generation | Filter draft posts in `build()` before rendering loop and before index template render |
| TAGS-01 | Parse `Tags: crypto, ai` header field from post metadata | Header parser already recognizes 'tags' key; split on comma, strip, lowercase |
| TAGS-02 | Display tags on individual post pages | Add tag links to `base.html` template in the `.meta` div, pass `tags` to template render call |
| TAGS-03 | Generate per-tag index pages listing filtered posts | Collect tags across all non-draft posts, render index template variant per tag |

</phase_requirements>

## Project Constraints (from CLAUDE.md)

- Only 2 dependencies: `markdown2` and `jinja2` -- no new packages
- Tests in `tests/` folder, run with `python3 tests/test_quality.py && python3 tests/test_build.py`
- Always run `python3 -m py_compile blogmaker.py` before declaring victory
- Simplicity over complexity; DRY and modular
- Conventional commits: `feat:`, `fix:`, `test:`, etc.
- No co-authored-by lines in commits
- Post size budget: <25KB (includes ~8KB inlined CSS)
- Index size budget: <10KB
- No inline `style=""` attributes
- No external fonts or JS libraries

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.13.1 | Runtime | Already installed |
| markdown2 | 2.5.2 | Markdown to HTML | Already a dependency |
| Jinja2 | 3.1.5 | Template rendering | Already a dependency |

No new dependencies needed. Both features are pure Python logic + Jinja2 template changes.

## Architecture Patterns

### Recommended Changes Structure
```
blogmaker.py          # Modify _parse_post() and build()
templates/base.html   # Add tag display in .meta section
templates/index.html  # No changes needed (reused via render call with different data)
tests/test_build.py   # Add draft and tag tests
```

### Pattern 1: Draft Header Parsing
**What:** Populate `draft` field from parsed header value
**When to use:** In `_parse_post()` after header parsing loop completes (around line 163)
**Example:**
```python
# After headers dict is populated (line 118)
# Before the return dict (line 163)
draft = headers.get('draft', '').lower() == 'true'

# In the return dict:
'draft': draft,
```

### Pattern 2: Tag Header Parsing
**What:** Parse comma-separated tags into a list
**When to use:** In `_parse_post()` alongside draft parsing
**Example:**
```python
tags_raw = headers.get('tags', '')
tags = [t.strip().lower() for t in tags_raw.split(',') if t.strip()] if tags_raw else []

# In the return dict:
'tags': tags,
```

### Pattern 3: Draft Filtering in build()
**What:** Filter drafts before rendering, clean stale files
**When to use:** In `build()` after posts are collected but before rendering
**Example:**
```python
# After collecting all posts from _parse_post() calls
# Separate drafts from published posts
published = [p for p in posts if not p['draft']]

# Delete stale HTML for draft posts
for post in posts:
    if post['draft']:
        stale_file = output_path / f"{post['slug']}.html"
        if stale_file.exists():
            stale_file.unlink()
            print(f"  ✗ {post['title']} (draft, removed)")

# Use `published` for: rendering posts, index page, tag pages
# Keep using `posts` only for the initial parse loop
```

### Pattern 4: Tag Index Page Generation
**What:** Collect all tags, generate one index page per tag
**When to use:** In `build()` after post rendering, before `_save_cache()`
**Example:**
```python
# Collect tags from published posts
tag_posts = {}
for post in published:
    for tag in post['tags']:
        tag_posts.setdefault(tag, []).append(post)

# Generate tag pages
for tag, tagged_posts in tag_posts.items():
    tagged_posts.sort(key=lambda x: x['date_obj'], reverse=True)
    tag_html = index_template.render(
        posts=tagged_posts,
        tag=tag,
        page_title=f"Posts tagged: {tag}",
    )
    (output_path / f"tag-{tag}.html").write_text(tag_html, encoding='utf-8')
    print(f"  ✓ Tag page: {tag}")
```

### Pattern 5: Tag Display in Post Template
**What:** Show tag links on post pages
**When to use:** In `base.html`, below the `.meta` div
**Example (Jinja2):**
```html
<div class="meta">
  {{ date }}
  {% if tags %}
  <span class="tags"> · {% for tag in tags %}<a href="/tag-{{ tag }}.html">{{ tag }}</a>{% if not loop.last %}, {% endif %}{% endfor %}</span>
  {% endif %}
</div>
```

### Pattern 6: Template Conditional for Tag Pages
**What:** The index.html template needs a conditional heading for tag pages vs homepage
**When to use:** Modify `index.html` to accept an optional `tag` variable
**Example (Jinja2):**
```html
{% if tag %}
<h1>Posts tagged: {{ tag }}</h1>
{% else %}
<h1>0xpili</h1>
<p class="tagline">On crypto, AI, and being human</p>
{% endif %}
```

### Anti-Patterns to Avoid
- **Separate tag template file:** Do NOT create a new `tag.html` template. Reuse `index.html` with conditional rendering. Keeps it DRY.
- **Nested tag directories:** Do NOT use `docs/tags/crypto.html`. Use flat `docs/tag-crypto.html` per D-06.
- **Forgetting to pass tags to template render:** The current `post_template.render()` call (line 270-276) does not pass `tags`. Must add it.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Tag normalization | Custom slug function | `.strip().lower()` | Tags are simple words; no need for full slugification |
| Tag page template | New template file | Conditional in `index.html` | One template with a branch is simpler than two templates |

**Key insight:** Both features are small additions to existing patterns. The codebase already has the scaffolding (known_headers, dict fields). No new libraries or complex abstractions needed.

## Common Pitfalls

### Pitfall 1: Draft Posts Leaking into Tag Pages
**What goes wrong:** Draft posts appear in tag index pages because tag collection happens before draft filtering.
**Why it happens:** Using the full `posts` list instead of `published` when building tag_posts dict.
**How to avoid:** Always use the draft-filtered list (`published`) for tag page generation AND index page rendering.
**Warning signs:** A test with a draft post that has tags -- check it does not appear on the tag page.

### Pitfall 2: Stale Tag Pages for Empty Tags
**What goes wrong:** A tag page exists from a previous build, but all posts with that tag are now drafts or the tag was removed. The stale HTML remains.
**Why it happens:** Tag pages are generated fresh each build, but old ones are not cleaned up.
**How to avoid:** Before generating tag pages, remove all existing `tag-*.html` files from output directory, then regenerate only current tags.
**Warning signs:** Old tag pages appearing in the site after removing tags from posts.

### Pitfall 3: Forgetting to Pass Tags to Post Template
**What goes wrong:** Tags display as empty on post pages even though they are parsed correctly.
**Why it happens:** The `post_template.render()` call (line 270-276) currently does not include `tags` in its keyword arguments.
**How to avoid:** Add `tags=post['tags']` to the render call.
**Warning signs:** Template renders without error but shows no tags (Jinja2 treats undefined variables as empty by default with autoescape).

### Pitfall 4: Tag Casing Inconsistency
**What goes wrong:** "AI" and "ai" become different tags, or "Crypto" and "crypto" generate separate pages.
**Why it happens:** Not normalizing tag casing consistently.
**How to avoid:** Lowercase all tags at parse time (D-04 mandates this). Display lowercase on pages.
**Warning signs:** Duplicate tag pages with different casing.

### Pitfall 5: Build Cache Not Invalidated for Tag Pages
**What goes wrong:** A post changes its tags but tag pages are not regenerated.
**Why it happens:** Tag pages have no entry in the build cache -- they depend on the collective state of all posts.
**How to avoid:** Always regenerate all tag pages on every build. They are cheap (just HTML from template). Do not try to cache tag pages individually.
**Warning signs:** Tag pages showing stale post lists.

### Pitfall 6: Index Page Size Budget Exceeded
**What goes wrong:** Adding tag metadata to the index template pushes it over 10KB.
**Why it happens:** Tags add extra HTML per post listing.
**How to avoid:** Keep tags off the homepage index (they are optional per Claude's discretion). If added, keep markup minimal.
**Warning signs:** `test_quality.py` fails with index >10KB.

## Code Examples

### Current Header Parser (lines 102-118 of blogmaker.py)
```python
headers = {}
i = 0
known_headers = {'date', 'draft', 'tags'}
while i < len(lines):
    line = lines[i].strip()
    if not line or line.startswith('#'):
        break
    if ':' in line:
        key, _, value = line.partition(':')
        key_lower = key.strip().lower()
        if key_lower in known_headers:
            headers[key_lower] = value.strip()
            i += 1
        else:
            break
    else:
        break
```
Note: `draft` and `tags` are already in `known_headers`. The parser will capture them. No parser changes needed.

### Current Post Dict (lines 163-177)
```python
return {
    'title': title,
    'slug': slug,
    'filename': slug,
    'date': date_obj.strftime(self.config["date_format"]),
    'iso_date': date_obj.isoformat(),
    'date_obj': date_obj,
    'content': html_content,
    'description': description,
    'cover_image': cover_image,
    'filepath': str(filepath),
    'hash': self._file_hash(filepath),
    'draft': False,       # <-- Replace with parsed value
    'tags': [],           # <-- Replace with parsed value
}
```

### Current build() Post Rendering (lines 263-288)
```python
for filepath in posts_path.glob("*.md"):
    post = self._parse_post(filepath)
    if post:
        posts.append(post)

        if self._needs_rebuild(post):
            # renders and writes HTML...
```
This loop needs to: (1) skip HTML generation for drafts, (2) pass `tags` to template render.

### Current Index Rendering (lines 312-317)
```python
posts.sort(key=lambda x: x['date_obj'], reverse=True)
index_html = index_template.render(posts=posts)
```
This needs to use `published` (draft-filtered) list instead of `posts`.

## Key Integration Points Summary

| Location | What Changes | Why |
|----------|-------------|-----|
| `_parse_post()` ~line 163 | Add draft/tags parsing from `headers` dict | Populate fields that are already initialized |
| `build()` ~line 263 | Skip HTML render for draft posts | DRFT-02 |
| `build()` ~line 263 | Delete stale HTML for draft posts | D-03 |
| `build()` ~line 270 | Add `tags=post['tags']` to render call | TAGS-02 |
| `build()` ~line 312 | Filter drafts before index render | DRFT-02 |
| `build()` after line 317 | Generate tag index pages | TAGS-03 |
| `build()` before tag gen | Clean stale `tag-*.html` files | Pitfall 2 |
| `templates/base.html` line 255 | Add tag links in `.meta` div | TAGS-02 |
| `templates/index.html` ~line 136 | Add conditional heading for tag pages | TAGS-03 |

## Open Questions

1. **Tag normalization for special characters**
   - What we know: Tags are lowercased, whitespace-trimmed (D-04)
   - What's unclear: What about hyphens, slashes, or spaces within tags? e.g., "machine-learning" vs "machine learning"
   - Recommendation: Allow hyphens in tags (common pattern). For filename safety, replace spaces with hyphens in the tag page filename. Keep it simple -- this is Claude's discretion per CONTEXT.md.

2. **Tag page size budget**
   - What we know: Index must be <10KB. Tag pages reuse the index template.
   - What's unclear: Do tag pages fall under the same 10KB limit or the 25KB post limit?
   - Recommendation: Tag pages should follow the index budget (~10KB) since they use the same template. With 15 posts max per tag, this is not a concern.

## Sources

### Primary (HIGH confidence)
- `blogmaker.py` -- direct code inspection of header parser, post dict, build() method
- `templates/base.html` -- direct template inspection
- `templates/index.html` -- direct template inspection
- `tests/test_build.py` -- existing test patterns for extending
- `.planning/phases/02-drafts-and-tags/02-CONTEXT.md` -- user decisions

### Secondary (MEDIUM confidence)
- Jinja2 3.1.x documentation (conditional rendering, loop variables) -- verified via installed version

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - no new dependencies, using existing Python/Jinja2/markdown2
- Architecture: HIGH - direct code inspection, changes are small and well-localized
- Pitfalls: HIGH - derived from code analysis of actual integration points

**Research date:** 2026-03-29
**Valid until:** Stable -- no external dependencies or fast-moving APIs involved
