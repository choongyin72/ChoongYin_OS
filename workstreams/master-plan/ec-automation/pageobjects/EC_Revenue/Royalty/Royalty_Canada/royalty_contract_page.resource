*** Settings ***
Documentation       T3 (screen) - Royalty Contract page object.
...                 Screen: EC_Revenue > Royalty > Royalty_Canada > Royalty Contract.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator cascade
...                 + GO. Cascade values are PROVEN explicit values (scripts/find_populated_scope.py),
...                 not first-available. Fields resolved BY LABEL (no hardcoded rows).
...                 DELETE IS PERMANENTLY OUT OF SCOPE on this screen (owner-confirmed 2026-08-15,
...                 closes Issue #336) - Contract Template "Royalty Fixed Percentage Canada" causes EC
...                 to auto-provision CNTR_PG_SETUP child rows with no UI path to remove them, so
...                 End=Start always fails (genuine EC product limitation, see PR #331). The "Delete
...                 Royalty Contract" keyword below is kept for reference/future use if this changes,
...                 but is NOT exercised by the current suite.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Royalty Contract
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}
${NAV_DD}            nav:form:G:1:R:1:C:0:dd
${INSERT_END_DATE}   2099-12-31


*** Keywords ***
Open Royalty Contract Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the navigator cascade with PROVEN
    ...    explicit values (not first-available) + GO, RETURN the top-parent PU.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Select EC Dropdown Option    ${NAV_DD}    Royalty Canada
    Apply Navigator
    VAR    ${pu}    Royalty Canada
    RETURN    ${pu}

Royalty Contract Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Royalty Contract Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Royalty Contract Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_ROYALTY_CONTRACT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_ROYALTY_CONTRACT    ${code}

Royalty Contract Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_ROYALTY_CONTRACT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_ROYALTY_CONTRACT    ${code}

Royalty Contract Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Royalty Contract Record
    [Documentation]    Insert (all fields BY LABEL) + Save. End Date is MANDATORY on this
    ...    screen's form (unusual, same as Contract) - ${INSERT_END_DATE} is unrelated to the
    ...    End=Start delete's End Date.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Royalty Contract Code    ${code}
    Fill OV Field By Label       objectForm    Royalty Contract Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Date By Label        objectForm    End Date      ${INSERT_END_DATE}
    Fill OV Dropdown By Label    objectForm    Contract Template    Royalty Fixed Percentage Canada
    Fill OV Dropdown By Label    objectForm    Contract Area    Alberta
    Save And Refresh List

Update Royalty Contract Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Royalty Contract Name    ${new_name}
    Save And Refresh List

Delete Royalty Contract
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
