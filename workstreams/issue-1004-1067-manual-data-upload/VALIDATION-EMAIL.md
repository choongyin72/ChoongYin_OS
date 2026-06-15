# Draft email — validate the PLP Manual Data Upload template (Issues 1004 + 1067)

> Draft for review before sending. Replace **[recipient]** / **[your name]** / hub-specific names.
> **Attach: `PLP_Data_Upload_Template_V1_DRAFT.xlsx`** (our first-draft Pluto template — one tab per EC
> screen with proposed columns) and, for reference, the AOPA baseline `ACTR-3098 Data_Upload_V4.xlsx`.

---

**To:** [Pluto data-owners / Josh Foleti / hub SME]
**Cc:** [PM / EC delivery]
**Subject:** Pluto Manual Data Upload (Issues 1004 + 1067) — please validate scope & template columns

Hi [recipient],

We're combining **Issue 1004** (PLP manual data-upload template) and **Issue 1067** (bulk-update for
measured streams/tanks/compositions) into one Excel-upload feature, using the **AOPA implementation as the
baseline** and uplifting it for Pluto. I've **attached a first-draft Pluto template
(`PLP_Data_Upload_Template_V1_DRAFT.xlsx`)** — one tab per EC screen, with the proposed columns already
laid out (key columns in orange, updatable values in blue, plus a mandatory Comments column). Please
**validate/correct the template** alongside the three points below: **(A) which screens are in/out,
(B) the columns per screen, (C) the upload rules.** Items we couldn't confirm are flagged **[confirm]** in
the template and **[CONFIRM]** below.

The template currently has **12 tabs**, one per screen in the "EC Screens" pack you provided:
Daily Production Well Status 1, Daily Gas Stream Status, Daily Liquid Stream Status, Daily Water Stream
Status, Daily Electrical Stream Status, Daily Tank Status (VCF), Stream Gas Component Analysis, Well Gas
Component Analysis, Daily Contract Account Status, Daily Contract Account Result – Company, Monthly
Contract Account Status, Monthly Contract Account Company Status.

### A. Screens in scope — please confirm in / out

**1. Carried over from AOPA (confirm columns in section B):**
Daily Production Well Status 1, Daily Gas Stream Status, Daily Liquid Stream Status, Daily Water Stream
Status, Daily Electrical Stream Status, Daily Tank Status (VCF).

**2. In AOPA but NOT in the Pluto screen pack — propose to EXCLUDE [CONFIRM]:**
- Well **Gas Injection** + Well **Water Injection** (AOPA injects; please confirm Pluto does not need these).
- AOPA **Monthly Liquid** tab — include for Pluto, or exclude?

**3. Pluto needs these but they are NOT in the AOPA template — we will ADD [CONFIRM each]:**
- **Stream Gas Component Analysis** and **Well Gas Component Analysis** (compositions — multi-component layout).
- **Daily Contract Account Status**, **Daily Contract Account Result – Company**, **Monthly Contract Account
  Status**, **Monthly Contract Account Company Status**. _(These were marked "maybe" in 1067 — are all four
  in scope? Any monthly-only or daily-only?)_

**4. Anything missing?** Is there any other daily/monthly input screen users update by hand that should also
get an upload tab (e.g. a well status #2 / hookup, or any composition besides gas)?

### B. Columns per screen — please validate (key vs updatable)

For each screen, the **key columns** identify the row (Facility / Object code / Date) and the **updatable
columns** are the measured values. Proposed below — please tick / correct / add. Every tab will also have a
mandatory **Comments** column and a hidden **Upload reference** (`ZWP_ACTR_REF`).

| Screen / tab | Key columns | Updatable columns (proposed) |
|---|---|---|
| Daily Production Well Status 1 | Facility, Well Code, Date | On-Stream Hrs, Oil, Cond, Gas, Water, Gas Lift (vol/mass), **+ [CONFIRM Pluto well attributes & whether `PWEL_DAY_STATUS_2` adds more]** |
| Daily Gas Stream Status | Facility, Stream Code, Date | Gross Vol [Sm³], Meas Energy [GJ] |
| Daily Liquid Stream Status | Facility, Stream Code, Date | Gross Vol [Sm³], Oil Spec Gravity, BS&W [%] |
| Daily Water Stream Status | Facility, Stream Code, Date | Gross Vol [m³], OIW Avg/Peak [ppm], Oil-in-Water, Density |
| Daily Electrical Stream Status | Facility, Stream Code, Date | Power Consumption [kWh], Available Hrs [hr] |
| Daily Tank Status (VCF) | Facility, Tank Code, Date | Closing Liquid [Sm³], Free Water [m³], Diluent [%] **[CONFIRM Pluto VCF attributes]** |
| Stream Gas Component Analysis | Facility, Stream Code, Date | **[CONFIRM component set — C1…nC5, CO2, N2, H2S…? mol% vs value]** |
| Well Gas Component Analysis | Facility, Well Code, Date | **[CONFIRM component set]** |
| Daily / Monthly Contract Account (× Company) | Facility, Account Code, Date | **[CONFIRM updatable attributes]** |

_(The AOPA columns for the first six are confirmed from their working template; the bottom three are new —
we need your input, or we can extract the exact attributes from the Pluto screens and send back for tick-off.)_

### C. Upload rules — please confirm

1. **Dropdowns:** facility + stream/well/tank pickers should list **Pluto** assets — please confirm the
   facility list (and whether streams should filter by selected facility).
2. **Granularity:** support both *many days for one stream* and *all inputs for a single day* — confirmed?
3. **Validations:** reject **negative** values; block a **locked month**; only update rows at record status
   **Verified or lower** (never overwrite Approved); **numeric-only** (blank = skip, non-numeric = error,
   except Comments) — confirmed?
4. **Mandatory comment:** every updated value needs a **non-blank comment** — confirmed? (One comment per row,
   or per value?)
5. **Permissions:** the upload must run **as the uploading user's role** (a Surveillance user can't update
   beyond their normal rights) — confirmed?
6. **Traceability:** `LAST_UPDATED_BY` = the uploader; `REV_TEXT` = "Upload File <file-number>" — confirmed
   format? Any Pluto reference (`ZWP_ACTR_REF`) value you want recorded?
7. **Processing cadence:** automated processing **every 5 minutes** — confirmed (vs on-demand)?

Once you confirm A–C, we'll finalise the Pluto template + ECIS mapping and share a test upload for UAT.
Happy to walk through it on a quick call.

Thanks,
[your name]
