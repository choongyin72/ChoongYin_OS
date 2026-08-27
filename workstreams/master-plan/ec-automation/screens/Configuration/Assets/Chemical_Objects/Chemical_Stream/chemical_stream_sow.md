# SOW - Chemical Stream IUD (Configuration > Assets > Chemical_Objects)

- **Screen:** Chemical Stream   **BF:** CO.0258   **View:** `OV_CHEM_STREAM`   **Base:** `CHEM_STREAM`
- **Type:** OV-GM (grid `manageObject:form:T_data`) with a **mandatory Pick-from-EC-Object POPUP**
  (From Connection). Navigator = SPECIFIC P1 values (P1 Production Unit -> P1 Area -> P1 Facility 1):
  the popup source is EMPTY under the first-available AS1 scope (the original park reason; owner
  screenshot 2026-07-30 proved the P1 scope populates it with CHEM_TANK entries P1 CT001..CT014).
- **The popup is NOT the standard object_popup** (recon-verified): `stream_node_ref_popup` has its
  own inner navigator (inherits the outer P1 scope), an **Object Type dd** (`nav:form:G:4`, EMPTY on
  open -> select `CHEM_TANK`), an **inner GO** (`button:form:B`), and its list grid id is
  **`manage_object_nav_nav:form:T_data`** (NOT `PopupList:form:T_data`). Hence screen-LOCAL popup
  handlers in both the driver and the T3 - the generic engine `pick_popup` / T1
  `Pick First EC Object Popup` do not fit (they wait for PopupList and drive no inner steps).
- **Insert extras:** Chemical Stream Type (mandatory dd, first-available = 'Pump Stream');
  From Connection = first CHEM_TANK row under the P1 scope. Form order quirk: Start Date is R:0
  (BEFORE Code/Name) - the T3 fills it first.
- **Start Date = 2020-01-01.** DELETE = End Date = Start Date. **Fixed test code `AUTOTEST_CHS`**
  (changed from the original per-run `AUTOTEST_CHS_<timestamp>` scheme by the 2026-08-26
  Area-pattern conversion, PR #545 - confirmed free in `OV_CHEM_STREAM` before use, self-cleaning
  every run so the code is free again for the next run).

## Known risks
- Nav scope + popup source are DATA-dependent (P1 chem tanks); if removed/renamed, re-derive a scope.
- Popup internals (grid id / Object Type dd position) are per-popup-type facts - if EC changes the
  stream_node_ref_popup layout, re-recon with tmp/recon_chs_popup2.py (kept in investigation/).

## Addendum 2026-08-27 - Area-pattern conversion (PR #545, merged 2026-08-26) + doc backfill

**Dev story (from PR #545's real body, per `docs/lean-deliverable-backfill-workorder.md` Section H
backfill):** owner standing rule 2026-08-26 - any EC screen whose navigator matches Area's same-row
cascade layout must follow Area's FULL pattern, not just the navigator-fill piece. Chemical Stream's
genuine 3-level Production Unit -> Area -> Facility Class 1 cascade (same-row, increasing column
`nav:form:G:0:R:1:C:1/C:2/C:3:dd`) qualified. The RF suite was rebuilt from its old 4-TC/
single-suite-login/inline-DB-verify shape to Area's 5-TC/per-TC-login/properties-file-driven/
pure-screen-verify shape - while the mandatory **From Connection** popup (`stream_node_ref_popup`,
screen-local `Open From Connection Popup List`/`Pick From Connection Popup` keywords, inner Object
Type dd `nav:form:G:4` = CHEM_TANK + inner GO + grid `manage_object_nav_nav:form:T_data`) was
**preserved exactly as-is** - it is orthogonal to the outer navigator, not a navigator replacement,
and was confirmed still firing during TC02 Insert (PR #545's own live `output.xml` +
`TC02 Insert Chemical Stream Data_action.png`).

**What changed in the RF suite (PR #545):**
- `pageobjects/.../chemical_stream_page.resource` rebuilt: navigator fill now delegates to the
  shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`) driven by
  `testdata/chemical_stream_navigator.properties`, instead of the old screen-local
  `Apply Chemical Stream Navigator` keyword. Popup keywords unchanged.
- `tests/.../chemical_stream_iud.robot` rebuilt: 5 TCs (added TC04 Find), per-TC
  `Login To EC Application`/`Logout From EC Application` on one browser opened once in Suite Setup,
  fixed test code `AUTOTEST_CHS`, zero inline DB-verify calls left in the `.robot` file (DB check
  now lives only inside the shared T2 `Verify Object Removed`).
- New properties files: `testdata/chemical_stream_{navigator,insert,update,form_verify,
  grid_verify}.properties`.
- `resources/credentials.py`: additive `CHEMICAL_STREAM_EC_USER`/`CHEMICAL_STREAM_EC_PASS`.
- No shared T1/T2 file changes needed - `resources/manage_object.resource`'s existing
  `Apply Navigator From Properties` already supported this 3-level same-row cascade shape.

**PR #545 evidence cited:** live RF 5/5 pass; full-tree `robot --dryrun tests/` 850/850 pass, no
regressions; robocop parity with Area's own baseline (10 issues at PR #545 time); filter-keyword
`Find Object Row By Filter` confirmed fired 15 times in live `output.xml`; DB self-clean confirmed
(0 residual `AUTOTEST%` rows in `OV_CHEM_STREAM`, fresh oracledb connection, post-run).

**This doc backfill (2026-08-27, `docs/lean-deliverable-backfill-workorder.md` Batch 2) does NOT
touch the RF automation** - it re-runs the existing suite once for fresh evidence and refreshes
SOW/README/JOURNAL/CHECKLIST.md/KB map per the retired lean waiver. Re-measured this session:
robocop now reports 7 issues (VAR02 x2 + DOC02 x5) on the same two files - same shape as Area's own
current baseline and Chemical Stream Hookup's, no functional drift from PR #545's 10-issue snapshot
(count difference is cosmetic/robocop-config drift over time, not a regression); full-tree
`robot --dryrun tests/` now 883/883 pass; live RF re-run 5/5 pass; DB self-clean re-confirmed (0
residual `AUTOTEST%` rows in `OV_CHEM_STREAM`, fresh connection, before and after this session's
run).
