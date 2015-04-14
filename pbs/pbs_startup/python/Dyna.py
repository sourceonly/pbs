#!/usr/bin/python 
import sys
sys.path.append('./runtime');
import taskManage


def dyna_smp ( ) : 
	dyna_smp=taskManage.taskManage();
	dyna_smp.cmd_template=['@DYNA_SMP@',"i=@KEY_FILE@","?@EXTRA_OPTION@"]; 
	dyna_smp.para['DYNA_SMP']='/usr/local/bin/optistruct'
	dyna_smp.para['KEY_FILE']='abc'
	dyna_smp.para['EXTRA_OPTION']=' aa bb cc'
	cmd=dyna_smp.make_cmd(dyna_smp.cmd_template);
	print cmd

dyna_smp()



def dyna_mpp(): 
	dyna_mpp=taskManage.taskManage();
	dyna_mpp.cmd_template=['@MPI_RUN@','-np @NCPUS@','-hostlist @HOSTLIST@','@DYNA_MPP@','-i=@KEY_FILE@','?-mem=@MEM1@','?-mem2=@MEM2@','?@EXTRA_OPTION@'];
	
