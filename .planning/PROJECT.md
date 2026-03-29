# 0xpili Blog Improvements

## What This Is

A set of targeted improvements to the 0xpili static blog engine — adding missing reader-facing features (meta descriptions, RSS feed, tags), improving the author workflow (drafts), and cleaning up code quality (error handling, image parsing, test coverage). The blog is a Python-based static site generator serving 15+ posts at 0xpili.xyz.

## Core Value

Every improvement must preserve the blog's core identity: zero external dependencies, sub-second load times, and austere minimalism. Nothing added should increase page weight meaningfully or introduce JavaScript libraries.

## Requirements

### Validated

- ✓ Static site generation from markdown to HTML — existing
- ✓ Incremental builds via SHA256 content hashing — existing
- ✓ Dark/light theme with CSS variables — existing
- ✓ Inlined CSS, no external stylesheets or fonts — existing
- ✓ GitHub Pages deployment from docs/ — existing
- ✓ Quality tests enforcing size budgets and accessibility — existing
- ✓ Static pages support (pages/ directory) — existing

### Active

- [ ] Auto-generate meta descriptions from post content (first ~160 chars)
- [ ] Generate RSS/Atom feed during build
- [ ] Draft post support (skip unpublished posts during build)
- [ ] Optional tags/categories in post metadata
- [ ] Fix bare except clause in cache loading
- [ ] Robust image extraction using regex instead of string parsing
- [ ] Test coverage for image extraction and date parsing edge cases

### Out of Scope

- Search functionality — would require JavaScript, violates core philosophy
- Post excerpts on homepage — user did not select this
- Image optimization — separate concern, not part of this milestone
- Cache cleanup for deleted posts — low priority, not selected
- JavaScript libraries of any kind — core constraint

## Context

- Blog has 15 posts spanning crypto, AI, philosophy, athletics
- Engine is `blogmaker.py` (~283 lines), single BlogBuilder class
- Posts use `Date: YYYY Mon DD` header format, optional `# Title` heading
- Templates: Jinja2 with all CSS inlined (base.html, index.html, page.html, 404.html)
- Only 2 dependencies: markdown2, jinja2
- Tests: test_quality.py (HTML quality, performance) and test_build.py (build system)
- CI: GitHub Actions runs build + both test suites

## Constraints

- **No new dependencies**: Must use only markdown2, jinja2, and Python stdlib
- **Page size budgets**: Index <10KB, posts <25KB, 404 <3KB
- **No external resources**: No CDN fonts, external CSS/JS, tracking
- **Backward compatible post format**: Existing posts must build without changes
- **Test-driven**: Write tests first, then implement (per CLAUDE.md workflow)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Meta descriptions from first paragraph | Simple, no new post format needed | — Pending |
| RSS as XML generated during build | No dependencies, standard format | — Pending |
| Draft support via header field | Consistent with existing Date: header pattern | — Pending |
| Tags as comma-separated header field | Minimal syntax, easy to parse | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-29 after initialization*
