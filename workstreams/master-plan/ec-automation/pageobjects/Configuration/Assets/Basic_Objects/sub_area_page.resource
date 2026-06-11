*** Settings ***
Documentation       T3 (screen) — Sub Area page object.
...                 Screen: Configuration > Assets > Basic Objects > Sub Area.
...                 Manage-Object (OV, groupmodel) screen with a CASCADING navigator:
...                 Production Unit, then Area (fills after the PU is picked), then GO.
...                 The inserted sub area carries Op Production Unit + Op Area so it
...                 shows in the filtered grid.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SUB_AREA_SCREEN}          Sub Area
${SUB_AREA_TABLE}           manageObject:form:T_data
# cascading navigator dropdowns — BOTH mandatory before the grid loads
${SUB_AREA_NAV_PU}          nav:form:G:0:R:1:C:1:dd
${SUB_AREA_NAV_AREA}        nav:form:G:0:R:1:C:2:dd
# objectForm field IDs (Insert — new object)
${SUB_AREA_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${SUB_AREA_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${SUB_AREA_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
${SUB_AREA_INS_OP_PU}       tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd
${SUB_AREA_INS_OP_AREA}     tab:tabPanel:objectForm:form:G:0:R:8:C:1:dd
# updateAttributes field IDs (Update — existing object)
${SUB_AREA_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${SUB_AREA_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${SUB_AREA_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Sub Area Screen
    [Documentation]    Suite Setup: launch, login, navigate, set the cascading
    ...    Production Unit -> Area navigator context and apply it.
    [Arguments]    ${production_unit}    ${area}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${SUB_AREA_SCREEN}
    Select EC Dropdown Option    ${SUB_AREA_NAV_PU}    ${production_unit}
    Select EC Dropdown Option    ${SUB_AREA_NAV_AREA}    ${area}
    Apply Navigator

Sub Area Row Should Exist
    [Documentation]    Assert a sub area with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${SUB_AREA_TABLE}    ${code}

Sub Area Row Should Not Exist
    [Documentation]    Assert a sub area with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${SUB_AREA_TABLE}    ${code}

Sub Area Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_SUB_AREA.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_SUB_AREA    ${code}

Sub Area Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_SUB_AREA.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_SUB_AREA    ${code}

Sub Area Row Should Show Name
    [Documentation]    Assert the Sub Area row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${SUB_AREA_TABLE}    ${code}    ${name}

Insert Sub Area Record
    [Documentation]    Insert a new sub area: Code/Name/Start Date + Op Production Unit
    ...    + Op Area (same as the navigator context) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${op_production_unit}    ${op_area}
    Fill New Object Form    ${SUB_AREA_INS_CODE}    ${SUB_AREA_INS_NAME}    ${SUB_AREA_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${SUB_AREA_INS_OP_PU}    ${op_production_unit}
    Select EC Dropdown Option    ${SUB_AREA_INS_OP_AREA}    ${op_area}
    Save And Refresh List

Update Sub Area Name
    [Documentation]    Select the sub area, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${SUB_AREA_TABLE}    ${SUB_AREA_UPD_CODE}    ${SUB_AREA_UPD_NAME}    ${code}    ${new_name}

Delete Sub Area
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${SUB_AREA_TABLE}    ${SUB_AREA_DEL_ENDDATE}    ${code}    ${date}
