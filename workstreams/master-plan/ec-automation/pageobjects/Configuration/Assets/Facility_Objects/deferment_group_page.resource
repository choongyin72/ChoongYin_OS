*** Settings ***
Documentation       T3 (screen) - Deferment Group page object.
...                 Screen: Configuration > Assets > Facility_Objects > Deferment Group (CO.0149). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Deferment Group
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Deferment Group Code" Name="Deferment Group Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Deferment Group Screen
    [Documentation]    Suite Setup: launch, login, open Deferment Group, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Deferment Group Row Should Exist
    [Documentation]    Assert a deferment_group with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Deferment Group Row Should Not Exist
    [Documentation]    Assert a deferment_group with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Deferment Group Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_DEFERMENT_GROUP.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_DEFERMENT_GROUP    ${code}

Deferment Group Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_DEFERMENT_GROUP.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_DEFERMENT_GROUP    ${code}

Deferment Group Row Should Show Name
    [Documentation]    Assert the Deferment Group row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Deferment Group Record
    [Documentation]    Insert a new deferment_group: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Deferment Group Code    ${code}
    Fill OV Field By Label    objectForm    Deferment Group Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Deferment Group Name
    [Documentation]    Select the deferment_group, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Deferment Group Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Deferment Group Name    ${new_name}
    Save
    Apply Navigator

Delete Deferment Group
    [Documentation]    Select the deferment_group, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
