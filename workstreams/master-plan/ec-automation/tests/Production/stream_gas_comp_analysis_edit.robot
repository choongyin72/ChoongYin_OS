*** Settings ***
Documentation       EC N1-composition Test - PO.0020 Stream Gas Component Analysis (edit-in-place).
...                 A NEW pattern vs the daily-status grids: per-COMPONENT rows. Open via the 8-field
...                 navigator (2 dates + PU/Area/Facility/Stream/Analysis Status/Sampling Method) -> GO
...                 (go_button:form:B); the grid only loads when Analysis Status=Approved +
...                 Sampling=*Spot match the analysis. EDIT one component's mol% (Methane,
...                 COMPONENT_NO=C1) via real keystrokes + Tab, Save (menubar), verify on-screen AND at
...                 the DB (DV_STRM_COMP_ANALYSIS.MOL_PCT for that COMPONENT_NO), assert a second
...                 component (Ethane C2) is UNCHANGED (Save did not normalize the set), then REVERT
...                 (self-cleaning). Layered: this test -> po0020_stream_gas_comp_analysis_page (T3) ->
...                 common (T1) + DbVerify. Gesture DB-proven (recon_comp_edit_probe 2026-06-17).

Resource            ../../pageobjects/Production/po0020_stream_gas_comp_analysis_page.resource

Suite Setup         Open Stream Gas Comp Analysis Screen
Suite Teardown      Close EC

Test Tags           n1    composition    stream_gas_comp_analysis


*** Variables ***
${ORIGINAL_VALUE}       ${EMPTY}
${SENTINEL_VALUE}       70.50


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The 8-field navigator + GO renders the per-component grid; the target
    ...    component's mol% cell resolves and shows a value.
    [Tags]    smoke
    ${v}=    Read Component Mol Pct
    Should Not Be Empty    ${v}    msg=Methane mol% cell empty - grid did not load for the scope
    Capture Step    po0020_tc01_grid_loaded

TC02 Edit Mol Pct And Persist
    [Documentation]    Record the original mol%, edit Methane to a sentinel, Save, and confirm
    ...    persistence on-screen AND in DV_STRM_COMP_ANALYSIS.MOL_PCT (COMPONENT_NO=C1). Also assert
    ...    Ethane (C2) is UNCHANGED -> Save persisted only the edited component (no normalize-on-save).
    [Tags]    edit
    ${orig}=    Read Component Mol Pct
    VAR    ${ORIGINAL_VALUE}    ${orig}    scope=SUITE
    Set Component Mol Pct    ${SENTINEL_VALUE}
    Save Composition
    Component Cell Should Show    ${SENTINEL_VALUE}
    Component Mol Pct Should Be In DB    ${SENTINEL_VALUE}
    Component Mol Pct Should Be In DB    ${GUARD_ORIGINAL_VALUE}    component_no=${GUARD_COMPONENT_NO}
    Capture Step    po0020_tc02_edited

TC03 Revert To Original (cleanup)
    [Documentation]    Restore the original mol% so the analysis is left exactly as found. Reload first
    ...    (post-commit re-render) so the revert edit re-arms Save.
    [Tags]    cleanup
    Reload And Find Target Component
    Set Component Mol Pct    ${ORIGINAL_VALUE}
    Save Composition
    Component Mol Pct Should Be In DB    ${ORIGINAL_VALUE}
    Capture Step    po0020_tc03_reverted
