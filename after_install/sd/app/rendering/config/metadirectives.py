# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from zope.configuration import fields as configuration_fields


class IRendererConfigurationDirective(Interface):

    name = schema.TextLine(
        title=u"Name",
        required=True)
    
    sheet = configuration_fields.GlobalObject(
        title=u"The class used for the configuration sheet.",
        required=True)

    schema = configuration_fields.GlobalInterface(
        title=u"The schema for the configuration sheet",
        required=True)
