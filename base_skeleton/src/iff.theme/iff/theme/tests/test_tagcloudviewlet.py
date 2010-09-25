#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest

from Products.CMFPlone.utils import getToolByName
from Products.Five.testbrowser import Browser
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.component import ComponentLookupError
from zope.interface import alsoProvides
from Products.Five.viewlet.manager import ViewletManager

from iff.theme.tests.base import FunctionalTestCase
from iff.theme.browser.viewlets import ImageFocusViewlet
from iff.theme.browser.interfaces import IThemeSpecific
from plone.app.layout.viewlets.interfaces import IBelowContent
from iff.theme.browser.viewletmanager import HeaderFocusViewletManager
from plone.app.viewletmanager.manager import OrderedViewletManager
class TagCloudViewletTestCase(FunctionalTestCase):

    def test_Render(self):
        request = self.portal.REQUEST
        alsoProvides(request,IThemeSpecific)
        context = self.portal
        view = getMultiAdapter((context,request), name="plone")
        klass = ViewletManager("plone.belowcontent",
                                        IBelowContent,
                                        bases=(OrderedViewletManager,))
        viewletmanager = klass(context,request,view)
#    viewlet = getMultiAdapter((context, request, view,
#        viewletmanager,),name="iff.newsfocus")
        viewlet = viewletmanager['iff.tagcloud']
        try:
            viewlet.render()
        except Exception,e:
            self.fail("There's a problem with a tagcloudviewlet!")


def test_suite():
    return unittest.makeSuite(TagCloudViewletTestCase)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
