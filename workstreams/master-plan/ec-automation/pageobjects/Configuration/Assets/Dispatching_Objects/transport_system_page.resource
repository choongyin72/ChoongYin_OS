*** Settings ***
Documentation       T3 (screen) — Transport System page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Transport System.
...                 OV-GM behaviour: the grid (manageObject:form:T_data) loads ONLY after
...                 a Business Unit is picked in the navigator + GO. The inserted object's
...                 "Business Unit Name" must be consistent with that BU or the filtered grid
...                 will never list it (recon 2026-06-12).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${TRNSYS_SCREEN}          Transport System
${TRNSYS_TABLE}           manageObject:form:T_data
# navigator: Business Unit dropdown — MANDATORY before the grid loads
${TRNSYS_NAV_BU}          nav:form:G:0:R:1:C:1:dd
# objectForm field IDs (Insert — new object)
${TRNSYS_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${TRNSYS_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${TRNSYS_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# Insert form's "Business Unit Name" dropdown (mandatory / grid-visibility parent)
${TRNSYS_INS_PARENT}      tab:tabPanel:objectForm:form:G:0:R:6:C:1:dd
# updateAttributes field IDs (Update — existing object)
${TRNSYS_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${TRNSYS_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${TRNSYS_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Transport System Screen
    [Documentation]    Suite Setup: launch, login, navigate, pick the Business Unit
    ...    navigator context and apply it (grid is empty until then).
    [Arguments]    ${business_unit}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${TRNSYS_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${TRNSYS_NAV_BU}    ${business_unit}
    Apply Navigator

Transport System Row Should Exist
    [Documentation]    Assert a transport system with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${TRNSYS_TABLE}    ${code}

Transport System Row Should Not Exist
    [Documentation]    Assert a transport system with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TRNSYS_TABLE}    ${code}

Transport System Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_transport_system.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_transport_system    ${code}

Transport System Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_transport_system.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_transport_system    ${code}

Transport System Row Should Show Name
    [Documentation]    Assert the Transport System row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TRNSYS_TABLE}    ${code}    ${name}

Insert Transport System Record
    [Documentation]    Insert a new transport system: New Object form -> Code/Name/Start Date +
    ...    "Business Unit Name" = ${parent} (mandatory / BU-visibility link) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${parent}
    Fill New Object Form    ${TRNSYS_INS_CODE}    ${TRNSYS_INS_NAME}    ${TRNSYS_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${TRNSYS_INS_PARENT}    ${parent}
    Save And Refresh List

Update Transport System Name
    [Documentation]    Select the transport system, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${TRNSYS_TABLE}    ${TRNSYS_UPD_CODE}    ${TRNSYS_UPD_NAME}    ${code}    ${new_name}

Delete Transport System
    [Documentation]    Select the transport system, set End Date = Start Date (true delete), Save.
    ...    Versioned GM grids redraw lazily — one extra Apply Navigator before asserting.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TRNSYS_TABLE}    ${TRNSYS_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
