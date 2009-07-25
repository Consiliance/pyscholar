#!/usr/bin/python
import os
import yaml
import classes
import __builtin__

##friendly shortcuts
#nature = classes.Nature

metadata = yaml.load_all(open(os.path.join(os.path.dirname(__file__),"metadata.yaml"),"r"))
for each in metadata:
    name = each["name"]
    classes2 = each["classes"]
    #locals()["classes"].__getattribute__("Nature")
    #setattr(__builtin__,name,(locals()["classes"]).__getattribute__(classes2[0]))
    exec "%s = locals()[\"classes\"].__getattribute__(classes2[0])" % (name)
