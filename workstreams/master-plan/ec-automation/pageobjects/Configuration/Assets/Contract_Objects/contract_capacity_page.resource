*** Settings ***
Documentation       T3 (screen) - Contract Capacity page object.
...                 Screen: Configuration > Assets > Contract_Objects > Contract Capacity.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator
...                 cascade + GO (capability Apply OV-GM Navigator First Available). Fields resolved
...                 BY LABEL (no hardcoded rows). Extra dropdowns + Op Production Unit first-available.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Contract Capacity
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}
${NAV_DD}            nav:form:G:0:R:1:C:1:dd


*** Keywords ***
Open Contract Capacity Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the OV-GM navigator cascade
    ...    first-available + GO, RETURN the top-parent PU (grid empty until then).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Select EC Dropdown Option    ${NAV_DD}    TS5 BU
    Apply Navigator
    VAR    ${pu}    TS5 BU
    RETURN    ${pu}

Contract Capacity Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Contract Capacity Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Contract Capacity Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_CONTRACT_CAPACITY.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CONTRACT_CAPACITY    ${code}

Contract Capacity Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_CONTRACT_CAPACITY.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CONTRACT_CAPACITY    ${code}

Contract Capacity Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Contract Capacity Record
    [Documentation]    Insert (all fields BY LABEL) + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Contract Capacity Code    ${code}
    Fill OV Field By Label       objectForm    Contract Capacity Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Contract Name    TS5 Shipper B Firm
    Fill OV Dropdown By Label    objectForm    Location Name    TS5 Domestic Gas Storage
    Save And Refresh List

Update Contract Capacity Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Contract Capacity Name    ${new_name}
    Save And Refresh List

Delete Contract Capacity
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
