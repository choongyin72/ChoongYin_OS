# Raw content — DOC-10
Modules: ['frmw/graphql', 'frmw/reporting-and-analytics', 'frmw/edac']
Pages: 19



==========================================================================================
## [1/19] EC GraphQL Overview
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/graphql/graphql-overview.html
==========================================================================================
EC GraphQL Overview
Introduction

EC provides a REST service endpoint for using GraphQL as the query language towards EC APIs. This serves as an alternative entry point for clients and integrations alongside the REST API itself. GraphQL empowers clients to ask for exactly what they need and no more by providing an intuitive and flexible syntax for describing data requirements and interactions.

Here are some highlights of GraphQL.

Intuitive Domain Specific Language Syntax

GraphQL is centered on high-level abstractions and provides a domain specific language for defining schemas, types, queries and mutations. For example, "PRODUCTIONUNIT" and "AREA" classes in EC can be represented as follows:

type PRODUCTIONUNIT {
  CODE: String
  NAME: String
  OBJECT_ID: ID
  REF__AREA(qc: [String], qf: String, qs: [String], qt: String): [AREA!]!
  ...
}

type AREA {
  CODE: String
  NAME: String
  OBJECT_ID: ID
  REL__CP_PRODUCTIONUNIT: PRODUCTIONUNIT
  REL__OP_PRODUCTIONUNIT: PRODUCTIONUNIT
  ...
}

A query to get PRODUCTIONUNIT and its associated AREA objects can be defined as follows:

query {
  PRODUCTIONUNIT(qc: ["CODE,=,P1_PU"]) {
    CODE
    NAME
    REF__AREA {
      CODE
    }
  }
}
Hierarchical Request and Response

A GraphQL request is structured hierarchically and the response data is shaped like the request. Multiple, potientially unrelated, data resources can be fetched using a single service request. It is a natural way for clients to describe their data requirements.

For example, the above query will return the following result in JSON format:

{
  "PRODUCTIONUNIT": [
    {
      "CODE": "P1_PU",
      "NAME": "P1 Production Unit",
      "REF__AREA": [
        {
          "CODE": "P1_AREA"
        }
      ]
    }
  ]
}
Strong Typing and Introspection

A GraphQL service publishes the capabilities that its clients can consume through its type system. For example, the EC GraphQL service ships with a type system for the EC domain model. Requests are executed within the context of the type system. Validation is performed before the execution. Clients can query the type system to know the capabilities the GraphQL service provides through the language itself.

EC GraphQL Service Usage

The EC GraphQL service can be accessed either via its REST interface or programmatically via its Java API.

EC GraphQL Web Service

The EC GraphQL web service endpoints are available under /rest/v1/services/graphql in the EC REST API.

It has the following sub-endpoints:

/schema: Returns the full GraphQL schema. Very useful as a reference while writing queries.

/query: E
…[truncated]


==========================================================================================
## [2/19] EC GraphQL Type System
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/graphql/graphql-ec-domain-model-schema.html
==========================================================================================
EC GraphQL Type System

EC ships with a GraphQL type system based on the EC domain model (also known as the class model) to provide query and modification capabilities for the domain model. This chapter explores the GraphQL types defined for operating on the EC domain model.

Scalar Types

Scalar types represent primitive leaf values in a GraphQL type system. In a query operation a field of scalar type will be resolved to some concrete data. EC GraphQL supports the following scalar types:

Table 1. Scalar Types

Scalar type

	

Description




Int

	

Standard scalar type, represents a signed 32-bit integer.




Float

	

Standard scalar type, represents a signed double-precision floating-point value.




String

	

Standard scalar type, represents a UTF-8 character sequence.




Boolean

	

Standard scalar type, represents true or false.




ID

	

Standard scalar type, represents a unique identifier. The ID type is serialized in the same way as a String; however, defining it as an ID signifies that it is not intended to be human‐readable.




Number

	

EC GraphQL specific scalar type, represents an arbitrary precision signed integer or an arbitrary precision signed decimal.




Void

	

EC GraphQL specific scalar type, represents null values.

EC GraphQL Query Types

This section describes the types provided for query operations on the EC domain model.

EC Domain Model Types

EC GraphQL generates a GraphQL type for each EC class. It has the following characteristics:

The type name is the same as the EC class name in capital case.

Includes all class attributes as fields named the same as the attribute in capital case. Class attributes that are disabled, ignored or report-only are excluded.

Includes all related objects as fields named REL__ + relation name. These are the outgoing relations from this class to other classes.

Includes all referenced objects as fields named REF__ + referenced class name. These are the incoming relations from other classes to this class.

Includes a field named meta of type EcClassRecordMeta. This holds meta information about the record.

Below is a shortened example of the AREA and FCTY_CLASS_1 types:

type AREA {
  CODE: String
  NAME: String
  OBJECT_ID: ID
  REF__FCTY_CLASS_1(qc: [String], qf: String, qs: [String], qt: String): [FCTY_CLASS_1!]!
  meta: EcClassRecordMeta
  ...
}

type FCTY_CLASS_1 {
  CODE: String
  NAME: String
  OBJECT_ID: ID
  REL__OP_AREA: AREA   # An FCTY_CLASS_1 object can only link to one AREA object
  REF__WELL(qc: [String], qf: String, qs: [String], qt: String): [WELL!]!
  meta: EcClassRecord
…[truncated]


==========================================================================================
## [3/19] EC GraphQL Queries
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/graphql/graphql-queries.html
==========================================================================================
EC GraphQL Queries

The syntax of a GraphQL query is quite simple and is explained in detail by the GraphQL specification and other resources on the web. In short, queries are declarative and hierarchical. You declare what data you want by using the type hierarchy to specify which fields to return, and optionally provide input variables to affect how the fields are resolved.

An example of a very basic query that fetches all country names and their associated company names:

query {
  COUNTRY {
    NAME
    COMPANY : REF__COMPANY {
      NAME
    }
  }
}
GRAPHQL
Copied!

This chapter focuses on how to query the EC domain model.

How to Query EC Domain Models Using GraphQL

Under the hood the EC GraphQL service utilizes the EC REST API code base for querying the EC domain model. The supported filters are thus the same both in syntax and usage as in the EC domain model REST API. The query returns results in a JSON format shaped in the same structure as the request, provided no directives have been used to manipulate the output structure. It supports using variables for passing dynamic values to the query at runtime. Aliases can be used to rename fields in the result.

With Filters

EC GraphQL supports four filters (qc, qs, qf, qt) on top level Query type fields. The same filters are also available on the referenced object fields prefixed with REF__.

Following is an example of querying an AREA object with its related objects. The key points of this query are:

Filter AREA objects with "CODE,=,P1_AREA", fetch CODE and NAME attributes.

Fetch related operational PRODUCTIONUNIT object’s CODE and NAME attributes.

Fetch referenced FCTY_CLASS_1 objects filtered by their CODE attribute.

Fetch referenced WELL objects filtered by DAYTIME and sorted by NAME in ascending order.

Fetch "createdBy" and "revNo" record status information.

{
  "query": "query {
    AREA(qc: [\"CODE,=,P1_AREA\"]) {
      CODE
      NAME
      REL__OP_PRODUCTIONUNIT {
        CODE
        NAME
      }
      REF__FCTY_CLASS_1 (qc: [\"CODE,in,(P1_FCTY_1,P1_FCTY_1B)\"]) {
        CODE
        RECONCILIATION_METHOD
        REF__WELL(qc: [\"DAYTIME,>=,2011-01-01\"], qs: [\"NAME\"] ) {
          NAME
          WELL_TYPE
        }
      }
      meta {
        createdBy
        revNo
      }
    }
  }"
}

The query result looks like this:

{
  "AREA": [
    {
      "CODE": "P1_AREA",
      "NAME": "P1 Area",
      "REL__OP_PRODUCTIONUNIT": {
        "CODE": "P1_PU",
        "NAME": "P1 Production Unit"
      },
      "REF__FCTY_CLASS_1": [
        {
          "CODE": "P1_FCTY_1",
          "RECO
…[truncated]


==========================================================================================
## [4/19] EC GraphQL Mutations
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/graphql/graphql-mutations.html
==========================================================================================
EC GraphQL Mutations

The syntax of a GraphQL mutation is the same as for a query. The only syntactical difference is that the query operation must be mutation rather than query. But whereas a query is read-only, the main purpose of a mutation is to modify data during the processing of the request.

Unlike query operations, mutation operations are always processed in sequential order as they appear in the request, top to bottom.

This chapter focuses on how to modify the EC domain model.

How to Modify the EC Domain Model Using GraphQL

EC GraphQL supports basic mutations such as insert, update, merge and delete on EC classes.

The following is an example of mutations defined for the AREA class:

type Mutation {
  insert_AREA(records: [AREA_Record!]!): [AREA!]!
  update_AREA(records: [AREA_Record!]!): [AREA!]!
  merge_AREA(records: [AREA_Record!]!): [AREA!]!
  delete_AREA(records: [AREA_Record!]!): Void
}
Insert

An insert mutation takes a list of objects of EC domain model input type as input. During execution it inserts the provided objects into the corresponding EC class view, followed by a fetch operation which returns the inserted objects.

Following is an example of inserting a T_BASIS_OBJECT and related T_BASIS_ACCESS object:

{
  "query": "mutation($objects: [T_BASIS_OBJECT_Record!]!, $access: [T_BASIS_ACCESS_Record!]!) {
    insert_T_BASIS_OBJECT(records: $objects) {
      OBJECT_ID
      OBJECT_NAME
      OBJECT_DESCR
      REL__APPLICATION {
        APP_NAME
      }
      meta {
        createdBy
        recId
      }
    }
    insert_T_BASIS_ACCESS(records: $access) {
      T_BASIS_ACCESS_ID
      LEVEL_NAME
      OBJECT_NAME
      REL__T_BASIS_ROLE {
        ROLE_NAME
      }
    }
  }",
  "variables": {
    "objects" : [
      {"APP_ID": 1, "OBJECT_ID": 99999, "OBJECT_NAME": "AREA", "OBJECT_TYPE": "CLASS", "OBJECT_DESCR": "GraphQL insert test"}
    ],
    "access": [
      {"APP_ID": 1, "OBJECT_ID": 99999, "ROLE_ID": "SYST.ADM", "LEVEL_ID": 40},
      {"APP_ID": 1, "OBJECT_ID": 99999, "ROLE_ID": "SCHEDULER", "LEVEL_ID": 10}
    ]
  }
}

The insert mutation returns the inserted objects with the requested fields as specified in the query:

{
  "insert_T_BASIS_OBJECT": [
    {
      "OBJECT_ID": "99999",
      "OBJECT_NAME": "AREA",
      "OBJECT_DESCR": "GraphQL insert test",
      "REL__APPLICATION": {
        "APP_NAME": "EC"
      },
      "meta": {
        "createdBy": "sysadmin",
        "recId": "077a0ec00d6b4adcaf551a3f1a67d764"
      }
    }
  ],
  "insert_T_BASIS_ACCESS": [
    {
      "T_BASIS_ACCESS_ID": 8475,
      "LEVEL_NAME": "
…[truncated]


==========================================================================================
## [5/19] EC GraphQL Directives
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/graphql/graphql-directives.html
==========================================================================================
EC GraphQL Directives

Directives are instructions that can alter the execution and output of a query. They can be used to transform the query output structure, to format field values and many other things. GraphQL has only a small number of standard directives. Most of the directives available in the EC GraphQL service are EC specific.

Syntax

Directives look like annotations, having an @-symbol in front of the directive name, optionally followed by parameters.

For example, the standard @include directive is defined like this in the schema:

directive @include(if: Boolean!) on FIELD | FRAGMENT_SPREAD | INLINE_FRAGMENT

The placement of a directive in the query depends on what parts of the query the directive supports. Valid positions are defined in the directive definition in the GraphQL schema. The most common placements are on individual fields or on the query itself. The schema lists all available directives, what parameters they take, and where in the query they can be used.

For example, the @include directive can be used on fields like this:

query($includeMeta: Boolean!) {
  COUNTRY {
    OBJECT_ID
    NAME
    meta @include(if: $includeMeta) {
      lastUpdatedDate
      recId
    }
  }
}

Some directives are repeatable, which means they can be used multiple times in the same location. There can also be multiple different directives in the same location. Multiple directives in the same location are typically processed in order of appearance. This makes it possible to chain directives that operates on the output of the previous directive.

Directives are not limited to queries. They can also be used on type definitions in the schema itself if the directive was created for this purpose. In that case it is the schema author who decides how to use the directive and where to place it.

Directives

The query directives available in EC are:

@distinct

@group

@include (standard)

@limit

@move

@put

@reduce

@remove

@skip (standard)

@trim

@void

This section describes each of them with usage examples.

@distinct
directive @distinct on QUERY | FIELD

The @distinct directive removes duplicate items from list type fields. When placed at query level the directive performs deep removal of duplicates from all nested lists at any level of the output structure. The directive has no effect on scalar and object type fields. List and object type fields are compared deeply when determining if they are identical.

Examples:

Query with duplicates in the result
Query with duplicates removed using the @distinct directive at field level
Query with duplicates re
…[truncated]


==========================================================================================
## [6/19] EC GraphQL Transformations
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/graphql/graphql-transformations.html
==========================================================================================
EC GraphQL Transformations

By default the output structure of a GraphQL query matches the structure of the schema types and fields that are being queried. If the schema types are not perfectly modelled to match the client domain, the query result might not be in the desired format.

Transforming the results of a query can be achieved in a number of ways:

A transformation engine is available as part of the EC GraphQL service. This document focuses on this option.

GraphQL directives can be used for simple transformations within the query itself.

Transform the raw JSON result on the client side using a 3rd party JSON transformation engine of your choice.

Extend the EC GraphQL schema and model your domain properly, eliminating the need for transforming the output.

Advanced Transformations in the EC GraphQL Service

The EC GraphQL service provides a JSON transformation engine as part of the service. The engine is based on a Java implementation of the popular JSONata engine for Javascript.

To apply JSON transformations as part of a request to the EC GraphQL service, add an attribute called transformation to the request. The value of this attribute is a string holding the transformation definition in JSONata syntax. Remember to escape double-quoutes in the definition to avoid invalid request JSON.

Example request that fetches a list of LANGUAGE objects each holding a NAME attribute and transforms the output into a simple list of languages:

Request	Result

{
  "query": "query { LANGUAGE { NAME } }",
  "transformation": "{ \"languages\": LANGUAGE.NAME }"
}
	
{
  "languages": [
    "English",
    "Norwegian",
    "Dutch",
    "Italian",
    "Spanish",
    "German",
    "Danish",
    "Swedish"
  ]
}

The syntax of the transformation language is well documented on the JSONata website. There is also a playground where you can paste your output JSON and play around with the transformation syntax.

References

JSONata website: https://jsonata.org

jsonata-java: https://github.com/dashjoin/jsonata-java


==========================================================================================
## [7/19] EC GraphQL Operations
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/graphql/graphql-operations.html
==========================================================================================
EC GraphQL Operations

EC has extended the standard GraphQL request format with an operations attribute that provides a way to execute multiple operations within a single request. This makes it possible to execute a series of queries, mutations and transformations for advanced request processing. The attribute is a list of operations to execute. Refer to the request format for the syntax definition of the operations attribute.

An operation is either a query or a transformation. A query operation fetches data just like a standard single query. It can also mutate data. A transform operation alters the output of a query operation or the contents of a variable. The transformed data can then be used as input to subsequent operations.

The list of operations is processed sequentially from top to bottom. The output of all query operations that are not marked as excluded are merged together into the final response. The output of transform operations can also be merged into the response if marked as included.

Query Operations

A query operation fetches or mutates data. Refer to the request format for the syntax definition of the query operation.

The GraphQL query or mutation to execute is provided using the query attribute. Existing variables or output from preceding query operations can be used directly as input parameters in the GraphQL query.

If a query operation is named by specifying the name attribute, subsequent operations can use the output of the query as input by referring to this name. The name can also be used to replace the query output with transformed data.

By default all query operation output is included in the final request response by merging the query output JSON objects together into one final JSON object. If the query is only meant as an intermediate step, the output can be excluded from the final response by setting the exclude attribute to true.

Example request:

The first operation is a query operation that fetches the object ids of well deferments that meet certain conditions. The query is named wellDeferments so that its output can be used in the next operation. The operation is marked as excluded because we don’t want to include this intermediate output in the response.

The second operation is a transform operation that extracts the object ids from the output JSON object of the first operation into a list of string values that are stored in a variable called wellIds for later use.

The third operation is a query operation that uses the list of well ids created in the previous operation as input by using the variable name as its 
…[truncated]


==========================================================================================
## [8/19] EC GraphQL Schema Extensions
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/graphql/graphql-schema-extensions.html
==========================================================================================
EC GraphQL Schema Extensions

The EC GraphQL service provides schema types for all EC classes and their attributes and relations. While this enables extracting all domain model data, there are scenarios where this is not sufficient. For example:

The desired output format is significantly different from the EC domain model hierarchy.

You require conditions and logic that is not possible to achieve using query syntax and directives.

The data comes from other sources than the EC domain model or must be calculated dynamically.

Situations like these can be solved by extending the EC GraphQL schema with your own custom types and type hierarchies. You can define types that match your desired output and write field resolvers that return the data you require. Schema extensions can be provided to the EC GraphQL service both from EC mothership modules and EC extensions.

Custom Schema Provider

To provide your own schema extension, implement the com.ec.frmw.graphql.spi.GraphQLSchemaProvider Java interface and register it as a Java service in your jar. The EC GraphQL service automatically detects the implementation classes and includes their custom types in the schema.

To register a Java service, create a file called com.ec.frmw.graphql.spi.GraphQLSchemaProvider in the src/main/resources/META-INF/services directory of your project. Write the name of your implementation class with full package path in the file.

Schema Provider SPI

The service provider interface is located in the com.ec.frmw.graphql.spi package in the frmw-graphql project.

The main GraphQLSchemaProvider interface has a single method that returns a GraphQLSchema. Your interface implementation must build an instance of this class.

The GraphQLSchema class has methods for adding type definitions both textually and programmatically. You can use both at the same time if some types are fixed and others must be generated dynamically based on config.

The simplest way to add your own GraphQL types is to define them textually using the same syntax as you see when looking at types in the existing GraphQL schema. It is also possible to extend existing types by adding new fields to them. To make custom types queriable without extending existing types, a custom schema must add at least one field to the top level Query type. This field acts as the starting point for querying your custom type hierarchy.

Additionally, the GraphQLSchema class has methods for hooking up field resolvers, also called data fetchers, to the fields in the custom types. A resolver is basically a function that returns the data this f
…[truncated]


==========================================================================================
## [9/19] EC Data Access Control (eDAC) Functional Guide
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/edac/edac-functional-guide.html
==========================================================================================
EC Data Access Control (eDAC) Functional Guide
eDAC Control Layer

The eDAC access control logic is added as a where-clause predicate (condition) in the generated EC class view. eDAC predicates are added to object, interface, data and table class views depending on the configuration. No eDAC predicates are applied to DB tables and hand-coded views, i.e. data that is accessed through the generated class view will be subject to access control. Data that is accessed directly from DB tables and hand-coded views will not.

eDAC Root Access Control Level

The object class is the root level for the eDAC predicates. EC maintains an Access Control Lookup list (ACL) for all access controlled object classes. The object class eDAC predicate will do a direct object id lookup against the ACL list to determine if a given user has access to that object (based on his/her explicitly assigned roles). eDAC predicates for the other class types will do indirect lookups of the owner class id or related class id.

eDAC Control Effect

From EC-12.0, all EC classes are access controlled. The access control setup will determine if the generated eDAC predicate is empty, or whether the predicate grants access based on direct or indirect ACL lookups. An empty eDAC predicate means that all users can see all class records. A non-empty eDAC predicate will filter the result set according to the content of the ACL list and the users assigned roles. The fact that the eDAC predicate is built into the generated class view means that the Application layer and DB layer have a unified view of the data.

Report View

Report views will get the same eDAC predicate as the corresponding class view.

Journal View

No eDAC predicates are generated for the journal views.

Feature Matrix Comparison of EC Data Access Control Between Pre EC-12.0 and eDAC from EC-12.0
Terminology

Direct Access Control

Only applicable for object classes. Access to records is determined by a direct ACL lookup for the object class itself. A user will get access to an object if the corresponding object id and user role can be found in the ACL table for that class (user must have at least one of the roles to get access).

Relational Access Control

Applicable to object, data and table classes. Access to records is determined by an indirect ACL lookup for one or more related objects.

Reference Access Control

Access to records is controlled via a reference class. Only used in rare cases when an object belongs to multiple object classes.

Active Object Partitioning Indicator

Class-level property that indicates whether an obje
…[truncated]


==========================================================================================
## [10/19] EC Data Access Control (eDAC) DB Upgrade Guide
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/edac/edac-upgrade-guide.html
==========================================================================================
EC Data Access Control (eDAC) DB Upgrade Guide
Introduction

EC-12.0 introduces a new unified EC Data Access Control mechanism (eDAC). This document describes the strategy for upgrading the access control setup from EC-11.2.SP03 to the new eDAC standard. Please refer to "EC Data Access Control (eDAC) Functional Guide" for details on the new standard.

Purpose

The EC upgrade package will contain auxiliary scripts that can be used to translate the access control setup from EC-11.2.SP03 to an EC-12.0/eDAC compliant setup. Please note that from a business perspective the resulting setup will be equivalent to the original, i.e. users will get access to the same rows as before. The internal implementation and configuration are different, however.

Abbreviation Definition

Active Object Partitioning Indicator (ACCESS_CONTROL_IND property on the class)

Object Partitioning (OP)

Ringfencing (RF)

Upgrade Strategy

In EC-12.0, it is not possible to partition an object class unless the Access Control Indicator on the class is set to 'Y'. The upgrade scripts will, therefore, set the Access Control Indicator to 'Y' for all object classes that have a valid OP configuration. Prior to EC-12.0, users without a partitioned role would get access to all the objects in a class. With eDAC, this is no longer the case. If an object class is access controlled, users will get access according to their explicitly assigned roles. They will no longer get access due to a lack of partitioned roles. To ensure that users get access to the same data after the upgrade, a new role with full access will be created for each partitioned class. That role will then be assigned to users that had full access due to a lack of partitioned roles.

The following table describes the technical details of the upgrade strategy:

Oracle Version	Legacy Mode	eDAC Context Translation


Oracle SE

	

Only OP

	

Each object class without valid OP configuration:

Do Nothing

Each object class with valid OP configuration for one or more roles (role_list):

Set ACCESS_CONTROL_IND = Y for the class

For users that have one or more roles from role_list:

Do nothing

If there are users without any roles from role_list:

Create new role named 'eDAC_$class_name$' with ALL operator.

Assign 'eDAC_$class_name$' to all users without roles in role_list




Oracle EE

	

OP + RF

	

Each object class ACCESS_CONTROL_IND <> Y and with valid OP configuration on roles (role_list):

Set ACCESS_CONTROL_IND = Y for the class

For users that have one or more roles from role_list:

Do nothing

If there are users without any role
…[truncated]


==========================================================================================
## [11/19] How to configure EC Data Access Control (eDAC)
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/edac/edac-how-to-configure.html
==========================================================================================
How to configure EC Data Access Control (eDAC)
Pre-requisite

Before reading this documentation, please read EC Data Access Control (eDAC) Functional Guide first.

Introduction

In the following sections, a short step-by-step configuration guide is provided for three simple scenarios: Direct Access Control, Reference Access Control, and Relational Access Control.

Method	Description


Direct Access Control

	

Direct access control can only be applied to object classes.

Add class property with property code ACCESS_CONTROL_IND and property value Y

Configure object partition




Reference Access Control

	

Reference access control can only be applied to an object class from another (readonly) object class that list a subset of the first object class. Example: CONTRACT and TRAN_CONTRACT, SALE_CONTRACT or REVN_CONTRACT.

Configure class dependency with PARENT_CLASS = the class with direct access control, CHILD_CLASS = the class that should be controlled, and DEPENDENCY_TYPE = ACCESS_CONTROLLED_BY

Add class property with property code ACCESS_CONTROL_IND and property value Y to the classes




Relation Access Control

	

Data class will get an automatic data access control effect when its owner object class has been set up with data access control.

Class relation between object classes

Add class property with property code ACCESS_CONTROL_IND and property value Y to the classes

Add class relation property with property code ACCESS_CONTROL_METHOD and value TO_CLASS if the to class access is controlled by the from class or value FROM_CLASS if the from class access is controlled by the to class

Class relation from object class to data/table class

Add class relation property with property code ACCESS_CONTROL_METHOD and value ACL_LOOKUP

Direct Access Control

Direct access control can only be applied to object classes. When you decide to enable data access control on an object class, you have to add a class property with property code ACCESS_CONTROL_IND and property value Y.

We use owner context 1000 throughout the documentation example, but you have to decide your owner context properly for your project.

As an example, we start by adding the class property ACCESS_CONTROL_IND on CONTRACT class. This can be done using the Class Model Editor tool as shown in the figure below.

Figure 1. Adding the class property ACCESS_CONTROL_IND on CONTRACT class

The produced class extension xml file would look like this:

Listing 1. Class xml for adding the class property ACCESS_CONTROL_IND on CONTRACT class
<?xml version="1.0" encoding="UTF-8"?>
<class-ref owner-cntx=
…[truncated]


==========================================================================================
## [12/19] How to configure EC Data Access Control for external database user
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/edac/edac_external_db_user.html
==========================================================================================
How to configure EC Data Access Control for external database user
Terminology

EC database users: EC database users refer to the ECKERNEL user and the ENERGYX user, these database users are reserved for EC application usage only.

external database users: any non-EC database users.

Motivation

Individuals or external applications that connect directly to the EC database should not connect to any EC database users when attempting to access EC data records. One or more external database users should be created specifically for that purpose. By default, an external database user does not have access to any EC data records. In this case, the EC implementation expert has to design and implement the data access control logic for external database users.

Solution

When EC implementation expert wants to grant an external database user to access EC data records, the underlying two steps need to be followed:

Link this external database user to an existing EC application user and user roles.

Allow this external database user to access EC data records.

After doing these two step, this external database user can access all the EC data records that the linked EC application user can access.

Example

In the following section, we will give a project example to show how to grant an external database user to access EC data records.

User Story: there exists an EC application user testappuser with roles TESTROLE1 and TESTROLE2 which can access only one EC data record Norway from the Country object class. When an existing external database user EXTDBUSER connects directly to the EC database, we would like that EXTDBUSER can access all the EC data records that testappuser can access.

Configuration Step:

Grant necessary system privileges to EXTDBUSER.

GRANT CREATE SESSION TO EXTDBUSER;
GRANT CREATE SYNONYM TO EXTDBUSER;

Then link EXTDBUSER to EC application user testappuser by creating a logon trigger.

CREATE OR REPLACE TRIGGER zt_logon_schema
AFTER LOGON
ON EXTDBUSER.SCHEMA
DECLARE
BEGIN
    IF USER = 'EXTDBUSER' THEN
        dbms_session.set_context('CLIENTCONTEXT', 'USER', 'testappuser');
        dbms_session.set_context('CLIENTCONTEXT', 'ROLES', '#$TESTROLE1$#TESTROLE2$#');
    END IF;
END;

Allow EXTDBUSER to access EC data records by adding explicit access logic in allowAccessToGlobalContext function of ue_ringfencing package.

CREATE OR REPLACE PACKAGE BODY ue_ringfencing IS
    FUNCTION allowAccessToGlobalContext
    RETURN BOOLEAN
    IS
    BEGIN
        IF USER = 'EXTDBUSER' and sys_context('CLIENTCONTEXT', 'USER') = 'testappuser' THEN
        -- please
…[truncated]


==========================================================================================
## [13/19] Introduction to Reporting in EC
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/reporting-and-analytics/reporting_in_ec.html
==========================================================================================
Introduction to Reporting in EC
Introduction

This document will give an introduction to the reporting capabilities in EC.

EC has a reporting system based on report templates. This system can be used to configure, generate, distribute and publish fixed reports in different formats using different 'report engines'. The report engine can either be provided by the EC product or by the customer project. The processes can be automated using the Scheduling or the Process Automation system.

For ad-hoc reporting, EC Reporting and Analytics can be used.

For simple export to Excel, the screen 'Export to Excel Express' can be used. Reports defined in this screen are not connected to the report template system. For more information on this, see the online help for the screen (RP.0011 – Export to Excel Express).

The sections below will give a high-level description of the system based on report templates.

Conceptual Overview

The screenshot below shows how reports are generated using an internal report engine. All processing is done by the EC system. The data is read from the EC database through the same database user as the application. When the report is generated, it is streamed directly to the database as a BLOB (binary large object). The generation process is synchronous. However, the call to the report engine is asynchronous so that when clicking the Report Generation button, it will send an asynchronous call to the report engine. This implies that the application will not wait for the report engine to finish.

Figure 1. EC internal report engine

The screenshot below shows the involved entities when using an external reporting engine. The report engine will normally be running on a separate server. The interface between EC and the report engine is implemented by sending commands to the report engine to a database table. It is then the reporting engine’s responsibility to read and process this information on a regular basis. The generation process is asynchronous. The generated report will end up in the same place as when using the internal report engine.

Figure 2. External reporting engine and its relation to EC
Configuration of Reports

The configuration of a report will contain different steps based on the type of report and how the report is to be used. However, all reports will need a report template, a report definition and a report (also called report runnable).

Step 1: Create and deploy the report

Before a report can be configured in EC, necessary template files must be created and made available to the EC system. For an Excel report this is a x
…[truncated]


==========================================================================================
## [14/19] How to use EC’s Reporting and Analytics
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/reporting-and-analytics/ec_reporting_and_analytics.html
==========================================================================================
How to use EC’s Reporting and Analytics
Introduction

EC utilizes Yellowfin to perform reporting and analytics. This document describes some basic steps for logging on to Yellowfin and to be able to create reports in Yellowfin.

Yellowfin uses a Data Source to connect to the database. The default data source for EC is called ECDS. This data source uses the ANALYTICS_<operation> database user to connect to the EC database. This database user has read access to views in the EC database. The Analytics Object Access screen in EC is used to configure which database views the ANALYTICS user has access to.

Yellowfin "views" are created using the data source. Yellowfin reports are created from Yellowfin "views". For more information about Yellowfin, see the Yellowfin Guide (https://wiki.yellowfinbi.com/display/yfcurrent/Yellowfin+Wiki+Home).

Configure Analytics database user access to EC database views

The Analytics Object Access screen is used to configure which views the ANALYTICS user has access to.

Figure 1. Analytics Object Access

The views are grouped using the class’s application space context (EC_FRMW, EC_PROD, etc), class type (object, data, etc.) and "class view", reporting view, or journal views. Select the object type and press the Go button to list the views. Tick the Access checkbox to give the ANALYTICS user access to that view. Untick the checkbox to remove access to that view. Click the Apply Changes button to update ANALYTICS access to views. For more information see the online help for the screen.

Yellowfin and Keycloak

The Yellowfin SAML Bridge is used to interface between Keycloak and Yellowfin. Use the url http://<yellowfin host>:<yellowfin port>/ra to log on to Yellowfin using Keycloak authentication. When a user authenticated by Keycloak is missing in Yellowfin, a new user is created in Yellowfin and assigned a default role (i.e. Consumer & Collaborator). The Yellowfin SAML Bridge uses a Yellowfin user with rights to create new users. The user is configured using the ECRA_ADMIN_USERNAME and ECRA_ADMIN_PASSWORD environment variables in your container configuration.

Yellowfin Data Source

The data source can be viewed from the Admin Console in Yellowfin (click  in the upper-right corner and select Admin Settings).

Click on the Data Sources to list the data sources.

Figure 2. Yellowfin data source list

Click on the ECDS to open the ECDS data source.

Figure 3. ECDS data source
Authentication Adapter

When EC Data Access Control (eDAC) is configured, Authentication Adapter must be set to Oracle AppContext Authentication. When eDAC 
…[truncated]


==========================================================================================
## [15/19] Database Reporting Layer
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/reporting-and-analytics/database_reporting_layer.html
==========================================================================================
Database Reporting Layer

This document gives a high-level description of the generated reporting layer shipped with Energy Components.

Overview

The overall purpose of the reporting layer is to make end-user reporting much easier and quicker.

Figure 1. Reporting layer overview
Architecture

This figure displays the high-level architecture of the reporting layer.

Figure 2. High-level architecture of the reporting layer
Reporting views (RV views)

One RV view will be generated for each data class, object class, and table class configured in EC. The RV view will include:

All attributes from the owner class (object class).

All attributes from the data class.

Reporting views always show the correct configuration for the selected production day(s).

All report unit configured (see screenshot).

A dedicated REPORTING_<operation> Oracle database user is created. This user id has read access to all RV views.

Figure 3. Measurement types TEMP has report unit C (Celsius) and F (Fahrenheit)

Any temperature attributes with property UOM_CODE = TEMP, will get two columns in the reporting view. One for C (Celsius) and one for F (Fahrenheit). The columns will get a _C and _F postfix to the attribute name. The end user who creates the reports does not need to know which unit is stored in the database, the reporting layer will automatically perform the conversion between units.

Reporting views (RV_) are not updatable.

Query Guidelines

Reporting views can potentially return a large number of records and columns from the database. The number will depend upon how many objects are defined in the database, and how many years of historical data are available.

As a general rule always

List which columns you want to extract from the view (avoid select * from)

Add where-condition for production day

Where production_day between…..

Where production_day = …….

Add where-condition for objects to extract if not all objects are of interest

Where op_fcty_1_code = 'AAAA' (e.g. get all objects which are connected to operational facility 1 code 'AAAA' only)

Where …………

View Listing

The SQL below can be used to list all DATA, OBJECT, and TABLE reporting views:

SELECT class_type, 'RV_'||class_name, label FROM class WHERE class_type IN ('DATA','OBJECT', 'TABLE') ORDER BY class_type, class_name;


==========================================================================================
## [16/19] How to create, install and configure a Jasper Report
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/reporting-and-analytics/how_to_create_jasper_reports.html
==========================================================================================
How to create, install and configure a Jasper Report
Introduction

JasperReports is a popular open source reporting engine. It is able to produce pixel-perfect documents that can be exported to different formats. Jasper reports are based on Jasper Report Definition files. These files can be created using a third party tool. JasperSoft provides a tool called Jasper Studio. It will be the customer’s responsibility to provide users with tooling for this. See https://community.jaspersoft.com/. There is both a community- and a professional edition of Jasper Studio.

Jasper Report Definition files can be uploaded into EC-RA. Refer to Yellowfin and Jasper Reports

EC supports Jasper Reports through EC-RA and directly in EC.
Jasper Report support in EC

Currently, we support PDF, Excel, and XML, and we support the database as an input source. We support Jasper Reports version 7.0.1 and 6.21.4. Jasper version 6.x is marked for deprecation and will be removed in a future release.

You should not use a higher version of Jasper Studio than 7.0.1, because a newer version could potentially produce report definitions that are incompatible with the Jasper version supported by EC.

Refer to Energy Components Software Development Kit (EC-SDK) for full examples on how to create (using third party tool) and deploy jasper reports via extension:

energycomponents-sdk/examples/extensions/70-report-jasper

energycomponents-sdk/examples/extensions/71-jasper-fonts

energycomponents-sdk/examples/extensions/72-jasper-report-v7

Optional Excel Report Parameters Configuration

JasperReports offers some additional parameters to be set when the report is configured to generate an Excel report. To be able to set these parameters for a Jasper report configured in EC, some special report parameters can be added to the report template (in the Report Template screen). For example, the Excel report can be configured to generate a multi-sheet report. All these special parameters are prefixed with the word "EXPORTXLS_" and they are case-sensitive. Therefore, they should be written exactly as given. Below is the list of parameters supported by EC.

Parameter Name	Parameter Sub Type	Description


EXPORTXLS_autoFitPageHeight

	

String

	

The value must be true/false. The value determines whether the fit height should be estimated automatically.




EXPORTXLS_firstPageNumber

	

Number

	

The value must be an integer. The number specifies the first-page number in the page setup dialog.




EXPORTXLS_fitHeight

	

Number

	

The value must be a number. The number specifies the number of vertical
…[truncated]


==========================================================================================
## [17/19] How to configure EC Standard Reports
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/reporting-and-analytics/how_to_config_ec_standard_reports.html
==========================================================================================
How to configure EC Standard Reports
Introduction

There are several 'out of the box' reports available in the system. These are referred to as 'Standard Reports'. EC Framework contains standard reports for general purposes. Similar reports will also be available for the other products in EC. They can be used as templates for customer specific reports, or just out of the box.

The reports are based on JasperReports, and the Jasper definition files are included in the frmw-report-web.war found inside ec-app.ear. The files are found under the folder reports\jasper. When using these reports as the starting point for your own customer specific reports, these files should be copied to a separate customer specific war-file. They can be edited directly as a text file or using a tool like iReport.

The following reports are currently supported:

Check Rule Log

User Access by User

User Access by Role

EC Role Privileges

EC Unit Conversion

To use a standard report a report template, a report definition and a report need to be created. The next sections will show how to configure each of these reports.

This section is organized with one chapter per report.

Check Rule Log

The check rule log report shows open check rule validation issues reported in the EC check rule log. Acknowledged issues are not included in this report.

The report uses the following report-specific parameters:

FROMDATE

	

Include log entries from this date.




TODATE

	

Include log entries to this date (inclusive).




SYSTEM_NAME

	

Name identifying the company/facility/system/etc of the report. Appears in the report header.

Report Template

Configure the report template as shown below. Attributes with user-defined values are not listed.

System

	

EC Jasper Report

Jasper Definition Url

	

/com.ec.frmw.report/reports/jasper/checkrule_log.jasper

Parameter Name	Parameter Type	Parameter Sub Type	Mandatory


FROMDATE

	

Basic Type

	

DATE

	

No




TODATE

	

Basic Type

	

DATE

	

No




SYSTEM_NAME

	

Basic Type

	

STRING

	

No




FORMAT

	

EC Code Type

	

REPORT_FORMAT

	

Yes

Report Definition

Configure the report definition as shown below. Attributes with user-defined values are not listed.

Functional Area

	

EC

FORMAT

	

pdf

User Access by User

The user access by user report shows all users who have privileged EC user access. These users also have Root-role and Web-access roles.

The report uses the following report-specific parameters:

SYSTEM_NAME

	

Name identifying the company/facility/system/etc of the report. Appears in the report header.

Report Temp
…[truncated]


==========================================================================================
## [18/19] How to generate an XML-report based on a PL/SQL function
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/reporting-and-analytics/how_to_gen_plsql_xml_reports.html
==========================================================================================
How to generate an XML-report based on a PL/SQL function

This is a step-by-step guide for how to configure an XML-report based on a PL/SQL function. The solution is based on the report system EC Internal. It will work as in EC 10 but is deprecated.

General knowledge about PL/SQL and the report system in EC is required.

Step-by-step guide

The db-package 'ue_report' contains the method 'generateXml'. This method needs to be implemented to return a string containing the XML-report.

See How to manage User Exit packages for more information about user exit package.

The parameters 'p_arg1, p_arg2 …​' can be used as you wish. Typically, the first argument can be used to route to the correct report to generate.

Create a new report template.

Select 'EC Internal' as report system (Note, if EC Internal is not available, you need to enable this. Go to EC Codes, and select code type 'REPORT_SYSTEM'.)

Add '/com.ec.frmw.report.screens/gen_xml_report_db' as the report template.

Add the parameters FORMAT, XML_ARG1, XML_ARG2…​ XML_ARG7, with parameter type 'BASIC_TYPE' and subtype 'String'.

Create a new report definition with the new report template.

Set FORMAT to 'xml'.

Create a new report in Report Administration based on the new report definition.


==========================================================================================
## [19/19] How to Configure Report Access
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/reporting-and-analytics/how_to_config_report_access.html
==========================================================================================
How to Configure Report Access

This article provides an overview of how to configure access to report files that are stored in EC.

Introduction

Key to access control is setting up object partitioning/ringfencing on the EC classes and class objects used to determine access to a report. This guide does not go into the details of how to configure object partitioning on a class. That is explained in How to configure EC Data Access Control (eDAC). In this guide we will focus on the parts of the report configuration that affects access control and what EC classes to apply object partitioning on.

There are several layers of access control for reports. Each layer is optional, but they are cumulative. A user must meet the requirements of all enabled layers to gain access to the report.

Basic Access Control with Functional Area and Report Area

Report definitions can be linked to a specific functional area and report area. This is configured in the Report Definition screen (RP.0002).

Figure 1. Setting functional area and report area on a report definition.

This can be used to control access to groups of reports based on what functional area or report area they belong to. All reports linked to a specific functional area object or report area object are subject to the object partitioning rules configured for that object.

The EC classes to set up object partitioning on in this case are called FUNCTIONAL_AREA and REPORT_AREA. You can set up access control for either or both classes based on your needs.

For example, if object partitioning is enabled for the FUNCTIONAL_AREA class and access to a functional area object called "Allocation" is granted to a user role called "Alloc Reports", only users having the "Alloc Reports" role will be able to view and download reports that are linked to the "Allocation" functional area.

Published reports that are based on uploaded external files are not linked to a report area. As a result, object partitioning on report area can not be used to control access to published uploaded reports. See Access Control for Published Reports.
Fine Grained Access Control with Report Parameters

Access control on specific generated report files is possible if the report has parameters of type "EC Object Type". Enabling object partitioning on the EC class of the parameter object type ensures that only users who have access to that object can view and download the report.

For example, a report might have a parameter of object type "Company". When generating this report with the company parameter value set to "ECLNG Norway", only users that 
…[truncated]