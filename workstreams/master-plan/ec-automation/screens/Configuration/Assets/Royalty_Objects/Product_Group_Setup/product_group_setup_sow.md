# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete Automation — Product Group Setup (3 sub-entities)
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-27
**Version:** 1.0 — COMPLETE (RF suite, live 10/10 + DB-verified, self-cleaning)

---

## 1. REQUIREMENT
Automate full Insert/Update/Delete for ALL THREE sub-entities of the Product Group Setup screen and
prove each at DB level. The most complex screen of the Royalty batch: 3-tier master->detail->sub-detail,
no navigator, multiple insert entities, tab-gated toolbar. NEVER modify existing data — the test adds a
new product to an existing group plus a cost + a stream-calc-category under it, then removes everything.

| Operation | Entity | Pass condition | Status |
|---|---|---|---|
| INSERT / UPDATE / DELETE | Product Group Setup | row + DB sentinel in `DV_PRODUCT_GROUP_SETUP` | PASS (TC02/03/10) |
| INSERT / UPDATE / DELETE | Product Group Cost | row + DB sentinel in `DV_PRODUCT_GROUP_COST` | PASS (TC04/05/09) |
| INSERT / UPDATE / DELETE | Stream Calc Category | row + DB sentinel in `PRODUCT_STRM_BAL_CAT` | PASS (TC06/07/08) |
| CLEANUP | all | zero leftover; ALL_GENERAL back to its original 7 products | PASS |

## 2. DESIGN

### 2.1 Screen classification — 3-tier PC (master -> detail -> sub-detail), tab-gated, NO navigator
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Royalty Objects > Product Group Setup |
| Tier 1 (parent) | top grid `nav:form:T_data` = Product Groups; **click a row to select (no date/dd/GO)** |
| Tier 2 (detail) | middle grid `prod_group_setup:form:T_data` = products in the group; select a product row |
| Tier 3 (sub-detail) | bottom TABS: COSTS `…tab1_header` (`prod_group_cost`) + Stream Calc Category `…tab2_header` (`strm_calc_cat`) — scoped to the selected product |
| Insert/Delete | TAB-GATED submenu: Product Group Setup / Product Group Cost / Stream Calculation Category — an entity is selectable only when its section/tab is active |
| Delete semantics | PHYSICAL row delete |

### 2.2 Per-entity layout + backing (recon-confirmed)
| Entity | Grid cells | Backing | NOT-NULL (fill on insert) |
|---|---|---|---|
| Setup | C2_in Sort, **C3_dd Product**, C4_dd UOM, C5/C6 cols, C7/8/9 cb flags, **C10_in Comments** | `DV_PRODUCT_GROUP_SETUP` (OBJECT_CODE=group, PRODUCT_CODE=member) | DAYTIME, PRODUCT_ID (+ UI-yellow Sort Order C2) |
| Cost | C2_in Sort, **C3_dd Cost Type**, C4_in Cost Column, C5_in Price Column, C6_cb Apply-to-Value, **C7_in Comments** | `DV_PRODUCT_GROUP_COST` (per-product) | COST_TYPE, **COST_COLUMN (C4)**, **SORT_ORDER (C2)** |
| SCC | **C2_dd Category**, **C3_in Comments** | `PRODUCT_STRM_BAL_CAT` (per-product) | STRM_BAL_CATEGORY (C2) |

⚠️ **The SCC tab is labelled "Stream Calculation Category" but its table is the Stream BALANCE Category
(`PRODUCT_STRM_BAL_CAT`)** — label != table. This cost ~5 failed DB-name searches before the grid id
(`strm_calc_cat`) + a broad search surfaced `PRODUCT_STRM_BAL_CAT`.

### 2.3 Verification oracle
`PRODUCT_CODE` / `COST_TYPE` / category are not unique across groups, so each test row carries a unique
**COMMENTS sentinel** (`AUTOTEST_PGS_*`) verified with `Code Should Be Present/Absent In View` (string-
column scan) on the entity's backing — no shared-file / DbVerify change needed.

### 2.4 Test data (pre-flight verified 2026-06-27)
Group `ALL_GENERAL`; test product **Chemical Product** (in OV_PRODUCT, NOT in ALL_GENERAL, offered in the
dd); Cost Type **Brokerage Fee**; SCC Category **Total Production**; date 2011-01-01. All sentinel baselines 0.

## 3. DEVELOPMENT — what it took (2026-06-27)
- 4 recon passes mapped the 3-tier structure, the tab-gated Insert/Delete, all 3 grids' cells + member
  dropdowns, and resolved the SCC backing (label != table).
- **Live run #1** (4/10): inserts "succeeded" in UI but DB-failed = EC **silent reject** — the Setup/Cost
  rows need mandatory cells (Sort Order, Cost Column) that the member+date+comment fill omitted. Fixed via
  `Fill New Row Fields` (the mandatory set = UI-yellow union DB-NOT-NULL).
- **Live run #2** (4/10 — TC01-04): updates failed with **Save disabled** = EC does not re-arm Save for a
  2nd edit on a still-loaded form; the failed update then polluted the screen and the deletes cascaded.
- A read-only diagnostic proved the Delete menu opens cleanly in a fresh state -> the delete "blocker" was
  cascade pollution, not a real wall. Fixed via `Enter Setup/Sub Context` (re-select group+product+tab to
  reload a fresh form before every Update/Delete).
- **Live run #3: 10/10 PASS**, all entities DB-verified, self-cleaning. Independent re-read: all backings 0,
  ALL_GENERAL back to its original 7 products.

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| robocop / dryrun | — | clean / 10/10 |
| RF live #1 | headless | 4/10 -> silent-reject diagnosed (mandatory cells) |
| RF live #2 | headless | TC01-04 PASS -> 2nd-save-no-rearm diagnosed (reload) |
| RF live #3 | headless | **TC01-TC10 10/10 PASS** — 3 entities x I-U-D, DB-verified |
| Independent DB re-read | — | all sentinels 0; ALL_GENERAL = original 7 products |

## 5. DELIVERABLES
| Deliverable | Where |
|---|---|
| RF suite | `tests/Configuration/Assets/Royalty_Objects/product_group_setup_iud.robot` (10 TCs) |
| RF page object | `pageobjects/Configuration/Assets/Royalty_Objects/product_group_setup_page.resource` (generic kw + per-entity dicts) |
| Recon scripts | `investigation/` | 
| Evidence | `evidence/` (10 step screenshots) |
| Shared keywords reused (T2) | `Insert New Grid Row By Label`, `Find Grid Row By Cell Input Value`, `Delete Selected Grid Row`, `Type Cell By Id`; `Code Should Be Present/Absent In View` (DbVerify) |
| Registry / scorecard | rows appended |

## 6. LESSONS LEARNED
1. **label != table** — resolve a tab/grid's backing from its grid-id segment + broad search, not the UI label
   ("Stream Calculation Category" -> `PRODUCT_STRM_BAL_CAT`).
2. **Silent reject = fill UI-yellow ∪ DB-NOT-NULL** before Save (Sort Order, Cost Column), or the row shows
   in the UI but never reaches the DB.
3. **EC does not re-arm Save for a 2nd edit on a loaded form** — reload (re-select context) before each
   subsequent Update/Delete; this also clears the state pollution that made the Delete menu look "flaky".
4. **Diagnose before declaring a blocker** — a read-only menu probe showed the Delete gesture was fine;
   the failure was cascade pollution. Saved me from chasing a non-existent delete bug.
