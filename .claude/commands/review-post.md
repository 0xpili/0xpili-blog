Review a blog post for quality, clarity, and formatting.

The user may provide a post filename or title: $ARGUMENTS

Steps:
1. If no post specified, show a list of posts in `posts/` and ask which to review
2. Read the post file
3. Check for:
   - Proper `Date:` header format
   - Title presence and quality
   - Markdown formatting correctness (links, images, lists, headers)
   - Content flow and readability
   - Spelling or grammar issues
   - Whether images referenced actually exist in `docs/images/`
4. Build with `python3 blogmaker.py` and verify the output HTML
5. Report findings with specific suggestions for improvement