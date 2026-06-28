*** Settings ***
Documentation       EC IUD Test - Document Received Term (Configuration > Assets > Date Objects > Document Received Term, CD.0108).
...                 Manage-Object (OV, date-effective) screen. DELETE = End Date = Start Date (true delete in ov_doc_received_term).
...                 Layered: this test -> document_received_term_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_DRT_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Date_Objects/document_received_term_page.resource

Suite Setup         Set Up Document Received Term Suite
Suite Teardown      Close EC

Test Tags           iud    document-date-term    date-objects


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}
# Screen-specific mandatory extras on the New-Object form
${DRT_METHOD}       Manual entry
${DRT_OFFSET}       0


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Document Received Term Row Should Not Exist    ${TEST_CODE}
    Document Received Term Should Not Exist In DB    ${TEST_CODE}
    Capture Step    drt_tc01_clean

TC02 Insert New Document Received Term
    [Documentation]    Insert a new Document Received Term (Code/Name/Start Date + METHOD + OFFSET) and confirm it appears in the list and DB.
    [Tags]    insert
    Insert Document Received Term Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${DRT_METHOD}    ${DRT_OFFSET}
    Document Received Term Row Should Exist    ${TEST_CODE}
    Document Received Term Should Exist In DB    ${TEST_CODE}
    Capture Step    drt_tc02_inserted

TC03 Update Document Received Term Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Document Received Term Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Document Received Term Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    drt_tc03_updated

TC04 Delete Document Received Term
    [Documentation]    Delete via End Date = Start Date and confirm the object is gone from list and DB.
    [Tags]    delete    cleanup
    Delete Document Received Term    ${TEST_CODE}    ${END_DATE}
    Document Received Term Row Should Not Exist    ${TEST_CODE}
    Document Received Term Should Not Exist In DB    ${TEST_CODE}
    Capture Step    drt_tc04_deleted


*** Keywords ***
Set Up Document Received Term Suite
    [Documentation]    Generate a unique test code/name, then open the Document Received Term screen.
    Prepare IUD Object Data    AUTOTEST_DRT_    Doc Received Term
    Open Document Received Term Screen
