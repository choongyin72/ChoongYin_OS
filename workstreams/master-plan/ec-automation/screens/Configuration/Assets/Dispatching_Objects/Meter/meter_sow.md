# SOW — Meter

_Screen: Configuration > Assets > Dispatching Objects > Meter. View `OV_METER` (versioned, BU-gated
OV-GM manage-object). Backfilled 2026-08-27 under `docs/lean-deliverable-backfill-workorder.md`
Batch 3 — the RF automation itself was already built and merged via PR #554 (2026-08-26); this SOW
documents that already-existing, already-verified work, it does not rebuild anything._

## Classification
OV-GM (BU-gated) **+ popup**. Converted to the full **Area pattern** (properties-file-driven,
per-TC login, T2-consolidated, explicit grid-filter wiring) via `ec-area-pattern-converter`,
PR #554, merged 2026-08-26.

## Navigator shape
Single mandatory **Business Unit** dropdown at `nav:form:G:0:R:1:C:1:dd` — the SAME
single-dropdown shape as Area's own Production Unit navigator. A second dropdown at
`nav:form:G:0:R:1:C:2:dd`, labelled "Delivery Point", exists in the navigator row but is
**optional** (GO succeeds with only C:1 filled, confirmed live 2026-08-26).

**IMPORTANT — real story, wrong-then-corrected classification:** earlier in the same working
session that eventually produced PR #554, Meter was WRONGLY classified as "does not fit the Area
pattern." That first call conflated the INSERT FORM's Delivery Point popup (a separate, generic T1
`Pick From EC Object Popup` field that lives entirely inside the insert form) with the navigator
itself. A deeper live re-investigation corrected this: the actual navigator is exactly the single
mandatory Business Unit dropdown described above, structurally identical to Area's. Once that was
seen clearly, the conversion proceeded exactly like every other Area-shaped screen. See
`JOURNAL.md`'s "Done wrong / lessons" section for the full account — this correction is the single
most important fact about Meter's conversion history and must not be softened or omitted from any
future summary of this screen.

## Grid / cell shape
- Grid: `manageObject:form:T_data`.
- Delete = End Date = Start Date (true date-effective delete in `OV_METER`), field id
  `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded — packed date row, same
  documented rationale as Area/Bank's own `_DEL_ENDDATE`).
- Field labels are screen-prefixed: "Meter Code" / "Meter Name" (not the generic "Code"/"Name"
  Bank/Object List use).

## Mandatory fields (insert form, confirmed live 2026-08-26, all MandatoryCellStyle/yellow)
- Start Date
- Delivery Point Name — the generic T1 popup picker (`resources/popup.resource`,
  `Pick From EC Object Popup`), NOT a dropdown. Navigator-filtered (must set Business Unit first
  or the popup list returns "No records found").
- Meter Code
- Meter Name
- Meter Type (dropdown: Entry/Exit/Fuel/Transit)

Insert file ORDER is load-bearing (preserved from the original 2026-06-13 driver): Start Date →
Delivery Point Name (popup) → Meter Code → Meter Name → Meter Type → Save. The popup's close
callback resets the form's dirty/save state, so Save immediately after the popup (before
Code/Name/Type are filled) would silently no-op.

Update form: only **Meter Name** is exercised (Meter Code is read-only in `updateAttributes`,
confirmed live).

## Test data used
- Fixed test code `AUTOTEST_METER` (confirmed free in `OV_METER` via a fresh oracledb connection
  before the build; confirmed 0 residual after every live run since).
- Navigator: Business Unit = `ECP Norway` (same value the pre-existing driver proved live
  2026-06-13).
- Insert: Start Date `2020-01-01`, Delivery Point Name `300005 PG Hoogerheide`, Meter Code
  `AUTOTEST_METER`, Meter Name `Automation Test Meter`, Meter Type `Entry`.
- Update: Meter Name → `Automation Test Meter UPDATED`.
- Delete: End Date = Start Date (`2020-01-01`).

## Dev story (from PR #554's real body + the registry row's detailed narrative)
Meter's existing RF automation (an older 4-TC/suite-login/generated-code/inline-DB-verify pattern,
live 4/4 since 2026-06-13) was converted to the full 5-TC Area pattern on 2026-08-26 — the same day
an earlier attempt in this session had wrongly concluded Meter "does not fit" the Area pattern by
conflating the Delivery Point popup with the navigator. Once corrected, the conversion carried the
genuine BU navigator gesture and the genuine Delivery Point popup mechanism through unchanged
(same situation as Chemical Stream's own From Connection popup, which likewise didn't block that
screen's own Area-pattern conversion) and rebuilt everything around them: properties-file-driven
insert/update/verify (`testdata/meter_navigator.properties`, `meter_insert.properties`,
`meter_update.properties`, `meter_form_verify.properties`, `meter_grid_verify.properties`),
per-TC login/logout (`METER_EC_USER`/`METER_EC_PASS` added to `resources/credentials.py`), a fixed
test code, TC04 Find added (5 TCs total), explicit `Find/Clear Meter Row By Filter` wired into
Update/Find/Verify-Found/Delete, and zero inline DB-verify calls in the `.robot` file. No shared
T1/T2 files were touched — the existing `Apply Navigator From Properties` and generic
`Pick From EC Object Popup`/`Pick OV Popup By Label` mechanisms already covered Meter's shape with
zero gaps. Full `tests/` tree dryrun 874/874 pass; robocop 7 issues on the changed screen files =
exact parity with `area_page.resource`/`area_iud.robot`'s own 7-issue baseline (+3 pre-existing
unrelated `credentials.py` findings, not a regression); live run 5/5 pass; DB self-clean confirmed
0 residual `AUTOTEST_METER%` rows via fresh independent oracledb connections both before and after
the live run.

## Files (unchanged by this backfill — listed for reference only)
- `pageobjects/Configuration/Assets/Dispatching_Objects/meter_page.resource`
- `tests/Configuration/Assets/Dispatching_Objects/meter_iud.robot`
- `testdata/meter_navigator.properties`, `meter_insert.properties`, `meter_update.properties`,
  `meter_form_verify.properties`, `meter_grid_verify.properties`
- `resources/credentials.py` (additive: `METER_EC_USER`/`METER_EC_PASS`)
- `docs/ec_screen_registry.md` (Meter row, starred, with the correction narrative)
- `docs/automation-scorecard.md` (Dispatching Objects — slice 2 row)
- `docs/meter_popup_notes.md` (the original 2026-06-13 popup-gesture recon, still the reference
  for the `Pick From EC Object Popup` mechanism)
