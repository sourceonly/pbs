#!/usr/bin/python


import pbs_tools
A=pbs_tools.pbs_tools();

#p=A.get_node_table();
#print p
#a,b=A.pbsnodes();
#print a


print A.pbsnodes_table
print 'gn01' in A.pbsnodes_table

