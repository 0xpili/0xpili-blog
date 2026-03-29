# Research Summary: 0xpili Blog Improvements

**Domain:** Static blog generator feature additions (RSS, meta descriptions, drafts, tags)
**Researched:** 2026-03-29
**Overall confidence:** HIGH

## Executive Summary

The 0xpili blog engine needs four features that are standard in every static site generator: meta descriptions, RSS feeds, draft support, and tags. The good news is that all four can be implemented using only Python's standard library and the existing two dependencies (markdown2, jinja2). No new packages are needed.

The most important architectural insight is that the current ad-hoc header parsing (hardcoded line indices for Date and Title) must be refactored into a generic `Key: Value` header parser before adding Draft and Tags headers. This is a ~10-line refactor that unblocks two features and makes the codebase extensible for future metadata fields. Without this refactor, adding headers creates brittle index arithmetic that will break on edge cases.

RSS 2.0 is the right feed format (not Atom, not JSON Feed). It should be generated using `xml.etree.ElementTree` from stdlib, which handles XML escaping automatically. However, there is a known pitfall: ElementTree does not natively support CDATA sections, which means HTML content in feed descriptions must be either entity-encoded or the description should use plain text (the meta description). Using the auto-generated plain-text meta description as the RSS item description sidesteps this problem entirely.

The templates are already wired for meta descriptions (`{{ description }}` placeholders exist in base.html and page.html) but receive `None` for every post. The implementation is primarily about generating the value, not plumbing it through.

## Key Findings

**Stack:** Python stdlib only (xml.etree.ElementTree, re). Zero new dependencies.
**Architecture:** Extend the post dict with 3 new fields (description, draft, tags). Filter drafts before rendering. Generate feed.xml as final build step.
**Critical pitfall:** Header parser refactor must happen first or new headers will break existing post parsing via fragile line-index arithmetic.

## Implications for Roadmap

Based on research, suggested phase structure:

1. **Code Quality + Header Parser Refactor** - Foundation phase
   - Addresses: bare except fix, image regex fix, generic header parsing
   - Avoids: Pitfall 10 (new headers breaking line-index parsing), Pitfall 2 (existing posts breaking)
   - Rationale: Every subsequent feature depends on clean header parsing

2. **Meta Descriptions** - Quick win, high SEO impact
   - Addresses: auto-generated descriptions, OG description
   - Avoids: Pitfall 4 (markdown artifacts in descriptions), Pitfall 8 (short content edge cases)
   - Rationale: Needed by RSS feed items. Templates already wired up.

3. **Draft Support + Tags** - Author workflow improvements
   - Addresses: draft filtering, tag parsing and display
   - Avoids: Pitfall 3 (drafts leaking to production), Pitfall 6 (tag casing duplicates)
   - Rationale: Both use the new header parser. Draft filtering must be in place before RSS.

4. **RSS Feed** - Capstone feature, depends on all above
   - Addresses: feed.xml generation, feed autodiscovery link
   - Avoids: Pitfall 1 (invalid XML), Pitfall 5 (wrong date format), Pitfall 9 (unbounded feed size)
   - Rationale: Uses meta descriptions for item content. Must respect draft filtering.

**Phase ordering rationale:**
- Header parser refactor is foundational -- drafts and tags both need it
- Meta descriptions are a prerequisite for good RSS item descriptions
- Draft filtering must exist before RSS generation (or drafts leak into the feed)
- RSS is the capstone that consumes all other features

**Research flags for phases:**
- Phase 1 (header refactor): Needs snapshot tests of all 15 existing posts before refactoring
- Phase 4 (RSS): Needs W3C Feed Validator testing; CDATA vs entity-encoding decision for descriptions
- All phases: Build cache does not track template changes -- clearing cache between feature additions is necessary

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All stdlib, no version concerns, stable APIs |
| Features | HIGH | Standard SSG features, well-understood patterns |
| Architecture | HIGH | Analysis of existing codebase, straightforward extensions |
| Pitfalls | HIGH | Common issues documented across SSG ecosystem |

## Gaps to Address

- **CDATA in RSS:** ElementTree lacks native CDATA support. Using plain-text descriptions (not HTML) in feed items avoids this entirely, but if full HTML content is ever desired in feeds, a string-template approach would be needed. This is a design decision, not a blocker.
- **Template cache invalidation:** The build cache does not track template file changes. When templates change (e.g., adding tag display, RSS link), posts are not rebuilt. Manual cache clearing is needed during development. A template-hash-in-cache enhancement could be a future improvement.
- **Tag index pages:** Deferred from this milestone. When the blog grows past ~30 posts, tag index pages become valuable. The tag parsing infrastructure built now will support them later.
