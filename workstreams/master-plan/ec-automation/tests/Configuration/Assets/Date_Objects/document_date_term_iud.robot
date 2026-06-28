*** Settings ***
Documentation       EC IUD Test - Document Date Term (Configuration > Assets > Date Objects > Document Date Term, CD.0107).
...                 Manage-Object (OV, date-effective) screen. DELETE = End Date = Start Date (true delete in ov_doc_date_term).
...                 Layered: this test -> document_date_term_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_DDT_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Date_Objects/document_date_term_page.resource

Suite Setup         Set Up Document Date Term Suite
Suite Teardown      Close EC

Test Tags           iud    document-date-term    date-objects


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}
# Screen-specific mandatory extras on the New-Object form
${DDT_METHOD}       Set Document Date manually
${DDT_OFFSET}       0


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Document Date Term Row Should Not Exist    ${TEST_CODE}
    Document Date Term Should Not Exist In DB    ${TEST_CODE}
    Capture Step    ddt_tc01_clean

TC02 Insert New Document Date Term
    [Documentation]    Insert a new Document Date Term (Code/Name/Start Date + METHOD + OFFSET) and confirm it appears in the list and DB.
    [Tags]    insert
    Insert Document Date Term Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${DDT_METHOD}    ${DDT_OFFSET}
    Document Date Term Row Should Exist    ${TEST_CODE}
    Document Date Term Should Exist In DB    ${TEST_CODE}
    Capture Step    ddt_tc02_inserted

TC03 Update Document Date Term Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Document Date Term Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Document Date Term Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    ddt_tc03_updated

TC04 Delete Document Date Term
    [Documentation]    Delete via End Date = Start Date and confirm the object is gone from list and DB.
    [Tags]    delete    cleanup
    Delete Document Date Term    ${TEST_CODE}    ${END_DATE}
    Document Date Term Row Should Not Exist    ${TEST_CODE}
    Document Date Term Should Not Exist In DB    ${TEST_CODE}
    Capture Step    ddt_tc04_deleted


*** Keywords ***
Set Up Document Date Term Suite
    [Documentation]    Generate a unique test code/name, then open the Document Date Term screen.
    Prepare IUD Object Data    AUTOTEST_DDT_    Doc Date Term
    Open Document Date Term Screen
