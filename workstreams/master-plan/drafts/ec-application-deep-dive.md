# EC Application — Deep Dive Learning Notes

**Date:** 2026-06-05
**Source:** C:\DEV\GIT\ec-application
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
