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
    ...    NOT a pass on its own — always pair with the DB assertion below.
    [Arguments]    ${cell_id}    ${value}
    ${v}=    Get Cell Value By Id    ${cell_id}
    Should Be Equal As Numbers    ${v}    ${value}
    ...    msg=Grid cell ${cell_id} shows '${v}', expected '${value}'

Save Daily Status
    [Documentation]    Persist the edited grid via the toolbar Save (async). Always follow with
    ...    the DB assertion — the spinner/optimistic grid is not proof.
    Save

Daily Status Value In DB Should Be
    [Documentation]    GROUND TRUTH: assert the measured value really persisted to the
    ...    (object x day) status row. Resolves the well's OBJECT_ID from its display NAME, then
    ...    reads ${table}.${column} for that OBJECT_ID + ${date}. ${table} e.g. PWEL_DAY_STATUS.
    [Arguments]    ${table}    ${well_name}    ${date}    ${column}    ${expected}
    ${oid}=    Well Object Id By Name    ${well_name}
    Day Status Value Should Be    ${table}    ${oid}    ${date}    ${column}    ${expected}
