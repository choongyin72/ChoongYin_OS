*** Settings ***
Documentation       T3 (screen) - Document Sequence page object.
...                 Screen: Configuration > Assets > Revenue_Document_Objects > Document Sequence (CD.0109). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${SCREEN_GRID};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Document Sequence
${SCREEN_GRID}          nav:form:T_data
# NO hardcoded ids: grid = shared T2 ${SCREEN_GRID}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Code" Name="Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Document Sequence Screen
    [Documentation]    Suite Setup: launch, login, open Document Sequence, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Refresh Screen    # custom-URL OV: no GO; grid loads on open, toolbar Refresh after writes

Document Sequence Row Should Exist
    [Documentation]    Assert a document_sequence with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${SCREEN_GRID}    ${code}

Document Sequence Row Should Not Exist
    [Documentation]    Assert a document_sequence with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${SCREEN_GRID}    ${code}

Document Sequence Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_DOC_SEQUENCE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_DOC_SEQUENCE    ${code}

Document Sequence Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_DOC_SEQUENCE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_DOC_SEQUENCE    ${code}

Document Sequence Row Should Show Name
    [Documentation]    Assert the Document Sequence row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${SCREEN_GRID}    ${code}    ${name}

Insert Document Sequence Record
    [Documentation]    Insert a new document_sequence: New Object form -> Code/Name/Start Date (+ mandatory dropdowns/extra fields) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Code    ${code}
    Fill OV Field By Label    objectForm    Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill Document Sequence Mandatory Extras
    Save And Refresh List

Fill Document Sequence Mandatory Extras
    [Documentation]    Fill the mandatory dropdown(s) + extra field(s) for Document Sequence, split out of Insert to keep
    ...    the Insert keyword within the keyword-count limit. All label-driven (no hardcoded ids).
    Fill OV Field By Label    objectForm    Starting Point    1

Update Document Sequence Name
    [Documentation]    Select the document_sequence, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${SCREEN_GRID}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Name    ${new_name}
    Save And Refresh List

Delete Document Sequence
    [Documentation]    Select the document_sequence, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${SCREEN_GRID}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save And Refresh List
