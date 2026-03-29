# Phase 2: Drafts and Tags - Context

**Gathered:** 2026-03-29
**Status:** Ready for planning

<domain>
## Phase Boundary

Add draft post support (exclude from build) and a tag system (parse tags, display on posts, generate per-tag index pages). Both features use the loop-based header parser built in Phase 1.

</domain>

<decisions>
## Implementation Decisions

### Draft Support
- **D-01:** Parse `Draft: true` from header block using the existing loop-based parser. Case-insensitive value matching (`true`, `True`, `TRUE` all work).
- **D-02:** Draft posts are excluded from: HTML output generation, index page post list, and future RSS feed. The post dict already has `draft: False` — populate from header.
- **D-03:** If a previously published post becomes a draft, delete its stale HTML output file from `docs/`.

### Tag System
- **D-04:** Parse `Tags: crypto, ai, philosophy` from header block. Comma-separated, whitespace-trimmed, lowercased for consistency.
- **D-05:** Display tags on individual post pages as comma-separated linked text (links point to tag index pages). Style consistent with blog's minimal aesthetic.
- **D-06:** Generate per-tag index pages at `docs/tag-{name}.html` (flat structure, no subdirectory).
- **D-07:** Tag index pages reuse the index.html template pattern with a heading like "Posts tagged: crypto". List only non-draft posts with that tag, sorted newest-first.

### Claude's Discretion
- Exact CSS styling for tag links on post pages
- Whether to add tags to the index.html post listing (not required, but allowed if it fits)
- Tag normalization edge cases (hyphens, special chars)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Engine
- `blogmaker.py` — Header parser at lines 69-86 (already handles known_headers including 'draft' and 'tags'). Post dict at line 129-142 already has draft/tags fields.

### Templates
- `templates/base.html` — Post template, needs tag display addition
- `templates/index.html` — Homepage template, reuse pattern for tag pages

### Tests
- `tests/test_build.py` — Existing 37 tests to extend
- `tests/test_quality.py` — Quality checks that must continue passing

### Prior Phase Context
- `.planning/phases/01-foundation-and-meta/01-CONTEXT.md` — Header parser decisions (D-01 through D-03)

### Research
- `.planning/research/PITFALLS.md` — Draft leaking pitfall, tag casing pitfall
- `.planning/research/FEATURES.md` — Tag system feature analysis

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Header parser already recognizes 'draft' and 'tags' keys — just need to populate the dict fields
- `_extract_description()` — works for tag index pages too
- Index template pattern — reusable for tag index pages
- Post dict already has `draft: False` and `tags: []` fields initialized

### Established Patterns
- Posts return dict, build() iterates and renders — same pattern for tag pages
- Incremental build via `_needs_rebuild()` — tag pages need rebuild when any tagged post changes

### Integration Points
- `_parse_post()` — populate draft and tags from parsed headers
- `build()` — filter drafts before rendering, generate tag pages after post processing
- `templates/base.html` — add tag display section below post metadata

</code_context>

<specifics>
## Specific Ideas

No specific requirements — standard patterns. Key constraint: tag pages must respect draft filtering (no draft posts in tag listings).

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 02-drafts-and-tags*
*Context gathered: 2026-03-29*
