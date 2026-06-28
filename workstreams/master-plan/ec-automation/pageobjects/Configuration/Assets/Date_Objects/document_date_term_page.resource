*** Settings ***
Documentation       T3 (screen) -- Document Date Term page object.
...                 Screen: Configuration > Assets > Date Objects > Document Date Term (CD.0107).
...                 Manage-Object (OV, date-effective) screen. Holds Document Date Term's
...                 locators + thin IUD wrappers that delegate to T2 (manage_object) and
...                 T1 (common). Richer than Bank: the New-Object form has two extra
...                 mandatory inputs beyond the universal Code/Name/Start-Date trio --
...                 a METHOD autocomplete dropdown (R:6) and a numeric OFFSET cell (R:7).
...                 DELETE = End Date = Start Date (true delete; row leaves ov_doc_date_term).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${DDT_SCREEN}           Document Date Term
${DDT_TABLE}            manage_object_nav_nav:form:T_data
${DDT_VIEW}             ov_doc_date_term
# objectForm field IDs (Insert -- new object)
${DDT_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${DDT_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${DDT_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
${DDT_INS_METHOD_DD}    tab:tabPanel:objectForm:form:G:0:R:6:C:1:dd
${DDT_INS_OFFSET}       tab:tabPanel:objectForm:form:G:0:R:7:C:1:in
# updateAttributes field IDs (Update -- existing object; Code read-only after creation)
${DDT_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${DDT_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete -- End Date = Start Date)
${DDT_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Document Date Term Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to env user),
    ...    navigate to the Document Date Term screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${DDT_SCREEN}    ${user}    ${pass}

Document Date Term Row Should Exist
    [Documentation]    Assert a Document Date Term with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${DDT_TABLE}    ${code}

Document Date Term Row Should Not Exist
    [Documentation]    Assert a Document Date Term with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${DDT_TABLE}    ${code}

Document Date Term Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_doc_date_term.
    [Arguments]    ${code}
    Code Should Be Present In View    ${DDT_VIEW}    ${code}

Document Date Term Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_doc_date_term.
    [Arguments]    ${code}
    Code Should Be Absent In View    ${DDT_VIEW}    ${code}

Document Date Term Row Should Show Name
    [Documentation]    Assert the Document Date Term row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${DDT_TABLE}    ${code}    ${name}

Insert Document Date Term Record
    [Documentation]    Insert a new Document Date Term: New Object form -> universal trio
    ...    (Code/Name/Start Date via T2) -> the two screen-specific mandatory extras
    ...    (METHOD dropdown + numeric OFFSET) -> Save + reload. The dropdown is filled
    ...    AFTER the date Tab-out and OFFSET is filled LAST so neither re-render clears it.
    [Arguments]    ${code}    ${name}    ${start_date}    ${method}    ${offset}
    Fill New Object Form    ${DDT_INS_CODE}    ${DDT_INS_NAME}    ${DDT_INS_DATE}    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${DDT_INS_METHOD_DD}    ${method}
    Fill EC Field    ${DDT_INS_OFFSET}    ${offset}
    Save And Refresh List

Update Document Date Term Name
    [Documentation]    Select the object by code (proves it loaded), edit Name, Save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${DDT_TABLE}    ${DDT_UPD_CODE}    ${DDT_UPD_NAME}    ${code}    ${new_name}

Delete Document Date Term
    [Documentation]    Select the object, set End Date = Start Date (true delete), Save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${DDT_TABLE}    ${DDT_DEL_ENDDATE}    ${code}    ${date}
