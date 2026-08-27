# Screen: Price Rate

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel;
  Business-Unit-GATED (**single-dropdown** navigator, C:1 only - NOT a multi-level cascade; same
  shape as Area/Contract Area's own single-dropdown navigator).
- **BF_CODE:** CO.3024 - **Treeview:** Configuration > Assets > Sales_Objects > Price Rate
- **DB view:** `OV_PRICE_RATE` (generic `CODE` column, per `libraries/DbVerify.py`)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05), fresh-connection DB self-clean 0 residual, `check_bundle_hygiene.py` PASS
  (backfill re-run of PR #534's Area-pattern conversion, merged 2026-08-26)

## Selectors
| Purpose | Selector |
|---|---|
| Grid | `manageObject:form:T_data` (empty until nav BU + GO) |
| Navigator (single dropdown) | `nav:form:G:0:R:1:C:1:dd` = Business Unit -> GO (`button:form:B`) |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not
  label-driven - the row packs Start Date C:1 + End Date C:3 with the End Date label at C:2) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Price Rate Code*** - **Price Rate Name*** - **Start Date*** (date) - dropdown **Frequency***
(mandatory but no fixed proven value in this sandbox - `__FIRST__` used) - **Business Unit***
(dropdown, MANDATORY - must equal the nav BU value "SS2 BU" or the inserted row never lists in
the filtered grid). Labels are SCREEN-PREFIXED ("Price Rate Code"/"Price Rate Name"), like Area's
"Area Code"/"Area Name" - NOT the generic "Code"/"Name" Bank/Object List use. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Price Rate Code` (ro, guard) - **`Price Rate Name`**. Delete: **`End Date`** = Start Date
(zero-length window) -> true delete, row leaves `OV_PRICE_RATE`.

## Navigator value (this environment)
Business Unit = **"SS2 BU"** (confirmed live via the original OLD-pattern driver and carried
unchanged through the Area-pattern conversion) - driven by
`testdata/price_rate_navigator.properties` via the shared T2 `Apply Navigator From Properties`
keyword.

## Automation (code in ec-automation)
- **RF (maintained/live test):** T3
  `pageobjects/Configuration/Assets/Sales_Objects/price_rate_page.resource` (label-driven,
  2026-08-26 Area-pattern conversion, PR #534) + suite
  `tests/Configuration/Assets/Sales_Objects/price_rate_iud.robot` (5 TC: Clean State / Insert /
  Update / Find / Delete, per-TC login/logout, fixed test code `AUTOTEST_PRICE_RATE`).
- **Playwright (historical reference only, NOT maintained):** `py/price_rate_iud.py` - original
  2026-08-02 build (shared engine `ec_object_iud.py` + explicit `select_dropdown`), preserved
  unchanged; no new Playwright bundle is built for Area-pattern work (owner decision 2026-08-27,
  Universal Screen Engine replaces this role).
- **Test data:** `testdata/price_rate_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `PRICE_RATE_EC_USER`/`PRICE_RATE_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- OV-GM Business-Unit-gated: grid empty until the nav Business Unit dropdown + GO completes.
- The navigator is a **single dropdown** (C:1 only) - earlier documentation (2026-08-02) described
  it as a multi-level cascade (`C:1..N:dd`); the real page object confirms it is not (corrected
  2026-08-27).
- Business Unit (insert field) MUST equal the nav Business Unit ("SS2 BU") or the inserted row is
  invisible under the filtered navigator scope - same convention as every other OV-GM screen
  converted in this batch.
- Frequency is a mandatory dropdown with no fixed proven value in this sandbox - the suite uses
  `__FIRST__` (picks the first available option), matching the prior driver's own convention.
- DB self-clean checks against `OV_PRICE_RATE` must use the generic `CODE` column.
- **Real environment flake hit during the 2026-08-27 backfill (not a screen defect):** a live
  re-run of this already-proven suite failed intermittently with `Could not find active page` /
  `browserContext.newPage: ... has been closed`, traced to a pile-up of leftover
  `chrome-headless-shell.exe`/`node.exe` processes from this session's other work - cross-checked
  as environment-wide via the **Area** suite's own TC01 failing identically in the same window.
  Resolved by killing the stray processes and retrying; the suite passed 5/5 on the clean attempt.
  See `screens/Configuration/Assets/Sales_Objects/Price_Rate/JOURNAL.md` for the full account.
