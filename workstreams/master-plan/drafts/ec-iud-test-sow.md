# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Task:** EC Screen Insert/Update/Delete (IUD) Automation
**Author:** Choong-Yin Lee / Claude Sonnet 4.6
**Date:** 2026-06-06
**Version:** 2.0 — COMPLETE

---

## 1. REQUIREMENT

### 1.1 Objective
Automate Insert, Update, Delete (IUD) operations on EC Web App screens to validate:
1. Each screen correctly allows creation of new records
2. Each screen correctly allows modification of existing records
3. Each screen correctly allows deletion/expiry of records
4. EC data integrity is maintained throughout the lifecycle

### 1.2 Scope
**Phase 1 — Proof of Concept:** Configuration > Finance Objects > Bank screen ✅ COMPLETE
**Phase 2+ (planned):**
- Create EC Schedule (Schedules screen)
- Setup ECIS File Upload (Adapter Configuration)
- Other Configuration/Production screens

### 1.3 Constraints
- **NEVER modify existing production/configuration data**
- All test data prefixed `AUTOTEST_` for easy identification
- Target environment: Local EC (`ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`)
- User: sysadmin

### 1.4 Acceptance Criteria
| Operation | Pass Condition | Status |
|---|---|---|
| INSERT | New record with AUTOTEST_ code appears in table after save | ✅ PASS |
| UPDATE | Bank Name changed and persisted after save | ✅ PASS |
| DELETE | Record no longer visible after End Date set + save | ✅ PASS |
| CLEANUP | Environment returned to near-pre-test state (bank expired) | ✅ PASS |

---

## 2. DESIGN

### 2.1 EC Screen Types and IUD Patterns

EC screens fall into two main types for IUD:

**Type A — NAVIGATOR+TABLE (standard data screens)**
```
Pattern: Navigator → Go → Table loads → Toolbar Insert → Fill row → Save
Example: Role Maintenance, Check Group, Units
```

**Type B — MANAGE OBJECT (master data screens)**
```
Pattern: Insert toolbar → New Object submenu → Fill objectForm → Save
         Select row → updateAttributes form → Edit fields → Save
         Select row → objectdates form → Set End Date → Save (soft-delete)
Example: Bank, Company, Well, Facility
```

### 2.2 Bank Screen Analysis (from DOM Deep Dive)

| Property | Value |
|---|---|
| Screen name | Bank |
| Screen path | Configuration > Finance Objects > Bank |
| Screen type | Manage Object (EC14+ pattern) |
| Screen URL | `/com.ec.frmw.co.screens/manage_object_nav/CLASS_NAME/BANK.jsf` |
| Navigator | Date filter (`nav:form:G:0:R:1:C:0:da_input`) + Go button |
| Object list | `manage_object_nav_nav:form:T` (TableScreenlet, 4 cols) |
| Toolbar | Save (enabled after edit), Insert (submenu), Delete (DISABLED by design) |
| Tab structure | objectdates, daytimes, updateAttributes, versions |

**Bank screen IUD design:**
```
INSERT:  Insert toolbar → hover → submenu → "New Object"
         → objectForm appears with 3 mandatory fields:
           R:0 = Bank Code        (tab:tabPanel:objectForm:form:G:0:R:0:C:1:in)
           R:1 = Bank Name        (tab:tabPanel:objectForm:form:G:0:R:1:C:1:in)
           R:2 = Start Date       (tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input)
         → Fill all 3 → Save → Go button → verify in table

UPDATE:  Click row span in table → updateAttributes form loads:
           Code: tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (read-only)
           Name: tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in (editable)
         → Edit Name → Save → Go → verify

DELETE:  EC Bank toolbar Delete submenu = DISABLED (no items configured)
         Banks are permanent master data (may have historical transaction references)
         Soft-delete approach: Click row → objectdates form End Date set:
           End Date: tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
         → Set End Date = day after Start Date → Save → Go
         → Bank no longer visible at current nav date = effectively deleted
```

### 2.3 Test Data Design

| Field | Value |
|---|---|
| Bank Code | `AUTOTEST_BNK_003` |
| Bank Name (Insert) | `AUTOTEST Bank 003` |
| Bank Name (Update) | `AUTOTEST Bank 003 UPDATED` |
| Start Date | `2000-01-01` |
| End Date (Delete) | `2000-01-02` |
| Note | EC bank hard-delete disabled; expired banks persist in DB with End Date set. |
| Note | Subsequent runs must use next numeric suffix (BNK_004, BNK_005, etc.) |

### 2.4 Technology Stack

| Component | Technology |
|---|---|
| Browser automation | Playwright (Python sync API) |
| Test framework | Robot Framework (generated RF script) |
| Screenshots | Playwright `page.screenshot()` per step (15 screenshots) |
| Results | JSON log at `tmp/logs/ec_iud_bank_final.json` |
| Evidence | Screenshots at `docs/EC/screenshots/iud_bank/` |

---

## 3. DEVELOPMENT

### 3.1 Technical Challenges and Solutions

#### Challenge 1: Bank Screen Type Identification
**Problem:** Bank screen appeared empty on initial load.
**Root cause:** Manage Object (EC14+ pattern) — requires Go button click for table, Insert submenu for new object.
**Solution:** DOM inspection revealed `manage_object_nav_nav:form:T` table, `nav:form` date navigator.

#### Challenge 2: Insert Submenu — Hover State Lost in Headless Mode
**Problem:** PrimeFaces hover menus require hover to show submenu items. In headless mode, hover state was lost.
**Solution:** Iterate over all `//ul[contains(@class,'ui-menu-child')]//li//a` links after hover, check visibility, click first visible item.

#### Challenge 3: Wrong Field IDs for Insert
**Problem:** v1/v2 filled sidebar search (`menu:searchForm:searchTxt`) instead of objectForm fields.
**Solution:** DOM inspection after "New Object" click revealed correct field IDs: `tab:tabPanel:objectForm:form:G:0:R:{N}:C:1:in`.

#### Challenge 4: Insert Save Failed — Required Field Missing
**Problem:** Save showed "Required fields: Start Date [OBJECT_START_DATE]".
**Solution:** Field `tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input` (Start Date, da_input type) must be filled. Use `fill()` + Tab + change event.

#### Challenge 5: Update Used Wrong Field IDs
**Problem:** After row selection, the UPDATE form uses `updateAttributes` screenlet, not `objectForm`.
**Solution:** DOM inspection after row click revealed: `tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in` for Bank Name.

#### Challenge 6: Delete Button — Empty Submenu
**Problem:** Toolbar Delete button has `ui-submenu-state-disabled` — no submenu items.
**Root cause:** EC Bank is permanent master data; hard-delete is disabled by EC configuration.
**Solution:** Soft-delete via End Date in `objectdates` form. Bank becomes inactive/expired at current nav date.

#### Challenge 7: Repeat Runs — Expired Bank Code Conflict
**Problem:** After a run, expired bank code still exists in DB. Next run tries same code → EC silently rejects insert.
**Solution:** Each test run uses an incrementing bank code (BNK_001 → BNK_002 → BNK_003). OR use nav date navigation to access expired bank and handle re-activation.

#### Challenge 8: Row Selection XPath Fails
**Problem:** XPath `//tr[td[normalize-space(text())='CODE']]` failed because text is in `<span>` child.
**Solution:** Use `//tr[.//span[normalize-space(text())='CODE']]` or CSS `span:text-is()` locator.

### 3.2 Scripts Produced

| Script | Purpose | Status |
|---|---|---|
| `ec_bank_inspect.py` | DOM inspection — initial Bank screen structure | Complete |
| `ec_bank_row_select_inspect.py` | DOM inspection — after row click, toolbar state | Complete |
| `ec_bank_delete_test.py` | Investigation — confirm delete button disabled | Complete |
| `ec_iud_bank.py` | v1 — initial attempt | Superseded |
| `ec_iud_bank_v2.py` | v2 — partial fix | Superseded |
| `ec_iud_bank_v3.py` | v3 — correct fields found | Superseded |
| `ec_iud_bank_v4.py` | v4 — mandatory Start Date discovery | Superseded |
| `ec_iud_bank_v5.py` | v5 — all 3 phases working | Superseded |
| `ec_iud_bank_final.py` | Final — complete IUD with all edge cases handled | **FINAL** |
| `ec_iud_bank.robot` | Robot Framework test suite | **FINAL** |

---

## 4. TEST EXECUTION

### 4.1 Test Runs Log

| Run | Script | Date | Result | Issue |
|---|---|---|---|---|
| v1 | ec_iud_bank.py | 2026-06-06 | FAIL | `get_attribute()` API error |
| v2 | ec_iud_bank_v2.py | 2026-06-06 | PARTIAL | Filled sidebar search instead of Bank Code |
| v3 | ec_iud_bank_v3.py | 2026-06-06 | PARTIAL | Fields filled, save failed (Start Date required) |
| v4 | ec_iud_bank_v4.py | 2026-06-06 | PARTIAL | EC error captured: "Start Date required" |
| v5 (run 1) | ec_iud_bank_v5.py | 2026-06-06 | INSERT PASS, UPDATE SKIP, DELETE SKIP | Row XPath wrong |
| v5 (run 2) | ec_iud_bank_v5.py | 2026-06-06 | INSERT PASS, UPDATE PASS, DELETE FAIL | Delete verification wrong |
| final (run 1) | ec_iud_bank_final.py | 2026-06-06 | PASS PASS PASS | **ALL PASS** — AUTOTEST_BNK_003 |

### 4.2 Final Test Results (AUTOTEST_BNK_003)

```
✓ login           : PASS
✓ navigate        : PASS
✓ clean           : CLEAN
✓ insert          : PASS
✓ update          : PASS
✓ delete          : PASS (soft-delete: EndDate=2000-01-02, bank expired)

Overall: ALL PASS
```

### 4.3 Screenshots Evidence (15 screenshots)
All in: `docs/EC/screenshots/iud_bank/`

| # | Screenshot | Step | Status |
|---|---|---|---|
| 01 | `final_01_bank_loaded.png` | Bank screen opened | ✅ |
| 02 | `final_02_clean_state.png` | Clean state verified (6 banks, no AUTOTEST) | ✅ |
| 03 | `final_03_insert_new_object.png` | After New Object click | ✅ |
| 04 | `final_04_insert_filled.png` | objectForm filled (Code+Name+StartDate) | ✅ |
| 05 | `final_05_insert_saved.png` | After insert save | ✅ |
| 06 | `final_06_insert_result.png` | 7 banks in table, AUTOTEST visible | ✅ |
| 07 | `final_07_update_row_selected.png` | Row selected, updateAttributes loaded | ✅ |
| 08 | `final_08_update_filled.png` | Bank Name updated | ✅ |
| 09 | `final_09_update_saved.png` | After update save | ✅ |
| 10 | `final_10_update_result.png` | Updated name in row verified | ✅ |
| 11 | `final_11_delete_row_selected.png` | Row selected for delete | ✅ |
| 12 | `final_12_delete_end_date_set.png` | End Date set in objectdates | ✅ |
| 13 | `final_13_delete_saved.png` | After delete save | ✅ |
| 14 | `final_14_delete_result.png` | Bank no longer in table | ✅ |
| 15 | `final_15_final_state.png` | Final state — 6 banks (no AUTOTEST) | ✅ |

---

## 5. COMPLETION CRITERIA (Phase 1)

| Deliverable | Status |
|---|---|
| ✅ Playwright script | `ec_iud_bank_final.py` — complete IUD automation |
| ✅ RF test script | `ec_iud_bank.robot` — 5 test cases + keywords |
| ✅ Screenshots | 15 screenshots per IUD step |
| ✅ Results JSON | `tmp/logs/ec_iud_bank_final.json` — ALL PASS |
| ✅ SOW document | This document (v2.0 COMPLETE) |
| ✅ Git commit | To be committed with all evidence |

---

## 6. EC BANK SCREEN — DOM REFERENCE (from deep dive)

### Insert objectForm Fields
```
Bank Code:   tab:tabPanel:objectForm:form:G:0:R:0:C:1:in     (text input, mandatory)
Bank Name:   tab:tabPanel:objectForm:form:G:0:R:1:C:1:in     (text input, mandatory)
Start Date:  tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input (date picker, mandatory)
End Date:    tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input (date picker, optional)
+ R:4-R:15:  other optional bank attributes
```

### Update Fields (after row selection)
```
Bank Code:   tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in  (read-only after creation)
Bank Name:   tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in  (editable)
+ R:2-R:13:  other editable attributes
```

### Delete / Object Dates
```
Start Date:  tab:tabPanel:objectdates:form:G:0:R:0:C:1:da_input  (editable)
End Date:    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input  (set to expire bank)
```

### Toolbar Structure
```
Save:    a[title='Save [Ctrl+s]']     — enabled after objectForm modified
Refresh: a[title='Refresh [Ctrl+r]']  — always enabled
Insert:  li.ui-menu-parent (submenu):
           'New Object' — creates new bank (objectForm: all blank)
           'New Version' — new date-effective version of existing bank
Delete:  li.ui-menu-parent (submenu) — ui-submenu-state-disabled (no items)
         EC DESIGN: Bank hard-delete is disabled (banks are permanent master data)
```

### Bank Table
```
manage_object_nav_nav:form:T_data  — tbody ID
Row columns: C0=BankCode, C1=BankName, C2=StartDate, C3=(empty/other)
Cell text is in span._la inside td — use //tr[.//span[text()='CODE']] for XPath
```

---

## 7. NEXT SCREENS (Phase 2+)

| Screen | Type | IUD pattern | Notes |
|---|---|---|---|
| Schedules | NAVIGATOR+TABLE | Navigator → Go → Insert row → fill | Cron schedule creation |
| Adapter Configuration | NAVIGATOR+TABLE | Insert → fill adapter → save | ECIS file upload setup |
| Role Maintenance | NAVIGATOR+TABLE | Insert → fill role → assign screens | User role management |
| Check Group | NAVIGATOR+TABLE | Insert → fill group → assign rules | Validation group setup |

---

## 8. LESSONS LEARNED

1. **Deep DOM inspection before automation is mandatory** — Bank screen looks like a standard table screen but is a Manage Object screen with completely different field IDs and patterns.

2. **EC Manage Object screens have 2 distinct form areas:**
   - `objectForm` — used for NEW object creation (Insert → New Object)
   - `updateAttributes` — used for editing existing objects (row selection)

3. **Mandatory fields vary by EC object type** — Bank requires Bank Code, Bank Name, Start Date. Missing Start Date causes silent save failure with EC notification message.

4. **EC Bank hard-delete is intentionally disabled** — Banks are master data that can have historical transaction references. Soft-delete (End Date expiry) is the EC-correct approach.

5. **PrimeFaces hover menus in headless Playwright** — After hover(), use `count() + is_visible()` to detect submenu items before clicking, with fallback iterating through all submenu links.

6. **Row text is in `<span>` children not `<td>` text** — XPath must use `normalize-space(.)` or `.//span[text()]` instead of `normalize-space(text())`.
