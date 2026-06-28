*** Settings ***
Documentation       EC IUD Test - Product Group Setup (Configuration > Assets > Royalty Objects).
...                 3-tier screen, ALL 3 sub-entities covered (full I-U-D each), self-contained
...                 under a test product added to an existing group:
...                   Setup  = add product 'Chemical Product' to group ALL_GENERAL
...                   Cost   = a Product Group Cost under that product (COSTS tab)
...                   SCC    = a Stream Calc Category under that product (SCC tab)
...                 Each entity row carries a unique COMMENTS sentinel and is verified at DB level
...                 (present-in-view) on its backing (DV_PRODUCT_GROUP_SETUP / DV_PRODUCT_GROUP_COST
...                 / PRODUCT_STRM_BAL_CAT). Children (Cost, SCC) are removed before the parent
...                 (Setup product), so the screen is left exactly as found. Existing rows in
...                 ALL_GENERAL and other groups are never touched.

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/product_group_setup_page.resource

Suite Setup         Set Up Product Group Setup Suite
Suite Teardown      Close EC

Test Tags           iud    product-group-setup


*** Variables ***
# pre-flight verified 2026-06-27: 'Chemical Product' is in OV_PRODUCT, NOT in ALL_GENERAL,
# offered in the Setup dd; all sentinel baselines 0 in the 3 backings.
${GROUP}            ALL_GENERAL
${SETUP_PRODUCT}    Chemical Product
${COST_TYPE}        Brokerage Fee
${SCC_CATEGORY}     Total Production
${S_SETUP}          AUTOTEST_PGS_SETUP
${S_SETUP_U}        AUTOTEST_PGS_SETUP_UPD
${S_COST}           AUTOTEST_PGS_COST
${S_COST_U}         AUTOTEST_PGS_COST_UPD
${S_SCC}            AUTOTEST_PGS_SCC
${S_SCC_U}          AUTOTEST_PGS_SCC_UPD


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    All three sentinels absent in their backings before the run.
    [Tags]    clean-state
    Comment Should Be Absent In DB    ${SETUP_E}    ${S_SETUP}
    Comment Should Be Absent In DB    ${COST_E}     ${S_COST}
    Comment Should Be Absent In DB    ${SCC_E}      ${S_SCC}
    Capture Step    product_group_setup_tc01_clean

TC02 Insert Product Group Setup
    [Documentation]    Add the test product to the group (middle grid) + DB verify.
    [Tags]    insert    setup
    Insert Member Row    ${SETUP_E}    ${SETUP_PRODUCT}    ${S_SETUP}
    Comment Should Be Present In DB    ${SETUP_E}    ${S_SETUP}
    Capture Step    product_group_setup_tc02_setup_inserted

TC03 Update Product Group Setup
    [Documentation]    Edit the Setup row's Comments + DB verify (new present, old absent).
    [Tags]    update    setup
    Enter Setup Context
    Update Member Comment    ${SETUP_E}    ${S_SETUP}    ${S_SETUP_U}
    Comment Should Be Present In DB    ${SETUP_E}    ${S_SETUP_U}
    Comment Should Be Absent In DB    ${SETUP_E}    ${S_SETUP}
    Capture Step    product_group_setup_tc03_setup_updated

TC04 Insert Product Group Cost
    [Documentation]    Under the test product, COSTS tab -> add a cost row + DB verify.
    [Tags]    insert    cost
    Enter Sub Context    ${TAB_COST}
    Insert Member Row    ${COST_E}    ${COST_TYPE}    ${S_COST}
    Comment Should Be Present In DB    ${COST_E}    ${S_COST}
    Capture Step    product_group_setup_tc04_cost_inserted

TC05 Update Product Group Cost
    [Documentation]    Edit the Cost row's Comments + DB verify (reload re-arms Save).
    [Tags]    update    cost
    Enter Sub Context    ${TAB_COST}
    Update Member Comment    ${COST_E}    ${S_COST}    ${S_COST_U}
    Comment Should Be Present In DB    ${COST_E}    ${S_COST_U}
    Comment Should Be Absent In DB    ${COST_E}    ${S_COST}
    Capture Step    product_group_setup_tc05_cost_updated

TC06 Insert Stream Calculation Category
    [Documentation]    Under the test product, SCC tab -> add a category row + DB verify.
    [Tags]    insert    scc
    Enter Sub Context    ${TAB_SCC}
    Insert Member Row    ${SCC_E}    ${SCC_CATEGORY}    ${S_SCC}
    Comment Should Be Present In DB    ${SCC_E}    ${S_SCC}
    Capture Step    product_group_setup_tc06_scc_inserted

TC07 Update Stream Calculation Category
    [Documentation]    Edit the SCC row's Comments + DB verify (reload re-arms Save).
    [Tags]    update    scc
    Enter Sub Context    ${TAB_SCC}
    Update Member Comment    ${SCC_E}    ${S_SCC}    ${S_SCC_U}
    Comment Should Be Present In DB    ${SCC_E}    ${S_SCC_U}
    Comment Should Be Absent In DB    ${SCC_E}    ${S_SCC}
    Capture Step    product_group_setup_tc07_scc_updated

TC08 Delete Stream Calculation Category
    [Documentation]    Physically delete the SCC row (child) first + DB verify.
    [Tags]    delete    scc    cleanup
    Enter Sub Context    ${TAB_SCC}
    Delete Member Row    ${SCC_E}    ${S_SCC_U}
    Comment Should Be Absent In DB    ${SCC_E}    ${S_SCC_U}
    Capture Step    product_group_setup_tc08_scc_deleted

TC09 Delete Product Group Cost
    [Documentation]    Physically delete the Cost row (child) + DB verify.
    [Tags]    delete    cost    cleanup
    Enter Sub Context    ${TAB_COST}
    Delete Member Row    ${COST_E}    ${S_COST_U}
    Comment Should Be Absent In DB    ${COST_E}    ${S_COST_U}
    Capture Step    product_group_setup_tc09_cost_deleted

TC10 Delete Product Group Setup
    [Documentation]    Physically delete the test product (parent) + DB verify - screen left as found.
    [Tags]    delete    setup    cleanup
    Enter Setup Context
    Delete Member Row    ${SETUP_E}    ${S_SETUP_U}
    Comment Should Be Absent In DB    ${SETUP_E}    ${S_SETUP_U}
    Capture Step    product_group_setup_tc10_setup_deleted


*** Keywords ***
Set Up Product Group Setup Suite
    [Documentation]    Open the screen and select the test Product Group (no navigator).
    Open Product Group Setup Screen
    Select Product Group    ${GROUP}

Enter Setup Context
    [Documentation]    Reload the screen context (re-select the group) so the middle grid is
    ...    fresh and the toolbar Save re-arms for the next edit (EC does not re-arm Save for a
    ...    2nd edit on a still-loaded form).
    Select Product Group    ${GROUP}

Enter Sub Context
    [Documentation]    Reload context for a sub-entity: re-select the group, the test product
    ...    row (by its Setup comment), and activate the entity's tab - fresh form, Save re-arms.
    [Arguments]    ${tab}
    Select Product Group    ${GROUP}
    Select Setup Row By Comment    ${S_SETUP_U}
    Activate Tab    ${tab}
