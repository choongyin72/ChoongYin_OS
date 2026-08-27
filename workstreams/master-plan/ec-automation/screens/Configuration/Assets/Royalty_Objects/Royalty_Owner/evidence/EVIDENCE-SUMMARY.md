# Evidence Summary — Royalty Owner

Two evidence sets live in this folder, from two different builds of the same screen:

## 1. Original build (undated subfolder-less files at the top level)
`royalty_owner_tc01_clean.png` .. `royalty_owner_tc04_deleted.png` — from the screen's original
IUD build (SOW dated 2026-06-25, pre-Bank-pattern-conversion). Kept as-is (not overwritten) per
the backfill work order's "UPDATE, don't duplicate" instruction — these already exist and remain
valid historical evidence of the same DB view/table.

## 2. Backfill live run — `2026-08-28_backfill_run/`
Fresh live re-run of the CURRENT (post-PR #447 Bank-pattern) suite, captured for this
documentation backfill (`docs/lean-deliverable-backfill-workorder.md`, Batch 8). Command:

```
EC_HEADLESS=true robot --outputdir results tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot
```

**Result: 5 tests, 5 passed, 0 failed** (TC01 Verify Clean State, TC02 Insert, TC03 Update,
TC04 Find, TC05 Delete — all PASS).

Contents:
- `output.xml` — full RF output for this run (374 KB, screen-scoped single suite — not the
  full-tree dryrun, which stays out of the repo per the size guidance in this backfill task).
- `tc01_verify.png` — clean-state check before insert (no `AUTOTEST_ROYALTY_OWNER` row present).
- `tc02_insert_action.png` / `tc02_verify.png` — insert filled-form pre-Save, and post-save grid+form verify.
- `tc03_update_action.png` / `tc03_verify.png` — update filled-form pre-Save, and post-save verify.
- `tc04_find_action.png` — Find Royalty Owner Record (TC04), row selected/filtered.
- `tc05_delete_action.png` / `tc05_verify.png` — End Date = Start Date set pre-Save, and post-delete
  removal verify (grid + `OV_ROYALTY_OWNER` both confirm absence).

**Independent re-verification performed for this backfill (not just re-citing PR #447's numbers):**
- `robocop check` on the T3 + suite → **9 issues** (4 VAR02 + 5 DOC02) — matches PR #447's cited
  baseline exactly; no new issues introduced since the original conversion.
- `robot --dryrun` on the full `tests/` tree → **883/883 pass** (dryrun output is small text-only,
  not committed here per this task's own "don't commit full-tree dryrun output" guidance — the
  count is cited here as the verification record instead).
- Fresh, independent `oracledb` connection (own script, not reusing the suite's own DB check) query
  `SELECT COUNT(*) FROM OV_ROYALTY_OWNER WHERE CODE = 'AUTOTEST_ROYALTY_OWNER'` → **0** rows —
  self-clean confirmed after TC05.
- `output.xml` grep for `kw name="Find Royalty Owner Row By Filter"` → **5** matches — confirms the
  explicit grid-filter wiring fired once per test case, matching PR #447's claim.

No automation files (`royalty_owner_page.resource`, `royalty_owner_iud.robot`, `testdata/royalty_owner_*.properties`)
were modified to produce this evidence — this is a read-only re-run of the already-merged suite.
