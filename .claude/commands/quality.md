Run all quality and build tests, then report a comprehensive status.

Steps:
1. Run `python3 tests/test_quality.py` — checks HTML quality, performance metrics, and accessibility
2. Run `python3 tests/test_build.py` — verifies the build system works correctly
3. Check all generated HTML files in `docs/` for size compliance:
   - Index: <8KB
   - 404: <3KB
   - Posts: <15KB each
4. Report total site size and average page size
5. Flag any issues found and suggest fixes