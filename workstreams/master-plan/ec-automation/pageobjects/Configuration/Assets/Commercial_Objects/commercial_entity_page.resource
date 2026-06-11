*** Settings ***
Documentation       T3 (screen) — Commercial Entity page object.
...                 Screen: Configuration > Assets > Commercial Objects > Commercial Entity.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${COMMERCIAL_ENTITY_SCREEN}         Commercial Entity
${COMMERCIAL_ENTITY_TABLE}          manageObject:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${COMMERCIAL_ENTITY_INS_CODE}       tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
${COMMERCIAL_ENTITY_INS_NAME}       tab:tabPanel:objectForm:form:G:0:R:3:C:1:in
${COMMERCIAL_ENTITY_INS_DATE}       tab:tabPanel:objectForm:form:G:0:R:5:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${COMMERCIAL_ENTITY_UPD_CODE}       tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in
${COMMERCIAL_ENTITY_UPD_NAME}       tab:tabPanel:updateAttributes:form:G:0:R:3:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${COMMERCIAL_ENTITY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Commercial Entity Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Commercial Entity screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${COMMERCIAL_ENTITY_SCREEN}

Commercial Entity Row Should Exist
    [Documentation]    Assert a commercial entity with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${COMMERCIAL_ENTITY_TABLE}    ${code}

Commercial Entity Row Should Not Exist
    [Documentation]    Assert a commercial entity with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${COMMERCIAL_ENTITY_TABLE}    ${code}

Commercial Entity Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_COMMERCIAL_ENTITY.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_COMMERCIAL_ENTITY    ${code}

Commercial Entity Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_COMMERCIAL_ENTITY.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_COMMERCIAL_ENTITY    ${code}

Commercial Entity Row Should Show Name
    [Documentation]    Assert the Commercial Entity row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${COMMERCIAL_ENTITY_TABLE}    ${code}    ${name}

Insert Commercial Entity Record
    [Documentation]    Insert a new commercial entity: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form
    ...    ${COMMERCIAL_ENTITY_INS_CODE}
    ...    ${COMMERCIAL_ENTITY_INS_NAME}
    ...    ${COMMERCIAL_ENTITY_INS_DATE}
    ...    ${code}
    ...    ${name}
    ...    ${start_date}
    Save And Refresh List

Update Commercial Entity Name
    [Documentation]    Select the commercial entity, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${COMMERCIAL_ENTITY_TABLE}
    ...    ${COMMERCIAL_ENTITY_UPD_CODE}
    ...    ${COMMERCIAL_ENTITY_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete Commercial Entity
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${COMMERCIAL_ENTITY_TABLE}    ${COMMERCIAL_ENTITY_DEL_ENDDATE}    ${code}    ${date}
