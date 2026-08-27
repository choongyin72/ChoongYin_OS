# Screen: Production Separator

- **Type:** OV-GM (EC Object Configuration, groupmodel manage-object, date-effective),
  navigator-GATED.
- **Treeview path:** Configuration > Assets > Facility_Objects > Production Separator (**CO.0042**)
- **DB view (ground truth):** `OV_PRODSEPARATOR` (versioned; key `CODE`; also `NAME`,
  `OBJECT_START_DATE`, `OBJECT_END_DATE`)
- **Last verified:** 2026-08-27 · EC **14.2.4** · local sandbox (`localhost:1521/ORCL`) · live RF
  5/5 (this backfill session)
- **Pattern:** RF suite STRUCTURE follows the Area-pattern 5-TC shape (PR #551, merged 2026-08-26,
  owner's 2026-08-26 standing rule: any navigator screen matching Area's layout gets Area's full
  pattern) while REMAINING OV-GM — this file only records what is Production-Separator-specific.

## Selectors `[from production_separator_page.resource Variables section, transcribed 2026-08-27]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `manageObject:form:T_data` |
| Navigator cascade (3-level, MANDATORY) | `nav:form:G:0:R:1:C:1:dd` (Production Unit) -> `C:2:dd` (Area) -> `C:3:dd` (Facility Class 1); no `C:4` |
| Navigator fill mechanism | Shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`), driven by `testdata/production_separator_navigator.properties` (explicit values: Op Production Unit=`AS1 EC Exploration Norway`, Op Area=`AS1_Area`, Op Facility Class 1=`AS1_Facility_01`) |
| Grid-filter | `Find/Clear Production Separator Row By Filter` → shared T2 `Find/Clear Object Row By Filter` on the grid's Code column |
| Insert/Update/Verify | Delegates to shared T2 `Insert/Update/Verify Object *` keywords, all called with `code_label=Production Separator Code` |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven — End Date label sits at `C:2`, Start Date at `C:1`, same row-packing rationale as Area's/Bank's own `${..._DEL_ENDDATE}`) |

## Mandatory / yellow fields
- **Navigator (before the grid loads any rows):** Production Unit -> Area -> Facility Class 1
  3-level cascade + GO — genuine OV-GM requirement, not removed by the Area-pattern conversion.
- **Insert form:** Production Separator Code, Production Separator Name, Start Date, Op Production
  Unit (all mandatory).
- **Update form:** Production Separator Name only (Production Separator Code is read-only in
  `updateAttributes`).
- Field labels are **screen-prefixed**: "Production Separator Code" / "Production Separator Name"
  (like Area's "Area Code"/"Area Name"), NOT the generic "Code"/"Name" that Bank/Object List use.

## Quirks
- **OV-GM grid stays empty until the navigator is filled + GO'd.**
- **Op Production Unit dropdown is date-effective-filtered by the form's OWN Start Date.**
  Requesting an EXACT value (even the correct alphabetically-first one resolved BEFORE Start Date
  is filled) reproducibly timed out live once Start Date=2000-01-01 was set — the post-Start-Date
  filtered list differs from the pre-filter list. Fix used (PR #551): the shared T2's `__FIRST__`
  literal (`Fill OV Dropdown By Label` / `Select First EC Dropdown Option`) instead of a fixed
  string — genuinely first-available-AFTER-filter. This is the SAME class of issue hit and fixed
  identically on **Chemical Tank** and **Chemical Injection Point** — check those screens' KB
  entries for the same pattern before assuming a fixed-value dropdown will work on any OV-GM screen
  with a date-effective reference field.
- Extra objectForm fields exist (Sort Order, Meter Frequency, Op Area/Op Facility Class 1, Cp
  Production Unit, Geo Area/Geo Field, etc.) but are NOT filled by the proven driver/suite — insert
  succeeds without them under this navigator scope.
- **Fixed test code `AUTOTEST_PSEP`** (not a generated/unique code) — every run must complete TC05
  so the code is free for the next run.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (the maintained suite):** T3
  `ec-automation/pageobjects/Configuration/Assets/Facility_Objects/production_separator_page.resource`
  (T2 `resources/manage_object.resource` + `libraries/PropertiesReader.py`) + suite
  `ec-automation/tests/Configuration/Assets/Facility_Objects/production_separator_iud.robot` (5
  TCs: Clean State/Insert/Update/Find/Delete, per-TC Login/Logout). Run:
  `EC_HEADLESS=true robot tests/Configuration/Assets/Facility_Objects/production_separator_iud.robot`
  → 5/5 PASS, self-clean 0 residual in `OV_PRODSEPARATOR`.
- **Playwright (pre-existing reference, waived from further build per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` — Universal Screen Engine replaces this role going forward):**
  `ec-automation/py/production_separator_iud.py` (shared engine `ec_object_iud.py` +
  `apply_ovgm_navigator`), kept unchanged since the 2026-07-30 build.
- Full bundle (SOW/README/JOURNAL/evidence/CHECKLIST):
  `ec-automation/screens/Configuration/Assets/Facility_Objects/Production_Separator/`.
