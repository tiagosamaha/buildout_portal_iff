# -*- coding: utf-8 -*-

from PIL import Image
from cStringIO import StringIO
from Acquisition import Explicit

from zope.component import adapts
from zope.interface import implements
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.interfaces import ITraversable
from zope.annotation.interfaces import IAnnotations
from zope.publisher.interfaces import NotFound
from zope.schema.fieldproperty import FieldProperty

from blocks.interfaces import IStructuredIllustratedBlock
from interfaces import IThumbnailWrapper, IImageMiniaturizer


class AssignmentThumbnailsHandler(object):
    """This adapter is an implementation of an IImageMiniaturizer.
    Adapting a portlet assignment, it will simply generate a set of
    thumbnails and write them on an annotation. The annotation key
    depends on the field name.
    """
    implements(IImageMiniaturizer)
    adapts(IStructuredIllustratedBlock)

    annotation_prefix = FieldProperty(IImageMiniaturizer['annotation_prefix'])
    thumbnails_scales = FieldProperty(IImageMiniaturizer['thumbnails_scales'])

    def __init__(self, context):
        self.context = context

    def generate_thumbnails(self, fieldname='image'):
        """Generates a set of thumbnails from the available
        sizes and stores them in an annotation.
        """
        original = getattr(self.context, fieldname, None)
        if not original:
            return False
        
        an_key = "%s.%s" % (self.annotation_prefix, fieldname)
        thumbs = dict()

        for format, size in self.thumbnails_scales.iteritems():
            data = StringIO(str(original))
            image = Image.open(data)
            image.thumbnail(size, Image.ANTIALIAS)
            tfd = StringIO()
            image.save(tfd, image.format, quality=90)
            thumbs[format] = tfd.getvalue()

        an = IAnnotations(self.context)
        an[an_key] = thumbs
        return True


    def delete_thumbnails(self, fieldname='image'):
        """Deletes the thumbnails of the given field
        """
        an = IAnnotations(self.context)
        an_key = "%s.%s" % (self.annotation_prefix, fieldname)
        an[an_key] = None


    def retrieve_thumbnail(self, scale, fieldname='image'):
        """Grabs the thumb from its scale name
        """
        image = getattr(self.context, fieldname, None)
        
        if image:
            an = IAnnotations(self.context)
            an_key = "%s.%s" % (self.annotation_prefix, fieldname)
            thumbnails = an.get(an_key, None)
            if thumbnails is not None and scale in thumbnails:
                return thumbnails[scale]
            
        return None


class ThumbnailWrapper(Explicit):
    """A class that masquarades an image, in order to access
    thumbnails of a given context.
    """
    implements(IThumbnailWrapper)

    def __init__(self, context, request, data, fieldname='image'):
        self.context = context
        self.request = request

        # internal data
        self._data = data
        self._fieldname = fieldname
        
        # contextual positionning
        self.__parent__ = context


    def browserDefault(self, request):
        return self, ()


    def __call__(self):
        response = self.request.response
        image = getattr(self.context, self._fieldname, None)
        if not image:
            raise NotFound(self.context, self._fieldname, self.request)
        content_type = image.get('content_type', 'image/jpeg')
        response.setHeader('Content-Type', content_type)
        return self._data


class PortletThumbnailsTraverser(object):
    """A traverser that is involved while traversing
    a portlet implementing IStructuredIllustratedBlock.
    It's merely a namespace traverser, retrieving and
    instanciating an image thanks to an IImageMiniaturizer.
    """
    implements(ITraversable)
    adapts(IStructuredIllustratedBlock, IHTTPRequest)
    
    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        
        handler = IImageMiniaturizer(self.context, None)

        try:
            fieldname, scale = name.split('.')
        except ValueError:
            raise NotFound(self.context, name, self.request)
            
        scale = handler.retrieve_thumbnail(scale, fieldname=fieldname)
        if scale is not None:
            return ThumbnailWrapper(self.context,
                                    self.request,
                                    scale).__of__(self.context)
        
        raise NotFound(self.context, name, self.request)
