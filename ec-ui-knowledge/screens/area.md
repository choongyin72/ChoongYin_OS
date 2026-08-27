# Screen: Area

- **Type:** OV-GM (EC Object Configuration, groupmodel manage-object, date-effective) — the
  **role-model / reference pattern** for the whole OV-GM navigator-screen family (owner's 2026-08-26
  standing rule; see `docs/navigator-screens-not-matching-area.md` in `ec-automation`).
- **Treeview path:** Configuration > Assets > Basic Objects > Area (**CO.0003**)
- **DB view (ground truth):** `OV_AREA` (versioned; key `CODE`; also `NAME`, `OBJECT_START_DATE`,
  `OBJECT_END_DATE` — no `DESCRIPTION` column, confirmed live, unlike Bank)
- **Last verified:** 2026-08-27 · EC **14.2.4** · local sandbox (`localhost:1521/ORCL`) · live RF
  5/5 (this session, run 2 of 2 — see Quirks)
- **Pattern:** RF suite STRUCTURE follows the Bank-pattern 5-TC shape (owner-directed exception,
  2026-08-25, PRs #521/#523) while REMAINING OV-GM — this file only records what is Area-specific.

## Selectors `[from area_page.resource Variables section, transcribed 2026-08-27]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `manageObject:form:T_data` |
| Navigator dropdown (Production Unit, MANDATORY) | `nav:form:G:0:R:1:C:1:dd` — value = `Production Unit` |
| Navigator fill mechanism | Shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`), driven by `testdata/area_navigator.properties` |
| Grid-filter | `Find/Clear Area Row By Filter` → shared T2 `Find/Clear Object Row By Filter` on the grid's Code column |
| Insert/Update/Verify | Delegates to shared T2 `Insert/Update/Verify Object *` keywords, all called with `code_label=Area Code` |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven — End Date label sits at `C:2`, Start Date at `C:1`, same row-packing rationale as Bank's `${BANK_DEL_ENDDATE}`) |

## Mandatory / yellow fields
- **Navigator (before the grid loads any rows):** Production Unit dropdown + GO — genuine OV-GM
  requirement, not removed by the 2026-08-25/26 structural conversion.
- **Insert form:** Area Code, Area Name, Start Date (mandatory); Op Production Unit must equal the
  navigator's own PU value or the inserted row is invisible under the filtered grid scope.
- **Update form:** Area Name only (Area Code is read-only in `updateAttributes`; OV_AREA has no
  Description column).
- Field labels are **screen-prefixed**: "Area Code" / "Area Name" (like State's "State Code"), NOT
  the generic "Code"/"Name" that Bank/Object List use — confirmed live 2026-08-25.

## Quirks
- **OV-GM grid stays empty until the navigator is filled + GO'd** — this is Area's defining
  characteristic and the reason it's the OV-GM role model.
- **Form dropdowns are effective-date-filtered** — only objects valid at the form's own Start Date
  are offered (original 2026-06-11 recon: with Start Date 2000-01-01 the Op PU list excluded
  "Production Unit," which starts 2002-01-01 — test dates use 2003-01-01).
- **Versioned grid redraws lazily after Delete** — a TC05 grid-existence assertion can transiently
  read the deleted row as still present immediately after Save, even though the DB delete already
  succeeded. Reproduced live 2026-08-27 (this backfill's evidence-capture run 1: TC05 UI assertion
  failed while a fresh-connection DB read in the same window already showed 0 rows for
  `AUTOTEST_AREA` in `OV_AREA`); a second run passed clean 5/5. Documented as a known characteristic
  in the screen's own `area_sow.md` since the 2026-06-11 build ("one extra GO" after delete) — not a
  new defect. Always verify at the DB, not the grid alone, for this screen's delete.
- **Fixed test code `AUTOTEST_AREA`** (not a generated/unique code) — every run must complete TC05
  so the code is free for the next run.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (the maintained suite):** T3
  `ec-automation/pageobjects/Configuration/Assets/Basic_Objects/area_page.resource` (T2
  `resources/manage_object.resource` + `libraries/PropertiesReader.py`) + suite
  `ec-automation/tests/Configuration/Assets/Basic_Objects/area_iud.robot` (5 TCs: Clean
  State/Insert/Update/Find/Delete, per-TC Login/Logout). Run:
  `EC_HEADLESS=true robot tests/Configuration/Assets/Basic_Objects/area_iud.robot` → 5/5 PASS,
  self-clean 0 residual in `OV_AREA`.
- **Playwright (pre-existing reference, waived from further build per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` — Universal Screen Engine replaces this role going forward):**
  `ec-automation/screens/Configuration/Assets/Basic_Objects/Area/playwright/ec_iud_area.py`
  (`../_shared/iud_engine.py`), kept unchanged since the 2026-06-11 build.
- Full bundle (SOW/README/JOURNAL/evidence/CHECKLIST):
  `ec-automation/screens/Configuration/Assets/Basic_Objects/Area/`.
