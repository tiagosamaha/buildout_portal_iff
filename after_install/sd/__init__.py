"""Structured Document base package
"""
PROJECTNAME = "sd"

# i18n
from zope.i18nmessageid import MessageFactory
_ = MessageFactory(PROJECTNAME)

# In Five, Browser, PageTemplateFile, it said to
# disable security. We're doing so.
import Products.Five.browser.pagetemplatefile
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

def _getContext(self):
    while 1:
        self = self.aq_parent
        if not getattr(self, '_is_wrapperish', None):
            return self
        
ZopeTwoPageTemplateFile._getContext = _getContext



