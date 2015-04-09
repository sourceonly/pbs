import time, os, sys, re

shell_script    = os.environ['HOST_SNIFFER']
python_path     = os.environ['PBS_PYTHON_PATH']

# TODO: Standardize job script line endings for better multiplaform/editor compatibility.

file = open( shell_script, 'r' )
line = file.readline()
file.close()

if line.startswith('#!'):
    try:
        interpreter = re.match( '^#!(.*)', line ).group(1)

        os.system( '%s %s' % ( interpreter, shell_script ) )

    except OS.Error:
        print >> sys.stderr, ('An error occurred while initiating your Shell Script.')
else:
   try:
        print >> sys.stdout, ('No #! line detected in Job Script, defaulting to Python.')
        os.system( '%s %s' % ( python_path, shell_script ) )

   except OS.Error:
        print >> sys.stderr, ('An error occurred while initiating your Job Script.')


