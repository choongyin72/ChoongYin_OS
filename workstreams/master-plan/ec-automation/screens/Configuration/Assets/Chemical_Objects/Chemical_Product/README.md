# Chemical Product IUD — Bundle README

**Screen:** Configuration > Assets > Chemical Objects > Chemical Product (`CO.0072`), OV
manage-object, date-effective. Built from scratch via `ec-bank-pattern-new-screen` (PR #486,
merged 2026-08-24). This bundle is a **documentation/evidence backfill** (Batch 12, per
`docs/lean-deliverable-backfill-workorder.md`) — the RF automation itself is untouched.

## Files in this bundle
- `chemical_product_sow.md` — classification, shape, test data, dev story.
- `README.md` — this file.
- `JOURNAL.md` — Built / Done well / Done wrong / Blockers / Decisions / Evidence, from PR #486.
- `evidence/` — a real live-run capture (log.html / output.xml / summary) from this backfill.
- `CHECKLIST.md` — the 21-item deliverable checklist, ticked with real evidence citations.

## Real automation files (NOT part of this bundle, NOT modified by this backfill)
- T3 page object: `workstreams/master-plan/ec-automation/pageobjects/Configuration/Assets/Chemical_Objects/chemical_product_page.resource`
- Suite: `workstreams/master-plan/ec-automation/tests/Configuration/Assets/Chemical_Objects/chemical_product_iud.robot`
- Test data: `workstreams/master-plan/ec-automation/testdata/chemical_product_{insert,update,form_verify,grid_verify}.properties`
- Screen-scoped cleanup library: `workstreams/master-plan/ec-automation/libraries/ChemicalProductCleanup.py`
- KB selector map: `ec-ui-knowledge/screens/chemical_product.md`

## Exact commands to run the suite

From `workstreams/master-plan/ec-automation/`:

**Dryrun (this suite only):**
```
robot --dryrun --outputdir results/chemical_product_dryrun tests/Configuration/Assets/Chemical_Objects/chemical_product_iud.robot
```

**Live headless run (5 TCs — clean-state / insert / update / find / delete):**
```
EC_HEADLESS=true robot --outputdir results/chemical_product_live tests/Configuration/Assets/Chemical_Objects/chemical_product_iud.robot
```

**Live headed run (visual confirmation):**
```
EC_HEADLESS=false robot --outputdir results/chemical_product_live tests/Configuration/Assets/Chemical_Objects/chemical_product_iud.robot
```

## DB self-clean check pattern (fresh connection, after the live run)

```sql
-- Should return 0 rows after a completed run (TC05 delete succeeded)
SELECT * FROM CHEM_PRODUCT WHERE OBJECT_CODE LIKE 'AUTOTEST%';
SELECT COUNT(*) FROM OV_CHEM_PRODUCT WHERE CODE LIKE 'AUTOTEST%';

-- Orphan check for the known-issue child table (should be 0 — no leftover
-- CHEM_USAGE_REPORT_CONF rows once ChemicalProductCleanup has run)
SELECT COUNT(*) FROM CHEM_USAGE_REPORT_CONF c
  WHERE NOT EXISTS (SELECT 1 FROM CHEM_PRODUCT p WHERE p.OBJECT_CODE = c.OBJECT_CODE);
```

Use a **fresh** DB connection for this check (not the same session as the live run) — per
CLAUDE.md's "verify live state fresh conn before claiming" rule.
