*** Settings ***
Documentation       T2 pattern — N3 Status-process RUN (the P->V->A record-status engine).
...                 For a DATE(range) + a Status Process picked in the navigator, the HA.0001
...                 "Daily Data Status Processes" screen RUNS the process via a "Run Process"
...                 button; the process lifts RECORD_STATUS on the scoped day-status rows
...                 (Provisional 'P' -> Verified 'V' -> Approved 'A') and appends a row to
...                 STAT_PROCESS_STATUS with ROWS_UPDATED = how many rows it lifted.
...
...                 RUN MECHANISM (DB-proven 2026-06-14): the run is ASYNC — dispatched to the
...                 ec-worker scheduler node (NOT synchronous like N2; status processes have NO
...                 Simulate). The "Process automation not available" toolbar bell is the same BPM
...                 red herring as HA.0002. So functional N3 tests submit the run, then POLL THE DB
...                 (STAT_PROCESS_STATUS + the RECORD_STATUS family) for the result — the UI
...                 RunningJobs/result grids are corroboration only. Requires ec-worker RUNNING
...                 (see DeepDiveLearnings/ec-bpm/ec-worker-and-scheduler.md); if it is down the
...                 run sits WAITING and the DB never changes.
...
...                 Cross-screen N3 screen gestures live here (the EC status-process run composite:
...                 date range, the process selector in nav G:2, the Run Process button). The
...                 screen NAME, the chosen process + scope, and the DB oracle live in the T3 page
...                 object. Forked from resources/allocation_run.resource (N2 analog).

Library             Collections
Library             String
Library             Browser
Resource            common.resource


*** Variables ***
# Navigator date fields — From Date = group G:0, To Date = G:1 (da_input calendar fields).
${STATUS_FROM_DATE_FIELD}       nav:form:G:0:R:1:C:0:da_input
${STATUS_TO_DATE_FIELD}         nav:form:G:1:R:1:C:0:da_input
# The Status Process selector is a navigator dropdown at GROUP 2 (its options ARE the process
# names, e.g. "P1 Forward Status Update"); picked BEFORE the navigator Go, like any nav filter.
${STATUS_PROCESS_GROUP}         2
# "Run Process" button (dispatches the run to the async executor).
${STATUS_RUN_BUTTON}            RunProcessButton:form:B
# In-flight jobs grid (shows the submitted run as WAITING until ec-worker acquires it).
${STATUS_RUNNING_GRID}          RunningJobs:form:T_data


*** Keywords ***
Set Status Process Date Range
    [Documentation]    Set the navigator From/To dates (the period to process). Use a DATA-BEARING
    ...    date that has Provisional ('P') rows in the chosen process's scope — otherwise the engine
    ...    finds nothing to lift (and PCK_STATUS raises ORA-06569 on the empty set).
    [Arguments]    ${from_date}    ${to_date}=${from_date}
    Fill EC Date    ${STATUS_FROM_DATE_FIELD}    ${from_date}
    Fill EC Date    ${STATUS_TO_DATE_FIELD}    ${to_date}

Select Status Process
    [Documentation]    Pick the Status Process in the navigator (G:2) — e.g. "P1 Forward Status
    ...    Update" (P->V). This is a mandatory navigator dropdown; the run panel/button only render
    ...    after a process is chosen AND the navigator Go is applied.
    [Arguments]    ${process}
    Select EC Dropdown Option    nav:form:G:${STATUS_PROCESS_GROUP}:R:1:C:0:dd    ${process}

Apply Status Process Navigator
    [Documentation]    Click the navigator Go (button:form:B) to load the run panel for the chosen
    ...    date range + process. Mandatory before Run Process.
    Apply Navigator

Run Status Process
    [Documentation]    Click the "Run Process" button to submit the status-process run. The run is
    ...    ASYNC (executed by ec-worker), so this returns once submitted — assert the DB result next
    ...    (poll STAT_PROCESS_STATUS), NOT a synchronous UI status.
    Click    css=[id="${STATUS_RUN_BUTTON}"]
    Wait For Load State    networkidle    timeout=30s
    Sleep    1.5s

Submit Status Process Run
    [Documentation]    The full screen gesture: set the date range, pick the process in the
    ...    navigator, apply Go, then click Run Process. Leaves the run submitted to the executor.
    [Arguments]    ${date}    ${process}
    Set Status Process Date Range    ${date}    ${date}
    Select Status Process    ${process}
    Apply Status Process Navigator
    Run Status Process

Submit Monthly Status Process Run
    [Documentation]    Monthly screen gesture (verified-live nav model): SINGLE Date (G:0:R:1:C:0:da_input)
    ...    + Process selector at GROUP 1 — NOT From/To + G:2 like the daily screen. Set the month date,
    ...    pick the process at G:1, apply Go, click Run Process. Leaves the run submitted to ec-worker.
    [Arguments]    ${date}    ${process}
    Fill EC Date    ${STATUS_FROM_DATE_FIELD}    ${date}
    Select EC Dropdown Option    nav:form:G:1:R:1:C:0:dd    ${process}
    Apply Status Process Navigator
    Run Status Process
