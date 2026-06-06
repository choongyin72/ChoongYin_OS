# Raw content — DOC-07
Modules: ['frmw/ecis', 'frmw/event']
Pages: 25



==========================================================================================
## [1/25] EC Event Architecture
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/event-architecture.html
==========================================================================================
EC Event Architecture

Energy Components provides a generic publish-subscribe service where events can be published, and subscriptions to application logic can be registered.

Features

support asynchronous concurrent pub-sub.

support forwarding events to external parties.

support consuming events from external parties, and processing them in EC.

Our Event processing Engine is implemented using the Apache Camel framework.

Publish Events

Publishing events have been added to a number of core parts of EC, including the domain model.

Examples: Publish events…​

…​when changes (data updated, inserted, deleted) to any domain object occur in EC.

…​when any CheckRules fails or succeed.

…​when any job (e.g. dispatch-calculation, report-generation) completes.

…​when the data set in a month has been approved and locked.

Publishing custom events are also supported by using the EC Event API.

Subscribe to Events

Subscribing to events can be done by either using our EC Event APIs or using the screens in EC to configure what actions (jobs, business logic) should be performed when an event is received.

For example, when new data has been imported into EC, we would like to execute a calculation or generate a report.This can be archived by setting up a subscription on the DomainObjectChanged event, with a specific filter and associate it with the job (business logic) to perform.Have a look at the new features added to the Scheduler web page in EC, where you can do this with pure configuration, no coding needed.

Bridge Events from external systems (Inbound)

In addition to events that originates from EC itself, receiving or consuming events from external sources are also supported.External systems can use the public EC Rest APIs to forward (or bridge) external events into EC.See Bridge Events from external systems and the EC Rest API documentation for more details.

Bridge Events to external systems (Outbound)

EC can also be configured to forward events from EC to external systems. See Bridge Events to external systems for more details.


==========================================================================================
## [2/25] EC Event API
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/event-api.html
==========================================================================================
EC Event API
Overview

EC Event API currently consist of three part:

Event API — Java

Event API — database

Event API — REST

The API provides a generic publish-subscribe service where events can be published, and subscriptions to application logic can be registered. The implementation of the API does not handle the routing of events itself, it will just act as proxy and hand the work over to the real pub-sub engine. The engine we use behind our API is Apache Camel. In addition, we use Apache ActiveMQ to support durable (persisted) events.

Event API — Java

The API is simple, it supports publishing events and subscribing to them via these two APIs:

EventMgr.getService().publish(String channel, Event event);
EventMgr.getService().subscribe(String beanExpression, Predicate<Event> filter, EventExecution execution);
You can also subscribe to Events by using the annotation @SubscribeToEvent.
Examples
1 Publish event
Event event1 = new Event(EventType.TestEvent, this);
EventMgr.getService().publish(event1);

This code example will create an Event with EventType as TestEvent, and then publish the event (on the default channel).

2 Publish event with payload
Event event2 = new Event(EventType.TestEvent, this);
event2.setPayload("param01", new BigDecimal("3.14"));
event2.setPayload("calculationMethod", "advanced");

EventMgr.getService().publish("test-channel", event2);

Here we create an Event with EventType as TestEvent, set two parameters and then publish this event to the 'test-channel'.

3 Publish event and wait for it to finish
// Create an Event, fill in data
Event testEvent = new Event(EventType.TaskStatus, this);
testEvent.setPayload("task-status", "PROVISIONAL");

// Publish the event, and wait for all subscribers to finish
EventMgr.getService().publish(Event.CHANNEL_MOBILE_NOTIFICATION, testEvent).get();

// If any of the subscribes add data to the event, we can read it like this (but only if we have waited for completions):
String myResult = testEvent.getPayload("theResult", "magic");

// The event contains a context map with parameters from the execution.
// We can get a list of all subscriptions that were executed:
log.info("These subscriptions where sucessfully run: " + testEvent.getContext(CONTEXT_SUBSCRIBED_BY, null));

The publish(event) method returns a standard Java Future<Event> object. To wait for completions call the Future.get() method. Note that there is no way to tell up front how long time this will take, especially since more subscriptions can be added later. To avoid waiting 'forever', you can set a timeout, like this: publish("so
…[truncated]


==========================================================================================
## [3/25] Publish Events
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/event-publish.html
==========================================================================================
Publish Events
Overview

Publishing Events can be done by several different mechanisms in EC.

Automatically

Several key areas of EC automatically publish events. Some examples include:

JobCompleted event when a business action (or job) completes. E.g. after an allocation calculation or report generation completes.

TaskStatus event when an EC BPM process changes status.

ExtensionRunning and stopping events when an EC Extension changes status.

CheckRuleIncident event when a check-rule incident happens in EC.

and many more…​.

These events are always published, no configuration is needed.
To see a full list of all the supported events, see Event Types.

Automatically — when EC Domain Object are updated (database)

EC can be configured to automatically publish events when any domain object in EC changes. This makes it possible to automatic publishing events whenever for example WELL changes in EC. All domain objects ('classes') in EC can be configured to publish events when they are being updated. This includes any insert, update and delete operations against this 'class' in the database.

For example, we would like to get notified when the tank level changes, so that we can start a new calculation or generate a report. We can achieve this by doing:

configure the domain class TANK_DAY_INV_OIL by setting the class property PUBLISH_EVENTS_IND to Y and regenerate the class view.

select the job (or create a new), in the Schedules screen, that you want to be executed in response to the event.

open the Event Subscriptions tab and add a subscription to DomainObjectChanged event. Also make sure the parameter Class Name has a required value of TANK_DAY_INV_OIL.

update the tank level (TANK_DAY_INV_OIL.DIP_LEVEL) and verify that the job/schedule has been executed.

The tank level can be updated using the EC web pages, through a calculation, by the ECIS data import, directly in the database, or from external access through the Rest APIs. The method used to update the tank level does not matter, a DomainObjectChanged event will always be published.
Programmatically

Our APIs can be used programmatically, both from Java code and also directly from the database to publish events.
See EC Event API for more details.

Inbound from external system

We also support publishing events received from external systems. See Bridge Events from external systems


==========================================================================================
## [4/25] Subscribe to Events — and execute jobs and business logic
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/event-subscriber-configuration.html
==========================================================================================
Subscribe to Events — and execute jobs and business logic
Overview

EC support two ways of subscribing to events; either programmatically by using EC Event APIs or, described here, using a pure configuration approach.

To configure a job (or a schedule) to be triggered when a specific Event is published, open the Schedules screen (CO.0130). Then, in the Event Subscriptions tab, add a new subscriber for each Event that should trigger this job.

Example:  In this example we subscribe to the DomainObjectChanged event. We also defined a filter for the event, specifying that the event parameter className must have the value TANK_DAY_INV_OIL. The result of this is that whenever data changes in the class TANK_DAY_INV_OIL, it will immediately trigger re-generation of the report.

The same configuration can also be defined by using the Event Route Configuration (CO.1081) screen.

Stateful jobs and execution modes

The job executor will use the execution mode settings configured in the Event Route Configuration screen. Ref Execution Modes.

You can also use the Stateful setting located under the Details tab to set the execution mode to Serial.

Stateful setting	Execution mode


Off

	

Parallel




On

	

Serial


==========================================================================================
## [5/25] Bridge Events from external systems
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/inbound/event-external-in.html
==========================================================================================
Bridge Events from external systems
Overview

EC has the capability to receive events from external systems. A dedicated Rest Endpoint is available for external system to call into when they want to inform EC about something.

Please see the Rest API specification Rest Endpoints for inbound Events. Also see the EC Rest API as a general introduction to the rest APIs.

Example

We would like to inform EC about something that happen in an external system. The external system could then issue a Rest POST call against the endpoint /services/event/types/{eventType}/events, like this:

Rest call
POST https://<EC-url>/rest/v1/services/event/types/TestEvent/events
with the following JSON payload:
{
  "eventType": "TestEvent",
  "channel": "ec-channel",
  "payload": {
    "param1": true,
    "param2": "some-very-important-data",
    "param3": 123321
  }
}
Please note that a number of preconditions must be met for this call to succeed. E.g. the EventType (TestEvent) must be valid, it must be allowed to originate from external parties and the authentication and authorization for this resource must be configured in EC.
If the external system is informing EC about an incident that are unknown to EC, it might be preferable to create a new custom EventType to represent this incident.
See Event Types — Custom for more details.
Energy Components SDK Example

See the Energy Components SDK for an example of how an external system can publish an Event into EC by using the publish-event Rest Endpoint.


==========================================================================================
## [6/25] Bridge Events to external systems
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/outbound/event-external-out.html
==========================================================================================
Bridge Events to external systems
Overview

When processing Events, EC supports integrating with other systems. By using available components in Apache Camel we can forward/bridge events from EC to these systems. EC includes a set of ready made integrations, called Event Routes, they are listed below.

When no pre-made Apache Camel components are available, we can instead implement a custom subscriber and putting the integration code there.

Implementing support for forwarding to a new external system

First, check if EC already support integrating with the external system. Check the list of supported external systems below. Maybe you can use the generic WebHook integration.

To integrate with a new external system, create a new java class implementing com.ec.frmw.eventproxy.route.EventRoute interface. Implement the method RouteBuilder configure() that should return a new Route for adding to the Camel engine. If this route will consume EC Events, then implement the method String getSubscriberEndpoint() so that it returns an endpoint name that will be connected to the EC Event publishing.

If you are unable to configure one or more Camel Routes to integrate with the external system, you might need to implement a custom subscription and handling the integration code there. See Subscribe to Events on how to do this.

Supported External systems

For this release of Energy Components, forwarding Events out of EC and into the following systems are supported. All configuration are done in the Event Route Configuration (BF CO.1081, Configuration → Integration Services → Event Route Configuration) web page.

Forward Events using WebHooks

Forward Events to the AWS Simple Notification Service

Forward Events to Firebase Cloud Messaging


==========================================================================================
## [7/25] Forward Events using WebHooks
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/outbound/event_route_webhooks.html
==========================================================================================
Forward Events using WebHooks
Overview

Using webhooks enables EC to automatically forward events to an external system, when some key events happen in EC. E.g. when data is calculated and ready. In this case EC will be the initiator, and send an event to the external system. The external system can then avoid polling EC, and instead directly continue its business process when it receives events.

EC can forward (or bridge) events to external systems using a technic called Webhook. This enables EC to integrate with common integration middleware like Azure LogicApp, MuleSoft and many more.

Setting up forwarding of events to an external system is done using the Event Route Configuration (CO.1081) screen.

Features

Main features supported by Forwarding Events using Webhooks:

a configurable endpoint url, the Webhook, to be called by EC when the events happen.

configurable filter to control which events are forwarded.

the complete EC Event, in Json format, will be forwarded as the payload to the external system, by issuing a POST request.

supports for these authentication types:

non auth

basic auth

OIDC client Credentials

OIDC Resource Owner

redelivery policy to define detailed behavior of how to retry when a Webhook request fails.

throttling policy to ensure that a Webhook (and the external system) does not get overloaded with events in a given time period.

The Webhook feature is only about forwarding EC Events to an external system, this feature does not add support for calling arbitrary external APIs.
Configuration

To configure EC to use Webhook to forward events, open Event Route Configuration (BF CO.1081, Configuration → Integration Services → Event Route Configuration) web page.

In this example a new Webhook has been configured and the parameter WebHook.url has been given the url of the endpoint of the external system. This is the endpoint EC will forward events to, as they happen in the EC system. The event itself will be posted as the payload (body) to the external system. Also, note that in this example no authorization is enabled, because the Webhook url is an Azure shared access signature (SAS) url.

A filter can be configured to only forward events that are applicable for the external system.

Here we define a filter that only subscribes to JobCompleted events, where the JobNo == 5082.


==========================================================================================
## [8/25] Forward Events to the AWS Simple Notification Service
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/outbound/event_route_aws_sns.html
==========================================================================================
Forward Events to the AWS Simple Notification Service
Overview

The AWS SNS Route enables EC to forward selected events to the AWS Simple Notification Service.

Configuration

Setting up forwarding of events to AWS Simple Notification Service is done by configuring a new Event Route in BF CO.1081: Configuration → Integration Services → Event Route Configuration.

Select the AWS SNS Route as route type and add the necessary configuration parameters. Also configure appropriate event subscriptions in the Event Subscriptions tab for your route.

Platform specific configuration

AWS SNS can publish events with a platform specific payload. This makes it possible to have different and specific settings for any of the supported mobile receivers. See detailed documentation here:

AWS SNS platform specific payload for mobile devices

Apple mobile devices specific configuration

Google mobile devices specific configuration

AWS Device Messaging

Property	Description


"sns.default"

	

Settings and payload for default devices (like e-mail)




"sns.apns"

	

Settings and payload for Apple devices




"sns.gcm"

	

Settings and payload for Google/Android/Firebase/GCM devices




"sns.adm"

	

Settings and payload for AWS device Messaging

When using one or more of the platform specific properties

then the messageStructure=json request parameter will also be set.

use the expressing language to expand values from the actual EC Event into the configuration. See example below where ${<expression>} are used.

Example:

Property	Value


sns.default

	

"This is the message. EventType=${event.eventType}, Task name: '${event.payload['task-name']}' Task status: ${event.payload['task-status']}"




sns.apns

	

"{\"aps\":{\"alert\": \"Check out ${event.eventType}!\",\"url\":\"https://energycomponents.com\"} }"

Example, publish an event to AWS SNS
// Create an Event, fill in data
Event taskstatusEvent = new Event(EventType.TaskStatus, this);

// this will be the AWS SNS message text
taskstatusEvent.setPayload("notification-message", "This is a EC Notification message: Task '" + taskstatusEvent.getParameter("task-name", "") + "' has status [" + taskstatusEvent.getParameter("task-status", "") + "]");
// this will be the AWS SNS message subject
taskstatusEvent.setPayload("notification-subject", "EC Task/Process Notification");

// all other parameters will be available on the AWS SNS serverside as attributes and can be used in filtering.
taskstatusEvent.setPayload("task-name", "Verify incoming daily data");
taskstatusEvent.setPayload("task-id", "qwerty1234");
taskstatusEvent.s
…[truncated]


==========================================================================================
## [9/25] Forward Events to Firebase Cloud Messaging
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/outbound/event_route_firebase.html
==========================================================================================
Forward Events to Firebase Cloud Messaging
Overview

The Firebase Route enables EC to forward selected events to the Firebase Cloud Messaging service.

Configuration

Setting up forwarding of events to Firebase Cloud Messaging service is done by configuring a new Event Route in BF CO.1081: Configuration → Integration Services → Event Route Configuration.

Select the Firebase Route as route type and add the necessary configuration parameters. Also configure appropriate event subscriptions in the Event Subscriptions tab for your route.

Google reference documentation :

Firebase Cloud Messaging

Authorize send requests

The Firebase route has the following parameters :

Property	Description


service_account_json

	

The full json formatted Google Service Account json. Download this from Firebase Cloud Console and paste it into the value field.




template_default

	

A message template with expression language as described for the AWS SNS route above.

The service_account_json field will look empty after saving, but the values are encrypted backend and theres no way to recover it.


==========================================================================================
## [10/25] Event Types
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/event-types.html
==========================================================================================
Event Types
Introduction

The EventType attribute of an Event carries the semantic meaning of the event. It is a critical aspect of an Event, and therefore, it must be declared and specified in the system before it can be used. EC maintains a list of valid event types and their associated payload parameters.

The list of valid event types can be seen and configured in the EC web app, open the EC Codes screen and select the 'CTRL_EVENT_TYPE' code type.

List all defined Event Types

The EC REST API can also be used to list all event types defined in the system. Issue a GET request to endpoint https://<ec-system>/rest/v1/services/event/types to receive a list of event types.

Retrieving Event Specification

To retrieve the specification of an event type, send a GET request to the following endpoint: https://<ec-system>/rest/v1/services/event/types/{eventType}. For example, to retrieve the specification and example of the 'ExtensionRunning' event, send a GET request to the following endpoint: https://<ec-system>/rest/v1/services/event/types/ExtensionRunning. This will return a JSON example of the 'ExtensionRunning' event with all its payload parameters documented, like this:

{
    "eventType": "ExtensionRunning",
    "channel": "Channel name where event will be published. Default is ec-channel.",
    "source": "Name or Id of the component that created this event.",
    "userId": "Name or Id of the user that created this event.",
    "description": "Extension is in Running State.",
    "payload": {
        "Extension-Id": {
            "description": "Extension id",
            "displayName": "Extension id",
            "mandatory": true
        },
        "Extension-Name": {
            "description": "Extension name",
            "displayName": "Extension name",
            "mandatory": true
        },
        "Extension-State": {
            "description": "Extension state",
            "displayName": "Extension state",
            "mandatory": true
        },
        "Extension-Version": {
            "description": "Extension version",
            "displayName": "Extension version",
            "mandatory": true
        }
    },
    "context": {
        "links": {
            "events": "/rest/v1/services/event/types/ExtensionRunning/events",
            "self": "/rest/v1/services/event/types/ExtensionRunning"
        }
    }
}

For more details, please see the Rest API specification Rest Endpoints for Events or the general EC Rest API documentation.

Custom Event Types

To declare and specify a custom event type, see Event Types — Custom.


==========================================================================================
## [11/25] Event Types — Custom
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/event-types-custom.html
==========================================================================================
Event Types — Custom
Introduction

Adding custom event types, is supported in EC, and can be done in the screen EC Codes. Selecting the CTRL_EVENT_TYPE in the navigator will list all known event types in the system and allow creating new custom types.

Naming convention for EventType

It is important to introduce custom EventTypes with well-defined semantic meaning. In addition, using past tense verbs to name event types is a common convention in event-driven architectures. This naming convention helps to convey that an event has already occurred and serves as a historical record of what has happened in the system.

For example, an event that signals that a user has created a new account could be named "userAccountCreated", while an event that indicates that an order has been shipped could be named "orderShipped".

Using imperative verbs to name subscribers is also a common convention. Imperative verbs suggest that the subscriber should take some action in response to the event. For example, a subscriber to the "orderShipped" event might be named "sendShippingNotification" or "updateInventory".

Overall, the naming conventions used for event types and subscribers should be clear, concise, and consistent. They should help to convey the purpose of the event and the action that subscribers should take in response.

Event Type attributes

All event types in EC has a set of attributes that control different aspect of how the events are processed.

EventType attributes

name

	

Values

	

Description




allowExternal

	

true, false

	

Allow events of this type to be exported or imported in/out of EC.




saveHistory

	

true, false

	

Control storing of event history for this event type. See Event history for details.


==========================================================================================
## [12/25] Subscriber Execution modes
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/event-subscriber-execution.html
==========================================================================================
Subscriber Execution modes
Overview

Defining Subscribers can be done with both code (using APIs) and with pure configuration. The runtime characteristics of subscribers can be controlled by configuring subscriber execution attributes. These attributes control the runtime behavior of the subscriber, including detailed control of transactions, authentication, concurrency, redelivery, throttling and more.

[1] Java API

Configuring execution attributes when using the Java Event API are done by declaring the @Execution annotation.

Java API example
@SubscribeToEvent(
  filter = @Filter( eventTypes = "TestEvent"),
  execution = @Execution(
    tx = Tx.REQUIRED,
    scope = Scope.PROTOTYPE,
    skipConcurrentEvents = false,
    serial = @Serial(maxSize = 50),
    redelivery = @Redelivery(maximumRedeliveries = 3, delay = 5000),
    throttle = @Throttle(maximumRequestCount = 5, timePeriodSeconds = 60),
    skipExceptions = IOException.class
  )
)
public static void subscriberMethod(Event event) {
    // Subscriber business logic
}
[2] Configuration screen

Configuration of execution modes are available on some subscribers. Open the Event Route Configuration web page, select a subscriber, then open the Execution tab to configure available execution mode attributes.

Overview of Execution mode attributes

The following attributes are available for controlling the runtime execution mode of subscribers.

Tx — transaction handling

Transaction propagation can be defined on subscribers by configuring the Tx attribute.

Tx attributes

Annotation

	

Config values

	

Description




Tx.REQUIRED

	

-

	

Uses the clients transactional context, or creates a new transaction if none exist.




Tx.REQUIRED_EXT_TIMEOUT

	

-

	

Same as Tx.REQUIRED, with the EC extended transaction timeout.




Tx.REQUIRES_NEW

	

-

	

Creates a new transactional context.




Tx.REQUIRES_NEW_EXT_TIMEOUT

	

-

	

Same as Tx.REQUIRES_NEW, with the EC extended transaction timeout.




Tx.IGNORE

	

-

	

Does not set any transactional context.

Redelivery — retry policy when subscriber fails

Use redeliver attributes to configure how the subscriber should behave in case of failure. The default when no redelivery is configured, is to not retry the execution.

Redelivery attributes

Annotation

	

Config values

	

Description




maximumRedeliveries

	

execution.redelivery.maximumRedeliveries

	

Maximum number of redelivery attempts allowed. 0 is default and used to disable redelivery.




maximumDelay

	

execution.redelivery.maximumDelay

	

An upper bound in milliseconds for redelivery 
…[truncated]


==========================================================================================
## [13/25] Event history
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/event-history.html
==========================================================================================
Event history
Overview

EC has the abillity to persist the history of all events that has been processed by the event engine. The history is stored in the CTRL_EVENT_HISTORY class and is readable from both the Rest Domain API and the /rest/v1/services/event/types/{eventType}/events endpoint, see Rest Endpoints for event services.

Configuration

The decision to save an events history is based on settings read from EC customise properties, the configured EventType and the settings on the individual event on publish time.

These settings can be configured in the Maintain System Settings screen under the EC Settings customise category.

The configurable settings are

Property	Description	Default value	Key


Store history of all events.

	

Store history of all processed events in CTRL_EVENT_HISTORY class. Has performance and storage impact.

	

N

	

/com/ec/frmw/eventproxy/route/eventhistory/save




Store history of external events.

	

Store history of inbound and outbound events in CTRL_EVENT_HISTORY class.

	

Y

	

/com/ec/frmw/eventproxy/route/eventhistory/saveAllExternal




Store history of events with errors.

	

Store history of events with errors during processing in CTRL_EVENT_HISTORY class.

	

N

	

/com/ec/frmw/eventproxy/route/eventhistory/saveOnError

Advanced Performance tuning

In addition, these parameters can be configured if necessary :

Property	Description	Default value	Key


Batch size for persisting.

	

The number of events that are aggregated before persisting.

	

100

	

/com/ec/frmw/eventproxy/route/eventhistory/completionSize




Persisting frequency.

	

The idle time in seconds before events are persisted independent of batch size.

	

10

	

/com/ec/frmw/eventproxy/route/eventhistory/completionTimeout


==========================================================================================
## [14/25] Event - FAQ
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/event-faq.html
==========================================================================================
Event - FAQ

Here are some frequently asked questions, and answers, about the EC Event architecture and pub-sub system in general.

FAQ
1. When subscribing to events, is the order of the received events guarantied to be the same order as the events are published?

No. All events are published asynchronously, and there is no guarantee in which order (or when) they will be processed by the subscribers. This means that subscribers must be able to handle 'older' events and also be able to process events concurrently.

2. Are subscribers executed concurrently?

Yes. All subscribers are executed concurrently and therefor must be coded in a thread safe manner.

When the event engine is processing an event, it will check the configuration and dispatch the event to all matching subscribers. These subscribers run concurrently.

Also, a single subscriber can receive multiple events concurrently, this can happen when events are publish at a high frequency or when the subscriber is busy processing an event and another event is being dispatched to this subscriber.

All subscribers run concurrently with other subscribers.

One subscriber can processes multiple events concurrently.

3. How to make sure a subscriber only process one event at a time?

Some subscribers are not written to handle concurrent execution, or it is unnecessary to process an incoming event if the subscriber is already busy processing an earlier event. In these cases the subscriber can be configured to skip the incoming event if it is already busy executing another event. This will make sure only one event is processed at a time.

See skipConcurrent

4. How can a subscriber be throttled, so no more that N events will be processed in a given time period?

See Throttling configuration.


==========================================================================================
## [15/25] EC Integration Services (ECIS) Technical Documentation
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ecis/ecis_technical_documentation.html
==========================================================================================
EC Integration Services (ECIS) Technical Documentation
Introduction

This section is the technical documentation of the EC Integration Services (EC IS). It is supplemented by:

ECIS - Configuration Guide - describing common data capture scenarios

ECIS Agent

ECIS - Advanced File Import

ECIS - Staging Table Extension

ECIS - Source Adapter Configuration

ECIS - Example adapter configurations

ECIS - Sample Periods explained

EC Integration Services (EC IS) is the module that handles the integration of EC with external parties including:

SCADA / Tag Based Integration Service:* Tailored for integration with metering/tag-based solutions.

File Integration Service: Exchanging row-based files.

The appendices include configuration examples.

*) SCADA - Supervisory Control And Data Acquisition

Overview

The individual integration services are designed as modularized, configurable components. As an example, the SCADA / Tag-Based Integration Service is segmented into components dealing with:

Connection to the source system (adapter).

Aggregating / transforming data.

Mapping data.

Inserting data in the database.

This approach makes it easier to adapt the system to the customer’s environment.

ECIS Components
Overall Process Flow

ECIS is comprised of two main parts that are isolated from each other by a message queue:

Source - Reading data from various external data sources and writing them to the message queue.

Target - Reading data from the message queue and transform it before storing it in the EC data storage.

Source Process Flow

EC Scheduler triggers the SourceAction (parameters, configuration-id)

SourceAction reads the adapter configuration.

This determines if we are reading the tag or row data.

If reading tag data:

SourceAction reads Source Tag Configuration.

SourceAdapter reads tag data.

SourceAction adjusts time intervals.

SourceAction applies source mapping.

SoureAction creates DataTransferObjects (DTOs).

SourceAction sends DTOs to the message queue.

If reading row data:

SourceAdapter reads row data.

SourceAction creates DTOs.

SourceAction sends DTOs to the message queue.

The TagService handles tag-based data from various sources, e.g. SCADA systems, files, or databases. A tag is a data structure that contains:

A tag id (typically identifying a specific metering device).

A date/time value (timestamp).

A data value.

A quality.

The RowService reads data with arbitrary content. The content is processed on the target side with a corresponding PackageService or ECClassService before being stored in the EC Data Storage.

The Dat
…[truncated]


==========================================================================================
## [16/25] ECIS - Configuration Guide
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ecis/ecis_configuration_quide.html
==========================================================================================
ECIS - Configuration Guide
Configuration Scenarios

The section describes how to configure EC Integration Services for the most common data capture scenarios and should be read in conjunction with the EC Integration Services (ECIS) Technical Documentation which describes all features and possible options for the different EC IS components. It focuses on typical configuration scenarios and defines a step by step approach on how to capture the data required.

Before starting this document, please see EC Integration Services (ECIS) Technical Documentation and perform the necessary steps.

For all configuration involving reading/writing files, note that the system will perform a security validation to prevent file traversal attacks. Please see Post Install Configuration, subsection Validation of Directories for Read/Write in the Installation Guideline.

For configuration involving ecisconfig.xml files, these files can either be imported in the Adapter Configuration screen or entered in to the configuration form in the screen.

How to setup an OPC Classic to EC connection
This guide uses the Classic version of the OPC adapter. An alternative is the OPC UA adapter. Please read ECIS - Source Adapter Configuration for more details about the configuration.

Main objective: Extract historian data from an OPC source and store it in EC classes.

Flow objects description: The configuration consists of six steps:

Configure the connection to the source system

Configure how tags should be retrieved

Configure how tags should be mapped to EC

Schedule the transfer job

Verify results

Verify connection

Step 1 – Configure the OPC connection

XML config template:

 <config name="OPCConfig">
    <sourceadapter>
        <class>com.ec.frmw.is.engine.adapter.opc.classic.OPCAdapter</class>
        <sequential>Yes/NO</sequential>
        <parameters>
            <parameter name="AUTH_DOMAIN">MyDomain</parameter>
            <parameter name="USR">opcreader</parameter>
            <parameter name="PWD">password</parameter>
            <parameter name="OPC_HOST">127.0.0.1</parameter>
            <parameter name="PROG_ID">Some.OPC.Server.1</parameter>
            <parameter name="IID"></parameter>
        </parameters>
    </sourceadapter>
</config>

Substitute the config name (ex. OPCConfig_Norway_1). No spaces are allowed in this name. The name is unique and cannot be used for any other config name.

Set the sequential flag to 'Yes' (indicating that data from OPC will come ordered by date).

Set the domain where the OPC server is located (AUTH_DOMAIN parameter).

Set the user n
…[truncated]


==========================================================================================
## [17/25] ECIS Agent
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ecis/ecis-agent.html
==========================================================================================
ECIS Agent
Introduction

ECIS Agent is a lightweight standalone application that can be placed close to your data source to extract/read data, and then push it to EC located on or off premise. Several ECIS Agents can be installed simultaneously and independently to handle multiple data sources. E.g. one ECIS Agent might be installed close to your SCADA system and another ECIS Agent can be installed on the server to monitor a file-drop directory.

ECIS Agent is provided as a standalone Java application (jar file) that communicates with the EC application server. All configuration is done within EC. Typically only the location (URI) of the EC system is needed on the Agent side, the Agent will connect to EC and read the interface configurations from there.

ECIS Agent is available from Energy Components version 12.0.

System Requirements
Software

Java 21 must to be installed on the host machine.

Hardware

The ECIS Agent does not have any concrete hardware requirements. The host machine must account for the number of agents running simultaneously on the same machine and the amount of data they are extracting and sending to EC. Start with something small, like 1 multi-core CPU, 1 GB RAM and 1 GB disk space (in addition to what the OS and other applications on the machine require), and scale up from there if it proves insufficient.

ECIS Agent - Installation
Download ECIS Agent

First, download the ECIS Agent from the EC app server to the server (or to a server close to it) where the source data resides.

The agent can be downloaded from the "Agent Configuration" screen or by the direct link:

https://[servername:port]/DownloadService/com.ec.ecdm.co.screens.model.web.AgentJarDownload

To be able to download the agent jar, the user has to have appropriate access to the download url. /DownloadService/com.ec.ecdm.co.screens.model.web.AgentJarDownload.
Configure ECIS Agent

ECIS Agent is mostly configured in the same way as ECIS.

For Tag and Row based import there is no change in how the sources are configured. Consult the ECIS - Configuration Guide and EC Integration Services (ECIS) Technical Documentation.

For Advanced File Import the ECIS Job Action parameters for the agent have been moved to the "Agent Configuration" screen and is stored in the EC class "IMP_AGENT_CONFIG". For complete configuration of Advanced File Import, consult the document "ECIS Advanced File Import".

ECIS Agent Authentication

For EC version since 13.2.9: The ECIS Agent allows client credential authentication as preferred method. Previous user authentication is still supported.

Ref
…[truncated]


==========================================================================================
## [18/25] ECIS - Advanced File Import
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ecis/ecis_advanced_file_import.html
==========================================================================================
ECIS - Advanced File Import
Introduction

This section is the technical reference of the Advanced File Import, describing the concepts behind the design, the configuration details, and how to perform the execution of file import. The file term in this context means files of different types, like Excel, CSV, Fixed Width, XML, etc.

This section has a top-down structure. The first section covers an overview of the Advanced File Import. This is followed by technical details about how to configure the extraction and loading and how this information is organized in the database.

Overview
Summary

The advanced file import mechanism in EC is a framework that enables the users to easily set up and reconfigure import of advanced files structures. For a typical Excel format, it supports multiple sheets, crosstab, tables, and forms. In addition, the import mechanism supports similar structures for TEXT (CSV and Fixed Width) and XML.

All configuration of the import is done through screens available in EC.

The import mechanism provides file pickup from any drop folder accessible from the EC application server.

Functional Concept

The main concept for the Advanced File Import consists of four steps:

Read the source file based on a set of source mappings.

Convert the read data to the staging format and write it to the staging area.

Read staging data and convert it to the EC class format based on a set of target mappings.

Store the EC class data.

The two first steps can be categorized as extraction and the two last steps as loading of data. In order to set up such a flow, it’s necessary to configure the mappings as described below.

Mapping Configuration

The mappings between a source file and the EC database are split into source mappings and target mappings. The first category represents the extraction and the last category the loading.

Interface definition

The source mappings or extraction part belongs to an interface so that it’s possible to control the execution of each separate file or file set. The interface consists of a name and options related to transaction types and user exits.

Field Name	Description


Code

	

The interface code.




Name

	

The interface name.




Functional Area

	

The interface EC Functional Area.




Type

	

The processing type, i.e. data write behavior (INSERT / UPDATE, INSERT or UPDATE).

Insert: Will only perform the insert operation.

Insert then update: Will first perform an insert. If this fails with a unique constraint, it will try an update.

Update: Will only try an update operation.




Transaction Type

	

Whet
…[truncated]


==========================================================================================
## [19/25] ECIS - Staging Table Extension
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ecis/ecis_staging_table_extension.html
==========================================================================================
ECIS - Staging Table Extension
Introduction

This section describes the architecture and functionality of a generic staging table concept for EC Integration Services. The solution is intended for loading tag-based data where there is a generic tag set that must be seen as a unit when loading data. An example of such data is a set of generic well test tags where one tag identifies the well number, one identifies the start time, while others identify the various measurements during the test.

The challenge in such cases is that when receiving a tagged sample on one of the tags, you do not have the necessary information in order to write the data. E.g. if you receive a pressure sample, you do not know what well it belongs to or what time the well test started. All this is part of the primary key, so you cannot yet write the data.

Another example of a similar case is for loading analysis data for cargos. In this case, there may also be a generic set of tags, one tag being the cargo number or another unique identifier.

One basic assumption in the outlined solution is that all samples belonging to one data set (one well test, one cargo, etc.) will be timestamped exactly the same in the source system. The timestamp will be the way to determine which data belongs together.

This document illustrates a generic product solution for loading timestamp grouped tag-based data from generic tag sets into EC. It is intended for customer key personnel, TE support personnel, and anyone who needs to understand how this module works.

General
Abbreviations
Abbreviation	Description


EC

	

Energy Components




SCADA

	

Supervisory Control And Data Acquisition. Source system where metering data is collected.




TC

	

TagCollector

Definitions
Database job	A scheduled event in a database which runs at specified intervals. Managed by DBMS_JOB in Oracle.


PI

	

Plant Information system. Commonly used SCADA system.




ECIS

	

EC Integration Services – the EC Data Transfer Framework.




Trigger

	

A piece of code stored in the database that executes when a certain event occurs, e.g. a row insert or update.




EC tables

	

Tables within the EC main database schema.




Staging tables

	

Temporary tables in the EC database schema. These are used to hold temporary data to be loaded into the EC tables.

Background

The following section describes the data capture of well test data in an example company. Although the ECIS Staging Table Extension is generic, the company well test data is the background for implementing the solution.

Well Test Data Capture

Data Capture f
…[truncated]


==========================================================================================
## [20/25] ECIS - Source Adapter Configuration
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ecis/source-adapter-configuration.html
==========================================================================================
ECIS - Source Adapter Configuration
Common Parameters

Some parameters/ element types are valid for all tag adapters:

Parameter/Element	Value	Comments


config name

	

Unique string

	

Identifier of the configuration. It must be added as EC codes with the type DT_SOURCE_ID.




class (mandatory)

	

<path to implementation>

	

Referring to the class of the adapter.




Sequential (optional)

	

Yes | True OR No | False

	

Indicates if the data coming from the adapter can be expected to be ordered by date/time.




ShiftTimeToPeriodStart (optional) <DEPRECATED, use the attribute in TRANS_TEMPLATE instead>

	

A comma-separated list of source functions

	

For each of the functions listed the timestamp will be moved one period back. This is commonly used if the timestamp is set at the end of a period for a specific function. The parameter will indicate that it should be moved to the start of the period.




DEFAULT_RECORD_STATUS (optional)

	

P | V | A

	

The record status on the values retrieved from the adapter. Valid values are:

P (provisional)

V (verified)

A (approved)

If no value is set the status of the records originating from this adapter will be P. If the value differs from P this must also be changed in the DB; trans_template.overwrite_status must be set to the same value for all affected templates.




RetryTimeout

	

The number of seconds.

	

How many seconds the timeout for the failover mechanism of the adapters should be. Only needed if you plan on using several adapters with the same configuration name for failover.




DateValueFormat

	

A date pattern in Java SimpleDataFormat syntax.

	

The date pattern to use when parsing sample values that are dates in string format. Should be specified when your source datatype is DATE.

To enable the failover mechanism for ECIS adapters, you can create multiple configurations with the same config name. ECIS will then use the first one as the default adapter. If this adapter fails during initialize, ECIS will use the next adapter until there are no more adapters left. If the last specified adapter fails while running, ECIS will fail the schedule and the next schedule that runs will use the next adapter with the same configuration name.

If an adapter fails, ECIS will wait for a timeout. When this timeout occurs the next schedule that runs will use the first adapter once again. If this adapter fails it will proceed to the next adapter in line, etc. How long this timeout should be is specified by the adapter RetryTimeout parameter which can be set as in the example above. This parameter spe
…[truncated]


==========================================================================================
## [21/25] ECIS - Example adapter configurations
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ecis/ecis_example_adapter_configuration.html
==========================================================================================
ECIS - Example adapter configurations

Here are some example configurations. Remember that the values inside the parameters need to be changed to fit your setup.

These examples can be imported in the Adapter Configuration screen.

<configurations>
    <config name="TagFileAdapter">
        <sourceadapter>
            <class>com.ec.frmw.is.engine.adapter.file.TagFileAdapter</class>
            <sequential>Yes</sequential> <!-- alternative: No -->
            <parameters>
                <parameter name="DropFolder">C:\\temp\\dropfolder</parameter>
                <parameter name="CompletedFolder">C:\\temp\\completed</parameter>
                <parameter name="ErrorFolder">C:\\temp\\error</parameter>
                <parameter name="BadFolder">C:\\temp\\bad</parameter>
                <parameter name="FileFilter">filefilter</parameter>
                <parameter name="DateFormat">yyyy-MM-dd'T'HH:mm:ss</parameter>
                <parameter name="DateValueFormat">yyyy-MM-dd'T'HH:mm:ss</parameter>
                <parameter name="HeaderRow">N</parameter>
                <parameter name="QualityColumnIndex">-1</parameter>
                <parameter name="TagColumnIndex">4</parameter>
                <parameter name="TimeColumnIndex">0</parameter>
                <parameter name="ValueColumnIndex">2</parameter>
                <parameter name="DecimalSeparator">.</parameter>
                <parameter name="FieldSeparator">;</parameter>
                <parameter name="StartCell">A1</parameter>
                <parameter name="EndCell"></parameter>
                <parameter name="EndRow"></parameter>
            </parameters>
        </sourceadapter>
    </config>
    <config name="RowFileAdapter_to_package">
        <sourceadapter>
            <class>com.ec.frmw.is.engine.adapter.file.RowFileAdapter</class>
            <parameters>
                <parameter name="DropFolder">C:\\temp\\dropfolder</parameter>
                <parameter name="CompletedFolder">C:\\temp\\completed</parameter>
                <parameter name="ErrorFolder">C:\\temp\\error</parameter>
                <parameter name="BadFolder">C:\\temp\\bad</parameter>
                <parameter name="FileFilter">filefilter</parameter>
                <parameter name="DateFormat">yyyy-MM-dd'T'HH:mm:ss</parameter>
                <parameter name="HeaderRow">N</parameter>
                <parameter name="DecimalSeparator">.</parameter>
                <parameter name="FieldSeparator">;</parameter>
                <parameter name="StartCell">A1</parameter>
                <parameter name="EndCell">
…[truncated]


==========================================================================================
## [22/25] ECIS - Sample Periods explained
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ecis/ecis_sample_period_explained.html
==========================================================================================
ECIS - Sample Periods explained

This section contains a number of cases with different target interval and time zones to show how ECIS will create the sample periods during aggregation.

Samples: Interval 30 minutes (1800 secs)
Sample: Interval 1 hour (3600 secs)
Samples: Interval 2 hours (7200 secs)
Samples: Interval 1 day (86400 secs)
Samples: Interval 30 minutes, Central Time
Samples: Interval 1 hour, Central Time

image::frmw/ecis/sample-period/sample_period_1hr_CET.png

Samples: Interval 2 hours, Central Time
Samples: Interval 1 day, Central Time
Samples: Interval 30 minutes, Brasília Time
Samples: Interval 1 hour, Brasília Time
Samples: Interval 2 hours, Brasília Time
Samples: Interval 1 day, Brasília Time


==========================================================================================
## [23/25] Remote endpoint configuration
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ecis/remote_endpoint_configuration.html
==========================================================================================
Remote endpoint configuration

EC provides a generic way of defining and configuring remote endpoints. These endpoints are used when EC is "calling out" to a remote third party system. These endpoints typically require some protocol specifier, some urls and some kind of confidential credentials.

The storage for the entered values for the parameters in this screen is NOT the ec database but a separate Secret Storage that is dependent on your runtime environment, see Storage backends. EC will select a secret storage provider automatically from the runtime environment and the selected provider will be displayed in the Remote Endpoint Configuration business function.

Adding a new remote endpoint for interfacing with 3rd party system

Open Remote Endpoint Configuration business function, click insert Remote Endpoint Configuration, fill in a Code, this will be used as the key for the backing secret storage, an optional Name and the appropriate type of the remote system. If this is a WebHook it would use the HTTP rest type, if its an ECIS endpoint, select the appropriate ECIS type. If you are planning to write your own java implementation to connect to a remote system, you should add your endpoint type first as described in Adding new endpoint types.

Save appropriately and click the VALIDATE ENDPOINT button to call the verify connection method and verify the connection details.

The newly configured endpoint will now be available around in EC where details and credentials for remote endpoints are required, typically in Webhooks, ECIS or mail sending configurations.

Java API and usage

When your business action or custom java code requires some configuration details or credentials to perform a request to a third party, the details can be configured by end-user in 'Remote Endpoint Configuration' business function as described above.

In your Java code you can then enumerate the client configurations of your type of interest or get a configuration by name. This name can be read from f.eks a customize property, user selected or an environment variable.

Connecting to a preconfigured HTTP rest endpoint
...
//1. Retrieve the client configuration
ClientConfiguration clientConfiguration = ClientConfigurationMgr.getService().getConfiguration("my-preconfigured-endpoint");

//2. Optional : Verify the configuration
ValidationResult vr = ClientFactory.validateConfiguration(clientConfiguration);
if (vr.getStatus() != ValidationResult.Status.OK && vr.getStatus() != ValidationResult.Status.WARNING) {
    final String errTxt = vr.getMessage() + " : " + vr.getDetailedMessage
…[truncated]


==========================================================================================
## [24/25] EC Event API
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/event/event-api.html#_event_api_java
==========================================================================================
EC Event API
Overview

EC Event API currently consist of three part:

Event API — Java

Event API — database

Event API — REST

The API provides a generic publish-subscribe service where events can be published, and subscriptions to application logic can be registered. The implementation of the API does not handle the routing of events itself, it will just act as proxy and hand the work over to the real pub-sub engine. The engine we use behind our API is Apache Camel. In addition, we use Apache ActiveMQ to support durable (persisted) events.

Event API — Java

The API is simple, it supports publishing events and subscribing to them via these two APIs:

EventMgr.getService().publish(String channel, Event event);
EventMgr.getService().subscribe(String beanExpression, Predicate<Event> filter, EventExecution execution);
You can also subscribe to Events by using the annotation @SubscribeToEvent.
Examples
1 Publish event
Event event1 = new Event(EventType.TestEvent, this);
EventMgr.getService().publish(event1);

This code example will create an Event with EventType as TestEvent, and then publish the event (on the default channel).

2 Publish event with payload
Event event2 = new Event(EventType.TestEvent, this);
event2.setPayload("param01", new BigDecimal("3.14"));
event2.setPayload("calculationMethod", "advanced");

EventMgr.getService().publish("test-channel", event2);

Here we create an Event with EventType as TestEvent, set two parameters and then publish this event to the 'test-channel'.

3 Publish event and wait for it to finish
// Create an Event, fill in data
Event testEvent = new Event(EventType.TaskStatus, this);
testEvent.setPayload("task-status", "PROVISIONAL");

// Publish the event, and wait for all subscribers to finish
EventMgr.getService().publish(Event.CHANNEL_MOBILE_NOTIFICATION, testEvent).get();

// If any of the subscribes add data to the event, we can read it like this (but only if we have waited for completions):
String myResult = testEvent.getPayload("theResult", "magic");

// The event contains a context map with parameters from the execution.
// We can get a list of all subscriptions that were executed:
log.info("These subscriptions where sucessfully run: " + testEvent.getContext(CONTEXT_SUBSCRIBED_BY, null));

The publish(event) method returns a standard Java Future<Event> object. To wait for completions call the Future.get() method. Note that there is no way to tell up front how long time this will take, especially since more subscriptions can be added later. To avoid waiting 'forever', you can set a timeout, like this: publish("so
…[truncated]


==========================================================================================
## [25/25] Remote endpoint configuration
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/ecis/remote_endpoint_configuration.html#_java_api_and_usage
==========================================================================================
Remote endpoint configuration

EC provides a generic way of defining and configuring remote endpoints. These endpoints are used when EC is "calling out" to a remote third party system. These endpoints typically require some protocol specifier, some urls and some kind of confidential credentials.

The storage for the entered values for the parameters in this screen is NOT the ec database but a separate Secret Storage that is dependent on your runtime environment, see Storage backends. EC will select a secret storage provider automatically from the runtime environment and the selected provider will be displayed in the Remote Endpoint Configuration business function.

Adding a new remote endpoint for interfacing with 3rd party system

Open Remote Endpoint Configuration business function, click insert Remote Endpoint Configuration, fill in a Code, this will be used as the key for the backing secret storage, an optional Name and the appropriate type of the remote system. If this is a WebHook it would use the HTTP rest type, if its an ECIS endpoint, select the appropriate ECIS type. If you are planning to write your own java implementation to connect to a remote system, you should add your endpoint type first as described in Adding new endpoint types.

Save appropriately and click the VALIDATE ENDPOINT button to call the verify connection method and verify the connection details.

The newly configured endpoint will now be available around in EC where details and credentials for remote endpoints are required, typically in Webhooks, ECIS or mail sending configurations.

Java API and usage

When your business action or custom java code requires some configuration details or credentials to perform a request to a third party, the details can be configured by end-user in 'Remote Endpoint Configuration' business function as described above.

In your Java code you can then enumerate the client configurations of your type of interest or get a configuration by name. This name can be read from f.eks a customize property, user selected or an environment variable.

Connecting to a preconfigured HTTP rest endpoint
...
//1. Retrieve the client configuration
ClientConfiguration clientConfiguration = ClientConfigurationMgr.getService().getConfiguration("my-preconfigured-endpoint");

//2. Optional : Verify the configuration
ValidationResult vr = ClientFactory.validateConfiguration(clientConfiguration);
if (vr.getStatus() != ValidationResult.Status.OK && vr.getStatus() != ValidationResult.Status.WARNING) {
    final String errTxt = vr.getMessage() + " : " + vr.getDetailedMessage
…[truncated]