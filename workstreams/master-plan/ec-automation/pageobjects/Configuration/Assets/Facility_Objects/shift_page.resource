*** Settings ***
Documentation       T3 (screen) - Shift page object.
...                 Screen: Configuration > Assets > Facility_Objects > Shift (CO.0224).
...                 OV-GM with a MANDATORY FREE-TEXT extra: Start Time (HH:MI) - value format
...                 '07:00' taken from the existing P1 S001 row (owner tip: scan an existing row's
...                 populated values to learn every element's expected format). Navigator =
...                 SPECIFIC P1 values. Op Production Unit = nav PU (parent-matching).
...                 Fields BY LABEL. DELETE = End Date = Start Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/navigator.resource


*** Variables ***
${SCR}              Shift
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${SH_NAV_PU}        P1 Production Unit
${SH_NAV_AREA}      P1 Area
${SH_NAV_FC1}       P1 Facility 1
${SH_START_TIME}    07:00


*** Keywords ***
Open Shift Screen
    [Documentation]    Suite Setup: launch, login, open the screen, apply the SPECIFIC 3-level
    ...    P1 navigator scope + GO - grid is empty until then.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Apply Shift Navigator

Apply Shift Navigator
    [Documentation]    Fill the 3-column cascade (row 1) with the owner-provided P1 values, then GO.
    Select EC Dropdown Option    nav:form:G:0:R:1:C:1:dd    ${SH_NAV_PU}
    Sleep    0.7s
    Select EC Dropdown Option    nav:form:G:0:R:1:C:2:dd    ${SH_NAV_AREA}
    Sleep    0.7s
    Select EC Dropdown Option    nav:form:G:0:R:1:C:3:dd    ${SH_NAV_FC1}
    Sleep    0.7s
    Apply Navigator

Shift Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Shift Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Shift Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_SHIFT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_SHIFT    ${code}

Shift Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_SHIFT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_SHIFT    ${code}

Shift Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Shift Record
    [Documentation]    Insert (all fields BY LABEL) + Save: the mandatory free-text
    ...    Start Time (HH:MI) + Op Production Unit = nav PU (parent-matching).
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Shift Code    ${code}
    Fill OV Field By Label       objectForm    Shift Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Field By Label       objectForm    Start Time (HH:MI)    ${SH_START_TIME}
    Fill OV Dropdown By Label    objectForm    Op Production Unit    ${SH_NAV_PU}
    Save And Refresh List

Update Shift Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Shift Name    ${new_name}
    Save And Refresh List

Delete Shift
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
