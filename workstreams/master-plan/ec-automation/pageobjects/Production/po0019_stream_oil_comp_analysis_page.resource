*** Settings ***
Documentation       T3 (screen) — PO.0019 Stream Oil Component Analysis page object.
...                 Screen: EC (search) > Stream Oil Component Analysis (Laboratory / Sample Analysis
...                 area). The OIL/condensate sibling of PO.0020 (gas): same per-COMPONENT grid + same
...                 8-field navigator (2 dates + Production Unit / Area / Facility Class 1 / Stream /
...                 Analysis Status / Sampling Method) -> GO `go_button:form:B`. TWO differences from
...                 gas, both DB-proven in recon: (1) the editable measured cell is the **WT_PCT**
...                 input `component_set:form:T:{row}:C2_in` (oil's C1_in = mol% is EMPTY — gas edits
...                 C1); (2) the target sits under Facility Class 1 = **P1 Facility Allocation**. WRITE
...                 gesture = real keystrokes + Tab (T1 Type Cell By Id) then menubar Save; the revert
...                 needs a reload first (Save won't re-arm in the same session post-commit). DB ground
...                 truth = view DV_STRM_COMP_ANALYSIS (ANALYSIS_TYPE=STRM_OIL_COMP), keyed (OBJECT_ID,
...                 DAYTIME, COMPONENT_NO); edit Methane (COMPONENT_NO=C1) WT_PCT -> Save persists ONLY
...                 that component (Ethane C2 unchanged = no normalize-on-save).
...                 Recon/design: docs/pattern_oil_composition_analysis_design.md.

Library             String
Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/common.resource


*** Variables ***
${COMP_SCREEN}              Stream Oil Component Analysis
${COMP_VIEW}                DV_STRM_COMP_ANALYSIS
${COMP_STREAM_SOURCE}       OV_STREAM
# Navigator scope (sandbox P1 oil-comp analysis under the ALLOCATION facility; 12-component grid)
${SCOPE_DATE}               2023-06-01
${SCOPE_PU}                 P1 Production Unit
${SCOPE_AREA}               P1 Area
${SCOPE_FACILITY}           P1 Facility Allocation
${TARGET_STREAM}            P1 Alloc S001 M OIL
${ANALYSIS_STATUS}          Approved
${SAMPLING_METHOD}          *Spot
# Navigator field ids (8 groups: G:0/G:1 dates, G:2..G:7 dropdowns)
${NAV_DATE_FROM}            nav:form:G:0:R:1:C:0:da_input
${NAV_DATE_TO}              nav:form:G:1:R:1:C:0:da_input
${NAV_GO}                   go_button:form:B
# Target component. Oil composition is reported in WT_PCT; the editable cell is the C2 column
# (C1 = mol%, EMPTY for oil). The UI row is found by its display label, never a hardcoded index.
${TARGET_COMPONENT_LABEL}   Methane
${TARGET_COMPONENT_NO}      C1
${COMP_COLUMN}              WT_PCT
${CELL_SUFFIX}              C2_in
${TARGET_CELL}              ${EMPTY}
# Guard component — assert Save did NOT normalize/rescale the set (Ethane left untouched)
${GUARD_COMPONENT_NO}       C2
${GUARD_ORIGINAL_VALUE}     0.1


*** Keywords ***
Open Stream Oil Comp Analysis Screen
    [Documentation]    Suite Setup: launch, login, open the screen, fill the 8-field navigator, GO,
    ...    then resolve the target component's wt% cell and cache it.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${COMP_SCREEN}    ${user}    ${pass}
    Apply Composition Navigator
    Cache Target Component Cell

Apply Composition Navigator
    [Documentation]    Set the 8 navigator fields (both dates + the 6 cascade/filter dropdowns) and
    ...    click GO (go_button:form:B). Analysis Status=Approved + Sampling=*Spot loads the grid for
    ...    this analysis (a first-option *New gives an empty grid). Mandatory after any change.
    Fill EC Date    ${NAV_DATE_FROM}    ${SCOPE_DATE}
    Fill EC Date    ${NAV_DATE_TO}    ${SCOPE_DATE}
    Fill Composition Navigator Filters
    Click    css=[id="${NAV_GO}"]
    Wait For Load State    networkidle    timeout=18s
    Sleep    1.2s

Fill Composition Navigator Filters
    [Documentation]    Pick the 6 cascade/filter dropdowns (PU / Area / Facility Class 1 / Stream /
    ...    Analysis Status / Sampling Method) by their data-item-label.
    Select EC Dropdown Option    nav:form:G:2:R:1:C:0:dd    ${SCOPE_PU}
    Select EC Dropdown Option    nav:form:G:3:R:1:C:0:dd    ${SCOPE_AREA}
    Select EC Dropdown Option    nav:form:G:4:R:1:C:0:dd    ${SCOPE_FACILITY}
    Select EC Dropdown Option    nav:form:G:5:R:1:C:0:dd    ${TARGET_STREAM}
    Select EC Dropdown Option    nav:form:G:6:R:1:C:0:dd    ${ANALYSIS_STATUS}
    Select EC Dropdown Option    nav:form:G:7:R:1:C:0:dd    ${SAMPLING_METHOD}

Cache Target Component Cell
    [Documentation]    Resolve the editable wt% input for ${TARGET_COMPONENT_LABEL} (its grid row is
    ...    found by the component's display label, never a hardcoded index) and cache it for the suite.
    ${cell}=    Resolve Component Cell    ${TARGET_COMPONENT_LABEL}
    Should Not Be Empty    ${cell}    msg=Component '${TARGET_COMPONENT_LABEL}' wt% cell not found in the loaded grid
    VAR    ${TARGET_CELL}    ${cell}    scope=SUITE

Reload And Find Target Component
    [Documentation]    Re-apply the navigator (GO) and re-resolve the component cell — used between
    ...    Save and the next edit so the revert edit re-arms Save (post-commit re-render; on this screen
    ...    the second Save does NOT re-arm without a fresh grid).
    Apply Composition Navigator
    Cache Target Component Cell

Resolve Component Cell
    [Documentation]    Return the id of the wt% input (`component_set:form:T:{row}:${CELL_SUFFIX}`) on
    ...    the grid row whose label cell equals ${label}. Returns empty string if not present.
    [Arguments]    ${label}
    ${id}=    Evaluate JavaScript    ${None}
    ...    () => {let id='';for(const tr of document.querySelectorAll('table tr')){if([...tr.querySelectorAll('td,th')].some(c=>(c.innerText||'').trim()==='${label}')){const i=tr.querySelector("input[id^='component_set:form:T:'][id$='${CELL_SUFFIX}']");if(i){id=i.id;break;}}}return id;}
    RETURN    ${id}

Read Component Wt Pct
    [Documentation]    Return the cached component cell's current wt% value (commas stripped so the raw
    ...    number can be re-typed on revert). T1 primitive — no daily-status-grid dependency.
    ${v}=    Get Cell Value By Id    ${TARGET_CELL}
    ${clean}=    Replace String    ${v}    ,    ${EMPTY}
    RETURN    ${clean}

Set Component Wt Pct
    [Documentation]    Edit the target component's wt% to ${value} via real keystrokes + Tab (T1 Type
    ...    Cell By Id) so the cell's change event stages the value; value must differ from current.
    [Arguments]    ${value}
    Type Cell By Id    ${TARGET_CELL}    ${value}

Save Composition
    [Documentation]    Commit the grid edit via the toolbar Save (T1; clicks only when enabled, so it
    ...    implicitly waits for the staged edit to arm Save). Always follow with the DB assertion.
    Save

Component Cell Should Show
    [Documentation]    Assert the on-screen wt% cell shows ${value} (UI side; pair with the DB check).
    ...    Comma-tolerant numeric compare.
    [Arguments]    ${value}
    ${v}=    Get Cell Value By Id    ${TARGET_CELL}
    ${vclean}=    Replace String    ${v}    ,    ${EMPTY}
    ${expclean}=    Replace String    ${value}    ,    ${EMPTY}
    Should Be Equal As Numbers    ${vclean}    ${expclean}
    ...    msg=Component cell ${TARGET_CELL} shows '${v}', expected '${value}'

Component Wt Pct Should Be In DB
    [Documentation]    Ground truth: assert ${COMP_COLUMN} of the (stream, date, component) row in
    ...    ${COMP_VIEW} equals ${expected}. ${component_no} defaults to the target component (C1); pass
    ...    the guard component (C2) to prove Save did NOT normalize the whole set.
    [Arguments]    ${expected}    ${component_no}=${TARGET_COMPONENT_NO}
    ${oid}=    Object Id By Name    ${COMP_STREAM_SOURCE}    ${TARGET_STREAM}
    Component Value Should Be    ${COMP_VIEW}    ${oid}    ${SCOPE_DATE}    ${component_no}    ${COMP_COLUMN}    ${expected}
