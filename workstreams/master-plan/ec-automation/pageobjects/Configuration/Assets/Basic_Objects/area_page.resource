*** Settings ***
Documentation       T3 (screen) — Area page object.
...                 Screen: Configuration > Assets > Basic Objects > Area.
...                 Manage-Object (OV, groupmodel) screen: the grid loads ONLY after a
...                 Production Unit is selected in the navigator + GO. The inserted area
...                 must carry the same Op Production Unit to appear in the filtered grid.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${AREA_SCREEN}          Area
${AREA_TABLE}           manageObject:form:T_data
# navigator (groupmodel): Production Unit dropdown — MANDATORY before the grid loads.
# 2026-08-26: the fill itself now goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/area_navigator.properties. ${AREA_NAV_PU}
# is kept only as documentation of the DOM id that properties-driven fill resolves to (row 1, C:1).
${AREA_NAV_PU}          nav:form:G:0:R:1:C:1:dd
${AREA_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/area_navigator.properties
# objectForm field IDs (Insert — new object)
${AREA_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${AREA_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${AREA_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
${AREA_INS_OP_PU}       tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd
# updateAttributes field IDs (Update — existing object)
${AREA_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${AREA_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${AREA_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Area Screen
    [Documentation]    Suite Setup: launch, login, navigate, then fill + submit the mandatory
    ...    Production Unit navigator context (grid is empty until then). Navigator fill delegates
    ...    to the shared T2 "Apply Navigator From Properties" (resources/manage_object.resource,
    ...    added 2026-08-26), driven by testdata/area_navigator.properties, instead of inlining
    ...    "Select EC Dropdown Option + Apply Navigator" here - so any other OV-GM screen with a
    ...    navigator can reuse the same shared keyword with its own properties file.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${AREA_SCREEN}    ${user}    ${pass}
    Apply Navigator From Properties    ${AREA_NAVIGATOR_PROPERTIES}

Area Row Should Exist
    [Documentation]    Assert an area with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${AREA_TABLE}    ${code}

Area Row Should Not Exist
    [Documentation]    Assert an area with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${AREA_TABLE}    ${code}

Area Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_AREA.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_AREA    ${code}

Area Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_AREA.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_AREA    ${code}

Area Row Should Show Name
    [Documentation]    Assert the Area row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${AREA_TABLE}    ${code}    ${name}

Insert Area Record
    [Documentation]    Insert a new area: Code/Name/Start Date + Op Production Unit
    ...    (same as the navigator PU so the new row shows in the filtered grid) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${op_production_unit}
    Fill New Object Form    ${AREA_INS_CODE}    ${AREA_INS_NAME}    ${AREA_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${AREA_INS_OP_PU}    ${op_production_unit}
    Save And Refresh List

Update Area Name
    [Documentation]    Select the area, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${AREA_TABLE}    ${AREA_UPD_CODE}    ${AREA_UPD_NAME}    ${code}    ${new_name}

Delete Area
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    ...    Versioned groupmodel grids redraw lazily after a delete - apply the
    ...    navigator once more so the assertion reads a fresh list, not stale state.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${AREA_TABLE}    ${AREA_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
