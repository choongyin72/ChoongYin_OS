# VERIFY-REPORT - Bank Account

_Hand-assembled for this backfill session (`docs/lean-deliverable-backfill-workorder.md`, Batch
11) — `scripts/verify_screen.py` was NOT used because this is a documentation/evidence backfill
around already-merged automation (PR #478, merged 2026-08-23), not a fresh build. Every tick below
cites the exact command run in this session (2026-08-28) and its real exit/output; where a gate
was already established by PR #478, that is cited separately and NOT re-claimed as this session's
own result._

**OVERALL: PASS** (all gates re-run this session, zero drift vs PR #478's own cited baseline)

## Gates re-run this session (2026-08-28)
- [x] **10** robocop clean — `py -m robocop check
      pageobjects/Configuration/Assets/Financial_Objects/bank_account_page.resource
      tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot` — **7 issues** (2
      VAR02 + 5 DOC02), matches PR #478's cited 7-issue baseline exactly.
- [x] **11** `robot --dryrun tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot`
      — **5/5 PASS**.
- [x] **12** LIVE headless run — `EC_HEADLESS=true robot --outputdir
      screens/Configuration/Assets/Financial_Objects/Bank_Account/evidence
      tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot` — **5/5 PASS on the
      first attempt** (no retry needed).
- [x] **13** DB ground-truth — `libraries.DbVerify.fetch_object("OV_BANK_ACCOUNT",
      "AUTOTEST_BACC")` via a fresh oracledb connection: `None` BEFORE the run (code free) and
      `None` AFTER the run (confirmed absent).
- [x] **15** Self-clean confirmed — same fresh-connection read as item 13, both before and after.
- [x] **16** Hygiene — `py scripts/check_bundle_hygiene.py` (repo root) → `RESULT: PASS` (167
      bundles + 272 recon scripts scanned; the sole WARN is a pre-existing, unrelated Contract
      Area `investigation/` script, not Bank Account).
- [x] **grid-filter fired** — `grep -o "Find Object Row By Filter\|Clear Object Row Filter"
      evidence/output.xml | sort | uniq -c` → 15 hits each, matching PR #478's cited 15x/15x
      exactly.

## Gates established by PR #478 (2026-08-23, cited from its PR body, not re-claimed as this
session's independent result — see `gh pr view 478`)
- Live 5/5, DbVerify `Code Should Be Present/Absent In View OV_BANK_ACCOUNT`, full-tree dryrun
  772/772, robocop 7 issues, grid-filter 15x/15x, DB self-clean 0 residual `AUTOTEST%` rows.

## Not applicable to this backfill
- Item 14 (full I-U-D scope) — confirmed by reading `bank_account_iud.robot`'s 5 TCs (Clean
  State/Insert/Update/Find/Delete), not a separate gate run.
- Items 17/18 (registry/scorecard rows) — already exist, appended at PR #478's own merge; this
  backfill does not touch them (append-only rule, R23).
