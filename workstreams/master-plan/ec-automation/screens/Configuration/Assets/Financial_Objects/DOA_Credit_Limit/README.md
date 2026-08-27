# DOA Credit Limit — IUD Bundle

Insert / Update / Delete automation for the EC **DOA Credit Limit** screen
(Configuration → Assets → Financial Objects → DOA Credit Limit).

DOA Credit Limit is a plain **Manage Object (OV), no navigator** screen (only the universal
Date+GO as-at-date bar). DELETE = **End Date = Start Date** (zero-length window) — EC true delete
(object removed from `OV_DOA_CREDIT_LIMIT`).

The **live/current automation is the RF suite** (converted to the Bank-pattern shape in PR #443,
2026-08-23; label-driven, properties-file-driven, T2-consolidated — see `JOURNAL.md`/
`doa_credit_limit_sow.md` Section 7 for the conversion history). The `playwright/` + `investigation/`
folders below are the screen's **original 2026-06-11 build**, kept as historical reference only —
permanently waived from further maintenance per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`
(the Universal Screen Engine replaces that role going forward).

## Run — RF suite (current automation)
```bash
# from workstreams/master-plan/ec-automation/

# 1. Dry-run (syntax/keyword-resolution check, no browser)
py -m robot --dryrun tests/Configuration/Assets/Financial_Objects/doa_credit_limit_iud.robot

# 2. Live headless run (evidence captured to this bundle's evidence/ folder)
EC_HEADLESS=true py -m robot --outputdir screens/Configuration/Assets/Financial_Objects/DOA_Credit_Limit/evidence \
    tests/Configuration/Assets/Financial_Objects/doa_credit_limit_iud.robot

# 3. Live headed run (visible browser), if needed for a fresh visual check
EC_HEADLESS=false py -m robot tests/Configuration/Assets/Financial_Objects/doa_credit_limit_iud.robot
```

## DB self-clean check (fresh connection, after any live run)
```bash
py -c "import sys; sys.path.insert(0,'libraries'); import DbVerify; \
print(DbVerify.fetch_object('OV_DOA_CREDIT_LIMIT', 'AUTOTEST_DOA'))"
# Expect: None (confirmed absent) - the fixed test code AUTOTEST_DOA must be
# fully cleaned up (deleted) by the end of every run for the next run to reuse it.
```

## Run — Playwright reference (legacy, unchanged since 2026-06-11)
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_doa_credit_limit.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_doa_credit_limit.py
```

## Folder
- `pageobjects/.../doa_credit_limit_page.resource` + `tests/.../doa_credit_limit_iud.robot` (outside
  this folder, treeview-mirrored paths) — the current, live-tested RF automation.
- `testdata/doa_credit_limit_{insert,update,form_verify,grid_verify}.properties` (outside this
  folder) — the RF suite's test data.
- `playwright/ec_iud_doa_credit_limit.py` — legacy Playwright reference driver (2026-06-11 build,
  unchanged; permanently waived from further maintenance).
- `investigation/` — legacy recon scripts used to learn the screen (2026-06-11 build, unchanged).
- `evidence/` — screenshots + results from BOTH the legacy Playwright run (2026-06-11) and the
  current RF live run (2026-08-28 backfill).
- `doa_credit_limit_sow.md` — statement of work / spec (Section 7 addendum covers the Bank-pattern
  conversion).
- `JOURNAL.md` — per-branch work journal (backfilled 2026-08-28 from PR #443's real content).
- `CHECKLIST.md` — the 21-item deliverable checklist, ticked with real evidence citations.

## KB selector map
`ec-ui-knowledge/screens/doa_credit_limit.md` (repo root) — nav path, DB view, grid id,
insert/update/delete selectors, mandatory-yellow fields, quirks.
