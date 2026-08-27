# Screen: Property

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel;
  navigator-GATED. Navigator is TWO separate DOM groups (`nav:form:G:0` Date, `nav:form:G:1`
  Business Unit), but only `G:1` is mandatory-and-empty - see "Quirks" below.
- **BF_CODE:** SP.0059 - **Treeview:** Configuration > Assets > Data Mapping Objects > Property
- **DB view:** `OV_PROPERTY` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`, `BUSINESS_UNIT_CODE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05, first attempt, no retry), grid-filter grep count 15 (matches PR #559's own
  cited count) (backfill re-run of PR #559's Area-pattern conversion, merged 2026-08-26).

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Property` -> `label.tv-link` "Property" |
| Grid | `manageObject:form:T_data` (OV-GM, lazy redraw; empty until nav Business Unit + GO) |
| Navigator - Date (`G:0`) | `nav:form:G:0:R:1:C:0:da_input` - already carries a non-empty default on load, **needs NO fill** |
| Navigator - Business Unit (`G:1`, MANDATORY) | `nav:form:G:1:R:1:C:0:dd` - addressed at **column 0**, not column 1 (unlike Area/Well/etc.) - confirmed live via DOM scan (`MandatoryCellStyle`, empty+mandatory) |
| Navigator GO | `button:form:B` |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven - same documented rationale as Area/Bank's own End Date field: this row packs Start Date/End Date together with the label between them) |

### Shared-keyword addressing (reused from Tract, PR #555; called by Property, PR #559)
The T2 `Apply Navigator From Properties` keyword (`resources/manage_object.resource`) carries two
optional, backward-compatible arguments (added for Tract's own conversion, PR #555, merged
2026-08-26, ahead of Property's):
- `${group}` (default `0`) - which `nav:form:G:N` group to target. Property passes `group=1`.
- `${start_col}` (default `1`) - which column within the group's row to start filling from.
  Property passes `start_col=0` (its Business Unit dropdown sits at `C:0`, not the default `C:1`).

Called from `property_page.resource`'s `Open Property Screen With Navigator Values Populated`:
```robotframework
Apply Navigator From Properties    ${PROPERTY_NAVIGATOR_PROPERTIES}    group=1    start_col=0
```
Every other existing caller (Area, Well Hookup, Contract, Meter, etc.) omits both arguments and
is unaffected - defaults preserve the original single-row/`C:1..C:N` cascade behavior.

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Property Code*** - **Property Name*** - **Start Date*** (date) - End Date - Comments -
**Business Unit Name** (reference dropdown, must equal nav scope) - Use as Property (checkbox).
(`*` mandatory per live scan; Business Unit Name is not flagged yellow but MUST be set to match
the navigator's Business Unit or the row won't list correctly under that scope.)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Property Code` (ro) - **`Property Name`**. Delete: **`End Date`** = Start Date -> leaves
`OV_PROPERTY` (raw SQL UPDATE is REJECTED - `ORA-20299: ... PROPERTY class is a read-only class`;
cleanup MUST go through the live UI's own End=Start gesture, same as `OV_ROYALTY_CONTRACT`).

## Navigator value (this environment)
Business Unit = **"Royalty Canada"** (16 total live options, confirmed present) - driven by
`testdata/property_navigator.properties` via the shared T2 `Apply Navigator From Properties`
keyword. This exact value MUST also appear in `testdata/property_insert.properties`'s "Business
Unit Name" field - the inserted/updated Property's Business Unit must equal the navigator's own
scope or the row is invisible under this OV-GM filter. "Royalty Canada" (`ROYALTY_CA`) is only
effective from `2003-01-01` onward - Start Date must be `>= 2003-01-01` or the reference dropdown
silently offers a different Business Unit instead (see Quirks).

## Automation (code in ec-automation)
- **Playwright:** `py/property_iud.py` (2026-08-02 build; shared engine `ec_object_iud.py` +
  explicit `select_dropdown` - PROVEN value. Left untouched by the 2026-08-26 RF-only Area-pattern
  conversion; the Universal Screen Engine is the owner-decided path forward for new Playwright
  work, not a hand-written driver refresh).
- **RF:** T3 `pageobjects/Configuration/Assets/Data_Mapping_Objects/property_page.resource`
  (label-driven, 2026-08-26 Area-pattern conversion, PR #559) + suite
  `tests/Configuration/Assets/Data_Mapping_Objects/property_iud.robot` (5 TCs: Clean State/
  Insert/Update/Find/Delete, per-TC login/logout, fixed test code `AUTOTEST_PROPERTY`).
- **Test data:** `testdata/property_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `PROPERTY_EC_USER`/`PROPERTY_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- **Reference-dropdown date trap (root cause of the 2026-08-02 build's original park + a false
  "shared-engine bug" chase):** the Business Unit Name dropdown only offers Business Units already
  effective as of the record's own Start Date. "Royalty Canada" (`ROYALTY_CA`) is only valid from
  `2003-01-01` onward. Using the plain default test date (`2000-01-01`) causes one of two failures
  depending on approach: leaving the field's navigator-inherited label untouched -> Save rejects
  with "Object not found"; explicitly re-selecting it -> the dropdown panel silently only offers
  Business Units that ARE valid at that date (e.g. SS1 BU/SS2 BU/TS5 BU), and the code falls back
  to the first one instead of the requested-but-absent option. **Fix: use Start Date >=
  2003-01-01** (this project's `EC_TEST_START_DATE_REFDD` constant in
  `resources/environment.py`) for ANY screen with a reference dropdown, not just the plain
  `TEST_START_DATE` (2000-01-01). See memory `feedback_child_object_date_must_follow_parent`.
- **Multi-group navigator, correctly classified as fitting Area's pattern (2026-08-26, PR #559):**
  Property's navigator superficially resembles the disqualifying "per-field navigator groups"
  shape (`docs/navigator-screens-not-matching-area.md`) because it spans two separate DOM groups
  (`G:0` Date, `G:1` Business Unit). Live recon confirmed `G:0`'s Date field already carries a
  non-empty default on load and needs no fill at all, so `G:1`'s Business Unit dropdown is the
  ONLY mandatory-and-empty nav field - structurally identical to Area's own single-dropdown
  navigator (just at a different group/column index). This is the SAME shape already proven on
  Tract (PR #555) - Property's own build applied that lesson proactively, without a
  wrong-then-corrected detour of its own.
- Insert/Update Business Unit Name (form field) MUST equal the nav Business Unit ("Royalty
  Canada") or the inserted row is invisible under the filtered navigator scope.
- DB self-clean checks against `OV_PROPERTY` use the `CODE` column; raw SQL UPDATE/DELETE against
  `OV_PROPERTY` is rejected (`ORA-20299`) - cleanup must go through the UI's own End=Start
  gesture.
- Test code is FIXED (`AUTOTEST_PROPERTY`, since PR #559) - NOT a per-run timestamp like the
  original 2026-08-02 build's `AUTOTEST_PROP<timestamp>`.
- See `workstreams/master-plan/ec-automation/screens/Configuration/Assets/Data_Mapping_Objects/
  Property/JOURNAL.md` for the full account, including this backfill's own clean (no-flake) live
  re-run (2026-08-28).
