*** Settings ***
Documentation       EC IUD Test - Document Template (Configuration > Assets > Revenue_Document_Objects > Document Template, CD.0013).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_DOC_TEMPLATE).
...                 Layered: this test -> document_template_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_DT_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Document_Objects/document_template_page.resource

Suite Setup         Set Up Document Template Suite
Suite Teardown      Close EC

Test Tags           iud    document_template


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test document_template does not exist before inserting.
    [Tags]    clean-state
    Document Template Row Should Not Exist    ${TEST_CODE}
    Capture Step    document_template_tc01_clean

TC02 Insert New Document Template
    [Documentation]    Insert a new document_template; confirm in list + DB (OV_DOC_TEMPLATE).
    [Tags]    insert
    Insert Document Template Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Document Template Row Should Exist    ${TEST_CODE}
    Document Template Should Exist In DB    ${TEST_CODE}
    Capture Step    document_template_tc02_inserted

TC03 Update Document Template
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Document Template Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Document Template Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_DOC_TEMPLATE    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    document_template_tc03_updated

TC04 Delete Document Template
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Document Template    ${TEST_CODE}    ${END_DATE}
    Document Template Row Should Not Exist    ${TEST_CODE}
    Document Template Should Not Exist In DB    ${TEST_CODE}
    Capture Step    document_template_tc04_deleted


*** Keywords ***
Set Up Document Template Suite
    [Documentation]    Generate a unique test code/name, then open the Document Template screen.
    Prepare IUD Object Data    AUTOTEST_DT_    Document Template
    Open Document Template Screen
