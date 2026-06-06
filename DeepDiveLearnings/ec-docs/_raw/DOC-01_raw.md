# Raw content — DOC-01
Modules: ['product_concept', 'user_guide', '(top)']
Pages: 11



==========================================================================================
## [1/11] Technical Documentation Overview
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/overview.html
==========================================================================================
Technical Documentation Overview

EC version: 14.2.4

This document provides a Technical Overview about Energy Components (EC). It contains chapters describing the Business Areas and related functionality, a basic user guide about how to get started, technical documentation for the different modules, and information about the process automation in EC.


==========================================================================================
## [2/11] Energy Components Business Areas
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/ec_business_area.html
==========================================================================================
Energy Components Business Areas
Introduction

This Chapter contains information about Energy Components (EC) and provides information about the different business areas covered by EC, and details about the specific functionality that is present within each module.

Energy Components (EC) covers accounting of hydrocarbon (oil and gas) quantities, qualities, and ownership from the wells via transportation systems until it is sold to the first buyer. It consists of five main business areas: Production, Chemistry, Transport, Sales, and Revenue. Below is a summary of each business module within EC.

Figure 1. Overview of the Energy Components system modules
EC Production

The EC Production module supports all aspects of production management from forecasting to full production. The module is able to take into account specific production requirements including gas/condensate fields, coal-bed methane fields, heavy oil and bitumen production, and onshore pumped wells (without any automation and tank farms). This module is also able to track actual performance against targets and identify bottlenecks in order to maximize production from the assets.

Core EC Production capabilities

Automatically acquire data from DCS, data historians and other sources

Perform comprehensive validation and quality control on all data

Record well tests and calculate test results for individual wells

Estimate individual well rates based on a range of methods, taking into account enhanced recovery mechanisms, including full support for so-called "intelligent" wells

Allocate each phase back to individual wells and completions

Allocate sales products back to individual wells and completions

Allocate production down to reservoir zones

Manage use and inventory of chemicals

Perform emission reporting and environmental accounting

Record all data required for daily production and operation reports

Perform inventory management including volumetric calculations based on e.g. tank strapping tables

Execute full 'ownership allocation' including royalty and production sharing arrangements

Manage production allowances, forecasts, targets, and potentials

Generate forecasts based on potentials, constraints, planned downtime, service factors etc.

Adopt a systematic approach to production downtime and deferments based on widely accepted principles, including the allocation of deferment quantities to events

Perform calculations of key performance indicators

Report internally and externally to JV partners, as well as all regulatory reporting

EC Chemistry

The EC Chemistry module is a comprehensive data management solution, collecting data from various sources including manual inputs, sensors, and laboratory analyses. Validating and processing data, it provides valuable insights through dashboards and reports.

Core EC Chemistry capabilities

Chemical Inventory Management involves monitoring chemical levels, calculating usage rates, and predicting the duration until supplies are depleted. This system ensures efficient tracking and management of chemicals, helping to prevent shortages and optimize usage.

Laboratory Integration Management focuses on managing sample schedules, which includes tracking sample analysis and integrating laboratory data. This approach aims to streamline laboratory operations and improve efficiency in handling samples.

Chemical Performance Optimization focuses on designing injection networks to enhance chemical usage efficiency. This process involves calculating target rates and dosages, as well as analysing trends to ensure optimal chemical usage.

EC Transport

The EC Transport module covers the transportation of hydrocarbons either through pipeline systems or by vessels. EC transport is used for a variety of transportation requirements including oil terminals, LNG Export/Import terminals, gas plants, and pipeline transport operations.

Core EC Transport capabilities

Perform cargo scheduling for multiple crude blends, condensates, LNG, and other products. Issue official and tentative lifting programme. EC can generate a lifting program based on entitlements and fixed cargo sizes (often the situation with offshore liftings) or build the lifting program based on nominations

Evaluate that lifting schedules and opportunities are operating within operational and commercial constraints in a sandbox environment

Record relevant data from tanker inspections and keep history record per ship

Issue all official cargo documents as defined in relevant Lifting Procedure, including e.g. Bill of Lading, Certificate of Quantity, Certificate of Quality, Time sheet, etc.

Demurrage handling including invoicing and payment tracking

Handle claims and fail-to-lift situations

Perform complete lift accounting per lifter per field and per product. Handle any swap arrangements between lifters

Calculate entitlements according to JV arrangements and prevailing royalty/PSA terms

Perform crude oil value adjustment supporting both in-kind and in-cash settlements

Perform scheduling LNG vessel arrivals, and storage evolution at LNG import terminals

Manage nominations and re-nominations from shippers. EC supports both non-pathed and pathed nomination models. EC offers a message broker solution ensuring safe and controlled data exchange with shippers and other parties

Track the flow of gas through the pipeline segments of the pipeline

Assess available capacity against aggregate nominations at each network point and handle curtailment situations

Implement and manage gas storage, balancing, and other flexibility arrangements

Handle title transfer and arrangements where parties buy/sell from each other

Perform matching of nominations with any adjacent transport network operators

Keep separate long term forecasts for expected gas availability

Record measurements of quantity and quality on a continuous basis

Perform allocation and reconciliation of all data at periodical intervals

EC Sales

The EC Sales module includes functionality that supports the sales organisation in all aspects of selling/trading hydrocarbons including managing complex gas sales contracts.

Core EC Sales capabilities

Manage nominations, re-nominations, and requests from individual buyers, and validate against contractual terms

Manage gas availability from own production, gas storage, balancing positions, substitution arrangements, etc.

Assess contractual obligations against gas availability and deal with any shortfall situations

Place shippers nominations to all relevant gas transport service operators

Attribute actual deliveries to sales contracts according to priority and user-defined rules

Perform full contractual accounting according to contract clauses. For take-or-pay contracts, this involves handling e.g. carry-forward gas, make-up gas, shortfall allowances, etc.

Calculate prices in multiple currencies according to published reference prices, consumer price indexes, and applicable contract terms

EC Revenue

The EC Revenue module covers the valuation of hydrocarbon Sales and Purchases as well as valuation of Tariff Income and Tariff Cost for infrastructure usage, including invoicing and revenue allocation and distribution of these financial transactions. Energy Components is the only solution that addresses the complete value chain from reservoir to revenue. It is specifically designed for the upstream industry. The system can handle some of the most complex revenue arrangements, including lifting agreements between joint venture parties, royalty/PSA agreements, and multi-product, multi-currency invoicing. The module offers full traceability and auditability - supporting SOX404 compliance.

Core EC Revenue capabilities

Valuate all hydrocarbon deliveries using prevailing prices and applicable contractual terms

Generate and submit invoices, calculate interest rates, and track payments

Perform accrual and preliminary postings

Perform prior period adjustments

Fully automated invoicing based on contractual rules and settings

Integrate with financial accounting systems for booking of cost and revenue

Valuate inventories and book value of hydrocarbon inventory positions

Calculate and book remaining reserves and production related depreciation keys (UOP)

Perform production and revenue forecasting and budgeting, including regular closure forecast for remaining months in year (both calendar and gas-year supported)

Interface with financial accounting system for booking of all transactions. The interface will update status of each booking in EC once the accounting system has confirmed the booking

Allowing of uploading and manipulating (grouping and splitting values and quantities) for the ERP system to produce amounts and values that can be used for reporting such as allowable deductible costs

Perform complex inventory valuations through a value chain, allowing tracking production, purchase, transportation, and other costs associated to each unit

EC Addon Packages

Add
…[truncated]


==========================================================================================
## [3/11] Energy Components: Getting Started
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/user_guide/ec_getting_started.html
==========================================================================================
Energy Components: Getting Started

Energy Components is a module-based application software with fully configurable screens and calculation models.

It is a web-based application, accessed through an internet browser - this means you as a user do not need to install any additional software. To access the system you will need to get the Energy Components URL, and a username and password from your IT Department.

Basic System Requirements

Browser: Google Chrome or Microsoft Edge (Chromium).

Operating System: No specific requirement

Screen Resolution: Minimum 1280 x 1024

For detailed system requirements, see the EC Installation Guide.

Because Energy Components is web based, any data you enter into a screen exists on your screen until you save it. Once you have saved the information it goes into the central database and is available to anyone who has access to the screen or record.
Logging On

Energy Components is a web-based application. To access the software, open your web browser (which must be according to basic system requirements). In the address bar of your web browser, type in the Energy Components web address (contact your IT department for the web address, or URL). The login screen (below) will appear. You will then need to type in your User Name and Password and click the Log In button.

Once you have logged in, do not use the browser’s "Back", "Forward" or "Refresh" buttons. Use the controls within the Energy Components screens. If you use the browser’s buttons you are likely to be logged out and might lose unsaved data.


==========================================================================================
## [4/11] The Energy Components Screen
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/user_guide/ec_screen.html
==========================================================================================
The Energy Components Screen
Introduction

The Energy Components screen is made up of seven different windows or panes: Title Bar, Tool Bar, Tree View, Data Window, Navigator Pane, Status Area and the browser’s Status Line. These panes will always stay the same, with the exception of the Data Window and the Navigator Pane, which change depending on the type of operations being carried out.

Below is a summary of the different windows or panes within the Energy Components screen:

Title Bar Displays application logos and labels, the login id of the person who is logged in, a logout icon, and the system menu bars.

Tool Bar Displays the standard Energy Components functions as icons, e.g. 'Save', 'Retrieve', 'Insert', 'Delete', 'Maximize/Minimize view', 'Add to Favorites', 'Screen settings' and 'Tasks'. It also displays the screen name.

Tree View Used to navigate to the specific Energy Components business function.

Navigator Pane Used to filter what data to display in the Data Window, e.g. select period, assets, etc.

Data Window Displays the data you have selected in the Tree View and the Navigator Pane.

Status Area Displays information about record creation/updates, record revisions, record status, four eye approval info, hints & tips, validation info, trending info and attachments.

Title Bar

The Title Bar displays the application logo, the Login ID of the user logged into the session (in this case sysadmin), a logout icon and the system menu bars:

The icons on the Title Bar have specific meanings as described in the following table:

Icon	Function


	

Logout

Ends the current user session and returns the user to the application Login screen




	

Help

Context sensitive help for the selected business function.

Tool Bar

The Energy Components Tool Bar has six icons (to use the icons, left click on them):

The icons on the Tool Bar have specific meanings as described in the following table:

Icon	Function


	

Save

Saves updated data in the Data Window to the database




	

Retrieve/Refresh

Refreshes the display




	

New

Insert fields, ready for new registration of data




	

Delete

Marks the selected row for deletion




	

Maximize/Minimize view

This shows or hides the Tree View area and the Status Area of the screen to make more horizontal space available for the display of data. This is particularly useful if you have to scroll across the screen to see a complete record.




	

Add to Favorites

Add the entry of current Business Function into the Favorites section




	

Screen settings

Override system of measurement (only valid from screens with group model navigator). Refer to System of Measurement

Reset personalisation for all components in the screen. Set or reset user defaults for the screen.




	

System of measurement

Only visible when system of measurement has been overridden. Show the selected system of measurement. Can be used to select system of measurement. Refer to System of Measurement




	

Available Tasks

This shows the number of available tasks waiting for an action. Clicking the icon takes you to the Todo List screen. The icon is refreshed every 5 minutes.

When a function on the Tool Bar is not available for use it is 'greyed out' to show that it is deactivated. In some screens when you start to add data, icons which have previously been deactivated will become activated.

Tree View

The Tree View is the basic navigation mechanism by which you can access screens and functions within the Energy Components system. It is similar in structure to Windows Explorer file menu. It is an expandable tree, which contains all of the menu options you are allowed to access. The menu supports several levels of indentation, so that screens can be grouped together under meaningful headings and in a way that supports the workflow process of the function. Select the relevant folder and file from the Tree View menu depending on the operation you wish to carry out.

The Tree View window has two distinct areas. The top portion of the Tree View contains configuration and maintenance functions. The lower portion contains business functions which are grouped together by specific function, i.e. Allocation, Terminal Operation, etc.

For ease of use, there is also a search field which allows you to search for Energy Components screens or business functions. You can also drag and drop your favorite screens into the Favorites section for easy access.

The screenshot below has been taken from a system that has access to all screens. The information displayed in the Tree View (as shown below) will vary depending on the access rights you have been granted. Your access rights will be set by the system administrator based on the role you are holding.

Navigator Pane

After selecting the appropriate screen on the Tree View menu, you can use the Navigator to select the class of data or date range you wish to view. There are two types of Navigator Panes, depending on the type of data you want to view: Standard Navigator and Filter Navigator.

Standard Navigator

The Standard Navigator consists of options to select the date range by clicking on the calendar icon. You can select the asset by clicking on any of the other drop-down menus. Click 'Go', and the information you require will appear in the data pane.

Data Window

The Data Window has several different layouts. The Data Window layout will depend on the specific screen you have selected from the Tree View window and the information selected in the Navigator Pane. The image below shows an example of a typical Data Window layout. This screen shows all the detail of a record in one list.


To update the data:

Place your cursor in the record you wish to update

Type in the new value or use the drop down lists to update information

If a data entry field is white you have the option to add data to the field to complete an action

If a data entry field is yellow it is mandatory that you add data to the field before an action can be completed

If a data entry field is gray the field is read only

Status Area

The Status Area (below) appears at the bottom of the main screen. It displays information about the specific screen that have been accessed in the Tree View menu. This is a standard section at the foot of each screen and includes five standard tab pages, including: Record Status, Revision Info, Hints & Tips, Validation and Trending.

Record Status

The Record Status Tab (below) tells you who created a record and when and who made the most recent changes to the record.


The Record Status Tab page displays the following information for a selected item of data on the screen:

User who created the item of data

Date and time when the item of data was created

User who last updated the item of data

Date and time when the item of data was last updated

Record status of the item of data, e.g. provisional or approved data, number of revisions

Provisional status is the default status for a record until a job is run and the status updates

Verified status is typically used when data has been automatically loaded into Energy Components using the EC data capture features or other interfaces

Approved status is where a job is run on the data, updating the status to the highest security level

Revision text associated with the current revision of the data item

Revision Info

This Revision Info Tab (below) lists all the changes that have been made to a record since its creation. This list is updated each time a user makes a change to the record.

The Revision Info Tab page displays the following information for a selected item of data on the screen:

List of all revisions associated with the data item

The actual value the item has in each revision (with changed values highlighted)

For each revision, the name of the user who updated the data

For each revision, the date/time when the data was updated

For each revision, the text associated with that revision

Approval Status

This Approval Status Tab (below) is used for four eyes approval. It is only applicable for screens with four eyes approval enabled. Refer to Four Eyes Approval.

The Approval Status Tab displays the four eyes approval status.

Click the Accept button to approve a changed.

Click the Reject Deletion button to reject deletion.

Hints & Tips

The Hints & Tips Tab can be used to display and edit helpful notes relating to a particular screen. An example of the Hints and Tips section of the Status Area is shown here:

To add a Hint or Tip:

Click on the Hints & Tips tab

Enter the text

Click on Save

When you go back to visit this screen, the hint/tip will be displayed

Validation

The Validation Tab is a log of the results of validation checks, created from using of the 'Check Rules' function. Any validation failures will appear in the Validation Tab screen. To clear the validation log, correct the record/s by rerunning the validation process or alternatively, delete the errors from the log. You can rerun a sin
…[truncated]


==========================================================================================
## [5/11] Help
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/user_guide/help.html
==========================================================================================
Help
Introduction to Help

The Help system in Energy Components (also referred to as 'Online Help') is contextualized depending on which screen you are using. For example, if you are in the Daily Gas Stream Status screen, the help information provided will relate specifically to the Daily Gas Stream Status screen.

Each help file contains the following:

Images of the screen

Description of the business function

Information of the DB class definitions for each screen component

Modifying Help content

Users with "Edit" access (user or role has the "onlinehelp" access object) are allowed to update the help content. To do so, open the help screen and click inside the description area. A text editor will then open automatically where you can do your modifications, and tick the accept button (v) when you are done. It is also possible to add new screenshots by clicking the "Add screenshot" link.


==========================================================================================
## [6/11] Configuration Overview
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/product_concept/configuration_overview.html
==========================================================================================
Configuration Overview
Introduction

The major concept behind Energy Components is that it is configurable without the need for programming expertise or system downtime. Both the back end functionality and the user interface can be configured. A unique feature of Energy Components is the ability to allow clients to reconfigure the system without the need for high level programming skills. The configuration changes are quick to make and take effect immediately. New configurations can be added while the system is in use – avoiding the need for system or user downtime. This makes system changes financially efficient as well as time efficient. Configurable areas include:

User interface, screens, and navigation features (referred to as 'Business Functions' in Energy Components)

The methods the system uses to react, calculate and process data (referred to as 'Business Processes' in Energy Components)

With the configuration capability, Energy Components can:

Include or hide new columns

Configure calculated numbers in the reporting layer that can then be displayed as and when required

Be configured for multiple languages

Be configured by role or record status

As illustrated in the screen shown below, the following areas within Energy Components can be configured by Quorum Software prior to roll-out, or by the client after roll-out:

Tree View

Navigator

Access to Objects

Units

Audit Tracking

Check Rules

Record Status

Screen Configuration

Tree View menu can be configured

Navigator can be configured

Access to Objects can be configured

Units can be configured

Configuration Options
Tree View

The Tree View can be tailored to meet the requirements of each customer. Energy Components comes with a standard menu layout where business functions are grouped together. These can easily be changed to reflect the customers' workflow and processes. The Tree View will contain different functions for different users depending on their business area and the users' level of access rights. When a user does not have access to a given screen or business function, the screen will not be visible on the Tree View.

For ease of use, there is also a search field, which allows you to search for the Energy Components screen or business function you are searching for. You can also drag and drop your favorite screens into the Favorites section for easy access.

Navigator

The Navigator can be configured for each screen. Most screens in Energy Components use a dynamic Group Model Navigator which reads the Group Model Configuration and populates the columns dynamically. If the Group Model Configuration is changed, the Navigator (and subsequently what is shown on the screen) will change to reflect the new model and hierarchy.

Units

The Units used in the application can be changed. There are two types of Units used in Energy Components, these are:
Display Unit - Indicates what unit type should be displayed in the screens
Storage Unit - Indicates what unit type should be stored in the database

Each Unit is configurable for each measurement type. For instance, once pressure measurements have been configured they will be stored using the same unit measurement throughout the system. The display unit will be the view unit to the default system of measurement. System of measurement can be configured per assets for objects in the group model. This will override the default system of measurement. Refer to System of Measurement.

Although it is possible to change Units within the system, careful consideration should be given before changing storage units e.g. kg to tonnes. Changing the storage unit will NOT trigger a recalculation and conversion of stored data.
Object Access

Object Access components can be configured to limit user access to specific assets such as network points. This feature prevents users from seeing specific objects anywhere in the system either in screens or on any dropdown menus. Object Access can be set up to filter any object types. This way the system can be configured to meet the needs of specific users or groups of users (i.e. roles).

Columns

The columns in the screens can be configured. New columns can be added and existing columns can be hidden from view. Screen labels and column sort orders can also be changed to meet your requirements.

Calculated Numbers

Columns containing calculated values are configurable and new ones can be added. These can be hidden in certain screens, yet still made visible and available in reporting views for use in reports.

Screen and Data Access

Screen and data access can be configured for each individual screen. The screen access is set up according to user roles, so that users can only see the screens that are relevant to their roles function. You can also control the type of access the user has within a screen.
The access levels defined in Energy Components are:

No access

	

Screen will be invisible for the users with this role




Read

	

Screen will be read only




Change

	

Only the 'Save' button will be activated in the screen where applicable




New

	

The 'Save' and 'New' buttons will be activated in the screen where applicable




Delete

	

The 'Save', 'New' and 'Delete' buttons will be activated in the screens where applicable




Edit on VERIFIED data

	

Access to change data with status VERIFIED




Edit on APPROVED data

	

Access to change data with status APPROVED

New Objects

New objects can quickly be added to the application using the configuration screens. As soon as the new object has been saved to Energy Components it is immediately available in the appropriate screens with no requirement for additional programming.

Audit Tracking

Energy Components automatically keeps a tracking journal of all data with a record status of 'VERIFIED' or higher. Again, this feature is configurable and can be changed to keep full information on all records with status of 'PROVISIONAL' or higher.

Check Rules

Each screen can have one or more Check Rules or validation hints applied to it. The Check Rules can be configured to automatically monitor the system for the correctness of data and can prompt the user to correct data and rerun processes if necessary.

Record Status Processes

System processes can be configured to run and update the record status automatically, or by manual intervention. These processes can be tailored to contain specific rules for each implementation project and customer. Access to these processes can be setup to prevent users from running unauthorized approval jobs, for example from V (Verified) to A (Approved), and thereby prevent data from being accidentally changed by users.

Language

The default language in Energy Components is English. However, the entire application can be configured to use the language of your choice. The language template is applied globally to Energy Components, but can also be configured and tailored for individual users so the system appears in their native language.


==========================================================================================
## [7/11] Calculation Framework
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/product_concept/calculation_framework.html
==========================================================================================
Calculation Framework
Introduction

The Calculation Framework in Energy Components is used to deploy client defined business logic applicable (in the form of process diagrams) for the business processes. The client can create process diagrams which may contain sub process diagrams, equation processes, Excel workbook processes and/or implemented calculation library processes, as they require. This unique feature allows specific process diagrams to be defined for each operation and applied in a consistent and controlled manner without the need for a compiler program. Each of the calculations are configurable - any changes can be added to the calculation process diagram which will then be applied consistently across the system.

The framework allows the user to build up and/or modify complex process diagrams containing sub process diagrams, equation processes, Excel workbook processes and/or implemented calculation library processes which influence the existing calculations. This is particularly useful when new assets are being added onto the system, enabling the user to manage varying calculations and scenarios. The framework has functionality allowing the user to make complex changes in a test environment before being launched in the live system - removing the risk of incorrect calculations entering the live system.

The framework can be used across most business functions including:

Hydrocarbon Accounting / Allocation calculations

Sales / Contract calculations

Price calculations

Cargo Scheduling

The Calculation Framework consists of two main components: the Calculation Definition Framework and the Calculation Execution Framework. The Calculation Definition Framework is used to create new and maintain existing calculation process diagrams. The Calculation Execution Framework reads and understands the calculation, which is created from the calculation editor and stored inside the database, and then executes it in the system.

The basic building elements for calculation process diagrams are attributes and variables. They refer directly to values already stored in the Energy Components database. Equations, sets and conditions combine attributes and variables with arithmetic and logical operators and functions. The equations then arithmetically deploy the calculation process diagram, and the sets define the group of objects that the equation relates to.

Figure 1. Calculation Framework Overview
Equation Editor

Equations are stored in the Energy Components database in MATHML format. MATHML is a form of XML (Extensible Mark-Up Language) designed for mathematic expressions. As illustrated below, MATHML comprises an editor, an interpreter and a MHT export function.

Calculations (process diagrams) are created using the Flowchart Editor found in the Maintain Calculation screen (as shown below). In the top half of the screen the user selects the date, calculation context and calculation.

Figure 2. Maintain Calculation - Process Diagram

The user can build iterations, conditions and equations using the Equation Editor.

Figure 3. Maintain Calculation - Equation Process

Calculations can be changed and are available immediately for execution without the need for programming or compiling code. The Equation Editor is a visual editor which provides tools for creating and editing equations conforming to the EC Calculation Syntax. A basic equation in the EC Calculation Syntax would have the variable or object components on the left hand side, and the arithmetic expression on the right hand side, as shown in the example given below in Equation Syntax 1:

An equation can also have an associated condition in the form of a logical expression, as shown in the example given below in Equation Syntax 2:

The equation given below sets the allocated daily net volume for all incoming oil streams (that are not fixed), equal to the measured daily stream volume, times the daily oil reconciliation factor:

The Stream Node Diagram

Within Energy Components, a Stream represents a flow from one point to another. An example would be a pipeline transporting gas. The points connecting a Stream are called Nodes. Examples of Nodes would be well, gathering station, platform, terminal. The main purpose of the Stream / Node concept is to model infrastructure and hydrocarbon flow. Further, to have a structure for applying quantities and calculations. The quantities are related to the Streams, e.g. a gas stream holding a quantity for the mass flowing for a certain period. The calculations are related to the Nodes, e.g. a calculation summarizing the quantities for two incoming gas streams and putting the result on the outgoing gas stream.

The Stream Node Diagram is used to show the structure of the production of oil and gas through pipelines and terminals. The visual representation is useful in situations where there is a large network, incorporating many streams and nodes (or network points and delivery points). The Stream Node Diagram is configurable using the Visualization Tool that’s provided alongside Energy Components. This means that any changes to the diagram can be made using the configuration screens and can be implemented immediately without the need for programming or system downtime. There are many functions that can be chosen from the context menu of the Stream Node Diagram: Auto layout, Edit Object, etc.

Figure 4. Stream Node Diagram Editor - Context Menu
Figure 5. Example of a Stream Node Diagram


==========================================================================================
## [8/11] Classes and Objects
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/product_concept/classes_and_objects.html
==========================================================================================
Classes and Objects

The EC system provides a large degree of flexibility to cater for different business scenarios. To be able to do this, the system has been designed with an abstraction view layer in the database that separates the business logic from the actual table structure used to store the data. This abstraction is defined as a set of what we call classes - very similar to the class concept used in object oriented design and programming languages.

This concept allows us to:

Have common functionality for data validation and integrity constraint without mixing it with the business logic

Choose to make some class attributes virtual (so that they are calculated when needed), or physically store them if needed without changing the table structure

Hide or show product attributes and also add customer class attributes if needed

Adjust and define the screen navigation model to be suitable for both small and larger operations

Control the properties of classes on several levels like packages, templates and project level. See section "Class Configuration Structure".

Enforce data protection with ringfencing and data locking

Support workflow operations, such as four eye approval and control point validation, as generic concepts that can be added to any class

Replicate some data for performance reasons without having the business layer writing special code for it

Change the table structure without interfering with the business logic

The class concept distinguishes between four different class types:

Object classes

Object classes are usually something static such as a physical object.

Typical Object classes are for example: Facility, Tank, Separator and Well.

Data classes

Data classes are typically owned by an object class, and represent a set of measurements or events linked to the owner object.

Daily tank volume readings and exported oil and gas volumes are very often part of a Data class.

Interface classes

Interface classes are abstractions over several object classes with a common subset of attributes.

They are used, among other things, for representing specific physical objects as nodes in a diagram showing how the hydrocarbons are passing through the system.

Table classes

Table classes are similar to data classes, but have less support for validation, row level security, etc.

A table class typically does not have an object owner or a timestamp as a part of the primary key.


==========================================================================================
## [9/11] Group model concept
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/product_concept/group_model_concept.html
==========================================================================================
Group model concept
Introduction

Information from a Group Model is used to populate the navigators on any screens that are configured to use the Group Model and therefore control what is viewed on the screen. Each different navigator represents a different Group Model. The Group Model is a hierarchical organisational structure of assets and classes within Energy Components, which again can be configured to meet the needs of the client.

There are parent and child relationships between objects. In the example below, the parent is the Production Unit; next in the structure is the area or field, and finally the child in the structure is the Production Facility i.e. the individual installation. There can only be one 'Parent' in a Group Model but there can be several interconnecting 'Child' relationships. The example below shows a full Group Model, where all areas in the structure link to the production unit.

In the example below the navigator is looking for information on a particular offshore facility. The structure of the Group Model used to populate this navigator is very simple. It contains the Production Unit at the top (which is the Parent) and the Offshore Area (which is a child object) and finally the specific Offshore Facility (which is also a child object). There are two predefined Group Models within Energy Components - Geographical and Operational. All other Group Models can be configured by the client to meet their requirements.

The Group Model screen is found in the configuration menu, under 'System'. You can view the class relations for a group type.

Figure 1. Group Model Configuration Screen


==========================================================================================
## [10/11] Users, Roles, Groups and Access Rights
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/product_concept/user_role_and_access_rights.html
==========================================================================================
Users, Roles, Groups and Access Rights

Users, groups and user’s role and group assignments are maintained in Keycloak or in dedicated EC business functions.

Roles and access rights are configured in Energy Components to control or limit which screens a user can view and control the users' ability to view, insert, update or delete data. These controls are enabled by assigning one or more roles to a user, then defining the level of access they will have within any screen.

Screens for maintaining roles, users and groups are found in the Tree View menu, under "Configuration" and then "Access".

Roles

Roles define the activities a particular business role can access – e.g. well tests, configuration etc. They also determine the level of access – e.g.: insert and update well tests, view well configurations, hide allocation configuration screens, etc.

Roles must exist in both EC and in Keycloak. The Role Maintenance screen can be used to synchronise the roles.

Partitioning

Partitioning defines the objects (e.g. fields, facilities, contracts, etc.) a role have access to. For example, an operator role for "platform A" can be restricted to only entering or viewing data for platform A.

Users

Keycloak is where individual users are created in the system and their access roles (one or more) allocated. Keycloak can use an LDAP user federation provider to federate users and user’s roles to Keycloak from a directory system such as LDAP or Active Directory.

Groups

User Groups in Energy Components can be defined as a meaningful collection of EC Roles that are combined to provide the required grants and permissions to serve a business function.

The type of EC Roles assigned to an EC Group will depend on the grants and permissions required by the business function that is being served.

The same individual EC Roles can be applied to multiple different groups as long as the assignment to the EC Group conforms to the desired grants and permissions access that the EC Group is trying to serve.

EC users can belong to multiple different groups, however traditional EC grants and permission levels still apply here with the highest level of access taking precedence over the lowest level.

The difference between EC Roles and EC Groups

EC Roles are a collection of grants and permissions i.e.(JBPM.ADMIN) that serve as part of a desired business function.

On their own EC Roles provide a small controlled window of grants and permissions, however if you want to provide users with grants and permissions to form a more comprehensive business function you would need to assign each EC Role individually.

EC Groups are a collection of one or more EC Roles combined under an EC Group to provide a more efficient method to assign EC Roles to a user instead of assigning roles individually.

EC Groups Advantages

Manage and maintain users more efficiently.

Assign user roles and access more efficiently.

Assign roles to users based on security groups a user belongs to inside of internal Identity Provider systems such as Microsoft Entra ID or other Active Directory (AD) providers.


==========================================================================================
## [11/11] Reporting concept
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/product_concept/reporting_concept.html
==========================================================================================
Reporting concept
Introduction

Energy Components contains a framework for reporting, supporting both product specific- and customer specific reports. The framework is designed to work with both internal reporting capabilities as well as 3rd party report tools.

The EC Product offers standard reports, delivered with the base product (e.g. Cargo documentation). Additional packages including reports for specific operations and geographical areas (e.g. Regulatory Reporting) can be installed in addition.

Customers can create their own reports, both ad-hoc and fixed reports. Most of the configuration is done through EC screens (see under 'Reporting' in the Tree View menu).

Fixed Reporting

The configuration of a fixed report in EC will include different elements based on type of report, and how it is to be used. However, all reports will need a report template, report definition and a report (also called report runnable).

A report template tells what 'system' to use for generating the report, and what parameters are needed. The report template represent one report artifact (pdf, excel etc.). There are currently five different Report Systems (report engines) to select from when creating a new report template:

Yellowfin

	

This system supports generation of reports based on Yellowfin reports. Creating reports using this is further described in How to use EC’s Reporting and Analytics. It is also possible to run JasperReports through Yellowfin.




EC Jasper Report

	

This system is deprecated in EC 13. This system supports generation of reports based on JasperReports. Creating reports using this report system is further described in How to create, install and configure a Jasper Report. A jasper report will usually be used to generate PDF, but other formats like Excel, CSV, etc. are supported.




EC Excel Report

	

EC has a system for configuration of Excel reports, with mapping of data between spreadsheet and the database. It can be used together with the calculation engine, as part of a calculation.

The formats xls and xlsx are supported.




External System

	

This system enables EC to handle reports generated by external systems. The reports (or documents) are created and stored on the external system. However, the execution of a report can be initiated from an EC screen, and the generated report is stored in the EC database and hence accessible from an EC screen.




EC Internal

	

This system is deprecated in EC 11, and is inactive by default (is set by the EC Code 'REPORT_SYSTEM'). It can still be used to generate jasper reports (in JasperReport version 3.1), but we recommend to update all jasper reports to use the EC Jasper Report system instead. EC Internal will still need to be used for reports that are based on gen_xml_report_db (See How to generate an XML-report based on a PL/SQL function)

Other report systems can be added by EC Packages (provided by Quorum Software as add-on to the core system) or by customer projects. Customer specific integration of any 3rd party reporting tool can be implemented. The only requirement is that the tool can connect to the Oracle database, and that there is a way for the system to interact with the tool.

A report definition will define the content of a report. A report definition can have one or several report templates attached. Values to be fixed for the report can be set here (cannot be changed when generating the report).

To be able to generate a report, a report (also called report runnable) needs to be created. A report will be connected to a report definition. Parameters not defined for the Report Definition can be set/modified here, before each generation of the report.

Ad-hoc Reporting

EC’s Reporting and Analytics (aka Yellowfin) can be used for ad-hoc reporting.

In addition, the screen 'Export to Excel Express' can be utilized for ad-hoc reporting. Any database view generated from an EC class can be used as basis for a report. Data can be filtered, and the user can select what columns to include.

Any external tool for Ad-hoc reporting can be set up to work against the EC database as well.

Workflow of Reporting

Configuration

	

Reports are configured through screens in EC. These are found under 'Reporting' in the Tree View. EC’s Reporting and Analytics or external tools like Excel and Jasper Report tool need to be used to create the report templates.




Generation

	

Reports can be generated through the 'Report Administration' screen. Some product screens will offer report generation as well (e.g. cargo documents). Scheduled tasks can be created for reports to be generated automatically at some time and frequency. Generation can also be added to a business process (BPM).




Search and View

	

Reports can be viewed/downloaded from 'Report Administration' screen. The screen also offers search on report parameters.




Distribute

	

Reports can be connected to messages configured in the EC Messaging System. By clicking the 'Send' button for a generated report, the report can e.g. be sent as email internally or to partners and government systems.




Publish

	

Generated reports can be registered as Published, so that they appear as published reports for a specific period. The 'Display Published Reports' screen will show the published reports.




Verify and Approve

	

A generated report will initially have the status Provisional. It can then be set to Verified and Approved. Users will need to have specific access to be able to approve reports.




Batch processing

	

The reports can be added to report sets to make it possible to generate, download and send reports in batch operations. This is done in the Report Set Administration screen.