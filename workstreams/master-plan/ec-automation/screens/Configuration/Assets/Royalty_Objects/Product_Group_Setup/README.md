# Product Group Setup — EC IUD bundle

**Screen:** Configuration > Assets > Royalty Objects > **Product Group Setup**
**Pattern:** 3-tier master → detail → sub-detail, **no navigator**, tab-gated multi-entity toolbar.
The most complex screen of the Royalty batch — **all 3 sub-entities** automated with full I-U-D.

```
Product Group (top grid nav:form:T_data — click a row; no GO)
  └─ Product Group Setup  = products in group (middle prod_group_setup:form:T_data)  [select a product]
       ├─ COSTS tab            = Product Group Cost   (DV_PRODUCT_GROUP_COST)
       └─ Stream Calc Category = PRODUCT_STRM_BAL_CAT (label "Calculation" != table "Balance Category")
```

## Maintained RF suite (the proof) — live 10/10, DB-verified, self-cleaning
- Suite: `tests/Configuration/Assets/Royalty_Objects/product_group_setup_iud.robot` (10 TCs)
- Page object (T3): `pageobjects/Configuration/Assets/Royalty_Objects/product_group_setup_page.resource`
- TC01 clean · TC02-03 Setup I/U · TC04-05 Cost I/U · TC06-07 SCC I/U · TC08-10 deletes (child→parent)
- Each entity row carries a unique COMMENTS sentinel verified via `Code Should Be Present/Absent In View`.

## Run
```bash
EC_HEADLESS=false py -m robot --outputdir results \
  tests/Configuration/Assets/Royalty_Objects/product_group_setup_iud.robot
```

## Test data (pre-flight verified 2026-06-27)
Group `ALL_GENERAL` · product **Chemical Product** (not in the group, offered in dd) · Cost Type
**Brokerage Fee** · SCC Category **Total Production** · date 2011-01-01. All sentinel baselines 0.

## Gotchas (the three that cost live runs — all fixed)
1. **label ≠ table:** SCC tab "Stream Calculation Category" → table `PRODUCT_STRM_BAL_CAT` (Balance Category).
2. **Silent reject:** Setup/Cost inserts need mandatory cells filled (Setup Sort Order C2; Cost Sort C2 +
   Cost Column C4) = UI-yellow ∪ DB-NOT-NULL, else the row shows in UI but never hits the DB.
3. **Save won't re-arm** for a 2nd edit on a loaded form → `Enter Context` re-selects group+product+tab to
   reload a fresh form before every Update/Delete (this also cleared the "flaky" Delete-menu pollution).

## Contents
| Path | What |
|---|---|
| `product_group_setup_sow.md` | SOW — classification, per-entity layout, dev story, lessons |
| `FINDINGS.md` | the read-only recon deep-dive |
| `investigation/` | recon + pre-flight + resolve scripts |
| `evidence/` | 10 step screenshots from the green run |
