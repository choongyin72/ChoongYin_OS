*** Settings ***
Documentation       T3 (screen) — Sales Order page object.
...                 Screen: Configuration > Assets > Financial Objects > Sales Order.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SALES_ORDER_SCREEN}    Sales Order
${SALES_ORDER_TABLE}    manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${SALES_ORDER_INS_CODE}    tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${SALES_ORDER_INS_NAME}    tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${SALES_ORDER_INS_DATE}    tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# mandatory reference dd: Company (banner-discovered; first option used)
${SALES_ORDER_INS_DD0}    tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd
# mandatory reference dd: Field (banner-discovered; first option used)
${SALES_ORDER_INS_DD1}    tab:tabPanel:objectForm:form:G:0:R:8:C:1:dd
# updateAttributes field IDs (Update — existing object)
${SALES_ORDER_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${SALES_ORDER_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${SALES_ORDER_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Sales Order Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Sales Order screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${SALES_ORDER_SCREEN}

Sales Order Row Should Exist
    [Documentation]    Assert a sales order with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${SALES_ORDER_TABLE}    ${code}

Sales Order Row Should Not Exist
    [Documentation]    Assert a sales order with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${SALES_ORDER_TABLE}    ${code}

Sales Order Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_PRODUCT_SALES_ORDER.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_PRODUCT_SALES_ORDER    ${code}

Sales Order Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_PRODUCT_SALES_ORDER.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_PRODUCT_SALES_ORDER    ${code}

Sales Order Row Should Show Name
    [Documentation]    Assert the Sales Order row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${SALES_ORDER_TABLE}    ${code}    ${name}

Insert Sales Order Record
    [Documentation]    Insert a new sales order: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${SALES_ORDER_INS_CODE}    ${SALES_ORDER_INS_NAME}    ${SALES_ORDER_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select First EC Dropdown Option    ${SALES_ORDER_INS_DD0}
    Select First EC Dropdown Option    ${SALES_ORDER_INS_DD1}
    Save And Refresh List

Update Sales Order Name
    [Documentation]    Select the sales order, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${SALES_ORDER_TABLE}    ${SALES_ORDER_UPD_CODE}    ${SALES_ORDER_UPD_NAME}    ${code}    ${new_name}

Delete Sales Order
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${SALES_ORDER_TABLE}    ${SALES_ORDER_DEL_ENDDATE}    ${code}    ${date}
