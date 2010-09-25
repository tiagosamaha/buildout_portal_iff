## Controller Python Script "prefs_slide_set"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=RESPONSE=None
##title=
##

from Products.PythonScripts.standard import html_quote
from Products.CMFCore.utils import getToolByName
request = container.REQUEST
RESPONSE =  request.RESPONSE

boxInfo = {'id':'slideshow',
           'name':'Plone SlideShow',
           'content_type':list(('News Item', 'File', 'Document')),
           'n_items':int(3),
           'search_states':list(('published',)),
           'n_searched_items':int(35),
           'with_image':bool(1),
           'image_states':list(('published',))}


portal_publicator = getToolByName(context, 'portal_publicator')
portal_url =  getToolByName(context, 'portal_url')

try:
   portal_publicator.addPublicationBox(id=boxInfo['id'],
                                       name=boxInfo['name'],
                                       content_type=boxInfo['content_type'],
                                       n_items=boxInfo['n_items'],
                                       search_states=boxInfo['search_states'],
                                       n_searched_items=boxInfo['n_searched_items'],
                                       with_image=boxInfo['with_image'],
                                       image_states=boxInfo['image_states'])

   return RESPONSE.redirect(str(portal_url()) + '/?portal_status_message=Created news box %s' %(boxInfo['id']))

except ValueError, e:
   e = str(e)
   if e == """The provided id is already in use.""":
      return RESPONSE.redirect(str(portal_url()) + '/?portal_status_message=The provided id %s is already in use.' %(boxInfo['id']))