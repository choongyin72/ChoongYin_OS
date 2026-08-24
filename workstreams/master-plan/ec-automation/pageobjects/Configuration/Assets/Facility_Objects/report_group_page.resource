*** Settings ***
Documentation       T3 (screen) — Report Group page object.
...                 Screen: Configuration > Assets > Facility Objects > Report Group (CO.0158).
...                 Manage-Object (OV) screen. Holds Report Group's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common). Plain OV (no
...                 mandatory cascade) — date-only navigator, GO populates the grid.
...                 Converted to the full Bank-pattern shape (2026-08-24): was previously a
...                 PARTIAL label-driven build (Fill OV Field By Label wrappers, but no
...                 properties-file-driven insert/update/verify and no explicit grid-filter
...                 wiring; test suite had 4 TCs / no Find, one shared Suite Setup login, unique
...                 timestamped test code). Now matches bank_page.resource/disposition_type_page
...                 .resource exactly: properties-file-driven insert/update/verify, explicit
...                 grid-filter wiring, fixed test code, per-TC Login/Logout, 5 TCs, PURE SCREEN
...                 verification (no inline DB-verify in the T3/test file).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${RG_SCREEN}          Report Group
${RG_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/report_group_insert.properties
${RG_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/report_group_update.properties
${RG_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/report_group_form_verify.properties
${RG_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/report_group_grid_verify.properties
# Grid id: Report Group's OWN datatable widget var — CONFIRMED live via the already-proven
# Python driver (py/report_group_iud.py GRID_DATA_ID) and the prior partial build's ${TBL}. NOT
# the shared ${OV_MANAGE_OBJECT_TABLE} constant (manage_object_nav_nav:form:T_data) that Bank/
# Disposition Type/County/Payment Term use — this screen's grid genuinely has its own
# screen-specific PrimeFaces id, confirmed by two independent prior builds (driver + T3), so it
# is kept as its own local constant rather than force-fit into the shared one.
${RG_TABLE}             report_group_table:form:T_data
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven — same documented precedent as Bank's own BANK_DEL_ENDDATE (the objectdates row
# packs TWO fields, Start Date C:1 / End Date C:3, a shape the one-field-per-row label scan
# cannot safely resolve).
${RG_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Report Group's own form-field label set (Start Date deliberately excluded — it lives only in
# objectForm/objectdates, not updateAttributes; Business Area deliberately excluded — it is a
# dropdown filled __FIRST__, which can re-render different display text after reload, matching
# the documented exclusion rule for every other __FIRST__-filled dropdown on this project, e.g.
# ec_code_object_page.resource's EC Code Type/EC Code). Labels are screen-prefixed ("Reporting
# Group Code"/"Reporting Group Name"), NOT the generic "Code"/"Name" Bank uses — confirmed live
# via the prior partial build's own Fill OV Field By Label usage.
@{RG_FORM_LABELS}    Reporting Group Code    Reporting Group Name    Description


*** Keywords ***
Find Report Group Row By Filter
    [Documentation]    Explicitly filter the Report Group grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) — matches
    ...    Bank's/Disposition Type's own explicit filter usage, rather than relying only on
    ...    Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${RG_TABLE}    ${code}

Clear Report Group Row Filter
    [Documentation]    Clear the Code column filter (see Find Report Group Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${RG_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Report Group's OWN credentials (${REPORT_GROUP_EC_USER}/
    ...    ${REPORT_GROUP_EC_PASS} from credentials.py) on the current page — works whether this
    ...    is the very first login (page freshly loaded on the login form via the shared T1 Open
    ...    EC Application) or a re-login after Logout From EC Application (same login form, not
    ...    a new page/tab). Screen-specific wrapper (matches Bank's convention:
    ...    report_group_iud.robot's test cases call this with ZERO arguments) that supplies
    ...    Report Group's own credential defaults to the shared T1 Login To EC Screen
    ...    (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${REPORT_GROUP_EC_USER}    ${REPORT_GROUP_EC_PASS}

Open Report Group Screen
    [Documentation]    Navigate to the Report Group screen, then click GO to populate the grid
    ...    (date-only navigator — no mandatory cascade). Assumes the caller already logged in
    ...    this test case (via Login To EC Application) — this keyword ONLY navigates, matching
    ...    Bank's per-TC Login/Open/action/Logout convention.
    Open EC Screen    ${RG_SCREEN}
    Apply Navigator

Insert Report Group Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Report Group From Properties,
    ...    purely so report_group_iud.robot's test case body reads as a plain business step with
    ...    ZERO arguments — the underlying mechanics (properties-file-driven insert) are
    ...    UNCHANGED. Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE}. The TC02 evidence screenshot is captured BEFORE Save is clicked (passed
    ...    through to Insert Object From Properties, which fills every field first).
    [Arguments]    ${properties_path}=${RG_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Reporting Group Code
    RETURN    ${code}

Verify Report Group Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification: row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By
    ...    Label) is compared to testdata/report_group_insert.properties (the file used to
    ...    insert, not the post-update report_group_form_verify.properties) — Reporting Group
    ...    Code, Reporting Group Name, Description (${RG_FORM_LABELS}). NOTE: Start Date and
    ...    Business Area are NOT verified here — Start Date is not an updateAttributes field
    ...    (matches Bank's own convention) and Business Area is a __FIRST__-filled dropdown
    ...    (excluded, same rule as every other __FIRST__ dropdown on this project). Delegates the
    ...    full sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Insert Exists. Filters via Find Report Group Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Report Group Row By Filter    ${code}
    Verify Object Insert Exists    ${RG_TABLE}    ${code}    Report Group
    ...    ${RG_INSERT_PROPERTIES}    @{RG_FORM_LABELS}    code_label=Reporting Group Code
    Clear Report Group Row Filter

Update Report Group Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the
    ...    applied {label: value} dict so the caller can DB-verify against exactly what was set.
    ...    The TC03 evidence screenshot is captured BEFORE Save is clicked (passed through to
    ...    Update Object From Properties, which fills every field first). Filters via Find
    ...    Report Group Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${RG_UPDATE_PROPERTIES}
    Find Report Group Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${RG_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Reporting Group Code
    Clear Report Group Row Filter
    RETURN    ${data}

Verify Report Group Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row (loading updateAttributes), then compares Reporting Group Name's LIVE
    ...    SCREEN value (via Get OV Field Value By Label) to testdata/report_group_update
    ...    .properties — only that one label, since that's the only field that file has.
    ...    Delegates the full sequence (select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Form Record. Filters via Find Report Group Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${RG_UPDATE_PROPERTIES}
    Find Report Group Row By Filter    ${code}
    Verify Object Form Record    ${RG_TABLE}    ${code}    Report Group    ${properties_path}
    ...    Reporting Group Name    code_label=Reporting Group Code
    Clear Report Group Row Filter

Find Report Group Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find Report Group Row By Filter first. Deliberately
    ...    does NOT clear the filter afterward — Verify Report Group Record Found (called right
    ...    after, same TC) needs the grid still filtered to ${code} for its own grid-check, since
    ...    it doesn't re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Report Group Row By Filter    ${code}
    Find Object Record    ${RG_TABLE}    ${code}    Report Group    code_label=Reporting Group Code

Verify Report Group Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data — the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find Report Group Record before this) AND left the Code filter active from
    ...    that same call — clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${RG_TABLE}    ${code}    ${RG_GRID_VERIFY_PROPERTIES}
    ...    ${RG_FORM_VERIFY_PROPERTIES}    @{RG_FORM_LABELS}
    Clear Report Group Row Filter

Delete Report Group Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the report group, set End Date = Start Date (true delete), Save. Captures the
    ...    TC05 evidence screenshot right after the End Date is filled but BEFORE Save is clicked
    ...    — showing the data as entered, not the after-save/reloaded-grid state. Filters via
    ...    Find Report Group Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Report Group Row By Filter    ${code}
    Delete Object Via End Date    ${RG_TABLE}    ${RG_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Report Group Row Filter

Verify Report Group Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database — the SAME two existing DB-ground-truth keywords,
    ...    just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${RG_TABLE}    OV_REPORT_GROUP    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Report Group Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${RG_TABLE}    ${code}
