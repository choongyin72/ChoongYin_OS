*** Settings ***
Documentation       T3 (screen) - Revenue Stream Category page object.
...                 Screen: Configuration > Assets > Stream_Objects > Revenue Stream Category (CD.0015). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${REVENUE_STREAM_CATEGORY_SCREEN}          Revenue Stream Category
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Stream Category Code" Name="Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Revenue Stream Category Screen
    [Documentation]    Suite Setup: launch, login, open Revenue Stream Category, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${REVENUE_STREAM_CATEGORY_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Revenue Stream Category Row Should Exist
    [Documentation]    Assert a revenue_stream_category with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Revenue Stream Category Row Should Not Exist
    [Documentation]    Assert a revenue_stream_category with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Revenue Stream Category Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_STREAM_CATEGORY.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_STREAM_CATEGORY    ${code}

Revenue Stream Category Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_STREAM_CATEGORY.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_STREAM_CATEGORY    ${code}

Revenue Stream Category Row Should Show Name
    [Documentation]    Assert the Revenue Stream Category row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Revenue Stream Category Record
    [Documentation]    Insert a new revenue_stream_category: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Stream Category Code    ${code}
    Fill OV Field By Label    objectForm    Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Revenue Stream Category Name
    [Documentation]    Select the revenue_stream_category, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Stream Category Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Name    ${new_name}
    Save
    Apply Navigator

Delete Revenue Stream Category
    [Documentation]    Select the revenue_stream_category, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
