# RF evidence — Bank-pattern backfill re-run (2026-08-28)

Backfill evidence capture per `docs/lean-deliverable-backfill-workorder.md` Batch 6. This is
a re-run of the ALREADY-MERGED Bank-pattern RF suite (PR #437, merged 2026-08-23) — no
automation files were changed to produce this evidence.

## Commands run

```bash
# dryrun (from workstreams/master-plan/ec-automation/)
robot --dryrun --outputdir <out>/dryrun tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot

# live headless run
EC_HEADLESS=true robot --outputdir <out>/live tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot
```

## Results

- **Dryrun:** 5/5 PASS (`dryrun_output.xml`).
- **Live headless run:** 5/5 PASS (`output.xml`, `log.html`, `report.html`) —
  TC01 Verify Clean State, TC02 Insert MMS Lease Data, TC03 Update MMS Lease Data,
  TC04 Find MMS Lease Data, TC05 Delete MMS Lease Data.
- **Filter wiring fired:** `grep -c "Find MMS Lease Row By Filter" output.xml` = 13,
  `grep -c "Clear MMS Lease Row Filter" output.xml` = 5 (Update/Find/Verify-Found/Delete
  call the Find keyword; each TC that filters also clears once).
- **robocop** (`py -m robocop check pageobjects/.../mms_lease_page.resource
  tests/.../mms_lease_iud.robot`): 9 issues (4 VAR02 + 5 DOC02) — identical count/kind to
  the Bank/Country baseline cited in PR #437's body.
- **Hygiene** (`py scripts/check_bundle_hygiene.py`, repo root): RESULT: PASS — no
  hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions. (The
  one WARN line printed by this repo-wide scan belongs to Contract_Area's recon script, not
  MMS Lease.)

## DB ground-truth (fresh `oracledb` connections, ECKERNEL_EC / localhost:1521/ORCL)

```sql
SELECT COUNT(*) FROM OV_MMS_LEASE WHERE CODE = 'AUTOTEST_MMS_LEASE'
```
- Before the live run: **0** (code free).
- After the live run: **0** (self-clean confirmed — TC05 Delete removed the row; no residual).

## Pre-existing evidence in this folder

The sibling screenshots (`mms_lease_01_loaded.png` .. `mms_lease_08_final_state.png`) and
`mms_lease_results.json` in `evidence/` are from the ORIGINAL 2026-06-12 Playwright-only
build (before the 2026-08-23 Bank-pattern RF conversion, PR #437) and are left as-is —
the Playwright driver + its evidence stay waived per Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md` (Universal Screen Engine supersedes it), this folder
just adds the RF-side evidence that Section H restores.
