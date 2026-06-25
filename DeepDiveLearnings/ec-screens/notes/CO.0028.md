# CO.0028 - Maintain Streams

_Deep-dive 2026-06-23 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0028 - URL: `/com.ec.frmw.co.screens/manage_copy_object_stream/GROUPMODEL/STREAM/TARGET/STREAM/CLASS_NAME/STREAM`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `STREAM` | OBJECT/VERSIONED | `STREAM` | `OV_STREAM` |

## Screen type
OV (master-data object)

## Help (description)
This is a generic screen; see description of generic screens in the beginning of the configuration manual.

This screen retrieves records from the Stream class. The version that is valid within the specified values in the navigator will be displayed. It displays all enabled attributes of Stream object. The screen provides the ease to update more than one record at the same time. It also allows creation of a new Stream as a copy of an existing Stream. To copy a Stream, select the Stream to copy from and then enter the new Stream Name, Stream Code, and Start Date, then hit Create a Copy button. If the Stream has Stream Set connections, it will automatically be included in the copy job.
