# -*- coding: utf-8 -*-

# Imports: Structured Document
from sd import PROJECTNAME
from sd.contents.container  import StructuredContainer
from sd.contents.interfaces import IStructuredChapter
from sd.contents.interfaces import IStructuredDocument

# Imports: Zope
from zope.interface import implements
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.document import ATDocument


class StructuredDocument( StructuredContainer ):
    """A structured document"""

    implements( IStructuredDocument )

    # Configuration of my type
    schema = StructuredContainer.schema.copy() + \
             ATDocument.schema.copy()
    
    # Contents
    allowed_interfaces = (IStructuredChapter,)
    
    # Modifications on the schema
    schema['text'].required    = False
    schema['subject'].schemata = 'default'
    schema['tableContents'].default = True
    
    # Reorganizing schema
    schema.moveField('subject', after='description')

    # We want this next previous by default
    def getNextPreviousParentValue(self):
        return True


registerType(StructuredDocument, PROJECTNAME)
