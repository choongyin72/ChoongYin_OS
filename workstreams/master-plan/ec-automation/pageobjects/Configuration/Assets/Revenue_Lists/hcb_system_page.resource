*** Settings ***
Documentation       T3 (screen) — HCB System page object.
...                 Screen: Configuration > Assets > Revenue Lists > HCB System (CD.0097, OV_BALANCE).
...                 Manage-Object (OV) screen — Bank-pattern conversion (2026-08-25): property-file-driven
...                 + label-driven + T2-consolidated, replacing the older hand-rolled driver that used a
...                 generated timestamp code and called the raw DbVerify keywords (Field Should Equal In
...                 View / *Should Exist In DB) directly from the .robot file — a deviation from Bank's
...                 owner-requested 2026-08-18 PURE-SCREEN-verification convention (same deviation class
...                 fixed on Calculation Context/Document Template/Royalty Depositor/Stream Item Category,
...                 GitHub Issue #504 — HCB System was not swept by that issue because its page object
...                 didn't yet use Insert Object From Properties, so this build both converts AND removes
...                 the inline DB-verify calls in one pass).
...                 Live recon (2026-08-25) found this screen uses GENERIC "Code"/"Name" labels (same
...                 shape as Bank, not screen-prefixed) — no code_label override needed anywhere below.
...                 No mandatory navigator/date+GO cascade beyond the universal as-at-date filter bar
...                 every manage-object OV screen has.
...                 CORRECTS a stale claim in ec-ui-knowledge/screens/hcb_system.md ("optional dropdowns
...                 only, none mandatory"): a live MandatoryCellStyle scan of objectForm (2026-08-25)
...                 found FOUR mandatory fields — Code, Name, Start Date, AND the "HCB Category" dropdown
...                 (options confirmed live: "Operating area system" / "Single field system" /
...                 "Plant / terminal system" — "Operating area system" used here, matching the
...                 pre-existing driver's own choice). HCB Category is also present in updateAttributes
...                 (live scan, R7 on the pre-existing RHEA_WETGFAS record) so it round-trips through the
...                 full-form check in TC02/TC04 too. Description/Comments/Mass UOM/Volume UOM/Energy UOM
...                 are optional and deliberately NOT filled (no scope expansion).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${HCB_SCREEN}           HCB System
${HCB_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/hcb_system_insert.properties
${HCB_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/hcb_system_update.properties
${HCB_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/hcb_system_form_verify.properties
${HCB_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/hcb_system_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string.
${HCB_TABLE}            ${OV_MANAGE_OBJECT_TABLE}
# HCB System's own form-field label set for the full-form check (TC02/TC04, both read
# updateAttributes — see Verify Object Insert Exists/Verify Object Found in manage_object.resource).
# Start Date is deliberately EXCLUDED (matches Bank/Royalty Depositor's own exclusion) — it lives
# only in objectForm/objectdates, not updateAttributes (confirmed live 2026-08-25: updateAttributes
# fields are Code/Name/Description/Comments/Mass UOM/Volume UOM/Energy UOM/HCB Category — no date).
@{HCB_FORM_LABELS}      Code    Name    HCB Category


*** Keywords ***
Find HCB System Row By Filter
    [Documentation]    Explicitly filter the HCB System grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    Bank/Royalty Depositor's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${HCB_TABLE}    ${code}

Clear HCB System Row Filter
    [Documentation]    Clear the Code column filter (see Find HCB System Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${HCB_TABLE}

Login To EC Application
    [Documentation]    Authenticate as HCB System's OWN credentials (${HCB_SYSTEM_EC_USER}/
    ...    ${HCB_SYSTEM_EC_PASS} from credentials.py) on the current page — works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application. Screen-specific wrapper
    ...    (matches Bank's convention: every test case calls this with ZERO arguments) — the
    ...    actual login mechanics live in the shared T1 Login To EC Screen (common.resource);
    ...    kept here only because a shared file should not hardcode any screen's credentials.
    Login To EC Screen    ${HCB_SYSTEM_EC_USER}    ${HCB_SYSTEM_EC_PASS}

Open HCB System Screen
    [Documentation]    Navigate to the HCB System screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) — matches Bank's convention where each
    ...    test case gets its own explicit Login/Logout step. Delegates to the shared T1 Open EC
    ...    Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${HCB_SCREEN}

Insert HCB System Record And Save
    [Documentation]    Friendly-narrative wrapper (matches Bank's convention) around the shared
    ...    T2 Insert Object From Properties And Verify Code, so the test case body reads as a
    ...    plain business step with ZERO arguments. Also owns the integrity check that the
    ...    inserted Code matches the suite's ${TEST_CODE} — fails on its own if
    ...    testdata/hcb_system_insert.properties' Code ever drifts out of sync with the suite
    ...    variable. The TC02 evidence screenshot is captured BEFORE Save is clicked.
    [Arguments]    ${properties_path}=${HCB_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify HCB System Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check here — that is TC02's own separate DbVerify assertion): row exists in the
    ...    grid, then every field's LIVE SCREEN value is compared to
    ...    testdata/hcb_system_insert.properties — Code, Name, HCB Category (${HCB_FORM_LABELS}).
    ...    Start Date is NOT verified here (matches Bank/Royalty Depositor) — it only exists as a
    ...    grid column, not an updateAttributes form field. Delegates the full sequence to the
    ...    shared T2 Verify Object Insert Exists. Filters via Find HCB System Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find HCB System Row By Filter    ${code}
    Verify Object Insert Exists    ${HCB_TABLE}    ${code}    HCB System    ${HCB_INSERT_PROPERTIES}
    ...    @{HCB_FORM_LABELS}
    Clear HCB System Row Filter

Update HCB System Record And Save
    [Documentation]    Friendly-narrative wrapper (matches Bank's convention) around T2's Update
    ...    Object From Properties, called with ZERO arguments (defaults ${code} to the suite's
    ...    ${TEST_CODE}). Returns the applied {label: value} dict so the caller can DB-verify
    ...    against exactly what was set. The TC03 evidence screenshot is captured BEFORE Save is
    ...    clicked. Filters via Find HCB System Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${HCB_UPDATE_PROPERTIES}
    Find HCB System Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${HCB_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear HCB System Row Filter
    RETURN    ${data}

Verify HCB System Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check): selects the row (loading updateAttributes), then compares Name's LIVE
    ...    SCREEN value to testdata/hcb_system_update.properties — the only field that file has.
    ...    Delegates the full sequence to the shared T2 Verify Object Form Record. Filters via
    ...    Find HCB System Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find HCB System Row By Filter    ${code}
    Verify Object Form Record    ${HCB_TABLE}    ${code}    HCB System    ${HCB_UPDATE_PROPERTIES}
    ...    Name
    Clear HCB System Row Filter

Find HCB System Record
    [Documentation]    Friendly-narrative wrapper (matches Bank's convention) around the shared
    ...    T2 Find Object Record, called with ZERO arguments (defaults ${code} to the suite's
    ...    ${TEST_CODE}). Calls Find HCB System Row By Filter first. Deliberately does NOT clear
    ...    the filter afterward — Verify HCB System Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check.
    [Arguments]    ${code}=${TEST_CODE}
    Find HCB System Row By Filter    ${code}
    Find Object Record    ${HCB_TABLE}    ${code}    HCB System

Verify HCB System Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Delegates the full sequence to the
    ...    shared T2 Verify Object Found. Caller must already have selected the row (TC04 does,
    ...    via Find HCB System Record before this) AND left the Code filter active from that same
    ...    call — clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${HCB_TABLE}    ${code}    ${HCB_GRID_VERIFY_PROPERTIES}
    ...    ${HCB_FORM_VERIFY_PROPERTIES}    @{HCB_FORM_LABELS}
    Clear HCB System Row Filter

Delete HCB System Record And Save
    [Documentation]    Friendly-narrative wrapper (matches Bank's convention) around T2's Delete
    ...    Object Via End Date, called with ZERO arguments (defaults ${code}/${date} to the
    ...    suite's ${TEST_CODE}/${END_DATE}). Select the HCB System object, set End Date = Start
    ...    Date (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked. Filters via Find HCB System Row By Filter
    ...    first, clears after. End Date is resolved by LABEL (not hardcoded) — the pre-existing,
    ...    previously verify_screen.py-PASSED driver already proved this works on this screen
    ...    (no re-derivation needed).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find HCB System Row By Filter    ${code}
    Select Object Row    ${HCB_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Capture Step    ${TEST NAME}_action
    Save
    Apply Navigator
    Clear HCB System Row Filter

Verify HCB System Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (ov_balance). Also captures the TC05 evidence
    ...    screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${HCB_TABLE}    ov_balance    ${code}
    Capture Step    ${TEST NAME}_verify

Verify HCB System Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${HCB_TABLE}    ${code}
