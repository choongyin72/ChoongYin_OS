# SOW - External Location IUD (Configuration > Assets > Facility_Objects)

- **Screen:** External Location   **BF:** CO.0227   **View:** `OV_EXTERNAL_LOCATION`   **Base:** `EXTERNAL_LOCATION`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), date-effective.
  Classified as the Area pattern's **zero-mandatory-nav edge case** [from `docs/ec_screen_registry.md`
  External Location row + `external_location_page.resource`'s own Documentation]: unlike Area/Well/
  Test Separator/Chemical Tank, the navigator has NO mandatory scope at all - its fields are optional
  filters, and the grid loads on GO alone.
- **Navigator shape:** GO only - no dropdown/cascade fill required. The RF suite still delegates to
  the shared T2 `Apply Navigator From Properties` keyword (`resources/manage_object.resource`) driven
  by an intentionally EMPTY `testdata/external_location_navigator.properties` (comments only, zero
  data lines), so its behaviour is byte-for-byte identical to a bare GO - this was proven live in
  PR #524 (see dev story below).
- **Grid id:** `manageObject:form:T_data`.
- **Mandatory fields** (New Object / `objectForm`, label-driven): **External Location Code**,
  **External Location Name**, **Start Date**. Update (`updateAttributes`): Code is read-only, only
  **External Location Name** is editable (no Description field on this screen). Delete
  (`objectdates`): End Date = Start Date (true delete in `OV_EXTERNAL_LOCATION`).
- **Test data used:** fixed test code `AUTOTEST_EXTERNAL_LOCATION` (converted from the original
  build's timestamped `AUTOTEST_EL<timestamp>` by PR #528, confirmed free of any existing row via a
  fresh `oracledb` query before first use under the new scheme); `START_DATE = 2000-01-01`;
  insert/update/verify field values driven by `testdata/external_location_{insert,update,
  form_verify,grid_verify}.properties`.
- **IUD flow (current, 5 TCs):** TC01 Verify Clean State -> TC02 Insert -> TC03 Update (Name) ->
  TC04 Find -> TC05 Delete (End Date = Start Date); self-clean = absent from `OV_EXTERNAL_LOCATION`.

## Dev story (real history, from PR #524 and PR #528 bodies - not invented)
Built 2026-08-01 as a standard `ec-object-iud-builder` OV-GM screen (4-TC RF suite, full Playwright +
RF bundle, `verify_screen.py` OVERALL PASS). On 2026-08-26, PR #524 used External Location as the
**first proof case** for a new shared T2 keyword, `Apply Navigator From Properties`
(`resources/manage_object.resource`, built for Area's mandatory-Production-Unit navigator in PR #523):
because External Location's own navigator has no mandatory scope, the conversion drove that keyword
with an intentionally empty properties file, confirming both live and via a `PropertiesReader.py`
source-read that an all-comment file degrades gracefully to zero fills -> bare GO, i.e. no behaviour
change at all. Immediately after (same day, stacked on #524's still-open branch since #524 had not
yet merged - a premise #528 explicitly verified via `gh pr view`/`git merge-base` rather than assuming
the task's stated "already merged" claim was correct), PR #528 applied the owner's 2026-08-26 standing
rule that any navigator-section screen matching Area's layout gets Area's FULL pattern - not just the
navigator-fill piece. That converted the RF suite's STRUCTURE from 4 TCs/single-login/inline-DB-verify
to Area's 5-TC/per-TC-login/properties-driven/explicit-grid-filter/pure-screen-verify shape, while
explicitly keeping the screen's genuine GO-only navigator behaviour unchanged. Both PRs are the real
source for every claim in this SOW and in `JOURNAL.md`.
- Deliverables: driver `py/external_location_iud.py` (untouched since 2026-08-01 - the 2026-08-26
  conversions were RF-only), T3 `pageobjects/Configuration/Assets/Facility_Objects/
  external_location_page.resource`, suite
  `tests/Configuration/Assets/Facility_Objects/external_location_iud.robot`, this SOW,
  `VERIFY-REPORT.md` (2026-08-01, auto-generated for the base build).
