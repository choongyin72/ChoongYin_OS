# Grid column-filter standardization — screen tracking checklist

_Created 2026-08-23. Tracks which EC screens have had the Account/Bank-style grid
column-filter row-locate feature applied, so future sessions don't redo work on a
screen that's already done, and know exactly which are still pending._

## Background

Account's IUD suite (PR #422, 2026-08-22) originally hit a live failure because
`OV_FIN_ACCOUNT` has 110+ rows across a 20-row/page grid, and the test code sorted
onto a page beyond page 1 — the shared T1/T2 row-select/check keywords only ever
looked at the currently-rendered page. The fix used EC's own grid hamburger-menu
column filter (`resources/grid_menu.resource`, a server-side "contains" search
across the FULL dataset in one call) instead of walking pages.

Per owner direction ("can other screens (e.g. bank, list_object) also use filter
too... standardise it" → "same to other ec screens"), this was generalized in two
layers, both in **PR #423** (`feature/ov-grid-filter-standardize`):

1. **Implicit fallback (applies automatically, zero code change per screen)** —
   `resources/manage_object.resource`'s `Select Object Row` / `OV Row Should Exist` /
   `OV Row Should Not Exist` try the fast direct-click/current-page path first, and
   only fall back to filtering if the row isn't found within 3s (or, for absence
   checks, always prefer the filter-based full-dataset check when the grid supports
   it). **This already applies to every OV screen using `manage_object.resource`,
   whether or not it appears in the "explicit" table below.**
2. **Explicit `Find <Screen> Row By Filter` / `Clear <Screen> Row Filter` wrappers**
   — thin T3 keywords calling the shared T2 `Find Object Row By Filter` /
   `Clear Object Row Filter`, wired directly into Update/Find/Verify-Found/Delete so
   the filter fires deliberately, not just as a fallback. This is what the table
   below tracks — it only applies to screens already rebuilt to the label-driven,
   T2-consolidated pattern (the "Bank pattern"), since that's the shape these
   wrapper keywords slot into.

**Deliberately NOT wired into `Verify <Screen> Record Removed`/`Does Not Exist`** on
any screen — those already get a filter-based full-dataset absence check for free
via the shared T2 `OV Row Should Not Exist` (layer 1 above), so an outer explicit
wrap there would be pure redundant duplication with no behavior change.

## Screens eligible for the explicit wrapper (rebuilt to the Bank-pattern T2-consolidated shape)

| Screen | Explicit filter wired? | Notes |
|---|---|---|
| Bank | ✅ DONE (2026-08-23) | Small/single-page grid — filter fires but narrows to 1 row instantly either way. Verified live 5/5, filter keywords confirmed fired via output.xml. |
| State | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired. |
| Object List | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired. |
| Account | ✅ DONE (2026-08-22, PR #422 + #423) | The original screen this fix was built for — 110+ rows/6 pages, genuinely needs it. `Find/Clear Account Row By Filter` were the FIRST version of this pattern, later promoted into shared T2 and Account's own T3 updated to delegate to the promoted keywords (commit a9a36cd9). |
| Cost Centre | ✅ DONE (2026-08-23) | Custom-URL OV, small grid. Live 5/5, filter confirmed fired. |
| Revenue Order | ✅ DONE (2026-08-23) | Custom-URL OV, small grid. Live 5/5, filter confirmed fired. |
| WBS | ✅ DONE (2026-08-23) | Custom-URL OV, small grid. Live 5/5, filter confirmed fired. |
| Payment Scheme | ✅ DONE (2026-08-23) | Manage-object OV. Live 5/5, filter confirmed fired. |
| Exchange Rate Source | ✅ DONE (2026-08-23) | Manage-object OV. Live 5/5, filter confirmed fired. |
| Region | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired (output.xml). |
| Functional Area | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired. |
| Business Unit | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired. |
| Production Unit | ✅ DONE (2026-08-23) | Small grid. Live 5/5, filter confirmed fired. |
| Company | ✅ DONE (2026-08-23) | Large PAGINATED grid (8 pages, hundreds of rows) with a prior non-reproducible TC05 flake on its first-ever live build - the strongest real candidate in this whole set for actually needing the filter, not just consistency. Live 5/5 clean on this run (no flake), filter confirmed fired. |
| Country | ✅ DONE (2026-08-23) | Small grid (20 rows). Batch-2 rebuild, filter wiring included from the start (not deferred as a follow-up). Live 5/5, filter confirmed fired exactly 5 times via output.xml grep (Update/Find/Verify-Insert-Exists/Verify-Found/Delete). |
| County | ✅ DONE (2026-08-23) | Manage-object OV, small grid (batch-2 conversion, parallel worker clone). Live 5/5, filter confirmed fired (5 hits for `Find County Row By Filter` in output.xml). |
| Currency | ✅ DONE (2026-08-23) | Manage-object OV, small grid. Batch-2 5-screen Bank-pattern conversion (Country/County/Regulatory Permits/Currency/VAT Code). Live 5/5, filter confirmed fired (5 hits in output.xml for `Find Currency Row By Filter`). Also confirmed live: the registry-flagged mandatory "Active" checkbox (`MandatoryCellStyleWhite` class) is NOT actually save-blocking - a checkbox has no "empty" state, so it's omitted from the insert properties (see currency_insert.properties). |
| VAT Code | ✅ DONE (2026-08-23, PR #431) | Manage-object OV, small/single-page grid (15 rows). Wired in from the start (batch-2, not a follow-up). Live 5/5, filter keyword confirmed fired 7x via output.xml grep. |
| Regulatory Permits | ✅ DONE (2026-08-23, batch-2) | Custom-URL OV (grid `nav:form:T_data`, WITH a GO button unlike Account/Cost Centre - confirmed live, a shape not seen elsewhere). Small grid, currently 0 rows on this sandbox. Live 5/5, filter confirmed fired (7 hits in output.xml). |
| Customer | ✅ DONE (2026-08-23, batch-3) | Manage-object OV, small grid (Commercial Objects). Batch-3 5-screen Bank-pattern conversion (Customer/Field Group/Licence/MMS Lease/Operator Lease, parallel isolated clones). Wired in from the start. Live 5/5, filter keyword confirmed fired 5x via output.xml grep. |

**20 of 20 done.** All 5 batch-2 screens (Country, County, Currency, VAT Code,
Regulatory Permits) and Customer (batch-3, 1st of 5 landed so far) are in.
Every screen already rebuilt to the Bank-pattern T2-consolidated shape now has
the explicit filter wiring. Any FUTURE screen rebuilt to this pattern should
get the same treatment as part of its own build (see "How to update this doc"
below).

## Screens NOT yet eligible (still on the older pre-Bank-pattern shape)

The ~80 other OV/OV-GM screens listed in `docs/ec_screen_registry.md` have not been
rebuilt to the label-driven, T2-consolidated pattern yet (they predate this
session's Bank-pattern conversion work). They don't have `Find/Clear Object Row By
Filter`-compatible T3 wrapper keywords to wire this into — that would require
rebuilding them to the Bank pattern FIRST (a separate, larger task), not just
retrofitting the filter. **Do not attempt to add filter wiring to a screen still on
the old pattern without rebuilding it first** — check this doc's "eligible" table
above before starting, and check `docs/ec_screen_registry.md` for the screen's
current pattern if it's not listed here at all.

## How to update this doc

When a new screen's T3 gets rebuilt to the Bank pattern, add it to the eligible
table above as "⬜ NOT YET DONE". When a screen gets the explicit filter wrapper
added (following the exact pattern in `bank_page.resource`/`account_page.resource`
— `Find <Screen> Row By Filter`/`Clear <Screen> Row Filter` wired into
Update/Find/Verify-Found/Delete, NOT into Removed/Does-Not-Exist), flip it to
"✅ DONE (date)" with a one-line note. Append-only in spirit — don't delete rows for
screens that get superseded/retired, just note it.
