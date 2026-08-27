# Screen: Pipeline Segment

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel;
  Business-Unit-GATED (single-dropdown navigator, same shape as Area's own).
- **Treeview:** Configuration > Assets > Dispatching Objects > Pipeline Segment
- **DB view:** `OV_PIPELINE_SEGMENT` (generic `CODE` column, per `libraries/DbVerify.py` - NOT a
  screen-specific `PIPELINE_SEGMENT_CODE` column)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05, after one disclosed browser-context flake + passing retry),
  fresh-connection DB self-clean 0 residual, `check_bundle_hygiene.py` PASS (backfill re-run of PR
  #558's Area-pattern conversion, merged 2026-08-26)

## Selectors
| Purpose | Selector |
|---|---|
| Grid | `manageObject:form:T_data` (empty until nav BU + GO) |
| Navigator Business Unit (mandatory dd) | `nav:form:G:0:R:1:C:1:dd` -> GO (`button:form:B`) |
| Navigator Date (pre-filled, not empty-mandatory) | `nav:form:G:0:R:1:C:0:da_input` |
| Navigator "Pipeline" filter (dd, optional - `mandatory:false` confirmed live) | `nav:form:G:0:R:1:C:2:dd` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not
  label-driven - the row packs Start Date C:1 + End Date C:3 with the End Date label at C:2) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Pipeline Segment Code*** - **Pipeline Segment Name*** - Start Date* (date) - **Pipeline Name***
(dropdown, mandatory - no popup on this screen's insert form, so fill order is not load-bearing
the way it is on Meter's Delivery Point Name). Labels are SCREEN-PREFIXED ("Pipeline Segment
Code"/"Pipeline Segment Name"), like Area's "Area Code"/"Area Name" - NOT the generic
"Code"/"Name" Bank/Object List use. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Pipeline Segment Code` (editable `<input>` here, unlike Meter's read-only one - but the
conversion deliberately keeps the "only Name changes" scope every other converted screen uses) -
**`Pipeline Segment Name`** (the only field actually re-edited by TC03). Delete:
**`End Date`** = Start Date (zero-length window) -> true delete, row leaves `OV_PIPELINE_SEGMENT`.

### Grid columns (confirmed live, `manageObject:form:T_head` scan)
Pipeline Segment Code / Pipeline Segment Name / Start Date / End Date (4-column shape, same as
Area/Meter's own grid).

## Navigator values (this environment)
Business Unit = `TS5 BU` - driven by `testdata/pipeline_segment_navigator.properties` via the
shared T2 `Apply Navigator From Properties` keyword. Insert Pipeline Name dropdown = `TS5 Gas
Pipeline` (the SAME value the pre-existing 2026-06-12 driver already proved live and DB-verified
under the TS5 BU navigator scope - reused, not reinvented).

## Automation (code in ec-automation)
- **RF (maintained/live test):** T3
  `pageobjects/Configuration/Assets/Dispatching_Objects/pipeline_segment_page.resource`
  (label-driven, 2026-08-26 Area-pattern conversion, PR #558) + suite
  `tests/Configuration/Assets/Dispatching_Objects/pipeline_segment_iud.robot` (5 TC: Clean State /
  Insert / Update / Find / Delete, per-TC login/logout, fixed test code
  `AUTOTEST_PIPELINE_SEGMENT`).
- **Playwright:** none. This screen's original build (2026-06-12) was RF-only; no Playwright
  bundle exists and none is built for Area-pattern work (owner decision 2026-08-27, Universal
  Screen Engine replaces this role).
- **Test data:** `testdata/pipeline_segment_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `PIPELINE_SEGMENT_EC_USER`/`PIPELINE_SEGMENT_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- OV-GM Business-Unit-gated: grid empty until the nav Business Unit dropdown + GO completes.
- The navigator's second dropdown ("Pipeline", `C:2`) LOOKS like it might also be mandatory
  (same row as Business Unit) but is confirmed live `mandatory:false` - GO succeeds with only the
  Business Unit filled. Do not assume every dropdown on the navigator row is required.
- Pipeline Segment Code IS an editable `<input>` in `updateAttributes` (unlike Meter's read-only
  Code field) - but the conversion deliberately keeps the same "only Name changes" TC03 scope as
  every other converted screen, per the owner's structural-only conversion rule.
- **Shared-checkout git-plumbing incident (PR #558, disclosed at merge):** this session's shared
  repo checkout had its HEAD moved to a detached state by concurrent agents converting other
  screens (Contract Inventory/Property/Pilot) at the same time. PR #558's own commit was built via
  isolated git plumbing (`read-tree`/`hash-object`/`commit-tree` against the shared branch's fork
  point) specifically to avoid cross-contamination, landing a commit with ONLY the 12 Pipeline
  Segment files. See
  `screens/Configuration/Assets/Dispatching_Objects/Pipeline_Segment/JOURNAL.md` for the full
  account.
- DB self-clean checks against `OV_PIPELINE_SEGMENT` must use the generic `CODE` column, not a
  screen-specific `PIPELINE_SEGMENT_CODE` column.
- A shared-environment browser-context flake was hit once during this backfill's own live-run
  evidence capture (`Could not find active page` after `tasklist | grep -i chrome` showed 0
  processes) - not reproduced on immediate retry; treat a single such failure as environment
  contention, not a screen defect, before re-investigating the automation itself.
