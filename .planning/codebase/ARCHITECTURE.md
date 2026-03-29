# Architecture

**Analysis Date:** 2026-03-29

## Pattern Overview

**Overall:** Static Site Generator (SSG) with Incremental Build Cache

**Key Characteristics:**
- Single-class monolithic architecture: `BlogBuilder` in `blogmaker.py` orchestrates the entire pipeline
- Content-driven: Markdown files are the source of truth; HTML is generated on demand
- Incremental builds via SHA256 content hashing to minimize regeneration
- Template-driven rendering using Jinja2 with inlined CSS (no external stylesheets)
- Stateless build process—cache only stores file hashes, no persistent state

## Layers

**Build Engine (`blogmaker.py`):**
- Purpose: Parse markdown posts/pages, compute hashes, render templates, write HTML
- Location: `blogmaker.py` (entire 283-line file is the engine)
- Contains: `BlogBuilder` class with methods for parsing, caching, rendering
- Depends on: `markdown2` (markdown→HTML), `jinja2` (templating), Python stdlib (hashlib, pathlib, datetime)
- Used by: CLI entry point `main()` which reads environment-overridden CONFIG dict

**Rendering Layer (Jinja2 Templates):**
- Purpose: Transform post/page data into final HTML documents
- Location: `templates/` directory
- Contains: Three templates — `base.html` (post layout), `index.html` (homepage), `page.html` (static pages), `404.html` (error page)
- Depends on: Post/page metadata (title, date, slug, content, cover_image)
- Used by: `BlogBuilder.build()` method via `self.env.get_template()`

**Content Layer (Markdown Source):**
- Purpose: Author-editable source for blog posts and static pages
- Location: `posts/` (15 markdown files with `Date:` header), `pages/` (static pages like about.md)
- Contains: Markdown with optional YAML-style date header, title heading, markdown body, cover image
- Depends on: None (leaf layer)
- Used by: `BlogBuilder._parse_post()` and `_parse_page()` methods

**Output Layer (Static HTML):**
- Purpose: GitHub Pages-served static site
- Location: `docs/` (generated on each build, committed to git)
- Contains: One HTML file per post/page, `index.html`, `404.html`, images in `docs/images/`, `.htaccess` for URL rewriting
- Depends on: Build engine to generate
- Used by: Web browser via GitHub Pages at `0xpili.xyz`

**Development Server:**
- Purpose: Local preview with no-cache headers for development
- Location: `serve.py` (simple Python HTTP server wrapper)
- Serves from: `docs/` at port 8000
- Used by: Developer for testing before push

## Data Flow

**Build Execution:**

1. `main()` reads environment variables to override CONFIG defaults
2. `BlogBuilder(config)` initializes:
   - Loads `.build_cache.json` (SHA256 hashes of source files)
   - Sets up Jinja2 environment pointing to `templates/` directory
3. `build()` orchestrates the pipeline:
   - Loads `base.html`, `page.html`, `index.html`, `404.html` templates
   - Reads all `*.md` files from `posts_dir` and `pages_dir`
4. For each post:
   - `_parse_post(filepath)` → extracts Date header, title, slug, markdown content, cover image
   - `_file_hash(filepath)` → computes SHA256 hex (first 16 chars) of file contents
   - `_needs_rebuild()` → compares hash against cache and output file existence
   - If rebuild needed: `base.html` renders post with context variables, HTML written to `docs/{slug}.html`
   - Cache updated with new hash
5. For each page:
   - `_parse_page(filepath)` → similar to post but no date header
   - `page.html` renders static page
6. All posts sorted by date (newest first)
7. `index.html` renders with sorted posts list
8. `404.html` renders (no context needed)
9. Cache saved to `.build_cache.json`

**Markdown Parsing:**

- Post header: `Date: YYYY Mon DD` (e.g., `Date: 2025 May 14`)
- Optional title: First line starting with `# ` becomes title; otherwise derived from filename
- Ordinal suffixes (st, nd, rd, th) stripped from dates before parsing
- Cover image: First standalone markdown image `![alt](url)` becomes cover; subsequent images remain in body
- Extras enabled in markdown2: `fenced-code-blocks`, `header-ids`, `tables`, `strike`

**Theme Switching:**

- Client-side JavaScript in both templates (base.html, index.html)
- On page load: checks `localStorage.theme`, falls back to `prefers-color-scheme` media query
- Toggle button updates `data-theme` attribute on document root, saves to localStorage
- CSS variables switch: light theme `--ink: #1a1a1a`, dark theme `--ink: #e0e0e0`

**Caching Strategy:**

- `.build_cache.json`: Maps `filepath` → 16-char SHA256 hex
- Incremental build: Only regenerates if hash changed OR output file missing
- Cache persists across builds; manually delete to force full rebuild

## Key Abstractions

**BlogBuilder Class:**
- Purpose: Encapsulates the entire build pipeline
- Location: `blogmaker.py` lines 32-269
- Pattern: Stateful class initialized with config dict; methods handle parsing, hashing, rendering
- Responsibilities: load cache, parse files, compute hashes, check rebuild needs, render templates, write output, save cache

**Post/Page Data Structure:**
- Purpose: Canonical representation of parsed content
- Pattern: Dictionary with keys: `title`, `slug`, `date`, `iso_date`, `date_obj`, `content`, `cover_image`, `filepath`, `hash`
- Passed to templates via Jinja2 context
- Examples: Return values of `_parse_post()` (line 103) and `_parse_page()` (line 163)

**CONFIG Dictionary:**
- Purpose: Centralized configuration with env var overrides
- Location: `blogmaker.py` lines 19-30
- Pattern: Key-value pairs overridable via `BLOG_*` environment variables (line 274-276)
- Keys: `site_url`, `site_title`, `site_description`, `author`, `templates_dir`, `posts_dir`, `pages_dir`, `output_dir`, `cache_file`, `date_format`

## Entry Points

**CLI Entry Point:**
- Location: `blogmaker.py` lines 272-280
- Triggers: `python3 blogmaker.py` command
- Responsibilities:
  1. Override CONFIG with environment variables
  2. Instantiate BlogBuilder
  3. Call `build()` to orchestrate the pipeline

**Development Server Entry Point:**
- Location: `serve.py` lines 19-32
- Triggers: `python3 serve.py` command
- Responsibilities:
  1. Start HTTP server on port 8000
  2. Serve `docs/` directory with no-cache headers
  3. Handle Ctrl+C gracefully

**GitHub Actions CI/CD:**
- Location: `.github/workflows/ci.yml`
- Triggers: Push to main, pull requests
- Responsibilities:
  1. Install dependencies (`pip install markdown2 jinja2`)
  2. Build blog (`python3 blogmaker.py`)
  3. Run tests (`python3 tests/test_build.py`, `python3 tests/test_quality.py`)

## Error Handling

**Strategy:** Fail-fast with warnings, skip invalid files

**Patterns:**

- Missing date header: Warning printed, post skipped (line 68)
- Invalid date format: Warning printed, post skipped (line 80)
- Missing required directories: Error printed, build returns early (line 198)
- Template loading errors: Error printed, build returns early (line 191)
- Individual post/page render errors: Error printed for that post/page, build continues (line 223, 245)
- Missing optional pages directory: Gracefully handled with `.exists()` check (line 230)

**No try-catch on file I/O:** Exceptions bubble up uncaught (e.g., `_parse_post` line 64 `read_text()`)

## Cross-Cutting Concerns

**Logging:**
- Print statements only, no logging library
- Status messages: "Building blog...", "✓ {title}", "- {title} (unchanged)", "✗ Error building..."
- Errors and warnings go to stdout

**Validation:**
- Post date format validated against `date_format` config (default `%Y %b %d`)
- Required date header checked; posts without it are skipped
- Output directories created if missing with `mkdir(exist_ok=True)`

**Authentication:**
- None—static site with no backend; no user authentication needed

**Content Security:**
- Markdown content passed to markdown2 with explicit extras; result marked safe in template with `|safe` filter (base.html line 256)
- No user input sanitization beyond markdown2's built-in handling
- HTML generated server-side only; no user-generated HTML accepted

---

*Architecture analysis: 2026-03-29*
