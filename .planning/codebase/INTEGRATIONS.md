# External Integrations

**Analysis Date:** 2026-03-29

## APIs & External Services

**None detected** - This is a static site generator with zero runtime API dependencies.

No external API calls, no SDK integrations, no third-party services.

## Data Storage

**Databases:**
- None - Blog is fully static; no database required
- No ORM or database client needed

**File Storage:**
- Local filesystem only
- Posts source: `posts/` directory (markdown files)
- Generated output: `docs/` directory (GitHub Pages root)
- Images: `docs/images/` (static assets, committed to repo)
- Configuration cache: `.build_cache.json` (JSON file, committed to repo)

**Caching:**
- Local SHA256 hash cache in `.build_cache.json` for incremental builds
- No external cache service (Redis, Memcached, etc.)
- Browser cache: Controlled via `Cache-Control: no-cache, no-store, must-revalidate` headers in `serve.py`

## Authentication & Identity

**Auth Provider:**
- None - No authentication system
- Static site accessible without login
- GitHub Pages deployment requires no authentication in output

**Authorization:**
- Not applicable - No user accounts or access control

## Monitoring & Observability

**Error Tracking:**
- None - No error monitoring service integrated

**Logs:**
- Local console output only
- Build process prints to stdout:
  - `✓ {post title}` for rebuilt posts
  - `- {post title} (unchanged)` for unchanged posts
  - Warning/error messages for missing dates or parse failures
- No persistent logging to external service

**Analytics:**
- Not detected - No analytics library or service
- No Google Analytics, Plausible, or similar
- Philosophy: No tracking, no JavaScript dependencies

## CI/CD & Deployment

**Hosting:**
- GitHub Pages
- Repository: 0xpili/blog_project
- Deployment branch: main (docs/ folder)
- Custom domain: `0xpili.xyz` (configured in `docs/CNAME`)

**CI Pipeline:**
- GitHub Actions workflow: `.github/workflows/ci.yml`
- Triggers: push to main, pull requests to main
- Runs on: ubuntu-latest
- Python 3.12 environment
- Steps:
  1. Checkout code (`actions/checkout@v4`)
  2. Setup Python 3.12 (`actions/setup-python@v5`)
  3. Install dependencies: `pip install markdown2 jinja2`
  4. Build blog: `python3 blogmaker.py`
  5. Run build tests: `python3 tests/test_build.py`
  6. Run quality tests: `python3 tests/test_quality.py`
- Deployment: Automatic to GitHub Pages on main push (GH Pages serves from docs/)

## Environment Configuration

**Required env vars:**
- None hardcoded as required
- All config has sensible defaults in `CONFIG` dict

**Optional env vars (override defaults):**
- `BLOG_SITE_URL` - Override site URL (default: `https://0xpili.xyz`)
- `BLOG_SITE_TITLE` - Override site title (default: `0xpili`)
- `BLOG_SITE_DESCRIPTION` - Override site description
- `BLOG_AUTHOR` - Override author name
- `BLOG_TEMPLATES_DIR` - Override templates directory path (default: `templates`)
- `BLOG_POSTS_DIR` - Override posts source directory (default: `posts`)
- `BLOG_OUTPUT_DIR` - Override output directory (default: `docs`)

**Secrets location:**
- Not applicable - No secrets in this static site
- No API keys, credentials, or sensitive configuration needed

## Webhooks & Callbacks

**Incoming:**
- None - Static site, no incoming webhooks

**Outgoing:**
- None - No outgoing webhook calls

**GitHub Integration:**
- GitHub Pages deployment (automatic, no webhook needed)
- CI/CD via GitHub Actions (event-driven on push/PR)

## Content Management

**Post Source Format:**
- Markdown files in `posts/` directory
- Required header: `Date: YYYY Mon DD` (e.g., `Date: 2025 Mar 29`)
- Optional title: First `# Heading` in post becomes title; filename used as fallback
- Cover image: First `![alt](url)` image in post becomes cover (removed from body)
- Markdown extras enabled: fenced-code-blocks, header-ids, tables, strike

**Template System:**
- Jinja2 variables passed from `BlogBuilder.build()` to templates:
  - `title`, `date`, `content` (HTML), `cover_image`, `slug`, `description`, `site_url`, `site_title`, `posts` (list for index)
- Template rendering happens in memory; output written to files

## Build System

**Entry Point:**
- `python3 blogmaker.py` - Full build with incremental caching
- No build flags or CLI options; all configuration via environment variables

**Incremental Build Logic:**
- Cache: `.build_cache.json` stores `{filepath: sha256_hash}`
- Rebuild triggers: Content hash changed OR output file missing
- Pages and posts evaluated separately; both support incremental builds

**Static File Handling:**
- `.htaccess` for URL rewriting (in `docs/`)
- `CNAME` for custom domain (in `docs/`)
- No asset pipeline or minification

---

*Integration audit: 2026-03-29*
