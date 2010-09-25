"""Definition of the Portlet Container content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from iff.types import typesMessageFactory as _
from iff.types.interfaces import IPortletContainer
from iff.types.config import PROJECTNAME
from sd.contents.interfaces import IStructuredDocument

#rom Products.ATContentTypes.content.document import ATDocument

PortletContainerSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

PortletContainerSchema['title'].storage = atapi.AnnotationStorage()
PortletContainerSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PortletContainerSchema, moveDiscussion=False)

class PortletContainer(base.ATCTContent):
    """ Portlet Container Content Type"""
    implements(IPortletContainer, IStructuredDocument)

    portal_type = "PortletContainer"
    schema = PortletContainerSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(PortletContainer, PROJECTNAME)
