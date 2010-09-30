# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute
from sd.common.adapters.storage.interfaces import IStorageItem


class IConfigurationSheetType(Interface):
    """A configuration sheet profile.
    """

class IConfigurationSheet(IStorageItem):
    """A configuration sheet.
    """
