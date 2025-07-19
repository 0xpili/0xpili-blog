#!/usr/bin/env python3
"""Test suite to ensure blog quality and performance."""

import os
import sys
from pathlib import Path
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_html_quality():
    """Ensure HTML follows our principles."""
    docs = Path("docs")
    if not docs.exists():
        print("Run 'python3 blogmaker.py' first")
        return False
    
    errors = []
    
    for html_file in docs.glob("*.html"):
        content = html_file.read_text()
        
        # No external resources
        if "fonts.googleapis.com" in content:
            errors.append(f"{html_file.name}: External font dependency")
        
        # No JavaScript
        if "<script" in content:
            errors.append(f"{html_file.name}: JavaScript found")
        
        # No inline styles (should use style tag)
        if 'style="' in content:
            errors.append(f"{html_file.name}: Inline styles found")
        
        # Check file size (reasonable for content-rich posts)
        size_kb = html_file.stat().st_size / 1024
        if html_file.name == "index.html" and size_kb > 8:
            errors.append(f"{html_file.name}: Too large ({size_kb:.1f}KB)")
        elif html_file.name == "404.html" and size_kb > 3:
            errors.append(f"{html_file.name}: Too large ({size_kb:.1f}KB)")
        elif size_kb > 15:  # Generous limit for content-rich posts
            errors.append(f"{html_file.name}: Too large ({size_kb:.1f}KB)")
        
        # Valid meta tags
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
    """Test performance characteristics."""
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
    
    return avg_size_kb < 10  # Average should be under 10KB

def test_accessibility():
    """Check basic accessibility."""
    docs = Path("docs")
    errors = []
    
    for html_file in docs.glob("*.html"):
        content = html_file.read_text()
        
        # Check for alt texts (if images exist)
        if "<img" in content and 'alt="' not in content:
            errors.append(f"{html_file.name}: Images without alt text")
        
        # Check heading hierarchy
        if "<h3" in content and "<h2" not in content:
            errors.append(f"{html_file.name}: H3 without H2")
        
        # Check lang attribute
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
    """Run all quality tests."""
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