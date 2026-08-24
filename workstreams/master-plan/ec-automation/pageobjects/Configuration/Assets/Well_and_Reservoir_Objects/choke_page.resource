*** Settings ***
Documentation       T3 (screen) — Choke page object.
...                 Screen: Configuration > Assets > Well and Reservoir Objects > Choke (CO.0185).
...                 Manage-Object (OV, date-effective) screen. Holds Choke's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Navigator is a single Date field (mandatory=False, confirmed live via
...                 tmp/scripts/scan_ec_screen.py 2026-08-25) + GO — the grid AUTO-LOADS on
...                 screen open (real seed data "P1 C001" visible BEFORE any GO click, unchanged
...                 after GO, confirmed live via a dedicated row-count recon), the SAME shape as
...                 Bank/Choke Model/Document Date Term — NOT a genuine mandatory-date gate.
...                 Corrects docs/bank-pattern-conversion-checklist.md's stale "Excluded" table
...                 entry ("Document Date Term, Payment Term, Choke, Choke Model | Mandatory
...                 single date + GO before grid loads") for Choke specifically — the LAST
...                 unverified member of that original 5-screen group (Disposition Type/Payment
...                 Term/Document Date Term/Choke Model already individually re-verified).
...                 Labels are SCREEN-PREFIXED ("Choke Code"/"Choke Name"), confirmed live via a
...                 fresh objectForm field-inventory scan 2026-08-25 (scan_ec_screen.py) —
...                 matches Choke Model/Disposition Type's screen-prefixed style.
...                 Converted to the full Bank-pattern shape (2026-08-25): was previously an OLD
...                 hardcoded-field-id build (Fill EC Field with raw R:n:C:n ids, a generated
...                 unique AUTOTEST_CHK_<timestamp> code, one shared Suite Setup login, inline
...                 DB-verify calls in the test file, only 4 TCs/no Find). Now matches
...                 bank_page.resource/choke_model_page.resource/disposition_type_page.resource
...                 exactly: properties-file-driven insert/update/verify, explicit grid-filter
...                 wiring, fixed test code, per-TC Login/Logout, 5 TCs, PURE SCREEN verification
...                 (no inline DB-verify in the T3/test file).
...                 DELETE = End Date = Start Date (true delete; row leaves OV_CHOKE). Grid has
...                 real seed data ("P1 C001") — strict AUTOTEST_ prefix, never touch it.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CHOKE_SCREEN}         Choke
${CHOKE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/choke_insert.properties
${CHOKE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/choke_update.properties
${CHOKE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/choke_form_verify.properties
${CHOKE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/choke_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string
# (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${CHOKE_TABLE}          ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven — same documented precedent as Bank's own BANK_DEL_ENDDATE/Choke Model's own
# CHKM_DEL_ENDDATE (the objectdates row packs TWO fields, Start Date C:1 / End Date C:3, a shape
# the one-field-per-row label scan cannot safely resolve). Reused unchanged from the prior
# OLD-pattern build (already live-confirmed working).
${CHOKE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Choke's own form-field label set (Start Date deliberately excluded — it lives only in
# objectForm/objectdates, not updateAttributes, same exclusion Bank/Choke Model/Disposition Type
# document for their own Start Date). Defined ONCE here so both Verify Choke Record Exists
# (TC02) and Verify Choke Record Found (TC04) share the same list.
@{CHOKE_FORM_LABELS}    Choke Code    Choke Name    Comments


*** Keywords ***
Find Choke Row By Filter
    [Documentation]    Explicitly filter the Choke grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource) — matches Bank's/
    ...    Choke Model's own explicit filter usage, rather than relying only on Select Object
    ...    Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CHOKE_TABLE}    ${code}

Clear Choke Row Filter
    [Documentation]    Clear the Code column filter (see Find Choke Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CHOKE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Choke's OWN credentials (${CHOKE_EC_USER}/${CHOKE_EC_PASS}
    ...    from credentials.py) on the current page — works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    ...    Screen-specific wrapper (matches Bank's convention: choke_iud.robot's test cases call
    ...    this with ZERO arguments) that supplies Choke's own credential defaults to the shared
    ...    T1 Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${CHOKE_EC_USER}    ${CHOKE_EC_PASS}

Open Choke Screen
    [Documentation]    Navigate to the Choke screen. Assumes the caller already logged in this
    ...    test case (via Login To EC Application) — this keyword ONLY navigates, matching
    ...    Bank's per-TC Login/Open/action/Logout convention. Deliberately does NOT call Apply
    ...    Navigator — the grid auto-populates on open (confirmed live: real seed data visible
    ...    BEFORE any GO click, unchanged after GO — same as Bank/Choke Model).
    Open EC Screen    ${CHOKE_SCREEN}

Insert Choke Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And
    ...    Verify Code, purely so choke_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments — the underlying mechanics (properties-file-driven insert)
    ...    are UNCHANGED. Also owns the integrity check that the inserted Code matches the
    ...    suite's ${TEST_CODE}. The TC02 evidence screenshot is captured BEFORE Save is clicked
    ...    (passed through to Insert Object From Properties, which fills every field first).
    [Arguments]    ${properties_path}=${CHOKE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Choke Code
    RETURN    ${code}

Verify Choke Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification: row exists in the grid, then every field's LIVE SCREEN value (via Get
    ...    OV Field Value By Label) is compared to testdata/choke_insert.properties (the file
    ...    used to insert, not the post-update choke_form_verify.properties) — Choke Code, Choke
    ...    Name (${CHOKE_FORM_LABELS} minus Comments, which does not exist yet at insert time —
    ...    Verify Object Form Fields From Properties only checks keys present in the properties
    ...    file, so passing the insert file naturally limits the check to Code/Name). NOTE: Start
    ...    Date is NOT verified here — it only exists as a grid column / objectForm/objectdates
    ...    field, not an updateAttributes field (matches Bank's own convention). Delegates the
    ...    full sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Insert Exists. Filters via Find Choke Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Choke Row By Filter    ${code}
    Verify Object Insert Exists    ${CHOKE_TABLE}    ${code}    Choke
    ...    ${CHOKE_INSERT_PROPERTIES}    Choke Code    Choke Name
    ...    code_label=Choke Code
    Clear Choke Row Filter

Update Choke Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. The TC03 evidence screenshot is captured BEFORE Save is clicked (passed through
    ...    to Update Object From Properties, which fills every field first). Filters via Find
    ...    Choke Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CHOKE_UPDATE_PROPERTIES}
    Find Choke Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CHOKE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Choke Code
    Clear Choke Row Filter
    RETURN    ${data}

Verify Choke Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification: selects the row (loading updateAttributes), then compares Choke Name/
    ...    Comments' LIVE SCREEN values (via Get OV Field Value By Label) to
    ...    testdata/choke_update.properties. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find Choke Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Choke Row By Filter    ${code}
    Verify Object Form Record    ${CHOKE_TABLE}    ${code}    Choke
    ...    ${CHOKE_UPDATE_PROPERTIES}    Choke Name    Comments
    ...    code_label=Choke Code
    Clear Choke Row Filter

Find Choke Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find Choke Row By Filter first. Deliberately
    ...    does NOT clear the filter afterward — Verify Choke Record Found (called right after,
    ...    same TC) needs the grid still filtered to ${code} for its own grid-check, since it
    ...    doesn't re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Choke Row By Filter    ${code}
    Find Object Record    ${CHOKE_TABLE}    ${code}    Choke    code_label=Choke Code

Verify Choke Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data — the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find Choke Record before this) AND left the Code filter active from that
    ...    same call — clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CHOKE_TABLE}    ${code}    ${CHOKE_GRID_VERIFY_PROPERTIES}
    ...    ${CHOKE_FORM_VERIFY_PROPERTIES}    @{CHOKE_FORM_LABELS}
    Clear Choke Row Filter

Delete Choke Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the choke, set End Date = Start Date (true delete), Save. Captures the TC05
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked —
    ...    showing the data as entered, not the after-save/reloaded-grid state. Filters via Find
    ...    Choke Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Choke Row By Filter    ${code}
    Delete Object Via End Date    ${CHOKE_TABLE}    ${CHOKE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Choke Row Filter

Verify Choke Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database — the SAME two existing DB-ground-truth keywords,
    ...    just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CHOKE_TABLE}    OV_CHOKE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Choke Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CHOKE_TABLE}    ${code}
