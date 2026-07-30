*** Settings ***
Documentation       T3 (screen) - Well page object.
...                 Screen: Configuration > Assets > Well_and_Reservoir_Objects > Well (CO.0049).
...                 OV-GM: 5-dd navigator, but only the standard 3-level cascade is needed - with
...                 SPECIFIC P1 values + GO the grid lists wells while the 2nd-row dds
...                 (Well & Well Hookup / Well) stay EMPTY (owner screenshot ground truth; the
...                 first-available AS1 path left the extra level empty = the original park).
...                 Insert extra: Well Type (mandatory dd, first-available). Fields BY LABEL.
...                 DELETE = End Date = Start Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/navigator.resource


*** Variables ***
${SCR}              Well
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# owner-provided working nav scope (screenshot 2026-07-30)
${WE_NAV_PU}        P1 Production Unit
${WE_NAV_AREA}      P1 Area
${WE_NAV_FC1}       P1 Facility 1


*** Keywords ***
Open Well Screen
    [Documentation]    Suite Setup: launch, login, open the screen, apply the SPECIFIC 3-level
    ...    P1 navigator scope + GO (2nd-row dds left empty) - grid is empty until then.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Apply Well Navigator

Apply Well Navigator
    [Documentation]    Fill the 3-column cascade (row 1) with the owner-provided P1 values, then GO.
    ...    Specific values, NOT first-available (AS1 first-available leaves a deeper level empty).
    Select EC Dropdown Option    nav:form:G:0:R:1:C:1:dd    ${WE_NAV_PU}
    Sleep    0.7s
    Select EC Dropdown Option    nav:form:G:0:R:1:C:2:dd    ${WE_NAV_AREA}
    Sleep    0.7s
    Select EC Dropdown Option    nav:form:G:0:R:1:C:3:dd    ${WE_NAV_FC1}
    Sleep    0.7s
    Apply Navigator

Well Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Well Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Well Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_WELL.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_WELL    ${code}

Well Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_WELL.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_WELL    ${code}

Well Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Well Record
    [Documentation]    Insert (all fields BY LABEL) + Save. Well Type first-available.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Well Code    ${code}
    Fill OV Field By Label       objectForm    Well Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Well Type    __FIRST__
    Save And Refresh List

Update Well Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Well Name    ${new_name}
    Save And Refresh List

Delete Well
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
