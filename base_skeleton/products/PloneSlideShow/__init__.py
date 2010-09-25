from Products.CMFCore.DirectoryView import registerDirectory
from config import SKINS_DIR, GLOBALS, PROJECTNAME, PORTAL_TYPE

skin_globals=globals()
registerDirectory(SKINS_DIR, GLOBALS)
