*** Settings ***
Documentation       T3 (screen) — Meter page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Meter.
...                 OV-GM (BU-gated) with TWO mandatory references on insert:
...                 Meter Type (dd, R4) and Delivery Point (POPUP PICKER, R5 pin/pinB —
...                 see resources/popup.resource; list is filtered by the navigator BU,
...                 so pick a DP belonging to the nav BU for grid visibility).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/popup.resource


*** Variables ***
${METER_SCREEN}          Meter
${METER_TABLE}           manageObject:form:T_data
# navigator: Business Unit dropdown — MANDATORY before the grid loads
${METER_NAV_BU}          nav:form:G:0:R:1:C:1:dd
# objectForm field IDs (Insert)
${METER_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${METER_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${METER_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
${METER_INS_TYPE}        tab:tabPanel:objectForm:form:G:0:R:4:C:1:dd
${METER_INS_DP_PIN}      tab:tabPanel:objectForm:form:G:0:R:5:C:1:pin
# updateAttributes field IDs (Update)
${METER_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${METER_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${METER_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Meter Screen
    [Documentation]    Suite Setup: launch, login, navigate, pick the Business Unit
    ...    navigator context and apply it (grid AND popup lists are empty until then).
    [Arguments]    ${business_unit}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${METER_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${METER_NAV_BU}    ${business_unit}
    Apply Navigator

Meter Row Should Exist
    [Documentation]    Assert a meter with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${METER_TABLE}    ${code}

Meter Row Should Not Exist
    [Documentation]    Assert a meter with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${METER_TABLE}    ${code}

Meter Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_meter.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_meter    ${code}

Meter Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_meter.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_meter    ${code}

Meter Row Should Show Name
    [Documentation]    Assert the Meter row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${METER_TABLE}    ${code}    ${name}

Insert Meter Record
    [Documentation]    Insert a new meter. ORDER MATTERS: the popup pick goes FIRST
    ...    (after the date) — the popup's close callback resets the form's dirty/save
    ...    state, so any Save immediately after it is a silent no-op; editing the other
    ...    fields AFTER the popup re-arms Save (proven empirically 2026-06-13).
    [Arguments]    ${code}    ${name}    ${start_date}    ${meter_type}    ${delivery_point}
    Open New Object Form
    Fill EC Date    ${METER_INS_DATE}    ${start_date}
    Pick From EC Object Popup    ${METER_INS_DP_PIN}    ${delivery_point}
    Fill EC Field    ${METER_INS_CODE}    ${code}
    Fill EC Field    ${METER_INS_NAME}    ${name}
    Select EC Dropdown Option    ${METER_INS_TYPE}    ${meter_type}
    Save And Refresh List

Update Meter Name
    [Documentation]    Select the meter, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${METER_TABLE}    ${METER_UPD_CODE}    ${METER_UPD_NAME}    ${code}    ${new_name}

Delete Meter
    [Documentation]    Select the meter, set End Date = Start Date (true delete), Save.
    ...    GM grids redraw lazily — one extra Apply Navigator before asserting.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${METER_TABLE}    ${METER_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
