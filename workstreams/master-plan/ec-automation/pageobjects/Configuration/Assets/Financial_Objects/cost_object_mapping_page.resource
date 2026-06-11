*** Settings ***
Documentation       T3 (screen) — Cost Object Mapping page object.
...                 Screen: Configuration > Assets > Financial Objects > Cost Object Mapping.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${COST_OBJECT_MAPPING_SCREEN}    Cost Object Mapping
${COST_OBJECT_MAPPING_TABLE}    manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${COST_OBJECT_MAPPING_INS_CODE}    tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${COST_OBJECT_MAPPING_INS_NAME}    tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
${COST_OBJECT_MAPPING_INS_DATE}    tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input
# mandatory reference dd: Object Type (banner-discovered; first option used)
${COST_OBJECT_MAPPING_INS_DD0}    tab:tabPanel:objectForm:form:G:0:R:6:C:1:dd
# mandatory reference dd: Company (banner-discovered; first option used)
${COST_OBJECT_MAPPING_INS_DD1}    tab:tabPanel:objectForm:form:G:0:R:9:C:1:dd
# mandatory reference dd: Distribution Object Type (banner-discovered; first option used)
${COST_OBJECT_MAPPING_INS_DD2}    tab:tabPanel:objectForm:form:G:0:R:12:C:1:dd
# mandatory reference dd: Cost Object (banner-discovered; first option used)
${COST_OBJECT_MAPPING_INS_DD3}    tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd
# updateAttributes field IDs (Update — existing object)
${COST_OBJECT_MAPPING_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${COST_OBJECT_MAPPING_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${COST_OBJECT_MAPPING_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Cost Object Mapping Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Cost Object Mapping screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${COST_OBJECT_MAPPING_SCREEN}

Cost Object Mapping Row Should Exist
    [Documentation]    Assert a cost object mapping with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${COST_OBJECT_MAPPING_TABLE}    ${code}

Cost Object Mapping Row Should Not Exist
    [Documentation]    Assert a cost object mapping with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${COST_OBJECT_MAPPING_TABLE}    ${code}

Cost Object Mapping Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_FIN_COST_OBJECT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FIN_COST_OBJECT    ${code}

Cost Object Mapping Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_FIN_COST_OBJECT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FIN_COST_OBJECT    ${code}

Cost Object Mapping Row Should Show Name
    [Documentation]    Assert the Cost Object Mapping row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${COST_OBJECT_MAPPING_TABLE}    ${code}    ${name}

Insert Cost Object Mapping Record
    [Documentation]    Insert a new cost object mapping: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${COST_OBJECT_MAPPING_INS_CODE}    ${COST_OBJECT_MAPPING_INS_NAME}    ${COST_OBJECT_MAPPING_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select First EC Dropdown Option    ${COST_OBJECT_MAPPING_INS_DD0}
    Select First EC Dropdown Option    ${COST_OBJECT_MAPPING_INS_DD1}
    Select First EC Dropdown Option    ${COST_OBJECT_MAPPING_INS_DD2}
    Select First EC Dropdown Option    ${COST_OBJECT_MAPPING_INS_DD3}
    Save And Refresh List

Update Cost Object Mapping Name
    [Documentation]    Select the cost object mapping, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${COST_OBJECT_MAPPING_TABLE}    ${COST_OBJECT_MAPPING_UPD_CODE}    ${COST_OBJECT_MAPPING_UPD_NAME}    ${code}    ${new_name}

Delete Cost Object Mapping
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${COST_OBJECT_MAPPING_TABLE}    ${COST_OBJECT_MAPPING_DEL_ENDDATE}    ${code}    ${date}
