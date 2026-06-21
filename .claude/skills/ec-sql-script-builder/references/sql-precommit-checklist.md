# EC SQL pre-commit checklist (scan before committing any config/scheduler SQL)

Tick all 10. If any fails, fix before commit. (Full rationale in `../SKILL.md`.)

1. ☐ **Writes through `OV_*`/`TV_*` views** where one exists; base tables only with a stated reason.
2. ☐ **FK by business CODE, no hardcoded GUIDs** (code subquery / `GetObjIDFromCode`).
3. ☐ **Repeated literals are `DECLARE` constants** (`v_code`, `v_rev`, dates, class names) — none repeated inline.
4. ☐ **Update-insert pattern** `UPDATE …; IF SQL%ROWCOUNT = 0 THEN INSERT … VALUES …; END IF;` — **no `MERGE`, no `NOT EXISTS`**, **flat blocks (no local procedures)**.
5. ☐ **`REV_TEXT = 'ECPR-XXXX'`** (real ticket) on **every** INSERT and UPDATE.
6. ☐ **No `EXCEPTION` block, no `COMMIT`** in the file; one `declare … begin … end; /`.
7. ☐ **Correct dependency order** — create parent→child; delete child→parent (incl. all qrtz trigger sub-types for schedules).
8. ☐ **Matching teardown shipped** (`delete_<name>.sql`, + `_ov` if view-deletable) — child-first, scoped by linkage, re-runnable, products untouched.
9. ☐ **Verify-before-assume done:** confirmed OV column code-vs-object_id; checked `TIME_SCOPE_CODE` for delete method; aware which view columns are derived/non-settable.
10. ☐ **Verified for real:** idempotency proven (`sql_idempotency_check.py` PASS) **and** the config works **end-to-end** (not just row counts), tested on a **throwaway** code (not live config); proof cited in the commit/PR.
