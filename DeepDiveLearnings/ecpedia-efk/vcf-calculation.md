# EFK Phase-2 — VCF Calculation in EC (tank volume correction; a clean test oracle)
Read 2026-06-14 from EC Knowledge (EFK): **VCF Calculation in EC** `1853432` (2023, recent + concrete).
VCF = **Volume Correction Factor** — corrects an observed tank volume to a *standard* volume/mass. This
is a deterministic, standards-published calc → an ideal test-oracle family (like N2 allocation but with
an external authority to check against). Complements `calc-engine-insights.md`.

## The tank measurement chain (API MPMS Chapter 12.1 = 16.2) — 8 steps
1. **Gross observed volume** — typically by *strapping* (tank gauging tables).
2. **Remove free water** — typically from strapping.
3. **Steel shell temperature correction** on the tank's gross volume (the steel expands/contracts).
4. **Floating roof adjustment**.
5. **Gross Standard Volume (GSV)** — apply the **VCF factor** (corrects volume to standard temperature
   /pressure).
6. **Net Standard Volume (NSV)** — remove **BS&W** (Bottom Sediment & Water).
7. **Mass in air**.
8. **Mass in vacuum** — ⚠️ **EC does NOT do this step** (explicit scope boundary worth knowing).

## How EC implements it (version history — matters for which logic is under test)
- **EC 9.3** — a *library* using an **external lookup table** (based on the **1980** Standards,
  temperature scale **IPTS-68**). Lookup, not formula.
- **EC 10.1+** — a **PL/SQL package** based on the **Manual of Petroleum Measurement Standards (MPMS)
  Chapter 11, May 2004** edition. Formula-based.
- **EC 10.4+** — supports **both pressure AND temperature** correction (combined into one procedure).
- Pluto is on EC **14.2.x**, so it's the **10.4+ PL/SQL formula** path (algorithmic, not table lookup).

## What changed 1980 → 2004 standard (the gotchas a test must respect)
From MPMS §11.1.1.5, the key shifts EC's modern calc embodies:
- **Temperature scale IPTS-68 → ITS-90** — inputs are corrected back to an IPTS-68 basis first;
  standard densities adjusted for the small standard-temperature shifts.
- **Combined temp + pressure** into a single unified procedure (driven by real-time density meters that
  measure at >atmospheric pressure). The old separate temp/pressure tables are special cases (pressure
  = 1 atm gives the 1980 temp table; etc.).
- **20°C tables added** (ISO 91-2) alongside 60°F / 15°C — international standard-temperature support.
- **Rounding rule (⭐ the test-critical one):** rounding/truncation of *initial and intermediate*
  values is **ELIMINATED**; rounding is applied **ONLY to the final VCF**, to a consistent **5 decimal
  digits**. (The 1980 tables rounded CTL to 4–5 dp depending on >/< 1.) The standard also gives a way to
  produce unrounded CTL/CPL factors that combine to the overall rounded CTPL.
- **Double-precision floating-point** math (the 1980 integer-arithmetic complexity dropped); a more
  **robust convergence** scheme for observed→base density.
- **No glass-hydrometer correction** applied (assume densities are pre-corrected per MPMS Ch 9).
- Range extended to lower temperatures / higher densities (lower API gravity). Basic equation forms +
  constants unchanged; only ranges/scales adjusted.

## Why this is a strong test target (the series' point)
- **External oracle:** unlike allocation (where the oracle is conservation/no-neg invariants I derive),
  VCF has a *published authoritative standard* (API MPMS Ch 11). A test can assert EC's GSV/NSV/mass
  outputs against standard reference values for known (volume, temp, pressure, density, BS&W) inputs.
- **The rounding rule is the headline test concern** — exactly the "rounding tolerance" hazard the
  calc-engine critique flagged ([[reference_ec_zwp_validation_functions]] / `calc-engine-insights.md`).
  Assert: intermediate steps are NOT rounded; only the final VCF is, to **5 dp**. A test that rounds
  intermediates would diverge — and that divergence is a real defect class to catch.
- **Step-boundary tests:** free-water removal (step 2) and BS&W removal (step 6) are subtraction steps;
  steel-shell + floating-roof (steps 3–4) are volume adjustments; the VCF factor (step 5) is the
  temp/pressure correction. Each is independently checkable; mass-in-vacuum (step 8) should be ABSENT
  (EC doesn't compute it — a negative assertion).
- **Custody-transfer relevance:** GSV/NSV/mass feed inventory valuation (EC Revenue **IN** module) and
  fiscal/custody-transfer reporting → a VCF error propagates straight into revenue + SOX-reported
  numbers, so it's high-value to guard.

## Open items / next
- Find the EC PL/SQL package name for VCF (10.4+ path) by DB recon when a tank/inventory screen is in
  scope (candidate: a `*_VCF_*` or measurement package; not confirmed here). Then a VCF test = feed
  known inputs → assert outputs vs API reference values within the 5-dp rule.
- Tank/inventory screens aren't yet in the Pluto coverage plan — file VCF as a calc-oracle pattern for
  when they are. Next Phase-2 idle item: **EC Framework `1854410`** or **EC Technology `1853250`**.
