*** Settings ***
Documentation       T3 (screen) — VAT Code page object.
...                 Screen: Configuration > Assets > Financial Objects > VAT Code.
...                 Manage-Object (OV) screen (navigator = manage-object, standard GO button,
...                 grid manage_object_nav_nav:form:T_data - registry-confirmed, not re-verified
...                 this session per the batch-2 shared findings doc). Rebuilt 2026-08-23 to
...                 mirror Bank/Account exactly (same batch as Country/County/Regulatory
...                 Permits/Currency) - replaces the older hardcoded-field-id pattern with the
...                 label-driven, properties-file-driven, T2-consolidated pattern.
...                 Live-confirmed 2026-08-23 (tmp/recon_vat_code_new_object_form.py +
...                 tmp/recon_vat_code_mandatory_check.py + tmp/recon_vat_code_update_form.py -
...                 deleted before final commit): registry's "(dds: Country, VAT Type; dates at
...                 R1/R2!)" note is CONFIRMED - the objectForm (Insert) has Start Date at R1 and
...                 End Date at R2 (both present in Insert, unlike Bank/Account where only Start
...                 Date is Insert-side) - this is fine, since every field here is resolved by
...                 LABEL, not by hardcoded row/column position, so the unusual row order needs
...                 no special handling. TWO mandatory reference dropdowns beyond Code/Name/Start
...                 Date, confirmed via raw outerHTML dump ({mandatory:true} MandatoryCellStyle
...                 on the wrapping <span class="...dd"> element, NOT on the dd_input/dd_hinput
...                 <input> children - the generic per-input MandatoryCellStyle check the recon
...                 script started with silently returned False for both dropdowns until the
...                 span itself was inspected instead): "Country" (17 real catalogued options:
...                 Any/Argentina/Australia/Bolivia/Canada/China/Denmark/Germany/Great Britain/
...                 Hong Kong/Italy/MHM13_Norway/Norway/Spain/Sweden/The Netherlands/USA) and
...                 "VAT Type" (2 real options: Income/Cost). Both use the literal first-option
...                 text ("Any"/"Country" -> "Any", "VAT Type" -> "Income") in the properties
...                 files, NOT the __FIRST__ placeholder - live-confirmed 2026-08-23 that TC02's
...                 Verify VAT Code Record Exists compares the live screen back against the SAME
...                 insert properties file (T2's Verify Object Insert Exists), so __FIRST__ would
...                 never match the resolved option text there (see vat_code_insert.properties'
...                 own header for the exact failure this fix corrects). A third mandatory text
...                 field, "VAT Code" (distinct from the object's own "Code" identifier), plus
...                 mandatory "Rate (Decimal)" - also confirmed via the same outerHTML dump.
...                 Grid is single-page/15 rows today (OV_VAT_CODE) - Find/Clear VAT Code Row By
...                 Filter wired in from the start per the batch-2 shared findings doc, matching
...                 Bank/Account's own filter-wiring convention, so this stays correct if the
...                 grid ever grows past one page.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${VAT_CODE_SCREEN}          VAT Code
${VAT_CODE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/vat_code_insert.properties
${VAT_CODE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/vat_code_update.properties
${VAT_CODE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/vat_code_form_verify.properties
${VAT_CODE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/vat_code_grid_verify.properties
# Grid id: reuse T2's centralized constant (plain manage-object OV, registry-confirmed).
${VAT_CODE_TABLE}       ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Framework-invariant shape already
# documented/proven on Bank/Account (Start Date C:1, End Date label C:2, End Date input C:3) -
# not re-verified this session per the batch-2 shared findings doc (recon budget spent on the
# field-level facts instead).
${VAT_CODE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# VAT Code's own form-field label set (Start Date/End Date deliberately excluded - both are
# objectForm/Insert-only, confirmed absent from updateAttributes via a live scan). Defined ONCE
# here so both Verify VAT Code Record Exists (TC02, against vat_code_insert.properties) and
# Verify VAT Code Record Found (TC04, against vat_code_form_verify.properties) share the same
# list. Only the fields this suite actually SETS are checked (IUD-fill-only-needed-fields
# convention) - Rate (%)/Legal Text/Comments/Country Validation are left at their EC defaults
# and are not part of this suite's data, so they are not verified either.
@{VAT_CODE_FORM_LABELS}    Code    VAT Code    Country    VAT Type    Name    Rate (Decimal)


*** Keywords ***
Find VAT Code Row By Filter
    [Documentation]    Filter the VAT Code grid's Code column to ${code}, matching Bank/Account's
    ...    own explicit filter usage (batch-2 shared findings doc: wire the filter in from the
    ...    start, not as a follow-up). Thin wrapper around the shared T2 Find Object Row By
    ...    Filter (resources/manage_object.resource). The grid is single-page/15 rows today, so
    ...    this narrows to exactly 1 row immediately either way - explicit here so this screen
    ...    stays correct if OV_VAT_CODE ever grows past one page.
    [Arguments]    ${code}
    Find Object Row By Filter    ${VAT_CODE_TABLE}    ${code}

Clear VAT Code Row Filter
    [Documentation]    Clear the Code column filter (see Find VAT Code Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${VAT_CODE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as VAT Code's OWN credentials (${VAT_CODE_EC_USER}/
    ...    ${VAT_CODE_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so vat_code_iud.robot's test cases read as a plain business
    ...    step; supplies VAT Code's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${VAT_CODE_EC_USER}    ${VAT_CODE_EC_PASS}

Open VAT Code Screen
    [Documentation]    Navigate to the VAT Code screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${VAT_CODE_SCREEN}

Insert VAT Code Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so vat_code_iud.robot's test case body reads as a plain business step
    ...    with ZERO arguments. Also checks the inserted Code matches the suite's ${TEST_CODE}.
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Account.
    ...    Fills every field in vat_code_insert.properties, including the mandatory extras
    ...    (VAT Code/Country/VAT Type/Rate (Decimal)) - auto-detected by kind, including the two
    ...    reference dropdowns via __FIRST__.
    [Arguments]    ${properties_path}=${VAT_CODE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify VAT Code Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check here, matching Bank/Account's TC02 convention): row exists in the grid, then
    ...    the form shows what was just inserted (${VAT_CODE_FORM_LABELS} - Start Date is
    ...    objectForm/insert-only, not present in updateAttributes). Delegates the full sequence
    ...    (row-check, select, form-compare, screenshot) to the shared T2 Verify Object Insert
    ...    Exists. Calls Find VAT Code Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find VAT Code Row By Filter    ${code}
    Verify Object Insert Exists    ${VAT_CODE_TABLE}    ${code}    VAT Code    ${VAT_CODE_INSERT_PROPERTIES}
    ...    @{VAT_CODE_FORM_LABELS}
    Clear VAT Code Row Filter

Update VAT Code Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Pre-save
    ...    evidence screenshot captured before Save is clicked, matching Bank/Account. Calls
    ...    Find VAT Code Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${VAT_CODE_UPDATE_PROPERTIES}
    Find VAT Code Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${VAT_CODE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear VAT Code Row Filter
    RETURN    ${data}

Verify VAT Code Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification,
    ...    matching Bank/Account's TC03 convention: the form shows the updated Name (the only
    ...    field vat_code_update.properties lists). Delegates the full sequence (select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Form Record. Calls Find VAT
    ...    Code Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find VAT Code Row By Filter    ${code}
    Verify Object Form Record    ${VAT_CODE_TABLE}    ${code}    VAT Code    ${VAT_CODE_UPDATE_PROPERTIES}
    ...    Name
    Clear VAT Code Row Filter

Find VAT Code Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find VAT Code Row By Filter first. Deliberately does NOT
    ...    clear the filter afterward - Verify VAT Code Record Found (called right after, same
    ...    TC) needs the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find VAT Code Row By Filter    ${code}
    Find Object Record    ${VAT_CODE_TABLE}    ${code}    VAT Code

Verify VAT Code Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the form record match the expected (post-update) data. Delegates the full sequence
    ...    (grid-compare, form-compare, screenshot) to the shared T2 Verify Object Found. Caller
    ...    must already have selected the row (TC04 does, via Find VAT Code Record before this)
    ...    AND left the Code filter active from that same call - this keyword clears the filter
    ...    itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${VAT_CODE_TABLE}    ${code}    ${VAT_CODE_GRID_VERIFY_PROPERTIES}
    ...    ${VAT_CODE_FORM_VERIFY_PROPERTIES}    @{VAT_CODE_FORM_LABELS}
    Clear VAT Code Row Filter

Delete VAT Code Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the vat code, set End Date = Start Date (true delete), Save. Captures the TC05
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked,
    ...    matching Bank/Account's convention. Calls Find VAT Code Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find VAT Code Row By Filter    ${code}
    Delete Object Via End Date    ${VAT_CODE_TABLE}    ${VAT_CODE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear VAT Code Row Filter

Verify VAT Code Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid (filtered by Code = ${code} via Find VAT Code Row By Filter) and the
    ...    database.
    [Arguments]    ${code}=${TEST_CODE}
    Find VAT Code Row By Filter    ${code}
    Verify Object Removed    ${VAT_CODE_TABLE}    OV_VAT_CODE    ${code}
    Clear VAT Code Row Filter
    Capture Step    ${TEST NAME}_verify

Verify VAT Code Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Filters the grid to
    ...    Code = ${code} first via Find VAT Code Row By Filter, then delegates the standard
    ...    check + screenshot to the shared T2 Verify Object Does Not Exist, and clears the
    ...    filter after.
    [Arguments]    ${code}=${TEST_CODE}
    Find VAT Code Row By Filter    ${code}
    Verify Object Does Not Exist    ${VAT_CODE_TABLE}    ${code}
    Clear VAT Code Row Filter
