# Execution Plan — EC Screen Program Completion (wake-up trigger: "execute the completion plan")

_Drafted 2026-07-05 at 776/1457. To be executed in ONE session when the runner finishes all 1,457 screens (expected 2026-07-06). Owner wakes the assistant; steps below run in order. All work on branch `feature/ec-screen-deepdive` via worktree `C:\tmp\wt-ec-learn`; runner code via `C:\tmp\wt-ecfix`; nothing on master except the final merge._

## Phase 0 — Verify completion (5 min)
1. `git fetch` + detach worktree to branch tip.
2. CHECKLIST tallies: expect `[x]` = 1457, `[ ]` = 0, `[~]` = 0. Session log: last runs show `progress: +N`, no ALARM, pushed.
3. If any screens remain: run `EC_LEARN_MAX=<n> py tools/deep-dive-scheduler/run_ec_screen_learn.py` once to finish, or stop and report why.
- **Done =** 1457/1457 complete, log clean.

## Phase 1 — Final full-map review (30–45 min)
1. Run the aggregation script (pattern: /tmp/quality_audit.py from 2026-07-05) over all 1,457 notes: per-module counts, screen-type & class-type/scope distributions, resolved-by stats, no-class flags, help-image coverage.
2. Write `REVIEW-<date>-COMPLETE-1457.md`: the full domain map (extend the 10-cluster CO model to every module: PO, GD, CD, WR, + whatever the last runs added), recurring motifs, per-module one-paragraph syntheses (Tier-2 depth), stats appendix.
3. Commit + push (this is the milestone's seed content).
- **Done =** review doc on branch; user gets the "what I learned" summary in chat.

## Phase 2 — Phase-A re-resolution sweep (45–60 min)
1. Scan all notes for the `no class resolved` flag + any pre-resolver-v3 vintage with empty binding (scripted; greppable flag exists since `f2ddb71`).
2. **Resolver v4** (patch in wt-ecfix, syntax-check, push, sync main-repo copy):
   - twin/sibling inference: `X.1`/`X.01` variants inherit the resolved class of their base BF code (and vice versa);
   - view-name search: token match against `all_views` `OV_/TV_/DV_%` names;
   - normalized fuzzy label match (strip spaces/dashes/case) — still UNIQUE-match-only, no guessing.
3. Reset flagged screens in CHECKLIST (reset-and-rerun pattern) → scoped manual run `EC_LEARN_MAX=<count>` → push.
4. Remainder = genuine process/config: add a small lookup (BF_CODE → config tables: PROSTY_CODES / CTRL_CHECK_* / STRM_FORMULA / SCHEDULE / BUSINESS_ACTION / STAT_PROCESS_* / TV_CTRL_CONFIGURATION_STORAGE) rendered into the note's Screen-type section.
- **Done =** zero screens with an unexplained empty binding; every no-class screen either resolved or carries named config tables.

## Phase 3 — Conformance audit + hygiene (10 min)
1. Re-run the format-conformance scan (pattern: /tmp/format_conformance.py): expect N/N corpus-format, 0 structural problems, CHECKLIST↔files consistent, 0 orphan artifacts.
2. Save the scan as `tools/deep-dive-scheduler/audit_notes_conformance.py` (committed, re-runnable — becomes the monthly audit).
- **Done =** audit script in repo; clean report.

## Phase 4 — Milestone merge (5 min + owner click if needed)
1. Pre-milestone sync: merge `origin/master` into branch in worktree (keep BRANCH versions on any ec-screens/runner conflicts), push.
2. Merge the standing draft PR (#170 or successor) — squash, branch NOT deleted. Requires the owner's explicit "merge it" in-chat (classifier needs it).
3. Verify: master tip, branch survives, auto-reopen workflow fires (new draft PR appears within seconds — `reopen-deepdive-draft-pr.yml`).
- **Done =** all 1,457 + reviews + fixes on master; fresh standing PR open.

## Phase 5 — (SEPARATE approval gate) Preserve-section feature + Tier-3 pilot
_Not auto-executed with the above — needs the owner's go + Fable-5 budget nod._
1. Runner feature: preserve a `## Deep-dive (manual)` section across regenerations (read old note, carry the section into the new render; test on a scratch screen).
2. Tier-3 pilot (10 screens, Fable-5 fan-out, DB-verified against local sandbox): CO.1040, CO.1042, CO.1059, CO.1060 (calc framework) · CO.3009, CO.3001, CO.2016, CO.2019 (CLP pricing/contract) · CO.0130, CO.0127 (platform machinery). Each gets a business-process section written into its note's manual block; CHECKLIST `★` marker = "understood".
- **Done =** 10 ★ screens; pattern proven for scaling by owner priorities.

## Also queued (independent of the runner): ECSR-35333 user summary
Draft-refresh the Jira comment covering: the 3-cause RCA (unverified deferments / SCA capacity-forecast missing / negative auto-deferments), today's findings (all 8 facilities DO load; PNI has zero 2026 RAU targets; Train1/2/Cond targets identical — confirm intent), and per-cause recommended actions. Present in chat for owner review — owner posts or approves posting. _(Can run any time — does not wait for the runner.)_

— End of plan —
