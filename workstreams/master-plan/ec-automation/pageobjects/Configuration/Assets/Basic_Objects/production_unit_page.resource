*** Settings ***
Documentation       T3 (screen) — Production Unit page object.
...                 Screen: Configuration > Assets > Basic Objects > Production Unit.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${PRODUCTION_UNIT_SCREEN}           Production Unit
${PRODUCTION_UNIT_TABLE}            manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object)
${PRODUCTION_UNIT_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${PRODUCTION_UNIT_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${PRODUCTION_UNIT_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${PRODUCTION_UNIT_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${PRODUCTION_UNIT_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${PRODUCTION_UNIT_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Production Unit Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Production Unit screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${PRODUCTION_UNIT_SCREEN}    ${user}    ${pass}

Production Unit Row Should Exist
    [Documentation]    Assert a production unit with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${PRODUCTION_UNIT_TABLE}    ${code}

Production Unit Row Should Not Exist
    [Documentation]    Assert a production unit with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${PRODUCTION_UNIT_TABLE}    ${code}

Production Unit Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_PRODUCTIONUNIT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_PRODUCTIONUNIT    ${code}

Production Unit Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_PRODUCTIONUNIT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_PRODUCTIONUNIT    ${code}

Production Unit Row Should Show Name
    [Documentation]    Assert the Production Unit row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${PRODUCTION_UNIT_TABLE}    ${code}    ${name}

Insert Production Unit Record
    [Documentation]    Insert a new production unit: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${PRODUCTION_UNIT_INS_CODE}    ${PRODUCTION_UNIT_INS_NAME}    ${PRODUCTION_UNIT_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Production Unit Name
    [Documentation]    Select the production unit, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${PRODUCTION_UNIT_TABLE}
    ...    ${PRODUCTION_UNIT_UPD_CODE}
    ...    ${PRODUCTION_UNIT_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete Production Unit
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${PRODUCTION_UNIT_TABLE}    ${PRODUCTION_UNIT_DEL_ENDDATE}    ${code}    ${date}
