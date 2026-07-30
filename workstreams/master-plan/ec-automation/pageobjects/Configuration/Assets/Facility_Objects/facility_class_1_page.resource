*** Settings ***
Documentation       T3 (screen) - Facility Class 1 page object.
...                 Screen: Configuration > Assets > Facility_Objects > Facility Class 1.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator
...                 cascade + GO (capability Apply OV-GM Navigator First Available). Fields resolved
...                 BY LABEL (no hardcoded rows). Extra dropdowns + Op Production Unit first-available.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Facility Class 1
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}


*** Keywords ***
Open Facility Class 1 Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the OV-GM navigator cascade
    ...    first-available + GO, RETURN the top-parent PU (grid empty until then).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    ${pu}=    Apply OV-GM Navigator First Available
    RETURN    ${pu}

Facility Class 1 Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Facility Class 1 Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Facility Class 1 Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_FCTY_CLASS_1.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FCTY_CLASS_1    ${code}

Facility Class 1 Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_FCTY_CLASS_1.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FCTY_CLASS_1    ${code}

Facility Class 1 Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Facility Class 1 Record
    [Documentation]    Insert (all fields BY LABEL) + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Facility Class 1 Code    ${code}
    Fill OV Field By Label       objectForm    Facility Class 1 Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Save And Refresh List

Update Facility Class 1 Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Facility Class 1 Name    ${new_name}
    Save And Refresh List

Delete Facility Class 1
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
