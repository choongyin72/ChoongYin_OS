# PR & Review Protocol — Worker ↔ Reviewer

**Status: v0.1 (DRAFT — proposed by the worker session 2026-06-15).** The "Open questions" at the
bottom need the reviewer's / user's confirmation; everything else is what the worker commits to now.
This doc is the shared contract for the feature-branch + PR workflow. Both sessions should read it at
session start. It evolves only via PR (append-only edits — see §Shared-file discipline).

## Roles
- **Worker** (builds EC automation): creates feature branches, opens PRs, never merges.
- **Reviewer** (daily 06:00 AWST): runs `/code-review --comment` on open worker PRs, posts inline
  findings, extracts actionable rules into `docs/lessons-learned.md` (via its own `review/` PR).
- **Human** (Choong-Yin): reviews; the merge is performed by the reviewer session / human, never the worker.

> **SCHEDULE UPDATE (2026-08-01): the automated 06:00/14:00 AWST scheduled reviewer trigger has been
> DISABLED by the owner.** The "daily 06:00 AWST" phrasing above is now historical, not current practice —
> do not wait for a timer that will not fire. The Reviewer role now runs **on-demand, interactively**: the
> owner asks directly in chat ("review raised PRs and merge", "any raised PRs?") and the Reviewer session
> checks GitHub state and acts immediately in that same turn. See "Reviewer per-PR checklist" below for
> what to run through on each such request.

## Branch & PR conventions
- **Branch naming:** `feature/<short-task-name>` (worker), `review/feedback-YYYY-MM-DD` (reviewer).
- **Base:** branch INDEPENDENT tasks off `master`; branch DEPENDENT tasks off the parent branch.
- **Stacking:** stacked/parallel PRs are allowed (don't idle waiting for a merge). If a PR builds on
  another, put **`depends on #N — merge after`** in the title/body; the merger must respect that order.
- **PR title prefix:** `feat:` / `fix:` / `recon:` / `chore:` / `review:`.
- **The worker never merges and never commits to `master` directly.**

## Worker guarantees (every PR)
1. **Standard PR body** (see template below) — same shape every time, so review is fast to parse.
2. **Small, single-purpose PRs** — one screen/pattern each.
3. **Evidence-first** — a PASS is claimed only with DB ground truth (live run + the exact DbVerify
   assertion), never a green UI log alone; the evidence is linked in the PR.
4. **Self-cleaning** — any test that writes data restores the sandbox exactly as found (DB-verified);
   the PR states the self-clean result.
5. **Engage comments with rigor** — verify each finding against code/DB, then fix or push back with
   technical reasoning (no performative agreement, no blind implementation).

## Reviewer asks (to make findings actionable)
1. **Tag each comment `MUST-FIX` vs `NICE-TO-HAVE`** so the worker knows what gates the merge.
2. **Cite `file:line` + the concrete failure mode + a suggested fix** — "always do X / never do Y",
   not "consider X" (the same bar `lessons-learned.md` rules are held to).
3. **Verify claims against the actual code/DB before posting** — especially DB/runtime claims not
   visible in the diff. (Precedent: a "3 Financial Objects parked" gap and a backwards ORA-06569 rule
   did not hold up on validation 2026-06-15.) The worker will validate feedback the same way — to
   anchor on ground truth, not to dismiss it.
4. **Append-only when writing to shared docs** (`lessons-learned.md`, `automation-scorecard.md`) —
   new dated sections / rows, never rewriting existing lines — so review PRs don't collide with open
   work PRs.
5. **Respect stack order** — never merge a `depends on #N` PR before #N.

## PR body template (worker)
```
## What
<one-line: what was built/fixed>

## Scope
- files: <list>
- base: <master | feature/parent>   depends on: <#N | none>

## Evidence (DB ground truth)
- suite: <path>   result: <live N/N>
- DB-verify: <the exact assertion, e.g. PWEL_SUB_DAY_STATUS.AVG_WH_PRESS 210->206.84 unit-robust>
- self-clean: <restored to baseline, 0 residual — verified>

## Lessons-learned rules applied
- R# <which rules from docs/lessons-learned.md this honoured>

## Notes / risks
<anything the reviewer should know>
```

## Shared-file discipline (both sessions)
These files are edited almost every task and are conflict-magnets:
`libraries/DbVerify.py`, `docs/ec_screen_registry.md`, `docs/automation-scorecard.md`,
`DeepDiveLearnings/SELF-LEARNING-BACKLOG.md`, `docs/lessons-learned.md`.
**Rule: APPEND-ONLY** — add new functions / table rows / dated sections at the end; never rewrite
existing lines. This keeps parallel PRs auto-mergeable and safe for an automated merger.

## Handling review comments (worker routine)
1. At **session start**, check my open PRs for new review comments before opening new branches.
2. For each comment: restate it, verify against code/DB, then **fix** (`MUST-FIX`) or **reply with
   technical reasoning** if I believe it's wrong (cite the test/DB that proves it).
3. Reply in the PR comment thread, not as a new top-level comment.
4. Re-run the affected suite + the canary after addressing comments; note the result in the thread.

## Confirmed answers (locked 2026-06-14 by reviewer + human)
1. **Merge gate:** MUST-FIX comments gate the merge. The reviewer will not merge a worker PR until
   all MUST-FIX comments are resolved. Merge-then-comment (advisory) is not used. Human approval
   required before merge — fully automated merge deferred until the system proves reliable.
2. **Session-start PR check:** Confirmed. Worker checks all open PRs for review comments before
   opening any new branch. Already mandated in `CLAUDE.md` — no separate wiring needed.
3. **Turnaround:** No PR is merged before the daily 06:00 AWST reviewer has seen it. The merge
   sequence is always: worker raises PR → reviewer reviews at 06:00 AWST → worker addresses
   MUST-FIX comments → human approves → reviewer session merges. Nothing auto-merges on a timer.

## Recommended wiring (not done in this PR)
Add this file to `CLAUDE.md`'s "On session start (mandatory)" reading list so both sessions load it.
(Left to the reviewer/human who own `CLAUDE.md`, to keep this PR single-purpose.)

## IUD PR gate (added 2026-06-28 — owner-directed; all items hard-gated)
Every **EC Object IUD** PR is checked against the canonical **`docs/IUD-DELIVERABLE-CHECKLIST.md`** (19 items:
artifacts SOW/README/JOURNAL/playwright/investigation/evidence/CHECKLIST · RF T3+suite · gates robocop/dryrun/
**live N/N**/**DB ground-truth**/**full I-U-D**/self-clean/hygiene · delivery registry+scorecard rows + R9 PR).
- The worker ships the bundle's `CHECKLIST.md` (copied from the canonical list) with every item ticked + evidence.
- **Reviewer:** verify each item against the PR (spot-check substance, not just the tick). **ALL 19 are HARD GATES** —
  any missing/failing item ⇒ **MUST-FIX: do not approve/merge, leave the PR open, post the note-back** (template in
  the checklist doc) listing the exact gaps; re-review next run after the worker pushes fixes to the same branch.
- This sits alongside the existing R-rules (R7/R9/R12/R13/R16/R20/R21/R23…); the reviewer may formalise it as an
  R# at its next run. Doc-only gaps need no code change.

## Reviewer merge discipline (added 2026-08-01 — from an extended interactive review/merge session, PRs #285-#298)
Written for a **fresh Reviewer session picking this up cold**: the written protocol above (session-start
reads, MUST-FIX gating, PR body format) transfers on its own, but the habits below are what actually
caught real defects across ~14 PRs in one session and are not otherwise written down anywhere.

1. **Never trust a PR's own description of its diff — read the diff.** Every substantive finding this
   session (a destructive JOURNAL/KB regeneration in #287, an undisclosed governance-file edit in #285, a
   literal unsubstituted `%s` in #294, false "cascade"/"first-available" claims surviving one layer deeper
   than the PR's own sweep in #295/#297/#298) was found by reading the actual `git diff`/`git show` content,
   not by trusting the PR body's narrative of what it did. Treat the PR body as a claim to verify, not a
   fact to summarize.
2. **Diff against the PR's real fork point, not current `origin/master`.** For a stacked PR opened before
   an earlier sibling merged, `git diff origin/master...HEAD` will show the earlier sibling's now-merged
   files as part of "this PR's diff" — apparent changes to files like a shared generator script can be pure
   staleness, not real conflicts. Use `git merge-base origin/master <branch>` to find the true fork point
   and diff from there (`git diff <fork-point>...<branch>`) before concluding anything is missing, added,
   or reverted.
3. **For stacked/parallel PRs, merge via a scratch worktree, never trust squash-merge.** Squash-merging a
   PR whose branch shares history with another open PR breaks that shared ancestry and orphans the sibling.
   Instead: `git worktree add --detach <path> origin/master`, then a real
   `git merge --no-ff --no-commit origin/<branch>`, resolve conflicts by hand (append-only docs: keep both
   sides if textually different, "ours" if byte-identical — verify byte-identical with `diff`, don't assume
   it from a matching first line), `git commit`, then `git push origin HEAD:refs/heads/master` (R24 applies
   here too — a bare `push origin master` from a detached worktree pushes the wrong ref). GitHub auto-detects
   the source PR as merged once its commits are ancestors of `master` — **except** when the PR's own declared
   base is another feature branch rather than `master` (see item 6).
4. **Before every push: full verification sweep, not just "the one gate I touched".**
   - Conflict-marker sweep: `grep -rl '^<<<<<<<\|^=======$\|^>>>>>>>' . | grep -v '.git/'`.
   - `python3 -c "import ast; ast.parse(open(f).read())"` on every touched `.py` file.
   - Non-ASCII scan on any touched doc row (`[c for c in text if ord(c) > 127]`) per R18/R20.
   - If a shared vocabulary/hygiene validator exists (e.g. `check_row_vocab.py`), re-run it across **every**
     screen in the manifest, not just the one this PR touches — a generator/template fix can silently break
     an unrelated already-shipped screen's wording.
   - When regeneration tooling changed, regenerate an UNRELATED already-shipped config through both the old
     and new generator and diff the output — "regression-proven" is a claim to re-prove, not to accept.
5. **A fixed text-correctness defect at one layer often recurs one layer deeper.** Three separate PRs this
   session (#295, #297, #298) each correctly hunted down a stale "cascade"/"first-available" claim across
   the CHECKLIST/SOW/KB/registry/scorecard/JOURNAL layer, and each time the identical false claim was still
   present, unfixed, in the driver `.py` docstring and the T3/suite `.resource`/`.robot` Settings and keyword
   `[Documentation]` strings — the artifacts a future engineer actually reads to understand runtime behavior.
   When a doc-correctness fix touches a template/generator, grep the files that generator actually PRODUCES
   for the same stale phrase before calling the sweep complete, not just the markdown layer.
6. **A PR stacked on another (unmerged) feature branch as its `base` will not auto-flip to "merged" on
   GitHub, even after its commits are verified ancestors of `master`.** GitHub's merge-detection checks the
   PR's *declared* base branch, not `master` generally. After merging such a PR via the worktree technique
   above, confirm nothing was lost with `git merge-base --is-ancestor <branch> origin/master`, then try
   retargeting the PR to `base: master` — if GitHub refuses with "no new commits between base branch and
   head branch", that confirms zero diff remains (the merge was complete), and the PR should be **closed
   manually** with a comment explaining why, rather than left open showing a misleading "unmerged" state.
7. **Reviewer may fix a defect directly, with disclosure, when the correct content is already
   known/reconstructable** — a single-line registry/scorecard wording error, a template placeholder with an
   unambiguous substitution value from elsewhere in the same PR, restoring content that already exists
   unchanged elsewhere in git history, a generator-root fix for a defect class already fixed once in the
   same PR. **Never fabricate genuinely new investigative/evidentiary content** (JOURNAL narrative for work
   not done, DB evidence, screenshots, root-cause claims not backed by something already on record) — that
   goes back to the Worker. When fixing directly, say so plainly in the merge commit and the PR comment;
   never let a hand-fix look indistinguishable from what the Worker shipped.
8. **Governance files (`CLAUDE.md`, `ec-ui-knowledge/EC_BUG_TRACE_SOP.md`) are categorically different from
   every other doc.** Any Worker edit to them — however reasonable it looks, however confident the Reviewer
   is in its correctness — requires an explicit owner decision before merging, and must be disclosed in the
   PR body's "Files touched" list. If undisclosed, exclude just those files from the merge
   (`git checkout HEAD -- <file>` inside the merge worktree, before committing) and tell the Worker why,
   rather than rejecting the whole PR or merging the governance change unreviewed.
9. **When all currently-open PRs are handled, standalone feedback for the Worker goes in a GitHub Issue,
   not a comment on a closed PR.** The Worker's own session-start protocol (`CLAUDE.md` step 6-7) only scans
   *open* Issues and *open* PRs — a comment left on an already-merged/closed PR will not surface again on its
   own. File an Issue when the feedback isn't tied to a PR that's still open.

## Reviewer per-PR checklist (added 2026-08-01 — run through this EVERY review pass, not just at first onboarding)

### A. Start of the review pass
- [ ] `git fetch origin master` — confirm remote access works before relying on it.
- [ ] List open PRs in `choongyin72/ChoongYin_OS` — this is the actual work queue (no schedule fires it).
- [ ] List open Issues — check for anything left for the Worker (or for you) not yet closed.
- [ ] If it's been a while since this session last read them: skim `docs/lessons-learned.md`'s changelog
      table for any new R# since you last checked, and `docs/session-memory.md` for new owner decisions.
- [ ] Note any PR whose title/body says `depends on #N` or is stacked on another feature branch —
      reviewing/merging order matters for these (item 6 in "Reviewer merge discipline" above).

### B. Per PR — verify, don't trust
- [ ] Read the PR body once for context, then treat every claim in it as unverified.
- [ ] Get the true diff: if the PR could be stacked, `git merge-base origin/master <branch>` first, then
      diff from that fork point — NOT blindly against current `origin/master` (item 2 above).
- [ ] Read the actual changed file contents for anything substantive (registry/scorecard/KB/JOURNAL rows,
      generator/template code, driver/T3/suite bundles) — a file list or diff stat is not enough.
- [ ] EC Object IUD PRs: spot-check the real 21-item `docs/IUD-DELIVERABLE-CHECKLIST.md` substance behind
      each tick, not just that the box is checked (R26).
- [ ] If a text-correctness fix touches CHECKLIST/SOW/KB/registry/scorecard/JOURNAL, also grep the actual
      GENERATED driver `.py` / T3 `.resource` / suite `.robot` files for the same stale claim (R32) —
      this recurred 3 PRs in a row before being caught.
- [ ] If a generator/template script changed, regenerate an UNRELATED already-shipped screen's config
      through both the old and new version and diff byte-for-byte before trusting "no regression."
- [ ] `CLAUDE.md` or `ec-ui-knowledge/EC_BUG_TRACE_SOP.md` touched? STOP — this needs an explicit owner
      decision (`AskUserQuestion`) before merging that part, regardless of how reasonable it looks (item 8).
- [ ] Decide fix-directly (mechanical/reconstructable, disclosed) vs. return-to-Worker (anything genuinely
      new/investigative) per item 7 above.

### C. Merge
- [ ] Stacked, or any hand-fix needed → worktree merge (`git worktree add --detach`, real
      `git merge --no-ff --no-commit`, resolve by hand, `git commit`, `git push origin HEAD:refs/heads/master`).
      Never a bare `push origin master` from a detached worktree (R24).
- [ ] Full sweep before pushing: conflict-marker grep, `ast.parse` on every touched `.py`, non-ASCII scan on
      touched doc rows, and (if it exists) the shared vocab/hygiene validator across the WHOLE manifest.
- [ ] After push: confirm the PR flipped to `merged: true`. If its `base` was another feature branch and it
      didn't, verify `git merge-base --is-ancestor <branch> origin/master`, try retargeting `base: master`
      (a "no new commits" error confirms zero diff remains), then close it manually with a comment (item 6).

### D. After merge
- [ ] Post a PR comment stating exactly what was verified and any fix folded in — never let a hand-fix look
      indistinguishable from what the Worker shipped.
- [ ] A recurring pattern worth remembering → append a dated entry + next R# to `docs/lessons-learned.md`.
- [ ] Feedback for the Worker with no PR left open to carry it → file a GitHub Issue, not a stray comment.

## Reviewer note — 2026-08-02 batch, docs-only PRs #307/#309/#310/#311/#313/#315

These 6 PRs are **docs-only** (`ov-non-bank-targets.md` park-record additions, zero code diff) from a
single-session OV-GM backlog sweep (8 screens parked, 6 screens shipped separately in #304/#306/#308/
#312/#314/#316). Per-PR reviewer instructions were already posted as PR comments at merge time (2026-08-01)
— this entry is the durable copy so a fresh Reviewer session cold-reading this doc doesn't have to dig
through GitHub comments to find them, per the "don't let a finding live only on an unmerged branch"
lesson this same sweep already re-learned once (Message Group's park record was lost this way and had to
be recovered from a stale branch — see #307's own commit body).

**Merge bar for all 6** (no regression risk, no code changed): confirm no shared-engine file
(`ec_object_iud.py` / `manage_object.resource` / `common.resource`) was touched, spot-check one DB
self-clean claim per PR (`SELECT COUNT(*) FROM <view> WHERE CODE LIKE 'AUTOTEST%'` = 0), then merge.

**Follow-ups worth tracking past the merge (none should block it):**
- **#307** (Message Group + Facility Class 2) — Message Group's suspected shared-engine dropdown bug
  (`select_dropdown`) was never confirmed systemic; Area's later `parent_dd` test passed 7/7 on the same
  mechanism. File an issue to formally close or confirm, rather than leaving it a loose thread across the
  22 OV-GM screens that use the same call.
- **#309** (Planned Well) — insert landed in the WRONG EC class (`WELL` not `PLANNED_WELL`, same base
  tables, discriminated only by `CLASS_NAME`) via the toolbar's "New Object" gesture. Root cause
  (menu-item disambiguation vs a scope-binding gap) not isolated. Worth checking whether other screens
  with an ambiguous "New Object" submenu share it.
- **#310** (Price Index) + **#315** (Royalty Contract) — both hit the SAME symptom: the 2nd of 2
  sequential dropdowns in the New-Object form silently persists the wrong value. NOT universal — Price
  Rate (#312) and Contract (#316) used the identical shape (2 sequential dropdowns) and worked correctly.
  Worth a dedicated repro session across all 4 screens (2 broken, 2 working) to isolate the actual
  trigger condition instead of it staying "sometimes happens."
- **#311** (Price Object) — real gap in the shared `row_exists`/`wait_for_row` pager-walk helper: the
  "next" button click times out (30s) on a grid scope large enough to paginate (5 pages here). Every
  OV-GM screen shipped before this one had a small enough scope to stay on page 1. **Recommend a tracked
  issue** — a fix touches the shared engine and needs the backup+canary+random-sibling protocol, not a
  quick patch.
- **#313** (Property) — **highest priority of the six.** `ec.ec_error(page)` returned EMPTY after a Save
  that silently failed, while a real, visible red error banner ("Object not found. The referenced object
  could not be found.") was on screen (screenshot in the PR). Every already-shipped OV/OV-GM driver's
  `insert_ui: PASS` step relies on this exact function. **Recommend spot-checking 2-3 already-merged
  screens'** evidence screenshots against their claimed PASS/DB-verified status — if `ec_error()` has
  blind spots on other screens' banner markup too, some already-"shipped" screens could carry the same
  undetected gap.
