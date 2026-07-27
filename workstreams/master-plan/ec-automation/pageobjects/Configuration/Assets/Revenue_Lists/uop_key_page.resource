*** Settings ***
Documentation       T3 (screen) - UOP Key page object.
...                 Screen: Configuration > Assets > Revenue_Lists > UOP Key (CD.0099). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          UOP Key
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Code" Name="Name" Date="Start Date" End="End Date".


*** Keywords ***
Open UOP Key Screen
    [Documentation]    Suite Setup: launch, login, open UOP Key, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

UOP Key Row Should Exist
    [Documentation]    Assert a uop_key with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

UOP Key Row Should Not Exist
    [Documentation]    Assert a uop_key with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

UOP Key Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_FIN_UOP_DEPR_KEY.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FIN_UOP_DEPR_KEY    ${code}

UOP Key Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_FIN_UOP_DEPR_KEY.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FIN_UOP_DEPR_KEY    ${code}

UOP Key Row Should Show Name
    [Documentation]    Assert the UOP Key row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert UOP Key Record
    [Documentation]    Insert a new uop_key: New Object form -> Code/Name/Start Date (+ mandatory dropdowns/extra fields) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Code    ${code}
    Fill OV Field By Label    objectForm    Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill UOP Key Mandatory Extras
    Save
    Apply Navigator

Fill UOP Key Mandatory Extras
    [Documentation]    Fill the mandatory dropdown(s) + extra field(s) for UOP Key, split out of Insert to keep
    ...    the Insert keyword within the keyword-count limit. All label-driven (no hardcoded ids).
    Fill OV Dropdown By Label    objectForm    Company    __FIRST__
    Fill OV Dropdown By Label    objectForm    Key Type    __FIRST__
    Fill OV Field By Label    objectForm    Key Number    1

Update UOP Key Name
    [Documentation]    Select the uop_key, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Name    ${new_name}
    Save
    Apply Navigator

Delete UOP Key
    [Documentation]    Select the uop_key, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
