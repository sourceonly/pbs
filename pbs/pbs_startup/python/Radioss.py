#!/usr/bin/python 
import sys
sys.path.append('./runtime');
import taskManage

starter_template=['@RADIOSS_S@', '-input @STARTER@', '-nspmd @STARTER_NCPUS@'];
engine_template=['@MPI_RUN@','-np @NCPUS@','-hostfile @HOSTFILE','?@MPI_ARGS@','@RADIOSS_E@','-input @ENGINE@' ]

para_list={};
para_list['RADIOSS_S']='/usr/local/bin/abc'
para_list['STARTER']='rad0001'
para_list['FEM_FILE']='a.fem'

radioss=taskManage.taskManage(); 

radioss.run_app(starter_template,para_list);


sys.exit(radioss.rc);
