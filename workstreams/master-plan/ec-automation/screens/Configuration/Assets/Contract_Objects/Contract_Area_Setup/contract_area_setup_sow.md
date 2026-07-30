# SOW - Contract Area Setup IUD (Configuration > Assets > Contract_Objects)

- **Screen:** Contract Area Setup   **BF:** CO.2038   **View:** `OV_CONTRACT_AREA_SETUP`   **Base:** `CONTRACT_AREA_SETUP`
- **Type:** CUSTOM-URL OV (grid `nav:form:T_data`), NO navigator, NO GO button - reload via toolbar
  Refresh (the shared engine's `click_go` / T2 `Save And Refresh List` fall back automatically).
- Fields BY LABEL. Extra mandatory over plain OV: **Contract Area Name** + **Contract Name**
  reference dropdowns (first-available).
- **Start Date = 2020-01-01** (NOT 2000-01-01): ref dropdowns only offer objects effective at the
  form Start Date - DB-verified 28 contract areas + 98 contracts effective at 2020-01-01.
- DELETE = End Date = Start Date (zero-length window = true delete from the OV view).
- Test data: unique `AUTOTEST_CAS_<timestamp>` per run; never touch existing rows; self-cleaning.

## Known risks
- Ref-dd effectiveness: if the sandbox's contract/contract-area start dates change, first-available
  may go empty at the chosen Start Date - the DB pre-check (counts at 2020-01-01) is the guard.
- First custom-URL OV built on the SHARED engine (`py/ec_object_iud.py`) rather than the legacy
  hardcoded-ID Calendar exemplar style - engine `click_go` toolbar-Refresh fallback is the proof.
