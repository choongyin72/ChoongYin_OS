# EC config tables/views glossary — time-scope + delete method + gotchas

A lookup so we stop re-deriving it. **Always confirm a class's `class_cnfg.TIME_SCOPE_CODE` before relying on a
delete method** — this table is what we've verified, not a substitute for checking.

`TIME_SCOPE_CODE`: **VERSIONED** = date-effective → delete by **End Date = Start Date** (removes from the `ov_*`
view). **INVARIANT** = not date-effective → End=Start does NOT remove it → use a real **DELETE** (via the OV
view's INSTEAD-OF-DELETE trigger, or base tables).

## ECIS interface config — all INVARIANT (verified 2026-06-21)
| Class / base table | OV/TV view | Delete method | Notes |
|---|---|---|---|
| `IMP_SOURCE_INTERFACE` | `OV_IMP_SOURCE_INTERFACE` | DELETE (INVARIANT) | the interface; filedrop files link by `INTERFACE_CODE` string |
| `IMP_SOURCE_MAPPING` | `OV_IMP_SOURCE_MAPPING` | DELETE | source mappings (KEY_LIST/DATA); `MAPPING_CODE`=code |
| `IMP_SOURCE_PATH` | `OV_IMP_SOURCE_PATH` | DELETE | path commands. ⚠️ **`IMP_SOURCE_MAPPING` = mapping CODE; `IMP_SOURCE_MAPPING_CODE` = mapping OBJECT_ID (GUID)** — filter on `IMP_SOURCE_MAPPING` |
| `IMP_TARGET_MAPPING` | `OV_IMP_TARGET_MAPPING` | DELETE | target (Class.Attribute, ec_key, class keys) |

## Scheduler config (verified 2026-06-21)
| Object | View / table | Notes |
|---|---|---|
| Schedule | `TV_SCHEDULE` (view) | `NAME`, `ENABLED`, `STATUS`, `SCHEDULE_TYPE`, `START_DATE`. Insert via this view; trigger auto-creates the detail rows |
| Schedule detail | `TV_JOB_SCHEDULE` (view over `JOB_SCHEDULE`) | **`START_DATE` = Valid From, `SCHEDULE_TYPE`, `SCHEDULE_WHEN_CLASS` are settable**; **`NEXT_FIRE_TIME` + `STATUS` are DERIVED** (app-computed; a view UPDATE won't stick; `WAITING` needs a QRTZ trigger created on app-save) |
| Schedule detail | `TV_SCHEDULE_DETAILS` / `_DETAILS_MORE` | username, log_level, retain_count, etc. |
| Action instance | `ACTION_INSTANCE` (base) / `TV_ACTION_INSTANCE` (view, deletable) | the `ECISAction` instance(s) per schedule; `business_action_no` of ECISAction = 8 |
| Instance param (jobid) | `ACTION_INSTANCE_VALUE` (base) | the `jobid` value. ⚠️ **`TV_ACTION_INSTANCE_PARAM` is a non-deletable join-view (`ORA-01752`/`ORA-01779`) — write/delete via base `ACTION_INSTANCE_VALUE`** |
| Job-action chain | `ACTION_JOB_CONFIG` (base) / `TV_ECIS_ACTION_JOB_PARAM` (view, deletable) | per `job_id`: AdvancedExcelJobAction(10) + StagingJobActionTarget(20), etc.; params FILE_DROP_SERVICE=DB, INTERFACE_CODE, FILE_FILTER |
| Quartz trigger | `QRTZ_JOB_DETAILS`, `QRTZ_TRIGGERS`, `QRTZ_SIMPLE_TRIGGERS` (ONCE), `QRTZ_CRON_TRIGGERS`, `QRTZ_BLOB_TRIGGERS`, `QRTZ_FIRED_TRIGGERS` | teardown must delete **all** sub-types child-first (else `FK_QRTZ_SIMPLE_TRIGGERS_1`) |
| History | `SCHEDULE_HISTORY`, `ACTION_INSTANCE_HISTORY`, `TV_ACTION_INSTANCE_HISTORY` | run log; `RUN_STATUS` (OK / Warning) |

## Filedrop (verified 2026-06-21)
| Table | Notes |
|---|---|
| `IMP_SOURCE_INTERFACE_FILE` | uploaded files; keyed by `INTERFACE_CODE` (string, no interface object_id FK); `FILE_CONTENT` BLOB; `RECORD_STATUS`; File Status → `WRITTEN_TO_EC` + `PARSED_DATE`/`WRITTEN_TO_EC_DATE` after a successful run |

## Master-data — VERSIONED (from memory `reference_ec_object_delete`; verify per class)
Bank, Company, Well, Facility, etc. → date-effective `ov_<object>` views; **delete by End Date = Start Date**
(zero-length window). Toolbar Delete is disabled for these; the date-equality method is the delete path.
