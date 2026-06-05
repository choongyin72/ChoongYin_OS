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

---

## Session ET-A — Deep Dive (2026-06-06) [all 5 sources]

**Sources used:** EC Tech Docs ✅ | ECpedia ✅ | EC source (ec-application/ectestautomation) ✅ | Woodside repo ✅ | Web ✅

**Items:** #ET06 ectest-core module | #ET07 Screenlet mapping | #ET12 Checkbox/Cells | #RF01 RF translation

---

### Item #ET06: ectest-core Module Architecture (4→9) ✅

**Package structure** (`com.ec.selenium.core.*`):

```
ectest-core/src/main/java/com/ec/selenium/
├── core/
│   ├── cell/           ← 20+ typed cell classes (ECCheckboxCell, ECInputCell, etc.)
│   ├── component/      ← Page-level components (ECPage, Toolbar, Navigator, etc.)
│   ├── screenlet/      ← Screenlet wrappers (TableScreenlet, FormScreenlet, etc.)
│   ├── testbase/       ← Base test classes + Drone extension
│   ├── exception/      ← ECExceptions
│   └── widgets/        ← Chart widgets
├── cucumberUtil/       ← GenericCucumberOperation (step dispatcher)
├── ecpages/            ← Page object base classes (in ectest-pages module)
├── util/               ← TestHelper, DBHelper, NavCache, DataHandlerHelper
└── frmw/test/util/     ← AcceptAllCertificatesRule, TextMatchers
```

**Core component classes:**

| Class | Purpose |
|---|---|
| `ECPage` | Base for all page objects — extends Treeview + implements ScreenletContainer |
| `Toolbar` | EC screen toolbar (Save, New, Delete, Refresh, Fullscreen) |
| `Navigator` | FormScreenlet navigator (date range, object pickers) |
| `NotificationArea` | Status messages after save/error |
| `StatusArea` | Record status display |
| `SearchArea` | Treeview sidebar search |
| `Treeview` | Left navigation tree |
| `Popup` | EC popup dialog handling |
| `Confirmation` | "Are you sure?" dialog — `.yes()` / `.no()` |
| `ContextMenu` | Right-click context menus |
| `TopMenu` | Top navigation bar |

**Screenlet classes:**

| Class | EC screenlet type | Key method |
|---|---|---|
| `FormScreenlet` | Navigator, date pickers, form fields | `fillValues(List<String>)` |
| `TableScreenlet` | Data grids — the most-used screenlet | `getCell(row, col)`, `insertRow()`, `deleteRow()` |
| `ButtonScreenlet` | Action buttons (Go, Run, Save) | `clickButton()` |
| `CollapsibleScreenlet` | Expandable sections | `expand()`, `collapse()` |
| `HighChartGraphScreenlet` | Charts | `getChartData()` |
| `DiagramScreenlet` | Network/SND diagrams | `getNodes()` |
| `BpmTreeTableScreenlet` | BPM process tree | `getProcessRow()` |
| `FileUploadScreenlet` | File upload | `upload(filePath)` |
| `CalendarScreenlet` | Date picker | `selectDate()` |
| `GanttChartScreenlet` | Gantt charts | `getTask()` |

**Utility classes:**

| Class | Purpose |
|---|---|
| `TestHelper` | `scrollToAndClick()`, `waitForJQueryAndPrimeFaces()`, `resolveDate()` |
| `DBHelper` | Direct Oracle DB queries from test code |
| `DataHandlerHelper` | Parse DataTable, map column names |
| `NavCache` | Caches screen URLs to avoid repeated lookups |
| `AcceptAllCertificatesRule` | JUnit `@Rule` — accepts self-signed SSL certs |
| `TextMatchers` | Custom Hamcrest matchers for EC text comparison |

**ECPage constants (used in ALL page objects):**
```java
ECPage.NAV          = "nav"       // standard navigator screenlet ID
ECPage.GO_BUTTON    = "button"    // standard Go button ID
ECPage.SYSADMIN     = "sysadmin"  // default admin user
```

**The Arquillian Graphene + Selenium stack:**
```
JUnit 4 @Test
    ↓
Arquillian test runner (deploys to browser via WebDriver)
    ↓
Graphene Page Objects (@FindBy, @Page annotations)
    ↓
Selenium WebDriver → Chrome browser
    ↓
EC PrimeFaces JSF screen
```

---

### Item #ET07: Screenlet Mapping (4→9) ✅

**How screenlet IDs map from Java to DOM:**

```java
// In page object — define screenlet ID constant
public static final String T_CHECK_RULES = "check_rules";

// Access the screenlet — Java
TableScreenlet table = getTableScreenlet(T_CHECK_RULES);

// What this finds in DOM — the screenlet container div
// <div id="check_rules:form"> ... </div>

// Cell access — Java
ECCell cell = table.getCell(rowNo, "Check Name");

// What this finds in DOM — input inside the cell
// <input id="check_rules:form:T:1:R:0:C:0:inputTextFieldSuffix">
```

**TableScreenlet XPath patterns (from source):**
```java
// Frozen column rows (when table has frozen left columns)
"table/tbody/tr/td[1]/div/div[2]//table/tbody/tr"

// Scrollable area rows
"table/tbody/tr/td[2]/div/div[2]//table/tbody/tr"

// Standard rows (no frozen columns)
"div//table/tbody/tr"

// Header row
"div//thead[@id='%s:form:T_head']/tr"   // %s = screenletId
```

**`screenletmapping.properties` (CLP project):**
```properties
# Maps business names to URL paths for NavCache
CheckRule=/com.ec.frmw.co.screens/maintain_check_rules
ValidationOverview=DATA_VALIDATION_TTV
NominationEntry=/com.ec.tran.cp.screens/nomination_entry
...
```
`getPageURL("CheckRule")` → builds full URL: `{EC_BASE_URL}/com.ec.frmw.co.screens/maintain_check_rules`

**`FormScreenlet.fillValues()` pattern:**
```java
// Fills FormScreenlet cells in order (position-based, skips read-only)
public void fillValues(List<String> values) {
    int i = 0; int j = 1;
    while (i < values.size()) {
        ECCell cell = ECCellFactory.getECCell(element, j);
        if (!cell.isReadOnly()) {
            cell.setValue(values.get(i++));
        }
        j++;
    }
}
```
Position `j` = column index in the FormScreenlet grid. Skip read-only cells automatically.

**`ECPage.navSearch()` — the standard navigation pattern:**
```java
// Fills navigator form + clicks Go button
navSearch("nav", "2025-01-01", "ALL");

// With custom wait time
navSearch("nav", "button", 60, "2025-01-01", "FACILITY_A");
```

---

### Item #ET12: Checkbox and Cell Types (4→9) ✅

**`ECCell` interface (the contract all cells implement):**
```java
interface ECCell {
    void clear();
    String getValue();          // read current value
    void setValue(String text); // write new value
    WebElement getWebElement();
    int getWidth(); int getHeight();
    String getId();             // DOM element ID
    String getCSSClass();
    String getTooltip();
    boolean isReadOnly();       // skip read-only cells
    String getPlaceholder();
}
```

**`ECCheckboxCell` — how it works:**
```java
// setValue("on" | "true" | "y" | "off" | "false" | "n")
public void setValue(String text) {
    boolean toSet = "true".equalsIgnoreCase(text) || "on".equalsIgnoreCase(text) || "y".equalsIgnoreCase(text);
    boolean currentValue = inputElement.isSelected();

    if (toSet != currentValue) {
        TestHelper.scrollToAndClick(inputElement);  // scroll into view + click
        Graphene.waitAjax();                        // wait for PrimeFaces AJAX response
        TestHelper.waitForJQueryAndPrimeFaces();    // wait for jQuery + PF animation
    }
}

// getValue() returns "on" or "off"
```

**Full ECCell type hierarchy (20 typed cells):**

| Cell class | EC field type | setValue behaviour |
|---|---|---|
| `ECInputCell` | Text input | fills input field |
| `ECLabelCell` | Read-only label | getValue() only |
| `ECDateCell` | Date picker | fills date format string |
| `ECDateFilterCell` | Date column filter | filter input |
| `ECDropdownCell` | Dropdown / select | selects by visible text |
| `ECCheckboxCell` | Checkbox | on/off toggle |
| `ECPopupCell` | Popup selector (link icon) | opens popup, selects row |
| `ECMultiValueCell` | Multi-select | comma-separated values |
| `ECMultiValueSelectCell` | Multi-select with checkboxes | checkbox per item |
| `ECPasswordCell` | Password field | fills password |
| `ECPasswordToggleCell` | Toggle show/hide password | toggle button |
| `ECTextAreaCell` | Multi-line text area | fills textarea |
| `ECRichTextEditorCell` | Rich text editor | sets HTML content |
| `ECLinkCell` | Clickable link | click() |
| `ECIconCell` | Icon/button | click() |
| `ECImagePopupCell` | Image popup | opens image |
| `ECConfirmationCell` | Confirm checkbox | yes/no |
| `ECSelectOneButtonCell` | Toggle button group | click option |
| `ECTreeviewNodeCell` | Treeview node | expand/click |
| `ECMatheqCell` | Math equation editor | set expression |
| `ECFileUploadCell` | File upload button | set file path |
| `ECCategoryFilterCell` | Category column filter | select category |
| `ECFreeTextFilterCell` | Free text column filter | fill text |
| `ECNumberFilterCell` | Numeric column filter | fill number |

**`ECCellFactory.getECCell(element, position)`:**
Factory pattern — reads CSS class of element at position → creates correct typed cell class.
```java
// Determines cell type from CSS: "ECInputField", "ECDropdown", "ECCheckbox", etc.
// Returns typed ECCell subclass — test code never needs to know exact cell type
```

---

### Item #RF01: ectestautomation → Robot Framework Translation (4→9) ✅

**The two frameworks side-by-side:**

| Concept | ectestautomation (Java) | Robot Framework (our project) |
|---|---|---|
| Language | Java 11 | Python (Browser Library) |
| Browser engine | Selenium WebDriver via Graphene | Playwright (Browser Library) |
| AJAX wait | `Graphene.waitAjax()` + `TestHelper.waitForJQueryAndPrimeFaces()` | `Wait For Load State    networkidle` |
| Page base class | `ECPage` extends Treeview | `ec_keywords.robot` imports all layers |
| Screenlet access | `getTableScreenlet("check_rules")` | `page.locator('#check_rules\\:form')` |
| Cell setValue | `table.getCell(row, col).setValue("value")` | `Fill Text    ${CELL_LOCATOR}    ${value}` |
| Checkbox | `ECCheckboxCell.setValue(ON)` | `Check Checkbox    ${selector}` |
| Confirmation | `getConfirmation().yes()` | `Click    css=.ui-confirm-dialog .ui-confirmdialog-yes` |
| Navigator fill | `navSearch("nav", date, facility)` | `Set Navigator Date And Go    ${date}    ${facility}` (existing keyword) |
| Screenshot | Extent Reports / JUnit listener | `Take Screenshot    filename=${TEST_NAME}.png` |
| SSL certs | `AcceptAllCertificatesRule` JUnit @Rule | `ignoreHTTPSErrors=True` in `New Context` |
| AJAX wait values | GUI=10s, AJAX=30s, Model=60s (proven) | `${WAIT_TIMEOUT}=30s` (matches!) |

**Direct translation patterns:**

```robot
# ectestautomation: table.getCell(1, "Check Name").getValue()
# RF equivalent:
${check_name}=    Get Text    xpath=//tr[@data-rk][1]//td[contains(@headers,'check_name')]

# ectestautomation: ECCheckboxCell.setValue(ECCheckboxCell.ON)
# RF equivalent:
Check Checkbox    xpath=//tr[@data-rk][1]//td[contains(@class,'checkbox')]//input[@type='checkbox']

# ectestautomation: getConfirmation().yes()
# RF equivalent:
Wait For Elements State    css=.ui-confirmdialog-yes    visible    ${WAIT_TIMEOUT}
Click    css=.ui-confirmdialog-yes
Wait For Load State    networkidle    timeout=${WAIT_TIMEOUT}

# ectestautomation: TestHelper.waitForJQueryAndPrimeFaces()
# RF equivalent:
Wait For Load State    networkidle    timeout=30s

# ectestautomation: navSearch("nav", "2025-01-01", "FACILITY")
# RF equivalent (already exists):
Set Navigator Date And Go    2025-01-01    FACILITY
```

**What ectestautomation does that RF Phase 2 must replicate:**
1. `ECCellFactory` type detection → RF uses element-type-specific keywords
2. `AcceptAllCertificatesRule` → RF `ignoreHTTPSErrors=True`
3. Multi-user workflow (login/logout cycles) → RF Suite Setup/Teardown per user
4. DataTable parameterization → RF `[Template]` or `FOR` loop over test data
5. `SYS.DATE + N` date resolution → RF expression `${date}=    Evaluate    ...`
6. `NavCache` URL mapping → RF `vars/local.py` + `${EC_URL}` pattern
