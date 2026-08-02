*** Settings ***
Documentation       T3 (screen) - Property page object.
...                 Screen: Configuration > Assets > Data_Mapping_Objects > Property.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator cascade
...                 + GO. Cascade values are PROVEN explicit values (scripts/find_populated_scope.py),
...                 not first-available. Fields resolved BY LABEL (no hardcoded rows).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Property
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}
${NAV_DD}            nav:form:G:1:R:1:C:0:dd


*** Keywords ***
Open Property Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the navigator cascade with PROVEN
    ...    explicit values (not first-available) + GO, RETURN the top-parent PU.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Select EC Dropdown Option    ${NAV_DD}    Royalty Canada
    Apply Navigator
    VAR    ${pu}    Royalty Canada
    RETURN    ${pu}

Property Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Property Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Property Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_PROPERTY.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_PROPERTY    ${code}

Property Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_PROPERTY.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_PROPERTY    ${code}

Property Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Property Record
    [Documentation]    Insert (all fields BY LABEL) + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Property Code    ${code}
    Fill OV Field By Label       objectForm    Property Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Business Unit Name    Royalty Canada
    Save And Refresh List

Update Property Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Property Name    ${new_name}
    Save And Refresh List

Delete Property
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
