#!/usr/bin/python

import sys
import os

if '__file__' in dir(): 
	script_dir=os.path.basename(__file__);
if not script_dir=="": 
	sys.path.append(script_dir);

import taskManage;
import cmdGen;
import template
from template import * 

cmd_obj=cmdGen.cmdGen(); 
print template_table['Optistruct']
cmd_obj.update_template(template_table['Optistruct'])
cmd_obj.update_data_table('PAS_EXECUTABLE', 'optistruct')
cmd_obj.update_data_table('NCPUS', '10' )


print cmd_obj.cmd_gen();
