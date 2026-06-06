# Tools Deep Dive — Robot Framework, Playwright, JasperReports
**Date:** 2026-06-05
**Target:** Fundamental → Expert mastery for production use

---

## SESSION RF-1: Robot Framework Foundations

### What Robot Framework Is

Robot Framework is a **Python-based, keyword-driven automation framework** for:
- Acceptance testing (ATDD)
- Browser automation (web testing)
- API testing
- RPA (Robotic Process Automation)
- Any system that can be driven by keywords

**Core principle:** Separate TEST LOGIC (what to test) from TEST IMPLEMENTATION (how to do it).

---

### Four-Layer Architecture

```
Layer 1: TEST DATA (.robot files)
  — Test cases, keywords, variables, settings
  — Human-readable syntax
         ↓
Layer 2: RF CORE ENGINE
  — Parses test data
  — Executes keywords in order
  — Generates reports/logs
         ↓
Layer 3: LIBRARIES
  — Browser (Playwright) — web automation
  — Collections, String, Process — built-in
  — Custom Python libraries
         ↓
Layer 4: SYSTEM UNDER TEST
  — EC Web App, REST API, DB, etc.
```

---

### .robot File Structure — Five Sections

```robot
*** Settings ***
Documentation     What this file does
Library           Browser                    # import library
Resource          ../../resources/ec_keywords.robot   # import shared keywords
Suite Setup       Suite Setup Steps          # runs before ALL tests in suite
Suite Teardown    Close Browser              # runs after ALL tests in suite
Test Setup        ...                        # runs before EACH test
Test Teardown     ...                        # runs after EACH test

*** Variables ***
${URL}            https://app-plutodev.woodside-pluto.tieto-og.cloud/
${HEADLESS}       False
@{LIST_VAR}       item1    item2    item3    # list variable
&{DICT_VAR}       key1=val1    key2=val2    # dict variable

*** Test Cases ***
TC01 Verify Something
    [Documentation]    What this test does
    [Tags]    smoke    critical
    [Setup]    Some Setup Keyword
    Open EC Application    ${URL}
    Login    sysadmin    Sysadmin@01
    Should Be Equal    ${result}    PASS

*** Keywords ***
My Custom Keyword
    [Documentation]    What this keyword does
    [Arguments]    ${arg1}    ${arg2}=default_value
    Log    Doing something with ${arg1}
    RETURN    ${result}

*** Comments ***
# Anything here is ignored
```

---

### Variable Types

| Syntax | Type | Example |
|---|---|---|
| `${VAR}` | Scalar (string/number/object) | `${URL}`, `${COUNT}` |
| `@{LIST}` | List | `@{BROWSERS}    chrome    firefox` |
| `&{DICT}` | Dictionary | `&{USER}    name=admin    pass=secret` |
| `${VAR}[0]` | List index | `${BROWSERS}[0]` → chrome |
| `${VAR}[key]` | Dict key | `${USER}[name]` → admin |

**Variable scopes:**
- `${VAR}` inside keyword = local
- `Set Suite Variable    ${VAR}    value` = suite-wide
- `Set Global Variable    ${VAR}    value` = global across all suites

---

### Keyword Types

**1. Built-in keywords** (always available):
```robot
Log           This is a message
Should Be Equal    ${actual}    ${expected}
Should Contain    ${text}    substring
Run Keyword If    condition    Keyword Name    args
Wait Until Keyword Succeeds    3x    1s    Flaky Keyword
```

**2. Library keywords** (from imported libraries):
```robot
# Browser Library (Playwright)
New Browser       chromium    headless=False
New Context       ignoreHTTPSErrors=True
New Page          ${URL}
Click             id=button
Fill Text         id=username    sysadmin
Type Text         id=searchBox    text    delay=50ms
Wait For Load State    networkidle    timeout=30s
Take Screenshot   filename=evidence.png
```

**3. User-defined keywords** (in .robot or .resource files):
```robot
*** Keywords ***
Login To EC
    [Arguments]    ${username}    ${password}
    Fill Text    id=username    ${username}
    Fill Text    id=password    ${password}
    Click        id=kc-login
    Wait For Load State    networkidle    timeout=60s
```

---

### Resource Files — Shared Keywords

Resource files (`.resource` or `.robot`) hold reusable keywords shared across test suites:

```robot
# resources/keywords/ec_browser.robot
*** Settings ***
Library    Browser

*** Keywords ***
Open EC Application
    [Arguments]    ${url}    ${headless}=False
    IF    '${headless}' == 'True'
        New Browser    chromium    headless=True
        New Context    ignoreHTTPSErrors=True    viewport={"width": 1920, "height": 1080}
    ELSE
        ${args}=    Create List    --start-maximized
        New Browser    chromium    headless=False    args=${args}
        New Context    ignoreHTTPSErrors=True    viewport=${None}
    END
    New Page    ${url}
```

**Import in test file:**
```robot
*** Settings ***
Resource    ../../resources/keywords/ec_browser.robot
```

---

### EC Project — Real Layered Architecture (from existing project)

The EC automation project uses a **9-layer keyword architecture**:

```
ec_keywords.robot (AGGREGATOR — test files import only this)
    ├── Layer 1: ec_browser.robot      — Browser launch, Login, Maximise Screen
    ├── Layer 2: ec_navigation.robot   — Search And Open Screen (sidebar treeview)
    ├── Layer 3: ec_navigator.robot    — Set Navigator Date And Go, Click Go Button
    ├── Layer 4: ec_toolbar.robot      — Save, Refresh, New, Delete, Fullscreen
    ├── Layer 5: ec_data_table.robot   — Wait For Data Table, row operations
    ├── Layer 6: ec_form_fields.robot  — Get/Set field values, field colours
    ├── Layer 7: ec_status_area.robot  — Status area tabs, Record Status
    ├── Layer 8: ec_verification.robot — Verify field data across all rows
    └── Layer 9: ec_filters.robot      — Column filter toggle (hamburger menu)
```

**Rule:** Test files only import `ec_keywords.robot` — never import individual layers directly.

---

### Tags — Test Organisation

```robot
TC01 Verify Something
    [Tags]    smoke    critical    unit    strm_comp

# Run only smoke tests:
robot --include smoke tests/

# Run all except slow tests:
robot --exclude slow tests/

# Run by multiple tags:
robot --include smoke AND critical tests/
```

**EC project tag conventions:**
- `unit` = DB-level verification (no browser)
- `system` = EC Web App UI test
- `ui` = browser interaction required
- `critical` / `high` / `medium` = severity
- Domain tags: `strm_comp`, `tank`, `strm_analysis`

---

### Control Flow

```robot
# IF/ELSE
IF    '${status}' == 'PASS'
    Log    Test passed
ELSE IF    '${status}' == 'SKIP'
    Log    Test skipped
ELSE
    Fail    Unexpected status: ${status}
END

# FOR loop
FOR    ${item}    IN    @{LIST}
    Log    Processing ${item}
END

# WHILE loop (RF 5+)
WHILE    ${counter} < 10
    ${counter}=    Evaluate    ${counter} + 1
END

# TRY/EXCEPT (RF 5+)
TRY
    Click    id=button
EXCEPT    ElementNotFound*
    Log    Button not found, skipping
END
```

---

### Test Templates — Data-Driven Testing

```robot
*** Test Cases ***
TC_Data_Driven
    [Template]    Verify Check Rule
    PHD_STRM_COMP_MOL_PCT_VAL1    RV_STRM_COMP_ANALYSIS    ERROR
    PHD_STRM_COMP_WT_PCT_VAL1     RV_STRM_COMP_ANALYSIS    ERROR
    PHD_STRM_ANALYSIS_DENSITY_VAL1    RV_STRM_ANALYSIS    ERROR

*** Keywords ***
Verify Check Rule
    [Arguments]    ${name}    ${table}    ${severity}
    # ... verification logic
```

---

### Running Robot Framework

```bash
# Run all tests
robot tests/

# Run specific file
robot tests/validation/issue_1052_check_rules.robot

# Run with variables
robot --variable URL:https://app-plutodev.woodside-pluto.tieto-og.cloud/ tests/

# Run with variable file
robot --variablefile config/environments/plutodev.yaml tests/

# Run only tagged tests
robot --include smoke tests/

# Output to specific directory
robot --outputdir results/ tests/

# Parallel execution (pabot)
pabot --processes 4 tests/
```

---

### Reports and Logs

After each run RF generates:
- `output.xml` — raw results (machine-readable)
- `log.html` — detailed execution log with screenshots
- `report.html` — summary report

```bash
# Combine multiple output.xml files
rebot results/output1.xml results/output2.xml
```

---

### Best Practices (Expert Level)

1. **Keyword names read like sentences:** `Verify Check Rule Exists In Database` not `verify_rule`
2. **One assertion per test** — easier to diagnose failures
3. **No hardcoded waits** — use `Wait For Load State`, `Wait For Elements State`, not `Sleep`
4. **Explicit teardown** — always close browser even if test fails
5. **Externalize all config** — URLs, credentials in YAML config files
6. **Tags over folders** — organise by tags, not by directory structure alone
7. **Document everything** — `[Documentation]` on every keyword and test
8. **Max 20 lines per keyword** — if longer, split into sub-keywords
9. **Variable files for locators** — don't embed selectors in test files

---

## SESSION RF-2 + PW-1: Browser Library (Playwright) in Robot Framework

### Why Browser Library over SeleniumLibrary

| Feature | SeleniumLibrary | Browser Library (Playwright) |
|---|---|---|
| Speed | Slow (HTTP-based WebDriver) | Fast (WebSocket direct API) |
| Auto-wait | Manual `Sleep` / `Wait Until` needed | Built-in auto-waiting |
| New browser session | Seconds | **< 10 milliseconds** |
| Network interception | No | Yes |
| Shadow DOM | Poor | Good |
| PrimeFaces AJAX | Unreliable timing | Reliable with `networkidle` |
| EC project uses | — | **✅ Browser Library** |

**The EC project already uses Browser Library** — `Library    Browser` in all keyword files.

---

### Browser Library Core Concepts

**Three-level hierarchy:**
```
Browser (chromium/firefox/webkit)
    └── Context (isolated session — cookies, localStorage isolated)
        └── Page (individual tab/window)
```

```robot
# Full setup
New Browser    chromium    headless=False
New Context    ignoreHTTPSErrors=True    viewport={"width": 1920, "height": 1080}
New Page       ${URL}

# Fast isolated session (< 10ms)
New Context    ignoreHTTPSErrors=True    # new context = clean session instantly
New Page       ${URL}
```

---

### Playwright Selectors — Priority Order

| Type | Syntax | Example | When to use |
|---|---|---|---|
| ID | `id=value` | `id=username` | Best — stable, unique |
| CSS | `css=.class` | `css=span.ui-icon-seek-end` | When ID not available |
| XPath | `xpath=//tag[@attr='val']` | `xpath=//label[contains(@class,'tv-link')]` | Complex conditions |
| Text | `text=Click Me` | `text=Go...` | Button text |
| Data attribute | `data-testid=btn` | `data-rk=row1` | EC `data-rk` rows |

**EC-specific patterns:**
```robot
# PrimeFaces sidebar search
${SEARCH_INPUT}    xpath=//input[@id='menu:searchForm:searchTxt']

# EC treeview link click
Click    xpath=//label[contains(@class,'tv-link') and normalize-space(.)='${screen_name}']

# EC table row by data-rk attribute
${ROW}    tr[data-rk='${row_key}']

# EC pagination — last page
Click    css=span.ui-icon-seek-end
```

---

### Key Browser Library Keywords

```robot
# Navigation
New Page          ${URL}
Go To             ${URL}
Reload

# State waiting (CRITICAL for PrimeFaces AJAX)
Wait For Load State    domcontentloaded    timeout=30s
Wait For Load State    networkidle         timeout=60s    # wait for all AJAX to settle

# Element state
Wait For Elements State    ${LOCATOR}    visible    timeout=15s
Wait For Elements State    ${LOCATOR}    enabled    timeout=10s
Wait For Elements State    ${LOCATOR}    detached   timeout=10s    # wait for overlay to disappear

# Interaction
Click           ${LOCATOR}
Fill Text       ${LOCATOR}    ${value}          # clears first, then types
Type Text       ${LOCATOR}    ${value}    delay=50ms    # types char by char — USE FOR AJAX search
Clear Text      ${LOCATOR}
Select Options By    ${LOCATOR}    value    ${option}
Check Checkbox  ${LOCATOR}
Uncheck Checkbox    ${LOCATOR}
Hover           ${LOCATOR}
Press Keys      ${LOCATOR}    Enter

# Reading
${text}=    Get Text        ${LOCATOR}
${value}=   Get Property    ${LOCATOR}    value
${attr}=    Get Attribute   ${LOCATOR}    data-rk
${count}=   Get Element Count    ${LOCATOR}
${visible}= Run Keyword And Return Status    Wait For Elements State    ${LOCATOR}    visible    timeout=3s

# Screenshots
Take Screenshot    filename=evidence.png           # saves to results/browser/screenshot/
Take Screenshot    filename=EMBED                  # embeds in log.html

# JavaScript execution
${result}=    Execute JavaScript    return document.title
Execute JavaScript    window.scrollTo(0, 0)
```

---

### PrimeFaces/EC-Specific Patterns

```robot
# ALWAYS wait for networkidle after clicking Go/Save/actions that trigger AJAX
Click    ${GO_BUTTON}
Wait For Load State    networkidle    timeout=30s

# ALWAYS use Type Text (not Fill Text) for search fields — PrimeFaces triggers on keyup
Type Text    ${SEARCH_INPUT}    ${screen_name}    delay=50ms

# Wait for PrimeFaces overlay spinner to disappear before interacting
Wait For Elements State    css=.ui-blockui-overlay    hidden    timeout=30s

# Handle PrimeFaces dialog
Wait For Elements State    css=.ui-dialog    visible    timeout=10s
Click    css=.ui-dialog .ui-button-text

# EC element ID pattern: {screenletId}:form:{elementId}
# Check rules filter field:
Fill Text    id=check_rules:form:T:sfilter0_ft_filter    ${filter_value}
```

---

### Python Integration in Robot Framework

```robot
# Run Python command and capture result
${result}=    Run Process
...    py    -c
...    import oracledb; conn=oracledb.connect(user='${DB_USER}',password='${DB_PASS}',dsn='${DB_URL}'); cur=conn.cursor(); cur.execute("SELECT COUNT(*) FROM CTRL_CHECK_RULES WHERE CHECK_NAME=:n",n='${name}'); cnt=cur.fetchone()[0]; cur.close(); conn.close(); print('PASS' if cnt>0 else 'FAIL')
...    stdout=PIPE    stderr=PIPE
RETURN    ${result.stdout.strip()}

# Custom Python library (better for complex logic)
# libraries/ECDatabase.py:
# class ECDatabase:
#     def query_check_rule(self, check_name): ...
```

---

### EC Project File Structure — Best Practice

```
AutomationTest/
├── config/
│   └── environments/
│       ├── plutodev.yaml          # COPS DEV environment
│       └── corp_sandbox.yaml      # Internal sandbox
├── libraries/
│   └── ECDatabase.py              # Custom Python library for DB operations
├── resources/
│   ├── ec_keywords.robot          # Aggregator — imports all layers
│   └── keywords/
│       ├── ec_browser.robot       # Layer 1: Browser/Login
│       ├── ec_navigation.robot    # Layer 2: Screen navigation
│       ├── ec_navigator.robot     # Layer 3: Navigator/date
│       ├── ec_toolbar.robot       # Layer 4: Toolbar actions
│       ├── ec_data_table.robot    # Layer 5: Table operations
│       ├── ec_form_fields.robot   # Layer 6: Form fields
│       ├── ec_status_area.robot   # Layer 7: Status area
│       ├── ec_verification.robot  # Layer 8: Data verification
│       └── ec_filters.robot       # Layer 9: Column filters
├── tests/
│   ├── smoke/                     # Quick health checks
│   ├── validation/                # Check rule + data validation tests
│   ├── configuration/             # EC configuration tests
│   ├── transaction/               # Business transaction tests
│   └── action/                    # Business action tests
└── results/
    └── browser/
        └── screenshot/            # Test evidence screenshots
```

---

### Advanced: Custom Python Library

```python
# libraries/ECDatabase.py
import oracledb

class ECDatabase:
    """Custom RF library for EC Oracle DB operations."""

    ROBOT_LIBRARY_SCOPE = 'SUITE'  # one instance per test suite

    def __init__(self, dsn, user, password):
        self.conn = oracledb.connect(user=user, password=password, dsn=dsn)

    def query_check_rule_count(self, check_name, table_id=None):
        """Returns count of matching check rules."""
        sql = "SELECT COUNT(*) FROM TV_CTRL_CHECK_RULES WHERE CHECK_NAME = :n"
        params = {'n': check_name}
        if table_id:
            sql += " AND TABLE_ID = :t"
            params['t'] = table_id
        cur = self.conn.cursor()
        cur.execute(sql, params)
        count = cur.fetchone()[0]
        cur.close()
        return count

    def check_rule_should_exist(self, check_name):
        """Fails test if check rule does not exist."""
        count = self.query_check_rule_count(check_name)
        if count == 0:
            raise AssertionError(f"Check rule '{check_name}' not found in DB")
```

```robot
# Using custom library:
*** Settings ***
Library    libraries/ECDatabase.py    ${DB_URL}    ${DB_USER}    ${DB_PASS}

*** Test Cases ***
TC01 Check Rule Exists
    Check Rule Should Exist    PHD_STRM_COMP_MOL_PCT_VAL1
```

---

## SESSION JR-1: JasperReports 7.0.3+ Foundations

### What JasperReports Is

JasperReports is an **open-source Java reporting engine** that:
- Takes a JRXML template + data source → generates PDF, Excel, HTML, CSV
- Oracle DB → JDBC data source → SQL query → formatted report
- Used in EC for all Jasper-based reports (deployed as `.jasper` compiled files)

**Two components:**
1. **Jasper Studio 7.0.3+** — IDE (Eclipse-based) for designing JRXML templates visually
2. **JasperReports Library 7.0.3+** — Java engine that compiles and fills reports

---

### JRXML File Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jasperReport xmlns="http://jasperreports.sourceforge.net/jasperreports"
              name="EC_Daily_Production"
              pageWidth="595" pageHeight="842"
              columnWidth="535" leftMargin="30" rightMargin="30"
              topMargin="20" bottomMargin="20">

    <!-- 1. Parameters — passed from outside at runtime -->
    <parameter name="P_DAYTIME" class="java.util.Date">
        <defaultValueExpression><![CDATA[new java.util.Date()]]></defaultValueExpression>
    </parameter>
    <parameter name="P_OBJECT_ID" class="java.lang.String"/>

    <!-- 2. Query — SQL against Oracle DB -->
    <queryString language="SQL">
        <![CDATA[
        SELECT o.object_code, s.daytime, s.net_oil_vol_sm3, s.gas_vol_sm3
        FROM rv_pwel_day_status s
        JOIN object o ON o.object_id = s.object_id
        WHERE s.daytime = $P{P_DAYTIME}
        ORDER BY o.object_code
        ]]>
    </queryString>

    <!-- 3. Fields — columns from the query -->
    <field name="OBJECT_CODE" class="java.lang.String"/>
    <field name="DAYTIME" class="java.util.Date"/>
    <field name="NET_OIL_VOL_SM3" class="java.lang.Double"/>
    <field name="GAS_VOL_SM3" class="java.lang.Double"/>

    <!-- 4. Variables — calculated values -->
    <variable name="TOTAL_OIL" class="java.lang.Double" calculation="Sum">
        <variableExpression><![CDATA[$F{NET_OIL_VOL_SM3}]]></variableExpression>
    </variable>

    <!-- 5. Bands — sections of the report -->
    <title>...</title>
    <pageHeader>...</pageHeader>
    <columnHeader>...</columnHeader>
    <detail>
        <band height="20">
            <textField>
                <reportElement x="0" y="0" width="100" height="20"/>
                <textFieldExpression><![CDATA[$F{OBJECT_CODE}]]></textFieldExpression>
            </textField>
        </band>
    </detail>
    <summary>...</summary>
    <pageFooter>...</pageFooter>
</jasperReport>
```

---

### Report Bands (Sections)

| Band | Renders | Use for |
|---|---|---|
| `title` | Once at start | Report title, logo, header |
| `pageHeader` | Top of every page | Column headers, date |
| `columnHeader` | Before detail | Table column headers |
| `detail` | Once per data row | The data rows |
| `columnFooter` | After detail | Column subtotals |
| `pageFooter` | Bottom of every page | Page number, footer text |
| `lastPageFooter` | Bottom of last page | Grand totals |
| `summary` | Once at end | Grand totals, summary |
| `noData` | When query returns 0 rows | "No data found" message |
| `background` | Every page (behind) | Watermarks |

---

### Expressions — The Power of JasperReports

All dynamic content uses **Java expressions** inside `<![CDATA[...]]>`:

```xml
<!-- Field value -->
<textFieldExpression><![CDATA[$F{NET_OIL_VOL_SM3}]]></textFieldExpression>

<!-- Parameter value -->
<textFieldExpression><![CDATA[$P{P_DAYTIME}]]></textFieldExpression>

<!-- Variable (calculated) -->
<textFieldExpression><![CDATA[$V{TOTAL_OIL}]]></textFieldExpression>

<!-- Conditional expression -->
<textFieldExpression><![CDATA[
    $F{NET_OIL_VOL_SM3} != null ? $F{NET_OIL_VOL_SM3} : 0.0
]]></textFieldExpression>

<!-- Formatting -->
<textFieldExpression><![CDATA[
    new java.text.DecimalFormat("#,##0.00").format($F{NET_OIL_VOL_SM3})
]]></textFieldExpression>

<!-- Date formatting -->
<textFieldExpression><![CDATA[
    new java.text.SimpleDateFormat("dd-MMM-yyyy").format($F{DAYTIME})
]]></textFieldExpression>
```

---

### Oracle JDBC Connection in Jasper Studio 7.0.3

**Setup steps in Jasper Studio:**
1. Window → Preferences → Jaspersoft Studio → Data Adapters → New
2. Select: Database JDBC Connection
3. Driver: `oracle.jdbc.OracleDriver`
4. URL: `jdbc:oracle:thin:@db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev`
5. Username: `ECKERNEL_EC`
6. Password: `energy`
7. Add Oracle JDBC driver JAR: `ojdbc17.jar` (from `C:\Tools\java\...`)

**In JRXML — data adapter reference:**
```xml
<property name="com.jaspersoft.studio.data.defaultdataadapter" value="Woodside_Pluto_Dev"/>
```

---

### Compiling and Deploying to EC

```
JRXML (design) → Jasper Studio compile → .jasper (binary) → EC deployment
```

**In EC, reports are configured in:**
- Report Admin screen (frmw.report module)
- Extension SQL: register report name, path, parameters
- `.jasper` file placed in extension WAR under `reports/` folder

**Key V7 change from V6:** JasperReports 7.x uses updated expression language and new element syntax. Reports designed in v7 Jasper Studio compile to v7 `.jasper` format which requires JasperReports 7.x runtime. **EC 14.2.5 ships with JasperReports 6.21.4 — deployment risk confirmed.**

---

### JasperReports 7.0.3 — Key New Features vs 6.x

| Feature | v6.x | v7.0.3+ |
|---|---|---|
| Table component | Limited | Enhanced with new API |
| HTML5 charts | Basic | Improved |
| Expression language | Java only | Enhanced |
| Accessibility | Limited | WCAG 2.1 support |
| PDF/A | v6.x format | Updated PDF/A-3 |
| Performance | Standard | Improved rendering |

---

### Groups — Subtotals and Grouping

```xml
<group name="WELL_GROUP">
    <groupExpression><![CDATA[$F{OBJECT_CODE}]]></groupExpression>
    <groupHeader>
        <band height="20">
            <!-- Well name header -->
            <textField>
                <reportElement x="0" y="0" width="200" height="20"/>
                <textFieldExpression><![CDATA[$F{OBJECT_CODE}]]></textFieldExpression>
            </textField>
        </band>
    </groupHeader>
    <groupFooter>
        <band height="20">
            <!-- Well subtotal -->
            <textField>
                <reportElement x="100" y="0" width="100" height="20"/>
                <textFieldExpression><![CDATA[$V{WELL_OIL_SUBTOTAL}]]></textFieldExpression>
            </textField>
        </band>
    </groupFooter>
</group>
```

---

### Subreports — Nested Reports

```xml
<!-- Main report calls subreport -->
<subreport>
    <reportElement x="0" y="0" width="535" height="200"/>
    <subreportParameter name="P_OBJECT_ID">
        <subreportParameterExpression><![CDATA[$F{OBJECT_ID}]]></subreportParameterExpression>
    </subreportParameter>
    <connectionExpression><![CDATA[$P{REPORT_CONNECTION}]]></connectionExpression>
    <subreportExpression><![CDATA["well_detail_subreport.jasper"]]></subreportExpression>
</subreport>
```

---

### Best Practices — JasperReports

1. **Always handle NULL** — use `$F{FIELD} != null ? $F{FIELD} : "N/A"` pattern
2. **Parameterise everything** — date range, object filter via `$P{PARAM}` not hardcoded SQL
3. **Use `$P!{PARAM}` for dynamic SQL** — injects raw SQL string (use carefully, SQL injection risk)
4. **Avoid too many bands** — keep report structure flat where possible
5. **Test with `noData` band** — always handle empty result set
6. **Print when expression** — use `<printWhenExpression>` to conditionally show elements
7. **Lazy evaluation** — expressions evaluate per row; keep them simple
8. **Named styles** — define reusable styles at report level, not inline per element
9. **Use report templates** — for corporate headers/footers, extend a template `.jrxml`

---

## Claude Code Integration Patterns

### Robot Framework + Claude Code

```
Claude Code reads EC screen → identifies elements → generates RF keywords
Claude Code analyses test failure → suggests fix in RF file
Claude Code generates new TC from requirement description
```

**Daily workflow:**
1. Describe screen to test → Claude generates keyword scaffold
2. Run test → paste failure log → Claude diagnoses and fixes
3. New EC screen deployed → Claude reads XHTML → generates page object keywords

### Playwright + Claude Code

```
Claude Code generates Playwright selectors from DOM screenshot
Claude Code converts manual test steps to Playwright automation
Claude Code debugs network failures from Playwright trace
```

### JasperReports + Claude Code

```
Claude Code generates JRXML from SQL query + requirements
Claude Code converts EC SQL view query to Jasper query + fields
Claude Code diagnoses expression errors in JRXML
```

---

## Quick Reference Card

### Robot Framework
```robot
*** Settings ***        Library, Resource, Suite Setup/Teardown
*** Variables ***       ${SCALAR}  @{LIST}  &{DICT}
*** Test Cases ***      [Documentation] [Tags] [Setup] [Teardown]
*** Keywords ***        [Arguments] [Documentation] RETURN
Control:                IF/ELSE/END  FOR/END  WHILE/END  TRY/EXCEPT/END
```

### Browser Library (Playwright)
```
New Browser/Context/Page    → setup
Wait For Load State networkidle    → after every AJAX action
Type Text (not Fill Text)   → for AJAX-triggered search fields
Wait For Elements State visible/hidden    → before interacting
Take Screenshot filename=EMBED    → test evidence
```

### JasperReports 7.0.3+
```
$F{field}    → query field value
$P{param}    → runtime parameter
$V{variable} → calculated variable
<![CDATA[Java expression]]>    → all dynamic content
Bands: title → pageHeader → columnHeader → detail → columnFooter → pageFooter → summary
```
