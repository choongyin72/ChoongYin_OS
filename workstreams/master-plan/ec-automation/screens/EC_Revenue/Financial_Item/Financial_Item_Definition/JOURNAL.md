# JOURNAL - Financial Item Definition

## Built
Full Insert->Update->Delete via the Universal Screen Engine, live + DB-verified, self-cleaned to
0 residual (`AUTOTEST_FID_006`). Only the 7 confirmed-mandatory fields filled (Item Code/Name/
Start Date/Item Type/Default Cost Object Type/Format Mask/Data Fallback Method).

## Context
This screen was originally built 2026-08-14 as Phase 4 Pilot 1 (proving the engine + generator on
a genuinely new screen shape) - see `docs/universal_screen_engine_design.md` section 23 for the
3 real, generalizable engine gaps found and fixed there. That work produced draft evidence
screenshots (in `docs/EC/screenshots/iud_fin_item_def/`) and confirmed DB facts (in
`docs/db-first-coverage-audit.md`), but never packaged a `screens/` bundle, registry row, or
scorecard row - a real documentation gap for an already-proven-working screen, found during a
2026-08-16 cleanup pass.

## Done wrong (this packaging pass)
- First driver attempt failed on `eng.select("Format Mask", "#,###,###.##0")` - the exact string
  from the original screenshot didn't match the live option's `data-item-label`. Fixed by using
  `__FIRST__` instead (the specific mask value doesn't matter for proving the mechanism).
- The evidence-screenshot path was computed as `_HERE.parents[3]` (miscounted - landed at the repo
  root's `screens/` instead of `workstreams/master-plan/ec-automation/screens/`). Fixed to
  `_HERE.parent` (`_HERE` is already the `py/` directory, so `.parent` is `ec-automation`).

## Done well
- Re-derived the real treeview menu path (`EC Revenue > Financial Item > Financial Item
  Definition`) from `tmp/treeview.json`'s config dump rather than guessing, since it was never
  recorded anywhere in the original pilot's commits.
- Confirmed the screen's actual mandatory-field set live via `Engine.field_inventory()` on the
  empty New Object form, rather than assuming it matched the design doc's prose description.
- Ran a completely fresh live proof (`AUTOTEST_FID_006`, 2026-08-16) rather than just repackaging
  the old draft evidence - real, current DB-verified proof.

## Evidence
`evidence/01_loaded.png` through `07_final_state.png` - fresh 2026-08-16 run. DB re-check: 0 rows
for `AUTOTEST_FID_006` in `OV_FINANCIAL_ITEM` after delete.
