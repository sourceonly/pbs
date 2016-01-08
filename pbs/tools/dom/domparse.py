

from xml.dom import minidom
from xml.dom.minidom import parse, parseString
def get_app_fullpath (appname) :
    base_dir="/var/spool/pas/repository/applications/"
    app_dir=appname
    app_input="/app-inp-" + appname + ".xml"
    return base_dir + app_dir + app_input

def parse_dom (appname):
    full_path=get_app_fullpath(appname);
    return parse(full_path);

def get_option_parent_node (doc) :
    option_nodes=doc.getElementsByTagName('Option')
    parent_list=[];
    for n in option_nodes:
        parent_list.append(n.parentNode);
    return list(set(parent_list))


def get_option_value (option_nodes):
    return str(option_nodes.childNodes[0].nodeValue) if option_nodes.childNodes else ''

def get_replace_option_node (doc) :
    option_nodes=doc.getElementsByTagName('Option')
    parent_list=[];
    for n in option_nodes:
        if ( get_option_value(n) == 'replacement_options' ) :
            parent_list.append(n.parentNode);
    return list(set(parent_list))
def get_type_name (argnode):
    for n in argnode.childNodes:
        if n.nodeType!=1:
            continue
        if str(n.tagName)=='Name': 
            return get_option_value(n)
    return '';

def get_input_require (argnode):
    for n in argnode.childNodes:
        if n.nodeType!=1:
            continue
        if str(n.tagName)=='InputRequired': 
            return get_option_value(n)
    return '';
def get_type_option (argnode):
    return_var=[];
    for n in argnode.childNodes:
        if n.nodeType!=1:
            continue
        if str(n.tagName) == 'Option':
            return_var.append(get_option_value(n))
    return return_var
        

def get_name_value_checklist (doc) :
    node_all=get_option_parent_node (doc);
    node_to_skip=get_replace_option_node(doc);
    check_list_all=[];
    for n in node_all:
        if n in node_to_skip :
            continue
        name=get_type_name(n);
        type=get_type_option(n);
	input_require=get_input_require(n);
        if input_require=='false':
		continue
        item=[name,type];
        check_list_all.append(item);
    return check_list_all
        
def checkInputList (dict,key,ref_list): 
    return dict[key] in ref_list;
def checkInputInt (dict, key, low, up) :
    return (int(dict [key]) <= up and int(dict [key]) >= low)

def get_bound_parent_node (doc):
    up_nodes=doc.getElementsByTagName('UpperBound')
    low_nodes=doc.getElementsByTagName('LowerBound')
    parent_list=[];
    for n in up_nodes:
        parent_list.append(n.parentNode);
    for n in low_nodes:
        parent_list.append(n.parentNode);

    return list(set(parent_list))



def get_type_upper (argnode):
    for n in argnode.childNodes:
        if n.nodeType!=1:
            continue
        if str(n.tagName) == 'UpperBound':
            return int(get_option_value(n))
    return 1000000000000000

def get_type_lower (argnode):
    
    for n in argnode.childNodes:
        if n.nodeType!=1:
            continue
        if str(n.tagName) == 'LowerBound':
            return int(get_option_value(n));
    return 0


def get_name_value_checkbound (doc): 
    node_all=get_bound_parent_node(doc);
    check_bound_all=[];
    for n in node_all: 
        name=get_type_name(n);
        up=get_type_upper(n);
        low=get_type_lower(n);
        item=[name,up,low];
        check_bound_all.append(item);
    return check_bound_all;


def check_app_option (appname,dict) : 
    doc=parse_dom(appname);
    check_list=get_name_value_checklist(doc);
    check_pass=1;
    for icheck in check_list :
        key=icheck[0];
        ref_list=icheck[1];
        check_pass=check_pass and checkInputList(dict,key,ref_list)
    return check_pass
    
def check_app_bound (appname,dict):
    doc=parse_dom(appname);
    check_list=get_name_value_checkbound(doc);
    check_pass=1;
    for icheck in check_list :
        key=icheck[0];
        up=icheck[1];
        low=icheck[2];
        check_pass=check_pass and checkInputInt(dict,key,low,up);
    return check_pass


def parse_test (file):
    return parse(file)


userInputs={}
userInputs['ITERATION']='2000'
userInputs['MEMORY']='1000'
userInputs['PLACEMENT']='free'
userInputs['PLACEMODE']='shared'
#userInputs['PRECISION']='Single'
userInputs['PRECISION']='abcd'
userInputs['DIMENSION']='3d'
userInputs['HOSTS']=10000
userInputs['CORES']=8
userInputs['MPI_TYPE']='smp'
userInputs['QUEUE']='Normal'
userInputs['CONNECT_ENABLED']='fakldjfa'
print "checkStringEnum= " 
print check_app_option('Fluent-journal',userInputs)
print "checkInt=" 
print check_app_bound('Fluent-journal',userInputs)
    
