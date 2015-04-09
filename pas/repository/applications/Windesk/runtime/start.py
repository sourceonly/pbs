import time, os, sys, re, subprocess

Debug = False 

job_script      = os.path.basename(os.environ['JOB_SCRIPT'])
job_args        = os.environ['JOB_ARGS']
python_path     = os.environ['PYTHONPATH']

# TODO: Standardize job script line endings for better multiplaform/editor compatibility.

job_script = job_script.replace('%20',' ')
if Debug:
    print "start.py: script: " + job_script  

file = open( job_script, 'r' )
line = file.readline()
file.close()

argsUnescaped = []
rc = 0
if (len(job_args)>0):

    args = job_args.split(' ')
    for arg in args:
        if (arg.strip()):
            arg = arg.replace('%20',' ')
            argsUnescaped.append(arg) 

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