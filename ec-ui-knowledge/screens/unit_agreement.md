# Screen: Unit Agreement

- **Type:** OV (EC Object Configuration, date-effective, Bank family) - **no navigator** (date-only,
  not OV-GM).
- **Treeview path:** Configuration > Assets > Royalty Objects > Unit Agreement (RC.0055).
- **Open via:** menu search / `Open EC Screen` (T1 common.resource).
- **DB view (ground truth):** `OV_UNIT_AGR` (base table `UNIT_AGR`, app `EC_REVN`; key `CODE`; also
  `NAME`, `COMMENTS`, `OBJECT_START_DATE`, `OBJECT_END_DATE`). ⚠️ **View name does NOT match the
  "unit_agreement" slug** - do not derive it from the slug.
- **Last verified:** 2026-08-28 (this backfill) · EC 14.2.4 · local sandbox
  (`ap-f0a7g341jn6d.corp.quorumsoftware.com:8443`) · live I-U-D 5/5 DB-verified. Selectors below
  transcribed from the current T3's own Variables section (converted 2026-08-23, PR #446), not
  re-scanned live by this backfill task.
- **Pattern:** follows `../EC_OBJECT_CONFIG_IUD.md` / Bank's own pattern (this file only records
  what is Unit-Agreement-specific).

## Selectors `[from unit_agreement_page.resource Variables section, PR #446]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `manage_object_nav_nav:form:T_data` (via T2's `${OV_MANAGE_OBJECT_TABLE}` constant - not re-hardcoded in the T3) |
| Row filter | `Find Object Row By Filter` / `Clear Object Row Filter` (shared T2, `resources/manage_object.resource`) - wrapped by `Find/Clear Unit Agreement Row By Filter` |
| Insert | `Insert Object From Properties And Verify Code` (shared T2) via `testdata/unit_agreement_insert.properties`, `code_label=Unit Agreement Code` |
| Update | `Update Object From Properties` (shared T2) via `testdata/unit_agreement_update.properties` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded - packed row, Start Date at `C:1`/End Date at `C:3`, label at `C:2`; NOT label-driven, same precedent as Bank's `END_DATE_ID`) |

### Field labels (live-confirmed 2026-08-23, PR #446)
- **`objectForm` (Insert) mandatory:** Unit Agreement Code, Unit Agreement Name, Start Date.
  Comments is optional (`{mandatory:false}`). End Date exists in `objectForm` but is deliberately
  left unset at insert (setting it = Start Date would create a zero-length true-delete window).
- **`updateAttributes` (Update) - exactly 3 labels:** Unit Agreement Code (read-only), Unit
  Agreement Name, Comments. Start Date/End Date are NOT present here - they live only in
  `objectForm`/`objectdates`.
- `@{UA_FORM_LABELS}` in the T3 = `Unit Agreement Code`, `Unit Agreement Name`, `Comments` - shared
  by both the TC02 insert-verify and TC04 find-verify checks.
- **Screen-prefixed labels:** "Unit Agreement Code"/"Unit Agreement Name" - NOT the generic
  "Code"/"Name" Bank itself uses. Same non-universal-label gotcha as State/County/Royalty Owner.

## Mandatory-yellow fields
Unit Agreement Code, Unit Agreement Name, Start Date (insert only). Comments is optional. No
navigator section exists on this screen at all (plain Bank-family OV).

## Quirks
- ⚠️ **View/slug mismatch:** DB view `OV_UNIT_AGR` does not derive from the "unit_agreement" slug -
  any new DbVerify call for this screen must cite `ov_unit_agr` explicitly, never assume it from
  the folder/screen name.
- Delete End Date id is a hardcoded constant (`UA_DEL_ENDDATE` in the T3), not label-resolved -
  the packed Start/End Date row defeats the one-field-per-row label scan.
- Grid-filter wiring (`Find/Clear Unit Agreement Row By Filter`) has been present since the
  2026-08-23 conversion (PR #446), not bolted on later.
- Test code is FIXED (`AUTOTEST_UA`), not per-run - TC05 (delete) must complete every run so the
  code stays free next time.

## Automation (code lives in ec-automation - this file is the MD selector reference)
- **RF (the maintained/live suite):** T3
  `ec-automation/pageobjects/Configuration/Assets/Royalty_Objects/unit_agreement_page.resource` +
  suite `ec-automation/tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot` (T2
  `manage_object.resource` + T1 `common.resource` + `libraries/DbVerify.py`). Converted to the full
  Bank pattern via PR #446 (2026-08-23). Live 5/5, DB-verified (`OV_UNIT_AGR`), self-cleaning.
- **Playwright (original 2026-06-25 reference, NOT rebuilt for the Bank-pattern conversion per
  owner decision 2026-08-27, Section H):**
  `ec-automation/screens/Configuration/Assets/Royalty_Objects/Unit_Agreement/playwright/
  ec_iud_unit_agreement.py`.
