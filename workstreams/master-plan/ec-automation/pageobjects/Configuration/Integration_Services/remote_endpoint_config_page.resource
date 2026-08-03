*** Settings ***
Documentation       T3 (screen) — Remote Endpoint Configuration page object.
...                 Screen: Configuration > Integration Services > Remote Endpoint Configuration (BF CO.1082).
...                 TV-style inline-editable grid, no navigator, physical delete (`TIME_SCOPE_CODE=INVARIANT`).
...                 Reuses shared T1 keywords (`Type Cell By Id`/`Select First EC Dropdown Option`/`Save`).
...
...                 QUIRK: Code must be lowercase alphanumeric + hyphens only (a DNS-slug format) -
...                 EC rejects the project's usual AUTOTEST_XX_ convention here with "Invalid Code,
...                 must consist of lower case alphanumeric characters or '-'...".

Library             Browser
Library             ../../../libraries/DbVerify.py
Resource            ../../../resources/common.resource
Resource            ../../../resources/table.resource
Resource            ../../../resources/toolbar.resource


*** Variables ***
${REC_SCREEN}       Remote Endpoint Configuration
${REC_TABLE}        endpointconfig:form:T_data


*** Keywords ***
Open Remote Endpoint Configuration Screen
    [Documentation]    Suite Setup: launch, login, navigate to the screen. No navigator on this
    ...    screen - the grid loads immediately on open.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${REC_SCREEN}    ${user}    ${pass}

Open Remote Endpoint Configuration Insert Menu
    [Documentation]    Insert toolbar (icon's OWN <li>) -> "Remote Endpoint configuration" (already
    ...    correctly title-cased) -> a blank row appears.
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Wait For Elements State
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul[contains(@class,'ui-menu-child')]//a
    ...    visible    timeout=10s
    Click
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul[contains(@class,'ui-menu-child')]//a
    Wait For Load State    networkidle    timeout=12s
    Sleep    1s

Find Remote Endpoint Configuration Row By Code
    [Documentation]    Return the 0-based row index whose Code cell (C0_in) equals ${code}, or -1
    ...    if not found. ${code}=${EMPTY} finds the first BLANK row (after Insert).
    [Arguments]    ${code}
    ${row}=    Evaluate JavaScript    ${None}
    ...    () => { const want = '${code}'; const m = document.querySelectorAll('input[id^="endpointconfig:form:T:"][id$=":C0_in"]'); for (const e of m) { if ((e.value||'') === want) { return parseInt(e.id.split(':')[3]); } } return -1; }
    RETURN    ${row}

Insert Remote Endpoint Configuration Record
    [Documentation]    Insert: Code (C0, lowercase-slug format) + Name (C1) + Remote Type
    ...    first-available (C2 dropdown) -> Save. Uses Type Cell By Id (real keystrokes + Tab).
    [Arguments]    ${code}    ${name}
    Open Remote Endpoint Configuration Insert Menu
    ${row}=    Find Remote Endpoint Configuration Row By Code    ${EMPTY}
    Should Be True    ${row} >= 0    msg=No blank row after Insert
    Type Cell By Id    endpointconfig:form:T:${row}:C0_in    ${code}
    Select First EC Dropdown Option    endpointconfig:form:T:${row}:C2_dd
    Type Cell By Id    endpointconfig:form:T:${row}:C1_in    ${name}
    Save
    Refresh Screen

Update Remote Endpoint Configuration Name
    [Documentation]    Find the row by code, edit Name (C1), Save.
    [Arguments]    ${code}    ${new_name}
    ${row}=    Find Remote Endpoint Configuration Row By Code    ${code}
    Should Be True    ${row} >= 0    msg=Row not found for update: ${code}
    Type Cell By Id    endpointconfig:form:T:${row}:C1_in    ${new_name}
    Save
    Refresh Screen

Open Remote Endpoint Configuration Delete Menu
    [Documentation]    Delete toolbar (icon's OWN <li>, scoped to avoid the identically-worded
    ...    Insert submenu item) -> click it.
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]
    Wait For Elements State
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]//ul[contains(@class,'ui-menu-child')]//a
    ...    visible    timeout=10s
    Click
    ...    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]//ul[contains(@class,'ui-menu-child')]//a
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.8s

Delete Remote Endpoint Configuration
    [Documentation]    Find the row by code, select it, Delete toolbar, Save (physical delete -
    ...    this class is TIME_SCOPE_CODE=INVARIANT).
    [Arguments]    ${code}
    ${row}=    Find Remote Endpoint Configuration Row By Code    ${code}
    Should Be True    ${row} >= 0    msg=Row not found for delete: ${code}
    Click    css=[id="endpointconfig:form:T:${row}:C0_in"]
    Sleep    0.4s
    Open Remote Endpoint Configuration Delete Menu
    Save
    Refresh Screen

Remote Endpoint Configuration Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_ENDPOINT_CONFIG.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_ENDPOINT_CONFIG    ${code}

Remote Endpoint Configuration Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was physically deleted from OV_ENDPOINT_CONFIG.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_ENDPOINT_CONFIG    ${code}
