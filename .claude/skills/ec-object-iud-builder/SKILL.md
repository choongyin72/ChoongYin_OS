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
replicates the exemplar's defects too (R16 was discovered this way). Four points where the template
**cannot protect you** and where real judgment is always required:

1. **First-contact recon on a gated navigator (OV-GM screens):** the BU/PU cascade fields, their exact
   IDs, mandatory yellow fields, and GO button id must be derived fresh from the live DOM — the exemplar's
   IDs will differ. Never copy navigator locators blindly.
2. **Treeview path:** always verify the path by opening the screen and reading the breadcrumb / treeview
   node. Don't infer from the menu text in the spec template — it may differ from the actual node label.
3. **Grid redraw timing (OV-GM):** even with R17 now in the template, the exact CSS selector for the
   `Wait For Elements State` call must be derived from this screen's grid, not copied from the exemplar.
4. **Grid id + GO presence are PER-SCREEN — never inherited from a sibling.** An OV can be either a
   **manage-object OV** (grid `manage_object_nav_nav:form:T_data` + a GO button `button:form:B`) **or** a
   **custom-URL OV** (grid `nav:form:T_data`, **NO GO**, reload via toolbar Refresh — e.g. Calendar,
   Account, Regulatory Permits). They look identical until you check. Take the grid id + GO presence from
   **THIS screen's scan output** and paste them into the T3 verbatim. (Real failure, CD.0024 Calendar
   2026-06-28: a sibling's `manage_object_nav_` grid id was assumed; the insert persisted but the UI
   row-check failed confusingly. This is now gated — see Step 5 pre-flight.) **When a UI assert fails,
   check the DB first: if the row persisted, it is a locator bug, not an insert bug.**

At these four points: slow down, recon first, verify against ground truth — do not trust the clone.

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

## Sweep-workflow rules (multi-screen batches — reviewer 2026-07-26, non-negotiable)
- **Engine-first, then off-master:** any shared-engine/T2 change ships as its OWN PR merged FIRST; then base
  each screen branch off **master**, independently. Do NOT deep-stack independent screens (a deep chain forces
  order-locked merges + conflicts for no benefit). Stack ONLY when a screen truly needs an unmerged engine symbol.
- **Tracking docs = append-only.** Append registry/scorecard ROWS; do NOT edit the shared
  `**N covered · M uncovered**` totals line in every screen PR (guaranteed conflict) — reconcile totals once at the end.
- **`verify_screen.py` on EVERY IUD PR** (ticks from real runs). Its hygiene gate scans `ec-automation/py/*.py`
  drivers + `screens/**/{playwright,investigation}/` — keep drivers ASCII + env-creds.
- **Recon-first classify before building:** plain Bank-layout (Code/Name/Start Date only, no mandatory dropdown,
  opens via tv-link) = BUILD; mandatory dropdown / gated nav / tv-link-not-found = PARK with the reason. A batch
  recon that fails UNIFORMLY = distrust the SCAN, not the screens. Siblings are NOT clones — recon each form.
- **Fix whole buckets, not one screen at a time:** if N parked screens block on the same missing capability
  (e.g. mandatory-dropdown fill), build it ONCE and unlock the batch.
- **Verify a reviewer's specific list against the files before acting** (a listed screen may already be fixed).

## Steps (execute in order, autonomously)
**0. CHECK-EXISTING-FIRST GATE (before any build).** The task is *check-then-build*, never *build*.
   - Read `ec-ui-knowledge/screens/<screen>.md` if it exists (use its selectors; don't re-scan).
   - Search for a working implementation:
     `grep -ril "<screen-slug>" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`.
     **Found → reuse/extend it; NEVER add a parallel copy** (real miss: a 3rd standalone Bank stack got
     built alongside the existing RF + Playwright). Also check the registry (`docs/ec_screen_registry.md`).
   - Prefer configuring the shared engine over new plumbing: `py/ec_object_iud.py` (OV IUD) +
     `libraries/DbVerify.py`. A new OV screen = a thin driver (copy `py/bank_iud.py`, swap config).
   - State the result in the plan ("existing impl: <path> / none") before writing anything.

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
   - **Grid id + GO come from THIS scan, pasted verbatim into the T3 — never from a sibling/exemplar.**
     The scan prints the real grid id + GO id for this screen. An OV is EITHER manage-object
     (`manage_object_nav_nav:form:T_data` + GO `button:form:B`) OR custom-URL (`nav:form:T_data`, NO GO,
     toolbar Refresh). Do not infer from a sibling — they look identical until checked (trust-boundary #4).
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
   and `os.environ.get("EC_PASS", "sysadmin")` — never hardcode strings in the bundle (the local sandbox
   is `sysadmin`/`sysadmin`; matches `tmp/scripts/ec_session.py`). Match the pattern in the recon scripts.

**4. Build the RF** (treeview-mirrored): T3 `pageobjects/<path>/<screen>_page.resource` + suite
   `tests/<path>/<screen>_iud.robot` (clean→insert→update→delete→cleanup, in-suite DB asserts).
   **⛔ NO HARDCODED field ids (owner rule).** OV field fills MUST resolve **by LABEL** via T2
   `Fill OV Field By Label ${form} <label> <value>` / `Fill OV Date By Label` / `OV Field Id By Label`
   (`${form}` = objectForm|updateAttributes|objectdates) — never a hardcoded `…R:<n>:C:<n>:in` id (row shifts
   per screen: Start Date R2 on Choke vs R4 on Choke Model). Keep only screen NAME + grid id (constant) as vars.
   **Reuse T2** `manage_object.resource` (OV) or `table_class.resource` (TV) + T1 + DbVerify; a shared-file edit
   ⇒ R12 (backup + canary + random sibling).
   **OV-GM wait wrapper (N2):** for any OV-GM screen (BU navigator required), the T3 MUST define its own
   `<Screen> Row Should Exist` keyword that calls `Wait For Elements State    css=...    visible    20s`
   before the T1 `Row Should Exist` — the OV-GM grid redraws lazily after Save+GO and the instant T1 assert
   false-fails if the row hasn't rendered yet. Keep this wrapper in T3 only; do not modify shared T1/T2.

**5. Verify.** robocop clean → `robot --dryrun` the suite + full `tests/` →
   **MANDATORY grid-locator pre-flight (R-gridid guard) BEFORE the live run** —
   `SCREEN="<name>" GRID_ID="<the T3 ${X_TABLE} value>" EXPECT_GO="<true|false>" py tmp/scripts/preflight_grid_locator.py`
   must print `RESULT: PASS`. It opens the screen and asserts the T3's declared grid id actually exists in
   the live DOM (and that GO presence matches), FAILING LOUD with the real grid id if a sibling's id was
   assumed. **Do not proceed to the live run until this passes** — this is the hard gate that makes the
   CD.0024 Calendar class of mistake (assumed `manage_object_nav_` on a custom-URL OV) un-shippable. →
   **live headed run**
   (`EC_HEADLESS=false`) N/N PASS → DbVerify each op → **independent DB re-read = clean** →
   **`py scripts/check_bundle_hygiene.py` must PASS** (R16 guard — no hardcoded creds in the bundle; **R20
   guard — fails statically on ANY non-ASCII char in `playwright/*.py` or `investigation/*.py`**, so author
   every bundle/recon `.py` ASCII-clean: use `-` not em-dash, `->` not arrow, `OK`/`X` not check/cross, plain
   quotes — including in docstrings/comments and untaken FAIL-branch strings).
   **⛔ MANDATORY GATE — `py scripts/verify_screen.py --name "<Screen>" --t3 <T3> --suite <suite> --driver <driver>
   --out <bundle>/VERIFY-REPORT.md` MUST print `OVERALL: PASS` (exit 0) BEFORE the PR.** It RUNS robocop +
   hygiene + dryrun + the live suite + the driver and writes the tick marks FROM THE REAL EXIT CODES — you do
   NOT hand-tick the verification gates (10/11/12/13/15/16). Copy its `VERIFY-REPORT.md` into the bundle and
   reference it from `CHECKLIST.md`. Ticking a gate the verifier did not pass is a hard violation
   ([[feedback_dont_trust_own_code_until_validated]] / CLAUDE.md 'NO GUESSING' rule).

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
| OV custom-URL variant | grid `nav:form:T_data` (NOT `manage_object_nav_`), **NO GO button** → T2 `Save And Refresh List` falls back to toolbar Refresh (e.g. Calendar, Account, Regulatory Permits). **Set `${X_TABLE}` from the scan, confirm via the Step-5 pre-flight guard.** | — |

## Done = ALL 21 items of `docs/IUD-DELIVERABLE-CHECKLIST.md` are green
A screen is "covered" ONLY when every item of the canonical **`docs/IUD-DELIVERABLE-CHECKLIST.md`** is done
with evidence. **Mandatory: copy that file into the bundle as `CHECKLIST.md` and tick each item** as you go
(**Step 0 check-existing gate**; artifacts: SOW + README + JOURNAL + playwright + investigation + evidence; RF:
T3 + suite; gates: robocop + dryrun + **live N/N** + **DB ground-truth** + **full I-U-D** + self-clean + hygiene;
delivery: registry row + scorecard row + R9 PR; **KB map `ec-ui-knowledge/screens/<screen>.md`**; **reuse clause**
— a reuse run still refreshes JOURNAL + evidence + KB map). "Done" is NEVER green tests alone. **Raise the PR only
when all 21 are green** — the automated reviewer enforces this list as HARD GATES and will MUST-FIX (not merge)
any PR with gaps. Reference exemplars:
`screens/.../Financial_Objects/Bank/` (OV), `screens/.../System/Language/` (TV),
`screens/.../Royalty_Objects/Product_Group_Setup/` (3-tier PC).
