*** Settings ***
Documentation       T3 (screen) — Transport Zone page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Transport Zone.
...                 OV-GM behaviour: the grid (manageObject:form:T_data) loads ONLY after
...                 a Business Unit is picked in the navigator + GO. The inserted object's
...                 "Transport System Name" must be consistent with that BU or the filtered grid
...                 will never list it (recon 2026-06-12).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${TRNZON_SCREEN}          Transport Zone
${TRNZON_TABLE}           manageObject:form:T_data
# navigator: Business Unit dropdown — MANDATORY before the grid loads
${TRNZON_NAV_BU}          nav:form:G:0:R:1:C:1:dd
# objectForm field IDs (Insert — new object)
${TRNZON_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${TRNZON_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${TRNZON_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input
# Insert form's "Transport System Name" dropdown (mandatory / grid-visibility parent)
${TRNZON_INS_PARENT}      tab:tabPanel:objectForm:form:G:0:R:5:C:1:dd
# updateAttributes field IDs (Update — existing object)
${TRNZON_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${TRNZON_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${TRNZON_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Transport Zone Screen
    [Documentation]    Suite Setup: launch, login, navigate, pick the Business Unit
    ...    navigator context and apply it (grid is empty until then).
    [Arguments]    ${business_unit}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${TRNZON_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${TRNZON_NAV_BU}    ${business_unit}
    Apply Navigator

Transport Zone Row Should Exist
    [Documentation]    Assert a transport zone with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${TRNZON_TABLE}    ${code}

Transport Zone Row Should Not Exist
    [Documentation]    Assert a transport zone with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TRNZON_TABLE}    ${code}

Transport Zone Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_transport_zone.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_transport_zone    ${code}

Transport Zone Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_transport_zone.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_transport_zone    ${code}

Transport Zone Row Should Show Name
    [Documentation]    Assert the Transport Zone row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TRNZON_TABLE}    ${code}    ${name}

Insert Transport Zone Record
    [Documentation]    Insert a new transport zone: New Object form -> Code/Name/Start Date +
    ...    "Transport System Name" = ${parent} (mandatory / BU-visibility link) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${parent}
    Fill New Object Form    ${TRNZON_INS_CODE}    ${TRNZON_INS_NAME}    ${TRNZON_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${TRNZON_INS_PARENT}    ${parent}
    Save And Refresh List

Update Transport Zone Name
    [Documentation]    Select the transport zone, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${TRNZON_TABLE}    ${TRNZON_UPD_CODE}    ${TRNZON_UPD_NAME}    ${code}    ${new_name}

Delete Transport Zone
    [Documentation]    Select the transport zone, set End Date = Start Date (true delete), Save.
    ...    Versioned GM grids redraw lazily — one extra Apply Navigator before asserting.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TRNZON_TABLE}    ${TRNZON_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
