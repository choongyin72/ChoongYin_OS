# EC Screen Knowledge Base
**Sources:** 
- Local EC sandbox (`ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`) — sysadmin
- Woodside Pluto COPS DEV (`app-plutodev.woodside-pluto.tieto-og.cloud/`) — sysadmin
**Date:** 2026-06-06
**Purpose:** Screen types, navigator fields, IUD capability — for Robot Framework automation

---

## Important: Two EC Instances

| Instance | URL | Screen Set | When to use |
|---|---|---|---|
| **Local EC sandbox** | `ap-f0a7g341jn6d:8443` | Generic EC screens (Configuration, Reporting, Process Automation) | Learning, framework testing |
| **Woodside Pluto COPS DEV** | `app-plutodev.woodside-pluto.tieto-og.cloud` | Woodside-specific production screens (Daily Stream Status, Well Status, Check Rules, PHD data) | All Woodside Pluto work |

The local EC has ~685 screens (generic EC). Woodside Pluto has the same plus the Woodside production screens (ZWT/ZWP extensions).

---

## Screen Type Classification

| Type | Pattern | RF approach |
|---|---|---|
| **NAVIGATOR+TABLE** | Fill navigator fields → Go → data table loads | Fill inputs → click Go → assert table has rows |
| **NAVIGATOR-ONLY** | Has navigator but loads chart/dashboard (no table) | Fill navigator → Go → check specific content loaded |
| **TABLE-ONLY** | No navigator — table loads immediately | Assert table visible → interact with rows directly |
| **ACTION/EMPTY** | Special config screens — content loads differently | Wait for specific elements per screen |

### IUD Indicators
- `S` = Save enabled (modify records)
- `+` = Insert menu enabled (add new records)
- `D` = Delete menu enabled (remove records)
- `-` = Not available on this screen

---

## Full EC Tree — 685 screens found (Local EC Sandbox)

### Configuration (380 screens) — key ones

| Screen | Type | Notes |
|---|---|---|
| **Check Group** (CO.0079) | Config | Defines check rule groups — links check rules to screens |
| **Rule Group Combination** (CO.0080) | Config | Many-to-many: check rules ↔ groups |
| **Validation Overview** (CO.0203) | NAVIGATOR+TABLE | Main validation screen — run check rules, view violations |
| **Validation Overview by Facility** | NAVIGATOR+TABLE | Facility-filtered validation view |
| **Class Validation** (CO.1031) | Config | Class-level min/max validation config |
| **Hierarchical Object Validation** (CO.0253) | Config | Cascaded object validation |
| **Object Validation - Default** (CO.1032.01) | Config | Object-level validation |
| **Maintain Calculation** | Config | Create/edit EC calculations |
| **Maintain Library Calculation** | Config | Library calc management |
| **Calculation Group Setup** (CO.0246) | Config | Calculation group config + logs |
| **Stream Node Diagram** | NAVIGATOR+TABLE | Visual allocation network diagram |
| **Validation Overview** | NAVIGATOR+TABLE | nav: Date, Facility | See check rule violations |
| **Initiate Day** | Config | Initialize production day |
| **Production Day Table** | Config | Production day configuration |
| **Business Actions** | Config | BPM business action configuration |
| **Schedules** | Config | EC scheduler management |
| **Adapter Configuration** | Config | ECIS adapter setup (PHD/PI) |
| **Maintain Mappings** | Config | ECIS tag-to-attribute mappings |
| **Check Group** | Config | Check rule group definition |
| **Rule Group Combination** | Config | Links check rules to groups |
| **Node** | Config | Allocation network node |
| **Alloc Job Status Process Conn** | Config | Allocation BPM connection config |

### EC Production (34 screens) — sysadmin access

| Screen | Type | Navigator Fields | Notes |
|---|---|---|---|
| **Daily Dashboard** | NAVIGATOR-ONLY | Date, Production Unit | Daily production overview |
| **Deferment Dashboard** | NAVIGATOR-ONLY | (none) | Deferment status dashboard |
| **Production Efficiency** | NAVIGATOR-ONLY | From Date, To Date | Efficiency KPIs |
| Well Finder | NAVIGATOR-ONLY | — | Find wells by criteria |
| Equipment Finder | NAVIGATOR-ONLY | — | Find equipment |
| Stream Finder | NAVIGATOR-ONLY | — | Find streams |
| Tank Finder | NAVIGATOR-ONLY | — | Find tanks |
| **Deferment** | NAVIGATOR+TABLE | — | Deferment records |
| **Deferment Day** | NAVIGATOR+TABLE | — | Day-level deferment |
| **Daily Data Status Processes** | NAVIGATOR+TABLE | — | Production→Verified status |
| **Daily Data Status Processes - by Facility** | NAVIGATOR+TABLE | — | Facility-filtered |
| **Daily Data Status Processes - Single Date** | NAVIGATOR+TABLE | Date | Single date status |
| **Monthly Data Status Processes** | NAVIGATOR+TABLE | — | Monthly verification |
| **Monthly Data Locking** | NAVIGATOR+TABLE | — | Lock monthly data |
| **Period Process Calculations** | NAVIGATOR+TABLE | — | Run period calcs |
| **Monthly Account Balance Calculation** | NAVIGATOR+TABLE | — | Monthly balance run |
| Analysis And Measurements | NAVIGATOR+TABLE | — | Lab analysis data |

### EC Production — NOT visible (Woodside Pluto only)
These screens appear in Woodside Pluto COPS DEV but NOT in the local sandbox:
- Daily Oil Stream Status (PO.0001)
- Daily Gas Stream Status (PO.0002)
- Daily Water Stream Status (PO.0003)
- Daily Production Well Status 1 (WR.0001)
- Monthly Production Well Status
- Monthly Allocated Production Well Data
- Stream Component Analysis (TC01/TC02 screens)
- Stream Analysis (TC03/TC04 screens)
- Daily Tank Status (TC05-TC08 screens)
- Maintain Check Rules (CO.0201) — check rule maintenance screen
- Daily Allocation (HA.0002)
- Monthly Allocation (HA.0003)

**These screens require the ZWT/ZWP Woodside extensions to be deployed.**

### Reporting (14 screens) — from earlier exploration

| Screen | Type | IUD | Notes |
|---|---|---|---|
| Report Template | NAVIGATOR+TABLE | -+D | Create/delete report templates |
| Report Definition | NAVIGATOR+TABLE | -+D | Define report structure |
| Report Generation | NAVIGATOR+TABLE | -+D | Run/schedule reports |
| Report Queue Status | NAVIGATOR+TABLE | --- | Monitor queued reports |
| Report Publishing | NAVIGATOR+TABLE | -+- | Publish completed reports |
| Display Published Report | NAVIGATOR+TABLE | --- | View published output |
| Report Area | NAVIGATOR-ONLY | --- | Config screen |
| Export to Excel Express | NAVIGATOR-ONLY | --- | Quick Excel export |

### Process Automation (13 screens) — from earlier exploration

| Screen | Type | IUD | Navigator Fields | Notes |
|---|---|---|---|---|
| **Project Management** | NAVIGATOR+TABLE | -+- | Created by, Record status | Deploy BPM JARs |
| **Process Template** | NAVIGATOR+TABLE | -+D | Created by, Record status | Configure BPM templates |
| **Process Execution** | NAVIGATOR-ONLY | --- | Date, Functional Area | Start BPM processes |
| **Process Overview** | NAVIGATOR-ONLY | --- | From, To | Monitor processes |
| **Process Overview Legacy** | NAVIGATOR+TABLE | --- | From date, To date | Historical view |
| **Todo List** | ACTION/EMPTY | --- | — | User task queue |
| **Task Management** | NAVIGATOR+TABLE | --- | — | Manage user tasks |
| **Process Monitor** | NAVIGATOR-ONLY | --- | Daytime, Functional Area | Monitor by date |
| **Process Monitor Configuration** | NAVIGATOR+TABLE | -+- | Created by, Record status | Config monitors |
| **Viewer Tag** | NAVIGATOR+TABLE | -+D | Created by, Record status | BPM viewer config |

---

## Robot Framework Screen Patterns

### Pattern 1: NAVIGATOR+TABLE (most common)
```robot
# Standard pattern — fill navigator, click Go, assert table
${NAV_FIELD}=    Set Variable    {screenlet}:form:G:0:R:0:C:1:{type}
Fill Text    id=${NAV_FIELD}    ${value}
Click    id=button:form:B
Wait For Load State    networkidle    timeout=30s
Wait For Elements State    css=.ui-datatable tbody tr    visible    20s
${row_count}=    Get Element Count    css=.ui-datatable tbody tr
Should Be True    ${row_count} > 0
```

### Pattern 2: Check Group / Validation Overview
```robot
# CO.0079 Check Group — no navigator needed, data loads directly
Search And Open Screen    Check Group
Wait For Load State    networkidle    timeout=30s
# Insert new check group:
Click    xpath=//a[.//span[contains(@class,'ui-icon-insert')]]
Wait For Load State    networkidle    timeout=15s

# CO.0203 Validation Overview — has navigator + Go + Run All button
Search And Open Screen    Validation Overview
Click    id=button:form:B    # Go
Wait For Load State    networkidle    timeout=30s
Click    xpath=//*[contains(@id,'runAllButton')]
Wait For Load State    networkidle    timeout=60s
```

### Pattern 3: Check Rule navigation (Woodside Pluto COPS DEV)
```robot
# These work on COPS DEV (app-plutodev.woodside-pluto.tieto-og.cloud)
Search And Open Screen    Check Rule
# Navigate to last page to find PHD check rules (rules 1142-1149)
Click    css=span.ui-icon-seek-end
Wait For Load State    networkidle    timeout=15s
# Verify rule visible
Verify Rule Visible In Grid    PHD_STRM_COMP_MOL_PCT_VAL1
```

---

## Key DOM Selectors for These Screens

```robot
# Check Group screen (CO.0079)
${SCREEN_CHECK_GROUP}        Check Group
# After opening: no navigator needed, table shows all groups
# Table ID: typically check_group:form
# Insert: xpath=//a[.//span[contains(@class,'ui-icon-insert')]]

# Validation Overview (CO.0203)
${SCREEN_VALIDATION}         Validation Overview
# Navigator: date range + facility
# Run All button: xpath=//*[contains(@id,'runAllButton')]
# Groups table: groups:form
# Logs table: logs:form

# Daily Data Status Processes
${SCREEN_DAILY_STATUS}       Daily Data Status Processes
# Navigator: date + facility
# Shows: Provisional → Verified status transitions

# Schedules screen
${SCREEN_SCHEDULES}          Schedules
# Shows all EC scheduled jobs
# Insert: create new schedule
# Can trigger jobs manually
```

---

## Screen Inventory Files
- **Full tree (685 items):** `docs/EC/ec_full_tree_inventory.json`
- **32 explored screens:** `docs/EC/screenshots/screens/`
- **Dom reference:** `docs/EC/screenshots/` (login, dashboard, Object Partition)

---

## Next Steps for Screen Knowledge Base
1. Connect to **Woodside Pluto COPS DEV** and explore production screens there
2. Capture: Daily Oil Stream Status, Check Rule screen, Stream Component Analysis
3. Document exact screenlet IDs for Issue_1052 Phase 2 RF tests
4. Add to this knowledge base as Woodside Pluto section
