#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

import iff.theme


@onsetup
def setup_iff_theme():
    ztc.installProduct("PloneSlideShow")
    ztc.installProduct("CMFPublicator")
    ztc.installPackage("vaporisation")
    fiveconfigure.debug_mode = True
    ztc.installPackage(iff.theme)
    fiveconfigure.debug_mode = False

setup_iff_theme()
ptc.setupPloneSite(products=['iff.theme'])

class TestCase(ptc.PloneTestCase):
    """"""
    pass

class FunctionalTestCase(ptc.FunctionalTestCase):
    """"""
    pass


