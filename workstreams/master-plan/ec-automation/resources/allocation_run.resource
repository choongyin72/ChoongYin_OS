*** Settings ***
Documentation       T2 pattern — N2 Allocation calc RUN + verify (the calculation heart of EC).
...                 For a DATE(range) + Allocation Network + Calculation Job, the screen RUNS the
...                 allocation synchronously via a green "RUN CALCULATIONS" button; the result lands
...                 in the `log_list` grid with an Exit Status (Success / Failure). The calc
...                 distributes measured field/stream totals onto wells/streams, writing per-object
...                 quantities to the *_DAY_ALLOC tables — verified with the DB conservation oracle
...                 (DbVerify: no-negatives, see docs/pattern_n2_allocation_run_design.md).
...
...                 RUN MECHANISM (DB- & UI-proven 2026-06-13): synchronous, NOT BPM. The
...                 "Process automation not available" bell is a BPM red herring. Use **Simulate**
...                 (a checkbox) for safe iteration — it runs the full calc flow but NEVER writes the
...                 DB (SME-confirmed), and completes in ~1-2s; the non-simulate path goes through
...                 the Quartz executor (ACQUIRED) and can stall in this sandbox. So functional
...                 RUN tests use Simulate; the conservation oracle is asserted on real persisted
...                 results (existing allocation data) at the DB.
...
...                 Cross-screen N2 mechanics live here (component ids are the EC allocation-run
...                 composite, shared by allocation RUN screens); the screen NAME + scope data
...                 (networks, jobs, dates, result table) live in the T3 page object.

Library             Collections
Library             String
Library             Browser
Resource            common.resource


*** Variables ***
# Navigator date fields — From Date = group G:0, To Date = G:1 (da_input calendar fields).
${ALLOC_FROM_DATE_FIELD}    nav:form:G:0:R:1:C:0:da_input
${ALLOC_TO_DATE_FIELD}      nav:form:G:1:R:1:C:0:da_input
# Navigator dropdown GROUP indices: G:2 = Allocation Network, G:4 = Calculation Job.
# (The dd is the autocomplete kind — handled by the robust Select EC Dropdown Option.)
${ALLOC_NETWORK_GROUP}      2
${ALLOC_CALCJOB_GROUP}      4
# Simulate checkbox — a native <input type=checkbox> styled with the EC ECCheckboxCell class
# (it IS the visible cell; there is no separate ...C:2 container element). Click it to toggle.
${ALLOC_SIMULATE_INPUT}     dateStartJob:form:G:0:R:1:C:2:cb
# Green RUN CALCULATIONS button (runs the calc synchronously).
${ALLOC_RUN_BUTTON}         ProdAllocButton:form:B
# Completed-runs grid; each row: [Timestamp, RunNo, User, Date, NETWORK(4), Duration, Details,
# EXIT STATUS(7), ...]. Newest run = top row (ri=0).
${ALLOC_LOG_GRID}           log_list:form:T_data
${ALLOC_LOG_NETWORK_COL}    ${4}
${ALLOC_LOG_STATUS_COL}     ${7}


*** Keywords ***
Set Allocation Date Range
    [Documentation]    Set the navigator From/To dates (the period to allocate). Use a DATA-BEARING
    ...    date — the network/job dds and the source data are date-effective.
    [Arguments]    ${from_date}    ${to_date}=${from_date}
    Fill EC Date    ${ALLOC_FROM_DATE_FIELD}    ${from_date}
    Fill EC Date    ${ALLOC_TO_DATE_FIELD}    ${to_date}

Select Allocation Network
    [Documentation]    Pick the Allocation Network (G:2). This cascades to populate the
    ...    Calculation Job dd (G:4) with the jobs wired to that network in ALLOC_NETWORK_JOB_CONN.
    [Arguments]    ${network}
    Select EC Dropdown Option    nav:form:G:${ALLOC_NETWORK_GROUP}:R:1:C:0:dd    ${network}

Select Allocation Calc Job
    [Documentation]    Pick the Calculation Job (G:4) — only populated after a network with a wired
    ...    calc job is selected (e.g. "01 Run No .test", "Daily Well Volume").
    [Arguments]    ${calc_job}
    Select EC Dropdown Option    nav:form:G:${ALLOC_CALCJOB_GROUP}:R:1:C:0:dd    ${calc_job}

Apply Allocation Navigator
    [Documentation]    Click the navigator Go (button:form:B) to load the run panel for the chosen
    ...    date + network + job. Mandatory before RUN CALCULATIONS.
    Apply Navigator

Enable Allocation Simulate
    [Documentation]    Turn the Simulate checkbox ON (idempotent) so the RUN executes the calc but
    ...    writes NOTHING to the DB. The checkbox is a native <input> styled as an EC cell; a JS
    ...    click toggles .checked AND fires EC's onclick (PrimeFaces serializes the checked state on
    ...    the RUN ajax). A direct JS click is used because the cell's headed actionability is flaky.
    ...    Asserts the input is checked afterwards (ground truth for the no-DB-write guard).
    ${now}=    Evaluate JavaScript    ${None}
    ...    () => { const i = document.getElementById('${ALLOC_SIMULATE_INPUT}'); if (!i) return false; if (!i.checked) i.click(); return !!i.checked; }
    Sleep    0.6s
    Should Be True    ${now}    msg=Simulate checkbox did not enable (no-DB-write guard failed)

Run Allocation Calculations
    [Documentation]    Click the green RUN CALCULATIONS button to execute the allocation calc.
    ...    Synchronous under Simulate (~1-2s); the result appears in the log_list grid.
    Click    css=[id="${ALLOC_RUN_BUTTON}"]
    Wait For Load State    networkidle    timeout=30s
    Sleep    1.0s

Get Allocation Top Log Row
    [Documentation]    Return the newest (top) log_list row as a list of cell texts, or an empty
    ...    list if the grid has no rows yet.
    ${cells}=    Evaluate JavaScript    ${None}
    ...    () => { const t=document.getElementById('${ALLOC_LOG_GRID}'); if(!t) return []; const tr=t.querySelector('tr'); return tr ? [...tr.querySelectorAll('td')].map(td=>(td.textContent||'').trim()) : []; }
    RETURN    ${cells}

Allocation Exit Status For Network
    [Documentation]    Poll the log_list top row until it belongs to ${network} AND shows a terminal
    ...    Exit Status (Success/Failure/Error), then return that status. Matching on the network cell
    ...    disambiguates the just-submitted run from a prior one. Fails if no terminal status for the
    ...    network appears within the poll window (~24s).
    [Arguments]    ${network}    ${polls}=12
    FOR    ${_}    IN RANGE    ${polls}
        ${row}=    Get Allocation Top Log Row
        ${len}=    Get Length    ${row}
        IF    ${len} > ${ALLOC_LOG_STATUS_COL}
            ${rownet}=    Get From List    ${row}    ${ALLOC_LOG_NETWORK_COL}
            ${status}=    Get From List    ${row}    ${ALLOC_LOG_STATUS_COL}
            ${terminal}=    Run Keyword And Return Status
            ...    Should Match Regexp    ${status}    (?i)(Success|Failure|Error)
            IF    '${rownet}' == '${network}' and ${terminal}
                Log    Allocation run for '${network}' exited: ${status}
                RETURN    ${status}
            END
        END
        Sleep    2s
        Run Keyword And Ignore Error    Wait For Load State    networkidle    timeout=6s
    END
    Fail    No terminal Exit Status for network '${network}' appeared in log_list within the poll window

Allocation Exit Status Should Be
    [Documentation]    Assert the latest allocation run for ${network} exited with ${expected}
    ...    (substring, case-insensitive — so "Success" matches "Simulate Success"). The trustworthy
    ...    run-outcome assertion; pair a Success with the DB conservation oracle.
    [Arguments]    ${network}    ${expected}
    ${status}=    Allocation Exit Status For Network    ${network}
    Should Contain    ${status}    ${expected}    ignore_case=True
    ...    msg=Allocation run for '${network}' exited '${status}', expected to contain '${expected}'
