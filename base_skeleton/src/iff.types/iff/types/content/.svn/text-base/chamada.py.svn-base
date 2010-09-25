"""Definition of the Chamada content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
#from Products.ATContentTypes.content import base
#from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.document import ATDocument

from iff.types import typesMessageFactory as _
from iff.types.interfaces import IChamada
from iff.types.config import PROJECTNAME

#ChamadaSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

#))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

#ChamadaSchema['title'].storage = atapi.AnnotationStorage()
#ChamadaSchema['description'].storage = atapi.AnnotationStorage()

#schemata.finalizeATCTSchema(ChamadaSchema, moveDiscussion=False)

class Chamada(ATDocument):
    """Chamada Processo Seletivo"""
    implements(IChamada)

    portal_type = "Chamada"
#    schema = ChamadaSchema

#    title = atapi.ATFieldProperty('title')
#    description = atapi.ATFieldProperty('description')

atapi.registerType(Chamada, PROJECTNAME)
