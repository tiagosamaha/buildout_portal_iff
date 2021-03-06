# $Id: _collage.py 69655 2008-08-08 16:58:31Z glenfant $

from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTMixin
from Products.Collage.content.common import LayoutContainer, CommonCollageSchema

from Products.CMFPlone.interfaces import INonStructuralFolder

from Products.Collage.interfaces import ICollage

from zope.interface import implements

from Products.Collage.utilities import CollageMessageFactory as _

CollageSchema = atapi.BaseContent.schema.copy() + atapi.Schema((
    atapi.StringField(
        name='title',
        searchable=True,
        widget=atapi.StringWidget(
            label='Title',
            label_msgid='label_title',
            i18n_domain='plone',
        )
    ),

    atapi.TextField(
        name='description',
        searchable=True,
        widget=atapi.TextAreaWidget(
            label='Description',
            label_msgid='label_description',
            i18n_domain='plone',
        )
    ),
    atapi.BooleanField('show_title',
        accessor='getShowTitle',
        widget=atapi.BooleanWidget(
            label=_(u'label_show_title', default=u"Show title")),

        default=1),

    atapi.BooleanField('show_description',
        accessor='getShowDescription',
        widget=atapi.BooleanWidget(
            label=_(u'label_show_description', default='Show description')),
        default=1),


))

CollageSchema = CollageSchema + CommonCollageSchema.copy()

# move description to main edit page
CollageSchema['description'].schemata = 'default'

# support show in navigation feature and at marshalling
# speciel case set folderish to False since we want related items to be used
finalizeATCTSchema(CollageSchema, folderish=False, moveDiscussion=False)

class Collage(LayoutContainer, ATCTMixin, atapi.OrderedBaseFolder):

    # FIXME: Do we always need Zope 2 style interfaces ?
    __implements__ = (getattr(atapi.OrderedBaseFolder,'__implements__',()),
                      getattr(ATCTMixin, '__implements__',()))

    schema = CollageSchema

    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    implements(ICollage, INonStructuralFolder)

    def SearchableText(self):
        return self.aggregateSearchableText()

atapi.registerType(Collage, 'Collage')
