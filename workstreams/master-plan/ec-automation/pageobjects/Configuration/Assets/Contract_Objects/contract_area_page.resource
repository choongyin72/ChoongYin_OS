*** Settings ***
Documentation       T3 (screen) — Contract Area page object.
...                 Screen: Configuration > Assets > Contract Objects > Contract Area.
...                 OV-GM behaviour: the grid (manageObject:form:T_data) loads ONLY after
...                 a Business Unit is picked in the navigator + GO. The inserted object's
...                 "Business Unit Name" must be consistent with that BU or the filtered grid
...                 will never list it (recon 2026-06-18). Sibling of Transport System.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CONTRACT_AREA_SCREEN}     Contract Area
${CONTRACT_AREA_TABLE}      manageObject:form:T_data
# navigator: Business Unit dropdown — MANDATORY before the grid loads
${CONTRACT_AREA_NAV_BU}     nav:form:G:0:R:1:C:1:dd
# objectForm field IDs (Insert — new object)
${CONTRACT_AREA_INS_CODE}    tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${CONTRACT_AREA_INS_NAME}    tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${CONTRACT_AREA_INS_DATE}    tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# Insert form's "Business Unit Name" dropdown (mandatory / grid-visibility parent) — R:5 on this screen
${CONTRACT_AREA_INS_PARENT}    tab:tabPanel:objectForm:form:G:0:R:5:C:1:dd
# updateAttributes field IDs (Update — existing object)
${CONTRACT_AREA_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${CONTRACT_AREA_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${CONTRACT_AREA_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Contract Area Screen
    [Documentation]    Suite Setup: launch, login, navigate, pick the Business Unit
    ...    navigator context and apply it (grid is empty until then).
    [Arguments]    ${business_unit}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CONTRACT_AREA_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${CONTRACT_AREA_NAV_BU}    ${business_unit}
    Apply Navigator

Contract Area Row Should Exist
    [Documentation]    Assert a contract area with ${code} is present in the list. The OV-GM
    ...    grid redraws lazily after Save+GO, so wait for the row span to render before the
    ...    instant first-cell read (the bare T1 Row Should Exist does not wait).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${CONTRACT_AREA_TABLE}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${CONTRACT_AREA_TABLE}    ${code}

Contract Area Row Should Not Exist
    [Documentation]    Assert a contract area with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${CONTRACT_AREA_TABLE}    ${code}

Contract Area Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_contract_area.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_contract_area    ${code}

Contract Area Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_contract_area.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_contract_area    ${code}

Contract Area Row Should Show Name
    [Documentation]    Assert the Contract Area row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${CONTRACT_AREA_TABLE}    ${code}    ${name}

Insert Contract Area Record
    [Documentation]    Insert a new contract area: New Object form -> Code/Name/Start Date +
    ...    "Business Unit Name" = ${parent} (mandatory / BU-visibility link) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${parent}
    Fill New Object Form    ${CONTRACT_AREA_INS_CODE}    ${CONTRACT_AREA_INS_NAME}    ${CONTRACT_AREA_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${CONTRACT_AREA_INS_PARENT}    ${parent}
    Save And Refresh List

Update Contract Area Name
    [Documentation]    Select the contract area, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${CONTRACT_AREA_TABLE}    ${CONTRACT_AREA_UPD_CODE}    ${CONTRACT_AREA_UPD_NAME}    ${code}    ${new_name}

Delete Contract Area
    [Documentation]    Select the contract area, set End Date = Start Date (true delete), Save.
    ...    Versioned GM grids redraw lazily — one extra Apply Navigator before asserting.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${CONTRACT_AREA_TABLE}    ${CONTRACT_AREA_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
