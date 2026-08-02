*** Settings ***
Documentation       T3 (screen) - Constant Standard page object.
...                 Screen: Configuration > Assets > Hydrocarbon_Objects > Constant Standard.
...                 TV-style inline-editable grid (cstandard:form:T_data), despite
...                 CLASS_TYPE=OBJECT/VERSIONED per class_cnfg. Insert menu item's real text is
...                 title-case ("Constant Standard") - the visible ALL-CAPS is CSS styling, not
...                 the DOM text; scoped to the Insert icon's OWN <li> since Delete's <li> has an
...                 identically-worded item. Delete = End Date = Start Date in the inline cell
...                 (this class IS date-effective despite the TV-looking grid), not a physical
...                 toolbar delete.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource


*** Variables ***
${SCR}              Constant Standard
${GRID}             cstandard:form:T_data
${VIEW}             OV_CONSTANT_STANDARD


*** Keywords ***
Open Constant Standard Screen
    [Documentation]    Suite Setup: launch, login, open Constant Standard (no navigator).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}

Find Constant Standard Row By Code
    [Documentation]    Return the T:N index whose C0 (Standard Code) equals ${code}, or -1.
    [Arguments]    ${code}
    ${idx}=    Evaluate JavaScript
    ...    ${None}
    ...    () => { const m=document.querySelectorAll('input[id^="cstandard:form:T:"][id$=":C0_in"]');
    ...    for (const e of m) { if ((e.value||'')==='${code}') { const r=e.id.match(/:T:(\\d+):/); if(r) return parseInt(r[1]); } }
    ...    return -1; }
    RETURN    ${idx}

Constant Standard Row Should Exist
    [Documentation]    Assert ${code} is present in the grid.
    [Arguments]    ${code}
    ${idx}=    Find Constant Standard Row By Code    ${code}
    Should Be True    ${idx} >= 0    msg=Constant Standard ${code} not found in grid

Constant Standard Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the grid.
    [Arguments]    ${code}
    ${idx}=    Find Constant Standard Row By Code    ${code}
    Should Be Equal As Integers    ${idx}    -1    msg=Constant Standard ${code} unexpectedly present

Constant Standard Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in ${VIEW}.
    [Arguments]    ${code}
    Code Should Be Present In View    ${VIEW}    ${code}

Constant Standard Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} closed out of ${VIEW} (End=Start).
    [Arguments]    ${code}
    Code Should Be Absent In View    ${VIEW}    ${code}

Constant Standard Row Should Show Name
    [Documentation]    Assert the Name cell (C1) of ${code} equals ${name}.
    [Arguments]    ${code}    ${name}
    ${idx}=    Find Constant Standard Row By Code    ${code}
    Should Be True    ${idx} >= 0
    ${val}=    Get Cell Value By Id    cstandard:form:T:${idx}:C1_in
    Should Be Equal    ${val}    ${name}    msg=Name mismatch: ${val}

Open Constant Standard Insert Menu
    [Documentation]    Insert toolbar (icon's OWN <li>) -> the REAL title-case menu item text
    ...    ("Constant Standard", not the displayed ALL-CAPS) -> a blank row appears.
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Wait For Elements State
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Constant Standard']
    ...    visible    timeout=10s
    Click
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Constant Standard']
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.5s

Insert Constant Standard Record
    [Documentation]    Open the Insert menu, then fill Standard Code / Standard Name / Start Date /
    ...    Daytime (Daytime is a genuinely separate mandatory field, not derived from Start Date) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open Constant Standard Insert Menu
    ${row}=    Find Constant Standard Row By Code    ${EMPTY}
    Should Be True    ${row} >= 0    msg=No blank row after Insert
    Type Cell By Id    cstandard:form:T:${row}:C0_in    ${code}
    Type Cell By Id    cstandard:form:T:${row}:C1_in    ${name}
    Type Cell By Id    cstandard:form:T:${row}:C2_da_input    ${start_date}
    Type Cell By Id    cstandard:form:T:${row}:C4_da_input    ${start_date}
    Save
    Refresh Screen

Update Constant Standard Name
    [Documentation]    Find the row, edit the Name cell (C1), Save.
    [Arguments]    ${code}    ${new_name}
    ${row}=    Find Constant Standard Row By Code    ${code}
    Should Be True    ${row} >= 0
    Type Cell By Id    cstandard:form:T:${row}:C1_in    ${new_name}
    Save
    Refresh Screen

Delete Constant Standard
    [Documentation]    This class IS date-effective (VERSIONED) despite the TV-looking grid -
    ...    set End Date (C3) = Start Date directly in the inline cell, then Save. NOT a physical
    ...    toolbar delete (Delete Selected Grid Row does not apply here).
    [Arguments]    ${code}    ${start_date}
    ${row}=    Find Constant Standard Row By Code    ${code}
    Should Be True    ${row} >= 0
    Type Cell By Id    cstandard:form:T:${row}:C3_da_input    ${start_date}
    Save
    Refresh Screen
