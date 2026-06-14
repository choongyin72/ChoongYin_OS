*** Settings ***
Documentation       EC N1 Test — "Sub Daily Production Well Status 1 - by Well" — the N1 SUB-DAILY
...                 generalization (intraday intervals). READ-ONLY scope (proven 2026-06-14): the
...                 genuinely-new mechanic is datetime-keyed navigation — the grid shows ONE well
...                 with the TIME down the rows, and a target interval is resolved by its Daytime
...                 value (DB key = PWEL_SUB_DAY_STATUS PK (OBJECT_ID, DAYTIME[+time], SUMMER_TIME),
...                 NOT the daily TRUNC(DAYTIME)). This suite proves the 4-level cascade + GO render
...                 the intraday grid AND that distinct hours resolve to distinct rows.
...
...                 The edit-in-place WRITE is now PROVEN: TC03 edits the 00:00 interval's WHP cell
...                 (C9 = AVG_WH_PRESS) and DB-verifies it persisted. KEY: the grid shows psi but the
...                 DB stores bar, so the oracle is UNIT-ROBUST — it derives the factor live
...                 (UI_before / DB_before) and asserts DB_after ≈ typed_display / factor (see
...                 docs reference_ec_ui_db_unit_conversion). (The original write fail targeted C3
...                 "On Strm[hr]", a non-persisting/derived cell — always edit→diff per screen.)
...                 Self-clean = DB-restore AVG_WH_PRESS to its known baseline (210 bar).
...                 Layered: this test → subdaily_well_status_page (T3) → daily_status_grid (T2) +
...                 common (T1) + DbVerify. Recon: tmp/scripts/n1_subdaily_*.

Resource            ../../pageobjects/Production/subdaily_well_status_page.resource

Suite Setup         Open Sub Daily Well Status Screen
Suite Teardown      Run Keywords    Restore WHP To Baseline    AND    Close EC

Test Tags           n1    sub_daily_well_status


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The 4-level cascade (FRMW PU → Area → Facility 1 → Well) + GO renders the
    ...    pre-instantiated intraday interval rows for the well on the day (hourly 00:00–23:00).
    [Tags]    smoke
    ${rows}=    Get Table Rows    ${SUBDAILY_GRID}
    Should Not Be Empty    ${rows}    msg=No sub-daily interval rows rendered for the navigator scope/date
    Capture Step    subdaily_tc01_grid_loaded

TC02 Distinct Hours Resolve To Distinct Rows
    [Documentation]    The NEW sub-daily mechanic (read-only proof): the grid is time-keyed — two
    ...    different Daytime values resolve to two different grid rows (so an edit can target a
    ...    specific intraday interval by its timestamp, the basis of the datetime-keyed DB oracle).
    [Tags]    datetime_key
    ${r0}=    Sub Daily Row Index For Daytime    ${SCOPE_DATE} 00:00
    ${r1}=    Sub Daily Row Index For Daytime    ${SCOPE_DATE} 01:00
    Should Be True    ${r0} >= 0    msg=Interval '${SCOPE_DATE} 00:00' did not resolve to a grid row
    Should Be True    ${r1} >= 0    msg=Interval '${SCOPE_DATE} 01:00' did not resolve to a grid row
    Should Not Be Equal As Integers    ${r0}    ${r1}
    ...    msg=Distinct hours resolved to the same row (${r0}) — datetime row keying is broken
    Capture Step    subdaily_tc02_datetime_rows

TC03 Edit Intraday WHP Cell And Persist (unit-robust)
    [Documentation]    The sub-daily WRITE proof: edit the 00:00 interval's WHP cell, Save, and
    ...    DB-verify it persisted to AVG_WH_PRESS — accounting for the UI(psi)↔DB(bar) unit
    ...    conversion by deriving the factor live. Proves edit-in-place commits for a specific
    ...    intraday interval (the datetime-keyed write), then teardown DB-restores the baseline.
    [Tags]    edit    write
    WHP Edit Should Persist
    Capture Step    subdaily_tc03_whp_persisted
