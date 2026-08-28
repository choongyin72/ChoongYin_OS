# Lean-Deliverable Backfill Work Order

**Owner decision, 2026-08-27:** Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` retired the
2026-08-23/26 lean waiver. Every screen converted under the old lean rule (Bank-pattern or
Area-pattern, converter or new-screen variant) must be retroactively backfilled with the
artifacts that waiver skipped: **SOW, README, JOURNAL, evidence, CHECKLIST.md, KB selector map**.
The Playwright bundle (driver + `investigation/`) stays waived permanently — the Universal Screen
Engine replaces that role — so it is NOT part of this backfill.

**Scope confirmed by owner:** BOTH Area-pattern (34 screens) and Bank-pattern batches (~48
screens) — everything built under `ec-bank-pattern-converter`/`-new-screen` or
`ec-area-pattern-converter`/`-new-screen` since the lean rule began (2026-08-23) through today
(2026-08-27). Total: **82 screens.**

**Pacing:** owner instruction — "not rush for times." This is background, batched work, not a
single mega fan-out. Batches of 6-8 screens, dispatched one batch at a time, each batch
independently verified (spot-check + PR review) before the next batch starts. No fixed deadline.

---

## Per-screen backfill task (what every subagent must produce)

For screen `<Screen>` at treeview path `<menu path>`, working in `screens/<menu path>/<Screen>/`
(create the folder if the screen never had one — Bank-pattern-new-screen and Area-pattern-new-screen
builds never got a `screens/` folder at all, only RF files):

1. **`<screen>_sow.md`** — SOW: screen classification (OV/OV-GM/TV, pattern name), navigator/grid/
   cell shape (pull from the screen's actual `_page.resource` and `docs/ec_screen_registry.md` row
   — do not re-derive from scratch, the facts already exist), test data used, one-paragraph dev
   story (when built, what pattern, any real gotcha hit during the original build — check the
   original PR body/commit message for this, don't invent one).
2. **`README.md`** — bundle overview + the exact commands to run the suite (`robot --dryrun ...`,
   `EC_HEADLESS=true robot ...`, the DB self-clean check pattern).
3. **`JOURNAL.md`** — modeled on `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`
   (read it first): Built / Done well / Done wrong-or-lessons / Blockers→resolution / Decisions /
   Evidence sections. Pull real content from the original conversion PR's body and commit
   messages — this is a backfill of what actually happened, not a fresh narrative. If the original
   PR disclosed a real issue (a flake, a wrong classification, a shared-file regression), that
   belongs in "Done wrong / lessons," not smoothed over.
4. **`evidence/`** — re-run the screen's live suite ONE more time (`EC_HEADLESS=true robot`) with
   screenshots enabled if the T3 supports a screenshot-per-step flag; if it doesn't, capture what
   the run produces (log.html, output.xml, a results summary) into this folder. This does not need
   a NEW live-testing pass beyond what "done" already required — it's evidence capture of a real
   run, not a fresh verification cycle.
5. **`CHECKLIST.md`** — copy `docs/IUD-DELIVERABLE-CHECKLIST.md`, tick Steps 0, A (skip 4/5 — mark
   N/A, Playwright bundle waived by owner decision), B, C, D, E with real evidence citations
   (dryrun count, live N/N, DB self-clean query result, hygiene PASS) pulled from the original PR
   or a fresh re-run if the original PR body didn't cite one of the items explicitly.
6. **KB selector map** `ec-ui-knowledge/screens/<screen-slug>.md` — nav path, DB view, grid id,
   insert/update/delete selectors, mandatory-yellow fields, quirks, last-verified date. Pull from
   the screen's own `_page.resource` Variables section — the selectors already exist, this is
   transcribing them into the KB format, not re-discovering them.

**Do NOT re-run the full original build.** The RF suite, registry row, and scorecard row already
exist and are already merged — this task adds documentation/evidence artifacts around already-
working, already-verified automation. A dryrun + one live confirmation run is the only "testing"
this task needs; if it fails, that's a real regression to report, not something to silently
work around.

**Git:** one PR per screen (or per small batch of 2-3 closely related screens, e.g. sibling split-key
screens), branch `docs/<screen>-backfill-artifacts`, isolated worktree, sync before push, standard
PR body (What was backfilled / Files added / Base branch = master). Never self-merge.

---

## Batch plan (82 screens, batches of ~7)

### Batch 1 — Area-pattern pilot + first wave (7 screens)
Area, External Location, Field, Facility Class 1, Operator Route, Sub Area, Well Hookup

### Batch 2 — Area-pattern second wave (7 screens)
Contract Area, Price Object, Chemical Stream, Chemical Injection Point, Production Separator,
Chemical Stream Hookup, Well

### Batch 3 — Area-pattern third wave (7 screens)
Price Rate, Tank, Meter, Service, Pipeline Segment, Contract, Collection Point

### Batch 4 — Area-pattern fourth wave (7 screens)
Storage, Contract Capacity, Shift, Chemical Tank, Well Hole, Tract, Contract Inventory

### Batch 5 — Area-pattern final wave (6 screens)
Transport Zone, Property, Pilot, Well Bore Interval, Well Bore, Lifting Account

### Batch 6 — Bank-pattern Batches 2-4 screens (7 screens)
Country, Payment Scheme, Field Group, Customer, Operator Lease, MMS Lease, Licence

### Batch 7 — Bank-pattern Batch 4-5 screens (7 screens)
Vendor, State Lease, Product Description, Cost Object Mapping, DOA Credit Limit, Sales Order,
Product Group

### Batch 8 — Bank-pattern Batch 5-6 screens (7 screens)
Unit Agreement, Royalty Owner, Royalty Depositor, Calendar Collection, Account Mapping, Calendar,
Berth

### Batch 9 — Bank-pattern Batch 7 screens (7 screens)
Calculation-Group-Context, Calculation-Context, Blend, Canal, Inventory-Area,
Chemical-Transport-Tank, Meter-Run

### Batch 10 — Bank-pattern Batch 8-9 screens (7 screens)
Orifice-Plate, Port, Reservoir-Block, Reservoir-Formation, Report-Area, Process Train,
Split Item Other

### Batch 11 — Bank-pattern Batch 10-11 screens (7 screens)
Storage Flow, Stream Item Category, Data Extract Set, Trailer, Carrier, Bank Account,
Deferment Group

### Batch 12 — Bank-pattern Phase 3 + remaining (6 screens)
Document Template, Product (new build), Chemical Product, Report Context,
Target Mapping Configuration (Find-only — CHECKLIST items 8/9/10-12 N/A per its own nature, not
this backfill's scope), County (re-align, verify no duplicate JOURNAL needed if #452's Batch 2-6
completion note already covers ground truth)

---

## Execution log (update as batches complete)

| Batch | Status | PRs | Notes |
|---|---|---|---|
| 1 | Complete (awaiting merge) | #566 Area, #567 Sub Area, #568 External Location, #569 Field, #570 Well Hookup, #571 Operator Route, #572 Facility Class 1 | 7/7 backfilled 2026-08-27. All independently re-verified no automation files touched. Notable: Field's PR #529 shows CLOSED not MERGED on GitHub despite content being live (flagged, not resolved); several screens had pre-existing bundles predating the lean rule that needed refreshing, not fresh creation. |
| 2 | Complete | #574 Price Object, #575 Contract Area, #576 Production Separator, #577 Chemical Injection Point, #578 Chemical Stream, #579 Well, #580 Chemical Stream Hookup | 7/7 backfilled + merged 2026-08-27 (push 522a46d..3139679). Zero automation files touched; provenance + sourced ticks verified per PR. _Row finalized by the reviewer at the Batch 3 merge (was "In progress - #575 Contract Area", written before the batch landed)._ |
| 3 | Complete | #581 Pipeline Segment, #582 Contract, #583 Meter, #584 Price Rate, #585 Tank, #586 Collection Point, #587 Service | 7/7 backfilled + merged 2026-08-27 (push 3139679..c401951). Zero automation files touched; provenance + sourced ticks verified per PR. _Row finalized by the reviewer at merge (was "In progress - Collection Point", written before the batch landed)._ |
| 4 | Complete | #588 Chemical Tank, #589 Shift, #590 Contract Capacity, #591 Storage, #592 Tract, #593 Well Hole, #594 Contract Inventory | 7/7 backfilled + merged 2026-08-27. Zero automation files touched; provenance + sourced ticks verified per PR. _Row finalized by the reviewer at merge (no batch PR owned the log row this round)._ |
| 5 | In progress — Transport Zone done | Transport Zone: PR TBD (branch `docs/transport-zone-backfill-artifacts`) | 1/6 backfilled 2026-08-28 (Transport Zone: SOW/README/JOURNAL/CHECKLIST/KB map + evidence added around the already-merged PR #557 Area-pattern conversion; zero automation files touched, confirmed via `git status`). Live re-run hit one disclosed page-load timeout on TC01 (first attempt 4/5), immediate single retry passed 5/5 — no chrome/node process killed, per this task's process rule. Remaining: Property, Pilot, Well Bore Interval, Well Bore, Lifting Account. |
| 6 | Not started | — | — |
| 5 | Not started | — | — |
| 6 | In progress — 1/7 | #602 Field Group | Field Group backfilled 2026-08-28 (zero automation files touched; robocop/dryrun/live/DB-self-clean/hygiene all re-verified with matching evidence to PR #434's own baseline). Remaining 6/7 (Country, Payment Scheme, Customer, Operator Lease, MMS Lease, Licence) not started. |
| 7 | Not started | — | — |
| 8 | Not started | — | — |
| 9 | Not started | — | — |
| 10 | Not started | — | — |
| 11 | Not started | — | — |
| 12 | Not started | — | — |

**Do not dispatch a batch until the previous batch's PRs are independently verified** (PR-read
tool check, not subagent self-report alone) — same discipline as every other batch playbook in
this project's skills.
