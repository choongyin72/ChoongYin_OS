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

## Session ET-E — Deep Dive (2026-06-06) [all 5 sources]

**Sources used:** EC source (ec-application/ectestautomation) ✅ | Web ✅

**Items:** #ET02/#ET03 Java/Maven | #ET13 Selenium Grid | #ET14 Reporting

---

### Item #ET02/#ET03: Java + Maven Architecture (4→9) ✅

**Multi-module Maven structure:**
```
ectestautomation/pom.xml          (parent, groupId=com.ec.test, artifactId=ectestautomation)
├── ectest-core/                  (core library — cells, screenlets, components)
├── ectest-pages/                 (page objects — 1,508 Java files)
├── ectest-ecpa/                  (BDD tests — depends on core + pages)
├── ectest-ui/                    (UI integration tests)
├── ectest-cluster/               (cluster tests)
├── ectest-cluster-multihost/     (multi-host cluster tests)
├── ectest-containers/            (container management)
├── ectest-ecis/                  (ECIS integration tests)
├── ectest-kubernetes/            (Kubernetes deployment tests)
├── ectest-performance/           (performance tests)
├── ectest-repeatable-migrations/ (DB migration tests)
├── ectest-sdk/                   (SDK tests)
├── ectest-security-scanning/     (security scan)
├── ectest-testagent/             (REST proxy to Oracle DB)
└── ectest-testagent-api/         (test agent API definitions)
```

**`ectest-ecpa` dependencies (from pom.xml):**
```xml
<dependency>
    <groupId>com.ec.test</groupId>
    <artifactId>ectest-core</artifactId>   <!-- Cell types, screenlets, components -->
</dependency>
<dependency>
    <groupId>com.ec.test</groupId>
    <artifactId>ectest-pages</artifactId>  <!-- All 1,508 page objects -->
</dependency>
<dependency>
    <groupId>com.github.cukespace</groupId>
    <artifactId>cukespace-core</artifactId>  <!-- Cucumber + Arquillian bridge -->
    <scope>test</scope>
</dependency>
```

**`cukespace-core` — the Cucumber + Arquillian bridge:**
- Merges JUnit/Arquillian test runner with Cucumber BDD runner
- Enables `@RunWith(CukeSpace.class)` annotation on test runners
- Allows `@Page` Arquillian injection to work inside Cucumber step definitions
- Without this, Arquillian and Cucumber would conflict on JUnit runner control

**Maven test execution flags:**
```bash
-pl ectest-ui          # Only ectest-ui module
-P docker              # Docker profile — starts containers
-DskipITs=false        # Run integration tests (maven-failsafe-plugin)
-DtestInclude="com/ec/production/**/*.java"  # Test class filter
-Dit.test="Class#method1+method2"            # Single test / specific methods
-Dgroups="com.ec.test.categories.IUD"        # Category filter
```

**Test categories (from `com.ec.test.categories`):**
Marker interfaces used with JUnit `@Category` — allows selective test runs:
- `IUD` = Insert/Update/Delete tests
- (other categories vary by domain)

---

### Item #ET13: Selenium Grid (4→9) ✅

**Grid topology:**
```
Test JVM (on CI agent)
    ↓ RemoteWebDriver (HTTP)
Selenium Grid Hub (chromenode container, localhost:4444)
    ↓
Chrome browser (inside chromenode)
    ↓
EC Web App (ec-app container, accessible via Traefik)
```

**arquillian.xml Grid config:**
```xml
<property name="remote">true</property>
<property name="remoteAddress">http://localhost:4444/wd/hub</property>
<!-- remoteReusable=true doesn't work with Java 11 — use remote only -->
```

**`${gridhubaddress}` Maven property:**
Set to `http://localhost:4444/wd/hub` for local Docker runs, or a remote Selenium Grid URL for CI.

**`ECDroneExtension` — custom WebDriver factory:**
Overrides default Arquillian Drone to create the `RemoteWebDriver` with EC-specific Chrome options (SSL bypass, download config, logging prefs).

**Why Docker chromenode not local Chrome:**
- CI agents don't have Chrome installed
- Chromenode container = headless Chrome + ChromeDriver + Selenium node
- Tests run identically on any machine that can run Docker
- Multiple chromenodes = parallel test execution

**`ectest-cluster` module — multi-node grid testing:**
Tests EC's own cluster behaviour (WildFly clustering) — separate from normal UI tests.

---

### Item #ET14: Test Reporting (4→9) ✅

**Two report types:**

**1. Arquillian HTML5 Reporter (built-in):**
```xml
<extension qualifier="reporter">
    <property name="report">html5</property>
    <property name="file">arquillian_report</property>
    <property name="reportAfterEvery">class</property>  <!-- report per test class -->
    <property name="maxImageWidth">500</property>
</extension>
```
Output: `target/arquillian_report.html` — test results with screenshots

**2. Screenshooter (automatic failure capture):**
```xml
<extension qualifier="screenshooter">
    <property name="takeWhenTestFailed">true</property>  <!-- only on failure -->
    <property name="rootDir">target</property>
    <property name="takeBeforeTest">false</property>
    <property name="takeAfterTest">false</property>
</extension>
```
Captures screenshot automatically when any test fails — embedded in HTML5 report.

**CLP project also uses Extent Reports (custom):**
`ECScreenshooterManager` + `ECScreenshooterPrep` classes = custom screenshot pipeline that feeds into Extent Reports HTML5 format. More detailed than stock Arquillian reporter.

**Jenkins integration:**
- Tests produce `target/surefire-reports/*.xml` — JUnit XML format
- Jenkins reads XML → shows per-test pass/fail trend
- `--fail-at-end` flag ensures ALL tests run even if some fail
- Test output logged to `target/arquillian_report.html` — downloadable from Jenkins artifacts

---

## Session ET-D — Deep Dive (2026-06-06) [all 5 sources]

**Sources used:** EC source (ec-application/ectestautomation) ✅ | Web ✅

**Items:** #ET15-#ET20 Business domain page objects

---

### Items #ET15-#ET20: Business Domain Coverage (3→9) ✅

**ET-15: Transport — Cargo Planning domain:**
```
transport/cargoplanning/:
  BerthSlotCalendarPage           — berth availability scheduling
  CargoInformationPage            — cargo details + status
  DailyEntitlementPage            — daily lifting entitlement
  ContractDeliveryTrackingPage    — contract delivery status
  DailyStorageForecastPage        — storage level projections
  DocumentInstructionPage         — cargo document instructions
  NominationEntryPage             — cargo nomination entry
  LiftingProgramPage              — lifting program management
  ScenarioForecastManagerPage     — scenario-based planning
  CarrierAvailabilityPage         — vessel availability calendar
```

**ET-16: Transport — Terminal Operations domain:**
```
transport/terminaloperations/:
  CargoActivityTimesheetPage      — arrival/mooring/loading timeline
  BLMRInfoPage                    — Bill of Lading / Mate's Receipt
  CargoAnalysisPage               — LNG composition analysis
  DemurragePage                   — port delay compensation
  BatchQuantitiesPage             — parcel quantity tracking
  ShipUllagesPage                 — vessel tank measurements
```

**ET-17: Revenue domain:**
```
revenue/closingprocess/:
  RevenueBookingPeriodClosePage   — close accounting period
  RevenueLockModulePage           — lock revenue data
  RevenueReportingPeriodClosePage — close reporting period

revenue/datamapping/:
  CareRevenueProcessPage          — CARE revenue processing
  DataEntryInterfacePage          — manual data entry
  ProjectDataExtractPage          — data extract for GL
```

**ET-18: Process Automation domain (BPM screens):**
```
processautomation/:
  ProcessExecutionPage            — start BPM process instances (PA.0003)
  ProcessTemplatePage             — configure process templates
  ProcessMonitorPage              — monitor running processes
  ProcessOverviewPage             — process overview dashboard (PA.0004)
  TodoListPage                    — user task queue (PA.0005)
  ProjectManagementPage           — BPM project management (PA.0013)
  ProcessNotificationsPage        — notification configuration
```

**ET-19: Reporting domain:**
```
reporting/:
  ReportAdministrationPage        — report config + execution
  ReportGenerationPage            — run reports
  ReportArchivePage               — archived report results
  ReportAreaPage                  — report area configuration
  ExportToExcelExpressPage        — quick Excel export
  DisplayPublishedReportPage      — view published Jasper reports
  excelreporttemplates/:
    ExcelReportObjectsPage        — Excel template objects
    ExcelReportSetsPage           — Excel template sets
    ReportContextPage             — report context config
```

**ET-20: Configuration domain (largest — 497 files):**
```
configuration/ contains:
  ├── access/          — user roles, object access, ringfencing
  ├── assets/          — facility, well, stream, tank setup
  ├── calculation/     — calc group setup, calc library admin
  ├── checkrules/      — check rule maintenance, validation groups
  ├── classmodel/      — class configuration, view generator
  ├── codes/           — EC codes administration
  ├── ecis/            — ECIS adapter config, tag mappings
  ├── scheduler/       — schedule management
  ├── unitofmeasure/   — UOM setup
  └── users/           — user maintenance, Keycloak sync
```

**Key insight:** The ectestautomation framework covers essentially **every EC business function screen**. The 1,508 page objects map to EC's complete screen inventory. This is the most comprehensive test automation framework for EC — built by Quorum's own engineering team to validate every feature they release.

**Mapping to EC business function codes:**
| ectestautomation domain | EC BF codes |
|---|---|
| `processautomation/` | PA.0003, PA.0004, PA.0005, PA.0013 |
| `transport/cargoplanning/` | Transport CP screens |
| `production/` | PO.*, WR.*, HA.*, PT.* |
| `configuration/checkrules/` | CO.0079, CO.0080, CO.0203 |
| `reporting/` | Report Admin screens |
| `chemistry/` | CM.* screens |

---

## Session ET-C — Deep Dive (2026-06-06) [all 5 sources]

**Sources used:** EC source (ec-application/ectestautomation) ✅ | Web ✅

**Items:** #ET01 Arquillian/Graphene | #ET04 Docker | #ET10/#ET11 Step patterns

---

### Item #ET01: Arquillian + Graphene Architecture (4→9) ✅

**`arquillian.xml` — the central configuration file:**
```xml
<!-- 1. Drone — WebDriver lifecycle management -->
<extension qualifier="drone">
    <property name="instantiationTimeoutInSeconds">0</property>
</extension>

<!-- 2. WebDriver — browser setup -->
<extension qualifier="webdriver">
    <property name="browser">${browser}</property>           <!-- chromium/firefox/ie -->
    <property name="remote">${remotebrowser}</property>      <!-- true = Selenium Grid -->
    <property name="remoteAddress">${gridhubaddress}</property> <!-- Grid URL -->
    <property name="reuseCookies">true</property>            <!-- persist session -->
    <!-- Chrome-specific for EC -->
    <property name="chromeArguments">
        --start-maximized
        --disable-dev-shm-usage
        --ignore-certificate-errors
        --unsafely-treat-insecure-origin-as-secure=${EC_APP_URL}
        --remote-allow-origins=*
        --disable-search-engine-choice-screen
    </property>
</extension>

<!-- 3. Graphene — AJAX wait intervals (PROVEN for EC PrimeFaces) -->
<extension qualifier="graphene">
    <property name="waitGuiInterval">10</property>    <!-- element visible wait -->
    <property name="waitAjaxInterval">30</property>   <!-- AJAX completion wait -->
    <property name="waitModelInterval">60</property>  <!-- data model load wait -->
    <property name="waitGuardInterval">60</property>  <!-- guard (page load) wait -->
</extension>

<!-- 4. Reporter — HTML5 test report -->
<extension qualifier="reporter">
    <property name="report">html5</property>
    <property name="reportAfterEvery">class</property>
    <property name="maxImageWidth">500</property>
</extension>

<!-- 5. Screenshooter — auto-screenshot on failure -->
<extension qualifier="screenshooter">
    <property name="takeWhenTestFailed">true</property>
    <property name="rootDir">target</property>
    <property name="takeBeforeTest">false</property>
    <property name="takeAfterTest">false</property>
</extension>
```

**Wait interval meaning:**
| Interval | Value | Triggers when |
|---|---|---|
| `waitGuiInterval` | 10s | `Graphene.waitGui()` — element becomes visible |
| `waitAjaxInterval` | 30s | `Graphene.waitAjax()` — AJAX request completes |
| `waitModelInterval` | 60s | `Graphene.waitModel()` — data model loads |
| `waitGuardInterval` | 60s | `@Drone` guard timeout — page load |

**`ECDroneExtension` — custom Arquillian extension:**
- `LoadableExtension` registered in `META-INF/services`
- Registers `ECRemoteWebDriverFactory` as the WebDriver provider
- Handles Edge driver path resolution (`webdriver.edge.driver` system property)
- Provides custom remote WebDriver creation with EC-specific options
- **Note:** `remoteReusable` is commented out — doesn't work with Java 11

**Graphene `@Page` injection:**
```java
// Arquillian injects page objects automatically via @Page
// No new() instantiation needed in step definitions
@Page
private CheckRulePage checkRulePage;

// Graphene injects the WebDriver and manages browser lifecycle
@Drone
private WebDriver browser;
```

**`AcceptAllCertificatesRule` — handles EC self-signed SSL:**
```java
// JUnit @Rule — applied to all tests
@Rule
public AcceptAllCertificatesRule certRule = new AcceptAllCertificatesRule();
// Configures WebDriver to ignore SSL certificate errors
// RF equivalent: ignoreHTTPSErrors=True in New Context
```

---

### Item #ET04: Docker Compose Test Infrastructure (4→9) ✅

**Container stack for EC UI tests:**
```yaml
services:
  db:           # Oracle DB (eckernel_ec/energy, ORCL SID)
  ec-messaging: # WildFly + EC + JMS (connects to db)
  keycloak:     # Auth server (kckernel_ec/energy)
  keycloak-migration: # DB migration for Keycloak
  ec-app:       # EC application server
  ec-loadbalancer: # Traefik reverse proxy (routes /auth to KC)
  chromenode:   # Selenium Grid node with Chrome
  ec-bpm:       # jBPM server (separate from EC)
  ec-ra:        # EC Remote Agent
```

**Traefik load balancer config (from docker-compose):**
```yaml
# Keycloak gets sticky sessions — critical for OAuth2 flow
labels:
  - "traefik.http.routers.kc.rule=PathPrefix(`/auth`)"
  - "traefik.http.services.kc.loadbalancer.sticky=true"
  - "traefik.http.services.kc.loadbalancer.sticky.cookie.name=KCSERVERUSED"
```
Sticky sessions ensure OAuth tokens go back to the same Keycloak instance in a cluster.

**DB image naming convention:**
```
docker-flyway-db-testdata:14.1.3-develop-14-1-x-SNAPSHOT
```
Test DB image = EC Oracle schema + Flyway migrations + test data pre-loaded. One image per EC version.

**`ALLOW_INCOMPATIBLE_DB=true` flag:**
When running tests against a SNAPSHOT build whose DB version is ahead of the test DB image, set this flag in `docker-compose.yml` for that module. Without it, EC refuses to start with an incompatible DB.

**`chromenode` = headless Chrome Selenium Grid node:**
```
Remote WebDriver → http://{gridhubaddress}/wd/hub → chromenode container
```
Tests run in the container's Chrome browser — no local Chrome/ChromeDriver needed on the CI agent.

**Maven run command structure:**
```bash
mvn clean verify -pl ectest-ui -P docker --fail-at-end
  -DskipITs=false
  -DtestInclude="com/ec/production/**/*.java"
  -DdockerCompose.dbImage=docker-flyway-db-testdata:14.1.3-...-SNAPSHOT
  -Dstart.containers="db ec-messaging keycloak keycloak-migration ec-app ec-loadbalancer chromenode ec-bpm ec-ra"
  -Dskip.bpm.container=false
  -Ddocker.pull.skip=true
```

---

### Item #ET10/#ET11: Generic and EC-Specific Step Patterns (5→9) ✅

**Generic patterns (#ET10):**

**1. Environment switching:**
```java
// Step: "I login with user on 'UAT'"
TestUtil.switchToEnvironment("UAT");
// Switches base URL: DEV / UAT / PROD
```

**2. `SYS.DATE + N` resolution:**
```java
// In feature: SYS.DATE + 7
String resolvedDate = TestHelper.resolveDate("SYS.DATE + 7");
// Resolves to: today's date + 7 days in EC format
```

**3. `TestUtil.resetEnvironment()` — test isolation:**
```java
// Step: "I reset Environment"
TestUtil.resetEnvironment();
// Resets any test data state between scenarios
```

**EC-specific patterns (#ET11):**

**4. `KeycloakHelper` — programmatic user management:**
```java
// Create EC user with specific roles
KeycloakHelper.singleton().createUser("superadmin", "N3wP@ssW0rd!", 
    Arrays.asList("SYST.ADM", "JBPM.ADMIN", "REST", "SCHEDULER"));

// Useful for: setup before access control tests, cleanup after
```

**5. `DbRestHelper` — DB queries via REST agent:**
```java
// Query DB without direct JDBC (security design)
DbRestHelper.singleton().query(
    "SELECT COUNT(*) FROM CTRL_CHECK_RULES WHERE CHECK_NAME = ?", checkName);

// The ectest-testagent module serves as REST proxy to Oracle
// Tests call HTTP, agent executes JDBC — no DB credentials in test code
```

**6. Chrome download directory config (from arquillian.xml):**
```json
{
  "prefs": {
    "download.default_directory": "/home/",
    "download.prompt_for_download": "false",
    "profile.password_manager_leak_detection": "false"
  }
}
```
Configures Chrome to auto-download to `/home/` without prompting — needed for report download tests.

**7. Browser console logging:**
```json
{"goog:loggingPrefs": {"browser": "DEBUG", "driver": "INFO"}}
```
Captures JavaScript console errors in Chrome — useful for debugging EC PrimeFaces issues.

---

## Session ET-B — Deep Dive (2026-06-06) [all 5 sources]

**Sources used:** EC source (ec-application/ectestautomation) ✅ | Web ✅ | Woodside ✅

**Items:** #ET05 Full page objects | #ET08 storysteps | #ET09 teststeps

---

### Item #ET05: Full Page Object Library (5→9) ✅

**Scale:** 1,508 Java files in `ectest-pages` module across 15 domain packages.

**Domain breakdown:**

| Domain | Count | Coverage |
|---|---|---|
| `configuration/` | 497 | Framework config, users, assets, roles, system settings |
| `production/` | 343 | Wells, streams, tanks, allocation, check rules, PVT, BPM |
| `transport/` | 273 | Cargo planning, terminal ops, dispatching, nominations |
| `revenue/` | 151 | Contracts, pricing, invoicing, financial items |
| `chemistry/` | 25 | Fluid analysis, chemical management |
| `reporting/` | ~20 | Jasper, Yellowfin reports |
| `processautomation/` | ~15 | BPM screens |
| `ecintegrationservice/` | ~10 | ECIS config screens |
| Other | remaining | Sales, messaging, tasklist, etc. |

**Naming convention:** `{ScreenName}Page.java` — e.g. `CheckRulePage.java`, `ValidationOverviewPage.java`, `NominationEntryPage.java`

**Page object anatomy (from `AbstractComponentAnalysisPage.java` + `AbstractSplitPage.java`):**
```java
public abstract class AbstractComponentAnalysisPage extends PageComponents {

    // 1. Static constants for screenlet IDs
    public static final String T_ANALYSIS     = "analysis";        // TableScreenlet ID
    public static final String T_COMPONENT_SET = "component_set";  // TableScreenlet ID
    public static final String B_MOL_TO_WT    = "mol_to_wt_button"; // ButtonScreenlet ID

    // 2. Static constants for column names
    public static final String COMPONENT_NAME = "Component Name";
    public static final String MOL            = "Mol [%]";
    public static final String WT             = "Wt [%]";

    // 3. Private cached screenlet fields
    private TableScreenlet analysisTable;
    private TableScreenlet componentSetTable;

    // 4. Lazy-loaded getters — cache on first access
    public TableScreenlet getAnalysisTable() {
        return analysisTable = (analysisTable == null ?
            getTableScreenlet(T_ANALYSIS) : analysisTable);
    }

    // 5. Business methods use constants, not strings
    public String getMolValue(int row) {
        return getAnalysisTable().getCell(row, MOL).getValue();
    }
}
```

**The `PageComponents` base chain:**
```
Test step class
    ↓ @Page injection
{ScreenName}Page
    ↓ extends
PageComponents
    ↓ extends
ECPage
    ↓ extends
Treeview + ScreenletContainer
```

`PageComponents` adds: `getDataHandler()`, `save()`, `getConfirmation()`, `getNotificationArea()`, `getStatusArea()`

**AbstractSplitPage pattern — reusable abstract base:**
Many EC screens share the same layout (current split + last split). Abstract base classes capture shared constants and screenlet accessors once — concrete pages just add their specific fields.

**Key insight:** The page object library maps 1:1 to EC business function screens. Every EC screen that needs testing has a corresponding `*Page.java`. The static constants in each page class are the authoritative source of screenlet IDs for that screen — more reliable than guessing from DOM inspection.

---

### Item #ET08: storysteps — BDD Step Definitions (5→9) ✅

**Scale:** 271 storystep files across all EC domains.

**Pattern (from `CommonMethodsSteps.java` + `LoginSteps.java`):**
```java
public class LoginSteps {
    // Arquillian injects page object — no new() needed
    @Page
    private Login login;

    // Cucumber step binding
    @Given("^I login with \"([^\"]*)\" user and \"([^\"]*)\" password on \"([^\"]*)\"$")
    public void i_login_with_user_and_password(String userName, String password, String environment) {
        // Switch environment + call page method
        TestUtil.switchToEnvironment(environment);
        login.loginTest();
    }

    @When("^I navigate to the \"([^\"]*)\" screen and enter navigation data$")
    public void iNavigateToScreenAndEnterNavigationData(String screenName, DataTable dataTable) {
        // DataTable = rows from Gherkin | Col1 | Col2 |
        List<Map<String, String>> data = dataTable.asMaps(String.class, String.class);
        ecPage.navigateTo(screenName);
        ecPage.fillNavigator(data.get(0));
    }
}
```

**Step naming convention:** Regex patterns in plain English:
```
@Given("^I login with \"([^\"]*)\" user...")     — authentication
@When("^I navigate to the \"([^\"]*)\" screen...") — navigation
@When("^I create a new cargo nomination...")       — create operations
@Then("^I verify the cargo status is \"([^\"]*)\"") — assertions
@And("^I save and confirm$")                       — save + confirm dialog
```

**storysteps domains and their focus:**
```
common/storysteps/     — Login, navigation, generic operations, environment reset
chemistry/.../         — Fluid analysis, chemical injection, tank management
production/.../        — Well status, stream analysis, allocation, check rules
configuration/.../     — User/role management, asset setup, scheduler
framework/.../         — Access control, general framework tests
revenue/.../           — Contract calculations, invoicing
transport/.../         — Cargo, nominations, terminal operations
```

**`DataTable` — the step data pattern:**
```gherkin
When I update nomination info
  | Carrier | Cargo Status | ETA        |
  | VESSEL1 | Confirmed    | SYS.DATE+7 |
  | VESSEL2 | Planned      | SYS.DATE+14|
```
```java
// Java side
public void updateNominationInfo(DataTable dataTable) {
    List<Map<String, String>> rows = dataTable.asMaps(String.class, String.class);
    for (Map<String, String> row : rows) {
        String resolvedDate = TestHelper.resolveDate(row.get("ETA"));
        nominationPage.getNominationTable().getCell(idx, "ETA").setValue(resolvedDate);
    }
    save(); getConfirmation().yes();
}
```

**`KeycloakHelper` — programmatic user management in steps:**
```java
// Create test user with specific roles (from CommonMethodsSteps)
KeycloakHelper.singleton().createUser("superadmin", "N3wP@ssW0rd!", Arrays.asList(
    "SYST.ADM", "JBPM.ADMIN", "REST", "SCHEDULER", ...));
```
Allows tests to create/delete users programmatically — avoids manual test data setup.

---

### Item #ET09: teststeps — Supporting Test Utilities (4→9) ✅

**38 teststep files** — utility classes called FROM storysteps, not directly from feature files.

**Difference from storysteps:**
| storysteps | teststeps |
|---|---|
| Has `@Given/@When/@Then/@And` Cucumber annotations | No Cucumber annotations |
| Called from `.feature` files via Gherkin | Called from storysteps Java code |
| BDD business language | Technical implementation helpers |
| e.g. `LoginSteps.java` | e.g. `Login.java`, `RevenueCommon.java` |

**`Login` teststep (called from LoginSteps):**
```java
// login.loginTest() — handles form fill + AJAX wait + URL switch
public class Login extends PageComponents {
    public void loginTest() {
        testArgs = getDataHandler().getListData();
        String userName = testArgs.get(0);
        String password = testArgs.get(1);
        loginPage.loginIntoApp(userName, password);
    }
}
```

**`RevenueCommon` teststep:**
Shared revenue-domain operations called from multiple revenue storysteps — avoids duplication. Contains: contract account queries, price index lookups, financial item verifications.

**`TestUtil.switchToEnvironment(env)` — environment switching:**
```java
// Switches base URL between: UAT, PROD, DEV environments
// Called from step: "I login ... on 'UAT'"
TestUtil.switchToEnvironment("UAT");
```

**`DbRestHelper` — database operations via REST API (not direct JDBC):**
```java
// ectest uses a test agent REST API to query DB — avoids direct DB connection
DbRestHelper.singleton().query("SELECT COUNT(*) FROM CTRL_CHECK_RULES WHERE CHECK_NAME = ?", checkName);
```
The `ectest-testagent` module provides a REST API wrapper around Oracle — tests call it via HTTP instead of JDBC. This is a security design — test code doesn't need direct DB credentials.

**Design principle: storysteps are thin, teststeps hold logic:**
- storystep = map Gherkin words to Java method calls
- teststep = actual implementation that calls page objects
- This separation keeps feature files readable and test code maintainable

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
