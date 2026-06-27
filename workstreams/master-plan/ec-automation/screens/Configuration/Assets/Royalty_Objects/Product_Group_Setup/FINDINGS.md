# RC.0054 Product Group Setup — recon FINDINGS (2026-06-27)

**Status:** Phase-1 recon COMPLETE. Setup + Cost fully mapped + DB-backed (ready to build).
**Stream Calculation Category = PARKED** (genuine blocker — see §SCC). Build scope for v1 =
**Product Group Setup + Product Group Cost** (DB-verified); SCC pending a backing source.

## Screen shape (data-confirmed)
3-tier master → detail → sub-detail, **no navigator** (top grid is the object list):
```
Product Group (top grid nav:form:T_data — click a row to select; NO date/dd/GO)
  └─ Product Group Setup  = products in group   (middle grid prod_group_setup:form:T_data)   [select a product row]
       ├─ COSTS tab (tab1_header)              = Product Group Cost  for that product
       └─ Stream Calc Category tab (tab2_header) = SCC for that product
```
- **Tab-gated Insert/Delete** (confirmed): Setup always enabled; **Cost** enabled when COSTS/middle active; **SCC** enabled ONLY when the SCC tab is active. Activate the target tab before Insert/Delete.
- Cost + SCC rows are scoped to the **selected product** in the middle grid (per-product), not just the group.

## Entity 1 — Product Group Setup (middle grid)  ✅ READY
- Grid `prod_group_setup:form:T_data`; toolbar Insert/Delete submenu label **"Product Group Setup"**.
- Cells: C0_da=Start, C1_da=End, **C2_in=Sort Order**, **C3_dd_input=Product** (member; opts Air/Bitumen/Blend/Butane/C2_Ethane…), C4_dd=Default UOM, C5_in=Product Column, C6_in=Price Column, C7_cb=Negative, C8_cb=Master, C9_cb=Apply Imbalance, **C10_in=Comments**.
- Backing `DV_PRODUCT_GROUP_SETUP` (OBJECT_CODE=group, PRODUCT_CODE=member, COMMENTS, SORT_ORDER).
- **Oracle:** PRODUCT_CODE is NOT unique across groups → verify via a unique **COMMENTS sentinel** (C10_in) using `Code Should Be Present/Absent In View    DV_PRODUCT_GROUP_SETUP    <sentinel>`. No shared-file edit.

## Entity 2 — Product Group Cost (COSTS tab)  ✅ READY
- Grid `product_group_sub:tabPanel:prod_group_cost:form:T_data`; Insert/Delete submenu **"Product Group Cost"** (enable COSTS tab first).
- Cells: C0_da=Start, C1_da=End, **C2_in=Sort Order**, **C3_dd_input=Cost Type** (opts Purchase Cost/Total Royalty Transport/Revenue/Value/Transportation Royalty/Transportation Financial/Storage Cost/Opex - Workforce/Opex - Workovers/Royalty Payment/Brokerage Fee), C4_in=Cost Column, C5_in=Price Column, C6_cb=Apply to Value (SUM_VALUE_COST_IND), C7_in=Comments.
- Backing `DV_PRODUCT_GROUP_COST` (OBJECT_CODE=group, PRODUCT_CODE=selected product, COST_TYPE, …, COMMENTS) — per-product (25 rows under TIETO_BLEND incl BITUMEN/BLEND).
- **Oracle:** COMMENTS sentinel (C7_in) present-in-view on `DV_PRODUCT_GROUP_COST`.

## SCC — PARKED (blocker)
- Grid exists (`product_group_sub:tabPanel:strm_calc_cat:form:T_data`); Insert enables when the SCC tab is active.
- **No DB backing found** after 5 read-only angles: object names (`%STRM_CALC%`/`%SCC%`/`%CALC_CAT%`/`%STREAM_CALCULATION%`), columns, class_cnfg class names, class_property_cnfg LABELs, and property_value referencing `strm_calc_cat` — all empty. Cost-Type-style reference views also absent.
- The SCC Insert gesture timed out in recon (menu/grid behaves differently).
- ⇒ Cannot establish DB ground-truth (hard rule) → **PARKED pending a backing source** (ask the EC config / As-Built for the Stream Calculation Category table behind the Product Group SCC tab). Do NOT silently drop; revisit with the backing identified, or deliver UI-verified-only if the user accepts that caveat.

## Test design (Setup + Cost, self-cleaning, never touch existing)
- Group: a loaded group (e.g. `ALL_GENERAL`); test product NOT already in it (confirm at build, e.g. METHANE).
- Setup: insert product membership (unique COMMENTS sentinel) → update COMMENTS → delete; count/sentinel deltas.
- Cost: select the product → COSTS tab → insert a cost row (Cost Type + unique COMMENTS sentinel) → update → delete.
- Date 2011-01-01. Independent DB re-read confirms existing group rows intact.

## Key ids (for the build)
- top grid `nav:form:T_data` (click row by group code) · middle `prod_group_setup:form:T_data`
- tabs `product_group_sub:tabPanel:tab1_header` (COSTS) / `tab2_header` (SCC)
- cost grid `product_group_sub:tabPanel:prod_group_cost:form:T_data`
- Insert toolbar parent: `//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]`
