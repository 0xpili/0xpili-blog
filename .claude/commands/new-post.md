Create a new blog post.

The user will provide the topic or title. Follow these steps:

1. Ask the user for the post topic/title if not provided as argument: $ARGUMENTS
2. Create a new markdown file in `posts/` with:
   - Filename: lowercase, hyphenated slug (e.g., `my-new-post.md`)
   - Date header: today's date in `YYYY Mon DD` format (e.g., `2026 Mar 03`)
   - Title as `# Heading` in sentence case (only the first word and proper nouns capitalized, e.g. `Once a year`)
   - `Tags:` header (required by tests), reusing existing tags where possible
   - Placeholder content that the user can fill in
3. Run `python3 blogmaker.py` to verify it builds correctly
4. Run `python3 tests/test_quality.py` to verify quality standards