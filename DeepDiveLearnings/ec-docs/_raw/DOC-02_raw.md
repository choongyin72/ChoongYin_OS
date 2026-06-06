# Raw content — DOC-02
Modules: ['frmw/general-config']
Pages: 25



==========================================================================================
## [1/25] Class configuration rules
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/class_configuration_rule.html
==========================================================================================
Class configuration rules

This document describes the class configuration rules that should be enforced when developing for EC. When creating or modifying classes through EC extensions, these rules are hard enforced and will fail the migration if not adhered to.

Common rules
Rule name	Valid for classtype	Description
	

OBJECT

	

INTERFACE

	

DATA

	

TABLE

	


AttributeLength

	

X

	

X

	

X

	

X

	

Max length for attribute names is 100




ClassDependencyValues

	

X

		

X

	

X

	

Class dependency type must be one of [IMPLEMENTS, ACCESS_CONTROLLED_BY]




ClassRelationValues

	

X

		

X

	

X

	

Class relation: relation type must be one of [OBJECT, OWNER, REF_CODE, GENERAL]
Class relation attribute mapping: is_main must be one of [Y, N]




DbMappingTypeIsNull

		

X

			

Interface classes cannot have dbMappingType




DbMappingTypeIsValid

	

X

		

X

	

X

	

DBMappingType must be one of [ATTRIBUTE, COLUMN, EXTENSION, FUNCTION, INNER_JOIN, LEFT_JOIN, EXT_JOIN]




DbObjectAttributeIsNotNull

	

X

				

Versioned object classes must have dbObjectAttribute (Attribute table)




DbObjectAttributeIsNull

		

X

	

X

	

X

	

Class can not have dbObjectAttribute (Attribute table)




DbObjectNameIsNotNull

	

X

		

X

	

X

	

Class must have must have Db Object Name (Main table)




DbObjectNameIsNull

		

X

			

Interface classes cannot have Db Object Name (Main table)




DbObjectTypeIsNull

		

X

			

DbObjectTypeIsNull




DbObjectTypeMappedCorrectlyToDb

	

X

		

X

	

X

	

DbObjectType must correspond to actual table or view in db




DbSqlSyntaxIsNull

		

X

			

Interface classes cannot have dbSqlSyntax




ExtAttrDbSqlSyntaxIsNull

	

X

	

X

	

X

	

X

	

Attribute with mapping type EXTENSION cannot have dbSqlSyntax




InvalidObjectClassAttributes

	

X

				

OBJECT_CODE and START_DATE cannot have mappingType COLUMN




NoAttributeMapping

			

X

	

X

	

TABLE and DATA classes cannot have attributes with ATTRIBUTE mappingtype




ObjectIdIsOnlyKey

	

X

	

X

			

Only OBJECT_ID can be key




OwnerClass

			

X

		

Data classes must have OWNER class




RequiredDataClassAttributes

			

X

		

Data classes must have OBJECT_ID




RequiredObjectClassAttributes

	

X

				

Versioned objectclasses must have these attributes and corresponding datatypes and mappings :

OBJECT_ID, STRING, [COLUMN,FUNCTION]

CODE, STRING, COLUMN

OBJECT_START_DATE, DATE, COLUMN

OBJECT_END_DATE, DATE, COLUMN

DAYTIME, DATE, ATTRIBUTE

NAME, STRING, [ATTRIBUTE,FUNCTION]

END_DATE, DATE, ATTRIBUTE

Invariant objectclasses must have these attributes and corresponding datatypes and mappings :

OBJECT_ID, STRING, [COLUMN,FUNCTION]

CODE, STRING, COLUMN

OBJECT_START_DATE, DATE, COLUMN

OBJECT_END_DATE, DATE, COLUMN

NAME, STRING, [COLUMN,FUNCTION]




RowSortOrderIsValid

	

X

		

X

	

X

	

ROW_SORT_ORDER property must have property-type="APPLICATION" and must be a positive integer.




RowSortPriorityIsValid

	

X

		

X

	

X

	

ROW_SORT_PRIORITY property must have property-type="APPLICATION" and must be one of : [ ASC, ASC_NULLS_FIRST, DESC, DESC_NULLS_LAST ]




TimeScopeCodes

	

X

				

TimescopeCode must be one of : [ VERSIONED, INVARIANT ]




TimeScopeCodes

		

X

			

TimescopeCode must be one of : [ VERSIONED, INVARIANT, NONE ]




TimeScopeCodes

			

X

	

X

	

TimescopeCode must be one of : [ NONE, EVENT, DAY, WEEK, MTH, QTR, YR, HR_1, HR_2, SAMPLE ]




ValidClassType

	

X

	

X

	

X

	

X

	

Classtype must be one of : [ OBJECT, DATA, TABLE, INTERFACE, REPORT, META ]




ViewLayerPresentationContext

	

X

	

X

	

X

	

X

	

VIEWLAYER properties must have presentationContext=/

Extension rules

Additional rules that only apply to extensions.

Rule name	Valid for classtype	Description
	

OBJECT

	

INTERFACE

	

DATA

	

TABLE

	

INTERFACE

	

REPORT

	


AttributePrefix

	

X

	

X

	

X

	

X

	

X

	

X

	

Attribute names must be prefixed with extension id




DbObjectAttributePrefixAndLength

	

X

						

dbObjectattribute must be prefixed with extension id if table belongs to extension, max length is 100 characters




DisabledIndicator

	

X

	

X

	

X

	

X

	

X

	

X

	

…[truncated]


==========================================================================================
## [2/25] Class Configuration Structure
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/class_configuration_structure.html
==========================================================================================
Class Configuration Structure
Introduction

This document contains a short summary of rules and valid properties for configuring the new class tables introduced in EC-11.2 and modified in EC 13.1.0. It assumes that you are familiar with the old class tables, and focuses primarily on what is new or changed, and describes how to utilize the new dimensions. For a more complete background for the class model, please refer to the EC View Generator and Class Model

Data Model

In the class model, there is a distinction between the domain model tables and the property tables.

The five domain model tables define the classes, their attributes, relations, dependencies, and trigger actions. The domain model tables have a single entry per class, class attribute, class relation, etc. Each entry belongs to an application space that is identified by the APP_SPACE_CNTX field. Projects and templates can extend the domain model by adding new classes. They can also add new attributes, relations, etc. to existing classes.

The property tables extend the domain model with additional features. They are designed to allow customer projects and templates to override product settings by inserting new values with a higher priority (see below for details).

Figure 1. Class relation data model
Domain Model

In the old class model, there were no clear rules regarding which domain model fields you could change. In the new structure, we want to move towards stricter rules and more standardization in what should be changed in the class domain definition. As a guiding principle, customers should not overwrite the product domain model entries. It is still technically possible to overwrite the columns in the domain model tables, but such changes will not be preserved in an upgrade. Consequently, projects must handle such overwrites manually themselves (as they have been doing before EC 11.2).

The set of rules defined below describes the ideal situation that we are striving towards.

Any Class definition in the domain model belonging to a Product APP_SPACE_CNTX (EC_FRMW, EC_PROD, EC_TRAN, EC_SALE, EC_REVN, EC_ECDM, EC_BPM) should not be changed by others.

It is still supported and expected for others to define their own classes, add class attributes and class relations to product classes, but these must be defined with an APP_SPACE_CNTX reflecting the owner of these rows, and not use Product values.

When defining your own classes, try to follow the usage pattern defined here:

Store user-defined classes in separate tables, typically starting with Z_

Map the Class to physical tables if possible, try to avoid defining classes on top of other classes.

For object classes, try to avoid constructs where the same object (object_id) belongs to several different classes. If the table contains a class_name column, use that as the distinction criteria between objects belonging to different classes

When adding new class attributes to existing Product classes:

Map Project and template class attributes to the columns reserved for this (TEXT_xx, Value_xx, Date_x)

If you are adding virtual attributes (functions) to a class, keep in mind the performance impact, especially if the attribute can be used in a where clause. Consider if the new Join attribute is an alternative for you here.

Property Tables

The four property tables contain many of the properties that were earlier stored directly on the classes, attributes, relations, and trigger actions. These are the properties where we expect that projects may want to override the product default values. To have a clearer separation on the configuration that can be done for these, there is established a table structure with a set of property_codes and property_values, where it becomes much clearer and easier to have a different class configuration for product, templates, and projects, and to do upgrades on all levels independently. Valid property codes for each property table are defined in table class_property_codes.

There are basically 2 dimensions where it is possible to keep an override property value:

OWNER_CNTX is a numeric value where the highest value is the one being active. The product usually defines its pr
…[truncated]


==========================================================================================
## [3/25] Class model presentation syntax guidelines
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/class_model_presentation_syntax_guidelines.html
==========================================================================================
Class model presentation syntax guidelines
Introduction
Figure 1. Class relation data model

The EC-11.2 release introduced four property tables, related to the class model. The EC-13.1.0 release updated the class model and replaced some of the tables.

The property tables are designed to support a clear separation between product, template, and asset configuration. In this model, individual property values are stored as separate rows. Templates or assets that want to override an individual property value can do so by inserting a new value for the same property with a higher owner context number. The property value with the highest owner context will “win” – i.e. will hide the values in lower contexts.

EC-11.2 also introduced a “directory” of valid property codes. Valid property codes and types were defined in the class_property_codes table, but the "rules" set out in this table were not enforced. From EC-11.2-SP02, the rules are enforced by a set of triggers on the property tables. The triggers raise an application error if the following rules are not adhered to:

The property code and type must be a valid combination for the table in question

The property value string must represent an integer number if the data type is NUMBER

The property value must be “Y” or “N” if the data type is BOOLEAN and the property type is VIEWLAYER or APPLICATION

The property value must be “true” or “false” if the data type is BOOLEAN and the property type is STATIC_PRESENTATION or DYNAMIC_PRESENTATION

Prior to EC-11.2, both static and dynamic presentation properties were defined as a semi-colon separated string of key-value pairs:

In EC-11.2 the static presentation syntax was converted into individual property values, but the dynamic presentation syntax was left as-is:

In EC-11.2-SP02, most of the dynamic presentation syntax has been converted to individual property values as well:

The PresentationSyntax property is still supported from EC-11.2-SP02 and onwards, however (i.e. semi-colon separated string of key-value pairs) have the potential to cause issues as described in the next section. It is thus recommended to remove them.

Caveats

Splitting the dynamic PresentationSyntax into individual properties can have an upgrade impact. Let’s say that EC-10.4 has a class attribute with the following PresentationSyntax:

An asset that wanted to increase the width of the attribute to 140 would update the PresentationSyntax value:

After an upgrade to EC-11.2_SP02, the product PresentationSyntax has been converted to individual properties with owner context 0:

The upgrade scripts will not convert the asset level PresentationSyntax to individual properties, however. So after the upgrade to EC-11.2-SP02, the following property values will be defined:

The EC application does not interpret the PresentationSyntax with owner context 1100 as an override of the two individual properties with owner context 0. Both sets of property values will be visible to the EC application, and the ambiguity is “resolved” by picking an arbitrary value.

To disambiguate cases such as this one, templates and assets should split their dynamic PresentationSyntax strings into individual properties. I.e. Override the relevant individual property instead of overriding all properties in the concatenated PresentationSyntax string.

Guidelines

Please consider the following guidelines when new presentation properties are defined:

Favor static over dynamic presentation when the property value does not change

Instead of

I.e. viewhidden is configured as a dynamic property, but the value is hard-coded to true, which is static and does not need object-level evaluation.

Use

Instead of

I.e. multiple static properties are configured as dynamic property - they should be split into individual static properties.

Use

Favor individual dynamic properties over dynamic PresentationSyntax

Instead of

Use

The main driver for splitting the PresentationSyntax into individual properties is to enable individual overrides.

Avoid returning dynamic PresentationSyntax from DB functions if possible

Consider the following example:

CREATE OR REPLACE PACKAGE BODY EcDp_Example IS

FUNCTION 
…[truncated]


==========================================================================================
## [4/25] Group model configuration in Energy Components
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/group_model_configuration_in_ec.html
==========================================================================================
Group model configuration in Energy Components
Background

Energy Components (EC) is a highly configurable system very much because of a logical abstraction layer we call "the View layer", that allows us to have a separation between business objects and physical storage structure in the database. It allows us to change existing business objects dynamically and to offer generic concepts like locking, row level access, four eyes approval etc. as configurable options on most business objects.

The view layer is defined in a set of meta data we call Classes (see EC View Generator and Class Model). One category of these classes is called Object Classes and represents what is defined as Master Data that is more static than the transitional data representing daily measurements. Object classes are often representing hierarchies within the system, that can be used to navigate down to a certain detail level or navigate up to find where an object belongs in the system. Since Object classes in EC by definition are versioned, it means that relations can change over time, and it can be time consuming to do a lookup in a normalized data model every time a user needs to navigate the hierarchy either in screens, allocation-read or for reporting.

The Group model concept was introduced in EC almost 20 years ago, to improve the performance especially related to Allocation read. The philosophy was to resolve more of the complexity in the object class hierarchy when master data and master data relation are changed, and store some more redundant data on the lower level in the object hierarchies, to simplify the queries needed during daily operations. This is achieved by a special set of class relations that is defined to be part of a named group model. This is a feature in the EC Framework that is used by other parts of the product, but also customer templates and projects can use it to make their own group models.

Data Model considerations

The implementation and support for this have been relatively unchanged for many years, but now there are several reasons to make some adjustments to the model.

With the introduction of The Extension concept, the possibility to make user defined group models based on the old implementation is not possible.

In the growing set of separate packages (Regulatory Reporting, Midstream, Upstream, EC Smart) running on top of the core product, any use of package owned group model involving product classes is not possible without violating extension principles or using columns reserved for customer group models.

The group model synchronization is partly done in the generated IUD trigger for object classes and in a set of generated trigger packages (ECTP). Over time the IUD triggers have gotten more and more complex as we have added new functionality around 4 eyes approval, row level security, locking etc., and it is all intermingled in the same code base, making it hard to maintain and add new functionality.

The old model has some special cases handled by hardcoding and assumption around naming, that makes the solution less generic than it needs to be.

We also see that the group model concept has been used in ways that are not entirely within the rules and limitations that were set up when the original concept was made, and even if it apparently has been working in most of these cases these are challenges with creative utilization of the model.

These are the main drivers behind the changes and new possibilities described here. Both the new and the traditional group model will be discussed in detail under and hopefully give an understanding both of the possibilities and limitation in the models. There is still a need to be backward compatible with the traditional group model. The new model was introduced in EC 12.2.9, but in this version, it was by default turned off. This was done so that all existing system on the EC 12.2.x series would run with the traditional group model unless it is actively switched over to use the new model on a higher owner_cntx level.

Traditional handling of project specific data model additions in EC

Until recently the way to extend product classes was to use some of the generic colum
…[truncated]


==========================================================================================
## [5/25] How to Correct Object Class IUD Triggers
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/how_to_correct_object_class_IUD_triggers.html
==========================================================================================
How to Correct Object Class IUD Triggers

This article will explain in short how to adjust class configuration in accordance with the new structure of object class IUD trigger introduced in the EC 13.0.0 release. For more information about the relevant changes, see Group model configuration in Energy Components

With EC 13.0.0, we have changed the structure of object class IUD triggers, which means that there is a chance some user defined class trigger actions and journaling rules must be modified slightly in order to function as before. For object classes, the n_- and o_- variables and the version table (vt) that used to be declared in the generated IUD trigger have been replaced by two new structures nct (new class table) and oct (old class table):

OLD	NEW

CREATE OR REPLACE TRIGGER IUD_AREA
 INSTEAD OF INSERT OR UPDATE OR DELETE ON OV_AREA
FOR EACH ROW
-- Generated by ecdp_viewlayer
DECLARE
   ...

   lv2_operation           VARCHAR2(30);
   lb_datechange           BOOLEAN := FALSE;
   lr_version_row          GEOGR_AREA_VERSION%ROWTYPE;
   lr_curr_main_row         GEOGRAPHICAL_AREA%ROWTYPE;
   lr_curr_version_row      GEOGR_AREA_VERSION%ROWTYPE;
   vt                       EcTp_AREA.ver_tab_type := EcTp_AREA.ver_tab_type();
   lb_new_version            BOOLEAN := FALSE;
   lv2_code_changed          VARCHAR2(1) := NULL;
   n_record_status           VARCHAR2(1);
   n_rev_text                VARCHAR2(4000);
   n_created_by              VARCHAR2(30);
   o_created_by              VARCHAR2(30) := :OLD.created_by;
   n_created_date            DATE;
   ...
BEGIN
	
CREATE OR REPLACE TRIGGER IUD_AREA
 INSTEAD OF INSERT OR UPDATE OR DELETE ON OV_AREA
FOR EACH ROW
-- Generated by ecdp_viewlayer
DECLARE
   nct    ECC_AREA.class_tab_type := ECC_AREA.class_tab_type();
   oct    ECC_AREA.class_tab_type := ECC_AREA.class_tab_type();

BEGIN

As a result of this, it is no longer possible to reference the n- and o- variables or the vt table representing the physical version table for the class, but the same values are available in the nct and oct table structures for all class attributes and relations that are enabled. Therefore, all references to n_, o_ and vt must be changed as shown in the examples below:

Example 1:

Example 2:

Example 3:

Notice that:

nct- table initially will have 1 row representing the values of the :new row, but like the old vt (version table), group model synchronization can result in several rows (versions) if aligning with parent versions are needed.

oct- table will always have only 1 row, on insert all the values in this table will be null.

p_nct and p_oct should always be followed by the logical name of the attribute, and not the db_sql_mapping, i.e p_nct(1).<attribute name> or p_nct(1).<role name>_id / p_nct(1).<role name>_code for relations.

You can still refer to :NEW.<attribute> and :OLD.<attribute> for class trigger actions, but not for journal rules:

The class property configuration journal rule (JOURNAL_RULE_DB_SYNTAX) can no longer contain the :NEW or :OLD prefixes, as they have been moved out of the class IUD trigger and into the class package. This means class journal rules must be altered from :new to p_nct(1), and :old to p_oct(1) as shown below:

Example:

After the product Flyway migration to EC 13.0.x has taken place, the IUD triggers for object classes will be based on the new concept. If the database you are upgrading contains additional Class Trigger Actions (CTA) for existing object classes, there is a chance that the IUD triggers for these object classes will be invalid. This is because the references over will not be loaded until the owners class definitions have been loaded and build viewlayer has been run at the end of the given Flyway migration queue. This is not a problem as long as the generated view is not actively used in a version script before the repeatable scripts are loaded. However, if version scripts are doing inserts or updates against an OV-view that has an invalid CTA, that version script has to be updated to fix the reference and rebuild the given object class (IUD trigger) before the version script can operate on the generated OV class. This illustrates how the co
…[truncated]


==========================================================================================
## [6/25] Class General Relations
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/class_general_relation.html
==========================================================================================
Class General Relations
Introduction

The main objective of this document is to provide guidelines for developers and projects on what general relations in the EC model is, what it can be used for and the impact and considerations they need to look out for when upgrading an older system.

The reason for introducing general relations

The main reason for introducing a new type of class relation into the EC class concept is:

To support defining logical keys and hide the complexity of system generated surrogate keys

It is mainly intended for configuration tools, rest API, sql script to use when inserting, updating and deleting.

It makes it possible for external callers to do these operations based on logical keys, rather than including system generated surrogate keys that can be different within database instances.

Inside an EC system using the physical database keys including surrogate keys will usually be the most efficient way to operate on the data.

New features

general relations possibilities

new end points in rest API

extensions to xml format

Known limitations

Support for the general relation concept is introduced in EC 13.1, and general relations have been added to some product owned classes as part of that release. However, there are many more product classes where we want to add logical keys and general relations.

To be able to do this it is important for product to be in control of the defined logical keys on product owned classes, there has therefore been build in restrictions in the extension framework, to prevent these from adding/extending logical keys on classes that are owned by the EC product.

We know that it is not ideal that all useful logical keys and general relation are not in place on product classes, but with over 1000 cases to consider this will take some time. Ways to influence the priority here are:

Register a jira to request new specific logical keys and general relations

Contact product team owning the classes to discuss options

Technical implementation

Introducing "general relations" in the EC class model is an extension of the existing relations that are possible to define in the model. The new needs did however not fit directly into the existing data model so the data model have been consolidated to have one set of tables supporting the different relations between classes.

Backward compatibility

Even if the physical storage structure for class meta data is changed, it has been important that existing class definitions expressed in Class XML files should still be supported.

In line with the class loader, transformers have been made to convert the old to the new format.

In the XML file both the old and the new class relation format can coexist. New general relations will however need to be expressed in the new format.

General relations structure in XML

The class definition in the Class XML files is backward compatible, so there should be no need to change the class definition unless you want to add new general relations in your owner context. This means that the old and new way of defining Class relation can coexist both within one XML file, and on different owner context for the same class. The translation to the new data model is done by transformers used by the class loader.

However, if you want to utilize the new possibilities and define a new general relation, it has to be expressed in a new syntax detailed under.

The information under is meant as background information for settings where it is needed to operate directly on the Class XML files.

How to define general relations in the EC class model

Consider the following example describing the relations between T_Basis_Application, T_Basis_Object, T_Basis_Role and T_Basis_Access. Earlier the only way to make references was by the surrogate keys:

TV_T_Basis_Application.app_id → TV_T_Basis_Object.app_id

TV_T_Basis_Application.app_id → TV_T_Basis_Role.app_id

TV_T_Basis_Application.app_id → TV_T_Basis_Access.app_id

TV_T_Basis_object.object_id → TV_T_Basis_Access.Object_id

TV_T_Basis_Role.role_id → TV_T_Basis_Access.role_id

TV_T_Basis_Level.level_id → TV_T_Basis_Access.level_id

These are marked in the diagram under
…[truncated]


==========================================================================================
## [7/25] Date integrity check for object relation
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/class_relation_date_integrity.html
==========================================================================================
Date integrity check for object relation
Introduction

The EC Class model has integrity checks on object relations defined in the view layer. This includes checking that dates on related data are within the life span of the object class. Many of these checks and constraints make sense to ensure data integrity, but not all.

A new class relation property is added to make it possible to configure the date integrity check: ENFORCE_DATE_CHECK

It can have the following property values:

Property Value	Description


STRICT

	

Parent object needs to be valid in all child objects life span but can start before and have end date after child objects lifespan.




IGNORE_NULL

	

Same as STRICT, but allow child objects to have NULL for OBJECT_END_DATE when setting the parent object end date.




OVERLAP

	

Parent object needs to be valid in part of child objects life span. I.e. Parent and child must overlap each other.




NONE

	

No object life span check.

Example - No object end date set for parent and child
Figure 1. No object end date
Set object end date for parent
Figure 2. Update Parent object end date
Property Value	Description


STRICT

	

It is not allowed to set the parent object end date to be before the child object end date.




IGNORE_NULL

	

It is allowed to set the parent object end date. Child object end date is null and is ignored.




OVERLAP

	

It is allowed to set the parent object end date. Parent and child overlap each other.




NONE

	

It is allowed to set the parent object end date. Date integrity check is ignored.

Set object end date for child class
Figure 3. Update child object end date
Property Value	Description


STRICT

	

It is allowed to set the child object end date when the parent object end date is not set.




IGNORE_NULL

	

It is allowed to set the child object end date when the parent object end date is not set.




OVERLAP

	

It is allowed to set the child object end date. Parent and child overlap each other.




NONE

	

It is allowed to set the child object end date. Date integrity check is ignored.

Example - object end date set for parent object
Figure 4. Object end date set for parent
When inserting and parent has object end date set, child class doesn’t need to have object end date set as long as it is not part of a group model.
Set object end date for parent class
Figure 5. Update parent object end date
Property Value	Description


STRICT

	

It is not allowed to set the parent object end date to be before the child object end date.




IGNORE_NULL

	

It is allowed to set the parent object end date. Child object end date is null and is ignored.




OVERLAP

	

It is allowed to set the parent object end date. Parent and child overlap each other.




NONE

	

It is allowed to set the parent object end date. Date integrity check is ignored.

Set child object end date to be before parent object end date
Figure 6. Update child object end date to be before parent object end date
Property Value	Description


STRICT

	

It is allowed to set the child object end date to be before parent object end date.




IGNORE_NULL

	

It is allowed to set the child object end date to be before parent object end date.




OVERLAP

	

It is allowed to set the child object end date. Parent and child overlap each other.




NONE

	

It is allowed to set the child object end date. Date integrity check is ignored.

Set child object end date to be after parent object end date
Figure 7. Update child object end date to be after parent object end date
Property Value	Description


STRICT

	

It is not allowed to set the child object end date to be after the parent object end date.




IGNORE_NULL

	

it is not allowed to set the child object end date to be after the parent object end date.




OVERLAP

	

It is allowed to set the child object end date. Parent and child overlap each other.




NONE

	

It is allowed to set the child object end date. Date integrity check is ignored.

Example - object end date set for child object
Figure 8. Object end date set for child
Set parent object end date equal child object end date
Figure 9. Update parent object end date to be equal to child object end date
Property V
…[truncated]


==========================================================================================
## [8/25] EC View Generator and Class Model
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/ec_view_generator_and_class_model.html
==========================================================================================
EC View Generator and Class Model
Introduction

This section introduces the Energy Components (EC) Data Services View Generator – what it is, what it does and how it relates to the EC Class Model. The fundamentals of the EC Class Model are also covered.

Disclaimer


This document is meant to give an overview of the EC Class Model, and illustrate the main way the concepts work. References have been updated to the adjusted class model that came in EC 11.2, but it is not given that all code examples are kept in sync with the live generated code. There are also details and possibilities in the class concept that are not described in this document.

Flexibility

The traditional Entity-Relation design approach to modelling data tends to require that everything about those data is known prior to modelling a concept, and once modeled, it becomes very difficult to change. Experience in the Energy Components domain shows that a more generic and flexible modelling approach enables us to better reflect our business knowledge as we learn more and as the business changes over time. We have seen that the need for data model changes continues to be high. We have experienced structures that we thought would be stable, turn out not to be valid anymore, e.g. that a well is part of a facility, whereas in reality, a well could switch facility.

In light of these insights, our approach is to move away from explicit structures to more generic data structures, termed the EC Class Model.

Abstraction

Currently, database tables are exposed directly to the various application parts. This makes it very difficult to build in common functionality to be shared by all parts of the application, e.g. EC provides a mechanism for creating an audit trail (the journal tables) by using database triggers. This is an example of functionality which is "hidden" from the application developer. In the same way, there are many areas where such functionality can be offered from the database, fully transparent to the application. In this way, we can simplify application development and ensure consistency, independent of front-end technology.

The approach is to offer, from the database, an access layer above the actual tables. This layer is referred to as EC Data Services. The definition of this access layer follows the object class definition (it is generated from the object class definition). The approach is to have the object classes (and hence the access layer) grouped according to product context, referred to as an EC App_Space_Cntx, e.g. EC Production could represent one App_Space_cntx.

The access layer takes the form of a set of views, generated automatically from the object class definitions.

Generic components

Experience has shown that parts of the EC application can be developed in a generic way so that configuration parameters control system behaviour. Examples of this are the allocation engine, configuration application, visual configurations, formula editors, generic check/validation rules etc. When developing generic components, we need to have a more generic way to access data as we have learned that using natural keys (the normal approach in ER / Relational databases), severely prevents us from making good generic code. The approach is to define a generic access layer, the GenAppSpace (which cannot "see" any of the other AppSpaces). As part of this approach, all objects in EC shall have a unique global identifier.

The EC Data Services Class Model

This section sets out the fundamentals of the Object Class Model, in order that these can be referred to in the subsequent description of how the View Generator works.

The principle elements of interest are Classes, Objects, and Attributes.

A Class is a high level definition of something, but does not include any data referring to an actual example of that Class, e.g. a car could be defined as a Class.

Attributes of a Class are the characteristics or properties of the Class, e.g. make, model, engine size, color, number of seats, and body style could all be attributes of the Car Class.

Classes, together with their attributes, can be thought of as templates which provide a complete description of an ite
…[truncated]


==========================================================================================
## [9/25] Simplified configuration for EC Codes and other popup attributes
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/simplified_configuration_for_ec_codes.html
==========================================================================================
Simplified configuration for EC Codes and other popup attributes

EC-12.0 and later versions simplify the configuration of class attributes where values are defined by an EC code type. Prior to EC-12.0, the relationship between the attribute and the EC code type was not explicitly captured in the class model. It was indirectly defined by the query XML file in combination with other properties.

EC-13.1.0 introduced general relation to capture such relationships.

Example - STREAM.STREAM_PHASE 


Between EC 12.0 and EC 13.0.x such relation could be capture in class_attribute_cnfg using column reference_type, reference_key and reference_value. These columns are removed in EC 13.1.0.


Prior to EC-12.0 the above relationship was modeled/configured using the following static presentation properties:

Example - STREAM.STREAM_PHASE (EC-11.2_SP03)

The reference to the EC code table class is "hidden" inside the PopupQueryURL document.

A class relation that specifies RELATION_TYPE = CODE_REF and optional FILTER_KEY and FILTER_VALUE will automatically get consistent and sensible default values for these presentation properties. In EC-12.0+ you do not need to specify individual Popup* properties in order to get an EC code attribute rendered as a popup on the screen. It is sufficient to create a class relation with relation type = CODE_REF as indicated above. An added benefit is that the REST-API is aware of this (the REST-API does not evaluate the Popup* properties).

The following classes can be used as ref class in a CODE_REF class relation:

EC_CODES

UNIT_REF

COMPONENT_SET_REF

HYDROCARBONCOMPONENT_REF

TRANS_TEMPLATE_REF

A TABLE class that satisfies the following requirements can be used as a reference type:

The class must have a CODE attribute of type STRING.

The class must have a NAME attribute of type STRING.

The class must have a SORT_ORDER attribute of type STRING or NUMBER.

The CODE attribute must have a REF_DB_PRES_SYNTAX property.

The class can have additional columns that will be used for filtering (i.e. as FILTER_KEY).

Attributes that have a mapping to a class relation with relation type CODE_REF will be rendered as a popup and have the following properties:

Property	Value


PopupQueryUrl

	
<data>
   <query>
      <distinct>true</distinct>
      <fromdate>1000-01-01T00:00:00</fromdate>
      <todate>9999-01-01T00:00:00</todate>
   </query>
   <class name="$REFERENCE_TYPE$"/>
   <object name="$REFERENCE_TYPE$">
      <property name="$REFERENCE_KEY$"
                datavalue="$REFERENCE_VALUE$"
                operator="="/>
   </object>
   <sort name="$REFERENCE_TYPE$">
      <property name="SORT_ORDER" order="ASC"/>
   </sort>
</data>

Example:

<data>
   <query>
      <distinct>true</distinct>
      <fromdate>1000-01-01T00:00:00</fromdate>
      <todate>9999-01-01T00:00:00</todate>
   </query>
   <class name="EC_CODES"/>
   <object name="EC_CODES">
      <property name="CODE_TYPE"
                datavalue="STREAM_PHASE"
                operator="="/>
   </object>
   <sort name="EC_CODES">
      <property name="SORT_ORDER" order="ASC"/>
   </sort>
</data>

The where clause will be omitted if the REFERENCE_KEY is blank.




PopupLayout

	

The layout XML document containing all enabled and visible attributes of the REFERENCE_TYPE class ordered by ascending SCREEN_SORT_ORDER.




PopupDependency

	
Screen.this.currentRow.<attribute_name>=ReturnField.CODE

Example:

Screen.this.currentRow.STREAM_PHASE=ReturnField.CODE
Screen.this.currentRow.WELL_TYPE=ReturnField.CODE
Screen.this.currentRow.DENSITY_VOLUME_UOM=ReturnField.CODE



PopupReturnColumn

	

NAME

Comment:
The STREAM_PHASE value returned from the popup to the screen cell is the NAME of the selected EC_CODES. E.g. the referring cell will display Water and not WAT.




DB_PRES_SYNTAX

	

The DB_PRES_SYNTAX property of the "referring class attribute" will be defaulted from the REF_DB_PRES_SYNTAX of the "ref class name CODE".

Example:

STREAM.STREAM_PHASE is the "referring class attribute".

EC_CODES.CODE is the "reference type CODE".

The DB_PRES_SYNTAX for STREAM.STREAM_PHASE will be derived from the REF_DB_PRES_SYNTAX of EC_CODES.CODE with the follow
…[truncated]


==========================================================================================
## [10/25] Configuring Tooltip functionality in EC
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/configuring_tooltip_functionality_in_ec.html
==========================================================================================
Configuring Tooltip functionality in EC

In this section, you will learn how to configure Tooltip functionality in EC.

Tooltip in Data Section

In this example, we are configuring tooltip functionality for the AVG_WH_TEMP attribute on the PWEL_DAY_STATUS class.

Insert a new property with Property Code = ‘verificationText’, Owner Context, Presentation Context, Property Type = ‘Dynamic Presentation’ and Property Value = ‘<The call function as per the requirement>’.

<class-ref version="1.0" class-name="PWEL_DAY_STATUS" owner-cntx="<owner_cntx>">
    <properties>
        <class-attribute-ref attribute-name="AVG_WH_TEMP">
            <class-attr-property-cnfg property-code="verificationText" property-type="DYNAMIC_PRESENTATION" presentation-cntx="/EC">
                <property-value>ecdp_tagid.GetTagID(DV_PWEL_DAY_STATUS.CLASS_NAME,DV_PWEL_DAY_STATUS.OBJECT_CODE,'AVG_WH_TEMP')</property-value>
            </class-attr-property-cnfg>
        </class-attribute-ref>
    </properties>
</class-ref>

In our example, the call function is: ecdp_tagid.GetTagID(DV_PWEL_DAY_STATUS.CLASS_NAME,DV_PWEL_DAY_STATUS.OBJECT_CODE,'AVG_WH_TEMP'). This is a package made for this example that shows the tag id connected with the attribute and well.

Open the Daily Production Well Status 1 screen.

Enter navigator values and hit go.

Hover your mouse cursor over the attribute. You will see a tooltip displaying the ID of the tag which is fetching the value for the particular attribute.

The package used in this example:

CREATE OR REPLACE PACKAGE EcDp_TagID IS

FUNCTION GetTagID(p_class_name VARCHAR2, p_object_code VARCHAR2, p_attribute VARCHAR2) RETURN VARCHAR2;

END EcDp_TagID;
/
CREATE OR REPLACE PACKAGE BODY EcDp_TagID IS

  FUNCTION GetTagID(p_class_name VARCHAR2, p_object_code VARCHAR2, p_attribute VARCHAR2) RETURN VARCHAR2 IS

    CURSOR c_key(cp_class_name VARCHAR2,cp_attribute VARCHAR2, cp_object_id VARCHAR2) IS
           SELECT tag_id
             FROM TRANS_MAPPING
            WHERE DATA_CLASS = cp_class_name
              AND ATTRIBUTE = cp_attribute and PK_VAL_1 = cp_object_id;

    lv2_tagid VARCHAR2(240) := '';
    lv2_object_id VARCHAR2(240);

  BEGIN

    lv2_object_id := ec_well.object_id_by_uk(p_object_code);
    FOR curKey IN c_key(p_class_name,p_attribute,lv2_object_id) LOOP
      lv2_tagid := curKey.tag_id;
    END LOOP;

    RETURN lv2_tagid;

  END GetTagID;

END;
/
Tooltip in EC Codes Dropdown

EC is enhanced to support tooltip on dropdown that uses EC Codes for any screen.

The tooltip displayed is the description of the EC Codes entered either in EC Codes - Non-System Codes (CD.0034), EC Codes - System Codes (CD.0084) or EC Codes - All (CO.1011).

There are two ways to enable the tooltip for EC Codes dropdown. It depends on how the EC Codes have been configured in the class:

EC Codes by using EC Codes Popup (with popupLayout ‘/com.ec.frmw.co.screens/layout/ec_code_popup.xml’)

EC Codes by using EC Code Ref

Step 1:

EC Codes by using EC Codes Popup

Enable the tooltip by adding a new class attribute property verificationText for CODE_TEXT attribute in EC_CODES_POPUP class.

owner_cntx: Owner Context should be the owner context decided for the project (0 is only used for product).

presentation_cntx: Presentation Cntx should be screen xhtml. For example, it should be '/EC/com.ec.prod.pd.screens/well_deferment' for Deferment screen. This can be applied to all of EC by using '/'.

<class-ref version="1.0" class-name="EC_CODES_POPUP" owner-cntx="<owner_cntx>">
    <properties>
        <class-attribute-ref attribute-name="CODE_TEXT">
            <class-attr-property-cnfg property-code="verificationText" property-type="DYNAMIC_PRESENTATION" presentation-cntx="/EC/com.ec.prod.pd.screens/well_deferment">
                <property-value>DESCRIPTION</property-value>
            </class-attr-property-cnfg>
        </class-attribute-ref>
    </properties>
</class-ref>

EC Codes by using EC Codes Ref

Enable the tooltip by adding a new class attribute property verificationText for NAME attribute in EC_CODE_REF class.

owner_cntx: Owner Context should be the owner context decided for the project (0 is only used for product).

present
…[truncated]


==========================================================================================
## [11/25] How to configure Smart Journaling
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/how_to_configure_smart_journaling.html
==========================================================================================
How to configure Smart Journaling
Abstract

The EC application has for many years supported journaling of old data values when changes are made to a row in the database.

The challenge with this solution has been that it also copies and stores rows that can be considered to be "noise" because it gives no additional information. Typically empty instantiated records, data capture updates to empty columns, etc.

The Smart journaling tries to minimize the journaling by excluding some of the cases where journaling is not needed. It also addresses the need for recording revision text on deleted rows.

Requirements Addressed

Avoid journaling for records created by system users (instantiated rows), based on user id stamp on the old record. There is a defined list of these users (1).

Avoid journaling when a record is updated by defined system users (i.e. Transfer) defined in another system user list (2), and the old record is also last updated by the same system user.

The lists of system users under 1 and 2 are independent lists and can contain one or more defined system users each.

When a record is deleted, this should always result in a new journal entry including the revision text entered for the deleted record.

The journal entries created as a result of delete in the EC client should have JN_OPERATION=DEL.

Configuration

The behavior and requirements above can be achieved in EC by configuring the following system attributes in CTRL_SYSTEM_ATTRIBUTE.

Attribute Name	Default Values	Comments


JOUR_USER_EXCL_OLD

	

'SYSTEM, INSTANTIATE'

	

List (1) of the user where journaling will not be done, ref. req. 1 (above).




JOUR_USER_EXCL_NEW

	

'TRANSFER'

	

List (2) of the user where journaling will not be done, ref. req. 2 (above).




JOUR_USER_EXCL_OLD_IND

	

N

	

The flag that determines if the JOUR_USER_EXCL_OLD list is used or not.




JOUR_USER_EXCL_NEW_IND

	

N

	

The flag that determines if the JOUR_USER_EXCL_NEW list is used or not.

In the default configuration, journaling will behave as for previous versions of EC. The projects will actively have to turn on and configure these to get the new Smart Journaling functionality.

The exception is the journal entry for deleted records (ref. requirement 4). Delete in the client will make the DAO trigger an update to set rev_text before it does the delete against the class.

Note that when changes are done to the 4 attributes listed here, the View layer needs to be regenerated before the new configuration applies.

Since the lists of system users are generated into the Instead of triggers, you should try to keep the number of system users in each list down to a reasonable level (<10).

Example 1 - Data class

Consider the following operations done to a given row in DV_PWEL_DAY_STATUS.

Operation	Change	Who	Comment


Insert

	

Empty row

	

INSTANTIATE

	

System user (list 1)




Update

	

ON_STREAM_HRS = 12

	

BILL

	

Normal user




Update

	

ON_STREAM_HRS = 14

	

TRANSFER

	

System user (list 2)




Update

	

ON_STREAM_HRS = 16

	

TRANSFER

	

System user (list 2)




Update

	

ON_STREAM_HRS = 24

	

BILL

	

Normal user




Delete

	

Set Rev_text and delete row

	

BILL

	

Normal user

After these operations, the row will no longer exist in the normal view DV_PWEL_DAY_STATUS, but the history of the row can be found in the journal table.

Without Smart Journaling turned on (the default setting), the entries in DV_PWEL_DAY_STATUS_JN will look like this:

Note that the revisions are sorted descending and that you find traces of all the operations as separate rows in the journal table.

With Smart Journaling activated, some of these operations are not journaled, because of the filtering related to system users. DV_PWEL_DAY_STATUS_JN will look like this:

If we inspect the entries here, we will see that there are 2 operations that have not been journaled:

When BILL updated the empty row created by INSTANTIATION (ref,requirement 1).

When TRANSFER updated ON_STRM_HRS from 14 → 16 (ref. requirement 2). TRANSFER as a system user (list 2) can update his own changes several times without trigging a new journal entry.

The journal entries can be used when gener
…[truncated]


==========================================================================================
## [12/25] How to use Icons from Font Awesome
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/how_to_use_icons_from_font_awesome.html
==========================================================================================
How to use Icons from Font Awesome
Introduction

This article provides a reference on how the Font Awesome icons (Primefaces Font Awesome, https://www.primefaces.org/showcase/ui/misc/fa.xhtml) are configured to work with EC. The first section provides an overview of how EC determines which icon type is to be used (standard or Font Awesome). This is followed by technical details on how to configure the application to support Font Awesome icons, with examples.

Summary

The Font Awesome icons have been added to EC to let clients have more freedom to customize the product to fit their own taste and desire. As per now (December 2020) there are 479 icons that can be added to the application. These icons provide a set of additional style attributes that makes it easy to style them as wanted.

Functional Concept

The concept is described as follows:

A client requests a component, in this case, a table cell, that contains an icon.

The EC presentation framework handles the request and asks for the metadata from the EC class.

The application will then assess the render type of the cell. In EC, there is 'icon' which is the default one, and then there is 'icon-fa' which supports Font Awesome icons. A render type and data value must be provided for both. The render type for Font Awesome is 'icon-fa'. The data value must be the class description of the Font Awesome icon (i.e. fa fa-xx).

The server generates a render response and forwards it to the client.

The table cell is rendered and the client should be able to see a default- or a Font Awesome-icon on the screen.

Configuration

In order to define a cell in a table to use custom icons, the following has to be done. In this example, we use the ‘Daily Capacity Validation’ screen which contains icons.


Daily Capacity Validation screen

The first step is to create or edit an attribute for the class that is associated with the current screen. Navigate to ‘Class Attribute Configuration’ and choose the class you want to edit (in this case ‘TRCN_DAY_CAP_VALID’). Then choose the viewtype property and replace/add ‘icon-fa’ as the value. Click the Generate Class View button.


The viewType is changed from 'icon' to 'icon-fa'. Please note that changing this attribute from ‘icon’ to ‘icon-fa’ will result in columns/cells that only support Font Awesome icons.

Once this is changed and generated, the property “dataValue” should contain the Font Awesome icon class. This value must be the declaration of the desired Font Awesome icon class and, optionally, styling (see the section below).

How to use Font Awesome styling

This section gives a brief introduction to styling the different Font Awesome icons that are supported in EC.

Colors

EC defines some default style classes that allow coloring the Font Awesome icons. The default color of these icons is black, but this can be overridden as follows.

StyleClassName	Color Description	Color-look


ECGreen

	

Default green color of EC

	

 (fa fa-check ECGreen)




ECRed

	

Default red color of EC

	

 (fa fa-info-circle ECred)




ECYellow

	

Default yellow color of EC

	

 (fa fa-warn ECYellow)




ECOrange

	

Default orange color of EC

	

 (fa fa-arrow-circle-right ECOrange)




ECBlue

	

Default blue color of EC

	

 (fa fa-home ECBlue)




ECPurple

	

Default purple color of EC

	

 (fa fa-medium ECPurple)

Sizing

Font Awesome also provides style classes for sizing, often prefixed fa-xx at the end of the class definition. Note that "em" is relative to the font size of the element. 2em means double the size of the element’s font size.


Class declaration	Size


Fa fa-home fa—​xs

	

.75em




Fa fa-home fa—sm

	

.875em




Fa fa-home fa—​lg

	

1.33em




Fa fa-home fa—2x

	

2em




Fa fa-home fa—3x

	

3em




Fa fa-home fa-5x

	

5em




Fa fa-home fa—​7x

	

7em




Fa fa-home fa—​10x

	

10em

Rotation

Font awesome also provides style classes for rotating the icons. This can be applied to all icons. An example is shown below.

Class Declaration	Rotation amount


fa-rotate-90

	

90 degrees




fa-rotate-180

	

180 degrees




fa-rotate-270

	

270 degrees




fa-flip-horizontal

	

Icon mirrored horizontally




fa-flip-vertical
…[truncated]


==========================================================================================
## [13/25] How to use verificationStatus to color cells
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/how_to_use_verification_status_to_color_cells.html
==========================================================================================
How to use verificationStatus to color cells
Introduction

EC table cells are styled according to the cell’s verification status. The styling can be customized using the verificationStatus class attribute property.

Overview

The standard styling of EC verificationStatus-cells is similar to the following screenshot:

Figure 1. Standard styling

Additional styles are available that colors either the cell background or the cell text as shown in the following screenshot:

Figure 2. Additional styling options
Styles

Standard style classes have the following styling:

Table 1. Standard styles
Class Name	Styling Description


VerShowStopper

	

Border-bottom: Red (#ab261c)




VerError

	

Border-bottom: Orange (#d58322)




VerWarn

	

Border-bottom: Dark Yellow (#cfc84a)




VerInfo

	

Border-bottom: Blue (#4067a5)




VerAdvice

	

Border-bottom: Purple (#9f5fcf)




VerOk

	

Border-bottom: Green (#8eb245)

Compared to the standard styling, the additional style classes set the background color of the whole cell or color the cell text. Most also add font weight bold to the text.

Table 2. Additional styles
Class Name	Styling Description


VerRed

	

Font weight: bold
Background-color: Red (#f48699)




VerYellow

	

Font weight: bold
Background-color: Yellow (#feec79)




VerGreen

	

Font weight: bold
Background-color: green (#b2d675)




VerBlue

	

Font-weight: bold
Background-color: Blue (#6a9ed4)




VerLightBlue

	

Font-weight: bold
Background-color: Light Blue (#afd2ef)




VerOrange

	

Font-weight: bold
Background-color: Orange (#fbb779)




VerGrey

	

Font-weight: bold
Background-color: Grey (#D3D3D3)




VerLightGrey

	

Background-color: LightGrey (#EFEFEF)




VerBlack

	

Font-weight: bold;
Background-color: Black (#000000)




VerBrown

	

Font-weight: bold
Background-color: (#A0522D)




VerPurple

	

Font-weight: bold
Background-color: Purple (#800080)




VerPink

	

Font-weight: bold
Background-color: Pink (#FFC0CB)




VerCyan

	

Font-weight: bold
Background-color: Cyan (#40E0D0)




FontRed

	

Font-weight: bold
Color: Red (#f48699)




FontBlue

	

Font-weight: bold
Color: Blue (#6a9ed4)




FontGrey

	

Font-weight: bold
Color: Grey (#a0a0a0)

Configuration

In order to configure cell styling, navigate to the Class Attribute Configuration screen and set the verificationStatus property.

In this example, we’ll use the PWEL_DAY_STATUS class and its attribute ON_STREAM_HOURS.

Figure 3. Static representation of the VerRed class

Dynamic presentation can be used to configure different styling based on some conditions. Please refer to the Class model presentation syntax guidelines.

Figure 4. An example that illustrates some of the different colors

Please note that if a class attribute is marked as mandatory in the Class Validation screen, it will override the class that is defined in the verificationStatus property in the Class Attribute Configuration screen.


==========================================================================================
## [14/25] Property IGNORE_IND
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/ignore-ind.html
==========================================================================================
Property IGNORE_IND

EC-13.0.2 introduced a new class attribute and relation property called IGNORE_IND. This property will replace the old DISABLED_IND for disabling attributes with extensions. The main difference between the two is that IGNORE_IND will not affect the generation of class views or triggers. Instead, the attribute will be excluded from the data retrieval process, i.e. it will be invisible to the application layer. The benefits of this change is that it will no longer be necessary to regenerate database objects after changing this property, which will save time when installing a new extension. This rule will only be enforced on attributes delivered by the product.

Group model class attributes are excluded from this rule. Extensions can still enable and disable group model class attributes using the DISABLED_IND set to Y/N.

It is still possible to enable attributes delivered pre-disabled, i.e. set DISABLED_IND to 'N'.

Existing extensions that use the DISABLED_IND to disable product attributes must change the property to IGNORE_IND. This will be done automatically on extensions already installed on an EC system with an upgrade script delivered with EC-13.0.2.


==========================================================================================
## [15/25] Property INTERFACE_ALIAS
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/property-code-interface-alias.html
==========================================================================================
Property INTERFACE_ALIAS

Every class implementing an interface class must have attributes with the exact same names as defined by the interface class. Projects that want to add an existing product class to an existing product interface class might need to add any missing attributes. The rules for class changes in extension prevent projects to add missing attributes with names that match the product interface attributes.

EC-13.0.5 introduced a new class attribute and relation property called INTERFACE_ALIAS. This property can be used to specify which interface attribute name the class attribute or relation represents.

Class attribute property: the INTERFACE_ALIAS value should be the interface attribute name or the interface relation role name ID or role name CODE.

Class relation property: _ID and _CODE are added to the INTERFACE_ALIAS value. E.g. INTERFACE_ALIAS = FROM_NODE will represent FROM_NODE_ID and FROM_NODE_CODE. It can represent interface class attributes or interface class relation.

Example: Interface class OPERATIONAL_LOCATIONS has attributes DESIGN_CAPACITY, RESERVED_CAPACITY and CAPACITY_UOM. Class STREAM are missing these attributes. To make it possible for STREAM to implement interface OPERATIONAL_LOCATION must these attributes be added. Extension EXT01 can add attributes to STREAM (e.g. EXT01_DESIGN_CAPACITY, EXT01_RESERVED_CAPACITY and EXT01_CAPACITY_UOM) and use property INTERFACE_ALIAS to define which interface attribute the attributes represent.

When using INTERFACE_ALIAS for interface classes that are owner class for data classes, the system setting Report view generation for data classes: join with IV view when owner is interface class should be set to Y. If not set to Y, the RV view will most likely not be generated successfully.

This can be set in the Maintain System Settings screens for the customisation category 'EC Settings'.

INTERFACE_ALIAS can not be used for attributes or relations used in the interface WHERE condition.

E.g. ALLOC_NODE has WHERE condition ALLOC_FLAG='Y'. ALLOC_FLAG can not be used as INTERFACE_ALIAS.


==========================================================================================
## [16/25] Application layer data sourcing and processing with custom Java processors
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/applayer_source_and_processing.html
==========================================================================================
Application layer data sourcing and processing with custom Java processors
Introduction

EnergyComponents allows you to customize how data is retrieved and persisted for any class through custom Java processors. These processors enable you to:

Modify, enrich, or filter data during retrieval (CUSTOM_RETRIEVE_PROCESSOR)

Customize persistence logic when saving data (CUSTOM_SAVE_PROCESSOR)

Define custom data sources for classes (CUSTOM_DATAMODEL_SOURCE, supersedes CUSTOM_DATA_RENDERER)

These features work with all class types, not just META classes. They provide a powerful alternative to database-level triggers, functions, and views by moving logic to the Java application layer.

They are also set on a per presentation context basis. You can then have different processors and sources for different use cases.

Common Use Cases:

Add computed attributes to retrieved rows

Pre-calculate values on-the-fly during queries

Implement local caching for performance

Replace database triggers with Java logic (using CUSTOM_SAVE_PROCESSOR)

Replace database functions with Java logic (using CUSTOM_RETRIEVE_PROCESSOR)

Integrate external data sources (REST APIs, file systems, etc.)

CUSTOM_RETRIEVE_PROCESSOR

The CUSTOM_RETRIEVE_PROCESSOR class property allows you to hook into the data retrieval pipeline to modify, add, or remove rows and attributes in a streaming fashion.

Configuration

Add the property to your class configuration:

<class-property-cnfg property-code="CUSTOM_RETRIEVE_PROCESSOR"
                     presentation-cntx="/"
                     property-type="APPLICATION">
    <property-value>com.example.MyRetrieveProcessor</property-value>
</class-property-cnfg>

Multiple processors can be specified (comma or whitespace-separated). They execute in the order specified, or by the order defined by the @ProcessorPriority annotation.

<property-value>com.example.Processor1, com.example.Processor2</property-value>
Implementation

Create a Java class that extends com.ec.eccore.domain.query.BaseRetrieveProcessor:

package com.example;

import com.ec.eccore.datamodel.EcDataModel;
import com.ec.eccore.datamodel.EcDataModelRow;
import com.ec.eccore.domain.query.BaseRetrieveProcessor;
import com.ec.eccore.domain.query.QueryConfig;
import java.util.stream.Stream;

public class MyRetrieveProcessor extends BaseRetrieveProcessor {

    public MyRetrieveProcessor(QueryConfig queryConfig) {
        super(queryConfig);
    }

    @Override
    public void rowProcess(EcDataModelRow row) {
        // Modify each row here
        if (row.cellExists("MY_ATTRIBUTE")) {
            row.getCell("MY_ATTRIBUTE").setDataValue(computeValue(row));
        }
    }

    @Override
    public void close() throws Exception {
        // Clean up resources
    }
}
Processor Lifecycle Hooks

The BaseRetrieveProcessor implements the Processor interface, which provides five callback methods executed in this order:

rowMap(EcDataModel dataModel, EcDataModelRow rowOrMetaRow)

Called for every row and metaRow in the stream

Can manipulate the stream itself: return 0, 1, or multiple rows

Use to filter, split or duplicate rows.

Emulate a sql UNION clause by duplicating rows with different attribute values.

Returns Stream<EcDataModelRow>

Default implementation: return Stream.of(rowOrMetaRow);

@Override
public Stream<EcDataModelRow> rowMap(EcDataModel dataModel, EcDataModelRow rowOrMetaRow) {
    // Filter out rows
    if (shouldSkipRow(rowOrMetaRow)) {
        return Stream.empty();
    }
    // Or duplicate rows
    return Stream.of(rowOrMetaRow, createDuplicateRow(rowOrMetaRow));
}

metaRowProcess(EcDataModelRow metaRow)

Called once per meta row (metadata about the dataset)

Use to process or modify metadata

@Override
public void metaRowProcess(EcDataModelRow metaRow) {
    // Process metadata
}

preProcess(EcDataModel datamodel)

Called once before any data rows are processed (but after at least one metaRow has been processed)

Use to initialize state, caching, database connections, or other resources

@Override
public void preProcess(EcDataModel datamodel) {
    // Initialize resources
    this.cache = loadCache();
}

rowProcess(EcDataModelRow row) ⭐ Most 
…[truncated]


==========================================================================================
## [17/25] Expressions and Scripting in the EC Domain Model
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/class_configuration/expression-domain-config.html
==========================================================================================
Expressions and Scripting in the EC Domain Model

Energy Components (EC) provides support for dynamic and real-time resolution of values, including both data values and meta-attributes, within the EC Domain Model. This resolution is performed directly by the database engine during data retrieval, ensuring high performance and flexibility.

However, in certain scenarios, it is more practical to perform this resolution at the application layer. The necessary information to resolve a meta-attribute might only be accessible at the application layer. Additionally, to avoid tight coupling, it may be beneficial to transfer business logic from the storage layer to the application layer.

Therefor, support for resolving Expressions on the application layer has been added to the Domain Model. All existing features around dynamic resolving in the database can now also be configured to be resolved on the application layer.

Summary:

#	Configuration	DB Function	App Expression	Comments


1

	

class_attribute_cnfg.DB_MAPPING_TYPE

	

FUNCTION

	

EXPRESSION

	

sdfsd




2

	

class_attr_property_cnfg.PROPERTY_CODE

	

WR_FUNCTION

	

WR_EXPRESSION

	

sdfsd




3

	

class_attr_property_cnfg.PROPERTY_CODE

	

DB_PRES_SYNTAX

	

APP_PRES_SYNTAX

	

sdfsd




4

	

class_attr_property_cnfg.PROPERTY_TYPE

	

DYNAMIC_PRESENTATION

	

DYNAMIC_PRESENTATION_APP

	

sdfsd

(1) - EXPRESSION Attributes

Expression Attributes can be used as an alternative to Function attributes. Configure the class_attribute_cnfg table with the following settings:

DB_MAPPING_TYPE='EXPRESSION'

DB_SQL_SYNTAX=<expression>

Ex:

-- EXPRESSION attribute [DB_MAPPING_TYPE=EXPRESSION, DB_SQL_SYNTAX=expression]
insert into class_attribute_cnfg (CLASS_NAME, ATTRIBUTE_NAME, APP_SPACE_CNTX, IS_KEY, DATA_TYPE, DB_MAPPING_TYPE, DB_SQL_SYNTAX, DB_JOIN_TABLE, DB_JOIN_WHERE)
values ('ALARMS', 'EXPRESS_YOUR_SELF', 'EC_PROD', 'N', 'STRING', 'EXPRESSION', '''isLogicalKey: '' + cell.getAttrValue(ECAttr.logicalkey)', null, null);

The DB_SQL_SYNTAX is used to hold the expression for both database resolving (function) and for application resolving (expression).

Setting DB_MAPPING_TYPE='FUNCTION' will make a FUNCTION attribute.


(2) - WR_EXPRESSION

WR_EXPRESSION can be used as an alternative to the WR_FUNCTION to make sure the expression will be resolved by the application layer.

Ex:

-- WR_EXPRESSION attribute [PROPERTY_CODE=WR_EXPRESSION, PROPERTY_VALUE=expression]
insert into class_attr_property_cnfg (CLASS_NAME, ATTRIBUTE_NAME, PROPERTY_CODE, OWNER_CNTX, PRESENTATION_CNTX, PROPERTY_TYPE, PROPERTY_VALUE)
values ('ALARMS', 'REASON', 'WR_EXPRESSION', 1000, '/EC', 'APPLICATION', '''uppercase:'' + origDatavalue?.toUpperCase() ?? ''''');
(3) - APP_PRES_SYNTAX

APP_PRES_SYNTAX can be used as an alternative to the DB_PRES_SYNTAX to make sure the expression will be resolved by the application layer.

Ex:

-- APP_PRES_SYNTAX attribute [PROPERTY_CODE=APP_PRES_SYNTAX, PROPERTY_VALUE=expression]
insert into class_attr_property_cnfg (CLASS_NAME, ATTRIBUTE_NAME, PROPERTY_CODE, OWNER_CNTX, PRESENTATION_CNTX, PROPERTY_TYPE, PROPERTY_VALUE)
values ('ALARMS', 'EXPRESS_YOUR_SELF', 'APP_PRES_SYNTAX', 1000, '/EC', 'APPLICATION', 'row.getCell('EXPRESS_YOUR_SELF').getDataValue().toUpperCase()');
(4) - DYNAMIC_PRESENTATION_APP

Dynamic resolving of meta attributes by the database is configured by using the DYNAMIC_PRESENTATION as the PROPERTY_TYPE. Using DYNAMIC_PRESENTATION_APP instead will make sure to resolve the meta attributes on the application layer instead.

Example, configuring an expression for meta attribute verificationText:

-- Meta attribute expression [PROPERTY_TYPE=DYNAMIC_PRESENTATION_APP, PROPERTY_VALUE=expression]
insert into class_attr_property_cnfg (CLASS_NAME, ATTRIBUTE_NAME, PROPERTY_CODE, OWNER_CNTX, PRESENTATION_CNTX, PROPERTY_TYPE, PROPERTY_VALUE)
values ('ALARMS', 'REASON', 'verificationText', 1000, '/EC', 'DYNAMIC_PRESENTATION_APP', '''Fire walk with me'' + (11 +12 +13)');


==========================================================================================
## [18/25] How to configure Screen Treeview Menu
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/treeview_configuration.html
==========================================================================================
How to configure Screen Treeview Menu
Introduction

EC uses a treeview menu for navigating to screens. A treeview menu is a graphical user interface component that displays items in a tree-like structure. It allows users to expand or collapse nodes to navigate to screens.

Pre 14.2.0

The treeview menu was configured in a table in the database: CTRL_TV_PRESENTATION. To update the treeview, records were inserted, updated, or deleted. It was only possible to have one treeview.

The URL for the screens were stored as part of the treeview configuration. When the URL for a business function changed, the treeview configuration had to be updated.

Post 14.2.0

Treeview menu is configured using JSON. It is possible to have many treeviews. A treeview can be based on an existing treeview (i.e. deltas). Treeview configuration with same name and different owner contexts, are merged based on owner context.

The configuration can be added as a JSON file to an extension by placing the file in the WEB-INF/configuration/treeview folder. It can also be stored in the database in TV_CTRL_CONFIGURATION_STORAGE.

The treeview configuration uses BF_CODE for references to business functions. When the URL for a business function changes, the treeview configuration doesn’t need to be updated.

Configuration JSON schema

JSON for configuration has two sections:

Meta - defines meta information like configuration type, configuration type version, name, owner context, etc.

Configuration - the configuration.

Meta
 "meta": {
    "configType": "ECTreeviewConfig",
    "version": "1.0",
    "javaType": "com.ec.frmw.ecconfiguration.treeview.ECTreeviewConfig",
    "name": "CustomTreeview",
    "description": "Customisation to treeview delivered with EC",
    "ownerCntx": 2000,
    "parentName": "ECProductScreenTreeview"
 }
Field	Description	Example value


configType

	

The configuration type. Should be ECTreeviewConfig for treeview configuration.

	

ECTreeviewConfig




version

	

The configuration type version.

	

1.0




javaType

	

The java class for the configuration type.

	

com.ec.frmw.ecconfiguration.treeview.ECTreeviewConfig




name

	

The name for the configuration.

	

CustomTreeview




description

	

Description of the configuration.

	

Customisation to treeview delivered with EC




ownerCntx

	

The owner context for the configuration. This is used when merging configuration.

	

2000




parentName

	

The name of the parent that this treeview configuration is a delta to (optional).

	

ECProductScreenTreeview

Configuration

Configuration can differ for different configuration type. Here is an example for treeview configuration:

  "configuration": {
    "@class" : "com.ec.frmw.ecconfiguration.treeview.entity.TreeviewConfiguration",
    "items": [
      {"key": "ZEX30.00","label": "ZEX30 3rd-party","sortOrder": "10","type": "FOLDER","screen": "","additionalParameters": "", "disabled": "false" , "children" : [
         {"key": "ZEX30.01","label": "ZEX30 3rd-party","sortOrder": "10","type": "URL","screen": "ZEX30.01","additionalParameters": "", "disabled": "false", "group": "TEST_SCREENS", "children" : []},
         {"key": "ZEX30.02","label": "ZEX30 pdf file","sortOrder": "20","type": "URL","screen": "ZEX30.02","additionalParameters": "", "disabled": "false", "group": "TEST_SCREENS", "children" : []},
         {"key": "ZEX30.03","label": "ZEX30 external web site","sortOrder": "30","type": "URL","screen": "ZEX30.03","additionalParameters": "", "disabled": "false", "group": "TEST_SCREENS", "children" : []}
      ]}
    ]}
Field	Description	Example value


@class

	

The entity class reading the JSON configuration.

	

com.ec.frmw.ecconfiguration.treeview.entity.TreeviewConfiguration




items

	

hierarchical structure with treeview item configuration.

	

<treeview item configuration>

Treeview Item configuration
{
  "key": "ZEX30.01",
  "label": "ZEX30 3rd-party",
  "sortOrder": "10",
  "type": "URL",
  "screen": "ZEX30.01",
  "additionalParameters": "",
  "disabled": "false",
  "group": "TEST_SCREENS",
  "children": []
}
Field	Description


key

	

Unique key for the treeview item. This is used to identify the item when merging w
…[truncated]


==========================================================================================
## [19/25] Unit of Measure Support in Energy Components
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/unit_of_measure_support_in_ec.html
==========================================================================================
Unit of Measure Support in Energy Components
Introduction
Disclaimer


This document was written for the release of EC 12.1 and was meant to describe changes that came with that release and also pointing forward to changes planned for future releases. Even if there has not been made significant changes since the release of EC 12.1 in this area, the information here is still relevant to describe how UOM is handled in EC. For projects upgrading from older versions of EC the explanation of the changes that came in 12.1 should be useful. The document has been reviewed and validated against this EC version, so the main message in this document should still be relevant and useful even if references to specific EC versions and example data might be a bit outdated.

What is this document About?

This document gives an overview of the changes around Unit of Measure handling that is came in EC 12.1 and the direction for future EC releases. This includes considerations around supporting several view units in the same EC system, what it means to the data model and links to object classes.

Who will find this document useful?

This document is intended to support database developers and technical upgrade consultants that are upgrading to EC 12.1, to understand the implications (if any) in this upgrade. But just as important to understand how future versions of EC will change to support several units of measure contexts and conversion factors. What will developers need to relate to when creating or extending business functions in EC.

What is not included in this document?

This document does not explain the key EC concept in detail, it assumes that the user has a relatively good understanding of the underlying principles for tables, classes, configuration structures, production day etc.

Versions/Applicability

The information presented here is related to upgrade to EC 12.1 from an earlier version. But it also outlines future changes we expect to be coming in the next 1-2 versions of EC.

Background

The Energy Components (EC) systems come with support for values with associated Unit of Measure (UOM) and unit conversions. There are different requirements and different ways of handling it for different parts of the system.

This document discusses the existing solutions around UOM, with advantages and limitations, and the new challenges with supporting several viewunit contexts within one EC system. It explains what the focus is for the delivery in EC 12.1, the choices and limitations that are still up for discussion, and the areas to address next after the first steps have been taken.

Starting point, fundamental requirements and considerations

The Energy Components system contains a big relational database. The data has been organized in wide table structures where data belonging to one object at one point in time are grouped together into one physical row. This example is from a table called Pwel_Day_Status

This table is now 275 columns wide! The product itself uses 195 of these columns:

2 columns for the key (object_id, daytime)

10 columns for Record metadata (Created/Last updated, Record Status, Approval, Revision info, etc)

80 columns are reserved for project specific class attributes

In total there are 227 numeric columns in this table

This grouping of values for one "time-unit" into one record has some clear advantages in a Hydro Carbon Accounting (HCA) setting where we want to have tight control on all changes with the full audit trail, journaling, and possibilities to lock data. For much of our processing, it is also an efficient way to organize the data that belongs together. It has got some challenges when it comes to handling the association between values and unit of measure (UOM) that the value represents.

Storing Unit of Measure together with the Value

There are around 900 of the numeric class attributes in EC where the value is stored together with the unit that the number represents. This is done because it has in these cases been identified that the number must be stored in a specific unit, either for legal/regulatory reasons or to avoid any risk of losing precision in a unit conversion step before storing th
…[truncated]


==========================================================================================
## [20/25] System of Measurement
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/measurement-system.html
==========================================================================================
System of Measurement
Introduction

In EC 12.1, Unit of Measure Support in Energy Components was delivered. It includes data model changes to support unit context (i.e. System of Measurement) and unit conversion context.

System of measurement (e.g. SI (Systeme Internationale), Oil Field Units, Imperial Units) specifies the view unit for measurement types. One system of measurement is marked as the default and is used when no system of measurement is specified. One system of measurement can be marked as common which contains common measurement types. E.g. measurement types with fraction or percentage as unit. The common system of measurement can only contain measurement types that are not in any other system of measurements.

System of measurement is only supported for business functions with group model navigator. System of measurement can be specified on objects in the group model, i.e. on production unit, area, facility class 1, etc. System of measurement of an object is found using the group model. If the object itself doesn’t have system of measurement configured, the parent object is checked, etc. When opening business functions with group model navigator, the system of measurement of the target (e.g. Facility, Well, Stream, etc.) is used to view the data. If no system of measurement is found, the default system of measurement is used. Users can override the asset’s system of measurement using the Override System of Measurement option in the …​ menu in the toolbar.

UOM Setup has been removed in 13.1.0 and is replaced with Unit Context, Unit Setup and Report Setup. See Appendix: Old and New data model

A measurement type has only one database unit. It can have one or more system of measurements (i.e. view units). The EC application converts the database value to view unit using standard unit conversion.

It is only needed to have unit conversion factors from the db unit to the view unit. EC calculate inverse unit conversion factors. This is more accurate than having symmetric unit conversion factors.

When no precision are specified for the unit conversion factor, EC uses the value for custom system property Number of Precision in Unit Conversion (key: /com/ec/eccore/util/UnitConversion/FALLBACK_PRECISION). Default values is 5.

Configure System of Measurement

System of measurement is maintained in business function Measurement Type (CO.1022) and the System of Measurement tab. The upper data section lists the system of measurements. The lower data section lists the measurement types for the selected system of measurement.

System of Measurement	Description


Common

	

Contains common measurement types for all system of measurements. E.g. measurement types with fraction, percentage etc. as unit.




Custom

	

System of measurement with view unit configured by customer.




Oil Field

	

System of measurement with Oil Field view units.




SI

	

System of measurement with SI (Systeme Internationale) view units.

A system of measurement must have view unit for all measurement types that are used by classes and unit conversion must exist between the database unit and the view unit. The system of measurement code is underlined when measurement types or unit conversions are missing. The tooltip shows the measurement types or unit conversion that are missing.

When a new system of measurement is inserted and saved, the measurement types from the default system of measurement are copied to the new system of measurement.

New measurement types can be added in the Measurement Types tab. It is also possible to configure the measurement type’s view unit for each system of measurement and the report unit.

Configure System of Measurement for assets

System of measurement can be configured on objects in the Group Model. E.g. Production Unit, Sub Production Unit, Area, Sub Area, Facility Class 2 and Facility Class 1. System of measurement configured on the object closest to the target object will be used. E.g. if system of measurement is configured on both Area and Facility Class 1 for a Well, the value of the Facility Class 1 is used.

Configure access for System of Measurement

Access for System of Measurement can be configur
…[truncated]


==========================================================================================
## [21/25] How to get Users and User’s roles
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_get_user_and_userrole.html
==========================================================================================
How to get Users and User’s roles
Introduction

From EC 14.0.0, users and user’s roles are configured in Keycloak. The T_BASIS_USER and T_BASIS_USERROLE tables have been removed from the database. The T_BASIS_USER and T_BASIS_USERROLE classes are changed to META classes. They can be used in the EC application, REST API and BPM as any other classes.

The classes support a limited set of query conditions and the result is sorted by username (T_BASIS_USER) or rolename (T_BASIS_USERROLE).

Supported query conditions for T_BASIS_USER*
Query condition	Description


<property name="USER_ID" datavalue="$USER_ID$" operator="="/>

	

User for a given user id.




<property name="ACTIVE" datavalue="Y" operator="="/>

	

User(s) that is active (i.e. enabled in Keycloak)




<property name="ROLE_ID" datavalue="$ROLE_ID$" operator="="/>

	

All users with a given role id.

Supported query conditions for T_BASIS_USERROLE
Query condition	Description


<property name="USER_ID" datavalue="$USER_ID$" operator="="/>

	

All user’s roles for a given user_id




<property name="ROLE_ID" datavalue="$ROLE_ID$" operator="="/>

	

All user’s roles for a given role_id.

It is possible to combine the query conditions. E.g. get all users for a role that is active.

Use T_BASIS_USER and T_BASIS_USERROLE in EC Application

The T_BASIS_USER and T_BASIS_USERROLE classes can be used as any other classes in EC. The query xml file for T_BASIS_USER or T_BASIS_USERROLE is like the query file for any other classes with the limitation that only some query conditions are supported.

<?xml version="1.0" encoding="UTF-8"?>
<data>
	<query>
		<recordstatus>false</recordstatus>
	</query>
	<class name="T_BASIS_USERROLE">
	</class>
	<object name="T_BASIS_USERROLE">
		<property name="ROLE_ID" datavalue="$ROLE$" operator="="/>
	</object>
</data>
Use T_BASIS_USER and T_BASIS_USERROLE in REST API

The T_BASIS_USER and T_BASIS_USERROLE classes can be used as any other classes in REST API. They support only the query condition listed above.

Example:

https://<ec server>:<port>/rest/v1/domain/data/T_BASIS_USER?qc=USER_ID,=,sysadmin&qa=*
Use T_BASIS_USER and T_BASIS_USERROLE in BPM

A new process action is added for retrieving data from EC classes: {ExecuteEcDataModelAction} (com.ec.bpm.ext.ec.process_actions.EcDataModelHandler). The process action takes classname, comma separated list of attributes (optional, default = all attributes), list of query conditions (optional) and return type (optional) as arguments. It returns either a List with a map of attribute and value (default) or a DatamodelInterface. It can be used to retrieve data from any classes in EC, also T_BASIS_USER and T_BASIS_USERROLE.

See Energy Components Software Development Kit (EC-SDK) - /energycomponents-sdk/examples/bpm/010-bpm-example-project - "EC Datamodel Sample and EC Datamodel Using DMI Sample".


==========================================================================================
## [22/25] System Property Exclude Synonyms
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/exclude-synonyms.html
==========================================================================================
System Property Exclude Synonyms

We have added a new system property Exclude Synonyms that can be used to indicate which database schemas to exclude from synonym generation. By default, no database user will be excluded. This can be changed from the Maintain System Settings screen under EC Settings.

By default, running an EC migration will trigger the generation of synonyms for all schema users that have a username that ends with [operation], and have one or more of the four EC roles applied to them:

APP_READ_ROLE_[operation]

APP_WRITE_ROLE_[operation]

REPORT_ROLE_[operation]

ANALYTICS_ROLE_[operation]

For example, if the operation name is EC, then a schema called EXAMPLE_EC with role APP_READ_ROLE_EC applied to it will get synonyms for ECKERNEL_EC objects, unless excluded:

It is still possible to generate all synonyms for the excluded user by calling the procedure directly from the eckernel_[operation] user:

call ecdb_buildutils.SyncPrivateSynonyms('EXAMPLE_EC')


==========================================================================================
## [23/25] Four Eyes Approval
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/four_eyes_approval.html
==========================================================================================
Four Eyes Approval
Introduction

This document shows how to use the Four Eyes Approval system.

The four eyes principle is a requirement that two individuals approve of some action before it can be performed. The four eyes principle is sometimes called the two-man rule or the two-person rule. The definition is given by http://whatis.techtarget.com/definition/four-eyes-principle.

In a business context, the four eyes required for approval are often those of the CEO (Chief Executive Officer) and the CFO (Chief Financial Officer), who must both sign off on any significant business decision. In editing, proofreading, and translation, documents typically have a second reader to detect errors and typos that a single pair of eyes might miss. Although neither individual might detect all errors, two readers are likely to miss different things so that, collaboratively, they will catch more mistakes.

Enable/Disable Approval

In EC, you have the option to enable Four Eyes Approval on changes on a specific EC Class. This is done by adding the class property 'APPROVAL_IND'. This can be done in the Class Configuration screen, as shown below. After adding this property, the class view must be generated.

To disable Four Eyes Approval, the APPROVAL_IND can be removed, or set to 'N'.

How to approve data

Approval of data is done in the Four Eye Approval screen shown below. The user that did the original change is not able to do the approval. It is also possible to reject the deletion of data.

How to Enable Four Eyes Approval in the Todo List

The system can add tasks in the Todo List for necessary approvals. There will be one task per class that needs approval(s). To enable this, a BPM process must be started.

Steps:

Add the bpm-project containing the standard processes, which is delivered with EC releases: ecbpm-std-processes-14.2.4-project-source.zip. This is done in the Project Management screen.

Create a Process Template for the process, as shown below.

Go to the Process Execution screen and select the Four Eyes Approval template.

Add parameter values and start the process (see below).

ROLES: A comma-separated list of roles that should see the tasks. Provide the code of the role.

WAIT_TIME: Milliseconds giving the interval for the update of the task list (the system will add tasks if missing). It could be e.g. per hour.

loop: This parameter is only for test purposes. Setting this to 'no' will make the process update the task list one time. Setting it to 'yes' will make the process run forever.

The process will now update the task list with necessary approvals. The tasks will not be removed automatically when all approvals are done. A user will need to complete the task.

You can go to Process Overview to see how the process progresses. The process can also be stopped there.

The process can also be started as a Scheduled task by creating a scheduled task that runs the 'Four Eyes Approval' business action. You will need to provide the same parameter values as described above.

The tasks should now appear in the Todo list, as shown below. By clicking the '4-Eyes Approval' button, a popup screen will show the Four Eyes Approval screen.


==========================================================================================
## [24/25] How to manage User Exit packages
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/how_to_manage_user_exit_package.html
==========================================================================================
How to manage User Exit packages
Introduction: Why do we need to change

This change is to separate ownership between product default implementation of the user exit and project overrides of the user exit and to avoiding injecting code into product owned PL/SQL packages.

This is a hard requirement in the new Extension Framework, that Extensions cannot change product packages.

With the old way of adding User Exit (UE) code, Flyway handling of project UE package implementations would not automatically detect that product had changed the default implementation.

What does this mean for the default Product implementation

The UE header is the definition of a User Exit with the Interface API.

The default Product implementation is done in User Exit Interface (UEI) package inside the Product.

The customers that want to override the default implementation will need to make their own UEI package and change the reference in table CTRL_USER_EXIT.

Handling of global variables in the UE package header:

Has been made into functions in the UE header.

Can still be variables in the UEI package header.

What does this mean for Project upgrading to EC 12.2.3 or above

Upgrade will copy existing project specific UE package into a ZUE_TEMP…

Map the reference in CTRL_USER_EXIT to point to the ZUE_TEMP…

This is only done when we detect a difference in the package.

You should rename the package in your project code repository to UEI_…​

Change reference and Owner Context in CTRL_USER_EXIT to point to your package.

Run ecdp_generate.generate_ue to UE_ package regenerating.

Remove the ZUE_TEMP… package.

Minimize the overrides to only the functions where you have an override. The upgrade will do all the functions/procedures in a package that has changed.

Upgrade implementation description

Mapping table CTRL_USER_EXIT is created. By default, the table CTRL_USER_EXIT has mappings from User Exit methods to the product implementation of the methods. The mapping can be turned ON or OFF by setting a column ACTIVE_IND to 'Y' or 'N', default value is 'Y'.

Run compare the checksum of the UE packages in the customer database with the old “clean” UE packages. As the “clean” database the EC 12.2.0 was taken, product default User Exit packages were not changed since that.

If the checksum is the same, no remapping is needed.

If the checksum is different, it means that there are customer/project changes that need to be handled.

The customer/project package is renamed to the ZUE_TEMP_ package

Insert into CTRL_USER_EXIT is done to point to this implementation, with owner_cntx = 1000.

The owner of the overridden package can change their package and point to it with their owner context and remove the temporary package.

Implement package headers for 18 UE_ packages where global variables are converted to functions.

Implement Product default User Exit packages as UEI_XXXX_ packages

Run ecdp_generate.generate_ue. The UE_ package bodies are generated based on the mapping table, to call the implementation package

either the Product default or the project-specific one.

Example: Customer-specific mapping in the CTRL_USER_EXIT table:

Figure 1. CTRL_USER_EXIT table

Example: The UE_ package body generated based on this mapping in CTRL_USER_EXIT:

CREATE OR REPLACE PACKAGE BODY UE_CALENDAR IS
   FUNCTION GetRecurringHoliday (p_recurring_holiday_code VARCHAR2, p_year NUMBER) RETURN DATE
   IS
      BEGIN
         RETURN UEI_KING_CALENDAR.GETRECURRINGHOLIDAY(p_recurring_holiday_code, p_year);
      END GetRecurringHoliday;
How to create a custom implementation of a product User Exit package

Product User Exit packages can not be modified.

Parameters for existing function/procedure can not be modified.

New function/procedure can not be added.

The set of parameters is defined in the UE package header.

Create a new custom implementation of the product UE package (e.g. UEI_KING_CALENDAR)

Add new functions/procedures to the UEI package header and body for functions/procedures you want to customise.

The function/procedure must have the same parameters as specified in the product UE package.

The custom UEI package can have additional functions/procedure
…[truncated]


==========================================================================================
## [25/25] Calculation Group configuration
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/general-config/calculation_group_configuration.html
==========================================================================================
Calculation Group configuration
Introduction

EC executes calculations by "calculation groups" together with a list of objects to do the calculation for, and what calculations to run.

Previously, EC has separate screens (Business Functions) for configuring this:

Calculation Type	Calculation Group screen	List screen / List entries	Job Connection screen


Production Allocation

	

Allocation Network

	

Allocation Network List / Allocation Nodes

	

Alloc Network Calc Job Conn




Contract calculations

	

Contract Group

	

Contract Group List / Contract objects

	

Contract Group Calculation Job Connection




Price calculations

	

Price Group

	

Price Group List / Price Objects

	

N/A




Financial Item calculations

	

<new - no existing screen>

	

<new - no existing screen> / Financial Item Templates

	

<new - no existing screen>




Product Stream

	

Product Stream Group

	

Product Stream Group Setup / Product Group objects

	

Product Stream Group Calculation Job Connection

All of this configuration is being stored in a common set of tables, but with different classes on top.

The purpose of the new Calculation Group configuration is to consolidate multiple screens into ONE screen with 3 tabs.

The underlying classes and table structures are not changed.

Calculation Group Context

The Calculation Group Context Screen is used to define an EC object used for Calculation Groups. The object defined here will be used in the Calculation Group Setup screen, where we can do the setup for the Calculation Groups in EC.

By default, this screen will have five entries provided with EC out of the box:

Allocation Network Calculation

Contract Calculation

Financial Item Calculation

Price Calculation

Product Stream Calculation

Please note that an implementation project may add more Calculation Group Context objects as needed.

Navigator

Navigator settings allow users to define the search criteria for Calculation Group Contexts and list them in the table below:

Navigator has one selection option:

Date – Auto-filled with yesterday’s date.
This is the date Calculation Group Contexts are valid at.

List Section

This section displays all Calculation Group Contexts matching the Navigator criteria.

Tab 'New Version'

This tab is used to create new Calculation Group Context objects or to amend an existing one. We can also create new versions of the Calculation Group Context using this tab.

Creating a New Calculation Group Context has these features:

Calculation Group Context Code - Mandatory
This is the code of the Calculation Group Context. It should be unique.

Calculation Group Context Name - Mandatory
This is the name of the Calculation Group Context.

Start Date - Mandatory
This is the date the Calculation Group Context is valid from.

End Date - Optional
This is the date the Calculation Group Context is valid to.

Description - Optional
This is a description of the Calculation Group Context.

Comments - Optional
This is a comment for the Calculation Group Context.

Calculation Group Object Class - Mandatory
This dropdown is for selecting the Object Class of the Calculation Group Context.

Calculation Group List Class - Mandatory
This dropdown is for selecting the Data Class (List) of the Calculation Group Context.

Calculation Group Job Connection Class - Optional
This dropdown is for selecting the Table Class (Job connection) of the Calculation Group Context.

Calculation Group Reference - Optional
This is used to set the Reference for the Calculation Group Context.

Please note that the Calculation Group Context object can be used for access control to the Calculation Group Setup screen (described below).
Calculation Group Setup

The Calculation Group Setup Screen is used to configure Calculation Groups for different types of calculations in EC:

Allocation Network

Contract

Financial Item

Price Groups

Product Stream

Each Calculation Group can be in the form of Daily, Monthly & Yearly Calculations.
We can also add the members/items to the Calculation Group for which the Calculation will be taking place using the List Tab.
This screen also gives the provision to connect the Calculation Job with the respectiv
…[truncated]