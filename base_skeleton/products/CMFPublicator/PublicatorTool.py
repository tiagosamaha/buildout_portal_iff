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

import os, string

from zLOG import LOG, INFO
from Globals import InitializeClass, DTMLFile, package_home
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.ActionInformation import ActionInformation
from Products.CMFCore.Expression import Expression

try: # New CMF
    from Products.CMFCore.permissions import ManagePortal, \
                                             ReviewPortalContent, \
                                             View
except: # Old CMF
    from Products.CMFCore.CMFCorePermissions import ManagePortal, \
                                                    ReviewPortalContent, \
                                                    View

from PublicationBoxInformation import PublicationBoxInformation

_wwwdir = os.path.join(package_home(globals()),'www')

# Change this value to 0 if you want to use CMFPublicator
# to manage boxes in another nodes of you portal.
_ROOT_SITE_ONLY = 0

if _ROOT_SITE_ONLY:
    from Products.CMFCore.utils import UniqueObject
else:
    from Products.CMFCore.utils import ImmutableId as UniqueObject


class PublicatorTool(UniqueObject, SimpleItem, ActionProviderBase):
    """A tool that provide a mechanism to store metadata items and allows you
    to choose only the items you want to publish in order you want to have.

    Oposed to default CMF/Plone publication machinary of queries under pre-
    defined rules with portal_catalog.
    """

    meta_type = 'CMF Publicator'
    id = 'portal_publicator'
    title = 'Content Publisher Tool'

    # Here is stored all publication boxes.
    _publication_boxes = ()


    ### Action items ###

    _actions = (ActionInformation(id='edit_publications_global',
                                  title='Publications',
                                  action=Expression(text='string:${portal_url}/publicator_select_form'),
                                  condition=Expression(text='member'),
                                  permissions=(ReviewPortalContent,),
                                  category='user',
                                  visible=1
                                 ),
                ActionInformation(id='edit_publications_local',
                                  title='Publications',
                                  action=Expression(text='python:object.portal_publicator.absolute_url()+"/publicator_select_form"'),
                                  condition=Expression(text='python:member and folder.portal_publicator.absolute_url()==folder.absolute_url()+"/portal_publicator"'),
                                  permissions=(ReviewPortalContent,),
                                  category='folder',
                                  visible=0
                                 )
               )


    ### ZMI tabs ###

    _publication_boxes_form = DTMLFile('editPublicationBoxes', _wwwdir)
    _publication_boxes_items_form = DTMLFile('viewPublicationBoxesItems', _wwwdir)

    manage_overview = PageTemplateFile('portal_publicator_overview', _wwwdir)

    manage_options = ({'label':'Overview', 'action':'manage_overview'},
                      {'label':'Configuration', 'action':'manage_editPublicationBoxesForm'},
                      {'label':'Stored items', 'action':'manage_viewPublicationBoxesItemsForm'}
                     ) + ActionProviderBase.manage_options + SimpleItem.manage_options

    security = ClassSecurityInfo()


    ### Internal methods ###

    security.declarePrivate('_listPublicationBoxes')
    def _listPublicationBoxes(self, box_id=None):
        """Return all the publication boxes or the specified box indicated by
        box_id.
        """

        if box_id is not None:
            for box in self._publication_boxes:
                if box.getId() == box_id:
                    return box

        return self._publication_boxes or ()


    security.declarePrivate('_clonePublicationBoxes')
    def _clonePublicationBoxes(self):
        """Return a list of publication boxes cloned from the current list.
        """

        return map(lambda x: x.clone(), list(self._listPublicationBoxes()))

 
    security.declarePrivate('_extractPublicationBox')
    def _extractPublicationBox(self, properties, box_id):
        """Extract the information of a publication box from the funky form
        properties.
        """

        pb_dict = {}

        pb_dict['id'] = properties.get('id_%s' % box_id, '')
        pb_dict['title'] = properties.get('name_%s' % box_id, '')
        pb_dict['content_type'] = properties.get('content_type_%s' % box_id, [])
        pb_dict['icon_url'] = properties.get('icon_url_%s' % box_id, '')
        pb_dict['n_items'] = properties.get('n_items_%s' % box_id, 0)
        pb_dict['n_searched_items'] = properties.get('n_searched_items_%s' % box_id, 0)
        pb_dict['search_states'] = properties.get('search_states_%s' % box_id, [])
        pb_dict['with_image'] = properties.get('with_image_%s' % box_id, 0)
        pb_dict['images_folder'] = properties.get('images_folder_%s' % box_id, '')
        pb_dict['image_states'] = properties.get('image_states_%s' % box_id, [])
        pb_dict['box_width'] = properties.get('box_width_%s' % box_id, '')
        pb_dict['box_height'] = properties.get('box_height_%s' % box_id, '')
        pb_dict['visible'] = properties.get('visible_%s' % box_id, 0)

        return pb_dict


    ### ZMI methods ###

    security.declareProtected(ManagePortal, 'manage_editPublicationBoxesForm')
    def manage_editPublicationBoxesForm(self, REQUEST, manage_tabs_message=None):
        """Show the 'Configuration' management tab.

        Returns data in a dictionary format.
        """

        publication_boxes = []

        for pb in self._listPublicationBoxes():
            pb_dict = pb.extract()
            publication_boxes.append(pb_dict)

        return self._publication_boxes_form(self,
                                            REQUEST,
                                            publication_boxes=publication_boxes,
                                            management_view='Configuration',
                                            manage_tabs_message=manage_tabs_message)


    security.declareProtected(ManagePortal, 'manage_viewPublicationBoxesItemsForm')
    def manage_viewPublicationBoxesItemsForm(self, REQUEST, manage_tabs_message=None):
        """Show the 'Stored items' tab.
        """

        publication_boxes_items = []

        for pb in self._listPublicationBoxes():
            pb_dict = {}
            pb_dict['id'] = pb.getId()
            pb_dict['items'] = pb.getItems()
            publication_boxes_items.append(pb_dict)

        return self._publication_boxes_items_form(self,
                                                  REQUEST,
                                                  publication_boxes_items=publication_boxes_items,
                                                  management_view='Stored items',
                                                  manage_tabs_message=manage_tabs_message)


    ### Iteractive methods ###

    security.declareProtected(ManagePortal, 'addPublicationBox')
    def addPublicationBox(self,
                          id,
                          name,
                          content_type=[],
                          icon_url='',
                          n_items=5,
                          n_searched_items=30,
                          search_states=['published'],
                          with_image=0,
                          images_folder='',
                          image_states=['visible'],
                          box_width='auto',
                          box_height='auto',
                          visible=1,
                          items=[],
                          REQUEST=None):
        """Add a publication box to the list.
        """

        new_publicationBoxes = self._clonePublicationBoxes()

        # Test if the provided id is already in use.
        if id:
            for pb in new_publicationBoxes:
                if pb.getId() == id:
                    raise ValueError('The provided id is already in use.')

        new_publicationBox = PublicationBoxInformation(id=id,
                                                       title=name,
                                                       content_type=content_type,
                                                       icon_url=icon_url,
                                                       n_items=n_items,
                                                       n_searched_items=n_searched_items,
                                                       search_states=search_states,
                                                       with_image=with_image,
                                                       images_folder=images_folder,
                                                       image_states=image_states,
                                                       box_width=box_width,
                                                       box_height=box_height,
                                                       visible=visible,
                                                       items=items)

        new_publicationBoxes.append(new_publicationBox)
        self._publication_boxes = tuple(new_publicationBoxes)

        if REQUEST is not None:
            return self.manage_editPublicationBoxesForm(
                REQUEST, manage_tabs_message='Publication box added.')


    security.declareProtected(ManagePortal, 'deletePublicationBoxes')
    def deletePublicationBoxes(self, selections=(), REQUEST=None):
        """Delete selected publication boxes indicated in 'selections'.

        selections is a list of ids of the selected boxes.
        """

        old_publication_boxes = self._clonePublicationBoxes()
        new_publication_boxes = []

        for pb in old_publication_boxes:
            if pb.getId() not in selections:
                new_publication_boxes.append(pb)

        self._publication_boxes = tuple(new_publication_boxes)

        if REQUEST is not None:
            return self.manage_editPublicationBoxesForm(REQUEST, manage_tabs_message=(
                   'Deleted %d publication box(es).' % len(selections)))


    security.declareProtected(ReviewPortalContent, 'changePublicationBox')
    def changePublicationBox(self, box_id, properties=None, REQUEST=None):
        """Update the specified publication box.
        """

        if properties is None:
            properties = REQUEST

        status_msg = 'Publication box configuration was been changed.'

        pb = self._listPublicationBoxes(box_id)
        pb_dict = self._extractPublicationBox(properties, box_id)
        pb.edit(**pb_dict)

        if REQUEST is not None:
            if REQUEST.get('came_from_zmi', 0):
                return self.manage_editPublicationBoxesForm(REQUEST,
                            manage_tabs_message=status_msg)
            else:
                REQUEST.RESPONSE.redirect('publicator_select_form?portal_status_message=%s' % status_msg)


    security.declareProtected(ReviewPortalContent, 'changePublicationBoxes')
    def changePublicationBoxes(self, properties=None, REQUEST=None):
        """Update all the publication boxes.
        """

        if properties is None:
            properties = REQUEST

        status_msg = 'Publication box configuration was been changed.'

        for pb in self._listPublicationBoxes():
            box_id = pb.getId()
            self.changePublicationBox(box_id, properties)

        if REQUEST is not None:
            if REQUEST.get('came_from_zmi', 0):
                return self.manage_editPublicationBoxesForm(REQUEST,
                            manage_tabs_message=status_msg)
            else:
                REQUEST.RESPONSE.redirect('publicator_select_form?portal_status_message=%s' % status_msg)


    security.declareProtected(ReviewPortalContent, 'changePBItems')
    def changePBItems(self, box_id=None, properties=None, REQUEST=None):
        """Update the list of items of the specified publication box.
        """

        if properties is None:
            properties = REQUEST

        status_msg = 'Publication box items was been changed.'
        portal_object = getToolByName(self, 'portal_url').getPortalObject()

        if box_id is not None and isinstance(box_id, str):
            pb = self._listPublicationBoxes(box_id)
            pb.changeItems(properties, portal_object)
        else:
            for pb in self._listPublicationBoxes():
                pb.changeItems(properties, portal_object)

        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('publicator_select_form?portal_status_message=%s' % status_msg)


    security.declareProtected(ReviewPortalContent, 'resetPBItems')
    def resetPBItems(self, box_id=None, REQUEST=None):
        """Reset the list of items of all publication boxes or the specified
        publication box.
        """

        status_msg = 'Publication box was been reseted.'

        if box_id is not None:
            pb = self._listPublicationBoxes(box_id)
            pb.resetItems()
        else:
            for pb in self._listPublicationBoxes():
                pb.resetItems()

        if REQUEST is not None:
            if REQUEST.get('came_from_zmi', 0):
                return self.manage_viewPublicationBoxesItemsForm(REQUEST,
                            manage_tabs_message=status_msg)
            else:
                REQUEST.RESPONSE.redirect('publicator_select_form?portal_status_message=%s' % status_msg)


    security.declareProtected(ReviewPortalContent, 'updatePBItems')
    def updatePBItems(self, box_id=None, REQUEST=None):
        """Update the list of items of all publication boxes or the specified
        publication box.
        """

        status_msg = 'Publication box was been updated.'
        portal_object = getToolByName(self, 'portal_url').getPortalObject()

        if box_id is not None:
            pb = self._listPublicationBoxes(box_id)
            pb.updateItems(portal_object)
        else:
            for pb in self._listPublicationBoxes():
                pb.updateItems(portal_object)

        if REQUEST is not None:
            if REQUEST.get('came_from_zmi', 0):
                return self.manage_viewPublicationBoxesItemsForm(REQUEST,
                            manage_tabs_message=status_msg)
            else:
                REQUEST.RESPONSE.redirect('publicator_select_form?portal_status_message=%s' % status_msg)


    security.declareProtected(View, 'getPublicationBoxes')
    def getPublicationBoxes(self, box_id=None):
        """Return all the publication boxes or a specified publication box.
        """

        return self._listPublicationBoxes(box_id)


    security.declareProtected(View, 'getPublicationBoxesInfo')
    def getPublicationBoxesInfo(self, box_id=None):
        """Return the content of all the publication boxes or a specified
        publication box.
        """

        if box_id is not None:
            pb = self._listPublicationBoxes(box_id)
            return pb.extract()
        else:
            publication_boxes = []

            for pb in self._listPublicationBoxes():
                publication_boxes.append(pb.extract())

            return publication_boxes


    security.declareProtected(View, 'getItemsContent')
    def getItemsContent(self, items, index):
        """Return the item content the from items list or empty dict.
        """

        items_size = len(items)
        if index < items_size:
            # Item has data
            return items[index]
        else:
            item_content = {}
            item_content['RelativeURL'] = ''
            item_content['NewWindow'] = None
            item_content['ImageURL'] = ''
            return item_content


    security.declareProtected(View, 'getImagesSearched')
    def getImagesSearched(self, need_image, relative_portal_path, content_type, content_state, relative=None):
        """Returns the searched catalog images path and id, if the item need it.
        """

        if need_image is not None:
            result = []
            catalog = getToolByName(self, 'portal_catalog')
            portal_url = getToolByName(self, 'portal_url')
            portal_path = portal_url.getPortalPath()
            relative_path = '%s/%s' % (portal_path, relative_portal_path)

            query = catalog.searchResults(path=relative_path,
                                          portal_type=content_type,
                                          sort_on='Date',
                                          sort_order='reverse',
                                          review_state=content_state)

            if relative is not None:
                portal_path_length = len(portal_url.getPortalObject().getPhysicalPath())
                # Extract the relative URL from cataloged items
                for obj in query:
                    content_dict = {}
                    content_path = obj.getPath().split('/')
                    relative_content_path = content_path[portal_path_length:]
                    content_dict['relative_url'] = '/'.join(relative_content_path)
                    content_dict['id'] = obj.id
                    result.append(content_dict)
            else:
                return query

            return result
        else:
            return None


    security.declareProtected(View, 'getListTypeInfo')
    def getListTypeInfo(self):
        """Return the list of registered types  in portal_types tool.
        """

        result = []
        portal_types = getToolByName(self, 'portal_types')

        for item in portal_types.listTypeInfo():
            result.append(str(item.getId()))

        return result


    ### Backwards compatibility - deprecated methods ###

    security.declareProtected(ReviewPortalContent, 'editPBItems')
    def editPBItems(self, properties=None, REQUEST=None):
        """Update the list of items of all publication boxes.
        """

        LOG('CMFPublicator', INFO, 'DEPRECATED - Please use changePBItems()')

        self.changePBItems(properties, REQUEST)

    security.declareProtected(ReviewPortalContent, 'changeAllPBItems')
    def changeAllPBItems(self, properties=None, REQUEST=None):
        """Update the list of items of all publication boxes.
        """

        LOG('CMFPublicator', INFO, 'DEPRECATED - Please use changePBItems()')

        self.changePBItems(properties, REQUEST)


    security.declareProtected(View, 'getPublicationBoxById')
    def getPublicationBoxById(self, box_id, field=None):
        """Return publication box if have the specified id.
        """

        LOG('CMFPublicator', INFO, 'DEPRECATED - Please use getPublicationBoxesInfo()')

        pb = self.getPublicationBoxesInfo(box_id)

        if field is None:
            return pb
        else:
            try:
                return pb[field]
            except:
                raise ValueError('The field is not a valid parameter.')


InitializeClass(PublicatorTool)

