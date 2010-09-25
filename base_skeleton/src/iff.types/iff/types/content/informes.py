"""Definition of the Informes content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
#from Products.ATContentTypes.content import base
#from Products.ATContentTypes.content import schemata

from iff.types import typesMessageFactory as _
from iff.types.interfaces import IInformes
from iff.types.config import PROJECTNAME

from Products.ATContentTypes.content.document import ATDocument

#InformesSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

#))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

#InformesSchema['title'].storage = atapi.AnnotationStorage()
#InformesSchema['description'].storage = atapi.AnnotationStorage()

#schemata.finalizeATCTSchema(InformesSchema, moveDiscussion=False)

class Informes(ATDocument):
    """Informes Processo Seletivo / Recursos, Reclassificacao, etc.."""
    implements(IInformes)

    portal_type = "Informes"
#   schema = InformesSchema

#   title = atapi.ATFieldProperty('title')
#   description = atapi.ATFieldProperty('description')

atapi.registerType(Informes, PROJECTNAME)
