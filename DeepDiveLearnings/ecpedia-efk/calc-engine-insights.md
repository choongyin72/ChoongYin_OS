# EC Calculation Engine — practitioner insights (EFK deep-dive, 2026-06-13)
Source: EFK page "The calculation engine is in dire need of enhancements" (id 1843903, 2017) — a
candid teardown by an EC allocation implementer (triggered by Shell Canada's ~80MB allocation
script). The single most useful EFK page so far for the N2/allocation track: it reveals the
engine's data model AND a real allocation TEST ORACLE.

## The calc engine's mental model (how Pluto's ZWP_ALLOC_* allocations actually run)
- The allocation is a **procedural program**, not just arithmetic: built from **iterators**
  (Iteration / Condition / Equation sections), **Decision Steps** (jump back to an earlier block),
  **calculation libraries** (reusable blocks — clunky), and **external functions** (Java, but only
  ONE parameter). Classes/Objects in EC **hold DATA only** — no behaviour/methods.
- **Everything lives in a global VARIABLE CACHE** — any block can read/update any variable. (The
  author likens it to "all data in public static variables" — tightly coupled, fragile.) This is
  why allocation changes ripple unexpectedly.
- **Variables are DIMENSIONED** — the key insight. e.g. net std volume:
  `NStdVol[ALLOC_STREAM,DAY]` · `[ALLOC_STREAM,DAY,PROFIT_CENTRE]` ·
  `[...,PROFIT_CENTRE,COMPANY]` · `[...,COMPANY,PRODUCT]` · `[ALLOC_STREAM,MTH]` ·
  `[...,MTH,RRCA_REG_OBJECT]` … The same quantity exists at many dimensional grains (stream × day ×
  profit-centre × company × product × regulatory-object, daily AND monthly). → This maps directly
  to the `STRM_DAY_*` result tables I saw: `STRM_DAY_ALLOC` (stream×day), `STRM_DAY_PC_ALLOC`
  (profit centre), `STRM_DAY_CPY_ALLOC` (company), `STRM_DAY_COENT_ALLOC` (co-entity),
  `STRM_DAY_COMP_ALLOC` (component), + `_MTH_` monthly variants. The engine writes each grain.
- **Core allocation operations**: **prorating** (allocate an actual to theoretical/estimate),
  **rounding**, **rolling up totals**, **composition-analysis** calcs, **recombine** (merge a gas +
  condensate stream → new composite analysis). These recur all over (the duplication he laments).
- **IsValid / IsZero everywhere**: the engine has no NVL; equations are cluttered with
  `IsValid(x) && !IsZero(x)` guards (and the inverse). Null/invalid variables are a constant hazard
  → a real source of allocation defects. (Wish-listed: NVL, optional IsValid, early block exit,
  strong-typed iterators with on-save validation, parallelisation, build-your-own functions.)
- **Debugging**: a debug log per equation (input/output links); runs are SERIAL (slow — a wrong
  iterator can cost 40-min reruns). Allocations run over an **Allocation Network List** (facilities
  prorated across the network) — matches HA.0002's "Allocation Network" navigator.

## ★ The allocation TEST ORACLE (what a meaningful allocation test checks)
Straight from the author's proration example — these are the invariants worth asserting (answers my
"what does an allocation test verify?" question for the N2 track):
1. **Conservation / sum-to-total**: the allocated subtotals MUST add up to the measured total —
   e.g. each well's allocated volume sums to the field's metered out-flow; per-profit-centre /
   per-company / per-component splits sum to the stream total. (Proration invariant.)
2. **No negatives**: allocated quantities should not go negative (a classic proration bug).
3. **Rounding tolerance**: subtotals-vs-total may differ by rounding → assert within a small
   tolerance, not exact equality (EC rounds, and rounding logic is duplicated/fragile).
4. **Multi-grain consistency**: the same quantity at day-grain should roll up to the month-grain;
   stream total should equal sum of its profit-centre / company / product splits.
→ N2 (HA.0002 Daily Allocation) test design: run the allocation for a date+network, then DB-assert
these invariants against `PWEL_DAY_ALLOC` / `STRM_DAY_*_ALLOC` (sum-to-total, ≥0, within tolerance,
day↔month + dimensional roll-up consistency). This is far more meaningful than "a row exists".

## Caveats
2017 opinion piece (engine may have improved since), but the data model (variable cache, dimensioned
variables, iterators, prorate/rollup/round, IsValid guards, calc libs, external Java functions) and
the conservation oracle are timeless and match what As-Built 06 (ZWP_ALLOC_*) describes. EC Production
parent page (1842679) is just a diagram — enumerate its children for the production KB later.
