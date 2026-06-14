# EFK Phase-1 — EC Sales + EC Revenue (the downstream half of the value chain)
Read 2026-06-13 from EC Knowledge (EFK): **EC Sales** `1838256` (2020) + **EC Revenue** `1840867`
(2018). Both are domain-overview parents (capability bullets + a sub-module map); the depth lives in
their children (ids captured below for on-demand drilling). Synthesized here to fill the series'
stated gap: *what makes a downstream test meaningful*. Completes the chain after Hydrocarbon
Accounting (allocation) — see [[reference_ec_multiclient_asbuilt]] and `calc-engine-insights.md`.

## The chain (where this sits)
**Production → Allocation (HA) → Sales → Revenue.** Allocation (N2/HA.0002, just automated) turns
measured field/stream totals into per-well/owner *quantities*. Sales commits those quantities to
buyers under contracts; Revenue turns delivered quantities into *money* and books it. EC's pitch:
"the only solution that addresses the complete value chain from reservoir to revenue."

## EC Sales (module capabilities — gas-trading centric)
- Manage **nominations / re-nominations / requests** per buyer, validated against **contractual terms**.
- Manage **gas availability** (own production, storage, balancing positions, substitution arrangements).
- Assess **contractual obligations vs availability**; handle **shortfall** situations.
- Place **shippers' nominations** to gas transport service operators.
- **Attribute actual deliveries to sales contracts** by priority + user-defined rules (← this is the
  sales analogue of allocation: a rules-driven assignment that a test could verify for conservation/
  priority-order, not just "a row saved").
- Full **contractual accounting** per clause: take-or-pay → carry-forward gas, make-up gas, shortfall
  allowances.
- **Pricing** in multiple currencies via published reference prices, CPI indexes, contract terms.

## EC Revenue (quantities → monetary value) — Business Areas
"Responsible for transferring quantities into monetary values"; covers valuation, invoicing,
accruals, prior-period adjustments, inventory valuation, UOP depreciation, forecasting/budgeting, and
a **bi-directional financial-accounting interface** (SAP, SUN, JD Edwards — updates EC booking status
on confirmation). Handles the hard upstream cases: **lifting agreements** between JV parties,
**royalty/PSA**, multi-product/multi-currency invoicing; SOX404 + full auditability.

| BA | Page id | Role |
|---|---|---|
| CD — Common Data | `1870092` | All revenue configuration |
| IN — Inventory | `1870077` | Revenue present in different storages |
| FT — Financial Transactions | `1870085` | Sales/Purchases/Tariff income+cost/Journal entries from qty + contract attrs |
| QTY — Quantities | `1870058` | Tracks quantities |
| FC — Forecast | `1870068` | Quantity + revenue forecasting |
| RTY — Royalty | `1854408` | Royalty contracts in revenue |
| FI — Financial Item | `11076130` (space RD120) | Stores monetary value (+ optionally qty) against ANY EC object (Field/Well/Stream/Facility/Tank/Pipeline) |

## Test-meaningfulness takeaways (the point of reading these)
- **Sales delivery attribution** is a rules+priority engine like allocation → a future "N-class" test
  pattern: run attribution, assert delivered-qty conserves to nominated/available, and priority order
  is honoured. Same shape as the N2 conservation oracle, different table.
- **Revenue = qty × price under contract clauses** → oracle candidates: invoice total =
  Σ(delivered_qty × applicable_price); take-or-pay carry-forward/make-up balances roll over correctly;
  JV lifting/royalty splits sum to 100%. These are *calculation* tests (like N2), not CRUD.
- **FI (Financial Item)** is the generic money-on-any-object table — the revenue analogue of the
  per-object day tables; worth a DB recon when a revenue test is in scope.
- All three modules are **contract-driven** — so a meaningful test needs a configured contract as
  fixture (the domain fact I'd otherwise lack). Flagged for the coverage track.

## Status / next
Both parents are thin overviews — captured. Deeper value is in the children (esp. Revenue FT/QTY/RTY
+ the Sales sub-modules) — drill **on demand** when a real sales/revenue test or As-Built question
arises. Next Phase-1 page in the series: **EC Regulatory Reporting** `1845940`, then the 3 link pages
(Chemistry/Environment/IAM).
