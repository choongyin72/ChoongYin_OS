# Deferment Group (CO.0149) — Bank-pattern OV IUD bundle

Manage-Object (OV) screen: **Configuration > Assets > Facility_Objects > Deferment Group**. Plain
Bank-pattern (no navigator, no mandatory dropdowns). Full Insert / Update / Find / Delete (End Date
= Start Date), DB-verified against `OV_DEFERMENT_GROUP`, self-cleaning. Rebuilt in PR #479
(Batch 8, merged 2026-08-23) to the label-driven, properties-file-driven, T2-consolidated,
explicit-grid-filter shape shared by Bank/State/Berth/Bank Account — **zero hardcoded field ids**.

_This bundle was backfilled 2026-08-28 per `docs/lean-deliverable-backfill-workorder.md` (Batch 11).
The RF automation itself was NOT modified as part of this backfill — see JOURNAL.md._

## Artifacts
- **SOW:** `deferment_group_sow.md`
- **RF T3 (page object):** `../../../../pageobjects/Configuration/Assets/Facility_Objects/deferment_group_page.resource`
- **RF suite:** `../../../../tests/Configuration/Assets/Facility_Objects/deferment_group_iud.robot`
- **Test data:** `../../../../testdata/deferment_group_{insert,update,form_verify,grid_verify}.properties`
- **Credentials:** `DEFERMENT_GROUP_EC_USER`/`DEFERMENT_GROUP_EC_PASS` in `../../../../resources/credentials.py`
- **evidence/** — see JOURNAL.md for what each artifact captures (includes a disclosed live-run failure)
- Playwright driver / `investigation/` — **waived** (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`;
  the Universal Screen Engine is the owner-decided replacement, not built per screen going forward)

## Exact commands

### Dryrun (static structure check, no live access needed)
```
cd workstreams/master-plan/ec-automation
robot --dryrun --outputdir results/_defermentgroup_dryrun tests/Configuration/Assets/Facility_Objects/deferment_group_iud.robot
```

### Live headless run
```
cd workstreams/master-plan/ec-automation
EC_HEADLESS=true robot --outputdir results/_defermentgroup_live tests/Configuration/Assets/Facility_Objects/deferment_group_iud.robot
```

### robocop
```
robocop check pageobjects/Configuration/Assets/Facility_Objects/deferment_group_page.resource
robocop check tests/Configuration/Assets/Facility_Objects/deferment_group_iud.robot
```

### DB self-clean check (fresh connection, not the RF library's own)
```sql
SELECT COUNT(*) FROM OV_DEFERMENT_GROUP WHERE CODE = 'AUTOTEST_DEFERMENT_GROUP';
-- expect 0 after a completed I-U-D cycle
```

### Live-access pre-flight (run this FIRST if the suite times out on the menu-search tv-link)
```sql
SELECT OBJECT_ID, ROLE_ID, LEVEL_ID FROM TV_T_BASIS_ACCESS WHERE OBJECT_ID = 1087 ORDER BY ROLE_ID;
-- LEVEL_ID=0 for all 5 roles = the screen is role-access-blocked (real, recurring issue — see JOURNAL)
```

## Verified (real runs, not hand-ticked) — see CHECKLIST.md for full citations
- robocop: page object 0 issues, suite 9 issues (VAR02/DOC02 baseline noise, same class accepted
  across Batches 7-11) — both re-confirmed 2026-08-28.
- Full-tree `--dryrun`: 774/774 PASS at PR #479 merge time; this screen's own `--dryrun` re-confirmed
  5/5 PASS 2026-08-28.
- **LIVE RF run: 5/5 PASS at PR #479 merge time (2026-08-23). Re-run 2026-08-28 for this backfill's
  evidence capture FAILED 0/5 (both an initial attempt and one retry) — root-caused via a direct
  `TV_T_BASIS_ACCESS` query to a REGRESSED role-access grant (`LEVEL_ID=0` again for `OBJECT_ID=1087`,
  all 5 roles), not an automation defect. See JOURNAL.md "Blockers -> resolution".**
- Self-clean: 0 residual rows confirmed at PR #479 merge time via a fresh `oracledb` connection.
- hygiene: PASS (repo-wide `check_bundle_hygiene.py`, re-run 2026-08-28).
