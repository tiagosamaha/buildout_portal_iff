# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent
from interfaces import ITreeUpdateEvent, ISteamer


class TreeUpdateEvent(ObjectModifiedEvent):
    """ We need to rebuild the tree from here
    """
    implements(ITreeUpdateEvent)


def UpdateTreeOnCloudChanges(obj, event):
    ISteamer(obj).setTree()
