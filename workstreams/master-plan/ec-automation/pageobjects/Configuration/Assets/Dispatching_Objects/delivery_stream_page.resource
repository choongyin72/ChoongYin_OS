*** Settings ***
Documentation       T3 (screen) — Delivery Stream page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Delivery Stream.
...                 OV-GM behaviour: the grid (manageObject:form:T_data) loads ONLY after
...                 a Business Unit is picked in the navigator + GO. VISIBILITY KEYS ON THE
...                 DELIVERY-POINT LINK, not the stream's own Business Unit column: the grid
...                 lists streams whose Entry/Exit Delivery Point belongs to the navigator BU
...                 (proven 2026-06-12: row with BU=ECP_NO but no DP never listed; TS3 streams
...                 all carry TS3 DPs). Insert must set Entry Delivery Point accordingly.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${DELSTRM_SCREEN}          Delivery Stream
${DELSTRM_TABLE}           manageObject:form:T_data
# navigator: Business Unit dropdown — MANDATORY before the grid loads
${DELSTRM_NAV_BU}          nav:form:G:0:R:1:C:1:dd
# objectForm field IDs (Insert — new object)
${DELSTRM_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${DELSTRM_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${DELSTRM_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# Insert form's "Business Unit" dropdown (data completeness) + "Entry Delivery Point"
# dropdown (THE grid-visibility link — see Documentation)
${DELSTRM_INS_PARENT}      tab:tabPanel:objectForm:form:G:0:R:8:C:1:dd
${DELSTRM_INS_ENTRY_DP}    tab:tabPanel:objectForm:form:G:0:R:4:C:1:dd
# updateAttributes field IDs (Update — existing object)
${DELSTRM_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${DELSTRM_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${DELSTRM_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Delivery Stream Screen
    [Documentation]    Suite Setup: launch, login, navigate, pick the Business Unit
    ...    navigator context and apply it (grid is empty until then).
    [Arguments]    ${business_unit}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${DELSTRM_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${DELSTRM_NAV_BU}    ${business_unit}
    Apply Navigator

Delivery Stream Row Should Exist
    [Documentation]    Assert a delivery stream with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${DELSTRM_TABLE}    ${code}

Delivery Stream Row Should Not Exist
    [Documentation]    Assert a delivery stream with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${DELSTRM_TABLE}    ${code}

Delivery Stream Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_delivery_stream.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_delivery_stream    ${code}

Delivery Stream Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_delivery_stream.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_delivery_stream    ${code}

Delivery Stream Row Should Show Name
    [Documentation]    Assert the Delivery Stream row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${DELSTRM_TABLE}    ${code}    ${name}

Insert Delivery Stream Record
    [Documentation]    Insert a new delivery stream: New Object form -> Code/Name/Start Date +
    ...    "Business Unit" = ${parent} + "Entry Delivery Point" = ${entry_dp} (the
    ...    delivery-point link is what makes the row VISIBLE in the BU-filtered grid) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${parent}    ${entry_dp}
    Fill New Object Form    ${DELSTRM_INS_CODE}    ${DELSTRM_INS_NAME}    ${DELSTRM_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${DELSTRM_INS_PARENT}    ${parent}
    Select EC Dropdown Option    ${DELSTRM_INS_ENTRY_DP}    ${entry_dp}
    Save And Refresh List

Update Delivery Stream Name
    [Documentation]    Select the delivery stream, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${DELSTRM_TABLE}    ${DELSTRM_UPD_CODE}    ${DELSTRM_UPD_NAME}    ${code}    ${new_name}

Delete Delivery Stream
    [Documentation]    Select the delivery stream, set End Date = Start Date (true delete), Save.
    ...    Versioned GM grids redraw lazily — one extra Apply Navigator before asserting.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${DELSTRM_TABLE}    ${DELSTRM_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
