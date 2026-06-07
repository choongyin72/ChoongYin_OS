*** Settings ***
Documentation       T3 (screen) — MIME Type Mapping page object.
...                 Screen: Configuration > System > MIME Type Mapping.
...                 TABLE class (TV view): inline-editable paginated grid, NO navigator,
...                 PHYSICAL delete. Does NOT use manage_object (T2) or navigator.
...                 Table-class IUD flow lives here for now (only Table-class screen);
...                 promote to a table_class.resource (T2) when a 2nd one appears.

Library             Browser
Library             ../../../libraries/DbVerify.py
Resource            ../../../resources/common.resource


*** Variables ***
${MIME_SCREEN}      MIME Type Mapping
${MIME_GRID}        mime_type_table:form:T_data
# cell input id pattern: mime_type_table:form:T:{row}:C{col}_in    (C0 = MIME Type, C1 = File Extensions)


*** Keywords ***
Open MIME Screen
    [Documentation]    Suite Setup: launch, login as ${user} (default env user), open MIME (no navigator).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${MIME_SCREEN}

MIME Cell Id
    [Documentation]    Build the cell input id for a grid row/column.
    [Arguments]    ${row}    ${col}
    RETURN    mime_type_table:form:T:${row}:C${col}_in

Find MIME Row Index On Page
    [Documentation]    Return the T:N index of ${mime} in C0 cells on the CURRENT page, or -1.
    [Arguments]    ${mime}
    ${idx}=    Evaluate JavaScript
    ...    ${None}
    ...    () => { let r=-1; document.querySelectorAll('input[id^="mime_type_table:form:T:"][id$=":C0_in"]').forEach(i=>{ if((i.value||'').trim()==='${mime}'){const m=i.id.match(/:T:(\\d+):C0_in/); if(m) r=parseInt(m[1]);}}); return r; }
    RETURN    ${idx}

Find MIME Row
    [Documentation]    Search across paginator pages; return the T:N index or -1.
    [Arguments]    ${mime}
    Go To First Page
    WHILE    True    limit=12    on_limit=pass
        ${idx}=    Find MIME Row Index On Page    ${mime}
        IF    ${idx} >= 0    RETURN    ${idx}
        ${more}=    Current Page Has Next
        IF    not ${more}    RETURN    ${-1}
        Go To Next Page
    END
    RETURN    ${-1}

Find Blank MIME Row
    [Documentation]    Return the index of the first blank C0 row on the current page, or -1.
    ${idx}=    Find MIME Row Index On Page    ${EMPTY}
    RETURN    ${idx}

MIME Row Should Exist
    [Documentation]    Assert ${mime} is present in the grid (across pages).
    [Arguments]    ${mime}
    ${idx}=    Find MIME Row    ${mime}
    Should Be True    ${idx} >= 0    msg=MIME ${mime} not found in grid

MIME Row Should Not Exist
    [Documentation]    Assert ${mime} is absent from the grid (across pages).
    [Arguments]    ${mime}
    ${idx}=    Find MIME Row    ${mime}
    Should Be Equal As Integers    ${idx}    -1    msg=MIME ${mime} unexpectedly present

MIME Should Exist In DB
    [Documentation]    DB ground-truth: assert ${mime} persisted in the base table.
    [Arguments]    ${mime}
    Code Should Be Present In View    ctrl_mime_type_mapping    ${mime}

MIME Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${mime} was physically removed from the base table.
    [Arguments]    ${mime}
    Code Should Be Absent In View    ctrl_mime_type_mapping    ${mime}

Insert New Grid Row
    [Documentation]    Insert toolbar -> first submenu item -> a blank editable row appears.
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Wait For Elements State    xpath=(//ul[contains(@class,'ui-menu-child')]//li//a)[1]    visible    timeout=10s
    Click    xpath=(//ul[contains(@class,'ui-menu-child')]//li//a)[1]
    Wait For Load State    networkidle    timeout=12s
    Sleep    1s

Delete Selected Grid Row
    [Documentation]    Delete toolbar -> the "MIME Type Mapping" item, scoped to the DELETE
    ...    menu-parent (the Insert submenu has an identically named item).
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]
    Wait For Elements State
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='MIME Type Mapping']
    ...    visible
    ...    timeout=10s
    Click
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='MIME Type Mapping']
    Wait For Load State    networkidle    timeout=12s
    Sleep    1s

Insert MIME Mapping
    [Documentation]    Add a blank row, type MIME type + extensions (Tab-commit), Save, reload.
    [Arguments]    ${mime}    ${ext}
    Insert New Grid Row
    ${row}=    Find Blank MIME Row
    Should Be True    ${row} >= 0    msg=No blank row after Insert
    ${c0}=    MIME Cell Id    ${row}    0
    ${c1}=    MIME Cell Id    ${row}    1
    Type Cell By Id    ${c0}    ${mime}
    Type Cell By Id    ${c1}    ${ext}
    Save
    Refresh Screen

Update MIME Extensions
    [Documentation]    Find the row, edit the File Extensions cell, Save, reload.
    [Arguments]    ${mime}    ${ext}
    ${row}=    Find MIME Row    ${mime}
    Should Be True    ${row} >= 0
    ${c1}=    MIME Cell Id    ${row}    1
    Type Cell By Id    ${c1}    ${ext}
    Save
    Refresh Screen

MIME Extensions Should Be
    [Documentation]    Assert the File Extensions cell of ${mime} equals ${ext}.
    [Arguments]    ${mime}    ${ext}
    ${row}=    Find MIME Row    ${mime}
    Should Be True    ${row} >= 0
    ${c1}=    MIME Cell Id    ${row}    1
    ${val}=    Get Cell Value By Id    ${c1}
    Should Be Equal    ${val}    ${ext}    msg=Extensions mismatch: ${val}

Delete MIME Mapping
    [Documentation]    Select the row (safety-check it), physically delete, Save, reload.
    [Arguments]    ${mime}
    ${row}=    Find MIME Row    ${mime}
    Should Be True    ${row} >= 0
    ${c0}=    MIME Cell Id    ${row}    0
    Click    css=[id="${c0}"]
    Sleep    0.4s
    ${active}=    Get Cell Value By Id    ${c0}
    Should Be Equal    ${active}    ${mime}    msg=SAFETY: active row is not the test row
    Delete Selected Grid Row
    Save
    Refresh Screen
