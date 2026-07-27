*** Settings ***
Documentation       T3 (screen) - Config Variable page object.
...                 Screen: Configuration > Assets > Calculation_Objects > Config Variable (IN.0031). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Config Variable
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Code" Name="Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Config Variable Screen
    [Documentation]    Suite Setup: launch, login, open Config Variable, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Config Variable Row Should Exist
    [Documentation]    Assert a config_variable with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Config Variable Row Should Not Exist
    [Documentation]    Assert a config_variable with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Config Variable Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CONFIG_VARIABLE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CONFIG_VARIABLE    ${code}

Config Variable Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CONFIG_VARIABLE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CONFIG_VARIABLE    ${code}

Config Variable Row Should Show Name
    [Documentation]    Assert the Config Variable row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Config Variable Record
    [Documentation]    Insert a new config_variable: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Code    ${code}
    Fill OV Field By Label    objectForm    Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Calculation Context    Cargo Load/Unload
    Save
    Apply Navigator

Update Config Variable Name
    [Documentation]    Select the config_variable, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Name    ${new_name}
    Save
    Apply Navigator

Delete Config Variable
    [Documentation]    Select the config_variable, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
