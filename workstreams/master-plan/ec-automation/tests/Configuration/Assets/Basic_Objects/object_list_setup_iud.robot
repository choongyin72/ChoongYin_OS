*** Settings ***
Documentation       EC IUD Test - Object List Setup (Configuration > Assets > Basic Objects).
...                 Parent-child setup screen: adds/removes a MEMBER ITEM of an existing
...                 Object List (list + class user-approved 2026-06-11). The member object
...                 6931250 is only REFERENCED (a membership row is created and physically
...                 deleted again) — the account object itself is never modified.
...                 DB oracle = count-delta on OBJECT_LIST_SETUP, so pre-existing rows in
...                 other lists never affect the result.

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/object_list_setup_page.resource

Suite Setup         Set Up Object List Setup Suite
Suite Teardown      Close EC

Test Tags           iud    object-list-setup


*** Variables ***
# navigator + member values - user-approved 2026-06-11
${LIST_CLASS}       FIN_ACCOUNT
${OBJECT_LIST}      OPEX GL Equipment Rental
${ITEM_OBJECT}      6931250
${START_DATE}       ${TEST_START_DATE_REFDD}
${BASE_COUNT}       ${EMPTY}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Record the DB baseline for the member code and confirm the item
    ...    is not currently in the chosen list's grid.
    [Tags]    clean-state
    Item Row Should Not Exist    ${ITEM_OBJECT}
    Capture Step    object_list_setup_tc01_clean

TC02 Insert Object List Item
    [Documentation]    Add the member item and confirm grid + DB (+1 vs baseline).
    [Tags]    insert
    Insert Object List Item    ${ITEM_OBJECT}    ${START_DATE}
    Item Row Should Exist    ${ITEM_OBJECT}
    ${expected}=    Evaluate    ${BASE_COUNT} + 1
    Item Count In DB Should Be    ${ITEM_OBJECT}    ${expected}
    Capture Step    object_list_setup_tc02_inserted

TC03 Delete Object List Item
    [Documentation]    Physically delete the member item and confirm grid + DB (back to baseline).
    [Tags]    delete    cleanup
    Delete Object List Item    ${ITEM_OBJECT}
    Item Row Should Not Exist    ${ITEM_OBJECT}
    Item Count In DB Should Be    ${ITEM_OBJECT}    ${BASE_COUNT}
    Capture Step    object_list_setup_tc03_deleted


*** Keywords ***
Set Up Object List Setup Suite
    [Documentation]    Open the screen with the approved navigator context and record
    ...    the DB baseline count for the member code (delta-style verification).
    Open Object List Setup Screen    ${LIST_CLASS}    ${OBJECT_LIST}
    ${n}=    Item Count In DB    ${ITEM_OBJECT}
    VAR    ${BASE_COUNT}=    ${n}    scope=SUITE
