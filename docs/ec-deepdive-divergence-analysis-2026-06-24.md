# EC-screen deep-dive branch — divergence analysis & reconciliation plan (2026-06-24)

**Author:** Worker session (ECSR task window). **Status:** ✅ RESOLVED 2026-06-24 16:4x (owner-approved align-to-remote).
**Audience:** other Claude Code workers + the owner. Read this before touching `feature/ec-screen-deepdive`.

## OUTCOME (executed, owner-approved)
Did **stash → reset --hard origin → stash pop** in `C:\Projects\ChoongYin_OS`:
- Local `feature/ec-screen-deepdive` now = `a8122ac` (remote), **0↔0 divergence**. The 12 batch-2 notes are preserved.
- The 26 local config/artifact mods were stashed and popped back cleanly (**no conflicts**); `.claude/settings.local.json`
  `bypassPermissions` is restored.
- **No force-push** — the remote was already correct and was never touched.
- Backup image (`C:\tmp\repo-backups\ec-deepdive-20260624_163706\`) + safety branch
  `backup/ec-deepdive-pre-rebase-1312bcc` retained until the owner confirms the program looks healthy.
- ⚠️ Heads-up: the autopilot worktree `C:\tmp\wt-ec-learn` is still detached at the **old** tip `2706d21`; if the
  daily runner does not self-sync to `a8122ac` it could re-diverge — verify on/after the next 13:30 run.

## TL;DR
A reviewer/other worker **force-reset the remote** `feature/ec-screen-deepdive` and worried the main checkout's
**15 unpushed local commits** would be lost, recommending **rebase-local-then-force-push**. I validated against
ground truth and that recommendation is **WRONG and would cause data loss**. The remote is a **strict superset**
of my local — the safe action is to align **local → remote**, not push local over remote.

## Ground state (as of 2026-06-24 16:37)
| Ref | Commit | Meaning |
|---|---|---|
| local `feature/ec-screen-deepdive` (main checkout `C:\Projects\ChoongYin_OS`) | `1312bcc` | 15 commits past merge-base; **diverged** |
| `origin/feature/ec-screen-deepdive` | `a8122ac` | "batch 2: 11 new full + 1 partial (26 total done)" + review history |
| merge-base | `6000e6a` | review feedback 2026-06-22 (#98) |
| `backup/ec-deepdive-pre-rebase-1312bcc` | `1312bcc` | safety branch I created (= old local HEAD) |
| autopilot worktree `C:\tmp\wt-ec-learn` | `2706d21` (detached) | the pre-reset remote tip |

Divergence: **15 local-only ↔ 6 remote-only** commits. Remote ref was a **forced update** (`2706d21 → a8122ac`).

## Validation (why local has nothing unique)
- **Screen notes:** local has 17; remote has 29. **Notes only on local: ZERO.** Remote has all 17 of mine
  **plus 12 more** (`CO.0021, CO.0027–0038`).
- **The 17 shared notes:** 15 are byte-identical; the only 2 that differ (`CO.0018`, `PO.0008`) differ **solely by a
  newer date stamp on the remote** (`2026-06-24` vs local `2026-06-22`) — remote is newer.
- **Runner** `tools/deep-dive-scheduler/run_ec_screen_learn.py`: **identical** local vs remote.
- **Supporting files:** remote has newer `CHECKLIST.md` (26 vs ~17 done), `MASTER-PLAN.md`, `STATUS.md`, and
  **+95 lines** of `docs/lessons-learned.md` (the reviewer rules).
- Net `git diff HEAD origin`: 370 insertions / 22 deletions — the 22 "deletions" are just older/superseded
  versions of CHECKLIST/STATUS/etc. on local. **No unique local content of value.**

**Conclusion:** my 15 local commits' work is already represented on the remote and surpassed by batch-2.

## Why the reviewer's fix is dangerous
`rebase local onto remote → force-push` would:
1. Conflict on ~32 overlapping files (not "only CHECKLIST.md").
2. If resolved "keep local", **overwrite the remote's 12 batch-2 notes + newer CHECKLIST/STATUS/lessons** →
   **roll the shared remote backward** and lose another worker's batch-2 output.

## Recommended SAFE plan (pending owner approval)
1. ✅ **Backup image created** (verified): `C:\tmp\repo-backups\ec-deepdive-20260624_163706\`
   (`repo-ALL-refs.bundle` = all refs/commits; `uncommitted-tracked.patch` = the 26 modified tracked files).
2. ✅ **Safety branch:** `backup/ec-deepdive-pre-rebase-1312bcc` (keeps the 15 commits retrievable).
3. **Stash the 26 uncommitted tracked files** (regenerated screenshots + `.claude/settings*.json`) — `git stash`
   (leaves the 467 untracked `tmp/` scratch alone; `reset --hard` does not delete untracked files anyway).
4. **Align local to remote:** `git reset --hard origin/feature/ec-screen-deepdive` (= `a8122ac`).
   This is safe *because* the backup + the proven superset relationship guarantee nothing is lost.
5. **Decide on the stash** (the 26 files): the screenshots are regenerated each run (drop), `.claude/settings*`
   may hold local config (review before discarding).
6. **No force-push.** The remote is already correct; local just catches up to it.
7. Keep the backup + safety branch until the owner confirms the deep-dive program looks healthy.

## Timing
Autopilot/Python runner = **once daily 13:30**. At analysis time it was 16:33 → today's run already happened;
safe window is the rest of 2026-06-24 before tomorrow 13:30.

## Open questions for the owner
- Confirm: align local **to** remote (my recommendation), NOT force-push local over remote?
- The `.claude/settings*.json` local modifications — keep or discard?
