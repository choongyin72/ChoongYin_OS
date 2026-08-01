*** Settings ***
Documentation       T3 (screen) - Action Trigger page object.
...                 Screen: Configuration > Business Action > Action Trigger (CO.0193).
...                 CUSTOM-URL OV: grid nav:form:T_data, NO navigator, NO GO button - cross-checked
...                 directly against class_cnfg/treeview (class CONTROL_POINT, VERSIONED). Fields
...                 resolved BY LABEL. 5 mandatory: Code, Name, Start date, Action Trigger Type (dd),
...                 Trigger Type (dd) - neither dropdown is scope-dependent (no navigator), both
...                 probed live with non-empty option lists. DELETE = End Date = Start Date.
...
...                 OPT-IN MANDATORY-FIELD GATE: this is the FIRST screen to adopt the standalone
...                 mandatory_field_gate.resource (owner-directed, built/tested 2026-08-01) - a
...                 PROACTIVE check for mandatory-and-empty fields BEFORE Save is clicked, instead of
...                 relying only on EC's post-Save error banner. Insert/Update keywords below inline
...                 Save And Refresh List's own logic (Save -> GO-or-Refresh) with the gate call
...                 placed just before Save - manage_object.resource itself is NOT modified.

Library             Browser
Library             ../../../libraries/DbVerify.py
Resource            ../../../resources/common.resource
Resource            ../../../resources/manage_object.resource
Resource            ../../../resources/mandatory_field_gate.resource


*** Variables ***
${SCR}              Action Trigger
${TBL}              nav:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Action Trigger Screen
    [Documentation]    Suite Setup: launch, login, open the screen (custom-URL OV: grid loads
    ...    directly, no navigator cascade to fill).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}

Action Trigger Row Should Exist
    [Documentation]    Assert ${code} is present (await grid redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Action Trigger Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Action Trigger Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_CONTROL_POINT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CONTROL_POINT    ${code}

Action Trigger Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_CONTROL_POINT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CONTROL_POINT    ${code}

Action Trigger Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Fill Action Trigger Mandatory Fields
    [Documentation]    Fill the 5 mandatory New-Object fields BY LABEL. Split out from Insert Action
    ...    Trigger Record to keep both keywords under robocop's LEN03 keyword-count limit.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill OV Field By Label       objectForm    Action Trigger Code    ${code}
    Fill OV Field By Label       objectForm    Action Trigger Name    ${name}
    Fill OV Date By Label        objectForm    Start date             ${start_date}
    Fill OV Dropdown By Label    objectForm    Action Trigger Type    __FIRST__
    Fill OV Dropdown By Label    objectForm    Trigger Type           __FIRST__

Insert Action Trigger Record
    [Documentation]    Insert (all fields BY LABEL), gate-check for empty mandatory fields BEFORE
    ...    Save, then Save + reload (inlines Save And Refresh List's own GO-or-Refresh logic).
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill Action Trigger Mandatory Fields    ${code}    ${name}    ${start_date}
    Assert No Empty Mandatory Field    tab:tabPanel:objectForm:form    Save (insert)
    Save
    ${has_go}=    Get Element Count
    ...    css=button[id="button:form:B"]:visible, a[id="button:form:B"]:visible
    IF    ${has_go} > 0    Apply Navigator    ELSE    Refresh Screen

Update Action Trigger Name
    [Documentation]    Select the row, edit Name (by label), gate-check, save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Action Trigger Name    ${new_name}
    Assert No Empty Mandatory Field    tab:tabPanel:updateAttributes:form    Save (update)
    Save
    ${has_go}=    Get Element Count
    ...    css=button[id="button:form:B"]:visible, a[id="button:form:B"]:visible
    IF    ${has_go} > 0    Apply Navigator    ELSE    Refresh Screen

Delete Action Trigger
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
