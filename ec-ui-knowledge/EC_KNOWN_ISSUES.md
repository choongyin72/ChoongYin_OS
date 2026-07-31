# EC Known Issues Log

> **Check this file before starting any bug investigation.**
> If the symptom matches an existing entry, apply the known fix/verification steps directly — do not re-diagnose from scratch.
> Add a new entry immediately once a root cause is confirmed, even if the fix is still in progress.

---

## How to use this file

- Search by symptom keywords first (error code, screen name, component).
- Each entry should be self-contained — someone with zero prior context should be able to apply the fix from the entry alone.
- Never delete an entry, even if the underlying system changes — mark it `Superseded` and link to the newer entry instead.

---

## Entry template

```
### <Short title> — <ORA-code / error type / component>

**Status:** Confirmed / Workaround only / Superseded
**Environment(s) seen:** e.g. plutodev, ecaas_clp_hongkong
**First seen:** YYYY-MM-DD
**Related case/ticket:** e.g. SF-25-01061899

**Symptom:**
What is observed — exact error message, screen behavior, log entry.

**Root cause:**
The actual underlying reason, in plain terms.

**Fix / resolution:**
Concrete steps taken. Include code/SQL snippet or config change if applicable.

**Verification:**
How it was confirmed fixed (test run, regression check, etc.)

**Notes:**
Anything situational — e.g. only occurs under specific data conditions, only in certain EC version.
```

---

## Confirmed issues

### Apigee OAuth2 non-compliant token_type — Nimbus SDK parse failure

**Status:** Confirmed
**Environment(s) seen:** CLP Hong Kong
**First seen:** 2026-06

**Symptom:**
EC framework OAuth2 calls via Apigee fail during token parsing.

**Root cause:**
Apigee returns `token_type: "BearerToken"` instead of the RFC-compliant `"Bearer"`, which the Nimbus SDK's OAuth2 client fails to parse.

**Fix / resolution:**
Intercept the raw HTTP response before it reaches Nimbus SDK parsing, and normalize/correct the `token_type` value prior to handoff.

**Verification:**
Token exchange succeeds after interception; confirmed no downstream auth failures.

**Notes:**
This is an Apigee-side non-compliance, not an EC bug — fix must live in the interception layer, not in Nimbus SDK config.

---

### ORA-20112 month-lock exception on DV_STRM_GAS_ANALYSIS

**Status:** Confirmed
**Environment(s) seen:** plutodev
**First seen:** 2026-05

**Symptom:**
`ORA-20112` thrown when writing to `DV_STRM_GAS_ANALYSIS` for a locked month.

**Root cause:**
Target month is locked via `TV_MONTHLY_DATA_LOCK` at the time of write.

**Fix / resolution:**
Unlock the month, perform the write, then re-lock — using `BULK COLLECT` pattern against `TV_MONTHLY_DATA_LOCK` for the affected rows.

**Verification:**
Write succeeds post-unlock; month re-locked immediately after to avoid leaving data open.

**Notes:**
Always re-lock in the same transaction/session — do not leave a month unlocked between steps.

---

### MessageOutDownload servlet — wrong content-type for non-XML formats

**Status:** Confirmed
**Environment(s) seen:** Woodside Pluto
**First seen:** 2026-05

**Symptom:**
Downloaded message output has incorrect content-type when the message format is not XML.

**Root cause:**
Content-type is hardcoded to `text/xml` in the servlet regardless of actual message format.

**Fix / resolution:**
Set content-type dynamically based on actual message format rather than hardcoding.

**Verification:**
Confirmed correct content-type returned for non-XML formats after fix.

---

### FK constraint failure deleting message definitions

**Status:** Confirmed
**Environment(s) seen:** Woodside Pluto
**First seen:** 2026-05

**Symptom:**
Cascading foreign key constraint violation when cleaning up message definitions.

**Root cause:**
Child tables deleted in wrong order relative to `MESSAGE_OUT`.

**Fix / resolution:**
Delete in this order: `MESSAGE_ATTACHMENT` → `RECIPIENT` → `REPORT_SEND_LOG` → then `MESSAGE_OUT`.

**Verification:**
Cleanup script runs without FK violations following corrected order.

---

### Docker Swarm stale TLS cert after redeploy

**Status:** Confirmed
**Environment(s) seen:** local dev (Windows laptop, hostname ap-f0a7g341jn6d.corp.quorumsoftware.com)
**First seen:** 2026-04

**Symptom:**
TLS handshake/cert errors persist even after cert files are updated on disk.

**Root cause:**
Docker Swarm snapshots cert files at deploy time — updating the file on disk doesn't refresh the running service's snapshot.

**Fix / resolution:**
Full `docker stack rm` followed by redeploy — a restart alone is not sufficient.

**Verification:**
Cert reflects updated value only after full stack removal + redeploy.

**Notes:**
Traefik (`ec-traefik:14.2.4`) is the sole TLS terminator on port 8443 — check its state specifically when diagnosing.

---

### AWS Client VPN TLS handshake failure — "Pluto - COPS" profile

**Status:** Confirmed
**Environment(s) seen:** Woodside Pluto VPN access
**First seen:** 2026-04

**Symptom:**
TLS handshake failure when connecting via AWS Client VPN.

**Root cause:**
CA certificate mismatch following server cert rotation.

**Fix / resolution:**
Export a fresh `.ovpn` profile from the AWS Console rather than reusing the cached one.

**Verification:**
Connection succeeds using freshly exported profile.

---

<!-- Add new confirmed issues below this line -->

### PI /batch gzip response not decompressed — gson "Expected BEGIN_OBJECT but was STRING" (apiqa gateway)

**Status:** Confirmed root cause; fix recommended, not yet implemented
**Environment(s) seen:** CLP Hong Kong — `apiqa.clp.com.hk` gateway + framework adapter. Incumbent `clpapigee.eipqa.clp.com.hk` gateway (fork adapter) unaffected.
**First seen:** 2026-07 (interface `ZXC_RetrieveJettyEquipment_PI`)
**Related case/ticket:** RCA at `C:\Projects\Woodside\jiras\PI\RCA_ZXC_RetrieveJettyEquipment_PI.md`

**Symptom:**
Jetty-equipment PI retrieval fails; scheduler job errors with gson `Expected BEGIN_OBJECT but was STRING` while parsing the `/batch` 207 response.

**Root cause:**
The apiqa gateway **gzips** the `/batch` 207 response, but **neither PI adapter decompresses it** (verified from source): the framework `com.ec.frmw.is.engine.adapter.pi.rest.PiRestAdapter` + shared `batch.Batch.send()` read the body via `response.readEntity(String.class)` straight into gson; the CLP fork `com.ec.extension.zxapp.pi.PiRestAdapter` has no gzip handling; and `com.ec.frmw.rest.client.RestClient` registers no GZip/EncodingFilter and sends no `Accept-Encoding`. So raw gzip bytes reach gson → parse failure. (Separate, second apiqa fault: `/points?path=&fields=WebId` returns ASP.NET routing **404** → summaries 409 → 0 tags.) The incumbent clpapigee gateway returns plain JSON, so the fork works there.

**Fix / resolution (recommended, not yet applied):**
Either (a) the apiqa gateway stops gzipping the `/batch` response (or only gzips when the client sends `Accept-Encoding: gzip`); or (b) add client-side gzip decode — register a JAX-RS `EncodingFilter` + `GZipEncoder` on `RestClient`, or a `Content-Encoding` check in `Batch.send()`. Separately, apiqa must route `/points`.

**Verification:**
Reproduced live with standalone tools (`PiAdapterRepro` = framework/apiqa; `PiForkAdapterRepro` = fork/clpapigee; in `C:\Projects\ChoongYin_Codes`): apiqa gzips + 0/15; a manual `EC_PI_GUNZIP=true` decode makes gson succeed — proving the adapters don't decode. clpapigee returns 15/15 plain JSON (env flaky).

**Notes:**
It's the gateway, not the adapter — both repros build the identical request; only the base URL differs. Sibling to the "Apigee OAuth2 non-compliant token_type" entry above (same PI interface, different fault).

---

### OV_CHEM_PRODUCT (Chemical Product, CO.0072) — End=Start delete blocked by a child-FK dependency

**Status:** Confirmed root cause (verified against the DB). Screen PARKED for IUD automation (insert/update fine; delete needs child-aware handling).
**Environment(s) seen:** Local sandbox `localhost:1521/ORCL` (ECKERNEL_EC), EC 14.2.4. 2026-07-26.

**Symptom:**
The standard EC "delete = End Date = Start Date" (zero-length window) does NOT persist for Chemical Product. In the UI the End Date field fills, Save clicks with **no error shown**, but `OV_CHEM_PRODUCT.OBJECT_END_DATE` stays NULL and the object remains in the view. No toolbar Delete exists on this screen.

**Root cause (verified):**
`CHEM_PRODUCT` is VERSIONED, but a zero-length close is blocked by a child foreign key. EC auto-creates a 1:1 `CHEM_USAGE_REPORT_CONF` row on product insert; the delete then raises
`ORA-02292: integrity constraint (ECKERNEL_EC.FK_CHEM_USAGE_REPORT_CONF_1) violated - child record found`
(child `CHEM_USAGE_REPORT_CONF.OBJECT_ID` -> `CHEM_PRODUCT.OBJECT_ID`, delete rule **NO ACTION**), and the `IUD_CHEM_PRODUCT` trigger returns `ORA-20102: Object delete is not allowed, set object end date`. The web UI swallows both, so it looks like a no-op. `CHEM_PRODUCT` is referenced by **18 FKs** total (CHEM_USAGE_REPORT_CONF, CHEM_PRODUCT_VERSION, CHEM_PHYSICAL_PROPERTIES, CHEM_PROD_STATUS, CHEM_UNIT_PRICE, CHEM_MATERIAL_COMPAT, ... ) so a clean delete must remove auto-created children first.

**Fix / resolution:**
To delete a Chemical Product: remove its child config rows (at minimum the `CHEM_USAGE_REPORT_CONF` record) — **there is NO UI screen for it** - verified 2026-07-31 against `DefaultScreenTreeview` (1385 entries; no label matches 'chemical report'/'chem usage'; `CHEM_USAGE_REPORT_CONF` is CLASS_TYPE=TABLE with no treeview screen). An earlier version of this entry claimed a 'Chemical Usage Report config screen' - that screen does not exist. So the child can only be removed at DB level, which makes the UI delete path a genuine EC PRODUCT DEFECT (the UI also swallows the resulting ORA-02292/ORA-20102 - see above) — THEN set End Date = Start Date. The generic OV engine (`py/ec_object_iud.py` `closeObjectRecord`) does NOT do child-aware delete; extend it (or a screen-specific driver) before automating this screen's delete.

**Verification:**
Reproduced live: End Date fills + Save (button) + `ec_error`='' but `object_end_date` NULL; raw view `update ... end=start` -> ORA-02292; view `delete` -> ORA-20102; direct child count `CHEM_USAGE_REPORT_CONF where OBJECT_ID=<product id>` = 1.

**Notes:**
Lesson for the OV IUD sweep: classify screens on **delete complexity** (child FKs / trigger rules), not just mandatory-dropdown presence, BEFORE building — an insert-only build leaves an un-deletable residual. Sibling dropdown screen HCB System (CD.0097) deletes cleanly via End=Start, so this is Chemical-Product-specific, not dropdown-wide.
