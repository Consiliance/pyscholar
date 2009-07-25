#!/usr/bin/python
import yaml

class Nature(yaml.YAMLObject):
    yaml_tag='!nature'
    def __init__(self):
        pass
    def yaml_repr(self):
        pass
    def __repr__(self):
        return "nature object"
 
class ScienceDirect(yaml.YAMLObject):
    yaml_tag='!sciencedirect'
    def __init__(self):
        pass
    def yaml_repr(self):
        pass
    def __repr__(self):
        return "sciencedirect object"

