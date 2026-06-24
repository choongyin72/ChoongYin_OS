# CO.0027 - Stream - by Group Model

_Deep-dive 2026-06-23 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0027 - URL: `/com.ec.prod.co.screens/manage_object_groupmodel_nav/GROUPMODEL/STREAM/TARGET/STREAM/CLASS_NAME/STREAM`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| `STREAM` | OBJECT/VERSIONED | `STREAM` | `OV_STREAM` |

## Screen type
OV (master-data object)

## Help (description)
The stream concept in EC is very central to the entire functional operation of the Energy Component system. It represents movement of all sorts of entities (e.g oil, water, NLG, flare gas, power fluid) between junction points, called "nodes", in a logical flow schematic, called a "stream node diagram". The stream concept is represented in the system by a dedicated and highly configurable object class "STREAM". Together with nodes, streams form the core set-up for creating allocation networks in EC.

Streams can represent:

- Real physical measurements, where data for one physical meter is transferred directly from the DSC system and stored as data for the stream.

- Real physical measurements, where data for many parallel physical meters are captured and averaged by DCS system before transfer and storage as data for a stream.

- Derived measurements that do not exist in the DCS system, b
