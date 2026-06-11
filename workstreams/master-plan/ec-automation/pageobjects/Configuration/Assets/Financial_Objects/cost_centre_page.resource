*** Settings ***
Documentation       T3 (screen) — Cost Centre page object.
...                 Screen: Configuration > Assets > Financial Objects > Cost Centre.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${COST_CENTRE_SCREEN}    Cost Centre
${COST_CENTRE_TABLE}    nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${COST_CENTRE_INS_CODE}    tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${COST_CENTRE_INS_NAME}    tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${COST_CENTRE_INS_DATE}    tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${COST_CENTRE_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${COST_CENTRE_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${COST_CENTRE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Cost Centre Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Cost Centre screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${COST_CENTRE_SCREEN}

Cost Centre Row Should Exist
    [Documentation]    Assert a cost centre with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${COST_CENTRE_TABLE}    ${code}

Cost Centre Row Should Not Exist
    [Documentation]    Assert a cost centre with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${COST_CENTRE_TABLE}    ${code}

Cost Centre Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_FIN_COST_CENTER.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FIN_COST_CENTER    ${code}

Cost Centre Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_FIN_COST_CENTER.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FIN_COST_CENTER    ${code}

Cost Centre Row Should Show Name
    [Documentation]    Assert the Cost Centre row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${COST_CENTRE_TABLE}    ${code}    ${name}

Insert Cost Centre Record
    [Documentation]    Insert a new cost centre: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${COST_CENTRE_INS_CODE}    ${COST_CENTRE_INS_NAME}    ${COST_CENTRE_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Cost Centre Name
    [Documentation]    Select the cost centre, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${COST_CENTRE_TABLE}    ${COST_CENTRE_UPD_CODE}    ${COST_CENTRE_UPD_NAME}    ${code}    ${new_name}

Delete Cost Centre
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${COST_CENTRE_TABLE}    ${COST_CENTRE_DEL_ENDDATE}    ${code}    ${date}
