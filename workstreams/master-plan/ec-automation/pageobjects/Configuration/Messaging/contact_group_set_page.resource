*** Settings ***
Documentation       T3 (screen) - Maintain Contact Group Set page object.
...                 Screen: Configuration > Messaging > Maintain Contact Group Set.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator
...                 cascade + GO (capability Apply OV-GM Navigator First Available). Fields resolved
...                 BY LABEL (no hardcoded rows). No Op Production Unit field or extra dropdowns on this screen (confirmed live).

Library             Browser
Library             ../../../libraries/DbVerify.py
Resource            ../../../resources/common.resource
Resource            ../../../resources/manage_object.resource


*** Variables ***
${SCR}              Maintain Contact Group Set
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}
${NAV_DD}            nav:form:G:0:R:1:C:1:dd


*** Keywords ***
Open Maintain Contact Group Set Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the OV-GM navigator cascade
    ...    first-available + GO, RETURN the top-parent PU (grid empty until then).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    ${pu}=    Apply OV-GM Navigator First Available
    RETURN    ${pu}

Maintain Contact Group Set Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Maintain Contact Group Set Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Maintain Contact Group Set Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_CONTACT_GROUP_SET.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CONTACT_GROUP_SET    ${code}

Maintain Contact Group Set Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_CONTACT_GROUP_SET.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CONTACT_GROUP_SET    ${code}

Maintain Contact Group Set Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Maintain Contact Group Set Record
    [Documentation]    Insert (all fields BY LABEL) + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Contact Group Set Code    ${code}
    Fill OV Field By Label       objectForm    Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Functional Area    ${GM_PU}
    Save And Refresh List

Update Maintain Contact Group Set Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Name    ${new_name}
    Save And Refresh List

Delete Maintain Contact Group Set
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
