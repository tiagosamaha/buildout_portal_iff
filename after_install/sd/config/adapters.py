# -*- coding: utf-8 -*-

from zope.component import adapts
from sd.common.fields.annotation import AdapterAnnotationProperty
from sd.contents.interfaces import IStructuredItem
from sd.common.adapters.storage.annotation import GenericAnnotationStorage
from sd.common.adapters.storage.interfaces import IDictStorage


class ConfigurationStorage(GenericAnnotationStorage):
    """
    """
    adapts(IStructuredItem)
    
    storage = AdapterAnnotationProperty(
        IDictStorage['storage'],
        ns="sd.contextual.configuration"
        )
