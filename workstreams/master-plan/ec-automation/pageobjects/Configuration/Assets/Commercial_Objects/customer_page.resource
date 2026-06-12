*** Settings ***
Documentation       T3 (screen) — Customer page object.
...                 Screen: Configuration > Assets > Commercial Objects > Customer.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CUSTOMER_SCREEN}          Customer
${CUSTOMER_TABLE}           manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${CUSTOMER_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${CUSTOMER_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${CUSTOMER_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# mandatory extra: ERP Customer Code (text)
${CUSTOMER_INS_X0}          tab:tabPanel:objectForm:form:G:0:R:6:C:1:in
# mandatory extra: Official Name (text)
${CUSTOMER_INS_X1}          tab:tabPanel:objectForm:form:G:0:R:7:C:1:in
# mandatory reference dd: Customer Group (banner-discovered; first option used)
${CUSTOMER_INS_DD0}         tab:tabPanel:objectForm:form:G:0:R:22:C:1:dd
# updateAttributes field IDs (Update — existing object)
${CUSTOMER_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${CUSTOMER_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${CUSTOMER_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Customer Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Customer screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CUSTOMER_SCREEN}    ${user}    ${pass}

Customer Row Should Exist
    [Documentation]    Assert a customer with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${CUSTOMER_TABLE}    ${code}

Customer Row Should Not Exist
    [Documentation]    Assert a customer with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${CUSTOMER_TABLE}    ${code}

Customer Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CUSTOMER.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CUSTOMER    ${code}

Customer Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CUSTOMER.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CUSTOMER    ${code}

Customer Row Should Show Name
    [Documentation]    Assert the Customer row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${CUSTOMER_TABLE}    ${code}    ${name}

Insert Customer Record
    [Documentation]    Insert a new customer: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${CUSTOMER_INS_CODE}    ${CUSTOMER_INS_NAME}    ${CUSTOMER_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Fill EC Field    ${CUSTOMER_INS_X0}    ERP999
    Fill EC Field    ${CUSTOMER_INS_X1}    AUTOTEST Official
    Select First EC Dropdown Option    ${CUSTOMER_INS_DD0}
    Save And Refresh List

Update Customer Name
    [Documentation]    Select the customer, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${CUSTOMER_TABLE}    ${CUSTOMER_UPD_CODE}    ${CUSTOMER_UPD_NAME}    ${code}    ${new_name}

Delete Customer
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${CUSTOMER_TABLE}    ${CUSTOMER_DEL_ENDDATE}    ${code}    ${date}
