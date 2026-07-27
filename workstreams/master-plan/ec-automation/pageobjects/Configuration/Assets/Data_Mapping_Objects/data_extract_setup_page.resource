*** Settings ***
Documentation       T3 (screen) - Data Extract Setup page object.
...                 Screen: Configuration > Assets > Data_Mapping_Objects > Data Extract Setup (SP.0043). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Data Extract Setup
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Data Extract Setup Code" Name="Data Extract Setup Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Data Extract Setup Screen
    [Documentation]    Suite Setup: launch, login, open Data Extract Setup, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Data Extract Setup Row Should Exist
    [Documentation]    Assert a data_extract_setup with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Data Extract Setup Row Should Not Exist
    [Documentation]    Assert a data_extract_setup with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Data Extract Setup Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_SUMMARY_SETUP.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_SUMMARY_SETUP    ${code}

Data Extract Setup Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_SUMMARY_SETUP.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_SUMMARY_SETUP    ${code}

Data Extract Setup Row Should Show Name
    [Documentation]    Assert the Data Extract Setup row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Data Extract Setup Record
    [Documentation]    Insert a new data_extract_setup: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Data Extract Setup Code    ${code}
    Fill OV Field By Label    objectForm    Data Extract Setup Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Data Extract Type    Actual
    Save
    Apply Navigator

Update Data Extract Setup Name
    [Documentation]    Select the data_extract_setup, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Data Extract Setup Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Data Extract Setup Name    ${new_name}
    Save
    Apply Navigator

Delete Data Extract Setup
    [Documentation]    Select the data_extract_setup, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
