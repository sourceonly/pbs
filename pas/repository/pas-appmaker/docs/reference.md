# pas-appmaker/docs/reference

A framework for creating powerful application definitions.

## Introduction

This document will serve as a reference for pas-appmaker authors who wish to know more about some of the special behaviors of pas-appmaker.

## Configuration Options

The following pas-appmaker command options are available for getting command help, setting up the pas-app environment, and changing application files permissions and ownership.

### --app-home

This command option sets the application's home directory. Alternatively, you can set this option in your environment using the UNIX export command:

    export PAS_APP_HOME=/var/spool/pas/repository/applications

#### Example
    
    pas-appmaker MyApp --app-home /var/spool/pas/repository/applications  


### --app-config

This command option sets the application's configuration directory. Alternatively, this option can be set in your environment using the UNIX export command:

    export PAS_APP_CONFIG=/var/spool/pas/repository/pas-appmaker/config

#### Examples

    pas-appmaker MyApp --app-config /var/spool/pas/repository/pas-appmaker/config/  

### --app-chmod

This command option changes the permissions of all application files. It is similiar to the UNIX chmod command:
    
    chmod -R <permissions> /var/spool/pas/repository/applications/MyApp

#### Examples

    pas-appmaker MyApp --app-chmod 0755

### --app-chown

This command option changes the ownership of all application files. It is similar to issuing the command:
    
    chown -R <owner:group> /var/spool/pas/repository/applications/MyApp

#### Examples

    pas-appmaker MyApp --app-chown 50005:100

or

    pas-appmaker MyApp --app-chown `id -u username`:`id -g groupname`
    
## Resource Options

The following pas-appmaker command options are available for presenting application arguments that can be used for requesting job resources.  

### --resources

This command option creates an applicationargument that allows job resources to be requested at job submission time.

#### Examples  

    pas-appmaker MyApp --resources  

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>RESOURCES</Name>
            <Description>Specify your -l resource requests here.</Description>
            <DisplayName>Resources</DisplayName>
            <InputRequired>true</InputRequired>
            <Value>software=Appname select=1:ncpus=1:mem=100mb</Value>
        <ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --resources behind the scenes in the Submit Phase of your application. This will not generate any XML, and as such, will not expose this option to any submitting users.

    pas-appmaker MyApp --submit-environment PAS_RESOURCES='software=MyApp select=1:ncpus=1'
    
### --select

This command option creates an application argument that allows chunks to be requested at job submission time.

#### Examples

    pas-appmaker MyApp --select

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentInt>
            <Name>SELECT</Name>
            <Description>The number of chunks (nodes)</Description>
            <DisplayName>Select (Nodes/Chunks)</DisplayName>
            <InputRequired>true</InputRequired>
            <LowerBound>1</LowerBound>
            <UpperBound>256</UpperBound>
            <Value>1</Value>
        </ArgumentInt>
    </ArgumentChoice>

Alternatively, you can set a value to --select behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_SELECT=1

### --ncpus

This command option presents an application argument that allows the number of CPUs to be requested at job submission time.

#### Examples

    pas-appmaker MyApp --ncpus  

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentIntEnumerated>
            <Name>NCPUS</Name>
            <Description>The total number of processors.</Description>
            <DisplayName>Number of Processors</DisplayName>
            <InputRequired>true</InputRequired>
            <Option default="true">2</Option>
            <Option>4</Option>
            <Option>6</Option>
            <Option>8</Option>
            <Option>10</Option>
            <Option>12</Option>
        </ArgumentIntEnumerated>
    </ArgumentChoice>

Alternatively, you can set a value to --ncpus behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_NCPUS=2
    
### --ngpus   

This command option generates an application argument that allows the number of graphical CPUs to be requested at job submission time.

#### Examples

    pas-appmaker MyApp --ngpus  

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentIntEnumerated>
          <Name>NGPUS</Name>
          <Description>The total number of graphical processors.</Description>
          <DisplayName>Number of Graphical Processors</DisplayName>
          <InputRequired>true</InputRequired>
          <Option default="true">2</Option>
          <Option>4</Option>
          <Option>6</Option>
          <Option>8</Option>
          <Option>10</Option>
          <Option>12</Option>
        </ArgumentIntEnumerated>
    </ArgumentChoice>

Alternatively, you can set a value to --ngpus behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_NGPUS=1

### --mpiprocs

This command option creates an application argument that allows the number of MPI processes per chunk to be requested at job submission time.

#### Examples  
    
    pas-appmaker MyApp --mpiprocs

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentIntEnumerated>
          <Name>MPIPROCS</Name>
          <Description>The total number of parallel processes.</Description>
          <DisplayName>MPI Processors</DisplayName>
          <InputRequired>true</InputRequired>
          <Option default="true">2</Option>
          <Option>4</Option>
          <Option>6</Option>
          <Option>8</Option>
          <Option>10</Option>
          <Option>12</Option>
        </ArgumentIntEnumerated>
    </ArgumentChoice>

Alternatively, you can set a value to --mpiprocs behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_MPIPROCS=2

### --ompthreads

This command option creates an application argument that allows the number of OpenMP threads for this chunk to be requested at job submission time.

### Examples

    pas-appmaker MyApp --ompthreads

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentIntEnumerated>
            <Name>OMPTHREADS</Name>
            <Description>The total number of parallel processes.</Description>
            <DisplayName>OMP Threads</DisplayName>
            <InputRequired>true</InputRequired>
            <Option default="true">2</Option>
            <Option>4</Option>
            <Option>6</Option>
            <Option>8</Option>
            <Option>10</Option>
            <Option>12</Option>
        </ArgumentIntEnumerated>
    </ArgumentChoice>

Alternatively, you can set a value to --mpiprocs behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_OMPTHREADS=4

### --mem

This command option creates an application argument that allows the amount of physical memory per chunk to be requested at job submission time.

#### Examples

    pas-appmaker MyApp --mem

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>MEM</Name>
            <Description>The physical memory to request. You will need to specify the unit type.</Description>
            <DisplayName>Physical Memory</DisplayName>
            <InputRequired>true</InputRequired>
            <Value>1gb</Value>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --mem behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_MEM=16gb

### --vmem

This command option creates an application argument that allows the amount of virtual memory per chunk to be requested at job submission time.

#### Examples

    pas-appmaker MyApp --vmem

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>VMEM</Name>
            <Description>The virtual memory to use. You will need to specify the unit type.</Description>
            <DisplayName>Virtual Memory</DisplayName>
            <InputRequired>true</InputRequired>
            <Value>100mb</Value>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --vmem behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_VMEM=4gb

### --walltime

This command option creates an application argument that allows the walltime to be requested at job submission time.

#### Examples

    pas-appmaker MyApp --walltime

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>WALLTIME</Name>
            <Description>The desired walltime (length) of the job duration.</Description>
            <DisplayName>Walltime</DisplayName>
            <InputRequired>false</InputRequired>
            <Value>01:00:00</Value>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --arch behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_WALLTIME=01:00:00

### --arch

This command option creates an application argument that allows the system architecture to be requested at job submission time.

#### Examples

    pas-appmaker MyApp --arch

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>ARCH</Name>
            <Description>Specify which system architecture to run your job on.</Description>
            <DisplayName>Architecture</DisplayName>
            <InputRequired>false</InputRequired>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --arch behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_ARCH=linux

### --vnode

This command option creates an application argument that allows the virtual node to be requested at job submission time.

#### Examples

    pas-appmaker MyApp --vnode

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>VNODE</Name>
            <Description>Specify which vnode you would like to run this job on.</Description>
            <DisplayName>VNode</DisplayName>
            <InputRequired>false</InputRequired>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --arch behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_VNODE=hostname
    
### --place

This command option creates an application argument that allows the placement of each chunk to be requested at job submission time.

#### Examples

    pas-appmaker MyApp --place

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentStringEnumerated>
            <Name>PLACE</Name>
            <Description>The placement of job resources.</Description>
            <DisplayName>Placement of Resources</DisplayName>
            <InputRequired>false</InputRequired>
            <Option default="true">pack</Option>
            <Option>free</Option>
            <Option>scatter</Option>
            <Option>shared</Option>
        </ArgumentStringEnumerated>
    </ArgumentChoice>

Alternatively, you can set a value to --arch behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_PLACE=skatter

## Attribute Options

The following pas-appmaker command options are available for creating application arguments that can be used for specifying job attributes.  

### --attributes

This command option creates an application argument that allows job attributes or characteristics to be set.

#### Examples

    pas-appmaker MyApp --attributes  

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>ATTRIBUTES</Name>
            <Description>Automatically include any of these ':' separated list of key/value attribute pairs.</Description>
            <DisplayName>Attributes</DisplayName>
            <InputRequired>true</InputRequired>
            <Value>group_list=user@hostname</Value>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --attributes behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_ATTRIBUTES=group_list=user@hostname
    
### --depend

This command option creates an application argument that allows job dependencies to be specified.

#### Examples

    pas-appmaker MyApp --depend  

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>DEPEND</Name>
            <Description>Specify which job ID this job will depend on and how.</Description>
            <DisplayName>Dependancy</DisplayName>
            <InputRequired>true</InputRequired>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --depend behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_DEPEND=

### --group-list

This command option creates an application argument that specifies the groups under which the job will run.

#### Example

    pas-appmaker MyApp --group-list

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>GROUP_LIST</Name>
            <Description>Automatically include any of these ',' separted list of groups to run under this job.</Description>
            <DisplayName>Group List</DisplayName>
            <InputRequired>true</InputRequired>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --group-list behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_GROUP_LIST=group1,group2,group3

### --account

This command option creates an application argument that specifies the account under which the job will run.

#### Examples

    pas-appmaker MyApp --account

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.
  
    <ArgumentChoice>
        <ArgumentString>
            <Name>ACCOUNT</Name>
            <Description>Specify the name of an account to associate with this job.</Description>
            <DisplayName>Account</DisplayName>
            <InputRequired>true</InputRequired>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --account behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_ACCOUNT=account_name

### --project

This command option creates an application argument that assigns a project to the job at job submission time.

#### Examples

    pas-appmaker MyApp --project

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>PROJECT</Name>
            <Description>Specify the name to associate with this job.</Description>
            <DisplayName>Project</DisplayName>
            <InputRequired>true</InputRequired>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --project behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_PROJECT=project_name

### --queue

This command option creates an application argument that specifies the queue to which the job will be submitted.

#### Examples

    pas-appmaker MyApp --queue

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentStringEnumerated>
            <Name>QUEUE</Name>
            <Description>Specify your desired queue.</Description>
            <DisplayName>Queue</DisplayName>
            <InputRequired>false</InputRequired>
            <Option>workq</Option>
        </ArgumentStringEnumerated>
    </ArgumentChoice>

Alternatively, you can set a value to --queue behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment PAS_QUEUE=workq

### --mail

This command option creates two application arguments:  
1. The first application argument allows the recipients of the mail to be defined.  
2. The second application argument is list that determines when the email should be sent:  
    * No mail is sent.  
    * Mail sent at the beginning of the job.  
    * Mail sent at the end of the job.  
    * Mail sent when the job aborts.    

#### Examples

    pas-appmaker MyApp --mail

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentStringMulti>
            <Name>MAIL_EMAILS</Name>
            <Description>A ';' separated list of email addresses to send notifications to. Example: sam@altair.com;bill@altair.com</Description>
            <DisplayName>Email Notifications</DisplayName>
            <InputRequired>true</InputRequired>
        </ArgumentStringMulti>
    </ArgumentChoice>
    <ArgumentChoice>
        <ArgumentStringEnumerated>
            <Name>MAIL_OPTIONS</Name>
            <Description>Select when you would like to be notified of job activity. Either 'a' if the job has aborted, 'b' for before the job starts or 'e' when the job exits. Example: 'abe'.</Description>
            <DisplayName>Notification Options</DisplayName>
            <InputRequired>true</InputRequired>
            <Option default="true">No mail is sent</Option>
            <Option>Mail sent at beginning of job</Option>
            <Option>Mail sent at end of job</Option>
            <Option>Mail sent on job abort</Option>
        </ArgumentStringEnumerated>
    </ArgumentChoice>

Alternatively, you can set a value to --queue behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example. 

    pas-appmaker MyApp --submit-environment "PAS_MAIL_EMAILS=user@domain.com,PAS_MAIL_OPTIONS=abe"

### --job-arrays

This option allows a job array to be created.  Three application arguments allow the user to specify the start, end and index of the array and a stepping factor.

#### Examples

    pas-appmaker MyApp --job-arrays

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentInt>
            <Name>JOB_ARRAY_START_INDEX</Name>
            <Description>The start index of a job array.</Description>
            <DisplayName>Job Array Start Index</DisplayName>
            <InputRequired>false</InputRequired>
            <LowerBound>0</LowerBound>
            <Value>0</Value>
        </ArgumentInt>
    </ArgumentChoice>
    <ArgumentChoice>
        <ArgumentInt>
            <Name>JOB_ARRAY_END_INDEX</Name>
            <Description>The end index of a job array.</Description>
            <DisplayName>Job Array End Index</DisplayName>
            <InputRequired>false</InputRequired>
            <LowerBound>1</LowerBound>
            <Value>1</Value>
        </ArgumentInt>
    </ArgumentChoice>
    <ArgumentChoice>
        <ArgumentInt>
            <Name>JOB_ARRAY_STEPPING_FACTOR</Name>
            <Description>The stepping factor of job array.</Description>
            <DisplayName>Job Array Stepping Factor</DisplayName>
            <InputRequired>false</InputRequired>
            <LowerBound>1</LowerBound>
            <Value>1</Value>
        </ArgumentInt>
    </ArgumentChoice>

## Execution Options

The following pas-appmaker command options are available for setting aspects of the application specific to the executable, its arguments, and other related "Solver" specific options.

### --software

This command option creates an application argument which allows you to specify the name of the software associated with the application being created.

#### Examples  
    
    pas-appmaker MyApp --software

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>SOFTWARE</Name>
            <Description>The name of your application.</Description>
            <DisplayName>Software</DisplayName>
            <InputRequired>false</InputRequired>
            <Value>AppMaker</Value>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --software behind the scenes in the Submit Phase of your application. This will not expose the option to a submitting user as in the above example.

    pas-appmaker MyApp --submit-environment PAS_SOFTWARE=SolverName

### --environment

This command option creates an application argument that allows environment variables to be exported to the job.

#### Examples
    
    pas-appmaker MyApp --environment

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentStringMulti>
            <Name>ENVIRONMENT</Name>
            <Description>A ';' separated list of environment variables to make available to the AppMaker job.</Description>
            <DisplayName>AppMaker Environment</DisplayName>
            <InputRequired>false</InputRequired>
        </ArgumentStringMulti>
    </ArgumentChoice>
 
Alternatively, you can set a value to --environment behind the scenes in the Start Phase of your application. This will not expose the option to a submitting user as in the above example.

    pas-appmaker MyApp --start-environment PAS_ENVIRONMENT=VAR_1=foo,VAR_2=bar,VAR_3=baz

### --executable

This command option creates an application argument that allows an executable to be specified for job execution.

#### Examples

    pas-appmaker MyApp --executable

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentString>
            <Name>EXECUTABLE</Name>
            <Description>A remote executable to run instead of a user supplied job script.</Description>
            <DisplayName>Executable</DisplayName>
            <InputRequired>true</InputRequired>
            <Value></Value>
        </ArgumentString>
    </ArgumentChoice>

Alternatively, you can set a value to --executable behind the scenes in the Start Phase of your application. This will not expose the option to a submitting user as in the above example.

    pas-appmaker MyApp --start-environment PAS_EXECUTABLE=/path/to/executable
    
### --script

This command option creates an application argument that specifies a specific job script to execute at run time.

#### Examples

    pas-appmaker MyApp --script

This option will create the appropriate XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-inp.xml`.

    <ArgumentChoice>
        <ArgumentFileName>
            <Name>SCRIPT</Name>
            <Description>A job script to run instead of a remote executable.</Description>
            <DisplayName>Job Script</DisplayName>
            <InputRequired>false</InputRequired>
        </ArgumentFileName>
    </ArgumentChoice>

It will also create the appropriate data staging XML required for your application definition. It will create XML output similiar to what you see below within `$PAS_APP_HOME/MyApp/app-MyApp-conv.xml`.

    <jsdl:DataStaging>
        <jsdl:FileName>name($SCRIPT)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>
        <jsdl:Source>
            <jsdl:URI>$SCRIPT</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>

Alternatively, you can set a value to --script behind the scenes in the Start Phase of your application. This will not expose the option to a submitting user as in the above example.

    pas-appmaker MyApp --start-environment PAS_SCRIPT=/path/to/script
    
### --arguments

This command option creates an application argument that allows arguments to be passed to an executable or script.

**Command example:**  pas-appmaker MyApp --arguments

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentString>
            <Name>ARGUMENTS</Name>
            <Description>Pass specific arguments to the job script or remote executable.</Description>
            <DisplayName>Arguments</DisplayName>
            <InputRequired>true</InputRequired>
            <Value></Value>
        </ArgumentString>
    </ArgumentChoice>

When the application job submission form is viewed using Compute Manager, a string argument called **Arguments** will be available. This argument can be used to pass arguments to an executable.

### --run-parallel

This command option creates an application argument that allows the user to choose to run the executable or script in parallel across all nodes.     

**Command example:**  pas-appmaker MyApp b-run-parallel

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentBooleanWithDescription>
            <Name>RUN_PARALLEL</Name>
            <Description>Run your Executable and Script in parallel across all nodes.</Description>
            <DisplayName>Run Parallel</DisplayName>
            <FeatureEnabled>true</FeatureEnabled>
            <InputRequired>true</InputRequired>
        </ArgumentBooleanWithDescription>
    </ArgumentChoice>

When the application job submission form is viewed using Compute Manager, a boolean argument called **Run Parallel** will be available. This argument will be displayed as a checkbox and by default will be enabled.  This argument allows a user to choose to run the executable in parallel.

## Attach and Process Job Files
The following pas-appmaker command options are available for creating application input arguments for different types of files.    
--input-file ------------------- Create an input file argument  
--input-file-array ----------- Create an input file argument for each job array index  
--master-file ----------------- Create a master file argument  
--starter-file ------------------ Create a starter file argument   
--engine-file ------------------ Create an engine file argument  
--restart-file ------------------ Create a restart file argument    
--nastran-file ----------------- Create a Nastran file argument  
--parameter-file ------------- Create a parameter file argument  
--additional-files ------------ Create an multi-file argument to attach any additional files to the job  
--attach-directory ----------- Create a directory argument to attach a directory of files to the job  
--convert-to-unix ------------ Convert file line endings to Unix  
--convert-to-windows ------ Convert file line endings to Windows  
--normalize-archives ------- Uncompress job files  
--transfer-include-files ----- Transfer include files to the execution node  
--compress-results ---------- Compress job result files 

###pas-appmaker --input-file

This command option creates an application argument that allows the user to choose the input file for the application.

- input ----------- any filename containing the word "input" is assigned as the job input file
- master --------- any filename containing the word "master" is assigned as the job master file
- starter --------- any filename containing the word "starter" is assigned as the job starter file
- engine --------- any filename containing the word "engine" is assigned as the job engine file
- restart --------- any filename containing the word "restart" is assigned as the job restart file
- nastran -------- any filename containing the word "nastran" is assigned as the job nastran file
- parameter ---- any filename containing the word "parameter" is assigned as the job parameter file

**Command example:**  pas-appmaker MyApp b-input-file

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentFileName>
            <Name>INPUT_FILE</Name>
            <Description>
                A standalone input file or ZIP archive. This option supports the automatic detection of master, starter and engine files.
            </Description>
            <DisplayName>Input File</DisplayName>
            <InputRequired>true</InputRequired>
        </ArgumentFileName>
    </ArgumentChoice>

It will also create a data staging argument within the application converter file:

    <jsdl:DataStaging>
        <jsdl:FileName>name($INPUT_FILE)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>
        <jsdl:Source>
            <jsdl:URI>$INPUT_FILE</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>

When the application job submission form is viewed using Compute Manager, a filename argument called **Input File** will be available. The CM user can then manually enter a filename, browse for a local file, or drag a file from the file tree.

###pas-appmaker --input-file-array

This command option creates an application argument that allows multiple filenames to be chosen as input files to the application. Each input file will be executed within its own job array index.

Addtionally, use the --normalize-archives option to uncompress .zip archive files, and automatically detect the following file designations contained within the archive file (matching is case-insensitive):

- input ----------- any filename containing the word "input" is assigned as the job input file
- master --------- any filename containing the word "master" is assigned as the job master file
- starter --------- any filename containing the word "starter" is assigned as the job starter file
- engine --------- any filename containing the word "engine" is assigned as the job engine file
- restart --------- any filename containing the word "restart" is assigned as the job restart file
- nastran -------- any filename containing the word "nastran" is assigned as the job nastran file
- parameter ---- any filename containing the word "parameter" is assigned as the job parameter file


**Command example:**  pas-appmaker MyApp b-input-file-array

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentFileNameMulti>
            <Name>INPUT_FILE_ARRAY</Name>
            <Description>Select your Input File (s). Each Input File will be executed inside of its own Job Array index.</Description>
            <DisplayName>Input File Array</DisplayName>
            <InputRequired>true</InputRequired>
        </ArgumentFileNameMulti>
    </ArgumentChoice>

It will also create a data staging argument within the application converter file:

    <jsdl:DataStaging>
        <jsdl:FileName>name($INPUT_FILE_ARRAY)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>
        <jsdl:Source>
            <jsdl:URI>$INPUT_FILE_ARRAY</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>

When the application job submission form is viewed using Compute Manager, a multi-filename argument called **Input File Array** will be available. This argument will allow multiple files to be selected as input files to the job script.  The CM user can manually enter filenames, browse for local files, or drag files from the file tree.

###pas-appmaker ---master-file

This command option creates an application argument that allows the user to choose the master file for the application. Use the --normalize-archives option to uncompress a .zip archive file, and automatically detect the following file designations contained within the archive file (matching is case-insensitive):

- input ----------- any filename containing the word "input" is assigned as the job input file
- master --------- any filename containing the word "master" is assigned as the job master file
- starter --------- any filename containing the word "starter" is assigned as the job starter file
- engine --------- any filename containing the word "engine" is assigned as the job engine file
- restart --------- any filename containing the word "restart" is assigned as the job restart file
- nastran -------- any filename containing the word "nastran" is assigned as the job nastran file
- parameter ---- any filename containing the word "parameter" is assigned as the job parameter file

**Command example:**  pas-appmaker MyApp ---master-file

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentFileName>
            <Name>MASTER_FILE</Name>
            <Description>
                A standalone master file or ZIP archive containing a master file.
            </Description>
            <DisplayName>Master File</DisplayName>
            <InputRequired>true</InputRequired>
        </ArgumentFileName>
    </ArgumentChoice>

It will also create a data staging argument within the application converter file:

    <jsdl:DataStaging>
        <jsdl:FileName>name($MASTER_FILE)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>
        <jsdl:Source>
            <jsdl:URI>$MASTER_FILE</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>

When the application job submission form is viewed using Compute Manager, a filename argument called **Master File** will be available. The CM user can then manually enter a filename, browse for a local file, or drag a file from the file tree.

###pas-appmaker --starter-file

This command option creates an application argument that allows the user to choose the starter file for the application.  Use the --normalize-archives option to uncompress a .zip archive file, and automatically detect the following file designations contained within the archive file (matching is case-insensitive):

- input ----------- any filename containing the word "input" is assigned as the job input file
- master --------- any filename containing the word "master" is assigned as the job master file
- starter --------- any filename containing the word "starter" is assigned as the job starter file
- engine --------- any filename containing the word "engine" is assigned as the job engine file
- restart --------- any filename containing the word "restart" is assigned as the job restart file
- nastran -------- any filename containing the word "nastran" is assigned as the job nastran file
- parameter ---- any filename containing the word "parameter" is assigned as the job parameter file


**Command example:**  pas-appmaker MyApp --starter-file

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentFileName>
            <Name>STARTER_FILE</Name>
            <Description>
                A standalone starter file or ZIP archive containing a starter file.
            </Description>
            <DisplayName>Starter File</DisplayName>
            <InputRequired>true</InputRequired>
        </ArgumentFileName>
    </ArgumentChoice>

It will also create a data staging argument within the application converter file:

    <jsdl:DataStaging>
        <jsdl:FileName>name($STARTER_FILE)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>
        <jsdl:Source>
            <jsdl:URI>$STARTER_FILE</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>

When the application job submission form is viewed using Compute Manager, a filename argument called **Starter File** will be available. The CM user can then manually enter a filename, browse for a local file, or drag a file from the file tree.

###pas-appmaker --engine-file

This command option creates an application argument that allows the user to choose the engine file for the application.  Use the --normalize-archives option to uncompress a .zip archive file, and automatically detect the following file designations contained within the archive file (matching is case-insensitive):

- input ----------- any filename containing the word "input" is assigned as the job input file
- master --------- any filename containing the word "master" is assigned as the job master file
- starter --------- any filename containing the word "starter" is assigned as the job starter file
- engine --------- any filename containing the word "engine" is assigned as the job engine file
- restart --------- any filename containing the word "restart" is assigned as the job restart file
- nastran -------- any filename containing the word "nastran" is assigned as the job nastran file
- parameter ---- any filename containing the word "parameter" is assigned as the job parameter file

**Command example:**  pas-appmaker MyApp --engine-file

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentFileName>
            <Name>ENGINE_FILE</Name>
            <Description>
                A standalone engine file or ZIP archive containing a engine file.
            </Description>
            <DisplayName>Engine File</DisplayName>
            <InputRequired>true</InputRequired>
        </ArgumentFileName>
    </ArgumentChoice>

It will also create a data staging argument within the application converter file:

    <jsdl:DataStaging>
        <jsdl:FileName>name($ENGINE_FILE)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>
        <jsdl:Source>
            <jsdl:URI>$ENGINE_FILE</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>

When the application job submission form is viewed using Compute Manager, a filename argument called **Engine File** will be available. The CM user can then manually enter a filename, browse for a local file, or drag a file from the file tree.

###pas-appmaker --restart-file

This command option creates an application argument of type filename that allows the user to choose the restart file for the job script.  Use the --normalize-archives option to uncompress a .zip archive file, and automatically detect the following file designations contained within the archive file (matching is case-insensitive):
- input ----------- any filename containing the word "input" is assigned as the job input file
- master --------- any filename containing the word "master" is assigned as the job master file
- starter --------- any filename containing the word "starter" is assigned as the job starter file
- engine --------- any filename containing the word "engine" is assigned as the job engine file
- restart --------- any filename containing the word "restart" is assigned as the job restart file
- nastran -------- any filename containing the word "nastran" is assigned as the job nastran file
- parameter ---- any filename containing the word "parameter" is assigned as the job parameter file

**Command example:**  pas-appmaker MyApp --restart-file

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentFileName>
            <Name>RESTART_FILE</Name>
            <Description>
                A standalone restart file or ZIP archive containing a restart file.
            </Description>
            <DisplayName>Restart File</DisplayName>
            <InputRequired>false</InputRequired>
        </ArgumentFileName>
    </ArgumentChoice>

It will also create a data staging argument within the application converter file:

    <jsdl:DataStaging>
        <jsdl:FileName>name($RESTART_FILE)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>
        <jsdl:Source>
            <jsdl:URI>$RESTART_FILE</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>

When the application job submission form is viewed using Compute Manager, a filename argument called **Restart File** will be available. The CM user can then manually enter a filename, browse for a local file, or drag a file from the server file tree.

###pas-appmaker --parameter-file

This command option creates an application argument of type filename that allows the user to choose the parameter file for the job script.   Use the --normalize-archives option to uncompress a .zip archive file, and automatically detect the following file designations contained within the archive file (matching is case-insensitive):
- input ----------- any filename containing the word "input" is assigned as the job input file
- master --------- any filename containing the word "master" is assigned as the job master file
- starter --------- any filename containing the word "starter" is assigned as the job starter file
- engine --------- any filename containing the word "engine" is assigned as the job engine file
- restart --------- any filename containing the word "restart" is assigned as the job restart file
- nastran -------- any filename containing the word "nastran" is assigned as the job nastran file
- parameter ---- any filename containing the word "parameter" is assigned as the job parameter file

**Command example:**  pas-appmaker MyApp --parameter-file

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentFileName>
            <Name>PARAMETER_FILE</Name>
            <Description>
                A standalone parameter file or ZIP archive containing a parameter file.
            </Description>
            <DisplayName>Parameter File</DisplayName>
            <InputRequired>false</InputRequired>
        </ArgumentFileName>
    </ArgumentChoice>

It will also create a data staging argument within the application converter file:

    <jsdl:DataStaging>
        <jsdl:FileName>name($PARAMETER_FILE)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>
        <jsdl:Source>
            <jsdl:URI>$PARAMETER_FILE</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>

When the application job submission form is viewed using Compute Manager, a filename argument called **Parameter File** will be available. The CM user can then manually enter a filename, browse for a local file, or drag a file from the file tree.

###pas-appmaker --nastran-file

This command option creates an application argument of type filename that allows the user to choose the Nastran file for the job script.   Use the --normalize-archives option to uncompress a .zip archive file, and automatically detect the following file designations contained within the archive file (matching is case-insensitive):
- input ----------- any filename containing the word "input" is assigned as the job input file
- master --------- any filename containing the word "master" is assigned as the job master file
- starter --------- any filename containing the word "starter" is assigned as the job starter file
- engine --------- any filename containing the word "engine" is assigned as the job engine file
- restart --------- any filename containing the word "restart" is assigned as the job restart file
- nastran -------- any filename containing the word "nastran" is assigned as the job nastran file
- parameter ---- any filename containing the word "parameter" is assigned as the job parameter file

**Command example:**  pas-appmaker MyApp --nastran-file

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentFileName>
            <Name>NASTRAN_FILE</Name>
            <Description>
                A standalone nastran file or ZIP archive containing a nastran file.
            </Description>
            <DisplayName>Nastran File</DisplayName>
            <InputRequired>false</InputRequired>
            </ArgumentFileName>
    </ArgumentChoice>

It will also create a data staging argument within the application converter file:

    <jsdl:DataStaging>
        <jsdl:FileName>name($NASTRAN_FILE)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>
        <jsdl:Source>
             <jsdl:URI>$NASTRAN_FILE</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>

When the application job submission form is viewed using Compute Manager, a filename argument called **Nastran File** will be available. The CM user can then manually enter a filename, browse for a local file, or drag a file from the file tree.


###pas-appmaker --additional-files

This command option creates an application argument that allows the user to stage any additional files required by the application to its working directory. 

**Command example:**  pas-appmaker MyApp --additional-files

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentFileNameMulti>
            <Name>ADDITIONAL_FILES</Name>
            <Description>Automatically stage any additional files to the AppMaker jobs working directory.</Description>
            <DisplayName>Additional Files</DisplayName>
            <InputRequired>false</InputRequired>
        </ArgumentFileNameMulti>
    </ArgumentChoice>

It will also create a data staging argument within the application converter file:

    <jsdl:DataStaging>
        <jsdl:FileName>name($ADDITIONAL_FILES)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>
        <jsdl:Source>
            <jsdl:URI>$ADDITIONAL_FILES</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>

When the application job submission form is viewed using Compute Manager, a multi-filename argument called **Additional Files** will be available. This argument will allow additional files required by the job to be staged to the job's working directory.  The CM user can manually enter filenames, browse for local files, or drag files from the file tree.

###pas-appmaker  --convert-to-unix

This command option creates an application argument of type boolean that allows all job file line endings to be converted to a Unix format.

**Command example:**  pas-appmaker MyApp b-convert-to-unix

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentBooleanWithDescription>
            <Name>CONVERT_TO_UNIX</Name>
            <Description>Convert the line endings of all files to UNIX format.</Description>
            <DisplayName>Convert to UNIX</DisplayName>
            <InputRequired>false</InputRequired>
            <FeatureEnabled>true</FeatureEnabled>
        </ArgumentBooleanWithDescription>
    </ArgumentChoice>

When the application job submission form is viewed using Compute Manager, a boolean argument called **Convert to UNIX** will be available. This argument will be displayed as a checkbox and by default will be enabled. This argument allows a user to choose to convert all job file line endings to a Unix format.

###pas-appmaker  --convert-to-windows

This command option creates an application argument of type boolean that allows all job file line endings to be converted to a Windows format.

**Command example:**  pas-appmaker MyApp --convert-to-windows

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentBooleanWithDescription>
            <Name>CONVERT_TO_WINDOWS</Name>
            <Description>Convert the line endings of all files to Windows format.</Description>
            <DisplayName>Convert to Windows</DisplayName>
            <InputRequired>false</InputRequired>
            <FeatureEnabled>true</FeatureEnabled>
        </ArgumentBooleanWithDescription>
    </ArgumentChoice>

When the application job submission form is viewed using Compute Manager, a boolean argument called **Convert to Windows** will be available. This argument will be displayed as a checkbox and by default will be enabled. This argument allows a user to choose to convert all job fiel line endings to a Windows format.

###pas-appmaker  --normalize-archives

This command option creates an application argument of type boolean that allows all job .zip archive files to be uncompressed, and automatically detects the following file designations contained within the archive file (matching is case-insensitive):
- input ----------- any filename containing the word "input" is assigned as the job input file
- master --------- any filename containing the word "master" is assigned as the job master file
- starter --------- any filename containing the word "starter" is assigned as the job starter file
- engine --------- any filename containing the word "engine" is assigned as the job engine file
- restart --------- any filename containing the word "restart" is assigned as the job restart file
- nastran -------- any filename containing the word "nastran" is assigned as the job nastran file
- parameter ---- any filename containing the word "parameter" is assigned as the job parameter file

**Command example:**  pas-appmaker MyApp --normalize-archives

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentBooleanWithDescription>
            <Name>NORMALIZE_ARCHIVES</Name>
            <Description>Automatically uncompress any attached .zip files. Additionally master, starter, engine and restart files will be automatically identified.</Description>
            <DisplayName>Normalize Archives</DisplayName>
            <InputRequired>false</InputRequired>
            <FeatureEnabled>true</FeatureEnabled>
        </ArgumentBooleanWithDescription>
    </ArgumentChoice>

When the application job submission form is viewed using Compute Manager, a boolean argument called **Normalize Archives** will be available. This argument will be displayed as a checkbox and by default will be enabled. This argument allows a user to choose to uncompress all a .zip job archive files and detect file designations.

##pas-appmaker  --transfer-include-files

This command option creates an application argument of type boolean that enables/disables the detection of include file statements in job files.  Any remote files designated by an include file statement will be copied to the execution node.  Include statements are then modified to point to the file that has been copied locally.  This reduces network intensive I/O.

**Command example:**  pas-appmaker MyApp --transfer-include-files

    <ArgumentChoice>
        <ArgumentBooleanWithDescription>
            <Name>TRANSFER_INCLUDE_FILES</Name>
            <Description>Automatically transfer any remote files mentioned as include statements.</Description>
            <DisplayName>Transfer Include Files</DisplayName>
            <InputRequired>false</InputRequired>
            <FeatureEnabled>true</FeatureEnabled>
        </ArgumentBooleanWithDescription>
    </ArgumentChoice>

When the application job submission form is viewed using Compute Manager, a boolean argument called **Transfer Include Files** will be available. This argument will be displayed as a checkbox and by default will be enabled. Any remote files designated by an include file statement will be copied to the execution node.

###pas-appmaker --compress-results

This command option creates an application argument of type boolean that allows the job result files to be compressed into a single .zip archive file.

**_Note_**  
This option also supports a .tar.gz archive file format. However, a special environment variable in the application exit phase must be set to make this happen.  Set this variable using the command option:

    --exit-environment=PAS_COMPRESS_RESULTS_FORMAT=.tar.gz
    
**Command example:**  pas-appmaker MyApp --compress-results

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentBooleanWithDescription>
            <Name>COMPRESS_RESULTS</Name>
            <Description>Compress job results into a single ZIP file.</Description>
            <DisplayName>Compress Results</DisplayName>
            <FeatureEnabled>true</FeatureEnabled>
            <InputRequired>false</InputRequired>
        </ArgumentBooleanWithDescription>
    </ArgumentChoice>

When the application job submission form is viewed using Compute Manager, a boolean argument called **Compress Results** will be available. This argument will be displayed as a checkbox and by default will be enabled. This argument allows the job result files to be compressed into a single archive file.

###pas-appmaker --attach-directory

This command option creates an application argument of type directory name that allows the user to attach a directory of files to the job.  These files will be staged to the job's working directory.

**Command example:**  pas-appmaker MyApp --attach-directory

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentDirectoryName>
            <Name>ATTACH_DIRECTORY</Name>
            <Description>Attach a directory filled with files to the AppMaker job.</Description>
            <DisplayName>Attach Directory</DisplayName>
            <InputRequired>false</InputRequired>
        </ArgumentDirectoryName>
    </ArgumentChoice>

It will also create a data staging argument within the application converter file:

    <jsdl:DataStaging>
        <jsdl:FileName>name($ATTACH_DIRECTORY)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>
        <jsdl:Source>
            <jsdl:URI>$ATTACH_DIRECTORY</jsdl:URI>
        </jsdl:Source>
    </jsdl:DataStaging>

When the application job submission form is viewed using Compute Manager, a filename argument called **Attach Directory** will be available. The CM user can then manually enter a directory name, or drag a directory from the directory tree.

## Create Application Actions
The following pas-appmaker command options are available for creating application actions.    
--send-signals ------------ Create an application action that will send a signal to your application  
--shell-command ------- Create an application action to execute a shell command

###pas-appmaker --send-signals

This command option enables an application action that will send a signal to your application and any processes that it may have spawned.  The application action will only be available while the job is in a running state.   The application action will allow an application to be suspended, resumed, or terminated. 

**Command example:**  pas-appmaker MyApp --send-signals

This option will create an application action called **Send Signals** having the following argument:

    <ArgumentChoice>
        <ArgumentStringEnumerated>
            <Name>SEND_SIGNALS</Name>
            <Description>Select which signal to send.</Description>
            <DisplayName>Signal</DisplayName>
            <InputRequired>true</InputRequired>
            <Option>Suspend</Option>
            <Option>Resume</Option>
            <Option default="true">Terminate</Option>
        </ArgumentStringEnumerated>
    </ArgumentChoice>
    
When the application action is executed from the Job Monitoring page of Compute Manager, a popup box will be displayed.  The user will be prompted to choose which signal to send to the application's process. The CM user can then choose to suspend, resume, or terminate the process.

###pas-appmaker --shell-command

This command option enables an application action that will execute a shell command in your job's execution directory.  The application action will only be available while the job is in a running state.  

**Command example:**  pas-appmaker MyApp --shell-command

This option will create an application action called **Shell Command** having the following argument:

    <ArgumentChoice>
        <ArgumentString>
            <Name>SHELL_COMMAND</Name>
            <Description>Run this shell command.</Description>
            <DisplayName>Command</DisplayName>
            <InputRequired>true</InputRequired>
        </ArgumentString>
    </ArgumentChoice>

When the application action is executed from the Job Monitoring page of Compute Manager, a popup box will be displayed.  The user will be prompted to enter a shell command which will be executed in the job's execution directory.

## Advanced Options
The following pas-appmaker command options are advanced options for more advanced application definition authors.  
--import-postsubmit ------- automatically installs a PBS hook  
--site-versions --------------- pulls versions from the site configuration file  
--logging ---------------------- enables appmaker logging  
--input-environment ------ directs appmaker to add environment variables to the application's input phase environment   
--input-hook ----------------- enable this file as the application's input hook    
--submit-environment ----- directs appmaker to add environment variables to the application's submit phase environment  
--submit-hook --------------- enable this file as the application's input hook    
--start-environment ------- directs appmaker to add environment variables to the application's start phase environment    
--start-hook ------------------ enable this file as the application's input hook    
--actions-environment ---- directs appmaker to add environment variables to the application's actions phase environment  
--actions-hook --------------- enable this file as the application's input hook      
--exit-environment --------- directs appmaker to add environment variables to the application's exit phase environment  
--exit-hook -------------------- enable this file as the application's input hook   

###pas-appmaker --import-postsubmit

Some of the features of appmaker require a _postsubmit.py_ PBS Professional hook, an extension to the _presubmit.py_ submit phase base file.  This command option will install the hook as long as you, the author, have permissions to install the PBS hook.  Otherwise, contact your site's PBS administrator to import this hook via qmgr.  Options that require the installation of a PBS hook are:  
 * --input-file-array  
 * --project

**Command example:**  pas-appmaker MyApp --import-postsubmit

###pas-appmaker --site-versions

This command option creates an application argument of type string that pulls the available versions of the application from the PAS site configuration file.   

**Command example:**  pas-appmaker MyApp --site-versions

This option will create the following application input argument within the application input file:

    <ArgumentChoice>
        <ArgumentStringEnumerated>
            <Name>SITE_VERSIONS</Name>
            <Description>Please select which version of AppMaker you would like to use.</Description>
            <DisplayName>Site Versions</DisplayName>
            <InputRequired>false</InputRequired>
            <xi:include href="site-config.xml" xpointer="xpath1(//Application[@id='MyApp']/ApplicationVersions//Option)"/>
        </ArgumentStringEnumerated>
    </ArgumentChoice>

When the application job submission form is viewed using Compute Manager, a string argument called _Site Versions_ will be available. This argument will be displayed as a drop-down box with a list of available versions of the application pulled from the site configuration file.  Once a version is selected from the drop-down box and the job is submitted, the environment variable PAS_EXECUTABLE will be set to the executable associated with the selected version from the site configuration file.

###pas-appmaker --logging

This command option enables logging.  Logging will be captured for each phase of the application lifecycle and will record:  
    * Processing environment
    * Resources
    * Attributes
    * Scripts
    * Process ids
    * Events 
    * Hooks
 
The log files will be returned with the job result files and will follow the naming convention _phasename.log_.

**Command example:**  pas-appmaker MyApp --logging

###pas-appmaker --input-environment=&lt;name&gt;=&lt;value&gt;,&lt;name&gt;=&lt;value&gt;....

This command option directs appmaker to add the environment variables defined by the key-value pairs to the application's input phase environment.  If the environment variable is already defined in the application's environment, then its value will be overlaid.  Otherwise, the variable will be added to the application's input phase environment.  Any environment variables prefixed with "_PAS\__" will persist to the subsequent application phase.  Otherwise, the environment variable will only exist during the application's input phase.

**Command example:**  pas-appmaker MyApp --input-environment=PAS_NCPUS=14

###pas-appmaker --input-hook=/path/to/your/script.ext

This command option directs appmaker to enable this script file as the application's input hook.  The file will be copied to the application's home directory _/var/spool/pas/repository/applications/AppName/submittime_.  The hook can be coded in any language and will be executed at the beginning of the input phase after the application's environment has been constructed. 

**Command example:**  pas-appmaker MyApp --input-hook=/path/to/your/script.ext

###pas-appmaker --submit-environment=&lt;name&gt;=&lt;value&gt;,&lt;name&gt;=&lt;value&gt;....

This command option directs appmaker to add the environment variables defined by the key-value pairs to the application's submit phase environment.  If the environment variable is already defined in the application's environment, then its value will be overlaid.  Otherwise, the variable will be added to the application's submit phase environment.  Any environment variables prefixed with "_PAS\__" will persist to the subsequent application phase.  Otherwise, the environment variable will only exist during the application's submit phase.

**Command example:**  pas-appmaker MyApp --submit-environment=PAS\_SELECT=2,PAS\_NCPUS=8,PAS_MEM=1gb

###pas-appmaker --submit-hook=/path/to/your/script.ext

This command option directs appmaker to enable this script file as the application's submit hook.  The file will be copied to the application's home directory _/var/spool/pas/repository/applications/AppName/submittime_.  The hook can be coded in any language and will be executed at the beginning of the submit phase after the application's environment has been constructed.  

**Command example:**  pas-appmaker MyApp --submit-hook=/path/to/your/script.ext

###pas-appmaker --start-environment=&lt;name&gt;=&lt;value&gt;,&lt;name&gt;=&lt;value&gt;....

This command option directs appmaker to add the environment variables defined by the key-value pairs to the application's start phase environment.  If the environment variable is already defined in the application's environment, then its value will be overlaid.  Otherwise, the variable will be added to the application's start phase environment.  Any environment variables prefixed with "_PAS\__" will persist to the subsequent application phase.  Otherwise, the environment variable will only exist during the application's start phase.

**Command example:**  pas-appmaker MyApp --start-environment=PAS\_EXECUTABLE=/bin/sleep,PAS\_ARGUMENTS=30

###pas-appmaker --start-hook=/path/to/your/script.ext

This command option directs appmaker to enable this script file as the application's start hook.  The file will be copied to the application's home directory _/var/spool/pas/repository/applications/AppName/runtime_.  The hook can be coded in any language and will be executed at the beginning of the start phase after the application's environment has been constructed.  

**Command example:**  pas-appmaker MyApp --submit-hook=/path/to/your/script.ext

###pas-appmaker --actions-environment=&lt;name&gt;=&lt;value&gt;,&lt;name&gt;=&lt;value&gt;....

This command option directs appmaker to add the environment variables defined by the key-value pairs to the application's actions phase environment.  If the environment variable is already defined in the application's environment, then its value will be overlaid.  Otherwise, the variable will be added to the application's actions phase environment.  Any environment variables prefixed with "_PAS\__" will persist to the subsequent application phase.  Otherwise, the environment variable will only exist during the application's actions phase.

**Command example:**  pas-appmaker MyApp --actions-environment=PAS\_SEND\_SIGNALS=true

###pas-appmaker --actions-hook=/path/to/your/script.ext

This command option directs appmaker to enable this script file as the application's action hook.  The file will be copied to the application's home directory _/var/spool/pas/repository/applications/AppName/runtime_.  The hook can be coded in any language and will be executed at the beginning of the action phase after the application's environment has been constructed.

**Command example:**  pas-appmaker MyApp --actions-hook=/path/to/your/script.ext

###pas-appmaker --exit-environment=&lt;name&gt;=&lt;value&gt;,&lt;name&gt;=&lt;value&gt;....

This command option directs appmaker to add the environment variables defined by the key-value pairs to the application's exit phase environment.  If the environment variable is already defined in the application's environment, then its value will be overlaid.  Otherwise, the variable will be added to the application's exit phase environment.  Any environment variables prefixed with "_PAS\__" will persist to the subsequent application phase.  Otherwise, the environment variable will only exist during the application's exit phase.

**Command example:**  pas-appmaker MyApp --exit-environment=PAS\_COMPRESS\_RESULTS=true

###pas-appmaker --exit-hook=/path/to/your/script.ext

This command option directs appmaker to enable this script file as the application's exit hook.  The file will be copied to the application's home directory _/var/spool/pas/repository/applications/AppName/runtime_.  The hook can be coded in any language and will be executed at the beginning of the exit phase after the application's environment has been constructed.

**Command example:**  pas-appmaker MyApp --exit-hook=/path/to/your/script.ext


## Copyright

o?= Copyright 2013 - 2014 Altair Engineering, Inc. All rights reserved.
