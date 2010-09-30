"""This package adds extensions to portal_catalog.
"""
from Acquisition import aq_inner
from sd.common.interfaces.providers import IImageContentProvider
from Products.ATContentTypes.interface.image import IImageContent
from Products.ATContentTypes.interface.image import IPhotoAlbumAble
from zope.interface import providedBy


def hasImageAndCaption(object, portal, **kw):
    """This indexable attribute is made to avoid the awakening of the
    object while needing to know if the supposedly attached image exists
    or not. It's very useful for the summary views or other kind of listings.
    """
    if (not IImageContent.providedBy(object) and
        not IPhotoAlbumAble.providedBy(object)):
        adapted = IImageContentProvider(object, None)
        if adapted is None:
            return None
        else:
            sub_path = adapted.sub_path
            image = adapted.getImage()
    else:
        sub_path = "image"
        image = object.getImage()
    
    if image:
        caption = getattr(aq_inner(object), "getImageCaption", None)
        return {'image': True,
                'sub_path': sub_path,
                'caption': caption and caption() or None}
    else:
        return {'image': False, 'caption': None, 'sub_path': None}


