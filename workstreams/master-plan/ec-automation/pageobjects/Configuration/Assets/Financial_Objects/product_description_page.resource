*** Settings ***
Documentation       T3 (screen) — Product Description page object.
...                 Screen: Configuration > Assets > Financial Objects > Product Description.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${PRODUCT_DESCRIPTION_SCREEN}    Product Description
${PRODUCT_DESCRIPTION_TABLE}    manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${PRODUCT_DESCRIPTION_INS_CODE}    tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${PRODUCT_DESCRIPTION_INS_NAME}    tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${PRODUCT_DESCRIPTION_INS_DATE}    tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input
# mandatory reference dd: Product (banner-discovered; first option used)
${PRODUCT_DESCRIPTION_INS_DD0}    tab:tabPanel:objectForm:form:G:0:R:5:C:1:dd
# mandatory reference dd: Node (banner-discovered; first option used)
${PRODUCT_DESCRIPTION_INS_DD1}    tab:tabPanel:objectForm:form:G:0:R:6:C:1:dd
# mandatory reference dd: Financial Code (banner-discovered; first option used)
${PRODUCT_DESCRIPTION_INS_DD2}    tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd
# updateAttributes field IDs (Update — existing object)
${PRODUCT_DESCRIPTION_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${PRODUCT_DESCRIPTION_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${PRODUCT_DESCRIPTION_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Product Description Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Product Description screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${PRODUCT_DESCRIPTION_SCREEN}    ${user}    ${pass}

Product Description Row Should Exist
    [Documentation]    Assert a product description with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${PRODUCT_DESCRIPTION_TABLE}    ${code}

Product Description Row Should Not Exist
    [Documentation]    Assert a product description with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${PRODUCT_DESCRIPTION_TABLE}    ${code}

Product Description Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_PRODUCT_NODE_ITEM.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_PRODUCT_NODE_ITEM    ${code}

Product Description Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_PRODUCT_NODE_ITEM.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_PRODUCT_NODE_ITEM    ${code}

Product Description Row Should Show Name
    [Documentation]    Assert the Product Description row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${PRODUCT_DESCRIPTION_TABLE}    ${code}    ${name}

Insert Product Description Record
    [Documentation]    Insert a new product description: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${PRODUCT_DESCRIPTION_INS_CODE}    ${PRODUCT_DESCRIPTION_INS_NAME}    ${PRODUCT_DESCRIPTION_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select First EC Dropdown Option    ${PRODUCT_DESCRIPTION_INS_DD0}
    Select First EC Dropdown Option    ${PRODUCT_DESCRIPTION_INS_DD1}
    Select First EC Dropdown Option    ${PRODUCT_DESCRIPTION_INS_DD2}
    Save And Refresh List

Update Product Description Name
    [Documentation]    Select the product description, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${PRODUCT_DESCRIPTION_TABLE}    ${PRODUCT_DESCRIPTION_UPD_CODE}    ${PRODUCT_DESCRIPTION_UPD_NAME}    ${code}    ${new_name}

Delete Product Description
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${PRODUCT_DESCRIPTION_TABLE}    ${PRODUCT_DESCRIPTION_DEL_ENDDATE}    ${code}    ${date}
