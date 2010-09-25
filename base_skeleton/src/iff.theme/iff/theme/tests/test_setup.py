#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from iff.theme.tests.base import TestCase
from Products.CMFPlone.utils import getToolByName
import unittest

class SetupTestCase(TestCase):

    def test_IfThemeIsInstalled(self):
        portal_skins = getToolByName(self.portal,'portal_skins')
        theme_layer = portal_skins.getSkinPath('IFF Theme')
        self.assertTrue('iff_theme_custom_templates' in theme_layer)
        self.assertEquals('IFF Theme', portal_skins.getDefaultSkin())

    def test_IsLayoutAvaliable(self):
        available_layouts = self.portal.getAvailableLayouts()
        layout_ids = [layout[0] for layout in available_layouts]
        self.assertTrue('home' in  layout_ids )

    def test_IsDependenciesInstalled(self):
        installer = self.portal.portal_quickinstaller
        self.assertTrue(installer.isProductInstalled("PloneSlideShow"))
        self.assertTrue(installer.isProductInstalled("CMFPublicator"))
        self.assertTrue(installer.isProductInstalled("vaporisation"))

def test_suite():
    return unittest.makeSuite(SetupTestCase)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
