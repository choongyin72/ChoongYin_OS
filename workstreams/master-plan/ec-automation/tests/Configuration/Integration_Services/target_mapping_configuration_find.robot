*** Settings ***
Documentation       EC Find-only Test - Target Mapping Configuration (Configuration > Integration
...                 Services > Import > Target Mapping Configuration, IS.0002). REDUCED SCOPE
...                 (owner-confirmed, and independently re-confirmed by this session's own live
...                 DOM probe: the Insert/Delete toolbar `<li>` both carry class
...                 `ui-submenu-state-disabled`; there is no Update icon at all) - this screen does
...                 NOT support Insert/Update/Delete, so only 2 test cases exist here: TC01 (clean
...                 load verification) and TC04 (find an existing real row). No TC02/TC03/TC05 -
...                 this is intentional, not an omission. Zero data mutation anywhere in this suite.
...
...                 Named `..._find.robot` (not the usual `..._iud.robot`) on purpose: this suite
...                 never performs an Insert, Update, or Delete, so the `_iud` suffix used by every
...                 other screen in this tree would misdescribe what it does. Kept in the same
...                 tests/Configuration/Integration_Services/ directory as its siblings
...                 (dummy_tag_event_object_iud.robot, remote_endpoint_config_iud.robot) for
...                 directory-structure consistency - only the filename suffix differs.
...
...                 TC04 uses ONE real, pre-existing row (owner-supplied, live-verified this
...                 session): Class=PWEL_DAY_STATUS, Attribute=AVG_LIQ_VOL, EC Key=ecValue16,
...                 Class Key 1="Key 1", Class Key 2="Key 2". Never modified/re-saved.
...
...                 Layered: this test -> target_mapping_configuration_page (T3) -> common.resource
...                 (T1 login/nav) + DbVerify (DB ground truth). Does NOT reuse manage_object.resource
...                 T2 Insert/Update/Delete keywords - they do not apply to this screen.

Resource            ../../../pageobjects/Configuration/Integration_Services/target_mapping_configuration_page.resource

Suite Setup         Open Target Mapping Configuration Screen
Suite Teardown      Close EC

Test Tags           find-only    target-mapping-configuration


*** Variables ***
${TARGET_CLASS}         PWEL_DAY_STATUS
${TARGET_ATTRIBUTE}     AVG_LIQ_VOL
${TARGET_EC_KEY}        ecValue16
${TARGET_KEY1}          Key 1
${TARGET_KEY2}          Key 2


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Not the usual "AUTOTEST code absent" check (this screen has no
    ...    AUTOTEST/Insert lifecycle) - instead confirms the screen loads correctly: navigator
    ...    renders, GO loads the grid, and at least one data row is visible (the screen's own
    ...    baseline, ~20 real rows on this sandbox). Purely observational, no filter applied.
    [Tags]    clean-state
    Apply Target Mapping Configuration Navigator
    ${count}=    Target Mapping Configuration Row Count
    Should Be True    ${count} > 0    msg=Expected at least one row on initial grid load, got ${count}
    Capture Step    tmc_tc01_clean_load

TC04 Find Existing Target Mapping Record
    [Documentation]    100% read-only: filter the navigator by the known Class, click GO, then
    ...    verify the exact pre-existing row (Class/Attribute/EC Key/Class Key 1/Class Key 2) is
    ...    present with matching field values, and cross-check it independently against the DB
    ...    (OV_IMP_TARGET_MAPPING) by its unique EC Key. Never selects/edits/saves/deletes the row.
    [Tags]    find
    Filter Target Mapping Configuration By Class    ${TARGET_CLASS}
    Apply Target Mapping Configuration Navigator
    Target Mapping Configuration Row Should Be Found
    ...    ${TARGET_CLASS}    ${TARGET_ATTRIBUTE}    ${TARGET_EC_KEY}    ${TARGET_KEY1}    ${TARGET_KEY2}
    Target Mapping Configuration Row Should Exist In DB    ${TARGET_EC_KEY}
    Capture Step    tmc_tc04_found
