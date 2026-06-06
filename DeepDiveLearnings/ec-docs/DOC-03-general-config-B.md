# DOC-03 — General Configuration B (System config & how-tos)
**Source:** EC 14.2.4 `frmw/general-config` (pages 26–50 of 50)
**Read:** 2026-06-06 · pages 1–18 in depth; 19–25 by title

> Mostly operational **config how-tos** + a few important system topics. Catalog below; 🔑 = cross-links to my work.

## 🔑 Database Users & Logging (explains who I connect as)
Each EC "operation" has its own Oracle users:
| User | Purpose |
|---|---|
| **`ECKERNEL_<op>`** | **Owner of all tables/triggers/views/PLSQL** — full access. *(This is `ECKERNEL_EC`, the user I run my DB verification queries as → full schema access, which is why I can read OV_BANK/OV_EQPM directly.)* |
| `ENERGYX_<op>` | the EC app's access point (granted I/U/D/execute on selected objects) |
| `REPORTING_<op>` | read-only for 3rd-party reporting (Ringfencing/row-level) |
| `TRANSFER_<op>` | data capture / **ECIS** staging-table writes |
| `KCKERNEL_<op>` | Keycloak tables |
| `YFKERNEL_/ANALYTICS_<op>` | Yellowfin install / connect |
Multiple independent operations can live in one Oracle SID.

## 🔑 Check Rules (validation framework) — ties to Issue_1052
- Validate DB data via a DB job; results in **`CTRL_CHECK_LOG`**; viewed in the **Validation tab** (the Status-Area tab from DOC-01) or screens **CO.0203 Validation Overview**, CO.0204 by Facility.
- A check rule = a SELECT with a **WHERE formula** that returns a row when validation *fails*. Keywords (AND/OR/IS NULL/IN/LIKE/NVL/DECODE/BETWEEN/CASE…), variables `${var}` (constant / RV-view attribute / function call / subquery).
- Function calls allowed from: classes with "Include in Validation"=Y, specific EC packages, `Z*` custom packages, or packages registered in EC code type `CHECK_RULE_PACKAGE`.
- Class Validation (CO.1031) / Object Validation (CO.1032/CO.0253) for simple min/max/missing checks.
- *(Relevant to Issue_1052 Check Group work + the Validation tab.)*

## 🔑 Time Zone & DAYTIME (explains the DAYTIME column)
- EC data model ≈ **2900 tables, ~1800 have a `DAYTIME` column.** DAYTIME (DATE) usually = a **Production Day**, not a timestamp (interpretation depends on the class TimeScopeCode).
- Sub-daily tables add **`SUMMER_TIME`** (DST overlap-hour disambiguation, part of PK) + replicated `PRODUCTION_DAY` for day-level aggregation; some add `END_DATE`.
- Multi-timezone support uses Oracle's TZ DB (auto DST); dual storage (local + UTC). `Ecdp_ProductionDay` deprecated → `Ecdp_Timestamp*` packages. *(DAYTIME = the column I saw in OV_EQPM.)*

## Scheduling / jobs
- **Calculation Library:** extract reusable calc steps into library calculations (shared globals/sets/iterators; can't self-call); reduces duplication, supports templates/regulatory packages.
- **Business Action → SQL:** `GenericScheduledSqlAction` (SQL in XML file, `$PARAM$` substitution) or `GenericRunSqlAction` (restricted post-EC-11.1-SP02 for security: declare `procedure.name/type/argN` params, no raw SQL).
- **Date Macro Parameter:** dynamic dates for schedules — `DATE_MACRO` param type + macros (Yesterday/Tomorrow/First of Month/Plus 1 Hour/Noon/Midnight…), based on Schedule Time vs Actual Time.
- **Blocked schedules:** false-blocks happen if DB drops mid-job; schedule **`ReleaseFalseBlockingJobs`** (set Ignore Misfires, not Stateful) to auto-unblock. Use the scheduler API, never update the DB directly.
- **Re-pin jobs:** Schedules screen "REPIN JOBS" button (hidden, grant by role) to move jobs to another server — never via DB.

## Screen/UI config how-tos
- **Tab Label override:** system setting `<screen url>/<tab screenlet id>/TabItemService/label`.
- **Context Menu:** right-click menu per screenlet (XML or DB config); items gated by access level / rows-selected / data content.
- **Dashboards:** widgets in `CTRL_DASHBOARD` + params in `CTRL_DASHBOARD_PARAM` (e.g. BigWidget with a QUERY renderer running SQL).
- **Title Bar:** customizable background (CSS, `${ENVIRONMENT}`/`${SCREEN_GROUP}` colour placeholders to visually distinguish instances), image, label — via Maintain System Settings.
- **Table Column Sets:** `viewcolsets` class-attribute property (comma-list) → radio buttons to show subsets of wide tables; "All" auto-added.
- **Language translation:** `T_BASIS_LANGUAGE` / `_SOURCE` / `_TARGET`; screens Language (CO.1023), Text Translation (CO.1024); per user/role via Regional Settings (CO.1008). English default.
- **PINC logging** (Product INtegrity Concept): `AP_` triggers log config changes during install/upgrade; toggle per table via `PINC_TRIGGER_IND` in `CTRL_OBJECT` + `ecdp_generate.generate(...,AP_TRIGGERS)`.

## Messaging (MHM)
- **Message Handling Module**: EC ↔ message broker via the **EC MHM adapter** (project-implemented; JDBC/web-services). EC pushes/pulls (firewalls block broker-initiated).
- **Send flow:** Actors (sender/receiver, in contact groups) → Distribution Lists (MHM.0001) → Message Definition (CO.0142, handling: manual/semi/auto) → Message Distribution → schedule with `MessagesSend` + `SendMail` business actions. Formats: Text/XML/EDI/Body Text. Free-text templates (CO.0144). *(This is the engine behind the morning-briefing email path.)*

## Navigator default values 🔑
Configured in Personal Settings (CO.1007) / Maintain User Settings (CO.1008). Group-model & nav-model navigators cache values across same-model screens (can disable cache). Lookup keys like `/com/ec/eccommon/genericmodel/navigator/defaultvalue/groupmodel/<Object class>` (e.g. WELL), and per-screen DATE defaults. *(Explains why the Equipment navigator pre-fills/remembers values; my automation set them explicitly.)*

## Pages 19–25 (by title)
How to send messages from EC (MHM send config) · **EC Dataloader** · **Data Purging** · Migration utility functions · **REC ID utility** · Pendo (in-app analytics). → revisit on demand.

---

## Cross-links
- `ECKERNEL_EC` = schema owner → my DB queries. `TRANSFER_<op>` = ECIS path (DOC-07 next-ish).
- Check Rules + Validation tab → Issue_1052 Check Group. `DAYTIME`/Production Day → OV_EQPM, data-grid screens.
- Messaging (MHM) → the morning-briefing automation. Navigator defaults → my cascading-navigator automation.
- Next: **DOC-04 Production** (prod module — deferment, allocation BPM, hydrocarbon accounting — high Woodside relevance).
