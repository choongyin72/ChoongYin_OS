# Raw content — DOC-09
Modules: ['frmw/ec-extensions', 'frmw/appdev', 'frmw/rest-api', 'frmw/expression']
Pages: 21



==========================================================================================
## [1/21] EC Rest API
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/rest-api/rest-api.html
==========================================================================================
EC Rest API
Introduction

The EC REST API will serve as the basis entry point for new integrations and clients.

Some high level features of the REST API include:

REST API for the Domain model. A full REST API is available to query and modify the EC Domain model (also called EC Class Concept).

REST API to support the ECIS Agent. The new ECIS Agent uses REST to communicate with EC. Miscellaneous REST API to support core EC functionality, like Job Scheduling. A REST API for triggering asynchronous Jobs through the EC Scheduler.

Miscellaneous endpoints for managing BPM Importing and exporting of configuration data

In future versions, EC might be extended with a more high level API for specific business logic. Examples might include, REST API for Production well Testing, Production Deferment, Cargo Planning, Gas Dispatching and so on.

Focus for this initial version of REST API has been to enable import and export of data, to and from external resources, like SCADA systems. To have a well-defined API for import/export of data is essential, especially when EC is running in the cloud with no access to SCADA systems.

The EC REST API tries to adhere to the following design principles: hypermedia as the engine of application state principle, HATEOAS

Client Development

A java library containing an SDK for creating java clients is provided in the Energy Components Software Development Kit (EC-SDK). Its provided as a jar and can be obtained using the following maven artifact id:

<dependency>
    <groupId>com.ec.frmw</groupId>
    <artifactId>frmw-core-api</artifactId>
    <version>${project.version}</version>
</dependency>

This library contains all EC REST entry points as interfaces with OpenAPI v3.0.3 annotations and all data interface classes that can be used to communicate with EC.

In addition it also contains an easy to use RestEasy client with EC specific authenticators to easily interface with EC.

See the EC-SDK for more examples (energycomponents-sdk/examples/rest).

API documentation

API documentation and description are auto-generated and follows the code. It is made available online through your EC installation.

The documentation is provided as OpenAPI version 3.0.3 JSON and YAML documents. Read more about this specification here: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md. It is also available in Swagger version 2.0 
…[truncated]


==========================================================================================
## [2/21] EC Extensions Overview
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/ec-extensions-overview.html
==========================================================================================
EC Extensions Overview
Introduction

Energy Components has introduced EC Extensions to easily extend and build solutions on top of the core EC product. These extensions will be managed by EC so that you will have control over which extensions are active and what modifications they have done to the system. You will also have full control over the extension lifecycle, including functions (web pages and APIs) to control start, stop, disable, update, database migrate and more.

Extensions are software projects with source code that are built into a binary executable, that can then be deployed on top of an EC system.

Quorum Software is shipping a number of extensions that can be used on top of EC.
Talk to your Quorum Software representative to get more information about the current status of the available extensions.

Custom extensions

Quorum Software has enable anyone to develop their own extensions, that may be deployed and managed on top of their EC system.

Manage extensions

Extensions are delivered as binary software components. These binaries can be uploaded into your EC system and managed from there, see How to install an EC Extension.

Use the Extensions Manager screen to manage the lifecycle of extensions. 

When the Run on startup checkbox is checked in the Extensions Manager, the extension starts when EC boot. EC downloads the extension from the database and extracts it, verifying that there is no pending database migration and starts the extension.

When the database migration fails with Unable to calculate checksum for …​, the reason could be the file encoding. The database migration script files should have UTF-8 encoding.

If the extension contains only database migration scripts and the database migration has been run, the Run on startup could be unchecked to prevent EC from downloading and verifying the extension every time EC boot.


==========================================================================================
## [3/21] How to create EC Extension
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/how_to_create_extension.html
==========================================================================================
How to create EC Extension

Extensions are software projects with source code that are built into a binary executable (i.e. WAR file), that can then be deployed on top of an EC system. Extensions can contain Flyway database migration scripts, custom business functions, custom business actions, Jasper reports, etc.

When developing an extension for EC it is required to follow a certain file structure as well as having a correctly configured pom file. The Maven Archetype for Extensions can be used to simplify this process by generating a skeleton maven project with some example files to get started. The skeleton will give a decent indication of "what goes where" as well as filling in information about the extension such as extensionID, name and description.

Alternative to using the Maven Archetype for Extensions is to copy an existing extension and update the pom file with extension information.

The extension can be build with Maven command mvn clean install. This will create an extension artifact which can be deployed on an EC system.

Example of how to create EC Extensions is available in the Energy Components SDK:
energycomponents-sdk/examples/extensions/000-create-extension.

Example extensions are available in the Energy Components SDK:
energycomponents-sdk/examples/extensions.

See also Database migration in Extensions, Starting an EC Extension Maven Project


==========================================================================================
## [4/21] How to install an EC Extension
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/how_to_install_ec_extensions.html
==========================================================================================
How to install an EC Extension
Introduction

This document describes the step-by-step guidelines on how to install an EC Extension in EC application. The screenshots shown below are using EC Chemistry (XCH 1.0.0) as an example.

However, the guidelines mentioned in this document are applicable for all EC Extensions.

Pre-requisites

If installing an EC Extensions from Quorum Software, please refer to the related Installation Guide document of the EC Extension to know the required EC version and pre-requisites before proceeding to install the EC Extension.

Installation

You have four options to install the EC Extension:

Extension manager web interface

Manually installing EC Extension, follow the instructions in Install the EC Extension on a running EC section.

Install the EC Extension during EC boot

Maven, use the ecextension-maven-plugin , as described in examples in Energy Components SDK .

Use the Rest API with your favorite rest client.

Automatically installing EC Extension, follow the instructions in Install the EC Extension during EC boot section.

Option 1: Install the EC Extension on a running EC

The screenshots shown below are using EC Chemistry (XCH 1.0.0) as an example.

Log in to EC with valid credentials.

Navigate to the Extensions Manager screen by following this path: CONFIGURATION / SYSTEM / DEVELOP / Extensions Manager

Alternatively, you may search for the keyword "Extensions Manager" in the Search field on the left-pane.

Click on the SELECT FILE button and select the WAR file (e.g. xch-aggregator-1.0.0.war). EC Extensions delivered by Quorum Software can be downloaded from the EC User Community.

The required WAR file(s) is mentioned in the related Installation Guide document of the EC Extension.

Multiple EC Extensions of different types can run simultaneously in an EC application.

Before a new version of the EC Extension is installed, the existing version(s) of the same EC Extension (if any) must be stopped and disabled. In order to do this, first, select the EC Extension to be disabled. Then, click on the STOP button. You also have the option to delete the disabled EC Extension.

Click on the UPLOAD EXTENSION button and wait until the selected WAR file has been uploaded.

Once the file is uploaded successfully, notice that the "State" is shown as "UNKNOWN", which is expected. Click on the START button.

If you want to start the
…[truncated]


==========================================================================================
## [5/21] Database migration in Extensions
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/db-migration.html
==========================================================================================
Database migration in Extensions
Introduction

Database migration scripts can be added to Extensions. The default location for database migration scripts is the src/main/webapp/WEB-INF/db folder. Extensions use Flyway to do the database migration.

Rules for data model changes

Extensions have strict rules for data model changes.

Table

Product tables can not be modified.

Table name must start with extension id, e.g. if the extension id = TPL then the table name must be TPL_<table name>.

Table name must not be longer than 100 characters including the extension id.

Table changes are versioned migrations

Package

Product package (including UE package) can not be modified.

Package name must contain extension id, e.g. TPL_<package name>, ZP_TPL_<package name>, UEI_TPL_<package name>.

Package changes are repeatable migrations

Views

Product view can not be modified

View name must start with extension id, e.g. TPL_V_<view name>

Views should be created with FORCE keyword if there is dependency on auto generated object which is supposed to get generated through build view/report layer

View changes are repeatable migrations

Triggers

Product triggers can not be modified

Trigger name must prefix with extension id, e.g. TPL_IU_<trigger name>

Triggers should be created with FORCE keyword if there is dependency on auto generated object which is supposed to get generated through build view/report layer.

Trigger changes are repeatable migrations

Rules for class changes

Changes of class attributes / class relation for existing class:

New class attributes which extend existing class should be prefixed with extension id, eg: TPL_<attribute name>.

New class relations which extend existing class should have ROLE_NAME prefixed with extension id. e.g. TPL_<role name>

While extending existing EC classes, ensure that APP_SPACE_CNTX is set to the extension id.

Ensure the OWNER_CNTX is more than or equal to 1000.

Product attributes should not be disabled (i.e. set DISABLED_IND = Y) except for class attributes used in group model. Instead, the IGNORE_IND property can be used to disable attributes from the application layer (i.e. screens and the rest API). See Property IGNORE_IND

New attribute or relation should not map to existing column in EC tables.

It there is only one or a few new attributes or relations that are added, then DB_MAPPING_TYPE = EXTENSION can 
…[truncated]


==========================================================================================
## [6/21] Starting an EC Extension Maven Project
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_starting_an_ec_extension_maven_project.html
==========================================================================================
Starting an EC Extension Maven Project

The purpose of this document is to explain how to get started the Energy Components Extension.

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Extension Configuration

For this example we are going to create a fictional extension for centre of excellence. The names, the configuration are only intended as guides. Make sure that you use due diligence when creating extensions for customers or projects.

Guidelines

Create a project space for your project

Download Maven Archetype Template

Make sure you maven repository is set up correctly, if you do not have access to the nexus hub you will need to manually download the maven archetype

In order to be able to create a maven extension project, ensure you have maven extension archetype template in your repository.

Maven Project Structure

Below is an example of the Maven Project build parameters you will need to populate as part of a New EC Extension Project.

Parameter	Description	Example


DgroupId

	

Extension group ID

	

com.ec.extension




DartifactId

	

Extension artifact ID

	

demo




Dpackage

	

Extension package folder definition, should be same like groupID

	

com.ec.extension.demo




DextensionId

	

Extension ID, use to register in EC, and cannot exceed 5 letters. also take into account that this id also takes up part of the characters naming space.

i.e. if a table has 100 characters limit the extension.id with take up part those characters

	

ZCOE




DownerContext

	

Context Owner ID Needs to be above 1000 for customer

	

2000




DarchetypeVersion

	

This a static parameters and should be the latest version of the archetype installed on the machine.

	

14.0.4




DecVersion

	

EC Version that this extension depends on. Example: "14.0.4"

	

14.0.4




Dversion

	

Extension version

	

1.0.0




DextensionDescription

	

Extension Description, can describe this extension belong to which project

	

Centre of Excellence Extension Demo




DextensionProvider

	

Extension provider, can describe the extension was provide from which office

	

Centre of Excellence Extension Office

Create Maven Project

Once the maven extension archetype template is ready, open an command as administrator and enter the command prompt below to create the extension project.

You will need to switch the parameter
…[truncated]


==========================================================================================
## [7/21] Simplified Developer Environment Set-up in EC 14.x
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_simplified_developer_environment_set_up_in_ec.html
==========================================================================================
Simplified Developer Environment Set-up in EC 14.x

The purpose of this document is to explain how to configure a simplified developer environment on your local device for EC 14.x development purposes only.

Prerequisites
EC Version Requirements
Development Item	Verified EC Version


Extension

	

12.2.10, 13.x, 14.x

Developer Requirements
System requirements
Item	Minimum Requirement


RAM

	

16GB




CPU

	

4 Cores




Storage

	

200 GB




OS

	

Windows 10 Pro, Mac Mojave, or Ubuntu

Software Requirements

Ensure that your operating system is up-to-date

Ensure that you have the latest Docker installed

Ensure the correct Java JDK version is installed and configured for your version of Energy Components

Ensure that you have the latest Maven installed

Ensure that you have installed a supported IDE Development tool (Eclipse or IntelliJ)

Environment Set-up
Maven Configuration

Maven configuration is the most important part of this process, you will need to ensure your Maven settings.xml is configured correctly.

Ensure that you have verified your user credentials for EC Hub by logging in to https://hub.energycomponents.com.

Install Maven and configure for your environment type

https://maven.apache.org/install.html

Navigate to your Maven settings.xml file (refer https://maven.apache.org/configure.html)

Make a backup of your settings.xml

Example Maven Project

Replace the content of your settings.xml with the following

In this step you will configure Maven to use EC Hub Nexus

Make sure to replace the username and password for hub profile with your EC Hub login details

Maven Setting.xml for EC 14.x Development
<?xml version="1.0" encoding="UTF-8"?>
<settings>

    <servers>
        <!-- Quorum Software Hub Server -->
        <server>
            <id>hub</id>
            <username>your.email.here@email.com</username> <!-- change this to your ec community login -->
            <password>YourSuperSecurePasswordHere</password> <!-- this is the password to your hub, if not working create a jira -->
        </server>
    </servers>

    <!-- START OF PROFILES -->
    <profiles>
        <!-- Quorum Software hub.energycomponents.com -->
        <profile>
            <id>ec-sdk</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <repositories>
                <repository>
            
…[truncated]


==========================================================================================
## [8/21] Compile and Deploy and Extensions
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_compile_and_deploy_extensions.html
==========================================================================================
Compile and Deploy and Extensions

The purpose of this document is to explain the process for compiling and creating the deployable Energy Components Extension.

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Compile Your Extension
Guidelines

Make sure that your project environment is clean and free of unneeded files.

Make sure that all project code is synced to your source control system.

Make sure that you are using all the latest script before compiling your maven.

Compile Maven Project

Open CMD and navigate to extension folder.

Run mvn clean package.

Ensure the build is run successful.

Go to target folder, ensure a new war file is created.

Deploy Your Extension
Upload Extension via EC Application

Extensions can be installed in EC application. An installation guide for installing extensions can be found in How to install an EC Extension.

Upload Extension via CLI

You can also deploy your extension from mvn command if you add the ecextension-maven-plugin to your project pom.

Configure Maven Plugin
<project>
    ...
    <build>
        ...
        <plugins>
            ...
            ...
            <!-- Deploy and migrate to EC. To run :  or bind it to an appropriate phase-->
            <!-- mvn install ecextension:deploy -->
            <plugin>
                <groupId>com.ec.extension.maven</groupId>
                <artifactId>ecextension-maven-plugin</artifactId>
                <configuration>
                    <ecappurl>https://YOUR_EC_URL</ecappurl>
                    <clientid>extension-client</clientid> <!-- client for uploading extension -->
                    <clientsecret>xxxxxxx</clientsecret> <!-- secret to the client -->
                    <timeout>60</timeout>
                    <force>true</force>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>

The client must have access role Extension Management Admin Role (i.e. access to /rest/v1/services/management/extensions).

Create a client in the User Maintenance (CO.1000) screen. See How to create Service Account for external integration access

Assign role Extension Management Admin Role to the client.

Deploy With Maven

mvn clean install ecextension:deploy


==========================================================================================
## [9/21] Create EC Extension Classes
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_create_ec_extension_classes.html
==========================================================================================
Create EC Extension Classes

The purpose of this document is to explain the creation of customer class changes in Energy Components Extension.

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Create A New EC Classes or Extending Product Class Objects Guidelines

See Class configuration rules for class configuration rules.

For adding datasources, processing and alternatives to trigger logic using Java and expressions, please see Application layer data sourcing and processing with custom Java processors

Starting from EC 12.2, there have some limitation where project cannot perform changes directly in the class, e.g.: cannot add new attributes directly in product’s class, either function attribute or column attribute which refer to generic column (TEXT_01, VALUE_01, DATE_01 and etc).

For existing project (below 12.2), for those class attributes which using the column TEXT_xx, VALUE_xx or DATE_xx, the project need to create a specific datamodel, migrate all the data into the new project table (data and rec_id). And for class, the customize attributes need to move into extension.

Extension class configuration script should be in XML format.

Extension of Class Attributes for existing class

All custom Extensions must start with the Extension ID used for the project

New classes should prefix with Extension ID. Attributes of new classes need not to be prefixed with Extension ID.

Attribute name must not be longer than 100 characters including the Extension ID.

While extending existing EC classes, ensure you are using the Extension ID as APP_SPACE_CNTX.

While extending existing EC classes, make sure you are not defining any configuration for EC APP_SPACE_CNTX.

Ensure the OWNER_CNTX is more than or equal to 1000.

You cannot add new column to existing EC tables.

New attribute should not map to existing column in EC tables.

You can create separate extension table for storing the value of additional attribute, then define the DB_MAPPING_TYPE of attribute as below:

EXT_JOIN

DB_SQL_SYNTAX to map to the extension table’s column name

DB_JOIN_TABLE to map to the extension table name

DB_JOIN_WHERE can remain as blank, system will auto join the attribute with extension table using rec_id

LEFT_JOIN or INNER_JOIN

Can be used to join with extension table for lookup values (i.e. read only attributes, similar to f
…[truncated]


==========================================================================================
## [10/21] Create EC Extension Java
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_create_ec_extension_java.html
==========================================================================================
Create EC Extension Java

The purpose of this document is to explain the creation of Energy Components Extension with custom Java code.

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Create New Java Object into Extensions Guidelines
For all the custom java, there is no changes compare with previous EC version.

If the java is being use in xhtml, ensure the path of java class in xhtml to prefix with /extension/<EXTENSION_NAME>/

Need to update path in configuration tables such as BUSINESS_ACTION to prefix with /extension/<EXTENSION_NAME>/

The custom java files can be added to (../src/main/com.ec.extension.${extensionId})

following the same package names in the ear file customisations as per the screenshot below.

Naming Conventions

You can see the scripts are ordered by name in the way they need to go into the database.

Java Scripts
Naming	Value


Must Have File Trigger Name

	

<EXTENSIONID>_YourJavaObjectFileNameHere




Must Have java file Format

	

.java

Folder Structure

All Java Code to be placed under following directories and subdirectories depending on the type of Java action performed.

\src\main\java\com\ec\extension\<extension.id>\<sub_directory>

Create New Java Object as an Extensions
Example Java Object Extension Object

Make sure to follow the standards above.

Example Java Script

Below is an example script called zxcoeHelloWorld.java, it is a customer java script referenced in an extension.

Example Java Object Extension
package com.ec.extension.zxcoe.action;

// import external Java libraries
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;
import java.util.ArrayList;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

// My Custom Java Object For customer project
public class HelloWorld {

    // Print Hello World
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
Convert An Existing Custom Java Object Into An Extension

Make sure to follow the standards above.

Update any names or references to others objects in the Java code to reference the correct "extensified" name.

i.e. Any View, Package, Screen etc that has been rename as part of conversion into an extension.

Update or add any unrecognised external libraries (EC/third party) dependencies in the pom.

Examp
…[truncated]


==========================================================================================
## [11/21] Create EC Extension Screens
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_create_ec_extension_screens.html
==========================================================================================
Create EC Extension Screens

The purpose of this document is to explain the creation of customer screens in Energy Components Extension

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Create Custom Screen Guidelines
This document has been updated for EC 14.2.0 and above. If you are migrating extensions from pre-14.2.0 versions, note that treeview menu configuration has changed from database table (CTRL_TV_PRESENTATION) to JSON-based configuration. See How to configure Screen Treeview Menu for details.
For all the custom business function, there is no changes compare with previous EC version.

Need to update path inside xhtml to prefix with /extension/<EXTENSION_NAME>/

Need to update path in configuration tables such as T_BASIS_OBJECT and BUSINESS_FUNCTION etc to prefix with /extension/<EXTENSION_NAME>/

Need to configure treeview menu items using the JSON configuration files (see How to configure Screen Treeview Menu)

All the BF script should place in folder src\main\webapp\com.ec.xxx.screens

Naming Conventions

You can see the scripts are ordered by name in the way they need to go into the database.

xhtml Scripts
Naming	Value


Must Have Screen Name as Filename

	

YOUR_SCREEN_NAME_HERE




Must Have .xhtml file Format

	

.xhtml

xml Scripts
Naming	Value


Must Have Screen Name as Filename

	

YOUR_SCREEN_NAME_HERE




Must Have .xml file Format

	

.xml

Folder Structure

All Screen Object Need to be Places here:

src \ webapp \ com.ec.extension.<extension.id>.screens \

Create A New Screens Object As An Extension
Building New Custom Screens in Custom Extensions

Customer screens built in extensions are created using the same method as screens in previous version of Energy Components, the only difference is the mapping.

The custom screens can be added to (../src/main/webapp/com.ec.extension.${extensionId}.screens)

Update the screens paths by adding (/extension/${extensionId}) as per the image below. Layout customisations can also be added.

Move An Existing Custom Screens into Extensions

Existing custom screens can be added to (../src/main/webapp/com.ec.extension.${extensionId}.screens)

Update the screens paths by adding (/extension/$\{extensionId}) as per the screenshot below. Layout customisations can also be added.

A version SQL script can be added to (../src/main/webapp/WEB-INF/db/migration
…[truncated]


==========================================================================================
## [12/21] Create EC Extension Online Help
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_create_ec_extension_online_help.html
==========================================================================================
Create EC Extension Online Help

The purpose of this document is to explain the creation of Online Help for new screens in Energy Component Extension.

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Create Online Help Extensions
Guidelines
If there is any new screen added in the EC extension, then need to provide online help for the new screen. Online help script should be written as re-runnable script as much as possible.

Ensure using the extension BF number which is assigned in the table Business Function.

SQL code

Need to remove all references to SET_DEFINE_OFF, SET SQLBLANKLINES, SPOOL, PROMPT, etc.

All Extensions scripts must have a ";" at the end of each individual SQL statement.

All Extensions must have a "/" at the end of each SQL block in a script.

Online help script is group as repeatable script, so the file name should follow the repeatable migration format, eg: R__1000_ZXCOE_ONLINEHELP script.

The script can place in folder src\main\webapp\WEB-INF\db\migration\common\Onlinehelp

Naming Convention

You can see the scripts are ordered by name in the way they need to go into the database.

Naming	Value


Views are considered Repeatable in Flyway so they are defined with an

	

R




View must be executed in order number

	

1000




Views must contain the extension.id in the name

	

ZXCOE

Table 1. Example
Type	View Part	Script Name	View Name


View

	

View

	

R__1000_ZXCOE_ONLINEHELPSCRIPT.sql


==========================================================================================
## [13/21] Create EC Extension Reports
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_create_ec_extension_reports.html
==========================================================================================
Create EC Extension Reports

The purpose of this document is to explain the creation of Reports in Energy Component Extension.

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Create Reports Extension
Guidelines

Any new report created in EC from EC 13.0.0 ++ should be implemented as a Yellowfin Report

Follow the guide here for creating reports How to use EC’s Reporting and Analytics

Any legacy reports created in Jasper should be bundled into their own extensions, this provides a method for customer to update reports with out the need to take down other EC extensions.

Migrating Legacy Jasper Reports to Yellowfin

You can import existing ".xrml" format Jasper Reports into Yellowfin with little effort, if for some reason you cannot import them into Yellowfin using the below example.

Migrating Legacy Jasper Reports into Extensions that cannot be imported into Yellowfin
Updating a Verifying Reports Data Sources

If migrating an asset to extensions you will need to verify that

All reports data sources are correctly updated to reflect any extensified changes from a traditional EC configuration to EC Extension configuration.

i.e. if you have moved a custom view "ZV_My_Custom_Oil_View" to an extensified view "ZXCOE_My_Custom_Oil_View" you will need to update the report to reflect this.

All reports generate the same data as in the old system.

i.e. all data is the same, all fields are the same, all presentation is the same.

Any mappings to sub reports, images, graphics are updated to match the extension location.

Report Extension Configuration
Maven Project Structure

Below is an example of the Maven Project build parameters you will need to populate as part of a New EC Extension Project

Parameter	Description	Example


DgroupId

	

Extension group ID

	

com.ec.extension




DartifactId

	

Extension artifact ID

	

reports




Dpackage

	

Extension package folder definition, should be same like groupID

	

com.ec.extension.reports




DextensionId

	

Extension ID, use to register in EC, and cannot exceed 5 letters. also take into account that this id also takes up part of the characters naming space.

i.e. if a table has 100 characters limit the extension.id with take up part those characters

	

reports




DownerContext

	

Context Owner ID Needs to be above 1000 for customer

	

2000




DarchetypeVe
…[truncated]


==========================================================================================
## [14/21] Create EC Extension Datamodel
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_create_extension_datamodel.html
==========================================================================================
Create EC Extension Datamodel

The purpose of this document is to explain the creation of version scripts for data model changes in Energy Components Extension.

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Create A New Data-Model Object Guidelines

Starting from EC12.2, projects do not have the flexibility to perform any changes in the product’s datamodel, any changes in product’s table will cause failure in future upgrade through flyway. For upgrade project, if there is any project specific column was added in the product’s table, the column should be remove and create a new project specific table to keep that column. The data stored in the existing column, should migrate into new table together with the detail of REC_ID.

Make sure that you have a good understanding of the new standards and practices with tool such as flyway

Flyway in Energy Components

All Extensions must start with the extension.id used for the project

Cannot modify product screens

SQL code

Need to remove all references to SET_DEFINE_OFF, SET SQLBLANKLINES, SPOOL, PROMPT, etc

Need to remove all sql parameters reference from scripts such as &data_tablespace, &index_tablespace, etc.

All Extensions must have a ";" at the end of each individual SQL Block

All Extensions must have a "/" at the end of each SQL block in a script

Product tables can not be modified.

Table Name Must not be longer than 100 characters including the extension.id

Table name must start with extension id, eg: zxcoe_<MyCustomTableName>

Table changes are versioned migrations.

Extension Naming Convention

Following the naming convention in Flyway in Energy Components

You can see the scripts are ordered by name in the way they need to go into the database.

You do not name the object the same way you name the script

Naming	Example Value


extension.id

	

zxcoe




Table name

	

My_Oil_Field

Data-Model File name Naming Convention
Naming	Description	Example Value


VERSION

	

Flyway uses V as the standard for version scripts

	

V




MAJOR

	

The Major Number of the release

	

1




MINOR

	

The Minor Number of the release

	

0.0




UPDATE

	

A space for future items 0.0

	

0.0




EXECUTION ORDER

	

A time stamp for file creation

	

0100




EXTENSIONID

	

your extension id

	

ZXCOE




FILENAME

	

Filename

	

MyCustomOilFieldTable




FIL
…[truncated]


==========================================================================================
## [15/21] Create EC Extension PL/SQL Package
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_create_extension_package.html
==========================================================================================
Create EC Extension PL/SQL Package

The purpose of this document is to explain the creation of customer PL/SQL Packages in Energy Components Extension.

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Create A New Package Object Guidelines

Project should not make any changes in the product’s package, and thats including UE package. Starting from EC 12.2.3, there will have a table CTRL_USER_EXIT used to control and map the function/procedure for UE package.

Make sure that you have a good understanding of the new standards and practices with tool such as flyway

Flyway in Energy Components

All Extensions must start with the extension.id used for the project

Cannot modify product packages

SQL code

Need to remove all references to SET_DEFINE_OFF, SET SQLBLANKLINES, SPOOL, PROMPT, etc

Need to remove all sql parameters reference from scripts such as &data_tablespace, &index_tablespace, etc.

All Extensions must have a ";" at the end of each individual SQL Block

All Extensions must have a "/" at the end of each SQL block in a script

Package Name Must not be longer than 100 characters including the extension.id

SQL files can be deployed multiple times.

Packages must be in SQL format

Naming Convention

You can see the scripts are ordered by name in the way they need to go into the database.

Naming	Value


Packages are considered Repeatable in Flyway so they are defined with an

	

R




Package header specification are in one file

	


View must be executed in order number

	

100




Package must have package type

	

uei, ue, package




Package body specification are in one file

	


View must be executed in order number

	

200




Package must have package type

	

uei, ue, package




Packages must contain the extension.id in the name

	

ZXKG

Table 1. Example
Type	Package Part	Script Name	Package Name


uei

	

head

	

R__100_uei_zcoe_cargo_legs_head.sql

	

uei_zcoe_cargo_legs




uei

	

body

	

R__200_uei_zcoe_cargo_legs_foot.sql

	

uei_zcoe_cargo_legs




ue

	

head

	

R__0100_ue_zcoe_cargo_legs_head.sql

	

ue_zcoe_cargo_legs




ue

	

body

	

R__0200_ue_zcoe_cargo_legs_body.sql

	

ue_zcoe_cargo_legs




Normal Package

	

head

	

R__0100_zcoe_cargo_legs_head.sql

	

zcoe_cargo_legs




Normal Package

	

body

	

R__0200_zcoe_cargo_legs_body.sql

	

zcoe_cargo_legs

Folder Structu
…[truncated]


==========================================================================================
## [16/21] Create EC Extension Views
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_create_extension_views.html
==========================================================================================
Create EC Extension Views

The purpose of this document is to explain the creation of customer Views in Energy Components Extension.

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Create A New Extension View Object Guidelines

Project should not make any changes in the product’s view.

Make sure that you have a good understanding of the new standards and practices with tool such as flyway

Flyway in Energy Components

All Extensions must start with the extension.id used for the project.

Cannot modify product views.

SQL code must conform to these standards:

Need to remove all references to SET_DEFINE_OFF, SET SQLBLANKLINES, SPOOL, PROMPT, etc

Need to remove all sql parameters reference from scripts such as &data_tablespace, &index_tablespace, etc.

All Extensions must have a ";" at the end of each individual SQL Block

All Extensions must have a "/" at the end of each SQL block in a script

View Name Must not be longer than 100 characters including the extension.id

SQL files can be deployed multiple times.

Views must be in SQL format

Views should be created with FORCE keyword if there is dependency on auto generated object which is supposed to get generated through build view/report layer.

View is group as repeatable script, so the file name should follow the repeatable migration format, eg: R__0400_ZXCOE_V_TEST_VIEW.

The script can place in folder src\main\webapp\WEB-INF\db\migration\common\views

Naming Convention

You can see the scripts are ordered by name in the way they need to go into the database.

Naming	Value


Views are considered Repeatable in Flyway so they are defined with an

	

R




View must be executed in order number

	

400




Views must contain the extension.id in the name

	

ZXCOE

Table 1. Example
Type	View Part	Script Name	View Name


View

	

View

	

R__400_ZXCOE_V_CAP_STAT.sql

	

ZXCOE_V_CAP_STAT

Folder Structure

All versionable scripts go under the src \ main \ webapp \ WEB-INF \ db \ common\views

Create Custom Extension View Example
Script Example of repeatable code
Example Custom View
CREATE OR REPLACE VIEW ZXCOE_V_CALC_LOG_LEVEL_COUNTS AS
(
/**************************************************************
** Script     : ZXCOE_V_CALC_LOG_LEVEL_COUNTS.SQL
**
** $Revision  : 1.0 $
**
** Purpose    :
**
** General Logic:
**
** Created    :  24.12.2020 pontaluk
**
*
…[truncated]


==========================================================================================
## [17/21] Create EC Extension Triggers
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_create_ec_extension_triggers.html
==========================================================================================
Create EC Extension Triggers

The purpose of this document is to explain the creation of customer database triggers in Energy Components Extension.

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Create A New or Custom Trigger Object Guideline

Project should not make any changes in the product’s triggers

Make sure that you have a good understanding of the new standards and practices with tool such as flyway.

Flyway in Energy Components.

All Extensions must start with the extension.id used for the project.

Cannot modify product Triggers.

SQL code must conform to these standards:

Need to remove all references to SET_DEFINE_OFF, SET SQLBLANKLINES, SPOOL, PROMPT, etc

Need to remove all sql parameters reference from scripts such as &data_tablespace, &index_tablespace, etc.

All Extensions must have a ";" at the end of each individual SQL Block

All Extensions must have a "/" at the end of each SQL block in a script

SQL files can be deployed multiple times.

Views must be in SQL format.

Triggers should be created with FORCE keyword if there is dependency on auto generated object which is supposed to get generated through build view/report layer.

Trigger is group as repeatable script, so the file name should follow the repeatable migration format, eg: R__0600_XCOE_IU_TEST_TRIGGER.

The script can place in folder src\main\webapp\WEB-INF\db\migration\common\triggers

Naming Convention

You can see the scripts are ordered by name in the way they need to go into the database.

Naming	Value


Views must contain the extension.id in the name

	

ZXCOE




Views are considered Repeatable in Flyway so they are defined with an

	

R




View must be executed in order number

	

600




Must Have File Trigger Name

	

YOUR_NEW_TRIGGER




Must Have SQL file Format

	

.sql

Type	Trigger Part	Script Name	Trigger Name


Trigger

	

Trigger

	

R__0600_biu_zxcoe_cargo_fcst_leg.sql

	

biu_zxcoe_cargo_fcst_leg

Folder Structure

All versionable scripts go under the

src \ main \ webapp \ WEB-INF \ db \ common\ <release_number> \ triggers

Create A New Trigger Object As An Extension

Adhere to the guidelines for Trigger Objects

Example Trigger Extension Object
Script Example of versionable code
CREATE OR REPLACE TRIGGER BIU_ZXCOE_CARGO_FCST_LEG
BEFORE INSERT ON ZXCOE_CARGO_FCST_LEG
FOR EACH ROW
BEGIN

      IF :new.C
…[truncated]


==========================================================================================
## [18/21] Create EC Extension Calculation Libraries
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ec-extensions/development/development_create_extension_calculation_libraries.html
==========================================================================================
Create EC Extension Calculation Libraries

The purpose of this document is to explain the creation of version scripts for Calculation Library Database Objects in Energy Components Extension.

Prerequisites

Please see the requirements here Simplified Developer Environment Set-up in EC 14.x

Create A New Calculation Library (Data-Model) Object Guidelines
Calculation Libraries have a similar concept to the data-model process, where they should be included as part of the extension. In some extreme cases the calculation libraries maybe rather large so it maybe required to side load these calculations until a more viable method is supported.

Make sure that you have a good understanding of the new standards and practices with tool such as Flyway

Flyway in Energy Components

All Extensions must start with the extension.id used for the project

Cannot modify product screens

SQL code

Need to remove all references to SET_DEFINE_OFF, SET SQLBLANKLINES, SPOOL, PROMPT, etc

Need to remove all sql parameters reference from scripts such as &data_tablespace, &index_tablespace, etc.

All Extensions must have a ";" at the end of each individual SQL Block

All Extensions must have a "/" at the end of each SQL block in a script

Product tables can not be modified.

Calculation name should start with extension id, eg: zxcoe_MyCustomOilCalculation

Calculation changes are versioned migrations.

Extension Object Naming Convention

Following the naming convention in Flyway in Energy Components

You can see the scripts are ordered by name in the way they need to go into the database.

You do not name the object the same way you name the script

Naming	Example Value


EXTENSIONID

	

zxcoe




OBJECT_NAME

	

MyCustomOilCalculation




Example:

	


Base:

	

<EXTENSIONID>_<OBJECT_NAME>




Final:

	

zxcoe_MyCustomOilCalculation

File Naming Convention
Naming	Description	Example Value


VERSION

	

Flyway uses V as the standard for version scripts

	

V




MAJOR

	

The Major Number of the release

	

1




MINOR

	

The Minor Number of the release

	

0.0




UPDATE

	

A space for future items 0.0

	

0.0




EXECUTION ORDER

	

A time stamp for file creation

	

0100




EXTENSIONID

	

your extension id

	

COE




FILENAME

	

Filename

	

MyCustomOilCalculation




FILEFORMAT

	

the file format to save the script in

	

sql




Example:

		


Base:

	

V<MAJOR>.<MINOR>.<
…[truncated]


==========================================================================================
## [19/21] Expression and Scripting support
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/expression/expression-overview.html
==========================================================================================
Expression and Scripting support

Energy Components offers a versatile scripting and expression language with a syntax similar to JavaScript. The scripting functionality is powered by the Apache JEXL library.

Features

For a comprehensive overview of the JEXL syntax, refer to the JEXL Syntax Reference.

Examples
Utilizing Expression and Scripting in EC

Expression and scripting capabilities can be leveraged in various aspects of Energy Components:

Defining Event Filters: Refer to Subscribe to Events — and execute jobs and business logic for more details.

Screen Development: Data transformation can be achieved using the com.ec.frmw.jsf.service.ExpressionService service.

Argument Resolution in Screen Development, utilize the XMLResolveArgs feature as demonstrated below:

<arg name="isBlue" value="event.parameters['RetrieveArgs.nav.COLOR'] == 'blue'" valuetype="expression"/>

EC Domain Model:

The EC Domain Model can be configured to use dynamic SQL for resolving both data values and meta-attribute values. Additionally, support for using expressions (JEXL) and dynamically resolving values at the application layer is now available.
Refer to Expressions in EC Domain Model for further information, examples and how to configure it.

Standard Expression Context Objects

The EC JEXL expression engine (see ExpressionResolver) automatically provides a set of objects and namespaces in every evaluation or script execution. These let you interact with the EC platform, use utilities, and troubleshoot without manual wiring.

Core Variables
Name	Type	Provided As	Description	Example


EC

	

ECStandardContext

	

Singleton instance

	

Entry point exposing helper sub-APIs and utilities. See subordinate rows below.

	

EC.dateHelper.getNow()




EC.propertyMgr

	

PropertyServiceProvider

	

Method call

	

Access configuration / property values.

	

EC.propertyMgr.getValue('APP.VERSION')




EC.dateHelper

	

DateHelper

	

Method call

	

Date/time helper utilities.

	

EC.dateHelper.getNow()




EC.domainEntityMgr

	

DomainEntityServiceProvider

	

Method call

	

Access and query the entire EC domain model. Ref: DomainEntityMgr documentation.

	

EC.domainEntityMgr.view('COUNTRY').build().fetch() .pk().withObjectId(row.getCell('ZEX40_COUNTRY_ID').getDataValueString()) .entity().orElse(null);




EC.domainUtils

	

DomainUtils

	

Method call

	

EC Domain object utili
…[truncated]


==========================================================================================
## [20/21] EC Application Development - Overview
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/appdev/appdev-overview.html
==========================================================================================
EC Application Development - Overview

Energy Components offers a comprehensive suite of Java libraries and APIs designed to facilitate application development. These tools can be utilized when creating EC Extensions and are also employed internally by Energy Components.

EC APIs and Libraries

DomainEntityMgr - provides access to the EC Domain Model and its entities.

EventMgr - provides a generic publish-subscribe Event API.

ClientConfigurationMgr - provides management of client configurations, including secrets.


==========================================================================================
## [21/21] DomainEntityMgr
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/appdev/appdev-domain-entity-mgr.html
==========================================================================================
DomainEntityMgr

DomainEntityMgr provides a Java API that enables application-layer access to the EC Domain Model, simplifying interaction with domain entities in Java applications.

The API is designed to be easy to use, with a fluent interface that allows you to build queries and retrieve entities in a simple and intuitive way. It also provides caching of EC Domain Entities, which can improve performance and reduce the number of database queries needed to retrieve entities.

The API is made up of 3 main parts:

A View into the EC Domain Model. This represents a view of a specific domain class, allowing you to query and retrieve entities from that class.

A Key representing primary, logical or 'query' keys.

The Entity itself. This is the EC Domain Entity that you can retrieve and manipulate using the API. It strictly follows the EC Domain Model structure, meaning it has a set of attributes, metadata, relations and methods that are consistent with how the EC Domain Model is configured.

The entry point to the API is the DomainEntityMgr class, which provides methods to create views and keys, and to fetch entities. Comprehensive documentation for each component is provided in the JavaDoc within the source code.

Usage examples:
(1) Basic example:
View area = DomainEntityMgr.view("AREA").build();      // 1) Get a view of the AREA domain class.
LK lk = Key.lk().withCode("SS2_AREA").build();         // 2) Create a logical key.
Entity ss2Area = area.fetch(lk).entity().orElse(null); // 3) Get an entity by logical key.
(2) Using the 'fluent API' syntax:
Entity ss2Area02 = DomainEntityMgr.view("AREA").build().fetch().lk().withCode("SS2_AREA").entity().orElse(null);
(3) Using the fluent API, with more custom settings:
// Get the 'NAME' attribute on the 'SS2_AREA' entity from the 'AREA' class
// If not found, return "NOTHING!"
String ss2AreaName = DomainEntityMgr
       .view("AREA")                               // A view of the 'AREA' class
          .withPresCntx("/EC/my/own/presentation") // ... make sure we get metadata from this presCntx
          .withGroupModelType("geographical")      // ... make sure we use the geographical group model
          .withVersionAt("2021-01-01T00:00:00")    // ... make sure we get version valid at this date
       .build()                                    // Create the view
       .fetch()                                    // 
…[truncated]