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
| Region | ⬜ NOT YET DONE | Rebuilt to Bank pattern (PR #412), eligible for this wiring - not yet actioned. |
| Functional Area | ⬜ NOT YET DONE | Rebuilt to Bank pattern (PR #413), eligible - not yet actioned. |
| Business Unit | ⬜ NOT YET DONE | Rebuilt to Bank pattern (PR #414), eligible - not yet actioned. |
| Production Unit | ⬜ NOT YET DONE | Rebuilt to Bank pattern (PR #415), eligible - not yet actioned. |
| Company | ⬜ NOT YET DONE | Rebuilt to Bank pattern (PR #416); its own scorecard entry already flags a large PAGINATED grid (8 pages) with a prior non-reproducible TC05 flake - a strong candidate to prioritize, since it's the one screen in this remaining group most likely to actually need the filter (not just get it for consistency). |

**9 of 14 done.** Remaining 5 (Region, Functional Area, Business Unit, Production
Unit, Company) are the next candidates if this standardization continues.

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
