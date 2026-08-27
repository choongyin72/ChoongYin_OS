# Screen: Tract

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel;
  Unit-Agreement-GATED. Navigator is TWO separate DOM groups (`nav:form:G:0` Date, `nav:form:G:1`
  Unit Agreement), but only `G:1` is mandatory-and-empty - see "Quirks" below for the
  wrong-then-corrected classification history.
- **BF_CODE:** RC.0056 - **Treeview:** Configuration > Assets > Royalty Objects > Tract
- **DB view:** `OV_TRACT` (generic `CODE` column, per `libraries/DbVerify.py`); base table `TRACT`; app `EC_REVN`.
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05, first attempt, no retry), fresh-connection DB self-clean 0 residual,
  `check_bundle_hygiene.py` PASS (backfill re-run of PR #555's Area-pattern conversion, merged
  2026-08-26).

## Selectors
| Purpose | Selector |
|---|---|
| Grid | `manageObject:form:T_data` (OV-GM, lazy redraw; empty until nav Unit Agreement + GO) |
| Navigator - Date (`G:0`) | `nav:form:G:0:R:1:C:0:da_input` - already carries a non-empty default on load, **needs NO fill** |
| Navigator - Unit Agreement (`G:1`, MANDATORY) | `nav:form:G:1:R:1:C:0:dd` - addressed at **column 0**, not column 1 (unlike Area/Well/etc.) - confirmed live via DOM scan, class included `{mandatory:true} MandatoryCellStyle` |
| Navigator GO | `button:form:B` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven - same documented rationale as Area/Bank's own End Date field) |

### Shared-keyword addressing (added for Tract, PR #555, 2026-08-26)
The T2 `Apply Navigator From Properties` keyword (`resources/manage_object.resource`) gained two
new OPTIONAL, backward-compatible arguments to reach Tract's navigator shape:
- `${group}` (default `0`) - which `nav:form:G:N` group to target. Tract passes `group=1`.
- `${start_col}` (default `1`) - which column within the group's row to start filling from.
  Tract passes `start_col=0` (its Unit Agreement dropdown sits at `C:0`, not the default `C:1`).

Called from `tract_page.resource`'s `Open Tract Screen With Navigator Values Populated`:
```robotframework
Apply Navigator From Properties    ${TRACT_NAVIGATOR_PROPERTIES}    group=1    start_col=0
```
Every other existing caller (Area, Well Hookup, Contract, Meter, etc.) omits both arguments and is
unaffected - defaults preserve the original single-row/`C:1..C:N` cascade behavior. Proven
backward-compatible via a full-tree dryrun (874/874 unchanged before/after) plus live 5/5
regression canaries on Area and Meter.

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Tract Code*** - **Tract Name*** - **Start Date*** (date) - **Unit Agreement*** (dropdown,
MANDATORY - must equal the nav Unit Agreement value or the inserted row never lists in the
filtered grid). Labels are SCREEN-PREFIXED ("Tract Code"/"Tract Name"), like Area's
"Area Code"/"Area Name" - NOT the generic "Code"/"Name" Bank/Object List use. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Tract Code` (ro, guard) - **`Tract Name`**. Delete: **`End Date`** = Start Date (zero-length
window) -> true delete, row leaves `OV_TRACT`.

## Navigator value (this environment)
Unit Agreement = **"Unit Agreement 1"** (has existing data; confirmed live) - driven by
`testdata/tract_navigator.properties` via the shared T2 `Apply Navigator From Properties`
keyword. **CRITICAL (owner field-reuse rule):** this exact value MUST also appear in
`testdata/tract_insert.properties`' "Unit Agreement" field - the inserted/updated Tract's Unit
Agreement must equal the navigator's own scope or the row is invisible under this OV-GM filter.
Unit Agreement parents (1-4) are all confirmed live effective `2010-01-01`
(`OV_UNIT_AGR.OBJECT_START_DATE`); the suite's Start Date `2011-01-01` is reused from the prior
driver and satisfies that constraint.

## Automation (code in ec-automation)
- **RF (the only test this screen has ever had - no Playwright bundle exists or is planned):** T3
  `pageobjects/Configuration/Assets/Royalty_Objects/tract_page.resource` (label-driven, 2026-08-26
  Area-pattern conversion, PR #555) + suite
  `tests/Configuration/Assets/Royalty_Objects/tract_iud.robot` (5 TC: Clean State / Insert /
  Update / Find / Delete, per-TC login/logout, fixed test code `AUTOTEST_TRACT`).
- **Test data:** `testdata/tract_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `TRACT_EC_USER`/`TRACT_EC_PASS` in `resources/credentials.py`.

## Quirks
- OV-GM Unit-Agreement-gated: grid empty until the nav Unit Agreement dropdown + GO completes.
- **Wrong-then-corrected classification (2026-08-26, PR #555's own first commit) - documented
  gotcha for future navigator-screen work:** Tract's navigator superficially resembles the
  disqualifying "per-field navigator groups" shape (`docs/navigator-screens-not-matching-area.md`)
  because it spans two separate DOM groups (`G:0` Date, `G:1` Unit Agreement). The build's first
  commit wrongly concluded on that basis that Tract did NOT fit the Area pattern and logged it as
  a disqualifying entry. The owner corrected this: a fresh live DOM recon showed `G:0`'s Date
  field already carries a non-empty default on load and needs no fill at all, so it was never a
  genuine second mandatory group - `G:1`'s Unit Agreement dropdown is the ONLY mandatory-and-empty
  nav field, making Tract structurally identical to Area's own single-dropdown navigator (just at
  a different group/column index). **Lesson: a multi-group navigator DOM shape is not itself
  disqualifying - check each group's live mandatory+empty state field-by-field before concluding
  "does not fit," per `feedback_verify_each_field_not_shape_match.md`.** The wrongly-added row was
  removed from `docs/navigator-screens-not-matching-area.md` with an explicit correction-log entry
  (kept there as a transparent record, not deleted).
- Insert Unit Agreement (form field) MUST equal the nav Unit Agreement ("Unit Agreement 1") or the
  inserted row is invisible under the filtered navigator scope - the owner's field-reuse rule,
  applied via identical values in the navigator and insert properties files.
- DB self-clean checks against `OV_TRACT` must use the generic `CODE` column.
- Test code is FIXED (`AUTOTEST_TRACT`, since PR #555) - NOT a per-run timestamp like the original
  2026-06-26 build's `AUTOTEST_TR_<run>`.
- See `workstreams/master-plan/ec-automation/screens/Configuration/Assets/Royalty_Objects/Tract/
  JOURNAL.md` for the full account, including this backfill's own clean (no-flake) live re-run.
