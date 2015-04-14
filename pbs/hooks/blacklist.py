

'''
format 
/tmp/blacklist
username1: queue1,queue2, ...
username2: queueN, queue(N+1), ...

'''
import pbs 
import os

file='/tmp/blacklist'
user_list={};

f=open(file,"r");


for i in f.readlines(): 
	user_name_list=i.strip("\n").split(":");
	user_name=user_name_list[0];
	queue_list=user_name_list[1].split(",");
	user_list[user_name]=queue_list;
f.close();

	



e=pbs.event();
j=e.job;
q=j.queue;
queue_name=q.name
owner=e.requestor;

if not queue_name: 
	queue_name="iworkq" 


if user_list.has_key(owner): 
	if queue_name in user_list[owner]: 
		e.reject( "black list:  user " + owner + " is blacklisted in " + queue_name);

#if owner in queue_table[queue_name] : 
#	e.reject("black list")


#if owner in user_list: 
#	e.reject("black list")


