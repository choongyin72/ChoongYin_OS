# Bank-pattern conversion — screen tracking checklist

_Created 2026-08-23. Tracks which EC screens (with an EXISTING IUD suite already built,
just on the older hardcoded-field-id pattern) have been converted to the label-driven,
properties-file-driven, T2-consolidated "Bank pattern" — so future sessions know exactly
which screens are done, which are queued, and which are out of scope, without redoing the
survey each time._

## Background

Bank/State/Object List/Account/Cost Centre/etc. were rebuilt (2026-08-22/23) from an older
per-screen hand-coded pattern (hardcoded `objectForm`/`updateAttributes` field ids, bespoke
per-screen keywords, no properties files) to a shared, label-driven, T2-consolidated pattern
(`resources/manage_object.resource` keywords: `Insert/Update/Find/Verify Object *`,
`Delete Object Via End Date`), including the explicit grid column-filter row-locate wiring
(see `docs/grid-filter-standardization-checklist.md`). A full-repo survey (2026-08-23)
found **129 OV/OV-GM screens still on the old pattern with an existing IUD suite** already
built, split into:

- **48 "Tier 0" screens** — genuinely old pattern (hardcoded field ids in
  `objectForm`/`updateAttributes`) — **these are the real candidates for conversion**,
  tracked below.
- **80 "Tier 1" screens** — already label-driven via a SEPARATE Playwright/generator
  pipeline (`verify_screen.py`-gated, built in an earlier session) — structurally modern
  already, just not the RF Bank-pattern shape. Lower priority / arguably optional; NOT
  tracked in this checklist (a different, already-adequate pattern).
- **56 OV-GM screens** (gated navigator) — bigger lift than a straight Bank-pattern
  conversion, needs a nav-cascade design decision first. NOT tracked here.

Of the 48 Tier-0 screens, a further live-verified filter (checking each screen's actual
documented navigator requirement in `docs/ec_screen_registry.md`, not just its OV/OV-GM
label) found:
- **23 screens are genuinely nav-free** (plain manage-object with no mandatory
  dropdown/date before GO, OR custom-URL with no navigator at all) — same shape as
  Bank/Account. **These are what this checklist tracks and batches.**
- **20 screens have a real navigator requirement** (mandatory single date+GO, or a
  mandatory dropdown/cascade) — SKIP per owner instruction ("if the ec screen is not same
  as bank... SKIP it for next target screen"). Listed in "Excluded" below for the record.
- **5 screens were unclear/not in the registry** at survey time — need live recon before
  they can be classified either way.

## Batch tracking (23 nav-free Tier-0 candidates)

| Screen | Folder | Status | PR |
|---|---|---|---|
| Country | Basic Objects | ✅ DONE (2026-08-23, Batch 2) | #428 |
| County | Basic Objects | ✅ DONE (2026-08-23, Batch 2) | #429 |
| Regulatory Permits | Basic Objects | ✅ DONE (2026-08-23, Batch 2) | #432 |
| Currency | Financial Objects | ✅ DONE (2026-08-23, Batch 2) | #430 |
| VAT Code | Financial Objects | ✅ DONE (2026-08-23, Batch 2) | #431 |
| Customer | Commercial Objects | ✅ DONE (2026-08-23, Batch 3) | #435 |
| Field Group | Commercial Objects | ✅ DONE (2026-08-23, Batch 3) | #434 |
| Licence | Commercial Objects | ✅ DONE (2026-08-23, Batch 3) | #438 |
| MMS Lease | Commercial Objects | ✅ DONE (2026-08-23, Batch 3) | #437 |
| Operator Lease | Commercial Objects | ✅ DONE (2026-08-23, Batch 3) | #436 |
| State Lease | Commercial Objects | ⬜ NOT YET DONE | - |
| Vendor | Commercial Objects | ⬜ NOT YET DONE | - |
| Cost Object Mapping | Financial Objects | ⬜ NOT YET DONE | - |
| DOA Credit Limit | Financial Objects | ⬜ NOT YET DONE | - |
| Product Description | Financial Objects | ✅ DONE (2026-08-23, Batch 4) | #441 |
| Sales Order | Financial Objects | ⬜ NOT YET DONE | - |
| Product Group | Royalty Objects | ⬜ NOT YET DONE | - |
| Royalty Depositor | Royalty Objects | ⬜ NOT YET DONE | - |
| Royalty Owner | Royalty Objects | ⬜ NOT YET DONE | - |
| Unit Agreement | Royalty Objects | ⬜ NOT YET DONE | - |
| Calendar Collection | Date Objects | ⬜ NOT YET DONE | - |
| Calendar | Date Objects | ⬜ NOT YET DONE | - |
| Account Mapping | Financial Objects | ⬜ NOT YET DONE | - |

**10 of 23 done.** Batch 3 complete (Customer #435, Field Group #434, Licence #438,
MMS Lease #437, Operator Lease #436). 13 remain — natural pool for Batch 4 onward,
5 screens per batch matching the established cadence.

Note: once a screen from this table is converted, it should ALSO be added to
`docs/grid-filter-standardization-checklist.md`'s "done" table in the same PR (per the
owner's standing instruction to include the filter wiring from day one, not as a
follow-up pass).

## Excluded — has a real navigator requirement (per owner: SKIP if not same as Bank)

| Screen | Reason |
|---|---|
| Document Date Term, Payment Term, Choke, Choke Model, Disposition Type | Mandatory single date + GO before grid loads |
| Field, Contract Area, Delivery Point, Delivery Stream, Nomination Point, Pipeline Segment, Transport Zone | Mandatory Business Unit/Area dropdown + GO |
| Sub Area | Cascading PU→Area + GO |
| Equipment | 5-field cascading navigator |
| Analysis Point | 3-level cascade (PU→Area→Facility Class) + GO |
| Tract | Gated: mandatory date + mandatory Unit Agreement dropdown + GO |

## Unclear at survey time — needs live recon before batching either way

Sub Field, Pipeline, Meter, Transport System, Commercial Entity, Company Contact,
Carrier — not found in `docs/ec_screen_registry.md`'s navigator column at survey time,
or registry text was ambiguous (e.g. "optional" dropdown/date). Do NOT assume nav-free;
recon live before adding to a batch.

## Out of scope (Tier 1 — different, already-adequate pattern)

The 80 Tier-1 screens (generator-scaffolded, `verify_screen.py`-gated, Playwright-driven,
already label-driven via a different mechanism) are NOT tracked in this checklist. They
are not "old pattern" in the sense this doc cares about — converting them to the RF
Bank-pattern would be a consistency change, not a functional uplift, and is lower
priority. If ever prioritized, treat as a separate initiative, not an extension of this
checklist.

## How to update this doc

When a new batch of screens from the "Batch tracking" table gets converted, flip each to
"✅ DONE (date, BatchN)" with its PR number. If a screen turns out to have an
undocumented navigator requirement once recon'd live (contradicts its "nav-free" premise
here), move it to the "Excluded" table instead of force-fitting it — this happened for
zero screens in Batch 2, but is a real possibility for any future batch. Append-only in
spirit for the "Excluded"/"Unclear" tables; the "Batch tracking" table's rows should only
ever flip status, not be deleted.
