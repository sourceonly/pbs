import time, os, sys, re, subprocess
import glob, shutil

Debug = False 

#job_script      = os.path.basename("/root/script.sh")
job_script	= "/root/script.sh"
python_path     = os.environ['PYTHONPATH']
job_name     = os.environ['PAS_JOB_NAME']

# TODO: Standardize job script line endings for better multiplaform/editor compatibility.

#job_script = job_script.replace('%20',' ')
if Debug:
    print "start.py: script: " + job_script  

file = open( job_script, 'r' )
line = file.readline()
file.close()

argsUnescaped = []
rc = 0
#            argsUnescaped.append(arg) 

##############################################################################
execution_dir = os.getcwd()
inputFileDir = execution_dir+"/"+job_name+"/"
for filename in glob.glob(os.path.join(inputFileDir, '*.*')):
    shutil.copy(filename, execution_dir)

shutil.rmtree(inputFileDir)

##############################################################################

if line.startswith('#!'):
    if Debug:
        print "start.py: #! detected"  

    try:
        interpreter = re.match( '^#!(.*)', line ).group(1)
        command = [interpreter] + [job_script] + argsUnescaped
        if Debug:
            print "start.py: executing:"  
            print command  

        sys.stdout.flush()            
        sys.stderr.flush()            
        res = subprocess.Popen(command, shell=False)
        res.communicate()
        sys.stdout.flush()            
        sys.stderr.flush()            
        rc = res.returncode
       
    except OSError, err:
        print >> sys.stderr, ('An error occurred while initiating the Job Script.')        

else:
    print "start.py: No #! line detected in Job Script, defaulting to Python."
    try:
        command = [python_path] + [job_script] + argsUnescaped
        if Debug:
            print "start.py: executing:"  
            print command  

        sys.stdout.flush()            
        sys.stderr.flush()            
        res = subprocess.Popen(command, shell=False)
        res.communicate()
        sys.stdout.flush()            
        sys.stderr.flush()            
        rc = res.returncode
 
    except OSError, err:
        print >> sys.stderr, ('An error occurred while initiating the Job Script.')
       
if Debug:
    print "start.py: rc : " + str(rc)  
    
sys.stdout.flush()
sys.stderr.flush()
# return the exit code from application script
sys.exit(rc)
