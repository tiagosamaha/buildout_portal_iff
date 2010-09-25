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
from iff.theme.browser.interfaces import (IHeaderFocusViewletManager,
                                          IThemeSpecific,)
from iff.theme.browser.viewletmanager import HeaderFocusViewletManager

class ImageViewletTestCase(FunctionalTestCase):


    def getMainView(self, content=None):
        context = content
        request = context.REQUEST
        alsoProvides(request,IThemeSpecific)
        view = getMultiAdapter((context,request),name="plone")
        return view

    def getFocusViewletManager(self):
        view = self.getMainView(self.portal)
        request = self.portal.REQUEST
        alsoProvides(request,IThemeSpecific)
        klass = ViewletManager("iff.headerfocus",
                               IHeaderFocusViewletManager,
                               bases=(HeaderFocusViewletManager,))
        manager = klass(self.portal,request,view)
        return manager


    def test_IfImageFocusViewletIsRendered(self):
        request = self.portal.REQUEST
        alsoProvides(request,IThemeSpecific)
        context = self.portal
        viewlet = ImageFocusViewlet(context, request, None, None)
        viewlet.update()
        try:
            viewlet.render()
        except Exception:
            self.fail("viewlet itself has a error!!")

    def test_IfImageNotRenderedinAnotherContext(self):
        request = self.folder.REQUEST
        context = self.folder
        self.failUnlessRaises(ComponentLookupError,getMultiAdapter,
                              (request,context,None,None),
                              name="iff.imagefocus")


    def test_IfViewletisRenderedByTheMainPage(self):
        request = self.portal.REQUEST
        context = self.portal
        alsoProvides(request,IThemeSpecific)
        view = self.getMainView(context)
        viewletmanager = self.getFocusViewletManager()
        viewlet = queryMultiAdapter((context,request,view,viewletmanager),
                                  name="iff.imagefocus")

        self.assertNotEquals(viewlet,None,"There isn't a image viewlet registered")
        viewlet.update()
        try:
            viewlet.render()
        except Exception:
            self.fail("Viewlet invoked throught the viewletmanager has any error!")


def test_suite():
    return unittest.makeSuite(ImageViewletTestCase)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
