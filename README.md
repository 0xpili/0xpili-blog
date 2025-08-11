# 0xpili Blog

Minimal static blog generator with dark mode support.

## Quick Start

```bash
# Install dependencies
pip install markdown2 jinja2

# Build the blog
python3 blogmaker.py

# Serve locally (http://localhost:8000)
python3 serve.py
```

## Writing Posts

Create markdown files in `posts/` with this format:

```markdown
Date: 2025 Aug 09
# Your Title Here

Your content in markdown...
```

When you add or edit a `.md` file in `posts/`:
1. Run `python3 blogmaker.py` to rebuild
2. The generator creates/updates the HTML in `docs/`
3. Changes are cached - only modified files rebuild
4. Commit and push to deploy via GitHub Pages

## Features

- Static HTML generation
- Dark/light mode with system detection
- Pink accent colors
- ~5KB average page size
- No JavaScript dependencies
- Responsive design

## Structure

- `posts/` - Markdown source files
- `templates/` - Jinja2 HTML templates
- `docs/` - Generated site (GitHub Pages)
- `blogmaker.py` - Static site generator
- `tests/` - Quality checks