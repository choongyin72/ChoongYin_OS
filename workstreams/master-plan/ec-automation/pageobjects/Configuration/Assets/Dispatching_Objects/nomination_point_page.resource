*** Settings ***
Documentation       T3 (screen) — Nomination Point page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Nomination Point.
...                 OV-GM behaviour: the grid (manageObject:form:T_data) loads ONLY after
...                 a Business Unit is picked in the navigator + GO. The inserted object's
...                 "Contract Name" must be consistent with that BU or the filtered grid
...                 will never list it (recon 2026-06-12).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${NOMPNT_SCREEN}          Nomination Point
${NOMPNT_TABLE}           manageObject:form:T_data
# navigator: Business Unit dropdown — MANDATORY before the grid loads
${NOMPNT_NAV_BU}          nav:form:G:0:R:1:C:1:dd
# objectForm field IDs (Insert — new object)
${NOMPNT_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${NOMPNT_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${NOMPNT_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input
# Insert form's "Contract Name" dropdown (mandatory / grid-visibility parent)
${NOMPNT_INS_PARENT}      tab:tabPanel:objectForm:form:G:0:R:5:C:1:dd
# updateAttributes field IDs (Update — existing object)
${NOMPNT_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${NOMPNT_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${NOMPNT_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Nomination Point Screen
    [Documentation]    Suite Setup: launch, login, navigate, pick the Business Unit
    ...    navigator context and apply it (grid is empty until then).
    [Arguments]    ${business_unit}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${NOMPNT_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${NOMPNT_NAV_BU}    ${business_unit}
    Apply Navigator

Nomination Point Row Should Exist
    [Documentation]    Assert a nomination point with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${NOMPNT_TABLE}    ${code}

Nomination Point Row Should Not Exist
    [Documentation]    Assert a nomination point with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${NOMPNT_TABLE}    ${code}

Nomination Point Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_nomination_point.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_nomination_point    ${code}

Nomination Point Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_nomination_point.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_nomination_point    ${code}

Nomination Point Row Should Show Name
    [Documentation]    Assert the Nomination Point row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${NOMPNT_TABLE}    ${code}    ${name}

Insert Nomination Point Record
    [Documentation]    Insert a new nomination point: New Object form -> Code/Name/Start Date +
    ...    "Contract Name" = ${parent} (mandatory / BU-visibility link) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${parent}
    Fill New Object Form    ${NOMPNT_INS_CODE}    ${NOMPNT_INS_NAME}    ${NOMPNT_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${NOMPNT_INS_PARENT}    ${parent}
    Save And Refresh List

Update Nomination Point Name
    [Documentation]    Select the nomination point, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${NOMPNT_TABLE}    ${NOMPNT_UPD_CODE}    ${NOMPNT_UPD_NAME}    ${code}    ${new_name}

Delete Nomination Point
    [Documentation]    Select the nomination point, set End Date = Start Date (true delete), Save.
    ...    Versioned GM grids redraw lazily — one extra Apply Navigator before asserting.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${NOMPNT_TABLE}    ${NOMPNT_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
