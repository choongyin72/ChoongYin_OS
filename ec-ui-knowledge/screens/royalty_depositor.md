# Screen: Royalty Depositor

- **Type:** OV (Manage-Object, date-effective) — Bank family (date-only navigator, NOT OV-GM)
- **Treeview path:** Configuration > Assets > Royalty Objects > Royalty Depositor (RC.0052)
- **Open via:** menu search / treeview, screen name `Royalty Depositor`
- **DB view (ground truth):** `OV_ROYALTY_DEPOSITOR` (base `COMPANY`/`COMPANY_VERSION`; app `EC_REVN`)
- **Last verified:** 2026-08-28 · EC 14.2.4 · sandbox `ap-f0a7g341jn6d.corp.quorumsoftware.com:8443`
  · dryrun 5/5, live headless 5/5, DB self-clean 0 residual (all re-confirmed by the 2026-08-28
  documentation backfill; RF automation itself last changed 2026-08-25, PR #448 + alignment fix)
- **Pattern:** Bank-pattern conversion (Batch 5, PR #448, merged 2026-08-23) — label-driven field
  resolution + properties-file-driven test data + T2-consolidated keywords, mirrors
  `bank_page.resource`/`state_page.resource`. See `ec-ui-knowledge/screens/bank.md` for the shared
  mechanic; this file records what is Royalty-Depositor-specific.

## Selectors `[from pageobjects/Configuration/Assets/Royalty_Objects/royalty_depositor_page.resource]`

| Purpose | Selector / value |
|---|---|
| Grid tbody id | `manage_object_nav_nav:form:T_data` (aliased in the T3 as `${RD_TABLE}` = the shared T2 `${OV_MANAGE_OBJECT_TABLE}` constant) |
| Code field label (screen-prefixed, NOT generic "Code") | `Royalty Depositor Code` |
| Form field labels used by IUD | `Royalty Depositor Code`, `Royalty Depositor Name` (`@{RD_FORM_LABELS}`) |
| Delete (End Date input, objectdates) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (Start Date at C:1, End Date label at C:2) |
| Grid filter keyword (screen-specific wrapper) | `Find Royalty Depositor Row By Filter` / `Clear Royalty Depositor Row Filter` → delegate to T2 `Find/Clear Object Row By Filter` on `${RD_TABLE}` |
| Login | `Login To EC Screen` (T1) called with `${ROYALTY_DEPOSITOR_EC_USER}`/`${ROYALTY_DEPOSITOR_EC_PASS}` from `resources/credentials.py` |

### Insert (`objectForm`) — mandatory fields only (live `MandatoryCellStyle` scan, 2026-08-23)
- **Royalty Depositor Code** (mandatory)
- **Royalty Depositor Name** (mandatory)
- **Start Date** (mandatory; lives only in `objectdates`, not `updateAttributes`)

Everything else in `objectForm` is optional and deliberately NOT filled by this suite (no scope
expansion vs. the pre-conversion driver): Official Name, Comments, System Company, Company
Number, Registration Details, Interface Sequence Owner, Address Line 1-8, Phone, Fax, Email,
Original Number, Fin Code, Country.

### Update (`updateAttributes`)
- **Royalty Depositor Code** — read-only after create.
- **Royalty Depositor Name** — the only field this suite edits on Update.
- Start Date / End Date are NOT present in `updateAttributes` — they live only in `objectdates`.

### Delete — `objectdates`
End Date = Start Date (zero-length window) → Save → GO → row leaves `OV_ROYALTY_DEPOSITOR`
(TRUE delete, DB-verified). Toolbar Delete is not used (standard EC Object delete mechanism).

### Grid columns (confirmed live 2026-08-23)
Royalty Depositor Code / Royalty Depositor Name / Start Date / End Date.

## Mandatory-yellow fields
Code, Name, Start Date — confirmed via live `MandatoryCellStyle` scan on 2026-08-23 (PR #448
recon). No navigator/date+GO cascade beyond the universal as-at-date filter bar every
manage-object OV screen has (confirmed live: `NAV_GO_BUTTON_COUNT=1`, `NAV_DROPDOWN_COUNT=0`).

## Quirks
- **Screen-prefixed labels**: this screen uses "Royalty Depositor Code"/"Royalty Depositor Name",
  not the generic "Code"/"Name" that Bank itself uses — same convention as State's own "State
  Code" precedent. Every T2 call in the T3 passes `code_label=Royalty Depositor Code` explicitly.
- **Fixed test code, not per-run-generated**: the suite reuses `AUTOTEST_ROYALTY_DEP` every run
  (matches Bank/Account's own convention) rather than generating a fresh code per run. EC keeps
  deleted codes in the base table (never truly reused), so every run MUST complete TC05 (delete)
  or the next run's TC01 clean-state check fails.
- **Pure-screen-only verification**: as of the 2026-08-25 alignment fix, the screen-verification
  keywords (`Verify Royalty Depositor Record Exists/Updated/Found`) do NOT perform their own DB
  reads — DB ground-truth checks live only in the dedicated TC02/TC05 DbVerify assertions. An
  earlier inline `Royalty Depositor Should Exist In DB` keyword violated this and was removed.
- **Shared-sandbox risk**: a concurrent agent's session on the same `sysadmin` login on this
  shared sandbox can produce a transient account lockout or a stale "unsaved changes" dialog —
  not a defect in this screen. Mitigate with a single retry (self-clean any leftover row first),
  never a killed browser/node process (shared-environment process rule).

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (the current/proven stack):** T3
  `ec-automation/pageobjects/Configuration/Assets/Royalty_Objects/royalty_depositor_page.resource`
  + suite `ec-automation/tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot`
  + testdata `ec-automation/testdata/royalty_depositor_{insert,update,form_verify,grid_verify}.properties`
  (T2 `manage_object.resource` + T1 `common.resource` + `libraries/DbVerify.py`, no shared-file
  edits). Validated live 5/5 (2026-08-23 PR #448; 2026-08-25 alignment-fix re-verify; 2026-08-28
  documentation-backfill confirmation run).
- **Legacy Playwright (reference only, pre-dates PR #448, not rebuilt):**
  `ec-automation/screens/Configuration/Assets/Royalty_Objects/Royalty_Depositor/playwright/ec_iud_royalty_depositor.py`.
  New Playwright drivers are waived by owner decision 2026-08-27 in favour of the Universal
  Screen Engine (`ec-automation/py/engine.py`).
- **Bundle:** `ec-automation/screens/Configuration/Assets/Royalty_Objects/Royalty_Depositor/`
  (SOW, README, JOURNAL, CHECKLIST, evidence/).
