## Python Script "list_panel"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=RESPONSE=None
##title=
##

from Products.CMFCore.utils import getToolByName
request=context.REQUEST

# PloneSlideShow box in CMFPublicator
boxId = 'slideshow'

try:
    publicatortool=getToolByName(context,'portal_publicator')
except AttributeError, e:
    e = str(e)
    if e == 'portal_publicator':
        list_pb = 'not instaled'
else:
    try:
        list_pb = publicatortool.getPublicationBoxesInfo(boxId)['items']
    except AttributeError, e:
        e = str(e)
        if e == """'tuple' object has no attribute 'extract'""":
            list_pb = 'not boxid'
    else:
        if not publicatortool.getPublicationBoxesInfo(boxId)['items']:
            list_pb = 'not list'

return list_pb