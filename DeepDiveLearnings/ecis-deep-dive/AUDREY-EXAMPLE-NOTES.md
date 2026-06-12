# AUDREY — the local working example (learning notes, 2026-06-12)

> ## 🏆 TASK COMPLETE (2026-06-12 ~14:55)
> **Built MY OWN interface (CLAUDE_WELL_TEST) + MY OWN schedule (CLAUDE_EXCEL_IMPORT)
> entirely through the EC screens and ran it end-to-end:** Excel (sheet Data:
> Well|Date|Pressure) → Upload Files → RUN NOW (single job chaining job actions
> 10 AdvancedExcel → 20 StagingTarget → 30 TargetMapping = flow option 2) →
> `dv_pwel_day_status` AVG_BH_PRESS = 151.5/152.7/153.9 on 2003-01-05, history OK,
> schedule restored to disabled. My one-schedule design is SIMPLER than the product's
> EXCEL_IMPORT_1+_2 two-schedule split and works.
> Schedules-screen build gotchas: grid params rows expose only the C1 value input
> (names are label cells — map via tr's first td text); new schedules DON'T appear in
> the default grid listing — find them via the Name column filter (sfilter0) after
> Active Status=All + GO; job-action param rows AUTO-GENERATE when the action row is
> created (just fill values). Scripts: build_claude_interface.py,
> build_claude_children.py, build_claude_schedule.py, set_claude_job_params.py,
> claude_e2e_run.py (all in tmp/scripts/).

Task (Choong-Yin): theory (3 ECpedia pages) → understand AUDREY on local EC → build MY OWN
simple Excel upload + schedule → upload file via Upload Files screen → run → DB-verify.
Habit cycle: blocker → stop → rethink → deeper dive → retry → retest.

## AUDREY = the EFK how-to example, live on the local sandbox

**Interface** (`IMP_SOURCE_INTERFACE`, OBJECT_CODE=AUDREY): EXCEL · INSERT_UPDATE · ROW ·
staging-validation N · EC_VALID_LEVEL P · EC_DATA_LEVEL P · OVERWRITE FULL.
(19 interfaces exist locally — COMPANY_IMPORT, TANK_OBJ_IMPORT, EXCEL_IMPORT… all same shape.)

**Source mappings** (origin all `Sheet1.A1`):
| code | type | value | EC_KEY | keys | paths (UL=UPPER_LEFT, LR=LOWER_RIGHT) |
|---|---|---|---|---|---|
| DATE | KEY_VALUE | DATE | — | — | UL Move(2,2) → C3 |
| WELL | KEY_LIST | STRING | — | — | UL FindVertical("ANNABEL"); UL Move(0,3); LR FindVertical("") |
| VALUE | DATA | NUMBER | ecValue | KEY_1=ROWS:WELL, KEY_2=DATE | UL FindVertical("ANNABEL"); UL Move(1,3); LR FindVertical("") |
| VALUE2 | DATA | NUMBER | ec2 | KEY_1=ROWS:WELL, KEY_2=DATE | UL FindVertical("ANNABEL"); UL Move(2,3); LR FindVertical("") |

**Target mappings**: ecValue → `PWEL_DAY_STATUS.AVG_BH_TEMP`; ec2 → `PWEL_DAY_STATUS.AVG_BH_PRESS`;
both CLASS_KEY_1=KEY_1 (well code), CLASS_KEY_2=KEY_2 (date). Class keys discoverable via
`ECDP_ADV_EXCEL_HELPER.getKey('PWEL_DAY_STATUS', n)` → OBJECT_CODE, DAYTIME.

**Schedule** `AudreyExcelImport` (TV_SCHEDULE_LIST schedule_no=5000, ENABLED=N, STATUS=EXPIRED):
- 2 action instances (TV_ACTION_INSTANCE), both Business Action **ECISAction**
  (`com.ec.frmw.is.dc.core.businessaction.ECISAction`):
  - exec 10 → BA param `jobid=AudreyJobID` (TV_ACTION_INSTANCE_PARAM)
  - exec 20 → BA param `jobid=AudreyReadFromStaging`
- `ACTION_JOB_CONFIG` rows per JOB_ID (job_action_no orders the chain):
  - **AudreyJobID**: 10 `AdvancedExcelJobAction` (FILE_DROP_SERVICE=**DB**, FILE_FILTER=*,
    INTERFACE_CODE=AUDREY, CONFIG_VALIDATION=Y, FTP_* empty) → 20 `StagingJobActionTarget`
  - **AudreyReadFromStaging**: 10 `StagingJobActionSource` (FILE_NAME=*, INTERFACE_CODE=AUDREY,
    CONFIG_VALIDATION=Y) → 20 `TargetMappingJobAction`
- So: instance 1 = file→staging, instance 2 = staging→EC (flow option 1 in ONE schedule).
- FILE_DROP_SERVICE=DB → files come from the **Upload Files** screen → `IMP_SOURCE_INTERFACE_FILE`
  (FILE_CONTENT blob; UPLOADED_INTO_EC_IND tracks state). No server filesystem needed.

## Screens (recon'd, screenshots in tmp/ecis_recon/)
- **Mapping Configuration**: 3 stacked inline grids — SOURCE INTERFACE
  (`imp_interface_table:form:T_data`), SOURCE MAPPING (`imp_source_mapping_table:form:T_data`,
  + tabs "Source Mapping Commands" / "Source Mapping Validation Rule" →
  `tab:tabPanel:imp_source_path_table:form:T_data`), TARGET MAPPING grid at bottom.
- **Schedules**: navigator `Active Status` dd (default Enabled — Audrey hidden! switch to All)
  + GO; grid `schedule:form:T_data`; **RUN NOW** button; tabs DETAILS (RUN AS/NOTIFY/HISTORY) /
  BUSINESS ACTION / SCHEDULE / EVENT SUBSCRIPTIONS / MONITOR.
- **Upload Files**: select Functional Area + Interface → choose file → Upload.
- Staging Area / Import History: treeview names differ — find later (search variants).

## 14.2.4 schema deltas vs old docs (gotchas)
- IMP_SOURCE_INTERFACE: code col = **OBJECT_CODE** (not INTERFACE_CODE); rows are
  date-effective objects (OBJECT_ID/START_DATE/END_DATE).
- IMP_SOURCE_MAPPING links via **IMP_SOURCE_INTERFACE_ID** (object id, not code).
- IMP_SOURCE_PATH links via **IMP_SOURCE_MAPPING_ID**.
- IMP_TARGET_MAPPING also has IMP_SOURCE_INTERFACE_ID (Audrey's rows have it NULL — global).
- IMP_STAGING still keyed by INTERFACE_CODE string.
- Schedule BA params live in **TV_ACTION_INSTANCE_PARAM** (jobid etc.), ACTION_JOB_CONFIG
  keyed by JOB_ID + JOB_ACTION_NO + PARAM_NAME.

## MY OWN build design (CLAUDE_WELL_TEST)
Sheet `Data`: A1="Date", B1=<date>; A4/B4/C4 headers "Well"/"Temperature"/"Pressure";
A5.. well codes (LOWER_RIGHT FindVertical("")), B5.. temps, C5.. pressures.
Mappings: DATE KEY_VALUE (UL Move(1,0) from Data.A1) · WELL KEY_LIST (UL FindVertical("Well"),
Move(0,1); LR FindVertical("")) · TEMP DATA NUMBER EC_KEY=claudeTemp (Move(1,1)) ·
PRESS DATA NUMBER EC_KEY=claudePress (Move(2,1)); keys KEY_1=ROWS:WELL, KEY_2=DATE.
Targets: claudeTemp→PWEL_DAY_STATUS.AVG_BH_TEMP, claudePress→AVG_BH_PRESS (KEY_1/KEY_2).
Schedule CLAUDE_EXCEL_IMPORT: ECISAction ×2 (jobid CLAUDE_JOB / CLAUDE_STAGE2EC) mirroring
Audrey's ACTION_JOB_CONFIG; FILE_DROP_SERVICE=DB; Upload via Upload Files; RUN NOW; verify
`dv_pwel_day_status` for the wells+date.
TODO before build: pick real well codes (query well table), pick a clean test date,
recon how the Schedules screen creates ACTION_JOB_CONFIG rows (BUSINESS ACTION tab on Audrey).

## Schedules screen recon RESULTS (2026-06-12 evening)
- Active Status dd (`nav:form:G:0:R:0:C:1:dd`) needs the BUTTON+panel-item gesture
  (typed text alone submits an unmatched value → empty grid); GO = `button:form:B`;
  RUN NOW = `runNowButton:form:B`. Grid `schedule:form:T_data` is an INLINE grid —
  row names are INPUT VALUES, not cell text. 90 schedules, paginated (20/page).
- **AudreyExcelImport does NOT appear in the screen even with Active Status=All**
  (date-expired out of the screen view) — use **EXCEL_IMPORT_1** instead: the product's
  own "ExcelFileUploadTest - Excel Import 1" example (FA: ECIS Interface Area), trio
  EXCEL_IMPORT_1 / _2 / _ERROR_1, paired with the EXCEL_IMPORT interface seen in
  Mapping Configuration.
- BUSINESS ACTION tab layout: BUSINESS ACTION grid (Action=ECISAction, Sequence#=10,
  Isolate Transaction cb) → PARAMETERS grid (jobid=EXCEL_IMPORT_1) → MACRO / FIXED
  PARAMETERS → **ECIS JOB ACTIONS section below (the ACTION_JOB_CONFIG editor — scroll
  down / screenshot next)**. Tabs: DETAILS / BUSINESS ACTION / SCHEDULE / EVENT
  SUBSCRIPTIONS / MONITOR (click tab text 'Business Action' etc., visible=true filter —
  hidden duplicates exist).
- Screenshots: tmp/ecis_recon/excel_import_sched_{details,business_action,schedule}.png

## EXCEL_IMPORT — the MINIMAL template (dumped 2026-06-12)
Interface EXCEL_IMPORT, Sheet1: header row 1, data row 2+: col A=wells, B=dates, C=temps.
Mappings (origin Sheet1.A1): WELL KEY_LIST STRING (UL Move(0,1); LR FindVertical(""));
DATE KEY_LIST DATE (UL Move(1,1); LR FindVertical("")); TEMPERATURE DATA NUMBER
EC_KEY=ecKeyTemp KEY_1=ROWS:WELL KEY_2=ROWS:DATE (UL Move(2,1); LR FindVertical("")).
Target: ecKeyTemp → PWEL_DAY_STATUS.AVG_BH_TEMP (CLASS_KEY_1=KEY_1, CLASS_KEY_2=KEY_2).
Job EXCEL_IMPORT_1 = action 10 AdvancedExcelJobAction (FILE_DROP_SERVICE=DB,
INTERFACE_CODE=EXCEL_IMPORT, FILE_FILTER=*, CONFIG_VALIDATION=Y) + 20 StagingJobActionTarget
— i.e. _1 only goes file→staging; check EXCEL_IMPORT_2's job config (expect
StagingJobActionSource + TargetMappingJobAction = staging→EC).
Wells available locally: AS1_Well_001..008 (table WELL, col OBJECT_CODE).

## ✅ END-TO-END PIPELINE PROVEN (2026-06-12 ~14:24, local sandbox)
My Excel (3 wells AS1_Well_001/2/3, date 2003-01-05, temps 41.5/42.7/43.9) ran the FULL chain:
Upload Files → EXCEL_IMPORT_1 (file→staging) → EXCEL_IMPORT_2 (staging→EC) →
`dv_pwel_day_status` shows exactly those values. History: ECISAction OK ×2.
Schedules restored to disabled afterwards (as found). Staging rows + file row remain
(EC's own retention handles them); AVG_BH_TEMP values left in place as evidence.

**The 4 hard-won gotchas (each cost one blocker→rethink cycle):**
1. **openpyxl xlsx = rejected as application/zip.** EC/Tika streaming detection needs
   `[Content_Types].xml` as the FIRST zip entry — openpyxl puts docProps first. Fix:
   rewrite the zip (tmp/scripts/fix_xlsx_order.py). MIME mappings themselves were fine.
2. **Upload Files order matters:** FA dd → Interface dd → **GO** → Select File → Upload File.
   Without GO first: "Missing values in required fields". File input id
   `upload_file_btn:form:fa_input`; Upload File button has NO id (click by text, visible=true).
3. **RUN NOW requires Enabled=Y** ("Schedule not enabled. Enable before you run schedule").
   DETAILS-tab Enabled cb = `tab:tabPanel:job_details_more:form:G:0:R:0:C:0:cb` + toolbar Save.
4. Schedules grid + Active Status dd gotchas (see screen recon section above).

Scripts (tmp/scripts/): ecis_make_and_upload.py (excel gen), fix_xlsx_order.py,
ecis_upload5.py (working upload), ecis_enable_and_run.py (enable+RUN NOW+verify),
ecis_disable_schedules.py (restore). Evidence: tmp/ecis_recon/*.png.

## ✅ OWN INTERFACE BUILT FROM SCRATCH VIA SCREENS (2026-06-12 evening)
**CLAUDE_WELL_TEST** fully configured through Mapping Configuration UI, DB-verified:
- Interface: EXCEL/INSERT_UPDATE/ROW/P/P/FULL, FA=ECIS Interface Area
- Mappings (origin Data.A1): WELL KEY_LIST STRING · DATE KEY_LIST DATE · PRESSURE DATA
  NUMBER EC_KEY=claudePress KEY_1=ROWS:WELL KEY_2=ROWS:DATE
- Commands per mapping: UL Move(x,1) [x=0/1/2] + LR FindVertical("")
- Target: claudePress → PWEL_DAY_STATUS.AVG_BH_PRESS (Key 1/Key 2)
- Excel shape: sheet 'Data', headers row1 (Well|Date|Pressure), data rows 2+.

**Mapping Configuration UI build gotchas (all conquered):**
- Insert menu items exist in BOTH Insert and Delete submenus → disambiguate with
  `contains(@onclick,"insert")`.
- Grid dd cells need the `_dd_button` + panel `tr[data-item-label]` click gesture
  (type+Tab does NOT commit) — labels are DISPLAY text: 'First Insert then Update',
  'Row based transactions', 'STRING/NUMBER/DATE', 'Move(col, row)', 'FindVertical(text)',
  'Key 1'/'Key 2' (not KEY_1).
- NEW command rows render Type/Path as dd cells; SAVED rows render as text inputs
  (blank-row detection must target C0_in sort cell).
- Save is async — poll the DB after clicking save (spinner lesson), don't trust the click.
- Scripts: build_claude_interface.py + build_claude_children.py (idempotent, DB-skip).

## Schedules screen build structure (probed)
Insert submenu: Schedule · Business Action · Macro · **ECIS Job Actions** · Trigger on · …
BA tab grids: `tab:tabPanel:busAction:form:T_data` (Action+Seq) ·
`tab:tabPanel:params:form:T_data` (jobid) · `tab:tabPanel:ecis_conf_action:form:T_data`
(job actions; EXCEL_IMPORT_1 has 2 rows) · `tab:tabPanel:ecis_params:form:T_data`
(per-action params; 12 rows). Toolbar hover menu must be dismissed by body click
(NOT Escape — it intercepts later clicks). Screenshots: ba_tab_full.png, schedule_tab_full.png.

## REMAINING (schedule + run):
1. Build CLAUDE_EXCEL_IMPORT schedule via Schedules screen: insert schedule row
   (recon Insert submenu there), Business Action tab: add ECISAction + param
   jobid=CLAUDE_JOB; ECIS JOB ACTIONS section: job actions 10 AdvancedExcelJobAction
   (INTERFACE_CODE=CLAUDE_WELL_TEST, FILE_DROP_SERVICE=DB, FILE_FILTER=*,
   CONFIG_VALIDATION=Y) → 20 StagingJobActionTarget → 30 TargetMappingJobAction
   (flow option 2, one job). SCHEDULE tab: type Once. Enable + Save.
2. New Excel: sheet 'Data', wells AS1_Well_001..003, date 2003-01-05, pressures
   151.5/152.7/153.9 (distinct from temps); fix zip order; upload via Upload Files
   (FA+Interface CLAUDE_WELL_TEST? name 'Claude Well Test' in dd; GO BEFORE file!).
3. RUN NOW → verify dv_pwel_day_status AVG_BH_PRESS + history; disable schedule after.
4. Then: business-domain deep dive (production/transport/sales/revenue) per user.

## NEXT STEPS (exact)
1. Scroll/expand the ECIS JOB ACTIONS section on EXCEL_IMPORT_1's Business Action tab —
   capture how job actions 10/20(/30) + params (DROP_FOLDER, FILE_DROP_SERVICE=DB,
   INTERFACE_CODE, FILE_FILTER) are edited. Also capture the SCHEDULE tab (schedule type ONCE).
2. Dump EXCEL_IMPORT interface mappings from DB (same query pattern as Audrey;
   tmp/scripts/audrey_config_dump2.py with EXCEL_IMPORT) — its Excel layout may be simpler
   AND its ACTION_JOB_CONFIG (job_id EXCEL_IMPORT_1) shows whether it uses DB file drop.
3. Pick wells: SELECT object_code FROM well WHERE ... (or ov_well) + clean date.
4. Build MY OWN config via the screens (CLAUDE_WELL_TEST + CLAUDE_EXCEL_IMPORT schedule),
   mirroring EXCEL_IMPORT_1; Excel file via openpyxl in tmp/; upload via Upload Files screen
   (FA + Interface + file); RUN NOW; verify dv_pwel_day_status (+ Scheduler History/MONITOR).
5. Habit cycle on any blocker: stop → rethink → deeper dive → retry → retest.
