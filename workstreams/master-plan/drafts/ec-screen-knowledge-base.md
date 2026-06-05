# EC Screen Knowledge Base
**Source:** Live DOM exploration of `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`
**Date:** 2026-06-06 | **User:** sysadmin
**Purpose:** Screen types, navigator fields, IUD capability — for Robot Framework automation

---

## Screen Type Classification

| Type | Count | Pattern | When to use in RF |
|---|---|---|---|
| **NAVIGATOR+TABLE** | 14 | Fill navigator → Go → data shows in table | Fill navigator fields → click Go → verify table loads |
| **NAVIGATOR-ONLY** | 12 | Has navigator but no table on load | Fill navigator → Go → content loads in non-table format |
| **ACTION/EMPTY** | 6 | No navigator, no table at load | Special screens — need investigation per screen |

### IUD Indicators
- `S` = Save button enabled (can save changes)
- `+` = Insert menu enabled (can add new records)
- `D` = Delete menu enabled (can delete records)

---

## All 32 Screens — Complete Reference

### Configuration / Framework Screens

| Screen | Type | IUD | Navigator Fields | Table Columns | Notes |
|---|---|---|---|---|---|
| Authentication Audit | NAVIGATOR+TABLE | --- | From Daytime UTC, To Daytime UTC | Time UTC, Type, Realm | Audit log — read only |
| Object Partition | NAVIGATOR-ONLY | --- | Class Name, Created by, Record status | — | Select class → loads access rules |
| Analytics Object Access | NAVIGATOR+TABLE | -+- | Object Type, Access, Created by | Object Type, Object Name, Access, Comments | Can insert access rules |

### EC Production

| Screen | Type | IUD | Navigator Fields | Notes |
|---|---|---|---|---|
| Daily Dashboard | NAVIGATOR-ONLY | --- | Date, Production Unit | Dashboard view — fill date+unit → load |
| Deferment Dashboard | NAVIGATOR-ONLY | --- | (none visible) | Special dashboard screen |
| Production Efficiency | NAVIGATOR-ONLY | --- | From Date, To Date | Date range → efficiency chart/view |

### EC Revenue

| Screen | Type | IUD | Navigator Fields | Notes |
|---|---|---|---|---|
| Document Tracing | NAVIGATOR-ONLY | --- | (none visible) | Document trace view |
| Visual Tracing | NAVIGATOR-ONLY | --- | Year, Property | Year + property → visual trace |

### Reporting

| Screen | Type | IUD | Navigator Fields | Table Columns | Notes |
|---|---|---|---|---|---|
| Report Area | NAVIGATOR-ONLY | --- | (none) | — | Config screen |
| Report and Analytics | ACTION/EMPTY | --- | — | — | Dashboard/iframe? Needs deeper look |
| **Report Template** | NAVIGATOR+TABLE | -+D | Created by, Record status | Report Template Code, Name, System | Create/delete templates — active IUD |
| **Report Definition** | NAVIGATOR+TABLE | -+D | Created by, Record status | Definition Code, Name, Functional Area | Define report structure — active IUD |
| Report Administration | ACTION/EMPTY | --- | — | — | Admin config — loads differently |
| **Report Generation** | NAVIGATOR+TABLE | -+D | Date, Functional Area, Generation Start | Name, Report Definition, Report Area | Run/schedule reports — active IUD |
| Report Set Administration | ACTION/EMPTY | --- | — | — | Config screen |
| **Report Queue Status** | NAVIGATOR+TABLE | --- | From Date, To Date | Report Name, Status, Generation Start | Monitor running reports — read only |
| Export to Excel Express | NAVIGATOR-ONLY | --- | (none) | — | Quick Excel export tool |
| **Report Publishing** | NAVIGATOR+TABLE | -+- | From Date, To Date | Functional Area, Publication Type, Generated Date | Publish reports — can insert |
| **Display Published Report** | NAVIGATOR+TABLE | --- | From Date, To Date | Report Date, Generated Date, Publish Start Date | View published reports |

### Process Automation (BPM)

| Screen | Type | IUD | Navigator Fields | Table Columns | Notes |
|---|---|---|---|---|---|
| **Project Management** | NAVIGATOR+TABLE | -+- | Created by, Record status | Name, Group Id, Artifact Id | Deploy BPM JARs — Undeploy/Delete btns |
| Process Action | ACTION/EMPTY | --- | — | — | Config screen |
| **Process Template** | NAVIGATOR+TABLE | -+D | Created by, Record status | Process Template, Deployment Id, Process Id | Configure BPM process templates |
| Process Execution | NAVIGATOR-ONLY | --- | Date, Functional Area | — | Start BPM process instances |
| Process Overview | NAVIGATOR-ONLY | --- | From, To | — | Monitor active processes |
| Process Overview Configuration | ACTION/EMPTY | --- | — | — | Config screen |
| Process Overview Legacy | NAVIGATOR+TABLE | --- | From date, To date | Start, End, Process Template | Historical BPM view |
| Todo List | ACTION/EMPTY | --- | — | — | Dynamic task list — loads differently |
| **Task Management** | NAVIGATOR+TABLE | --- | (none visible) | — | Manage user tasks |
| Process Notifications | NAVIGATOR-ONLY | --- | (none) | — | Notification config |
| Process Monitor | NAVIGATOR-ONLY | --- | Daytime, Functional Area | — | Monitor processes by date/area |
| **Process Monitor Configuration** | NAVIGATOR+TABLE | -+- | Created by, Record status | Code, Name, Functional Area | Configure monitors — can insert |
| **Viewer Tag** | NAVIGATOR+TABLE | -+D | Created by, Record status | Name, Description, Property | BPM viewer configuration — active IUD |

---

## Robot Framework Patterns by Screen Type

### Pattern A: NAVIGATOR+TABLE (most data entry screens)
```robot
# Fill navigator fields
Fill Text    id=${NAV_FIELD_1_ID}    ${value}
Select Options By    id=${NAV_FIELD_2_ID}    label    ${option}
# Click Go button
Click    id=button:form:B
Wait For Load State    networkidle    timeout=30s
# Verify table loaded
Wait For Elements State    css=.ui-datatable tbody tr    visible    30s
```

### Pattern B: NAVIGATOR-ONLY (dashboards, charts, special views)
```robot
# Fill navigator
Fill Text    id=${NAV_DATE_ID}    2025-01-01
# Click Go
Click    id=button:form:B
Wait For Load State    networkidle    timeout=30s
# Verify content loaded (no table — check specific element)
Wait For Elements State    id=screenToolbar:form:screenLabel    visible    10s
```

### Pattern C: ACTION/EMPTY (config screens loaded differently)
```robot
# These screens may load via AJAX or special handlers
# Navigate and wait for networkidle — content appears without Go
Wait For Load State    networkidle    timeout=30s
# Check if specific elements are visible
${has_content}=    Get Element Count    css=.ECScreenlet
```

---

## Key DOM IDs per Screen (from live exploration)

### Common navigator cell ID pattern
`{screenletId}:form:G:{grid}:R:{row}:C:{col}:{type}`

### Authentication Audit
```
Navigator: form screenlet with date range inputs
From/To UTC date inputs
Go button: button:form:B
Table shows: audit events (Time UTC, Type, Realm, ...)
```

### Report Template / Report Definition / Process Template / Viewer Tag
```
Navigator: Created by + Record status filters only
Table loads immediately (no Go needed for initial view)
Insert enabled: can create new records
Delete enabled: can remove records
```

### Process Execution
```
Navigator: Date + Functional Area
Purpose: Launch a BPM process
After Go: shows process instances to start
```

### Project Management (BPM)
```
Table shows: deployed BPM JARs (Name, Group Id, Artifact Id, Version)
Action buttons: Undeploy, Delete
Insert: upload new BPM deployment
Used for: deploying process templates from .zip/.jar files
```

---

## Screens That Support Insert (active + enabled)

| Screen | Section | What gets inserted |
|---|---|---|
| Analytics Object Access | Configuration | Access rule for an object |
| Report Template | Reporting | New report template |
| Report Definition | Reporting | New report definition |
| Report Generation | Reporting | New report generation job |
| Report Publishing | Reporting | New publication rule |
| Project Management | Process Automation | New BPM deployment |
| Process Template | Process Automation | New process template |
| Process Monitor Configuration | Process Automation | New monitor config |
| Viewer Tag | Process Automation | New viewer tag |

---

## Screens That Support Delete (active + enabled)

| Screen | Section |
|---|---|
| Report Template | Reporting |
| Report Definition | Reporting |
| Report Generation | Reporting |
| Process Template | Process Automation |
| Viewer Tag | Process Automation |

---

## ACTION/EMPTY Screens — Investigation Needed

These 6 screens showed empty content at load time. They likely:
- Load content via JavaScript after a user action
- Display in an embedded iframe or dashboard widget
- Require different navigation/interaction patterns

| Screen | Section | Likely behaviour |
|---|---|---|
| Report and Analytics | Reporting | Yellowfin/analytics dashboard iframe |
| Report Administration | Reporting | Admin config — tree/accordion structure |
| Report Set Administration | Reporting | Set config screen |
| Process Action | Process Automation | Action config — tree/list |
| Process Overview Configuration | Process Automation | Config screen |
| Todo List | Process Automation | Dynamic task list — loaded via BPM event |

---

## EC Treeview — Full Screen Inventory (sysadmin access)

**Total accessible screens found: 32** (from menu expansion)

Missing from list (not accessible to sysadmin or not in scope):
- All EC Production specific screens (Daily Well Status, Check Rules, Validation Overview, etc.) — need to search by name
- EC Chemistry, EC Transport, EC Sales screens — same
- These screens exist but didn't appear in the expanded tree for sysadmin

**To access domain screens:** Use the search box with screen name, or navigate via sub-sub-sections after expanding domain sections further.
