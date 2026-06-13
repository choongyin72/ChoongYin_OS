# EC Revenue — domain dive 4 (2026-06-13, local sandbox) — DRAFT

Sources: menu walk (`ec_revenue_branch.txt`, 82 nodes) · DB counts · DOC-05B.

## 1. Menu shape
- **Quantity** (Daily/Monthly/Forecast): Stream Items — the unit of quantity Revenue tracks
  (VO.* screens, month-by-day tabs, accruals ACCRUAL→FINAL).
- **Financial Transaction**: Document Finder, Period/Cargo/ERP Documents, Payment Tracking,
  Interface Files, Validation. = the invoicing/document engine.
- **Inventory**: validation/setup/process + transactional inventory.
- **Data Mapping**: Project Data Entry/Mapping/Extract (±accrual, ±10yr) + Cost of Service.
- **Royalty**: Canada + USA sub-branches (jurisdictional royalty engines).
- **Closing Process**: Revenue Lock Module, Booking/Reporting Period close + re-open.
- **Financial Item**: definitions/templates + D/M/Y values & calculations (monetary values
  against ANY EC object).
- Document Tracing + Visual Tracing (lineage), Revenue Logs.

## 2. Sandbox data
FIN_ITEM_ENTRY 486 · FIN_COST_CENTER 241 · FIN_ACCOUNT 110 · DOC_DATE_TERM 134 ·
DOC_TEMPL_REPORT_SETUP 70 — config + modest transactional seed; document tables (PDG/CDG)
to be checked in the deep pass. Lighter than Production/Transport: Revenue on this sandbox
is mostly configured-but-not-heavily-run.

## 3. Core flow
```
Stream Item quantities (daily→monthly; from Production allocation + Sales replication
  IFAC_SALES_QTY + Transport cargo quantities)
  └─ accruals when actuals missing (RUN ACCRUAL → ACCRUAL → FINAL)
Documents generated (Period/Cargo Document Generation)
  └─ validation lifecycle: OPEN → VALID1 → VALID2 → TRANSFER (booking period set) → BOOKED
  └─ ERP interface (transfer batches, accrual reversals)
Closing: all docs BOOKED → close Booking Period → close Reporting Period → Revenue Lock
Royalty: jurisdiction engines compute crown/owner shares from allocated volumes × prices
```
Third status machine learned: OPEN→BOOKED (after P/V/A and T/R/C/A) — Revenue's spine.

## 4. Ties to our work
- Financial Objects screens (Assets) we automated = this domain's master data (accounts,
  cost centres, VAT, exchange rates...). Financial Posting Setup (dependency screen,
  FULL IUD per user) configures posting here.
- CSDV (client-side data validation, zones green/orange/red) = the validation layer our
  Issue_1052 checks complement; regenerated via BUILDVIEWLAYER (View Generator spine!).

## 5. Candidate business test cases
1. **Document lifecycle**: generate period doc → walk OPEN→VALID1→VALID2→TRANSFER→BOOKED,
   assert status + booking period at each step; assert edit-lock after TRANSFER.
2. **Closing gate**: leave one doc unBOOKED → attempt booking-period close → assert refusal.
3. **Accrual flip**: month with missing actuals → RUN ACCRUAL (last-actual method) → assert
   ACCRUAL values = previous actual; load actuals → TO FINAL → assert FINAL.
4. **CSDV zones**: stream item with limits → enter warning-zone value (saves, yellow) vs
   red-zone (blocked unless Conditional) — UI-level validation test.

## 6. Open questions
- Pluto: which document types/ERP interface are in As-Built scope (SAP?); royalty likely
  N/A for Australia? (check As-Built)
