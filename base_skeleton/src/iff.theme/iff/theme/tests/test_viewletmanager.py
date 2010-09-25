#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from iff.theme.tests.base import TestCase
from iff.theme.browser.viewlets import NewsFocusViewlet
from iff.theme.browser.interfaces import IHeaderFocusViewletManager
from iff.theme.browser.viewletmanager import HeaderFocusViewletManager
from Products.CMFPlone.utils import getToolByName
from Products.Five.viewlet.manager import ViewletManager
from zope.component import getMultiAdapter, ComponentLookupError, getAdapters
import unittest


class RenderTestCase(TestCase):

    def test_ViewletManagerRender(self):
        portal = self.portal
        request = portal.REQUEST
        viewlet_manager_klass = ViewletManager(
                'iff.HeaderFocusViewletManager',
                IHeaderFocusViewletManager,
                bases=(HeaderFocusViewletManager,))
        view = getMultiAdapter((portal, request), name="view")
        manager = viewlet_manager_klass(portal, request, view)
        manager.update()
        self.assertEquals(manager.render(),u'')

def test_suite():
    return unittest.makeSuite(RenderTestCase)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
