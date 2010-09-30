# -*- coding: utf-8 -*-

from file import FileField


class ImageField(FileField):
    """A field for representing an image.
    """

    def __init__(self, preferred_dimensions=None, **kw):
        super(ImageField, self).__init__(**kw)
        self.preferred_dimensions = preferred_dimensions
    
