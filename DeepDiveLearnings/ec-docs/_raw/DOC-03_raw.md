# Raw content — DOC-03
Modules: ['frmw/general-config']
Pages: 25



==========================================================================================
## [1/25] Calculation Library
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/calculation_library.html
==========================================================================================
Calculation Library
Introduction
Module applicability

This module introduces the Calculation Library functionality for EC calculations.

Intended audience:

Users that already know the basics of the EC calculation framework.

Version applicability:

The basis for this module is the EC11+ calculation engine.

Calculation libraries main principles (1)

One or more calculation steps can be extracted to a separate library calculation:

The library calculation is maintained independently from the main calculation.

The main calculation can «call» the library calculation by using a special step type.

Library calculations can be reused.

It can be called multiple times from the same calculation.

It can be called from different calculations (in the same calculation context).

Calculation libraries main principles (2)

Library calculations share some data structures with the calling calculation.

All global variables are shared.

Sets and iterators can be passed from the calling calculation to the library calculation.

Local variables can be shared between the calculations, and be used to pass data between them.

Library calculations are organized in calculation libraries.

Each library can include any number of library calculations.

A calculation can call library calculations from different libraries.

Library calculations can call other library calculations.

Library calculations can call other library calculations, both from the same and other libraries.

However, a library calculation cannot call itself, neither directly nor indirectly.

Typical use cases for calculation libraries

Avoiding multiple instances of commonly used calculations.

For example, some calculations apply fairly complex rounding rules at various points in the calculation.

Such rounding rules can then be extracted into a library calculation and reused.

This reduces maintenance efforts.

Using the same calculation steps for different periods.

For example, many monthly allocations include running a large part of the daily allocation for each day in the month.

The shared part of the daily allocation can then be extracted into a library calculation.

The daily allocation «main calculation» is then very simple and mainly consists of a call to the library calculation which implements most of the actual daily allocation logic.

Standardizing calculations across operations.

This could e.g. be relevant in a template approach, where parts of the calculation are predefined and other parts are operation specific.

The standardized parts could be extracted into library calculations.

Maintaining standardized calculations independently of the main calculation.

For example, regulatory reporting calculations can be put into a library that is maintained as a separate package.

It can be relevant on different levels, e.g. single operations, template approaches and also the EC product itself.

How does it work?
A simple example

Example:

The main calculation has three steps, M1, M2, and M3.

M3 has two sub-steps, M3.1 and M3.2

M2 and M3.1 are both calls to our library calculation.

Library calculation has two steps, L1 and L2.

Run-time execution flow

Example execution flow:

If we 
…[truncated]


==========================================================================================
## [2/25] Database Users and Logging
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/database_users_and_logging.html
==========================================================================================
Database Users and Logging
Introduction
What is this document about?

This document gives an overview of the predefined Oracle users that is used by the EC system, giving some background for the thoughts behind each of these, and outlining the journaling, logging, and audit possibilities built into the EC system.

Who will find this document useful?

System administrators and others that need to understand the EC database architecture and how the control and management around this can be set up.

What is not included in this document?

This document explains briefly or refers to several important concepts in an EC system without explaining them in detail, including 4 eyes approval, Row level security, Oracle journaling strategies and the EC architecture on the database and application side.

Versions/Applicability

The information presented here is based on the 11.2 release of the Energy Components. But the structure and architecture outlined here apply to all EC versions from EC 9.0 up to the current release.

Document Structure

This document explains the different Oracle users related to an EC operation and what they are used for.

EC operation database structure

An Oracle SID/Service can have several EC operations installed in parallel that operates completely independent from each other.
Each of these operations will have a set of Oracle users and roles that control the access to the database objects for the operation.
Each of these Oracle users is explained in detail in the following sections.

Oracle user	Purpose	Comments


ECKERNEL_<operation>

	

Owner of all the operations data tables, triggers, Views, PL/SQL code, etc.

	

Access to this user should be very limited since any direct login here will have full system access.




ENERGYX_<operation>

	

Intended as the access point for the EC application, and should not be used for other purposes.

	

This user is granted insert/update/delete/execute on selected objects from the ECkernel schema, but might not see all objects and rows. It should not have access to drop or change the core ECKERNEL objects with the exception of generated views/triggers based on class changes.




REPORTING_<operation>

	

User intended for use by 3rd party reporting tools. Should only be given read-only access to ECKERNEL reporting views. There might be login triggers or several different reporting users to control Ringfencing (Row Level Data access)

	


TRANSFER_<operation>

	

User intended for use in data capture/ECIS settings. Will typically be given write access to some data capture related data tables or staging tables

	


KCKERNEL_<operation>

	

Owner of all Keycloak related tables.

	

This user should only be used by the Keycloak system.




YFKERNEL_<operation>

	

User is intended to install Yellowfin configuration data.

	


ANALYTICS_<operation>

	

User is intended to be used by Yellowfin to connect to EC database.

	
ECKERNEL_<operation>

This is the Oracle schema that holds all the core database objects used by an EC system. You should only need to log in with the ECKERNEL user when you are installing, upgrading, or changing the objects owned by this schema.

Changes done in this setti
…[truncated]


==========================================================================================
## [3/25] How to change table content PINC logging in install mode
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_pinc_logging.html
==========================================================================================
How to change table content PINC logging in install mode

As part of the Product INtegrity Concept (PINC) in EC, there is a set of AP triggers that are actively logging changes during Install mode (When you install or upgrade EC). The idea is to log all configuration changes done during install and upgrade. As this logging is time-consuming and is using disk space, it is not desirable to do this for all the EC tables, so we want to limit it to some configuration tables and tables of special interest. How much of this logging you want to have active depends on the required audit level for your system, and might depend on:

How tight control you have on your configuration in a version control system.

Different needs between development, test, and production environments, etc.

Which tables that will have an AP_TRIGGER and do this kind of logging is determined by a flag PINC_TRIGGER_IND in the table CTRL_OBJECT.

The projects can turn on/off the PINC logging for a table by setting the PINC_TRIGGER_IND to Y (logging on) or N (logging off). If the PINC_TRIGGER_IND is null or there is no entry in CTRL_OBJECT for that table, then the trigger will be created as if the flag was set to Y.

As EC develops and new tables are added both in the product and in projects, the PINC logging settings in CTRL_OBJECT may need to be adjusted. For individual tables, if you turn on the logging you need to create a new AP trigger.

To do this:

Set pinc_trigger_ind to 'Y'

sql> UPDATE ctrl_object SET pinc_trigger_ind='Y' WHERE object_name='PROSTY_CODES';
sql> COMMIT;

Generate the AP trigger

sql> exec ecdp_generate.generate('PROSTY_CODES', ecdp_generate.AP_TRIGGERS);

If you want to turn off the logging:

Set pinc_trigger_ind to 'Y'

sql> UPDATE ctrl_object SET pinc_trigger_ind='N' WHERE object_name='PWEL_DAY_STATUS';
sql> COMMIT;

Remove the existing AP trigger

sql> drop trigger AP_PWEL_DAY_STATUS;
Calling sql> exec ecdp_generate.generate('PWEL_DAY_STATUS',ecdp_generate.AP_TRIGGERS); will not remove any existing AP trigger.

In some cases, typically in a development and Continuous Integration (CI) setting, you might want to turn off all the PINC logging of table changes to save time and space. In that case, assuming all the tables have entries in CTRL_OBJECT, do the following:

Execute the following query:

sql> UPDATE ctrl_object SET pinc_trigger_ind='N';
sql> COMMIT;

To delete the existing AP triggers (assuming that the project doesn’t have other types of triggers starting with 'AP_')

-- Create drop trigger statements

select 'drop trigger '||trigger_name||';'
from user_triggers t
join ctrl_object o on o.object_name = substr(t.trigger_name,4)
where substr(trigger_name,1,3) = 'AP_';

exec ecdp_generate.generate(null, ecdp_generate.AP_TRIGGERS);

The result can either be spooled to a file and run in again in sql*plus, or copied out from the result grid if you are using another SQL tool.

If the PINC table content logging is turned off, we lose some of the trace possibilities to detect changes done in the system and upgrade tools like the pre-check.

The methods described here are intended for development environments and settings where it is safe to do this kind
…[truncated]


==========================================================================================
## [4/25] How to configure a Business Action to call SQL procedure
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_config_business_action_sql_procedure.html
==========================================================================================
How to configure a Business Action to call SQL procedure

This document describes how to set up a Business Action with a call to an SQL procedure.

Introduction

EC has two business action for calling an SQL procedure

Business Action	Description


com.ec.eccommon.genericmodel.model.ejb.GenericScheduledSqlAction

	

Static parameter SQL_XML specify an XML file with the SQL procedure call. The XML file can use parameters from the business action.




com.ec.eccommon.genericmodel.model.ejb.GenericRunSqlAction

	

Parameters specify the SQL procedure call and parameters to the call. The parameters are prefixed with procedure.

Date parameters can use macro to get a value based on actual or scheduled time. Refer to How to use Date Macro Parameter.
GenericScheduledSqlAction
Business Action screen

Static Business Action parameter is configured with the name SQL_XML and the URL of the XML file as the value. Additional Business Action parameters can be added as needed.

Example XML file:
$<parameter name>$ is used in the XML file to refer to Business Action parameters.

<data>
<sql type="procedure">ec_bs_instantiate.i_initiate_day(to_date($START_DATE$, 'YYYY-MM-DD"T"HH24:MI:SS'), to_date($END_DATE$, 'YYYY-MM-DD"T"HH24:MI:SS'))</sql>
</data>

The XML file can be in an EC Extensions. When extension id = EX010 and XML file my_sql_action.xml is in folder src\main\webapp\com.ec.mycompany.action, the url to the XML file is /extension/EX010/com.ec.mycompany.action/my_sql_action.xml

For example on how to create extensions, see the Energy Components Software Development Kit (EC-SDK) - /energycomponents-sdk/examples/extensions.

Schedules screen

On tab BUSINESS ACTION, after inserting the business action, any additional parameters can be filled out.

GenericRunSqlAction

In EC-10.4-SP06 and EC-11.1-SP02, the GenericRunSqlAction has been rewritten due to security constraints. To avoid possible security attacks, the usage of GenericRunSqlAction has been restricted. This is intentional. This means that a Business Action with sql as a parameter and the procedure call as value, will not work in EC-11.1-SP02+. This section describes the differences in the configuration in Business Action between pre and post EC-11.1-SP02 using the GenericRunSqlAction.

Example case

A schedule running a Business Action calling an SQL procedure in an EC package. The procedure to be called in the Business Action is ec_bs_instantiate.i_initiate_day , which takes 2 arguments. The declaration of the procedure is shown below:


PROCEDURE i_initiate_day(p_daytime DATE,
                         p_to_daytime DATE DEFAULT NULL);
Old solution
Business Action screen

In this case, a Business Action parameter is configured with sql as a name. Type is Basic Type, sub type is String.

Schedules screen

On tab BUSINESS ACTION, the value for the sql parameter is the actual sql call to the procedure:

call ec_bs_instantiate.i_initiate_day('28-JUN-2021', '29-JUN-2021');

New solution

In the new solution it is no longer possible to insert the sql directly. Instead we have to declare the following Business Action parameters:

procedure.name

procedure.type

procedure.arg1

procedure.arg1.type

etc.

…[truncated]


==========================================================================================
## [5/25] How to use Date Macro Parameter
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_use_date_macro.html
==========================================================================================
How to use Date Macro Parameter
When to use Date Macro?

Date macros are used when there is a need to replace static date parameter values with dynamic values. This means that there is no need for users to change the parameter values manually; the system will change it accordingly. Date macro parameter values can be defined to follow scheduled firing time or actual firing time. Additional macros (various periods such as 'Yesterday', 'Tomorrow', 'Minus 1 Hour', 'Plus 1 Hour', etc) can be used to calculate the actual date parameter value.

Steps to use Date Macro

The first step is to set up a parameter in the "Business Actions" screen to have the DATE_MACRO as its type. Refer to the screenshot below.

Figure 1. Configure DATE_MACRO type in Business Actions screen

Next, fill in the macro in the "Schedules" screen. Refer to the screenshot below.

Figure 2. Configure macro in Schedules screen

Here we have selected the symbolic time "Schedule Time" as the starting point.

Then we have added two macros on top of this. The first one is the "Yesterday" macro and the second one is the "Minus 1 Hour" macro.

Example:

The schedule fires on "2014-12-09T12:00". Based on the macro setting the system will calculate the value of parameter startDate="2014-12-09T12:00". Refer to the screenshot below.

Figure 3. Configure schedule timing in Schedules screen

If we selected the symbolic time "Actual Time" and if the job was actually triggered at "2014-12-09T12:03" because of the server being busy, then the value of parameter startDate="2014-12-09T12:03". Refer to the screenshot below.

Figure 4. Configure Actual Time schedule timing in Schedules screen
Macro Sequence Number Validation

When entering the sequence number, ensure that the number is entered correctly. This is to inform the system of the correct sequence of the calculations for date parameter values. Upon clicking the save icon, an error message - "Record already exists" - will appear when the same sequence number is entered. Refer to the screenshot below.

Figure 5. Check the correct sequence number
List of Date Macros

The following is a list of date macros that can be used with the DATE_MACRO parameter.

Example: Date=05-OCT-2006 Time=10.30 AM

Macro Name	Example Parameter Value


First of Last Year

	

01-JAN-2005 10.30 AM




First of Month

	

01-OCT-2006 10.30 AM




First of Next Month

	

01-NOV-2006 10.30 AM




First of Next Year

	

01-JAN-2007 10.30 AM




First of Prev Month

	

01-SEP-2006 10.30 AM




First of Year

	

01-JAN-2006 10.30 AM




Last of Month

	

31-OCT-2006 10.30 AM




Last of Next Month

	

30-NOV-2006 10.30 AM




Last of Prev Month

	

30-SEP-2006 10.30 AM




Last of Year

	

31-DEC-2006 10.30 AM




Next Year

	

05-OCT-2007 10.30 AM




Tomorrow

	

06-OCT-2006 10.30 AM




Yesterday

	

04-OCT-2006 10.30 AM




Noon

	

05-OCT-2006 12.00 PM




Plus 1 Hour

	

05-OCT-2006 11.30 AM




Minus 1 Hour

	

05-OCT-2006 09.30 AM




Midnight

	

05-OCT-2006 12.00 AM


==========================================================================================
## [6/25] How to resolve blocked schedules automatically
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_resolve_blocked_schedule.html
==========================================================================================
How to resolve blocked schedules automatically
Introduction

To have blocked schedules are in most cases ok and normal. That just means it’s waiting for the currently running job to complete. There are some cases where the scheduler thinks a job is running when it’s not. If the database becomes unavailable while the application server is running, the status of a completed job fails to be updated. Hence, when the database comes back up the status will still be running and the schedule has a false block.

The scheduler has an API that has to be used. Updating the database directly is not the correct way and will cause unexpected behavior. There is a schedule that checks if there are any running jobs that are blocked and unblocks them if that is the case.

Note that there are some jobs that are scheduled at one specific time and others that are repeatable, but it does not matter if executions are skipped. A morning report or instantiation of data is something that you want to do even if the server was offline at the scheduled time. Polling an interface will typically recover even if the jobs have not been fired during maintenance etc. Hence, for the polling jobs, the ignore misfired option should be set to prevent all non-executed jobs to fire when the server is running again. If this is not set it will try to run all schedules not executed while the server was down.

If the jobs are still blocked it should be investigated why the job is running and not completing.

Scheduling the job releasing the blocked jobs

Find the predefined schedule named "ReleaseFalseBlockingJobs" and schedule it to run at a given interval as below.

Go to the job details, set the run as user and make sure it has Ignore Misfires set and Stateful not set. Save if any modifications.

Enable the job.

In the example above, the job has been scheduled to unblock jobs having a wrong status.


==========================================================================================
## [7/25] How to re-pin scheduled jobs
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_re_pin_scheduled_job.html
==========================================================================================
How to re-pin scheduled jobs
Introduction

The re-pinning of scheduled jobs is not usually required. Since scheduled jobs are pinned to either a cluster or a server the scheduled jobs will not automatically be transferred to another cluster or server. If one server needs maintenance it can be taken out of the cluster for a while and the remaining servers will handle the scheduled jobs. However, if it is a standalone server the scheduled jobs have to be pinned to another server. Several users have done this by updating the status in the database directly or via a custom button. The scheduler keeps the state of running jobs in memory and updating directly in the database does not work. Typically, this is not discovered in the test environment due to frequent restarts of the test servers hiding that the job is not pinned to other servers before restarting the server. This can also lead to schedules becoming blocked instead of pinned to the new server as intended.

Hence there is provided a button for re-pinning in the correct way. The button is hidden by default and can be enabled as described below.

Give Access To Role

To enable the button, grant access to the intended roles.

Re-pin schedules in Schedules screen

Re-pinning is done in the Schedules screen. It will re-pin the schedules that are enabled and pinned to other servers. To see which jobs will be affected, filter on the enabled jobs only.

The jobs can be pinned to the server currently serving the screen by clicking the "REPIN JOBS" button. The other server should be shut down gracefully so that already running jobs can complete.


==========================================================================================
## [8/25] How to define check rules
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_define_check_rules.html
==========================================================================================
How to define check rules
Introduction

This document describes how to set up Check Rules. Check rules can be used to validate data in the EC database. The check rules are run as a database job and the results are stored in a log table (CTRL_CHECK_LOG). The check rules can be run from the Validation Overview (CO.0203), Validation Overview by Facility (CO.0204), from the Validation tab to the screens or as a scheduled job. The result can be viewed in the Validation tab on the screens.

When defining a check rule, the goal is to create a SELECT statements with a WHERE condition that return a row when the validation fails. Check rules can either use a WHERE formula to specify the validation, or use the validation rules configured in Class Validation (CO.1031) and Hierarchical Object Validation (CO.0253) or Object Validation - Default (CO.1032.01). Class and Object validation can be used for simpler validation like checking for missing values and checking if values are between min and max boundaries.

Access to the Check Rules screen could be disabled. To get access to the screen, open the Object Maintenance screen and give proper access level to the relevant roles.
Object Name: /com.ec.frmw.co.screens/maintain_check_rules
Description: Check Rule
Check rule - Where formula

The WHERE condition to the check rule is specified as a formula. The formula can use:

Keywords (AND, OR, IS NULL, IS NOT NULL, IN, LIKE, NULL, NOT, NVL, COALESCE, SUBSTR, LENGTH, ROUND, TRUNC, COUNT, MAX, MIN, ABS, GREATEST, LEAST, SYSDATE, DECODE, BETWEEN, CASE, WHEN, THEN, ELSE, END, EXISTS, ADD_MONTHS, LAST_DAY)

Special characters (<, ⇐, =, ⇒, >, <>, !=, ( ,) )

Numbers

Variables defined as $\{variable name}

A variable can be:

Constant (free text, can not contain ";"). Constant will be bind parameter to the query.

Attribute from the RV view

Function call (call to a function in a package)

Sub query (only sub query from one view is supported)

Variables are automatically created when the WHERE formula is stored in the database. It is not possible to manually add variables.

Function call

A function call can be used to get the previous value, a reference value, call a customised validation function, etc. It is only possible to call a function from:

EC packages of classes that are included in validation (i.e. classes with "Include in Validation" = Y).

EC packages of the following classes: ECBP_WELL_THEORETICAL, ECBP_STREAM_FLUID, EC_WELL_REFERENCE_VALUE, EC_STRM_REFERENCE_VALUE.

Packages starting with Z (custom defined packages).

Packages configured in EC codes with Code Type 'CHECK_RULE_PACKAGE'. Use the Code attribute to specify package name in all uppercase.

First is the package selected and then the function. When the function is selected and stored in the database, the parameter list to the function is created and the user can fill out the values. The parameter can be a constant or an attribute from the RV view. For Date parameters a date and hour offset can be specified.

Example: Get the measured oil rate to the previous day to the well: ec_pwel_day_status.avg_oil_rate(object_id, (daytime - 1), '=')

Sub query

A sub query can be used to check the number of
…[truncated]


==========================================================================================
## [9/25] How to configure Tab Label in EC Screens
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_configure_tab_label.html
==========================================================================================
How to configure Tab Label in EC Screens

Tab labels can be overridden using EC system settings. This is available since EC-12.2.8.

The system setting property key must have the following format:

<screen url>/<tab screenlet id>/TabItemService/label

<screen url> is the URL to the screen. It can be found in the online help under Business Function Url.

<tab screenlet id> is the ID to the tab screenlet. It can be found in the screen XHTML by searching for tabScreenlet id.

For example, for Forecast Manager - Schedule tab (CP.0068) the property key value should be:

/com.ec.tran.cp.screens/fcst_manager/tab3/TabItemService/label

If there’s a system setting property present for a tab, it will override the hard-coded tab label in the screen XHTML.

The following steps are an example of how to configure a tab label for the Forecast Manager screen:

In the screenshot of the Forecast Manager screen below we can see that the tab label for tab 3 is "SCHEDULE", which is hard-coded in the XHTML.

Label hard-coded in the screen XHTML:

<ect:tabScreenlet id="tab3" label="Schedule">
<ect:screenletConfig energyx-version="3" screenXmlConversion="11.1.SP01-SNAPSHOT$2016-02-03T06:03:28">
<service class="com.ec.frmw.jsf.service.TabItemService"/>

In the screen:

To configure the tab label, we can add the system property from the Create Preference screen as shown below.

Then go to the Maintain System Settings screen and filter on the "Tab Label - Forecast Manager - Schedule Tab".

Add a new system setting property value (e.g. "test label") and save it.

Go back to the Forecast Manager screen and refresh it. The new configured label "TEST LABEL" should appear for tab 3.


==========================================================================================
## [10/25] How to configure Context Menu
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_configure_context_menu.html
==========================================================================================
How to configure Context Menu
Introduction

A context menu is a menu that will appear on the screen when the user performs a right click on a screenlet (table/form). This allows the user to perform actions connected to data in the screenlet.

When a screenlet is set to have a context menu, this will override the browser’s standard right-click menu. For screenlets not configured with a context menu, the standard menu will appear when right-clicking.

The context menu can consist of a number of menu items, each representing a different action. The menu items can have sub items. An action could be to open a new browser window with a content limited by the underlying data, change the underlying data, perform a calculation based on the underlying data or similar. The screenshot below shows a context menu in the Maintain Calculation screen.

Access to the different menu items depends on:

The access level for the user.

The number of rows selected.

The data content in the row(s).

Based on the combination of these factors, menu items will be enabled/disabled and visible/hidden. It is possible to add separator lines to group items on the menu. Press the Ctrl key in combination with mouse-click to multi-select rows in tables with multi-selection enabled. The context menu supports the multilingual features implemented in the framework.

There are two different ways of adding a context menu to a screenlet:

Configuration using XML.

Configuration using database entries.

For project specific context menus, the database approach would normally be the preferred one.

Configuration using XML

To configure a screenlet to utilize the context menu feature using XML, there are normally two or three steps to follow:

Define a menu XML file or a model that generates an XML file.

Add support for rendering of the context menu in screenlet/XHTML.

Add actions to be performed when executing an item (service/listener). This is optional.

Structure of the Menu XML

Here is a dummy example of a menu XML for a context menu, giving most of the usage capabilities of this service:

A menu with a set of items which contains conditions and a action

<?xml version="1.0" encoding="UTF-8"?>
<menu title="Options">
    <item id="disable_ec_code" text="Disable EC CODE" mouseover="Sets the disabled flag for selected rows">
        <conditions>
            <objectAccess threshold="60">/com.ec.screens.test_connection/disable_ec_code</objectAccess>
            <function message="This operation can only be performed on one or two rows." show="hidden">validateSelectedRowCount(1,2)</function>
            <function message="This operation can only be performed on codes of type GAS_FLARE or GAS_PROD" show="disabled">fieldvalue("CODE")=="GAS_FLARE" || fieldvalue("CODE")=="GAS_PROD"</function    >
        </conditions>
        <action>
            <arg name="confirm" value="Do you want to disable EC CODE(s)?"/>
            <arg name="send" value="DisableECCode"/>
            <arg name="target" value="this.component"/>
        </action>
    </item>

    <item id="disable_ec_code_2" text="View EC CODE status flag" mouseover="Displays the diabled flag for selected rows - accesslevel 10">
   
…[truncated]


==========================================================================================
## [11/25] How to configure EC Dashboards
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_configure_dashboard.html
==========================================================================================
How to configure EC Dashboards
Introduction

This document describes how to create (configure) new Widgets so they become available for the end-users in theEC Dashboard screen.

Database configuration

All widgets made available for end-users must be configured in two tables in the EC database.

First, a new Widget must be defined as a new row in CTRL_DASHBOARD. This table describes key attributes of a widget, like a label and the type of widget to use.

Second, any configuration parameters must be added to the table CTRL_DASHBOARD_PARAM. Different widgets have a different set of possible configuration parameters that can be used to change how the widget retrieves data, how the widget display data, and so on.

Example

As an example we will create a new Widget called_Oracle Version_ that displays the Oracle database version number. It will look something like this:

First we need to insert a new row into the database table CTRL_DASHBOARD. In this table each row represents one widget. Here we define the name of the Widget and also the widget type (WIDGET_CLASS). We use_BigWidget_in this example:

CTRL_DASHBOARD

WIDGET_CODE	CATEGORY	NAME	LABEL	DESCRIPTION	WIDGET_CLASS


ORACLEVERSION

		

OracleVersion

	

Oracle Version

	

Display the Oracle Database version number.

	

com.ec.frmw.jsf.dashboard.wg.BigWidget

The_BigWidget_needs some configuration parameters to be able to retrieve and display data. In this example we use 3 parameters:*QUERY,__footer*and*text*.

The*QUERY*parameter contains the actual SQL query that the widget will run.

The*footer*parameter contains a literal text that will be displayed as a footer.

The*text*parameter contains a DATAMODEL expression that will be resolved after the widget has retrieved data. The expression 'EcDatamodel.row[0].col[VERSION].datavalue' means: look up the_datavalue_attribute in the_ECDatamodel_on_row 0_for the_VERSION_column.

CTRL_DASHBOARD_PARAM

WIDGET_CODE	NAME	LABEL	RESOLVE_ TYPE	PARAMETER_ TYPE	PARAMETER_ SUB_TYPE	PARAMETER_VALUE


ORACLEVERSION

	

QUERY

					
<renderer>
  <model class="com.ec.eccommon.genericmodel.model.web.GenericSqlModel">
   <arg name="sqlXml" value="data" valuetype="subXml">
     <data>
       <sql>SELECT VERSION FROM PRODUCT_COMPONENT_VERSION WHERE product like 'Oracle Database%'</sql>
     </data>
   </arg>
  </model>
</renderer>



ORACLEVERSION

	

footer

					

Oracle Version




ORACLEVERSION

	

text

		

DATAMODEL

			

EcDatamodel.row[0].col[VERSION].datavalue

The QUERY Parameter

The QUERY parameter is an important parameter used in many of the widgets. It is responsible for doing the actual retrieval of data for the widget.

This parameter has to contain a <renderer> element just like in screen xml’s, and therenderer element must contain a model element and may contain transformer elements as needed.

Placeholders enclosed in $ will be replaced with the parameter of the same name.

For example $FROMDATE$ will be replaced with the value of the FROMDATE parameter.

Example using GenericDaoModel:
<?xml version="1.0" encoding="utf-8"?>
<renderer>
    <model class="com.ec.eccommon.genericmodel.model.web.GenericDaoModel">
        <arg name="daoQueryXml" value
…[truncated]


==========================================================================================
## [12/25] How to Configure the Application Title Bar
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_configure_title_bar.html
==========================================================================================
How to Configure the Application Title Bar

The title bar is the topmost section of the application window. By default it looks like this:

Several aspects of the title bar can be customized.

Background: The title bar background can be customized to display colors based on environment and screen groups.

Image: A custom image can be added next to the Energy Components logo.

Label: A textual label can be added next to the images.

Background

The visual style of the title bar background is customizable. This can be used to distinguish different EC instances visually. The background styling has support for dynamic color adjustments based on environment and screen groups.

To customize the title bar background:

Open the Maintain System Settings screen.

Navigate to the Custom Settings category.

Find the Application Title Bar Background property.

Create a new property value and enter the background style as the value.

Refresh the screen to see the change. You may have to flush cache to make the changes take effect.

Background Style Format

The background style must be a valid CSS background property value. You can specify anything from solid colors to gradients and more.

Logos and text above the background should remain visible and readable in both the light and the dark theme.

Window width can affect the appearance of the background. Test your style with different browser window sizes.

Examples of basic background styles:

Solid color.
palegoldenrod


Single color gradient.
linear-gradient(45deg, transparent, palegreen 25% 45%, transparent 80%)


Two color gradient.
linear-gradient(45deg, transparent, palegreen 25% 45%, cyan 55% 70%, transparent)


Background Style Placeholders

Placeholders can be used to dynamically inject environment and screen group specific colors into the background value. The title bar will then look different based on which environment you are logged into and the screen group of the screen you are viewing.

Placeholder syntax:

${ENVIRONMENT} to insert current environment color here.

${ENVIRONMENT:<CSS color value>} to insert current environment color here, with fallback to hardcoded color value.

${ENVIRONMENT:SCREEN_GROUP:<CSS color value>} to insert current environment color here, with fallback to current screen group color, with final fallback to hardcoded color.

${SCREEN_GROUP} to insert current screen group color here.

${SCREEN_GROUP:<CSS color value>} to insert current screen group color here, with fallback to hardcoded color value.

${SCREEN_GROUP:ENVIRONMENT:<CSS color value>} to insert current screen group color here, with fallback to current environment color, with final fallback to hardcoded color.

If a placeholder is used but no color can be resolved, EC will use transparent as the fallback color.

Examples of background styles using placeholders:

${ENVIRONMENT}

${ENVIRONMENT:lightgreen}

${ENVIRONMENT:SCREEN_GROUP:lightgreen}

${SCREEN_GROUP}

${SCREEN_GROUP:lightblue}

${SCREEN_GROUP:ENVIRONMENT:lightblue}

linear-gradient(45deg, transparent, ${ENVIRONMENT} 25% 45%, transparent 80%)

linear-gradient(45deg, transparent, ${ENVIRONMENT:blue} 25% 45%, transparent 80%)

linear-gradient(45deg, pa
…[truncated]


==========================================================================================
## [13/25] How to Configure Table Column Sets
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_configure_table_column_sets.html
==========================================================================================
How to Configure Table Column Sets

Table column sets is a way to reduce the number of columns visible in tables. It’s useful for tables where the number of columns is so large that the table doesn’t fit in the screen, forcing you to scroll horizontally to see the rightmost columns.

Usage

When column sets are configured, a row of radio buttons appear in the table, one button per column set.

Selecting a column set hides all columns that are not included in that set.

You can switch between column sets while editing the table without having to save changes first.

Column sets are also available from the table popup menu.

A checkmark marks the currently selected column set.

If you don’t like having buttons in the table, you can hide the column set buttons by setting the Personal Setting called Hide Table Column Set Buttons to true. When the buttons are hidden you can still use the table menu to select column sets.

Configuration

Column sets are defined in EC class configuration as a STATIC_PRESENTATION class attribute property called viewcolsets. The value of the property is a comma-separated list of column set names. viewcolsets can optionally also be added as an APPLICATION class property on the class itself.

Class attribute property

viewcolsets as a class attribute property defines which column sets this attribute is included in. The attribute will only be visible as a column in the table when one of the listed column sets is selected.

In the below example the OBJECT_ID attribute on PWEL_DAY_STATUS, displayed as the Well Name column in the table, are included in three column sets: Choke, Theor. Calc and Well Head.

If viewcolsets is only defined on class attributes and not on the class itself, the table will display one button for each unique column set name found on all class attributes, sorted alphabetically by column set name. In addition an All set is automatically added as the first button if it’s not already defined in the configuration. The All set displays all table columns, including those that do not have a viewcolsets property defined.

Class property (optional)

If you want to specify the ordering and visibility of the column set buttons yourself, add viewcolsets as a class property.

When viewcolsets is defined on the class, only the column sets that are listed in the class property value will be visible in the table, and the buttons will be displayed in the listed order. In this case, the All set is not automatically added, but you can include it in the list yourself.

In the below example only the Well Head and Choke column sets will be visible in the table, regardless of what other column sets might be defined on the individual class attributes.


==========================================================================================
## [14/25] Time Zone Support in Energy Components
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/timezone_support_in_ec.html
==========================================================================================
Time Zone Support in Energy Components
Introduction

This document describes the time zone handling implementation in Energy Components. EC supports multiple time zones within the same system through production day and time zone configuration.

What is this document About?

This document provides an overview of time zone handling in EC, including: * Multiple time zone support via production day configuration * Dual timestamp storage model (local time with DST flag and UTC time) * Configuration of time zones at EC data model, object classes, and production day levels * Known limitations and restrictions

Who will find this document useful?

This document is intended for: * Database developers working with EC time zone functionality * Technical consultants configuring multiple time zones * Project teams implementing EC solutions with multi-timezone requirements

What is not included in this document?

This document does not explain the key EC concept in detail, it assumes that the user has a relatively good understanding of the underlying principles for tables, classes, configuration structures, production day etc.

Background

Support for several time zones has been a wish from customers for many years. EC has had a partly solution tied to production day, and several configuration elements spread around to control daylight saving, available time zones etc.

The time zone framework uses Oracle’s built-in time zone database, which automatically handles DST transitions and historical time zone changes. This eliminates the need for manual DST configuration.

This document outlines how several time zones are supported within the same EC system, design choices made, how it is implemented, challenges and limitations.

Data Model
Daytime Column

The EC data model consists of over 2900 tables, almost 1800 of these have a DAYTIME column. This is currently in most cases representing the single local time zone as defined in the T_PREFERENCE table.

A typical transactional table for sub-daily data in EC could look something like this:

There is a Daytime column of data type DATE (Equal to DAYTIME in other DB systems)

Because of daylight saving and the overlapping hour in the autumn, there is an additional column called SUMMER_TIME to separate the records when there is overlapping local timestamps. This is usually part of the Primary key for sub-daily data or event tables.

Many sub-daily tables have an additional replicated PRODUCTION_DAY column, to simplify aggregation and reporting on day level.

Several tables also have an END_DATE column to represent the end of events or periods.

In the current EC system, DAYTIME is representing a Production Day and not a timestamp in most of the tables, there are several hundred cases where DAYTIME is a timestamp, and then there are also quite a few tables where the interpretation of the DAYTIME column might depend on the time scope code of the classes mapping towards the physical tables.

When introducing support for several time zones, it is only the tables that can hold sub-daily data that is adjusted to be time zone aware. This is done to keep the refactoring of generic code, naming conventions etc. at a minimum
…[truncated]


==========================================================================================
## [15/25] Deprecating Ecdp_ProductionDay
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/deprecated_Ecdp_ProductionDay.html
==========================================================================================
Deprecating Ecdp_ProductionDay
Background

The document describe the effect of removal of Ecdp_ProductionDay and Ecdp_ContractDay.

Ecdp_ContractDay is a simple wrapper to Ecdp_ProductionDay and the effect of its removal does not affect much compared to Ecdp_ProductionDay.

The package Ecdp_ProductionDay responsibilities are now moved to a group of timezone related packages since EC-12.2. As of 13.2.0, the package is just a façade to the actual functions in Ecdp_Timestamp* functions, except a couple of auxiliary functions, getProductionDayFraction and other functions that are easier to run than relying on the package. EC-13.2.2 introduces class METER_FREQUENCY to replace last function in the Ecdp_Productionday. EC-13.2.3 removes all references to the package in product code base and move the calls to Ecdp_Productionday with its' replacement. The package is expected to be completely removed in future major releases.

Existing Functions and it’s Replacements

Note: Class name is no longer valid for any of the functions. Object is unique; objects_table and objects_version_table is sufficient to identify the specific objects.

Original proc/func	New call


findProductionDayDefinition(p_class_name, p_object_id, p_daytime)

	

Ecdp_Timestamp.getProductionDayId(p_object_id, p_production_day)




findSubDailyFreq(p_class_name, p_object_id, p_daytime)

	

N/A, use Ecdp_Timestamp_Utils.getMeterFrequency




getProductionDayFraction(p_class_name, p_object_id, p_day, p_from_daytime, p_from_summer_time, p_to_daytime, p_to_summer_time)

	

Ecdp_Timestamp_Local.getProductionDayFraction(p_object_id, p_day, p_from_daytime, p_to_daytime)




getProductionDayOffset(p_class_name, p_object_id, p_daytime, p_summertime)

	

Ecdp_Timestamp_Local.getProductionDayOffset(p_object_id, p_production_day)




getProductionDayStart(p_class_name, p_object_id, p_day)

	

Ecdp_Timestamp_Local.getProductionDayStart(p_object_id, p_production_day)




getProductionDay(p_class_name, p_object_id, p_daytime, p_summertime)

	

Ecdp_Timestamp_Local.getProductionDay(p_object_id, p_timestamp_local)

Effects on summer time

It is important to note that any of the summer time parameters in Ecdp_Productionday is ignored and does not affect any of the functions. This may affect date with switching summer time. The actual functions in Ecdp_Timestamp handles summer time correctly - refer to Ecdp_Timestamp.local2utc to find the correct way to deal with summer time switch.

Detailed design inspect the summer time effects on each applicable functions.

Terminologies

PRODUCTION_DAY/DAY - defined a date, without time components and without time zone awareness.

Daytime - a local date. The time zone information is carried by the object when a query is performed. Otherwise it is defined by the default time zone.

Utc_daytime - a date at UTC.

Summertime flag - defined in Ecdp_Productionday and ancient Ecdp_Date_Time, to identify the hour during DST switch to winter. EC Pre-12.1 choose next hour for invalid date and first hour during DST switches. 12.1 and above use default database behavior i.e. throw 0RA-1878 during invalid hour and 2nd hour during duplicated hour. In effect, the current Ecpd_Prod
…[truncated]


==========================================================================================
## [16/25] How to configure language translation in EC
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_configure_language_translation.html
==========================================================================================
How to configure language translation in EC
Introduction

Energy Components support language translation in the application. It’s capable of translating the texts which are not defined as "user data". More specifically, the following items can be translated:

Screen name in the tree view

GUI labels (Search, Favorites, Menu, screen label, sum, etc..)

Items in system menus (table menu, the menu for HELP & ABOUT)

Button captions and tooltips

Screen component labels (table labels, form labels, tab labels…​)

Table column name (normally defined by the CLASS attribute label)

Form attribute labels

Verification status texts

System notification messages

The EC application is by default in English. The translation looks up the text mapping for a given target language and translates the source text into target text for a specific language. Below are the basic tables involved for language translation:

T_BASIS_LANGUAGE (Store all languages)

T_BASIS_LANGUAGE_SOURCE (Store the source text)

T_BASIS_LANGUAGE_TARGET(Store the target text for a specific language)

This document describes the basic steps for configuring language translation through the EC front end.

Step-by-step guide
1. Define the target language if it’s not in the system yet.

Go to the Language (CO.1023) screen, and check the predefined languages. If your target language for translation is not listed, insert it through this screen.

2. Define the Source and Target text translation for a given target language.

Prepare the translation list with source and target text for a given language. This will be the input for configuring text translation within EC.

Based on your translation list, go to the Text Translation (CO.1024) screen where you can define the Source and Target text for the selected language. Screen and navigator usage can be found in the HELP page for the Text Translation screen.

The example below contains a few text translation mappings for Norwegian (NO). This configuration will be used as an example in later steps.

3. Define the language in Regional Settings through the Maintain User Settings screen.

By default, all EC users have the EC_Default user with EN as language. A given user or role can be configured to have a different language. In the example, we have defined the language for the "sysadmin" user to be Norwegian (NO). When "sysadmin" logs into EC, the system should be translated according to the text translation for Norwegian (NO).

4. Check the translated system after all the configuration is finished.

After the configuration is done, text translation should in most cases take effect after the next screen refresh. If not, flush cache and translation will take effect afterward. Below is a demo of the Daily Production Well Status 1 screen with some screen elements translated.

Before the translation.

After the translation. The translated elements are highlighted with YELLOW.

Bonus Step (Back End) - Translate Drop Downs.

Some dropdowns in EC have dynamic property types. In order to have the values of these translated, in addition to the previous steps you also need to make a simple change to the DYNAMIC_TYPE_POPUP class. The class attribute property: vi
…[truncated]


==========================================================================================
## [17/25] How to configure Messaging
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_configure_messaging.html
==========================================================================================
How to configure Messaging
Introduction

This section describes the Message Handling Module in the Energy Components (EC). It describes the module at a sufficient level of detail to gain an understanding of the actual implementation of the system.

The flow of messages and their statuses seen from EC are presented.

The interface between EC and the message broker has been tightly coupled in the past. Now, this coupling is loose, but the implementing projects are responsible for the message broker.

Business Context

This chapter contains an overview of the Message Handling Module (EC MHM) and the interface to the message broker.

MHM - Architecture Overview

The following figure illustrates the functionality in the messaging software:

Figure 1. Overview of the interface between EC and the message broker

The parts that constitute the messaging are:

The message broker.

The EC specific extensions to the message broker.

The EC MHM adapter handling all interactions with the message broker.

A set of screens in EC covering required end-user functionality using data from both EC and the message broker with extensions.

All messages sent from EC to the message broker are routed through the EC MHM adapter, which transfers the messages to the message broker. Incoming messages are fetched by the EC MHM module through the EC MHM adapter and routed to the destination module in EC. Due to security reasons, firewalls will typically block requests initiated from the message broker. Hence, the EC MHM pushes and pulls messages to and from the message broker. There is no actual EC MHM adapter delivered with EC. The projects have to implement a class implementing an interface and configure EC MHM to use this class. This configuration is done by the system settings feature in EC.

The interface between the EC MHM adapter and message broker would typically be based on JDBC or web services.

The message broker or the message broker extensions are responsible for the message archive. This should have the original and converted messages and their status and log.

The message broker extensions make it possible to provide the services that EC needs without modifying the message broker used. Then it is more straight forward to upgrade the message broker in use.

Message Handling Module
General scope

The MHM strategy is to have whatever required end-user functionality to handle messaging in a standard EC user interface. The MHM is the interface for the interchange of messages in EC. All EC sub-systems are connected to the message broker via the EC MHM module. The message broker handles the logistics side of this process. To support this part, there are functions in the message broker that technically secure the interchange of messages with internal functions that support all the demands of track and trace. The message broker can be used for handling external and on-site interface integration with EC.

Figure 2. Main steps - incoming messages

It is important to get a clear idea of what the role of the messaging module is in EC. The purpose of the messaging module is to be the infrastructure required in order to support the business requirements of the different bus
…[truncated]


==========================================================================================
## [18/25] Navigator default values
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/navigator_default_values.html
==========================================================================================
Navigator default values
Introduction

When a screen is open, it looks for default values for the navigator. Default navigator values are configured in Personal Settings (CO.1007) or Maintain User Settings (CO.1008), for Customise Category Navigator Default Value.

Group model navigator and nav model navigator uses session cache variables for navigator values. The first time a screen for a group model or nav model is open, the default values are used. Then, when you move between screens with same group model or nav model and same date input fields, the navigator values are remembered across the screens. It is possible to disable the navigator cache.

It is possible to configure that the dates should be remembered differently for different type of screens. E.g. screen listing forecast values will be for different dates than screens listing actual values.

Configure navigator default values

Default navigator values are configured in Personal Settings (CO.1007) for current user or in Maintain User Settings (CO.1008) for users or roles, for Customise Category Navigator Default Value.

When default values are for roles and a user have several roles with default values, it is random which default values are used.

Group model
It is possible to specify default values for the different OBJECT in the group model. E.g. WELL, STREAM, TANK etc.
Lookup key: /com/ec/eccommon/genericmodel/navigator/defaultvalue/groupmodel/<Object class>
Example: /com/ec/eccommon/genericmodel/navigator/defaultvalue/groupmodel/WELL

Nav Model
It is possible to specify default values for the different navigation model and OBJECT. E.g. TRANSPORT_COMMERCIAL and CONTRACT, NOMINATION_POINT, etc. Lookup key: /com/ec/eccommon/genericmodel/navigator/defaultvalue/navmodel/<model>/<class>/<class>
Example: /com/ec/eccommon/genericmodel/navigator/defaultvalue/navmodel/TRAN_COMMERCIAL/CONTRACT/CONTRACT

Date(s)
It is possible to specify default value for DATE, FROMDATE and TODATE. This can be done for a specific screen or for all screens. First is the specify default value checked. If this is missing, the default for all screens is used.

Lookup key for all screens: /com/ec/eccommon/genericmodel/navigator/defaultvalue/DATE

Lookup key for specify screen: <url to the screen>/nav/defaultvalue/DATE
Example: /com.ec.prod.wr.screens/daily_well_status/GROUPMODEL/WELL/TARGET/WELL/CLASS_NAME/PWEL_DAY_STATUS/nav/defaultvalue/DATE

Objects classes
It is possible to specify default values for object classes in the navigator.
Lookup key: /com/ec/eccommon/genericmodel/navigator/defaultvalue/<class name>
Example: /com/ec/eccommon/genericmodel/navigator/defaultvalue/CALC_COLLECTION_DAILY

Remember dates for different type of screens

Dates selected in the navigator are remembered between group and nav model screens using session cache variables. The datenavkey argument allows screens to remember different dates that the default.

datanavkey in screen XHTML

datenavkey can be specified in the screen XHTML for GenericGroupModelNavigator or GenericNavModelNavigator.
Example:

<model scope="renderer" class="com.ec.eccommon.genericmodel.model.web.GenericGroupModelNavigator">
  <arg name="groupmodel" value="
…[truncated]


==========================================================================================
## [19/25] How to send messages from EC
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_send_messages_from_ec.html
==========================================================================================
How to send messages from EC
Introduction

This section provides a detailed guide on how to send messages from the EC using Message Handling Module (MHM),

Actors defines the sender and receiver of the messages.

Distribution list groups multiple recipients together.

Message Definition defines the type of message, subject of the message, handling of the message (manual, semi-automatic, automatic), sender of the message, etc.

Message Distribution connects Message Definition with Distribution Lists. A message definition can be linked to multiple distribution lists. Parameters are used to identify which distribution list to use when sending a message.

Report Name - Distribution list for sending reports, the value is the name of the runnable report.

SUBJECT - Distribution list for sending free text messages, the value is the subject of the free text template.

A schedule with two business action are used to send messages.

MessagesSend - transfer outgoing messages to MHM for processing

SendMail - send the messages.

Remove Endpoint Configuration is used to configure endpoint for sending mail from EC

Actors

Actors belongs to a company and a contact group. Contact groups are group together to contact group sets.

The Maintain Contact Group Set (CO.0225) screen maintains the contact group sets. Contact group sets belongs to a functional area.

The Actor Maintenance (MHM.0012) screen maintains the contact groups and the actors belonging to a contact group. An actor has a primary address and secondary address. When both addresses are defined, the message is sent to both addresses.

Distribution Lists

The Distribution List (MHM.0001) screen maintains the distribution lists. A distribution list belongs to a functional area. Distribution list groups multiple actors together. An actor can belong to multiple distribution lists.

Message Definition

The Maintain Message Type (CO.0142) screen maintains the message definitions. A message definition belongs to a functional area.

Subject - subject of the message. When sending reports, $REPORT_NAME$ in the subject will be replaced with the runnable name of the report. $<report parameter name>$ with the parameter value.

Handling - manual, semi-automatic, automatic. Manual and -semi-automatic messages needs to be processed in the Outgoing Messages (MHM.0009) screen before they are ready to be sent.

Sender - defines the sender of the message

External Format

The external format for the message definition is configured in the Message Format (CO.0143) screen. A message can have multiple external formats, one of them can be marked as default.

Text - plain text format

XML - XML format

EDI - EDI format

Body Text - plain text format where only the message body is used in the email body.

Free Text Template

The Freetext Message Template (CO.0144) screen maintains the free text templates for the message definition. The subject is used to identify the template. The template text can be modified before sending the message in the Send Freetext Message (MHM.0010) screen.

Message Distribution

The Message Distribution (MHM.0004) screen is used to link message definitions with distribution lists. One message de
…[truncated]


==========================================================================================
## [20/25] How to disable navigator cache
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_disable_navigator_cache.html
==========================================================================================
How to disable navigator cache
Introduction

By default, screens in EC will remember navigator values in the current user session. The remembered values will take priority over default navigator values. In some cases it might be preferable to always have the default values in the navigator instead of the remembered values. This can be useful if for example there are user configured default values. To achieve this the navigator cache can be disabled for a given screen.

Navigator cache can only be toggled on a screen-by-screen basis.
How to disable the navigator cache

To disable the navigator cache you need update access to the Maintain Treeview screen and the name of the screen you wish to configure. In this example we will use the "Contract Bundle Transfer" screen.

Open Maintain Treeview screen.

(optional) If you are not using a custom treeview, create one.

Find the treeview item for the screen and select it.

Enter the following in the Additional Parameters: DISABLE_NAVIGATOR_CACHE=TRUE

How to re-enable the navigator cache

To re-enable the navigator cache, remove the additional parameters for the treeview item.

Conclusion

When the navigator cache has been successfully disabled for a screen the navigator will use the configured default values whenever you go to the screen. These values can be found and configured in the "Maintain User Settings" screen under Customise Category "Navigator Default Value".


==========================================================================================
## [21/25] EC Dataloader
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/configuration-and-data-loading.html
==========================================================================================
EC Dataloader

Entering configuration data can be unnecessarily complicated due to auto-generated keys and foreign keys. A migration tool was developed to accept JSON representations of configuration data with the possibility of referring to columns in different rows across the JSON. The JSON format is the same as the one used for the Rest API. The way you refer to different rows within a JSON is through the EC Expression Language. The tool aims to replace SQL scripts that have the sole job of inserting data.

The tool is currently used in EC Extensions and the EC REST API.

EC Extensions

Dataloader JSONs are interchangeable with SQL scripts in extensions, meaning they follow the same rules for naming conventions and file locations. They will be read and migrated by Flyway the same way as SQL files. Examples of these files can be found in the Energy Components Software Development Kit (EC-SDK) - /energycomponents-sdk/examples/extensions.

EC REST API

Configuration data in EC can be exported and imported in JSON or CSV formats using the EC REST API.

Export

/rest/v1/services/dataloader/export

This service will run the query given for a mainclass and then recursively find all classes that these objects depend on. The service will look for and export ownerclasses, relations, reference types, and foreign keys of the mainclass. In addition, it will add classes that are listed in the associatedClasses parameter and has dependencies on the mainclass. The output is a multiclass datamodel in JSON format compatible with the EC dataloader where the objects are sorted in the correct order and the dependency keys are replaced with EC datamodel expressions, so the exported file can be imported by the EC dataloader.

If an exported class is readonly, the exported object will have verificationStatus="warning", verificationText="readonly" and status="unchanged". In such cases, the object either has to exist in the target database or has to be replaced offline with a class that is not readonly. A typical example of this is the EC_CODE_REF class that is normally readonly and has to be replaced with EC_CODES to be able to update/create it.

Some objects may contain references that do not exist in the database. In such cases, this service will autogenerate an object in the exported file with the verificationStatus="warning", verificationText="autogenerated" and status="unchanged". Offline verification has to be performed and the status changed to status="merge" or status="create" before these objects can be imported.

Classes listed in ignoredClasses will not be exported.

Import

/rest/v1/services/dataloader/import

This service accepts a datamodel in EC dataloader format and imports data in the way described in this document. The http header Content-Type determines the accepted dataformat.

Content-Type	Format


application/json

	

JSON




text/plain

	

CSV

For large datasets make sure the client is using chunked http transfer by setting the Transfer-Encoding: chunked http header.

Common Parameters

Both endpoints are able to run asynchronously by passing async=true parameter. The resulting export/import will then run in the background on EC and the re
…[truncated]


==========================================================================================
## [22/25] Data Purging
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/data-purging.html
==========================================================================================
Data Purging
Data Purging Functionality

The datapurging module is designed to manage the deletion of data from the database based on specific purging policies. This module ensures that data is removed efficiently and according to the rules defined in the purging policies. It does not do database maintenance tasks like truncating data, running tablespace compaction or other such activities. Here is an overview of its main functionalities:

Purging Data:

Responsible for deleting data from the database tables based on the provided purging policy. It supports different types of policies.

MAIN : Purges data from the classes backing storage.

JOURNAL : Purges data from the classes journal storage.

MAIN_JOURNAL : Purges both main and journal storage.

Counting Rows Affected:

Includes a method to calculate the number of rows that would be affected by the purging operation without actually deleting the data. This is useful for understanding the impact of a purging policy before executing it.

Validation and Error Handling:

Includes validation checks to ensure that the purging policies are correctly defined. It throws exceptions if required fields are missing or if the policy configuration is invalid. Additionally, it handles SQL exceptions and logs errors to help with troubleshooting.

Logging:

Uses logging for important actions and errors. This helps in monitoring the purging process and provides insights into the operations performed.

Overall, the data purging module provides a robust and flexible way to manage data purging in a database, ensuring that data is deleted according to defined policies while providing mechanisms for validation, error handling, and logging.

Overview of Policy Rules

The policy rules defines various rules and attributes that govern how data purging is performed. Here is a generic overview of the different policy rules:

Active:

Description: When not active, the policy will be skipped when executing the purging policies. The policy can still be run ad-hoc with the button provided in the Data Purging business function.

Exec Order:

Description: The order the policies will be applied in. Useful for cleaning up data with child records (foreign key constraints) before the main data.

Policy Name:

Description: A unique identifier for the purging policy.

Class Name:

Description: The name of the Energy Components domain class from which data will be purged.

Policy Type:

Description: Specifies the type of purging policy. Possible values are MAIN, JOURNAL, and MAIN_JOURNAL, which determine the scope and type of data to be purged.

Retentions:

Description: The number of days, months, or years for which data should be retained before being purged. This is used in conjunction with the Scope type.

Scope Type:

Description: Defines the scope of the retention period. Possible values are Items, Days, Months, and Years.

Retention Date:

Description: A specific date before which data should be purged. This is an alternative to using Retentions.

Retention Date Column:

Description: The name of the column in the domain class that contains the date values used for determining which data to purge.

Batch Size:

Description: T
…[truncated]


==========================================================================================
## [23/25] Migration utility functions
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/migration_utility_functions.html
==========================================================================================
Migration utility functions

Utility packages for with procedures that can be used in migration scripts.

ecdp_config_util

This package contains procedures for making it easier to add some basic configuration:

Access (Objects, Roles, User Roles, Access, Object partition)

Preference

Treeview item

Language Translation

Remove classes

Configure Access
Objects
  PROCEDURE mergeBasisObject(p_object_name  VARCHAR2,
                             p_object_descr VARCHAR2,
                             p_object_type  VARCHAR2 DEFAULT 'URL',
                             p_app_id       NUMBER DEFAULT 1,
                             p_created_by   VARCHAR2 DEFAULT USER)

Procedure mergeBasisObject can be used to add or update access object (T_BASIS_OBJECT).

Example:

begin
  ecdp_config_util.mergeBasisObject(p_object_name => '/com.ec.frmw.co.screens/unit',
                                    p_object_descr => 'Unit',
                                    p_created_by => 'UPGD-13.2.1');
end;
/
Role
  PROCEDURE mergeBasisRole(p_role_id    VARCHAR2,
                           p_role_name  VARCHAR2,
                           p_app_id     NUMBER DEFAULT 1,
                           p_created_by VARCHAR2 DEFAULT USER);

Procedure mergeBasisRole can be used to add or update access role (T_BASIS_ROLE).

Example:

begin
  ecdp_config_util.mergeBasisRole(p_role_id => 'ALLOC_USER',
                                  p_role_name => 'Allocation User',
                                  p_created_by => 'UPGD-13.2.1');
end;
/
Access
  PROCEDURE mergeBasisAccess(p_object_name VARCHAR2,
                             p_role_id     VARCHAR2,
                             p_level_id    NUMBER,
                             p_app_id      NUMBER DEFAULT 1,
                             p_class_name  VARCHAR2 DEFAULT NULL,
                             p_created_by  VARCHAR2 DEFAULT USER);

Procedure mergeBasisAccess can be used to add or update access to an object for a role (T_BASIS_ACCESS).

Example:

begin
  ecdp_config_util.mergeBasisAccess(p_object_name => '/com.ec.frmw.co.screens/unit',
                                    p_role_id => 'SYST.ADM',
                                    p_level_id => 10,
                                    p_created_by => 'UPGD-13.2.1');
end;
/
Object and Access
  PROCEDURE mergeBasisObjectAndAccess(p_object_name  VARCHAR2,
                                      p_object_descr VARCHAR2,
                                      p_object_type  VARCHAR2 DEFAULT 'URL',
                                      p_access       VARCHAR2,
                                      p_app_id       NUMBER DEFAULT 1,
                                      p_created_by   VARCHAR2 DEFAULT USER);

Procedure mergeBasisObjectAndAccess can be used to add or update an access object and assign access to roles.

Role and level are specified in a JSON structure: [["role id", <level>],["role id", <level>], …​ ]

Example:

begin
  ecdp_config_util.mergeBasisObjectAndAccess(p_object_name => '/com.ec.frmw.co.screens/unit',
                                             p_object_descr => 'Unit',
                                             p_object_type => 'URL',
                       
…[truncated]


==========================================================================================
## [24/25] REC ID utility
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/rec_id_utility.html
==========================================================================================
REC ID utility
Introduction

REC_ID is populated with a GUID (Global Unique Identifier). It is used to identify one row in a table. All rows in EC should have a REC_ID. Extension attributes uses REC_ID to join the extension table with the main table. From EC 14.0, REC_ID will be used to list revision info for a row.

If REC_ID is not populated, extension attributes or revision info will not work.

If journal tables are missing REC_ID, revision info will not be listed.

From EC 14.0, to enforce that REC_ID is filled out, REC_ID will be set to NOT NULL for tables with a corresponding journal table and a unique index will be created for REC_ID. When upgrading to EC 14.0, a script will check that all tables with corresponding journal table have value for REC_ID, that the REC_ID is unique and that the journal row(s) have correct REC_ID. If not, the script will update these values. This could take some time to run. To minimise the impact, the check of the REC_ID can be done before upgrading to EC 14.0.

The utility PL/SQL package ecdp_rec_id_util can be used to check and update REC_ID. The utility procedure CheckAndVerifyRecID or SyncJournalRecID writes status to table CTRL_REC_ID_UTIL_STATUS. This table should be checked to see if there are any tables that needs to be fixed.

When CheckAndVerifyRecID or SyncJournalRecID are rerun for the same table and the previous run didn’t find any issue, only changes after the previous run are checked. Tables without any changes are skipped.

It is possible to exclude tables from the check of REC_ID by inserting the table name into the CTRL_REC_ID_UTIL_BLACKLIST table.

The REC_ID utility procedures could take some time to run and could create heavy load on the database. It depends on the number of rows for the tables and if REC_ID has not been populated.

It is recommended to first test it on a copy of the production database before running it on the production database.

Tables with duplicate REC_ID and used by classes with extension attributes will not be fixed. The duplicated REC_ID must be manually fixed to ensure that the values for the extension attributes are mapped to correct REC_ID.

Check tables for missing REC_ID and verify journal REC_ID
PROCEDURE CheckAndVerifyRecID(p_table VARCHAR2 DEFAULT '%');

This procedure checks that the tables have value for REC_ID, that the REC_ID is unique and verify that the REC_ID for the journal tables are correct using the primary key. Journal rows for deleting is not included.

It inserts the result into the CTRL_REC_ID_UTIL_STATUS table.

Column name	Description


TABLE_NAME

	

The name of the table checked.




DAYTIME

	

The time the check was run. When the table is checked again and the previous check was OK, only new or updated rows after this date is checked (.e.g nvl(last_updated_date, created_date) > daytime)




NEED_FIXING

	

Set to Y when the table is missing REC_ID or has duplicate REC_ID or has journal rows with wrong REC_ID.




STATUS_INFO

	

Information about the result of the check. When everything is OK, it is empty.

Parameter p_table can be used to limit the list of table that are checked.

Tables in CTRL_REC_ID_UTIL_BLACKLIST are not checke
…[truncated]


==========================================================================================
## [25/25] Pendo
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/pendo.html
==========================================================================================
Pendo

The Software Experience Management platform Pendo has been integrated into EC.

For Pendo to function, you might have to turn off any 'Tracking Protection' and tracking blockers in your browser.

Setup

To use Pendo with EC you have to configure the PENDO_API_KEY variable to your Pendo API key.

After EC is deployed with the PENDO_API_KEY configured, the Pendo-EC integration can be verified to ensure that it is working correctly. To do this, open the web console in the browser and run the command:

pendo.validateEnvironment()

If successful the output of this command should contain visitor and account metadata and not give an error message.