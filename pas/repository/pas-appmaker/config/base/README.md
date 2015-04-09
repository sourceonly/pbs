# pas-appmaker/config/base/README

A framework for creating powerful application definitions.

## Base

    pas-appmaker/config/base

Modifying the Base files directly is not advised. However, in advanced cases where some customization of these files is required to satisfy customer specific needs, use the pas-appmaker Templating files. The easiest way is to copy the Base files you'd like to customize into `$PAS_APP_CONFIG/templates/` and make your modifications there. pas-appmaker checks for Template files first before eventually looking for Base files.

### Input Files

    pas-appmaker/config/base/app-inp.xml
    pas-appmaker/config/base/app-conv.xml
    pas-appmaker/config/base/input.py

### Submit Files

    pas-appmaker/config/base/presubmit.py
    pas-appmaker/config/base/postsubmit.py

### Start Files
    
    pas-appmaker/config/base/start.py

### Actions Files

    pas-appmaker/config/base/app-actions.xml    
    pas-appmaker/config/base/actions.py

### Exit Files

    pas-appmaker/config/base/exit.py
    
### External Scripts (No Template Support)

    pas-appmaker/config/base/include_parser.py
    pas-appmaker/config/base/qlaunch.sh
    pas-appmaker/config/base/rcheck.pl

## Copyright

(c) Copyright 2013 - 2014 Altair Engineering, Inc. All rights reserved.
