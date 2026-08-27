# SOW - Collection Point IUD (Configuration > Assets > Facility_Objects)

_Updated 2026-08-27 (lean-deliverable backfill, `docs/lean-deliverable-backfill-workorder.md`,
Batch 3): reflects PR #541's Area-pattern conversion. Section below the rule is the original
2026-08-01 SOW, retained for history._

## Current shape (post PR #541, 2026-08-26)
- **Screen:** Collection Point   **BF:** CO.0205   **View:** `OV_COLLECTION_POINT`   **Base:** `COLLECTION_POINT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- **Navigator:** genuine 3-level SAME-ROW cascade Production Unit -> Area -> Operator Route
  (`nav:form:G:0:R:1:C:1/C:2/C:3:dd`, C:4 absent) + GO. Confirmed live 2026-08-26 via
  `tmp/recon_cp_navigator_cascade.py`. Delegated to the shared T2 `Apply Navigator From
  Properties` keyword (`resources/manage_object.resource`), driven by
  `testdata/collection_point_navigator.properties` with the SAME explicit values the prior
  bespoke driver used (Op Production Unit=P3 Production Unit, Op Area=P3 Area, Op Operator
  Route=Oper Route 1) — first-available breaks a later level on this screen, so these are
  PROVEN explicit values, not re-invented ones.
- **Timing:** the shared T2 keyword's flat 0.7s sleep between cascade levels was confirmed live
  SUFFICIENT for this screen's redraw timing at BOTH the PU->Area and Area->Operator Route
  transitions — no shared-file change and no per-screen extra `Sleep` were needed. This is a
  second independent confirmation of the shared keyword's default timing generalizing beyond its
  first proof point (Chemical Stream Hookup, Batch 2).
- **Grid columns:** Collection Point Code / Collection Point Name / Start Date / End Date
  (confirmed live via `manageObject:form:T_head` scan) — same 4-column shape as Area/Facility
  Class 1.
- **Fields BY LABEL**, screen-prefixed (`Collection Point Code`/`Collection Point Name`, not the
  generic `Code`/`Name`), matching Area's own convention.
- **TC structure:** 5 TCs — TC01 Verify Clean State, TC02 Insert, TC03 Update (Name), TC04 Find,
  TC05 Delete (End Date = Start Date) — each with its own Login/Logout (no suite-level login).
- **Test data:** fixed code `AUTOTEST_COLLECTION_POINT` (confirmed free via a fresh oracledb
  connection before use, 0 rows in `OV_COLLECTION_POINT`), not a generated/timestamped code.
  Self-clean = absent in `OV_COLLECTION_POINT` after TC05.
- **Dev story (from PR #541):** converted from the OLD bespoke pattern (4 TCs, suite-level login,
  inline nav-fill via 3x `Select EC Dropdown Option` + `Apply Navigator`, timestamped test code,
  inline screen-local DB-verify wrapper keywords) to Area's full pattern — the real gotcha the PR
  called out was that the navigator's 3-level cascade and its timing had to be RE-VERIFIED LIVE
  rather than trusted from the old driver's documentation, per the owner's standing "no guessing"
  rule; that re-verification passed cleanly (C:1/C:2/C:3 present, C:4 absent, 0.7s sleep
  sufficient both transitions), so no shared-file change was required, only the T3/suite rebuild.
- **Deliverables:** T3 `pageobjects/Configuration/Assets/Facility_Objects/collection_point_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot` (5 TCs), 5
  properties files, this SOW, `README.md`, `JOURNAL.md`, `CHECKLIST.md`, `evidence/`, KB map
  `ec-ui-knowledge/screens/collection_point.md`. Playwright driver `py/collection_point_iud.py`
  and its `investigation/recon.py` are RETAINED from the original 2026-08-01 build but were
  explicitly UNTOUCHED by PR #541 (RF `.robot` structural conversion only) and are not part of
  this backfill's scope (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` keeps items 4/5 waived
  for Area-pattern work — the Universal Screen Engine is the owner-decided replacement going
  forward).

---

## Original SOW (2026-08-01 build, retained for history)
- **Screen:** Collection Point   **BF:** CO.0205   **View:** `OV_COLLECTION_POINT`   **Base:** `COLLECTION_POINT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade (PROVEN explicit values, not first-available) + GO; fields BY LABEL.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_CP<timestamp>`; self-clean = absent in OV_COLLECTION_POINT.
- Deliverables: driver `py/collection_point_iud.py`, T3 `pageobjects/Configuration/Assets/Facility_Objects/collection_point_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
