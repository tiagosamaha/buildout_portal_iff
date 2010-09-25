from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

#Defines the availables types for special links
# SpecialTypeLinkGenerator will get the remote Url for a link, the url for availableTypes
# The LinkGenerator method will return the link to the object, it will add '/view' for availableTypes
# the IsExternalEditorAvailable method will provide an external editor link for the availableTypes
availableTypes = ['File','PloneExFile']

class PortletFolderView(BrowserView):
    """New view for folders"""

    __call__ = ViewPageTemplateFile('folderview.pt')
    
    def getFolderContentsUpgrade(self,index_,Type_):
        #getFolderContents with file exclusion when the file medata 
        # "exclude_from_nav" is true
        context = aq_inner(self.context)
        brains = context.getFolderContents({str(index_):str(Type_)})
        brains = [x for x in brains if not x['exclude_from_nav']]  
        return brains
    
    def getFolderInnerContent(self,itempath):        
        # Gets the portal_catalog tool from Plone 
        context = aq_inner(self.context)
        portal_catalog = getToolByName(context, 'portal_catalog')
       
        # The portal_catalog looks for first level items, it means it does not
        # return the elements contained in subfolders.
        # The brain contains items sort by date, from the last one created to
        # the first one, the itempath is given by the folderview template
        
        brains = portal_catalog.searchResults(path = {'query' : itempath,
                                                      'depth' : 1 },
                                             )
        brains = [x for x in brains if not x['exclude_from_nav']]
        return brains
    
    def LinkGenerator(self,item):
        # Check that our link policy is used : global click ->document view
        # 1rst special link : direct link to content / url
        # 2nd special link : external editing link
        linkTypes = [x for x in availableTypes]
        linkTypes.append('Image')
        if item['portal_type'] in linkTypes:
            return item.getURL()+'/view'
        else:
            return item.getURL()
        
    def SpecialTypeLinkGenerator(self,item):
        # 1rst special link : direct link to content / url
        if item['portal_type'] == 'Link':
            return item['getRemoteUrl']
        if item['portal_type'] in availableTypes:
            return item.getURL()
        else:
            return False        
            
    def IsExternalEditorAvailable(self,brainobject):
        # 2nd special link : external editing link
        
        #check if object portal type is in availableTypes.
        # If not, it's not usefull to test further.
        # Also checks if tool portal_external_editor_helper is installed,
        # if yes, we don't need availableTypes because the externalEditorEnable()
        # method is upgraded by the tool.
        
        try:
            portal_ext_edit = getToolByName(context, 'portal_external_editor_helper')
        except:
            portal_ext_edit = None
        if portal_ext_edit or brainobject['portal_type'] in availableTypes :
                if brainobject.getObject().externalEditorEnabled():
                   return True
    

        
     
        

       
