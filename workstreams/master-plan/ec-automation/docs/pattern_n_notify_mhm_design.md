# Pattern N-notify — MHM messaging / notification verification

The first **messaging/notification** test pattern, alongside the data patterns:
N1 (edit-in-place status grids), N2 (allocation/calc RUN), N3 (status-process P→V→A).
Where N1–N3 prove *data* mutations, **N-notify** proves a *message* was produced and journaled.

Suite: [send_freetext_notification.robot](../tests/Production/send_freetext_notification.robot)
T3: [send_freetext_message_page.resource](../pageobjects/Production/send_freetext_message_page.resource)
T2: [message_send.resource](../resources/message_send.resource)
Oracle: `DbVerify.message_journal_*` ([DbVerify.py](../libraries/DbVerify.py))

## The mechanism (stock EC MHM)

```
Send Freetext Message screen               MHM_MSG journal              transmission (async)
  nav: Date + Functional Area +     ──▶   new row, DIRECTION='O',  ──▶  scheduler/ec-worker picks
       Message Type + Subject → GO         STATUS='PREPARED'             PREPARED rows → SMTP/MS-Graph
  edit Template body → SEND                (the test ORACLE)             → STATUS advances (SENT/…)
```

**Verified live screen model (2026-06-15):** nav columns are Date (`G:0:R:1:C:0:da_input`),
Functional Area (`…C:1:dd`), Message Type (`…C:2:dd`, cascades from FA), Subject (`…C:4:dd`,
fixed-list popup); GO = `button:form:B`; body = `template:form:G:0:R:1:C:0:ta`; SEND = `SendButton:form`.
**There is NO distribution/recipient selector on the screen** — recipients are fixed entirely by the
chosen Message Type's wiring (`MESSAGE_DISTRIBUTION.MSG_DISTR_CODE` → `DISTRIBUTION_SET`). Under FA=EC
the only freetext type is `FRMW_TEST_MSG_1` ("FRMW Test Msg 1 for message body"), wired to
`FRMW_DISTR_SET_FREE_TEXT` (the real-domain set).

- **Oracle = MHM_MSG append-only delta** (`message_journal_new_row_should_exist`, +1), the same
  delta shape as the N3 STAT_PROCESS_STATUS oracle. A send that journals a fresh outbound row proves
  the send→journal mechanism end-to-end — regardless of whether transmission later fires.
- Maps to client flavors by swapping the oracle table: **AOPA** stock `MESSAGE_OUT`,
  **CLP** custom `ZXC_T_NOTIFICATION`. Stock `MHM_MSG` is the client-agnostic core (present here).

## Sandbox transmission posture (verified 2026-06-15, read-only)

Ground-truth recon of the local sandbox (`localhost:1521/ORCL`, ECKERNEL_EC):

| Fact | Evidence |
|------|----------|
| Outbound never transmits | `MHM_MSG` GROUP BY: **O / PREPARED = 4, O / SENT = 0** (all outbound stuck at PREPARED) |
| No async sender running | N3 deep-dive: no scheduler/ec-worker node firing in this sandbox (PREPARED rows never advance) |
| Endpoints defined but idle | `ENDPOINT_CONFIG`: `default-smtp-endpoint` (smtp) + `msgraph-sendmail-v10` exist, RECORD_STATUS=P |
| Send journals as PREPARED | the 4 existing outbound rows sit PREPARED → the send step is journal-only here |

**Implication:** a live N-notify send adds a 5th `PREPARED` row (journal delta proves the mechanism)
and — given no sender node — does not transmit, exactly like the existing 4.

## ⚠️ Why the live send is still GATED

The evidence above is strong but does **not** 100% rule out that the screen's *Send* performs a
**synchronous** SMTP/MS-Graph attempt at click time (the 4 PREPARED rows could have been seeded by a
non-screen path). And **every** existing distribution resolves to a **real domain**:

| Distribution | Recipient(s) | Safe? |
|---|---|---|
| `FRMW_DISTR_SET_FREE_TEXT` | receiver_1/2/3@**energycomponents.com** (vendor) | ❌ real |
| `MHM13_OCH_WL` | birger.kvam@**holmen.com**, eirike@**norskefjell.no** (real people) | ❌ real |
| `EC111_DIST_LIST` | test@**testdomainxyz.com** | ⚠️ placeholder, not reserved-non-deliverable |
| `TEST_LIST` | everyone@**home.com** | ⚠️ placeholder, not reserved-non-deliverable |

Sending a real email is an irreversible outward-facing action. **No distribution uses an RFC-2606
guaranteed-non-deliverable domain** (`.invalid` / `.test` / `.example`). So a live run must first
guarantee a safe recipient.

## Paths to the live proof (decision)

Because the screen has **no distribution selector**, the only lever to change recipients is the
message type's wiring. The single controlling row is `MESSAGE_DISTRIBUTION` where
`OBJECT_ID = 491091C52373…` (FRMW_TEST_MSG_1) and `MSG_DISTR_CODE = FRMW_DISTR_SET_FREE_TEXT`.

1. **Rewire the message type to a safe `.invalid` distribution, then revert.** Create a non-deliverable
   distribution (additive clone → `autotest@example.invalid`, see
   [mhm_safe_distribution_prep.sql](../../../../tmp/scripts/mhm_safe_distribution_prep.sql)),
   repoint that one `MESSAGE_DISTRIBUTION` row to it, run the suite live, verify the MHM_MSG +1 delta,
   then restore the row. Guaranteed safe even if SEND transmits synchronously. Touches one reversible
   shared-config row.
2. **Send to the real FRMW distribution**, relying on the journal-only evidence (no config change).
   Faster, but can't 100% rule out a synchronous SMTP attempt to the real domain.
3. **Stay build-ready, defer the send** — the suite encodes the verified screen model; the live proof
   waits for path 1 or 2. **(current state, chosen 2026-06-15)**

Build status: suite is **robocop-clean, journal oracle live-verified, screen model corrected to the
live UI**; the live send is deferred (path 3). The orphan `.invalid` distribution created during
recon was removed (clean) — it is unreachable from the screen and only useful once a message type is
wired to it (path 1).
