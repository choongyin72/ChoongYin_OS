# Field Group — EC UI selector map

**Treeview path:** Configuration > Assets > Commercial Objects > Field Group
**Screen type:** Manage Object (OV) — plain, **no navigator** (confirmed live 2026-08-23,
matches `docs/ec_screen_registry.md`).
**DB view:** `OV_FIELD_GROUP`
**Grid id:** `manage_object_nav_nav:form:T_data` (T3 references this via T2's centralized
`${OV_MANAGE_OBJECT_TABLE}` constant, not re-hardcoded — confirmed live 2026-08-23 this
screen's grid uses the same id as every other plain manage-object screen).
**Grid columns (confirmed live):** Code / Name / Start Date / End Date (4 columns).
**Delete semantics:** End Date = Start Date (EC true delete — row removed from
`OV_FIELD_GROUP`).
**Pattern:** Bank pattern (label-driven, properties-file-driven, T2-consolidated), converted
PR #434, merged 2026-08-23 — Batch 3 of the Bank-pattern conversion project (Customer/Field
Group/Licence/MMS Lease/Operator Lease). RF automation:
`pageobjects/Configuration/Assets/Commercial_Objects/field_group_page.resource` +
`tests/Configuration/Assets/Commercial_Objects/field_group_iud.robot`.

## Insert / Update selectors
Labels are the generic **"Code"/"Name"** (NOT screen-prefixed, unlike e.g. Field's "Field
Code"/"Field Name") — confirmed live 2026-08-23. Insert/Update are driven by the shared T2
keywords (`Insert Object From Properties And Verify Code` / `Update Object From Properties`),
reading `testdata/field_group_insert.properties` / `field_group_update.properties` — no
hardcoded field-id selectors remain in `field_group_page.resource` for these forms
(label-driven via the shared T2 layer). Round-trip form-label comparison list
(`@{FIELD_GROUP_FORM_LABELS}`) = Code, Name, Description.

Delete's End Date field IS hardcoded (deliberately, not label-driven — same precedent as
Bank's own `objectdates` shape):
```
${FIELD_GROUP_DEL_ENDDATE}   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```
Row shape: Start Date at C:1, End Date label at C:2, End Date input at C:3 — single row.

## Mandatory / yellow fields (confirmed live via objectForm recon, 2026-08-23)
- Code
- Name
- Start Date

NOT mandatory (confirmed live): End Date, Description, Comments, Field Group Type (dropdown),
Reporting Field Group Indicator (checkbox). Description is included in the test data /
form-label comparison anyway for business-realistic coverage (matching Bank's own inclusion
of optional descriptive fields) — the dropdown/checkbox are deliberately left untested
(optional, not part of this screen's core IUD flow).

## Quirks
- Plain manage-object screen — no mandatory navigator scope, confirmed live at conversion
  time and reconfirmed by this backfill's grep/registry check (2026-08-28). Do not confuse
  with **Field** (`field_page.resource`/`field_iud.robot`), a DIFFERENT screen — an OV-GM
  groupmodel screen with a mandatory Area navigator, screen-prefixed "Field Code"/"Field Name"
  labels, and its own KB map at `ec-ui-knowledge/screens/field.md`.
- Uses a FIXED test code `AUTOTEST_FIELD_GROUP` (matching Bank/State/Country/Object List's
  convention) — every live run must complete TC05 (delete) so the code stays free for the
  next run.
- The pre-conversion (2026-06-12) build used a generated, timestamped code
  (`AUTOTEST_FG_<timestamp>`); PR #434 (2026-08-23) switched this to the fixed code as part of
  the Bank-pattern conversion.
- Explicit grid Code-column filter via the shared T2 `Find/Clear Object Row By Filter`,
  wrapped in screen-local `Find Field Group Row By Filter`/`Clear Field Group Row Filter`
  keywords, wired into Update/Find/Verify-Found/Delete.

## Credentials
Dedicated pair in `resources/credentials.py`: `FIELD_GROUP_EC_USER`/`FIELD_GROUP_EC_PASS`
(added additively by PR #434).

## Last verified
2026-08-28 (backfill re-run: robocop 9 issues — exact parity with PR #434's own baseline;
full-tree dryrun 883/883 PASS; live 5/5 PASS, first attempt; DB self-clean 0 residual
`AUTOTEST_FIELD_GROUP`/`AUTOTEST%` rows in `OV_FIELD_GROUP`) against the local sandbox EC
environment (`localhost:1521/ORCL`, `ECKERNEL_EC`). Selectors/labels themselves last confirmed
live 2026-08-23 (PR #434).
