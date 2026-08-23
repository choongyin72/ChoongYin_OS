*** Settings ***
Documentation       T3 (screen) — Canal page object.
...                 Screen: Configuration > Assets > Transport Objects > Canal (CO.2069).
...                 Manage-Object (OV) screen. Holds Canal's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Brought up to full Bank-pattern shape (Batch 7, 2026-08-23): properties-file-
...                 driven insert/update/verify + explicit grid-filter wiring, replacing the prior
...                 argument-driven keywords (Insert Canal Record/Update Canal Name/Delete Canal).
...                 Mandatory fields (live-confirmed via docs/ec_screen_registry.md +
...                 screens/.../Canal/canal_sow.md + the already-proven py/canal_iud.py driver,
...                 7/7 live): Canal Code / Canal Name / Start Date. Time Zone dropdown is
...                 documented optional and deliberately skipped (matches the proven driver).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CANAL_SCREEN}          Canal
${CANAL_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/canal_insert.properties
${CANAL_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/canal_update.properties
${CANAL_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/canal_form_verify.properties
${CANAL_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/canal_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string.
${CANAL_TABLE}          ${OV_MANAGE_OBJECT_TABLE}
# objectdates field id (Delete - End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented shape as Bank's/Customer's own ${BANK_DEL_ENDDATE}/${CUSTOMER_DEL_ENDDATE} (the
# row packs TWO fields: Start Date C:1, End Date label C:2, End Date field C:3). Confirmed live via
# the source of Canal's already-proven Playwright driver (py/ec_object_iud.py END_DATE_ID, the
# SAME default value Canal's own driver uses unmodified, 7/7 live) - not a guess ported from Bank.
${CANAL_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Canal's own form-field label set. Labels are "Canal Code"/"Canal Name" (screen-prefixed) - live-
# confirmed via the already-proven Playwright driver (py/canal_iud.py INSERT_FIELDS), same shape as
# State's own "State Code"/"State Name" (2026-08-22 precedent: NOT a universal Bank-family "Code"/
# "Name" convention). Start Date deliberately excluded from updateAttributes - it lives only in
# objectdates, matching Bank's own confirmed shape. Defined ONCE here so both Verify Canal Record
# Exists (TC02, against canal_insert.properties) and Verify Canal Record Found (TC04, against
# canal_form_verify.properties) share the same list.
@{CANAL_FORM_LABELS}    Canal Code    Canal Name


*** Keywords ***
Find Canal Row By Filter
    [Documentation]    Explicitly filter the Canal grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource) - matches Bank/Account's
    ...    own explicit filter usage. Canal's grid is small (2 real rows: SUEZ/PANAMA) so this
    ...    narrows to exactly 1 row immediately either way - explicit here for consistency and to
    ...    keep this screen future-proof if its grid ever grows.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CANAL_TABLE}    ${code}

Clear Canal Row Filter
    [Documentation]    Clear the Code column filter (see Find Canal Row By Filter) via the shared
    ...    T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CANAL_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Canal's OWN credentials (${CANAL_EC_USER}/${CANAL_EC_PASS}
    ...    from credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    ...    Screen-specific wrapper (matches Bank's shape: canal_iud.robot's test cases call this
    ...    with ZERO arguments) that supplies Canal's own credential defaults to the shared T1
    ...    Login To EC Screen (common.resource), which owns the actual login mechanics - kept here
    ...    only because a shared file should not hardcode any screen's credentials.
    Login To EC Screen    ${CANAL_EC_USER}    ${CANAL_EC_PASS}

Open Canal Screen
    [Documentation]    Navigate to the Canal screen. Assumes the caller already logged in this
    ...    test case (via Login To EC Application) - this keyword ONLY navigates, matching Bank's
    ...    shape (every test case gets its own explicit Login/Logout step instead of one shared
    ...    Suite Setup/Teardown login). Delegates to the shared T1 Open EC Screen (common.resource)
    ...    for the actual mechanics.
    Open EC Screen    ${CANAL_SCREEN}

Insert Canal Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, purely so canal_iud.robot's test case body reads as a plain business step with
    ...    ZERO arguments - the underlying mechanics (properties-file-driven insert) are UNCHANGED.
    ...    Also owns the integrity check that the inserted Code matches the suite's ${TEST_CODE} -
    ...    this keyword fails on its own if testdata/canal_insert.properties' Code ever drifts out
    ...    of sync with the suite variable, instead of the test case asserting it separately. The
    ...    TC02 evidence screenshot is captured BEFORE Save is clicked (passed through to Insert
    ...    Object From Properties, which fills every field first).
    [Arguments]    ${properties_path}=${CANAL_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Canal Code
    RETURN    ${code}

Verify Canal Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here, matching Bank's shape): row exists in the grid, then every field's LIVE
    ...    SCREEN value (via Get OV Field Value By Label) is compared to
    ...    testdata/canal_insert.properties (the file used to insert, not the post-update
    ...    canal_form_verify.properties) - Code, Name (${CANAL_FORM_LABELS}). Start Date is NOT
    ...    verified here - it only exists as a grid column, not a form field (matches Bank's shape).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the shared
    ...    T2 Verify Object Insert Exists. Filters via Find Canal Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Canal Row By Filter    ${code}
    Verify Object Insert Exists    ${CANAL_TABLE}    ${code}    Canal    ${CANAL_INSERT_PROPERTIES}
    ...    @{CANAL_FORM_LABELS}    code_label=Canal Code
    Clear Canal Row Filter

Update Canal Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the applied
    ...    {label: value} dict so the caller can DB-verify against exactly what was set. The TC03
    ...    evidence screenshot is captured BEFORE Save is clicked (passed through to Update Object
    ...    From Properties, which fills every field first). Filters via Find Canal Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CANAL_UPDATE_PROPERTIES}
    Find Canal Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CANAL_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Canal Code
    Clear Canal Row Filter
    RETURN    ${data}

Verify Canal Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check): selects the row (loading updateAttributes), then compares Name's LIVE SCREEN
    ...    value (via Get OV Field Value By Label) to testdata/canal_update.properties - the only
    ...    field that file has (unlike the default canal_form_verify.properties/
    ...    ${CANAL_FORM_LABELS}, which has the full field set). Delegates the full sequence
    ...    (select, form-compare, screenshot) to the shared T2 Verify Object Form Record. Filters
    ...    via Find Canal Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Canal Row By Filter    ${code}
    Verify Object Form Record    ${CANAL_TABLE}    ${code}    Canal    ${CANAL_UPDATE_PROPERTIES}
    ...    Canal Name    code_label=Canal Code
    Clear Canal Row Filter

Find Canal Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find Canal Row By Filter first. Deliberately does NOT
    ...    clear the filter afterward - Verify Canal Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Canal Row By Filter    ${code}
    Find Object Record    ${CANAL_TABLE}    ${code}    Canal    code_label=Canal Code

Verify Canal Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND the
    ...    full form record match the expected data - the SAME two existing live-DOM round-trip
    ...    keywords, just called under one name. Also captures the TC04 evidence screenshot.
    ...    Delegates the full sequence (grid-compare, form-compare, screenshot) to the shared T2
    ...    Verify Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Canal Record before this) AND left the Code filter active from that same call - clears
    ...    the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CANAL_TABLE}    ${code}    ${CANAL_GRID_VERIFY_PROPERTIES}
    ...    ${CANAL_FORM_VERIFY_PROPERTIES}    @{CANAL_FORM_LABELS}
    Clear Canal Row Filter

Delete Canal Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the canal, set End Date = Start Date (true delete), Save. Captures the TC05
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked -
    ...    showing the data as entered, not the after-save/reloaded-grid state. Calls T2 directly
    ...    (no middle "Delete Canal" alias, matching Bank's single-hop shape). Filters via
    ...    Find Canal Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Canal Row By Filter    ${code}
    Delete Object Via End Date    ${CANAL_TABLE}    ${CANAL_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Canal Row Filter

Verify Canal Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database - the SAME two existing DB-ground-truth keywords,
    ...    just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CANAL_TABLE}    ov_canal    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Canal Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CANAL_TABLE}    ${code}
