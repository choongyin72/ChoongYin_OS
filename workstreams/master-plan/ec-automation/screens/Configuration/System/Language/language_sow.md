# EC Screen IUD Operation Test — Language — Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Task:** EC Language screen Insert/Update/Delete (IUD) Automation
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-08
**Version:** 1.0 — **COMPLETE** (RF + Playwright, DB-verified)
**Pattern:** **Table class (TV view)** — 2nd Table-class screen (confirms the pattern with MIME)

---

## 1. REQUIREMENT
Automate Insert / Update / Delete on the EC **Language** screen (Configuration → System):
1. Create a new language (Id + Language code + Name)
2. Modify a language's Name
3. Delete a language
4. Existing data integrity — the 8 standard languages untouched

**Constraints:** never modify existing rows; local sandbox; DB-verified at `localhost:1521/ORCL`.

**Acceptance:** INSERT row present in grid + base table; UPDATE persisted; DELETE **physically removed** from `T_BASIS_LANGUAGE`; existing 8 rows intact.

---

## 2. DESIGN
| Property | Value |
|---|---|
| Screen | Language (Configuration → System) |
| Screen type | **Table class (TV)** — inline-editable grid, **no navigator** |
| Grid | `table:form:T_data`; cells `table:form:T:{row}:C0_in` (Id), `C1_in` (Language code), `C2_in` (Name) |
| Toolbar | Save, Refresh, Insert (→ "Language"), Delete (→ "Language") |
| Base table | `T_BASIS_LANGUAGE` — `LANGUAGE_ID` (numeric, PK), `LANGUAGE VARCHAR2(255)` (code), `NAME VARCHAR2(32)` |
| Delete | **physical** row removal (table classes are not date-effective) |

**IUD flow:** Insert toolbar → blank grid row → fill **Id (required)** + Language + Name (real keys + Tab) → Save → Refresh. Update = edit Name cell. Delete = select row → Delete toolbar "Language" → Save → physically gone.

### ⚠️ Key mechanic (the gotcha)
The **Id (`LANGUAGE_ID`) cell is a mandatory (yellow) field** — it must be filled before Save. Leaving it blank triggers a *"Required fields are empty: Id[LANGUAGE_ID]"* validation error (a grey overlay that blocks further clicks — **not** a confirmation dialog). EC marks mandatory cells **yellow**.

---

## 3. DEVELOPMENT
| Artifact | Purpose |
|---|---|
| `pageobjects/Configuration/System/language_page.resource` (T3) | locators + IUD wrappers (fills required Id; finds by Language code C1) |
| `tests/Configuration/System/language_iud.robot` | RF suite TC01–04, in-suite DB assertions |
| `resources/table_class.resource` (T2) | shared Table-class flow (Insert row / Delete row) — **promoted** from MIME for this 2nd Table-class screen |
| `playwright/ec_iud_language.py` | standalone Playwright implementation |
| `investigation/` | recon: `language_inspect.py` (DOM), `db_find_language.py` (schema), `recon_language_confirm.py` (the required-field discovery) |

---

## 4. TEST EXECUTION
| Tool | Result | DB evidence |
|---|---|---|
| Robot Framework (`language_iud.robot`) | **4/4 PASS** (headless) | in-suite: present in `T_BASIS_LANGUAGE` after insert; **gone** after physical delete |
| Playwright (`ec_iud_language.py`) | **ALL PASS** (headed + headless) | `T_BASIS_LANGUAGE` 8 rows, no residue |

**Final DB state:** `T_BASIS_LANGUAGE` = 8 rows, no `ZZ` test row. No existing data touched.

---

## 5. COMPLETION
| Deliverable | Status |
|---|---|
| RF suite (T3 page object + test) | ✅ 4/4 |
| Playwright impl | ✅ ALL PASS |
| T2 `table_class.resource` promotion (+ MIME re-verified) | ✅ 8/8 System |
| DB ground-truth (physical delete) | ✅ |
| `screens/` bundle (SOW, README, playwright, investigation, evidence) | ✅ |
| Robocop clean · committed | ✅ |

---

## 6. LESSONS LEARNED
1. **Yellow cell = mandatory field** — fill all required (yellow) cells before Save. The blocking "modal" was a *required-fields validation error*, not a confirmation. (Verify-at-DB caught the false "insert PASS": the grid showed an unsaved row while the DB had none.)
2. **Physical-delete (Table-class) screens are repeatable with fixed test data** — delete fully removes the row, so a fixed `ZZ`/`999` test row self-cleans (no unique-per-run needed, unlike the OV screens whose codes linger).
3. **2nd Table-class screen → promote the pattern to T2** — `table_class.resource` now shared by MIME + Language (Insert/Delete grid-row flow, with the delete submenu label parameterized).
4. **Match relative-import depth to the menu path** — System is one level shallower than Assets/<Group>, so imports use `../../../` (3), not `../../../../` (4).
