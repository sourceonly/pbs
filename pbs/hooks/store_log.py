#!/usr/bin/python
import pbs 
import os 
import sys
sys.path+=['', '/opt/pbs/default/python/lib/python25.zip', '/opt/pbs/default/python/lib/python2.5', '/opt/pbs/default/python/lib/python2.5/plat-linux2', '/opt/pbs/default/python/lib/python2.5/lib-tk', '/opt/pbs/default/python/lib/python2.5/lib-dynload', '/opt/pbs/default/python/lib/python2.5/site-packages']
import subprocess
import re


e=pbs.event();
j=e.job; 

path=pbs.server().resources_available['store_path']



os.system('/usr/bin/scp ' + '/var/spool/PBS/spool/' + j.id+'.OU'+ ' '  + path);
os.system('/usr/bin/scp ' + '/var/spool/PBS/spool/' + j.id+'.ER'+ ' '  + path);




f=open("/tmp/hooks","w")
#for i in dir(pbs.server()) : 
#	f.write("%s\n" % i);
f.write(repr(pbs.server().resources_available['store_path']))
#f.write(j.Error_Path)
#f.write(j.Output_Path)

f.write('/usr/bin/scp ' + '/var/spool/PBS/spool/' +j.id+'.OU'+ ' '  + path);
f.write('/usr/bin/scp ' + '/var/spool/PBS/spool/' +j.id+'.ER'+ ' '  + path);


f.close();

