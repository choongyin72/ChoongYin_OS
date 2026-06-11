*** Settings ***
Documentation       T3 (screen) — MMS Lease page object.
...                 Screen: Configuration > Assets > Commercial Objects > MMS Lease.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${MMS_LEASE_SCREEN}         MMS Lease
${MMS_LEASE_TABLE}          manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${MMS_LEASE_INS_CODE}       tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${MMS_LEASE_INS_NAME}       tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${MMS_LEASE_INS_DATE}       tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${MMS_LEASE_UPD_CODE}       tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${MMS_LEASE_UPD_NAME}       tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${MMS_LEASE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open MMS Lease Screen
    [Documentation]    Suite Setup: launch, login, navigate to the MMS Lease screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${MMS_LEASE_SCREEN}

MMS Lease Row Should Exist
    [Documentation]    Assert a mms lease with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${MMS_LEASE_TABLE}    ${code}

MMS Lease Row Should Not Exist
    [Documentation]    Assert a mms lease with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${MMS_LEASE_TABLE}    ${code}

MMS Lease Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_MMS_LEASE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_MMS_LEASE    ${code}

MMS Lease Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_MMS_LEASE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_MMS_LEASE    ${code}

MMS Lease Row Should Show Name
    [Documentation]    Assert the MMS Lease row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${MMS_LEASE_TABLE}    ${code}    ${name}

Insert MMS Lease Record
    [Documentation]    Insert a new mms lease: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${MMS_LEASE_INS_CODE}    ${MMS_LEASE_INS_NAME}    ${MMS_LEASE_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update MMS Lease Name
    [Documentation]    Select the mms lease, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${MMS_LEASE_TABLE}
    ...    ${MMS_LEASE_UPD_CODE}
    ...    ${MMS_LEASE_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete MMS Lease
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${MMS_LEASE_TABLE}    ${MMS_LEASE_DEL_ENDDATE}    ${code}    ${date}
