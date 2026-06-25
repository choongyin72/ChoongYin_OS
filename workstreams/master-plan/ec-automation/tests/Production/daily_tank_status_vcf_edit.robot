*** Settings ***
Documentation       EC N1 Test - PO.0005.02 Daily Tank Status - VCF Calc (edit-in-place).
...                 TANK variant of the N1 daily-status-grid pattern (after the gas/oil/water/
...                 electrical stream siblings). Open via the 3-level nav cascade, EDIT the Liquid
...                 Dip cell (real keystrokes + Tab -> stage), Save (menubar execute=@all -> commit;
...                 triggers the VCF recalc), verify on-screen AND at the DB
...                 (DV_TANK_DAY_DIP_STATUS.LIQUID_DIP_LEVEL), then REVERT (self-cleaning). UPDATE-only.
...                 Layered: this test -> po000502_daily_tank_status_vcf_page (T3) ->
...                 daily_status_grid (T2) + common (T1) + DbVerify.

Resource            ../../pageobjects/Production/po000502_daily_tank_status_vcf_page.resource

Suite Setup         Open Daily Tank Status VCF Screen
Suite Teardown      Close EC

Test Tags           n1    daily_tank_status_vcf


*** Variables ***
${ORIGINAL_VALUE}       ${EMPTY}
${SENTINEL_VALUE}       1234.5


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The cascade + GO renders the pre-instantiated tank rows for the day.
    [Tags]    smoke
    ${n}=    Tank Grid Row Count
    Should Be True    ${n} > 0    msg=No tank rows rendered for the navigator scope/date
    Capture Step    po000502_tc01_grid_loaded

TC02 Edit Liquid Dip And Persist
    [Documentation]    Record the original dip, edit it to a sentinel, Save (VCF recalcs), and confirm
    ...    persistence on-screen AND in DV_TANK_DAY_DIP_STATUS.LIQUID_DIP_LEVEL (the oracle).
    [Tags]    edit
    ${orig}=    Read Stream Status Value
    VAR    ${ORIGINAL_VALUE}    ${orig}    scope=SUITE
    Set Stream Status Cell    ${SENTINEL_VALUE}
    Save Stream Status
    Stream Status Cell Should Show    ${SENTINEL_VALUE}
    Stream Status Value Should Be In DB    ${SENTINEL_VALUE}
    Capture Step    po000502_tc02_edited

TC03 Revert To Original (cleanup)
    [Documentation]    Restore the seed dip so the test leaves the row exactly as found.
    ...    Reload first (post-commit re-render) so the revert edit arms Save.
    [Tags]    cleanup
    Reload And Find Target Stream
    Set Stream Status Cell    ${ORIGINAL_VALUE}
    Save Stream Status
    Stream Status Value Should Be In DB    ${ORIGINAL_VALUE}
    Capture Step    po000502_tc03_reverted
