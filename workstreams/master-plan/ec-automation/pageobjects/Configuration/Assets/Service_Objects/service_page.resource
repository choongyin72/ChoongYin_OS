*** Settings ***
Documentation       T3 (screen) - Service page object.
...                 Screen: Configuration > Assets > Service_Objects > Service.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator cascade
...                 + GO. Cascade values are PROVEN explicit values (scripts/find_populated_scope.py),
...                 not first-available. Fields resolved BY LABEL (no hardcoded rows).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Service
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}
${NAV_DD}            nav:form:G:0:R:1:C:1:dd


*** Keywords ***
Open Service Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the navigator cascade with PROVEN
    ...    explicit values (not first-available) + GO, RETURN the top-parent PU.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Select EC Dropdown Option    ${NAV_DD}    TS3 BU1
    Apply Navigator
    VAR    ${pu}    TS3 BU1
    RETURN    ${pu}

Service Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Service Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Service Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_SERVICE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_SERVICE    ${code}

Service Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_SERVICE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_SERVICE    ${code}

Service Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Service Record
    [Documentation]    Insert (all fields BY LABEL) + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Service Code    ${code}
    Fill OV Field By Label       objectForm    Service Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Service Template    __FIRST__
    Fill OV Dropdown By Label    objectForm    Service Type    __FIRST__
    Fill OV Dropdown By Label    objectForm    Service Status    __FIRST__
    Fill OV Dropdown By Label    objectForm    Contract    TS3 GTA Shipper A
    Fill OV Dropdown By Label    objectForm    Transport System    TS3 Transport System
    Save And Refresh List

Update Service Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Service Name    ${new_name}
    Save And Refresh List

Delete Service
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
