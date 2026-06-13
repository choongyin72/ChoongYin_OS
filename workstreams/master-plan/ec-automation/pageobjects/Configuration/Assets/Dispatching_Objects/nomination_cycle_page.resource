*** Settings ***
Documentation       T3 (screen) — Nomination Cycle page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Nomination Cycle.
...                 TABLE class (TV): inline grid, NO navigator, PHYSICAL delete.
...                 Cells: C0 Code (key) / C1 Name / C2 Sort Order / C3-C6 deadline TIMES
...                 (da_input, HH:MM) / C7 Gas Day Offset (dd). Base table NOMINATION_CYCLE
...                 (code in NOM_CYCLE_CODE).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/table_class.resource


*** Variables ***
${NOMCYC_SCREEN}    Nomination Cycle
${NOMCYC_GRID}      table:form:T_data
# cell id pattern: table:form:T:{row}:C{col}_in (C3..C6 use _da_input, C7 dd)


*** Keywords ***
Open Nomination Cycle Screen
    [Documentation]    Suite Setup: launch, login as ${user} (default env user), open the screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${NOMCYC_SCREEN}    ${user}    ${pass}

Nomination Cycle Cell Id
    [Documentation]    Build the cell input id for a grid row/column (text cells).
    [Arguments]    ${row}    ${col}
    RETURN    table:form:T:${row}:C${col}_in

Type Nomination Cycle Cell
    [Documentation]    Commit a value into the grid text cell at (row, col).
    [Arguments]    ${row}    ${col}    ${value}
    ${cid}=    Nomination Cycle Cell Id    ${row}    ${col}
    Type Cell By Id    ${cid}    ${value}

Type Nomination Cycle Time Cell
    [Documentation]    Commit an HH:MM value into a deadline time cell (C3..C6, _da_input).
    [Arguments]    ${row}    ${col}    ${value}
    Type Cell By Id    table:form:T:${row}:C${col}_da_input    ${value}

Find Nomination Cycle Row Index On Page
    [Documentation]    Return the T:N index whose C0 (code) equals ${code} on the CURRENT page, or -1.
    [Arguments]    ${code}
    ${idx}=    Evaluate JavaScript
    ...    ${None}
    ...    () => { let r=-1; document.querySelectorAll('input[id^="table:form:T:"][id$=":C0_in"]').forEach(i=>{ if((i.value||'').trim()==='${code}'){const m=i.id.match(/:T:(\\d+):C0_in/); if(m) r=parseInt(m[1]);}}); return r; }
    RETURN    ${idx}

Find Nomination Cycle Row
    [Documentation]    Search across paginator pages; return the T:N index or -1.
    [Arguments]    ${code}
    Go To First Page
    WHILE    True    limit=12    on_limit=pass
        ${idx}=    Find Nomination Cycle Row Index On Page    ${code}
        IF    ${idx} >= 0    RETURN    ${idx}
        ${more}=    Current Page Has Next
        IF    not ${more}    RETURN    ${-1}
        Go To Next Page
    END
    RETURN    ${-1}

Find Blank Nomination Cycle Row
    [Documentation]    Return the index of the first blank C0 row on the current page, or -1.
    ${idx}=    Find Nomination Cycle Row Index On Page    ${EMPTY}
    RETURN    ${idx}

Nomination Cycle Row Should Exist
    [Documentation]    Assert ${code} is present in the grid (across pages).
    [Arguments]    ${code}
    ${idx}=    Find Nomination Cycle Row    ${code}
    Should Be True    ${idx} >= 0    msg=Nomination Cycle ${code} not found in grid

Nomination Cycle Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the grid (across pages).
    [Arguments]    ${code}
    ${idx}=    Find Nomination Cycle Row    ${code}
    Should Be Equal As Integers    ${idx}    -1    msg=Nomination Cycle ${code} unexpectedly present

Nomination Cycle Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in NOMINATION_CYCLE.
    [Arguments]    ${code}
    Code Should Be Present In View    nomination_cycle    ${code}

Nomination Cycle Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was physically removed from NOMINATION_CYCLE.
    [Arguments]    ${code}
    Code Should Be Absent In View    nomination_cycle    ${code}

Fill Nomination Cycle Row
    [Documentation]    Fill a (blank) row: Code/Name/Sort + 4 deadline times + the
    ...    Gas Day Offset dd (C7 — leaving it empty makes Save silently reject and the
    ...    follow-up reload raises a blocking confirmation modal).
    [Arguments]    ${row}    ${code}    ${name}    ${sort}    ${offset}
    Type Nomination Cycle Cell    ${row}    0    ${code}
    Type Nomination Cycle Cell    ${row}    1    ${name}
    Type Nomination Cycle Cell    ${row}    2    ${sort}
    Type Nomination Cycle Time Cell    ${row}    3    11:00
    Type Nomination Cycle Time Cell    ${row}    4    14:00
    Type Nomination Cycle Time Cell    ${row}    5    15:00
    Type Nomination Cycle Time Cell    ${row}    6    06:00
    Select EC Dropdown Option    table:form:T:${row}:C7_dd    ${offset}

Insert Nomination Cycle
    [Documentation]    Add a blank row, fill it (incl. Gas Day Offset), Save, reload.
    [Arguments]    ${code}    ${name}    ${sort}    ${offset}=D-1
    Insert New Grid Row
    ${row}=    Find Blank Nomination Cycle Row
    Should Be True    ${row} >= 0    msg=No blank row after Insert
    Fill Nomination Cycle Row    ${row}    ${code}    ${name}    ${sort}    ${offset}
    Save
    Refresh Screen

Update Nomination Cycle Name
    [Documentation]    Find the row, edit the Name cell, Save, reload.
    [Arguments]    ${code}    ${name}
    ${row}=    Find Nomination Cycle Row    ${code}
    Should Be True    ${row} >= 0
    ${c1}=    Nomination Cycle Cell Id    ${row}    1
    Type Cell By Id    ${c1}    ${name}
    Save
    Refresh Screen

Nomination Cycle Name Should Be
    [Documentation]    Assert the Name cell of ${code} equals ${name}.
    [Arguments]    ${code}    ${name}
    ${row}=    Find Nomination Cycle Row    ${code}
    Should Be True    ${row} >= 0
    ${c1}=    Nomination Cycle Cell Id    ${row}    1
    ${val}=    Get Cell Value By Id    ${c1}
    Should Be Equal    ${val}    ${name}    msg=Name mismatch: ${val}

Delete Nomination Cycle
    [Documentation]    Select the row (safety-check it), physically delete, Save, reload.
    [Arguments]    ${code}
    ${row}=    Find Nomination Cycle Row    ${code}
    Should Be True    ${row} >= 0
    ${c0}=    Nomination Cycle Cell Id    ${row}    0
    Click    css=[id="${c0}"]
    Sleep    0.4s
    ${active}=    Get Cell Value By Id    ${c0}
    Should Be Equal    ${active}    ${code}    msg=SAFETY: active row is not the test row
    Delete Selected Grid Row    Nomination Cycle
    Save
    Refresh Screen
