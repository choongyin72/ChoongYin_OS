# Raw content — DOC-11
Modules: ['frmw/iam', 'frmw/databasedevelopment', 'frmw/containers', 'frmw/flyway', 'frmw/blobstorage', 'frmw/tools']
Pages: 28



==========================================================================================
## [1/28] Energy Components Docker Images
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/index.html
==========================================================================================
Energy Components Docker Images

This section contains reference documentation for the individual EC docker images. Specifically, which parameters or environment variables each image support.

Most of these settings are for advanced configuration of EC containers.
Complete examples on how to configure and deploy EC containers are available in the Energy Components SDK.

The Energy Components distribution contains the following docker images

Energy Components - Application

Energy Components - BPM

Energy Components - Identity manager

Energy Components - Identity Manager Configuration

Energy Components - Reporting and Analytics

Energy Components - Messaging broker

Energy Components - Antivirus

Energy Components - Analytics Manager

Energy Components - Analytics Manager Runner

Secrets

Secrets provide a mechanism to hold sensitive information such as credentials. Secrets can be created from plain text files. The text file contains key-value pairs in plain text.

Example:

DB_HOSTNAME=ecdb
DB_USERNAME=ENERGYX_EC
DB_PASSWORD=SecretPassword
The secret files must have Unix (LF) line ending.
The secret file should be mounted to the path "/mnt/secrets/secret.properties" (this cannot be changed) in the containers.


==========================================================================================
## [2/28] Energy Components - Application
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-ec-app.html
==========================================================================================
Energy Components - Application
Description

Energy Components main application docker image.

Image name

ec-ec-app

Environment variables for runtime configuration

An environment file can be passed as a parameter to Docker run:

docker run --env-file src/main/resources/ecruntime.env …​image-name and other params…​

Database connection settings

Database connection string can be specified by DB_URL or by DB_HOSTNAME, DB_PORT and DB_SERVICENAME. DB_URL has precedence.

DB_URL=jdbc:oracle:thin:@//ecdb:1521/orcl

or

DB_HOSTNAME=ecdb

DB_PORT=1521

DB_SERVICENAME=orcl

Username and password for database schema ENERGYX and ECKERNEL

DB_USERNAME=ENERGYX_EC

DB_PASSWORD=energy

DB_ADMINUSER=ECKERNEL_EC

DB_ADMINPASSWORD=energy

DB_URL can be used to configure failover database connection.

DB_URL=jdbc:oracle:thin:@(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=host1)(PORT=1521))(ADDRESS=(PROTOCOL=TCP)(HOST=host2)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=service_name)))

If a separate Message Broker database is used, environment variables DB_MHM_BROKER_URL, DB_MHM_BROKER_USERNAME and DB_MHM_BROKER_PASSWORD can be set to configure database connection.

DB_MHM_BROKER_URL=jdbc:oracle:thin:@//db:1521/orcl

DB_MHM_BROKER_USERNAME=ENERGYX_EC

DB_MHM_BROKER_PASSWORD=energy

If these environment variables are not set the default DB_URL, DB_USERNAME, and DB_PASSWORD will be used.

Management settings

The Jboss local admin user account, for development and debugging.

MGMT_USER=admin

MGMT_PASSWORD=admin

Enable debugging

To enable remote JVM debugging, hot deployable resources and development stack traces and connection leak detection.

ENABLE_DEBUGGING=true

Enabling debugging has severe performance and security impact and cannot be used in production.

Enable debugging will cause runtime exceptions if there are any connection leaks.

Advanced memory settings
EC_NONHEAP_MEM

Define the amount memory in Mb’s that should be available outside of the heap space. This should normally not be changed. Defaults to 1400.

If EC gets OOM killed by the docker orchestrator, either increase the memory limits in the container runtime or increase EC_NONHEAP_MEM.

*** JBossAS pr
…[truncated]


==========================================================================================
## [3/28] Energy Components - BPM
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-ecbpm.html
==========================================================================================
Energy Components - BPM
Description

The Energy Components business process management docker image.

Image name

ec-ecbpm

Environment variables for runtime configuration

An environment file can be passed as a parameter to Docker run:

docker run --env-file src/main/resources/ecruntime.env …​image-name and other params…​

Database connection settings

Database connection string can be specified by DB_URL or by DB_HOSTNAME, DB_PORT and DB_SERVICENAME. DB_URL has precedence.

DB_URL=jdbc:oracle:thin:@//ecdb:1521/orcl

or

DB_HOSTNAME=ecdb

DB_PORT=1521

DB_SERVICENAME=orcl

Username and password for database schema ENERGYX and ECKERNEL

DB_USERNAME=ENERGYX_EC

DB_PASSWORD=energy

DB_ADMINUSER=ECKERNEL_EC

DB_ADMINPASSWORD=energy

Max db connection pool size

Max pool size for managed db connections. Default is 100

DB_MAX_POOL_SIZE=100

Management settings

The Jboss local admin user account, for development and debugging.

MGMT_USER=admin

MGMT_PASSWORD=admin

Enable debugging

To enable remote JVM debugging, hot deployable resources and development stack traces.

ENABLE_DEBUGGING=true

Enabling debugging has severe performance and security impact and cannot be used in production.
Advanced memory settings
EC_NONHEAP_MEM

Define the amount memory in Mb’s that should be available outside of the heap space. This should normally not be changed. Defaults to 600.

If EC gets OOM killed by the docker orchestrator, either increase the memory limits in the container runtime or increase EC_NONHEAP_MEM.

*** JBossAS process (xxx) received KILL signal ***

EC_NONHEAP_MEM=600

ENABLE_NMT

Enable java native memory tracking. See Java 11 Oracle documentation. Used only for tracking down native memory leaks in a dev environment. Has 5-10% performance impact.

ENABLE_NMT=false

Enable wildfly statistics

This will enable statistics for the ejb3, transactions, web-services, undertow and the datasource subsystems. Enabling this might have a performance impact.

WILDFLY_STATISTICS=false

Specify log level

Default is WARN.

EC_LOGLEVEL=WARN

Specify log level for underlying image

Default is INFO.

ROOT_LOGLEVEL=INFO

Networking settings
Internal location of the EC application

Wh
…[truncated]


==========================================================================================
## [4/28] Energy Components - Identity manager
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-keycloak.html
==========================================================================================
Energy Components - Identity manager
Description

The Energy Components identity provider docker image built on keycloak

Image name

ec-keycloak

Environment variables for runtime configuration

An environment file can be passed as a parameter to Docker run :

docker run --env-file src/main/resources/ecruntime.env …​image-name and other params…​

The official keycloak container documentation.

Database connection settings

Database connection string can be specified by DB_URL or by DB_ADDR, DB_PORT and DB_DATABASE. DB_URL has precedence.

DB_URL=jdbc:oracle:thin:@//ecdb:1521/orcl

or

DB_ADDR=ecdb

DB_PORT=1521

DB_DATABASE=orcl

Database vendor and username and password for KCKERNEL database schema

DB_VENDOR=oracle

DB_USER=kckernel_ec

DB_PASSWORD=energy

Management settings
Keycloak admin account

The keycloak admin console account, only use during initial installation before the master realm and admin-cli-confidential client is imported.

After the master realm has been imported the admin user credentials is stored in the db and this variable should not be used.

KC_BOOTSTRAP_ADMIN_USERNAME=admin

KC_BOOTSTRAP_ADMIN_PASSWORD=admin

Enable keycloak statistics

This will enable statistics for the db, http and jgroups subsystems. Enabling this might have a performance impact.

WILDFLY_STATISTICS=false

Specify log level

KEYCLOAK_LOGLEVEL=DEBUG

Keycloak hostname / url

See keycloak documentation

KC_HOSTNAME=ec.companydomain.com

KC_HOSTNAME=https://ec.companydomain.com/auth

Do not include a port section if using default ports (443 for https or 80 for http). The formed url must be the exact same string as what is displayed in the browser address bar.
Keycloak hostname strict https
KC_HOSTNAME_STRICT_HTTPS is removed from Hostname v2 configuration. Ref: Configuring the hostname (v2).
Instead, specify KC_HOSTNAME as a url (e.g. KC_HOSTNAME=https://ec.companydomain.com:8443/auth)

When KC_HOSTNAME is not an URL and KC_HOSTNAME_STRICT_HTTPS is configured, KC_HOSTNAME is updated as following:

KC_HOSTNAME_STRICT_HTTPS=false and KC_HOSTNAME=ec.companydomain.com:8080, ⇒ http://ec.companydomain.com:8080/auth

KC_HOSTNAME_STRICT_HTTPS=true and KC_HOSTNAME=ec.company
…[truncated]


==========================================================================================
## [5/28] Energy Components - Identity Manager Configuration
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-keycloak-migration.html
==========================================================================================
Energy Components - Identity Manager Configuration
Description

The Energy Components identity provider configuration migration docker image. This container is closely linked to the ec-keycloak container and is supposed to run either as a Kubernetes init-container or alongside this.

There are several Keycloak configurations that has to be done before Keycloak can be used as an IDP for EC. The minimal configuration for running EC is done by this container. The container is using the same configuration variables as the main ec-keycloak container and have to run to completion before EC can be used.

The container is powered by Flyway technology to keep track of applied configurations, hence in the rest of this document configuration changes will be referred to using the Flyway term migrations.

It will create the realms, clients and service-accounts required for EC as versioned Flyway migrations. Environment specific configurations like system urls, client-ids and so on will be applied as repeatable migrations configured with environment variables, and will be applied each time the environment variables changes. One example of this is the EC-RA clientId.

In Kubernetes and Openshift this is handled by running the container as an Init container. See Kubernetes Init Container documentation for detailed information on how this works. In this mode the container will use the embedded Keycloak to apply the migrations.

On Docker swarm the container has to be run alongside the existing ec-keycloak container, it will then use the configured EC_URL_AUTH_SERVER and apply the migrations there.

Image name

ec-keycloak-migration

Environment variables for runtime configuration

An environment file can be passed as a parameter to Docker run :

docker run --env-file src/main/resources/ecruntime.env …​image-name and other params…​

This container uses the same configuration variables as Energy Components - Identity manager.

Common required variables as described in ec-keycloak documentation

Database connection string can be specified by DB_URL or by DB_HOSTNAME, DB_PORT and DB_SERVICENAME. DB_URL has precedence.

DB_URL=jdbc:oracle:thin:@//ecdb:1521/orcl

or

DB_ADDR=ecdb

DB_
…[truncated]


==========================================================================================
## [6/28] Energy Components - Reporting and Analytics
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-ra.html
==========================================================================================
Energy Components - Reporting and Analytics
Description

The Energy Components Reporting and Analytics docker image.

Image name

ec-ra

License deployment and upgrade

The image will look in /opt/jboss/wildfly/ecra-license folder for license files. If exactly one license file is found, it will be uploaded to yellowfin automatically. This folder can be mounted as a volume or a docker swarm secret file. See https://docs.docker.com/engine/swarm/secrets/ for how to work with docker swarm secrets.

Environment variables for runtime configuration

An environment file can be passed as a parameter to Docker run:

docker run --env-file src/main/resources/ecruntime.env …​image-name and other params…​

Database connection settings

YELLOWFIN_DB_URL=jdbc:oracle:thin:@//db:1521/ORCL

YELLOWFIN_DB_USER=YFKERNEL_EC

YELLOWFIN_DB_PASSWORD=energy

YELLOWFIN_ECDS_URL=jdbc:oracle:thin:@//db:1521/ORCL

YELLOWFIN_ECDS_USER=ANALYTICS_EC

YELLOWFIN_ECDS_PASSWORD=energy

Networking settings

EC_URL_AUTH=https://ec.companydomain.com:8443/auth

EC_URL_RA_EXT=https://ec.companydomain.com:8443/ra

ECRA_ADMIN_USERNAME=admin

ECRA_ADMIN_PASSWORD=admin

YELLOWFIN_CONCURRENT_TASKS=25

YELLOWFIN_INIT_WAIT_TIME=5

YELLOWFIN_MAX_EXEC_TIME=240

YELLOWFIN_NO_SCHEDULER_THREADS=25

YELLOWFIN_MAX_THREAD_QUEUE=100

SAMLINCOMINGCERT=theIdPEntityCertificate

SAMLSTRICTMODE=false

SAMLSPCERTIFICATE=theServiceProviderCertificate

SAMLSPPRIVATEKEY=theServiceProviderPrivateKey

Identity Provider URL
EC_URL_AUTH variable has to be set to the public, DNS resolvable and reachable endpoint of the Keycloak frontend.
Identity Provider Certificate

The content for SAMLINCOMINGCERT should be copied from keycloaks energyx realm settings under the Keys tab. Click on the Certificate button and a popup with the certificate will pop up. Another way to get hold of the certificate is to use the keycloak rest api to query for it.

Example :

kcadm.sh get keys  -r energyx  --server http://ul001918:8080/auth --realm master --user admin --password admin  | jq '.keys[1].publicKey'
Saml Strict mode

To enable SAML strict mode set SAMLSTRICTMODE=true . This will enable strict verification of the SAML response. For this to work a
…[truncated]


==========================================================================================
## [7/28] Energy Components - Messaging broker
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-messaging.html
==========================================================================================
Energy Components - Messaging broker
Description

The Energy Components messaging broker docker image.

All durable messages will be dropped after 10 days.

Image name

ec-messaging

Environment variables for runtime configuration

An environment file can be passed as a parameter to Docker run:

docker run --env-file src/main/resources/ecruntime.env …​image-name and other params…​

Database connection settings

Database connection string can be specified by DB_URL or by DB_HOSTNAME, DB_PORT and DB_SERVICENAME. DB_URL has precedence.

DB_URL=jdbc:oracle:thin:@//ecdb:1521/orcl

or

DB_HOSTNAME=ecdb

DB_PORT=1521

DB_SERVICENAME=orcl

Username and password for database schema ENERGYX

DB_USERNAME=ENERGYX_EC

DB_PASSWORD=energy

Memory settings

The default memory setting is 800 MB. How much memory it will use will vary based on how many messages will go through it. Every message is persisted in the database, however the container keeps metadata in memory to keep track. This metadata can grow large depending on the number of messages in the queue. It is recommended to do an evaluation of how much data will be imported through EC Integration Services (ECIS) and how much event functionality will be utilized in the system.

An out of memory situation will often manifest with a messaging pod that keeps restarting. If large amount of data is expected (or if you receive memory heap issues), it is recommended to increase the memory settings of the container.

JMS Queue paging

In scenarios where heap memory is limited and the workload is large, it is possible to enable memory paging for the queues. That means that after the queue size reaches a certain limit, it will start to page out parts of the queues to the database. To do this it will create tables in the db to store the paged data, and the db schema user thus has to have CREATE TABLE privilege or equivalent. The eckernel_&operation schema will have this out of the box.

Even with paging enabled, large queue sizes still require some memory to handle. If after enabling paging you still get shutdown by the container orchestrator, the only recourse is to increase the memory limits for the container until the workload can
…[truncated]


==========================================================================================
## [8/28] Energy Components - Antivirus
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-antivirus.html
==========================================================================================
Energy Components - Antivirus
Description

Antivirus scanning of uploaded files is an important step in securing the EC system from malicious content. By default EC scans all files uploaded via EC screens and the EC REST API.

The EC antivirus service is based on the official Docker image of the ClamAV open-source virus scanner. EC connects to the antivirus container either over HTTP or TCP depending on configuration.

It is very important that the ports on this image is not exposed externally. The ports must only be available to other containers on the internal network.

The Docker image contains the latest virus definitions that were available at build time. Virus definitions are automatically updated during container startup and periodically while the container is running. Update frequency can be configured. Virus databases are downloaded from database.clamav.net.

Image name

ec-clam-av

Configuration

The following environment variables are exposed by the base ClamAV Docker image and controls the main behavior of the image. Please refer to the ClamAV Docker documentation for a complete description of these variables.

CLAMAV_NO_CLAMD=false : Enable or disable the ClamD scanning daemon. Do not disable this!

CLAMAV_NO_FRESHCLAMD=false : Enable or disable automatic virus definition updates.

FRESHCLAM_CHECKS=1 : Number of automatic virus definition updates per day.

CLAMD_STARTUP_TIMEOUT=1800 : Max seconds to wait for the ClamD daemon to start.

The ClamD scanning daemon is configured via a config file on the image. The config file is located in /etc/clamav/clamd.conf. To make configuration simpler, the most useful of these settings can be tweaked using environment variables. The environment variable names are similar to the underlying ClamD setting names for easy comparison. The settings are documented in more detail in the config file itself. A sample ClamD config file can be viewed in the ClamAV source repository.

CLAMD_TCP_SOCKET=3310 : The TCP port the ClamD daemon listens to. If the port number is changed, the AV_PORT environment variable in the ec-app container must also be set to the same value if EC is connecting over TCP. Do not expose this port ex
…[truncated]


==========================================================================================
## [9/28] Energy Components - Analytics Manager
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-analytics-manager.html
==========================================================================================
Energy Components - Analytics Manager
Description

The Energy Components Analytics Manager docker image. It is used to manage analytics jobs from Energy Components.

Image name

ec-analytics-manager

Environment variables for runtime configuration

An environment file can be passed as a parameter to Docker run:

docker run --env-file src/main/resources/ecruntime.env …​image-name and other params…​

Open ID settings

These environment variables are used for authentication. They specify the url for open ID configuration, client id and secret used to authenticate REST requests, and client admin role and user role.

Open ID configuration url

EC_ANALYTICS_OPENID_CONFIG_URL=http://keycloak:8080/auth/realms/energyx/.well-known/openid-configuration

Client id

EC_ANALYTICS_OPENID_CLIENTID=analytics-manager

Admin role name

EC_ANALYTICS_OPENID_ADMIN_ROLE_NAME=analytics-manager-admin

Client role name

EC_ANALYTICS_OPENID_USER_ROLE_NAME=analytics-manager-start-job

Agent role name

EC_ANALYTICS_OPENID_AGENT_ROLE_NAME=analytics-manager-agent

Agents modification role name. Can be assigned to agent service account to have autopaired with Analytics Manager. Applied by default for internal agent (analytics-manager-runner container). For manual pairing of external agents use only single role analytics-manager-start-job.

EC_ANALYTICS_OPENID_AGENTS_MODIFY_ROLE_NAME=analytics-manager-agents-modify

Modules modification role name. To fine-tune access rights of users who can add/remove analytics modules.

EC_ANALYTICS_OPENID_MODULES_MODIFY_ROLE_NAME=analytics-manager-modules-modify

Frontend modification role name.

EC_ANALYTICS_OPENID_FRONTEND_MODIFY_ROLE_NAME=analytics-manager-frontend-modify

Database settings

Oracle connection string. Usually point to a database container or ip/host if external service.

EC_ANALYTICS_ORACLE_CONNECT="//ecdb:1521/ORCL"

Oracle user. The EC default is AMKERNEL_EC

EC_ANALYTICS_ORACLE_USERNAME="AMKERNEL_EC"

Oracle user password.

EC_ANALYTICS_ORACLE_PASSWORD="energy"

Oracle database OOB specific

In case of running Oracle on the host (accessible as host ip address) the connection to Oracle database happens via docker-proxy to the host network
…[truncated]


==========================================================================================
## [10/28] Energy Components - Analytics Manager Runner
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-analytics-manager-runner.html
==========================================================================================
Energy Components - Analytics Manager Runner
Description

The Energy Components Analytics Manager Runner docker image. It is used by the Analytics Manager to run analytics jobs.

Image name

ec-analytics-manager-runner

Environment variables for runtime configuration

An environment file can be passed as a parameter to Docker run:

docker run --env-file src/main/resources/ecruntime.env …​image-name and other params…​

Analytics Manager Host

The host name for EC Analytics Manager

ANALYTICS_MANAGER_HOST=ec-analytics-manager

Open ID settings

These environment variables are used for authentication. They specify the client id and secret used to authenticate.

Client id

EC_ANALYTICS_OPENID_CLIENTID=analytics-manager-agent

Client secret

EC_ANALYTICS_OPENID_CLIENTSECRET=CHANGE_ME

The Client’s service account user must have client role analytics-manager-agent for client analytics-manager.


==========================================================================================
## [11/28] Identity & Access Management
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/iam/iam-overview.html
==========================================================================================
Identity & Access Management
Authentication and Authorisation

Keycloak is used for Authentication and Authorisation.

Users, role assignments and group membership can be managed in Keycloak or Energy Components business functions. Keycloak can use different Identity Providers and user federation providers, such as identity brokering with OIDC or SAML, or userfederation using LDAP providers

There’s a large number of commercially available Identity Providers that can be used with Keycloak, such as Azure AD, Okta, Google, etc. The recommended integration approach is to use Identity brokering with OpenId Connect towards third party Identity Providers.

For more information about Keycloak, see https://www.keycloak.org/docs/latest/server_admin/

Pre EC 14.0.0, users and user’s roles were configured in EC and table T_BASIS_USER and T_BASIS_USERROLE. These tables have been removed and the T_BASIS_USER and T_BASIS_USERROLE classes are converted to META classes. These classes list the same information as before, but are retrieving it from Keycloak and not the EC database. They can be used in the EC application, REST API and BPM. They are not available in the database.

Roles

Roles define the activities a particular business role can access – e.g. well configuration, well data, REST endpoints, etc. They also determine the level of access – e.g.: view well configurations, insert and update well data, view well configurations.

The activity objects that can be accessed are defined in the Object Maintenance screen. Roles access to the objects can be assigned in the Object Maintenance screen or Role Maintenance screen.

Roles exist in both Keycloak and EC. Keycloak is the master. Roles can be synchronised between Keycloak and EC from the Role Maintenance screen.


==========================================================================================
## [12/28] How to configure the User session timeout
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/iam/how_to_configure_session_timeout.html
==========================================================================================
How to configure the User session timeout

The User Session in EC and the authentication session provided by Keycloak are tightly coupled.

The EC session timeout value and the value for "Keycloak SSO Session Idle" value should be set to the same value.

The EC session timeout is set by environment variable EC_SESSION_TIMEOUT. Refer to Energy Components - Application.

The setting for Keycloak "SSO Session Idle" can be found in "Realm Settings", "Sessions":


==========================================================================================
## [13/28] User Federation, Identity brokering and Single sign-on
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/iam/userfederation_idp_sso.html
==========================================================================================
User Federation, Identity brokering and Single sign-on
Introduction

The examples in this article are based on Keycloak, an open-source Identity and Access Management (IAM) solution that provides features such as Single sign-on (SSO), Identity brokering, and User federation. These features are essential for managing user identities, authenticating users, and providing secure access to applications and services. In this article, we will explain what these features are and how they can be used to enhance the security and user experience of your Energy Components installation.

This document assumes a good understanding of authentication, authorization and the standards used in IAM such as OAuth2, OpenID Connect (OIDC), LDAP, and SAML. One should also have a firm grasp of the Keycloak concepts and terminology, such as realms, clients, users, roles, and groups.

The process of migrating an existing Energy Components installation, with users and authorization already configured, to use an external identity provider or user federation requires careful planning and testing. Make sure proper backup and restore procedures are in place, it is recommended to consult with the administrators or other subject-matter experts of the external IAM system to gather the required information and mapping requirements.
Authentication

Authentication is the process of verifying the identity of a user or system. It is the first step in the security process and is used to ensure that only authorized users have access to a system or application. Authentication is typically done by verifying a user’s credentials, such as a username and password, against a known set of credentials stored in a database or directory. In the context of Keycloak, authentication refers to the process of verifying the identity of a user by validating their credentials against the Keycloak user database or an external identity provider.

Authorization

Authorization is the process of determining what a user is allowed to do after they have been authenticated. It is used to control access to resources or services based on the user’s identity and the permissions they have been granted. Authorization is typically don
…[truncated]


==========================================================================================
## [14/28] User account settings
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/iam/keycloak/keycloak-account-setting.html
==========================================================================================
User account settings

Keycloak has a built-in User Account Service which every user has access to. This service allows users to manage their account, change their credentials, update their profile, and view their login sessions. The URL to this service is /auth/realms/energyx/account.

For more information see https://www.keycloak.org/docs/latest/server_admin/#_account-service.


==========================================================================================
## [15/28] How to configure audit logging
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/iam/keycloak/keycloak-audit-logging.html
==========================================================================================
How to configure audit logging

Keycloak supports logging of login events and admin events. For more information see https://www.keycloak.org/docs/latest/server_admin/#auditing-and-events.

To configure Audit logging, login to Keycloak admin console and go to the "Realm Settings" left menu item, then click on the Events tab. Events can be viewed in the "User Events Settings" tab or the "Admin Events Settings" tab.


==========================================================================================
## [16/28] How to configure Brute Force Protection
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/iam/keycloak/keycloak_brute-force.html
==========================================================================================
How to configure Brute Force Protection

A brute force attack happens when an attacker is trying to guess a user’s password. Keycloak has some limited brute force detection capabilities. See https://www.keycloak.org/docs/latest/server_admin/#password-guess-brute-force-attacks.

To enable Brute Force Protection, login to Keycloak admin console and go to the Realm Settings left menu item, click on the Security Defenses tab, then go to the Brute Force Detection sub-tab.


==========================================================================================
## [17/28] How to configure Password Policy
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/iam/keycloak/keycloak-password-policy.html
==========================================================================================
How to configure Password Policy

Password policy is a set of rules to increase the security against intruders. Keycloak supports several different policies that can be enabled through the admin console. See https://www.keycloak.org/docs/latest/server_admin/#_password-policies.

To enable Keycloak password policies, login to the Keycloak admin console, click on the Authentication left menu item, select the Policies tab and go the the Password Policy sub-tab. Choose the policy you want to add in the drop down list box. This will add the policy in the table on the screen. Choose the parameters for the policy. Hit the Save button to store your changes.


==========================================================================================
## [18/28] How to assign roles to jbpmengine user
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/iam/keycloak/keycloak_jbpmengine_roles.html
==========================================================================================
How to assign roles to jbpmengine user

The jbpmengine user is the Service Account User for the bpm-client client. The jbpmengine user runs the BPM processes.

To assign roles to the jbpmengine user, login to the Keycloak admin console, click on the Clients left menu item, click on the bpm-client client and go to the Service Account Roles tab.


==========================================================================================
## [19/28] How to create Service Account for external integration access
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/iam/how_to_create_service_account.html
==========================================================================================
How to create Service Account for external integration access
Introduction

Using the EC public APIs require a service account. It is best practice to use individual service accounts for each integration. This makes it easier to administer, audit and for example revoke the credentials (secret) for one integration without disrupting any other.

Client and Service Account

Clients are entities that can request Keycloak to authenticate a user. Most often, clients are applications and services that want to use Keycloak to secure themselves and provide a single sign-on solution. Clients can also be entities that just want to request identity information or an access token so that they can securely invoke other services on the network that are secured by Keycloak.

Each client has a built-in service account which allows it to obtain an access token. Roles can be assigned to the service account. The assigned roles defines which access the service account has.

When a User Account is used to load data into EC, the created by and last updated by will be set to the Service Account username.

The service account should be assigned the minimum access that it needs.

Example: A client reading data from rest endpoint /rest/v1/domain/data/PWEL_DAY_STATUS should only have access to this endpoint.

The role’s access is configured in EC and Role Maintenance or Object Maintenance screens.

Client Credential Flow

The Client Credential Flow involves an application exchanging its application credentials, such as client id and client secret, for an access token.

This flow is best suited for Machine-to-Machine (M2M) applications, such as CLIs, daemons, or backend services, because the system must authenticate and authorize the application instead of a user.

Application sends application’s credentials to the Auth0 Authorization Server.

Authorization Server validates application’s credentials.

Authorization Server responds with an access token.

Application can use the access token to call an API on behalf of itself.

API responds with requested data.

Service accounts delivered with EC
Client	Service account	Description


ecworker

	

service-account-ecworker

	

Client used by EC 
…[truncated]


==========================================================================================
## [20/28] How to Update Online Help
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/tools/how_to_update_online_help.html
==========================================================================================
How to Update Online Help
Introduction
What is this Document about?

The Help system in Energy Components (also referred to as 'Online Help') is contextualized depending on which screen the user is using. For example, if the user is at the "Company" screen, the help information provided will relate specifically to the "Company" screen.

This How-To guideline describes the nature of the Online Help in EC and the steps required when the user wants to make additions to the Online Help for a given screen (Business Function) for EC 13.0.0 version.

This How-To also describes the process of extracting Online Help Description from the database for import to other databases.

Who will find this Document useful?

This document is intended to support IT staff working with the installation, maintenance, and operation of the Energy Components software.

The document assumes the reader has knowledge of Energy Components, MS Windows, and Oracle RDBMS management tools such as PL/SQL Developer or Toad. Therefore, descriptions are often concise rather than verbose.

What is not included in this Document?

This document doesn’t include:

Basic hardware and software installation guidelines

Guidelines for Energy Components business configuration

Versions / Applicability

The information presented here pertains to the EC 13.0.0 release of the Energy Components product.

Online Help Content

Online Help contains necessary information about the certain screen and consists of the following parts:

1. Business Function (BF) name

Business Function (or BF) name represents the screen name and a Business Function code. BF code is comprised of an abbreviation of a business module and the order number of the screen in this module.

This part of the Online Help is set by default and cannot be changed by the user.

The BF Code for each Business Function is displayed in the upper left corner of the Online Help screen. The following SQL statements may be found useful:

--Lists all the Business Functions in EC:
SELECT * FROM business_function
--Holds the Online Help Description for each BF:
SELECT * FROM bf_description
-- Holds all the images being in-line with the Online Help Description:
SELE
…[truncated]


==========================================================================================
## [21/28] PKI - Public Key Infrastructure
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/tools/pki.html
==========================================================================================
PKI - Public Key Infrastructure
Signing Process

EC screens can be configured to use signing. This means that when doing insert/update/delete the user will be required to sign the action when pressing the save button. The signing requires a certificate from a PKI provider. These certificates are located in smart cards, which are pocket-sized cards with embedded integrated circuits. When inserted into a card-reader, the chip makes contact with electrical connectors that can read information from the chip. The certificate holds information about a specific user so when a signature is performed it is a binding confirmation that the changes were made by the user owning that certificate.

Detailed Process Description

The description below uses Buypass as an example. There is also a distinction between internal and external users. External users must log in with Buypass.

Signing of Data

When data in specific screens are changed by insert, update, or delete, it will require the user to sign the data before it can be saved. This way the changed data will be stored with the signature of the user that changed it.
To sign data the user must first insert the PKI certificate, modify the data and after clicking on the save button, the window as shown in the screenshot below appears. All data that is to be signed is wrapped in a text-document in EC and will be transferred to this PKI Signature Page.

Figure 1. Accepting the containing data to be signed

The PKI signature page contains a view that shows the user that the PKI certificate is recognized. Below this view, the user can see the text-document transferred from EC containing all the data that will be signed and stored.
This information can also be viewed in a separate window by using the "Click here to open the document in a separate window".
To verify that the document is read, the user must check the checkbox and press the Continue button to accept the changes.

Figure 2. Enter certificate PIN-code to sign all changes

The window as shown in the screenshot above is the last step in the signing process where the user must enter the certificate PIN-code and press the
Confirm button. If PIN-code is accepted, the chang
…[truncated]


==========================================================================================
## [22/28] Password Encryption Tool
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/tools/password_encryption_tool.html
==========================================================================================
Password Encryption Tool

Password Encryption tool is a replacement of encrypt_pw.bat/encrypt_pw.sh for encrypting plaintext passwords. It utilizes Wildfly Elytron security module to encrypt password. The old encrypted password support is deprecated and going to be removed in future release, so it is recommended to use this Password Encryption Tool to encrypt passwords or migrate your existing passwords.

The password-encryption-tool-14.2.4.jar file can be downloaded from Energy Component Artifact Repository.

Encrypt

Run the following command to encrypt a plain-text password:

java -jar password-encryption-tool.jar -m ENCRYPT -p energy

Expected output is:

Password encrypted: RLZNLcYLvoU
Migrate

Run the tool with "MIGRATE" mode will convert existing encrypted password to new encrypted password. For example, "-66d6bf0f7ee54805" is the encrypted value of "energy" using encrypt_pw.bat script, run the following command to re-encrypt it:

java -jar password-encryption-tool.jar -m MIGRATE -p -66d6bf0f7ee54805

Expected output is:

New encrypted password: RLZNLcYLvoU


==========================================================================================
## [23/28] Blob Storage Service Implementation
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/blobstorage/blobstorage.html
==========================================================================================
Blob Storage Service Implementation

This package provides a multi-provider blob storage service that supports AWS S3, Azure Blob Storage, and Local File Storage through a plugin-based architecture using Java ServiceLoader.

Features

Multi-provider support: AWS S3, Azure Blob Storage, and Local Folder Storage

ServiceLoader-based discovery: Providers are automatically discovered and loaded

Environment-based configuration: Providers self-configure from BLOBSTORAGE_* environment variables

Extensible design: Easy to add new storage providers with @ServiceProvider annotation

Testing support: Local file storage for development and testing

Thread-safe: Concurrent access to configured provider

Exception handling: Uses checked exception BlobStorageError for all operations

Architecture
Core Components

Located in frmw-core-base:

BlobStorageProvider: Interface defining blob storage operations (uploadBlob, downloadBlob, deleteBlob)

BlobStorageMgr: Manager class that provides access to the valid provider via getService()

BlobStorageError: Checked exception for blob storage operations

DbBlobStorageProvider: Database storage implementation (priority 0) - Default fallback when no cloud provider is configured

FolderBlobStorageProvider: Local file system storage implementation (priority 80)

Located in frmw-core:

Storage Providers: Cloud storage implementations

AwsS3BlobStorageProvider: AWS S3 integration (priority 100)

AzureBlobStorageProvider: Azure Blob Storage integration (priority 90)

Class Diagram
BlobStorageProvider (interface, extends ServiceProviderInterface)
    ↑
    ├── AwsS3BlobStorageProvider (@ServiceProvider, priority 100)
    ├── AzureBlobStorageProvider (@ServiceProvider, priority 90)
    ├── FolderBlobStorageProvider (@ServiceProvider, priority 80)
    └── DbBlobStorageProvider (@ServiceProvider, priority 0) [DEFAULT FALLBACK]

BlobStorageMgr (extends ServiceManagerBase)
    └── provides: getService(), getInstance()

Each provider:
    - Reads BLOBSTORAGE_* environment variables in constructor
    - Implements isValid() to return true only if TYPE matches
    - Self-configures during construction
How It Works

Service Discovery: BlobStorageMgr 
…[truncated]


==========================================================================================
## [24/28] Data Modelling Guideline
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/databasedevelopment/data_modelling_guideline.html
==========================================================================================
Data Modelling Guideline
Introduction

The main objective of this document is to provide guidelines for the developer and data model checkers on code standards, best practices and special considerations for an EC system.

EC has a logical data model mainly represented by the class concept with key concepts like Object-, Data- and Table- classes to represent business objects, data series and configuration. Please read the class documentation for details in the class model. The rest of these guidelines is focusing on the physical table structure in the database, but there will be references to the class model. It is important to have the class concept in mind also when designing the physical data model.

General Standards and Concepts

The main approach of data modelling in EC is to create table- and relationship- structures on at least 3NF. There is however exceptions where data have been replicated for performance reasons.

The physical EC data model is semantically rich with broad table structures. Until recently the tables had a combination of named columns used by the owner, and a set of generic columns for project additions.

With the introduction of the extension concept, we are gradually phasing out the use of generic columns. Additions should be stored in separate tables linked in the class model as EXTENSION or EXT_JOIN.

Additions with mapping_type=EXTENSION are stored in a narrow table. If there are several/many attributes or relations to be added to a class, these should be gathered in one table. This table should have named columns using EXT_JOIN to link to the main class table. The reason for this recommendation is:

performance to limit the number of joins in the view/report layer.

be aligned with the wide table structure, and the semantics concepts of the existing model.

There can be several reasons why an alternative narrow table and more generic structure could be tempting to consider. But this is a different approach, and the 2 models does not necessarily mix well, so as a general rule new table structures should follow the wide and semantically rich model.

Code standards

Earlier table and column names in EC should not exceed 24 characters.
…[truncated]


==========================================================================================
## [25/28] EC Flyway Developer Handbook
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/databasedevelopment/ec_flyway_developer_handbook.html
==========================================================================================
EC Flyway Developer Handbook
Introduction

This document is intended to act as a handbook for preparation of EC database upgrade scripts in conformation with Flyway guidelines.

Pre-requisites

Ensure that the following pre-requisites are in place before starting off with the development process:

Standard EC development environment.

Docker installation

Maven (standard EC version)

Flyway version supported by the EC release. (As of 13.1.0, it is v6.4.3) - through pom dependency.

You are introduced to the concepts of developing migration scripts using Flyway.

It is recommended to refer to Flyway in Energy Components for additional reference information on using flyway in the EC development space.

Repository Structure

New project has been created inside ec-application repository called database to include Flyway related DB script.

The Flyway common utility and callbacks are placed in the "ec-application" repository under sub-project *"database/ec-db-tools". *

Product flyway migrations are placed in the "ec-application" repository under the sub-project "*database/ec-db". *

Similarly product flyway test data migration scripts are placed in the "ec-application" repository under the sub-project "database/ec-db-testdata".

Refer to the folder naming convention for further information.

EC Standard Core Product is represented by folder owner_context_0

EC Test Data is represented by folder owner_context_800

For EC Extensions / Packages, the migrations are based out of their respective repository.

For e.g.

The RR PRODCA Package is represented by folder owner_context_rr-prodca_400 and so on.

Migration scripts per release will then be placed in a folder named with the same name as EC Release.

For e.g.

ec-db/src/main/resources/db/migration/owner_context_0/*12.2.0*

ec-db/src/main/resources/db/migration/owner_context_0/common

ec-db-testdata/src/resources/db/migration/owner_context_800/*12.2.0*

ec-db-testdata/src/resources/db/migration/owner_context_800/common

and so on..

Getting Started with Migrations

Check-out code from the specific release branch of "ec-application" Bitbucket repository to your local system.

Pull the appropriate docker image from nexu
…[truncated]


==========================================================================================
## [26/28] PL/SQL - Coding Standard And Style
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/databasedevelopment/pl_sql_coding_standard_and_style.html
==========================================================================================
PL/SQL - Coding Standard And Style
Introduction

This document is based on an original document from ECPEDIA and it describes the coding standard and best practices of PL/SQL source code in EC. Additional tags were added to identify coding standards that were created/changed by the Australia team as well as customer specific standards.

Each item is marked with a unique ID. IDs can be grouped into the following groups:

CS1-54 Level 1. The associated rules are mandatory. All code must implement rules in this group.

CS2-16 Level 2. The associated rules are strongly recommended. Code should implement rules in this group, in other words, implementation is optional.

CS3-2 Level 3. The associated rules are recommended. It is suggested to implement the rules when possible.

CSPRJ-00 Australia  and Malaysia Team Specific. The associated rules are mandatory and apply to projects implemented by the Australian and Malaysian offices.

Source File

CS1-1 All files should be put in database module. The database module is named [product_name].ds.database .

CS1-2 One object per file.^ ^A database source file contains only one object declaration, except for data model files (files under datamodel folder).

CS1-3 Name file after its content. For source files that contain single database object declaration (views, types, triggers), the file name should be the same as its enclosing object name, suffix could be used when a declaration is separated into multiple files.

CS3-1 Put header and body in two files when possible.

The original idea of separating body and head into two files is to avoid deploy errors when circular references happen. However, circular reference is not supposed to exist, the suggestion here still supports separating the two parts is for better code organization. Being in two files, it is easier to know if a change would affect other database objects (when header changes, it usually requires changes in all references), plus, it would reduce the length of source code files. The suggested naming convention is:

Use extension “.pks” for head files

Use extension “.pkb” for body files

CS1-4 Use correct file extension.

File Content	Extension	Folder


Data Mode
…[truncated]


==========================================================================================
## [27/28] Custom Oracle Error Messages
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/databasedevelopment/custom_oracle_error_messages.html
==========================================================================================
Custom Oracle Error Messages

Oracle provides the raise_application_error procedure to allow you to raise custom error numbers within your PL/SQL code. You can generate errors and their associated text starting with -20000 and proceeding through -20999.

Example:

RAISE_APPLICATION_ERROR(-20128,'Daytime is less than owner object start date.');

The Oracle error message can be translated using language translation in EC. The Oracle error number (e.g. ORA-20128) is used for finding the translated message.

To expand the range of Oracle custom error number, a postfix can be added to the start of the Oracle error message text. EC will then use the Oracle error number + the postfix to find the translated message. The postfix is specified as the first part of the Oracle error message text. The first character must be # and it ends with |.

Example:

RAISE_APPLICATION_ERROR(-20128,'#EXT01|Data values must be between 0 and 100.');

ORA-20128#EXT01 is used for finding the translated message.

Customers are advised to use a postfix (e.g. the extension ID) for custom Oracle error messages. It will then not conflict with EC’s custom Oracle error messages.

For more information about language translation, see How to configure language translation in EC


==========================================================================================
## [28/28] Flyway in Energy Components
URL: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/flyway/flyway.html
==========================================================================================
Flyway in Energy Components
Introduction

Flyway is an Apache open-source version control tool for databases. It is based around seven basic commands:

Name	Description


baseline

	

Baselines an existing database, excluding all migrations up to and including baselineVersion




clean

	

Drops all objects in the configured schemas




info

	

Prints the details and status information about all the migrations




migrate

	

Running the Upgrade / Migration




repair

	

Repairs the schema history table




validate

	

Validates the applied migrations against the ones available on the classpath

With Flyway, all changes to the database are called migrations. Energy Components (EC) uses Flyway to apply migrations to the database, and to keep track of them. This is done in three ways:

Deploying a new ec-application.ear file, EC automatically checks for any pending migrations and applies them.

Installing an extension. For more information about this, see Extension migration.

Using the Flyway tool to execute one of the seven available basic commands manually.

For a simple guide on how it works, take a look at How Flyway works

Flyway uses placeholder. Placeholder is specified by using ${<place holder name>}. If migration scripts contain ${…​..} that is not a placeholder, it needs to be split like this:

'.... $'||'{ ....} ...'
Flyway Migrations

Migrations can be either versioned or repeatable. Versioned migrations have a version, a description and a checksum. The version must be unique. They are applied in order exactly once. These are identified by the prefix V in the file name.

Repeatable migrations have a description and a checksum, but no version. Instead of being run just once, they are (re-)applied every time their checksum changes. Repeatable migrations are applied in the order of their description and only after the migration of all versioned scripts. These are identified by the prefix R in the file name.

Execution order

The sequence of execution for Flyway migrations would be:

First pre-upgrade scripts are run. The scripts perform some checks and update the ASSIGN_ID table.

Next, all Versioned migrations will be invoked in ascending order based
…[truncated]