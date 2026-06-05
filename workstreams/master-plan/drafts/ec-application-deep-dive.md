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

## Session A — Deep Dive Results

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

## Session B — Deep Dive Results

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

---

## Session C — Deep Dive Results

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

**Woodside Issue_1052 note:** PHD tags showing NULL → check TRANS_SOURCE_TIME.LAST_TRANSFER. If stuck, move it back to force re-read. This is the root cause diagnostic tool.
