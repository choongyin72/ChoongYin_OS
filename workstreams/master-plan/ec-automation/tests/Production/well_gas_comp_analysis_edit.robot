*** Settings ***
Documentation       EC N1-composition Test - WR.0010.01 Well Gas Component Analysis (edit-in-place).
...                 WELL-level gas-composition sibling of PO.0020. Open via the mandatory (yellow)
...                 navigator (Date + PU + Area + Facility Class 1) -> GO (go_button:form:B); the
...                 analysis HEADER grid lists all date-valid analyses, so SELECT the target analysis
...                 row (by well name) -> its component grid loads. EDIT one component's **mol%**
...                 (Methane, COMPONENT_NO=C1; cell C1_in — like gas, not oil's C2) via real keystrokes
...                 + Tab, Save, verify on-screen AND at the DB (DV_WELL_COMP_ANALYSIS.MOL_PCT for that
...                 COMPONENT_NO), assert a second component (Ethane C2) is UNCHANGED (no normalize),
...                 then REVERT (self-cleaning). TC03 RELOADS + RE-SELECTS the analysis row before
...                 reverting (2nd Save won't re-arm without a fresh grid + row re-select). Layered:
...                 this test -> wr0010_well_gas_comp_analysis_page (T3) -> common (T1) + DbVerify.

Resource            ../../pageobjects/Production/wr0010_well_gas_comp_analysis_page.resource

Suite Setup         Open Well Gas Comp Analysis Screen
Suite Teardown      Close EC

Test Tags           n1    composition    well_gas_comp_analysis


*** Variables ***
${ORIGINAL_VALUE}       ${EMPTY}
${SENTINEL_VALUE}       0.2


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    Mandatory nav + GO + select the analysis row renders the per-component grid; the
    ...    target component's mol% cell resolves and shows a value.
    [Tags]    smoke
    ${v}=    Read Component Mol Pct
    Should Not Be Empty    ${v}    msg=Methane mol% cell empty - grid/analysis row did not load
    Capture Step    wr0010_tc01_grid_loaded

TC02 Edit Mol Pct And Persist
    [Documentation]    Record the original mol%, edit Methane to a sentinel, Save, and confirm
    ...    persistence on-screen AND in DV_WELL_COMP_ANALYSIS.MOL_PCT (COMPONENT_NO=C1). Also assert
    ...    Ethane (C2) is UNCHANGED -> Save persisted only the edited component (no normalize-on-save).
    [Tags]    edit
    ${orig}=    Read Component Mol Pct
    VAR    ${ORIGINAL_VALUE}    ${orig}    scope=SUITE
    Set Component Mol Pct    ${SENTINEL_VALUE}
    Save Composition
    Component Cell Should Show    ${SENTINEL_VALUE}
    Component Mol Pct Should Be In DB    ${SENTINEL_VALUE}
    Component Mol Pct Should Be In DB    ${GUARD_ORIGINAL_VALUE}    component_no=${GUARD_COMPONENT_NO}
    Capture Step    wr0010_tc02_edited

TC03 Revert To Original (cleanup)
    [Documentation]    Restore the original mol% so the analysis is left exactly as found. Reload +
    ...    re-select the analysis row first (post-commit re-render) so the revert edit re-arms Save.
    [Tags]    cleanup
    Reload And Find Target Component
    Set Component Mol Pct    ${ORIGINAL_VALUE}
    Save Composition
    Component Mol Pct Should Be In DB    ${ORIGINAL_VALUE}
    Capture Step    wr0010_tc03_reverted
