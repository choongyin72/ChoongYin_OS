*** Settings ***
Documentation       T3 (screen) - Product Group page object.
...                 Screen: Configuration > Assets > Royalty Objects > Product Group.
...                 Manage-Object (OV) screen. Holds Product Group's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${PG_SCREEN}            Product Group
${PG_TABLE}             manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert - new object)
${PG_INS_CODE}          tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${PG_INS_NAME}          tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${PG_INS_DATE}          tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update - existing object)
${PG_UPD_CODE}          tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${PG_UPD_NAME}          tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete - End Date = Start Date)
${PG_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Product Group Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Product Group screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${PG_SCREEN}    ${user}    ${pass}

Product Group Row Should Exist
    [Documentation]    Assert a product group with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${PG_TABLE}    ${code}

Product Group Row Should Not Exist
    [Documentation]    Assert a product group with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${PG_TABLE}    ${code}

Product Group Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_product_group.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_product_group    ${code}

Product Group Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_product_group.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_product_group    ${code}

Product Group Row Should Show Name
    [Documentation]    Assert the Product Group row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    ${row}=    Get Text    xpath=//tbody[@id='${PG_TABLE}']//tr[.//span[normalize-space(text())='${code}']]
    Should Contain    ${row}    ${name}    msg=Product Group row ${code} does not show name ${name}

Insert Product Group Record
    [Documentation]    Insert a new product group: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill EC Field    ${PG_INS_CODE}    ${code}
    Fill EC Field    ${PG_INS_NAME}    ${name}
    Fill EC Date    ${PG_INS_DATE}    ${start_date}
    Save
    Apply Navigator

Update Product Group Name
    [Documentation]    Select the product group, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${PG_TABLE}    ${code}
    ${loaded}=    Get Property    css=[id="${PG_UPD_CODE}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill EC Field    ${PG_UPD_NAME}    ${new_name}
    Save
    Apply Navigator

Delete Product Group
    [Documentation]    Select the product group, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${PG_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${PG_DEL_ENDDATE}    ${date}
    Save
    Apply Navigator
