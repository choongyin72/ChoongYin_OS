*** Settings ***
Documentation       T3 (screen) — "Sub Daily Gas Stream Status - by Stream" page object — the
...                 SUB-DAILY N1 generalization to a 2nd object class (STREAM, after PWEL). Proves
...                 the datetime-keyed sub-daily pattern is not a one-off: same intraday model as
...                 PWEL_SUB_DAY_STATUS but for STRM_SUB_DAY_STATUS, PK (OBJECT_ID, DAYTIME[+time],
...                 SUMMER_TIME). Reuses the sub-daily DbVerify helpers + the N1 T2 grid gestures.
...                 Non-iframed. Nav: Date (G:0) + cascade PU(G:1) → Area(G:2) → Facility(G:1 leaf
...                 stream, G:4). Grid shows one stream with the time down the rows.
...                 C0 = Daytime (resolve the row by its value — an input, scanned not page-text).
...                 C2 = Grs Vol[Sm³] = GRS_VOL (proven-editable, unitless → direct equality, no UI/DB
...                 conversion). ⚠️ C1 = On Strm[hr] is DERIVED/non-persisting — do NOT edit (the live
...                 edit→diff proved it). The target cell is NON-NULL (=1000), so the edit→diff is
...                 unambiguous and the self-clean restores the recorded original (1000). Name source = OV_STREAM.
...                 Recon: tmp/scripts/n1_subdaily_strm_*. Layered: this test → this T3 →
...                 daily_status_grid (T2) + common (T1) + DbVerify.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/daily_status_grid.resource


*** Variables ***
${SDS_SCREEN}              Sub Daily Gas Stream Status - by Stream
${SDS_GRID}               subDailyGasStreamStatusTable:form:T_data
${SDS_CELL_PREFIX}        subDailyGasStreamStatusTable:form:T
${SDS_DB_TABLE}           STRM_SUB_DAY_STATUS
# Navigator: Date (G:0) + cascade PU(G:1) → Area(G:2) → Facility(G:3) → Stream(G:4, leaf).
${SDS_DATE_FIELD}         nav:form:G:0:R:1:C:0:da_input
${NAV_PU}                 nav:form:G:1:R:1:C:0:dd
${NAV_AREA}               nav:form:G:2:R:1:C:0:dd
${NAV_FCTY}               nav:form:G:3:R:1:C:0:dd
${NAV_STREAM}             nav:form:G:4:R:1:C:0:dd
# Working scope (P1 gas stream with hourly P data on 2011-01-01; SUMMER_TIME single value).
${SCOPE_DATE}             2011-01-01
${SCOPE_PU}               P1 Production Unit
${SCOPE_AREA}             P1 Area
${SCOPE_FCTY}             P1 Facility 1
${SCOPE_STREAM}           P1 S059 M GAS PO.0028
# Target interval + cells. C0 = Daytime (row key, an input). C2 = Grs Vol[Sm³] = GRS_VOL — the real
# editable measured cell (proven editable on daily PO.0002; same unit UI↔DB → direct equality).
# NB: C1 "On Strm[hr]" is DERIVED/non-persisting on this grid (an edit to it doesn't commit) — same
# trap as sub-daily PWEL's On Strm cell; always edit→diff per screen to find the writable column.
${TARGET_HOUR}            00:00
${DAYTIME_COL}            C0
${CELL_COLUMN}            C2
${TARGET_DB_COLUMN}       GRS_VOL
${ORIGINAL_VALUE}         ${1000}
${TARGET_CELL}            ${EMPTY}


*** Keywords ***
Open Sub Daily Gas Stream Screen
    [Documentation]    Suite Setup: launch, open the screen, set Date, walk the cascade
    ...    (PU → Area → Facility → Stream), GO, then resolve the target interval row + cache its cell.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SDS_SCREEN}    ${user}    ${pass}
    Fill EC Date    ${SDS_DATE_FIELD}    ${SCOPE_DATE}
    Select EC Dropdown Option    ${NAV_PU}    ${SCOPE_PU}
    Select EC Dropdown Option    ${NAV_AREA}    ${SCOPE_AREA}
    Select EC Dropdown Option    ${NAV_FCTY}    ${SCOPE_FCTY}
    Select EC Dropdown Option    ${NAV_STREAM}    ${SCOPE_STREAM}
    Reload Daily Status Grid
    Reload And Find Target Interval

Reload And Find Target Interval
    [Documentation]    Re-apply GO and re-resolve the target interval's row/cell by its Daytime value
    ...    (use after a Save so the next edit arms on a freshly-rendered grid).
    Reload Daily Status Grid
    ${idx}=    Sub Daily Row Index For Daytime    ${SCOPE_DATE} ${TARGET_HOUR}
    Should Be True    ${idx} >= 0
    ...    msg=Interval '${SCOPE_DATE} ${TARGET_HOUR}' not found for stream '${SCOPE_STREAM}'
    VAR    ${TARGET_CELL}    ${SDS_CELL_PREFIX}:${idx}:${CELL_COLUMN}_in    scope=SUITE

Sub Daily Row Index For Daytime
    [Documentation]    Return the 0-based grid row whose Daytime cell (C0 input) holds ${daytime_text}
    ...    (e.g. '2011-01-01 00:00'). Daytime is an INPUT, so scan input values, not row text.
    [Arguments]    ${daytime_text}
    ${idx}=    Evaluate JavaScript    ${None}
    ...    () => { const tb=document.getElementById('${SDS_GRID}'); let i=-1; if(tb){ tb.querySelectorAll('tr').forEach((tr,n)=>{ const inp=tr.querySelector('[id$=":${DAYTIME_COL}_in"]'); if(inp && (inp.value||'').trim()==='${daytime_text}') i=n; }); } return i; }
    RETURN    ${idx}

Set Stream Cell
    [Documentation]    Edit the target interval's measured cell to ${value} (real keystrokes + Tab).
    [Arguments]    ${value}
    Edit Daily Status Cell    ${TARGET_CELL}    ${value}

Save Stream Status
    [Documentation]    Commit the grid edit via the toolbar Save (menubar, execute=@all).
    Save Daily Status

Stream Cell Should Show
    [Documentation]    Assert the on-screen cell shows ${value} (UI side; pair with the DB check).
    [Arguments]    ${value}
    Daily Status Cell Should Show    ${TARGET_CELL}    ${value}

Stream Value Should Be In DB
    [Documentation]    Ground truth: assert STRM_SUB_DAY_STATUS.${TARGET_DB_COLUMN} of the
    ...    (stream × date × hour) interval equals ${expected} (datetime-keyed; GRS_VOL unitless).
    [Arguments]    ${expected}
    ${oid}=    Object Id By Name    OV_STREAM    ${SCOPE_STREAM}
    Sub Day Status Value Should Be    ${SDS_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_HOUR}    ${TARGET_DB_COLUMN}    ${expected}

Restore Stream Cell To Original
    [Documentation]    Self-clean teardown: restore the (stream × date × hour) cell to its recorded
    ...    original (${ORIGINAL_VALUE}) at the DB so the test leaves the sandbox exactly as found.
    ${oid}=    Object Id By Name    OV_STREAM    ${SCOPE_STREAM}
    Reset Sub Day Status Value    ${SDS_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_HOUR}    ${TARGET_DB_COLUMN}    ${ORIGINAL_VALUE}
    Stream Value Should Be In DB    ${ORIGINAL_VALUE}
