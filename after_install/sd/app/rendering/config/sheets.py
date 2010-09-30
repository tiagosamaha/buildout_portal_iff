# -*- coding: utf-8 -*-

from OFS.SimpleItem import SimpleItem
from zope.schema.fieldproperty import FieldProperty
from zope.interface import implements
from interfaces import *


class BaseConfigSheet(SimpleItem):
    
    def __init__(self, name):
        self.name = name


class EnhancedPhotoAlbumConfig(BaseConfigSheet):
    implements(IEnhancedPhotoAlbumConfig)
    name  = FieldProperty(IEnhancedPhotoAlbumConfig['name'])
    timer = FieldProperty(IEnhancedPhotoAlbumConfig['timer'])
