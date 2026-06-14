*** Settings ***
Documentation       T3 (screen) — "Sub Daily Production Well Status 1 - by Well" page object — the
...                 N1 SUB-DAILY generalization (intraday intervals). Screen: EC Production (search)
...                 > Sub Daily Production Well Status 1 - by Well. Same edit-in-place N1 mechanics
...                 as the daily well screens (reuses daily_status_grid T2: same `:T:{r}:C{c}_in`
...                 cell pattern + same Save gesture) BUT the DB row is keyed by the full DATETIME:
...                 PWEL_SUB_DAY_STATUS PK = (OBJECT_ID, DAYTIME[+time-of-day], SUMMER_TIME), so each
...                 grid row is one intraday interval, not one object. The grid shows ONE well with
...                 the time down the rows ("Daytime" column), so the target row is resolved by its
...                 Daytime value (an input — scanned by value, not page text), and the DB oracle is
...                 the datetime-keyed `Sub Day Status Value Should Be` (date + HH:MI).
...
...                 Non-iframed. 4-level nav cascade PU → Area → Facility Class 1 → Well (leaf), GO.
...                 Cell C3 = On Strm[hr] = ON_STREAM_HRS (DIFFERENT C-col than the daily screens'
...                 C4 — per-screen edit→diff; here null-original, proven by the edit→Save→DB test).
...                 Null-original cell → self-clean = DB-restore to NULL (like IWEL/EQPM).
...                 Layered: this test → this T3 → daily_status_grid (T2) + common (T1) + DbVerify.
...                 Recon: docs/pattern_n1_daily_status_grid_design.md §Sub-daily; tmp/scripts/n1_subdaily_*.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/daily_status_grid.resource


*** Variables ***
${SUBDAILY_SCREEN}          Sub Daily Production Well Status 1 - by Well
${SUBDAILY_GRID}            subDailyWellStatusTable:form:T_data
${SUBDAILY_CELL_PREFIX}     subDailyWellStatusTable:form:T
${SUBDAILY_DB_TABLE}        PWEL_SUB_DAY_STATUS
# Navigator cascade groups (nav:form:G:{n}) — PU → Area → Facility Class 1 → Well (leaf).
${NAV_PU}                   G:1
${NAV_AREA}                 G:2
${NAV_FCTY_CLASS_1}         G:3
${NAV_WELL}                 G:4
# Working scope (FRMW framework data; clean hourly set 00:00–23:00, all P, SUMMER_TIME='Y').
${SCOPE_DATE}               2024-10-01
${SCOPE_PU}                 FRMW PU
${SCOPE_AREA}               FRMW Area
${SCOPE_FCTY_CLASS_1}       FRMW Facility 1
${SCOPE_WELL}               FRMW Well 1
# Target interval + cell + DB column. C3 = On Strm[hr]; the DB key is date + this hour.
${TARGET_HOUR}              00:00
${CELL_COLUMN}              C3
${TARGET_DB_COLUMN}         ON_STREAM_HRS
${TARGET_CELL}              ${EMPTY}


*** Keywords ***
Open Sub Daily Well Status Screen
    [Documentation]    Suite Setup: launch, login, open the screen, set the data-bearing Date, walk
    ...    the nav cascade (PU → Area → Facility Class 1 → Well), GO, then resolve the target
    ...    interval's row by its Daytime and cache its measured-cell id.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SUBDAILY_SCREEN}    ${user}    ${pass}
    Set Daily Status Date    ${SCOPE_DATE}
    Set Navigator Filter    ${NAV_PU}    ${SCOPE_PU}
    Set Navigator Filter    ${NAV_AREA}    ${SCOPE_AREA}
    Set Navigator Filter    ${NAV_FCTY_CLASS_1}    ${SCOPE_FCTY_CLASS_1}
    Set Navigator Filter    ${NAV_WELL}    ${SCOPE_WELL}
    Reload Daily Status Grid
    Reload And Find Target Interval

Reload And Find Target Interval
    [Documentation]    Re-apply the navigator GO and re-resolve the target interval's row/cell by its
    ...    Daytime value (use after a Save so the next edit arms on a freshly-rendered grid).
    Reload Daily Status Grid
    ${idx}=    Sub Daily Row Index For Daytime    ${SCOPE_DATE} ${TARGET_HOUR}
    Should Be True    ${idx} >= 0
    ...    msg=Interval '${SCOPE_DATE} ${TARGET_HOUR}' not found for well '${SCOPE_WELL}' in the loaded grid
    VAR    ${TARGET_CELL}    ${SUBDAILY_CELL_PREFIX}:${idx}:${CELL_COLUMN}_in    scope=SUITE

Sub Daily Row Index For Daytime
    [Documentation]    Return the 0-based grid row whose "Daytime" cell (the C1 input) holds
    ...    ${daytime_text} (e.g. '2024-10-01 00:00'). The Daytime is an INPUT, so its value is not in
    ...    the row text — scan input values, not textContent. Robust to row re-ordering after a Save.
    ...    Returns -1 if not found.
    [Arguments]    ${daytime_text}
    ${idx}=    Evaluate JavaScript    ${None}
    ...    () => { const tb=document.getElementById('${SUBDAILY_GRID}'); let i=-1; if(tb){ tb.querySelectorAll('tr').forEach((tr,n)=>{ const inp=tr.querySelector('[id$=":C1_in"]'); if(inp && (inp.value||'').trim()==='${daytime_text}') i=n; }); } return i; }
    RETURN    ${idx}

Set Sub Daily Cell
    [Documentation]    Edit the target interval's measured cell to ${value} (real keystrokes + Tab).
    [Arguments]    ${value}
    Edit Daily Status Cell    ${TARGET_CELL}    ${value}

Save Sub Daily Status
    [Documentation]    Commit the grid edit via the toolbar Save (menubar, execute=@all).
    Save Daily Status

Sub Daily Cell Should Show
    [Documentation]    Assert the on-screen cell shows ${value} (UI side; pair with the DB check).
    [Arguments]    ${value}
    Daily Status Cell Should Show    ${TARGET_CELL}    ${value}

Sub Daily Value Should Be In DB
    [Documentation]    Ground truth: assert PWEL_SUB_DAY_STATUS.${TARGET_DB_COLUMN} of the
    ...    (well × date × hour) interval equals ${expected} — datetime-keyed (date + HH:MI).
    [Arguments]    ${expected}
    ${oid}=    Object Id By Name    WELL_VERSION    ${SCOPE_WELL}
    Sub Day Status Value Should Be    ${SUBDAILY_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_HOUR}    ${TARGET_DB_COLUMN}    ${expected}

Restore Sub Daily Cell To Null
    [Documentation]    Self-clean teardown: restore the (well × date × hour) cell to NULL at the DB so
    ...    the test leaves the sandbox exactly as found (cell was NULL-original; UI-clear is unreliable).
    ${oid}=    Object Id By Name    WELL_VERSION    ${SCOPE_WELL}
    Reset Sub Day Status Value    ${SUBDAILY_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_HOUR}    ${TARGET_DB_COLUMN}
    Sub Daily Value Should Be In DB    ${None}
