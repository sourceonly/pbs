#!/usr/bin/python 

import taskManage
A=taskManage.taskManage();
A.para['NCPUS']=10
A.para['OPTISTRUCT']='optitruct'
A.para['FEM_FILE']='test.fem'
A.para['MEM']='100mb'
print A.make_cmd("@OPTISTRUCT@ -np @NCPUS@ ?-mem=@MEM@ -input @FEM_FILE@")

print A.eval_cmd("sleep @NCPUS@",True)
#print A.run_cmd("sleep 100")
print A.eval_cmd("ls -al")


