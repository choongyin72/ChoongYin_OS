*** Settings ***
Documentation       T3 (screen) — Delivery Point page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Delivery Point.
...                 OV-GM behaviour: the grid (manageObject:form:T_data) loads ONLY after
...                 a Business Unit is picked in the navigator + GO. The inserted object's
...                 "Business Unit Name" must be consistent with that BU or the filtered grid
...                 will never list it (recon 2026-06-12).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${DELPNT_SCREEN}          Delivery Point
${DELPNT_TABLE}           manageObject:form:T_data
# navigator: Business Unit dropdown — MANDATORY before the grid loads
${DELPNT_NAV_BU}          nav:form:G:0:R:1:C:1:dd
# objectForm field IDs (Insert — new object)
${DELPNT_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${DELPNT_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${DELPNT_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input
# Insert form's "Business Unit Name" dropdown (mandatory / grid-visibility parent)
${DELPNT_INS_PARENT}      tab:tabPanel:objectForm:form:G:0:R:11:C:1:dd
# updateAttributes field IDs (Update — existing object)
${DELPNT_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${DELPNT_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${DELPNT_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Delivery Point Screen
    [Documentation]    Suite Setup: launch, login, navigate, pick the Business Unit
    ...    navigator context and apply it (grid is empty until then).
    [Arguments]    ${business_unit}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${DELPNT_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${DELPNT_NAV_BU}    ${business_unit}
    Apply Navigator

Delivery Point Row Should Exist
    [Documentation]    Assert a delivery point with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${DELPNT_TABLE}    ${code}

Delivery Point Row Should Not Exist
    [Documentation]    Assert a delivery point with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${DELPNT_TABLE}    ${code}

Delivery Point Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_delivery_point.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_delivery_point    ${code}

Delivery Point Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_delivery_point.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_delivery_point    ${code}

Delivery Point Row Should Show Name
    [Documentation]    Assert the Delivery Point row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${DELPNT_TABLE}    ${code}    ${name}

Insert Delivery Point Record
    [Documentation]    Insert a new delivery point: New Object form -> Code/Name/Start Date +
    ...    "Business Unit Name" = ${parent} (mandatory / BU-visibility link) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${parent}
    Fill New Object Form    ${DELPNT_INS_CODE}    ${DELPNT_INS_NAME}    ${DELPNT_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${DELPNT_INS_PARENT}    ${parent}
    Save And Refresh List

Update Delivery Point Name
    [Documentation]    Select the delivery point, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${DELPNT_TABLE}    ${DELPNT_UPD_CODE}    ${DELPNT_UPD_NAME}    ${code}    ${new_name}

Delete Delivery Point
    [Documentation]    Select the delivery point, set End Date = Start Date (true delete), Save.
    ...    Versioned GM grids redraw lazily — one extra Apply Navigator before asserting.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${DELPNT_TABLE}    ${DELPNT_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
