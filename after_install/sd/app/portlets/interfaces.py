# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.schema import Dict, TextLine
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.publisher.interfaces.browser import IBrowserPublisher


class IImageUpdatedEvent(IObjectModifiedEvent):
    """Triggered on an image creation or modification
    """
    
class IImageMiniaturizer(Interface):
    """Defines an ImageMiniaturizer, a handy adapter that has
    for mission to generate, store, and retrieve thumbnails on
    a given object.
    """    
    annotation_prefix = TextLine(title=u"Thumbnails size",
                                 description=u"List of thumbnails size",
                                 default=u'thumbnails',
                                 required=True)
    
    thumbnails_scales = Dict(title=u"Prefix of thumbnails",
                             description=u"Prefix of thumbnails",
                             default= {'large'  : (700, 700),
                                       'preview': (400, 400),
                                       'mini'   : (250, 250),
                                       'thumb'  : (150, 150),
                                       'small'  : (128, 128)},
                             required=True)


    def generate_thumbnails(fieldname):
        """Generates a set of thumbnail from the image located
        on the context and with the given name.
        """

    def retrieve_thumbnail(scale, fieldname):
        """Retrieves the thumbnail with the given scale  of the
        given field on the context. 
        """


class IThumbnailWrapper(IBrowserPublisher):
    """A wrapper around a binary data, representing an image thumbnail
    """
    def __call__():
        """Return the thumbnail raw data with the
        correct HTTP response header.
        """
