# Phase 1: Foundation and Meta - Context

**Gathered:** 2026-03-29
**Status:** Ready for planning

<domain>
## Phase Boundary

Refactor the blog engine's header parsing from index-based to loop-based, fix code quality issues (bare except, string-based image extraction), add comprehensive tests for image extraction and date parsing, and auto-generate meta descriptions from post content.

</domain>

<decisions>
## Implementation Decisions

### Header Parser Refactor
- **D-01:** Parse headers as `Key: Value` lines until the first blank line or first `# ` heading. This replaces the current index-based approach (`lines[0]` for Date, `lines[1]` for Title).
- **D-02:** The parser must be backward-compatible — all 15 existing posts must build identically before and after the refactor.
- **D-03:** Supported headers for now: `Date:`, `Draft:`, `Tags:`. Title remains extracted from the first `# ` heading after the header block.

### Meta Description Generation
- **D-04:** Extract description from raw markdown text (not rendered HTML). Strip markdown syntax (links, images, bold, italic, code) to get plain text, then truncate to ~160 characters at a word boundary.
- **D-05:** Populate the existing `description` parameter in template render calls (currently `None`). Templates already have `{{ description }}` plumbing.

### Image Extraction
- **D-06:** Replace string-based image detection with a regex pattern matching `![alt](url)`. Only standard inline image syntax — no reference-style images (not used in any existing post).

### Exception Handling
- **D-07:** Replace bare `except:` in `_load_cache()` with `except (json.JSONDecodeError, IOError):`.

### Claude's Discretion
- Exact regex pattern for image extraction
- How to strip markdown syntax from description text (regex vs simple replacements)
- Test structure and organization within test files

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Engine
- `blogmaker.py` — The entire build engine. Header parsing at lines 62-89, image extraction at lines 120-141, cache loading at line 50.

### Templates
- `templates/base.html` — Post template with existing `{{ description }}` variable in meta tags
- `templates/page.html` — Page template with existing `{{ description }}` variable

### Tests
- `tests/test_build.py` — Existing build tests to extend
- `tests/test_quality.py` — Quality checks that must continue passing

### Research
- `.planning/research/PITFALLS.md` — Header parser fragility (Pitfall 10), description extraction gotchas (Pitfall 4)
- `.planning/research/ARCHITECTURE.md` — Component boundaries and data flow for the refactor

### Codebase Maps
- `.planning/codebase/CONVENTIONS.md` — Code style and patterns to follow
- `.planning/codebase/TESTING.md` — Test structure and practices

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `BlogBuilder._parse_post()` — Current header/content parser to refactor in place
- `BlogBuilder._extract_cover_image()` — Image extraction method to rewrite with regex
- Template `description` plumbing — Already wired in base.html and page.html, just receiving `None`

### Established Patterns
- Posts return dict with keys: title, slug, date, iso_date, date_obj, content, cover_image, filepath, hash
- Markdown extras: fenced-code-blocks, header-ids, tables, strike
- Tests use Python unittest, custom assertions in test files

### Integration Points
- `_parse_post()` return dict gets a new `description` field
- `build()` method passes `description` to template render calls (replacing `None`)
- `_parse_page()` should also get description generation for consistency

</code_context>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches. The key constraint is backward compatibility with all 15 existing posts.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 01-foundation-and-meta*
*Context gathered: 2026-03-29*
