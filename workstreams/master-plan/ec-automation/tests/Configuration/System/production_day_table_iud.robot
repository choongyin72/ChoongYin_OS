*** Settings ***
Documentation       EC IUD Test - Production Day Table (Configuration > System > Production Day
...                 Table, CO.1033). TV-style inline-editable grid, no navigator. Layered: this
...                 test -> production_day_table_page (T3) -> table/toolbar (T1) + DbVerify.
...
...                 INSERT ONLY - Update and Delete are permanently out of scope. Owner-confirmed
...                 live 2026-08-03: "no deletion is allow in Production Day Table screen. such
...                 feature been disabled." Toolbar Delete never enables for ANY row (confirmed
...                 across 3+ pre-existing rows, not just test data); End Date = Start Date does
...                 NOT remove a row from OV_PRODUCTION_DAY (confirmed via DB - this class is
...                 TIME_SCOPE_CODE=INVARIANT, unlike Constant Standard's VERSIONED delete path).
...
...                 SELF-CLEAN IS IMPOSSIBLE BY DESIGN: every run of this suite permanently
...                 accumulates ONE AUTOTEST_PDT_<timestamp> row with no way to remove it via the
...                 UI. Owner decision 2026-08-03: accept this as a permanent, disclosed exception
...                 (same precedent as Royalty Contract's residual CNTR_PG_SETUP rows). RUN THIS
...                 SUITE SPARINGLY - do not include it in routine/repeated regression sweeps.

Resource            ../../../pageobjects/Configuration/System/production_day_table_page.resource

Suite Setup         Set Up Production Day Table Suite
Suite Teardown      Close EC

Test Tags           iud    production-day-table


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${START_DATE}       ${TEST_START_DATE}


*** Test Cases ***
TC01 Insert New Production Day Table Record
    [Documentation]    Insert a new Production Day Table record (Code + Time Zone
    ...    first-available + Start Date + Name) and confirm it persists in the DB.
    ...    No clean-state / delete test cases - see suite docstring (Insert-only, no
    ...    delete mechanism exists on this screen by design).
    [Tags]    insert
    Insert Production Day Table Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Production Day Table Should Exist In DB    ${TEST_CODE}
    Capture Step    production_day_table_tc01_inserted


*** Keywords ***
Set Up Production Day Table Suite
    [Documentation]    Generate a unique test code, then open the Production Day Table screen.
    Prepare IUD Object Data    AUTOTEST_PDT_    Production Day Table
    Open Production Day Table Screen
