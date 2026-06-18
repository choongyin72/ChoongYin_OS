---
name: ec-object-iud-builder
description: Use when building Insert/Update/Delete (IUD) automation END-TO-END for an EC master-data/config screen that behaves like Bank (OV / Manage-Object) or Language (TV / Table-class) — e.g. "automate Contract Area IUD", "build the IUD suite for <screen>", "do the full IUD for <EC screen>". Drives recon → fill the spec template → Playwright bundle + RF suite → live DB-verified run → self-clean → registry/scorecard → PR, autonomously. Pairs with the `ec-screen-automation` gesture cookbook (HOW to click) — this skill is WHAT to do, in order, hands-off.
---

# EC Object IUD Builder — autonomous end-to-end workflow

> **INPUT CONTRACT: the user provides ONLY the EC screen name.** Claude does EVERYTHING else —
> Step 1 (resolve metadata via `resolve_ec_screen.py`) through Step 7 (PR), hands-off. Do NOT ask the
> user for screen type, tables, delete method, field ids, etc. — derive/recon them yourself. The only
> times to come back to the user: a genuine blocker unresolved after ≤6 tries, or a real decision.

Build a new OV/TV IUD screen the **exact same way** as Bank/Language, hands-off. Fill the spec template
(`workstreams/master-plan/ec-automation/docs/EC-OBJECT-IUD-SPEC-TEMPLATE.md`) by recon, then deliver the
Playwright bundle + RF suite, live + DB-verified + self-cleaning, and raise the PR. For the exact click
gestures use the **`ec-screen-automation`** skill. Consult `docs/ec_screen_registry.md` first (the screen
may already be characterised).

## Standing guardrails (apply throughout — non-negotiable)
- **Branch FIRST** off master before any repo edit; reuse a fitting empty branch; one screen per PR.
- **AUTOTEST_ prefix** on all test data; **never touch existing rows**.
- **DB ground truth** (`libraries/DbVerify.py`) for every pass claim — never a green UI alone.
- **Self-clean**: leave the sandbox exactly as found; re-read the DB to confirm 0 residual.
- **No ad-hoc dirty probes** — let the suite (with self-clean) be the live proof ([[feedback_probe_write_self_clean]]).
- **Blocker rule:** if a step won't pass after ≤6 tries → STOP and (a) ask the user, (b) attack differently
  (DB-verify the data, re-recon), or (c) PARK it and continue the next step. Never grind.
- **Before the PR:** scan [[feedback_pre_commit_mistakes_review]] and confirm none repeated; stage only
  this session's files by explicit path.

## Steps (execute in order, autonomously)
**1. Branch + scope.** `git checkout -b feature/<screen-slug>-iud origin/master`. Read the registry row if present.

**2. Recon → fill the spec template (§1–§6).** DB-first → Finder/Toolbar/Nav → DOM:
   - **DB metadata is auto-derived from the screen NAME only** — run
     `SCREEN="<name>" py tmp/scripts/resolve_ec_screen.py` (queries `class_property_cnfg` LABEL → class_name,
     then `class_cnfg`): **CLASS_TYPE `OBJECT`⇒OV / `TABLE`⇒TV**; **TIME_SCOPE_CODE `VERSIONED`⇒date-effective
     (End=Start delete) / else physical**; base=`DB_OBJECT_NAME`, version=`DB_OBJECT_ATTRIBUTE`, view=`OV_<class>`.
     Pick the **type** → IUD block. Then row count + the LIVE recon below.
   - **Live recon is ONE read-only scan** — run `SCREEN="<name>" py tmp/scripts/scan_ec_screen.py`
     (opens the screen, never Saves). It returns, keyed by name: type (OV/TV, from the DB), **toolbar
     New/Delete state** (default = enabled; it only flags the rare DISABLED — R10), navigator shape +
     **which nav fields are mandatory (yellow)** + the GO id, the grid id, and the form/field ids with
     mandatory flags + labels — for OV it drives row-select (`updateAttributes` + `objectdates` End-Date
     C:3) and New-Object (`objectForm`); for TV it dumps the grid cells. Add reference-dd sources by eye
     only if the scan can't.
   - Write the filled spec as `screens/<menu path>/<Screen>/<screen>_sow.md`.

**3. Build the Playwright bundle** under `screens/<menu path>/<Screen>/`:
   `playwright/ec_iud_<slug>.py` (clone Bank's `ec_iud_bank.py` for OV or Language's `ec_iud_language.py`
   for TV — swap field ids/view/type per the spec; env-controlled EC_HEADED/SLOWMO/CODE; screenshots per
   step), `investigation/` (the recon scripts), `evidence/` (after a full run), `README.md`.

**4. Build the RF** (treeview-mirrored): T3 `pageobjects/<path>/<screen>_page.resource` (locators in
   Variables; docstring matches Variables — R7) + suite `tests/<path>/<screen>_iud.robot`
   (clean→insert→update→delete→cleanup, in-suite DB asserts). **Reuse T2** `manage_object.resource` (OV) or
   `table_class.resource` (TV) + T1 + DbVerify; a shared-file edit ⇒ R12 (backup + canary + random sibling).

**5. Verify.** robocop clean → `robot --dryrun` the suite + full `tests/` → **live headed run**
   (`EC_HEADLESS=false`) N/N PASS → DbVerify each op → **independent DB re-read = clean**.

**6. Package.** Append a row to `docs/ec_screen_registry.md` + `docs/automation-scorecard.md` (append-only).

**7. PR.** Pre-commit mistakes review → commit (stage own files) → R8 sync → push → `gh pr create` with the
   **R9 6-field body** (What / Files / DB ground-truth evidence (live N/N + the exact DbVerify assertion) /
   Self-clean / Rules applied / Base branch). **Never self-merge.**

## Type cheat-sheet (from Bank + Language)
| | OV (Manage-Object) — *Bank* | TV (Table-class) — *Language* |
|---|---|---|
| INSERT | Insert→New Object→`objectForm` mandatory (Code/Name/Start Date + ref dds)→Save→GO | Insert→"<label>"→blank row→fill yellow cells (incl PK) real-keys+Tab→Save→Refresh |
| UPDATE | row-select→`updateAttributes` Name→Save→GO | edit Name cell→Save→Refresh |
| DELETE | **End Date = Start Date** (objectdates) → true delete (toolbar Delete disabled) | select row→Delete→"<label>"→Save → **physical** |
| Test data | unique-per-run code (codes linger) | fixed code (physical delete self-cleans) |
| Verify | absent in `OV_*` after End=Start | physically gone from base table |
| OV-GM variant | + Business Unit / PU cascade + GO first | — |

## Done = a screen is "covered" when
RF suite (robocop-clean, dryrun, **live + DB-verified, self-cleaning**) + Playwright bundle + filled SOW +
registry row + scorecard row + PR raised. Reference exemplars: `screens/.../Financial_Objects/Bank/` (OV),
`screens/.../System/Language/` (TV).
