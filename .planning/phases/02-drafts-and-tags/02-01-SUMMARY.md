---
phase: 02-drafts-and-tags
plan: 01
subsystem: build
tags: [draft, static-site, content-management]

requires:
  - phase: 01-foundation
    provides: Header parser with known_headers allowlist, post dict with draft placeholder
provides:
  - Draft header parsing (case-insensitive) in _parse_post()
  - Draft filtering in build() separating published from draft posts
  - Stale HTML cleanup when published post becomes draft
affects: [02-02 tag system must also exclude drafts]

tech-stack:
  added: []
  patterns: [multi-header parsing loop in _parse_post, published/draft separation in build]

key-files:
  created: []
  modified: [blogmaker.py, tests/test_build.py]

key-decisions:
  - "Header parsing refactored to loop over known_headers set instead of single Date line"
  - "Draft filtering uses separate published list rather than removing from posts in-place"
  - "Stale HTML cleanup runs before build loop to handle draft transitions"

patterns-established:
  - "Header parsing: loop with known_headers set and key:value splitting"
  - "Content filtering: separate published list for index, full list for processing"

requirements-completed: [DRFT-01, DRFT-02]

duration: 2min
completed: 2026-03-29
---

# Phase 02 Plan 01: Draft Support Summary

**Case-insensitive Draft header parsing with stale HTML cleanup and 6 TDD tests**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-29T23:09:45Z
- **Completed:** 2026-03-29T23:11:17Z
- **Tasks:** 1
- **Files modified:** 2

## Accomplishments
- Draft header parsed case-insensitively (true/True/TRUE) via known_headers loop
- Draft posts excluded from HTML output and index page listing
- Stale HTML files automatically deleted when a published post becomes a draft
- 6 comprehensive draft tests added following TDD (RED then GREEN)

## Task Commits

Each task was committed atomically:

1. **Task 1: Draft parsing and filtering with tests** - `cea1ac4` (feat)

## Files Created/Modified
- `blogmaker.py` - Added multi-header parsing loop, draft filtering, stale cleanup in build()
- `tests/test_build.py` - Added 6 draft-related tests

## Decisions Made
- Refactored header parsing from single Date: line extraction to a loop over known_headers set -- enables future header additions (Tags, Description, etc.)
- Used separate `published` list for index rendering rather than mutating `posts` list in-place -- preserves full post list for stale cleanup logic

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Known Stubs
None.

## Next Phase Readiness
- Draft support complete, ready for Plan 02 (tag system)
- Tag system can use the same known_headers pattern for Tags header parsing
- Tag pages must filter draft posts using the same published list pattern

---
*Phase: 02-drafts-and-tags*
*Completed: 2026-03-29*
