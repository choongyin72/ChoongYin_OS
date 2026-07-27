*** Settings ***
Documentation       T3 (screen) - HCB System page object.
...                 Screen: Configuration > Assets > Revenue_Lists > HCB System (CD.0097). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          HCB System
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Code" Name="Name" Date="Start Date" End="End Date".


*** Keywords ***
Open HCB System Screen
    [Documentation]    Suite Setup: launch, login, open HCB System, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

HCB System Row Should Exist
    [Documentation]    Assert a hcb_system with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

HCB System Row Should Not Exist
    [Documentation]    Assert a hcb_system with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

HCB System Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_BALANCE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_BALANCE    ${code}

HCB System Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_BALANCE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_BALANCE    ${code}

HCB System Row Should Show Name
    [Documentation]    Assert the HCB System row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert HCB System Record
    [Documentation]    Insert a new hcb_system: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Code    ${code}
    Fill OV Field By Label    objectForm    Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    HCB Category    Operating area system
    Save
    Apply Navigator

Update HCB System Name
    [Documentation]    Select the hcb_system, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Name    ${new_name}
    Save
    Apply Navigator

Delete HCB System
    [Documentation]    Select the hcb_system, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
