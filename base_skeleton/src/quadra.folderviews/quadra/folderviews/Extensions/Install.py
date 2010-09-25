from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-quadra.folderviews:uninstall')
    setup_tool.runAllImportSteps()
    return "Quadra Folderview uninstalled - uninstall profile loaded"
    
