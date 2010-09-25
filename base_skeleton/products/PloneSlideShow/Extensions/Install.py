import logging
logger = logging.getLogger('PloneSlideShow')

from os.path import isdir, join
from os import listdir
from Globals import package_home
from Products.CMFCore.utils import minimalpath, getToolByName
from Products.CMFCore.DirectoryView import manage_listAvailableDirectories, registerDirectory, addDirectoryViews

from cStringIO import StringIO
import string

# CHANGE this to use the name of your product - this will be used to ensure
#  we register a skin directory in the correct context
from Products.PloneSlideShow.config import PROJECTNAME, GLOBALS, PORTAL_TYPE 
from Products.PloneSlideShow.config import SKINS_DIR, SKINNAME
from Products.PloneSlideShow.config import LISTPROPERTIES
skinname = SKINNAME
baseSkin = 'Plone Default'

def install_skins(self, out, globals=GLOBALS, product_skins_dir=SKINS_DIR):

    logger.info('Installing Skin Product')

    out.write('PloneSlideShow Installation on %s\n' % self.id)
    out.write('======================\n\n')

    # Setup the skins
    skinstool=getToolByName(self, 'portal_skins')

    fullProductSkinsPath = join(package_home(globals), product_skins_dir)
    productSkinsPath = minimalpath(fullProductSkinsPath)
    registered_directories = manage_listAvailableDirectories()
    if productSkinsPath+'/SlideShow' not in registered_directories:
        registerDirectory(product_skins_dir+'/SlideShow', globals)
    try:
        addDirectoryViews(skinstool, product_skins_dir, globals)
        out.write("Added %s directory view to portal_skins\n" % skinname)
    except BadRequestException, e: 
       pass  # directory view has already been added
       out.write("%s directory view already existed in portal_skins\n" % skinname)

    # Insert 'SlideShow' and 'SlideShow/skinsJs' into the skin configurations.
    files = listdir(fullProductSkinsPath)
    for productSkinName in files:
        if (isdir(join(fullProductSkinsPath, productSkinName))
            and productSkinName != 'themes'
            and productSkinName != 'CVS'
            and productSkinName != '.svn'):
            for skinName in skinstool.getSkinSelections():
                path = skinstool.getSkinPath(skinName)
                path = [i.strip() for i in  path.split(',')]
                try:
                    if productSkinName not in path:
                        path.insert(path.index('custom') +1, productSkinName)
                except ValueError:
                    if productSkinName not in path:
                        path.append(productSkinName)
                path = ','.join(path)

                # addSkinSelection will replace existing skins as well.
                skinstool.addSkinSelection(skinName, path)
                out.write("Added %s to %s skin\n" % (skinname, skinName))

    path = [p.strip() for p in skinstool.getSkinPath('Plone Default').split(',')]
    path.remove('custom')

def install_resources(self,out):
        """Add the js and css files from the resource registries"""

        logger.info('Installing Resources Product')

	try:
		from Products.ResourceRegistries.config import JSTOOLNAME
		from Products.ResourceRegistries.config import CSSTOOLNAME
	except ImportError:
		print >>out, "Resource registry not found: ploneskins will load its own resources"
		return

	jstool = getToolByName(self, JSTOOLNAME)
	csstool = getToolByName(self, CSSTOOLNAME)

	# Add CSS in resources.
       	print >>out, "Css Instalation completed"
	import pdb; pdb.set_trace()
       	csstool.manage_removeStylesheet(id='slideshow.css')
       	csstool.manage_addStylesheet(id='slideshow.css',
                media='All',
       		expression='',
       		rel='stylesheet',
       		enabled=True,
       		cookable=True)

	# Add JavaScript in resources.
	print >>out, "JavaScripts Instalation completed"
	jstool.manage_removeScript(id='skinsJs/slideshow.js')
	jstool.manage_removeScript(id='skinsJs/openSlide.js')
	jstool.manage_addScript(id='skinsJs/slideshow.js',
                                        expression='',
                                        enabled=True,
                                        cookable=True)
	jstool.manage_addScript(id='skinsJs/openSlide.js',
                                        expression='',
                                        enabled=True,
                                        cookable=True)
        install_configlet(self, out)

def install_configlet(self, out):
    """Added SlideShow the configlet from the portal control panel."""

    logger.info('Installing Configlet Product')

    try:
        portal_conf=getToolByName(self,'portal_controlpanel')
    except AttributeError:
        print >>out, "Configlet could not be installed"
        return
    try:
        portal_conf.registerConfiglet( 'slideshow'
               , 'SlideShow Configuration'
               , 'string:${portal_url}/slideshow_config'
               , ''              # a condition
               , 'Manage portal' # access permission
               , 'Products'      # section to which the configlet should be added
                                 #(Plone,Products,Members)
               , 1               # visibility
               , PROJECTNAME
               , 'slideshow_icon.png' # icon in control_panel
               , 'SlideShow Configuration'
               , None
               )
	print >>out, "SlideShow Instaled the configlet from the portal control panel"
    except KeyError:
        pass # Get KeyError when registering duplicate configlet.

    install_global_properties(self, out)

def install_global_properties(self, out):

    logger.info('Installing Global Properties Product')

    # install PloneSlideShow global properties
    if not hasattr(self.portal_properties, 'ploneslideshow_properties'):
        self.portal_properties.addPropertySheet(
            'ploneslideshow_properties', 'PloneSlideShow properties')

    props = self.portal_properties.ploneslideshow_properties
    for prop, tp, val in LISTPROPERTIES:
        if not props.hasProperty(prop):
            props._setProperty(prop, val, tp)

    print >> out, "Successfully installed Plone Slide Show global properties."



def install_CustomSlots(self, out):

   logger.info('Installing Slots Product')

   """ sets up the custom slots"""
   #use the right zpt

   slideshow_portlet = 'context/portlet/portlet_slideshow/macros/portlet'
   if hasattr(self, "right_slots"):
       right_slots_list=list(self.right_slots)
       if slideshow_portlet in right_slots_list:
          out.write("Right slot for PloneSlideShow exists already\n")
       else:
          self._delProperty('right_slots')
          right_slots_list.append(slideshow_portlet)
          self._setProperty('right_slots',tuple(right_slots_list),'lines')
          out.write("Added right slot for PloneSlideShow\n")


def uninstall_global_properties(self, out):

    logger.info('Uninstalling Global Properties Product')

    """Remove the PloneSlideShow of global properties"""
    try:
        if hasattr(self.portal_properties, 'ploneslideshow_properties'):
            self.portal_properties.manage_delObjects(ids='ploneslideshow_properties')
        print >>out, "Removed ploneslideshow_properties."
    except KeyError:
        pass


def uninstall_configlet(self, out):
    
    logger.info('Uninstalling Configlet Product')

    """Remove the configlet from the portal control panel"""
    try:
        configTool=getToolByName(self,'portal_controlpanel', None)
    except AttributeError:
        print >>out, "Configlet could not be installed"
        return
    try:
        configTool.unregisterConfiglet('slideshow')
        out.write('Removed slideshow configlet\n')
    except KeyError:
        pass # Get KeyError when registering duplicate configlet.


def uninstall_resources(self, out):

    logger.info('Uninstalling Resources Product')

    """Remove the js and css files from the resource registries"""
    try:
        from Products.ResourceRegistries.config import CSSTOOLNAME, JSTOOLNAME
    except ImportError:
        return

    csstool = getToolByName(self, CSSTOOLNAME)
    jstool = getToolByName(self, JSTOOLNAME)

    csstool.manage_removeStylesheet(id='slideshow.css')
    jstool.manage_removeScript(id='skinsJs/slideshow.js')
    jstool.manage_removeScript(id='skinsJs/atmrt.js')
    jstool.manage_removeScript(id='skinsJs/openSlide.js')
    print >>out, "Resource files removed"


def removeSkin(self, out):

    logger.info('Uninstalling Skin Product')

    portal_skins = getToolByName(self, 'portal_skins')
    skins = portal_skins.getSkinSelections()
    for skin in skins:
        path = portal_skins.getSkinPath(skin)
        path = map(string.strip, string.split(path,','))
        if skinname in path:
            path.remove(skinname)
            path = string.join(path, ', ')
            portal_skins.addSkinSelection(skin, path)

    if skinname in portal_skins.objectIds():
        portal_skins._delObject(skinname)
        out.write('Removed %s from the portal_skins\n' % skinname)


def uninstall_CustomSlots(self, out):

   logger.info('Uninstalling Slots Product')

   slideshow_portlet = 'context/portlet/portlet_slideshow/macros/portlet'
   if hasattr(self, "right_slots"):
       right_slots_list=list(self.right_slots)
       if slideshow_portlet in right_slots_list:
          self._delProperty('right_slots')
          right_slots_list.remove(slideshow_portlet)
          self._setProperty('right_slots',tuple(right_slots_list),'lines')
          out.write("Removed right slot for PloneSlideShow\n")


def install (self):
    out = StringIO ()

    install_skins (self, out)
    # try for plone
    try:
        import Products.CMFPlone
    except ImportError:
        pass
    else:
        install_resources(self, out)
        install_CustomSlots(self, out)

    out.write ('%s Installation completed.\n' % PROJECTNAME)
    return out.getvalue()

def uninstall (self):
    out = StringIO ()

    uninstall_configlet(self, out)
    removeSkin (self, out)
    uninstall_resources(self, out)
    uninstall_global_properties(self, out)
    uninstall_CustomSlots(self, out)
    out.write ('Uninstallation completed.\n')
    return out.getvalue()
