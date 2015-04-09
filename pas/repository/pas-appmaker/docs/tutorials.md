# pas-appmaker/docs/tutorials

A framework for creating powerful application definitions.

## Introduction

This document is for application authors who are learning to create application definitions with pas-appmaker. If you are an administrator, and have not yet configured pas-appmaker for your environment, please read the pas-appmaker/docs/installation document to learn how.

## Tutorial: The basic concepts

pas-appmaker has many simple and advanced methods for describing your applications logic. In this tutorial, you will see the most basic concepts applied by example.

### BasicApp 

Make a simple application that presents a few resources and expects an executable with command line arguments to be given by the submitting user.

    pas-appmaker BasicApp --select --ncpus --mem --executable --arguments --logging

Or, make an application where the resources, as well as the executable and command line arguments are already defined by the author.

    pas-appmaker BasicApp --submit-environment PAS_SELECT=1,PAS_NCPUS=1,PAS_MEM=100mb --start-environment PAS_EXECUTABLE=/bin/sleep,PAS_ARGUMENTS=60 --logging

## Tutorial: Making real-world applications

A few examples of how pas-appmaker can easily create application definitions for common solvers.

### OptiStruct

    pas-appmaker OptiStruct --input-file --additional-files --arguments --logging --submit-environment PAS_SELECT=1,PAS_NCPUS=1,PAS_MEM=1gb --start-environment PAS_EXECUTABLE=/path/to/optistruct,PAS_ARGUMENTS="PAS_INPUT_FILE PAS_ARGUMENTS"

### RADIOSS

    pas-appmaker RADIOSS --ncpus --mem --starter-file --engine-file --logging --start-environment PAS_EXECUTABLE=/path/to/radioss,PAS_ARGUMENTS="-both PAS_STARTER_FILE -nthread PAS_NCPUS"

### Abaqus

    pas-appmaker Abaqus --ncpus --mem --input-file --additional-files --arguments --logging --start-environment PAS_EXECUTABLE=/path/to/abaqus,PAS_ARGUMENTS="job=PAS_INPUT_FILE_NO_EXT cpus=PAS_NCPUS interactive"

## Tutorial: Making generic applications

pas-appmaker allows you to present job resources, attributes, executables and job files in a variety of different ways.

### byForm

An example of how to create an application where HTML form fields are how the author would prefer submitting users to request their resources.

    pas-appmaker byForm --select --ncpus --mem --place --job-arrays --input-file --additional-files --software --executable --arguments --environment --logging

### byStatement

An example of how to create an application where submitting users, more comfortable with the command-line, can request resources and attributes using the familiar select and attribute syntax of qsub.

    pas-appmaker byStatement --resources --attributes --software --executable --arguments --environment --logging

### byEnvironment

An example of how to create an application where submitting users invoke all pas-appmaker options using environment variables only.

    pas-appmaker byEnvironment --environment --logging
    
## Tutorial: Extending your applications with hooks

pas-appmaker allows you to modify and extend its core functionality using hooks written in any language and at every phase of your applications life cycle.
Using pas-appmaker hooks will give the author power to manipulate job parameters provided by the user and additionally manipulate the environment server side.

### SubmitHook

Example of executing a Perl hook at the beginning of the Submit Phase. This happens before the job is submitted to PBS Professional.

Hook

    #!/usr/bin/env perl

    use strict;
    use warnings;

    use IO::File;

    if (not defined $ENV{'PAS_RESOURCES'}) {
        $ENV{'PAS_RESOURCES'} = 'select=1:ncpus=1:mem=1gb';
    }
    
    if (not defined $ENV{'PAS_ATTRIBUTES'}) {
        $ENV{'PAS_ATTRIBUTES'} = 'group_list=hpcteam@cluster';
    }

    ### Export any environment changes to pas-appmaker and exit.
    
    my $environment = IO::File->new('submit.import', 'w');
    
    if (defined $environment) { 
    
        for my $variable (keys %ENV) {
            print $environment "$variable=$ENV{$variable}\n";
        }
    }
    
    undef $environment and exit(0);

Command

    pas-appmaker SubmitHook --submit-hook /path/to/my/hook.pl 

### StartHook

An example of executing a Python hook at the beginning of the Start Phase. This happens before the job actually runs.

Hook

    #!/usr/bin/env python
    
    #coding: utf-8

    import os
    import sys
    
    os.environ['PAS_LOGGING'] = 'true'
    
    if not 'PAS_EXECUTABLE' in os.environ:
        os.environ['PAS_EXECUTABLE'] = '/path/to/program.bin'
    
    ### Export any environment changes to pas-appmaker and exit.
    
    environment = open('start.import', 'w')
    
    for k, v in os.environ.items():
        environment.write('%s=%s\n' % (k, v))
    
    environment.close()
    sys.exit(0)

Command

    pas-appmaker StartHook --start-hook /path/to/my/hook.py 


## Tutorial: Advanced configurations with template files

With pas-appmaker, you can pre-define template files to be used automatically at application creation time. This is
especially powerful for administrators wanting to apply common or application specific input arguments, hooks or environment files.

### Input Template

Will append custom arguments to the end of all pas-appmaker generated argument input files.

app-inp.xml

    <ArgumentChoice>
        <ArgumentBooleanWithDescription>  
            
            <Name>Something</Name>
            <Description>Do something special when clicked.</Description>
            
            <DisplayName>Something</DisplayName>
            <FeatureEnabled>true</FeatureEnabled>
            <InputRequired>false</InputRequired>
        </ArgumentBooleanWithDescription>
    </ArgumentChoice>    

### Appname Template

Will append application specific arguments to the end of any pas-appmaker generated application definition that matches the correct appnlication name.

app-inp-appname.xml

    <ArgumentChoice>
        <ArgumentFileName>
            
            <Name>STAGE_SOMETHING</Name>
            <Description>Stage something over with the APP_NAME job.</Description>
            <DisplayName>Stage Something</DisplayName>
            <InputRequired>true</InputRequired>
        
        </ArgumentFileName>
    </ArgumentChoice>

### Converter Template

Will append data staging directives to the end of all pas-appmaker generated input converter files.

app-conv.xml

    <jsdl:DataStaging>    

        <jsdl:FileName>name($STAGE_SOMETHING)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>

        <jsdl:Source>
            <jsdl:URI>$STAGE_SOMETHING</jsdl:URI>
        <//jsdl:Source>

    </jsdl:DataStaging>

### Appname Template

Will append application specific data staging directives to the end of any pas-appmaker generated input converter file that matches the given application name.

app-conv-appname.xml

    <jsdl:DataStaging>    
        
        <jsdl:FileName>name($STAGE_SOMETHING_ELSE)</jsdl:FileName>
        <jsdl:CreationFlag>overwrite</jsdl:CreationFlag>

        <jsdl:Source>
            <jsdl:URI>$STAGE_SOMETHING_ELSE</jsdl:URI>
        </jsdl:Source>
    
    </jsdl:DataStaging>

### The following templates are supported.

Input Files

    app-inp.xml
    app-inp-appname.xml
    app-conv.xml
    app-conv-appname.xml
    app-actions.xml
    app-actions-appname.xml
    input.py
    input.hook
    input.environment

Submit Files

    presubmit.py
    postsubmit.py
    submit.hook
    submit.environment

Start Files

    start.py
    start.hook
    start.environment
    
Actions Files

    app-actions.xml
    app-actions-appname.xml
    actions.py
    actions.hook
    actions.environment
    
Exit Files

    exit.py
    exit.hook
    exit.environment

## Copyright

(c) Copyright 2013 - 2014 Altair Engineering, Inc. All rights reserved.
