Full deploy pipeline: build, test, commit, and push. ARR!

Steps:
1. Run `python3 blogmaker.py` to build the blog
2. Run `python3 tests/test_quality.py` to verify quality standards
3. If tests pass, show `git status` and `git diff --stat` so the user can review changes
4. Ask the user for a commit message (suggest one based on the changes using conventional commits)
5. Stage the relevant files, commit, and push to origin

IMPORTANT: Always confirm with the user before pushing. Never force push.