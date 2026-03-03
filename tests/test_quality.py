#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# The inline theme-toggle script is intentional — match it so we can allow it
_THEME_TOGGLE_RE = re.compile(
    r"<script>\s*\(function\(\)\{\s*const toggle",
    re.DOTALL,
)


def test_html_quality():
    docs = Path("docs")
    if not docs.exists():
        print("Run 'python3 blogmaker.py' first")
        return False

    errors = []

    for html_file in docs.glob("*.html"):
        content = html_file.read_text()

        if "fonts.googleapis.com" in content:
            errors.append(f"{html_file.name}: External font dependency")

        # Allow the inline theme-toggle, flag anything else
        if "<script" in content:
            without_toggle = _THEME_TOGGLE_RE.sub("", content)
            if "<script" in without_toggle:
                errors.append(f"{html_file.name}: Disallowed JavaScript found")

        if 'style="' in content:
            errors.append(f"{html_file.name}: Inline styles found")

        # Size budgets account for ~8KB of inlined CSS per page
        size_kb = html_file.stat().st_size / 1024
        if html_file.name == "index.html" and size_kb > 10:
            errors.append(f"{html_file.name}: Too large ({size_kb:.1f}KB, limit 10KB)")
        elif html_file.name == "404.html" and size_kb > 3:
            errors.append(f"{html_file.name}: Too large ({size_kb:.1f}KB, limit 3KB)")
        elif size_kb > 25:
            errors.append(f"{html_file.name}: Too large ({size_kb:.1f}KB, limit 25KB)")

        if "<meta name=\"viewport\"" not in content:
            errors.append(f"{html_file.name}: Missing viewport meta")
    
    if errors:
        print("❌ Quality issues found:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✓ HTML quality: Excellent")
        return True

def test_performance():
    docs = Path("docs")
    total_size = 0
    file_count = 0
    
    for html_file in docs.glob("*.html"):
        total_size += html_file.stat().st_size
        file_count += 1
    
    avg_size_kb = (total_size / file_count / 1024) if file_count > 0 else 0
    
    print(f"✓ Performance metrics:")
    print(f"  - Average page size: {avg_size_kb:.1f}KB")
    print(f"  - Total site size: {total_size/1024:.1f}KB")
    print(f"  - Load time (3G): ~{avg_size_kb * 0.1:.1f}s")
    
    return avg_size_kb < 15

def test_accessibility():
    docs = Path("docs")
    errors = []
    
    for html_file in docs.glob("*.html"):
        content = html_file.read_text()
        
        if "<img" in content and 'alt="' not in content:
            errors.append(f"{html_file.name}: Images without alt text")
        
        if "<h3" in content and "<h2" not in content:
            errors.append(f"{html_file.name}: H3 without H2")
        
        if 'lang="en"' not in content:
            errors.append(f"{html_file.name}: Missing lang attribute")
    
    if errors:
        print("❌ Accessibility issues:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✓ Accessibility: Good")
        return True

def main():
    print("Running quality tests...\n")
    
    results = [
        test_html_quality(),
        test_performance(),
        test_accessibility(),
    ]
    
    if all(results):
        print("\n🏆 All quality tests passed!")
        print("Your blog embodies:")
        print("  - Speed (fucking FAST)")
        print("  - Quality (built for decades)")
        print("  - Craft (artisan-level code)")
        print("  - Minimalism (austere luxury)")
    else:
        print("\n⚠️  Some tests failed. Fix issues and run again.")
        sys.exit(1)

if __name__ == "__main__":
    main()