*** Settings ***
Documentation       EC IUD Test - Language (Configuration > System).
...                 TABLE class (TV): inline grid, NO navigator, PHYSICAL delete (base T_BASIS_LANGUAGE).
...                 Id (LANGUAGE_ID) is a REQUIRED (yellow) field and must be filled before Save.
...                 Layered: this test -> language_page (T3) -> table_class (T2) + common/table/toolbar (T1) + DbVerify.
...                 NEVER touch existing data. Fixed test row (physical delete is self-cleaning, so repeatable).

Resource            ../../../pageobjects/Configuration/System/language_page.resource

Suite Setup         Open Language Screen
Suite Teardown      Close EC

Test Tags           iud    language


*** Variables ***
${TEST_ID}      999
${TEST_CODE}    ZZ
${LANG_NAME}    Autotest Lang
${NAME_UPD}     Autotest Lang UPD


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the test language does not exist yet.
    [Tags]    clean-state
    Language Row Should Not Exist    ${TEST_CODE}
    Capture Step    lang_tc01_clean

TC02 Insert New Language
    [Documentation]    Insert a new language (Id + code + name) and confirm it appears (UI + DB).
    [Tags]    insert
    Insert Language    ${TEST_ID}    ${TEST_CODE}    ${LANG_NAME}
    Language Row Should Exist    ${TEST_CODE}
    Language Should Exist In DB    ${TEST_CODE}
    Capture Step    lang_tc02_inserted

TC03 Update Language Name
    [Documentation]    Edit the Name and confirm the change persisted.
    [Tags]    update
    Update Language Name    ${TEST_CODE}    ${NAME_UPD}
    Language Name Should Be    ${TEST_CODE}    ${NAME_UPD}
    Capture Step    lang_tc03_updated

TC04 Delete Language (physical)
    [Documentation]    Physically delete the language and confirm it is gone (UI + base table).
    [Tags]    delete    cleanup
    Delete Language    ${TEST_CODE}
    Language Row Should Not Exist    ${TEST_CODE}
    Language Should Not Exist In DB    ${TEST_CODE}
    Capture Step    lang_tc04_deleted
