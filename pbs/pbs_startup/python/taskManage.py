#!/usr/bin/python

import re
import os
import sys
import subprocess
class taskManage():
    def __init__ (self):
        self.para={};
        self.snapshot={};
        self.rc=1;
        self.history=[];

    def make_cmd (self, cmd_template):
        cmd=[];
        for i in re.split(r"\s+", cmd_template):
            cmd.append(self.make_word(i));
        return cmd

    def make_word (self, string):
        optional_flag=False;
        key_not_exist_flag=False;
        key_empty_flag=False;
        if string[0]=='?':
            optional_flag=True;
        res_string=re.sub("^\?","",string);
        reg_key=re.compile("@([A-Za-z0-9_\-]+)@");
        while True:
            key_match=reg_key.search(res_string);
            if not key_match:
                break
            key=key_match.group(1);
            replace_key=re.compile("@"+key+"@");
            if not self.para.has_key(key):
                key_not_exist_flag=True;
                res_string=replace_key.sub("",res_string);
            else:
                if str(self.para[key])=='' :
                    key_empty_flag=True;
                res_string=replace_key.sub(str(self.para[key]),res_string);
            
        if optional_flag and key_not_exist_flag:
            return '';
        return res_string;
    
    def eval_cmd (self, cmd_template, bg=False):
        ''' use to snap the stdout of a command
        rc code is stored '''
        
        cmd=self.make_cmd(cmd_template);
        task=subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE);
        self.history.append(cmd);
        if not bg :
            self.rc=task.wait()
            self.comment=task.stderr.read();
            return task.stdout.read();
        return "";

    def run_cmd ( self, cmd_template, bg=False) :
        ''' use to run_cmd,  interactive, all the stdout and stderr are not buffed'''
        cmd=self.make_cmd(cmd_template);
        task=subprocess.Popen(cmd,shell=False);
        task.communicate();
        self.history.append(cmd);
        if not bg :
            self.rc=task.wait();
            return self.rc;
        return 0;


    
    
            
            
            
        
        
