*** Settings ***
Documentation       T3 (screen) - Document Template page object.
...                 Screen: Configuration > Assets > Revenue_Document_Objects > Document Template (CD.0013). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Document Template
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Code" Name="Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Document Template Screen
    [Documentation]    Suite Setup: launch, login, open Document Template, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Document Template Row Should Exist
    [Documentation]    Assert a document_template with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Document Template Row Should Not Exist
    [Documentation]    Assert a document_template with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Document Template Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_DOC_TEMPLATE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_DOC_TEMPLATE    ${code}

Document Template Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_DOC_TEMPLATE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_DOC_TEMPLATE    ${code}

Document Template Row Should Show Name
    [Documentation]    Assert the Document Template row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Document Template Record
    [Documentation]    Insert a new document_template: New Object form -> Code/Name/Start Date (+ mandatory dropdowns/extra fields) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Code    ${code}
    Fill OV Field By Label    objectForm    Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill Document Template Mandatory Extras
    Save
    Apply Navigator

Fill Document Template Mandatory Extras
    [Documentation]    Fill the mandatory dropdown(s) + extra field(s) for Document Template, split out of Insert to keep
    ...    the Insert keyword within the keyword-count limit. All label-driven (no hardcoded ids).
    Fill OV Field By Label    objectForm    Document Title    1

Update Document Template Name
    [Documentation]    Select the document_template, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Name    ${new_name}
    Save
    Apply Navigator

Delete Document Template
    [Documentation]    Select the document_template, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
