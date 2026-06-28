*** Settings ***
Documentation       T3 (screen) -- Document Received Term page object.
...                 Screen: Configuration > Assets > Date Objects > Document Received Term (CD.0108).
...                 Manage-Object (OV, date-effective) screen. Holds Document Received Term's
...                 locators + thin IUD wrappers that delegate to T2 (manage_object) and
...                 T1 (common). Richer than Bank: the New-Object form has two extra
...                 mandatory inputs beyond the universal Code/Name/Start-Date trio --
...                 a METHOD autocomplete dropdown (R:6) and a numeric OFFSET cell (R:7).
...                 DELETE = End Date = Start Date (true delete; row leaves ov_doc_received_term).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${DRT_SCREEN}           Document Received Term
${DRT_TABLE}            manage_object_nav_nav:form:T_data
${DRT_VIEW}             ov_doc_received_term
# objectForm field IDs (Insert -- new object)
${DRT_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${DRT_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${DRT_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
${DRT_INS_METHOD_DD}    tab:tabPanel:objectForm:form:G:0:R:6:C:1:dd
${DRT_INS_OFFSET}       tab:tabPanel:objectForm:form:G:0:R:7:C:1:in
# updateAttributes field IDs (Update -- existing object; Code read-only after creation)
${DRT_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${DRT_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete -- End Date = Start Date)
${DRT_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Document Received Term Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to env user),
    ...    navigate to the Document Received Term screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${DRT_SCREEN}    ${user}    ${pass}

Document Received Term Row Should Exist
    [Documentation]    Assert a Document Received Term with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${DRT_TABLE}    ${code}

Document Received Term Row Should Not Exist
    [Documentation]    Assert a Document Received Term with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${DRT_TABLE}    ${code}

Document Received Term Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_doc_received_term.
    [Arguments]    ${code}
    Code Should Be Present In View    ${DRT_VIEW}    ${code}

Document Received Term Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_doc_received_term.
    [Arguments]    ${code}
    Code Should Be Absent In View    ${DRT_VIEW}    ${code}

Document Received Term Row Should Show Name
    [Documentation]    Assert the Document Received Term row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${DRT_TABLE}    ${code}    ${name}

Insert Document Received Term Record
    [Documentation]    Insert a new Document Received Term: New Object form -> universal trio
    ...    (Code/Name/Start Date via T2) -> the two screen-specific mandatory extras
    ...    (METHOD dropdown + numeric OFFSET) -> Save + reload. The dropdown is filled
    ...    AFTER the date Tab-out and OFFSET is filled LAST so neither re-render clears it.
    [Arguments]    ${code}    ${name}    ${start_date}    ${method}    ${offset}
    Fill New Object Form    ${DRT_INS_CODE}    ${DRT_INS_NAME}    ${DRT_INS_DATE}    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${DRT_INS_METHOD_DD}    ${method}
    Fill EC Field    ${DRT_INS_OFFSET}    ${offset}
    Save And Refresh List

Update Document Received Term Name
    [Documentation]    Select the object by code (proves it loaded), edit Name, Save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${DRT_TABLE}    ${DRT_UPD_CODE}    ${DRT_UPD_NAME}    ${code}    ${new_name}

Delete Document Received Term
    [Documentation]    Select the object, set End Date = Start Date (true delete), Save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${DRT_TABLE}    ${DRT_DEL_ENDDATE}    ${code}    ${date}
