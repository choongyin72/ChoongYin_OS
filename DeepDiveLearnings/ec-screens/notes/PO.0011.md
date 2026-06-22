# PO.0011 — Daily Equipment Status

_Deep-dive 2026-06-22 (partial: Help captured; DB view pending a recon pass). Module: PO._

## Identity
- BF_CODE: PO.0011 · URL: /com.ec.prod.po.screens/daily_equipment_status
- Treeview: EC Production > Production Operations > Daily Equipment Status

## Help (description)
Track equipment status; EC creates one record per equipment item per production day. Only equipment with attribute "equipment status screen"=YES appears; drop-downs configurable. Daily-status grid, edit-in-place.

## Type
N1 daily-status.

## DB binding
View/table: TBD on recon (equipment daily-status table).

## Status
[~] Help + purpose captured. Next: live recon to resolve the backing class/view (OV_/TV_/DV_) + confirm grid/nav + insert/update capability.
