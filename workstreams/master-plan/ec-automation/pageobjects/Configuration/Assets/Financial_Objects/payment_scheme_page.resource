*** Settings ***
Documentation       T3 (screen) — Payment Scheme page object.
...                 Screen: Configuration > Assets > Financial Objects > Payment Scheme.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${PAYMENT_SCHEME_SCREEN}    Payment Scheme
${PAYMENT_SCHEME_TABLE}    manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${PAYMENT_SCHEME_INS_CODE}    tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${PAYMENT_SCHEME_INS_NAME}    tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${PAYMENT_SCHEME_INS_DATE}    tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${PAYMENT_SCHEME_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${PAYMENT_SCHEME_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${PAYMENT_SCHEME_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Payment Scheme Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Payment Scheme screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${PAYMENT_SCHEME_SCREEN}

Payment Scheme Row Should Exist
    [Documentation]    Assert a payment scheme with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${PAYMENT_SCHEME_TABLE}    ${code}

Payment Scheme Row Should Not Exist
    [Documentation]    Assert a payment scheme with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${PAYMENT_SCHEME_TABLE}    ${code}

Payment Scheme Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_PAYMENT_SCHEME.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_PAYMENT_SCHEME    ${code}

Payment Scheme Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_PAYMENT_SCHEME.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_PAYMENT_SCHEME    ${code}

Payment Scheme Row Should Show Name
    [Documentation]    Assert the Payment Scheme row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${PAYMENT_SCHEME_TABLE}    ${code}    ${name}

Insert Payment Scheme Record
    [Documentation]    Insert a new payment scheme: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${PAYMENT_SCHEME_INS_CODE}    ${PAYMENT_SCHEME_INS_NAME}    ${PAYMENT_SCHEME_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Payment Scheme Name
    [Documentation]    Select the payment scheme, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${PAYMENT_SCHEME_TABLE}    ${PAYMENT_SCHEME_UPD_CODE}    ${PAYMENT_SCHEME_UPD_NAME}    ${code}    ${new_name}

Delete Payment Scheme
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${PAYMENT_SCHEME_TABLE}    ${PAYMENT_SCHEME_DEL_ENDDATE}    ${code}    ${date}
