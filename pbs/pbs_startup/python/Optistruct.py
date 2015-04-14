#!/usr/bin/python 
import sys
sys.path.append('./runtime');
import taskManage

cmd_template=['@OPTISTRUCT@','-len @MEM@','?-cpu @NCPUS@','@FEM_FILE@', '?@EXTRA_OPTION@'];
para_list={};
para_list['OPTISTRUCT']='/usr/local/bin/optistruct'
para_list['MEM']='100mb'
para_list['FEM_FILE']='a.fem'

optistruct=taskManage.taskManage(); 
optistruct.run_app(cmd_template,para_list);


sys.exit(optistruct.rc);
