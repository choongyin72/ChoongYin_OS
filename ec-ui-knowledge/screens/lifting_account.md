# Screen: Lifting Account

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.2004 - **Treeview:** Configuration > Assets > Transport_Objects > Lifting Account
- **DB view:** `OV_LIFTING_ACCOUNT` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - Area-pattern RF suite (PR #562,
  merged 2026-08-27 at `6a8c328`) re-confirmed live 5/5 this session; DB self-clean 0 residual via a
  fresh independent oracledb connection.

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Lifting Account` -> `label.tv-link` "Lifting Account" |
| Navigator (ONE group, cascade spans TWO grid rows) | `nav:form:G:0:R:1:C:1..3:dd` = P1 Production Unit -> P1 Area -> P1 Facility 1, PLUS Storage on row 3: `nav:form:G:0:R:3:C:0:dd` = P1_CRUDE_STOR (SPECIFIC values - Storage level EMPTY under first-available AS1) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Lifting Account Code*** - **Lifting Account Name*** - **Start Date*** (date, 2020-01-01) + **Company Name*** (first-available) + **Storage Name*** = nav Storage P1_CRUDE_STOR (parent-matching - row never lists otherwise). NO Op Production Unit field. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Lifting Account Code` (ro) - **`Lifting Account Name`**. Delete: **`End Date`** = Start Date at
field id `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded deliberately, confirmed
live via the Playwright driver) -> leaves `OV_LIFTING_ACCOUNT`.

## Navigator shape - the real, verified story (2026-08-27, PR #562)
A prior UNVERIFIED chat-level classification called this screen's navigator "two separate rows/
groups" (which would have disqualified it from the shared Area-pattern navigator keyword, per
Tract's genuinely-separate-`G:1`/`G:2`-fieldsets precedent). Live per-field DOM recon corrected
this: the navigator is **ONE fieldset** (`nav:form:G:0`), not two groups - its mandatory 4-value
cascade is simply rendered across TWO grid rows within that one group (R:1 C:1..C:3, then R:3
C:0). All four dropdown spans confirmed live to carry `{mandatory:true} MandatoryCellStyle`
(genuinely empty on load).

To fill this in one call, the shared T2 keyword `Apply Navigator From Properties`
(`resources/manage_object.resource`) was extended with new optional arguments
`${row2_from}`/`${row2}`/`${row2_start_col}`. Caller usage (from
`lifting_account_page.resource`):
```robotframework
Apply Navigator From Properties    ${LA_NAVIGATOR_PROPERTIES}
...    row2_from=3    row2=3    row2_start_col=0
```
(3 values fill the primary row=1/start_col=1 sequence; the 4th value, "past" `row2_from=3`, fills
row=3 starting at col=0.)

## GOTCHA - the shared-keyword regression this extension caused (caught pre-merge)
**This is a documented, real regression, not a hypothetical risk - read before touching this
keyword again.** The FIRST version of the extension used a string-interpolated RF `IF` condition
(`"${idx} > ${row2_from}"`). RF substitutes `${row2_from}` **textually** before the condition is
evaluated - so its empty default (`${EMPTY}`, used by every OTHER caller of this keyword) collapsed
the condition to the literal `"1 > "`, invalid Python syntax, **for every existing caller**. Area
and Meter both failed a live regression canary 0/5 with `Invalid IF condition ... SyntaxError`
BEFORE this reached master - caught by the reviewer's mandatory live-canary gate on shared-keyword
changes (2+ existing callers, live, every time, no exceptions), not by the full-tree dryrun (which
had already passed 881/881 - a dryrun proves syntax, not behavior).

**The actual current fix** (transcribed verbatim from `resources/manage_object.resource` as of
2026-08-27, NOT paraphrased):
```robotframework
    [Arguments]    ${properties_path}    ${row}=1    ${group}=0    ${start_col}=1
    ...    ${row2_from}=${EMPTY}    ${row2}=1    ${row2_start_col}=1
    ${data}=    Read Properties    ${properties_path}
    ${col}=    Set Variable    ${start_col}
    ${idx}=    Set Variable    ${0}
    FOR    ${label}    IN    @{data.keys()}
        ${idx}=    Evaluate    ${idx} + 1
        ${past_row2_from}=    Evaluate    $row2_from != "" and $idx > int($row2_from)
        IF    ${past_row2_from}
            ${use_row}=    Set Variable    ${row2}
            ${use_col}=    Evaluate    ${row2_start_col} + ${idx} - int($row2_from) - 1
        ELSE
            ${use_row}=    Set Variable    ${row}
            ${use_col}=    Set Variable    ${col}
            ${col}=    Evaluate    ${col} + 1
        END
        ${dd}=    Set Variable    nav:form:G:${group}:R:${use_row}:C:${use_col}:dd
        Select EC Dropdown Option    ${dd}    ${data}[${label}]
        Sleep    0.7s
    END
    Apply Navigator
```
The fix uses RF's native-variable syntax (`$row2_from`/`$idx`, no braces) inside a dedicated
`Evaluate` call with an explicit `int()` conversion - this form is read directly from RF's variable
store by Python, bypassing the textual pre-substitution that broke the original `IF`-based version.

**Re-canaried live after the fix:** Area 5/5, Meter 5/5, Lifting Account's own suite 5/5. Full-tree
dryrun re-confirmed 883/883.

**Rule for the next screen that needs to extend this keyword again:** any change to a shared
keyword's internal branching/loop logic (not just adding a new optional argument that's a no-op
when unset) needs a LIVE regression canary on 2+ existing callers before merge - a dryrun cannot
catch this class of bug, and neither can a careful manual trace of the Python logic alone (the
reviewer traced this by hand first, believed it was safe, and was still wrong until the live canary
ran).

## Automation (code in ec-automation)
- **Playwright:** `py/lifting_account_iud.py` (thin driver with screen-local
  `apply_lifting_account_navigator`; left UNTOUCHED by the PR #562 RF-only conversion, per the
  owner's permanent waiver of new Playwright-bundle work for Bank-/Area-pattern conversions).
- **RF:** T3 `pageobjects/Configuration/Assets/Transport_Objects/lifting_account_page.resource`
  (Area-pattern, properties-file-driven since PR #562) + suite
  `tests/Configuration/Assets/Transport_Objects/lifting_account_iud.robot` (5 TCs, per-TC login/
  logout).
- **Test data:** `testdata/lifting_account_{navigator,insert,update,form_verify,grid_verify}.properties`.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. Storage has no options under the
  first-available AS1 path (the original 2026-07-30 park reason) - the navigator uses the SPECIFIC
  P1 scope proven live by the original hand-built driver, reused verbatim; form Storage Name must
  equal nav Storage or the inserted row is invisible under this OV-GM scope (parent-matching rule).
- See the GOTCHA section above for the shared-keyword regression - do not re-derive the row2
  addressing from scratch; the current code is transcribed verbatim above.
