# -*- coding: utf-8 -*-
from zope.interface import implements
from plone.app.portlets.portlets.base import Assignment
from interfaces import IVaporizedCloud, ICustomizableCloud, ISteamer


class Cloud( Assignment ):
    """ The tagcloud itself """

    implements( IVaporizedCloud, ICustomizableCloud )

    # Tag storage
    keywords = list()
    all_keys = list()
    tagsTree = dict()

    # Weight
    highest  = 0
    lowest   = 0

    # Customization
    name     = u""
    steps    = 10
    joint    = True
    limit    = 0
    restrict = tuple()

    def __init__(self, name=u"", steps=10, joint=True, limit=0, restrict=()):
        self.name = name
        self.steps = steps
        self.joint = joint
        self.limit = limit
        
    @property
    def title(self):
        """ The title property for the menus. """
        return self.name
