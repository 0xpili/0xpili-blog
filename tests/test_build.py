#!/usr/bin/env python3
"""Test that the blog builds correctly and produces expected output."""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import blogmaker

def test_blog_builds_successfully():
    """Test that blog generation completes without errors."""
    # Create temporary directories
    with tempfile.TemporaryDirectory() as tmpdir:
        # Set up test environment
        test_posts = Path(tmpdir) / "posts"
        test_templates = Path(tmpdir) / "templates"
        test_output = Path(tmpdir) / "docs"
        
        test_posts.mkdir()
        test_templates.mkdir()
        
        # Create test post
        (test_posts / "test-post.md").write_text("""Date: 2025 Jan 01
# Test Post
This is a test.""")
        
        # Copy templates
        for template in ["base.html", "index.html", "404.html"]:
            src = Path("templates") / template
            if src.exists():
                shutil.copy(src, test_templates / template)
        
        # Temporarily override paths
        original_posts = blogmaker.POSTS_DIR
        original_templates = blogmaker.TEMPLATES_DIR
        original_output = blogmaker.OUTPUT_DIR
        
        blogmaker.POSTS_DIR = str(test_posts)
        blogmaker.TEMPLATES_DIR = str(test_templates)
        blogmaker.OUTPUT_DIR = str(test_output)
        
        try:
            # Run blog generation
            blogmaker.generate_blog()
            
            # Verify output
            assert (test_output / "index.html").exists(), "Index not generated"
            assert (test_output / "404.html").exists(), "404 page not generated"
            assert (test_output / "test-post.html").exists(), "Post not generated"
            
            # Check content
            index_content = (test_output / "index.html").read_text()
            assert "Test Post" in index_content, "Post not listed in index"
            
            print("✓ Blog builds successfully!")
            
        finally:
            # Restore original paths
            blogmaker.POSTS_DIR = original_posts
            blogmaker.TEMPLATES_DIR = original_templates
            blogmaker.OUTPUT_DIR = original_output

if __name__ == "__main__":
    test_blog_builds_successfully()