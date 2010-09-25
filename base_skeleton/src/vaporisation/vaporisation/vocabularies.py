# -*- coding: utf-8 -*-

from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface.declarations import directlyProvides, implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.CMFCore.utils import getToolByName
from zope.schema.interfaces import ITokenizedTerm, ITitledTokenizedTerm


class KeywordTerm(object):
    """Simple tokenized keyword used by SimpleVocabulary."""
    
    implements(ITokenizedTerm)
    
    def __init__(self, value):
        """Create a term from the single value
        This class prevents the use of the silly bugged SimpleTerm.
        """
        self.value = value
        self.token = value            
        self.title = value
        directlyProvides(self, ITitledTokenizedTerm)


class KeywordVocabulary(object):
    """Vocabulary factory for keywords of a cloud.
    """
    implements( IVocabularyFactory )

    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        putils   = getToolByName(context, 'plone_utils')
        encoding = putils.getSiteEncoding()
        subjects = catalog.uniqueValuesFor('Subject')
        keywords = [unicode(k, encoding) for k in subjects]        
        keywords.sort()
        terms = [KeywordTerm(k) for k in keywords]
        return SimpleVocabulary(terms)

KeywordVocabularyFactory = KeywordVocabulary()
