*** Settings ***
Documentation       T3 (screen) - Create Calculation page object.
...                 Screen: Configuration > Assets > Calculation_Objects > Create Calculation (CO.1042).
...                 Context-gated TV-STYLE dual grid: nav = Date + ONE mandatory Calculation Context
...                 dd (first-available) + GO; header grid calculation:form:T_data (inline cells -
...                 INPUTS, so row checks read input VALUES via JS, not row text); companion
...                 VERSIONS grid calculation_version:form (the authoritative Calculation Name).
...                 INSERT = toolbar Insert 'Public Calculations' -> blank inline row (dynamic
...                 index - EC drops it mid-grid) -> C0 Code/C1 Name/C2 Start Date + C4 Period/C5
...                 Type dds (mandatory-yellow on the blank row; values from sibling rows).
...                 UPDATE = select row -> edit VERSIONS C0. DELETE = select row -> the purpose-
...                 built DELETE CALCULATION button (+ YES confirm). Header IUD only (no equations).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/table.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/navigator.resource


*** Variables ***
${SCR}              Create Calculation
${CC_GRID}          calculation:form:T
${CC_CTX_DD}        nav:form:G:1:R:1:C:0:dd
${CC_PERIOD}        Day
${CC_TYPE}          Equations


*** Keywords ***
Open Create Calculation Screen
    [Documentation]    Suite Setup: launch, login, open the screen, pick the FIRST Calculation
    ...    Context + GO (grid empty until then).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Select First EC Dropdown Option    ${CC_CTX_DD}
    Sleep    0.7s
    Apply Navigator

Create Calculation Row Index Of
    [Documentation]    Return the grid row index whose C0 (code) INPUT value equals ${code},
    ...    or ${None} - TV cells are inputs, invisible to text-based row scans.
    [Arguments]    ${code}
    ${idx}=    Evaluate JavaScript    ${None}
    ...    (arg) => { let hit = null; document.querySelectorAll("[id^='calculation:form:T:'][id$='C0_in']").forEach(e => { const m = e.id.match(/T:(\\d+):C0_in/); if (m && e.value.trim() === arg) hit = +m[1]; }); return hit; }
    ...    arg=${code}
    RETURN    ${idx}

Create Calculation Row Should Exist
    [Documentation]    Assert a calc row with code ${code} is present (input-value scan).
    [Arguments]    ${code}
    ${idx}=    Create Calculation Row Index Of    ${code}
    Should Not Be Equal    ${idx}    ${None}    msg=Calculation '${code}' not in grid

Create Calculation Row Should Not Exist
    [Documentation]    Assert no calc row with code ${code} (input-value scan).
    [Arguments]    ${code}
    ${idx}=    Create Calculation Row Index Of    ${code}
    Should Be Equal    ${idx}    ${None}    msg=Calculation '${code}' still in grid

Create Calculation Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_CALCULATION.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CALCULATION    ${code}

Create Calculation Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_CALCULATION.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CALCULATION    ${code}

Fill Calc Cell
    [Documentation]    TV inline-cell edit: click the cell input, select-all, REAL keystrokes, Tab.
    [Arguments]    ${cell_id}    ${value}
    Click    css=[id="${cell_id}"]
    Sleep    0.3s
    Keyboard Key    press    Control+a
    Type Text    css=[id="${cell_id}"]    ${value}    delay=25ms
    Keyboard Key    press    Tab
    Sleep    0.5s

Insert Blank Calc Row
    [Documentation]    Toolbar Insert -> 'Public Calculations' -> RETURN the new blank row's index
    ...    (dynamic - EC drops it mid-grid; found as the row whose C0 input is empty).
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Sleep    0.9s
    Click    xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='Public Calculations']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1s
    ${idx}=    Evaluate JavaScript    ${None}
    ...    () => { let hit = null; document.querySelectorAll("[id^='calculation:form:T:'][id$='C0_in']").forEach(e => { const m = e.id.match(/T:(\\d+):C0_in/); if (m && !e.value.trim() && hit === null) hit = +m[1]; }); return hit; }
    Should Not Be Equal    ${idx}    ${None}    msg=No blank insert row appeared
    RETURN    ${idx}

Insert Create Calculation Record
    [Documentation]    Insert the calc header: blank row -> Code/Name/Start Date cells + Period/Type
    ...    dds (mandatory-yellow on the blank row) -> Save -> reload.
    [Arguments]    ${code}    ${name}    ${start_date}
    ${r}=    Insert Blank Calc Row
    Fill Calc Cell    ${CC_GRID}:${r}:C0_in    ${code}
    Fill Calc Cell    ${CC_GRID}:${r}:C1_in    ${name}
    Fill Calc Cell    ${CC_GRID}:${r}:C2_da_input    ${start_date}
    Select EC Dropdown Option    ${CC_GRID}:${r}:C4_dd    ${CC_PERIOD}
    Select EC Dropdown Option    ${CC_GRID}:${r}:C5_dd    ${CC_TYPE}
    Save And Refresh List

Update Create Calculation Name
    [Documentation]    Select the calc row (loads its VERSIONS panel), edit the VERSIONS grid's
    ...    Calculation Name (the authoritative source - the header C1 only mirrors it), Save + reload.
    [Arguments]    ${code}    ${new_name}
    ${r}=    Create Calculation Row Index Of    ${code}
    Click    css=[id="${CC_GRID}:${r}:C0_in"]
    Sleep    1.2s
    Fill Calc Cell    calculation_version:form:T:0:C0_in    ${new_name}
    Save And Refresh List

Delete Create Calculation
    [Documentation]    Select the calc row, click the purpose-built DELETE CALCULATION button,
    ...    confirm (YES), reload. Physically removes the calc (+ its version) - DB-verified.
    [Arguments]    ${code}
    ${r}=    Create Calculation Row Index Of    ${code}
    Click    css=[id="${CC_GRID}:${r}:C0_in"]
    Sleep    1.2s
    Click    xpath=//button[normalize-space(.)='DELETE CALCULATION' or normalize-space(.)='Delete Calculation']
    Sleep    1.2s
    ${n}=    Get Element Count    xpath=//button[normalize-space(.)='YES' or normalize-space(.)='Yes']
    IF    ${n} > 0
        Click    xpath=//button[normalize-space(.)='YES' or normalize-space(.)='Yes']
    END
    Wait For Load State    networkidle    timeout=15s
    Apply Navigator
