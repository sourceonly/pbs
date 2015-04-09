#!/usr/bin/python
#
# Version 0.1
#
# Name:  include_parser.py
# Purpose: Copies include files from user's working directory to scratch(or any desired directory)
#          subsequently modifying master and connected include file(s) (if nested paths are involved)
# Solver(s) supported:   Abaqus , LsDyna , Radioss
#
# Usage: start.py and/or presubmit.py (depending on invocation circumstances)
#
# NOTE: Please ensure Python 2.6 along with shutil module are installed before launching
#
# Functionality: ( NESTED Include file(s) capability supported )
#
#   - Check correct number of invocation arguments
#   - Validate the solver mentioned (if it belongs to the 3 supported solvers)
#   - Validate the master file and corresponding include file extension (.rad , .inp , .key)
#   - If above points are verified and processed based on solver, start master file parsing
#   - Based on solver's "INCLUDE" pattern/regex extract all relevant paths
#   - Perform copy operations of include file(s) to destination path
#   - Modify all paths in the master file serially and localizing to the target folder
#   - Rename copied files to that modified in master file
#   - Support for nested include files (involves the same steps as mentioned in the previous points)
#
# Author: Avinaba Roy
#

import os
import re       # Regular expression matching operations similar to those found in Perl
import sys
import shutil   # Offers a number of high-level operations on files and collections of files

"""  GLOBAL DATA SET  """

solver_supported=["abaqus","lsdyna","radioss"]                          # Types of solver(s) supported
extension_supported=[".inp",".key",".rad"]                              # File extension(s) corresponding to solvers supported
solver_regex=["^\*INCLUDE, INPUT\s*=\s*(\S*)","^\*INCLUDE\s*(\S*)","^\#INCLUDE\s*(\S*)"]  # Regex's for various "INCLUDE" styles
index=0                                                                 # File name prefix index (Also acts as a counter for total files processed)
file_count=0
logging = False

"""  UNPARSED FILE(S) WITH ABSOLUTE PATH DATA SET  """

unparsed_files=[]                       
unparsed_files_destination_names=[]

""" LOGGING OPTION CHECK """
def logging_option_check():
    if 'PAS_LOGGING' in os.environ:
        if os.environ['PAS_LOGGING'] == 'true':
            logging = True

"""  SAME_FILE_NAME_CHECK  """

def file_name_check(file_name,d_dir):
    if os.path.exists(os.path.join(d_dir,file_name))==True:
        if logging is True:
            log.write("\n\nFile_name "+file_name+" already exists...Renaming\n")
        return 1
    else:
        return 0
    

"""  INDEX REQUIREMENT CHECK FUNCTION  """

def index_requirement(in_file_path,dest_directory):
    head , tail = os.path.split(in_file_path)
    if head == "":
        return file_name_check(tail,dest_directory)
    else:
        return 1


"""  MASTER FILE PARSER FUNCTION  """ 

def master_file_parser(in_file,out_file,solver,regex):
    
    global index
    global unparsed_files
    global unparsed_files_destination_names
    global file_count
    
    if regex == "":
        if logging is True:
            log.write("\n\nCurrently under development. Exiting program.\n")
        sys.exit(0)
        
    include=re.compile(regex, flags=re.IGNORECASE)                      # Regex declaration with ignore case flag
    line = in_file.readline()
    
    while line:                                                         # Loop to extract the path-to-include-file data from the line
        if include.match(line):                                         # If pattern match then perform follwing operations
            file_count +=1
            if solver=="lsdyna":
                line = in_file.readline()
                include_statement = line
                include_statement=include_statement.strip('\n')
                include_statement=include_statement.strip()
            else:
                include_statement = include.match(line).group(1)
            cp_source=os.path.abspath(include_statement)                # Get the absolute path of the file name mentioned
            include_name=os.path.basename(include_statement)            # Get the file name mentioned
            include_path = os.path.dirname(include_statement)
            if index_requirement(include_statement,destination_directory) == 1:
                index += 1                                                  # Prefix index to new file (at destination)
                line = line.replace(include_statement,str(index) + '_' + include_name)          # Replace line with new path (localized)
                cp_dest=os.path.join(destination_directory,str(index) + '_' + include_name)     # Prefix index to new file (at destination)
            else:
                cp_dest=os.path.join(destination_directory,include_name)
            unparsed_files.append(cp_source)                            # Add the file path (encountered/read) to the list of unparsed files
            unparsed_files_destination_names.append(cp_dest)            # Add the file name (encountered/read) to the list of unparsed files
            try:
                shutil.copyfile(cp_source,cp_dest)                          # Perform copy operations from source to destination
            except Exception as inst:
                if logging is True:
                    log.write("\n\nPlease check error code.\n"+str(inst)+"\n")
                exit(0)
            out_file.write(line)                                        # Finalize changes to output file
        else:
            out_file.write(line)                                        # If pattern does not match then simply copy line to target output file
            
        line = in_file.readline()                                       # Proceed to next line
        
    in_file.close()                                                     # Close respective file(s)
    out_file.close()                                                    # Close respective file(s)
    
    if logging is True:
        log.write("\n\nMaster file "+os.path.basename(in_file.name)+" parsing complete!\n")
    
"""  INCLUDE FILE PARSER FUNCTION  """ 
    
def include_file_parser(in_file,out_file,solver,path,regex):
    
    global index
    global unparsed_files
    global unparsed_files_destination_names
    global file_count
    
    if regex == "":
        if logging is True:
            log.write("\n\nCurrently under development. Exiting program.\n")
        exit(0)
        
    include=re.compile(regex, flags=re.IGNORECASE)                      # Regex declaration with ignore case flag
    line = in_file.readline()
    
    while line:                                                         # Loop to extract the path-to-include-file data from the line
        if include.match(line):                                         # If pattern match then perform follwing operations
            file_count +=1
            if solver=="lsdyna":
                line = in_file.readline()
                include_statement = line
                include_statement=include_statement.strip('\n')
                include_statement=include_statement.strip()
            else:
                include_statement = include.match(line).group(1)
            cp_source=os.path.join(path,include_statement)              # Join the path of include file being read with the path mentioned IN the line
            include_name=os.path.basename(include_statement)            # Get the file name mentioned
            include_path = os.path.dirname(include_statement)           
            if index_requirement(include_statement,destination_directory) == 1:
                index += 1                                                  # Prefix index to new file (at destination)
                line = line.replace(include_statement,str(index) + '_' + include_name)          # Replace line with new path (localized)
                cp_dest=os.path.join(destination_directory,str(index) + '_' + include_name)     # Prefix index to new file (at destination)
            else:
                cp_dest=os.path.join(destination_directory,include_name)
            unparsed_files.append(cp_source)                            # Add the file path (encountered/read) to the list of unparsed files
            unparsed_files_destination_names.append(cp_dest)            # Add the file name (encountered/read) to the list of unparsed files
            try:
                shutil.copyfile(cp_source, cp_dest)                          # Perform copy operations from source to destination
            except Exception as inst:
                if logging is True:
                    log.write("\n\nPlease check error code.\n"+str(inst)+"\n")
                exit(0)
            out_file.write(line)                                        # Finalize changes to output file
        else:
            out_file.write(line)                                        # If pattern does not match then simply copy line to target output file

        line = in_file.readline()                                       # Proceed to next line

    in_file.close()                                                     # Close respective file(s)
    out_file.close()                                                    # Close respective file(s)

    if logging is True:
        log.write("\n\nInclude file "+os.path.basename(in_file.name)+" parsing complete!\n")

"""  MAIN PROGRAM  """

# Using pre-defined environment variables : PAS_MASTER_FILE , PAS_LOGGING , PAS_SOFTWARE , PAS_SUBMISSION_DIRECTORY

logging_option_check()

if logging is True:
    log.write("\n\nTransfer Include Files...\n")

if 'PAS_MASTER_FILE' in os.environ:
    Master_file_name = os.path.basename(os.environ['PAS_MASTER_FILE'])
else:
    if logging is True:
        log.write("\n\nEnvironment variable : PAS_MASTER_FILE not defined!\n")
    exit(0)

if 'PAS_SUBMISSION_DIRECTORY' in os.environ:
    Submission_file_name = os.environ['PAS_SUBMISSION_DIRECTORY']
else:
    if logging is True:
        log.write("\n\nEnvironment variable : PAS_SUBMISSION_DIRECTORY not defined!\n")
    exit(0)

if 'PAS_SOFTWARE' in os.environ:
    Solver_name = os.environ['PAS_SOFTWARE']
else:
    if logging is True:
        log.write("\n\nEnvironment variable : PAS_SOFTWARE not defined!\n")
    exit(0)

# Sample Test case (for pre-set directory path(s) )

"""
Master_file_name = 'N_3472088_0000.rad'
Submission_file_name = 'Z:\N_3472088_0000.rad'
Solver_name = 'radioss'
"""

if logging is True:
        log.write("\n\nAll arguments successfully supplied!\n")

# Exception handling if any inconsistency with file extension if it does not match with supported types

ext_flag = 0
filename, extension = os.path.splitext(Master_file_name)
for ext in extension_supported:
    if ext == extension:
        ext_flag = 1
        break

if ext_flag == 1:
    if logging is True:
        log.write("\n\nFile extension "+extension+" supported!\n")
else:
    if logging is True:
        log.write("\n\nFile extension "+extension+" NOT supported!\n")
    exit(0)


# Exception handling if any inconsistency with solver name entered if it does not match with supported type

solver_flag=0
i=0
solver_input=Solver_name
solver_input=solver_input.lower()
for solver in solver_supported:
    if solver_input==solver:
        solver_flag=1
        s_regex = solver_regex[i]
        break
    i +=1

if solver_flag==1:
    if logging is True:
        log.write("\n\nSolver "+solver_input+" supported!\n")
else:
    if logging is True:
        log.write("\n\nSolver "+solver_input+" NOT supported!\n")
    exit(0)
    
# Getting and setting destination path details
    
destination_file_path=os.path.abspath(Submission_file_name)
destination_directory=os.path.dirname(destination_file_path)
destination_directory=os.path.abspath(destination_directory)

""" COPY MASTER PARSER PROGRAM INTO DESTINATION IN ORDER TO MAINTAIN PERSPECTIVE """

program_copy_path=os.path.join(destination_directory,'include_parser.py')

try:
    shutil.copyfile('include_parser.py',program_copy_path)
except Exception as inst:
    if logging is True:
        log.write("\n\nPlease check error code.\n"+str(inst))
    exit(0)

Master_file = open(Master_file_name,'r')
Submission_file = open(Submission_file_name,'w')

master_file_parser(Master_file,Submission_file,solver_input,s_regex)      # Master file parser function call

while unparsed_files:                                                               # Process unparsed file(s)                                               
    file = unparsed_files.pop()                                                     # Eliminate file from list
    file_output = unparsed_files_destination_names.pop()                            # Eliminate file from list
    file_dir=os.path.dirname(file)
    file_dir=os.path.abspath(file_dir)
    try:
        input_file = open(file, 'r')        # Open file (as stored in list)
    except Exception as inst:
        if logging is True:
            log.write("\n\nPlease check error code.\n"+str(inst)+"\n")
        exit(0)
    try:
        output_file = open(os.path.join(destination_directory,file_output),'w')         # Create output file with modified filename(indexed file_name)
    except Exception as inst:
        if logging is True:
            log.write("\n\nPlease check error code.\n"+str(inst)+"\n")
        exit(0)
    include_file_parser(input_file,output_file,solver_input,file_dir,s_regex)       # Include file parser function call
    #index +=1

if logging is True:
        log.write("\n\n*** Total files processed : "+str(file_count)+" ***\n")
    
