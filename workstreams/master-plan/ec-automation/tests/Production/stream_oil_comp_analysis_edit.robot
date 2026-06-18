*** Settings ***
Documentation       EC N1-composition Test - PO.0019 Stream Oil Component Analysis (edit-in-place).
...                 OIL/condensate sibling of PO.0020 (gas). Open via the 8-field navigator (2 dates +
...                 PU/Area/Facility/Stream/Analysis Status/Sampling Method) -> GO (go_button:form:B);
...                 grid loads when Analysis Status=Approved + Sampling=*Spot. EDIT one component's
...                 **wt%** (Methane, COMPONENT_NO=C1; cell C2_in — oil's C1=mol% is empty) via real
...                 keystrokes + Tab, Save, verify on-screen AND at the DB
...                 (DV_STRM_COMP_ANALYSIS.WT_PCT for that COMPONENT_NO), assert a second component
...                 (Ethane C2) is UNCHANGED (Save did not normalize), then REVERT (self-cleaning).
...                 TC03 RELOADS before reverting (this screen's 2nd Save won't re-arm without a fresh
...                 grid). Layered: this test -> po0019_stream_oil_comp_analysis_page (T3) -> common
...                 (T1) + DbVerify. Gesture DB-proven (recon_oilcomp_probe 2026-06-17).

Resource            ../../pageobjects/Production/po0019_stream_oil_comp_analysis_page.resource

Suite Setup         Open Stream Oil Comp Analysis Screen
Suite Teardown      Close EC

Test Tags           n1    composition    stream_oil_comp_analysis


*** Variables ***
${ORIGINAL_VALUE}       ${EMPTY}
${SENTINEL_VALUE}       0.2


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The 8-field navigator + GO renders the per-component grid; the target
    ...    component's wt% cell resolves and shows a value.
    [Tags]    smoke
    ${v}=    Read Component Wt Pct
    Should Not Be Empty    ${v}    msg=Methane wt% cell empty - grid did not load for the scope
    Capture Step    po0019_tc01_grid_loaded

TC02 Edit Wt Pct And Persist
    [Documentation]    Record the original wt%, edit Methane to a sentinel, Save, and confirm
    ...    persistence on-screen AND in DV_STRM_COMP_ANALYSIS.WT_PCT (COMPONENT_NO=C1). Also assert
    ...    Ethane (C2) is UNCHANGED -> Save persisted only the edited component (no normalize-on-save).
    [Tags]    edit
    ${orig}=    Read Component Wt Pct
    VAR    ${ORIGINAL_VALUE}    ${orig}    scope=SUITE
    Set Component Wt Pct    ${SENTINEL_VALUE}
    Save Composition
    Component Cell Should Show    ${SENTINEL_VALUE}
    Component Wt Pct Should Be In DB    ${SENTINEL_VALUE}
    Component Wt Pct Should Be In DB    ${GUARD_ORIGINAL_VALUE}    component_no=${GUARD_COMPONENT_NO}
    Capture Step    po0019_tc02_edited

TC03 Revert To Original (cleanup)
    [Documentation]    Restore the original wt% so the analysis is left exactly as found. Reload first
    ...    (post-commit re-render) so the revert edit re-arms Save.
    [Tags]    cleanup
    Reload And Find Target Component
    Set Component Wt Pct    ${ORIGINAL_VALUE}
    Save Composition
    Component Wt Pct Should Be In DB    ${ORIGINAL_VALUE}
    Capture Step    po0019_tc03_reverted
