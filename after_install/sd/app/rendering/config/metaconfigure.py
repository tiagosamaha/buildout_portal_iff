# -*- coding: utf-8 -*-

from sd.config.register import registerConfigurationSheetType


def configurationSheetDirective(_context, name, sheet, schema):
    """Register a chapter renderer.
    """
    registerConfigurationSheetType(_context, name, sheet, schema)
