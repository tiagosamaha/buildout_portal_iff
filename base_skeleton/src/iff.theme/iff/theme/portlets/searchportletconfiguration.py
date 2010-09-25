from zope.interface import Interface

from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from plone.portlet.collection import collection
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import string


class ISearchPortletConfiguration(collection.ICollectionPortlet):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    image = schema.TextLine(
        title=u"image path",
        description=u"Image of collection portlet",
        required=True)

class Assignment(collection.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(ISearchPortletConfiguration)


    def __init__(self, 
        header=u"", 
        target_collection=None, 
        limit=None, 
        random=False, 
        show_more=True, 
        show_dates=False,
        image=''):
        self.header = header
        self.target_collection = target_collection
        self.limit = limit
        self.random = random
        self.show_more = show_more
        self.show_dates = show_dates
        self.image = image


class Renderer(collection.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('searchportletconfiguration.pt')


class AddForm(collection.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ISearchPortletConfiguration)

    def create(self, data):
        return Assignment(**data)



class EditForm(collection.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ISearchPortletConfiguration)
