# N-notify: a client-agnostic EC notification/messaging verification pattern

**Capstone of the MHM/notification SME track.** Distils the stock-MHM mechanics (generic sandbox) +
four client implementations (CLP, AOPA, Pluto, SLNG) into one reusable test-design pattern, so an
N-notify suite can be stood up for any EC client by filling in a small, well-defined parameter set —
not by re-reverse-engineering each time.

Companion docs: [[reference_slng_project_sources]] · `slng-mhm-implementation.md` ·
`clp-mhm-implementation.md` (PR #17) · `aopa-mhm-implementation.md` (PR #18) ·
`ec-mhm-sme.md` (PR #15) · `ec-mhm-trigger-and-test-pattern.md` (PR #16) ·
`workstreams/master-plan/ec-automation/docs/pattern_n_notify_mhm_design.md` (the generic-sandbox suite).

## 1. The universal shape

Every EC notification implementation studied collapses to the same five stages, even though each
client customises *where* in the stack the custom code sits:

```
(1) EVENT ──▶ (2) PRODUCER ──▶ (3) STORE/QUEUE ──▶ (4) BRIDGE ──▶ (5) DELIVERY
 business      builds the        a row whose         hands the      transport +
 trigger       message + its     STATUS is the       message to     a STATUS
 (screen save, recipients        primary oracle      the channel    transition
 scheduler,                                          (stock MHM,    back onto the
 check rule)                                          SES, EIP)     store row
```

The **test oracle is always stage (3): a row in a table, with a STATUS that advances.** What differs
per client is *which table* and *which status values* — never the shape of the assertion. This is the
key insight: **verify at the store/journal table, parameterised per client; never assume one mechanism.**

## 2. Per-client parameter set (the only things that change)

| Param | Generic (sandbox) | CLP | AOPA | Pluto | SLNG |
|---|---|---|---|---|---|
| **Store/oracle table** | `MHM_MSG` / `MESSAGE_OUT` | `ZXC_T_NOTIFICATION` | `MESSAGE_OUT` | `MHM_MSG` | `Z_NOTIFICATION` → `MESSAGE_OUT`/`MHM_MSG` |
| **Producer** | screen (Send Freetext) | EIP/custom | `ZWA_P_NOTIFICATIONS` (PL/SQL) | `ZWP_P_MAIL_UTIL` | `ZP_NOTIFICATIONS` (PL/SQL) |
| **Bridge to delivery** | stock MHM | EIP→SES | PL/SQL→MESSAGE_OUT | PL/SQL→MHM_MSG | **Java** `SendNotifications`→MESSAGE_OUT |
| **Channel** | SMTP/MS-Graph (idle) | AWS SES | SMTP | SMTP | SMTP |
| **Status column / values** | `STATUS` PREPARED→SENT | (custom) | MESSAGE_OUT status | MHM_MSG status | `Z_NOTIFICATION.STATUS` NEW→PROCESSED |
| **Recipients from** | `DISTRIBUTION_SET_CONTACT`→`COMPANY_CONTACT_VERSION` | custom | same | same | same |
| **Prefix** | — (stock) | `ZXC` | `ZWA` | `ZWP` | `Z`/`ZP` |

To build a client's N-notify suite, fill this row. Everything else is shared.

## 3. The oracle: append-only +1 delta (parameterised)

All five stores are **append-only** (a send adds a row; nothing is rewritten), so the same
delta-assertion used by the generic sandbox suite (`DbVerify.message_journal_*`) generalises. The only
parameters are the table name, the type/filter column, and the direction/status filter:

```
baseline = COUNT(*) FROM <store> WHERE <type_col>=<type> [AND <dir/status filter>]
... trigger the event ...
assert   COUNT(*) FROM <store> WHERE ... == baseline + 1     (a fresh notification was produced)
[and optionally] assert latest row STATUS advanced (NEW→PROCESSED / PREPARED→SENT)
```

**Design recommendation for DbVerify:** generalise the existing `message_journal_*` helpers into a
`notification_oracle(table, type_col, type_val, status_col=None, dir_col='DIRECTION', dir='O')` form
(append-only; keep the current MHM_MSG helpers as a thin stock-preset wrapper — *append, don't rewrite*,
per the conflict-magnet rule on `DbVerify.py`). One oracle, any client.

## 4. Two oracle grains (pick per what you're testing)

- **Producer grain** — assert the STORE row appears with initial status after a business event
  (screen save / submit / publish). Tests the *producer* (e.g. `ZP_NOTIFICATIONS.fcstSubmitNotification`).
  Screen-drivable; no scheduler needed. **Most robust for automation.**
- **Bridge/delivery grain** — assert the status transition (NEW→PROCESSED / PREPARED→SENT) + the
  downstream `MESSAGE_OUT`/`MHM_MSG` row after the *sender* runs. Tests the bridge (SLNG's Java action,
  AOPA/Pluto PL/SQL). **Needs the scheduler job enabled + a node firing it** (see §6).

## 5. Trigger taxonomy (how to make stage 1 happen in a test)

| Trigger | How the test fires it | Seen in |
|---|---|---|
| Screen save / submit / publish | drive the EC screen (existing T2/T3 gestures) | SLNG submit/publish, generic Send-Freetext |
| EC Scheduler business-action | enable the job + ensure an ec-worker node runs it | SLNG `SendNotifications`, status processes |
| Check/validation rule | run the rule (N3-style) → notification on WARNING | Pluto `N_R_D_VALIDATION_REVIEW` (Issue_1052) |
| Direct PL/SQL call | call the producer proc with binds (recon/seed) | all PL/SQL producers |

## 6. Standing gotchas (banked from the track)

- **No scheduler node ⇒ bridge never advances.** Generic sandbox: outbound rows sit `PREPARED`
  forever (0 SENT) because no node fires the sender. Prefer the **producer grain** unless a worker node
  is confirmed running. (Same root cause as the N3 status-process finding.)
- **No distribution selector on the Send-Freetext screen.** Recipients are fixed by the message type's
  `MESSAGE_DISTRIBUTION` wiring — you cannot pick a distribution at send time. (Cost me a wrong screen
  model; see `pattern_n_notify_mhm_design.md`.)
- **Client config isn't in the generic sandbox.** Stock MHM tables exist everywhere, but `ZXC_*`,
  `Z_NOTIFICATION`, `ZWA_*` live only in the client env / its dataload. A client N-notify *live* test
  needs that client's environment; the *pattern* is portable.

## 7. ⚠️ Safety protocol (outbound email is an external action)

Mandatory before any live send, regardless of client:
1. Resolve the actual recipient domains (`DISTRIBUTION_SET_CONTACT`→`COMPANY_CONTACT_VERSION.DELIVERY_ADDRESS`
   or the client's equivalent). If ANY is a real domain → **gate**.
2. Make recipients non-deliverable first — point the message type's distribution at an
   `@example.invalid` (RFC-2606) contact (reversible config), OR confirm the env cannot transmit
   (no scheduler node + idle endpoint) AND get explicit approval.
3. Default to the **producer grain** (no transmission at all) when in doubt.

## 8. Decision tree — "given a client, build its N-notify test"

```
1. Identify the store table + producer + status values  → fill the §2 row (recon the client repo).
2. Can I drive the producing EVENT from a screen?
      yes → PRODUCER-grain suite (assert store +1 delta after the screen action).  ← preferred
      no  → is a scheduler/worker node running the sender?
               yes → BRIDGE-grain suite (assert status transition + downstream MESSAGE_OUT/MHM_MSG).
               no  → producer-grain via direct PL/SQL call, OR park (document the node gap).
3. Apply the §7 safety protocol before any live send.
4. Oracle = parameterised append-only +1 delta (§3) on the store table.
```

## 9. Status & next steps
- Pattern is **complete and portable**; the generic-sandbox suite (`send_freetext_notification.robot`)
  is the reference producer-grain implementation (build-ready, live send gated).
- Implementation TODO (when prioritised): generalise `DbVerify.message_journal_*` → `notification_oracle`
  (§3), append-only. Then a client suite = the §2 row + the shared keywords.
- Per-client live tests depend on reaching each client's environment (open question for SLNG/CLP/AOPA).
