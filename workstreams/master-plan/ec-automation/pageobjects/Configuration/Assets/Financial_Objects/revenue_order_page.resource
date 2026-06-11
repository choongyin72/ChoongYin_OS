*** Settings ***
Documentation       T3 (screen) — Revenue Order page object.
...                 Screen: Configuration > Assets > Financial Objects > Revenue Order.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${REVENUE_ORDER_SCREEN}         Revenue Order
${REVENUE_ORDER_TABLE}          nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${REVENUE_ORDER_INS_CODE}       tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${REVENUE_ORDER_INS_NAME}       tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${REVENUE_ORDER_INS_DATE}       tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${REVENUE_ORDER_UPD_CODE}       tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${REVENUE_ORDER_UPD_NAME}       tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${REVENUE_ORDER_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Revenue Order Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Revenue Order screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${REVENUE_ORDER_SCREEN}

Revenue Order Row Should Exist
    [Documentation]    Assert a revenue order with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${REVENUE_ORDER_TABLE}    ${code}

Revenue Order Row Should Not Exist
    [Documentation]    Assert a revenue order with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${REVENUE_ORDER_TABLE}    ${code}

Revenue Order Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_FIN_REVENUE_ORDER.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FIN_REVENUE_ORDER    ${code}

Revenue Order Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_FIN_REVENUE_ORDER.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FIN_REVENUE_ORDER    ${code}

Revenue Order Row Should Show Name
    [Documentation]    Assert the Revenue Order row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${REVENUE_ORDER_TABLE}    ${code}    ${name}

Insert Revenue Order Record
    [Documentation]    Insert a new revenue order: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${REVENUE_ORDER_INS_CODE}    ${REVENUE_ORDER_INS_NAME}    ${REVENUE_ORDER_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Revenue Order Name
    [Documentation]    Select the revenue order, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${REVENUE_ORDER_TABLE}
    ...    ${REVENUE_ORDER_UPD_CODE}
    ...    ${REVENUE_ORDER_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete Revenue Order
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${REVENUE_ORDER_TABLE}    ${REVENUE_ORDER_DEL_ENDDATE}    ${code}    ${date}
