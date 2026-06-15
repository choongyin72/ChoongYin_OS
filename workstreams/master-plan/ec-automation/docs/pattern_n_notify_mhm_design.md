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
Send Freetext Message screen          MHM_MSG journal              transmission (async)
  nav: Date + Message Type +   ──▶   new row, DIRECTION='O',  ──▶  scheduler/ec-worker picks
       Distribution → GO              STATUS='PREPARED'             PREPARED rows → SMTP/MS-Graph
  compose: subject/body                (the test ORACLE)            → STATUS advances (SENT/…)
  click Send
```

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

## Two paths to the live proof (user decision)

1. **Create a safe `.invalid` distribution (recommended).** Additive, reversible config: a contact
   whose `DELIVERY_ADDRESS` is `autotest@example.invalid` + a `AUTOTEST_FREETEXT_INVALID` distribution
   with that one contact. Point `${SAFE_DISTRIBUTION}` at it → live send is guaranteed safe even if Send
   transmits synchronously. EC-correct route = the Distribution List UI screen (MHM.0001); a turnkey
   additive-SQL clone is prepped for review at
   [tmp/scripts/mhm_safe_distribution_prep.sql](../../../../tmp/scripts/mhm_safe_distribution_prep.sql)
   (NOT executed — review + approve first; it clones the FRMW free-text contact row and changes only
   OBJECT_CODE + DELIVERY_ADDRESS).
2. **Approve a one-off send through an existing distribution**, accepting the PREPARED-only evidence
   that nothing transmits. Faster, but relies on the synchronous-send assumption — not recommended
   while unattended.

Build status: suite is **dryrun-green, robocop-clean, journal oracle live-verified**; only the live
send awaits a safe recipient (path 1) or explicit approval (path 2).
