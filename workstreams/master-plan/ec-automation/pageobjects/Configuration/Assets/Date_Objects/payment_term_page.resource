*** Settings ***
Documentation       T3 (screen) -- Payment Term page object.
...                 Screen: Configuration > Assets > Date Objects > Payment Term (CD.0023).
...                 Manage-Object (OV, date-effective) screen. Holds Payment Term's
...                 locators + thin IUD wrappers that delegate to T2 (manage_object) and
...                 T1 (common). Richer than Bank: the New-Object form has two extra
...                 mandatory inputs beyond the universal Code/Name/Start-Date trio --
...                 a METHOD autocomplete dropdown (R:6) and a numeric OFFSET cell (R:7).
...                 DELETE = End Date = Start Date (true delete; row leaves ov_payment_term).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${PT_SCREEN}           Payment Term
${PT_TABLE}            manage_object_nav_nav:form:T_data
${PT_VIEW}             ov_payment_term
# objectForm field IDs (Insert -- new object)
${PT_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${PT_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${PT_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
${PT_INS_METHOD_DD}    tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd
${PT_INS_OFFSET}       tab:tabPanel:objectForm:form:G:0:R:8:C:1:in
# updateAttributes field IDs (Update -- existing object; Code read-only after creation)
${PT_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${PT_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete -- End Date = Start Date)
${PT_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Payment Term Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to env user),
    ...    navigate to the Payment Term screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${PT_SCREEN}    ${user}    ${pass}

Payment Term Row Should Exist
    [Documentation]    Assert a Payment Term with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${PT_TABLE}    ${code}

Payment Term Row Should Not Exist
    [Documentation]    Assert a Payment Term with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${PT_TABLE}    ${code}

Payment Term Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_payment_term.
    [Arguments]    ${code}
    Code Should Be Present In View    ${PT_VIEW}    ${code}

Payment Term Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_payment_term.
    [Arguments]    ${code}
    Code Should Be Absent In View    ${PT_VIEW}    ${code}

Payment Term Row Should Show Name
    [Documentation]    Assert the Payment Term row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${PT_TABLE}    ${code}    ${name}

Insert Payment Term Record
    [Documentation]    Insert a new Payment Term: New Object form -> universal trio
    ...    (Code/Name/Start Date via T2) -> the two screen-specific mandatory extras
    ...    (METHOD dropdown + numeric OFFSET) -> Save + reload. The dropdown is filled
    ...    AFTER the date Tab-out and OFFSET is filled LAST so neither re-render clears it.
    [Arguments]    ${code}    ${name}    ${start_date}    ${method}    ${offset}
    Fill New Object Form    ${PT_INS_CODE}    ${PT_INS_NAME}    ${PT_INS_DATE}    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${PT_INS_METHOD_DD}    ${method}
    Fill EC Field    ${PT_INS_OFFSET}    ${offset}
    Save And Refresh List

Update Payment Term Name
    [Documentation]    Select the object by code (proves it loaded), edit Name, Save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${PT_TABLE}    ${PT_UPD_CODE}    ${PT_UPD_NAME}    ${code}    ${new_name}

Delete Payment Term
    [Documentation]    Select the object, set End Date = Start Date (true delete), Save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${PT_TABLE}    ${PT_DEL_ENDDATE}    ${code}    ${date}
