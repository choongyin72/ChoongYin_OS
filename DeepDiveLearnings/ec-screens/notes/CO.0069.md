# CO.0069 - Cargo Account

_Deep-dive 2026-06-27 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0069 - URL: `/com.ec.frmw.co.screens/manage_table/CLASS_NAME/CARGO_ACCOUNT`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `CARGO_ACCOUNT` | TABLE/EVENT | `ACCOUNT` | `TV_CARGO_ACCOUNT` |

## Screen type
TV (table-class)

## Help (description)
Cargo accounts are holding export storage inventory for each owner and product. Owners are those having equity shares in the incoming production to storage. One company having equity shares in several licenses will therefore have one account for each license.

Official production into the storage times your equity share is your input to your account. Cargo lifting is your output from your account. Production into the storage is often determined as delta storage + export out from storage. Accounts can become negative, as own owner can lift more than he has on storage. However, the sum of all accounts for storage is always equal closing inventory of the storage.

Future account balances can be calculated based on planned production, equity shares and lifting nominations.
