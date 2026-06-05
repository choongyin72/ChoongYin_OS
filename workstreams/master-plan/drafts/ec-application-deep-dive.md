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

## Session E — Business Domain (2026-06-05) [ENHANCED — all 5 sources]

**Sources used:** EC Tech Docs 14.2.5 ✅ | ECpedia BPR ✅ | EC source code ✅ | Woodside repo ✅ | Web ✅

**Items:** #22 Production Well/Stream/Tank | #23 Hydrocarbon Accounting | #24 Daily+Monthly Allocation BPM

---

### Item #22: Production Well/Stream/Tank (7→9) ✅

**EC production object hierarchy:**
```
Field
 └── Facility (Platform / Processing Plant)
      ├── Well (physical wellbore — producer or injector)
      ├── Stream (flow path — connects wells/facilities/tanks)
      └── Tank (storage vessel — holds product before export)
```

**Polar Bear reference config (ECpedia — best practice pattern):**
- 2 fields (North + South) → 1 platform → multiple wells by type:
  - **OP** = Oil Producer, **GI** = Gas Injector, **WI** = Water Injector
- Oil stored in tank (no export yet in sandbox); gas and water follow separate streams
- Stream Node Diagram (SND) shows the full allocation network visually

**EC Business Function codes for well/stream operations:**
| Module | Code | Description |
|---|---|---|
| Production Operation | PO.0001 | Daily Oil Stream Status |
| Production Operation | PO.0002 | Daily Gas Stream Status |
| Production Operation | PO.0003 | Daily Water Stream Status |
| Production Operation | PO.0059 | Daily Oil Stream Status by Stream |
| Well & Reservoir | WR.0001 | Daily Production Well Status 1 |
| Well & Reservoir | WR.0002 | Daily Gas Injection Well Status |
| Well & Reservoir | WR.0003 | Daily Water Injection Well Status |
| Well & Reservoir | WR.0088 | Maintain Well Status |
| Production Testing | PT.0005 | Production Test Define |
| Production Testing | PT.0021 | Automated Production Test |

**Three core production object types in EC:**

| Object | Role | Key Table | Default Helper |
|---|---|---|---|
| Well | Source of production — physical wellbore | `WELL`, `WELL_VERSION` | `WellDefaultValueHelper` → `EcDp_Well_Event.getLastClosingDaytime()` |
| Stream | Flow path between nodes — connects wells/facilities | `STREAM`, `STREAM_VERSION` | `StreamDefaultValueHelper` → `EcDp_Stream_Event.getLastClosingDaytime()` |
| Tank | Storage vessel — holds product volumes | `TANK`, `TANK_VERSION` | `TankDefaultValueHelper` → queries `tank_version.export_stream_id` |

**Time scope codes (from XSD class model):**
`1HR, 2HR, DAY, WEEK, MTH, QTR, YR, VERSIONED, EVENT, NONE, INVARIANT, SAMPLE`
Every data class in EC is assigned a time scope — this determines how production data is bucketed (hourly, daily, monthly etc).

**Well PVT split calculation (`EcBsWellSplit.java`):**
```sql
-- Theoretical rates per well from PVT model
SELECT OBJECT_ID, RESULT_NO,
       THEOR_NET_OIL_RATE, THEOR_GAS_RATE,
       THEOR_NET_COND_RATE, THEOR_WATER_RATE
FROM TV_PVT_PT_THEOR_WELLS
WHERE RESULT_NO = ?
```
Outputs: `wellOilPart[]`, `wellGasPart[]`, `wellConPart[]`, `wellWatPart[]` — used to split commingled stream volumes back to individual wells.

**Stream node diagram (`StreamNodeDiagramModel.java`):**
Visual network of streams between production nodes — merge/split logic rendered as a directed graph in the EC UI.

**Tank export stream pattern:**
Every tank has an export stream — `tank_version.export_stream_id` links the tank to its outflow stream. TankDefaultValueHelper resolves this at runtime.

**Woodside extension functions (ZWT):**
```
zwt_prod_stream_formula.evaluateMethod(p_object_type, p_object_id, p_method, p_daytime, p_to_date, p_stream_id)
zwt_prod_well_theoretical.findGasOilRatio(well_id, daytime)
zwt_prod_well_theoretical.findGCV(well_id, daytime)
zwt_prod_well_theoretical.getGasEnergyMonth(well_id, daytime)
```
Unified evaluation pattern — same signature for well/stream/tank/facility objects.

**Stream closing daytime pattern (`StreamDefaultValueHelper.java`):**
```java
// Calls Oracle PL/SQL function to get last stream closing event
SELECT to_char(EcDp_Stream_Event.getLastClosingDaytime(
    ?, ?, to_date(?,'yyyy-mm-dd"T"hh24:mi:ss')),
    'yyyy-mm-dd"T"hh24:mi:ss') FROM dual
-- Same pattern exists for Well: EcDp_Well_Event.getLastClosingDaytime()
```
Closing daytime = when a well/stream was last "closed" (i.e., a production period ended). Used as the default date on data entry screens.

**Time scope codes (from XSD class model):**
`1HR, 2HR, DAY, WEEK, MTH, QTR, YR, VERSIONED, EVENT, NONE, INVARIANT, SAMPLE`
Every data class is assigned a time scope — determines how production data is bucketed.

**Well PVT split calculation (`EcBsWellSplit.java`):**
```sql
SELECT OBJECT_ID, RESULT_NO,
       THEOR_NET_OIL_RATE, THEOR_GAS_RATE,
       THEOR_NET_COND_RATE, THEOR_WATER_RATE
FROM TV_PVT_PT_THEOR_WELLS WHERE RESULT_NO = ?
```
Splits commingled stream volumes back to individual wells using PVT theoretical rates.

**Tank export stream pattern:**
Every tank has an export stream — `tank_version.export_stream_id`. TankDefaultValueHelper resolves this at runtime to link tank data entry to the correct outflow stream.

**Stream Node Diagram (SND):**
`StreamNodeDiagramModel.java` + `StreamNodeDiagramAction.java` — renders the production network as a directed graph. Nodes are wells/facilities/tanks; edges are streams. Filter transformers (`NetworkFilterTransformer`, `GroupTransformer`, `DynamicQueryTransformer`) allow different views of the same network.

**Woodside extension functions (ZWT — unified evaluation):**
```
zwt_prod_stream_formula.evaluateMethod(p_object_type, p_object_id, p_method, p_daytime, p_to_date, p_stream_id)
zwt_prod_well_theoretical.findGasOilRatio(well_id, daytime)   -- GOR at standard conditions
zwt_prod_well_theoretical.findGCV(well_id, daytime)           -- Gross Calorific Value
zwt_prod_well_theoretical.getGasEnergyMonth(well_id, daytime) -- energy content of gas (monthly)
```
GCV converts gas volumes to energy (GJ/MMBtu) — critical for LNG and sales accounting.

**Industry context (web):**
Best-in-class upstream systems model wells, meters, tanks as interconnected "objects" with date-effective records, run tickets, well tests, and flexible formulas — exactly EC's pattern. Central data warehouse approach ensures production volumes feed directly into financials without re-keying.

**Key insight:** Well → Stream → Facility is EC's production hierarchy. Wells produce into streams; streams flow to facilities or tanks. PVT-based back-allocation splits commingled stream volumes to source wells. Stream Node Diagram provides the visual representation of the entire allocation network.

---

### Item #23: Hydrocarbon Accounting (5→9) ✅

**What HC accounting covers (industry + EC context):**
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
| Calculation Engine | Computes volumes: daily (`ZXIC_DAILY_VOLUME`) and monthly (`ZXIC_MONTHLY_VOLUME`) |
| Data Lifecycle (BPM) | Controls Provisional → Verified → Approved state transitions |

**Allocation Network:**
- `ALLOC_NETWORK` defines the production network graph for allocation
- Each network links to a calculation object: the engine that runs the actual volume calculations
- Woodside Pluto: network code `AN_SHN` (Shenzi network) → calc `ZXIC_DAILY_VOLUME` / `ZXIC_MONTHLY_VOLUME`
- Network has `include_subgroups` flag — controls whether sub-group wells are included in allocation

**HC phases tracked in EC:**
| Phase | Attribute example | Notes |
|---|---|---|
| Oil | `THEOR_NET_OIL_RATE` | Net after water cut |
| Gas | `THEOR_GAS_RATE` | Total gas rate |
| Condensate | `THEOR_NET_COND_RATE` | NGL/condensate |
| Water | `THEOR_WATER_RATE` | Tracked even though not HC — affects ratios |

**Data lifecycle state codes (Woodside Pluto — project-specific):**
```
D_SHENZI_P_TO_V  — Provisional → Verified   (daily step, run by Daily Data Status Process HA.0001)
D_SHENZI_V_TO_A  — Verified → Approved      (monthly step, run by approval in BPM)
```
State codes are passed as BPM parameters — the core EC BPMN process does not change between projects.

**"Work by Exception" principle (ECpedia + EC Tech Docs):**
No manual user interaction required if everything is within expected range. Users only get tasks when:
- Check rules fail (warning/error)
- Reports need verification/approval
- A step encounters an error

**Ghost Data Cleanup (mentioned in both daily and monthly BPM docs):**
Before running allocation, EC optionally removes "ghost" data — orphan records from previous cancelled or partial allocation runs. Prevents double-counting. A step in both daily and monthly BPM.

**Woodside-specific HC calculations:**
```
zwt_prod_well_theoretical.getGasEnergyMonth()  — energy content of gas (monthly, GJ/MMBtu)
zwt_prod_well_theoretical.findGasOilRatio()    — GOR at standard conditions
zwt_prod_well_theoretical.findGCV()            — Gross Calorific Value
```

**Key insight:** HC accounting = network topology config + calculation engine execution + BPM lifecycle control. These three are deliberately decoupled: you can change the allocation calculation without touching the BPM, and change the state workflow without touching the network. Woodside injects project-specific codes at the BPM parameter level.

---

### Item #24: Daily + Monthly Allocation BPM (5→9) ✅

**EC BPM foundation:**
- Introduced in **EC10** (jBPM engine), BPMN 2.0 support from **EC11**
- Current engine: **jBPM 7.74.1.Final** (EC 14.2.1+)
- Designed in Eclipse 2023-12 + BPMN2 Modeler plugin 1.5.4-202212
- Deployed via "Project Management" business function (PA.0013)
- Executed via "Process Execution" business function (PA.0003)
- Core principle: **"Work by Exception"** — no manual steps unless something fails

**Deployment steps (EC Tech Docs):**
1. Download BPM artifacts from Nexus: `downloads/com/ec/prod/prod-bpm-building-blocks`
2. In EC → Project Management (PA.0013) → Add record (GroupId=`com.ec.bpm`, ArtifactId=`prod-bpm-building-blocks`)
3. Upload and Deploy → artifacts appear in Project Management
4. Configure Process Template → execute from Process Execution (PA.0003)

**Two core BPMN processes:**

| Process | ID | Woodside Trigger | Calc |
|---|---|---|---|
| Daily Allocation | `ECProd_DailyProductionAllocation` | CRON `0 0 7 ? * * *` (7 AM CET, runs for YESTERDAY) | `ZXIC_DAILY_VOLUME` |
| Monthly Allocation | `ECProd_MonthlyProductionAllocation` | Manual / scheduled monthly | `ZXIC_MONTHLY_VOLUME` |

**Daily BPM sub-steps (in order, all optional except input init/validation):**
1. **Input data initialization** (mandatory)
2. **Input validation** (mandatory) — checks concurrent runs, resolves network/dates
3. Run data pre-checks — Check Rules + object/class validation
4. Run data verification — Provisional → Verified (`D_SHENZI_P_TO_V`)
5. Run allocation — executes `ZXIC_DAILY_VOLUME` calculation
6. Ghost Data Cleanup — removes orphan records from cancelled prior runs
7. Run report process — generates Daily Production Report
8. Approve allocation process

**Monthly BPM adds over daily:**
- Run Data Approval — Verified → Approved (`D_SHENZI_V_TO_A`)
- **Month Lock user task** — user confirms data is ready to lock
- `perform_data_locking = Y` — locks the monthly period after approval
- `ask_rerun_alloc_pre_data_approval = N` — skip rerun prompt by default
- `data_approval_auto_run = Y` — auto-run approval without manual trigger
- Screen link: `/com.ec.prod.ha.screens/mth_data_lock` (Monthly Data Lock screen)

**All BPM building blocks (ECpedia):**
| Building Block | Description |
|---|---|
| `ECProd_AllocInputValidation` | Input validation for allocation; resolves alloc_net_id, start/end dates, created_by |
| `ECProd_RunReports` | Run report + optional Verify/Approve by stakeholders |
| `ECProd_VerifyApproveProcess` | Data status transitions (Verified/Approved/Approve Allocation) |
| `EC_CheckRuleWithErrorHandling` | Check rule run + user task routing for warning/error |
| `EC_RunCalculation` | Run a calculation |
| `EC_RunCalculationWithErrorHandling` | Run calculation + handle warning/error user tasks |
| `EC_RunCheckRules` | Run check rules |
| `EC_RunReport` | Run a single report |
| `EC_CreateEmailNotification` | Send email to user/role/contact group |

**Error handling — three levels (configured via role parameters):**
| Level | Woodside role | Behaviour |
|---|---|---|
| Fatal | `role_handle_alloc_fatal_error = SYST.ADM` | Stops process; assigns task to role |
| Non-fatal | `role_handle_alloc_nonfatal_error = SYST.ADM` | Assigns task; process can continue |
| Warning | `role_handle_alloc_warning = SYST.ADM` | Notifies role; no stop |

**Woodside BPM configuration (from V1.0.0.1600 and V1.0.0.1700 SQL):**
```sql
-- Registered as TV_BUSINESS_ACTION_JBPM
JBPM Deployment: com.ec.woodside:WSTEMPLATE:1.0
Action class:    StartProcessInstanceBusinessAction
Functional area: EC

-- Key daily params
alloc_net_code = AN_SHN, calc_id = ZXIC_DAILY_VOLUME
production_day: DATE (mandatory), include_subgroups = N
calc_log_class = CALC_DAY_PROD_LOG, calc_context = EC_PROD
data_verification_status_process = D_SHENZI_P_TO_V

-- Key monthly extras
run_data_approval = Y, data_approval_auto_run = Y
data_approval_status_process = D_SHENZI_V_TO_A
perform_data_locking = Y, role_confirm_data_lock = SYST.ADM
calc_log_class = CALC_MTH_PROD_LOG
```

**Woodside also has its own BPMN overrides:**
`/c/DEV/GIT/woodside_impl_pluto_12839/bpm/prod-bpm-building-blocks/` — Woodside carries its own customised copies of `ECProd_DailyProductionAllocation.bpmn2`, `ECProd_MonthlyProductionAllocation.bpmn2`, and `ECProd_AllocInputValidation.bpmn2`. This means Woodside's BPM behaviour may differ slightly from core EC — always check this folder for Pluto-specific changes.

**Key insight:** EC BPM is fully configuration-driven — same BPMN structure, all behaviour controlled by parameters. The "Work by Exception" principle means operators don't touch the system on normal days; they only act when the system assigns them a task. Monthly adds Data Locking on top of daily — once locked, the period cannot be changed without unlocking. Woodside has its own BPM overrides stored in the project repo.


