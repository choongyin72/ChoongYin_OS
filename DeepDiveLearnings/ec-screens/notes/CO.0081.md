# CO.0081 - Stream Formula Editor

_Deep-dive 2026-06-29 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0081 - URL: `/com.ec.prod.co.screens/stream_formula_editor`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| (no class resolved from URL/LABEL) | | | |

## Screen type
unknown (no class resolved)

## Help (description)
Stream Formula Editor is an editor where simple equations can be configured for stream methods. This is often used to set up virtual streams not directly metered but to be calculated by taking the sum of other streams. As an example, "Total Flare" can be the sum of the metered "LP Flare" and "HP Flare". Another example is "Total facility gas produced" = "Gas export" + "Fuel" + "Flare" - "Gas Import"

The editor supports calculation of both net and gross volume and mass. Objects that can be included in the editor are Stream, Tank, Storage, Facility Class 1 and Well Hookup. The formulas are date effective and can change over time. Supported formulas are as below:-

No
	
Formulas
	
Example

1	Standard Oracle functions such as NVL, POWER, GREATEST, LEAST, ROUND, SQRT, CEIL, FLOOR, MOD, REMAINDER, SIGN, TRUNC, ABS, EXP. Any standard Oracle functions that can be construct using a one row SQL s
