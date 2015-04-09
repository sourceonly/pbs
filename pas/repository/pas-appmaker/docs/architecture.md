# pas-appmaker/docs/architecture

A framework for creating powerful application definitions.

### Application Creation
The pas-appmaker command line tool can be used to create a base application definition.  Once the application definition is created its functionality can then be extended using hooks, templates, and enviroment variables.

The only command argument required by the pas-appmaker command is the name of the application.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_pas-appmaker [OPTION]... [APPNAME]_  

If you create the simplest application the following files will be created in the /var/spool/pas/repository/applications directory:   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_pas-appmaker MyApp_  

    total 24
    -rw-r--r-- 1 root root  276 May 30 07:41 app-actions-MyApp.xml
    -rw-r--r-- 1 root root  888 May 30 07:41 app-conv-MyApp.xml
    -rw-r--r-- 1 root root 1360 May 30 07:41 app-inp-MyApp.xml
    -rw-r--r-- 1 root root 1024 May 30 07:41 app-summary-MyApp.log
    drwxr-xr-x 2 root root 4096 May 30 07:41 runtime
    drwxr-xr-x 2 root root 4096 May 30 07:41 submittime
    
     ./runtime:
    total 32
    -rwxr-xr-x 1 root root  5816 May 30 07:41 actions.py
    -rwxr-xr-x 1 root root  5020 May 30 07:41 exit.py
    -rw-r--r-- 1 root root 14949 May 30 07:41 start.py

    ./submittime:
    total 24
    -rwxr-xr-x 1 root root   223 May 30 07:41 input.py
    -rwxr-xr-x 1 root root  2137 May 30 07:41 postsubmit.py
    -rwxr-xr-x 1 root root 13890 May 30 07:41 presubmit.py

###Files in the Application Directory
* app-actions-AppName.xml ------- appplication action file
* app-conv-AppName.xml ---------- application converter file
* app-inp-AppName.xml ------------ application input file
* app-summary-AppName.log ---- application build summary log file  

####Application Input File
The application input file is where arguments are defined for a given application.  You can edit this file to add application arguments, remove application arguments, or tune existing arguments per site nomenclature.  
***Warning:***   
Changing the value of the **&lt;Name&gt;** XML element of any of the pas-appmaker base arguments may have adverse effects on your application definition.  Modifications of this kind should only be done by advanced application definition authors. 

####Application Converter File
The application converter file takes the values of the application arguments defined in the application input file and communicates this information to PBS Application Services.  This file allows the job submission environment to be configured.  
***Warning:***   
Changing the value of the **&lt;jsdl:FileName&gt;** XML element of any of the pas-appmaker base filename arguments may have adverse effects on your application definition.  Modifications of this kind should only be done by advanced application definition authors. 
####Application Action File
The application action file defines the arguments, applicable job state, and executable for an application action.  An application action allows some type of action to be performed on a application.  For instance, sending a signal to an application to terminate.
####Application Build Summary Log File
Log file that summarizes the arguments, files, actions, and hooks that were enabled for the application definition.

###Files in the Runtime Directory
* actions.py ---- appplication action runtime script
* exit.py --------- application exit script
* start.py -------- application runtime script

***Warning:***  
The base pas-appmaker scripts found in the runtime directory should NOT be modified by application definition authors.  Use hooks or environment variables to extend their functionality.

####Application Action Runtime Script
Python script that performs the application action.

####Application Exit Script
Python script that performs any actions that should occur when an application reaches the exit phase.

####Application Runtime Script
Python script file which is the primary execution script.  This script file is responsible for executing the application using the information entered by the user (defined by the application input file), and converted (via the application converter file).

###Files in the Submittime Directory
* input.py ------------- application input script
* postsubmit.py ----- application post-submit script
* presubmit.py ------ application pre-submit script
 
####Application Input Script
Python script that performs any actions that should occur when an application reaches the input phase.

####Application Pre-Submit Script
Python script that performs any actions that should occur when an application reaches the pre-submit phase.

####Application Post-Submit Script
Python script that performs any actions that should occur when an application reaches the post-submit phase.

### Application Lifecycle

##Life Cycle of an Application
There are two main application phases that are divided into sub-phases:
* Submittime
  - Input
  - Submit
* Runtime
  - Start
  - Actions
  - Exit

###Input phase
The input phase begins when a user displays a job submission form in Computer Manager and enter arguments for the application.  It ends when the _Submit_ button is clicked.  

The information contained in the application input file is used during the input phase to communicate the available application arguments to CM.

###Submit phase
The submit phase begins when a user clicks the _Submit_ button.  It ends when the job is received by PBS Professional and placed into a queue.

The submit phase processes and validates the arguments entered for the application.  It verifies the existence of and permissions of job files.  It constructs the job attributes and job resource request.

It then creates an application object containing all the information necessary to execute the application.

####Application environment variables
Any arguments supplied during the input phase will be saved as environment variables.  These environment variables are persisted throughout each phase of the application life cycle.  The naming convention for these environment variables is PAS_ARGNAME where ARGNAME is the name of the application argument as defined by the XML element **&lt;NAME&gt;** in the application input file. 
####Script Files Responsible for Submit Phase Activities
presubmit.py ------ resource and attribute processing  
postsubmit.py ---- bridges the gap for features that are not supported by PAS using a qsub hook.

###Start phase
The start phase begins when the job reaches a running state.

The start phase is responsible for starting the application.

####Script Files Responsible for Start Phase Activities
start.py ------ starts execution of the application  

###Actions phase
The actions phase is initiated by the user when an application action is requested using Compute Manager.  

The actions phase is responsible for starting and executing the application action.  

####Script Files Responsible for Action Phase Activities
actions.py ------ executes the application action  

###Exit phase
The exit phase begins when the job completes.

It is responsible for any application post-processing and clean-up, for instance, compressing all job results files.

####Script Files Responsible for Exit Phase Activities
exit.py ------ performs any necessary post-processing  

###Environment Files
Application definition authors can extend the functionality of an application definition by implementing environment files.  

An environment file contains key-value pairs in the format:

&lt;ENV_VAR_NAME&gt;=&lt;VALUE&gt;  

Where &lt;ENV_VAR_NAME&gt; is the name of an environment variable and &lt;VALUE&gt; is its value.

Each phase has its own environment file, except for the input phase.  The naming convention for environment files is _phaseName.environment_:  
* submit.environment ---- place file in submittime directory of application definition  
* start.environment ------- place file in runtime directory of application definition
* action.environment ----- place file in runtime directory of application definition
file
* exit.environment -------- place file in runtime directory of application definition

When an application phase begins, the environment file will be read, and any environment variables contained in the file will be processed and added to the application's environment.  Authors can add environment variables and override existing environment variables in this way. 

####How Are Environment Variables Processed
If the environment variable is already defined in the application's environment, then its value will be overlaid. Otherwise, the variable will be added to the application's environment. Any environment variables prefixed with "PAS_" will persist to the subsequent application phase. Otherwise, the environment variable will only exist during the application's phase.

As long as an environment file exists, is located in the correct application definition directory, and the application has permission to read it, then the environment file will be processed.

####Environment File Example  
This is an example of a start.environment file:

    PAS_EXECUTABLE=/bin/sleep
    PAS_ARGUMENTS=30 

####Environment Variable Substitution
Substitution of environment variable values is supported within an environment file.  In the example below, the environment variable for the number of graphical CPUs will be set to the value of the number of CPUs.
    
    PAS_NGPUS=PAS_NCPUS

You can also use the --phasename-environment=&lt;var&gt;=&lt;valueE&gt;,&lt;var&gt;=&lt;value&gt; command line option to define phase environment variables.

###Hooks
Application definition authors can extend the functionality of an application definition by using hooks.  

An hook is a script written in any language.  You can use the hook to manipulate the application object to set up the environment specific to your site's needs.

Each phase has its own hook, except for the input phase.  The naming convention for hook files is _phaseName.hook_:  
* submit.hook ---- place hook in submittime directory of application definition  
* start.hook ------- place hook in runtime directory of application definition 
* action.hook ----- place hook in runtime directory of application definition  
* exit.hook -------- place hook in runtime directory of application definition

When an application phase begins, the environment file will be processed first.  Once the environment is in place, then the phase hook will be executed.

As long as a hook file exists, is located in the correct application definition directory, is executable, and the application has permissions to run it, then the hook will be executed.

You can also use the --phasename-hook /path/to/my/hook.pl command line option to tell pas-appmaker the location of your hook.

###Templates  

Pre-defined template files can be used to override or add to base appmaker behavior.  This is especially powerful for administrators wanting to apply common or application specific input arguments, hooks or environment files.

####Template Directory
The template directory is _/var/spool/pas/repository/pas-appmaker/config/templates_.

####Template Use Case
For instance, to change the **&lt;Input_Required&gt;** of XML element **&lt;NCPUS&gt;** for all your site's applications from the default of "true" to "false", you could edit every application input file and change the value of **&lt;Input_Required&gt;** to "false".

    <ArgumentChoice>
        <ArgumentIntEnumerated>
            <Name>NCPUS</Name>
            <Description>The total number of processors.</Description>
            <DisplayName>Number of Processors</DisplayName>
            <InputRequired>true</InputRequired>                 ---Change true to false
            <Option default="true">2</Option>
            <Option>4</Option>
            <Option>6</Option>
            <Option>8</Option>
            <Option>10</Option>
            <Option>12</Option>
        </ArgumentIntEnumerated>
    </ArgumentChoice>

Or you could use a template to override the base application argument.

####Global Input Template

Create a file called _app-inp.xml_ and place the following XML in the file - notice that the XML sets **&lt;Input_Required&gt;** to "false" :

    <ArgumentChoice>
        <ArgumentIntEnumerated>
            <Name>NCPUS</Name>
            <Description>The total number of processors.</Description>
            <DisplayName>Number of Processors</DisplayName>
            <InputRequired>false</InputRequired>                  
            <Option default="true">2</Option>
            <Option>4</Option>
            <Option>6</Option>
            <Option>8</Option>
            <Option>10</Option>
            <Option>12</Option>
        </ArgumentIntEnumerated>
    </ArgumentChoice>

Place the _app-inp.xml_ file in the template directory.  This will append the custom argument to the end of all appmaker generated argument input files, and appmaker will override the base input argument.

You can also use templates to add new input arguments to appmaker.

####Application Specific Input Template
If you would like to append only a specific application's arguments, create a file called _app-inp-appname.xml_ and place it in the template directory.  This will append application specific arguments to the end of any appmaker generated application definition that match the correct application name.

####Global Converter Template
Similarly, you can also append data staging directives to the end of all appmaker generated input converter files using the file _app-conv.xml_ and placing it in the template directory.

    <jsdl:DataStaging>    
        <jsdl:FileName>name($STAGE_SOMETHING)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>

        <jsdl:Source>
              <jsdl:URI>$STAGE_SOMETHING</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>


####Application Specific Converter Template
If you would like to append only a specific application's data staging directives, create a file called _app-conv-appname.xml_ and place it in the template directory.  This will append application specific directives to the end of any appmaker generated application definition that match the correct application name.

#### The following templates are supported.
Templates can be used for input arguments, data staging directives, hooks, application actions, and environment files.

Input Files

    app-inp.xml
    app-inp-appname.xml
    app-conv.xml
    app-conv-appname.xml
    app-actions.xml
    app-actions-appname.xml
    input.hook
    input.environment

Submit Files

    submit.hook
    submit.environment

Start Files

    start.hook
    start.environment
    
Actions Files

    app-actions.xml
    app-actions-appname.xml
    actions.hook
    actions.environment
    
Exit Files

    exit.hook
    exit.environment



## Copyright

© Copyright 2013 - 2014 Altair Engineering, Inc. All rights reserved.
