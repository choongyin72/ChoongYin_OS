# SOW - Project Data Mapping Setup (Configuration > Assets > Data_Mapping_Objects)

- **Screen:** Project Data Mapping Setup   **BF:** SP.0039   **View:** `OV_COST_MAPPING`   **Base:** `COST_MAPPING`
- **Type:** OV, NONSTANDARD navigator (`StandardNavigator:form:G:0:R:<row>:C:<col>:dd/da_input`,
  real GO = `buttongo:form:B` - not the usual `nav:form:...` prefix), date-effective.
- Built via the Universal Screen Engine (`engine.py`), Phase 4 Pilot 3 (2026-08-14, packaged
  2026-08-16) - by far the deepest pilot: a genuine multi-level, cross-screen master-data
  dependency chain (Target Property -> Property screen, Target Project -> Project Properties
  screen, Reference -> Report Reference screen, scoped by matching Dataset) plus several real
  engine bugs found and fixed along the way (nonstandard nav/GO id scheme, duplicate-label
  shadowing, popup-vs-dropdown misclassification). Full narrative in
  `docs/universal_screen_engine_design.md`'s "Pilot 3" section - not duplicated here.
- **Mandatory Insert fields** (confirmed live via `Engine.field_inventory()`): Code, Name, Start
  Date, Data Entry Source, Dataset/Report, Mapping Type. Cross-field OR-mandatory rule (neither
  individually yellow): Target Property OR Target Project/Product Stream must be set - satisfied
  with Target Property = "Oil Sands Projects" (real, confirmed-existing option).
- **Date-effectivity gotcha (confirmed via DB, real lesson from this packaging pass):** popup-
  backed fields like Target Property and Reference only offer options whose OWN
  `OBJECT_START_DATE` is on/before the new row's Start Date. "Oil Sands Projects" is only valid
  from 2003-01-01; the Report Reference used ("Allowed Costs - Capital Test") only from
  2009-01-01. Start Date must be >= the LATER of any date-scoped dependency's own effective date,
  or the option silently won't appear (not a bug - the record genuinely doesn't exist yet at an
  earlier date).
- **Known defect + fix applied on Update:** the Reference field (`REPORT_REF_ID`) fails to
  auto-populate its displayed value on row-select even though the row's own value is intact -
  re-selecting the SAME already-correct value from the dropdown before Save restores it with zero
  data loss (root-caused in `docs/universal_screen_engine_design.md` section 24; demonstrated live
  and DB-verified in this pass). This driver applies the fix explicitly on Update.
- IUD: INSERT -> UPDATE(Name + Reference-fix) -> DELETE(End=Start). Test data `AUTOTEST_PDMS_007`;
  self-clean = absent in `OV_COST_MAPPING`.
- Deliverables: driver `py/project_data_mapping_setup_iud.py`, this SOW, `README.md`, `JOURNAL.md`,
  `playwright/ec_iud_project_data_mapping_setup.py` (delegator), `investigation/` (4 real recon
  scripts), `evidence/` (fresh 2026-08-16 run, `AUTOTEST_PDMS_007`).
