# EC Web App — Live DOM Deep Dive
**Source:** Live DOM exploration of local EC `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`
**Date:** 2026-06-06
**Auth:** sysadmin / sysadmin
**Purpose:** Complete element ID reference for Robot Framework + Playwright automation

---

## EC Screen Layout Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  TOP BAR: logo | [sysadmin ▼] [⚙ settings] [≡ hamburger]      │
├─────────────────┬───────────────────────────────────────────────┤
│  LEFT SIDEBAR   │  TOOLBAR: [💾][↺][➕][🗑][↗][⭐][···][🔔]  │
│                 │  ────────────────────────────────────────────  │
│  SEARCH: [    ] │  NAVIGATOR: [Class Name ▼] [▶ Go]            │
│                 │  ────────────────────────────────────────────  │
│  FAVORITES:     │                                               │
│  ○ Auth Audit   │      MAIN DATA AREA (Screenlets)              │
│  ○ Obj Partition│                                               │
│  ○ Analytics    │                                               │
│                 │                                               │
│  MENU:          │                                               │
│  ● Dashboard    │                                               │
│  > Configuration│                                               │
│  > EC Production│  ────────────────────────────────────────────  │
│  > EC Chemistry │  STATUS AREA (bottom splitter, resizable)     │
│  > EC Transport │  [RECORD STATUS][REVISION INFO][APPROVAL]     │
│  > EC Sales     │  [HINTS & TIPS][VALIDATION][TRENDING][ATTACH] │
│  > EC Revenue   │                                               │
│  > ...          │                                               │
└─────────────────┴───────────────────────────────────────────────┘
```

---

## 1. App Container Structure

| Element | ID | Class | Purpose |
|---|---|---|---|
| Root container | `ec-app-container` | `flexContainerCol ec-app-container` | Outer wrapper |
| Top bar | `ec-top-container` | `noFlexItem ec-top-container` | Top navigation |
| App splitter | `ec-app-splitter` | `ui-splitter ui-widget ec-app-splitter` | Horizontal split (menu|screen) |
| Left panel | `ec-menu-container_0` | `ui-splitter-panel ec-menu-container` | Left sidebar |
| Right panel | `ec-screen-container_1` | `ui-splitter-panel ec-screen-container` | Screen content |
| Screen splitter | `ec-screen-splitter` | `ui-splitter ui-widget ec-screen-splitter` | Vertical split (content|status) |
| Screen content | `ec-screen-content_0` | `ui-splitter-panel ec-screen-content` | Main data area |
| Status area | `ec-screen-sa-content_1` | `ui-splitter-panel ec-screen-sa-content` | Status tabs at bottom |

---

## 2. Top Bar

| Element | ID | Selector | Purpose |
|---|---|---|---|
| Top form | `topForm` | `id=topForm` | Form container |
| Top toolbar | `topForm:topMenu` | `xpath=//*[@id='topForm:topMenu']` | `ui-toolbar` bar |
| User menu | `topForm:j_idt15` | `xpath=//*[@id='topForm:j_idt15']` | Menubar with username |
| Logout button | (no id) | `xpath=//a[@title='Logout']` | Logout link |
| Settings/hamburger | `topForm:dynaButton` | `xpath=//*[@id='topForm:dynaButton']` | Settings menu trigger |

**Playwright/RF selectors:**
```robot
# Logout
xpath=//a[@title='Logout']
# Username display
xpath=//*[@id='topForm:j_idt15']//span[contains(@class,'ui-menuitem-text')]
# Settings
id=topForm:dynaButton
```

---

## 3. Left Sidebar — SEARCH

| Element | ID | How to find |
|---|---|---|
| Search section header | `menu:tabSearch_header` | PrimeFaces accordion header |
| Search section content | `menu:tabSearch` | Accordion panel |
| **Search input** | `menu:searchForm:searchTxt` | `xpath=//input[@id='menu:searchForm:searchTxt']` |
| Search results list | `menu:searchForm:searchList` | `id=menu:searchForm:searchList` |

**Critical:** Use `Type Text` with `delay=50ms` — PrimeFaces triggers AJAX on keyup:
```robot
# Robot Framework
Type Text    xpath=//input[@id='menu:searchForm:searchTxt']    ${screen_name}    delay=50ms
Wait For Load State    networkidle    timeout=15s
```

**Search results appear as:** `<span class="tv-link">ScreenName</span>` — no stable ID.
**Selector for results:**
```robot
xpath=//span[contains(@class,'tv-link') and normalize-space(text())='${screen_name}']
```

---

## 4. Left Sidebar — FAVORITES

| Element | ID pattern | Purpose |
|---|---|---|
| Favorites section | `menu:tabFavorites_header` / `menu:tabFavorites` | Accordion section |
| Favorites form | `menu:favoritesForm` | Container form |
| Favorites list | `menu:favoritesForm:favoriteList` | PrimeFaces OrderList |
| Doc icon (per item) | `menu:favoritesForm:icon:{N}` | Document icon |
| Star/open button | `menu:favoritesForm:j_idt40:{N}` | Opens/activates the favorite |
| Close/remove button | `menu:favoritesForm:j_idt42:{N}` | Removes favorite (X button) |
| Favorite link (span) | (no id) | `span.tv-link` with screen name text |

**Navigate to favorite:**
```robot
# Click by text (most reliable)
Click    xpath=//span[contains(@class,'tv-link') and normalize-space(text())='Object Partition']
Wait For Load State    networkidle    timeout=20s
```

---

## 5. Left Sidebar — MENU TREE

| Element | ID pattern | Class | Notes |
|---|---|---|---|
| Tree form | `menu:tvForm` | FORM | |
| Tree root | `menu:tvForm:treeView` | `ui-tree ui-widget` | PrimeFaces tree |
| Menu node (LI) | `menu:tvForm:treeView:{N}` | `ui-treenode-unselected ui-treenode` | N=0-12 for top-level items |
| Node label | `menu:tvForm:treeView:{N}:N` | `tv-link ui-draggable` | LABEL — click this to navigate |
| Expand button | `menu:tvForm:treeView:{N}:j_idt48` | `ui-button` | Click to expand sub-items |

**Top-level menu items (N values):**
| N | Screen name |
|---|---|
| 0 | Dashboard |
| 1 | Configuration |
| 2 | EC Production |
| 3 | EC Chemistry |
| 4 | EC Transport |
| 5 | EC Sales |
| 6 | EC Revenue |
| 7 | System Messages |
| 8 | Reporting |
| 9 | Process Automation |
| 10 | Messaging |
| 11 | Task List |
| 12 | EC Integration Service |

**Click to expand Configuration:**
```robot
Click    xpath=//*[@id='menu:tvForm:treeView:1:j_idt48']
Wait For Load State    networkidle    timeout=10s
```

---

## 6. Screen Toolbar

### Main Toolbar (`screenToolbar:form:menuBar`)

| Element | ID | Title | Icon class | RF selector |
|---|---|---|---|---|
| Toolbar container | `screenToolbar:screenToolbar` | — | `screenlet toolbarScreenlet` | `id=screenToolbar:screenToolbar` |
| Toolbar form | `screenToolbar:form` | — | — | `id=screenToolbar:form` |
| **Main icon bar** | `screenToolbar:form:menuBar` | — | `ECMenuBar` | `id=screenToolbar:form:menuBar` |
| **Extra icon bar** | `screenToolbar:form:extraBar` | — | `ECExtraMenuBar` | `id=screenToolbar:form:extraBar` |

### Toolbar Icon Selectors (by title attribute)

```robot
# Save [Ctrl+s]
xpath=//a[@title='Save [Ctrl+s]']
# Refresh [Ctrl+r]
xpath=//a[@title='Refresh [Ctrl+r]']
# New/Insert (submenu)
xpath=//a[.//span[contains(@class,'ui-icon-insert')]]
# Delete (submenu)
xpath=//a[.//span[contains(@class,'ui-icon-delete')]]
```

### Extra Bar Selectors

| Element | ID | Purpose |
|---|---|---|
| **Fullscreen/minmax toggle** | `screenToolbar:form:minmaxMenu` | Hide treeview for more space |
| **Add to favorites** | `screenToolbar:form:favorite` | Star button |
| Settings submenu | `screenToolbar:form:settingsSub` | Settings/options |
| **Notification bell** | `screenToolbar:form:taskNotification` | Task notifications (`taskNotificationIcon`) |
| **Screen label** | `screenToolbar:form:screenLabel` | Displays current screen name (`ECTopScreenDesc`) |

**EC Robot Framework pattern:**
```robot
# Toggle fullscreen (hide left panel)
Click    id=screenToolbar:form:minmaxMenu
Wait For Load State    networkidle    timeout=10s

# Get current screen name
${screen_name}=    Get Text    id=screenToolbar:form:screenLabel
```

### Toolbar Click Pattern
Toolbar buttons use PrimeFaces menubar AJAX:
```javascript
// onclick format for toolbar actions:
EC.forceChange();
PrimeFaces.ab({s:"screenToolbar:form:menuBar", f:"screenToolbar:form",
               pa:[{name:"screenToolbar:form:menuBar_menuid", value:"..."}]});
```

---

## 7. Navigator (FormScreenlet)

### Pattern: `{screenletId}:form:G:{grid}:R:{row}:C:{col}:{type}`

**Object Partition screen navigator:**
| Element | ID | Type | Purpose |
|---|---|---|---|
| Navigator form | `classNameNav:form` | FORM (`formScreenlet`) | Navigator container |
| Fieldset | `classNameNav:form:G:0:FS` | FIELDSET | Grid row container |
| Class Name label | `classNameNav:form:G:0:R:0:C:0:la` | SPAN (`ECLabelCell`) | "Class Name" label |
| **Class Name dropdown** | `classNameNav:form:G:0:R:0:C:1:dd` | SPAN (autocomplete) | Dropdown widget |
| Class Name input | `classNameNav:form:G:0:R:0:C:1:dd_input` | INPUT | Type-ahead input |
| Class Name button | `classNameNav:form:G:0:R:0:C:1:dd_button` | BUTTON | Dropdown trigger |
| **Go button form** | `button:form` | FORM (`buttonScreenlet goButtonScreenlet`) | |
| **Go button** | `button:form:B` | BUTTON | Click to execute navigator |

**Cell type suffixes:**
| Suffix | Element type | Use case |
|---|---|---|
| `:la` | SPAN `ECLabelCell` | Read-only label |
| `:in` | INPUT `ECCell` | Text input field |
| `:dd` | SPAN autocomplete widget | Dropdown selector |
| `:dd_input` | INPUT | Autocomplete text input |
| `:dd_button` | BUTTON | Dropdown trigger arrow |
| `:da` | INPUT date | Date field |
| `:da_input` | INPUT | Date input part |

**Fill navigator and Go:**
```robot
# Fill Class Name autocomplete
Fill Text    id=classNameNav:form:G:0:R:0:C:1:dd_input    WELL
Wait For Load State    networkidle    timeout=10s
# Click first autocomplete suggestion
Click    xpath=//li[contains(@class,'ui-autocomplete-item')][1]

# Click Go button
Click    id=button:form:B
Wait For Load State    networkidle    timeout=30s
```

---

## 8. Data Table (TableScreenlet)

### Standard table IDs (Object Partition example)

| Screenlet | Form ID | Type |
|---|---|---|
| Class Access | `classAccess:form` | `tableScreenlet` |
| Partition | `partition:form` | `tableScreenlet` |
| Operator | `operator:form` | `formScreenlet` |

### Table Column Filter Inputs

Filter input ID pattern: `{screenletId}:form:T:sfilter{N}_ft_filter`

```robot
# Filter Check Name column (column 0) in check_rules table
Fill Text    id=check_rules:form:T:sfilter0_ft_filter    PHD_STRM
Wait For Load State    networkidle    timeout=15s
```

### Table Row Data

```robot
# EC data rows have data-rk attribute
tr[data-rk]                              # All data rows
tr[data-rk='SPECIFIC_KEY']              # Specific row by key

# Row content by column
xpath=//tr[@data-rk][1]//td[1]         # First cell of first row
```

### Pagination Controls

```robot
# Last page button
css=span.ui-icon-seek-end

# First page
css=span.ui-icon-seek-first

# Next page
css=span.ui-icon-seek-next

# Previous page
css=span.ui-icon-seek-prev

# Current page number (active)
css=.ui-paginator-page.ui-state-active
```

### Column Filter Toggle (Hamburger)

```robot
# Enable column filters (hamburger / filter toggle)
xpath=//span[contains(@id,'tfo')]        # Filter toggle button
```

### Column Resize / Freeze Toggle

```robot
# Column menu per header
xpath=//th[@id='TABLE_ID_head']//span[@class='ui-column-resizer']
```

---

## 9. Status Area (Bottom Tabs)

### Tab Panel

| Element | ID | Tab name |
|---|---|---|
| Tab container | `statusarea_tab:tabPanel` | `ui-tabs` |
| Tab 1 header | `statusarea_tab:tabPanel:_sa_tab1_header` | Record Status |
| Tab 2 header | `statusarea_tab:tabPanel:_sa_tab2_header` | Revision Info |
| Tab 3 header | `statusarea_tab:tabPanel:_sa_tab3_header` | Approval Status |
| Tab 4 header | `statusarea_tab:tabPanel:_sa_tab4_header` | Hints & Tips |
| Tab 5 header | `statusarea_tab:tabPanel:_sa_tab5_header` | Validation |
| Tab 6 header | `statusarea_tab:tabPanel:_sa_tab6_header` | Trending |
| Tab 7 header | `statusarea_tab:tabPanel:_sa_tab7_header` | Attachments |
| Panel 1 | `statusarea_tab:tabPanel:_sa_tab1` | Record Status content |

### Record Status Tab Fields

| Field | ID | Type |
|---|---|---|
| Created by label | `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:0:C:0:la` | ECLabelCell |
| Created by value | `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:0:C:1:in` | INPUT |
| Created date | `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:0:C:2:in` | INPUT |
| Record status label | `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:0:C:3:la` | ECLabelCell |
| Record status value | `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:0:C:4:in` | INPUT |
| Last updated by | `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:1:C:1:in` | INPUT |
| Last updated date | `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:1:C:2:in` | INPUT |
| Revision text label | `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:1:C:3:la` | ECLabelCell |
| Revision text value | `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:1:C:4:in` | INPUT |
| Revision event label | `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:1:C:5:la` | ECLabelCell |
| Revision event dropdown | `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:1:C:6:dd` | Autocomplete |

**Click status area tab:**
```robot
Click    id=statusarea_tab:tabPanel:_sa_tab5_header    # Validation tab
Wait For Load State    networkidle    timeout=10s
```

---

## 10. Notification Areas

| Element | ID | Purpose |
|---|---|---|
| Main notification | `ECNotificationArea` | Save success/error messages |
| Client notification | `ECClientNotificationArea` | Client-side warnings |
| Warning area | `JSWarningArea` + `JSWarningMsg` | JS/AJAX warnings |
| Error area | `JSErrorArea` + `JSErrorMsg` | JS/AJAX errors |
| AJAX indicator | `ajaxStatus` | Loading spinner |

**Check for errors after save:**
```robot
# Check notification area for messages
${msg}=    Get Text    id=ECNotificationArea
Should Not Contain    ${msg}    error    ignore_case=True

# Or wait for success indicator
Wait For Elements State    id=ECNotificationArea    visible    5s
```

---

## 11. Global Forms (always present)

| ID | Purpose |
|---|---|
| `popupForm` | Popup windows/dialogs |
| `ScreenForm` | Screen-level form |
| `confirmationForm` | "Are you sure?" confirmation dialogs |
| `dialogForm` | General dialog form |
| `pollForm` | Long-running operation polling |
| `ScreenTemplateForm` | Screen template |
| `jsChannel` | JavaScript message channel |
| `styleChannel` | Dynamic CSS channel |

**Handle confirmation dialog:**
```robot
# After Save that triggers confirmation
Wait For Elements State    css=.ui-confirm-dialog-message    visible    10s
# OR
Wait For Elements State    css=.ui-confirmdialog-yes    visible    10s
Click    css=.ui-confirmdialog-yes
Wait For Load State    networkidle    timeout=15s
```

---

## 12. EC Field Colour Meanings (from PPT slide 22)

| Colour | Meaning | RF detection |
|---|---|---|
| Grey | Read-only | `css=.ECCell:not([class*=editable])` |
| White | Editable | `ECCell` without special class |
| Yellow | Mandatory | Class includes `mandatory:true` |
| Yellow/Red | Value out of warning/error range | Configured per check rule |

**Cell class pattern:** `ECCell ECInputCell {mandatory:false}` or `{mandatory:true}`

---

## 13. Key Robot Framework Patterns Summary

```robot
*** Variables ***
${SEARCH_INPUT}        xpath=//input[@id='menu:searchForm:searchTxt']
${SCREEN_LABEL}        id=screenToolbar:form:screenLabel
${SCREEN_TOGGLE}       id=screenToolbar:form:minmaxMenu
${GO_BUTTON}           id=button:form:B
${STATUS_TAB_RECORD}   id=statusarea_tab:tabPanel:_sa_tab1_header
${STATUS_TAB_VALID}    id=statusarea_tab:tabPanel:_sa_tab5_header
${CONFIRM_YES}         css=.ui-confirmdialog-yes
${PAGINATION_LAST}     css=span.ui-icon-seek-end
${PAGINATION_FIRST}    css=span.ui-icon-seek-first
${AJAX_STATUS}         id=ajaxStatus
${NOTIF_AREA}          id=ECNotificationArea

*** Keywords ***
Search And Open Screen
    [Arguments]    ${screen_name}
    Wait For Elements State    ${SEARCH_INPUT}    visible    ${WAIT_TIMEOUT}
    Click           ${SEARCH_INPUT}
    Clear Text      ${SEARCH_INPUT}
    Type Text       ${SEARCH_INPUT}    ${screen_name}    delay=50ms
    Wait For Load State    networkidle    timeout=15s
    ${link}=    Set Variable    xpath=//span[contains(@class,'tv-link') and normalize-space(text())='${screen_name}']
    Wait For Elements State    ${link}    visible    15s
    Click    ${link}
    Wait For Load State    networkidle    timeout=30s

Get Current Screen Name
    RETURN    Get Text    ${SCREEN_LABEL}

Click Toolbar Save
    Click    xpath=//a[@title='Save [Ctrl+s]']
    Wait For Load State    networkidle    timeout=30s

Click Toolbar Refresh
    Click    xpath=//a[@title='Refresh [Ctrl+r]']
    Wait For Load State    networkidle    timeout=30s

Handle Confirmation Dialog
    Wait For Elements State    ${CONFIRM_YES}    visible    10s
    Click    ${CONFIRM_YES}
    Wait For Load State    networkidle    timeout=15s

Click Status Tab
    [Arguments]    ${tab_num}
    Click    id=statusarea_tab:tabPanel:_sa_tab${tab_num}_header
    Wait For Load State    networkidle    timeout=10s

Get Record Status Value
    RETURN    Get Property    id=statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:0:C:4:in    value
```

---

## 14. PPT Slide Content — EC Standard Features Deep Dive

### Screen Bar (Slide 14)
- Shows logged-in user name (top right: `topForm:j_idt15`)
- Log off button: `xpath=//a[@title='Logout']`
- Help icon (3 lines): `topForm:dynaButton` (hamburger/settings)

### Tool Bar (Slides 16-17)
**Left to right order:**
1. 💾 Save — `xpath=//a[@title='Save [Ctrl+s]']`
2. ↺ Refresh — `xpath=//a[@title='Refresh [Ctrl+r]']`
3. ➕ New — submenu with `ui-icon-insert` — inserts blank row
4. 🗑️ Mark for deletion — submenu with `ui-icon-delete`
5. ↗️ Fullscreen — `id=screenToolbar:form:minmaxMenu`
6. ⭐ Add to Favorites — `id=screenToolbar:form:favorite`
7. ··· Settings/More — `id=screenToolbar:form:settingsSub`
8. 🔔 Task Notification — `id=screenToolbar:form:taskNotification`

### Navigator (Slide 18)
- Filters data for the screen
- Default settings remembered per user/group
- **Memory** — remembers choices within session
- **Dependencies** — child dropdowns filter based on parent
- **Go button** (`id=button:form:B`) — must click after any navigator change
- Trying to save without clicking Go first → EC shows error

### Status Area Tabs (Slide 19) — confirmed IDs
1. **Record Status** (`_sa_tab1`) — created_by, last_updated, record_status, rev_text
2. **Revision Info** (`_sa_tab2`) — history of all previous revisions from journal
3. **Approval Status** (`_sa_tab3`) — four-eye approval configuration
4. **Hints & Tips** (`_sa_tab4`) — free text user notes
5. **Validation** (`_sa_tab5`) — execute defined check rules
6. **Trending** (`_sa_tab6`) — trend graphs / PDF report
7. **Attachments** (`_sa_tab7`) — file attachments

### Data Table Menu (Slide 24)
All accessible via hamburger icon (`xpath=//span[contains(@id,'tfo')]`):
- Enable/disable column filters
- Enable scrollbar (combine all data in one page)
- Freeze selected columns
- Set rows per page
- Copy to clipboard (for Excel)
- Paste from clipboard (from Excel)
- Show/hide columns
- Reset to default
- Set as default for all users

### Excel Copy-Paste (Slides 25-27)
```robot
# Copy data from EC to clipboard
Click    xpath=//span[@title='Copy to Clipboard']
# Or via column header menu
```
```robot
# Paste from Excel back to EC
Click    xpath=//span[@title='Paste from Clipboard']
Wait For Load State    networkidle    timeout=15s
```

### Field Colours (Slide 22)
- Grey = read-only field → don't try to edit
- White = editable → can fill
- Yellow = mandatory → must fill before save
- Red/Yellow border → out of error/warning range (check rule triggered)

---

## 15. Variables File Updates for EC Project

```python
# vars/local.py — add these discovered IDs
EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
EC_USERNAME = 'sysadmin'
EC_PASSWORD = 'sysadmin'

# Key selectors (confirmed from live DOM)
SEARCH_INPUT_ID = 'menu:searchForm:searchTxt'
SEARCH_INPUT_XPATH = "xpath=//input[@id='menu:searchForm:searchTxt']"
TV_LINK_XPATH_TMPL = "xpath=//span[contains(@class,'tv-link') and normalize-space(text())='{name}']"
SCREEN_LABEL_ID = 'screenToolbar:form:screenLabel'
SCREEN_TOGGLE_ID = 'screenToolbar:form:minmaxMenu'
FAVORITES_BTN_ID = 'screenToolbar:form:favorite'
NOTIF_BELL_ID = 'screenToolbar:form:taskNotification'
GO_BUTTON_ID = 'button:form:B'
STATUS_AREA_ID = 'statusarea_tab:tabPanel'
CONFIRM_YES_CSS = 'css=.ui-confirmdialog-yes'
PAGINATION_LAST_CSS = 'css=span.ui-icon-seek-end'
TOOLBAR_SAVE_XPATH = "xpath=//a[@title='Save [Ctrl+s]']"
TOOLBAR_REFRESH_XPATH = "xpath=//a[@title='Refresh [Ctrl+r]']"
```
