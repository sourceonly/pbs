# pas-appmaker/docs/installation

A framework for creating powerful application definitions.

## Introduction

This document is for administrators who are deploying pas-appmaker in their environment for the first time.
If you are an application author and would like to create applications with pas-appmaker, please read the pas-appmaker/docs/tutorials document to learn how.

### Required: App Home

The application home/ directory is where your application definitions will be placed at creation time. 

    export PAS_APP_HOME=/var/spool/pas/repository/applications
    
or
    
    pas-appmaker Appname --app-home /path/to/pas/repository/applications


### Required: App Config

The application config/ directory is where your pas-appmaker base and template files are located.

    export PAS_APP_CONFIG=/var/spool/pas/repository/pas-appmaker/config
    
or
    
    pas-appmaker Appname --app-config /path/to/pas-appmaker/config 


### Optional: postsubmit.py

pas-appmaker has an extension to the PAS presubmit.py hook called postsubmit.py. postsubmit.py was created
to bridge the gaps between the PBS job object available to presubmit.py, and the job object available to queuejob hooks in PBS.
Because of this, postsubmit.py allows pas-appmaker functionality never before possible with typical application definitions.

    qmgr -c "create hook postsubmit"
    qmgr -c "set hook postsubmit type = site"
    qmgr -c "set hook postsubmit enabled = true"
    qmgr -c "set hook postsubmit event = queuejob"

    qmgr -c "import hook postsubmit application/x-python default /path/to/app/config/base/postsubmit.py"

or
    qmgr -c "import hook postsubmit application/x-python default /path/to/app/config/template/postsubmit.py"
    
### Recomended: App Environment

Make these adjustments to have CM and PAS refresh your applications every minute.
Additionally you can configure the authors environment, too.

#### Compute Manager (12.0.1 and below)

Check PAS for updated applications every minute.

    vim /opt/altair/pbsworks/12.0/services/cm/config/spring-config.xml

    <bean id="updateAppTrigger" class="org.springframework.scheduling.quartz.CronTriggerBean">
        <property name="jobDetail">
            <ref bean="updateAppBean" />
        </property>
        <property name="cronExpression">
            <value>0 * * * * ?</value>
        </property>
    </bean>

#### PBS Application Services

Remove the time_stamp.txt file every minute.

    vim /etc/cron.d/pas-timestamp-remove

    * * * * * root rm -rf /var/spool/pas/repository/time_stamp.txt

#### Author Environment

Automatic environment setup on login.

    vim /etc/profile.d/pas-appmaker-environment.sh 

    export PAS_APP_HOME=/var/spool/pas/repository/applications/
    export PAS_APP_CONFIG=/var/spool/pas/repository/pas-appmaker/config/
    export PATH=$PATH:/var/spool/pas/repository/pas-appmaker/

### Optional: Download Nightly Builds

You can download and deploy daily pas-appmaker updates from the Altair ftp.

    vim /etc/cron.daily/pas-appmaker-update
    
    #!/bin/sh
    
    cd /var/spool/pas/repository
    wget ftp://ftp.altair.com/pub/outgoing/pas-appmaker/pas-appmaker-`date +%F`.tar.gz
    tar -xvf pas-appmaker-`date +%F`.tar.gz
    
## Copyright

(c) Copyright 2013 - 2014 Altair Engineering, Inc. All rights reserved.
