"""Definition of the Processo Seletivo content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from iff.types import typesMessageFactory as _
from iff.types.interfaces import IProcessoSeletivo
from iff.types.config import PROJECTNAME

ProcessoSeletivoSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ProcessoSeletivoSchema['title'].storage = atapi.AnnotationStorage()
ProcessoSeletivoSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ProcessoSeletivoSchema, folderish=True, moveDiscussion=False)

class ProcessoSeletivo(folder.ATFolder):
    """Processo Seletivo / Vestibular / Concomitancia"""
    implements(IProcessoSeletivo)

    portal_type = "Processo Seletivo"
    schema = ProcessoSeletivoSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(ProcessoSeletivo, PROJECTNAME)
