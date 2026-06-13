# EC Sales — domain dive 3 (2026-06-13, local sandbox)

Sources: menu walk (`ec_sales_branch.txt`, 165 nodes) · DB counts · DOC-05A.

## 1. Menu shape — three pillars
- **Sales Dispatching**: Daily Gas Sales Forecast → Daily Nomination / Re-Nomination →
  Daily/Monthly Delivery (+Profit-Centre splits), availability, targets (Before/Within
  Day), NGL/Wet-Gas exports. = the daily gas commercial operations loop.
- **Price Determination** (the biggest sub-branch, ~35 screens): Price Indices
  (daily/sub-daily/monthly/yearly ±dataset ±price-object), Price Rates, Product/Contract/
  Cargo Price Lists, Price Components, Price Calculations. = price engine around
  Price Concept → Price Object → calc rule sets.
- **Sales Allocation**: Daily/Monthly/Yearly Contract Calculations (±by Contract),
  Contract Account Status/Events, allocation adjustments. = contractual-commitment
  follow-up on Contract Accounts.

## 2. Sandbox data
| Family | Rows | Meaning |
|---|---|---|
| PRICE_IN_ITEM_VALUE 2.6k, PRICE_* lists/indices | ✅ | price engine seeded |
| PRODUCT_PRICE(+VALUE) 251/404 | ✅ | product price lists |
| CNTRACC_PER_* (status + DIMn allocs) ~7k | ✅ | contract-account results computed |
| CNTR_SUB_DAY_STATUS 491k (see transport.md) | ✅✅ | sub-day contract statuses — gas nominations grain |
| NOMPNT_DAY_NOMINATION 4.2k | ✅ | nominations vs our Dispatching objects |

## 3. Core flow
```
Contract (+ accounts, attributes) ──┐
Price indices (daily feeds) ─→ Price Calculations ─→ Contract/Product Price Lists
Nominations (daily/renom) ─→ Deliveries (daily→monthly) ─┤
                                                         └─→ Sales Allocation
                                  (calc rule sets per Contract Account, equations)
                                  → CNTRACC_* quantities/statuses (D/M/Y)
                                  → replicate to Revenue (IFAC_SALES_QTY; monthly only,
                                    needs revn_ind=Y + interface_to_revenue=Y)
```

## 4. Candidate business test cases
1. **Nomination → delivery chain**: enter Daily Nomination → confirm → Daily Delivery
   reflects nominated qty; renominate → assert revision trail.
2. **Price math**: set a Daily Price Index value → run Price Calculation → assert
   Contract Price List = index × formula (oracle = the rule equation).
3. **Contract account calc**: known deliveries → run Daily Contract Calculation →
   assert CNTRACC quantity (e.g. Take-or-Pay accumulation).
4. **Sales→Revenue gate**: account without interface_to_revenue=Y → assert NO
   IFAC_SALES_QTY rows; enable → monthly replicate → assert rows.

## 5. Open questions
- Pluto's sales scope: LNG cargo sales (→ Transport/cargo pricing) vs pipeline gas
  (→ nominations)? Which contract types are configured in As-Built?
