#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import os
import sys
import redis

sys.path.append(os.environ['AIL_BIN'])
##################################
# Import Project packages
##################################
from lib.ConfigLoader import ConfigLoader

config_loader = ConfigLoader()

config_loader = None

def get_ail_uuid():
    pass

#### AIL OBJECTS ####

# # TODO: check change paste => item
def get_all_objects():
    return ['domain', 'item', 'pgp', 'cryptocurrency', 'decoded', 'screenshot', 'username']

def get_object_all_subtypes(obj_type):
    if obj_type == 'cryptocurrency':
        return ['bitcoin', 'bitcoin-cash', 'dash', 'ethereum', 'litecoin', 'monero', 'zcash']
    if obj_type == 'pgp':
        return ['key', 'mail', 'name']
    if obj_type == 'username':
        return ['telegram', 'twitter', 'jabber']

##-- AIL OBJECTS --##
