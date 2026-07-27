*** Settings ***
Documentation       EC IUD Test - Document Sequence (Configuration > Assets > Revenue_Document_Objects > Document Sequence, CD.0109).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_DOC_SEQUENCE).
...                 Layered: this test -> document_sequence_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_DS_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Document_Objects/document_sequence_page.resource

Suite Setup         Set Up Document Sequence Suite
Suite Teardown      Close EC

Test Tags           iud    document_sequence


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test document_sequence does not exist before inserting.
    [Tags]    clean-state
    Document Sequence Row Should Not Exist    ${TEST_CODE}
    Capture Step    document_sequence_tc01_clean

TC02 Insert New Document Sequence
    [Documentation]    Insert a new document_sequence; confirm in list + DB (OV_DOC_SEQUENCE).
    [Tags]    insert
    Insert Document Sequence Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Document Sequence Row Should Exist    ${TEST_CODE}
    Document Sequence Should Exist In DB    ${TEST_CODE}
    Capture Step    document_sequence_tc02_inserted

TC03 Update Document Sequence
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Document Sequence Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Document Sequence Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_DOC_SEQUENCE    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    document_sequence_tc03_updated

TC04 Delete Document Sequence
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Document Sequence    ${TEST_CODE}    ${END_DATE}
    Document Sequence Row Should Not Exist    ${TEST_CODE}
    Document Sequence Should Not Exist In DB    ${TEST_CODE}
    Capture Step    document_sequence_tc04_deleted


*** Keywords ***
Set Up Document Sequence Suite
    [Documentation]    Generate a unique test code/name, then open the Document Sequence screen.
    Prepare IUD Object Data    AUTOTEST_DS_    Document Sequence
    Open Document Sequence Screen
