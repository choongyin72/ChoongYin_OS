*** Settings ***
Documentation       T2 pattern — N1 Daily/Monthly STATUS data-entry grid (edit-in-place).
...                 The Pluto operational core: for a chosen DATE + object-scope cascade, the
...                 screen shows a grid of PRE-INSTANTIATED (object x day) rows whose measured
...                 cells you EDIT (no insert/delete). Reachable at top level (the screen is the
...                 main frame — no iframe piercing). Built entirely on existing T1 keywords
...                 (navigator/table/toolbar) + the DbVerify day-status helpers.
...                 Recon + design: docs/pattern_n1_daily_status_grid_design.md.
...                 Screen-specific bits (nav-group ids, scope, grid/cell ids, DB table) live in
...                 the T3 page object; this layer is the cross-screen N1 mechanics.

Library             String
Library             Browser
Library             ../libraries/DbVerify.py
Resource            common.resource


*** Variables ***
# The N1 navigator's Date is group G:0 on every daily-status screen seen so far.
${DS_NAV_DATE_FIELD}    nav:form:G:0:R:1:C:0:da_input


*** Keywords ***
Set Daily Status Date
    [Documentation]    Set the navigator Date (the period whose status rows to load). Use a
    ...    DATA-BEARING date — reference dds + grid only show objects effective at this date
    ...    (object-start-date = version filter; e.g. the seed epoch 2003-01-01 in the sandbox).
    [Arguments]    ${date}
    Fill EC Date    ${DS_NAV_DATE_FIELD}    ${date}

Reload Daily Status Grid
    [Documentation]    Click the navigator Go (button:form:B) to (re)load the grid for the
    ...    current Date + scope. Mandatory after setting any navigator value.
    Apply Navigator

Daily Status Row Index For
    [Documentation]    Return the 0-based row index of the grid row whose text contains ${name}
    ...    (the object/well display name). The grid is NOT ordered as you'd guess — e.g. on
    ...    WR.0001, 'AS2_Onshore Well no 2' is row 1, not row 0 — so ALWAYS resolve by name,
    ...    never hardcode the row. Returns -1 if not found.
    [Arguments]    ${grid_id}    ${name}
    ${idx}=    Evaluate JavaScript    ${None}
    ...    () => { const tb=document.getElementById('${grid_id}'); let i=-1; if(tb){tb.querySelectorAll('tr').forEach((tr,n)=>{ if((tr.textContent||'').includes('${name}')) i=n; });} return i; }
    RETURN    ${idx}

Edit Daily Status Cell
    [Documentation]    Edit one measured-value cell of a pre-instantiated (object x day) row.
    ...    PROVEN GESTURE (DB-verified 2026-06-13): real keystrokes + Tab fire the cell's `change`
    ...    behavior (POST source=...C{c}_in event=change) which STAGES the value server-side; then
    ...    `Save Daily Status` (menubar, execute=@all) COMMITS it. The value MUST differ from what
    ...    the cell currently shows or no change event fires (a fill()/no-op stages nothing).
    ...    Type Cell By Id does the real-keystroke+Tab correctly. ${cell_id} e.g.
    ...    daily_well_status:form:T:1:C4_in.
    [Arguments]    ${cell_id}    ${value}
    Type Cell By Id    ${cell_id}    ${value}

Daily Status Cell Should Show
    [Documentation]    Assert the on-screen grid cell currently displays ${value} (UI-side).
    ...    Comma-tolerant: EC formats large numbers with thousands separators (e.g. 2,949.9), so
    ...    strip commas before the numeric compare. NOT a pass on its own — pair with the DB check.
    [Arguments]    ${cell_id}    ${value}
    ${v}=    Get Cell Value By Id    ${cell_id}
    ${vclean}=    Replace String    ${v}    ,    ${EMPTY}
    ${expclean}=    Replace String    ${value}    ,    ${EMPTY}
    Should Be Equal As Numbers    ${vclean}    ${expclean}
    ...    msg=Grid cell ${cell_id} shows '${v}', expected '${value}'

Read Daily Status Cell
    [Documentation]    Return a grid cell's current value with thousands-separator commas stripped
    ...    (so the raw number can be re-typed/compared). e.g. '2,949.9' -> '2949.9'.
    [Arguments]    ${cell_id}
    ${v}=    Get Cell Value By Id    ${cell_id}
    ${clean}=    Replace String    ${v}    ,    ${EMPTY}
    RETURN    ${clean}

Save Daily Status
    [Documentation]    Persist the edited grid via the toolbar Save (async). Always follow with
    ...    the DB assertion — the spinner/optimistic grid is not proof.
    Save

Clear Daily Status Cell
    [Documentation]    Clear a measured cell (focus → select-all → Delete → Tab) so its change event
    ...    stages an EMPTY value — the UI-driven DELETE of a daily value. After `Save Daily Status` this
    ...    nulls the DB column (DB-proven on IFLW 2026-06-15: clear + Save → ON_STREAM_HRS NULL).
    ...    The cell must currently hold a value (else no change event fires).
    [Arguments]    ${cell_id}
    Click    css=[id="${cell_id}"]
    Keyboard Key    press    Control+A
    Keyboard Key    press    Delete
    Keyboard Key    press    Tab
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.6s

# GROUND-TRUTH DB assertion: each T3 resolves its object's OBJECT_ID via the DbVerify library
# keyword `Object Id By Name  <name_source>  <name>` (WELL_VERSION / OV_STREAM / ...), then calls
# `Day Status Value Should Be  <table>  <oid>  <date>  <column>  <expected>`. Kept in the T3 (not a
# shared wrapper) so this layer stays within the arg-count limit and each screen owns its resolver.
