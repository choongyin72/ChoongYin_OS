*** Settings ***
Documentation       T3 (screen) - Transactional Inventory Layout Set page object.
...                 Screen: EC_Revenue > Inventory > Transactional_Inventory > Configuration > Transactional Inventory Layout Set (IN.0033). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../../libraries/DbVerify.py
Resource            ../../../../../resources/common.resource
Resource            ../../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Transactional Inventory Layout Set
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Code" Name="Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Transactional Inventory Layout Set Screen
    [Documentation]    Suite Setup: launch, login, open Transactional Inventory Layout Set, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Transactional Inventory Layout Set Row Should Exist
    [Documentation]    Assert a transactional_inventory_layout_set with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Transactional Inventory Layout Set Row Should Not Exist
    [Documentation]    Assert a transactional_inventory_layout_set with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Transactional Inventory Layout Set Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_TRANS_INV_TMPL_SET.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_TRANS_INV_TMPL_SET    ${code}

Transactional Inventory Layout Set Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_TRANS_INV_TMPL_SET.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_TRANS_INV_TMPL_SET    ${code}

Transactional Inventory Layout Set Row Should Show Name
    [Documentation]    Assert the Transactional Inventory Layout Set row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Transactional Inventory Layout Set Record
    [Documentation]    Insert a new transactional_inventory_layout_set: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Code    ${code}
    Fill OV Field By Label    objectForm    Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Transactional Inventory Layout Set Name
    [Documentation]    Select the transactional_inventory_layout_set, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Name    ${new_name}
    Save
    Apply Navigator

Delete Transactional Inventory Layout Set
    [Documentation]    Select the transactional_inventory_layout_set, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
