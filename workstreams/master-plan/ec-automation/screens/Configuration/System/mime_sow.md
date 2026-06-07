# EC Screen IUD Operation Test — MIME Type Mapping — Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Task:** EC MIME Type Mapping screen Insert/Update/Delete (IUD) Automation
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-07
**Version:** 2.0 — **COMPLETE** (executed, DB-verified, both frameworks ALL PASS)
**Pattern:** **Table class (TV view)** — contrast to the Manage Object (OV) pattern of Bank/Equipment

---

## 1. REQUIREMENT

### 1.1 Objective
Automate Insert, Update, Delete (IUD) on the EC **MIME Type Mapping** screen to validate:
1. Creation of a new MIME-type → file-extension mapping
2. Modification of an existing mapping
3. Deletion of a mapping
4. Data integrity maintained (existing mappings untouched)

### 1.2 Scope
MIME Type Mapping screen only (Configuration → System). Same scope as the Bank task: perform a full IUD lifecycle, two implementations (Playwright + Robot Framework), DB-verified.

### 1.3 Constraints
- **NEVER modify existing rows** — only the `application/x-ec-autotest` test row.
- Test data prefixed/identifiable as autotest.
- Target: local EC sandbox `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (user `sysadmin`).
- DB verification: `localhost:1521/ORCL` (`ECKERNEL_EC` / `energy`).

### 1.4 Acceptance Criteria
| Operation | Pass Condition |
|---|---|
| INSERT | New `application/x-ec-autotest` row appears in the grid after save |
| UPDATE | File Extensions value changed and persisted after save |
| DELETE | Row **physically removed** (gone from `TV_CTRL_MIME_TYPE_MAPPING` AND base `CTRL_MIME_TYPE_MAPPING`) |
| INTEGRITY | Existing MIME mappings untouched |

---

## 2. DESIGN

### 2.1 Screen analysis (from read-only recon)
| Property | Value |
|---|---|
| Screen | MIME Type Mapping (Configuration → System) |
| Screen type | **Table class** — inline-editable grid, **no navigator** |
| Screenlet | `mime_type_table:form` (tableScreenlet) |
| Columns | MIME Type, File Extensions (both editable) |
| Toolbar | Save (enables on edit), Refresh, Insert (→ "MIME Type Mapping"), Delete (→ "MIME Type Mapping") |
| Backing view | **`TV_CTRL_MIME_TYPE_MAPPING`** (TV = Table-class view) |
| Base table | `CTRL_MIME_TYPE_MAPPING` (+ `_JN` journal) |

### 2.2 Key contrast vs Bank/Equipment (Object class / OV)
| | Bank/Equipment (OV / Object) | **MIME Type Mapping (TV / Table)** |
|---|---|---|
| Navigator | cascading filters + Go | none — loads directly |
| Insert | Insert → New Object → object form | Insert → new editable **grid row** |
| Edit | updateAttributes form | edit **cells inline** |
| Delete | End Date = Start Date (date-effective) | **physical row delete** (table classes are not versioned) |
| Key | OBJECT_ID surrogate + dates | natural key (MIME_TYPE), no Start/End dates |

### 2.3 IUD design (exact field/cell IDs to be confirmed in §3 scan)
```
INSERT:  Insert toolbar → "MIME Type Mapping" submenu → a new editable row appears in the grid
         → fill MIME Type + File Extensions cells (expected mime_type_table:form:T:{row}:C{col}_in)
         → Save → Refresh → verify row present
UPDATE:  Click the File Extensions cell of the AUTOTEST row → change value → Save → verify
DELETE:  Select the AUTOTEST row → Delete toolbar (→ "MIME Type Mapping") → Save
         → verify row PHYSICALLY removed (UI + DB; not end-dated)
```

### 2.4 Test data
| Field | Value |
|---|---|
| MIME Type (Insert) | `application/x-ec-autotest` |
| File Extensions (Insert) | `.ectest` |
| File Extensions (Update) | `.ectest,.ectest2` |
| Delete | remove the row entirely |
| Note | MIME Type is the natural key — use a clearly-fake value that won't collide. |

### 2.5 Technology stack
Playwright (Python sync) + Robot Framework (Browser lib) + oracledb (DB verify). Repo-root-relative paths; env-overridable. Identical toolchain to the Bank deliverable.

---

## 3. DEVELOPMENT

| Script | Purpose | Status |
|---|---|---|
| `investigation/mime_inspect.py` | DOM scan — grid `mime_type_table:form:T_data`, toolbar, Insert/Delete submenus, new-row cell IDs | ✅ done |
| `investigation/mime_cell_scan.py` | Cell-commit mechanism deep-dive — `onchange→PrimeFaces.ab` partial submit, paginator, 20 rows/page in DOM | ✅ done |
| `ec_iud_mime.py` | Playwright IUD (full lifecycle, env-overridable, repo-relative paths) | ✅ done |
| `ec_iud_mime.robot` | Robot Framework suite (TC01 clean → TC02 insert → TC03 update → TC04 delete) | ✅ done |
| `investigation/db_query_tv_mime.py` | DB verification (TV view + base table counts, row presence) | ✅ done |

### 3.1 Confirmed screen mechanics (from §2 scan)
- **Grid:** `mime_type_table:form:T_data`; cell inputs `mime_type_table:form:T:{row}:C0_in` (MIME Type), `…:C1_in` (File Extensions).
- **Insert:** Insert toolbar submenu → a new editable row is added (blank `C0_in`/`C1_in`) at the top of the grid.
- **Delete:** Delete toolbar submenu ("MIME Type Mapping") on the selected row → **physical** removal.
- **Pagination:** ~20 rows/page in the DOM with a PrimeFaces paginator — row lookup must page through (first → next…).

### 3.2 Challenges & solutions
| # | Challenge | Root cause | Solution |
|---|---|---|---|
| 1 | Playwright run 1: INSERT/UPDATE reported PASS but DB had **0** rows; integrity check false-alarmed | (a) `el.fill()` + synthetic `dispatchEvent('change')` did **not** fire the cell's real `onchange→PrimeFaces.ab` partial-submit → nothing staged server-side → Save committed nothing. (b) grid is **paginated** (89 rows) so "compare visible rows" mis-read existing data as changed. | Commit cells with **real keystrokes + `Tab`** (`click → Ctrl+A → Delete → type(delay) → Tab → wait_ajax`); **reload (Refresh)** before verifying; **page-aware** row lookup (`find_row_paged`). |
| 2 | RF run 1: `ReferenceError: arguments is not defined` in `Evaluate JavaScript` | Browser-library arrow function has no `arguments` object | Embed the search value via RF variable substitution into the JS literal instead of passing an arg |
| 3 | RF run 2: TC04 Delete failed — "element is not visible" | Delete-submenu xpath `//ul[…ui-menu-child]//a[.='MIME Type Mapping']` also matched the **Insert** submenu's identically-named (hidden) item | Scope the click to the delete menu-parent: `//li[…ui-icon-delete]//ul[…ui-menu-child]//a[.='MIME Type Mapping']` |

---

## 4. TEST EXECUTION

### 4.1 Playwright (`ec_iud_mime.py`, test row `application/x-ec-autotest`)
| Run | Mode | Result | DB evidence |
|---|---|---|---|
| 1 | full | INSERT/UPDATE false-PASS, DELETE fail | DB still 0 rows → exposed the `fill()`/pagination bug (see §3.2 #1) |
| 2 | insert-only | INSERT **PASS** | base table 89 → **90** (persisted) |
| 3 | delete-only | DELETE **PASS** | base table 90 → **89** (physically gone) |
| 4 | full | **ALL PASS** | 89 → 90 (insert) → updated → 89 (delete); existing 89 untouched |

### 4.2 Robot Framework (`ec_iud_mime.robot`, self-cleaning test row `application/x-ec-autotest-rf`)
| Run | Result | Notes |
|---|---|---|
| 1 | 0/4 | `arguments` JS error (§3.2 #2) |
| 2 | 3/4 | TC01–03 PASS; TC04 delete xpath matched insert submenu (§3.2 #3) — left row in DB; **cleaned up** via Playwright delete-only |
| 3 | **4/4 PASS** | TC01 clean → TC02 insert → TC03 update → TC04 physical delete; **self-cleaned** — DB back to 89, no test row left |

**Final DB state:** `CTRL_MIME_TYPE_MAPPING` = 89 rows, `TV_CTRL_MIME_TYPE_MAPPING` = 89 rows, 0 autotest rows. **No existing data touched.**

---

## 5. COMPLETION CRITERIA
| Deliverable | Status |
|---|---|
| Playwright script (`ec_iud_mime.py`) | ✅ ALL PASS |
| Robot Framework suite (`ec_iud_mime.robot`) | ✅ 4/4 PASS |
| DB verification (TV + base table; true delete confirmed) | ✅ physical delete confirmed |
| Screenshots evidence | ✅ committed: `docs/EC/screenshots/iud_mime/` (14) + `recon_mime_type_mapping/` (1). RF reports in `tmp/rf_mime/` are scratch (not backed up). |
| SOW updated with final results + Lessons Learned | ✅ this doc (v2.0) |
| `mime-type-mapping-iud/` folder (README, requirements, repo-relative paths) | ✅ packaged |
| Committed + pushed | ✅ 8be581a (deliverable) + ddae059 (evidence), pushed to master |

---

## 6. RISKS / UNKNOWNS (resolved in §3 scan)
| Risk | Mitigation |
|---|---|
| Exact inline-cell input IDs unknown | Phase scan (DOM deep-dive) before automation |
| Insert mechanism (inline row vs popup) | scan the Insert → "MIME Type Mapping" action |
| Delete mechanism (toolbar vs submenu) + real-delete confirmation | scan + DB-verify base table |
| MIME_TYPE natural-key duplicate handling on re-run | use fresh/cleaned test value; cleanup if pre-exists |
| Stuck manipulating screen items | **scan + DOM deep-dive, or KB; escalate if >8 tries** |

## 7. CONFIDENCE (pre-execution vs actual)
**Pre-execution:** ~75–80% to ALL-PASS; fewer iterations than Bank expected (no navigator/object form/dates).
**Actual:** ALL PASS in **both** frameworks. The pre-task estimate held — but the one place it *under*-estimated was the inline-cell **commit mechanism** (the `onchange→PrimeFaces.ab` partial submit). Pagination + the synthetic-event no-op cost the iterations, not the cell IDs.

---

## 8. LESSONS LEARNED

1. **Verify at the DB, not the green UI** *(recurring meta-lesson, 3rd instance).* The Playwright run-1 UI reported INSERT/UPDATE PASS while the DB held **0** rows. A confirmation toast / clean grid is not proof — the row count in `CTRL_MIME_TYPE_MAPPING` is.
2. **PrimeFaces inline cells commit via `onchange→PrimeFaces.ab`.** `el.fill()` and synthetic `dispatchEvent('change')` do **not** stage the value server-side. You must drive **real keystrokes + a real blur (`Tab`)** and then wait for the AJAX, or Save commits nothing.
3. **Reload before verifying.** After Save, click **Refresh** so the grid reflects the DB rather than stale client state — otherwise the verification reads the optimistic client value.
4. **The grid is paginated (~20/page).** "Compare the visible rows" is an invalid integrity check on a paginated table — it false-alarmed on run 1. Row lookup must page (first → next…) and integrity must be a DB row-count comparison.
5. **Table class (TV) delete is physical.** Unlike the OV/Manage-Object pattern (Bank/Equipment) where delete = End Date = Start Date (date-effective true delete), a Table class row is `DELETE`d outright from the base table. No versioning, no dates.
6. **Watch for identically-named menu items across toolbar actions.** The Insert and Delete submenus both expose a "MIME Type Mapping" item; a global xpath matched the hidden Insert one. **Scope submenu clicks to their menu-parent.**
7. **Browser-library `Evaluate JavaScript`:** arrow functions have no `arguments`; embed values via RF variable substitution into the JS literal (or use the documented arg signature) — don't reference `arguments[0]`.
8. **Self-cleaning RF suite design works well:** TC01 asserts clean → TC02 insert → TC03 update → TC04 delete leaves the DB exactly as found (89 rows). When a mid-run failure leaves a row behind (RF run 2), the Playwright **delete-only** mode is the cleanup tool.
