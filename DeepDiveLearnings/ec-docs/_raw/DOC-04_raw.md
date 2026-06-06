# Raw content — DOC-04
Modules: ['prod']
Pages: 22



==========================================================================================
## [1/22] Dashboard
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_dashboard.html
==========================================================================================
Dashboard
Introduction

This document describes the EC Production Dashboard widgets that come as part of the standard EC product. The EC Production Dashboard consists of line widgets, bar widgets, pie chart widgets, table widgets and gauge widgets. They are predefined. However, it is possible for projects to create or modify the dashboard query to support their business needs. The new widget (i.e. line, pie chart, bar, etc.) can be configured using CTRL_DASHBOARD table. The query is stored in the QUERY parameter in the CTRL_DASHBOARD_PARAM table along with other required parameters. To define these widgets from the dashboard, there is a menu consisting of different input parameters on the top right-hand corner of the widget.

Production widgets that are available in this release are as follows:

Top 5 Yearly Producers at Area (separate widgets for Oil/Gas/Condensate)

Top 5 Yearly Producers at Facility (separate widgets for Oil/Gas/Condensate)

Top 5 Monthly Producers at Area (separate widgets for Oil/Gas/Condensate)

Top 5 Monthly Producers at Facility (separate widgets for Oil/Gas/Condensate)

Daily Actual Vs Planned For Area (separate widgets for Oil/Gas/Condensate/Water)

Daily Actual Vs Planned For Facility (separate widgets for Oil/Gas/Condensate/Water)

Monthly Actual Vs Planned For Area (separate widgets for Oil/Gas/Condensate/Water)

Monthly Actual Vs Planned For Facility (separate widgets for Oil/Gas/Condensate/Water)

Oil Production For Area

Oil Production For Facility

Gas Utilization For Area

Gas Utilization For Facility

Well on Stream by Facility

Daily Production Well Status by Facility

Daily Injection Well Status by Facility

Reconciliation Factor by Facility (separate widgets for Oil/Gas/Water)

Daily Stream Data

Widget 1: Top 5 Yearly Producers at Area

This dashboard widget displays the top 5 producers for the selected area and year. Separate widget is present per phase, details are as follows:

Top 5 Yearly Oil Producers at Area

Widget Code

	

AREA_TOP5_YR_OIL_PROD




Database Class

	

DSHBD_AREA_TOP5_OIL_YR




Database View

	

V_DSHBD_AREA_T5_OIL_YR, V_DAY_ALLOC_OIL_SUM_YR




Label

	

Top 5 Yearly Oil Producers at Area




Description

	

Filters top 5 yearly oil producers for the selected year and area based on the sum of allocated well volumes. This widget will accumulate the pwel_day_alloc.alloc_net_oil_vol from 1st Jan to 31st Dec for wells belonging to the area. The widget will only be populated after a successful allocation run.

Top 5 Yearly Gas Producers at Area

Widget Code

	

AREA_TOP5_YR_GAS_PROD




Database Class

	

DSHBD_AREA_TOP5_GAS_YR




Database View

	

V_DSHBD_AREA_T5_GAS_YR, V_DAY_ALLOC_GAS_SUM_YR




Label

	

Top 5 Yearly Gas Producers at Area




Description

	

Filters top 5 yearly gas producers for the selected year and area based on the sum of allocated well volumes. This widget will accumulate the pwel_day_alloc.alloc_gas_vol from 1st Jan to 31st Dec for wells belonging to the area. The widget will only be populated after a successful allocation run.

Top 5 Yearly Cond Producers at Area

Widget Code

	

AREA_TOP5_YR_COND_PROD




Database Class

	

DSHBD_AREA_TOP5_COND_YR




Da
…[truncated]


==========================================================================================
## [2/22] System Attributes
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_system_attribute.html
==========================================================================================
System Attributes
System Attributes

EC Production uses a number of System Attributes to control system behavior. This document explains these system attributes.

For a new EC installation, all of these should be checked and set according to the required behavior of EC Production.

System Attribute 'ADJUST_POTENTIAL_DST'

This attribute controls whether the well potential will be adjusted for daylight saving dates. "Y" means that the well potential will be adjusted. Used in EcBp_Well_Potential.

Options are Y | N.

The Default EC installation value is 'Y'.

System Attribute 'ALLOW_ALLOC_LOCK_MONTH'

This attribute indicates whether the daily/monthly allocation is allowed on locked months. "Y" means that daily/monthly allocation is allowed on locked months.

Options are Y | N.

The Default EC installation value is 'N'.

System Attribute 'ALLOW_DUP_PROD_DEF_EVENT'

This attribute indicates whether overlapping non-well group deferment events will be allowed. This applies to the obsolete deferment version Low and Off Deferments.

Options are Y | N.

The Default EC installation value is 'N'.

System Attribute 'API_CALC_BIT_DENSITY_MAX'

This attribute indicates the default maximum bitumen density.

The default EC installation value is 1050.

System Attribute 'API_CALC_BIT_DENSITY_MIN'

This attribute indicates the default minimum bitumen density.

The default EC installation value is 950.

System Attribute 'API_CALC_DIL_DENSITY_MAX'

This attribute indicates the default maximum diluent density.

The default EC installation value is 750.

System Attribute 'API_CALC_DIL_DENSITY_MIN'

This attribute indicates the default minimum diluent density.

The default EC installation value is 500.

System Attribute 'API_CALC_MAX_ITERATIONS'

This attribute indicates the default max iteration used in the loop to calculate blend/diluent volume in EcBp_Vcf.calcAPIBlendShrinkage.

The default EC installation value is 20.

System Attribute 'API_CALC_TOLERANCE'

This attribute indicates the default tolerance value used in the loop to calculate blend/diluent volume in EcBp_Vcf.calcAPIBlendShrinkage.

The default EC installation value is 1E-6.

System Attribute 'BITUMEN_DENSITY'

Default value for Bitumen. Density Default EC installation value is 1020.

System Attribute 'DAILY_DEFERMENT_LEVEL'

This attribute indicates the level in the operational group model events is stored against. This is applicable for the PD.0004: Daily Deferment Master.

Valid choices : SUB_AREA, FCTY_CLASS_2, FCTY_CLASS_1.

Default EC installation value is 'FCTY_CLASS_1'.

System Attribute 'DECIMAL_COMP_NORMALIZE'

This attribute indicates the number of decimals to be stored when component normalization to 100 is performed.

Default EC installation value is NULL (Blank).

System Attribute 'DEFERMENT_VERSION'

This attribute indicates the deferment version to use. Note that with the introduction of the new deferment version PD.0020 (Well Deferment), " PD.0001 / PD.0001.02 and PD.0006" are now obsolete and will not be supported in future EC versions.

Valid choices : PD.0004 , PD.0020

Default EC installation value is 'PD.0020'.

System Attribute 'DEF_WELL_CALC_RULE'

This attribute indicates th
…[truncated]


==========================================================================================
## [3/22] How To Define Status Processes
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_status_processes.html
==========================================================================================
How To Define Status Processes
Introduction

This document describes on how to set up Status Processes (CO.0076). Status process is a job that is executed to update record status on a set of classes. Record status controls data access to the data. There are three record statuses configured in EC as below:

P = Provisional. Data inserted manually will become provisional. This is the lowest security level.

V = Verified. Provisional data can be lifted to verified by running a process.

A = Approved. This is the highest security level. A monthly process will set data to approved.

Data status can be updated from P to V and from V to A, as well as in the reverse direction. The revision tracking will track the record status being updated in both directions. Status process will not be triggered if the date is within a locked month.

When defining a status process, the goal is to create an UPDATE statement with a WHERE condition to update the record status. Status process will use a WHERE formula to specify the checks. In the new design of Status Processes screen, there are three columns to support the WHERE condition as described below:

Where Clause (existing): will be a non-editable column

Where Formula: a new column to replace Where Clause to specify the Where condition

Where SQL: generated Where condition based on the Where Formula

Existing data in the Where Clause from prior to the migration will continue to be supported. However, any updates or new entries for the Where conditions must adhere to the new definition of the Where formula method in the Where Formula column.

Access to the Status Process screen could be disabled. To get the access to the screen, open the Object Maintenance screen and give proper access level to the relevant roles.

Object Name: /com.ec.prod.co.screens/status_processes

Description: Status Processes

Status Process – Where Formula

The WHERE condition to the Status Process is specified as a formula. The formula supports:

Keywords (AND, OR, IS NULL, IS NOT NULL, IN, LIKE, NULL, NOT, NVL, COALESCE, SUBSTR, LENGTH, ROUND, TRUNC, COUNT, MAX, MIN, ABS, GREATEST, LEAST, SYSDATE, DECODE, BETWEEN, CASE, WHEN, THEN, ELSE, END, EXISTS, ADD_MONTHS, LAST_DAY)

Special characters (<, ⇐, =, ⇒, >, <>, !=, ( ,) )

Numbers

Variables defined as ${variable name}.Example:

(${fcty_class_1} = ${ConstFCTY1})

(${fcty_id} = ${FuncFCTY1})

Variables are automatically created when the process task is saved (and the WHERE formula is updated).A variable can be

Constant (free text, cannot contain ";")

Attribute from the RV of Class name

Function call (call to a function in a package)

Sub query (only sub query from one view is supported)

Variables are automatically created when the WHERE formula is stored in the database. It is not possible to manually add variables.

${ConstXXX} will create a variable type ‘Constant’

${FuncXXX} will create a variable type ‘Function’

${SubQueryXXX} will create a variable type ‘Sub query’

Constant and Attribute

A constant can be used to check the value based on the defined attributes.

Example 1: Get the records which belong a facility ‘P1_FCTY_STATUS_PROCESS’

Where conditions

	

Where formula


…[truncated]


==========================================================================================
## [4/22] Deferment (PD.0020)
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_deferment_pd.0020.html
==========================================================================================
Deferment (PD.0020)
Introduction

This document provides a detailed explanation of deferment events and event loss calculation in the Deferment (PD.0020).

General Description of Deferment and Event loss calculation

A deferment is an event that leads to production or injection not meeting the planned production or injection numbers. The Deferment (PD.0020) screen can be used to enter and calculate deferment losses.

A deferment can affect only a single well or multiple wells. The deferment can be either a reduced flow rate of the wells (constraint deferment) or a full shut-in of the wells (down deferment).

Types of deferment events

Both down and constraint deferments can be recorded against:

Single well only

Group (without linked wells)
Deferment events on the Operator Route, Collection Point, Facility, Well Hookup, Equipment, or Tank level, without any linked wells.

Group (with linked wells)
Deferment events with linked wells grouped using 'Parent' which are Operator Route, Collection Point, Facility, Well Hookup, Equipment, and Tank.

Pre-requisite

The wells in single and group events should be set to 'Open Normal’ status in Maintain Well Status (WR.0088).

If there is any locked month within the deferment event period, the event loss volume will not be calculated.

Deferment Event Loss Calculation

Deferment calculation will be triggered for deferment events which are updated prior to the last calculation run. This can include new deferment events, updates to the existing events, or deletion of events as well as overlapping events with other events.

Deferment losses can be calculated using:

Calculate Deferment button in Deferment (PD.0020)
The Calculate Deferment button will run the 'DefermentRecalculation' scheduler event which is defined in Business Actions (CO.0127).

Scheduler job
Users can configure the parameters to be used for a scheduler job in the Business Actions screen (CO.0127) for DefermentRecalculation action. The Schedules (CO.0130) screen can be used to configure the scheduled job.

Run Calculations button in Period Deferment Calculation (PD.0010)
The Run Calculations button will run the EcDp_Deferment.periodDefermentCalc database procedure to run the event loss calculation based on the defined period and object in the navigator for the screen. The events will not be recalculated (by removing them from the intermediate table) if the event’s start and end daytime are within the selected period.

Downtime duration is calculated based on Start Daytime and End Daytime. Event losses are calculated based on the following conditions:

If Loss Volume is empty and Loss Rate is specified, then Event Loss = Loss Rate * Downtime Duration.

If both Loss Rate and Loss Volume are not empty, then Event Loss will equal to Loss Volume.

When loss volume is entered, event loss will be calculated based on the entered loss volume regardless of the settings defined.

The default event loss calculation has the precedence as below:

Down events take precedence over Constraint events.

Deferments with earlier start time take precedence.

Unscheduled events take precedence over Scheduled events.

Single event takes precedence over Group eve
…[truncated]


==========================================================================================
## [5/22] Operation Mode
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_operation_mode.html
==========================================================================================
Operation Mode
1 Introduction

This document provides a detailed explanation for the Operation Mode feature available in EC-13.1.0.

2 General Description of Operation Mode

Operation mode is a feature that allows users to quickly change production mode for a well for a single day without creating a new version in the configuration screens. The operation mode can be considered as a template-like configuration that allows the operations to apply the setting on top of the existing configuration. This feature is currently only supported for the daily operation of Well objects. Operation mode is configured at the daily level, but will also impact the sub-daily calculated values. Operation mode is not supported for monthly well business functions.

3 Configuration Business Functions
3.1 Well Mode Attributes (CO.0255)

The Well Mode Attributes screen is used to show all available attributes based on the attributes in the Well (CO.0049) screen. The user can configure which attributes will be displayed in the Well Mode (CO.0256) screen by enabling the attribute in this screen. Attributes that are unique to each Well object (like ID, name and code), linked objects (like Quality Stream and Group Model) and functions will be excluded from the list. Attributes that are hidden and disabled in the Well object screen will be excluded as well. Excluded attributes include:

Group model relation (CP_*, OP_*, GEO_*)

Dates (DAYTIME, END_DATE, OBJECT_START_DATE, OBJECT_END_DATE)

Object identifier (*_ID, OBJECT_NAME, NAME)

ALLOC_*

BH_*

*_UOM

COMP_*

*_UTM

WELL_METER_*

Monthly attribute (*_MTH)

WELL_REFERENCE_OBJECT

DESCRIPTION

MASTER_SYS_CODE

MASTER_SYS_NAME

APPROACH_METHOD

BF_PROFILE

DEPTH_MEAS_REF

INSTRUMENTATION_TYPE

LATITUDE & LONGITUDE

ON_STREAM_METHOD

PROD_METHOD

PUMP_TYPE

REF_OIL_FLUID_STATE

RKB_HEIGHT

SHAFT

WELL_TEST_METHOD

FORECAST_TYPE & FORECAST_SCENARIO

DETAILED_PROD_METHOD

Sync Attributes button will synchronize the attributes between Well (CO.0049) configurations and Well Mode (CO.0256). This button will synchronize:

Custom attributes that were added into OV_WELL class. This button will add the new custom attributes and they will be listed on this screen.

Attributes that are set as disabled or hidden in OV_WELL class. This button will remove those attributes from the attributes list in Well Mode Attributes (CO.0255) and Well Mode (CO.0256).

A confirmation message will be displayed prior to synchronization, as this will delete the attributes if any of the attributes have been set to disable or hidden in OV_WELL class.  Rollback is not available once the attributes have been deleted.


Enabling and disabling the attributes in Well Mode (CO.0256) can be controlled using the Enabled checkbox. All attributes that have been enabled, will be available in the Well Mode (CO.0256) screen even for the previously added records. However, if any of the attributes have been disabled, those attributes will be removed from Well Mode (CO.0256). A confirmation message will be displayed prior to deletion.


3.2 Well Mode (CO.0256)

The Well Mode screen is used to create a new well mode and configure all the relevant methods.  Only attribute
…[truncated]


==========================================================================================
## [6/22] Default Client Value
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_default_client_value.html
==========================================================================================
Default Client Value
1 Introduction

This document provides guidance on default date configuration of date attributes for new insert record using class attribute property DEFAULT_CLIENT_VALUE.

2 Types of DEFAULT_CLIENT_VALUE

The class attribute property DEFAULT_CLIENT_VALUE provides flexibility in configuring the various default values for date attributes. Below are the DEFAULT_CLIENT_VALUE property values and their functionality.

Note:

Current configuration is set to derive the default date for attribute DAYTIME based on the navigator To Date and to truncate the derived default date to hour (For example 2023-07-14 07:44:00 to 2023-07-14 07:00:00). Refer the section 4 - Screen xhtml file configuration.

In this section, the examples of class configuration are given by using the product’s Owner Context (0 is only used for product), please use the project’s Owner Context.

2.1 NULL

To get attribute with default value as NULL/Blank in new insert.

Example: The property DEFAULT_CLIENT_VALUE of attribute DAYTIME of table class WELL_DEFERMENT is set to NULL.

Below is the screenshot of EC screen Class Attribute Configuration for class WELL_DEFERMENT and attribute DAYTIME:

Below is the screenshot of EC screen Deferment (PD.0020):

2.2 NOW

To get attribute with default value as system date in new insert. Current system time zone is Europe/Oslo.

Example: The property DEFAULT_CLIENT_VALUE of attribute DAYTIME of table class WELL_DEFERMENT is set to NOW.

Note that the current system date and time is Friday, 14 July 2023 7:44 am.

Below is the screenshot of EC screen Class Attribute Configuration for class WELL_DEFERMENT and attribute DAYTIME:

Below is the screenshot of EC screen Deferment (PD.0020):

2.3 YESTERDAY

To get attribute with default value as “system date – 1” (yesterday) truncated to day in new insert.

Example: The property DEFAULT_CLIENT_VALUE of attribute DAYTIME of table class WELL_DEFERMENT is set to YESTERDAY.

Note that the current system date and time is Friday, 14 July 2023 4:44 pm (time zone is Europe/Oslo).

Below is the screenshot of EC screen Class Attribute Configuration for class WELL_DEFERMENT and attribute DAYTIME:

Below is the screenshot of EC screen Deferment (PD.0020):

2.4 PROD_DAY_START

To get attribute with default value as “Navigator To Date truncated to day + Offset” in new insert.

The navigator To Date truncated to day implies that the time stamp of that day is set to 00:00:00 (hh:mi:ss).

Example: The property DEFAULT_CLIENT_VALUE of attribute DAYTIME of table class WELL_DEFERMENT is set to PROD_DAY_START.

Below is the screenshot of EC screen Class Attribute Configuration for class WELL_DEFERMENT and attribute DAYTIME:

Case 1: Positive offset

Navigator To Date is 2023-07-01 (yyyy-mm-dd) and Offset is 8.

Below is the screenshot of EC screen Deferment (PD.0020):

Case 2: Negative offset

Navigator To Date is 2023-07-01 (yyyy-mm-dd) and Offset is -8.

Below is the screenshot of EC screen Deferment (PD.0020):

2.5 TO_DATE_PROD_START

To get attribute with default value as:

If Offset is positive, then default value is “Navigator To Date + Offset”.

If Offset is negative, then default value is “(Navigat
…[truncated]


==========================================================================================
## [7/22] API Measurement Standards in Energy Components
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_api_measurement_standards.html
==========================================================================================
API Measurement Standards in Energy Components
Introduction

In this document, Gross Observed Volume (GOV) calculation for tanks will be explained based on reference from Manual of Petroleum Measurement Standards Chapter 12.1.1, 3rd edition, April 2012.

1.0 Calculation of Gross Observed Volume (GOV)

Gross Observed Volume (GOV) is calculated by deducting any free water (FW) from the total observed volume (TOV) and multiply by tank shell temperature correction (CTSh) and, applying the floating roof adjustment (FRA) or floating roof correction (FRC) where applicable.

1.1 Total Observed Volume (TOV)

Total observed volume is also known as gross volume in Energy Components (EC). The gross volume can be calculated based on the method defined in the Manage Tank (CO.0252) under Tank Grs Vol Method.

1.2 Adjustment for the Presence of Free Water (FW)

Free water (FW) adjustments will always be in the form of volumetric deduction. Free water volume calculation is based on the Free Water Vol Method defined in Manage Tank (CO.0252).

1.3 Correction for Temperature of Shell (CTSH)

Tank volume is subjected to changes in temperature. Changes in temperature will impact the volume in tank. If the observed tank shell temperature (TSh) differs from the capacity table’s tank shell reference temperature (TShREF), the volumes extracted from that table can be corrected accordingly.

Storage tanks differ from test measures in size and thickness. Differences also occur because the tanks cannot readily be sheltered from the elements. Therefore, ambient temperatures as well as product temperatures(run/line) must be considered when calculating an appropriate correction for the effect of temperature on the shell of the tank.

The correction factor for temperature on the shell of the tank (CTSh) is calculated by using the formula:

α is a linear coefficient of expansion constant based on tank material (refer to 1.3.1 Tank Material)

ΔT is Tank Shell Temperature (TSh) - Tank Shell Reference Temperature (TShREF)

1.3.1 Tank Material

Linear coefficient of expansion constant is based on tank material which needs to be configured under the Tank Material in Manage Tank (CO.0252) screen.

Material

	

Metric Unit (oC)

	

Oil Field (oF)




Mild Steel

	

0.00001116

	

0.0000062




Carbon steel

	

0.0000112

	

0.00000620




Monel

	

0.0000139

	

0.00000772




Type 316 stainless steel

	

0.0000160

	

0.00000899




Type 304 stainless steel

	

0.0000173

	

0.00000961

1.3.2 Tank Shell Reference Temperature (TShREF)

Tank Shell Reference Temperature (TShREF) is normally disclosed on the capacity table, and it is the tank shell temperature which capacity table volumes were calculated to, typically 60oF, 15oC or 20oC. This can be configured in System Attributes (CO.1012) under attribute type REF_TEMP_TANK_SHELL. The default value is 15oC. The value should be entered as Fahrenheit if the unit of measurement used for TEMP is oF.

1.3.3 Tank Shell Temperature (TSh)

Tank Shell Temperature (TSh) calculation depends on if the tank is insulated or non-insulated metal tanks. This can be configured in the Manage Tank (CO.0252) screen under the Insulated checkbox. The default
…[truncated]


==========================================================================================
## [8/22] Daily Allocation BPM Workflow
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/bpm/prod_daily_allocation_bpm_workflow.html
==========================================================================================
Daily Allocation BPM Workflow
1 Introduction

Energy Components (EC) includes functionality for automating business processes. This will significantly reduce the number of manual actions executed by users daily and allow us to move to a ‘Work by Exception’ approach. A user will only need to interact with the business process when needed functionally or to handle exceptions.

EC can run business processes that have been captured and engineered in a BPMN (Business Process Model Notation) design. The BPMN designed processes will have generic – configurable – warning/error handling and user task notification.

This document will focus on providing generic BPM functionality that can be applied to every asset to automate the daily allocation process.

2 How to deploy production bpm artifacts

BPM workflows need to be deployed in EC using the BPM zip file. This file can be found at (Insert Nexus link).

The steps to deploy workflow are as below:-

Download the latest BPM artifacts from nexus (URL: https://hub.energycomponents.com/#browse/browse:downloads:com%2Fec%2Fprod%2Fprod-bpm-building-blocks).

Login to EC and navigate to ‘Project Management’ business function

Add a new record for production allocation template with input values as below-

Name = ECProd_RunAllocationProcess

Group Id = com.ec.bpm

Artifact Id = prod-bpm-building-blocks

Version = 1.0

Once the new record is added, deploy the bpm artifact by clicking on 'Choose File', 'Upload and Deploy' buttons.

After uploading the artifacts, you should see below records on ‘Project Management’ business function.

Now deployment of production’s BPM artifacts is done, and process can be executed using ‘Process execution’ business function.

Design

EC comes with several easy-to-use BPMs that only require proper put parameter values, delivering certain functionality like:-

Running check rules (incl. class & object validation and check rule)

Run Status Process for Data verification (updates data from provisional to verified status)

Running calculation (Including Excel or MathML based calculations)

Removing Ghost Data (applies only for Production allocation)

Approve Allocation.

Generate a report (Jasper, Excel, or BO), optionally verify, approve and send the same on email.

The next paragraphs will contain details for the design.

3 Design - Standard Main Daily Allocation Process

The standard process for daily allocation consists of the following subprocesses:

Mandatory Input data initialization

Mandatory input validation.

Optional Run data pre-checks (Execution of check rules along with object & class validations).

Optional Run data verification process (e.g., Provisional to Verified)

Optional Run allocation.

Optional Ghost Data Cleanup

Optional Run report process.

Optional Approve allocation process.

The Input parameters for BPM processes are categorized in below two types:-

Static Parameters – Parameter for which value is already in Process template and can be updated depending on the steps that user wants to execute.

Dynamic Parameters – Parameters for which user needs to provide value each time they trigger process from Process Execution screen.

Below is the list of parame
…[truncated]


==========================================================================================
## [9/22] Monthly Allocation BPM Workflow
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/bpm/prod_monthly_allocation_bpm_workflow.html
==========================================================================================
Monthly Allocation BPM Workflow
1 Introduction

Energy Components (EC) includes functionality for automating business processes. This will significantly reduce the number of manual actions executed by users daily and allow us to move to a ‘Work by Exception’ approach. A user will only need to interact with the business process when needed functionally or to handle exceptions.

EC can run business processes that have been captured and engineered in a BPMN (Business Process Model Notation) design.

The BPMN designed processes will have generic – configurable – warning/error handling and user task notification.

This document will focus on providing generic BPM functionality that can be applied to every asset to automate the monthly allocation process.

2 How to deploy production bpm artifacts

BPM workflows need to be deployed in EC using the BPM zip file. This file can be found at (Insert Nexus link).

The steps to deploy workflow are as below:-

Download the latest BPM artifacts from nexus (URL: https://hub.energycomponents.com/#browse/browse:downloads:com%2Fec%2Fprod%2Fprod-bpm-building-blocks).

Login to EC and navigate to ‘Project Management’ business function.

Add a new record for production allocation template with input values as below-

Name = ECProd_RunAllocationProcess

Group Id = com.ec.bpm

Artifact Id = prod-bpm-building-blocks

Version = 1.0

Once the new record is added, deploy the bpm artifact by clicking on 'Choose File', 'Upload and Deploy' buttons.

After uploading the artifacts, you should see below records on 'Project Management' business function.

Now deployment of production’s BPM artifacts is done, and process can be executed using 'Process execution' business function.

Design

EC comes with several easy-to-use BPMs that only require proper put parameter values, delivering certain functionality like:-

Running check rules (incl. class and object validation).

Run Status Process for Data verification (updates data from provisional to verified status).

Running calculation (Including Excel or MathML based calculations).

Removing Ghost Data (applies only for Production allocation).

Generate a report (Jasper, Excel, or BO), optionally verify, approve and send the same on email.

Run Status Process for Data approval (Update data from verified to approved status) & Approve allocation.

The next paragraphs will contain details for the design.

3 Design - Standard Main Monthly Allocation Process

This standard process for Monthly Allocation consists of the following subprocesses:-

Mandatory input data initialization.

Mandatory input validation process.

Optionally Run data pre-checks (Execution of check rules along with object & class validations).

Optionally Run data verification process (e.g., Provisional to Verified).

Optionally Run allocation.

Optionally removing Ghost Data.

Optionally Generate, Verify, Approve report process.

Optionally Approve Data (Update data from verified to approved status) & approve Allocation.

Optionally Month Lock user task.

The Input parameters for BPM processes are categorized in below two types:-

Static Parameters – Parameter for which value is already in Process template and can 
…[truncated]


==========================================================================================
## [10/22] Analytics Integration BPM Workflow
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/bpm/prod_analytics_integration_bpm_workflow.html
==========================================================================================
Analytics Integration BPM Workflow
1 Introduction

Energy Components (EC) includes functionality for automating business processes. This will significantly reduce the number of manual actions executed by users daily and allow us to move to a ‘Work by Exception’ approach. A user will only need to interact with the business process when needed functionally or to handle exceptions.

EC can run business processes that have been captured and engineered in a BPMN (Business Process Model Notation) design.

This document provides comprehensive technical documentation for integrating a third-party system with Energy Component by using Business Process Management (BPM) workflow.

2 How to deploy production bpm artifacts

BPM workflows need to be deployed in EC using the BPM zip file. The steps to deploy workflow are as below:

Download latest BPM artifacts from hub - (URL: https://hub.energycomponents.com/#browse/browse:downloads:com%2Fec%2Fprod%2Fprod-bpm-building-blocks).

Login to EC and navigate to ‘Project Management’ business function.

Add a new record for analytics integration workflow template as below and save the record.

Name = ECProd_AnalyticsIntegrationWorkflow

Group Id = com.ec.bpm

Artifact Id = prod-bpm-building-blocks

Version = 1.0

Once the new record is added, deploy the bpm artifact by clicking on ‘Choose File’, ‘Upload and Deploy' buttons.

After uploading the artifacts, you should see below records on ‘Project Management’ business function.

Now deployment of production’s BPM artifacts is done, and process can be executed using ‘Process execution’ business function.

3 Overview Of Analytics Integration Workflow

This document provides comprehensive technical insights on integrating third-party systems with Energy Component by using Business Process Management (BPM) workflow and Analytics Manager.

The integration aims to enhance the efficiency and functionality of EC by leveraging external applications' capabilities.

This Workflow can be used to interact with external simulators, e.g. HYSYS, PROSPER, PREVISO or to connect with external APIs and get some required data.

High Level Design

Below Illustration shows the high-level connectivity design of EC – Analytics Manager – External Application Integration:

EC interacts with External Application via Analytics Manager, and Analytics Manager then connects to external applications.

Whenever a new external system wants to integrate with EC, Analytics will need to develop a new API to support the same.

EC will only need to configure new REST API endpoints, GraphQL query, and user exit to save response from external system.

End to End Dataflow

Detailed end to end dataflow between EC – Analytics Manager – External System:

When Analytics Integration workflow is executed -

It first checks for mandatory configuration such as API endpoints or GraphQL query etc. If the required configurations are missing, then the workflow will create a user task requesting user to add the missing configuration.

Once everything is configured correctly, workflow will execute GraphQL query to extract the required data from EC data models in JSON format and then share it with POST job analytics API.

…[truncated]


==========================================================================================
## [11/22] Analysis Data Management BPM Workflow
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/bpm/prod_analysis_data_management_bpm_workflow.html
==========================================================================================
Analysis Data Management BPM Workflow
1 Introduction

Energy Components (EC) includes functionality for automating business processes. This will significantly reduce the number of manual actions executed by users daily and allow us to move to a 'Work by Exception' approach. A user will only need to interact with the business process when needed functionally or to handle exceptions.

EC can run business processes that have been captured and engineered in a BPMN (Business Process Model Notation) design.

This document provides comprehensive technical documentation for management of Analysis Data by using Business Process Management (BPM) workflow.

2 How to deploy production bpm artifacts

BPM workflows need to be deployed in EC using the BPM zip file. The steps to deploy workflow are as below:

Download latest BPM artifacts from hub - (URL: https://hub.energycomponents.com/#browse/browse:downloads:com%2Fec%2Fprod%2Fprod-bpm-building-blocks).

Login to EC and navigate to 'Project Management' business function.

Add a new record for analysis data management workflow template below and save the record.

Name = ECProd_AnalysisDataManagement

Group Id = com.ec.bpm

Artifact Id = prod-bpm-building-blocks

Version = 1.0

Once the new record is added, deploy the bpm artifact by clicking on 'Choose File', 'Upload and Deploy' buttons.

After uploading the artifacts, you should see below records on 'Project Management' business function.

Now deployment of production’s BPM artifacts is done, and process can be executed using 'Process execution' business function.

3 Overview Of Analysis Data Management Workflow

This document provides comprehensive technical insights for Analysis Data Management workflow. Analysis Data Management workflow performs validation, processing and acceptance of analysis data in a structured and automated manner. This workflow is critical for managing analysis data, ensuring data quality, and facilitating business processes efficiently.

This workflow is designed to process the analysis data in bulk, processing includes operation on analysis data e.g. Mol to WT, WT to Mol, Mol to Energy, Normalization etc.

This workflow aims to save time and effort for end users, as it automatically validates & processes the data across screens, ensuring exception only interaction with system and makes it easier for end users to interact with Energy Components for running operations related to analysis data.

High Level Design

The Illustration below shows the high-level design of Analysis Data Management workflow:

When Analysis Data Management workflow is executed, then workflow performs below steps : -

Input Validation/Initialization: The process starts by initializing variables and ensures that all required parameters are present and valid before further processing.

Data Validation: This step calls the exiting building block which validates the data based on configured rules, if the check rule returns error/warning, then user task is created to fix those errors and warnings.

Data Verification: This step calls the exiting building block which executes the status process to update data to verified state from provisional.

Data Processing: 
…[truncated]


==========================================================================================
## [12/22] Hydrocarbon Accounting
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_hydrocarbon_accounting.html
==========================================================================================
Hydrocarbon Accounting
1 Introduction

The Hydrocarbon Accounting business area covers functionality for data verification & approval, reconciliation and allocation. Reconciliation is a volumetric or mass/component balancing of the fluids of a production system whereby the sum of the well/reservoir contributions to the system, are adjusted to equal the total outgoing volume or mass per phase. For each individual calculation node, the sum of incoming streams will be adjusted to balance with the sum of outgoing streams. Well allocation is in principle the same as reconciliation, but the incoming ‘streams’ are wells streams.

The allocation module supports volumetric and mass/component allocation on a daily and monthly basis, however only volumetric calculations are included by default:

Delivery point measurements of oil, gas and water are allocated back to individual production wells.

Master gas and water injection volumes are allocated to individual injection wells.

Master gas lift volumes are allocated to individual gas lifted wells.

Master diluent volumes are allocated to diluted wells.

The allocation module performs its calculations in the context of an allocation network. An allocation network is a logical model of the oil production infrastructure. Multiple allocation networks may be defined in an EC Production installation. The networks consist of objects that represent production wells, injection wells, platforms, terminals, etc. These objects are referred to as nodes. The hydrocarbon flows that connect the network objects are referred to as streams.

The image below shows an example of allocation network:

Figure 1. Sample of allocation network

The Goldfish field consists of three platforms, the Gray Seal Offshore Facility A, the Gray Seal Offshore Facility B and the Gray Seal Offshore Facility C. The production from the Goldfish field are declining and only a few producing wells and a number of injectors are still in operation. There are 5 wells producing into the Gray Seal C facility, the primary phase is oil. Further, 3 wells are injecting water and/or gas from the Gray Seal A facility. All oil and the majority of the gas is exported from the Gray Seal C facility. Gray Seal A receives produced water and any gas not exported and injects that back into the reservoir.

The allocation network above is depicted in EC using Stream Node Diagram as below:

Figure 2. Sample allocation network in Stream Node Diagram

Allocation calculations implement the algorithms used to determine reconciled data from the initial measurements and estimates. The allocation module splits delivery point measurements and master injection measurements back to the wells by simple pro-rating. The module supports the use of daily and monthly allocation/reconciliation factors.

Different business areas and operations need different calculations, owing to both physical and commercial differences.

EC supports three types of calculations:

Equation-based calculations:

This calculation type uses a special mathematical syntax to express calculations. This mathematical syntax has been developed specifically for the type of calculations typically performed in EC an
…[truncated]


==========================================================================================
## [13/22] Stream Node Diagram
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_stream_node_diagram.html
==========================================================================================
Stream Node Diagram
1. Introduction
1.1 What is this Document About?

This document gives an overview of available functionality in this version of the Stream Node Diagram Business Function.

1.2 Who will Find this Document Useful?

This document is intended to support personnel implementing and using the Stream Node Diagram Business Function.

1.3 Versions / Applicability

The Stream Node Diagram Business Function information presented here is pertinent to Energy Components Release 11.2-SP01 onward.

1.4 Document structure

This document will first give an introduction to some general concepts of the business function. Further, one section details the network visualization capabilities, another section details the network configuration change capabilities.

2. Stream Node Diagram
2.1 Screenshot

2.2 Description

The Stream Node Diagram Business Function is a tool that can be used to define and view allocation stream/node networks and layouts. It provides a comprehensive diagramming component to support visualization and configuration of the objects used during allocation.

An allocation network is a collection of streams and nodes that form a logical model of the infrastructure. Although the name is Allocation Network, it is actually a Calculation Network, where other calculations than allocation calculations can be done. Examples are Production Sharing Agreement calculations and Deferment calculations. The allocation network can be edited using the Allocation Network (CO.0084) screen. Nodes can be added to the network from the Calculation Group Setup (CO.0246) screen.

2.2.1 Installation and Startup

The Stream Node Diagram Business Function is based on an EC initiative for richer client functionality than the traditional web screens.

If the default configuration is used the tool can be found in the EC application treeview under Configuration → Assets → Calculation Objects with the title “Stream Node Diagram”. The network diagram screen will appear when clicking on the link.

After loading the screen the user must select a date to view the network for. The user must also select one specific allocation network. Only objects from that network will be displayed. By clicking the “Go” button, the network diagram will be loaded and shown in the diagram area.

2.2.2 User Access Levels

The Business Function can be used with two different access levels. With read-only access, the user is able to view and export the network view. With edit access the user may, in addition to the capabilities of read-only access level, edit the layout of the network, add objects into the diagram and save it.

2.2.3 Menu

The main toolbar contains global EC Product controls. The actions include save that saves the changes to the diagram and refresh that reloads the Business Function. Within the Stream Node Diagram Business Function screen, an input date specifies which date to show the network for. A dropdown specifies which allocation network to show.

2.2.4 Context Menu

A context menu is available within the network diagram part of the view area. The menu is activated by clicking the right-hand mouse button anywhere in the diagram. Some context menu actions will o
…[truncated]


==========================================================================================
## [14/22] Removing Ghost Data in Production Allocation tables/classes
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_removing_ghost_data_from_product_calculations.html
==========================================================================================
Removing Ghost Data in Production Allocation tables/classes
1. Background

This User Guide provides information on how to remove ghost data from allocation result tables. Ghost data are allocated data that have records in the allocation tables, but the records are no longer valid. This could be caused by changes in the configuration such as if a well changed from producer to injector.

There are two ways to execute removal of ghost data in production allocation tables:

Existing approach: User exit package (UE_CALC_ENGINE) which can be called from the calculation engine. Examples can be found in Approach 1 section. A good knowledge of allocation in EC is expected to implement the suggested solution.

New approach: A standard procedure named EcDp_Allocation.dataCleanup for removing ghost data has been introduced. This procedure is executed in the optional process block of Daily and Monthly Production Allocation BPM workflow. This package may also be called from a scheduler job which can be configured by the project.

2. Allocation Tables

EC provides a list of allocation tables to support different types of allocation as below:

Object	Daily Allocation Table	Monthly Allocation Table


Stream

	

STRM_DAY_ALLOC

STRM_DAY_CPY_ALLOC

STRM_DAY_COMP_ALLOC

STRM_DAY_PC_ALLOC

STRM_DAY_PC_CPY_ALLOC

STRM_DAY_PC_CP_CPY_ALLOC

STRM_DAY_PC_CP_ALLOC

STRM_DAY_PROD_ALLOC

STRM_DAY_PROD_CP_ALLOC

STRM_DAY_PROD_CPY_ALLOC

	

STRM_MTH_ALLOC

STRM_MTH_CPY_ALLOC

STRM_MTH_COMP_ALLOC

STRM_MTH_PC_ALLOC

STRM_MTH_PC_CPY_ALLOC

STRM_MTH_PC_CP_CPY_ALLOC

STRM_MTH_PC_CP_ALLOC

STRM_MTH_PROD_ALLOC

STRM_MTH_PROD_CP_ALLOC

STRM_MTH_PROD_CPY_ALLOC




Well

	

IWEL_DAY_ALLOC

PWEL_DAY_ALLOC

PWEL_DAY_COMP_ALLOC

PWEL_DAY_PROD_ALLOC

PWEL_DAY_CPY_PROD_ALLOC

	

IWEL_MTH_ALLOC

PWEL_MTH_ALLOC

PWEL_MTH_COMP_ALLOC

PWEL_MTH_PROD_ALLOC

PWEL_MTH_CPY_PROD_ALLOC




Perforation Interval

	

PERF_DAY_ALLOC

PERF_DAY_COMP_ALLOC

PERF_DAY_PROD_ALLOC

PERF_DAY_CPY_PROD_ALLOC

	

PERF_MTH_ALLOC

PERF_MTH_COMP_ALLOC

PERF_MTH_PROD_ALLOC

PERF_MTH_CPY_PROD_ALLOC




Allocation Objects

	

OBJECT_DAY_DIM1_ALLOC

OBJECT_DAY_DIM2_ALLOC

OBJECT_DAY_DIM3_ALLOC

OBJECT_DAY_DIM4_ALLOC

OBJECT_MTH_DIM1_ALLOC

OBJECT_MTH_DIM2_ALLOC

OBJECT_MTH_DIM3_ALLOC

OBJECT_MTH_DIM4_ALLOC

OBJECT_MTH_DIM5_ALLOC

	

OBJECT_DAY_DIM1_ALLOC

OBJECT_DAY_DIM2_ALLOC

OBJECT_DAY_DIM3_ALLOC

OBJECT_DAY_DIM4_ALLOC

OBJECT_MTH_DIM1_ALLOC

OBJECT_MTH_DIM2_ALLOC

OBJECT_MTH_DIM3_ALLOC

OBJECT_MTH_DIM4_ALLOC

OBJECT_MTH_DIM5_ALLOC

Approach 1: Ghost Data Cleanup using UE_CALC_ENGINE

In this user guide, we will only provide an example for the commonly used allocation tables which are STRM_DAY_ALLOC, PWEL_DAY_ALLOC, IWEL_DAY_ALLOC, PERF_DAY_ALLOC, STRM_MTH_ALLOC, PWEL_MTH_ALLOC, IWEL_MTH_ALLOC and PERF_MTH_ALLOC.

These are the parameters to be passed to the procedure in UE_CALC_ENGINE:

Alloc_job_log.run_no for the calling calc engine transaction

End date for the calling calc engine transaction

Value of 'startdate' calc engine parameter

Value of 'enddate' calc engine parameter

Value of 'context' calc engine parameter

Value of 'jobcode' calc engine parameter

Value of 'loglevel' calc engine parameter

Value of 
…[truncated]


==========================================================================================
## [15/22] Multi Well Testing
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_multi_well_testing.html
==========================================================================================
Multi Well Testing
1 Introduction
1.1 What is this Document About?

This document provides information relates to how multi well testing can be performed in EC and the related business functions.

1.2 Who will Find this Document Useful?

This document is intended to support personnel implementing multi well testing in EC.

1.3 Versions / Applicability

The related business functions presented here is pertinent to Energy Components Release 13.0 onward.

1.4 Document structure

This document will first introduce some general concepts of the business function. Further, one section details the examples with regards to the configuration and test result calculations.

2 Multi Well Testing
2.1 Multi Wells Testing Flow

2.2 Business Function Description

The process to complete multi wells testing is as below: -

No	Description	Business Function


1.

	

Define Well Test (start time, end time, test device, flowline, well, wbi & test device phase outlets)

	

Production Test Define (PT.0005)




2.

	

Gather or collect high frequent (typically 5min) data from data historians (PI or other) for test device, flowline, wells and well bore intervals.

	

Stable Period and Summarise (PT.0009)




3.

	

Optionally, manually register events (sampling and observations for TD, FL, Well and WBI.

	

Production Test Events (PT.0007)




4.

	

Select a stable period using stability criteria.

	

Stable Period and Summarise (PT.0009)




5.

	

Summarise the results to produce aggregated raw-data results in Production Test Results (PT.0010).

	

Stable Period and Summarise (PT.0009)




6.

	

Set Primary and Flowing flags for related wells in all results.

	

Production Test Results (PT.0010)




7.

	

Pre-process to produce test device fluid rate results at the flowing condition

	

Production Test Results (PT.0010)




8.

	

Calculate PVT to produce test device fluid rate results at standard conditions

	

Production Test Results (PT.0010)




9.

	

For multi wells testing, there is an additional step to calculate the result using combined results as explained in the section below.

	

Production Test Combination (PT.0011)




10.

	

Compare new results with previous test results and Accept with a valid from date or reject the well test result

Direct approval or Rejection without comparison.

	

Enhanced Production Well Test Validation (PT.0025)

Production Test Result (PT.0010)

2.2.1 Production Test Define (PT.0006)

This business function is used to connect the test device, flowlines, and wells on test. Well bore intervals are populated automatically for the connected wells.

Preprocess button is used to reselect the Test Device meter rates for Oil/Gas/Water meters. This action will update the selected meter values in ‘Data Test Device’ tab of Stable Period and Summarise (PT.0009).

When a well is inserted in Wells on Test data section, Flowlines that are linked to the well in Flowline Well Connection (CO.0067) will be also be inserted in Flowlines on Test data section based on valid date period.

Default test device will be selected based on configuration in Well/ Test Device configuration screen. If Auto-populate Multi Well checkbox is checked in Te
…[truncated]


==========================================================================================
## [16/22] Production Test Result - PreProcessing and Calculate PVT
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_prod_test_result_preprocessing_and_calculate_pvt.html
==========================================================================================
Production Test Result - PreProcessing and Calculate PVT
1 Introduction

This document provides a detailed explanation about the behaviour of PreProcess and Calculate PVT functionality in PT.0010 - Production Test Result.

2 General Description of PreProcess and Calculate PVT Buttons

Energy Components currently offers the following types of calculations:

2.1 Triangular conversions

Start time – End time – Duration (PreProcess)

Test volume – Test volumetric rate – Duration (PreProcess)

Volumetric rate – Mass rate – Density (PreProcess)

These calculations will be performed to the extent possible for each phase, and each fluid state, whenever there are 2 out of 3 data points available in each triangle.

Errors during the preprocessing will be generated and updated in the ptst_result.preprocess_log. There are three types of error codes: A, B, and C.

Error A: when there are at least 2 out of 3 attributes (volume, mass, and density) that are null.

Error B: when a volume attribute is 0 and mass is not 0. Volume cannot be 0 when the mass has a value different from 0.

Error C: when density is 0. Density cannot be 0 when mass and volume have a value different from 0.

2.2 Calculations involving mass transfer between phases

Purification of the oil phase by subtraction of dispersed water. (PreProcess)

Purification of the oil phase by subtraction of diluent injected pr. well for all participating wells. (PreProcess)

Purification of the gas phase by subtraction of lift gas injected pr. well for all participating wells. (PreProcess)

Correction of water phase by addition of water dispersed in the oil phase. (PreProcess)

Adding gas volume from residual saturation from the oil phase to the gas phase. (Calculate PVT)

Compensating for different fluid behaviour in the test device as compared to the full process. (Calculate PVT)

2.3 Calculations not involving mass transfer between phases

Volume changes (shrinkage/expansion) as a result of changes in temperature and pressure between test-measurement system and standard conditions.

2.4 Diagrams and detailed description

An overview of the flow of data and transactional attributes used can be found in the 3 figures as shown below. Detailed descriptions of the functionality are included in subsequent paragraphs. The diagrams are meant as a reference for those descriptions.

Diagram illustrating the data flow for the oil phase when activating the PreProcess and Calculate PVT buttons

Diagram illustrating the data flow for the gas phase when activating the PreProcess and Calculate PVT buttons

Diagram illustrating the data flow for the water phase when activating the PreProcess and Calculate PVT buttons

3 PreProcess Functionality
3.1 Entering Fully Pre-Processed Test Results

The correct way of entering production test results that originate from test analysis performed in external systems will depend on the state these data are in. If the results are completely preprocessed and no further calculations are required, the rate data can be entered directly into EC using the following rate attributes in the pwel_result_# classes:

Adjusted Rate Attributes	Description


net_oil_rate_adj

	

Well net oil rat
…[truncated]


==========================================================================================
## [17/22] Single Production Well Test Result (PT.0013)
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_single_production_well_test_result.html
==========================================================================================
Single Production Well Test Result (PT.0013)
1 Introduction

In this document, configuration advice and well test result calculation for Single Production Well Test Result (PT.0013) will be explained. This business function is used to store single production well test results. (Important Note : Multi records and/or multi well tests are not supported by this screen.)

When a well test is linked to a test device in data section 1, data section two will be populated. Data section two stores and displays the test device input data, plus calculated data before and after shrinkage functions.

Test Device Result – Input data

Test Device Result - Net Rates (prior to shrinkage)

Test Device Result - Net Rates at Standard Conditions (after shrinkage)

There are few ways to use this business function to calculate rates at standard conditions as below : -

Rates at standard conditions are available. No adjustment of values is needed.

Rates at flowing conditions are available and shrinkage needs to be applied to produce rates at standard conditions.

Gross rates are available but needs to deduct impurities (i.e. water, diluent, power water) prior to applying shrinkage.

Volumes are available, EC will then calculate rates based on duration of test and shrinkage.

2 Test Device

Test device is configured in Test Device (CO.0123).

Test device can be linked to a well in Manage Well (CO.0250). This is an optional configuration which enables the test device to be populated automatically when the well is inserted in Single Production Well Test Result (PT.0013).

2.1 Test Device Configuration

Test device configuration will be explained in the sections below. When a test device is assigned to a single well test result, 'Test Device Result' data section will be rendered in Single Production Well Test Result (PT.0013).

2.1.1 Instrumentation Type

Instrumentation type is required to populate the correct data class for 'Test Device Result' data section. There are 4 classes available to support relevant attributes for the test device.

Instrumentation Type	Description


Instr Type 1

	

Data class TDEV_PT_0013_1 will be used for the test device in PT.0013.




Instr Type 2

	

Data class TDEV_PT_0013_2 will be used for the test device in PT.0013.




Instr Type 3

	

Data class TDEV_PT_0013_3 will be used for the test device in PT.0013.




Instr Type 4

	

Data class TDEV_PT_0013_4 will be used for the test device in PT.0013.

2.1.2 Std Net Rate Method

This configuration is used to calculate values at standard conditions (values after shrinkage).

Std Net Rate Method	Description


<phase> Rate Std Adj Attributes

	

Oil or cond, gas & water net rates at Standard Conditions are available.




NetRateMethod adjusted for Shrinkage

	

Oil or cond, gas, & water net rates need to be converted to rates at Standard Conditions.




User Exit

	

Project/customer solutions.

Reference Function: Ecbp_TestDevice.findStdNetRate

2.1.3 Net Rate Method

This configuration is used to calculate or simply return values at flowing conditions. This method is required when Std Net Rate Method = NetRateMethod adjusted for Shrinkage.

Net Rate Method	Description


Net Oil Rate Flc

	
…[truncated]


==========================================================================================
## [18/22] Well Performance Curve
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_well_performance_curve.html
==========================================================================================
Well Performance Curve
Introduction

Well performance curves are supported in Well Performance Curves (PT.0003) to dynamically calculate estimated production and injection based on measured input parameters like choke, well head pressure, etc.

This document shows examples of graphs that are rendered using different formula types.

Graphs for each Formula Types

Supported Formula types:

No	Formula Type	Equation	Coefficient required


1

	

Linear

	

y = c1*x + c0

	

c0, c1




2

	

2nd Order Polynomial

	

y = c2*x^2 + c1*x + c0

	

c0, c1, c2




3

	

Inverted 2nd Order Polynomial

	

x = c2*y^2 + c1*y + c0

	

c0, c1, c2




4

	

3rd Order Polynomial

	

y = c3*x^3 + c2*x^2 + c1*x + c0

	

c0, c1, c2, c3




5

	

4th Order Polynomial

	

y = c4*x^4 + c3*x^3 + c2*x^2 + c1*x + c0

	

c0, c1, c2, c3, c4




6

	

5th Order Polynomial

	

y = c5*x^5 + c4*x^4 + c3*x^3 + c2*x^2 + c1*x + c0

	

c0, c1, c2, c3, c4, c5




7

	

Curve Points

	

None

	

None

Important Note:

Coefficients can be entered on the screen or calculated using the ‘Curve Fit’ button.

The axis for rate is configurable by setting the system attribute "PERF_CURVE_RATE_AXIS" to either X or Y in System Attributes (CO.1012). Default is X axis.

Example 1: Curve Point (no coefficient is required)

Example 2: Linear (Coefficients c0 and c1 are required)

Example 3: 2nd Order Polynomial (Coefficients c0, c1 and c2 are required)

Example 4: 3rd Order Polynomial (Coefficients c0, c1, c2 and c3 are required)

Example 5: 4th Order Polynomial (Coefficients c0, c1, c2, c3 and c4 are required)

Example 6: 5th Order Polynomial (Coefficients c0, c1, c2, c3, c4 and c5 are required)

Example 7: Inverted 2nd Order Polynomial (Coefficients c0, c1, and c2 are required)

Example 8: Previous curves when current curve is Linear

The draw feature not only plots the selected curve point set and curve function but also includes the plotting of previous curve points based on the 'Maximum Curves to Draw' selection. The previous curve must align with the parameter selection of the current curve and have a third axis parameter set to 'NONE' to be displayed. These previous curves are distinguished by a pale shade of grey to differentiate them from the currently focused curve.

In the screenshot below, previous graph is plotted for the following Valid from date when selected Valid from date is 2021-10-4:

2021-10-03

2021-10-02

Graph with Valid from date ‘2021-10-1’ is not included in the previous graphs since it has third axis set to ‘Pump Speed’.

Example 9: Curve point with third axis

Example 10: Previous curves when current curve is Curve point with third axis

In this scenario, when the current curve (valid from 2021-10-3, curve parameter = WHP, third axis parameter = Gas Lift Rate) has only one value for its third axis, previous curve (valid from 2021-10-2, curve parameter = WHP, third axis parameter = Gas Lift Rate) will also be plotted. The previous curve is plotted even though it has more than one third axis. Curves that are valid from 2021-10-01 and 2021-09-30 are not plotted because they have a different third axis parameter (Pump Speed).

Figure 1: Data for current selected curve
Figu
…[truncated]


==========================================================================================
## [19/22] Well Decline Curve
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_well_decline_curve.html
==========================================================================================
Well Decline Curve
1 Introduction

The decline curve functionality in EC enables the calculation of theoretical production based on a declined/Inclined reference estimate. The source of the reference estimate is defined by the theoretical calculation method setting (e.g. performance curve, last accepted well test, etc. ) whereas the decline curve defined in this business function determines how much the reference well performance should be changed. This depends on the decline curve constants in addition to the number of days between the production day and the date of the reference well performance. The decline curve can accommodate multiple last accepted well tests valid within the period of the well decline curve and apply decline factors from the date for the decline curve of the valid accepted well test.

This business function provides the logic necessary for handling well decline curves and the accompanying decline constants. Time-dependant decline curves can be defined individually for 9 different trend parameters, including: -

phases like oil, water, gas, condensate, water, and phase ratios such as GOR, water cut, WOR, CGR and WGR.

Four classical decline trend methods are available including: -

Linear, Exponential, Hyperbolic and Harmonic.

Typical use

A reference estimate has been established for an oil producer and is defined in the system as a performance curve that expresses the oil production as a function of choke position.  Limited well testing capacity makes it difficult to keep this reference estimate updated. However, an extensive well test history shows that the well has been on a steady decline for any months and is expected to continue, on the same trend.

Navigate to the well using the navigator well dropdown.

Insert a new empty record and

Select a Valid from date.

Select a trend parameter from dropdown.

Select trend method from dropdown.

2 Screenshot

3 Settings

Well Decline Curves (PT.0015) has setting in Maintain System Settings (CO.1006) to support either both decline and incline curves or solely decline curve as below:

When setting is set to Y, both incline and decline graph is supported and populated. k is entered as a positive number for incline curve and k is a negative number for decline curve.

When setting is set to N, only decline graph is supported and populated. k is entered as a positive number.

There is no changes to the plotted graph but please ensure that k is entered correctly based on the preferred settings as above to support incline and decline correctly.

4 Trend Methods and Trend Parameters

Different trend methods will render different graph types accordingly.

The formula for each trend type is as below which supports both decline (when k is -ve value) and incline curve (when k is +ve value) when the system setting is set to Y (see previous section.)

Trend Method	Formula


Exponential

	

Qo = Qi * e**kt and b = 0




Linear

	

Qo = Qi * (1 + (k*t))




Harmonic

	

Qo = Qi / (1 - (k*t)) and b =1




Hyperbolic

	

Qo = Qi / (1 – (k*t*b))**(1/b) and 0 < b < 1




User Exit

	

Project defined formula

The formula for each trend type is as below which supports only decline curve (k i
…[truncated]


==========================================================================================
## [20/22] Production Forecasting
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_production_forecast.html
==========================================================================================
Production Forecasting

Forecasting Business Functions and explanations

1 Introduction

Energy Components (EC) includes functionality for forecasting. This document describes important business functions and their usage from defining a forecast & scenario to calculating forecast volume, export volume, revenue, net cash margin and operator’s net cash margin per well for the selected scenario and day as explained in the diagram below.

2 Forecasting Overview

Below are steps in EC to be able to finally obtain net cash margin: -

2.1 Define Forecast and Scenario

Forecast and scenario supports operational and geographical group models and are defined in Forecast and Scenarios (PP.0039). For each forecast, there can be multiple scenarios linked to it. Each forecast can be linked directly to a parent group (Facility Class 1, Area, etc). The forecast is stored in FORECAST_GROUP and FORECAST_GROUP_VERSION table. Meanwhile, the scenario is stored in the FORECAST and FORECAST_VERSION tables.

Any scenario can be promoted to ‘Official’. However, there can only be one official scenario for the same lowest level asset and period. For example, ‘Scenario A’ and ‘Scenario B’ are both linked to the same facility ‘Facility 1’. If ‘Scenario A’ has been made official, promoting ‘Scenario B’ as official will demote ‘Scenario A’ to unofficial.

2.2 Calculate Potential

Potential can either be imported from another system/entered manually or calculated in EC using the decline curve formula. You can decide the potential to be used which is referred to as ‘Chosen Potential’ based on the imported/entered or calculated potential. Two identical business functions are available for this purpose:-

Well Production Curves (PP.0067)

Records are filtered by the selected well.

Forecast Scenario Curves (PP.0068)

Records are filtered by the selected scenario.

When the ‘Potential Used’ is ‘Calculated’, EC will calculate the curve potential based on the segment configuration data section upon saving. The ‘Well Selection’ data section will have a start date and an end date which will be used to generate the daily data for potential and forecast rates. If the end date is null, the end date of the forecast will be used.

The calculated potential can also be viewed in Forecast Production Well Potential (PP.0055). Thus, any changes to the segment configuration will also be reflected for ‘<Phase> Constrained – Chosen’ attributes on this screen.

2.2.1 Segment Configuration

The configuration input is as follows:

Phase: Phase of each segment like Oil, Gas and Water. This can be configured using EC Codes ⇒ ‘FCST_CURVE_PHASE’

Segment: Incremental order number based on each phase. This is automatically assigned when a new segment is added, and re-sequenced when any of the segment is deleted.

Method: Curve potential will be calculated using the decline curve formula as below:

where,

Qi: Rate of production at the start of the curve (day 0) which is required for the 1st segment. For the consecutive segment, Qi is displayed which equals to the previous day of preceding segment for the phase.

B: The exponent which defines the curvature of the line. This is required for Hyperbolic cu
…[truncated]


==========================================================================================
## [21/22] Forecasting Upgrade Guide
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_production_forecasting_upgrade_guide.html
==========================================================================================
Forecasting Upgrade Guide
1 Introduction

Below is the detailed information which regards to Production Forecasting business function changes done in EC-13.0.21, EC-13.1.12, EC-13.2.9 and EC-14.0.0. This document is useful to understand the relevant changes made.

2 Filter From and Filter To navigator
Navigator in older versions:

New navigator:

What was changed:

Forecast screens now have only 'Date' instead of 'From Date' and 'To Date' in the navigator. Date in the navigator will be used to filter the group model, forecast and scenario only.

It also has 'Filter From' and 'Filter To' which are optional. When these filters are NULL, all rows will be retrieved. If the filters have dates, the records will be filtered based on the date range. This new forecast filtering will only be applicable to the navigator that has Scenario and not objects (i.e, Well. Streams).

3 Well Production Curves (PP.0067)/Forecast Scenario Curves (PP.0068)
3.1 Scenario/Well Selection Data Section
Screen design in older versions:

New Screen design:

What was changed:

Label ‘Curve Type’ is updated to ‘Potential Used’. The dropdown option remains as ‘Imported’ and ‘Calculated’.

The button’s label is updated from ‘Calculate Forecast Volume’ to ‘Calculate Forecast’ but the calling function remains the same.

Treeview has been updated.

/com.ec.prod.pp.screens/forecast_well_curves/GROUPMODEL/WELL/CLASS_NAME/FCST_CURVE/CLASS_NAME_1/FCST_CURVE_SEGMENT/CLASS_NAME_2/FCST_VOLUME/CLASS_NAME_3/FCST_POTENTIAL_VOLUME/CLASS_NAME_4/FCST_ACTUAL_VOLUME?screentemplate=/com.ec.prod.pp.screens/forecast_well_curves
3.2 Draw Graph in Curves tab

Segment configuration will remain unchanged. There are a few changes in the draw graph.

Screen design in older versions:
Segment Configuration Data Section

Draw Curve

New Screen design:
Segment Configuration Data Section

New button: Draw Potential

Draw Curve

Newly added button:

‘Draw Potential’ is a newly added button. This button will draw both imported and curve potential graphs. Users could compare these two graphs to select which potential they want to use.

What was changed:

‘Draw Curve’ and ‘Compare Curve’ will show chosen potential which is determined by the selected potential used in the scenario/well selection. If calculated is selected, this will show the calculated curve potential. If imported is selected, this will show the imported potential.

3.3 Potential Volume tab
Screen design in older versions:

New Screen design:

Newly added features:

Imported potential has been introduced for each phase and this is used to store imported numbers from an external system.

Chosen potential will be the potential based on the selected ‘Potential Used’.

What was changed:

Potentials in Well Production Curves (PP.0067), Forecast Scenario Curves (PP.0068) and Forecast Event (PP.0047) will now use constraint values in FCST_WELL_POTENTIAL class instead of the base.

When ‘Imported’ is selected as potential used, the potential will be based on the imported attribute in FCST_WELL_POTENTIAL class. If ‘calculated’ is selected, the potential will be based on the constraint’s value in FCST_WELL_POTENTIAL.

What was removed:

System setting ‘Inc
…[truncated]


==========================================================================================
## [22/22] EC Chemistry
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/prod/prod_ec_chemistry.html
==========================================================================================
EC Chemistry
1 Chemical Management
1.1 Introduction

Chemical management is data management related to chemical status and use. EC Chemistry Lite offers features for basic chemical availability and tracking usage.

1.2 Chemical product management
1.2.1 Introduction

The purpose of chemical products is to track and report usage, spend and performance for individual chemical products. This enables verification if the right chemical product is selected for each application or area, or initiate change out due to non-efficient chemical.

A chemical product may look the same from vendor to vendor, however, similar chemicals may have a slight difference in composition or properties that make them behave differently. Thus, EC is tracking chemicals by preferable their commercial name as given by the vendor.

1.2.2 Maintaining chemical vendors

Chemical vendors are maintained on the Company object. A company is added and managed as normal, however, the difference is that the company is checked as a Chemical vendor. A chemical vendor often offers laboratory services, or manages shot-trucks and in such case, these must be checked as well. For samples being sent to the vendor laboratory the Company must both be a vendor and a laboratory to track the samples.

Emergency phone is the phone number often given on the safety data sheet and when added here it will appear in the Chemical QHS app. as a link to dial directly to the vendor.

For calculation of chemical spend the local currency must be selected.

1.2.3 Maintaining chemical product type

The chemical product type is sometimes referred to as application and may named differently by different operators and vendors. The chemical product types are managed as EC codes and can be changed or added new.

It is recommended to use industry standard grouping of chemicals to avoid misunderstandings.

1.2.4 Adding new chemical product

Chemical products are selected from the list and can be sorted or filtered by chemical type.

The chemical code and chemical product name must be provided. It is highly recommended to use the vendor commercial name for both the product code and product name.

In the case of a vendor commercial name change it is recommended to create a new version and only change the chemical name and not the code, to maintain consistency and ease of history tracking.

As a general practice do not add more than the commercial chemical name to the product name. If it is necessary to describe usage or property, use the description field. All chemical product codes and names should be unique just by using the commercial name.

Chemical product is added with a code and name. The general recommendation is using the vendors code and commercial name. The code should not change (for traceability), but the name can follow the change of commercial names.

Approval status can be selected for use in reports (and chemical inventory log). Estimated days to delivery can be the vendor turnaround days. In reports a “safety margin” can be added as a parameter accounting for shipment and weather.

It is general recommended that unless EC is used as master data for chemical products, they should be linked to a data sou
…[truncated]