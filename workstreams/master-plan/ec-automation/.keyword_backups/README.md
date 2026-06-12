# Keyword-file backups

**Rule (Choong-Yin, 2026-06-12):** ALWAYS copy a common/shared keyword file here BEFORE
changing it, so any problem can be reverted to the exact pre-change state — even for
uncommitted mid-session edits that git can't restore.

- Naming: `<original-name>.<YYYYMMDD_HHMMSS>.bak`
- Scope: `resources/*.resource`, `libraries/*.py`, `screens/.../_shared/*.py`
- Helper: `py tmp/scripts/backup_keyword_file.py <path> [<path>...]`
- Backups are gitignored (git history covers committed states; this covers the gap).
- Revert = copy the .bak back over the file, then dryrun + canary pack.
