# ectestautomation — Deep Dive Learning Notes

**Date:** 2026-06-05
**Source:** C:\DEV\GIT\ecaas_clp_hongkong\ectestautomation
**Project:** CLP Hong Kong EC SaaS implementation
**Purpose:** Deep learning of EC test automation framework

---

## What It Is

Test automation suite for **CLP Hong Kong** — an EC SaaS project managing LNG, Pipeline Gas (PGAS), Coal, By-Products (ByP) and ULSD. Production-grade BDD framework built on EC's own `ectestautomation` framework.

---

## Technology Stack

| Component | Technology | Version |
|---|---|---|
| Language | Java | 11 |
| Test Framework | Arquillian | 1.6.0.Final |
| UI Interaction | Graphene | 3.0.0-EC |
| BDD Runner | Cucumber (cukespace-core) | 1.6.7 |
| Base Test | JUnit | 4.13.1 |
| Browser | Selenium WebDriver / Chrome | - |
| Grid | Selenium Grid | localhost:4444 |
| Reports | Extent Reports + HTML5 | - |
| Build | Maven (multi-module) | - |

---

## Project Structure

```
ectestautomation/
├── pom.xml                          Aggregator — parent config
├── READ ME.md                       Prerequisites, exclusions, known issues
├── ectest-ecpa/                     BDD tests module
│   ├── pom.xml                      URL: https://uat.clp-nprod.ecaas.cloud/
│   └── src/
│       ├── main/java/com/ec/storysteps/   90+ step definition classes
│       │   ├── GenericSteps/             Generic navigation + form filling
│       │   ├── PlanningAndScheduling/    ~20 cargo/nomination steps
│       │   ├── ProcurementFinance/       ~30 pricing/invoice/doc steps
│       │   ├── TerminalServices/         ~10 cargo mgmt steps
│       │   ├── Configuration/            User/asset config steps
│       │   └── Other/                    ECIS, Messaging, Reporting steps
│       └── test/
│           ├── features/                 96 feature files
│           │   ├── LNG/                  ~30 scenarios
│           │   ├── PGAS/                 ~20 scenarios
│           │   ├── LGAS/                 ~10 scenarios
│           │   ├── Coal/                 ~15 scenarios
│           │   ├── ByP/                  ~10 scenarios
│           │   └── CommonSanitySuite/    ~5 scenarios
│           ├── testRunners/              20+ JUnit runners by product line
│           └── resources/
│               ├── arquillian.xml        Browser/grid/wait config
│               ├── test.properties       REST credentials
│               ├── ectest-core.properties WebDriver timeouts
│               ├── environment.properties Environment mapping
│               └── screenletmapping.properties Screenlet key mapping
└── ectest-pages/                    Page Object Models module
    └── src/main/java/com/ec/selenium/  113 page classes
        ├── pageutils/                LoginPage, PageComponents
        ├── planningandscheduling/    15+ cargo/nomination pages
        ├── procurementfinance/      10+ pricing/document pages
        ├── terminalservices/        5+ terminal pages
        ├── configuration/           User/asset config pages
        └── ecpages/production/      Production screen pages
```

---

## Core Architecture Pattern

```
Feature File (.feature / Gherkin)
        ↓
Step Definition (Java — extends PageComponents)
        ↓
Page Object (extends PageComponents → extends ECPage)
        ↓
Base Methods: getTableScreenlet() / getFormScreenlet() / getButtonScreenlet()
        ↓
Arquillian Graphene → Selenium WebDriver → PrimeFaces EC screen
```

### PageComponents Base Methods

| Method | Purpose |
|---|---|
| `getTableScreenlet(key)` | Access a TableScreenlet by ID key |
| `getFormScreenlet(key)` | Access a FormScreenlet (navigator) |
| `getButtonScreenlet(key)` | Access a ButtonScreenlet |
| `getTabScreenlet(key)` | Access a tab panel |
| `save()` | Click Save button |
| `getConfirmation().yes()` | Confirm dialog after Save |
| `getPageURL(pathKey)` | Build screen URL from path key |

### Page Object Lazy Loading Pattern

```java
// Screenlet cached on first access — avoids repeated DOM queries
public TableScreenlet getNominationsTable() {
    return nominationsTable = (nominationsTable == null ?
        getTableScreenlet(ADD_CARGO) : nominationsTable);
}
```

---

## Authentication

```gherkin
Given I login with "resttest" user and "BDgUcNbdPhfh$e5m#1014" password
```

**9 Test Users:**

| User | Role | Password |
|---|---|---|
| resttest | System admin/test | BDgUcNbdPhfh$e5m#1014 |
| testuser01 | Test User 1 | IfQOO#S1AYThsr1C |
| testuser02 | Fuel Team/Test User 2 | IfQOO#S2AYThsr2C |
| testuser03 | Test User 3 | IfQOO#S3AYThsr3C |
| zxc_byp_team_test_user | BYP Team | WHSlh(U1=pk*1!#DILS |
| zxc_byp_admin_test_user | BYP Admin | Zz'Uu.Lyy9H.`:qk0B]> |
| zxc_coal_term_test_user | Coal Terminal | jIWU&U^#2#qKd22w2 |
| coal_test_user | Coal Test | DF76qN^cIevRcmbs2 |
| sysadmin | System Admin | encrypted |

`LoginPage.java` clears fields before typing (handles browser autocomplete), enters credentials, clicks login button, waits for AJAX completion.

---

## Test Configuration (arquillian.xml)

```xml
Browser: Chrome (--start-maximized --disable-dev-shm-usage)
Remote: ${remotebrowser} → Selenium Grid at ${gridhubaddress}
Default URL: https://clp.non-prod.eg.qs.energycomponents.com/
UAT URL: https://uat.clp-nprod.ecaas.cloud/

Wait times (PROVEN for EC PrimeFaces):
  GUI wait: 10 seconds
  AJAX wait: 30 seconds
  Model wait: 60 seconds
  Guard wait: 60 seconds
  Page load: 180 seconds
  WebDriver wait: 180 seconds
```

---

## Test Tagging System

```gherkin
@LNG @LNGDocumentsReports
Feature: LNG Cargo Documents
  @GCCTA-1063
  Scenario: Generate LNG Cargo Documents
```

**Tag hierarchy:**
- `@LNG` / `@PGAS` / `@LGAS` / `@Coal` / `@ByP` / `@ULSD` — product line
- `@LNGDocumentsReports` / `@LNGPlanningScheduling` etc. — sub-area
- `@GCCTA-####` — Jira ticket number (finest grain)
- `@sanity` — quick health checks

**Test Runners:** 20+ runners — one per product+area combination:
```java
@CucumberOptions(tags = {"@LNGDocumentsReports"})
class testrunnerLNGDR {}

@CucumberOptions(tags = {"@GCCTA-1142"})
class Production {}  // Run single ticket
```

---

## Navigation Pattern (GenericSteps.java)

```java
// Step
@When("^I navigate to the \"([^\"]*)\" screen and enter navigation data$")
public void iNavigateToTheScreenAndEnterNavigationData(String screenName, DataTable dataTable)

// Flow:
// 1. Parse screen name against NavCache (ecurl.properties)
// 2. Navigate to URL via getPageURL()
// 3. Fill FormScreenlet navigator with DataTable values
// 4. Date resolution via TestHelper.resolveDate(map)
// 5. Wait for AJAX/jQuery completion
```

**Date resolution patterns:**
- `SYS.DATE` → today's date
- `SYS.DATE + 3` → today + 3 days
- `2024-06-01` → literal date

---

## Confirmation Dialog Pattern

```java
// ALWAYS after Save on a TableScreenlet that changes status/data
save();
getConfirmation().yes();  // handles modal "Are you sure?" dialog
```

**Critical for Robot Framework Phase 2:** EC shows confirmation dialogs after status changes. Must handle in Robot keywords.

---

## Checkbox Handling

```java
ECCheckboxCell checkBox = table.getCell(rowNo, "TRANSFER");
checkBox.setValue(ECCheckboxCell.ON);   // or ECCheckboxCell.OFF
save();
getConfirmation().yes();
```

---

## DataTable Parameterization Pattern

```gherkin
And I update the nomination info of cargo and save
  | Carrier | Cargo Status | Estimated Arrival |
  | VESSEL1 | Confirmed    | SYS.DATE + 7     |
```

```java
public void iUpdateTheNominationInfo(List<Map<String, String>> data) {
    for (Map<String, String> row : data) {
        String resolvedDate = TestHelper.resolveDate(row);
        table.getCell(rowIndex, columnName).setValue(resolvedDate);
    }
    save();
}
```

---

## Multi-User Workflow Pattern

Complex business processes span multiple user logins:

```gherkin
# User 1 creates
Given I login with "testuser01" user and password
When I create cargo...
And I logout

# User 2 verifies
Given I login with "testuser02" user and password
When I verify analysis data...
And I logout

# User 3 approves
Given I login with "testuser03" user and password
When I approve analysis...
```

---

## EC Screens Tested (40+)

**Planning & Scheduling:** Nomination Entry, Cargo Information, BL/MR Info, Berth Slot Calendar, Daily Entitlement, Scenario Forecast Manager

**Terminal Services:** Unload Info, Cargo Analysis, Daily Tank Data, Stream Sample Analysis, Demurrage, Cargo Activity Timesheet

**Procurement & Documents:** Cargo Document Parcel, Document Valid2, Document Transfer, Document Un-transfer, Document Booked, Invoice Verification (×4 variants)

**Pricing:** Forecast Price, Daily/Monthly Price Index, Price Calculations, Cargo Price List, Exchange Rates

**Configuration:** User Maintenance, Actor Maintenance, Company Master, Port Master, Bank Account

**Monitoring:** Application Server Health, Database Connection, Cluster Heartbeat, EC Version

---

## Key Page Objects

### CheckRulePage.java
```java
public static final String T_TABLE = "check_rules";
public static final String T_VARIABLE = "variables";
public static final String T_FUNC_PARAM = "function_param";
public static final String T_SUB_QUERY_VAR = "sub_query_var";
public static final String CHECK_NAME = "Check Name";
location = getPageURL("CTRL_CHECK_RULES");
```

### ValidationOverviewPage.java
```java
public static final String T_GROUPS = "groups";
public static final String T_LOGS = "logs";
public static final String RUN_ALL_BTN = "runAllButton";
public static final String NAV = "nav";
public static final String GROUP = "Group";
componentId = "DATA_VALIDATION_TTV";
```

---

## My Overall Rating: 7.5/10

**Areas below 9/10 scheduled for deep dive (ET-A to ET-E):**

| Session | Items | Focus |
|---|---|---|
| ET-A | ET06, ET07, ET12, RF01 | ectest-core, screenletmapping, checkbox, RF translation |
| ET-B | ET05, ET08, ET09 | 113 page objects + 90 step classes |
| ET-C | ET01, ET04, ET10, ET11 | Arquillian, Docker, step patterns |
| ET-D | ET15–ET20 | All business domain screens |
| ET-E | ET02, ET03, ET13, ET14 | Java/Maven/Grid/Reporting |

---

## What This Means for Robot Framework Phase 2

1. **Element IDs confirmed** — Java constants match DOM scan findings 100%
2. **runAllButton confirmed** — `groups:form:runAllButton` works
3. **AJAX wait values** — GUI=10s, AJAX=30s, Model=60s proven for EC
4. **Confirmation dialogs** — must handle after every Save
5. **Navigation pattern** — mirrors our `Search And Open Screen` keyword
6. **ECpedia pages mapped** — 158 pages indexed, relevant pages identified per session
