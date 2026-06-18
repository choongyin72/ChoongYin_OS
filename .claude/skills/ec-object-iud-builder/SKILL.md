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

## Template trust boundary — where you must think, not clone

The skill is a force-multiplier, not autopilot. Cloning a known-good exemplar is fast — but it silently
replicates the exemplar's defects too (R16 was discovered this way). Three points where the template
**cannot protect you** and where real judgment is always required:

1. **First-contact recon on a gated navigator (OV-GM screens):** the BU/PU cascade fields, their exact
   IDs, mandatory yellow fields, and GO button id must be derived fresh from the live DOM — the exemplar's
   IDs will differ. Never copy navigator locators blindly.
2. **Treeview path:** always verify the path by opening the screen and reading the breadcrumb / treeview
   node. Don't infer from the menu text in the spec template — it may differ from the actual node label.
3. **Grid redraw timing (OV-GM):** even with R17 now in the template, the exact CSS selector for the
   `Wait For Elements State` call must be derived from this screen's grid, not copied from the exemplar.

At these three points: slow down, recon first, verify against ground truth — do not trust the clone.

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
   - **OV-GM pre-flight check (N3):** if this is an OV-GM screen (BU/PU navigator required), add a note to the
     SOW §4 (Known Risks): _"OV-GM lazy redraw — grid redraws asynchronously after Save+GO; T3 `Row Should
     Exist` MUST await the row element before asserting."_ This is a known risk on all OV-GM screens; flag
     it in the SOW before building, not after a TC02 live failure.
   - Write the filled spec as `screens/<menu path>/<Screen>/<screen>_sow.md`.

**3. Build the Playwright bundle** under `screens/<menu path>/<Screen>/`:
   `playwright/ec_iud_<slug>.py` (clone Bank's `ec_iud_bank.py` for OV or Language's `ec_iud_language.py`
   for TV — swap field ids/view/type per the spec; env-controlled EC_HEADED/SLOWMO/CODE; screenshots per
   step), `investigation/` (the recon scripts), `evidence/` (after a full run), `README.md`.
   **Credential rule (N1):** always read EC credentials from env vars — `os.environ.get("EC_USER", "sysadmin")`
   and `os.environ.get("EC_PASS", "Sysadmin@01")` — never hardcode strings in the bundle. Match the pattern
   already used in all investigation scripts.

**4. Build the RF** (treeview-mirrored): T3 `pageobjects/<path>/<screen>_page.resource` (locators in
   Variables; docstring matches Variables — R7) + suite `tests/<path>/<screen>_iud.robot`
   (clean→insert→update→delete→cleanup, in-suite DB asserts). **Reuse T2** `manage_object.resource` (OV) or
   `table_class.resource` (TV) + T1 + DbVerify; a shared-file edit ⇒ R12 (backup + canary + random sibling).
   **OV-GM wait wrapper (N2):** for any OV-GM screen (BU navigator required), the T3 MUST define its own
   `<Screen> Row Should Exist` keyword that calls `Wait For Elements State    css=...    visible    20s`
   before the T1 `Row Should Exist` — the OV-GM grid redraws lazily after Save+GO and the instant T1 assert
   false-fails if the row hasn't rendered yet. Keep this wrapper in T3 only; do not modify shared T1/T2.

**5. Verify.** robocop clean → `robot --dryrun` the suite + full `tests/` → **live headed run**
   (`EC_HEADLESS=false`) N/N PASS → DbVerify each op → **independent DB re-read = clean** →
   **`py scripts/check_bundle_hygiene.py` must PASS** (R16 guard — no hardcoded creds in the bundle).

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
| OV-GM variant | + Business Unit / PU cascade + GO first; T3 MUST define `<Screen> Row Should Exist` with `Wait For Elements State visible 20s` before T1 assert (lazy redraw) | — |

## Done = a screen is "covered" when
RF suite (robocop-clean, dryrun, **live + DB-verified, self-cleaning**) + Playwright bundle + filled SOW +
registry row + scorecard row + PR raised. Reference exemplars: `screens/.../Financial_Objects/Bank/` (OV),
`screens/.../System/Language/` (TV).
