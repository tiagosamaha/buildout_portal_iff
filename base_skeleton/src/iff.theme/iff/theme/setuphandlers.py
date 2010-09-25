import logging

from iff.theme.config import DEPENDENCIES
from Products.CMFPlone.utils import getToolByName
from StringIO import StringIO
import transaction

def install_dependencies(portal,out):
    portal = getToolByName(portal,'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    for dependency in DEPENDENCIES:
        print >> out, "Installing dependency %s:" % dependency
        quickinstaller.installProduct(dependency)
        transaction.savepoint()


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('iff.theme_various.txt') is None:
        return
    portal = context.getSite()
    out = StringIO()
    install_dependencies(portal,out)
    logger = context.getLogger('iff.theme.setuphandlers')
    logger.info(out.getvalue())
