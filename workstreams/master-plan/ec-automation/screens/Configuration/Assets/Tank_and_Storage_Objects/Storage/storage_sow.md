# SOW — Storage IUD (Configuration > Assets > Tank_and_Storage_Objects)

- **Screen:** Storage   **BF:** CO.0034   **View:** `OV_STORAGE` (versioned)   **Grid id:** `manageObject:form:T_data`
- **Type:** OV-GM (manage-object, groupmodel), navigator-GATED, date-effective.
- **Pattern (current, since PR #537, merged 2026-08-26):** full Area pattern — 5 TCs (Verify
  Clean State / Insert / Update / Find / Delete), per-TC Login/Logout on one Suite-Setup-opened
  browser, PURE SCREEN verification in the `.robot` file (zero inline DB-verify calls — the DB
  check for TC05 lives inside the shared T2 `Verify Object Removed`).
- **Navigator shape:** genuine 3-level same-row cascade Production Unit -> Area -> Facility
  Class 1 (`nav:form:G:0:R:1:C:1/C:2/C:3:dd`) + GO, filled via the shared T2
  `Apply Navigator From Properties` (moved off the old "Apply OV-GM Navigator First Available"
  mechanism), driven by `testdata/storage_navigator.properties` with EXPLICIT values confirmed
  live via a dedicated recon script (`tmp/recon_storage_navigator_cascade.py`, gitignored):
  `Op Production Unit=AS1 EC Exploration Norway`, `Op Area=AS1_Area`,
  `Op Facility Class 1=AS1_Facility_01` — the same values the prior first-available mechanism
  already picked, now captured explicitly.
- **Mandatory fields:** Storage Code, Storage Name, Start Date (objectForm) + Storage's own
  genuine mandatory dropdowns Storage Type / Product Name (kept as `__FIRST__`, exactly as the
  pre-existing proven driver handled them). `Op Production Unit`/`Op Area`/`Op Facility Class 1`
  also exist on the objectForm but are left blank, matching the already-proven driver's
  behaviour (per-screen trust of proven behaviour over hunting an unstated requirement).
- **Test data:** fixed test code `AUTOTEST_STG` (confirmed free in `OV_STORAGE` via a fresh
  DB connection before use — replacing the old generated/timestamped `AUTOTEST_STG_<timestamp>`
  code). Insert Name = "Automation Test Storage", Update Name = "Automation Test Storage
  UPDATED". Delete = End Date = Start Date (zero-length window, true delete from `OV_STORAGE`).
- **Deliverables:** T3 `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/
  storage_page.resource`, suite `tests/Configuration/Assets/Tank_and_Storage_Objects/
  storage_iud.robot`, `testdata/storage_{navigator,insert,update,form_verify,grid_verify}.properties`,
  this SOW, `README.md`, `JOURNAL.md`, `evidence/`, `CHECKLIST.md`, KB map
  `ec-ui-knowledge/screens/storage.md`. Playwright driver `py/storage_iud.py` predates this
  conversion and stays as-is (permanently waived going forward per the 2026-08-27 owner
  decision — the Universal Screen Engine replaces that role; not rebuilt or re-verified by
  this backfill).

## Dev story (from PR #537, merged 2026-08-26)
Storage started as a bespoke build (4 TCs, single suite-level login, generated/timestamped
test code, inline "Apply OV-GM Navigator First Available" navigator-fill, label-driven
Playwright/RF). PR #537 converted it structurally to Area's full pattern under the owner's
standing rule that any navigator screen matching Area's layout follows Area's pattern: 5 TCs,
per-TC login/logout, fixed test code, properties-file-driven Insert/Update/verify via the
shared T2, explicit `Find/Clear Storage Row By Filter` grid-filter wiring, and pure-screen
verification. The genuine 3-level PU -> Area -> Facility Class 1 cascade itself was *kept* — this
was a structural conversion, not a reclassification of the screen's navigator shape. No T1/T2
(`resources/manage_object.resource`/`resources/common.resource`) changes were needed. Live RF
5/5 pass, full-tree dryrun 850/850, DB self-clean 0 residual via a fresh `oracledb` connection,
filter keyword confirmed fired 15x in `output.xml`.

This backfill (2026-08-28, Batch 4 of `docs/lean-deliverable-backfill-workorder.md`) adds the
documentation/evidence bundle the 2026-08-23/26 lean waiver skipped for this conversion — it does
not modify any RF automation file.
