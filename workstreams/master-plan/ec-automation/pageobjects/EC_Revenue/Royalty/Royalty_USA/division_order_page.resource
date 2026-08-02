*** Settings ***
Documentation       T3 (screen) - Division Order page object.
...                 Screen: EC_Revenue > Royalty > Royalty_USA > Division Order.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator cascade
...                 + GO. Cascade values are PROVEN explicit values (scripts/find_populated_scope.py),
...                 not first-available. Fields resolved BY LABEL (no hardcoded rows).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Division Order
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}
${NAV_DD}            nav:form:G:1:R:1:C:0:dd
${INSERT_END_DATE}   2099-12-31


*** Keywords ***
Open Division Order Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the navigator cascade with PROVEN
    ...    explicit values (not first-available) + GO, RETURN the top-parent PU.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Select EC Dropdown Option    ${NAV_DD}    Royalty USA
    Apply Navigator
    VAR    ${pu}    Royalty USA
    RETURN    ${pu}

Division Order Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Division Order Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Division Order Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_DIVISION_ORDER.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_DIVISION_ORDER    ${code}

Division Order Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_DIVISION_ORDER.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_DIVISION_ORDER    ${code}

Division Order Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Division Order Record
    [Documentation]    Insert (all fields BY LABEL) + Save. End Date is functionally mandatory on
    ...    this screen's form (not flagged yellow, but Save rejects without it) - ${INSERT_END_DATE}
    ...    is unrelated to the End=Start delete's End Date.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Division Order Code    ${code}
    Fill OV Field By Label       objectForm    Division Order Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Date By Label        objectForm    End Date      ${INSERT_END_DATE}
    Fill OV Dropdown By Label    objectForm    Contract Template    __FIRST__
    Fill OV Dropdown By Label    objectForm    Contract Area    Louisiana North
    Save And Refresh List

Update Division Order Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Division Order Name    ${new_name}
    Save And Refresh List

Delete Division Order
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
