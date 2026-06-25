# Stream/Well Gas Component Analysis (PO.0020) — SME deep-dive

_Pre-build deep-dive 2026-06-17 (per user advice: understand the screen before automating it).
Sources: EC tech-doc "Analysis Data Management BPM Workflow" (DOC-04 §11); ECpedia — "Polar Bear -
Component Analysis" (BPR), "Component Analysis - Mol% to Wt% Functionality in Stream Gas Component
Analysis" (EFK), XEM "Stream Configuration"; As-Built 06 (calc chain) + 09 (validations); local
chemistry.md; sandbox DB `DV_STRM_COMP_ANALYSIS`._

## 1. What the screen is
**Stream Gas Component Analysis (PO.0020)** captures the **hydrocarbon composition** of a produced
gas stream — the **component mol %** (and reference density) from **laboratory / analyser
(gas-chromatograph) samples**, to **C6+**. It lives in the **Laboratory → Sample Analysis** area, not
the daily production-status area. Siblings (same shape, different phase/scope):
- **Stream Oil Component Analysis (PO.0019)** — oil composition to C8+.
- **Well Gas Component Analysis (WR.0010.01)** — well-level gas composition.
- **Stream Emission Component Analysis (XEM)** — an *extension* of this screen for emissions.

## 2. Why it matters (business purpose)
Composition is the **quality data that drives the production calc chain**: component fractions →
**mass balance / allocation** (WFrac), **energy/GCV**, **emissions → CO2e**, and **contract-account**
quality. It is the input the Issue_1052 validations protect. Get the composition wrong and allocation,
energy and emissions are all wrong — hence the heavy validation around it.

## 3. Data model (DV_STRM_COMP_ANALYSIS) — PER-COMPONENT ROWS
Unlike the daily-status grids (one row per object×day), composition is **one row per COMPONENT**:
key = **(OBJECT_ID, DAYTIME, COMPONENT_NO)** [+ ANALYSIS_NO / ANALYSIS_TYPE / SAMPLING_METHOD / PHASE].
Columns: **`MOL_PCT`**, **`WT_PCT`**, `MOL_WT`, `DENSITY`, `RECORD_STATUS` (P→V→A), `COMPONENT_NO`.
Standard component set (shared across allocation + emissions): **C1 · C2 · C3 · iC4 · nC4 · iC5 · nC5**
(+ CO2 · N2 · C6+ …); ~12 components/analysis on the sandbox. Sandbox gas-comp data e.g.
`P1_S0163_M_GAS_COMP` @ 2025-04-02 (GAS, 12 comp).

## 4. Config behind it
- **Component Constant (CO.0103)** — per-component molecular weight / GCV constants (used by Mol↔Wt
  and Mol→Energy).
- **Component Set List** — which components are in the set (and order).
- **System Attributes** — composition behaviour toggles.

## 5. Screen behaviour / processing (the toolbar actions)
The screen has explicit **processing buttons** (also run in bulk by the **Analysis Data Management
BPM workflow**: "validation, processing and acceptance" — Mol↔Wt, Mol→Energy, Normalization):
- **MOL→WT**: EC **normalizes mol% to 100 first**, then `WT%_i = (mol_i·MW_i) / Σ(mol·MW)` (MW from
  CO.0103).
- **WT→MOL**: inverse.
- **MOL→ENERGY** / GCV.
- **Normalize**: scales the entered components so Σ = 100%.

## 6. Validations (the quality gate — Issue_1052 turf)
- **Component sum 98–102%** (check rules **1156 / 1157**) — the composition must sum to ~100%.
- **"Missing component value(s). All components must have a value to be able to normalize"** — every
  component in the set needs a value before Normalize/Mol→Wt will run.
- Frozen checks + missing-data (ZWP validation family).
- Record-status governance **P → V → A** per analysis.

## 7. Automation implications (for the N1-composition build)
- **Navigator = 8 fields** (deeper than the daily grids): 2 dates + Production Unit / Area /
  Facility Class 1 / **Stream** / **Analysis Status** / **Sampling Method** → GO `button:form:B`.
  Resolve PU/Area/Facility via **Stream Finder**; Stream/Status/Sampling must match the analysis.
- **Grid is per-component** (~12 rows). Editable inputs = **MOL_PCT** (and WT_PCT). The exact cell
  column (`:C{n}_in`) still needs a live grid-map (run `recon_comp_grid.py`).
- **DB ground truth needs a NEW component-keyed verify**: the existing `Day Status Value Should Be`
  keys only (object, date) — composition has many rows per (object,date), so add an APPEND-ONLY
  DbVerify keyword **`component_value_should_be(view, object_id, daytime, component_no, column,
  expected)`** filtering `COMPONENT_NO`. Shared T1 edit ⇒ **R12 canary** (backup first + cite a
  consumer dryrun). Verify against the view `DV_STRM_COMP_ANALYSIS`.
- **Edit gesture caution**: editing ONE component's mol% + Save should just persist that `MOL_PCT`
  row. **Do NOT click Normalize / Mol→Wt in the test** — those recalc the whole set (and need all
  components valued); the suite should assert only the single edited component's mol% (UI + DB) then
  revert, like the stream siblings. Watch for a normalize-on-save side effect.
- **Self-clean**: revert the edited component to its original mol% (read-then-restore).

## 8. Pluto relevance
ECpedia "Polar Bear – Component Analysis" (BPR/Pluto best-practice) confirms PO.0020/PO.0019 are the
composition screens in use; composition feeds the Burrup LNG Park / Scarborough monthly allocation
reports. So this is genuinely Pluto-relevant, not just generic-EC.

## 9. Next step
Run `tmp/scripts/recon_comp_grid.py` (already written) to map the editable mol% cell, add the
component-keyed DbVerify keyword (+canary), then build the N1-composition suite (edit mol% → Save →
verify `DV_STRM_COMP_ANALYSIS.MOL_PCT` for that component → revert).
