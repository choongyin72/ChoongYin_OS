*** Settings ***
Documentation       T3 (screen) — Chemical Stream Hookup page object.
...                 Screen: Configuration > Assets > Chemical_Objects > Chemical Stream Hookup (CO.0260).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the mandatory
...                 3-level same-row cascade (Production Unit -> Area -> Facility Class 1) + GO.
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-26) - Chemical Stream Hookup remains OV-GM; the cascade+GO gesture is
...                 real and required, not something this conversion removed. Navigator fill now
...                 goes through the shared T2 "Apply Navigator From Properties"
...                 (resources/manage_object.resource), driven by
...                 testdata/chemical_stream_hookup_navigator.properties, whose 3 values were
...                 confirmed LIVE (2026-08-26, temporary probe reading back each column's actual
...                 first-available resolution) - not guessed, not copied from Well's own "P1 ..."
...                 scope (a different screen's proven value).
...                 Fields resolved BY LABEL (no hardcoded row/column ids); labels are SCREEN-PREFIXED
...                 ("Chemical Stream Hookup Code"/"Chemical Stream Hookup Name" - confirmed live via
...                 the pre-existing driver). No Op Production Unit field on this screen's objectForm
...                 (confirmed live: mand=False, not filled).
...                 KEEPS the standalone mandatory_field_gate.resource pre-flight check exactly as the
...                 prior OLD-pattern automation had it (owner instruction: this screen's mandatory-
...                 field gate requirement is NOT to be dropped or weakened by this structural
...                 conversion) - Insert/Update below inline Save And Refresh List's own GO-or-Refresh
...                 logic with the gate call inserted before Save, exactly as the pre-conversion
...                 automation did; manage_object.resource itself is NOT modified.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/mandatory_field_gate.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CSH_SCREEN}           Chemical Stream Hookup
${CSH_TABLE}             manageObject:form:T_data
# navigator (groupmodel): Production Unit -> Area -> Facility Class 1, 3-level same-row cascade
# (nav:form:G:0:R:1:C:1/C:2/C:3) + GO. Values below are kept only as documentation of the DOM ids
# (row 1, C:1/C:2/C:3) - the properties-driven fill (Apply Navigator From Properties) resolves to
# the same ids, not different ones.
${CSH_NAV_C1}           nav:form:G:0:R:1:C:1:dd
${CSH_NAV_C2}           nav:form:G:0:R:1:C:2:dd
${CSH_NAV_C3}           nav:form:G:0:R:1:C:3:dd
${CSH_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_stream_hookup_navigator.properties
${CSH_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_stream_hookup_insert.properties
${CSH_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_stream_hookup_update.properties
${CSH_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_stream_hookup_form_verify.properties
${CSH_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_stream_hookup_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's/Bank's own del-enddate constant. Value confirmed live via the
# pre-existing driver (py/chemical_stream_hookup_iud.py).
${CSH_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Chemical Stream Hookup's own form-field label set (Start Date deliberately excluded - it lives
# only in objectdates, not updateAttributes/objectForm's fill-once trio).
@{CSH_FORM_LABELS}    Chemical Stream Hookup Code    Chemical Stream Hookup Name


*** Keywords ***
Find Chemical Stream Hookup Row By Filter
    [Documentation]    Explicitly filter the Chemical Stream Hookup grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource),
    ...    matching every other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CSH_TABLE}    ${code}

Clear Chemical Stream Hookup Row Filter
    [Documentation]    Clear the Code column filter (see Find Chemical Stream Hookup Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${CSH_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Chemical Stream Hookup's OWN credentials
    ...    (${CHEMICAL_STREAM_HOOKUP_EC_USER}/${CHEMICAL_STREAM_HOOKUP_EC_PASS} from
    ...    credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${CHEMICAL_STREAM_HOOKUP_EC_USER}    ${CHEMICAL_STREAM_HOOKUP_EC_PASS}

Open Chemical Stream Hookup Screen With Navigator Values Populated
    [Documentation]    Navigate to the Chemical Stream Hookup screen, THEN fill + submit the
    ...    mandatory 3-level cascade navigator (dropdown x3 + GO) - the grid stays empty until
    ...    this happens, so this single keyword bundles both steps for the test case (one line
    ...    per TC). Assumes the caller already logged in this test case (via Login To EC
    ...    Application). Navigator fill delegates to the shared T2 "Apply Navigator From
    ...    Properties" (resources/manage_object.resource), driven by
    ...    testdata/chemical_stream_hookup_navigator.properties, instead of inlining
    ...    "Select EC Dropdown Option x3 + Apply Navigator" here - so any other OV-GM screen with
    ...    a same-row cascade can reuse the same shared keyword with its own properties file.
    Open EC Screen    ${CSH_SCREEN}
    Apply Navigator From Properties    ${CSH_NAVIGATOR_PROPERTIES}

Fill Object Form Fields And Save With Gate
    [Documentation]    Shared body for the Insert/Update wrappers below: fill EVERY field named
    ...    in ${properties_path} into ${form} (auto-detecting kind by label, same mechanism as
    ...    the shared T2 Insert/Update Object From Properties), capture the pre-save evidence
    ...    screenshot, GATE-CHECK for empty mandatory fields under ${scope_prefix} BEFORE Save
    ...    (owner instruction: keep this screen's mandatory-field gate exactly as-is), then Save
    ...    and reload via Apply Navigator (GO) or Refresh Screen - inlining Save And Refresh
    ...    List's own GO-or-Refresh logic with the gate call inserted before Save, exactly as the
    ...    pre-conversion automation did. manage_object.resource itself is NOT modified for this.
    ...    Extracted (2026-08-26) so neither caller exceeds the house keyword-length convention.
    [Arguments]    ${form}    ${properties_path}    ${scope_prefix}    ${action_label}
    ${data}=    Read Properties    ${properties_path}
    FOR    ${label}    IN    @{data.keys()}
        Fill OV Field By Label Any Kind    ${form}    ${label}    ${data}[${label}]
    END
    Capture Step    ${TEST NAME}_action
    Assert No Empty Mandatory Field    ${scope_prefix}    ${action_label}
    Save
    ${has_go}=    Get Element Count
    ...    css=button[id="button:form:B"]:visible, a[id="button:form:B"]:visible
    IF    ${has_go} > 0    Apply Navigator    ELSE    Refresh Screen
    RETURN    ${data}

Insert Chemical Stream Hookup Record And Save
    [Documentation]    Friendly-narrative wrapper: open the New Object form, fill + gate-check +
    ...    save via Fill Object Form Fields And Save With Gate. Also owns the integrity check
    ...    that the inserted Code matches the suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${CSH_INSERT_PROPERTIES}
    Open New Object Form
    ${data}=    Fill Object Form Fields And Save With Gate    objectForm    ${properties_path}
    ...    tab:tabPanel:objectForm:form    Save (insert)
    VAR    ${code}    ${data}[Chemical Stream Hookup Code]
    Should Be Equal    ${code}    ${TEST_CODE}
    ...    msg=${properties_path} Code does not match the expected ${TEST_CODE}
    RETURN    ${code}

Verify Chemical Stream Hookup Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Code/Name's LIVE SCREEN value is compared to
    ...    testdata/chemical_stream_hookup_insert.properties. Filters via Find Chemical Stream
    ...    Hookup Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Stream Hookup Row By Filter    ${code}
    Verify Object Insert Exists    ${CSH_TABLE}    ${code}    Chemical Stream Hookup
    ...    ${CSH_INSERT_PROPERTIES}    @{CSH_FORM_LABELS}    code_label=Chemical Stream Hookup Code
    Clear Chemical Stream Hookup Row Filter

Update Chemical Stream Hookup Record And Save
    [Documentation]    Friendly-narrative wrapper: select the row, verify row-identity (Code read
    ...    back BEFORE writing anything), then fill + gate-check + save via Fill Object Form
    ...    Fields And Save With Gate. Called with ZERO arguments (defaults ${code} to the suite's
    ...    ${TEST_CODE}). Filters via Find Chemical Stream Hookup Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CSH_UPDATE_PROPERTIES}
    Find Chemical Stream Hookup Row By Filter    ${code}
    Select Object Row    ${CSH_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Chemical Stream Hookup Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    ${data}=    Fill Object Form Fields And Save With Gate    updateAttributes    ${properties_path}
    ...    tab:tabPanel:updateAttributes:form    Save (update)
    Clear Chemical Stream Hookup Row Filter
    RETURN    ${data}

Verify Chemical Stream Hookup Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Name's LIVE SCREEN value to
    ...    testdata/chemical_stream_hookup_update.properties. Filters via Find Chemical Stream
    ...    Hookup Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Stream Hookup Row By Filter    ${code}
    Verify Object Form Record    ${CSH_TABLE}    ${code}    Chemical Stream Hookup
    ...    ${CSH_UPDATE_PROPERTIES}    Chemical Stream Hookup Name
    ...    code_label=Chemical Stream Hookup Code
    Clear Chemical Stream Hookup Row Filter

Find Chemical Stream Hookup Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Chemical
    ...    Stream Hookup Row By Filter first. Deliberately does NOT clear the filter afterward -
    ...    Verify Chemical Stream Hookup Record Found (called right after, same TC) needs the grid
    ...    still filtered to ${code} for its own grid-check; it clears the filter once both checks
    ...    are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Stream Hookup Row By Filter    ${code}
    Find Object Record    ${CSH_TABLE}    ${code}    Chemical Stream Hookup
    ...    code_label=Chemical Stream Hookup Code

Verify Chemical Stream Hookup Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Chemical Stream Hookup Record before this) AND left the Code
    ...    filter active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CSH_TABLE}    ${code}    ${CSH_GRID_VERIFY_PROPERTIES}
    ...    ${CSH_FORM_VERIFY_PROPERTIES}    @{CSH_FORM_LABELS}
    Clear Chemical Stream Hookup Row Filter

Delete Chemical Stream Hookup Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the object, set End Date = Start Date (EC true delete for
    ...    OV_CHEM_STRM_HOOKUP), Save. Filters via Find Chemical Stream Hookup Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Chemical Stream Hookup Row By Filter    ${code}
    Delete Object Via End Date    ${CSH_TABLE}    ${CSH_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Chemical Stream Hookup Row Filter

Verify Chemical Stream Hookup Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_CHEM_STRM_HOOKUP) - the DB check lives here, in
    ...    the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CSH_TABLE}    OV_CHEM_STRM_HOOKUP    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Chemical Stream Hookup Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CSH_TABLE}    ${code}
