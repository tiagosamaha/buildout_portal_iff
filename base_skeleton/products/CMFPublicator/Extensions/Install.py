##############################################################################
#
# Copyright (c) 2004 Dinheiro Vivo <www.dinheirovivo.com.br>
#                    by Jean Rodrigo Ferri <jeanrodrigoferri@yahoo.com.br>
# 
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
##############################################################################

"""CMFPublicator Installer

This file is an installation script for CMFPublicator.  It's meant to be used
as an External Method.  To use, add an external method to the root of the CMF
Site that you want CMFPublicator registered in with the configuration:

 id: install_publicator
 title: Install Publicator *optional*
 module name: CMFPublicator.Install
 function name: install

Then go to the management screen for the newly added external method and click
the 'Test' tab.  The install function will execute and give information about
the steps it took to register and install the CMFPublicator into the CMF Site
instance.
"""

import string
from cStringIO import StringIO
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.utils import getToolByName
from Products.CMFPublicator import publicator_globals

out = StringIO()

def install(self):
    """Register CMF ToolBox with the necessary tools.
    """

    out.write('CMF Publicator Installation on %s\n' % self.id)
    out.write('======================\n\n')

    actionstool = getToolByName(self, 'portal_actions')
    portal_skins = getToolByName(self, 'portal_skins')
    portal = getToolByName(self, 'portal_url').getPortalObject()

    # Create and register tools
    tools = {'portal_publicator':'CMF Publicator'}

    for tool in tools.keys():
        if not tool in portal.objectIds():
            portal.manage_addProduct['CMFPublicator'].manage_addTool(tools[tool], None)
            out.write('Created %s\n' % tools[tool])
            portal_publicator = getToolByName(self, 'portal_publicator')
            portal_publicator.addPublicationBox(id='news',
                                                name='News',
                                                content_type=['News Item'],
                                                n_items=5,
                                                search_states=['published'])
            out.write('Created news box\n')
        else:
            out.write('%s already exists\n' % tools[tool])

    ap = actionstool.listActionProviders()
    for tool in tools.keys():
        if (type(ap) is not type([]) and type(ap) is not type(())) or not tool in ap:
            try:
                actionstool.addActionProvider(tool)
                out.write('Added %s as action provider\n' % tools[tool])
            except:
                out.write('Failed adding %s as action provider\n' % tools[tool])
        else:
            out.write('%s already existed as action provider\n' % tools[tool])
    
    
    # Setup the skins
    skinname = 'publicator'
    if skinname not in portal_skins.objectIds():
        addDirectoryViews( portal_skins, 'skins', publicator_globals )
        out.write("Added %s directory view to portal_skins\n" % skinname)
    else:
        out.write("%s directory view already existed in portal_skins\n" % skinname)

    # Insert 'publicator' into the skin configurations.
    skins = portal_skins.getSkinSelections()
    for skin in skins:
        path = portal_skins.getSkinPath(skin)
        path = map(string.strip, string.split(path,','))
        if skinname not in path:
            try:
                path.insert(path.index('custom') + 1, skinname)
            except ValueError:
                path.append(skinname)

            path = string.join(path, ', ')
            # addSkinSelection will replace existing skins as well.
            portal_skins.addSkinSelection(skin, path)
            out.write("Added %s to %s skin\n" % (skinname, skin))
        else:
            out.write("Skipping %s skin, %s is already set up\n" % (skin,skinname))
    skins = portal_skins.getSkinSelections()

    #try to install the slot (bare except, because it will fail on bare CMF)
    slotpath = testPlone(self)
    try:
        if slotpath is not None and not slotpath in portal.right_slots:
            portal.right_slots = [slotpath,] + list(portal.right_slots)
            out.write("Added %s to right_slots\n" % slotpath)
        else:
            out.write("%s is already set up in right_slots\n" % slotpath)
    except: 
        out.write("Can't set up right_slots\n")

    return out.getvalue()

def uninstall(self):
    """Remove skins, types and special objects.
    """

    out.write('CMF Publicator Un-Installation\n')
    out.write('===========================\n\n')
    portal = getToolByName(self, 'portal_url').getPortalObject()
    actionstool = getToolByName(self, 'portal_actions')
    tools = {'portal_publicator':'CMF Publicator'}

    removeSkin(self, 'publicator')

    if 'portal_publicator' in portal.objectIds():
        portal._delObject('portal_publicator')
        out.write('Removed Publicator Tool\n')

    ap = actionstool.listActionProviders()
    for tool in tools.keys():
        if tool in ap:
            try:
                actionstool.deleteActionProvider(tool)
                out.write('Removed %s as action provider\n' % tools[tool])
            except:
                out.write('Failed removing %s as action provider\n' % tools[tool])
        else:
            out.write('%s not existed as action provider\n' % tools[tool])

    #try to remove the slot
    slotpath = testPlone(self)
    try:
        if slotpath is not None and slotpath in portal.right_slots:
            right_slots = portal.right_slots
            right_slots.remove(slotpath)
            portal.right_slots = right_slots
            out.write("Removed %s from right_slots\n" % slotpath)
    except:
        pass

    return out.getvalue()

def testPlone(self):
    """Test wich Plone version is installed.
    """

    try:
        from Products.CMFPlone.migrations import v2_1
        return 'here/portlet_news_p21/macros/portlet'
    except:
        try:
            from Products.CMFPlone.migrations import v2
            return 'here/portlet_news_p20/macros/portlet'
        except:
            try:
                from Products.CMFPlone.migrations import final_one_zero_one
                return 'here/news_slot_p10/macros/newsBox'
            except:
                return None

def removeSkin(self, skinname):
    """Remove a skin from portal_skins.
    """

    portal_skins = getToolByName(self, 'portal_skins')
    skins = portal_skins.getSkinSelections()
    for skin in skins:
        path = portal_skins.getSkinPath(skin)
        path = map(string.strip, string.split(path,','))
        if skinname in path:
            path.remove(skinname)
            path = string.join(path, ', ')
            portal_skins.addSkinSelection(skin, path)
            out.write("Removed %s from %s skin\n" % (skinname, skin))

    if skinname in portal_skins.objectIds():
        portal_skins._delObject(skinname)
        out.write('Removed %s from the portal_skins\n' % skinname)
