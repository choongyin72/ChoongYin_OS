# Dependency Screens — Draft Prerequisite Map (FOR REVIEW)

> Status: **DRAFT 2026-06-12** — built from read-only recon (`tmp/dep_recon/`, screenshots + DOM dump).
> These are the Financial/Commercial screens excluded from the standalone-IUD pass because they
> depend on objects configured in other screens (Choong-Yin, 2026-06-12: "all these screens have
> screen dependency. we handle differencely later"). Confidence markers: ✅ = parent screen already
> automated by us, ❓ = needs Choong-Yin/SME confirmation.

## Financial Objects leftovers (7)

| Screen | Observed structure | Prerequisite objects (draft) | Test-design idea |
|---|---|---|---|
| Exchange Rates | Navigator: From/To Date, Forex Source, Forex Time Scope, From/To Currency + GO | ✅ Exchange Rate Source, ✅ Currency (×2) | Seed AUTOTEST source+currencies → insert a rate row for the pair → verify → delete chain in reverse |
| Exchange Rate Setup | Date-anchored setup grid (record-status area) | ✅ Currency, ✅ Exchange Rate Source ❓ | Same seed chain as Exchange Rates; confirm which object the setup rows attach to |
| Financial Posting Setup | Navigator: Financial Code dd + GO | ❓ Financial Code / posting config (As-Built specific) | Need SME input — posting rules look client-config, may be look-don't-touch |
| VAT Country Setup | Date-anchored setup grid | ✅ Country, ✅ VAT Code | Seed AUTOTEST VAT Code (+ reuse real Country?) → map row → delete |
| Payment Scheme Setup | From/To Date setup grid | ✅ Payment Scheme | Seed AUTOTEST Payment Scheme → add setup row → delete |
| Account Mapping Assistance | Daytime + Contract / Transaction Template / Price Object / Product / Line Item Template+Type | ❓ CONTRACT-world objects (Sales & Transportation module) | Deep chain outside Assets — defer until contract screens are in scope |
| Cost Object Mapping Assistance | Same as above + Profit Centre, Account | ❓ same + ✅ Account, ❓ Profit Centre | Defer with its sibling |

## Commercial Objects leftovers (6)

| Screen | Observed structure | Prerequisite objects (draft) | Test-design idea |
|---|---|---|---|
| Customer VAT Reg No | Date-anchored setup grid | ✅ Customer (+ ❓ VAT registration country) | Seed AUTOTEST Customer → add reg-no row → delete |
| Vendor VAT Reg No | Date-anchored setup grid | ✅ Vendor | Same pattern as Customer VAT Reg No |
| Restricted Customer Setup | Date-anchored setup grid | ✅ Customer | Seed AUTOTEST Customer → restrict → unrestrict/delete |
| Restricted Vendor Setup | Date-anchored setup grid | ✅ Vendor | Same pattern |
| Field Group Setup | Date-anchored setup grid | ✅ Field Group, ✅ Field | Seed AUTOTEST Field Group + Field → membership row → delete |
| Maintain Equity Share | Navigator: Date + Licence + Commercial Entity + Phase + GO | ✅ Licence, ✅ Commercial Entity, ❓ Phase | Seed AUTOTEST Licence + Commercial Entity → equity rows (must sum 100%? ❓) → delete |

## Cross-cutting observations (from recon)
1. **Most of these are "Setup" screens**: a date/navigator header + an inline grid + the standard
   record-status area — closer to TV/PC mechanics than OV. Likely ONE new T2 pattern
   ("date-anchored setup grid") covers VAT Reg No / Restricted / Field Group Setup / VAT Country /
   Payment Scheme Setup.
2. **The setup-chain test shape**: Suite Setup seeds the parent AUTOTEST objects (reusing our
   existing page objects!), tests exercise the dependent screen, Suite Teardown deletes in
   REVERSE order (child rows first, then parents). Our existing T3s make the seeding nearly free.
3. **The two Assistance screens are a different league** — they hang off the Contract/Sales
   module, not Assets. Recommend keeping them deferred until that module is in scope.
4. Dropdown OPTION lists came back empty in headless DOM dump (PrimeFaces lazy panels) — per-screen
   recon at build time still needed; this map only fixes the dependency DIRECTION.

## Open questions for Choong-Yin
- Financial Posting Setup: is this client-config we should treat as read-only (no IUD)?
- Maintain Equity Share: business rule on shares (sum to 100%?) and what "Phase" is keyed to.
- The Assistance screens: confirm defer-until-contracts.
