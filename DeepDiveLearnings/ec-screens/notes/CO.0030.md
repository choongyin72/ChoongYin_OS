# CO.0030 - Stream Set List

_Deep-dive 2026-06-23 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0030 - URL: `/com.ec.prod.co.screens/stream_set`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `STREAM_SET_LIST` | TABLE/EVENT | `STRM_SET_LIST` | `TV_STREAM_SET_LIST` |

## Screen type
TV (table-class)

## Help (description)
Stream sets are used to group streams together, e.g. for displaying certain streams together in one data screen. The stream set list screen enables the user to add, delete and modify streams connected to a stream set.

The connection to the Stream is time controlled, where each Stream Set-Stream (Stream Set List) connection will have daytime and an end date. The end date can be empty.

The group navigator is used for navigation down to Stream. The Stream Set dropdown will include all Stream Sets in the system regardless of navigator choices. The Other Streams linked to selected Stream Set data section at the bottom of the screen shows all Streams linked to the Stream Set selected in the first data section.
