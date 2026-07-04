# Periodic Deep-Dive Review — 180/1,457 screens (2026-07-04)

_Milestone review of all completed screen notes at the 180-screen mark (first 100-batch run). Supersedes nothing; builds on the 29-screen review of 2026-06-27._

## Coverage snapshot

| Metric | Value |
|---|---|
| Screens complete | **180** (0 partial, 1,277 todo) |
| Modules touched | **CO (Configuration): 173** · PO (Production Operations): 7 |
| Screen types | OV 84 · process/config 28 · DATA/EVENT 26 · TV 24 · N1 daily 9 · DATA/NONE 5 · unresolved 4 |
| Class type/scope | OBJECT/VERSIONED 82 · DATA/EVENT 26 · TABLE/EVENT 21 · DATA/DAY 11 · DATA/NONE 5 · TABLE/NONE 3 · INTERFACE/VERSIONED 2 |

The run has now effectively swept the **entire EC Configuration (CO) master-data domain** from CO.0001 to CO.1003.

## The 10 domain clusters of EC Configuration (what these 180 screens actually are)

1. **Corporate / geographic backbone** — Production Unit, Area, Sub Area, Country, County, State, Region, Field, Sub Field, Licence, Company (+Contact), Commercial Entity, Functional Area, External Location. The org/geo tree everything else hangs from.
2. **Facility & production topology** — Facility Class 1/2, Production Sub Unit, Process Train, Flowline, Pipeline, Collection Point, Test/Production Separators, Storage, Tank (+Usage/Strapping), Blend (+Content Split), Intermediate Storage Products.
3. **Well & subsurface spine** (deepened from the 29-screen review) — Well → Well Hole → Well Bore (+Split) → Bore Interval (+Split) → Perforation Interval (+Split), Well Hookup, Planned Well, Well Mode (+Attributes), Reservoir Block/Formation (+link), Deferment Group (+Well Conn). Date-effective OV chain with sum-to-100% DATA/EVENT split satellites — the allocation backbone.
4. **Streams & allocation network** — Stream (+3 Maintain/Manage variants), Stream Set (+List), **Stream Node Diagram (class ALLOC_NETWORK_LIST — the allocation-network editor)**, Stream Well/Profit-Centre connections, Stream PT/DPT/ORF conversion values, Seasonal Values, Component Set (+List).
5. **Metering & fiscal-measurement science** — Orifice Plate, Meter Run (+Orifice connection), Choke (+Conversion, Gas-Lift Conversion, Choke Model +Ref Values), Test Device (+Ref Values), Analysis Point, Mismeasurement Event, **Constant Standard cluster** (Compression & Summation Factor, Calorific Values Ideal Gas Mol/Wt/Vol, Vi Interpolation, K1/K2 Interpolation, Equation Of State) — AGA/ISO gas-measurement science encoded as DATA/DAY-EVENT configuration.
6. **Chemicals subsystem** — Chemical Tank/Product (+Combination), Chemical Injection Point, Chemical Transport Tank, Chemical Stream (+Hookup), and its logistics: Truck, Trailer, Driver.
7. **Marine / logistics** — Vessel, Carrier, Cargo Activity, Cargo Account, Weather Site, Shift, Operator Route.
8. **North-America land & regulatory heritage** — MMS Lease, State Lease, Operator Lease, Regulatory Permits.
9. **Platform machinery (process/config screens)** — Status Processes, **Initiate Day** (the ECSR-35448 engine), Check Rule/Group/Rule-Group Combination, Validation Overview (x2), Stream Formula Editor, Business Actions, Schedules/Schedule History/Manage Scheduler, Action Trigger (+Conn), Task Process (+Item), System Messages, Message Definition/Format/Group/Freetext Template, Calculation Group Context/Setup, Asset Calculation Attributes, Alloc Job Status Process Conn, plus Account Settings/Documentation/Dashboard and User/Role/Object Maintenance (CO.1000-1003).
10. **Reference-value pattern family** — System / Well / Equipment / Facility / External-Location / Test-Device / Choke-Model Reference Values: one recurring `*_REFERENCE_VALUE` shape re-instantiated per object type.

## Recurring EC design motifs (confirmed at scale)

- **Master object (OBJECT/VERSIONED, End=Start delete) + `Maintain X`/`Manage X` bulk twin** — Well/Storage/Tank/Stream/FCTY/Chem all follow it (the twins resolve to the SAME class; only the screen shape differs).
- **Topology is data, not code** — every physical/logical link is its own DATA/EVENT class (`*_CONN`, `*_SPLIT*`, `*_COMBINATION`): Flowline-Well, Stream-Well, Equipment, Facility-ExtLocation, Deferment-Group-Well, Meter-Run-Orifice…
- **Science-as-config** — the Constant Standard cluster shows EC ships measurement-standard tables as maintainable data, not hardcoded constants.
- **Platform machinery is PROSTY/CTRL config** — checks, schedules, triggers, messages, status processes: all "no data class" process/config screens wired via config tables (PROSTY_CODES, CTRL_CHECK_*, etc.).
- **INTERFACE class type is rare** (2 of 180: Equipment twins) — attribute-driven generic screens.

## Data-quality observations (for the runner backlog)

- **4 unresolved names** (PO.0001/0002/0003/0005 show `?` titles) — early-format notes; will self-heal if ever re-run, cosmetic otherwise.
- **Duplicate BF pair** CO.0096 and CO.0096.01 both = Pipeline (same class) — checklist source artifact, harmless.
- Process/config screens still carry no config-table linkage (known enhancement: map to PROSTY_CODES/CTRL_CHECK_*/STRM_FORMULA…).
- Notes remain structure/metadata cards — business-process depth (like the Initiate Day / ECSR-35448 dissection) still requires manual deep-dives; the 10-cluster map above is the navigation aid for choosing them.

## What this milestone means for the north star

The CO sweep gives a **complete configuration-domain map**: every master object, its class/scope/view, and where the platform machinery lives. Next runs move into the operational modules (PO daily data and beyond) — where the N1/DATA-DAY patterns and the calc/allocation wiring dominate, which is exactly the territory of the calc-SME goal.

— End of review —
