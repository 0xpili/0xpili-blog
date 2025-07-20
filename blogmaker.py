#!/usr/bin/env python3

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

CONFIG = {
    "site_url": "https://0xpili.xyz",
    "site_title": "0xpili",
    "site_description": "Thoughtful writings on technology, privacy, and the human condition.",
    "author": "0xpili",
    "templates_dir": "templates",
    "posts_dir": "posts",
    "output_dir": "docs",
    "cache_file": ".build_cache.json",
    "date_format": "%Y %b %d",
}

class BlogBuilder:
    
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
        cache_path = Path(self.config["cache_file"])
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        with open(self.config["cache_file"], 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def _file_hash(self, filepath: Path) -> str:
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    
    def _parse_post(self, filepath: Path) -> Optional[Dict]:
        try:
            content = filepath.read_text(encoding='utf-8')
            lines = content.strip().split('\n')
            
            if not lines or not lines[0].startswith('Date:'):
                print(f"Warning: {filepath.name} missing date header")
                return None
                
            date_str = lines[0].replace('Date:', '').strip()
            
            try:
                clean_date = date_str
                for suffix in ['st', 'nd', 'rd', 'th']:
                    clean_date = clean_date.replace(suffix, '')
                
                date_obj = datetime.strptime(clean_date, self.config["date_format"])
            except ValueError:
                print(f"Warning: Invalid date format in {filepath.name}: {date_str}")
                return None
            
            slug = filepath.stem.lower().replace(' ', '-')
            
            title = filepath.stem.replace('-', ' ').title()
            if lines and lines[1].startswith('# '):
                title = lines[1][2:].strip()
            
            cover_image, filtered_lines = self._extract_cover_image(lines, slug)
            
            if cover_image:
                content_text = '\n'.join(filtered_lines[1:]).strip()
            else:
                content_text = '\n'.join(lines[1:]).strip()
            
            html_content = markdown2.markdown(
                content_text,
                extras=['fenced-code-blocks', 'header-ids', 'tables']
            )
            
            return {
                'title': title,
                'slug': slug,
                'filename': slug,
                'date': date_obj.strftime(self.config["date_format"]),
                'iso_date': date_obj.isoformat(),
                'date_obj': date_obj,
                'content': html_content,
                'cover_image': cover_image,
                'filepath': str(filepath),
                'hash': self._file_hash(filepath),
            }
            
        except Exception as e:
            print(f"Error parsing {filepath.name}: {e}")
            return None
    
    def _extract_cover_image(self, lines: List[str], slug: str) -> Tuple[Optional[str], List[str]]:
        cover_image = None
        filtered_lines = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('![') and '](' in stripped and stripped.endswith(')'):
                if cover_image is None:
                    start = stripped.find('](') + 2
                    end = stripped.rfind(')')
                    image_path = stripped[start:end]
                    
                    if image_path.startswith('http'):
                        cover_image = image_path
                    elif image_path.startswith('/'):
                        cover_image = image_path
                    else:
                        cover_image = f"/{image_path}"
                    continue
            filtered_lines.append(line)
        
        return cover_image, filtered_lines
    
    def _needs_rebuild(self, post: Dict) -> bool:
        cached_hash = self.cache.get(post['filepath'])
        return cached_hash != post['hash']
    
    def build(self):
        print("Building blog...")
        
        output_path = Path(self.config["output_dir"])
        output_path.mkdir(exist_ok=True)
        
        try:
            post_template = self.env.get_template("base.html")
            index_template = self.env.get_template("index.html")
            error_template = self.env.get_template("404.html")
        except Exception as e:
            print(f"Error loading templates: {e}")
            return
        
        posts = []
        posts_path = Path(self.config["posts_dir"])
        
        if not posts_path.exists():
            print(f"Error: Posts directory '{posts_path}' not found")
            return
            
        for filepath in posts_path.glob("*.md"):
            post = self._parse_post(filepath)
            if post:
                posts.append(post)
                
                if self._needs_rebuild(post):
                    try:
                        html = post_template.render(
                            title=post['title'],
                            date=post['date'],
                            content=post['content'],
                            cover_image=post['cover_image'],
                            slug=post['slug'],
                            description=None,
                        )
                        
                        output_file = output_path / f"{post['slug']}.html"
                        output_file.write_text(html, encoding='utf-8')
                        
                        self.cache[post['filepath']] = post['hash']
                        print(f"  ✓ {post['title']}")
                        
                    except Exception as e:
                        print(f"  ✗ Error building {post['title']}: {e}")
                else:
                    print(f"  - {post['title']} (unchanged)")
        
        posts.sort(key=lambda x: x['date_obj'], reverse=True)
        
        try:
            index_html = index_template.render(posts=posts)
            (output_path / "index.html").write_text(index_html, encoding='utf-8')
            print("  ✓ Index page")
        except Exception as e:
            print(f"  ✗ Error building index: {e}")
        
        try:
            error_html = error_template.render()
            (output_path / "404.html").write_text(error_html, encoding='utf-8')
            print("  ✓ 404 page")
        except Exception as e:
            print(f"  ✗ Error building 404: {e}")
        
        self._save_cache()
        
        print(f"\nBlog built successfully!")
        print(f"View at: {output_path / 'index.html'}")


def main():
    for key in CONFIG:
        env_key = f"BLOG_{key.upper()}"
        if env_key in os.environ:
            CONFIG[key] = os.environ[env_key]
    
    builder = BlogBuilder(CONFIG)
    builder.build()


if __name__ == "__main__":
    main()