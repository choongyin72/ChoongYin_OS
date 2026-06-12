*** Settings ***
Documentation       T3 (screen) — Operator Lease page object.
...                 Screen: Configuration > Assets > Commercial Objects > Operator Lease.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${OPERATOR_LEASE_SCREEN}            Operator Lease
${OPERATOR_LEASE_TABLE}             manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${OPERATOR_LEASE_INS_CODE}          tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${OPERATOR_LEASE_INS_NAME}          tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${OPERATOR_LEASE_INS_DATE}          tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${OPERATOR_LEASE_UPD_CODE}          tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${OPERATOR_LEASE_UPD_NAME}          tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${OPERATOR_LEASE_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Operator Lease Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Operator Lease screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${OPERATOR_LEASE_SCREEN}    ${user}    ${pass}

Operator Lease Row Should Exist
    [Documentation]    Assert a operator lease with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OPERATOR_LEASE_TABLE}    ${code}

Operator Lease Row Should Not Exist
    [Documentation]    Assert a operator lease with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OPERATOR_LEASE_TABLE}    ${code}

Operator Lease Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_OPERATOR_LEASE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_OPERATOR_LEASE    ${code}

Operator Lease Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_OPERATOR_LEASE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_OPERATOR_LEASE    ${code}

Operator Lease Row Should Show Name
    [Documentation]    Assert the Operator Lease row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OPERATOR_LEASE_TABLE}    ${code}    ${name}

Insert Operator Lease Record
    [Documentation]    Insert a new operator lease: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${OPERATOR_LEASE_INS_CODE}    ${OPERATOR_LEASE_INS_NAME}    ${OPERATOR_LEASE_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Operator Lease Name
    [Documentation]    Select the operator lease, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${OPERATOR_LEASE_TABLE}
    ...    ${OPERATOR_LEASE_UPD_CODE}
    ...    ${OPERATOR_LEASE_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete Operator Lease
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${OPERATOR_LEASE_TABLE}    ${OPERATOR_LEASE_DEL_ENDDATE}    ${code}    ${date}
