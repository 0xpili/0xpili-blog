# Roadmap: 0xpili Blog Improvements

## Overview

Three phases take the blog engine from its current state to a feature-complete v1 with meta descriptions, RSS, drafts, and tags -- all while preserving zero external dependencies and sub-second load times. The code quality and header parser refactor come first because every new feature depends on clean, extensible header parsing. Meta descriptions slot into Phase 1 since the templates are already wired and the value feeds directly into RSS. Author workflow features (drafts, tags) follow in Phase 2 using the new header parser. RSS is the capstone in Phase 3, consuming meta descriptions for item content and respecting draft filtering.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Foundation and Meta** - Refactor header parsing, fix code quality issues, add meta descriptions
- [ ] **Phase 2: Drafts and Tags** - Draft post support and tag system using the new header parser
- [ ] **Phase 3: RSS Feed** - Generate valid RSS 2.0 feed consuming meta descriptions and respecting drafts

## Phase Details

### Phase 1: Foundation and Meta
**Goal**: The blog engine has clean, extensible header parsing and every post has an auto-generated meta description
**Depends on**: Nothing (first phase)
**Requirements**: QUAL-01, QUAL-02, QUAL-03, QUAL-04, QUAL-05, META-01
**Success Criteria** (what must be TRUE):
  1. All 15 existing posts build identically before and after the header parser refactor (no regressions)
  2. The header parser handles arbitrary Key: Value pairs, not just Date and Title by index position
  3. Every generated post HTML contains a meta description tag with content derived from the post body
  4. No bare except clauses remain in the codebase; image extraction uses regex
  5. Tests exist and pass for cover image extraction edge cases and date parsing edge cases
**Plans:** 2 plans

Plans:
- [x] 01-01-PLAN.md — Refactor header parser, image regex, bare except fix, edge-case tests
- [ ] 01-02-PLAN.md — Auto-generate meta descriptions from post content

### Phase 2: Drafts and Tags
**Goal**: Authors can mark posts as drafts to exclude them from the live site, and can categorize posts with tags displayed on post pages and browsable via tag index pages
**Depends on**: Phase 1
**Requirements**: DRFT-01, DRFT-02, TAGS-01, TAGS-02, TAGS-03
**Success Criteria** (what must be TRUE):
  1. A post with `Draft: true` header is excluded from the index page and produces no HTML output in docs/
  2. Tags specified via `Tags: crypto, ai` header appear on the rendered post page
  3. Per-tag index pages are generated listing only posts with that tag
  4. Existing posts without Draft or Tags headers build without any changes needed
**Plans**: TBD
**UI hint**: yes

### Phase 3: RSS Feed
**Goal**: The blog publishes a valid RSS 2.0 feed that readers can subscribe to
**Depends on**: Phase 2
**Requirements**: RSS-01
**Success Criteria** (what must be TRUE):
  1. Running the build produces a docs/feed.xml file containing all published (non-draft) posts
  2. Each feed item includes title, link, auto-generated description, and publication date in RFC 822 format
  3. The feed validates as well-formed XML (parseable by xml.etree.ElementTree round-trip)
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation and Meta | 0/2 | Planned | - |
| 2. Drafts and Tags | 0/TBD | Not started | - |
| 3. RSS Feed | 0/TBD | Not started | - |
