*** Settings ***
Documentation       T3 (screen) - Storage Flow page object.
...                 Screen: Configuration > Assets > Tank_and_Storage_Objects > Storage Flow (CO.2091). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Storage Flow
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Storage Flow Code" Name="Storage Flow Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Storage Flow Screen
    [Documentation]    Suite Setup: launch, login, open Storage Flow, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Storage Flow Row Should Exist
    [Documentation]    Assert a storage_flow with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Storage Flow Row Should Not Exist
    [Documentation]    Assert a storage_flow with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Storage Flow Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_STORAGE_FLOW.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_STORAGE_FLOW    ${code}

Storage Flow Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_STORAGE_FLOW.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_STORAGE_FLOW    ${code}

Storage Flow Row Should Show Name
    [Documentation]    Assert the Storage Flow row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Storage Flow Record
    [Documentation]    Insert a new storage_flow: New Object form -> Code/Name/Start Date (+ mandatory dropdowns/extra fields) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Storage Flow Code    ${code}
    Fill OV Field By Label    objectForm    Storage Flow Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill Storage Flow Mandatory Extras
    Save
    Apply Navigator

Fill Storage Flow Mandatory Extras
    [Documentation]    Fill the mandatory dropdown(s) + extra field(s) for Storage Flow, split out of Insert to keep
    ...    the Insert keyword within the keyword-count limit. All label-driven (no hardcoded ids).
    Fill OV Dropdown By Label    objectForm    Flow Direction    __FIRST__
    Fill OV Dropdown By Label    objectForm    Storage    __FIRST__

Update Storage Flow Name
    [Documentation]    Select the storage_flow, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Storage Flow Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Storage Flow Name    ${new_name}
    Save
    Apply Navigator

Delete Storage Flow
    [Documentation]    Select the storage_flow, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
