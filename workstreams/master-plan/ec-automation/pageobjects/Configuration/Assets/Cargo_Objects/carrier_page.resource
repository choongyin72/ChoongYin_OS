*** Settings ***
Documentation       T3 (screen) — Carrier page object.
...                 Screen: Configuration > Assets > Cargo Objects > Carrier.
...                 Manage-Object (OV) screen, Bank-family grid (manage_object_nav_nav:form:T_data) —
...                 NOT gated (navigator is just an optional date). Holds Carrier's locators + thin
...                 IUD wrappers delegating to T2 (manage_object) and T1 (common). Insert requires a
...                 mandatory reference dropdown — "Unit" (first option used for the throwaway record).
...                 DELETE = End Date = Start Date (true delete from ov_carrier).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CARRIER_SCREEN}       Carrier
${CARRIER_TABLE}        manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows from recon LABELS (Start Date at R:4, not R:2)
${CARRIER_INS_CODE}     tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${CARRIER_INS_NAME}     tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${CARRIER_INS_DATE}     tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
# mandatory reference dd: Unit (first option used — value irrelevant for a deleted-again test record)
${CARRIER_INS_UNIT}     tab:tabPanel:objectForm:form:G:0:R:9:C:1:dd
# updateAttributes field IDs (Update — existing object)
${CARRIER_UPD_CODE}     tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${CARRIER_UPD_NAME}     tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${CARRIER_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Carrier Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Carrier screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CARRIER_SCREEN}    ${user}    ${pass}

Carrier Row Should Exist
    [Documentation]    Assert a carrier with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${CARRIER_TABLE}    ${code}

Carrier Row Should Not Exist
    [Documentation]    Assert a carrier with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${CARRIER_TABLE}    ${code}

Carrier Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CARRIER.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CARRIER    ${code}

Carrier Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CARRIER.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CARRIER    ${code}

Carrier Row Should Show Name
    [Documentation]    Assert the Carrier row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${CARRIER_TABLE}    ${code}    ${name}

Insert Carrier Record
    [Documentation]    Insert a new carrier: Code/Name/Start Date + mandatory "Unit" dd -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${CARRIER_INS_CODE}    ${CARRIER_INS_NAME}    ${CARRIER_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select First EC Dropdown Option    ${CARRIER_INS_UNIT}
    Save And Refresh List

Update Carrier Name
    [Documentation]    Select the carrier, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${CARRIER_TABLE}    ${CARRIER_UPD_CODE}    ${CARRIER_UPD_NAME}    ${code}    ${new_name}

Delete Carrier
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${CARRIER_TABLE}    ${CARRIER_DEL_ENDDATE}    ${code}    ${date}
