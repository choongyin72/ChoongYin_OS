*** Settings ***
Documentation       T3 (screen) - Chemical Tank page object.
...                 Screen: Configuration > Assets > Chemical Objects > Chemical Tank.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator
...                 cascade (Production Unit -> Area -> Facility Class 1) + GO. Sibling of Node.
...                 Fields resolved BY LABEL (no hardcoded rows). Extra mandatory over the plain
...                 OV: Measure unit (dropdown). Op Production Unit set first-available for grid
...                 visibility (the nav PU is not necessarily a valid Op PU option - probe per screen).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CT_SCREEN}            Chemical Tank
${CT_TABLE}             manageObject:form:T_data
# objectdates End Date input (Delete = End Date = Start Date) - EC-wide stable id
${CT_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${CT_PU}                ${EMPTY}


*** Keywords ***
Open Chemical Tank Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the OV-GM navigator cascade
    ...    first-available + GO, and RETURN the top-parent PU (grid empty until then).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CT_SCREEN}    ${user}    ${pass}
    ${pu}=    Apply OV-GM Navigator First Available
    RETURN    ${pu}

Chemical Tank Row Should Exist
    [Documentation]    Assert a chemical tank with ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${CT_TABLE}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${CT_TABLE}    ${code}

Chemical Tank Row Should Not Exist
    [Documentation]    Assert a chemical tank with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${CT_TABLE}    ${code}

Chemical Tank Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CHEM_TANK.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CHEM_TANK    ${code}

Chemical Tank Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CHEM_TANK.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CHEM_TANK    ${code}

Chemical Tank Row Should Show Name
    [Documentation]    Assert the Chemical Tank row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${CT_TABLE}    ${code}    ${name}

Insert Chemical Tank Record
    [Documentation]    Insert a new chemical tank (all fields BY LABEL): Code/Name/Start Date +
    ...    Measure unit + Op Production Unit (first-available for grid visibility) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Chemical Tank Code    ${code}
    Fill OV Field By Label       objectForm    Chemical Tank Name    ${name}
    Fill OV Date By Label        objectForm    Start Date            ${start_date}
    Fill OV Dropdown By Label    objectForm    Measure unit          __FIRST__
    Fill OV Dropdown By Label    objectForm    Op Production Unit    __FIRST__
    Save And Refresh List

Update Chemical Tank Name
    [Documentation]    Select the chemical tank, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${CT_TABLE}    ${code}
    Fill OV Field By Label    updateAttributes    Chemical Tank Name    ${new_name}
    Save And Refresh List

Delete Chemical Tank
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    ...    OV-GM grids redraw lazily after a delete - apply the navigator once more.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${CT_TABLE}    ${CT_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
