#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import os
import sys
import re

from flask import url_for
from pymisp import MISPObject

sys.path.append(os.environ['AIL_BIN'])
##################################
# Import Project packages
##################################
from lib import ail_core
from lib.ConfigLoader import ConfigLoader
from lib.objects.abstract_subtype_object import AbstractSubtypeObject, get_all_id

config_loader = ConfigLoader()
baseurl = config_loader.get_config_str("Notifications", "ail_domain")
config_loader = None


################################################################################
################################################################################
################################################################################

class UserAccount(AbstractSubtypeObject):
    """
    AIL User Object. (strings)
    """

    def __init__(self, id, subtype):
        super(UserAccount, self).__init__('user-account', id, subtype)

    # def get_ail_2_ail_payload(self):
    #     payload = {'raw': self.get_gzip_content(b64=True),
    #                 'compress': 'gzip'}
    #     return payload

    # # WARNING: UNCLEAN DELETE /!\ TEST ONLY /!\
    def delete(self):
        # # TODO:
        pass

    def get_link(self, flask_context=False):
        if flask_context:
            url = url_for('correlation.show_correlation', type=self.type, subtype=self.subtype, id=self.id)
        else:
            url = f'{baseurl}/correlation/show?type={self.type}&subtype={self.subtype}&id={self.id}'
        return url

    def get_svg_icon(self): # TODO change icon/color
        if self.subtype == 'telegram':
            style = 'fab'
            icon = '\uf2c6'
        elif self.subtype == 'twitter':
            style = 'fab'
            icon = '\uf099'
        else:
            style = 'fas'
            icon = '\uf007'
        return {'style': style, 'icon': icon, 'color': '#4dffff', 'radius': 5}

    def get_first_name(self):
        return self._get_field('firstname')

    def get_last_name(self):
        return self._get_field('lastname')

    def get_phone(self):
        return self._get_field('phone')

    def set_first_name(self, firstname):
        return self._set_field('firstname', firstname)

    def set_last_name(self, lastname):
        return self._set_field('lastname', lastname)

    def set_phone(self, phone):
        return self._set_field('phone', phone)

    # TODO REWRITE ADD FUNCTION

    def get_username(self):
        return ''

    def get_usernames(self):
        usernames = []
        correl = self.get_correlation('username')
        for partial_id in correl.get('username', []):
            usernames.append(f'username:{partial_id}')
        return usernames

    def get_meta(self, options=set()):
        meta = self._get_meta(options=options)
        meta['id'] = self.id
        meta['subtype'] = self.subtype
        meta['tags'] = self.get_tags(r_list=True)
        if 'username' in options:
            meta['username'] = self.get_username()
        if 'usernames' in options:
            meta['usernames'] = self.get_usernames()
        return meta

    def get_misp_object(self):
        obj_attrs = []
        if self.subtype == 'telegram':
            obj = MISPObject('telegram-account', standalone=True)
            obj_attrs.append(obj.add_attribute('username', value=self.id))

        elif self.subtype == 'twitter':
            obj = MISPObject('twitter-account', standalone=True)
            obj_attrs.append(obj.add_attribute('name', value=self.id))

        else:
            obj = MISPObject('user-account', standalone=True)
            obj_attrs.append(obj.add_attribute('username', value=self.id))

        first_seen = self.get_first_seen()
        last_seen = self.get_last_seen()
        if first_seen:
            obj.first_seen = first_seen
        if last_seen:
            obj.last_seen = last_seen
        if not first_seen or not last_seen:
            self.logger.warning(
                f'Export error, None seen {self.type}:{self.subtype}:{self.id}, first={first_seen}, last={last_seen}')

        for obj_attr in obj_attrs:
            for tag in self.get_tags():
                obj_attr.add_tag(tag)
        return obj

def get_user_by_username():
    pass

def get_all_subtypes():
    return ail_core.get_object_all_subtypes('user-account')

def get_all():
    users = {}
    for subtype in get_all_subtypes():
        users[subtype] = get_all_by_subtype(subtype)
    return users

def get_all_by_subtype(subtype):
    return get_all_id('user-account', subtype)


# if __name__ == '__main__':
#     name_to_search = 'co'
#     subtype = 'telegram'
#     print(search_usernames_by_name(name_to_search, subtype))
