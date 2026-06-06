# Raw content — DOC-05
Modules: ['revn', 'sale']
Pages: 18



==========================================================================================
## [1/18] Overview
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/sale/ec_sales_overview.html
==========================================================================================
Overview

EC Sales is divided into several business areas (BA), which are as follows:

Business Area	Description


GS (Gas Sales)

	

Supporting the Gas Sales processes




SD (Sales Dispatching)

	

Sub area within GS, supporting capacity booking, nominations, nomination rules, delivery events and follow-up of actual deliveries




PR (Price Determination)

	

Sub area within GS, supporting the calculation of unit prices based rules typically defined by a contract. Such rules will normally relate to price indices as a basis for the price determination




SA (Sales Allocation)

	

Sub area within GS, supporting the calculation of hydrocarbon sales quantities according to rules and conditions stated in the commercial sales contracts




TR (Trading)

	

Sub area within GS, supporting portfolio management, risk management, deal capturing / validation and price simulation




GP (Gas Purchase)

	

Supporting the gas purchasing processes




OS (Oil Sales)

	

Supporting oil sales processes


==========================================================================================
## [2/18] Sales Allocation (SA)
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/sale/sa/ec_sales_sales_allocation(sa).html
==========================================================================================
Sales Allocation (SA)
Introduction

Sales Allocation is the EC concept for following up contractual commitments relating to transactional quantities.

As shown in the figure, the sales allocation (sales calculation) concept relies on the EC Contract Concept. For a contract, it is possible to associate Sales Calculation Rule Sets. The calculation rules will relate to Contract Accounts associated to the given contract, and the results of the calculations will be stored as Contract Account Quantities.

As an example, a gas sales agreement defines that a monthly off-spec gas quantity shall be recorded, according to described rules. To configure this in EC, a contract account: Monthly Off Spec Qty would typically be defined. Further, the rules described by the contract will be configured as equations. The defined equations may also relate to contract attributes for the relevant contract. To execute the actual Sales Allocation for the Monthly Off Spec Qty account, the calculation will be run, using available Input Quantities (e.g. delivery quantities combined with Off Spec Events), and the result will be stored for the appropriate period in the Contract Account Quantities "table".

A complex contract will typically have a number of contract accounts, typically also operating on different time spans, e.g. daily, monthly and yearly level.


==========================================================================================
## [3/18] Price Determination (PR)
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/sale/pr/ec_sales_price_determination(pr).html
==========================================================================================
Price Determination (PR)
Introduction

The EC Price Determination capabilities support the determination of product unit prices, typically based on price indices and contractual price definition rules.

There are two types of prices. Prices that relate to a specific contract only, and more generic prices that are valid for a given product but multiple contracts.

As show in the figure, the price calculations relates to Price Objects as well as the EC Contract Concept. The price calculation rules defined by the Price Object will be associated to Price Calculation Rule Sets. Further, the price calculations rely on price indices, typically available on daily, monthly and yearly level. The price calculations may also relate to contract parameters or contract account quantities. The results of the calculations will be stored as Contract Price List or Product Price List values.

Price Concept definition example

In the next paragraphs the process defining a price concept is described step by step. Two price concepts are constructed to illustrate the process from defining the price concept until the price is ready for use for a given product or contract. The price concepts that will be used as examples are:

ABC price concept (is used for illustration in each step and included in example data)

CIF price concept (is included in example data)

Step 1- define the price concept

The price concept can be any concept that the customer wants to define. The price concept will have to be defined with a name and a code. Note that the price concept is not time driven, meaning that there are no date information related to a price concept. Example data:

Price concept code	Name


ABC

	

ABC Price Concept




CIF

	

CIF Price Concept

Step 2 – define price elements

The next step is to define all the elements that the price concept consists of. In the constructed example 'ABC price concept'' each price element in the price concept has to be defined and they are A, B and C. First of all, we have to relate each price element to a price concept which is the 'ABC price concept''. Furthermore, we have to define a price element code and a price element name. Example data:

Price concept code	Price element code	Name


ABC

	

A

	

A element




ABC

	

B

	

B element




ABC

	

C

	

C element




CIF

	

Cost

	

Cost element




CIF

	

Insurance

	

Insurance element




CIF

	

Freight

	

Freight element

Step 3 – define the price object

The price object is defined based on a price concept and the price object has to point to either a product or the combination product/contract. When creating the price object, the following information can be defined:

Price object code and name

Start and end date

Product name

Price concept

Contract name

Currency

UOM

Time span

Calculation rule

Calculation sequence number

Description

Example data:

Price object code	Name	Start date	End date	Product	Price concept code	Contract	Currency	UOM	Time span	Calc rule	Calc seq	Desc


EX_1

	

EX_1

	

01.01.2005

		

Prod_1

	

ABC

	

Contr_1

	

EUR

	

SM3

	

MTH

	

RULE_1

	

1

	

Ex_1




EX_2

	

EX_2

	

01.01.2005

		

Prod_2

	

CIF

	

Contr_2

	

EUR

	

SM3

	
…[truncated]


==========================================================================================
## [4/18] System Properties
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/sale/ec_sales_system_properties.html
==========================================================================================
System Properties

The following properties are maintained in the ctrl_property_meta table.

 System properties
Label	Screen	Description	Default Value


Instantiate Comment at Period Sales Nomination

	

Period Sales Nomination

	

Flag for whether or not to instantiate a new empty comment to Period Sales Nomination

	

Y




Instantiate Daily Contract Delivery

	

Daily Delivery

	

Flag for whether or not to instantiate Daily Contract Delivery records

	

Y




Instantiate Daily Contract Status

	

Daily Contract Account Status

	

Flag for whether or not to instantiate records used to list values in Daily Contract Account Status

	

Y




Instantiate Daily Price Index

	

Daily Price Index

	

Flag for whether or not to instantiate Daily Price Index records

	

Y




Instantiate Daily Price Rate

	

Daily Price Rate

	

Flag for whether or not to instantiate Daily Price Rate records

	

Y




Instantiate Monthly Contract Delivery

	

Monthly Delivery

	

Flag for whether or not to instantiate Monthly Contract Delivery records

	

Y




Instantiate Monthly Contract Status

	

Monthly Contract Account Status

	

Flag for whether or not to instantiate records used to list values in Monthly Contract Account Status

	

Y




Instantiate Monthly Expenditure

	

Monthly Expenditure

	

Flag for whether or not to instantiate Monthly Expenditure records

	

Y




Instantiate Monthly Expenditure Forecast

	

Monthly Expenditure Forecast

	

Flag for whether or not to instantiate Monthly Expenditure Forecast records

	

Y




Instantiate Monthly Price Index

	

Monthly Price Index

	

Flag for whether or not to instantiate Monthly Price Index records

	

Y




Instantiate Monthly Price Rate

	

Monthly Price Rate

	

Flag for whether or not to instantiate Monthly Price Rate records

	

Y




Instantiate Sub Daily Contract Status

	

Sub Daily Contract Account Status

	

Flag for whether or not to instantiate records used to list values in Sub Daily Contract Account Status

	

Y




Instantiate Wet Gas Hourly Profile

	

Wet Gas Hourly Profile

	

Flag for whether or not to instantiate Wet Gas Hourly Profile records

	

Y




Instantiate Yearly Contract Status

	

Yearly Contract Account Status

	

Flag for whether or not to instantiate records used to list values in Yearly Contract Account Status

	

Y




Price Determination - Disable/Enable validation on negative price value

	

Cargo Price List – Dataset, Cargo Price List, Cargo/Parcel Price List, Contract Price List - Dataset

	

Disable/Enable validation on negative price value for price list screens

	

false




Allow re-running of approved Sales calculation

	

Daily/Monthly Contract Calculation, Price Calculation

	

Set to Y to allow re-running of the approved calculation but will block dependent calculation job defined in Calculation Group Setup (CO.0246) which is ticked.

	

N


==========================================================================================
## [5/18] System Attributes
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/sale/ec_sales_system_attributes.html
==========================================================================================
System Attributes

EC Sales uses a number of System Attributes to control system behavior. This document explains these system attributes.

For a new EC installation, all of these should be checked and set according to the required behavior of EC Sales.

System Attribute 'ALLOW_SALE_CALC_LOCK_MTH'

This attribute indicates whether Sales price calculation is allowed on locked months. "Y" means that Sales price calculation is allowed on locked months.

Options are Y | N.

The Default EC installation value is 'N'.


==========================================================================================
## [6/18] System Attributes
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_System_Attributes.html
==========================================================================================
System Attributes
Introduction

EC Revenue uses several System Attributes to control system behaviour. This document explains these system attributes.

For a new EC installation, all of these should be checked and set according to the required behaviour of EC Revenue.

For more details on each System Attribute, please see descriptions below the following overview table:

System Attribute ACC_REV_INTERFACE_IND

This attribute controls whether to create an interface file to the ERP system for Accrual Reversals or not.

Options are Y | N

Default EC installation value is Y 

System Attribute ACC_REV_VALIDATION_LEVEL

This attribute indicates the default validation level for the Accrual Reversal document.

Options are OPEN | VALID1 | VALID2 | TRANSFER | BOOKED

Default EC installation value is OPEN

System Attribute ACNT_LOGIC_DATE_METHOD

This attribute indicates which date is used to pick up fin_account_mapping, fin_account, fin_cost_object_mapping, fin_cost_object versions when generating posting data. Options are DOC_DATE | TRANS_DATE.

Use DOC_DATE when the versions are decided by the document date.

Use TRANS_DATE when the versions are decided by the transaction date.

Default EC installation value is TRANS_DATE.

System Attribute ALIGN_REPORTING_BOOKING

This attribute indicates whether Booking Period and Reporting Period should follow the same close/re-open process, i.e., when closing a given Booking Period then also the corresponding Reporting Period will be closed automatically.

Options are Y | N

Default EC installation value is N

System Attribute ALLOW_BATCH_OPTION

This is for controlling the following:

In the Document Transfer Validation screen, when the user checks the TRANSFER checkbox and presses the SAVE button, the user is promoted to do the process in Batch or Now.
This prompt is now controlled by System Attribute ALLOW_BATCH_OPTION.

By Default, it is set as Y which means the user will get the prompt for Batch or Now.
If this system attribute is set as N, the prompt will not come, and the document(s) will be set to level TRANSFER immediately.

System Attribute ALLOW_DIFF_CUST_ON_REV

When creating a dependent document on a document with a different customer, by default the reversal will keep the customer from the reversing entry. To have the reversal keep the customer on the current document, this system attribute with value "Y" must be used.

The attribute is not added to the default EC installation.

System Attribute ALWAYS_GEN_POSTING

This attribute indicates whether the system will always generate posting data, Options are Y | N.

If set to Y the system will generate posting data also for vendors for which there will be no interfacing of postings to the ERP system.

The default EC installation value is N.

System Attribute CASCADE_BOE_FACT_CHANGE

This attribute indicates whether immediate cascade will be run when the BOE Conversion Factors are changing.

Options are AUTO | MANUAL | NONE.

Default EC installation value is AUTO

When this attribute is set to AUTO the system will recalculate Stream Item values immediately for all Stream Items that are using the BOE Conversion Factor being changed.

When this attribute i
…[truncated]


==========================================================================================
## [7/18] Interface with EC Sales
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_Interface_with_EC_Sales.html
==========================================================================================
Interface with EC Sales
Introduciton

This document describes the technical details for moving transactional data from the EC Sales Contract Accounts data tables to the IFAC_SALES_QTY data tables in EC Revenue.

New EcBp_Replicate_Sales_Qty package

This document describes the functionality of the EcBp_Replicate_Sales_Qty database package. The package has been completely reworked and will work directly out-of-the-box when certain requirements are met.

All the important procedures and functions within the new package have User Exit support through the ue_Replicate_Sales_Qty package.

The new package can receive Contract Account data from these levels:

Contract Account Level

No Profit Centre set

No Company set

Classes:

DV_SCTR_ACC_MTH_STATUS

DV_SCTR_ACC_YR_STATUS

Contract Account / Profit Centre Level

Profit Centre set

No Company set

Classes:

DV_SCTR_ACC_MTH_PC_STATUS

DV_SCTR_ACC_YR_PC_STATUS

Contract Account / Profit Centre Level / Company Level

Profit Centre set

Company set

Classes:

DV_SCTR_ACC_MTH_PC_CPY

DV_SCTR_ACC_YR_PC_CPY

Note that none of the DAILY Contract Account Data is supported. Such data should be aggregated to a monthly level and stored at the ..MTH…​classes.

The structure of the new EcBp_Replicate_Sales_Qty package is as follows:

Please note that the IFAC_PROFIT_CENTRE_LEVEL procedure can interface to the Profit Centre Level or the Company Level in the IFAC table:

If the number of vendors in the contract = 1 (Single Vendor Contract): Interface to Company Level

If Contract Attribute 'IFAC_PC_USE_FULL_VENDOR' = 'Y' | NULL and the number of vendors in the contract > 1: Interface to Profit Centre

If Contract Attribute 'IFAC_PC_USE_FULL_VENDOR' = 'N': Interface to Company Level

EcBp_Replicate_Sale_Qty.InsertSalesQty Procedure

This is the entry point for all Class Trigger Action calls for all the data classes that are configured for interfacing quantity data into the IFAC_SALES_QTY table.

The procedure makes some initial checks to ensure that IFAC interfacing should take place:

Contract is 'Available in EC Revenue' (ec_contract.revn_ind = Y)

Contract Account has be set to do 'Interface to EC Revenue (ec_contract_account.interface_to_revenue = Y)

The procedure has User Exit support through the UE_Replicate_Sale_Qty.ue_insertSalesQty(…​) procedure.

This procedure evaluates the call and makes the subsequent call to the correct procedure:

If profit_centre_id is null and company_id is null: call IFAC_TRANSACTION_LEVEL

If profit_centre_id is not null and company_id is null: call IFAC_PROFIT_CENTRE_LEVEL

If profit_centre_id is not null and company_id is not null: call IFAC_COMPANY_LEVEL

EcBp_Replicate_Sale_Qty.IFAC_TRANSACTION_LEVEL Procedure

This procedure is called when p_profit_centre_id is null and p_company_id is null in the incoming call to the EcBp_Replicate_Sale_Qty.InsertSalesQty procedure.
The quantities sitting in the Contract Account data classes have not been split to Profit Centre nor Company.

Supported data classes are:

DV_SCTR_ACC_MTH_STATUS

DV_SCTR_ACC_YR_STATUS

These quantities will be interfaced to the IFAC_SALES_QTY table if the contract in question is a truly Single Profit Centre 
…[truncated]


==========================================================================================
## [8/18] Dashboards
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_Dashboards.html
==========================================================================================
Dashboards
Introduction

This document describes the EC Revenue Dashboard widgets that come with the standard EC product. The widgets are designed to be useful as-is, but they can also be used as an example for creating your own dashboards.

Dashboard Data Query

Each dashboard widget in EC must have a Query that will provide the data. This Query is stored in the QUERY record in the CTRL_DASHBOARD_PARAM table. The QUERY must be in XML format.


There are 3 different ways to define the query:

By accessing a data class directly – CLASS syntax

By creating a view in the database and then use the SQL syntax for the QUERY parameter with a SQL query that accesses the data in the view

By a SQL that gives the data directly

For the EC Revenue Dashboards described in this document, we have mostly used variant 2. This variant gives good flexibility such as EC function calls and it is easy to change the where-conditions, etc.
For the Inventory value dashboards, a new Class has been created – DASH_INV_VALUES – and the widgets access the data through this class

All the views defined are using this naming standard for the view definition: V_DASH_<xxxx>.

Each individual Dashboard definition is uniquely identified by a WIDGET_CODE. All the EC Revenue Dashboard widgets are using this naming standard: REVN_<yyyy>

Financial Transactions

The dashboard widgets for the EC Revenue Financial Transaction business area are divided into two main categories:

Counting of documents at the various Document Validation Levels:
Open / Valid 1 / Valid 2 / Transfer / Booked

Monetary values added up to various levels

For all of these, there are a number of variants further described in the following sections.

Financial Transactions - Document Validation Status Dashboards

The purpose of these dashboards is to give an overview of the number of documents at the various document validation levels. Typically it is important to make sure that all documents for the current booking period are set to booked before closing the booking period:

The Document Validation Status dashboards will have variants:

All (showing all with no filtering on Contract Owner Company / Business Unit / Contract Area)

By Contract Owner Company

By Contract Area

By Business Unit

By Business Unit and Contract Owner Company

By Contract Area and Contract Owner Company

Document Date vs Booking Period

When grouping the documents into a given month this can be done either by Document Date or Booking Period. The result may be different for these two variants because the Document Date may be in a different calendar month compared to the Booking Period.

Documents at level Open / Valid 1 / Valid 2 have no Booking Period set as the Booking Period is set then the document is moved to Transfer. For these documents, EC will predict the Booking Period by finding the Booking Period that would have been used if the document was taken to Transfer at the time. This logic also supports the case where system attribute
'DEFAULT_BOOKING_PERIOD' = 'BY_DOC_DATE', in which case the booking period will be the same as the Document Date. Also note that because of this additional check these dashboards may run a little bi
…[truncated]


==========================================================================================
## [9/18] Visual Tracing
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_Visual_Tracing.html
==========================================================================================
Visual Tracing
Introduction

This document describes the functionality and configuration of the Visual Tracing screen. The purpose of the screen is to visualize various data entities in play for a given month and how these data entities are linked together through the tracing.

This document will also describe the technicalities related to the screen and will also give a description of how to customize the screen and the data feeding the screen.

Screen Layout

The Visual Tracing screen looks like this when the tracing is not activated:

The Visual Tracing screen looks like this when the tracing is activated:

The screen has these components:

Navigator
The navigator has these selection options:

Month – Mandatory
This is the month for which to view the Visual Tracing

Property – Mandatory
This is the Property for which to view the Visual Tracing

Actual/Accrual – Optional
This attribute tells if the Visual Tracing should show Actual data or Accrual Data. If left blank it will show both Actual and Accrual data

Show Deprecated – Optional
This attribute tells if the deprecated data entities should be shown or not. When left blank the deprecated entities will be shown. By selecting ’No’ in the popup the deprecated data entities will not be shown.

Year Status section
This section shows the Year Status with one entry for each month of the year for the combination of navigator selections
Month | Property | Actual/Accrual. The Refresh button will regenerate the Year Status for the given navigator selection by calling the EcDp_Visual_Tracing.UpdateYearStatus() procedure. Note that in the current version of the Visual Tracing screen this is the only way to populate the Year Status table.
Each entry in the Year Status table has an icon indicating the status for that month:

    All data for the month has been set to Approved/Booked
    There is data for the month but not all data entities have been set to Approved/Booked
    There is no data for the month
 
The user can click an entry in the Year Status section to reload the screen with data for the selected month.

Visual Tracing graphical component
The Visual Tracing graphical component will show the data entities for the given combination of the navigator values.

The Visual Tracing graphical component has these features:

Which Data Entities to show is controlled by the content of the v_tracing_config view. For more details on the content of this view please see section ’Views’ below.

Each different type of Data Entity will be listed in separate columns. Each individual column of data will have vertical scrolling in case the number of Data Entities is greater than what can be shown within the Visual Tracing graphical component boundaries.

The details of each Data Entity is represented as a Data Entity Box

Each Data Entity Box can have up to 30 lines of text. Each line of text can have an individual background color set:


12 ‘Top Text’ lines of text


6 ‘ordinary’ lines of text


12 ‘Bottom Text’ lines of text
For the Oil Sands business, the 12 Top Text lines will be used for indicating previous month actions/information – and the 12 Bottom Text line will be used for indicating coming months a
…[truncated]


==========================================================================================
## [10/18] Interfacing of 'Other' Line Items
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_Interfacing_Other_Line_Items.html
==========================================================================================
Interfacing of 'Other' Line Items
Introduction

One of the virtues of EC Revenue is to be able to interface values that can be processed into a Period or Cargo document.
Until version EC-11_1-SP02 this was reserved for quantities only.
From version EC-11_1-SP02 it is possible to interface Other Line Items as well, such as:

Fixed Value

Free Unit Price Object

Quantity Based - Free Unit

Interest

Percentage All

Percentage Quantity

Percentage Manual

This document will describe the technicalities related to the different Other Line Items.

Fixed Value

This is to interface a fixed monetary pricing value. The currency is not to be interfaced and is decided by the transaction template.

Line Item Type is mandatory. If not provided, it needs to be added to the document after processing.

Pricing Value is mandatory. If not provided and this is the only line item in the transaction, it will be automatically deleted during process. This because it is empty (no pricing value).

Pricing Currency is not to be interfaced. The currency is decided by the transaction template.

When processing the interfaced data into a document, all line items from the associated template are added to the document according to this rule:

All interfaced Fixed Values with the specified line item type are added to the document.

If the interfaced Fixed Value with the specified line item type matches the one from the template, the template one will not be added to the document.

To interface and process Fixed Value line items into an existing transaction having Quantity line items only is supported.
To interface and process Quantity line items into an existing transaction having Fixed Value line items only is not supported. In this case, the Quantity line items will be processed into a new transaction.

Free Unit Price Object

This is to interface a Free Unit line item with a specified Price Object. The currency is not to be interfaced and is decided by the transaction template.

Price Object is mandatory. This need to be a price object that exists in the current template.

Quantity is mandatory.

Unit is not mandatory. But if provided, it need to match the specified price object.

Unit Price is mandatory only if the "Price Source" in the transaction template is set to "Based on Price Date". Then the Pricing Value will be recalculated based on Quantity and Unit Price.
If the "Price Source" in the transaction template is set to "Based on Pricing Value and Quantity", the Unit Price will be recalculated based on Quantity and Pricing Value.
Mark: The Unit Price need to match the template price list for specified price object.

Pricing Value is mandatory only if the "Price Source" in the transaction template is set to "Based on Pricing Value and Quantity". Then the Unit Price will be recalculated based on Quantity and Pricing Value.
If the "Price Source" in the transaction template is set to "Based on Price Date", the Pricing Value will be recalculated based on Quantity and Unit Price.

Line Item Type is mandatory. If not provided, it needs to be added to the document after processing.

Pricing Currency is not to be interfaced. The currency is decided by the transaction templa
…[truncated]


==========================================================================================
## [11/18] Financial Item
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_Financial_Item.html
==========================================================================================
Financial Item
Introduction

The purpose of the Financial Item features is to be able to store monetary values to any object in EC, i.e. Field, Well, Stream, Facility, Tank, Pipeline, etc. It can also handle quantities in order to handle cases where a quantity has a financial impact.

This document describes the Financial Item (FI) functionality and its configuration details.

Financial Item - key features

A financial Item is an object in EC.

Financial Item transactional data entries can be a monetary value or a quantity value.

Financial Item transactional data entries can be connected to any object in EC.

Financial Item transactional data entries can be connected to a Company type of object.

Financial Item transactional data entries can be connected to a Cost object type of object.

Financial Item transactional data entries can be connected to a Financial Account.

Financial Item transactional data entries can be connected to a Contract Area.

Financial Item transactional data entries can be stored on a Daily, Monthly, and Yearly basis.

Financial Item transactional data entries can have different Datasets for the same time period.

Financial Item transactional data entries can be created as follows:

The user inserts a single Financial Item object

The user inserts from a Financial Item Template containing one or more Financial Item objects

A Calculation execution

The following Business Functions (screens) are available for the Financial Item concept:

Financial Item Definition: Financial Item objects and corresponding Dataset linking is maintained in this BF

Financial Item Template: Financial Item objects can be grouped into one or several templates in this BF

Daily Financial Item: Managing Transactional data at Daily level

Daily Financial Item Calculation: To use EC Calculation engine to calculate Financial Item values at Daily level

Monthly Financial Item: Managing Transactional data at Monthly level

Monthly Financial Item Calculation: To use EC Calculation engine to calculate Financial Item values at Monthly level

Yearly Financial Item: Managing Transactional data at Yearly level

Yearly Financial Item Calculation: To use EC Calculation engine to calculate Financial Item values at Yearly level

Financial Item Definition

Financial Item Definition screen is used to create and maintain Financial Item (FI) objects and their Datasets.

The Financial Item Definition screen has these components:

Navigator

Navigator settings allow the user to define the search criteria for the Financial Item objects and list them in the table.

Navigator has these selection options:

Date – Auto-filled with the first day of the current month.
Only Financial Item objects being valid on this date will be listed on the screen.

Business Unit - Optional
This is the Business Unit the Financial Item belongs to.

Contract Area – Optional
This is the Contract Area the Financial Item belongs to. Please note that when a particular Contract Area has been selected then any Financial Item objects with this Contract Area will be listed together with any Financial Item objects having no Contract Area set. The Contract Area setting can be used for limiting data
…[truncated]


==========================================================================================
## [12/18] Calendar / Calendar Collection
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_Calendar.html
==========================================================================================
Calendar / Calendar Collection
Introduction

EC Revenue uses Calendar objects and Calendar Collection objects to define business days/holidays, which then is used for finding the correct Document Date, Document Received Date and Payment Date.

It is the Calendar Collection object that is used when finding business days/holidays for the Document Date, Document Received Date, and Payment Date.
Each Calendar Collection will have one or more Calendar objects linked to it with their own set of business days/holidays.
The effective set of business days/holidays is then the union of business days/holidays in all the calendars being part of the Calendar Collection - this means that if a given date is a holiday in one of the calendars, then this is a holiday for the Calendar Collection.

In earlier versions of EC setting up the various Calendars for a given year were a bit cumbersome where the user could only view one month at the time.
Also, recurring holidays had to be entered for each year when instantiating the Calendar for that year.

The new Calendar / Calendar Collection Business Functions have new functionality that makes it much more user-friendly to work with these BFs.

Calendar Featrues

One single Business Function (BF) with tabs for managing the Calendar object
In earlier versions of EC, we had two different BFs for handling the Calendar: Calendar object and Calendar Setup

The tabs are:

Calendar object

Recurring Holidays

Calendar Setup

Calendar Usage

The new Calendar Collection BF has these features:

One single BF with tabs for managing the Calendar Collection object
In earlier versions of EC, we had three different BFs for handling the Calendar Collection: Calendar Collection object, Calendar Collection Setup, and Calendar Collection Usage

The tabs are:

Calendar Collection

Calendar Collection Setup

Calendar Collection Usage

Calendar Business Function

The new Calendar BF has these features:

One single BF with tabs for managing the Calendar
In earlier versions of EC, we had two different BFs for handling the Calendar: Calendar object and Calendar Setup

New functionality for handling Recurring Holidays, including moving holidays such as Easter and holidays being relative to Easter

Support for customized moving Recurring Holidays, i.e. Holidays that occur every year, but on a different date.
An example of this is the Early Spring Bank Holiday in the UK, which is the first Monday of May every year.

New functionality for configuring the business days/holidays for a given Calendar / Year using a full-year calendar component showing the year in one go.

Support for adding 'Holidays and Observances' entries for any date in the year

Calendar Tooltip showing the Holidays and Observances description when hovering over a date in the calendar

Dates having a 'Holidays and Observances' entry are marked with a different background color.

New functionality for showing 'Calendar Usage' - this feature tells which Calendar Collection is using the given Calendar object.

Navigator

The top section of the screen has a Navigator with just a Date field.

The resulting list of Calendar objects will be those Calendars being valid for the date 
…[truncated]


==========================================================================================
## [13/18] How-To configure LOCALE in EC
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_How_To_Configure_LOCALE_in_EC.html
==========================================================================================
How-To configure LOCALE in EC
Introduction

The LOCALE can be configured in EC such that calendars starts with the correct weekday, i.e starting with Monday in Europe or starting with Sunday in the US.

This How-To explains how to do this in EC.

Step-by-Step Guide

The LOCALE variable in Java is a combination of Language code and Country code, like this: 'en_US' for English in the USA, 'no_NO' for Norwegian in Norway.
Please see https://www.oracle.com/java/technologies/javase7locales.html for more details.

The steps for configuring this in EC are as follows:

Step 1:
Make sure you have the required countries defined in the Language screen:

Step 2:
Define the Language setting for the user in question. We are using 'sysadmin' as user id in this example.
Go to screen Personal Settings and select ‘Regional Settings' in the 'Customise Category' popup - click the 'Go' button.


Step 3:
Select entry 'Language'

Step 4:
Add a 'User Property Value' for the user:

Please note that if you want to change the default value for user 'EC_Default', then this must be one in the database backend with the following update statement:

update ctrl_property_meta x set x.default_value_string ='NO'
where x.key = '/com/ec/eccore/locale/language';

Step 5:
USER entry added for user 'sysadmin':

Step 6:
Select a Language from the 'Value' drop-down - in this case, 'NO' for Norway:

Step 7:
Select the 'Country' entry on the same screen.

Please note that if you want to change the default value for user 'EC_Default', then this must be one in the database backend with the following update statement:


update ctrl_property_meta x set x.default_value_string ='NO'
where x.key = '/com/ec/eccore/locale/country';

Step 8:
Add 'USER' entry for the user in question:


Step 9:
Select a Country from the 'Value' drop-down - in this case, 'NO' for Norway:

Step 10:
Go to a screen where there is a Date selector and see that the week starts on the correct weekday - in this case, it will start with Monday:

Step 11:
Go to the Calendar screen and see that the weeks are starting on the correct weekday - in this case, it will start with Monday:


==========================================================================================
## [14/18] How to configure Stream Item Calculations
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_How_To_Configure_Stream_Item_Calculations.html
==========================================================================================
How to configure Stream Item Calculations
Introduction

The EC Calculation Framework can be used for calculating Stream Item values in the EC Revenue Quantity module, both Daily and Monthly.

This 'How-to' explains how to configure this.

Define the calculations

The calculations for Stream Items must have Calculation Context = 'Stream Item Volumes':

Configure the calculations

Add the calculation steps - just a simple INFO statement in this example (similar for the monthly calculation):

Define the Allocation Network

The Stream Item type of calculations is executed by Allocation Networks and the Nodes connected to each Allocation Network. An Allocation Network must be defined:

Please note that the 'Period' can be Daily | Monthly | Daily and monthly.
You can also have separate Allocation Network objects for Daily vs Monthly calculations.

Define the Allocation Networks List

Define the Nodes being members of the Allocation Network List:

Stream Items are connected to Stream objects that are connected to Nodes. This means that from within the calculation itself you will have access to all Stream Items connected to Streams that are connected to the Nodes in the list provided in the Allocation Network List screen.

Define the Calculation Job Connection

Link the Calculations to the Allocation Network:

Note that you can link both Daily and Monthly type of calculations to the same Allocation Network object.

Run Monthly Quantity Allocation

You can now run the calculation for monthly Stream Items from the 'Monthly Quantity Allocation' screen:

Note that the 'Calculation Job' popup will only list the calculations having Period = Monthly.
Also note that if you have been into the Daily Quantity Allocation screen and set the 'To Date' then this date will be remembered into this screen with a date that might not be the first of the month.
In this case, the calculation will fail. To prevent this error you need to re-select the 'To Month'. This error will be fixed in EC-12.1.

Run Daily Quantity Allocation

You can now run the calculation for daily Stream Items from the 'Daily Quantity Allocation' screen:

Note that the 'Calculation Job' popup will only list the calculations having Period = Daily.


==========================================================================================
## [15/18] Consolidation of Financial Transactions / Process screens
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_Consolidation_of_Financial_Transactions_Process_Screens.html
==========================================================================================
Consolidation of Financial Transactions / Process screens
Introduction

The various parts of a Financial Document in EC can be managed through a number of screens. In the early days of EC Revenue, all these screens were organized under the EC Revenue > Financial Transaction > Process folder in the EC Treeview.

At a later stage, we introduced the Period Document Generation (PDG) / Cargo Document Generation (CDG) screens. In the beginning, the purpose of these screens was to handle interfaced data in the IFAC_SALES_QTY table for the Period type of data and the IFAC_CARGO_VALUE table for Cargo type of data. The PDG/CDG screens have gradually been enhanced with more and more functionality, including functionality that is available from the EC Revenue > Financial Transaction > Process folder screens, resulting in having similar functionality in separate screens.

In EC-12.1, we have decided to take all relevant functionality in the existing EC Revenue > Financial Transaction > Process folder screens and incorporate it into the PDG/CDG screens, and then remove the EC Revenue > Financial Transaction > Process folder screens. As part of moving the functionality into the PDG/CDG screens, we have also made a number of enhancements to the functionality.

The following overview lists the EC Revenue > Financial Transaction > Process folder screens in EC-12.0 and how these have been changed in EC-12.1:

Financial Transaction > Process > Document General screen: Functionality has been moved to PDG/CDG screen and the screen has been removed.

Financial Transaction > Process > Transaction General screen: Functionality has been moved to PDG/CDG screen and the screen has been removed.

Financial Transaction > Process > Transaction Quantities screen: Functionality has been moved to PDG/CDG screen and the screen has been removed.

Financial Transaction > Process > Transaction Values screen: Functionality has been moved to PDG/CDG screen and the screen has been removed.

Financial Transaction > Process > Transaction Distribution screen: Functionality has been moved to PDG/CDG screen and the screen has been removed.

Financial Transaction > Process > Document Text screen: Functionality has been moved to PDG/CDG screen and the screen has been removed.

Financial Transaction > Process > Banking Details screen: Functionality has been moved to PDG/CDG screen and the screen has been removed.

Financial Transaction > Process > Calculation Log screen: Moved to folder EC Revenue > Revenue Logs folder. No changes have been made to this screen.

Financial Transaction > Process > Interface Files screen: Moved to Financial Transaction folder. No changes have been made to this screen.

The result of this is also that the EC Revenue > Financial Transaction > Process folder has been removed as well.

The PDG/CDG screens have been implemented using tabs in combination with the new expand/collapse section feature.  It has also been important to design the screen such that any information is a few mouse clicks away as possible.

All data handled by the PDG/CDG screens are using proper classes allowing for customer implementation customization by adding/hiding data elements, with a 
…[truncated]


==========================================================================================
## [16/18] Consolidation of Inventory screens
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_Consolidation_of_Inventory_Screens.html
==========================================================================================
Consolidation of Inventory screens
Introduction

For this version of EC, we have consolidated all the Inventory Setup and Inventory Process screens into two separate screens:

Inventory Configuration

Inventory Processing Year-to-Month

This will make configuration and processing of Inventories much easier for the front-end user with all functionality one-click away.

Inventory Configuration

The new Inventory Configuration screen is made up of the following old screens:

Inventory Properties

Inventory Rate Definition

Inventory Rate Selection

Inventory Rate Values

Inventory Item Selection

Inventory Historic Layer

The layout of the new screen is illustrated in the printscreen below. The old screens are now represented as individual tabs in the screen. The "Copy to New" button in the first tab (Inventory Properties) will not only copy the configuration in the Inventory Properties tab, but all the configuration for the selected Inventory in all six tabs, except the Historic Layer.

New logic has been implemented to hide unused sections or attributes from the front-end user, e.g. if physical stock is not utilized, all sections and attributes related to physical stock will be hidden from the front-end user.
Similarly, if Memo Currency is not in use, then all the references to this is hidden. Same applies to the UOM2 - hidden if not in use.

The functionality of each tab in the screen is briefly explained below:

Inventory Properties - This tab is for managing the Inventory object itself. From this tab the user can add new Inventory objects, modify existing objects, delete existing objects, and create new versions of an existing object. Please note that attributes related to Physical Stock will be hidden if the Inventory object in question is not using the Physical Stock feature, i.e. 'Use Physical Stock' attribute is not ticked.

Inventory Rate Definition - This tab is for managing the Rate Objects to be used with the Inventory. Typically there will be different Rate objects for Underlift vs Overlift, and also separate Rate objects for Physical Stock. For a Pool type of Inventory there is also typically individual Rate objects for each Field taking part in the Pool.

Inventory Rate Selection - This tab is for linking the Rate Objects to the Underlift / Overlift / Physical Stock for each Field taking part in the Inventory. The section for linking Physical Stock type of Rate objects is hidden if the Inventory object in question is not using the Physical Stock feature, i.e. 'Use Physical Stock' attribute is not ticked.

Inventory Rate Values - This tab is for managing the rates for each of the Rate Objects taking part in the Inventory. Each Rate value has a Valid From date, and the Rate value is then valid until there is a new entry for the same Rate object having a later Valid From date.
This tab has also got a new feature which allows for adding entries for all the Rate Objects for each month of a year in one go.

Inventory Item Selection - This tab is for linking Stream Item objects for Inventory Movement / Production Source / Physical Stock to the Field(s) taking part in the Inventory.
The section for Physical Stock Stream Items is hidden i
…[truncated]


==========================================================================================
## [17/18] Quantity Module Enhancements
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_Quantity_Module_Enhancements.html
==========================================================================================
Quantity Module Enhancements
Introduction

Two new tabs have been created and added to the Daily- and Monthly Quantity screens to improve usability and overview for the front-end user:

Month-by-Day tab: shows Stream Item values for the selected Stream Item for all days of the selected month

Year-by-Month tab: shows Stream Item values for the selected Stream Item for all months of the selected year

Daily Quantity screens

New functionality has been created, allowing the front-end user to manage daily data for a full month for the selected Stream Item where data for each of the days of the month in question are listed in a separate tab in the screen.

The Month-by-Day tab has been added to the following screens:

Daily List Input (VO.0002)

Daily List Overview (VO.0015)

Daily Node Input (VO.0016)

Daily Node Overview (VO.0017)

Daily Quantity Input (VO.0026)

Daily Quantity Overview (VO.0018)

Monthly Quantity screens

New functionality has been created, allowing the front-end user to manage monthly data for a full year for the selected Stream Item where data for each of the months of the year in question are listed in a separate tab in the screen

The Year-by-Month tab has been added to the following screens:

Monthly List Input (VO.0019)

Monthly List Overview (VO.0020)

Monthly Node Input (VO.0021)

Monthly Node Overview (VO.0022)

Monthly Quantity Input (VO.0025)

Monthly Quantity Overview (VO.0023)

Accruals

It’s also possible to calculate the accruals for the following days or months using the Daily / Monthly Accrual Method selected on the Stream Item in these new tabs by pressing the RUN ACCRUAL button

For the Daily Stream Items, the accrual method can be either:

Take the last available daily actual

Take the month’s average daily actual

Manual entry

For the Monthly Stream Items, the accrual method can be either:

Take the previous month’s available value

Take the average daily number in the month and multiple with the number of days in the same month

Manual entry

Once the accrual calculation is finished and the calculated value has been populated on the stream item, the stream items will receive status = ACCRUAL. If you press the ACCRUAL TO FINAL FOR ALL SI IN SCREEN button, all the accruals displayed in the screen will be set to FINAL.


==========================================================================================
## [18/18] Client Side Data Validation for Stream Items
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/revn/EC_Revenue_Client_Side_Data_Validation_for_Stream_Items.html
==========================================================================================
Client Side Data Validation for Stream Items
Introduction

This is a guide for how to configure Client Side Data Validation (CSDV) for EC Revenue Stream Items.

Configuration for the Stream Item object class

For CSDV to work you first need to set the INCLUDE_IN_VALIDATION class attribute to Y for the Stream Item object class:
(You need to add the attribute – it is not there by default)

Re-generate the class, either using the 'Generate Class View' button, or by SQL command:

EXEC ecdp_viewlayer.BUILDVIEWLAYER(p_class_name => 'STREAM_ITEM', p_force => 'Y');
EXEC ecdp_viewlayer.BUILDREPORTLAYER(p_class_name => 'STREAM_ITEM', p_force => 'Y');
Configuration for the Stream Item data class – STIM_MTH_VALUE in this case

For CSDV to work you also need to set the INCLUDE_IN_VALIDATION class attribute to Y for the Stream Item data class – in this case data class STIM_MTH_VALUE:
(You need to add the attribute – it is not there by default)

Re-generate the class, either using the 'Generate Class View' button, or by SQL command:

EXEC ecdp_viewlayer.BUILDVIEWLAYER(p_class_name => 'STIM_MTH_VALUE', p_force => 'Y');
EXEC ecdp_viewlayer.BUILDREPORTLAYER(p_class_name => 'STIM_MTH_VALUE', p_force => 'Y');
Setting the validation limits

Go to screen 'Object Validation – Default'

Set Navigator values:
Object Class = Stream Item
Object Name = <the Stream Item you want to set the limits for>
(Note that the drop-down in only showing Name – so having unique Stream Item naming is smart!

Set a New Version Date and click the ‘Create New Version’ button.

Note that the Conditional check-box is not ticked. This means that if the value is in the Error range you will not be able to save.
When the Conditional check-box is ticked, you are able to save after confirming that you want to save the value – see section below.

In this case the Volume validation will be:


Screen behavior

Go to screen ‘Monthly Quantity Overview’

Set Navigator values:

Month = <an instantiated month where the CSDV is valid for>
Stream Item Code = <The Stream Item you have set the CSDV for>

Data entered is in the Green zone – no warning or anything:

Data entered is in the Orange zone – warning issued as a Yellow underline and also the mouse-over will tell the limits.

The data can be saved.

Data entered is in the Red zone with the Conditional flag set:

User must confirm to save the value:

Confirming the Conditional Action will save the value and the value will appear in red with the error range shown when mouse-over:

Data entered is in the Red zone with the Conditional flag not set:

In this case you will not be able to save the data value, and a warning will appear:

The error message is a bit misleading as there is no red…the red is there AFTER the save…which is no allowed…so using the Text Translation is advised, for instance:

Then this is the result:

Data populated into the class from the DB

The Data validation will also work when inserting data directly into the database, but it will not prevent you from saving.

update stim_mth_value v set v.net_volume_value = 50
  where v.object_id = ec_stream_item.object_id_by_uk('SI000001')
  and v.daytime = to_date('2020-01-01','YYYY-MM-DD');
…[truncated]