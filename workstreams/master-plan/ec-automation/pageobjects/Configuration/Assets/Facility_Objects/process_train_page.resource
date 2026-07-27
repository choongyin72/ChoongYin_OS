*** Settings ***
Documentation       T3 (screen) - Process Train page object.
...                 Screen: Configuration > Assets > Facility_Objects > Process Train (CO.0120). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Process Train
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Process Train Code" Name="Process Train Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Process Train Screen
    [Documentation]    Suite Setup: launch, login, open Process Train, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Process Train Row Should Exist
    [Documentation]    Assert a process_train with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Process Train Row Should Not Exist
    [Documentation]    Assert a process_train with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Process Train Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_PROCESS_TRAIN.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_PROCESS_TRAIN    ${code}

Process Train Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_PROCESS_TRAIN.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_PROCESS_TRAIN    ${code}

Process Train Row Should Show Name
    [Documentation]    Assert the Process Train row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Process Train Record
    [Documentation]    Insert a new process_train: New Object form -> Code/Name/Start Date (+ mandatory dropdowns/extra fields) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Process Train Code    ${code}
    Fill OV Field By Label    objectForm    Process Train Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill Process Train Mandatory Extras
    Save
    Apply Navigator

Fill Process Train Mandatory Extras
    [Documentation]    Fill the mandatory dropdown(s) + extra field(s) for Process Train, split out of Insert to keep
    ...    the Insert keyword within the keyword-count limit. All label-driven (no hardcoded ids).
    Fill OV Dropdown By Label    objectForm    Production Facility Class 1    __FIRST__

Update Process Train Name
    [Documentation]    Select the process_train, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Process Train Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Process Train Name    ${new_name}
    Save
    Apply Navigator

Delete Process Train
    [Documentation]    Select the process_train, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
