"""Definition of the Arte e Cultura content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
#rom Products.ATContentTypes.content import base
#rom Products.ATContentTypes.content import schemata

from iff.types import typesMessageFactory as _
from iff.types.interfaces import IArteeCultura
from iff.types.config import PROJECTNAME
from sd.app.contents.document import StructuredDocument
from sd.contents.interfaces import IStructuredDocument

#rteeCulturaSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

#)

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

#rteeCulturaSchema['title'].storage = atapi.AnnotationStorage()
#rteeCulturaSchema['description'].storage = atapi.AnnotationStorage()

#chemata.finalizeATCTSchema(ArteeCulturaSchema, moveDiscussion=False)

class ArteeCultura(StructuredDocument):
    """Description of the Example Type"""
    implements(IArteeCultura)

    portal_type = "Arte e Cultura"
    #chema = ArteeCulturaSchema

    #itle = atapi.ATFieldProperty('title')
    #escription = atapi.ATFieldProperty('description')

atapi.registerType(ArteeCultura, PROJECTNAME)
