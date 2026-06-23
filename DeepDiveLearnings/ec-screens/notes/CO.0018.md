# CO.0018 - Maintain Equity Share

_Deep-dive 2026-06-22 (deterministic runner). Module: CO._

## Identity
- BF_CODE: CO.0018 - URL: `/com.ec.prod.co.screens/maintain_equity_share`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
| (no class resolved from URL/LABEL) | | | |

## Screen type
unknown (no class resolved)

## Help (description)
The equity share defines the companies' roles and ownership percentages to a commercial entity.

The 'Copy Current Split' button will create a new share on the date selected in navigator. The rows from previous share are copied and the end date is set to the new start date.

The last row in the screen contains a sum row. If the sum is more or less than 100 am error message is shown to the user.

To validate equity share the rounding is set to 9 decimals.

CONFIGURATION IN MAINTAIN SYSTEM SETTINGS (CO.1006)

Copy Current Split - Confirmation Message

Choose the setting between Yes or No. Setting to Yes will display a confirmation message upon creating a new split based on the selected date in the navigator.
