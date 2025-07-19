#!/usr/bin/env python3
"""Migrate to the new, faster blog system."""

import shutil
from pathlib import Path

def migrate():
    """Complete the migration to the new system."""
    print("Migrating to new blog system...")
    
    # Backup old files
    old_files = [
        ("blogmaker.py", "blogmaker_old.py"),
        ("templates/base.html", "templates/base_old.html"),
        ("templates/index.html", "templates/index_old.html"),
        ("templates/404.html", "templates/404_old.html"),
    ]
    
    for src, dst in old_files:
        if Path(src).exists():
            shutil.copy2(src, dst)
            print(f"  Backed up {src} → {dst}")
    
    # Move new files into place
    new_files = [
        ("blogmaker_new.py", "blogmaker.py"),
        ("templates/base_new.html", "templates/base.html"),
        ("templates/index_new.html", "templates/index.html"),
        ("templates/404_new.html", "templates/404.html"),
    ]
    
    for src, dst in new_files:
        if Path(src).exists():
            shutil.move(src, dst)
            print(f"  Installed {src} → {dst}")
    
    # Clean up unused files
    unused = ["styles/main.css", "output/"]
    for path in unused:
        p = Path(path)
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            print(f"  Removed unused: {path}")
    
    print("\n✓ Migration complete!")
    print("  Your blog is now:")
    print("  - Fucking FAST (3-8KB pages)")
    print("  - Built for decades")
    print("  - Austere yet luxurious")
    print("  - Crafted with mathematical precision")
    print("\nRun 'python3 blogmaker.py' to build.")

if __name__ == "__main__":
    migrate()