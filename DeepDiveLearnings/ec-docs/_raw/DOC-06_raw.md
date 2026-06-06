# Raw content — DOC-06
Modules: ['transport']
Pages: 12



==========================================================================================
## [1/12] Overview
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_overview.html
==========================================================================================
Overview

A transport operation in Energy Components is defined as one oil / gas pipeline or group of pipelines which share processing, terminal and storage facilities and have at least one interconnecting hydrocarbon stream. Basically the transporter’s role is to redeliver hydrocarbons at an exit point according to an agreement (transport agreement). In the case of transporting hydrocarbons in the liquid phase, such a role might also include managing the off-take liftings according to agreement (lifting procedure). Such a redelivery service may include processing and storage of hydrocarbons (processing / storage agreement).

In many cases the transport is clearly distinguished from the producer of the hydrocarbons, where the transporter offers services according to a fee (often referred to as "tariff") for one or more producers of hydrocarbons. In other cases the transport operation forms an integral part of the production operation by, e.g. performing the cargo lifting and inventory management of crude or other products shipped on tankers (or trains / trucks).

Quorum Software provides complete hydrocarbon accounting solutions for any type of transport operation, including commercial gas pipelines, oil pipelines, LNG/NGL plants and off-take terminals.

EC Transport is divided into several business areas (BA), which are as follows:

Business Area	Description


CA (Cargo Administration)

	

Supporting the Cargo Administration process (also known as tanker scheduling, shipment planning, etc)




CP (Cargo Planning)

	

Sub area within CA, supporting the planning of the cargo lifting activities




TO (Terminal Operation)

	

Sub area within CA, supporting the terminal activities, irregularities and production of cargo documents




LA (Lifting Account)

	

Sub area within CA, supporting lifting account transactions




OD (Oil Delivery)

	

Supporting the Oil Delivery process




GD (Gas Dispatching)

	

Supporting the Gas Dispatching process




GD (Gas Delivery)

	

Supporting the Gas Delivery process




FC (Forecast)

	

Supporting the matching of field forecast volumes with plant production capacities


==========================================================================================
## [2/12] Dashboard
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_dashboard.html
==========================================================================================
Dashboard

This document describes the EC Transport Dashboard widgets that comes with the standard EC product. EC Transport Dashboard consists of two line widgets and two table widgets. They are predefined, however, it is possible for projects to create or modify the dashboard query in order to support their business needs. The query is stored in the QUERY parameter in CTRL_DASHBOARD_PARAM table. To setup these widgets from the dashboard, there is a menu consists of different input parameters on the top right hand corner of the widget.

Transport widgets which are shipped from EC-12.1 and onwards are:

Schedule Lifting Chart

Lifting Account Entitlement Chart

Logbook

Operational Restrictions

Transport Forecast List

Forecast - Schedule Lifting Chart

Schedule Lifting Chart

This dashboard line widget displays the Storage level for a period.

The parameters which can be setup for Schedule Lifting Chart is shown in the screenshot below:

The Schedule Lifting Chart widget can be filtered by From Date, To Date, Storage, Production Plan.

The function of each chart parameters is defined below:

Show X Axis: Shows the x axis value and its label (Daytime).

Show Y Axis: Shows the y axis value (Storage Level).

Minimum Level Y Axis: If this checkbox is selected, it will show the Y Axis of the Minimum Level Storage Level

Maximum Level Y Axis: If this checkbox is selected, it will show the Y Axis of the Maximum Level Storage Level

Minimum Safe Level Y Axis: If this checkbox is selected, it will show the Y Axis of the Minimum Safe Level Storage Level

Maximum Safe Level Y Axis: If this checkbox is selected, it will show the Y Axis of the Maximum Safe Level Storage Level

Show Markers: Each series will be marked with a circle

Legend position: The position of the legend in the chart

Y axis Min: The minimum value of the Y axis to be displayed on the chart

Y axis Max: The maximum value of the Y axis to be displayed on the chart

Animate: Will show animation of the line being drawn

Show Point Labels: Each series will be labeled with the storage level value

Lifting Account Entitlement Chart

This dashboard line widget displays the entitlement per lifting account.

The parameters which can be setup for Lifting Account Entitlement Chart is shown in the screenshot below:

The Lifting Account Entitlement Chart widget can be filtered by From Date, To Date and Lifting Account.

The function of each chart parameters is defined below:

Animate – Will show animation of the line being drawn

Show X Axis – shows the x axis and its label (Daytime).

Show Y Axis -  Shows the y axis value (Closing Balance).

Show Markers – Each series will be marked with a circle

Show point labels – Each series will be labeled with the closing balance

Y axis Min – The minimum value of the Y axis to be displayed on the chart

Y axis Max – The maximum value of the Y axis to be displayed on the chart

Legend position – The position of the legend in the chart

Logbook

This dashboard t
…[truncated]


==========================================================================================
## [3/12] System Properties
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_system_properties.html
==========================================================================================
System Properties

The following properties are maintained in the ctrl_property_meta table

System properties

Below table contains system properties

Label	Screen	Description	Default value


Allowed file extensions for Cargo Documents Upload

	

Cargo Documents

	

Comma separated list of allowed file extensions for uploading document in Cargo Document screen

	

.xml,.txt,.csv,.xls,.xlsx,.pdf,.docx




Allowed file extensions for Other Cargo Documents Upload

	

Cargo Document Other

	

Comma separated list of allowed file extensions for uploading document in Cargo Document Other screen

	

.xml,.txt,.csv,.xls,.xlsx,.pdf,.docx




Allowed file extensions for documents upload in Cargo Documents Parcel

	

Cargo Document Parcel

	

Comma separated list of allowed file extensions for uploading document in Cargo Document Parcel screen

	

.xml,.txt,.csv,.xls,.xlsx,.pdf,.docx




Allow re-running of approved calculation

	

Transport and Sales Calculation screens

	

Set to Y to allow re-running of approved calculation

	

N




Allow sub lifting account

	

Nomination Entry

Cargo Information

	

Flag to determine whether it should be possible to nominate cargo on sub lifting accounts (lifting accounts that are part of lifting agreement)

	

N




Allow cargo transport status change in EC Transport

	

Cargo Information

	

Set to Y to allow cargo transport status change in EC Transport

	

Y




BL/MR Light Account Split Tab

	

BL/MR Light

	

Show or hide Nomination Split tab

	

true (show)




BL/MR Light Actual Lifted Qty Tab

	

BL/MR Light

	

Show or hide Parcel Load tab

	

true (show)




BL/MR Light Nomination Details Tab

	

BL/MR Light

	

Show or hide Nomination Details tab

	

true (show)




Capacity Release Details Contact Tab

	

Capacity Release Details

	

Show or hide Contact tab

	

true (show)




Capacity Release Details Misc Tab

	

Capacity Release Details

	

Show or hide Misc tab

	

true (show)




Capacity Release Details Other Tab

	

Capacity Release Details

	

Show or hide Other Terms tab

	

true (show)




Capacity Release Details Rate Tab

	

Capacity Release Details

	

Show or hide Rate tab

	

true (show)




Capacity Release Details Recall/Reput Tab

	

Capacity Release Details

	

Show or hide Recall/Reput tab

	

true (show)




Capacity Validation auto expand levels

	

Capacity Validation

	

How many levels to auto expand in Capacity Validation in EC Transport - Gas Dispatching

	

2




Cargo Doc - List All

	

Cargo Document

	

List all current cargo documents regardless of selected parcel

	

N




Cargo Doc - Show Tab #2

	

Cargo Document

	

Show or hide the "Other Document" tab

	

null




Cargo Doc Generate - All Parcels

	

Cargo Document

	

Generate all documents for current cargo in one click

	

N




Cargo Doc Generate - Confirmation Message

	

Cargo Document

	

Display a confirmation message before cargo document generation

	

null




Cargo Doc Generate - Receipt List

	

Cargo Doc
…[truncated]


==========================================================================================
## [4/12] Cargo Status Rules
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_cargo_status_rules.html
==========================================================================================
Cargo Status Rules

In addition to the general record status concept, the Cargo Administration part of EC Transport includes a dedicated cargo status. This section explains, in some detail, the cargo status concept.

Cargo Status Values and Workflow

Cargo status can be customised as required by the customers. All customer cargo statuses must be mapped against system cargo statuses.

This can be done in Cargo Status Mapping (CO.2006). For more information about the mapping see the Business Function document.

The next sections describe the different system statuses that a Cargo can have. This is also the general workflow. Not following these steps will have an impact on how the system behaves.

The available system cargo statuses are described below. The natural workflow is top-down (Not cancelled).

T – Tentative (part of future plan, cargoes are not available in terminal operation screens)

R – Ready for Harbour (cargoes are available in terminal operations)

C – Closed (lifting completed)

A – Approve (warranty expired)

D – Cancelled (lifting will not take place)

The only requirement for customer cargo statuses is that the Cancelled status must have the code D.

There are four screens where the user can change system cargo status.

Nomination Entry (CP.0001) – The cargo is created in this business function with status set to 'Tentative'

Cargo Information (CP.0003)

Nomination Details (CP.0004)

Lifting Instruction (CP.0005) – Typically used to set to 'Ready for Harbour'

BL/MR Info (TO.0005) – Typically used to set to 'Closed'

When a system cargo status is set to Closed the record status is set to V (Verified) for these tables in the database. This will prevent the user from doing updates after cargo is closed.

CARGO_TRANSPORT

STORAGE_LIFT_NOMINATION

STORAGE_LIFTING

When a system cargo status is set to Approved the record status is set to A (Approved) for these tables in the database. This will prevent the user from doing updates after cargo is approved.

CARGO_TRANSPORT

STORAGE_LIFT_NOMINATION

STORAGE_LIFTING

CARGO_ACTIVITY

CARGO_ANALYSIS, CARGO_ANALYSIS_ITEM

CARGO_LIFTING_DELAY

CARRIER_INSPECTION

Rules for System cargo status

The matrix below describes what a system cargo status can change to

From/ To	Tentative	Ready for Harbour	Closed	Approved	Cancelled


Tentative

		

Y

	

N

	

N

	

Y




Ready for Harbour

	

Y*

		

Y*

	

N

	

Y




Closed

	

N

	

Y

		

Y

	

N




Approved

	

N

	

N

	

Y

		

N




Cancelled

	

N

	

N

	

N

	

N

	

See the 'Validation' section for special rules.

The property "Allow cargo transport status change in EC Transport" in Maintain System Settings can be set to N to prevent cargo transport status change from Approved to Closed if required.

The default value for the property is Y.

Validation

Below is a list of additional validation rules used when system cargo status changes.

From Status	To Status	Validation


Ready For Harbour

	

Tentative

	

Not allowed if there are stora
…[truncated]


==========================================================================================
## [5/12] EC Revenue Interface
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_ec_revenue_interface.html
==========================================================================================
EC Revenue Interface
Overview

The modules of EC Transport have a close integration with other EC modules, and wherever applicable do rely on the same data sources. However, when information is used in different domains, information is normally replicated from the source domain to the target domain. Such replication is performed by Interface Functions. A set of default Interface Functions are supplied with the EC product. An example of such replication is when cargo related information is to be used for invoicing purposes. Then the cargo information (source domain) is replicated to EC Revenue (target domain) to ensure the information lives its own life as it enters the commercial domain.

When configuring an integrated EC implementation, the available Integration Functions must be verified to ensure that the default information mapping corresponds with the identified business requirements. The Interface Functions must be adjusted if deviations exists.

The below diagram outlines the default Interface Functions supplied with the EC Transport product:

Cargo Liftings (Parcels)

Cargo Liftings (per Parcel) are replicated to EC Revenue when it is actually lifted on the carrier, i.e. the Bill of Lading value. For CIF (Cost Insurance Freight) cargoes also expected unload and unload values are replicated.

In Product Measurement Setup (CO.2002) the quantities to replicate can be configured. There can be only four different UOMs, but each can have both net and gross. It is recommended that the mapping is the same for Load and Unload lifting events.

In EC Revenue there are three quantity types:

LOAD

EXP_UNLOAD

UNLOAD

Load represent the quantities set in BLMR Info (TO.0005) business function. Expected Unload is calculated based on the load value. The unload value is set in Unload Info (TO.0010). Expected Unload and Unload is only replicated for cargoes where incoterm is CIF.

Preconditions

Nominations must be connected to a Contract and the contract must have 'Available in Revenue' checked. If not it will not be replicated to EC Revenue. No error message.

Nominations must have an Incoterm. Error message from EC Revenue

At least one measurement item must exist on the product associated to the storage.

In 'Product Measurement Setup' there must exist a mapping on at least one measurement item and it must be 'Qty 1'. Measurement Item will indicate if this is a 'Net' or 'Gross' value. 'Net' is default.

Some of the values replicated to EC Revenue can be updated in other business functions, e.g. Carrier in Cargo Info, Consignor in Nomination Detail. This is ok as long as the nomination is not used in EC Revenue. As soon as a contract is processed and the cargo details are picked up, updates on a cargo/nomination are not allowed.

Cargo Quantities

Cargo Quantities are quantities that are replicated to EC Revenue on a monthly basis.

Typically these quantities are replicated a few days after the month end. The month should be finalised and closed. Some o
…[truncated]


==========================================================================================
## [6/12] The EC Contract Concept
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_the_ec_contract_concept.html
==========================================================================================
The EC Contract Concept

The EC Contract Concept is designed to model different contract types, spanning from straightforward to very complex variants. As shown in the figure below, modelling a contract in EC involves:

A further description is provided below.

Contract

The definition of the core contract values, including contract period, contract year/day offsets, etc.

Contract Parties

Attaching the contract Vendor and Customer to the contract. The contract parties may be a constellation of multiple companies, associated with the contract through an equity split.

Contract Template

A contract template is a set of contract attributes relevant for a type of contracts. As an example, a gas sales agreement would typically need a defined set of contract attributes. It would then be appropriate to define a contract template called GSA, containing those attributes.

Contract Attributes

All contracts must be associated with a Contract Template, defining all additional attributes relevant for this contract. In the example of a gas sales agreement, the contract could be associated with the GSA contract template, meaning the already defined contract attributes are available.

Contract Accounts

A contract may be set up with associated Contract Accounts. Contract accounts are typically used for contracts where sales allocations (also know as contract calculations or sales calculations) are performed. The accounts for a contract would typically represent those contract obligations relating to a transactional quantity. The transactional quantities can be stored as volume, mass and energy units. Examples of contract accounts are: Monthly Sales Gas Qty, Monthly Off Spec Qty, Monthly Take Or Pay Qty.

When configuring Contracts and Contract Attributes it is possible to define if these should be accessible throughout all EC modules, or if access limitation should apply to one or several modules (EC Transport, EC Sales, etc). All contract attributes are effective dated, meaning it is possible to define contract attributes changing value during the contract life time.


==========================================================================================
## [7/12] Screen Configurability
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_screen_configurability.html
==========================================================================================
Screen Configurability
EC Transport Gas Dispatching
Screen Parameters

To increase the flexibility in some of the dispatching navigators the following features has been added to the url, thus making it easy for projects to re-use the same screen definitions for capturing alternative / additional data:

Parameter	Description


NAV_MODEL

	

Optional, will always have a default. 
Will in most screens default to the most common alternative (CONTRACT / NOMINATION_POINT…) 
Using this option will result in user not being able to change the model for this specific bf in preferences.




FORCE_NAV_CLASS

	

Optional. 
Indicate the navigation level of mandatory field(s) to populate.




CLASS

	

Optional. Owner of this class must be defined as target as per screen definition.




BF_PROFILE

	

See CO.1025 – Business Function Profiles (located in https://eccommunity.portal.tieto.com/archive_folders[EC User Community Downloads section], then navigate to folder "EC Documentation". BF Documentation zip file is in the related release folder)




TARGET

	

Constant. Set in screen definition.

Example from the Daily Input Nomination BF (pattern: <parameter name>/<value>) :

Default / Simple version:
../com.ec.tran.gd.screens/daily_input_nomination/CLASS/TRNP_DAY_NOM_INPUT/NOMINATION_CYCLE/false?screentemplate=/com.ec.tran.gd.screens/daily_input_nomination

With all arguments set / Advanced version:
../com.ec.tran.gd.screens/daily_input_nomination/CLASS/TRNP_DAY_NOM_INPUT/NOMINATION_CYCLE/false/NAV_MODEL/TRAN_OPERATIONAL/BF_PROFILE/GD.0020/FORCE_NAV_CLASS/NOMINATION_POINT?screentemplate=/com.ec.tran.gd.screens/daily_input_nomination

EC Transport Cargo Administration
Additional Units

This area of the product supports multiple units, by setting up an additional nomination unit in Product Measurement Setup and enabling the additional attributes on the relevant screens/classes one can setup e.g. both BBLS and m3 or GJ and kWh etc.

Context Menu

Cargo Administration supports simple setup of context menus by using the predefined / implemented BusinessAction: com.ec.tran.cp.screens.model.ejb. GenericCargoAction.java in conjunction with the database package: ue_cargo_action.execute()

Using this, the projects can setup database code to be executed merely by populating the database tables: BF_COMPONENT, CNTX_MENU_ITEM and CNTX_MENU_ITEM_PARAM 
Example:

insert into BF_COMPONENT (BF_CODE, COMP_CODE, NAME, URL)
values ('CP.0001', 'nominations', 'nominations', '/nominations');
insert into CNTX_MENU_ITEM (BF_CODE, COMP_CODE, ITEM_CODE, NAME, ACTION_CLASS_NAME, ACTION_ROW_SCOPE, THRESHOLD_LEVEL, CONFIRM_MESSAGE, REMARK_IND, AUTO_SAVE_IND, MIN_SELECTED_ROW, MAX_SELECTED_ROW, FUNC_MESSAGE, FUNC_VALIDATION, DIVIDER_IND, SORT_ORDER, DESCRIPTION)
values ('CP.0001', 'nominations', 'MOVE_P1', 'Move +1 day', 'com.ec.tran.cp.screens.model.ejb.GenericCargoAction', 'selectedRows', 10, null, 'N', 'N', null, null, null, null, 'N', 10, null);
insert into CNTX_MENU_ITEM_PARAM(BF_CODE,C
…[truncated]


==========================================================================================
## [8/12] How to Configure Form Layout in Demurrage Screen
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_how_to_configure_form_layout_in_demurrage_screen.html
==========================================================================================
How to Configure Form Layout in Demurrage Screen

The form layout in Demurrage (TO.0007) and Demurrage Unload (TO.0015) was hardcoded prior to EC-12.2. It was not possible to change the form layout of Demurrage and Demurrage Unload screen from the class configuration.

In EC-12.2, we have introduced a new transformer called FormLabelLayoutTransformer, where the form layout will be rendered according to the value of the following class attribute properties if they exist in the Demurrage/Demurrage Unload class.

viewgroup - grouping of attributes in the same group

viewcol - the column the attribute should be positioned

viewrow - the row the attribute should be positioned

For example, the attributes Commenced Laytime Activity and Carrier Laytime Allowance are configured as follow in the Class Attribute Configuration:

Attribute: Commenced Laytime Activity

Attribute: Carrier Laytime Allowance

In the Demurrage screen, this is how Commenced Laytime Activity and Carrier Laytime Allowance is positioned:

In the above example, the attribute viewcol values are set to 1 and 2. The FormLabelLayoutTransformer makes room for the labels and positions them to the left of the fields. The resulting form has 4 columns. I.e. It is not necessary to explicitly position the attributes in column 2 and 4. Hidden attributes with viewgroup, viewcol, viewrow properties in will not be rendered on the screen.

It is also possible that each demurrage type can have its own form layout. The class attribute properties viewgroup, viewcol, viewrow can be overridden by setting the Property Type to "DYNAMIC_PRESENTATION".

For example, this is the default layout for Demurrage and Ebo in EC:

We can configure the form layout for Ebo as follow, where Status Date and Comments will be positioned on a different row/column.

Class Attribute Configuration:

The FormLabelLayoutTransformer picks up the viewrow/viewcol values from the selected record. Using dynamic viewrow/viewcol properties that return different values depending on demurrage type, will effectively change the layout of the form based on demurrage type. Note that the toolbar insert button is disabled in demurrage screens. It has been replaced by Create buttons that create an empty demurrage record in the DB. The reason for this is that the dynamic viewrow/viewcol properties are evaluated for persisted records only.


==========================================================================================
## [9/12] GanttChartTooltipTransformer, GanttChartConflictDetector and DataModelFilterTransformer in Gantt Charts
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_ganttcharttooltiptransformer_ganttchartconflictdetector_and_datamodelfiltertransformer_in_gantt_charts.html
==========================================================================================
GanttChartTooltipTransformer, GanttChartConflictDetector and DataModelFilterTransformer in Gantt Charts
Introduction

There were several performance issues identified especially when accessing and loading the Gantt Charts in EC Transport. One of the reasons is the logic behind the Gantt charts is depending too much on the database layer.

The approach we have taken to improve the performance of the Gantt charts is by introducing 3 types of Transformers that are designed to move the database logic to the application layer for the Berth Utilization Chart and Carrier Utilization chart, which can be found in Forecast Manager (CP.0068) and Schedule Lifting Overview (CP.0072). This has improved the performance of these Gantt charts to a great extent.

DataModelFilterTransformer

This DataModelFilterTransformer is created to filter the datamodel according to the arguments provided in the screen XHTML. The filtering is based on the values provided in the navigator for EC screens that implement DataModelFilterTransformer.

The transformer arguments express the condition that a datamodel row must satisfy in order to be returned by the transformer.

In the example code snippet below, the "name" argument identifies the cell. The "operator" argument identifies the comparison operator to use, and "value" argument is the value to compare against.

The DataModelFilterTransformer supports these three (3) functionalities:

the operator "equal"

"eq" operator

<arg name="transform" value="com.ec.xms.screens.model.web.DataModelFilterTransformer" datatype="string">
       <arg name="name" value="STORAGE_ID" datatype="string" valuetype="constant"/>
       <arg name="operator" value="eq" datatype="string" valuetype="constant"/>
       <arg name="value" value="RetrieveArgs.nav_lift.STORAGE_ID" datatype="string" valuetype="requestParam"/>
</arg>

the operator "between"

"between" operator

 <arg name="transform" value="com.ec.xms.screens.model.web.DataModelFilterTransformer" datatype="string">
       <arg name="name" value="QTY" datatype="string" valuetype="constant"/>
       <arg name="operator" value="between" datatype="string" valuetype="constant"/>
       <arg name="value1" value="RetrieveArgs.nav_lift.MIN" datatype="string" valuetype="requestParam"/>
       <arg name="value2" value="RetrieveArgs.nav_lift.MAX" datatype="string" valuetype="requestParam"/>
</arg>

the operator "in"

"in" operator

<arg name="transform" value="com.ec.xms.screens.model.web.DataModelFilterTransformer" datatype="string">
       <arg name="name" value="STORAGE_TYPE" datatype="string" valuetype="constant"/>
       <arg name="operator" value="in" datatype="string" valuetype="constant"/>
       <arg name="value1" value="" datatype="string" valuetype="constant"/>
       <arg name="value2" value="RetrieveArgs.nav_lift_type_2" datatype="string" valuetype="requestParam"/>
       <arg name="value3" value="type_3" datatype="string" valuetype="constant"/>
</arg>

The between operator can take two val
…[truncated]


==========================================================================================
## [10/12] End Dating of Contracts
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_end_dating_of_contracts.html
==========================================================================================
End Dating of Contracts
Introduction to Contract - End Date (CO.2086)

Shortening the lifetime of a contract is a business operation that is difficult to do in EC. When the end date of a contract is changed in Contract (CO.2016), EC checks whether there are data dependencies outside the new validity period. If such dependencies are found, an exception is raised and the change is rolled back:

In EC 13.0.0, we have created a new business function Contract - End Date (CO.2086), that can be used to find and resolve data dependencies that are outside the new validity period. The new contract end date can be set after the dependencies have been resolved. The new screen lists all dependent records, and indicates the operations that are needed to "resolve" them.

How to use Contract - End Date

End-users will select a contract from the dropdown and once a contract is selected, End Date column will be populated for the selected contract. User will then populate New End Date column for the selected contract.

Once "FIND DEPENDENCIES" button is clicked, the second data section "Dependency Sets" will list all the contracts which are required to be resolved together with the total number of records to be resolved and the status of the dependency set.

Upon selecting a contract from the "Dependency Sets" section, the third data section "Dependency Summary" will be displayed. "Dependency Summary" section will list all the corresponding dependency set records in detail. There are three columns under this section: Table Summary, Class Summary and Class Data.

Table Summary	Class Summary	Class Data


Lists all tables that have dependency on setting the new contract end date.

Table Name

Operation Type

Record Count

	

Lists all classes based on the selected table in Table Summary section.

Class Name

Class Label

Class Type

Record Count

	

Lists all data in viewable columns based on the selected class in Class Summary section.

User shall review all dependent records from this Dependency Summary section list.

Upon clicking "RESOLVE DEPENDENCY SET" button, this will resolve the dependencies according to the operation type for the selected contract. After all the dependencies for the selected contract have been resolved, it will be possible for user to update the contract End Date to the new end date in Contract screen.

User may opt to rollback the dependency set using "ROLLBACK DEPENDENCY SET" button. The corresponding dependency set records of the selected contract will be rollback.

Generated Package and User Exit

Behind this contract end dating process, there is a database package that is introduce to generate eced_<CLASS_NAME> package.

Package	Procedure	Input parameter	Example


ecdp_object_dependency

	

generateDependencyPackage

	

object class name e.g. CONTRACT

	

ecdp_object_dependency.generateDependencyPackage('CONTRACT')

This procedure do not contain any business logic. It is taking care of the logic that finds and resolving object dependenc
…[truncated]


==========================================================================================
## [11/12] Berth Slot Calendar
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_berth_slot_calendar.html
==========================================================================================
Berth Slot Calendar

The Berth Slot Calendar screen reads nominations and period berth restriction data from the STORAGE_LIFT_NOM_INFO and BERTH_PERIOD_RESTRICTION classes. The screen transforms the data into a format that can be displayed in a calendar screenlet. This transformation is responsible for:

determining the color of each date cell

building the tooltip text that is displayed when the mouse pointer hovers over a date cell

From EC-13.0.11 onwards, the Berth Slot Calendar transformation is configured from Maintain System Settings.

System Property

The following properties in Maintain System Settings are required to configure the Berth Slot Calendar. They are pre-configured for Berth Slot Calendar (CP.0078), Forecast - Berth Slot Calendar (CP.0079) and Berth Slot Calendar tab in Forecast Manager (CP.0068).

System Property Label	Default Property Value	Description


Berth Slot Calendar - Tooltip label column property

	

TOOLTIP_LABEL

	

Tooltip label column property. Attribute should be available in class.

The tooltip label shows the information of the cargo name or the restriction type.




Berth Slot Calendar - Daytime column property

	

DAYTIME

	

Daytime column property. Attribute should be available in class.

The nomination date for a cargo nomination. As for the berth restriction, this is the start date of the restriction event.




Berth Slot Calendar - Berth Id column property

	

BERTH_ID

	

Berth Id column property. Attribute should be available in class




Berth Slot Calendar - Berth Name column property

	

BERTH_POPUP

	

Berth Name column property. Attribute should be available in class




Berth Slot Calendar - Duration column property

	

DURATION_DAYS

	

Duration (in days) column property.

Number of days taken to complete an event, especially for berth restriction.

For cargo nominations, if the duration is not defined from class view, it will have a default duration of 1 day.




Berth Slot Calendar - Berth occupancy detail code column property

	

DETAIL_CODE

	

Detail code column property.

This detail code will determine the code for each of the berth occupancy date.

List of detail code are defined in the EC Code, CARGO_CALENDAR_DETAIL.




Berth Slot Calendar - Berth occupancy color code column property

	

COLOR_CODE

	

Event color code column property




Berth Slot Calendar - Text color code column property

	

TEXTCOLOR_CODE

	

Text color code column property




Berth Slot Calendar - Tooltip column property

	

TOOLTIP

	

Tooltip column property




Berth Slot Calendar - Cargo No column property

	

CARGO_NO

	

Cargo No column property. Attribute should be available in class.

EC Codes

There are two types of EC Codes in Berth Slot Calendar:

EC Codes Type	Description	Sample screenshot


CARGO_CALENDAR_DETAIL

	

Code text is used as the detail code for each of the berth occupancy date.

Alt code is used as the configuration of the Date box color. This color code will be the box color for speci
…[truncated]


==========================================================================================
## [12/12] New Cargo Planning And Terminal Operations Data Model
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/transport/ec_transport_new_cargo_planning_and_terminal_operations_data_model.html
==========================================================================================
New Cargo Planning And Terminal Operations Data Model

EC-13.2.0 introduces the core elements of a new cargo planning and terminal operations data model. Multiple lifting and delivery nominations can be grouped together in a single cargo, and commercial nominations are decoupled from physical execution. The new model can support a wide variety of commercial arrangements and provide planners with a more granular view of loading, transport and unloading operations. Based on this model, future versions of EC can develop richer and more powerful features to support the decision-making processes.

One of the most important features of the new model is that it introduces a clean separation between the commercial nominations and the physical execution of activities related to the transfer and movement of product.

A second important feature is the introduction of an explicit “nomination type”. Prior to EC-13.2.0, all export storage nominations were implicitly treated as liftings. For import storages, nominations were implicitly treated as deliveries. In the new commercial model, all nominations have an explicit “nomination type” which indicates whether product is lifted out of the storage or delivered into the storage. Both “nomination types” (lifting and delivery) can be used independently of storage type (import or export).

Thirdly, the new model has better support for capturing complex cargos and commercial arrangements. A single cargo can be comprised of any number of lifting nominations and any number of delivery nominations, each with an optional storage association.

EC-13.2.0 introduces the core elements of the new model. Functional features that utilize the flexibility of the new model will be delivered in future versions. The main goal in EC-13.2.0 is to put the new model in place and thereby lay the groundwork for future versions. The EC-13.2.0 upgrade scripts will migrate data from the old to the new data structures, but they also install DB level logic to ensure that the old model is still supported. The old model should be considered as deprecated, though, and will be removed in future versions.

Commercial vs physical model

Prior to EC-13.2.0, only the commercial side of cargo nominations were captured in EC. The need to capture details related to the physical transfer and movements typically resulted in creative use of the model – beyond the intention for which it was designed. With the addition of designated tables for this purpose, the new model introduces a clear separation between the commercial aspects of cargo nominations and the physical activities involved in the transfer and movement of product/fluids.

The below figure gives a simplified view of the commercial and physical cargo planning data tables and the relationships between them.

The following describes the tables of the physical model:

VOY_CARGO_ACT:Captures activities related to the physical loading or unloading of product.

activity_no	Primary key that is allocated 
…[truncated]