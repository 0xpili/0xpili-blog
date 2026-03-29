# Requirements: 0xpili Blog Improvements

**Defined:** 2026-03-29
**Core Value:** Every improvement preserves zero external dependencies, sub-second load times, and austere minimalism.

## v1 Requirements

### Meta Descriptions

- [ ] **META-01**: Auto-generate description from first ~160 chars of post markdown content

### RSS Feed

- [ ] **RSS-01**: Generate valid RSS 2.0 feed.xml during build with title, link, description, pub date per post

### Draft Support

- [ ] **DRFT-01**: Support `Draft: true` header field to exclude posts from build output
- [ ] **DRFT-02**: Draft posts excluded from index page, RSS feed, and HTML generation

### Tags

- [ ] **TAGS-01**: Parse `Tags: crypto, ai` header field from post metadata
- [ ] **TAGS-02**: Display tags on individual post pages
- [ ] **TAGS-03**: Generate per-tag index pages listing filtered posts

### Code Quality

- [x] **QUAL-01**: Fix bare `except:` to specific exception types
- [x] **QUAL-02**: Replace string-based image extraction with regex
- [x] **QUAL-03**: Refactor header parser from index-based to loop-based
- [x] **QUAL-04**: Add tests for cover image extraction edge cases
- [x] **QUAL-05**: Add tests for date parsing edge cases

## v2 Requirements

### RSS Enhancements

- **RSS-V2-01**: Configurable item count limit for feed
- **RSS-V2-02**: Add `<link rel="alternate">` autodiscovery in HTML templates

### Meta Enhancements

- **META-V2-01**: Populate og:description from auto-generated description

### Tags Enhancements

- **TAGS-V2-01**: Tag pages reachable via clean URLs

## Out of Scope

| Feature | Reason |
|---------|--------|
| Search functionality | Requires JavaScript, violates zero-JS philosophy |
| Image optimization | Separate concern, not part of this milestone |
| Post excerpts on homepage | Not selected by user |
| Cache cleanup for deleted posts | Low priority, not selected |
| Tag index pages with pagination | Overkill for 15 posts |
| Full HTML content in RSS items | Plain text descriptions avoid CDATA/encoding pitfalls |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| QUAL-01 | Phase 1 | Complete |
| QUAL-02 | Phase 1 | Complete |
| QUAL-03 | Phase 1 | Complete |
| QUAL-04 | Phase 1 | Complete |
| QUAL-05 | Phase 1 | Complete |
| META-01 | Phase 1 | Pending |
| DRFT-01 | Phase 2 | Pending |
| DRFT-02 | Phase 2 | Pending |
| TAGS-01 | Phase 2 | Pending |
| TAGS-02 | Phase 2 | Pending |
| TAGS-03 | Phase 2 | Pending |
| RSS-01 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 12 total
- Mapped to phases: 12
- Unmapped: 0

---
*Requirements defined: 2026-03-29*
*Last updated: 2026-03-29 after roadmap creation*
