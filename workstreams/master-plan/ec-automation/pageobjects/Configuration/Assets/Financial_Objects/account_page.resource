*** Settings ***
Documentation       T3 (screen) — Account page object.
...                 Screen: Configuration > Assets > Financial Objects > Account.
...                 Custom-URL OV screen (confirmed live 2026-08-22): grid id nav:form:T_data,
...                 NO GO button (manage_object_nav_ count=0, button:form:B count=0), reload via
...                 toolbar Refresh - T2's Save And Refresh List auto-detects this and falls back.
...                 Rebuilt 2026-08-22 to mirror Bank/State exactly (same batch as Cost Centre/
...                 Revenue Order/WBS) - replaces the older hardcoded-field-id pattern with the
...                 label-driven, properties-file-driven, T2-consolidated pattern.
...                 Grid is 110+ rows/6 pages (OV_FIN_ACCOUNT) - located via the Code column
...                 filter (grid_menu.resource's Filter/Clear Grid Text Column Filter, already
...                 proven live on Business Function), not page-walking. Owner-directed
...                 2026-08-22 after a page-walking fix already worked live: EC's grid filter
...                 re-queries the FULL dataset server-side in one call, confirmed live via
...                 tmp/recon_account_filter.robot - simpler and faster than looping pages.
...                 The filter mechanics were later PROMOTED into the shared T2
...                 resources/manage_object.resource (Find/Clear Object Row By Filter,
...                 2026-08-22) so any OV screen can reuse them - this T3's own Find/Clear
...                 Account Row By Filter are now thin wrappers around those.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${ACCOUNT_SCREEN}          Account
${ACCOUNT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/account_insert.properties
${ACCOUNT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/account_update.properties
${ACCOUNT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/account_form_verify.properties
${ACCOUNT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/account_grid_verify.properties
# Custom-URL OV grid id (NOT the manage-object constant - confirmed live 2026-08-22: no GO
# button, no manage_object_nav_ prefix - matches Cost Centre/Revenue Order/WBS's convention).
${ACCOUNT_TABLE}        nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date). Row layout confirmed live 2026-08-22
# (Start Date C:1 input present, End Date C:3 input present) - same framework-invariant shape
# documented on Bank/State (Start Date C:1, End Date label C:2, End Date input C:3).
${ACCOUNT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Account's own form-field label set (Start Date deliberately excluded - Insert-only, not
# present in updateAttributes). Includes the 2 confirmed-mandatory extras (MandatoryCellStyle
# CSS class, live-checked 2026-08-22 on both the New Object form and an existing real row):
# "Cost Object Type" (dropdown) and "GL Account" (text). Defined ONCE here so both Verify
# Account Record Exists (TC02, against account_insert.properties) and Verify Account Record
# Found (TC04, against account_form_verify.properties) share the same list.
@{ACCOUNT_FORM_LABELS}    Code    Name    Cost Object Type    GL Account


*** Keywords ***
Find Account Row By Filter
    [Documentation]    Filter the Account grid's Code column to ${code}, so the row is found
    ...    regardless of which of the 110+ rows/6 pages it would otherwise land on. Thin
    ...    zero-boilerplate wrapper around the shared T2 Find Object Row By Filter
    ...    (resources/manage_object.resource) - promoted there 2026-08-22 (owner: "the Find
    ...    Account Row By Filter, Clear Account Row Filter SF keywords step should move to
    ...    manage_object.resource so that all object similar to Account can utilise same filter
    ...    feature") from what was originally a T3-local fix here (added after a live TC03
    ...    failure 2026-08-22: OV_FIN_ACCOUNT has 110+ real rows on a 20-rows-per-page grid, and
    ...    a code starting with a letter, e.g. "AUTOTEST_ACCOUNT", sorts alphabetically AFTER
    ...    every existing numeric-string GL Code, landing on the LAST page). Kept as Account's
    ...    own named keyword (not called directly at each of the 7 use sites) so this T3's own
    ...    call sites/docs didn't need touching when the logic moved up to T2.
    [Arguments]    ${code}
    Find Object Row By Filter    ${ACCOUNT_TABLE}    ${code}

Clear Account Row Filter
    [Documentation]    Clear the Code column filter (see Find Account Row By Filter), restoring
    ...    the grid's normal unfiltered view. Thin wrapper around the shared T2 Clear Object Row
    ...    Filter (promoted 2026-08-22 alongside Find Account Row By Filter - see that keyword's
    ...    docs). Called after every keyword that filters, so the grid (and the sandbox user's
    ...    server-side filter personalisation - grid_menu.resource notes this is per-user, DB
    ...    CTRL_PERSONALISATION) is left clean for the next step or the next test run.
    Clear Object Row Filter    ${ACCOUNT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Account's OWN credentials (${ACCOUNT_EC_USER}/
    ...    ${ACCOUNT_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so account_iud.robot's test cases read as a plain business
    ...    step; supplies Account's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${ACCOUNT_EC_USER}    ${ACCOUNT_EC_PASS}

Open Account Screen
    [Documentation]    Navigate to the Account screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${ACCOUNT_SCREEN}

Insert Account Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so account_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/State. Fills every field in account_insert.properties, including
    ...    the 2 mandatory extras (Cost Object Type/GL Account) - auto-detected by kind.
    [Arguments]    ${properties_path}=${ACCOUNT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Account Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Code/Name/Cost Object
    ...    Type/GL Account - Start Date is grid/insert-only, not present in updateAttributes).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists. Calls Find Account Row By Filter first (the
    ...    grid is 110+ rows/6 pages - see that keyword's docs) so the row-check/select land on
    ...    the one filtered row holding ${code}, then clears the filter afterward.
    [Arguments]    ${code}=${TEST_CODE}
    Find Account Row By Filter    ${code}
    Verify Object Insert Exists    ${ACCOUNT_TABLE}    ${code}    Account    ${ACCOUNT_INSERT_PROPERTIES}
    ...    @{ACCOUNT_FORM_LABELS}
    Clear Account Row Filter

Update Account Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State.
    ...    Calls Find Account Row By Filter first (see that keyword's docs - 110+ rows/6 pages),
    ...    then clears the filter afterward.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${ACCOUNT_UPDATE_PROPERTIES}
    Find Account Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${ACCOUNT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear Account Row Filter
    RETURN    ${data}

Verify Account Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State's TC03 convention: the form shows the updated
    ...    Name (the only field account_update.properties lists). Delegates the full sequence
    ...    (select, form-compare, screenshot) to the shared T2 Verify Object Form Record. Calls
    ...    Find Account Row By Filter first (Save And Refresh List's Refresh resets the grid to
    ...    page 1, off ${code}'s page again - see that keyword's docs), then clears the filter
    ...    afterward.
    [Arguments]    ${code}=${TEST_CODE}
    Find Account Row By Filter    ${code}
    Verify Object Form Record    ${ACCOUNT_TABLE}    ${code}    Account    ${ACCOUNT_UPDATE_PROPERTIES}
    ...    Name
    Clear Account Row Filter

Find Account Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Account Row By Filter first
    ...    (fresh TC04 navigation defaults back to page 1 - see that keyword's docs). Deliberately
    ...    does NOT clear the filter afterward - Verify Account Record Found (called right after,
    ...    same TC) needs the grid still filtered to ${code} for its own grid-check, since it
    ...    doesn't re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Account Row By Filter    ${code}
    Find Object Record    ${ACCOUNT_TABLE}    ${code}    Account

Verify Account Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Account Record before this) AND left the Code filter active from that same call (the
    ...    grid-check here still needs ${code}'s row visible - see Find Account Record's docs) -
    ...    this keyword clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${ACCOUNT_TABLE}    ${code}    ${ACCOUNT_GRID_VERIFY_PROPERTIES}
    ...    ${ACCOUNT_FORM_VERIFY_PROPERTIES}    @{ACCOUNT_FORM_LABELS}
    Clear Account Row Filter

Delete Account Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the account, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/State's convention. Calls Find
    ...    Account Row By Filter first (fresh TC05 navigation defaults back to page 1 - see that
    ...    keyword's docs), then clears the filter afterward.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Account Row By Filter    ${code}
    Delete Object Via End Date    ${ACCOUNT_TABLE}    ${ACCOUNT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Account Row Filter

Verify Account Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid (filtered by Code = ${code} via Find Account Row By
    ...    Filter - the 110+ row/6-page grid means an unfiltered current-page-only check could
    ...    miss a leftover row on a later page, see that keyword's docs) and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Find Account Row By Filter    ${code}
    Verify Object Removed    ${ACCOUNT_TABLE}    OV_FIN_ACCOUNT    ${code}
    Clear Account Row Filter
    Capture Step    ${TEST NAME}_verify

Verify Account Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Filters the grid
    ...    to Code = ${code} first via Find Account Row By Filter (the 110+ row/6-page grid, see
    ...    that keyword's docs - a leftover row from a prior failed run could otherwise sit
    ...    unseen on a later page while page 1 looks clean), then delegates the standard check +
    ...    screenshot to the shared T2 Verify Object Does Not Exist, and clears the filter after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Account Row By Filter    ${code}
    Verify Object Does Not Exist    ${ACCOUNT_TABLE}    ${code}
    Clear Account Row Filter
