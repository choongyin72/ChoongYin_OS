# Raw content — DOC-08
Modules: ['frmw/bpm']
Pages: 24



==========================================================================================
## [1/24] Architecture
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/bpm-architecture.html
==========================================================================================
Architecture
Introduction

In this section, we describe ECBPM architecture. Architecture might change between releases. Please refer to documentation from previous releases for earlier architecture.

Systems

ECBPM consists of two systems: Energy Components and BPM Console. Domains that are strongly associated with EC, such as Process Template, Process Action, Process Notification, Viewer Tag, EC scheduler and presentation related domains, are deployed within Energy Components together with the EC application. Domains that are associated with the tailored jBPM engine, such as Process, Process API and Task, are deployed standalone within the BPM Console (on a separate server group).

Figure 1. Architecture of ECBPM
Energy Components

Energy Components is the main entrance for end-users to execute and manage process instances. All BPM functionality should in EC be accessed either via the UI or the API, except for process authoring and process source code management.

Energy Components also participate in process execution when it comes to business action invocation. See section Process Action Invocations for more information.

Job Executor

EC Job Executor is used for process execution. The jbpmengine user is the user executing the processes.

When eDAC is used, the jbpmengine user must be assigned roles with access to the data that the BPM processes are using.

To run Record Status Processes, the jbpmengine user must be assigned the roles that can run the status processes.

Refer to How to assign roles to jbpmengine user

Built-in Schedules

The following schedules are installed to support ECBPM. Some of them may need to be configured and enabled before the functionality can be used.

Schedule	Description	Dependent Function


BpmSchedulerEnv

	

This schedule is referenced by the Job Executor when executing the process execution, however, it is only the log level configuration is been used, hence it is not need to enable. This schedule should only be used by BPM internally.

	

Log level configuration of process execution log.




BpmEventInboundWatcher

	

Responsible for checking EC side BPM inbound events. This schedule is not required to be enabled as long as the EC Dataset tracing feature is not used in any process.

	

EC Dataset tracing for process instances.




BpmProcessInstanceCleanUp

	

This schedule supports automatic process instance cleanup functionality. It can be used for deleting process instances of a certain process, or all the process instances. Note that the deletion is not recoverable.

	

Automatic (scheduled) process instance cle
…[truncated]


==========================================================================================
## [2/24] Project Management
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/bpm-project-management.html
==========================================================================================
Project Management
Background

In EC 11, we used KIE Workbench for process source management. Users needed to create a repository and project to host their BPM process definitions, and then build and deploy the projects to the engine. This is quite heavy and the usability is poor. From EC 12, we have removed KIE workbench and introduced Project Management.

Project Management is designed for BPM administrators (users with role JBPM.ADMIN) to create BPM projects, upload project source files and deploy or undeploy BPM projects to the engine. It also provides an overview of the processes associated with the deployed project.

Project

Similar to the project concept within KIE Workbench, projects are the direct containers of process files. In other words, process files are not allowed to be placed outside a project.

A project is the smallest unit for process compilation and deployment. To deploy a process, it must be compiled and deployed together with the whole project.

In ECBPM, projects use the Maven structure. Documentation on project and process authoring can be found in BPM Process Authoring and Project Deployment in EC SDK (energycomponents-sdk/examples/bpm/030-bpm-process-authoring-and-deployment).

A new project contains the following information:

Attribute	Description


Name

	

The name of the project




Group ID

	

The group ID of the new project. This attribute is kept in order to sync with the project concept in jBPM engine and also for upgrade compatibility. The group ID is required for Maven projects, which is to distinguish projects with the same name created by different parties. This is often named com.organization_name.project_name or com.organization_name (no space or special characters are allowed).




Artifact ID

	

The artifact name of this project after it is compiled. This attribute is kept in order to sync with the project concept in the jBPM engine and also for upgrade compatibility. An artifact is a result of a compilation of a project, and usually, a project has one artifact and the name is usually the same as the project name (no space or special characters are allowed).




Version

	

The version of the artifact. When a major change is done, it is usually required to change the version number of the project to reflect it (no space or special characters are allowed). Note that ECBPM allows multiple versions to be deployed at the same time, and when a new version is deployed, a new Process Template should be created for that.




Comment

	

Comment or description of the project.

Once the project is deployed to the engi
…[truncated]


==========================================================================================
## [3/24] Process Template and Execution
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/bpm-process-template-and-execution.html
==========================================================================================
Process Template and Execution
Process Templates

A Process Template is an EC alias of a deployed process in the process engine. Multiple Process Templates can point to the same process.

Process Templates are the only way that EC can start a process instance. Therefore, to be able to execute a deployed process, it has to be registered in EC as a Process Template.

Process Templates by nature are also registered business actions. Created Process Templates can be found in the Business Action drop down in the Schedules screen. They can be scheduled using the EC scheduler to be executed periodically.

Creating Process Templates

To create Process Templates, go to the screen Process Automation → Process Template.

Figure 1. Process Template screen

Click the Insert button  and select Process Template for a new record. A new row should appear in the list. Fill in the fields as described below:

Property Name	Description


Process Template

	

The display name of the process template.




Deployment Id

	

The id of the deployed artifact that contains the process.




Process Id

	

The id of the process. This drop-down lists all deployed processes from the selected deployment (as in Deployment Id).




Functional Area

	

The functional area this process template belongs to. This can be used to restrict user access to a group of process templates.

Parameters

To input values to a process instance, corresponding process variables need to be defined as Process Template Parameters. When executing a Process Template, the user will have a chance to provide values to Process Template Parameters. The parameter values are then sent to the new process instance variable with the same name (case-sensitive).

Note that it is not allowed to add undefined process variables to the Parameters list, as it may cause process instances to fail during execution.

Click the Insert button  and select "Parameters" for a new record. A new row should appear in the parameter list. Fill in the fields as described below:

Property Name	Description


Name

	

Name of the process template parameter. This has to be the same (case-sensitive) as defined in the process.




Type

	

The data type of the parameter.




Sub Type

	

Sub data type of the parameter.




Mandatory

	

Indicates whether the parameter is mandatory or not.




Description

	

Description of the parameter.

Static Parameters

Static Parameters are like ordinary parameters, with the exception that their values are provided on the Process Template and can not be changed for each execution.

Note that it is not allowed t
…[truncated]


==========================================================================================
## [4/24] Process Instance Management
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/bpm-process-instance-management.html
==========================================================================================
Process Instance Management
Managing Process Instances
Viewing Process Instances

Process instances can be managed via EC screen Process Automation → Process Overview.

The navigator provides common filters for process instances, as described below:

Field Name	Description


From date

	

Start of process instance daytime range (including the date itself)




To date

	

End of process instance daytime range (excluding the date itself)




Date Param

	

The process instance daytime parameter/variable. This variable indicates where to pull process instance daytime from. If left blank, the process instance start time will be used.




Functional Area

	

The functional area of the process templates where the process instances were created from.




Process Template

	

The process template from which process instances were created. If left blank, all process instances that fall into the selected Functional Area will be queried.

Click the Go button. The screen will load with queried process instances.

Figure 1. Process Overview screen

Refer to the section "Viewing Process Instances" for how to query process instances.

Configuring Process Instance Table Columns

By default, ECBPM lists Id, Process Template, State, Started by, Start and End time in the instance table. The table columns can be customized via the Process Overview Configuration screen.

Process Instance Diagram

The process instance diagram shows the most recent state of the selected instance. Colors and tags are used to indicate node and process instance status.

Zooming in and out

The diagram can be zoomed in and out by rolling the mouse wheel up and down, or by using the zoom in and out buttons on the bottom of the diagram.

Panning the diagram

The diagram can be moved by mouse dragging (moving the mouse while holding the left mouse button).

Node Instance Color

Node instances, by their status during diagram generation, are rendered with different colors. Node status colors are stored as attributes on viewer tags, which can be customized via the Viewer Tag screen.

The following table lists all possible statuses and examples using the default color scheme:

Example	Node Status	Description	Viewer Tag


	

Active

	

Active node instances are nodes currently being executed during diagram generation. Active node instances are colored with a green background by default.

	

ecbpm__node_active




	

Pending

	

Pending node instances are nodes that have not been executed in the process instance. Pending node instances are colored with a yellow background by default.

	

ecbpm__node_pendin
…[truncated]


==========================================================================================
## [5/24] Process Action Invocations
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/bpm-process-action-invocations.html
==========================================================================================
Process Action Invocations
Introduction

Process actions are actions being carried out by EC and triggered on demand from the process engine.

A process action can be configured to have one or several action handlers. An action handler can be a business action or a generic action handler. If a process action has more than one action handler, users need to define the execution order of the action handlers.

Each action handler is configured independently. The required parameters for action handlers can be retrieved from the process execution parameters, the output of preceding action handlers, or static values. Action handlers defined for a process action is invoked in a given order. Parameters being provided by a process instance are input to the first action handler, whose output serves as input to the next action handler. Action handlers are chained to each other in this manner.

Although it is possible to chain multiple business actions together in a process action, it is recommended to avoid chaining together business actions with different business 'goals'.

The purpose of using Process Action instead of Business Action is to achieve the following:

Reuse of existing Business Actions.

Transform the input or output of business action.

Wrapping a business action with "pre" and "post" actions.

Provide possible UI actions for further processing the action execution results with Process Operations.

Provide the possibility to show process action specific data in the Process Overview screen with Process Attributes.

Defining Process Actions

In order to use process actions in a process, they need to be defined in the EC Process Action Screen. The screen is located at Process Automation → Process Action.

Figure 1. Process Action screen

The screen contains three parts, as described below:

Component	Description


Action

	

The process action is identified by the Action Name column, thus the action name needs to be unique.




Handlers

	

Users need to define which action handlers to perform and the execution order of the corresponding process action invocation. An action handler can be a business action or a generic process action handler.




Handler Parameter Overwrite

	

This section is optional. If the parameter of the action handler is given in the Handler Parameter Overwrite section, it would overwrite the default parameter provided by ECBPM. Default parameter values are provided in an output-as-input manner.

The mapping types of the parameter are categorized into four types:

Default (no mapping): The action handler parameter is given by the
…[truncated]


==========================================================================================
## [6/24] User Tasks and Task Management
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/bpm-user-tasks-and-task-management.html
==========================================================================================
User Tasks and Task Management
Introduction

It is usually the case that part of an automated process requires user interaction. In BPMN, such work is also modeled as an activity, called the User Task. The workflow for User Tasks is the same as Service Tasks. The process engine generates user tasks, assigns them to groups or users according to the process definition, and then progress the process instance once the task is done. Additionally, ECBPM supports creating ad-hoc tasks without a process. These ad-hoc tasks contain basic information about the task and it has the same workflow as the user tasks generated from the process.

ECBPM supports user tasks supposed to be taken by EC users. Active and completed tasks can be viewed and operated through the EC To-do List screen. ECBPM also supports displaying formatted task information (input variables) with EC Data and UI integration. This section describes how the User Tasks can be used in ECBPM.

Figure 1. Todo List screen
Use In Process
The activity

BPMN uses the notation below for User Tasks:

Figure 2. User task node

This task can be found under the Tasks category in the Object Library.

Task Subject

Task subject is the short description of a task, and it will be shown to the task taker in the To-do List screen. Since jBPM doesn’t support value injection (the #\{} format) on the Name property, ECBPM introduces its own task subject variable, named "ec.extension.task.subject". If not defined, the Comment property is displayed instead. See the description of the variable below.

Variable	Type	Data Type	Description


ec.extension.task.subject

	

Input

	

String

	

Task subject. If not given, Comment property on User Task activity is used.

Task Description

ECBPM reads the Description property as a task description. It has a limit of a maximum of 2000 characters.

Task Assignment

Task assignment is done during process design time. A task can be preassigned to a set of users (called actors in jBPM) or groups. Preassigned tasks will show up in the target user’s To-do list.

The following properties indicate who a task is preassigned to:

Parameter	Data Type	Description	Example


Actors

	

List

	

List of preassigned users for a task. When the task is triggered, only the selected users can see the task. EC login id should be used.

	

sysadmin




Groups

	

List

	

List of preassigned user roles for a task. When the task is triggered, only users from selected user roles can see the task. EC user role id should be used.

	

SYST.ADM

Task Attributes

Task attributes serve as additional information f
…[truncated]


==========================================================================================
## [7/24] EC Inbound Events (Deprecated)
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_events/deprecated-bpm-ec-inbound-events.html
==========================================================================================
EC Inbound Events (Deprecated)
This has been deprecated, please refer to Process Inbound Events for notifying BPM process with events.
Introduction

A frequent requirement is that the user wants to notify the BPM process about updates in process dependent data. One scenario would be when calculation data is updated and the user wants to notify all the running process instances which are dependent on this data to terminate and rerun the calculation with the updated data. Or when data generated by a process instance is approved by an end user, and we need to notify this specific process instance about this change. To achieve this, ECBPM introduces a concept named EC Inbound Events.

ECBPM supports 5 kinds of EC inbound events:

Event Type	Usage Case	Name	Usage in the BPMN process


EcGenericEvent

	

This event is for use cases that need to broadcast an event to all active process instances.

	

"ecbpm_ec_" + user defined event name

	

Process instances which are interested in this event can catch this event using  (signal event node) with corresponding event name,




DatasetUpdated

	

This is typically used when an attribute of a data set is updated.

	

: "ecbpm_dataset_updated"

: "ecbpm_dataset_updated" + "__" + process variable referencing the data set,

e.g. "ecbpm_dataset_updated__alloc_dataset".

	

The BPMN process can catch this event using  (signal event node) or  (message event node).




DatasetDeleted

	

This is typically used when a data set is deleted.

	

: "ecbpm_dataset_deleted"

: "ecbpm_dataset_deleted" + "__" + process variable referencing the data set,

e.g. "ecbpm_dataset_deleted__alloc_dataset".

	

The BPMN process can catch this event using  (signal event node) or  (message event node).




DatasetStateUpdated

	

This is typically used when the state of a data set is updated.

	

: "ecbpm_dataset_state_updated"

: "ecbpm_dataset_state_updated" + "__" + process variable referencing the data set,

e.g. "ecbpm_dataset_state_updated__alloc_dataset".

	

The BPMN process can catch this event using  (signal event node) or  (message event node).




DatasetSourceUpdated

	

This is typically used when the source of a data set is updated.

	

: "ecbpm_dataset_source_updated"

: "ecbpm_dataset_source_updated" + "__" + process variable referencing the data set,

e.g. "ecbpm_dataset_source_updated__alloc_dataset".

	

The BPMN process can catch this event using  (signal event node) or  (message event node).

In order to enable ECBPM to fetch the events and notify the process instances, the events above need to be added to the event que
…[truncated]


==========================================================================================
## [8/24] Process Inbound Events
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_events/bpm-process-inbound-events.html
==========================================================================================
Process Inbound Events
Introduction

Process inbound events in this context means events being forwarded/bridged to BPM process. These events are captured by the "Catching events" element within the process, influencing the flow of the process. The “Catching Events” element in the BPM process acts as a listener for these inbound events. When an event is caught, it can trigger specific paths in the process flow, cancel tasks or sub processes, or even start new process instances, depending on the process design.

Usage in BPMN process
Event definition in process properties

ECBPM currently supports two types of events as per the BPMN specification:

Signal events: These events reference a named signal and have a global scope (broadcast semantics), they are delivered to all active handlers.

Message events: These events reference a named message, which has a name and a payload. Unlike a signal, a message event is always directed at a single recipient.

In ECBPM, as well as in JBPM, the API implementations are weakened, client can signal a specific process instance to receive the signal event as well as message multiple process instances to receive a message. However, for readability, it is recommended to follow the specification.

Define your signals or messages under the "Definitions" section in the Process Properties panel. For a message event which reference a dataset, the message definition should be event name + "__" + the process variable referencing the data set.

Start Event

Use start event node to trigger a process when the event is caught.

Intermediate Catch Events

Use intermediate catch event to catch event during the process and continue with flow.

Signal:

Message:

Boundary Events

Interrupt: Use boundary event attached to a user task or sub process to cancel the task or sub process currently processed. See more details in EC-SDK.

Non-interrupt: Use boundary non-interrupt event attached to a user task or sub process to proceed with another path without interrupting the current task or sub-process. See more details in EC-SDK.

Issuing Process Inbound Events

There are two primary ways to issue process inbound events.

Publish "BpmProcessInboundEvent" event

EC events with event type "BpmProcessInboundEvent" will be automatically forwarded to BPM process. This is a straightforward way to inform BPM process about an event occurrence. Here are details of "BpmProcessOutboundEvent" event. Please note that both the "processEventName" and "processEventType" need to match the event definition in the process to be correctly processed.

{
  "eventTy
…[truncated]


==========================================================================================
## [9/24] Process Outbound Events
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_events/bpm-process-outbound-events.html
==========================================================================================
Process Outbound Events
Introduction

In BPMN specification, "Throwing events" are events that are triggered during the process or at the end of process. Process outbound events in this context refer to events that are thrown by BPMN process and are then forwarded to EC. User can then create their subscribers to react to these process outbound events and perform asynchronous business logics, such as sending out notification. These outbound events provide a way to extend the functionality of your BPM processes, allowing you to trigger additional actions or workflows based on the state of your process.

Usage in BPMN process
Event definition in process properties

Currently, ECBPM only support "Signal event" element, define your signals under the "Definitions" section in the Process Properties panel. For outbound events, the event name needs to start with "ecbpm_ec_", indicating the event will be forwarded to EC for external consumption. Events that do not start with "ecbpm_ec_" will only be available internally within the process context.

Intermediate Throw Events

Use intermediate throw event to trigger event during the process and continue with flow.

End Event

Use end event to trigger event at the end of the process.

Process outbound event type and payload

The process outbound events forwarded to EC will have "BpmProcessOutboundEvent" event type with following details.

{
  "eventType" : "BpmProcessOutboundEvent",
  "channel" : "Channel name where event will be published. Default is ec-channel.",
  "source" : "Name or Id of the component that created this event.",
  "userId" : "Name or Id of the user that created this event.",
  "description" : "BPM Process Outbound Event",
  "payload" : {
    "processEventData" : {
      "description" : "process event data",
      "displayName" : "processEventData",
      "mandatory" : false
    },
    "processEventDate" : {
      "description" : "process event published date",
      "displayName" : "processEventDate",
      "mandatory" : true
    },
    "processEventName" : {
      "description" : "process event name",
      "displayName" : "processEventName",
      "mandatory" : true
    },
    "processEventType" : {
      "description" : "process event type",
      "displayName" : "processEventType",
      "mandatory" : true
    },
    "processInstanceRefJson" : {
      "description" : "Process instance identifier json which publishes the signal",
      "displayName" : "processInstanceRefJson",
      "mandatory" : false
    }
  },
  "context" : {
    "links" : {
      "events" : "/rest/v1/services/event/types/B
…[truncated]


==========================================================================================
## [10/24] API
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/bpm-api.html
==========================================================================================
API

From EC-11.2 ECBPM opens a set of APIs for the project to better customize their processes. It is strongly recommended to follow the How to’s documentation to utilize these APIs.

INodeInstance

applyTag(String tag): This API enables applying a specific viewer tag on the node instance. The viewer tag needs to be defined in the Viewer Tag screen.

removeTag(): This API is used for removing viewer tags from the node instance.

IProcessInstance

applyTag(String tag): This API is used for applying a viewer tag on the process instance. The viewer tag needs to be defined in the Viewer Tag screen.

removeTag(): This API is used for removing viewer tags from the process instance if there are any.

References
Please refer to the example processes: "lock_process_instance.bpmn" and "unlock_process_instance.bpmn" .

IVariableInstance

markAsDataHolder(): This API is used for marking the variable as process data holder so that it will display as a data set holder variable marked with  in the Process Overview screen.

unMarkAsDataHolder(): This API is used for removing the data holder mark on the variable.

withLabel(String label): This API enables applying a label on a variable. When applied, instead of the variable name, this label will be displayed in the Variables tab in the Process Overview screen.

withDescription(String description): This API enables applying a description on a variable. When defined, this description will be shown as a tooltip when pointing to the variable.

References

How-to Show variables in the Variables tab

How-to Show generated calculation log and report as data holder in Variables tab

EC’s Business Action Interface (BusinessAction)
All process action handlers defined by third parties should implement this interface.

Process Inbound and Outbound Events
BPM process can interact with EC using events. Please refer to Process Inbound Events and Process Outbound Events.

The list above shows the only supported APIs for project usage. Other undocumented APIs are still in the implementation phase and should not be used. It is suggested that all third-party code should be implemented either as Script Tasks or as Business Actions.


==========================================================================================
## [11/24] Standard Processes
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/bpm-standard-processes.html
==========================================================================================
Standard Processes

EC BPM comes with a few standard processes. This document describes these processes and how to configure them.

Control Point process

The BPM control point process detects and generates human tasks from control point tasks created by the control point validation system.

The process listens for CP_ERROR and CP_WARNING control point tasks. When a task arrives, a human task is generated and made available in the Todo List and Task Management screens. The task can be claimed, started and completed like any other human BPM task. Once completed, the process will close the corresponding control point task.

Configuration

Follow these steps to configure the Control Point process.

Enable the BpmEventInboundWatcher schedule and schedule it to run at regular intervals, for example, every minute.

Configure the BpmSchedulerEnv schedule and schedule it to run once. It is not necessary to enable it, it is only used as a configuration holder.

Create a BPM project containing the standard processes in the Project Management screen. The standard processes zip file is available in Energy Components artifact repository (hub.energycomponents.com).

Create a Process Template for the process. The process id is control_point_task_execution.

Add a mandatory parameter called roles to the process template with Type=Basic Type and Sub Type=String.

Go to the Process Execution screen. Select the process, specify the roles of the users that are allowed to handle control point tasks as a comma-separated string of EC user role ids, and start the process.

The process will now generate human tasks on the fly whenever a new control point validation task arrives. The tasks can be handled in the Todo List and Task Management screens.

It is not recommended to use the old Task List screen for control point task handling when this process is active.

Four Eyes Approval process

See Four Eyes Approval for information about this process and how to configure it.


==========================================================================================
## [12/24] How-to Configure default process instance list columns
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_overview/bpm_how_to_config_process_list_columns.html
==========================================================================================
How-to Configure default process instance list columns
Introduction

Columns in the Process Instance List tab in the Process Overview screen can be customized. This document guides you on how to modify the default columns.

Expected Result

Have the process instance list show the following columns: Process Template, Id, State, Creator, Deployment Id, and Start Time.

Guide
S1. Find the configuration screen

Go to screen Process Overview Configuration.

Open tab "Process Instance List" - "Default Properties".

S2. Modify default properties

The "Default Properties" tab lists all columns that are displayed for all processes. Some additional columns can be displayed when querying a specific Process Template. Those are defined in the "Template Properties" tab.

Modify the tab data with the following:

Display Order	Name	Label	Property Value


1

	

process_instance_id

	

Id

	

Process instance id




2

	

state

	

State

	

Process instance state




3

	

creator

	

Creator

	

Process instance creator




4

	

deployment_id

	

Deployment

	

Process deployment id




5

	

start_time

	

Start

	

Process instance start time

S3. See the update

Go to screen Process Overview, update the navigator, and click Go.

See that the columns are displayed as configured:


==========================================================================================
## [13/24] How-to Configure process instance list columns for a specific process
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_overview/bpm_how_to_config_process_list_columns_specific_process.html
==========================================================================================
How-to Configure process instance list columns for a specific process
Introduction

The Process Instance List tab in the Process Overview screen supports per-process column configuration. Columns added as process specific are shown after the default columns when a Process Template is specified in the navigator.

This document guides you on how to add process specific columns to the screen.

Expected Result

In addition to default columns, show the process variable "daytime" and "log_level" in the process instance list for process "advanced_calc_sample".

Guide
S1. Find the configuration screen

Go to screen Process Overview Configuration.

Open tab "Process Instance List" - "Template Properties".

Choose a proper Functional Area, and click the Go button.

Select the process template "advanced_calc_sample".

The default properties are already listed on the screen. Note that it is not allowed to modify default properties in this tab. To do modifications, use the "Default Properties" tab.

S2. Add process specific properties

Add the following properties to the list:

Display Order	Name	Label	Property Value	Variable


1

	

daytime

	

Daytime

	

Process instance variable value

	

daytime




2

	

log_level

	

Log Level

	

Process instance variable value

	

log_level

S3. Create a process instance

Start a new process instance for process "advanced_calc_sample", with parameters:

Name	Value


daytime

	

2015-05-02




start_date

	

2015-05-01




end_date

	

2015-05-02




log_level

	

Full




report_definition_code

	

EC_USER_ACCESS_BY_USER




skip_calc

	

[ ]

S4. See the update

Go to screen Process Overview and update the navigator. Choose process "advanced_calc_sample" in the "Process Template" field, and click Go.

See that the columns are displayed as configured.


==========================================================================================
## [14/24] How-to Display a button when a Process Action node is selected
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_overview/bpm_how_to_display_button_process_action.html
==========================================================================================
How-to Display a button when a Process Action node is selected
Introduction

This example shows how to display a customized button in the Process Overview screen when a certain Process Action node is selected in the diagram. We use the calculation process action as an example. The expected result is to show a button that reads the result calculation log URL and displays the URL in a modal (popup) window.

Expected Result

When Process Action node instance "Run Sale Calculation" is selected, the right panel should have two buttons, "Calculation Log" and "My Button".

When clicking on the button, it should show a modal window containing the calculation log:

Guide
S1. Prepare the process

Make sure the sampling process "advanced_calc_sample" is correctly configured. If not, see the technical documentation for parameters.

S2. Config the Process Action

Go to Process Action, find the "CalculationAction", open the Operations tab.

Add a new operation called "My Button" with values:

Name	Value	Description


Order

	

2

	

The display order of the button.




Name

	

My Button

	

The display text of the button. Note that EC will capitalize on the text when displaying it on the screen.




Type

	

EC URL

	

The type of operation. "EC URL" means the button brings up a modal EC screen.




Key

	

#\{process_action_result.calc_dataset_ref.source}

	

The URL of the screen to display. Here you can use an ECBPM Value Expression. For more information, see the technical documentation section Process Action. In this example, the URL is stored in the action result parameter "calc_dataset_ref", field "source".




Description

	

My new button

	

The description of the button. This is rendered as a button tooltip.

S3. Create a process instance

Start a new process instance for process "advanced_calc_sample", with parameters:

Name	Value


daytime

	

2015-05-02




start_date

	

2015-05-01




end_date

	

2015-05-02




log_level

	

Full




report_definition_code

	

EC_USER_ACCESS_BY_USER




skip_calc

	

[ ]

S4. Test the button

Go to the Process Overview screen, find the newly created process instance.

Wait until the process instance reaches the node "Allocation status accepted".

Click on node "Run calculation", you should see the new button "My Button" displayed in the right panel.


==========================================================================================
## [15/24] How-to Show process action specific data from a query file in External Data view
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_overview/bpm_how_to_show_process_action_data_query_file.html
==========================================================================================
How-to Show process action specific data from a query file in External Data view
Introduction

The Process Overview screen has a Data View panel, which is for displaying large amounts of data related to the selected node instance/process instance. The External Data section is mainly for projects who need to present data that is not owned by ECBPM, for example, data from another EC module.

By default, the External Data section is left blank. This document guides you to configure this section to show data from a query file whose path and parameters are attached to a process action.

The External Data section only works for Process Action node instances.
Expected Result

The External Data section shows all business actions registered in EC, using a query file and layout specified in a Process Action attribute.

Guide
S1. Add Process Action attributes

As some of the configurations are going to reference process action attributes, we add these attributes first.

Go to screen Process Action.

Open tab Attributes.

Select Process Action "CalculationAction".

Add the following attributes:

Name	Value	Description


functional_area_code

	

EC

	

Functional Area code that’s going to be used as an input parameter of the query XML.




test_url

	

/com.ec.bpm.ext.ec.web/query/schedule_history.xml

	

The path to the query XML.

S2. Set Data View Type

Go to screen Process Overview Configuration.

Open the tab "External Data Panel".

Set "Data View Type" to "EC DAO". This indicates the section handler to retrieve data from the EC Generic DAO model.

Save, more settings should come up.

S3. Configure the EC DAO handler

Update the settings with the following values:

Name	Value	Description


Query XML URL

	

#\{process_action_att.test_url}

	

The relative EC URL to the query XML. Here we use an ECBPM Value Expression, which indicates the XML URL should be retrieved from the Attribute "test_url" of the selected Process Action, which eventually will be resolved to "/com.ec.bpm.ext.ec.web/query/schedule_history.xml".




Layout XML URL

		

The relative EC URL to the layout XML file. This setting is optional.

S4. Configure query XML parameter values

The query XML file requires 4 parameters, which have to be provided to the panel settings.

Add the following parameters to the list:

Name	Value Expression	Description


$FA_ID$

	

#\{ec_obj_id("FUNCTIONAL_AREA", process_action_att.functional_area_code)}

	

The functional area ID. This expression first gets the functional area code from the attribute "functional_area_code" of the selected Process Action, which is "
…[truncated]


==========================================================================================
## [16/24] How-to Show result from a query XML in the External Data view
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_overview/bpm_how_to_show_result_xml_file.html
==========================================================================================
How-to Show result from a query XML in the External Data view
Introduction

The Process Overview screen has a Data View panel, which is for displaying large amounts of data related to the selected node instance/process instance. The External Data section is mainly for projects who need to present data that is not owned by ECBPM, for example, data from another EC module.

By default, the External Data section is left blank. This document guides you to configure this section to show data from a query file.

The External Data section only works for Process Action node instances.
Expected Result

The External Data section shows all business actions registered in EC, using the query file "/com.ec.frmw.co.screens/query/business_action.xml" and layout file "/com.ec.frmw.co.screens/layout/business_action.xml".

Guide
S1. Set Data View Type

Go to screen Process Overview Configuration.

Open the tab "External Data Panel".

Set "Data View Type" to "EC DAO". This tells the section handler to retrieve data from the EC Generic DAO model.

Save, more settings should come up.

S2. Configure the EC DAO handler

Update the settings with the following values:

Name	Value	Description


Query XML URL

	

/com.ec.frmw.co.screens/query/business_action.xml

	

The relative EC URL to the query XML.




Layout XML URL

	

/com.ec.frmw.co.screens/layout/business_action.xml

	

The relative EC URL to the layout XML file. This setting is optional.

S3. Configure query XML parameter values

The query XML file requires the parameter "$BA_TYPE$", which contains the scheduler name. Here we hard code it to "JBPM", meaning it always shows business actions of type "JBPM" (i.e. Process Templates).

Add the following parameter to the list:

Name	Value Expression	Description


$BA_TYPE$

	

JBPM

	
S4. Create a process instance

Start a new process instance for process "advanced_calc_sample", with parameters:

Name	Value


daytime

	

2015-05-02




start_date

	

2015-05-01




end_date

	

2015-05-02




log_level

	

Full




report_definition_code

	

EC_USER_ACCESS_BY_USER




skip_calc

	

[ ]

S5. Check the result

Go to screen Process Overview, update the navigator values, and click the Go button.

Select the new process instance. Wait until the process instance reaches node "Allocation status accepted".

Click on the node "Run calculation", see the "External Data" section loaded with Process Templates.


==========================================================================================
## [17/24] How-to Show variables in the Variables tab
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_overview/bpm_how_to_show_variable.html
==========================================================================================
How-to Show variables in the Variables tab
Introduction

By default, the Variables tab shows no variables, as all variables are considered "internal". This document guides you to enable a variable to be shown on the Variable tab.

Expected Result

Create a new process and show its process variable and node variable in the Variables tab.

Guide
S1. Create a new process

Create a new BPMN2 process, with name "Guide Process".

Add a script node and name it "Initialization".

Add a task node and name it "Leave Comments". Assign group "SYST.ADM" to the task (by setting the Group Id field).

The process should now look like below:

S2. Define variables

Define process variables as below:

Name	Data Type


role

	

String




message

	

String




_comments

	

String

Define variables for Leave Comments as below:

Type	From	To


Input Mapping

	

(Data Item) message

	

Message




Input Mapping

	

(Data Item) role

	

Role




Output Mapping

	

Comments

	

(Data Item) _comments

S3. Apply process variable labels

Process variable labels are applied by the script task "Initialization". Select the node and put the following script into the "Script" field:

com.ec.bpm.api.process.EcbpmSupport ecbpm = com.ec.bpm.api.process.EcbpmSupport.of(kcontext);
ecbpm.processVar("role").withLabel("Role Name").withDescription("The name of the role as input to the process");
ecbpm.processVar("message").withLabel("Message").withDescription("The message as input to the process");
ecbpm.processVar("_comments").withLabel("Comments").withDescription("The comments from user");
S4. Apply node instance variable labels

Node instance variable labels are applied on node basis by using On Entry Script or On Exit Script. In this guide, we add labels to node "Leave Comments".

Select the node "Leave Comments" and put the following code into "On Entry Script":

com.ec.bpm.api.process.EcbpmSupport ecbpm = com.ec.bpm.api.process.EcbpmSupport.of(kcontext);
ecbpm.inputVar("Message").withLabel("Message").withDescription("Message");
ecbpm.inputVar("Role").withLabel("Role").withDescription("Role");
ecbpm.outputVar("Comments").withLabel("Comments").withDescription("Comments");

By now we have completed the process.

S5. Upload the process, build and deploy the project
S6. Add process template in EC

Add a new process template for the new process. Add process template parameters as below:

Name	Type	Sub Type	Mandatory	Description


message

	

Basic Type

	

String

	

Yes

	


role

	

Basic Type

	

String

	

Yes

	
S7. Create a new process instance from the template

Create a new process ins
…[truncated]


==========================================================================================
## [18/24] How-to Show generated calculation log and report as data holder in Variables tab
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_overview/bpm_how_to_show_calc_log.html
==========================================================================================
How-to Show generated calculation log and report as data holder in Variables tab
Introduction

The How-to Show variables in the Variables tab demonstrates how to show simple variables in the Variables tab, but it does not cover how to show data holder variables in the Variables tab. This document guides you on how to show the generated calculation log and report as data holder variables in the Variables tab.

Expected Result

Use the "multiple_report_sample" process which runs calculation and report generation business actions as an example and shows the generated calculation log and report as data holder variables in the Variables tab.

Guide
S1. Multiple Report Sample Overview
S2. About the Process Actions "CalculationAction" and "GenerateReportAction"

It is suggested to read the BPM Sample Process in the Energy Components Software Development Kit (EC-SDK) (energycomponents-sdk/example/bpm/010-bpm-example-project) first to have a general understanding of the "multiple_report_sample" process.

The "multiple_report_sample" process runs the process actions "CalculationAction" and "GenerateReportAction". These two process actions are defined on the Process Action screen. To show the data holder variables in the Variables tab, both these two process actions have a handler called "com.ec.bpm.ext.ec.handlers.AppendParam" to append the generated data set the reference to the output variables. This section will explain the details of these two actions.

CalculationAction
Handlers	Description	Handler Parameter Overwrite


com.ec.frmw.bs.calc.engine.CalcAction

	

Runs calculation business action

	
Parameter Name	Parameter Value


calc_collection_id

	

#\{ec_obj_id( "CONTRACT_GROUP", process_action_input.calc_collection_code)}




jobid

	

#\{ec_obj_id( "CALCULATION", process_action_input.jobcode)}

Explanation:

The parameter "calc_collection_id" is mapped to a value which is fetched by performing a query:

SELECT distinct object_id FROM objects WHERE class_name = "CONTRACT_GROUP" and code = The_Value_of_calc_collection_code

By doing this, users do not need to hard code the "calc_collection_id" in the process.

The parameter "jobid" is given a value which is fetched by performing a query:

SELECT distinct object_id FROM objects where class_name = "CALCULATION" and code = The_Value_of_jobcode

By doing this, users do not need to hard code the "jobid" in the process.

Handlers	Description	Handler Parameter Overwrite


com.ec.bpm.ext.ec.handlers. AppendParam

	

Appends calculation result data set description

	
Parameter Name	Parameter Value


append_param.na
…[truncated]


==========================================================================================
## [19/24] How-to Populate Process Overview Legacy
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_overview/bpm_how_to_populate_process_overview_legacy.html
==========================================================================================
How-to Populate Process Overview Legacy

Process Overview Legacy is a screen to show previously run processes from EC 10 in a read-only state on later versions of EC. In order to do this, there are certain steps that need to be taken before, during and after the migration:

Before you migrate any data from your EC 10 database, and after your last process is run on the EC 10 system, run the following business action: com.ec.frmw.action.logupgrade.ConvertJbpmLogs
This business action will move data from the native JBPM tables in 10.4 to EC_JBPM_LOG.

Migrate the following tables from EC 10 to your EC database:

JBPM_PROCESSINSTANCE

JBPM_PROCESSDEFINITION

JBPM_VARIABLEINSTANCE

JBPM_NODE

EC_JBPM_LOG

Any business action with BA_TYPE 'JBPM' in the EC 10 database, needs to be migrated from the old system to the new system with the exact same BUSINESS_ACTION_NO.

When these steps are taken, the processes should show up in your Process Overview Legacy screen.


==========================================================================================
## [20/24] Process Monitor Cache
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_monitor/bpm_pm_monitor_cache.html
==========================================================================================
Process Monitor Cache
Introduction

In order to improve performance of Process Monitor screen, a process monitor instance snapshot cache is implemented to cache snapshots for completed and aborted instances. Completed and aborted instance snapshots are finalized since the corresponding process instances have come to an end state. On the contrary, active or pending instances cannot be cached since the process instances are still in progressive state.

Cache Capacity

Custom property "Process Monitor Instance Snapshot Cache Capacity" is used to configure the cache size, default value is 0, meaning the cache is disabled by default. User can change the cache capacity according to their own usages of BPM and process monitor. Note that EC application need to be restarted to apply the cache capacity changes.

Cached Process Variables

To avoid fetching and caching all process variables for the process instance snapshot, a system property named "Process Monitor Instance Snapshot Cache Process Variables" is used to define which process variables should be fetched and cached for process monitor. For example, if you configure process monitors to view instances based on daytime variables, then the daytime variables should be defined in this property, use comma to separate different variables.

Note that this property is used by all process monitors, so be careful when deleting variable from the list. User might need to refresh MonitorInstanceSnapshotCache when adding new process variable to the property.

View and Flush Cache

Use EC Flush Cache page to view and flush process monitor cache, user can either flush the whole MonitorInstanceSnapshotCache or delete entries from the cache for specific process instances.


==========================================================================================
## [21/24] How-to Apply a customized viewer tag to node instance in business action
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_monitor/bpm_pm_customised_viewer_tag.html
==========================================================================================
How-to Apply a customized viewer tag to node instance in business action
Introduction

By default, Process Monitor - Daytime Range View uses node status and task status as default viewer tags. However, customized viewer tags can also be given by the invoking business action to provide features like

Business Action Intermediate State - For a long time running business actions it may be useful to show the intermediate state in the Process Monitor

Customized Business Action State

This guide shows how to create a business action that injects customized viewer tags to the invoking node instance.

Guide
S1. Define Viewer Tags

The new business action injects three viewer tags. They have to be registered in the system before being used.

Go to the screen Viewer Tag and add the following tags:

Name	Description	Property/color	Property/text


tag_1

	

Tag 1

		

Tag 1




tag_2

	

Tag 2

		

Tag 2




tag_3

	

Tag 3

		

Tag 3

S2. Create a business action

Create a new business action class, extending class com.ec.eccore.controller.event.AbstractBusinessAction.

The class may look like:

public class SimpleViewerUpdateBusinessAction extends AbstractBusinessAction {
    @Override
    public Object execute(Connection connection) throws BusinessActionExecuteException {
        Consumer<String> tagUpdater = (Consumer<String>)getUserEvent().getParameterObject("ecbpm_vtag.tag_updater");
        waitOneMin();
        tagUpdater.accept("tag_1");
        waitOneMin();
        tagUpdater.accept("tag_2");
        waitOneMin();
        tagUpdater.accept("tag_3");

        return null;
    }

    private void waitOneMin() {
        try {
            Thread.sleep(60 * 1000);
        } catch (InterruptedException e) { }
    }
}

The business action updates tags per 1 minute. In three minutes, the three tags are applied in turn. On completion of the node, the viewer tag is overwritten by the completed status.

Include this business action in the project extension and start the extension in EC. See Energy Components Software Development Kit (EC-SDK) - energycomponents-sdk/examples/extensions for example to create an extension with business action.

S3. Create a process

Create a new process (or use an existing one) and add a new node that invokes the new business action.

Add an additional String/Boolean argument "arg_ecbpm_use_tag_updater" to the business action/process action invocation node, with value "true".

Save and deploy the project.

Register the process in Process Template. In this guide, we use the name "viewer_tag_process_sample".

S4. Create a Process Monitor
…[truncated]


==========================================================================================
## [22/24] How-to Apply production day offset to sub-daily process monitor
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_monitor/bpm_pm_production_day_offset.html
==========================================================================================
How-to Apply production day offset to sub-daily process monitor
Introduction

The Process Monitor provides an aggregated view of multiple process instance data. Depending on the view type being used, Process Monitor can provide data to different interests.

In this guide, we walk you through how to apply EC Production Day Offset to a Process Monitor that aggregates sub-daily process instances.

EC Production Day Offset can only be applied when "Hours of a production day" is used for Daytime List Provider.
Expected Result

Monitor view lists hours of a given day starting from the Day Offset of the specified Production Day.

Guide
S1. Verify the existing Process Monitor

Verify that your process monitor is sub-daily, meaning that it is using "Hours of a production day" or "Hours of a day" for Daytime List Provider. This can be checked in the screen Process Monitor Configuration, Settings tab.

Note that if your monitor is not sub-daily, it doesn’t list hours in the view, meaning that this guide is not valid for your monitor.

Your monitor daytime list should look like:

S2. Apply Production Day Offset

Go to the screen Process Monitor Configuration.

Select your process monitor.

Go to tab Settings.

Update the Daytime List Provider to "Hours of a production day".

Choose a Production Day object for the Production Day field. In this guide, we use "P1 0060" from EC test data, which has 6 hours offset.

S3. View the monitor

Go to the Process Monitor screen, your monitor should have daytime starting at 06:00 of the specified day.


==========================================================================================
## [23/24] How-to Customize texts and background colors in Process Monitor view
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_monitor/bpm_pm_background_colors.html
==========================================================================================
How-to Customize texts and background colors in Process Monitor view
Introduction

Process Monitor - Daytime Range View displays node instance status and task status with pre-configured text and color. ECBPM supports customizing view texts and colors via Viewer Tag. This guide will walk you through how to update those texts and colors.

Currently, only Daytime Range View monitors support updating display text and color.
Expected Result

In this example, we are going to use an existing process monitor, which has a view:

We are going to update the default text for Task Ready state and its background color.

Guide
S1. Verify the Process Monitor Type

To verify your monitor type, go to Process Monitor Configuration screen, see the column "Monitor Type".

S2. Update Viewer Tag Properties

Texts and background colors are stored as Viewer Tag properties. To change the default values, first, go to screen Viewer Tag.

This screen lists all tags in the system. System preserved tags are named with prefix "ecbpm__", and are read-only. You can also add your own tags to this list for later reference in your business action.

Select tag "ecbpm__task_ready", and update properties:

Property	Value


color

	

#23f6af




text

	

Ready

S3. See the monitor view update

Go back to the monitor view and reload it. Background color and text updates should take effect:


==========================================================================================
## [24/24] How-to View execution status of monthly process within a year
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/bpm/process_monitor/bpm_pm_monthly_process.html
==========================================================================================
How-to View execution status of monthly process within a year
Introduction

The Process Monitor provides an aggregated view of multiple process instance data. Depending on the view type being used, Process Monitor can provide data to different interests.

In this guide, we will walk you through how to use the Process Monitor to overview all process instance execution status within a given month.

Expected Result

To create a Process Monitor that shows execution status of process "advanced_calc_sample" within a month, with a detailed status of node "Run calculation", "Allocation status accepted", "Generate and send report/Generate Report" and "Generate and send report/Send Report".

Guide
S1. Create Process Instances

Create 5 process instances of "advanced_calc_sample", with the following parameters:

Instance 1

Name	Value


daytime

	

2015-01-02




start_date

	

2015-01-01




end_date

	

2015-01-02




log_level

	

Full




report_definition_code

	

EC_USER_ACCESS_BY_USER




skip_calc

	

[ ]

Instance 2

Name	Value


daytime

	

2015-02-02




start_date

	

2015-02-01




end_date

	

2015-02-02




log_level

	

Full




report_definition_code

	

EC_USER_ACCESS_BY_USER




skip_calc

	

[ ]

Instance 3

Name	Value


daytime

	

2015-03-02




start_date

	

2015-03-01




end_date

	

2015-03-02




log_level

	

Full




report_definition_code

	

EC_USER_ACCESS_BY_USER




skip_calc

	

[ ]

Instance 4

Name	Value


daytime

	

2015-04-02




start_date

	

2015-04-01




end_date

	

2015-04-02




log_level

	

Full




report_definition_code

	

EC_USER_ACCESS_BY_USER




skip_calc

	

[ ]

Instance 5

Name	Value


daytime

	

2015-05-02




start_date

	

2015-05-01




end_date

	

2015-05-02




log_level

	

Full




report_definition_code

	

EC_USER_ACCESS_BY_USER




skip_calc

	

[ ]

S2. Create a Process Monitor

Go to the Process Monitor Configuration screen.

Create a new Process Monitor with the following data:

Code	Name	Functional Area	Monitor Type	Description


calculation_monthly_view

	

Calculation Monthly View

	

EC

	

Daytime Range View

	
S3. Add available processes

Select the new process monitor.

Open the Process Templates tab.

Add a new Process Template:

Process Template


advanced_calc_sample

S4. Add nodes to monitor

Open the Nodes tab.

Add nodes with the following data:

Display Text	Order	Root Process	Node	Sub-Node 1	Sub-Node 2	Sub-Node 3	Sub-Node 4	Comments


Calculation

	

1

	

advanced_ calc_sample

	

Run calculation

					


Calculation Accepted

	

2

	

advanced_calc_sample

	

Allocation sta
…[truncated]