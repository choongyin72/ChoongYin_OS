*** Settings ***
Documentation       T3 (screen) — Language page object.
...                 Screen: Configuration > System > Language.
...                 TABLE class (TV): inline-editable grid, NO navigator, PHYSICAL delete.
...                 Cells: C0 = Id (LANGUAGE_ID, REQUIRED/yellow) / C1 = Language (code, key) / C2 = Name.
...                 Base table T_BASIS_LANGUAGE (code in the LANGUAGE column).

Library             Browser
Library             ../../../libraries/DbVerify.py
Resource            ../../../resources/common.resource
Resource            ../../../resources/table_class.resource


*** Variables ***
${LANG_SCREEN}      Language
${LANG_GRID}        table:form:T_data
# cell id pattern: table:form:T:{row}:C{col}_in    (C0 Id / C1 Language code / C2 Name)


*** Keywords ***
Open Language Screen
    [Documentation]    Suite Setup: launch, login as ${user} (default env user), open Language (no navigator).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${LANG_SCREEN}

Language Cell Id
    [Documentation]    Build the cell input id for a grid row/column.
    [Arguments]    ${row}    ${col}
    RETURN    table:form:T:${row}:C${col}_in

Type Language Cell
    [Documentation]    Commit a value into the grid cell at (row, col).
    [Arguments]    ${row}    ${col}    ${value}
    ${cid}=    Language Cell Id    ${row}    ${col}
    Type Cell By Id    ${cid}    ${value}

Find Language Row Index On Page
    [Documentation]    Return the T:N index whose C1 (code) equals ${code} on the CURRENT page, or -1.
    [Arguments]    ${code}
    ${idx}=    Evaluate JavaScript
    ...    ${None}
    ...    () => { let r=-1; document.querySelectorAll('input[id^="table:form:T:"][id$=":C1_in"]').forEach(i=>{ if((i.value||'').trim()==='${code}'){const m=i.id.match(/:T:(\\d+):C1_in/); if(m) r=parseInt(m[1]);}}); return r; }
    RETURN    ${idx}

Find Language Row
    [Documentation]    Search across paginator pages; return the T:N index or -1.
    [Arguments]    ${code}
    Go To First Page
    WHILE    True    limit=12    on_limit=pass
        ${idx}=    Find Language Row Index On Page    ${code}
        IF    ${idx} >= 0    RETURN    ${idx}
        ${more}=    Current Page Has Next
        IF    not ${more}    RETURN    ${-1}
        Go To Next Page
    END
    RETURN    ${-1}

Find Blank Language Row
    [Documentation]    Return the index of the first blank C1 row on the current page, or -1.
    ${idx}=    Find Language Row Index On Page    ${EMPTY}
    RETURN    ${idx}

Language Row Should Exist
    [Documentation]    Assert ${code} is present in the grid (across pages).
    [Arguments]    ${code}
    ${idx}=    Find Language Row    ${code}
    Should Be True    ${idx} >= 0    msg=Language ${code} not found in grid

Language Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the grid (across pages).
    [Arguments]    ${code}
    ${idx}=    Find Language Row    ${code}
    Should Be Equal As Integers    ${idx}    -1    msg=Language ${code} unexpectedly present

Language Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in T_BASIS_LANGUAGE.
    [Arguments]    ${code}
    Code Should Be Present In View    t_basis_language    ${code}

Language Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was physically removed from T_BASIS_LANGUAGE.
    [Arguments]    ${code}
    Code Should Be Absent In View    t_basis_language    ${code}

Insert Language
    [Documentation]    Add a blank row; fill Id (required) + Language code + Name; Save; reload.
    [Arguments]    ${id}    ${code}    ${name}
    Insert New Grid Row
    ${row}=    Find Blank Language Row
    Should Be True    ${row} >= 0    msg=No blank row after Insert
    Type Language Cell    ${row}    0    ${id}
    Type Language Cell    ${row}    1    ${code}
    Type Language Cell    ${row}    2    ${name}
    Save
    Refresh Screen

Update Language Name
    [Documentation]    Find the row, edit the Name cell, Save, reload.
    [Arguments]    ${code}    ${name}
    ${row}=    Find Language Row    ${code}
    Should Be True    ${row} >= 0
    ${c2}=    Language Cell Id    ${row}    2
    Type Cell By Id    ${c2}    ${name}
    Save
    Refresh Screen

Language Name Should Be
    [Documentation]    Assert the Name cell of ${code} equals ${name}.
    [Arguments]    ${code}    ${name}
    ${row}=    Find Language Row    ${code}
    Should Be True    ${row} >= 0
    ${c2}=    Language Cell Id    ${row}    2
    ${val}=    Get Cell Value By Id    ${c2}
    Should Be Equal    ${val}    ${name}    msg=Name mismatch: ${val}

Delete Language
    [Documentation]    Select the row (safety-check it), physically delete, Save, reload.
    [Arguments]    ${code}
    ${row}=    Find Language Row    ${code}
    Should Be True    ${row} >= 0
    ${c1}=    Language Cell Id    ${row}    1
    Click    css=[id="${c1}"]
    Sleep    0.4s
    ${active}=    Get Cell Value By Id    ${c1}
    Should Be Equal    ${active}    ${code}    msg=SAFETY: active row is not the test row
    Delete Selected Grid Row    Language
    Save
    Refresh Screen
