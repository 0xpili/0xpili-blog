# Codebase Concerns

**Analysis Date:** 2026-03-29

## Performance Bottlenecks

**Unoptimized image assets:**
- Problem: Images in `docs/images/` are large JPEGs (4MB, 3.9MB, 2.3MB) — these account for 10MB of the 11MB total site size
- Files: `docs/images/agentic-zero1.jpg`, `docs/images/agenticzero3.jpg`, `docs/images/agentic-zero2.jpg`
- Cause: High-resolution source images are served uncompressed and without modern formats (WebP)
- Improvement path: Compress JPEGs to <500KB each, provide WebP alternatives, consider lazy loading in base template
- Impact: Visitors on slow connections (3G) will load 10MB+ just for images, violating the "fucking FAST" philosophy

**Cache invalidation risk:**
- Problem: SHA256 hash stored in `.build_cache.json` is truncated to 16 characters, creating collision risk
- Files: `blogmaker.py` line 60, `.build_cache.json` (all entries)
- Cause: Micro-optimization reducing hash storage size
- Improvement path: Store full 64-character hash or use guaranteed unique hash algorithm
- Current mitigation: Collision probability is low but not impossible with many files

## Tech Debt

**Bare exception handling:**
- Problem: Catch-all `except:` without exception type (line 50 in `blogmaker.py`)
- Files: `blogmaker.py` line 50 in `_load_cache()`
- Impact: Masks all errors (including KeyboardInterrupt, SystemExit) instead of just JSON errors
- Fix approach: Replace `except:` with `except (json.JSONDecodeError, IOError):`

**Unused template variable:**
- Problem: `description=None` passed to post and page templates in 6 locations but never populated
- Files: `blogmaker.py` lines 214, 239
- Impact: Meta descriptions in HTML always fall back to default, missing SEO opportunity
- Current behavior: All pages show generic description instead of derived from content
- Fix approach: Extract first 160 chars of post content as description, or use first paragraph

**Stateless date handling:**
- Problem: Post `date_obj` (Python datetime) stored in post dict but not serialized or cached
- Files: `blogmaker.py` line 109
- Impact: Re-parsed on every build; if parsing changes, post order could change unexpectedly
- Fix approach: Cache or validate date parsing separately

**Bare filename to title conversion:**
- Problem: Title derived from filename by splitting hyphens and title-casing (`the-complexity-tax` → `The Complexity Tax`) with no override
- Files: `blogmaker.py` lines 85, 150
- Impact: Posts with acronyms (e.g., `defi-agents`) render incorrectly (`Defi Agents` not `DeFi Agents`)
- Current workaround: Set explicit `# Title` heading in post markdown
- Fix approach: Document that explicit headings are required for proper capitalization

## Code Quality

**Inconsistent error logging:**
- Problem: Some errors print to stdout, others silently return None
- Files: `blogmaker.py` lines 68, 80, 117-118, 170-171
- Impact: Build errors are not consistently visible; silent failures in `_parse_post()` may hide corrupted posts
- Example: Invalid date format prints warning but post is skipped with no exception
- Fix approach: Centralize error logging, optionally collect errors for summary

**No validation of template existence:**
- Problem: Template loading catches exceptions but doesn't validate templates are loadable before build
- Files: `blogmaker.py` lines 185-192
- Impact: Large build can complete before discovering template is missing
- Fix approach: Validate all templates exist during `__init__`

**Magic strings in code:**
- Problem: Hardcoded regex patterns, image path handling, and markdown extras scattered throughout
- Files: `blogmaker.py` lines 74-76 (ordinal suffix removal), 126-138 (image path parsing), 100 (markdown extras)
- Impact: Difficult to maintain or test in isolation
- Fix approach: Extract to constants or methods

## Fragile Areas

**Image extraction logic:**
- Problem: Image URL extraction depends on exact markdown format `![alt](url)` with specific character positions
- Files: `blogmaker.py` lines 120-141
- Impact: Any variation (extra spaces, different syntax) will fail silently and not extract cover image
- Current detection: `stripped.startswith('![') and '](' in stripped and stripped.endswith(')')`
- Risk: Brittle string parsing with no fallback
- Safe modification: Use regex parser or markdown AST instead of string matching

**Incremental build with deleted posts:**
- Problem: `.build_cache.json` retains entries for deleted post files — orphaned cache entries accumulate
- Files: `blogmaker.py` (no cleanup in `_save_cache()`), `.build_cache.json`
- Impact: Cache file grows indefinitely; deleted posts leave traces
- Fix approach: Prune cache entries for non-existent files during save

**Hard-coded output directory check:**
- Problem: `_needs_rebuild()` checks output file existence but does NOT validate file is valid HTML
- Files: `blogmaker.py` line 177
- Impact: Corrupted or partial HTML output from previous run will be treated as "up to date"
- Fix approach: Validate output HTML is well-formed or use timestamp + hash combo

## Security Considerations

**Markdown injection risk:**
- Problem: Post content is marked as `safe` and rendered unescaped via `|safe` filter
- Files: `templates/base.html` line 28, `templates/page.html` line 230
- Current trust model: Posts are trusted (not from untrusted sources)
- Risk: If posts ever accept user input or external markdown, XSS is possible
- Recommendation: Document that post content must be trusted; consider sanitizing if model changes

**No input validation on config:**
- Problem: Environment variables override CONFIG with no validation
- Files: `blogmaker.py` lines 273-276
- Current mitigation: CLI-only tool, no web input
- Risk: If blogmaker ever exposes a web API, arbitrary paths could be injected
- Recommendation: Validate config values against whitelist if this tool becomes a service

## Missing Critical Features

**No drafts/unpublished post support:**
- Problem: All files in `posts/` are published; no way to work on unpublished content
- Impact: Draft posts must be stored outside the repo or in non-`.md` format
- Fix approach: Support `draft: true` in post header or prefix (e.g., `_draft-post.md`)

**No redirect/alias support:**
- Problem: Posts can't have canonical redirects if URL slug changes
- Impact: URL changes break external links permanently
- Fix approach: Support `redirects:` or `aliases:` field in post header

**No built-in search:**
- Problem: Blog has no search functionality; users can't find posts except via homepage
- Current state: Static HTML only, no backend
- Note: This is by design (no JavaScript), but worth documenting as limitation

**No post metadata extraction:**
- Problem: Posts can only have title, date, and cover image; no tags, categories, or author
- Impact: Can't organize or filter posts thematically
- Fix approach: Support optional YAML frontmatter or structured metadata

## Test Coverage Gaps

**No tests for image extraction:**
- What's not tested: Cover image detection, path normalization
- Files: `blogmaker.py` lines 120-141 (untested)
- Risk: Edge cases in image URL parsing could break cover images without test failure
- Priority: Medium

**No tests for date parsing edge cases:**
- What's not tested: Invalid dates, ordinal suffix removal, boundary dates
- Files: `blogmaker.py` lines 71-81 (partially tested, but no edge case coverage)
- Risk: Parsing failures are caught but exact behavior isn't validated
- Priority: Medium

**No tests for markdown rendering:**
- What's not tested: Which markdown extras are enabled, HTML output quality
- Files: `blogmaker.py` lines 98-101, 158-161
- Risk: Markdown rendering can change without tests catching it
- Priority: Low (markdown2 handles this)

**No tests for template rendering failures:**
- What's not tested: Jinja2 errors, missing template variables
- Files: `blogmaker.py` lines 207-224 (error handling only)
- Risk: Template rendering errors are caught but behavior isn't validated
- Priority: Low

## Dependency Risk

**Locked to markdown2 extras:**
- Risk: Markdown extras are hardcoded and can't be configured
- Impact: If a feature needs different extras (e.g., footnotes), code must change
- Mitigation: Low impact (extras are stable)

**Python version assumption:**
- Problem: Code uses type hints (Dict, List, Optional) requiring Python 3.5+
- Current requirement: CI uses Python 3.12
- Risk: If deployed on older Python, will fail
- Recommendation: Add python_requires in setup or document 3.9+ requirement

## Scaling Limits

**Single-pass build:**
- Current: Builds all posts, pages, index, 404 in one pass with no parallelization
- Limit: At 15 posts, build is <1s; at 1000+ posts, build will be slow
- Scaling path: Implement parallel post rendering or multi-file template caching

**Cache file size:**
- Current: `.build_cache.json` grows linearly with post count
- Limit: At 10,000 posts, cache will be ~500KB (negligible)
- Not a concern

**Output directory flat structure:**
- Current: All posts at `docs/post-slug.html`; no subdirectories
- Limit: Works fine; GitHub Pages serves any .html filename
- Not a concern

---

*Concerns audit: 2026-03-29*
