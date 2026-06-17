*** Settings ***
Documentation       T3 (screen) — WR.0010.01 Well Gas Component Analysis page object.
...                 Screen: EC (search) > Well Gas Component Analysis (Laboratory / Sample Analysis).
...                 The WELL-level gas-composition sibling of PO.0020 (stream gas). Same per-COMPONENT
...                 grid + same MOL_PCT measure (editable cell `component_set:form:T:{row}:C1_in`, like
...                 gas — NOT oil's C2/wt%), but TWO differences (Phase-1 recon): (1) fill ONLY the
...                 mandatory (yellow) navigator fields — Date + Production Unit + Area + Facility Class 1
...                 — then GO `go_button:form:B` (Well/Well&Hookup/Analysis Status/Sampling are optional);
...                 (2) PU/Area/Facility loads the analysis HEADER grid listing ALL date-valid analyses,
...                 so you must SELECT the target analysis row (`analysis:form`, by Well Name) before its
...                 components load. WRITE gesture = real keystrokes + Tab (T1 Type Cell By Id) then
...                 menubar Save; the revert needs a reload + RE-SELECT of the row first (post-commit
...                 Save won't re-arm in the same session). DB ground truth = view DV_WELL_COMP_ANALYSIS
...                 (ANALYSIS_TYPE=WELL_GAS_COMP), keyed (OBJECT_ID, DAYTIME, COMPONENT_NO); OID via
...                 WELL_VERSION NAME. Recon/design: docs/pattern_well_gas_composition_analysis_design.md.

Library             String
Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/common.resource


*** Variables ***
${COMP_SCREEN}              Well Gas Component Analysis
${COMP_VIEW}                DV_WELL_COMP_ANALYSIS
${WELL_SOURCE}             WELL_VERSION
# Navigator scope — ONLY the mandatory (yellow) fields are filled; Well/Status/Sampling left empty
${SCOPE_DATE}               2025-04-01
${SCOPE_PU}                 P1 Production Unit
${SCOPE_AREA}               P1 Area
${SCOPE_FACILITY}           P1 Facility 1
${NAV_DATE_FROM}            nav:form:G:0:R:1:C:0:da_input
${NAV_DATE_TO}              nav:form:G:1:R:1:C:0:da_input
${NAV_GO}                   go_button:form:B
# Target analysis (selected in the header grid by well name) + component
${TARGET_WELL}              P1 W260 GP Comp Gas
${TARGET_COMPONENT_LABEL}   Methane
${TARGET_COMPONENT_NO}      C1
${COMP_COLUMN}              MOL_PCT
${CELL_SUFFIX}              C1_in
${TARGET_CELL}              ${EMPTY}
# Guard component — assert Save did NOT normalize/rescale the set (Ethane left untouched)
${GUARD_COMPONENT_NO}       C2
${GUARD_ORIGINAL_VALUE}     0.1


*** Keywords ***
Open Well Gas Comp Analysis Screen
    [Documentation]    Suite Setup: launch, login, open the screen, apply the mandatory navigator + GO,
    ...    select the target analysis row, then resolve + cache the component's mol% cell.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${COMP_SCREEN}    ${user}    ${pass}
    Apply Well Comp Navigator
    Select Analysis Row
    Cache Target Component Cell

Apply Well Comp Navigator
    [Documentation]    Fill ONLY the mandatory (yellow) navigator fields — both dates + Production Unit /
    ...    Area / Facility Class 1 — and click GO. The Well / Well & Well Hookup / Analysis Status /
    ...    Sampling Method dropdowns are optional; setting them wrong over-filters to an empty grid.
    Fill EC Date    ${NAV_DATE_FROM}    ${SCOPE_DATE}
    Fill EC Date    ${NAV_DATE_TO}    ${SCOPE_DATE}
    Select EC Dropdown Option    nav:form:G:2:R:1:C:0:dd    ${SCOPE_PU}
    Select EC Dropdown Option    nav:form:G:3:R:1:C:0:dd    ${SCOPE_AREA}
    Select EC Dropdown Option    nav:form:G:4:R:1:C:0:dd    ${SCOPE_FACILITY}
    Click    css=[id="${NAV_GO}"]
    Wait For Load State    networkidle    timeout=18s
    Sleep    1.2s

Select Analysis Row
    [Documentation]    Select the analysis HEADER-grid row whose Well Name = ${TARGET_WELL} (clicking its
    ...    Analysis-No cell), so the component grid loads that analysis. The header lists ALL date-valid
    ...    analyses, so this select step is mandatory (unlike stream/oil which narrow to one analysis).
    ${rid}=    Evaluate JavaScript    ${None}
    ...    () => {let id='';document.querySelectorAll("input[id^='analysis:form:T:'][id$=':C1_in']").forEach(inp=>{if((inp.value||'').trim()==='${TARGET_WELL}'){const m=inp.id.match(/^(analysis:form:T:\\d+):/);if(m)id=m[1]+':C0_in';}});return id;}
    Should Not Be Empty    ${rid}    msg=Analysis row for well '${TARGET_WELL}' not found in the header grid
    Click    css=[id="${rid}"]
    Wait For Load State    networkidle    timeout=12s
    Sleep    1.0s

Cache Target Component Cell
    [Documentation]    Resolve the editable mol% input for ${TARGET_COMPONENT_LABEL} (its grid row found
    ...    by the component's display label, never a hardcoded index) and cache it for the suite.
    ${cell}=    Resolve Component Cell    ${TARGET_COMPONENT_LABEL}
    Should Not Be Empty    ${cell}    msg=Component '${TARGET_COMPONENT_LABEL}' mol% cell not found in the loaded grid
    VAR    ${TARGET_CELL}    ${cell}    scope=SUITE

Reload And Find Target Component
    [Documentation]    Re-apply the navigator (GO), RE-SELECT the analysis row, and re-resolve the
    ...    component cell — used between Save and the revert edit so the revert re-arms Save (post-commit
    ...    re-render; on this screen the second Save does NOT re-arm without a fresh grid + row re-select).
    Apply Well Comp Navigator
    Select Analysis Row
    Cache Target Component Cell

Resolve Component Cell
    [Documentation]    Return the id of the mol% input (`component_set:form:T:{row}:${CELL_SUFFIX}`) on the
    ...    grid row whose label cell equals ${label}. Returns empty string if not present.
    [Arguments]    ${label}
    ${id}=    Evaluate JavaScript    ${None}
    ...    () => {let id='';for(const tr of document.querySelectorAll('table tr')){if([...tr.querySelectorAll('td,th')].some(c=>(c.innerText||'').trim()==='${label}')){const i=tr.querySelector("input[id^='component_set:form:T:'][id$='${CELL_SUFFIX}']");if(i){id=i.id;break;}}}return id;}
    RETURN    ${id}

Read Component Mol Pct
    [Documentation]    Return the cached component cell's current mol% value (commas stripped so the raw
    ...    number can be re-typed on revert). T1 primitive.
    ${v}=    Get Cell Value By Id    ${TARGET_CELL}
    ${clean}=    Replace String    ${v}    ,    ${EMPTY}
    RETURN    ${clean}

Set Component Mol Pct
    [Documentation]    Edit the target component's mol% to ${value} via real keystrokes + Tab (T1 Type
    ...    Cell By Id) so the cell's change event stages the value; value must differ from current.
    [Arguments]    ${value}
    Type Cell By Id    ${TARGET_CELL}    ${value}

Save Composition
    [Documentation]    Commit the grid edit via the toolbar Save (T1; clicks only when enabled). Always
    ...    follow with the DB assertion.
    Save

Component Cell Should Show
    [Documentation]    Assert the on-screen mol% cell shows ${value} (UI side; pair with the DB check).
    [Arguments]    ${value}
    ${v}=    Get Cell Value By Id    ${TARGET_CELL}
    ${vclean}=    Replace String    ${v}    ,    ${EMPTY}
    ${expclean}=    Replace String    ${value}    ,    ${EMPTY}
    Should Be Equal As Numbers    ${vclean}    ${expclean}
    ...    msg=Component cell ${TARGET_CELL} shows '${v}', expected '${value}'

Component Mol Pct Should Be In DB
    [Documentation]    Ground truth: assert ${COMP_COLUMN} of the (well, date, component) row in
    ...    ${COMP_VIEW} equals ${expected}. ${component_no} defaults to the target component (C1); pass
    ...    the guard component (C2) to prove Save did NOT normalize the whole set.
    [Arguments]    ${expected}    ${component_no}=${TARGET_COMPONENT_NO}
    ${oid}=    Object Id By Name    ${WELL_SOURCE}    ${TARGET_WELL}
    Component Value Should Be    ${COMP_VIEW}    ${oid}    ${SCOPE_DATE}    ${component_no}    ${COMP_COLUMN}    ${expected}
