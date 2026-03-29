# Phase 3: RSS Feed - Context

**Gathered:** 2026-03-29
**Status:** Ready for planning

<domain>
## Phase Boundary

Generate a valid RSS 2.0 feed.xml during build, containing all published (non-draft) posts with title, link, auto-generated description, and RFC 822 publication date.

</domain>

<decisions>
## Implementation Decisions

### RSS Generation
- **D-01:** Generate RSS 2.0 feed as `docs/feed.xml` using Python stdlib `xml.etree.ElementTree`.
- **D-02:** Each item includes: title, link (full URL), description (from auto-generated meta description), pubDate (RFC 822 format), guid (permalink).
- **D-03:** Feed channel includes: title (site_title), link (site_url), description (site_description), lastBuildDate.
- **D-04:** Only include published (non-draft) posts, sorted newest-first.
- **D-05:** Use plain-text descriptions (from `_extract_description`) as item descriptions to avoid CDATA/encoding issues.
- **D-06:** Include all posts (no item count limit) — 15 posts is small enough.

### Claude's Discretion
- Whether to add `<link rel="alternate" type="application/rss+xml">` autodiscovery (nice to have, not required by RSS-01)
- Exact XML formatting/indentation

</decisions>

<canonical_refs>
## Canonical References

### Engine
- `blogmaker.py` — `published` list in `build()`, `_extract_description()` method, post dict with `description` field

### Research
- `.planning/research/PITFALLS.md` — RSS encoding pitfalls, date format requirements
- `.planning/research/STACK.md` — Recommends xml.etree.ElementTree

### Prior Phase Context
- `.planning/phases/01-foundation-and-meta/01-CONTEXT.md` — Meta description decisions
- `.planning/phases/02-drafts-and-tags/02-CONTEXT.md` — Draft filtering decisions

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `published` list — already filtered, sorted newest-first in `build()`
- Post dict `description` field — auto-generated plain text, perfect for RSS items
- `CONFIG['site_url']`, `CONFIG['site_title']`, `CONFIG['site_description']` — feed channel metadata

### Integration Points
- Add RSS generation after tag page generation in `build()`
- RFC 822 date format: `post['date_obj'].strftime('%a, %d %b %Y 00:00:00 +0000')`

</code_context>

<specifics>
## Specific Ideas

No specific requirements — standard RSS 2.0 generation.

</specifics>

<deferred>
## Deferred Ideas

None.

</deferred>

---

*Phase: 03-rss-feed*
*Context gathered: 2026-03-29*
