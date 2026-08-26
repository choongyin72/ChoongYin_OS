*** Settings ***
Documentation       T3 (screen) — Pipeline Segment page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Pipeline Segment
...                 (OV_PIPELINE_SEGMENT). OV-GM (BU-gated): the grid (manageObject:form:T_data)
...                 loads ONLY after a Business Unit is picked in the navigator + GO.
...                 Converted to the full Area-pattern STRUCTURE (owner standing rule 2026-08-26:
...                 any EC screen with a navigator matching Area's layout MUST follow Area's FULL
...                 pattern). Pipeline Segment's navigator was re-confirmed live (2026-08-26): a
...                 single mandatory Business Unit dropdown at nav:form:G:0:R:1:C:1:dd - the SAME
...                 single-dropdown shape as Area's own Production Unit navigator / Meter's own
...                 Business Unit navigator. A second dropdown at nav:form:G:0:R:1:C:2:dd
...                 (labelled "Pipeline", an optional grid filter) exists but is NOT mandatory
...                 (mandatory:false, confirmed live) - GO succeeds with only C:1 filled. This
...                 conversion is structural only - the genuine BU navigator gesture and the
...                 genuine mandatory "Pipeline Name" dropdown on the insert form are both kept
...                 exactly as they behave.
...                 Field labels confirmed live (2026-08-26): objectForm/updateAttributes use
...                 SCREEN-PREFIXED "Pipeline Segment Code"/"Pipeline Segment Name" (like Area's
...                 "Area Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use -
...                 every T2 call below passes code_label=Pipeline Segment Code accordingly.
...                 DELETE = End Date = Start Date (true delete in OV_PIPELINE_SEGMENT).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PIPESEG_SCREEN}          Pipeline Segment
${PIPESEG_TABLE}            manageObject:form:T_data
# navigator (OV-GM): Business Unit dropdown — MANDATORY before the grid loads. The fill itself
# now goes through the shared T2 "Apply Navigator From Properties" (resources/manage_object.
# resource), driven by testdata/pipeline_segment_navigator.properties. ${PIPESEG_NAV_BU} is kept
# only as documentation of the DOM id (row 1, C:1) - the properties-driven fill resolves to the
# same id/value, not a different one.
${PIPESEG_NAV_BU}          nav:form:G:0:R:1:C:1:dd
${PIPESEG_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/pipeline_segment_navigator.properties
${PIPESEG_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/pipeline_segment_insert.properties
${PIPESEG_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/pipeline_segment_update.properties
${PIPESEG_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/pipeline_segment_form_verify.properties
${PIPESEG_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/pipeline_segment_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented rationale as Area's/Bank's/Meter's own ${..._DEL_ENDDATE}: this
# row packs Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape
# the one-field-per-row label scan cannot safely resolve. Value confirmed live via the
# pre-existing pipeline_segment_page.resource ("Delete Pipeline Segment" keyword, live
# 2026-06-12).
${PIPESEG_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Pipeline Segment's own form-field label set (Start Date/Pipeline Name deliberately excluded
# from the live-DOM round-trip compare - Start Date lives only in objectdates, Pipeline Name is
# a dropdown that can re-render different display text after reload, same caveat as every other
# converted screen's dropdown fields).
@{PIPESEG_FORM_LABELS}    Pipeline Segment Code    Pipeline Segment Name


*** Keywords ***
Find Pipeline Segment Row By Filter
    [Documentation]    Explicitly filter the Pipeline Segment grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PIPESEG_TABLE}    ${code}

Clear Pipeline Segment Row Filter
    [Documentation]    Clear the Code column filter (see Find Pipeline Segment Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${PIPESEG_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Pipeline Segment's OWN credentials
    ...    (${PIPELINE_SEGMENT_EC_USER}/${PIPELINE_SEGMENT_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab).
    Login To EC Screen    ${PIPELINE_SEGMENT_EC_USER}    ${PIPELINE_SEGMENT_EC_PASS}

Open Pipeline Segment Screen With Navigator Values Populated
    [Documentation]    Navigate to the Pipeline Segment screen, THEN fill + submit the mandatory
    ...    Business Unit navigator (dropdown + GO) - the grid is scoped by it, so this single
    ...    keyword bundles both steps for the test case (Area's exact skeleton calls this as ONE
    ...    line per TC, not two). Assumes the caller already logged in this test case (via Login
    ...    To EC Application). Navigator fill delegates to the shared T2 "Apply Navigator From
    ...    Properties" (resources/manage_object.resource), driven by testdata/
    ...    pipeline_segment_navigator.properties, instead of inlining "Select EC Dropdown Option
    ...    + Apply Navigator" here.
    Open EC Screen    ${PIPESEG_SCREEN}
    Apply Navigator From Properties    ${PIPESEG_NAVIGATOR_PROPERTIES}

Insert Pipeline Segment Record And Save
    [Documentation]    Friendly-narrative wrapper (Area-pattern shape, ZERO arguments) around a
    ...    properties-file-driven insert: fills every field named in testdata/
    ...    pipeline_segment_insert.properties, in FILE ORDER (Code, Name, Start Date, then the
    ...    mandatory Pipeline Name dropdown - no popup on this screen's insert form, so order is
    ...    not load-bearing the way it is on Meter). Also owns the integrity check that the
    ...    inserted Pipeline Segment Code matches the suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${PIPESEG_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Pipeline Segment Code
    RETURN    ${code}

Verify Pipeline Segment Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the
    ...    grid, then Pipeline Segment Code/Pipeline Segment Name's LIVE SCREEN value is compared
    ...    to testdata/pipeline_segment_insert.properties. Filters via Find Pipeline Segment Row
    ...    By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Pipeline Segment Row By Filter    ${code}
    Verify Object Insert Exists    ${PIPESEG_TABLE}    ${code}    Pipeline Segment    ${PIPESEG_INSERT_PROPERTIES}
    ...    @{PIPESEG_FORM_LABELS}    code_label=Pipeline Segment Code
    Clear Pipeline Segment Row Filter

Update Pipeline Segment Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Pipeline Segment Name is listed in testdata/pipeline_segment_update.properties - only
    ...    Name is re-edited, matching every other converted screen's TC03 scope. Filters via
    ...    Find Pipeline Segment Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PIPESEG_UPDATE_PROPERTIES}
    Find Pipeline Segment Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PIPESEG_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Pipeline Segment Code
    Clear Pipeline Segment Row Filter
    RETURN    ${data}

Verify Pipeline Segment Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Pipeline Segment Name's LIVE SCREEN value to testdata/
    ...    pipeline_segment_update.properties. Filters via Find Pipeline Segment Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Pipeline Segment Row By Filter    ${code}
    Verify Object Form Record    ${PIPESEG_TABLE}    ${code}    Pipeline Segment    ${PIPESEG_UPDATE_PROPERTIES}
    ...    Pipeline Segment Name    code_label=Pipeline Segment Code
    Clear Pipeline Segment Row Filter

Find Pipeline Segment Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find
    ...    Pipeline Segment Row By Filter first. Deliberately does NOT clear the filter afterward
    ...    - Verify Pipeline Segment Record Found (called right after, same TC) needs the grid
    ...    still filtered to ${code} for its own grid-check; it clears the filter once both
    ...    checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Pipeline Segment Row By Filter    ${code}
    Find Object Record    ${PIPESEG_TABLE}    ${code}    Pipeline Segment    code_label=Pipeline Segment Code

Verify Pipeline Segment Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Pipeline Segment Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PIPESEG_TABLE}    ${code}    ${PIPESEG_GRID_VERIFY_PROPERTIES}
    ...    ${PIPESEG_FORM_VERIFY_PROPERTIES}    @{PIPESEG_FORM_LABELS}
    Clear Pipeline Segment Row Filter

Delete Pipeline Segment Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the pipeline segment, set End Date = Start Date (EC true delete for
    ...    OV_PIPELINE_SEGMENT), Save. Filters via Find Pipeline Segment Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Pipeline Segment Row By Filter    ${code}
    Delete Object Via End Date    ${PIPESEG_TABLE}    ${PIPESEG_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Pipeline Segment Row Filter

Verify Pipeline Segment Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_PIPELINE_SEGMENT) - the DB check lives here,
    ...    in the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PIPESEG_TABLE}    OV_PIPELINE_SEGMENT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Pipeline Segment Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (grid-only check) - delegates to the shared T2 Verify Object Does Not
    ...    Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PIPESEG_TABLE}    ${code}
