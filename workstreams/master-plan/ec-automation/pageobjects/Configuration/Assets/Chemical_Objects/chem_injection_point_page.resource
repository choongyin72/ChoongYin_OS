*** Settings ***
Documentation       T3 (screen) - Chemical Injection Point page object.
...                 Screen: Configuration > Assets > Chemical Objects > Chemical Injection Point.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator
...                 cascade (Production Unit -> Area -> Facility Class 1) + GO. Sibling of Node.
...                 Fields resolved BY LABEL (no hardcoded rows). Mandatory = Code/Name/Start Date;
...                 Op Production Unit set first-available for grid visibility.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CIP_SCREEN}           Chemical Injection Point
${CIP_TABLE}            manageObject:form:T_data
${CIP_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${CIP_PU}               ${EMPTY}


*** Keywords ***
Open Chemical Injection Point Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the OV-GM navigator cascade
    ...    first-available + GO, and RETURN the top-parent PU (grid empty until then).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CIP_SCREEN}    ${user}    ${pass}
    ${pu}=    Apply OV-GM Navigator First Available
    RETURN    ${pu}

Chemical Injection Point Row Should Exist
    [Documentation]    Assert a point with ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${CIP_TABLE}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${CIP_TABLE}    ${code}

Chemical Injection Point Row Should Not Exist
    [Documentation]    Assert a point with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${CIP_TABLE}    ${code}

Chemical Injection Point Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CHEM_INJ_POINT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CHEM_INJ_POINT    ${code}

Chemical Injection Point Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CHEM_INJ_POINT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CHEM_INJ_POINT    ${code}

Chemical Injection Point Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${CIP_TABLE}    ${code}    ${name}

Insert Chemical Injection Point Record
    [Documentation]    Insert a new point (all fields BY LABEL): Code/Name/Start Date +
    ...    Op Production Unit (first-available for grid visibility) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Chem Inj Point Code    ${code}
    Fill OV Field By Label       objectForm    Chem Inj Point Name    ${name}
    Fill OV Date By Label        objectForm    Start Date             ${start_date}
    Fill OV Dropdown By Label    objectForm    Op Production Unit     __FIRST__
    Save And Refresh List

Update Chemical Injection Point Name
    [Documentation]    Select the point, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${CIP_TABLE}    ${code}
    Fill OV Field By Label    updateAttributes    Chem Inj Point Name    ${new_name}
    Save And Refresh List

Delete Chemical Injection Point
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${CIP_TABLE}    ${CIP_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
