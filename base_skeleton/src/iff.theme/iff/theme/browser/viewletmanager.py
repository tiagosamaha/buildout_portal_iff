from interfaces import IHeaderFocusViewletManager, INewsViewletManager
from Products.Five.viewlet.manager import ViewletManagerBase
from zope import interface


class HeaderFocusViewletManager(ViewletManagerBase):
    interface.implements(IHeaderFocusViewletManager)

class NewsViewletManager(ViewletManagerBase):
    interface.implements(INewsViewletManager)
