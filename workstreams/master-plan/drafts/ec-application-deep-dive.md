# EC Application — Deep Dive Learning Notes

**Date:** 2026-06-05
**Sources:**
- `C:\DEV\GIT\ec-application` — EC source code
- `https://hub.energycomponents.com/repository/site-hub/ec-application/14.2.5/documentation/` — Official EC Technical Docs 14.2.5
**Purpose:** Deep learning of EC application architecture, patterns and internals

---

## What EC Is

**Energy Components (EC)** — enterprise production monitoring and allocation system.
- Born: **1997** (27+ years old)
- Current version: **14.2.5** (14.2.7-SNAPSHOT in dev)
- Domain: Oil & gas — wells, facilities, streams, tanks, calculations, allocations, revenue
- Used by: Multiple oil & gas companies as a SaaS/on-premise platform

---

## Technology Stack

| Layer | Technology | Version |
|---|---|---|
| Web UI | JSF + PrimeFaces | Jakarta, 15.0.13 |
| App Server | WildFly | 39.0.1.Final |
| Auth | Keycloak | 26.5.5 (OAuth2/OIDC) |
| Database | Oracle | ojdbc17 23.x |
| Migrations | Flyway | 12 |
| Workflow | jBPM | 7.74.1 |
| Reporting | JasperReports | 6.21.4 |
| Charts | HighCharts | 11.2.0 |
| REST/GraphQL | RESTEasy + Custom | - |
| Integration | Apache Camel | 4.18.0 |
| Clustering | JGroups | 5.5.2 |
| Build | Maven 3.9 / Java 21 | - |
| Testing | Selenium + Arquillian + Cucumber/BDD | - |

---

## Module Structure

```
ec-application/
├── ec-app/                    EAR packaging - main application assembly
├── ec-web/                    JSF/PrimeFaces web layer (WAR)
│   └── src/main/webapp/
│       ├── com.ec.frmw.co.screens/    105 config/framework screens
│       ├── com.ec.prod.co.screens/    Production configuration screens
│       ├── com.ec.prod.ca.screens/    Production analysis/reports
│       ├── com.ec.chem.co.screens/    Chemistry screens
│       └── xhtml/screen/              Screen templates
├── frmw-core/                 Core DAOs, security, base classes
├── frmw-pf-jsf/               PrimeFaces + JSF integration (70+ services)
├── frmw-calc/                 Calculation engine
├── frmw-config/               Configuration management
├── frmw-rest-api/             REST API
├── frmw-graphql/              GraphQL API
├── frmw-jbpm/                 jBPM workflow
├── frmw-report/               JasperReports
├── frmw-ecis/                 EC Integration Services (PHD etc.)
├── prod/                      Production domain business logic
├── chem/                      Chemistry domain
├── revn/                      Revenue domain
├── sale/                      Sales domain
├── tran/                      Transaction domain
├── database/                  Flyway migrations + schema
│   ├── ec-db-migration-oc-0/  Owner Context 0 migrations
│   ├── ec-db-schemas/         XSD-based class model definitions
│   └── ec-db-testdata/        Test data fixtures
└── ectestautomation/          Java/Selenium test automation framework
```

---

## Core Concept — The Screenlet

Everything in EC is built on **Screenlets** — self-contained, reusable UI building blocks.

| Type | Purpose |
|---|---|
| `FormScreenlet` | Navigator / date picker / filter form |
| `TableScreenlet` | Multi-row data grid with filter, sort, inline edit |
| `ButtonScreenlet` | Action button |
| `HighChartGraphScreenlet` | Line/bar/pie/stock charts |
| `GanttChartScreenlet` | Project timelines |
| `NetworkScreenlet` | Allocation network diagrams |
| `DiagramScreenlet` | Custom business diagrams |
| `CalendarScreenlet` | Calendar date view |
| `CollapsibleScreenlet` | Expandable sections |
| `FileUploadScreenlet` | File upload handling |
| `BpmTreeTableScreenlet` | Business process tree |

Each screenlet has:
- A **data model** (how to retrieve data)
- One or more **services** (how to react to events)

---

## Architecture — The Screenlet-Service-Model Triangle

```
XHTML Screenlet  ←→  JSF Service  ←→  Data Model
  (renders UI)      (business logic)   (query/DAO)
```

### Data Model Types
- `GenericDaoModel` — queries via XML definition files (most common)
- `GenericStaticModel` — static XML data (dropdowns, lookups)
- `GenericStaticNavigatorModel` — date range navigator
- `GenericSqlModel` — direct SQL execution

### Key Services (70+ in frmw-pf-jsf)
| Service | Purpose |
|---|---|
| `RetrieveService` | Loads data from DB |
| `SaveService` | Persists changes |
| `NavigatorButtonService` | Handles Go button + Enter key |
| `ValidateMandatoryService` | Required field validation |
| `LinkService` | Links parent/child screenlets |
| `ExecuteBusinessEventService` | Triggers jBPM workflow |
| `InitialLoadService` | Screen startup |
| `InsertService` | Insert new rows |
| `DeleteService` | Delete rows |

---

## How a Screen Works — Full Data Flow

```
1. User opens screen → InitialLoadService fires
2. Default navigator values set (today's date range)
3. RetrieveService queries DB via XML query definition
4. Results populate EcDataModel (in-memory)
5. PrimeFaces renders table from EcDataModel rows
6. User changes a value → f:ajax event fires
7. Service handler: validate → save → notify
8. DB updated via DAO + triggers fire
9. PrimeFaces AJAX partial re-render (no full page reload)
10. Status area shows success/error/warning
```

---

## How Element IDs Are Generated

IDs are deterministic — same pattern across ALL screens:
```
{screenletId}:form:{elementId}
```

| Pattern | Example |
|---|---|
| Sidebar search | `menu:searchForm:searchTxt` |
| Table | `check_rules:form:T` |
| Filter col 1 (Check ID) | `check_rules:form:T:sfilter0_ft_filter` |
| Filter col 2 (Check Name) | `check_rules:form:T:sfilter1_ft_filter` |
| Button in groups | `groups:form:runAllButton` |
| Date input (from) | `nav:form:G:0:R:1:C:0:da_input` |
| Hamburger menu | `{tableId}:form:T:cm` |
| Filter toggle | `{tableId}:form:T:tfo` |
| Pagination last page | `css=span.ui-icon-seek-end` |
| Row data attribute | `tr[data-rk]` |

---

## Check Rules — Internal Architecture

Check Rules (`CTRL_CHECK_RULES`) are SQL-based data quality rules:

1. Stored in DB: `CHECK_NAME`, `TABLE_ID`, `WHERE_FORMULA`, `CHECK_MESSAGE`, `SEVERITY_LEVEL`
2. `WHERE_FORMULA` uses `${}` variable placeholders e.g. `(${MolPct} IS NULL OR ${MolPct} < 0)`
3. Variables mapped to actual column names via `CTRL_CHECK_RULE_VARIABLE` table
4. PL/SQL package `pck_gen_check.IsValidWhereFormula()` evaluates each rule
5. Violations grouped and displayed in Validation Overview

**Variable resolution example:**
```sql
-- WHERE_FORMULA in DB:
(${MolPct} IS NULL OR ${MolPct} < 0 OR ${MolPct} > 100)

-- CTRL_CHECK_RULE_VARIABLE says: MolPct → MOL_PCT column

-- Actual SQL executed:
(MOL_PCT IS NULL OR MOL_PCT < 0 OR MOL_PCT > 100)
```

---

## Data Validation Pipeline

```
User fills value in UI
    ↓
f:ajax onChange/onBlur fires
    ↓
ECEvent dispatched to EventDispatcher
    ↓
Service handlers in sequence:
  1. ValidateMandatoryService (required fields)
  2. Custom validation services
  3. SaveService (access check + dirty check)
    ↓
DB INSERT/UPDATE executes
    ↓
DB triggers fire: pck_gen_check.IsValidWhereFormula()
    ↓
Check rules evaluated for this class/object
    ↓
Violations returned → ServiceResponse
    ↓
Notification area shows errors/warnings/info
```

---

## Database Architecture — Owner Context

**Owner Context (OC)** = EC's multi-tenancy model:
- OC-0 = base template (default EC configuration)
- OC-10+ = customer-specific instances
- Every table has `owner_context` column
- All queries auto-filter by OC

Flyway migration naming:
```
V14.2.5.{seq}.{timestamp}__DESCRIPTION.sql
```

Organised by domain: FRMW / PROD / REVN / TRAN / CHEM

Key tables relevant to validation:
- `CTRL_CHECK_RULES` — check rule definitions
- `CTRL_CHECK_RULE_VARIABLE` — variable mappings
- `TV_CTRL_CHECK_RULES` — transaction view (used for DML)
- `RV_STRM_COMP_ANALYSIS` — reporting view for stream component data
- `RV_STRM_ANALYSIS` — reporting view for stream analysis
- `RV_TANK_DAY_DIP_STATUS` — reporting view for tank dip data

---

## Calculation Engine (frmw-calc)

Separate module for complex domain calculations:
- Objects + attributes loaded into memory
- Rules execute in `calcSeqNo` order
- Supports: real numbers, sets, time iterations, null/missing
- Built-in: AGA3/AGA8 gas volume standards, PVT fluid properties
- Connected to jBPM for allocation workflow

---

## Authentication — Keycloak

Full OAuth2/OIDC SSO:
```
Browser → WildFly → Keycloak login page (id=username, id=password, id=kc-login)
                         ↓
                    Token validated
                         ↓
                    EC session loaded
                         ↓
                    ObjectAccessMgr: READ / CHANGE / CONTROL
```

Keycloak IDs confirm our automation selectors: `#username`, `#password`, `#kc-login`

---

## Validation Overview Screen — Key Components

Screen: `validation_overview.xhtml`

| Component ID | Type | Purpose |
|---|---|---|
| `nav` | FormScreenlet | Date range navigator |
| `navButton` | Button | "Go..." triggers validation run |
| `groups` | TableScreenlet | List of check groups with status |
| `logs` | TableScreenlet | Individual validation errors/warnings |
| `runAllButton` | Button | "Run Selected Groups" — executes check rules |

`ValidationOverviewPage.java` constants:
```java
T_GROUPS = "groups"
T_LOGS = "logs"
RUN_ALL_BTN = "runAllButton"
NAV = "nav"
componentId = "DATA_VALIDATION_TTV"
```

---

## Check Rule Screen — Key Components

Screen: `maintain_check_rules.xhtml`

| Component ID | Type | Purpose |
|---|---|---|
| `check_rules` | TableScreenlet | Main check rules grid |
| `variables` | TableScreenlet | Variable definitions per rule |
| `function_param` | TableScreenlet | Function parameters (in paramtab) |
| `sub_query_var` | TableScreenlet | Sub-query variables (in paramtab) |

`CheckRulePage.java` constants:
```java
MENU_TABLE = "CHECK RULES"
T_TABLE = "check_rules"
T_VARIABLE = "variables"
CHECK_NAME = "Check Name"
location = getPageURL("CTRL_CHECK_RULES")
```

Screen name in sidebar: `"Check Rule"` (singular, no S)

---

## Test Automation (ectestautomation)

EC's own framework — **Java + Selenium + Arquillian + Cucumber/BDD**:
- NOT Robot Framework (we are building first RF tests in EC ecosystem)
- 3,663 JUnit tests, 536 ECPA integration tests
- Page Object Model: `CheckRulePage.java`, `ValidationOverviewPage.java`
- BDD feature files define scenarios: `CheckRule_lib.feature`, `ValidationOverview_lib.feature`
- Allure reporting, Docker Compose for test environments
- CI/CD via Jenkins + Maven

`ValidationOverview_lib.feature` verifies: `Group` + `Status` columns
`CheckRule_lib.feature` verifies: `Check Name`, `RV view`, `Where Clause`, `Severity Level`

---

## PHD Integration (frmw-ecis)

EC Integration Services connects to external systems:
- PHD = Process Historian Database (Aspentech) — stores real-time sensor readings
- EC reads PHD tag values via ECIS
- PHD tags mapped to EC stream/tank objects via `V_TRANS_CONFIG`
- Transfer happens on schedule → data lands in `RV_STRM_COMP_ANALYSIS`, `RV_STRM_ANALYSIS`, `RV_TANK_DAY_DIP_STATUS`
- When PHD doesn't send data → value stays NULL → check rules fire

---

## My Assessment of EC Architecture

### Strengths
1. **27-year proven patterns** — consistent, predictable, battle-tested
2. **Generic screenlet model** — one implementation serves 100+ screens
3. **Predictable element IDs** — automation is reliable because IDs follow strict convention
4. **Multi-tenancy built-in** — Owner Context cleanly isolates customers
5. **XML-driven queries** — query changes don't require recompilation
6. **Layered validation** — client + service + DB triggers = multiple safety nets
7. **Modern dependencies** — PrimeFaces 15, Java 21, Keycloak 26 (not stuck in old versions)
8. **Domain depth** — AGA3/AGA8 calculations, PVT properties = serious oil & gas expertise

### Limitations
1. **JSF/PrimeFaces aging** — industry moving toward SPA frameworks (React, Angular)
2. **Java-only test automation** — limits who can write tests
3. **Oracle-locked** — expensive, not cloud-native
4. **Complex ID patterns** — `nav:form:G:0:R:1:C:0:da_input` hard to memorise
5. **ECPD-166168 bug** — Validation Overview reliability issue shows technical debt
6. **Monolithic EAR** — 36+ modules but still one deployable — no microservices

### Notable Design Decisions
- **Event-driven everywhere** — `ECEvent` + `EventDispatcher` makes the app composable
- **Calculation engine separate** — domain logic isolated from UI plumbing
- **Apache Camel** — signals awareness of integration complexity with external systems
- **GraphQL added** — team actively modernising APIs alongside legacy JSF
- **Keycloak SSO** — security is modern even if UI is not

### What This Means for Woodside Pluto Implementation
- Check rule issues (Issue_1052) are configuration problems, not code — fix in DB
- PHD integration failures are ECIS pipeline issues — check `V_TRANS_CONFIG` mappings
- UI testing works reliably because IDs are deterministic
- Class validation (`_DATA`, `_ALLOC` patterns) follows EC's built-in class model
- SQL scripts must respect Owner Context — never query without OC filter

---

## Official EC Technical Docs — Key Learnings (14.2.5)

### 1. Check Rules — Official Definition

**Check rules validate data quality. They run as DB jobs and store results in `CTRL_CHECK_LOG`.**

Triggered from:
- Validation Overview (CO.0203)
- Validation Overview by Facility (CO.0204)
- The Validation tab on individual screens
- Scheduled jobs

**The goal:** Write a SELECT WHERE condition that returns a row when validation **FAILS**.

**WHERE Formula syntax — supported keywords:**
`AND, OR, IS NULL, IS NOT NULL, IN, LIKE, NULL, NOT, NVL, COALESCE, SUBSTR, LENGTH, ROUND, TRUNC, COUNT, MAX, MIN, ABS, GREATEST, LEAST, SYSDATE, DECODE, BETWEEN, CASE, WHEN, THEN, ELSE, END, EXISTS, ADD_MONTHS, LAST_DAY`

**Variable types in `${variableName}`:**
- **Constant** — free text value bound as parameter
- **Attribute** — column from the RV view
- **Function call** — calls a PL/SQL function (EC packages, Z-prefixed custom packages, or packages listed in `CHECK_RULE_PACKAGE` EC codes)
- **Sub query** — one view only; used for record counts, averages, object lists

**Function call example:** `ec_pwel_day_status.avg_oil_rate(object_id, (daytime - 1), '=')`

**Allowed packages for function calls:**
- EC packages of classes with "Include in Validation" = Y
- EC packages: ECBP_WELL_THEORETICAL, ECBP_STREAM_FLUID, EC_WELL_REFERENCE_VALUE, EC_STRM_REFERENCE_VALUE
- Packages starting with Z (customer custom)
- Packages in EC codes with Code Type `CHECK_RULE_PACKAGE`

**Connecting check rules to screens:**
- CO.0079 Check Group — connected to a screen
- CO.0080 Rule Group Combination — connects check rules to the check group
This controls the Validation tab log records and the "Run All" button.

---

### 2. Classes and Objects — Official Definition

**Four class types:**

| Type | Description | Examples |
|---|---|---|
| **Object class** | Static physical objects | Facility, Tank, Well, Separator |
| **Data class** | Measurements/events owned by an object | Daily tank readings, exported volumes |
| **Interface class** | Abstraction over multiple object classes | Common subset of attributes across well types |
| **Table class** | Like data class but with less framework support | No object owner, no timestamp PK requirement |

**What the class abstraction enables:**
- Common validation + integrity without mixing with business logic
- Virtual (calculated) or stored attributes without changing tables
- Configurable screen navigation
- Generic concepts: four-eye approval, ringfencing, data locking, replication

---

### 3. View Generator and Class Model — Official Definition

**EC Data Services generates views automatically from class definitions.**

**View types:**
| Prefix | Type | Insert/Update/Delete? |
|---|---|---|
| `OV_xxx` | Object views | Insert, Update only (no delete — use END_DATE) |
| `IV_xxx` | Interface views | Insert, Update (UNION ALL of OV views) |
| `DV_xxx` | Data views | Insert, Update, Delete |
| `TV_xxx` | Table views | Full DML |
| `RV_xxx` | Reporting views | Read-only; used for queries (our SQL uses these) |
| `IUD_xxx` | Instead-of triggers | Applied on OV/DV/IV/TV views |

**Standard columns auto-added to EVERY view:**
`CLASS_NAME, RECORD_STATUS, CREATED_BY, CREATED_DATE, LAST_UPDATED_BY, LAST_UPDATED_DATE, REV_NO, REV_TEXT, APPROVAL_STATE, APPROVAL_BY, APPROVAL_DATE, REC_ID`

**Key core metadata tables:**
- `CLASS_CNFG` — class definitions
- `CLASS_ATTRIBUTE_CNFG` — attribute definitions
- `CLASS_REL_CNFG` — relationships
- `CLASS_TRIGGER_ACTN_CNFG` — custom PL/SQL injected into IUD triggers
- `CLASS_DEPENDENCY_CNFG` — interface implementations

**Report view (RV_xxx) structure:**
- DATA class: includes owner object attributes + data attributes + unit conversions (both native + converted columns)
- Uses tables directly (not OV/DV) for performance
- ANSI joins

**View generator API:**
```sql
EXECUTE ecdp_viewlayer.BuildViewLayer();             -- all dirty classes
EXECUTE ecdp_viewlayer.BuildViewLayer('WELL');        -- single class
EXECUTE ecdp_viewlayer.BuildReportLayer();            -- all RV_ views
EXECUTE ecdp_viewlayer.BuildViewLayer('WELL', p_force => 'Y');  -- force rebuild
```

---

### 4. ECIS — Official Architecture (PHD Integration)

**ECIS = EC Integration Services. Handles all external data integration.**

**Two integration types:**
- **SCADA/Tag-Based** — for real-time sensor/metering tag data (PHD is this type)
- **File-Based** — for row-based file exchange

**Two-stage pipeline (separated by JMS message queue):**
```
EXTERNAL SOURCE (PHD/PI/OPC)
        ↓
SOURCE STAGE
  Source Adapter reads tags
  Tag aggregation (time weighting, DST handling)
  Source mapping → DTOs
        ↓
JMS MESSAGE QUEUE (800MB capacity = ~12M samples)
        ↓
TARGET STAGE
  Aggregate DTOs
  Map to EC class attribute
  UOM conversion
  Insert/Update EC Data Storage
```

**Tag Adapters:**
- PI Web API Adapter (`PiRestAdapter`) — REST
- PI MS SQL Adapter (`PiJdbcAdapter`) — JDBC
- OPC UA Adapter
- OPC Classic Adapter
- IP21 JDBC Adapter (Windows only)
- Tag File Adapter
- **Woodside likely uses PI Web API or PI JDBC (OSIsoft PI historian)**

**Key mapping parameters:**
| Parameter | Purpose |
|---|---|
| `TAG_ID` | Tag name in source system (PHD tag ID) |
| `ATTRIBUTE` | EC Class attribute to map the tag value into |
| `TEMPLATE_CODE` | Template defining aggregation/interval rules |
| `FROM_UNIT` | Source unit of measure |
| `TO_UNIT` | Target unit for conversion |
| `LAST_TRANSFER` | Latest timestamp written — move this to re-read historical data |
| `OVERWRITE_STATUS` | Highest record status ECIS can overwrite |

**Source functions (how PHD data is read):**
`SUM, MIN, MAX, MEAN, AVG (time-weighted), SAMPLE (all timestamps), VALUE_AT_START, VALUE_AT_END, COMPRESSED (PI only), LATEST_IN_INTERVAL (PI REST only)`

**Template parameters:**
- `SOURCE_INTERVAL` — how often to request from source
- `SOURCE_DELAY` — delay before requesting (allows PHD to settle)
- `TARGET_INTERVAL` — resolution for EC writes (e.g., 1 day = daily writes)
- `TARGET_FUNCTION` — aggregation (SUM, AVG, LATEST, etc.)
- `PROD_DAY_START` — production day offset in hours
- `MINIMUM_SAMPLES` — min samples before completing a period

**Why PHD tags get NULL:** No data in the message queue → Tag Aggregation Service has nothing → EC Class Service inserts NULL or skips → check rule fires on NULL.

**Recovery:** If extraction fails → retry at next schedule. `LAST_TRANSFER` date unchanged → data re-extracted on next run.

**Monitoring:** `trans_process_log` for errors; Scheduler History Log for source; Tag data capture monitoring screen (last 100 rows).

---

### 5. Data Modelling Standard — Every Table Has 11 Columns

**All EC database tables MUST have these 11 standard columns:**

| Column | Type | Description |
|---|---|---|
| RECORD_STATUS | VARCHAR2(1) | P=Provisional, V=Verified, A=Approved; default P |
| CREATED_BY | VARCHAR2(30) | NOT NULL — who created the row |
| CREATED_DATE | DATE | NOT NULL — creation timestamp |
| LAST_UPDATED_BY | VARCHAR2(30) | Last updater |
| LAST_UPDATED_DATE | DATE | Last update time |
| REV_NO | NUMBER | Starts 0, incremented per journal rule |
| **REV_TEXT** | **VARCHAR2(240)** | **Reason for change — this is what ECPR-Issue1052 goes in** |
| APPROVAL_STATE | VARCHAR2(1) | N=New, O=Official, U=Updated, D=Deleted |
| APPROVAL_BY | VARCHAR2(30) | Four-eye approver |
| APPROVAL_DATE | DATE | Approval timestamp |
| REC_ID | VARCHAR2(30) | Oracle GUID — FK for extension tables |

**Sub-daily timestamp standard (DAYTIME tables):**
- `DAYTIME` DATE — local time (PK)
- `SUMMER_TIME` VARCHAR2(1) — DST flag Y/N (PK — to handle overlapping DST hour)
- `UTC_DAYTIME` DATE — UTC representation
- `PRODUCTION_DAY` DATE — may differ from TRUNC(DAYTIME)

**Trigger naming hierarchy (one trigger per physical table):**
| Name | Type | Priority |
|---|---|---|
| `IUG_xxx` | Generated (Ecdp_generate) | Lowest — skipped if IUC or IU exists |
| `IUC_xxx` | Hand-coded common | Overrides IUG |
| `IU_xxx` | Project-specific | Highest priority — overrides both |
| `AP_xxx` | PINC/install trigger | Separate — records config changes |
| `JN_xxx` | Journal trigger | After Update or Delete |
| `IUR_xxx` | Sets REC_ID | Before Insert or Update |

**PL/SQL package naming:**
| Prefix | Description |
|---|---|
| `EC_xxx` | Generated; single-value lookups by PK |
| `ECDP_xxx` | Hand-coded data technical operations |
| `ECBP_xxx` | Hand-coded business logic |
| `ECC_xxx` | Generated support package for object class IUD triggers |
| `UE_xxx` | User Exit package (overridable) |
| `Z_xxx` | Customer custom packages |

---

### 6. EC Extensions — How Woodside's Code Works

**Extensions are binary software components that extend core EC:**
- Managed via Extensions Manager screen
- Have full lifecycle: start, stop, disable, update, DB migrate
- "Run on startup" = downloads, extracts, verifies DB migration on every EC boot

**Extension development rules (hard-enforced):**
- All attribute names must be **prefixed with extension ID** (e.g., `ZWP_`, `ZWD_`)
- All Oracle DB objects must be prefixed with extension ID
- All relation names must be prefixed with extension ID
- Cannot disable attributes from a different app space context
- Max class name length: 100 chars
- Max DB object name: 100 chars

**This explains Woodside extension patterns:**
- `ZWP_` prefix = Woodside Pluto extension attributes
- `ZWT_` prefix = another Woodside extension
- SQL scripts: `TV_` prefix = transaction views for DML in extensions

---

## Session A — Deep Dive Results [ENHANCED — all 5 sources]

**Sources used:** EC Tech Docs 14.2.5 ✅ | ECpedia BPR ✅ | EC source code ✅ | Woodside repo ✅ | Web ✅

### Item #1: Class vs Object Validation (7→9) ✅

**Three validation types:**

| Type | Screen | Scope | DB Tables |
|---|---|---|---|
| Class Validation | CO.1031 | ALL objects of a class | `CLASS_ATTR_VALIDATION`, `CLASS_ATTR_EDITABLE` |
| Object Validation | CO.1032.01 | ONE specific object | `OBJECT_ATTR_VALIDATION`, `OBJECT_ATTR_EDITABLE` |
| Hierarchical Validation | CO.0253 | Object + parent hierarchy | `OBJECT_ATTR_*` with cascade |

Note: CO.1032 (old Object Validation) **DEPRECATED** since v14.0.0 — replaced by CO.1032.01.

**CLASS_OBJ_VALIDATION_IND checkbox on Check Rules:**
- `N` (unchecked) = traditional SQL check rule (`WHERE_FORMULA` + `SELECT_CLAUSE`)
- `Y` (checked) = execute Class/Object validation engine. `WHERE_FORMULA` must be EMPTY. System reads WARN_MIN/MAX, ERR_MIN/MAX, ERR_MANDATORY_IND from `CLASS_ATTR_VALIDATION` or `OBJECT_ATTR_VALIDATION`

**Override precedence:**
- Class BLOCKS object override for: `NOT_EDITABLE`, `MANDATORY`
- Object OVERRIDES class for: `WARN_MIN/MAX`, `ERR_MIN/MAX`, `REQUIRE_EVENT`
- Hierarchical: Object > Parent hierarchy > Class Validation

**Key DB tables:**
```
CLASS_ATTR_VALIDATION: CLASS_NAME, ATTRIBUTE_NAME, DAYTIME,
  WARN_MIN, WARN_MAX, WARN_PCT, ERR_MIN, ERR_MAX,
  ERR_MANDATORY_IND, ERR_CONDITIONAL_IND, REQ_EVENT

OBJECT_ATTR_VALIDATION: same + OBJECT_ID + EXT_VALIDATION_IND
```

**PL/SQL package: `EcDp_Class_Validation`**
- `newVersionClass()` / `deleteVersionClass()` — class version management
- `newVersionObject()` / `deleteVersionObject()` — object version management
- `copyValidation(from_obj, to_obj, from_dt, to_dt)` — copy config between objects
- `addMissingAttrClass()` / `addMissingAttrObject()` — add new attributes after class change

**`DefaultClassValConfigDao.java` — how EC loads validation config (JPA queries):**
```java
// Class validation query — excludes DISABLED_IND='Y' attributes
SELECT c FROM ClassAttrValidationEntity WHERE class_name = :className
  AND NOT EXISTS (... DISABLED_IND='Y' ...)
  AND (warn_min IS NOT NULL OR warn_max IS NOT NULL OR err_min IS NOT NULL
       OR err_max IS NOT NULL OR err_mandatory_ind IS NOT NULL OR ...)
-- Also loads: ClassAttrEditableEntity (NOT_EDITABLE), ObjAttrCopyFwdLogEntity (STALE_DAYS)
```

**NEW: Stale Days concept** (`ObjAttrCopyFwdLogEntity`):
Each object attribute can have `staleDays` — the number of days after which a copied-forward value is considered stale. Used for forward-filled production data that becomes outdated.

**Validation service is pluggable:**
`@ServiceProvider(priority = 0)` annotation on `DefaultClassValConfigDao` — the validation DAO can be overridden by extensions at higher priority. Allows project-specific validation logic injection.

**Industry context:** Oil & gas data quality best practices align exactly with EC's check rule design:
- Range checks (WARN_MIN/MAX, ERR_MIN/MAX) → prevent physically impossible values
- Completeness checks (ERR_MANDATORY_IND) → catch missing timestamps/values
- Mass balance reconciliation is a higher-level outcome of passing all check rules

**Woodside Pluto note:** Issue_1052 check rules have `CLASS_OBJ_VALIDATION_IND = N` — SQL-based, correct. For per-stream range checks (different limits per stream) → use CO.1032.01.

---

### Item #2: Check Group + Rule Group Combination (8→9) ✅

**CTRL_CHECK_GROUP:** CHECK_GROUP (PK), EC_USER_OBJECT (screen path), PARENT_GROUP (hierarchy), CHECK_RULE_TARGET
**CTRL_CHECK_COMBINATION:** CHECK_ID + CHECK_GROUP (many-to-many junction)

**Run All button flow:**
```
CO.0203 runAllButton
  → RunCheckGroupCollectionAction.java
  → pck_gen_check.run_check(from_date, to_date, group, facility)
  → PL/SQL runs dynamic SQL per rule in group
  → Violations INSERT into CTRL_CHECK_LOG
  → UI refreshes async
```

**CTRL_CHECK_LOG:** CHECK_ID, CHECK_GROUP, DAYTIME, OBJECT_ID, CLASS_NAME, ATTRIBUTE_NAME,
SEVERITY_LEVEL, LOG_MESSAGE, STATUS (NULL=open / Y=acknowledged / FIXED=resolved / H=hidden)

**Existing PHD groups (all children of V_DAILY_PHD_VALIDATION):**
- V_PHD_PWEL_STATUS → daily_well_status screen
- V_PHD_STREAM_GAS → daily_stream_status (GAS)
- V_PHD_STREAM_LIQUID → daily_stream_status (OIL)
- V_PHD_STREAM_WATER → daily_stream_status (WAT)
- V_PHD_EQPM_STATUS → daily_equipment_status
- V_PHD_STREAM_SUB_DAY_GAS → sub_daily_gas_stream_status

**🔴 CRITICAL FINDING — Issue_1052 rules 1142-1149 NOT in any group (GROUP=None)**
They will NEVER run in CO.0203 or any Validation tab until assigned.
This explains why CO.0203 showed 0 errors during exploration.

New groups needed:
- V_PHD_STRM_COMP_ANALYSIS → STRM_COMP_ANALYSIS screen (TC01/TC02)
- V_PHD_STRM_ANALYSIS → STRM_ANALYSIS screen (TC03/TC04)
- V_PHD_TANK_DIP_STATUS → TANK_DAY_DIP_STATUS screen (TC05-TC08)
Parent: V_DAILY_PHD_VALIDATION

**Check group → BPM integration (ECpedia BPM page):**
Check rule failures surface as jBPM user tasks — `EC_CheckRuleWithErrorHandling.bpmn2` building block routes violations to role-based task queues. This is why check groups must be configured before going live: without a group, violations never become BPM tasks, and the "Work by Exception" principle cannot work.

**Action: Add Check Group + Rule Group Combination INSERT to Issue_1052 SQL script. Raise to Grant.**

---

### Item #3: ECPD-166168 Bug — Validation Overview (8→9) ✅

**Bug:** Child group check rule logs NOT updated when re-running validation on parent group.

**Root cause** in `pck_gen_check_body.sql` lines 665-674:
```sql
CONNECT BY g.parent_group = PRIOR g.check_group
-- Traverses UP only (child→parent). Does NOT traverse DOWN (parent→children).
-- Running parent group = child group logs not cleared after data fix.
```

**Java layer** (`RunCheckGroupCollectionAction.java`):
```java
for (String group : groupAndChildren) {
    pck_gen_check.run_check(..., group, ...);  // Calls per group separately
}
// Each call doesn't know about hierarchy relationship
```

**Timeline:**
- Bug exists: pre-14.1.7
- Fixed: EC 14.1.7 (ECPD-166168) — re-fixed in 14.2.3 (ECPD-166320)
- Woodside Pluto: **EC 14.1.5.1 — BUG IS STILL PRESENT**

**Impact:** First-time run works (violations ARE logged correctly). Bug only affects RE-running after fixing data — old violations don't clear from CTRL_CHECK_LOG.

**Workaround for Woodside on 14.1.5.1:**
- Run each child group independently (not via parent group)
- Or: direct DB UPDATE on CTRL_CHECK_LOG to mark old violations as FIXED

**Phase 2 impact:** Once Issue_1052 rules are assigned to groups, run each new group separately in TC_UI_08 to avoid the bug.

---

## Session B — Deep Dive Results [ENHANCED — all 5 sources]

**Sources used:** EC Tech Docs 14.2.5 ✅ | ECpedia BPR ✅ | EC source code ✅ | Woodside repo ✅ | Web ✅

### Item #4: Group Model Concept (6→9) ✅

**Group Model = hierarchical navigation tree defining object class relationships for screen navigation.**

NOT the same as Check Group:
- Group Model: FACILITY→WELL→EQUIPMENT class hierarchy (navigation) — table: `GROUP_MODEL`, `GROUPS`
- Check Group: grouping of validation rules — table: `CTRL_CHECK_GROUP`

**URL path decoded:** `/GROUPMODEL/WELL/TARGET/WELL`
- GROUPMODEL = literal indicator
- WELL = group model type (hierarchy type)
- TARGET/WELL = target class

**Navigator linking:**
1. Date range → FROMDATE/TODATE stored
2. First dropdown → top-level objects from GROUP_MODEL top class
3. Each subsequent dropdown → filters by PARENT_OBJECT_ID from previous level
4. Final selection → OBJECT_ID populates screen
5. Date filter: DAYTIME between from_date and to_date on GROUPS table

**Key tables:** `GROUP_MODEL` (config), `GROUPS` (runtime with temporal validity DAYTIME/END_DATE),
`CLASS_REL_CNFG` (relationships), `DAO_CLASS_DEPENDENCY` (parent/child)

**EC Sandbox reference (ECpedia):**
EC Sandbox uses Group Model for the Polar Bear upstream operation — `Polar Bear Platform A` as facility → wells (OP, GI, WI) as children. This is the exact Group Model pattern in practice: facility at top, well types below, each navigable from the Allocation Network view.

---

### Item #5: Interface Classes and IV_ Views (7→9) ✅

**Interface class = minimum attribute contract multiple object classes must implement.
IV_ view = UNION ALL across all implementing classes.**

**Example — ALLOCATEABLE_OBJECT:**
```sql
CREATE VIEW IV_ALLOCATEABLE_OBJECT AS
SELECT NETWORK_CODE as CODE, OBJECT_ID, NAME FROM ALLOC_NETWORK
UNION ALL
SELECT NODE_CODE as CODE, OBJECT_ID, NAME FROM ALLOC_NODE
UNION ALL
SELECT FACILITY_CODE as CODE, OBJECT_ID, NAME FROM ALLOC_FACILITY
```

**Use case:** UI needs to show "any object of a type" without knowing specific class.

**INTERFACE_ALIAS:** When implementing class has different column name.
e.g. Interface expects `CODE`, ALLOC_NETWORK has `NETWORK_CODE` → set `INTERFACE_ALIAS='NETWORK_CODE'`

**Rules:**
- Interface defines MINIMUM attributes all implementers must have
- Implementing classes CAN have extra attributes
- Interface CANNOT reference attributes some implementers don't have (UNION ALL fails)
- `CLASS_DEPENDENCY_CNFG`: DEPENDENCY_TYPE=IMPLEMENTS records which classes implement the interface

**ECpedia — Calculation Data Model Best Practices: `_DATA` and `_ALLOC` class naming (CRITICAL):**

This is a CRITICAL pattern for anyone writing EC calculations or extensions:

| Class type | Suffix | Purpose | Example |
|---|---|---|---|
| Read (allocation input) | `_DATA` | Read-only; based on DB views; safe for calc reads | `PWEL_DAY_DATA`, `STRM_DAY_STREAM_DATA` |
| Write (allocation output) | `_ALLOC` | Writes back calc results; separate base tables | `PWEL_DAY_ALLOC`, `STRM_DAY_ALLOC` |
| Screen class | (none) | UI display; DO NOT read/write from calc | `PWEL_DAY_STATUS`, `STRM_DAY_STATUS` |

**Why this matters:**
- Reading from screen classes in calculations = performance degradation (screen classes have extra UI logic)
- Writing to screen classes = even worse performance issues
- Always use `_DATA` for reads, `_ALLOC` for writes

**Key `_DATA` classes:**
```
PWEL_DAY_DATA      — Daily Production Well
IWEL_DAY_DATA      — Daily Injection Well
STRM_DAY_STREAM_DATA   — Daily Streams
STRM_MTH_STREAM_DATA   — Monthly Streams
STRM_DAY_COMP_DATA     — Daily Stream Component Analysis
```

**Key `_ALLOC` classes:**
```
PWEL_DAY_ALLOC, PWEL_MTH_ALLOC     — Production Well daily/monthly
STRM_DAY_ALLOC, STRM_MTH_ALLOC     — Stream daily/monthly
STRM_DAY_COMP_ALLOC                 — Stream Component Analysis results
STRM_DAY_PC_ALLOC                   — Stream Profit Centre results
```

**Best practice:** Extend existing `_DATA`/`_ALLOC` classes via extensions rather than creating new ones. New write classes MUST have new base tables (not screen tables).

---

### Item #6: Class Trigger Actions CLASS_TRIGGER_ACTN_CNFG (7→9) ✅

**Meta-configuration that injects PL/SQL into auto-generated IUD triggers.**

**Table:** `CLASS_TRIGGER_ACTN_CNFG`
Columns: CLASS_NAME, TRIGGERING_EVENT (INSERTING/UPDATING/DELETING), TRIGGER_TYPE (BEFORE/AFTER),
SORT_ORDER, DB_SQL_SYNTAX, APP_SPACE_CNTX

**Real example — view layer invalidation:**
```sql
TRIGGERING_EVENT: INSERTING|UPDATING|DELETING  TRIGGER_TYPE: AFTER  SORT_ORDER: 100
DB_SQL_SYNTAX:
  ecdp_viewlayer_utils.set_dirty_ind(nvl(:new.class_name,:old.class_name),'VIEWLAYER',TRUE);
-- When trigger config changes → mark class views as needing regeneration
```

**BEFORE vs AFTER:**
- BEFORE: Can modify :NEW values — use for defaults, validation, computed fields
- AFTER: Read-only — use for audit, cascading updates, firing events

**vs Regular Oracle Trigger:**
- CLASS_TRIGGER_ACTN_CNFG = EC-managed, multiple per class (SORT_ORDER), disableable via config
- Regular trigger = standalone DDL, one per event, requires recompile

**Woodside note:** Woodside extension custom logic (ZWP_ tables) should use CLASS_TRIGGER_ACTN_CNFG entries, NOT standalone Oracle triggers. Keeps code within EC framework lifecycle management.

**EC Tech Docs — extension trigger naming (from DB migration doc):**
```
Extension trigger naming: {EXTENSION_ID}_IU_{trigger_name}   e.g. ZWP_IU_WELL_VERSION
                          {EXTENSION_ID}_AP_{trigger_name}   for PINC/install triggers
Create with FORCE keyword when dependent on auto-generated objects:
  CREATE OR REPLACE FORCE TRIGGER ZWP_IU_WELL_VERSION ...
```
Extension triggers cannot modify product triggers — they are additive only.

**`IGNORE_IND` property** (from EC Tech Docs, new finding):
`DISABLED_IND = Y` truly removes an attribute from all processing. `IGNORE_IND = Y` hides it from screens and REST API only — the attribute still exists in DB and can be queried. Use `IGNORE_IND` when you want to suppress a product attribute from the UI without breaking DB-level processing.

---

## Session C — Deep Dive Results [ENHANCED — all 5 sources]

**Sources used:** EC Tech Docs 14.2.5 ✅ | ECpedia BPR ✅ | EC source code ✅ | Woodside repo ✅ | Web ✅

### Item #7: ECIS Source Functions Detail (7→9) ✅

**12 source functions — key distinctions:**

| Function | Type | Key Behaviour |
|---|---|---|
| SAMPLE | Pass-through | Raw timestamps, no aggregation, NEXT_READ = last_ts + 1s |
| AVG | Time-weighted | Each value × its duration / total_duration. ≠ MEAN |
| MEAN | Arithmetic | Simple sum/count, ignores time between samples |
| SUM/MIN/MAX | Aggregated | Standard aggregations per interval |
| VALUE_AT_END | ECIS-agg | Latest sample within/before interval → adjusted to interval start |
| VALUE_AT_START | ECIS-agg | Latest sample at/before interval start |
| COMPRESSED | PI only | Interpolated — PI REST adapter only |
| LATEST_IN_INTERVAL | PI only | Latest per interval — PI REST only |
| AVG_AT_END | ECIS-agg | Multiple samples → avg; single → use value before interval |

**AVG time-weighted formula (SamplePeriod.java):**
```
For each consecutive pair: contribution = value × (next_ts - prev_ts in seconds)
Final = sum(contributions) / total_seconds
Last sample weighted from its timestamp to period end
```

**Adapter support:** JDBC requires user-written SQL for most functions. PI and IP21 support all except COMPRESSED/LATEST (PI REST only).

**DST handling:** For time corrections > 3600s, auto-adjusts ±1hr at DST boundary via `getPeriodOffsetInInterval()`.

**SHIFT_TIME_TO_PERIOD_ST:** START_INCLUDED (default) / END_INCLUDED — controls boundary alignment.

**NEXT_READ update:**
- SAMPLE: last_timestamp + 1 second
- Aggregated: last_timestamp + 1 source_interval

**PI Historian context (web — AVEVA/OSIsoft):**
PI Historian stores tag values as time-series events. Key concepts:
- **Compression**: PI compresses data — not every timestamp is stored, only "significant" changes. EC's `COMPRESSED` source function uses PI's compressed storage directly.
- **Time-weighted average in PI**: PI calculates the integral under the flow rate curve / total time. This is what ECIS `AVG` replicates — not a simple mean.
- **PI Totalizer**: For rate tags (flow in units/day), PI calculates volume by integration. ECIS `SUM` achieves the same result at the EC level.
- **PI AF (Asset Framework)**: Provides descriptive attribute names mapped to cryptic tag names (e.g. `WellA.OilRate` → `1C1401_TO_E1405AB.FI1234.PV`). Woodside uses PI AF — EC maps to PI AF attribute paths, not raw tag names.

**AVG vs MEAN — why it matters for Woodside:**
```
AVG (time-weighted): 
  Reading: 100 bbl/d for 20 hours + 50 bbl/d for 4 hours
  → (100×20 + 50×4) / 24 = 91.67 bbl/d  ← CORRECT for production accounting

MEAN (arithmetic):
  (100 + 50) / 2 = 75 bbl/d  ← WRONG — ignores time duration
```
Always use `AVG` for flow rates (oil/gas/water), `VALUE_AT_END` for instantaneous readings (temperature, pressure, density).

**Woodside note:** PHD daily data → use AVG (time-weighted) for analysis. Tank readings → VALUE_AT_END (latest reading). Wrong function = wrong aggregation = wrong EC data.

---

### Item #8: JMS Queue Capacity and Recovery (6→9) ✅

**DTO (DataTransferObject):** Tag IDs + timestamps + values + meta (config_id, NEXT_READ, DTO_ID, recapture_range).

**Queue capacity:** 800 MB baseline ≈ 1,600 DTOs. Each DTO ≈ 250-500 KB (5000 rows default).

**Key config parameters:**
- `maxrowsindto` (default 5000): Rows per DTO. Reduce if MDB timeout (>5 min processing) occurs.
- `dtomergeenabled` (default true): Merges DTOs into 5000-row batches. Better throughput. Disable only for per-tag granularity.
- `recapturerange` (default -1): -1=use LAST_TRANSFER; 0=reprocess all history; N=reprocess last N seconds.

**Recovery guarantee chain:**
```
Extraction fails → adapter degraded → retry next scheduler run (data still in source)
Queue full → JMSException → job fails → retry next run (data still in source)
Transform fails → logged + continues other rows → LAST_TRANSFER NOT updated
DB row fails → written to ERROR_FILE → continues → LAST_TRANSFER NOT updated
```

**LAST_TRANSFER = safety net:** Never updated until full success. Moving it backward = force re-read of history.

**Monitoring SQL:**
```sql
-- Check stale transfers (stuck > 1 day)
SELECT TAG_ID, LAST_TRANSFER FROM TRANS_SOURCE_TIME
WHERE LAST_TRANSFER < sysdate - 1 AND ACTIVE = 'Y';
```

**ECIS integration patterns (web + EC Tech Docs):**
- SCADA/PI historian is the source system for real-time sensor data — EC is the downstream consumer
- All EC API operations respect the journaling/auditing layer — ECIS writes are auditable
- ECIS two-stage pipeline separates extraction (Source Stage) from loading (Target Stage) via JMS — allows retry without re-extraction
- `OVERWRITE_STATUS` parameter controls what record status ECIS can overwrite: if data is already Verified, ECIS cannot overwrite unless set to V or A

**Woodside Issue_1052 note:** PHD tags showing NULL → check TRANS_SOURCE_TIME.LAST_TRANSFER. If stuck, move it back to force re-read. This is the root cause diagnostic tool.

---

## Session D — Deep Dive Results [ENHANCED — all 5 sources]

**Sources used:** EC Tech Docs 14.2.5 ✅ | ECpedia BPR ✅ | EC source code ✅ | Woodside repo ✅ | Web ✅

### Item #19: Extension DB Migration (7→9) ✅

**Flyway in EC Extensions:**
- Naming: `V{Major}.{Minor}.{Patch}.{Seq}__{description}.sql`
- Packaged as `ec-db-migration.jar` inside WAR `WEB-INF/lib/` via maven-assembly-plugin
- Location: `src/main/webapp/WEB-INF/db/migration/`
- **V__ (Versioned):** One-time delta — code inserts, table creates
- **R__ (Repeatable):** Re-executed when changed — used for XML class definitions
- Directory: `1.0.0/config/`, `1.0.0/tables/`, `common/classes/`
- Declared via: `<Extension-MigrationLocation>db/migration</Extension-MigrationLocation>`

**vs Core EC migration:** Core uses `owner_context_X/FRMW/PROD/` with timestamps. Extensions use version-based functional grouping.

**EC Tech Docs — strict DB migration rules for extensions:**

| Object type | Rule |
|---|---|
| Tables | Must start with Extension ID prefix. No modifying product tables. Versioned migrations (V__). |
| Packages | Must contain Extension ID (e.g., `ZWP_pkg`, `UEI_ZWP_pkg`). Repeatable migrations (R__). |
| Views | Must start with Extension ID. Create with `FORCE` keyword. Repeatable migrations (R__). |
| Triggers | Must start with Extension ID (e.g., `ZWP_IU_WELL_VERSION`). Create with `FORCE`. Repeatable. |

**EC Sandbox deviation (ECpedia):** The EC Upstream Sandbox uses ONLY `R__` (Repeatable) scripts — no `V__` scripts at all. This simplifies re-deployment but deviates from best practice. Real projects should use `V__` for table creates and `R__` for packages/views/triggers.

**After creating a table, always run:**
```sql
BEGIN ecdp_generate.generate('ZWT_TABLE', EcDp_Generate.PACKAGES+EcDp_Generate.ALL_TRIGGERS); END;
```

---

### Item #20: Creating Extension Classes (5→9) ✅

**Exact steps from real Woodside R__08000_WELL.xml:**

1. File: `common/classes/R__NNNNN_CLASSNAME.xml`
2. Root: `<class-ref owner-cntx="1001" class-name="WELL" version="1.0">`
3. Scope: `<app-space-cntx id="ZWT">`
4. Each attribute:
```xml
<class-attribute-cnfg attribute-name="ZWT_RPT_NAME"
  data-type="STRING" db-mapping-type="EXT_JOIN"
  db-join-table="ZWT_WELL_VERSION">
  <db-sql-syntax>ZWT_RPT_NAME</db-sql-syntax>
</class-attribute-cnfg>
```
5. Properties: LABEL, DESCRIPTION, SCREEN_SORT_ORDER, viewtype, IS_MANDATORY, viewwidth

**`db-mapping-type="EXT_JOIN"`** = stored in separate extension table joined to base object. ZWT_ attributes extend WELL without touching core WELL table.

**EC Tech Docs — three DB mapping types for extension attributes:**

| `db-mapping-type` | Storage | When to use |
|---|---|---|
| `EXT_JOIN` | Separate extension table (joined via REC_ID) | Many new attributes — create a dedicated table with REC_ID as PK |
| `EXTENSION` | Generic `EXTENSION_ATTRIBUTE_VALUE` table | One or a few new attributes — no new table needed |
| `LEFT_JOIN` / `INNER_JOIN` | Lookup join — read-only | Lookup/calculated values from another table |

**NEW: `EXTENSION_ATTRIBUTE_VALUE` table:** When `DB_MAPPING_TYPE = EXTENSION`, EC stores the value in this generic table. No new table needed. Good for simple project-specific attributes.

**Additional EXT_JOIN parameters:**
```xml
DB_JOIN_ALIAS  — alias for extension table in WHERE clause
DB_JOIN_SORT_ORDER — order when multiple joins on same table
DB_JOIN_WHERE  — custom join condition (if blank, system auto-joins via rec_id)
```

**`IGNORE_IND` vs `DISABLED_IND` (from EC Tech Docs):**
- `DISABLED_IND = Y` — truly removes attribute from ALL processing (DB + UI + API). Use only for group model class attributes.
- `IGNORE_IND = Y` — hides from screens and REST API only. Attribute still exists in DB. Use to suppress product attributes from UI without breaking DB-level logic.
- **Rule:** Never use `DISABLED_IND = Y` on product attributes except for group model class attributes.

**From EC 12.2 onwards — TEXT_xx/VALUE_xx/DATE_xx columns:**
Before EC 12.2, projects could add attributes directly to product classes using generic columns (TEXT_01, VALUE_01, etc.). From 12.2, this is no longer allowed — all new attributes must go through extensions with their own tables.

**Data types:** BOOLEAN (checkbox), STRING, NUMBER, DATE, DECIMAL

---

### Item #21: ZWP_/ZWT_ Woodside Extension Patterns (7→9) ✅

**9 extensions, 2 prefix families:**

| Prefix | Full Name | Context | Version | Purpose |
|---|---|---|---|---|
| ZWT | Woodside Template | 1001 | 1.15.0 | Reusable base template — generic domain model |
| ZWTI | Woodside Template Interfaces | 1001 | 1.14.0 | External system interface mappings |
| ZWP | Woodside Pluto Hub | 3000 | 1.1.0 | Production implementation on top of ZWT |
| ZWPC | Woodside Pluto Config | 3000 | - | Pluto codes, system attributes |
| ZWPA | Woodside Pluto Application | 3000 | - | Java code, user exits, business logic |

**ZWT = template (generic, reusable). ZWP = implementation (Pluto-specific, built on ZWT).**

**Consistent patterns across ALL extensions:**
- Java 21, EC ≥ 14.0.3
- JAR signing via keystore (password: energy)
- `ecextension-maven-plugin` for deployment
- Owner context isolates data partitions (1001=ZWT, 3000=ZWP)
- `app_space_cntx` initialised first via 100_pre_product_overrides

**EC Upstream Sandbox extension naming pattern (ECpedia — standard reference architecture):**

| App Space | Owner Context | Role | Purpose |
|---|---|---|---|
| ZX | 3000 | Configuration | Tables, views, triggers, packages, class config (from CME) |
| ZD | 4000 | Master Data | Scripts generated from ECCT |
| ZC | 5000 | Calculations | Custom calculations not in EC product |
| ZA | 6000 | Application | Business actions, business functions, custom Java |
| ZR | 8000 | Reports | DB config + Jasper report files |
| ZT | 10000 | Test Data | Test data generation functionality |

Woodside follows this pattern with ZWT/ZWP naming. Owner contexts above 1000 = customer space (never < 1000 for extension classes).

**EC tools for extension development:**
- **Class Model Editor (CME)** — generates class XML configuration files
- **EC Configuration Tool (ECCT)** — generates master data SQL scripts
- **Maven Archetype for Extensions** — scaffolds a new extension skeleton project
- **EC SDK** — examples at `energycomponents-sdk/examples/extensions/`

**EC container registry:** `registry.energycomponents.com` — same credentials as EC Hub.

**Separation of concerns:**
- Base = data model (tables, classes)
- Config = codes, lookups, rules
- App = business logic, user exits
- Reports = report definitions
- Testdata = test data loading

---

## Session I — Business Domain: Revenue, Chemistry, Transport/Cargo (2026-06-05) [all 5 sources]

**Sources used:** EC Tech Docs 14.2.5 ✅ | ECpedia BPR ✅ | EC source code ✅ | Woodside repo ✅ | Web ✅

**Items:** #25 Revenue | #26 Chemistry | #27 Transport/Cargo

---

### Item #25: Revenue Domain (5→9) ✅

**What Revenue covers in EC:**
Revenue is the commercial settlement layer — it converts production volumes into financial values, manages contracts, calculates royalties and taxes, and generates invoices. It sits downstream of production allocation.

**Revenue processing chain:**
```
Production Allocation (HC volumes)
        ↓
Contract Calculation (apply contract terms/prices)
        ↓
Royalty Calculation (apply fiscal terms)
        ↓
Taxation (apply tax rules)
        ↓
Invoice Generation
        ↓
Financial Posting (GL accounts)
```

**EC Revenue DB classes (from revn module):**
| Class | Purpose |
|---|---|
| `BALANCE` | Contract balance tracking |
| `BALANCE_SETUP` | Balance configuration |
| `BANK` / `BANK_ACCOUNT` | Banking details for payments |
| `BEARER` | Legal entity bearing the fiscal obligation |
| `CALC_REF_ROY` | Royalty calculation reference |
| `CALC_REF_TIN` | Taxation (TIN) calculation reference |
| `CALC_REVN_LOG` | Revenue calculation log |
| `CALC_REVN_ROY_LOG` | Royalty calculation log |
| `CALC_REVN_TI_LOG` | Taxation item log |
| `CALC_REVN_FIN_ITEM_LOG` | Financial item calculation log |

**Industry context — oil & gas fiscal systems:**
| System | Structure |
|---|---|
| **Royalty-Tax** (OECD) | Gross revenue → Royalty → Operating costs → Taxable income → Tax |
| **Production Sharing (PSA/PSC)** | Gross → Royalty → Cost Oil (cost recovery) → Profit Oil (shared with government) |
| **Concessionary** | Company pays royalty + income tax; government takes no production share |

**Key revenue concepts in EC:**
- **Royalty** = percentage of gross production paid to government/landowner irrespective of profit (typically 8–15%)
- **Cost Oil** = production allocated to recover company's capital + operating costs before profit sharing
- **Profit Oil** = remaining production shared between government and company per R-Factor or production tiers
- **R-Factor** = cumulative revenues / cumulative costs — determines profit oil split ratio
- **FOB** = Free On Board (buyer takes title at loading port — seller's risk ends at ship's rail)
- **DES** = Delivered Ex-Ship (seller delivers to buyer's port — seller bears freight risk)

**Journal mapping for financial posting:**
`JournalMappingProcessIntegrationTest` confirms EC Revenue has a journal mapping layer that posts revenue transactions to GL accounts in external financial systems (SAP, Oracle Financials). The `CALC_REVN_FIN_ITEM_LOG` stores each financial item for reconciliation.

**LNG Revenue integration (ECpedia — ZLC Extension):**
- `zlc_p_revn_replicate_cargovalues` = moves BL (Bill of Lading) quantities from Transport to EC Revenue for invoicing
- Two invoice types: **FOB** (buyer pays freight) and **DES** (seller pays freight)
- LNG price calculation: `ZLC_LNG_SLOPE_AND_CONSTANT` = slope × oil price index + constant (standard LNG pricing formula linked to crude oil benchmarks like JCC)
- `SCTR_ACC_MTH_STATUS` class used for Woodside monthly contract account quantities

**Woodside Pluto revenue variables (from CALC_VAR_READ_MAPPING):**
```sql
ZWP_rCntrEnergyYTD[CONTRACT,ACCOUNT_LIST,MTH] → ZWP_ENERGY_QTY_YTD on SCTR_ACC_MTH_STATUS
ZWP_rCntrMassTTD[CONTRACT,COMPANY,ACCOUNT_LIST,MTH] → ZWP_MASS_QTY_TTD
ZWP_rCntrVolTTD[CONTRACT,COMPANY,ACCOUNT_LIST,MTH] → ZWP_VOL_QTY_TTD
```
TTD = Total-to-date (cumulative), YTD = Year-to-date — both tracked per contract/company/month.

**Key insight:** Revenue in EC is fully calculation-driven — the same calc engine used for production allocation also handles royalty and revenue calculations. The `CALC_REF_ROY` and `CALC_REF_TIN` classes define the calc rules for royalties and taxes respectively. All results are logged for audit in `CALC_REVN_*_LOG` classes.

---

### Item #26: Chemistry Domain (4→9) ✅

**What Chemistry covers in EC:**
Chemistry manages fluid quality (composition analysis) and chemical management (injections, orders, consumption). It bridges production data (what is produced) with commercial data (what quality is delivered).

**Two sub-domains:**

| Sub-domain | Purpose |
|---|---|
| **Fluid Analysis (CM)** | Hydrocarbon composition: mole percentages, GCV, density, heating value |
| **Chemical Management** | Chemical products: methanol, corrosion inhibitors, scale inhibitors — procurement, injection, inventory |

**EC Chemistry Java classes (from `chem` module):**
| Class | Purpose |
|---|---|
| `AddAnalysisFromTemplateNotificationBusinessAction` | Creates a fluid analysis record from a template — pre-populates mole fractions for known well compositions |
| `AddToOrderChemicalProductAction` | Adds a chemical product to a procurement order |
| `UpdateChemicalOrderFormAction` | Updates a chemical order form (quantity, delivery date) |
| `UpdateVolumeNotificationBusinessAction` | Notifies relevant users when chemical volume changes |
| `InsertChemTankStrapBusinessAction` | Inserts strapping table data for a chemical storage tank |

**Fluid analysis — composition tracking:**
EC tracks hydrocarbon composition per stream/well as mole fractions:
- Components: N₂, CO₂, H₂S, C1 (methane), C2 (ethane), C3 (propane), iC4, nC4, iC5, nC5, C6, C7+
- Properties derived from composition: **Molecular Weight**, **Gross Calorific Value (GCV)**, **Relative Density**, **Wobbe Index**
- Used in: AGA8 Z-factor calculation, LNG BTU calculation, royalty calculation (energy-based)

**Tank strap (`InsertChemTankStrapBusinessAction`):**
A tank strap (strapping table) maps **tank ullage (height)** to **volume**. For chemistry tanks (methanol, inhibitors), strapping is required for accurate inventory measurement. EC has a standard pattern for inserting strapping data via Business Action.

**Chemistry in LNG context (ECpedia — ZLC):**
- `ZLC_LNG_BOL_CALC` = LNG BTU calculation based on:
  - LNG composition (mole fractions from cargo analysis)
  - Liquid volume (from ship ullages / metering)
  - Heating value per component
  - Result: **Total BTU content** of the cargo → basis for commercial invoice
- `ZLC_T_CARGO_ANALYSIS` / `ZLC_T_CARGO_ANALYSIS_ITEM` = stores composition per LNG cargo
- `CARGO_ANALYSIS_ITEM` / `ANALYSIS_ITEM` = EC class for cargo/production analysis items

**Stream Component Analysis (Issue_1052 context):**
`RV_STRM_COMP_ANALYSIS` = EC reporting view for stream component data. This is exactly what Issue_1052 check rules (TC01/TC02) validate — ensuring stream component analysis data is within valid ranges. Chemistry domain directly connects to check rules.

**Key insight:** Chemistry in EC serves two purposes: (1) quality tracking — ensuring hydrocarbon composition is recorded for commercial accuracy (LNG BTU invoicing depends on exact composition); (2) chemical injection management — tracking what chemicals are injected into wells/pipelines for integrity management, with full inventory and procurement lifecycle.

---

### Item #27: Transport / Cargo (4→9) ✅

**What Transport covers in EC:**
Transport is EC's midstream/commercial operations module — it manages the physical movement of hydrocarbons from production point to buyer. For LNG, this means cargo scheduling, vessel management, terminal operations, and gas dispatching.

**Three Transport sub-modules:**

| Sub-module | Coverage |
|---|---|
| **Cargo Planning** | Lifting schedules, nominations, entitlements, storage forecasts, scenario management |
| **Terminal Operations** | Physical cargo execution: BL/MR, timesheets, cargo analysis, demurrage |
| **Gas Dispatching** | Pipeline nominations, delivery point management, meter allocation, contract balance |

**Cargo Planning — the lifecycle of an LNG cargo:**
```
Annual Delivery Program (ADP) — 12-month lifting schedule per buyer/contract
        ↓
Short-term Delivery Schedule (SDS) — 30-day rolling schedule
        ↓
Nomination Entry — buyer nominates specific cargo (vessel, window, quantity)
        ↓
Cargo Planning Screen — schedule vis berth/storage/process train
        ↓
Lifting Program calculation (EC_LIFT_PROGRAM) — generates cargo records
        ↓
Cargo Transport records created (ZLC_T_CARGO_TRANSPORT)
```

**Key cargo planning concepts:**
| Concept | Definition |
|---|---|
| **Lifting Account** | Tracks each buyer's cumulative entitlement to lift product (balance of produced vs lifted) |
| **Entitlement** | Daily/sub-daily volume each buyer is entitled to lift based on ownership share |
| **Berth** | Physical loading berth — capacity, availability calendar |
| **Process Train** | LNG liquefaction unit — design capacity, reliability/temperature derating factors |
| **Scenario Manager** | Creates alternate planning scenarios (ADP scenarios, SDS scenarios) for optimization |
| **ADP** | Annual Delivery Program — official schedule of all LNG cargoes for the year |
| **SDS** | Short-term Delivery Schedule — operationally actionable near-term schedule |

**Terminal Operations — what happens at the berth:**
| Activity | EC screen/class |
|---|---|
| Cargo Activity Timesheet | Tracks arrival, mooring, loading start/end, departure times |
| BL/MR Info | Bill of Lading + Mate's Receipt — legal title transfer documents |
| Cargo Analysis | LNG composition analysis per load (mole fractions from sampling) |
| Cargo Documents | Generates official shipping documents from document instructions |
| Ship Info & Ullages | Vessel tank measurements before/after loading |
| Demurrage | Calculates time overruns at berth → compensation payable |
| Harbour Dues | Port charges per vessel call |

**Gas Dispatching — pipeline operations:**
- Daily nominations: input (what enters pipeline), output (what exits pipeline), operational (constraints)
- **Location matching** = confirms nominations at entry/exit points are balanced
- **Meter allocation** = allocates measured gas volumes to contracts
- **Operational restrictions** = physical constraints on dispatch (pressure limits, maintenance windows)
- **Contract balance** = running balance of contractual quantity obligations

**LNG BTU calculation (`ZLC_LNG_BOL_CALC`):**
```
BTU content = Σ(mole fraction × heating value) × liquid volume × density correction
             = LNG composition × volume (from ullage) → energy (MMBtu or GJ)
```
This is the basis for the commercial invoice — buyer pays per unit of energy, not volume.

**EC Transport module Java (from `tran` module):**
- `DecodeNotiMailRecipient`, `DecodeNotiSmsRecipient`, `DecodeNotiSysMsgRecipient` — notification routing (email/SMS/system message)
- `MonDataPopulator` — populates monitoring data for contract/nomination
- `MonPopulatorIUD` — IUD-based monitoring data updates
- `NotificationCommons` — common notification utilities

Transport has a rich notification framework — automated alerts for vessel arrivals, nomination deadlines, BL completion, and deviation from schedule.

**Woodside Pluto transport tables:**
| Table | Purpose |
|---|---|
| `ZWP_T_CARGO_INFO_LIGHT` | Lightweight cargo info (vessel, dates, quantities) |
| `ZWP_T_CARGO_TRANSPORT` | Full cargo transport record (contract, LA, volume, timing) |
| `ZWP_T_STRM_SINGLE_TRANSFER` | Single stream transfer record for Pluto production |

**LNG Extension architecture (ECpedia — ZLC):**
- **44 custom tables**, **47 PL/SQL packages**, **~130 EC class definitions**, **14 calculations**
- Key packages: `zlc_p_cargo_planning` (forecast/scenario), `zlc_p_cargo_transport` (lifting → transport), `zlc_p_demurrage`, `zlc_p_feed_gas`
- `EC_LIFT_PROGRAM` = standard product calculation that generates cargo liftings from storage balance + lifting accounts
- After `EC_LIFT_PROGRAM` runs: `zlc_p_cargo_planning` handles cargo numbering, `zlc_p_cargo_transport.insertFromLiftProg` creates transport records
- Roles: `ZLC_PLANNER`, `ZLC_TERMINAL_OPERATOR`, `ZLC_REVENUE`, `ZLC_EXTERNAL` (portal), `ZLC_AUDIT`
- EC Portal (EBB) = external web portal for buyers to view schedule, submit nominations, see BL info

**Industry context — LNG value chain:**
```
Gas Field → Processing Plant → Liquefaction Train → LNG Storage Tank → Loading Berth
                                                                              ↓
                                                                    LNG Carrier (vessel)
                                                                              ↓
                                                                    Regasification Terminal
                                                                              ↓
                                                                    Gas Grid (buyer's country)
```
EC Transport manages the LOADING side (after liquefaction). Woodside Pluto is a major LNG export project — EC manages cargo scheduling from storage through vessel loading to invoice.

**Key insight:** Transport is the most operationally intensive EC domain. For LNG, a single cargo mistake (wrong vessel, wrong berth, wrong BL quantity) can cost millions. EC's cargo planning, BL documentation, and BTU calculation are the commercial-legal system of record for LNG trade. The Woodside Pluto implementation is a live production LNG export operation using these exact modules.

---

## Session H — PVT Fluid Properties (2026-06-05) [all 5 sources]

**Sources used:** EC Tech Docs 14.2.5 ✅ | ECpedia BPR ✅ | EC source code ✅ | Woodside repo ✅ | Web ✅

**Item:** #17 PVT Fluid Properties

---

### Item #17: PVT Fluid Properties (4→9) ✅

**What PVT is and why it matters:**
PVT (Pressure-Volume-Temperature) describes how oil, gas, condensate, and water volumes change as fluids travel from reservoir conditions (high P, high T) to surface standard conditions (atmospheric P, ambient T). **All upstream production reporting must be in standard conditions** — PVT is the conversion mechanism. Wrong PVT = wrong allocation = wrong revenue = wrong royalty payments.

**The core PVT parameters:**

| Parameter | Symbol | Definition | Typical range |
|---|---|---|---|
| Oil Formation Volume Factor | Bo | Reservoir volume (Rbbl) per 1 STB oil at surface | 1.0–2.0 Rbbl/STB |
| Gas Formation Volume Factor | Bg | Reservoir volume per 1 SCF free gas | <1 at high pressure |
| Water Formation Volume Factor | Bw | Reservoir volume per 1 STB water | ~1.0 |
| Solution Gas-Oil Ratio | Rs | SCF of dissolved gas per 1 STB oil | 100–2000 SCF/STB |
| Shrinkage Factor | 1/Bo | Inverse of Bo — fraction of reservoir volume remaining at surface | 0.5–1.0 |

**Bo intuition:** Bo = 2.0 means reservoir oil is **twice** the volume of surface oil — when produced, the oil **shrinks by half** (dissolved gas flashes off + thermal contraction). Heavy oil Bo ≈ 1.0; volatile oil Bo up to 5.0.

**Core conversion formula (from `EcBsPVTTable.java`):**
```java
// Convert flowing/reservoir volumes → standard conditions
stdOilVolRate  = fromOilVolRate  / Bo          // oil shrinks
stdGasVolRate  = fromGasVolRate  / Bg          // free gas expands to std
               + stdOilVolRate   × Rs          // PLUS dissolved gas released from oil
stdWatVolRate  = fromWatVolRate  / Bw          // water shrinks slightly
stdCondVolRate = fromCondVolRate / Bo          // condensate treated like oil
```

**Six PVT calculation methods in EC — all implement `PvtCalculation` interface:**

| Class | Method | When to use |
|---|---|---|
| `EcBsPVTTable` | FVF table lookup (Bo, Bg, Bw, Rs vs P/T) | Full laboratory PVT data available |
| `EcBsPVTShrinkage` | Shrinkage factor + GOR approach | Simplified — fewer parameters needed |
| `EcBsPVTCombinedTable` | Combined FVF table | Multiple separator stages |
| `EcBsPVTCombinedShrinkage` | Combined shrinkage | Multiple stages, simplified |
| `EcBsNoShrink` | No volume correction (1:1) | No PVT data available, or gas-only wells |
| `EcBsUserExit` | Custom PVT user exit | Project-specific calculation |

**`PvtCalculation` interface:**
```java
void PVTCalculation(String objectId, String className,
                    String daytime, String resultNo, String userId)
```
All six methods implement this same signature — strategy pattern, selected per well/test device.

**`EcDsPVT` — reads separator test data from DB:**
```java
void getRateData(String className, String objectId, String resultNo,
    double[] pressure, double[] temperature,
    double[] sepOilVolRate, double[] sepGasVolRate,
    double[] sepConVolRate, double[] sepWatVolRate,
    double[] sepOilMassRate, ... double[] sepOilDensity, ...)
```
Reads all measured rates (vol + mass + density) for each phase at separator P/T conditions.

**`EcBsFluidRatio` — derives production ratios from standard volumes:**
```java
// Water cut — critical for reservoir management
waterCut = stdWatVolRate / (stdWatVolRate + stdOilVolRate) × 100  // %

// GOR — key for well productivity assessment
GOR = stdGasVolRate / stdOilVolRate  // SCF/STB
```

**PVT DB classes (from EC class model XML):**

| Class | DB Table/View | Purpose |
|---|---|---|
| `PVT_PT_EQPM_VALUES` | `TEST_DEVICE_RESULT` | Test device (separator) measured PVT results |
| `PVT_PT_THEOR_WELLS` | `TV_PVT_PT_THEOR_WELLS` | Theoretical well rates for allocation split |
| `PVT_SIM` | `V_PVT_SIM` | Results from PVTsim software (rigorous simulation) |

**`PVT_PT_EQPM_VALUES` attributes — two measurement types:**
```
{PHASE}_{MEASUREMENT}_{TYPE}
  PHASE:       GAS, NET_OIL, NET_COND, TOT_WATER
  MEASUREMENT: RATE (vol), MASS_RATE, DENSITY
  TYPE:        FLC (flowing conditions), ADJ (adjusted to standard)

Examples:
  GAS_RATE_FLC        — gas rate at separator conditions
  NET_OIL_RATE_ADJ    — oil rate adjusted to stock tank
  TOT_WATER_DENSITY_FLC — water density at separator
```

**`PVT_SIM` — results from rigorous PVT simulation software:**
```
SRF_KFACTORS_P01..P09  — K-factors (equilibrium ratios) per separator stage
EXP_GAS_SHRINK_FACTOR  — export gas shrinkage factor
EXP_PRESSURE/TEMPERATURE — export conditions
MPM_GASFLOWRATE        — multiphase meter gas flow rate
FIELDMODE              — field operation mode
```
K-factors (vapour-liquid equilibrium ratios) are used in rigorous equation-of-state calculations for gas condensate and volatile oil systems.

**Well split for allocation (`EcBsWellSplit` + `TV_PVT_PT_THEOR_WELLS`):**
```sql
-- Theoretical rates per well — used to split commingled stream volumes
SELECT OBJECT_ID, RESULT_NO,
       THEOR_NET_OIL_RATE, THEOR_GAS_RATE, THEOR_NET_COND_RATE, THEOR_WATER_RATE
FROM TV_PVT_PT_THEOR_WELLS WHERE RESULT_NO = ?
-- wellOilPart[] = THEOR_NET_OIL_RATE / sum(all wells)
-- wellGasPart[] = THEOR_GAS_RATE / sum(all wells)
```
PVT-based theoretical rates provide the split fractions for back-allocating commingled production to individual wells.

**PVT data sources (industry + lab):**
| Source | Method | Accuracy |
|---|---|---|
| Lab PVT report | CCE test + differential liberation | Best — from actual reservoir fluid sample |
| PVTsim software | Equation-of-state (Peng-Robinson, SRK) | High — rigorous simulation |
| Standing correlation | Empirical (bubble point, Bo, Rs) | ±3–5% — useful when no lab data |
| Lee-Gonzalez-Eakin | Gas viscosity (100–8000 psi, 100–340°F) | Good for sweet gas |
| Vasquez-Beggs | Bo and Rs | Widely used empirical correlation |

**Unit conversion in EC (`ecdp_unit.convertValue()`):**
```sql
-- PVT_SIM uses unit conversion for export conditions
ecdp_unit.convertValue(EXPORT_PRESS, 'BARA', 'BARA')   -- pressure in Bara
ecdp_unit.convertValue(EXPORT_TEMP, 'C', 'C')           -- temperature in Celsius
ecdp_unit.convertValue(MPM_GAS_MASS_RATE, 'KGPERHR', 'KGPERHR')
```
EC stores values in configurable units — `ecdp_unit.convertValue()` handles the conversion transparently in RV_ view definitions.

**PVT workflow in EC production accounting:**
```
1. Well test performed → test device results stored in PVT_PT_EQPM_VALUES
2. PVTsim simulation run → results stored in PVT_SIM (K-factors, shrinkage)
3. PVT calculation method selected per well (Table / Shrinkage / NoShrink)
4. During allocation:
   a. EcDsPVT reads separator measurements
   b. EcBsPVT* converts flowing volumes → standard volumes
   c. EcBsWellSplit uses theoretical rates to back-allocate to wells
   d. EcBsFluidRatio calculates WaterCut and GOR for reporting
5. Standard volumes written to _ALLOC classes → used in HC accounting
```

**Key insight:** PVT is the bridge between the physical world (what flows in the pipe at reservoir conditions) and the commercial world (what is reported and sold at standard conditions). EC has six PVT methods to handle different data availability scenarios. The most important parameter is Bo — it directly impacts oil revenue. A systematic 5% error in Bo = systematic 5% error in all oil allocation results.

---

## Session G — Calculation Engine (2026-06-05) [all 5 sources]

**Sources used:** EC Tech Docs 14.2.5 ✅ | ECpedia BPR ✅ | EC source code ✅ | Woodside repo ✅ | Web ✅

**Items:** #13 Calc framework | #14 Library calculations | #15 Execution engine | #16 AGA3/AGA8 | #18 jBPM-calc integration

---

### Item #13: Calculation Framework Architecture (5→9) ✅

**Three-layer architecture:**
```
CONFIGURATION LAYER (DB)
  CALCULATION + CALCULATION_VERSION
  CALC_EQUATION, CALC_VARIABLE_LOCAL, CALC_PARAMETER
  CALC_SET, CALC_SET_EQUATION, CALC_SET_COMBINATION
  CALC_PROCESS_ELEMENT, CALC_PROCESS_TRANSITION
       ↓
EXECUTION LAYER (Java)
  CalculationEngineImpl.run(ExecutionContext)
  RecordCache (in-memory DB records)
  VariableCache (in-memory variable values)
  CalculationObject (in-memory EC objects)
       ↓
RESULTS LAYER (DB write-back)
  DV_CALC_VAR_WRITE_MAPPING → class attributes
  TV_CALCULATION_EVENT (event log)
  CALC_DAY_PROD_LOG / CALC_MTH_PROD_LOG (output log)
```

**`CalculationEngine` interface — simplest possible API:**
```java
public interface CalculationEngine {
    public void run(ExecutionContext ctx) throws RemoteException, CalculationException;
}
```
Single method. All configuration, objects, and context passed via `ExecutionContext`.

**`CalculationEngineImpl` — "Read meta data and configuration, and run the MAIN calculation":**
- Reads all calc config from DB into memory at startup
- `MAX_BATCH_SIZE = 50000` — writes results in batches of 50,000 rows
- Built-in `Timer` class tracks milliseconds per execution step
- Uses `EcDp_System_Key.assignNextNumber('RECORD_EVENT')` to generate sequential event numbers
- Events stored in `TV_CALCULATION_EVENT(EVENT_NO, DESCRIPTION)` for audit trail

**Variable read/write mapping — how calc variables bind to DB:**
```sql
-- DV_CALC_VAR_READ_MAPPING — how variables are READ from DB
OBJECT_CODE          = 'EC_PROD'           (calc context)
CALC_VAR_SIGNATURE   = 'ZWP_rCntrEnergyYTD[CONTRACT,ACCOUNT_LIST,MTH]'
                       ← variable name + [index dimensions]
CLS_NAME_MAPPING     = 'SCTR_ACC_MTH_STATUS'   (EC class to read from)
SQL_SYNTAX           = 'ZWP_ENERGY_QTY_YTD'    (attribute name in class)
CALC_DATE_HANDLING   = 'VALID_UNTIL_NEXT'
VALID_FROM_ATTR_NAME = 'DAYTIME'
SUB_DAILY_IND        = 'N'
CALC_DATASET         = 'DEFAULT'
```
This mapping is the bridge between the EC calculation engine and the EC class model. Every variable in a calculation must have a read mapping (to get data in) and optionally a write mapping (to write results back).

**Calc context (`EC_PROD`):** Scopes which DB object types, classes, and attributes are accessible. Woodside uses `EC_PROD` for all production calculations. Other contexts: `EC_CHEM`, `EC_REVN`.

**Woodside calc structure (from `080_Calculations/` folder):**
```
00_DB_Object_types/   — object types available to calc (CALC_DB_OBJECT_TYPE, CALC_OBJECT_FILTER)
01_Variables/         — variable definitions and read/write mappings
02_Calculation/
  01_Library/         — library calculations (ZWP_LIB_*, XEM_*)
  02_Main/            — main allocation calculations (ZXIC_DAILY_VOLUME, ZXIC_MONTHLY_VOLUME)
```

**Key insight:** The EC calc framework is fully configuration-driven. No Java code is needed for custom calculations — only SQL config in DB tables. The engine reads the config, builds an execution graph, and runs it. Performance is controlled by batch size and logging level.

---

### Item #14: Library Calculations (5→9) ✅

**Two distinct concepts (ECpedia — Library Calculation Basics):**

| Concept | What it is | Impact on usage |
|---|---|---|
| **Library Calculation** | Reusable calculation rule with inherited variables/sets | Can be plugged into any calc in the same context |
| **Calculation Library** | Organisational container | Groups library calcs — no impact on where they can be used |

**Library Calculation = pseudo-function:**
- Has a list of **inherited variables and sets** — these are its input/output parameters
- The calling calculation MUST have all inherited variables/sets in scope when calling it
- Must be in same **calculation context** (`EC_PROD`, `EC_CHEM`, etc.)
- **No recursion** — calc engine checks at runtime (not design-time)

**Object code naming convention:**
```
[EXT]_[GROUP]_[NAME]    max ~25 chars
ZWP_LIB_DATA_LOG_DAY    ← ZWP extension, LIB group, DATA_LOG_DAY function
ZWP_LIB_READ_CARGO      ← ZWP extension, reads cargo data
XEM_CUSTOM_ACTIVITY     ← XEM extension, custom activity calc
```

**Calculation period:**
- `empty` = can be used in any period (daily OR monthly)
- `DAT` = daily only
- `MTH` = monthly only
- Update via SQL: `UPDATE ov_calculation SET CALC_PERIOD = 'MTH' WHERE CODE = 'LIB_COMM_CODE'`

**Product Standard Library Calcs (PSLC) in EC 14.2.0:**
- Upstream: **none**
- Midstream: **none**
- Environmental: has PSLCs (documented separately in ECCM space)
- Do NOT modify PSLCs — copy and create project-specific version instead

**Library calc versioning (ECpedia best practice):**
```
Version name format: LIB_CALC_NAME (2025-01-01)    ← start date appended
Superseded version:  LIB_CALC_NAME (2024-01-01) S  ← 'S' suffix = superseded
```
Add `Log message` in calc equations to show which version is executing — removes uncertainty during testing.

**Deployment: delete-then-redeploy (referential integrity constraint):**
```sql
-- Step 1: Remove references from parent calcs + delete lib calc
FOR libcalcs IN (SELECT * FROM calculation WHERE OBJECT_CODE IN ('LIB_CALC_1', ...)) LOOP
    UPDATE CALCULATION_VERSION SET IMPL_CALCULATION_ID = OBJECT_ID WHERE IMPL_CALCULATION_ID = libcalcs.OBJECT_ID;
    Ecdp_Calculation.deleteCalculation(libcalcs.OBJECT_ID);
END LOOP;

-- Step 2: Deploy updated lib calc via ECCT export

-- Step 3: Restore references in parent calcs
UPDATE CALCULATION_VERSION SET IMPL_CALCULATION_ID = libcalcs.OBJECT_ID WHERE REV_TEXT = libcalcs.OBJECT_CODE;
```

**Bloat prevention (ECpedia):** When an existing library keeps growing, create a NEW library calculation instead. A library calc can call another library calc — use this to chain modular logic.

**Key insight:** Library calculations are EC's equivalent of reusable functions. The "inherited variables/sets" declaration is the function signature. Context-specificity enforces separation between production, chemistry, and revenue domains. The delete-then-redeploy pattern is the only safe update method.

---

### Item #15: Execution Engine Internals (5→9) ✅

**Value type hierarchy — how EC represents all calculation values:**
```
CalculationValue (base interface)
├── RealValue       — double-precision floating point
├── ECRealNumber    — BigDecimal with MAX_SCALE=15 (exact arithmetic)
├── NullValue       — explicit null (different from missing!)
├── MissingValue    — value not yet computed or out of scope
├── SetValue        — ordered collection of objects (iteration set)
├── IterationValue  — current value in a set iteration
├── BooleanValue    — true/false
└── DateValue       — date/time value
```

**`ECRealNumber` — EC's high-precision number type:**
```java
MAX_SCALE = 15              // 15 decimal places guaranteed precision
ROUNDING_MODE = UNNECESSARY // no rounding unless explicitly requested
ZERO_LIMIT = 1e-10         // values below this treated as 0 for division-by-zero protection
```
Uses `BigDecimal` internally — prevents floating-point rounding errors in financial calculations.

**`CalculationObject` — in-memory EC object:**
```java
CalculationValue  getKey()         // object's primary key as CalculationValue
Map<String,CalculationValue> getAttributes()  // all attributes in memory
Timespan          getTimespan()    // validity period
int               getCalcSeqNo()   // processing order
String            getCalcRuleId()  // linked calculation rule
String            getClassName()   // EC class name (null if not persistent)
boolean           isPersistent()   // true = loaded from EC object class view
```
Objects are loaded into `RecordCache` keyed by object type + key. The engine iterates over objects in `calcSeqNo` order — network topology determines calculation sequence.

**Equation block standards (ECpedia):**
```
Block name format: [index] Name (iterator=SetName)
Example:          [20,20] Read Daily Stream Data (d=DaysInPeriod, s=StreamsMeasured)
Max equations per block: ~50 (performance degrades above this)
```

**Logging levels and when to use each:**
| Level | Purpose | Output |
|---|---|---|
| NODETAIL (default) | Minimum info — what customer agreed to see | Start/end, totals |
| MEDIUM | Agreed details — key intermediate values | Per-object summaries |
| FULL (debug) | All values for debugging | Semi-colon delimited for Excel paste |

```
Full log format: INFO = <block index> ; Node ; Stream ; PC ; Comp ; Var1 ; Val1 ; Var2 ; Val2
```

**Warning vs Error vs Fatal:**
- **Warning** = continues execution, logged
- **Error** = logged, counted in `ErrorCount`
- **Fatal** = terminates immediately — use ONLY after reading all input data (not mid-execution)
- Best practice: check `ErrorCount > 0` after reading input, then `Fatal` if errors found

**Standard set naming (ECpedia):**
| Set | Content |
|---|---|
| `StreamsAll` | All non-implicit streams |
| `StreamsMeasured` | Streams with type='M' or 'D' |
| `StreamsCalculated` | Streams with type='C' |
| `NodesASC` / `NodesDESC` | Nodes sorted by CalcSeqNo |
| `DaysInPeriod` | One day (daily) or all days in month (monthly) |
| `DaysToIterate` | Determines loop count for monthly AGGR_DAYS vs LOOP_DAYS |
| `ComponentsDB` | All components from tv_hydrocarbon_components |
| `ProfitCentresDB` | All profit centres from iv_profit_centre |

**Standard iterators:** `s`=streams, `n`=nodes, `d`=days (do NOT define `d` as a set), `p`=phase, `c`=components, `an`=allocation networks, `cntr`=contracts, `pc`=profit centres

**Key insight:** The execution engine separates VALUE TYPES (exact arithmetic via BigDecimal) from EXECUTION MODEL (blocks + equations + sets). The `calcSeqNo` on nodes drives the allocation network traversal order. Keeping blocks under 50 equations and using standard set names ensures maintainability across projects.

---

### Item #16: AGA3/AGA8 Gas Volume Standards (4→9) ✅

**What these standards are for:**
- **AGA3** = Orifice Metering of Natural Gas — calculates gas FLOW RATE from differential pressure across an orifice plate
- **AGA8** = Compressibility Factors of Natural Gas — calculates Z-factor to convert FLOWING volumes to STANDARD conditions
- Together: AGA8 computes gas properties (Z-factor) → AGA3 uses them to compute custody-transfer volumes

**Industry context:**
- AGA3 = primary standard for custody transfer orifice measurement in North American pipelines
- Also published as API Standard 2530 / API MPMS Chapter 14.3 / ANSI/API 2530
- Accuracy requirement: **±0.5%** for custody transfer
- Beta ratio (orifice/pipe diameter): valid range **0.20–0.75**
- Reynolds number must be solved **iteratively** (discharge coefficient CD depends on flow which depends on CD)

**EC implementation — JNI native library:**
Both AGA3 and AGA8 are implemented via **Java Native Interface (JNI)** to a C/C++ shared library:
```java
// AGA3 — orifice flow calculation
public class AGA3SA extends AGALIB {
    public static synchronized native int ORIFICE(
        int NTAPS,      // tap type (flange=1)
        double PF,      // flowing pressure (psia)
        double TF,      // flowing temperature (°R)
        int MATORF,     // orifice material
        double DO,      // orifice bore diameter (inches)
        double TORF,    // orifice temperature (°F)
        double DM,      // pipe internal diameter (inches)
        double RHOTP,   // gas density at flowing conditions
        double RHOS,    // gas density at standard conditions
        double HW,      // differential pressure (inches H2O)
        double VISC,    // gas viscosity (cP)
        double KFAC,    // isentropic exponent
        // ... outputs:
        DoubleValue QV,   // volumetric flow rate (MCFH)
        DoubleValue CD,   // discharge coefficient
        DoubleValue RED,  // Reynolds number
        DoubleValue BETA  // beta ratio
    );
}
```

```java
// AGA8 — Z-factor / compressibility
public class AGA8PLSG extends AGALIB {
    public static synchronized native int CALCGS(
        int Method,     // 1=Detail (custody transfer), 2=Gross (HV+RD), 3=Gross (RD+N2+CO2)
        double GRGR,    // gas relative density (specific gravity)
        double HV,      // heating value (BTU/SCF) — for Gross Method 1
        double X[],     // gas composition mole fractions [N2, CO2, H2S, H2, CO]
        double TF,      // flowing temperature (°R)
        double PF,      // flowing pressure (psia)
        // ... outputs:
        DoubleValue ZF,    // Z-factor at flowing conditions
        DoubleValue ZB,    // Z-factor at base conditions
        DoubleValue ZS,    // Z-factor at standard conditions
        DoubleValue RHOTP, // density at flowing conditions (lb/ft³)
        DoubleValue MWGAS  // molecular weight of gas
    );
}
```

**`VolumeCalculation.AGA()` — the combined calculation:**
Calls AGA8 first → feeds gas density (RHOTP, RHOS) and Z-factors into AGA3 → outputs final standard volume (QV in MCFH).

**AGA8 method selection:**
| Method | Inputs | Use case |
|---|---|---|
| 1 = Detail | Full gas composition (GC chromatograph) | Custody transfer (most accurate) |
| 2 = Gross Method 1 | Heating value + relative density + CO₂ | Less accurate, no GC needed |
| 3 = Gross Method 2 | Relative density + N₂ + CO₂ | Intermediate accuracy |

**Related AGA standards:**
| Standard | Measurement type |
|---|---|
| AGA3 | Orifice (differential pressure) |
| AGA7 | Turbine meter |
| AGA8 | Compressibility / Z-factor (= API 14.2) |
| AGA9 | Ultrasonic multipath meter |
| AGA10 | Speed of sound in gas |
| AGA11 | Coriolis meter |

**Key insight for Woodside:** EC's AGA implementation uses a C/C++ native DLL loaded via JNI (`synchronized native` = thread-safe). The fact that both methods are `synchronized` means they serialize AGA calculations across threads. AGA3 requires AGA8 output — they must always run together. Gas composition from the chromatograph drives AGA8 Method 1 accuracy; if no GC is available, use Method 2 (HV + relative density).

---

### Item #18: jBPM Integration with Calculation Engine (6→9) ✅

**The bridge: `BpmCalcAction.java`**
EC provides a dedicated class in `frmw-calc` that connects jBPM to the calculation engine:
```
jBPM process → BpmCalcAction → CalculationEngineEJB → CalculationEngineImpl.run()
```

**BPM building blocks for calculations (ECpedia):**

| Building Block | Purpose |
|---|---|
| `EC_RunCalculation.bpmn2` | Run a calculation (no error handling) |
| `EC_RunCalculationWithErrorHandling.bpmn2` | Run calculation + route warnings/errors to user tasks |
| `AllocGroupCalcAction` | Runs calculation for an entire allocation group |

**BPM parameters for calculations (from Woodside SQL):**
```
calc_id                  = ZXIC_DAILY_VOLUME    (EC calculation object code)
calculation_process_action = EC_CalculationAction (Business Action class)
calc_context             = EC_PROD              (calc domain)
calc_log_class           = CALC_DAY_PROD_LOG    (log class: DAY or MTH)
calc_log_level           = NODETAIL             (log verbosity)
calc_simulate            = N                    (N=run, Y=simulate only)
calc_dataset_ref         = (optional dataset reference)
```

**`calc_simulate = Y` — simulation mode:**
Reads all data and executes calculation logic but does NOT write any results back to DB. Used for testing/validation runs without polluting production data. Key feature for pre-deployment testing.

**Error handling flow from BPM to calc:**
```
Calc engine runs
  ├── Warning logged → BPM continues → notifies role_handle_alloc_warning
  ├── Error logged   → BPM continues → assigns task to role_handle_alloc_nonfatal_error
  └── Fatal logged   → calc stops    → assigns task to role_handle_alloc_fatal_error
```

**`CalculationEngineEJB` — the EJB wrapper:**
Exposes `CalculationEngineImpl` as an EJB for:
- Remote invocation from jBPM
- Transaction management (calc runs in its own transaction)
- Async execution (BPM can fire-and-forget or wait for completion)

**Calc log classes (where output goes):**
| Class | Purpose | Screen |
|---|---|---|
| `CALC_DAY_PROD_LOG` | Daily production calc log | CO.0246 Calculation Group Setup |
| `CALC_MTH_PROD_LOG` | Monthly production calc log | CO.0246 |
| `CALC_LOG` | Generic calc log | |

**Key insight:** The BPM-calc integration is entirely parameter-driven. The `EC_RunCalculation` building block handles all the plumbing — just configure `calc_id` and `calc_context`. Simulation mode (`calc_simulate=Y`) is a critical feature for pre-production testing. The three-level error handling (warning/error/fatal) maps directly to BPM role-based task routing.

---

## Session F — Architecture + Database (2026-06-05) [all 5 sources]

**Sources used:** EC Tech Docs 14.2.5 ✅ | ECpedia BPR ✅ | EC source code ✅ | Woodside repo ✅ | Web ✅

**Items:** #9 JSF/PrimeFaces rendering | #10 Screen templates | #11 Flyway core | #12 Journal tables

---

### Item #9: JSF/PrimeFaces Rendering Pipeline (6→9) ✅

**JSF 6-phase lifecycle — what EC uses each phase for:**

| Phase | Name | EC behaviour |
|---|---|---|
| 1 | Restore View | JSF rebuilds component tree from viewstate; screen beans loaded |
| 2 | Apply Request Values | AJAX payload decoded; screenlet component values updated |
| 3 | Process Validations | `ValidateMandatoryService` runs; custom validators execute |
| 4 | Update Model | Data model values synced from UI component values |
| 5 | Invoke Application | `EventDispatcher` fires; EC service chain executes in order |
| 6 | Render Response | PrimeFaces PPR renders only requested component IDs |

**For AJAX requests, phases 2-5 only run on components in the `process` set. Phase 6 only updates components in the `update` set.** EC exploits this to keep screen performance high — a data save only re-renders the affected table, not the whole page.

**`AbstractECService` — base for all 70+ EC services:**
```java
public abstract class AbstractECService extends ScreenXmlObject implements IECService {
    private Screenlet screenlet;           // the owning screenlet
    protected EventDispatcher eventDispatcher;  // routes ECEvents through service chain
    private Map<String,String> staticRetrieveArgs; // args declared in XHTML config
}
```
Every service declares its args in the XHTML `<ect:screenletConfig>` block. The screenlet XML is parsed once at screen load; services share the parsed element tree.

**`EventDispatcher` — EC's event bus:**
- Dispatches `ECEvent` objects through the service chain
- Services subscribe to event types (retrieve, save, navigate, etc.)
- Each service can add results to the `ServiceResponse`
- Error/warning/info messages collected → shown in notification area

**`RerenderBean` (@RequestScoped, @Deprecated):**
Was used to track component IDs for partial re-render. Now replaced by inline `update` lists in PrimeFaces components. Shows that EC is actively modernising its JSF patterns.

**PrimeFaces rendering specifics:**
- Client-side based on **jQuery** (not Mojarra/MyFaces client APIs)
- Partial Page Rendering (PPR) = only `update` component IDs re-rendered
- `process` = components that go through phases 2-5
- `@form` shorthand = process entire enclosing form
- `@this` = only the triggering component

**Web — JSF lifecycle best practices applied in EC:**
- Never use full-page submit for field changes — EC uses `f:ajax` everywhere
- Group validation using `process` attribute — EC's `ValidateMandatoryService` follows this
- Dependent dropdowns re-populated via PPR triggered by parent change

**Key insight:** EC's JSF architecture is a layered event system. The XHTML declares WHAT (screenlet type, model, services). The services decide HOW (retrieve, validate, save). The EventDispatcher coordinates WHEN. PrimeFaces handles the AJAX transport and partial re-render.

---

### Item #10: Screen Templates and XHTML Patterns (6→9) ✅

**All EC screens follow one template pattern:**
```xml
<ui:composition xmlns="http://www.w3.org/1999/xhtml"
  template="/xhtml/screen/screen.xhtml"
  xmlns:ec="http://java.sun.com/jsf/composite/screenlet"
  xmlns:ect="http://energycomponents.com/ectags"
  xmlns:p="http://primefaces.org/ui">
  <ui:define name="ecScreen">
    <!-- screen content here -->
  </ui:define>
</ui:composition>
```

- `template="/xhtml/screen/screen.xhtml"` = master page (navigation bar, layout, CSS, JS)
- `ui:define name="ecScreen"` = the only slot screens need to fill
- All screens are identical in structure — only the screenlet config differs

**Layout system — three tags:**
```xml
<ect:gridContainer>      ← outer grid wrapper
  <ect:gridRow>          ← horizontal row
    <ect:gridCell>       ← column within row
      <ec:tableScreenlet .../>
    </ect:gridCell>
  </ect:gridRow>
</ect:gridContainer>
```

**Screenlet config anatomy (from real `daily_data_status_process.xhtml`):**
```xml
<ec:formScreenlet id="nav" label="Navigator">
  <ect:screenletConfig energyx-version="3">
    <renderer>
      <model class="GenericStaticModel">          ← static XML data (dropdowns)
        <arg name="xmlResultUrl" value="/path/to/static/data.xml">
          <arg name="$PARAM$" value="CONSTANT" valuetype="constant"/>
        </arg>
      </model>
      <transformer class="JSFFormNavigatorTransformer"/>
    </renderer>
    <service class="InitialLoadService"/>
    <service class="ValidateMandatoryService">
      <arg name="buttonIDRef" value="navButtonID" datatype="string" valuetype="constant"/>
    </service>
    <service class="NavigatorHotkeyService">
      <arg name="buttonName" value="button"/>
    </service>
    <service class="RetrieveService">
      <arg name="eventSource" value="nav" datatype="object" valuetype="constant"/>
    </service>
    <service class="NavigatorButtonService">
      <arg name="buttonIDRef" value="navButtonID" datatype="string"/>
    </service>
    <service class="LinkService"/>
  </ect:screenletConfig>
</ec:formScreenlet>
```

**`valuetype` options:**
| valuetype | Meaning |
|---|---|
| `constant` | Hardcoded literal value |
| `requestParam` | Read from JSF view scope / request (e.g., `RetrieveArgs.DAYTIME`) |
| `function` | Call a Java static method |

**`RetrieveArgs` prefix = inter-screenlet data passing:**
```xml
<arg name="Param1" value="RetrieveArgs.nav.OBJECT" valuetype="requestParam"/>
```
`RetrieveArgs.nav.OBJECT` = value the `nav` screenlet published under key `OBJECT`. `LinkService` wires parent/child screenlets so child refreshes when parent selection changes.

**Model types and when to use each:**
| Model class | Use case |
|---|---|
| `GenericDaoModel` | Query driven by XML definition file (most common) |
| `GenericStaticModel` | Static XML data (dropdowns, navigator options) |
| `GenericSqlModel` | Direct SQL with parameters |
| `GenericStaticNavigatorModel` | Date range navigator model |

**`energyx-version="3"` = current screenlet config format version.** Earlier versions (1, 2) are still present in old screens but v3 is the standard from EC 11 onwards.

**Key insight:** Every EC screen is 30-60 lines of XML config. No custom Java needed for standard CRUD screens. The framework does all the work — model fetches data, services handle user actions, LinkService wires parent/child. Adding a new screen means writing the XHTML config + XML query file only.

---

### Item #11: Flyway Migration Patterns in Core EC (7→9) ✅

**Core EC migration directory structure:**
```
database/ec-db-migration-oc-0/src/main/resources/db/migration/
└── owner_context_0/
    ├── {version}/                  ← e.g. 14.2.5/
    │   ├── FRMW/                   ← framework changes
    │   ├── PROD/                   ← production domain
    │   ├── REVN/                   ← revenue domain
    │   ├── TRAN/                   ← transport domain
    │   └── CHEM/                   ← chemistry domain
    └── common/                     ← PL/SQL packages (always repeatable)
        ├── frmw/packages/
        ├── prod/packages/
        ├── revn/packages/
        └── {domain}/onlinehelp/    ← online help text (repeatable)
```

**Versioned migration filename anatomy:**
```
V14.2.5.0.0.20260204100100__ECPD-113067_fitness_rest_api_role.sql
│ │         │               │           │
│ version   timestamp       ECPD ticket description
│
V = versioned (run once, checksum locked)
```

**Repeatable migration filename anatomy:**
```
R__0100_ecbp_chemical_stream_head.sql
   │    │
   │    package name
   execution order (0100=head, 0200=body)
R__ = repeatable (re-runs when checksum changes)
```

**Head/body pattern for PL/SQL packages:**
```
R__0100_ecdp_classjournalhelper_head.sql  ← package header (spec)
R__0200_ecdp_classjournalhelper_body.sql  ← package body (impl)
```
EC always deploys head before body (0100 before 0200) — guaranteed by the numeric prefix. Both are repeatable so any code change triggers re-deploy.

**Flyway schema history table (`flyway_schema_history`):**
```sql
-- Flyway records every applied script:
installed_rank  -- sequential order applied
version         -- NULL for repeatable, version string for versioned
description     -- derived from filename
type            -- SQL or JDBC
script          -- relative path to script file
checksum        -- CRC32 of script content
installed_by    -- DB user (ECKERNEL_EC)
installed_on    -- timestamp
execution_time  -- ms
success         -- 1=OK, 0=failed
```
If a versioned migration's checksum changes after deployment → Flyway throws `ERROR: Migration checksum mismatch` → cannot start EC. This protects production data integrity.

**`ecdp_config_util` — EC's migration helper package:**
```sql
ecdp_config_util.mergeBasisRole(p_role_id, p_role_name)
ecdp_config_util.mergeBasisObject(p_object_name, p_object_type, p_object_descr)
ecdp_config_util.mergeBasisAccess(p_object_name, p_role_id, p_level_id)
```
All `merge*` procedures are idempotent — safe to run multiple times. This is the standard pattern for data inserts in versioned migrations.

**Flyway best practices (web) applied in EC:**
- Timestamp in version = prevents conflicts when two developers add migrations simultaneously
- V__ for schema/data, R__ for PL/SQL = EC follows this exactly
- One ECPD Jira ticket = one migration file = full traceability
- Never edit a deployed versioned migration = EC enforces this via checksum

**Key insight:** EC's Flyway structure is domain-separated and fully traceable. Every DB change maps to a Jira ticket. PL/SQL packages are always repeatable (code can be updated). Schema changes are always versioned (locked after deploy). The `common/` folder holds the entire PL/SQL library — hundreds of package head+body pairs.

---

### Item #12: Journal Tables and Audit Trail (5→9) ✅

**EC audit trail — three layers:**

| Layer | Mechanism | What it captures |
|---|---|---|
| REV_NO / REV_TEXT | Standard columns on every table | Revision number + reason for change |
| JN_ trigger | After Update/Delete Oracle trigger | Full row snapshot before each change |
| AP_ trigger | PINC/install trigger | Configuration change events |

**Standard table template — 11 mandatory columns (from `create_table_template.sql`):**
```sql
record_status       VARCHAR2(1)   NULL        -- P=Provisional, V=Verified, A=Approved
created_by          VARCHAR2(30)  NOT NULL
created_date        DATE          NOT NULL
last_updated_by     VARCHAR2(30)  NULL
last_updated_date   DATE          NULL
rev_no              NUMBER        NULL        -- starts 0, incremented on each update
rev_text            VARCHAR2(240) NULL        -- reason for change (e.g. ECPR-Issue1052)
approval_state      VARCHAR2(1)   NULL        -- N=New, O=Official, U=Updated, D=Deleted
approval_by         VARCHAR2(30)  NULL
approval_date       DATE          NULL
rec_id              VARCHAR2(32)  NULL        -- Oracle GUID, FK for extension tables
```

**Journal trigger (`JN_` prefix) — After Update or Delete:**
```sql
-- Generated by ecdp_classjournalhelper for each auditable table
CREATE OR REPLACE TRIGGER JN_WELL_VERSION
  AFTER UPDATE OR DELETE ON WELL_VERSION
  FOR EACH ROW
BEGIN
  IF UPDATING THEN
    INSERT INTO WELL_VERSION_JN VALUES (
      :OLD.*, 'U', SYSDATE, SYS_CONTEXT('ECKERNEL','EC_USER')
    );
  ELSIF DELETING THEN
    INSERT INTO WELL_VERSION_JN VALUES (
      :OLD.*, 'D', SYSDATE, SYS_CONTEXT('ECKERNEL','EC_USER')
    );
  END IF;
END;
```

**Journal table structure (`{TABLE}_JN`):**
- All columns from the base table
- PLUS: `JN_OPERATION VARCHAR2(1)` — U=Update, D=Delete
- PLUS: `JN_DATETIME DATE`
- PLUS: `JN_USER VARCHAR2(30)`
- No journal entry on INSERT — the base table row IS the record

**`ecdp_classjournalhelper` package:**
Generates journal triggers programmatically from class metadata. Called during `ecdp_generate()` — the same generator that creates IUD triggers and EC/ECC packages. One call generates all supporting DB objects for a class.

**`IUR_` trigger — Sets REC_ID on Insert:**
```sql
CREATE OR REPLACE TRIGGER IUR_WELL_VERSION
  BEFORE INSERT OR UPDATE ON WELL_VERSION
  FOR EACH ROW
BEGIN
  IF :NEW.REC_ID IS NULL THEN
    :NEW.REC_ID := SYS_GUID();
  END IF;
END;
```
REC_ID is the FK that extension tables use to link back to the base row — set via `IUR_` trigger, not by the application.

**Trigger priority chain (one physical table):**
```
IUR_xxx  (Before Insert/Update — sets REC_ID)
     ↓
IUG_xxx / IUC_xxx / IU_xxx  (Before/After IUD — business logic)
     ↓
JN_xxx   (After Update/Delete — journal copy)
     ↓
AP_xxx   (PINC/install — config change tracking)
```

**REV_NO lifecycle:**
```
INSERT → REV_NO = 0, REV_TEXT = 'INITIAL'
UPDATE → REV_NO = REV_NO + 1, REV_TEXT = reason (e.g. 'ECPR-Issue1052')
DELETE → Journal entry written, base row removed
```

**REV_TEXT in practice (Issue_1052):**
Every INSERT in the SQL script should set `REV_TEXT = 'ECPR-Issue1052'` — this makes every inserted row traceable in the journal to this change request.

**Flyway integration:** Journal trigger creation is part of `ecdp_generate()` — called after table creation in Flyway migrations. This is why the Session D pattern says "always call `ecdp_generate()` after creating a new table."

**Key insight:** EC's audit trail is zero-effort for developers — journal triggers are auto-generated, REV_NO is auto-incremented, and REV_TEXT is the only field developers need to populate (with their change reason). The `ecdp_classjournalhelper` package manages all journal infrastructure automatically.

---

## Session E — Business Domain (2026-06-05) [ENHANCED v2 — EC Tech Docs 14.2.5 + all 5 sources]

**Sources used:** EC Tech Docs 14.2.5 ✅ | ECpedia BPR ✅ | EC source code ✅ | Woodside repo ✅ | Web ✅

**Items:** #22 Production Well/Stream/Tank | #23 Hydrocarbon Accounting | #24 Daily+Monthly Allocation BPM

**v2 corrections:** Fixed incorrect AN_SHN/ZXIC_DAILY_VOLUME references (these don't exist in Woodside Pluto). Actual networks: PLU_EMISSION, PLU_OFFSHORE_ALLOC, PLU_ONSHORE_ALLOC, SCA_OFFSHORE_ALLOC, PLU_PRRT. Added complete Well type table, Stream phases/categories, Tank types/materials, and HC accounting algorithm details from EC Tech Docs 14.2.5.

---

### Item #22: Production Well/Stream/Tank (7→9) ✅

**EC production object hierarchy:**
```
Field
 └── Facility (Platform / Processing Plant)
      ├── Well → Well Hole → Well Bore → Well Bore Interval → Perforation Interval
      ├── Stream (flow path — connects wells/facilities/tanks)
      └── Tank (storage vessel — holds product before export)
```

**Well object hierarchy (EC Tech Docs 14.2.5):**

All sub-objects below Well are required only for reservoir allocation. For surface allocation only, Well is sufficient.

| # | Object | Required for | BF |
|---|---|---|---|
| 1 | Well | Allocation | CO.0250 |
| 2 | Well Hole | Optional (skip if not needed) | CO.0051 |
| 3 | Well Bore | Reservoir Allocation | CO.0054 |
| 4 | Well Bore Interval | Reservoir Allocation | CO.0057 |
| 5 | Reservoir Block | Reservoir Allocation | CO.0133 |
| 6 | Reservoir Formation | Reservoir Allocation | CO.0135 |
| 7 | Reservoir Block Formation | Reservoir Allocation | CO.0127 |
| 8 | Perforation Interval | Reservoir Allocation | CO.0153 |
| 9 | Well Bore Split | Reservoir Allocation | CO.0055 |
| 10 | Well Bore Interval Split | Reservoir Allocation | CO.0058 |
| 11 | Perforation Interval Split | Reservoir Allocation | CO.0154 |

**Initiate Day (CO.0077):** Creates the daily production well status record — the basis for theoretical volume and mass calculations. When set to first day of month, also creates the monthly status record. Same pattern applies for Stream and Tank.

**20 Well Types supported in EC (cannot add new types — fixed set):**

| Code | Type | Phases | Key BF |
|---|---|---|---|
| OP | Oil Producer | Oil, Gas, Water | WR.0001/0027/0028 |
| GP | Gas Producer | Gas, Cond, Water | WR.0001/0027/0028 |
| GP2 | Gas Producer (oil) | Gas, Oil, Water | WR.0001/0027/0028 |
| CP | Condensate Producer | Cond only | WR.0001/0027/0028 |
| GI | Gas Injector | Gas Injection | WR.0002 |
| WI | Water Injector | Water Injection | WR.0003 |
| WS | Water Source | Water | WR.0013 |
| WG | Water and Gas Injector | Water + Gas Inj | WR.0002 + WR.0003 |
| WSI | Water and Steam Injector | Water + Steam Inj | WR.0003 + WR.0029 |
| SI | Steam Injector | Steam Inj | WR.0029 |
| WA | Waste Injector | Waste Inj | WR.0040 |
| OB | Observation | — (not instantiated daily) | WR.0014 |
| AI | Air Injector | Air Injection | WR.0051 |
| OPGI | Oil Producer + Gas Injector | Oil/Gas/Water + GI | WR.0001 + WR.0002 |
| GPI | Gas Producer + Gas Injector | Gas/Cond/Water + GI | WR.0001 + WR.0002 |
| OPSI | Oil Producer + Steam Injector | Oil/Gas/Water + SI | WR.0001 + WR.0029 |
| SOPSI | Sim. Oil Producer + Steam Injector | Oil/Gas/Water + SI simultaneously | WR.0001 + WR.0029 |
| SWG | Sim. Water + Gas Injector | Water + Gas simultaneously | WR.0002 + WR.0003 |
| WID | Water Injection for Disposal | Water Inj | WR.0003 |
| CI | CO2 Injector | CO2 Inj | — |

**Introducing new well types is not supported** — it would break numerous system dependencies.

**Well production methods (for OP/GP/OPGI etc.):**
- Natural Flow, Gas Lift, Gas-Assisted Plunger Lift, Pumped (diluted/undiluted)
- Injection types: Hydrocarbon/Non-HC Gas Injector, Gas Disposal, Cold/Hot Water Injector

**Commercial/equity linkage:**
- Commercial Entity = many-to-many between License and Field
- Equity Share = many-to-many between Commercial Entity and Company
- Reservoir Block Formation must belong to one Commercial Entity

**Three core production object types:**

| Object | Role | Key Table | Default Helper |
|---|---|---|---|
| Well | Source of production — physical wellbore | `WELL`, `WELL_VERSION` | `WellDefaultValueHelper` → `EcDp_Well_Event.getLastClosingDaytime()` |
| Stream | Flow path between nodes | `STREAM`, `STREAM_VERSION` | `StreamDefaultValueHelper` → `EcDp_Stream_Event.getLastClosingDaytime()` |
| Tank | Storage vessel — holds product volumes | `TANK`, `TANK_VERSION` | `TankDefaultValueHelper` → `tank_version.export_stream_id` |

---

**STREAM — EC Tech Docs 14.2.5:**

A Stream object represents the logical or physical flow of hydrocarbons through production, processing, storage, and sales. Streams have metering functionality (flow rate, pressure, temperature). They also act as virtual/calculated meters.

**15 Stream Phases:**

| Phase | Notes |
|---|---|
| Oil | |
| Gas | |
| Water | |
| Condensate | |
| Reservoir Fluid | Composition analysis |
| NGL | Natural Gas Liquids |
| Solid | |
| Steam | |
| Electrical | |
| CO2 | |
| LNG | Liquefied Natural Gas |
| Dry Gas | |
| LPG | Liquefied Petroleum Gas |
| Sulfur | |
| Chemical | |

**20 Stream Categories:**
Oil Production, Condensate Production, Gas Production, Oil Export, Oil Import, Gas Export, Gas Import, Oil Fuel, Gas Fuel, Gas Flare, Gas Vent, Gas Lift, Gas Injection, Water Disposal, Water Injection, Water Production, Oil Loss, Steam Injection, Diluent, Gas Lost

**5 Stream Types:**
| Type | Meaning |
|---|---|
| Measured | Has a physical meter — actual reading |
| Reference | Reference value (not measured directly) |
| Calculated | Computed by the allocation program |
| Quality | Quality reference stream |
| Derived | Calculated using functions |

**Stream Meter Frequency:** Regular Intervals — Year / Month / Day / 1 Hour / One Minute. Aggregate flag: Yes/No.

**Stream Sets:** CO.0029 (Stream Set) groups streams for display together in a BF screen (e.g., PO.0001 Daily Oil Stream Status). CO.0030 (Stream Set List) adds/removes streams from a set.

**Alloc Period attribute** on stream — controls which allocation the stream participates in:
- Daily Allocation | Monthly Allocation | Daily and Monthly | Not included

**Alloc Fixed** — Fixed or Adjustable. Fixed streams are not modified by allocation (fiscal meters, master injection). Adjustable = modified by allocation. **Allocation fails if no adjustable incoming streams exist for a production node.**

---

**TANK — EC Tech Docs 14.2.5:**

Four interconnected concepts:
1. **Tank** — physical vessel (crude oil, condensate, refined products)
2. **Storage** — accounting value (changes with fills, withdrawals, transfers, losses)
3. **Tank Strapping** — calibration table: height → volume. Used to convert level measurements (dip tape/sensor) to volume. Essential for accurate HC accounting.
4. **Tank Tap** — physical connection point (valve/nozzle) for sampling, transfer, or gauging

**Tank Types:**
| Type | Description |
|---|---|
| Export tank | |
| Settling tank | |
| Pipeline inventory as virtual tank | |
| Other tank types | Terminal tanks |
| Import tank | |

**Tank Materials:** Mild Steel, Carbon Steel, Monel (nickel-copper, corrosive HC), Type 316 SS, Type 304 SS

**Initiate Day:** Creates daily tank status record (BSW, density, tank volume, mass). Last day of month → monthly tank status record.

**Tank = member of Allocation Node** — tanks participate in the allocation network as nodes.

**Tank BF screens:**
- PO.0005 — Daily Tank Status
- PO.0006 — Monthly Tank Status
- PO.0023 — Batch Oil Tank Export (Tank Dip)

**Analysis Stream attribute** on Tank — used for BSW/density from stream sample analysis. Functions:
| Function | Retrieves | Used in |
|---|---|---|
| `findBSWVol` | BSW volume fraction | Calc Tank BSW at PO.0005 |
| `findBSWWt` | BSW weight fraction | Net Oil Mass at PO.0023 |
| `findStdDens` | Density at standard conditions | Calc Tank Density at PO.0005 |
| `findObsDens` | Observed density | Gross Oil Mass at PO.0023 |

**Woodside Pluto tanks:**
- PLU_COND_TANK_1, PLU_COND_TANK_2, PLU_COND_TANK_3 (condensate storage)
- Report: `DPR_SUB8_STORAGE_TANK.jasper`

---

**Common patterns across all three objects:**
- Time scope codes: `1HR, 2HR, DAY, WEEK, MTH, QTR, YR, VERSIONED, EVENT, NONE, INVARIANT, SAMPLE`
- Every data class is assigned a time scope — determines production data bucketing
- All three require Initiate Day (CO.0077) to create status records
- All three use closing daytime: `EcDp_Well_Event.getLastClosingDaytime()`, `EcDp_Stream_Event.getLastClosingDaytime()`

**Well PVT split (`EcBsWellSplit.java`):**
```sql
SELECT OBJECT_ID, RESULT_NO,
       THEOR_NET_OIL_RATE, THEOR_GAS_RATE,
       THEOR_NET_COND_RATE, THEOR_WATER_RATE
FROM TV_PVT_PT_THEOR_WELLS WHERE RESULT_NO = ?
```
Outputs: `wellOilPart[]`, `wellGasPart[]`, `wellConPart[]`, `wellWatPart[]` — splits commingled volumes back to individual wells.

**Stream Node Diagram (SND):**
`StreamNodeDiagramModel.java` + `StreamNodeDiagramAction.java` renders the production network as a directed graph. Nodes = wells/facilities/tanks; edges = streams. Phase colours configurable in CO.1006 (Maintain System Settings). Filter transformers: `NetworkFilterTransformer`, `GroupTransformer`, `DynamicQueryTransformer`.

**Woodside ZWT extension functions:**
```
zwt_prod_stream_formula.evaluateMethod(p_object_type, p_object_id, p_method, p_daytime, p_to_date, p_stream_id)
zwt_prod_well_theoretical.findGasOilRatio(well_id, daytime)   -- GOR at standard conditions
zwt_prod_well_theoretical.findGCV(well_id, daytime)           -- Gross Calorific Value (gas → energy)
zwt_prod_well_theoretical.getGasEnergyMonth(well_id, daytime) -- monthly gas energy content (GJ/MMBtu)
```
GCV converts gas volumes to energy — critical for LNG and sales accounting.

**Woodside production views:**
- OFM well views: `ZWP_V_OFM_WELL_DAY`, `ZWP_V_OFM_WELL_MTH`
- NOPTA regulatory views: `ZWP_V_NOPTA_WELL`, `ZWP_V_NOPTA_WELL_SEC2`, `ZWP_V_NOPTA_WELL_TEST`
- Allocation reporting: `ZWP_V_REP_PWEL_MTH_ALLOC`, `ZWP_V_REP_STRM_DAY_ALLOC`, `ZWP_V_REP_STRM_MTH_ALLOC`
- Report: `DPR_SUB12_WELLS.jasper` (well report)

**ECpedia Polar Bear reference pattern:**
- 2 fields (North + South) → 1 platform → multiple wells: OP = Oil Producer, GI = Gas Injector, WI = Water Injector
- Oil stored in tank (no export yet in sandbox); gas and water follow separate streams
- Stream Node Diagram (SND) shows the full allocation network visually

**Key insight:** Well → Stream → Facility is EC's production hierarchy. 20 well types are fixed by EC (cannot extend). Initiate Day (CO.0077) is the trigger that creates status records for all three object types. Tank strapping converts physical level measurements to volumes. Streams can be Measured, Derived, or Calculated — the allocation engine only adjusts "Adjustable" streams.

---

### Item #23: Hydrocarbon Accounting (5→9) ✅

**What HC accounting covers:**
- Field operations: well tests, meter readings, tank dipping
- Volumetric allocation: splitting commingled volumes to owners/wells
- Contractual allocation: applying ownership percentages
- Data lifecycle: Provisional → Verified → Approved
- Revenue distribution, royalty management, regulatory reporting

**EC business functions for HC accounting (HA.* module):**
| Code | Description |
|---|---|
| HA.0001 | Daily Data Status Processes |
| HA.0002 | Daily Allocation |
| HA.0003 | Monthly Allocation |
| HA.0010 | Daily Allocation — Single Date |
| HA.0011 | Daily Data Status Processes — Single Date |

**HC accounting in EC = three decoupled subsystems:**

| Subsystem | Role |
|---|---|
| Allocation Network (`ALLOC_NETWORK`) | Network topology — which streams/wells contribute to which nodes |
| Calculation Engine | Computes volumes: allocation calculations per network |
| Data Lifecycle (BPM) | Controls Provisional → Verified → Approved state transitions |

**Three calculation types in EC (EC Tech Docs 14.2.5):**
| Type | Description | When to use |
|---|---|---|
| Equation-based | EC-specific math syntax; compact and dynamic | Complex multi-phase volume calculations |
| Excel workbook | Maps data between EC and Excel | When users prefer Excel-based design |
| Calculation Processes | Flowchart breaking calc into sub-calcs | Complex workflow with mixed sub-calc types |

Library calculations (CO.1061/CO.1062) can be sub-steps in Calculation Processes.

**Allocation Network — how it works:**
- `ALLOC_NETWORK` defines the production network graph for allocation
- Each network links to a calculation via `TV_ALLOC_NETWORK_JOB_CONN`
- Multiple networks can be defined per installation
- Node types: Well, Well Hookup (manifold/subsea template), Facility Class 1/2, Node (generic)

**Well allocation configuration flags (affect standard calculation):**
| Flag | Effect |
|---|---|
| Include in allocation | Must be checked for well to participate |
| Allocate all Phases Fixed | Well not modified by allocation — all phases fixed |
| Allocate using Fixed GOR | GOR not changed by allocation |
| Allocate using Fixed WC | Water cut not changed by allocation |

**Stream allocation configuration flags:**
| Attribute | Options | Effect |
|---|---|---|
| Stream type | Measured / Derived / Calculated | Measured/Derived = initial value from DB; Calculated = computed in calc |
| Alloc Period | Daily / Monthly / Both / Not included | Which allocation runs include this stream |
| Alloc Data Frequency | Daily / Monthly | Whether daily or monthly data feeds allocation |
| Alloc Fixed | Fixed / Adjustable | Fixed = not modified; Adjustable = modified by allocation |

**Well Hookup configuration:**
- Include in allocation checkbox
- Calculation Sequence Number — order in which nodes are reconciled
- Can process phases — which fluid types
- Allocation Reconciliation Method — factor calculated per day or as monthly average

**Calculation algorithm (from EC Tech Docs HC Accounting section):**
- All nodes except wells have a calc sequence number
- Wells are FIXED at calc sequence 99
- Values decrease as you move UP the network (facility = low sequence, wells = 99)
- Initial values come from DB (measurements/estimates)
- Well flows start with theoretical volumes (PVT-based), then are adjusted by allocation
- Fixed streams receive allocated volume identical to measured volume (no adjustment)
- Reconciliation: each node adjusts its well contributions so that sum(in) = sum(out) per phase

**Woodside Pluto allocation networks (from actual git repo — CORRECTED):**

| Network Code | Name | Period | Linked Calculation |
|---|---|---|---|
| PLU_EMISSION | Pluto Emissions | DAY | ZWPC_EMISSION_DISCHARGE |
| PLU_OFFSHORE_ALLOC | Pluto Offshore Allocation | MONTH | C_ALLOC_OFFSHORE_MTH |
| PLU_ONSHORE_ALLOC | Pluto Onshore Allocation | DAY_MONTH | (C_MASS_BALANCE_MTH — commented out) |
| SCA_OFFSHORE_ALLOC | Scarborough Offshore Allocation | DAY_MONTH | — |
| SCA_EMISSION | Scarborough Emissions | DAY | ZWPC_SCA_EMISSION_DISCHARGE |
| PLU_PRRT | PRRT | MONTH | C_PRRT |

**Note:** AN_SHN and ZXIC_DAILY/MONTHLY_VOLUME do NOT exist in Woodside Pluto. These were from a different project. Pluto uses PLU_/SCA_ prefixed networks and calculation codes.

**Woodside allocation tables:**
| Table | Period | Content |
|---|---|---|
| ZWP_T_PWEL_DAY_ALLOC | Daily | `ZWP_ALLOC_HC_GAS_VOL`, `ZWP_ALLOC_HC_GAS_MASS`, `ZWP_THEOR_HC_GAS_RATE`, `ZWP_HC_GAS_VOL_FACTOR` |
| ZWP_T_STRM_DAY_ALLOC | Daily | `ZWP_EMIS_ALLOC_MASS`, `ZWP_EMIS_ALLOC_VOL`, `ZWP_EMIS_ALLOC_ENERGY`, `ZWP_EMIS_RUN_NO` |
| ZWP_PWEL_MTH_ALLOC | Monthly | Production well monthly allocation |
| ZWP_STRM_MTH_ALLOC | Monthly | Stream monthly allocation + emissions |

**Data lifecycle state codes (Woodside Pluto — project-specific):**
```
D_SHENZI_P_TO_V  — Provisional → Verified   (daily step, run by HA.0001 Daily Data Status Process)
D_SHENZI_V_TO_A  — Verified → Approved      (monthly step, run by approval BPM)
```

**"Work by Exception" principle:**
No manual user interaction required unless something fails. Users get tasks only when check rules fail, reports need verification, or a step errors. On normal days, the BPM runs fully automated.

**HC phases tracked:**
| Phase | Attribute example |
|---|---|
| Oil | `THEOR_NET_OIL_RATE` |
| Gas | `THEOR_GAS_RATE` |
| Condensate | `THEOR_NET_COND_RATE` |
| Water | `THEOR_WATER_RATE` |

**Woodside-specific HC calculations (ZWP_P_PROD_WELL_THEORETICAL):**
```
getCondStdRateDay()    -- condensate at standard conditions (from fluid analysis + density)
getGasStdRateDay()     -- gas at standard conditions
getFlowlineConHrs()    -- flowing condensate hours
findGasOilRatio()      -- GOR at standard conditions
findGCV()              -- Gross Calorific Value (gas → energy)
getGasEnergyMonth()    -- monthly gas energy content (GJ/MMBtu)
```

**Key insight:** HC accounting = network config (PLU_/SCA_ codes) + calc engine (equation/Excel/flowchart) + BPM lifecycle. The three are deliberately decoupled. Woodside uses separate daily emissions networks (PLU_EMISSION, SCA_EMISSION) and monthly offshore allocation networks (PLU_OFFSHORE_ALLOC) — not a single unified allocation network. Fixed streams are not touched by allocation; adjustable streams are reconciled.

---

### Item #24: Daily + Monthly Allocation BPM (5→9) ✅

**EC BPM foundation:**
- Introduced in **EC10** (jBPM engine), BPMN 2.0 support from **EC11**
- Current engine: **jBPM 7.74.1.Final** (EC 14.2.1+)
- Designed in Eclipse 2023-12 + BPMN2 Modeler plugin 1.5.4-202212
- Deployed via "Project Management" business function (PA.0013)
- Executed via "Process Execution" business function (PA.0003)
- Core principle: **"Work by Exception"** — no manual steps unless something fails

**Deployment steps:**
1. Download BPM artifacts from Nexus: `downloads/com/ec/prod/prod-bpm-building-blocks`
2. In EC → Project Management (PA.0013) → Add record (GroupId=`com.ec.bpm`, ArtifactId=`prod-bpm-building-blocks`)
3. Upload and Deploy → Configure Process Template → execute from PA.0003

**Two core BPMN processes:**

| Process | ID | Woodside config |
|---|---|---|
| Daily Allocation | `ECProd_DailyProductionAllocation` | V1.0.0.1600__BPM_D_01.sql |
| Monthly Allocation | `ECProd_MonthlyProductionAllocation` | V1.0.0.1700__BPM_M_01.sql |

Both are overridden in Woodside repo: `/bpm/prod-bpm-building-blocks/src/main/resources/building-blocks/allocation/` — always check this folder for Pluto-specific changes.

**Daily BPM sub-steps (in order):**
1. **Input data initialization** (mandatory)
2. **Input validation** (mandatory) — checks concurrent runs, resolves network/dates
3. Run data pre-checks — Check Rules + object/class validation
4. Run data verification — Provisional → Verified (`D_SHENZI_P_TO_V`)
5. Run allocation — executes the configured allocation calculation
6. Ghost Data Cleanup — removes orphan records from cancelled prior runs
7. Run report process — generates Daily Production Report
8. Approve allocation process

**Monthly BPM adds over daily:**
- Run Data Approval — Verified → Approved (`D_SHENZI_V_TO_A`)
- **Month Lock user task** — user confirms data is ready to lock
- `perform_data_locking = Y` — locks the monthly period after approval
- `ask_rerun_alloc_pre_data_approval = N` — skip rerun prompt
- `data_approval_auto_run = Y` — auto-run approval without manual trigger

**Key BPM parameters (CORRECTED from actual Woodside BPM SQL):**
```sql
-- Registered as TV_BUSINESS_ACTION_JBPM
JBPM Deployment: com.ec.woodside:WSTEMPLATE:1.0
Action class:    StartProcessInstanceBusinessAction
Functional area: EC

-- Common daily params
production_day: DATE (mandatory)
include_subgroups: N
calc_log_class: CALC_DAY_PROD_LOG
calc_context: EC_PROD
data_verification_status_process: D_SHENZI_P_TO_V
-- (alloc_net_code and calc_id are set per network — PLU_OFFSHORE_ALLOC, C_ALLOC_OFFSHORE_MTH etc.)

-- Monthly extras
run_data_approval: Y
data_approval_auto_run: Y
data_approval_status_process: D_SHENZI_V_TO_A
perform_data_locking: Y
role_confirm_data_lock: SYST.ADM
calc_log_class: CALC_MTH_PROD_LOG
```

**All BPM building blocks:**
| Building Block | Description |
|---|---|
| `ECProd_AllocInputValidation` | Input validation; resolves alloc_net_id, start/end dates, created_by |
| `ECProd_RunReports` | Run report + optional Verify/Approve by stakeholders |
| `ECProd_VerifyApproveProcess` | Data status transitions (Verified/Approved/Approve Allocation) |
| `EC_CheckRuleWithErrorHandling` | Check rule run + user task routing for warning/error |
| `EC_RunCalculation` | Run a calculation |
| `EC_RunCalculationWithErrorHandling` | Run calculation + handle warning/error user tasks |
| `EC_RunCheckRules` | Run check rules |
| `EC_RunReport` | Run a single report |
| `EC_CreateEmailNotification` | Send email to user/role/contact group |

**Error handling — three levels:**
| Level | Woodside role | Behaviour |
|---|---|---|
| Fatal | `role_handle_alloc_fatal_error = SYST.ADM` | Stops process; assigns task to role |
| Non-fatal | `role_handle_alloc_nonfatal_error = SYST.ADM` | Assigns task; process can continue |
| Warning | `role_handle_alloc_warning = SYST.ADM` | Notifies role; no stop |

**Woodside BPM supporting components:**
- `ECProd_AllocInputValidation.bpmn2` — input validation
- `ECProd_VerifyApproveProcess.bpmn2` — approval workflows
- `ECProd_RunReports.bpmn2` — report generation
- `EC_RunCalculation.bpmn2` — calculation execution
- `EC_CheckRuleWithErrorHandling.bpmn2` — validation rules
- Allocation reports: `R_BLP_DAILY_PROD_ALLOC_PLUTO.sql`, `R_BLP_DAILY_PROD_ALLOC_SCA.sql`, `R_BLP_MONTHLY_ALLOC_PLUTO.sql`

**Key insight:** EC BPM is configuration-driven — same BPMN structure, behaviour controlled by parameters. The "Work by Exception" principle means operators don't touch the system on normal days; only act when the system assigns a task. Monthly adds Data Locking. Woodside has its own BPM overrides in the project repo and uses PLU_/SCA_ allocation network codes (not AN_SHN). Each allocation network maps to a specific calculation via `TV_ALLOC_NETWORK_JOB_CONN`.


