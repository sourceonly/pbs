

import pbs 
import os


j=pbs.event().job

f1=open("/tmp/abc","w");
for i in dir(j): 
	f1.write(i);
	f1.write("\n");
f1.write('---')
for i in dir(e):
	f1.write(i);
	f1.write("\n");



f1.write("=======\n")

if  type(j.Job_Owner)==None :
	f1.write("123")

f1.write(e.requestor)

f1.close();

