*** Settings ***
Documentation       T3 (screen) - Well Hole page object.
...                 Screen: Configuration > Assets > Well and Reservoir Objects > Well Hole.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator
...                 cascade + GO (capability Apply OV-GM Navigator First Available). Fields resolved
...                 BY LABEL (no hardcoded rows). Extra dropdowns + Op Production Unit first-available.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Well Hole
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}


*** Keywords ***
Open Well Hole Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the OV-GM navigator cascade
    ...    first-available + GO, RETURN the top-parent PU (grid empty until then).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    ${pu}=    Apply OV-GM Navigator First Available
    RETURN    ${pu}

Well Hole Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Well Hole Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Well Hole Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_WELL_HOLE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_WELL_HOLE    ${code}

Well Hole Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_WELL_HOLE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_WELL_HOLE    ${code}

Well Hole Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Well Hole Record
    [Documentation]    Insert (all fields BY LABEL) + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Well Hole Code    ${code}
    Fill OV Field By Label       objectForm    Well Hole Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Op Production Unit    __FIRST__
    Save And Refresh List

Update Well Hole Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Well Hole Name    ${new_name}
    Save And Refresh List

Delete Well Hole
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
