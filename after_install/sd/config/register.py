# -*- coding: utf-8 -*-

from zope.component import getSiteManager
from zope.interface import Interface, Attribute
from persistent import Persistent
from interfaces import IConfigurationSheetType
from zope.component.factory import Factory


class ConfigurationGenerator(Persistent):
    """A configuration sheet registration.
    """
    name = Attribute("The name of the targeted renderer.")
    schema = Attribute("The schema of the configuration sheet.")

    def __init__(self, name, sheet, schema):
        self.name = name
        self.schema = schema
        self.factory = Factory(sheet, title=u"Generate a new config sheet.")

    def configurationFactory(self):
        return self.factory(self.name)


def registerConfigurationSheetType(site, name, sheet, schema):
    """
    """
    sm = getSiteManager(site)
    util = ConfigurationGenerator(name, sheet, schema)  
    sm.registerUtility(component=util,
                       provided=IConfigurationSheetType,
                       name=name)
