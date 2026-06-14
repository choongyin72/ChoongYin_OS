*** Settings ***
Documentation       EC N1 Test — "Sub Daily Gas Stream Status - by Stream" (edit-in-place), the
...                 SUB-DAILY generalization to a 2nd object class (STREAM, after PWEL). Proves the
...                 datetime-keyed sub-daily pattern is not a one-off: STRM_SUB_DAY_STATUS keys on
...                 (OBJECT_ID, DAYTIME[+time], SUMMER_TIME) just like PWEL_SUB_DAY_STATUS. Open via
...                 the Date + PU→Area→Facility→Stream cascade, resolve the target interval by its
...                 Daytime, EDIT the On Strm[hr] cell (real keystrokes + Tab → stage), Save (menubar
...                 @all → commit), verify on-screen AND in STRM_SUB_DAY_STATUS.ON_STREAM_HRS at that
...                 exact hour (unitless → direct equality), then RESTORE to the recorded original.
...                 The edit→Save→DB check also PROVES the cell↔column map (C1 = On Strm[hr]).
...                 Layered: this test → subdaily_gas_stream_status_page (T3) → daily_status_grid (T2)
...                 + common (T1) + DbVerify.

Resource            ../../pageobjects/Production/subdaily_gas_stream_status_page.resource

Suite Setup         Open Sub Daily Gas Stream Screen
Suite Teardown      Run Keywords    Restore Stream Cell To Original    AND    Close EC

Test Tags           n1    sub_daily_gas_stream_status


*** Variables ***
${SENTINEL_VALUE}       1500


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The Date + 4-level cascade (PU → Area → Facility → Stream) + GO renders the
    ...    pre-instantiated intraday interval rows for the gas stream (hourly). Counts <tr> directly
    ...    (this grid's cells are all inputs — no text — so the text-based Get Table Rows sees none).
    [Tags]    smoke
    ${n}=    Evaluate JavaScript    ${None}
    ...    () => { const t=document.getElementById('${SDS_GRID}'); return t ? t.querySelectorAll('tr').length : 0; }
    Should Be True    ${n} > 0    msg=No sub-daily stream interval rows rendered for the scope/date
    Capture Step    sds_tc01_grid_loaded

TC02 Distinct Hours Resolve To Distinct Rows
    [Documentation]    The sub-daily datetime mechanic (read-only proof): two different Daytime values
    ...    resolve to two different grid rows — so an edit can target a specific intraday interval by
    ...    its timestamp (the basis of the datetime-keyed DB oracle).
    [Tags]    datetime_key
    ${r0}=    Sub Daily Row Index For Daytime    ${SCOPE_DATE} 00:00
    ${r1}=    Sub Daily Row Index For Daytime    ${SCOPE_DATE} 01:00
    Should Be True    ${r0} >= 0    msg=Interval '${SCOPE_DATE} 00:00' did not resolve to a grid row
    Should Be True    ${r1} >= 0    msg=Interval '${SCOPE_DATE} 01:00' did not resolve to a grid row
    Should Not Be Equal As Integers    ${r0}    ${r1}
    ...    msg=Distinct hours resolved to the same row (${r0}) — datetime row keying is broken
    Capture Step    sds_tc02_datetime_rows

TC03 Edit Intraday Cell And Persist
    [Documentation]    Edit the target hour's On Strm[hr] to a sentinel, Save, and confirm persistence
    ...    on-screen AND in STRM_SUB_DAY_STATUS.ON_STREAM_HRS for that exact (stream × date × hour)
    ...    interval — the datetime-keyed oracle (which also proves C1 = ON_STREAM_HRS). Self-cleans by
    ...    restoring the recorded original in Suite Teardown.
    [Tags]    edit
    Set Stream Cell    ${SENTINEL_VALUE}
    Save Stream Status
    Stream Cell Should Show    ${SENTINEL_VALUE}
    Stream Value Should Be In DB    ${SENTINEL_VALUE}
    Capture Step    sds_tc03_edited
