# -*- coding: utf-8 -*-

from zope.component import adapts, queryUtility, getMultiAdapter
from zope.interface import implements
from sd.contents.interfaces import IStructuredItem
from sd.common.adapters.storage.interfaces import IStorage
from sd.config.interfaces import IConfigurationSheetType
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.interfaces import ITraversable
from zope.annotation.interfaces import IAnnotations
from zope.publisher.interfaces import NotFound


class ConfigurationTraverser(object):
    """A traverser that is involved while traversing to a renderer
    configuration sheet.
    """
    implements(ITraversable)
    adapts(IStructuredItem, IHTTPRequest)
    
    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):

        utility = queryUtility(IConfigurationSheetType, name, None)

        if utility is None:
            raise NotFound(self.context, name, self.request)

        configuration = IStorage(self.context).retrieve(name)
        if configuration is None:
            view = getMultiAdapter((self.context, self.request),
                                   name = u"sd.configuration.create")
            view.id = name
            return view
        return getMultiAdapter((configuration, self.request),
                                 name = u"edit")
        
        
