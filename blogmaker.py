#!/usr/bin/env python3
"""
A minimalist blog generator built for decades, not quarters.
Fast, robust, and crafted with care.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

try:
    import markdown2
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    print("Error: Required dependencies not found.")
    print("Install with: pip install markdown2 jinja2")
    sys.exit(1)

# Configuration with sensible defaults
CONFIG = {
    "site_url": "https://0xpili.xyz",
    "site_title": "0xpili",
    "site_description": "Thoughtful writings on technology, privacy, and the human condition.",
    "author": "0xpili",
    "templates_dir": "templates",
    "posts_dir": "posts",
    "output_dir": "docs",
    "cache_file": ".build_cache.json",
    "date_format": "%Y %b %d",  # Clean, unambiguous format
}

class BlogBuilder:
    """A blog builder focused on speed, reliability, and longevity."""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.cache = self._load_cache()
        self.env = Environment(
            loader=FileSystemLoader(config["templates_dir"]),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
    def _load_cache(self) -> Dict[str, str]:
        """Load build cache for incremental builds."""
        cache_path = Path(self.config["cache_file"])
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save build cache."""
        with open(self.config["cache_file"], 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def _file_hash(self, filepath: Path) -> str:
        """Calculate file hash for change detection."""
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    
    def _parse_post(self, filepath: Path) -> Optional[Dict]:
        """Parse a markdown post with robust error handling."""
        try:
            content = filepath.read_text(encoding='utf-8')
            lines = content.strip().split('\n')
            
            # Extract date from first line
            if not lines or not lines[0].startswith('Date:'):
                print(f"Warning: {filepath.name} missing date header")
                return None
                
            date_str = lines[0].replace('Date:', '').strip()
            
            # Parse date robustly
            try:
                # Remove ordinal suffixes (1st, 2nd, 3rd, etc.)
                clean_date = date_str
                for suffix in ['st', 'nd', 'rd', 'th']:
                    clean_date = clean_date.replace(suffix, '')
                
                date_obj = datetime.strptime(clean_date, self.config["date_format"])
            except ValueError:
                print(f"Warning: Invalid date format in {filepath.name}: {date_str}")
                return None
            
            # Process content
            md_content = '\n'.join(lines[1:]).strip()
            html_content = markdown2.markdown(
                md_content,
                extras=['fenced-code-blocks', 'tables', 'header-ids']
            )
            
            # Create URL-friendly slug
            slug = filepath.stem.lower().replace(' ', '-')
            
            # Extract title from filename or first heading
            title = filepath.stem.replace('-', ' ').title()
            if lines and lines[1].startswith('# '):
                title = lines[1][2:].strip()
            
            return {
                'title': title,
                'slug': slug,
                'filename': slug,  # For compatibility
                'date': date_obj.strftime(self.config["date_format"]),
                'iso_date': date_obj.isoformat(),
                'date_obj': date_obj,
                'content': html_content,
                'filepath': str(filepath),
                'hash': self._file_hash(filepath),
            }
            
        except Exception as e:
            print(f"Error parsing {filepath.name}: {e}")
            return None
    
    def _needs_rebuild(self, post: Dict) -> bool:
        """Check if a post needs rebuilding."""
        cached_hash = self.cache.get(post['filepath'])
        return cached_hash != post['hash']
    
    def build(self):
        """Build the blog with focus on speed and reliability."""
        print("Building blog...")
        
        # Ensure output directory exists
        output_path = Path(self.config["output_dir"])
        output_path.mkdir(exist_ok=True)
        
        # Load templates once
        try:
            post_template = self.env.get_template("base.html")
            index_template = self.env.get_template("index.html")
            error_template = self.env.get_template("404.html")
        except Exception as e:
            print(f"Error loading templates: {e}")
            return
        
        # Process all posts
        posts = []
        posts_path = Path(self.config["posts_dir"])
        
        if not posts_path.exists():
            print(f"Error: Posts directory '{posts_path}' not found")
            return
            
        for filepath in posts_path.glob("*.md"):
            post = self._parse_post(filepath)
            if post:
                posts.append(post)
                
                # Only rebuild if changed
                if self._needs_rebuild(post):
                    try:
                        html = post_template.render(
                            title=post['title'],
                            date=post['date'],
                            content=post['content'],
                            slug=post['slug'],
                            description=None,  # Could extract from content
                        )
                        
                        output_file = output_path / f"{post['slug']}.html"
                        output_file.write_text(html, encoding='utf-8')
                        
                        # Update cache
                        self.cache[post['filepath']] = post['hash']
                        print(f"  ✓ {post['title']}")
                        
                    except Exception as e:
                        print(f"  ✗ Error building {post['title']}: {e}")
                else:
                    print(f"  - {post['title']} (unchanged)")
        
        # Sort posts by date (newest first)
        posts.sort(key=lambda x: x['date_obj'], reverse=True)
        
        # Generate index
        try:
            index_html = index_template.render(posts=posts)
            (output_path / "index.html").write_text(index_html, encoding='utf-8')
            print("  ✓ Index page")
        except Exception as e:
            print(f"  ✗ Error building index: {e}")
        
        # Generate 404
        try:
            error_html = error_template.render()
            (output_path / "404.html").write_text(error_html, encoding='utf-8')
            print("  ✓ 404 page")
        except Exception as e:
            print(f"  ✗ Error building 404: {e}")
        
        # Save cache
        self._save_cache()
        
        print(f"\nBlog built successfully!")
        print(f"View at: {output_path / 'index.html'}")


def main():
    """Entry point with error handling."""
    # Allow config overrides from environment
    for key in CONFIG:
        env_key = f"BLOG_{key.upper()}"
        if env_key in os.environ:
            CONFIG[key] = os.environ[env_key]
    
    # Build the blog
    builder = BlogBuilder(CONFIG)
    builder.build()


if __name__ == "__main__":
    main()