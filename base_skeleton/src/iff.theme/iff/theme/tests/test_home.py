#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest

from Products.CMFPlone.utils import getToolByName
from Products.Five.testbrowser import Browser

from iff.theme.tests.base import FunctionalTestCase

class HomeAccessTestCase(FunctionalTestCase):

    def test_access_HomePage(self):
        browser = Browser()
        browser.handleErrors = False
        browser.open("http://nohost/plone")
        status = browser.headers['status']
        self.assertEquals("200 OK", status )


def test_suite():
    return unittest.makeSuite(HomeAccessTestCase)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
