*** Settings ***
Documentation       T3 (screen) - Lifting Account page object.
...                 Screen: Configuration > Assets > Transport_Objects > Lifting Account (CO.2004).
...                 OV-GM 4-LEVEL nav variant: standard PU -> Area -> Facility Class 1 cascade
...                 (nav row 1, C:1..3) PLUS a mandatory Storage dropdown on a SECOND navigator
...                 row (nav:form:G:0:R:3:C:0) - empty under the first-available AS1 path, so the
...                 navigator uses SPECIFIC owner-provided values (P1 scope). The insert form's
...                 Storage Name must equal the nav Storage (parent-matching) or the row never
...                 lists. Fields resolved BY LABEL. DELETE = End Date = Start Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/navigator.resource


*** Variables ***
${SCR}              Lifting Account
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# owner-provided working nav scope (4th level empty under first-available AS1 path)
${LA_NAV_PU}        P1 Production Unit
${LA_NAV_AREA}      P1 Area
${LA_NAV_FC1}       P1 Facility 1
${LA_NAV_STORAGE}   P1_CRUDE_STOR
${LA_STORAGE_DD}    nav:form:G:0:R:3:C:0:dd


*** Keywords ***
Open Lifting Account Screen
    [Documentation]    Suite Setup: launch, login, open the screen, apply the SPECIFIC 4-level
    ...    navigator scope (P1 cascade + Storage row) + GO - grid is empty until then.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Apply Lifting Account Navigator

Apply Lifting Account Navigator
    [Documentation]    Fill the 3-column cascade (row 1) + the Storage dd (row 3) with the
    ...    owner-provided P1 values, then GO. Specific values, NOT first-available: the Storage
    ...    level has no options under the first-available AS1 path.
    Select EC Dropdown Option    nav:form:G:0:R:1:C:1:dd    ${LA_NAV_PU}
    Sleep    0.7s
    Select EC Dropdown Option    nav:form:G:0:R:1:C:2:dd    ${LA_NAV_AREA}
    Sleep    0.7s
    Select EC Dropdown Option    nav:form:G:0:R:1:C:3:dd    ${LA_NAV_FC1}
    Sleep    0.7s
    Select EC Dropdown Option    ${LA_STORAGE_DD}    ${LA_NAV_STORAGE}
    Sleep    0.7s
    Apply Navigator

Lifting Account Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Lifting Account Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Lifting Account Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_LIFTING_ACCOUNT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_LIFTING_ACCOUNT    ${code}

Lifting Account Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_LIFTING_ACCOUNT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_LIFTING_ACCOUNT    ${code}

Lifting Account Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Lifting Account Record
    [Documentation]    Insert (all fields BY LABEL) + Save. Company first-available; Storage Name
    ...    = the nav Storage (parent-matching rule).
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Lifting Account Code    ${code}
    Fill OV Field By Label       objectForm    Lifting Account Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Company Name    __FIRST__
    Fill OV Dropdown By Label    objectForm    Storage Name    ${LA_NAV_STORAGE}
    Save And Refresh List

Update Lifting Account Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Lifting Account Name    ${new_name}
    Save And Refresh List

Delete Lifting Account
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
