# Technology Stack

**Analysis Date:** 2026-03-29

## Languages

**Primary:**
- Python 3.12+ - All server-side code and build system (`blogmaker.py`, `serve.py`)

**Secondary:**
- HTML5 - Templates and generated output
- CSS3 (inlined) - All styling embedded in page `<style>` blocks, golden ratio typography
- JavaScript - Minimal: theme toggle script only (inline in templates)

## Runtime

**Environment:**
- Python 3.12 (enforced in CI)

**Package Manager:**
- pip - Python dependency management
- Lockfile: Not used; pinned to exact versions in CI workflow

## Frameworks

**Core:**
- Jinja2 2.x - Template rendering engine for HTML generation (`templates/base.html`, `templates/index.html`, `templates/404.html`)
- markdown2 - Markdown to HTML conversion with extras: fenced-code-blocks, header-ids, tables, strike

**Testing:**
- Python unittest (stdlib) - No external test framework required; custom assertions in `tests/test_quality.py` and `tests/test_build.py`

**Build/Dev:**
- Python stdlib only - no build tool needed beyond Python itself
  - `hashlib` - SHA256-based incremental build caching (`.build_cache.json`)
  - `json` - Config and cache persistence
  - `pathlib` - Cross-platform file operations
  - `datetime` - Post date parsing
  - `http.server` - Development server (`serve.py`)
  - `socketserver` - HTTP server transport

## Key Dependencies

**Critical:**
- `markdown2` (latest) - Converts post markdown to HTML with semantic extras
- `jinja2` (latest) - Renders blog templates; core to all HTML generation

**Infrastructure:**
- None; the blog uses only Python stdlib beyond the two above

## Configuration

**Environment:**
- Configured via `CONFIG` dict in `blogmaker.py` (lines 19-30)
- Overridable with environment variables prefixed `BLOG_*` (e.g., `BLOG_SITE_URL`, `BLOG_SITE_TITLE`)
- Template: `config.example.json` provides example configuration structure
- No secrets needed; all configuration is public (site URL, titles, descriptions)

**Build:**
- Incremental builds via `.build_cache.json` - SHA256 content hashing
- Cache file auto-created on first build, updated after each successful render
- Cache key: full file path; value: first 16 chars of SHA256 hex digest

## Platform Requirements

**Development:**
- Python 3.12+
- pip for dependency installation
- `python3 -m py_compile blogmaker.py` passes syntax check
- No C extensions or compiled dependencies required

**Production:**
- Deployment: GitHub Pages (static site hosting)
- Domain: `0xpili.xyz` (configured in `docs/CNAME`)
- Output: Static HTML files in `docs/` directory (repository root for GH Pages)
- URL rewriting: `.htaccess` for clean URLs (strips `.html` extension)

## Performance Targets

**Page Size Budgets** (enforced by `test_quality.py`):
- Index: <10KB
- 404: <3KB
- Regular posts: <25KB (~8KB is inlined CSS overhead)
- Average page: <15KB
- Load time on 3G: ~0.5 seconds

**Build Performance:**
- Incremental: Only rebuilds posts whose content hash changed
- Full rebuild: <100ms for typical 15-post blog

---

*Stack analysis: 2026-03-29*
