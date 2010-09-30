# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.formlib.form import Fields
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from sd import _
from base import *
from interfaces import IPersonBlock


class Person(AssignmentWithImage):
    """A portlet representing a person.
    """
    implements(IPersonBlock)

    def __init__(self, name, details=[], caption=u"", image=None):
        super(Person, self).__init__(name, caption, image)
        self.details = details
    
        
class AddForm(AddFormWithImage):
    """Person block add form
    """
    form_fields = Fields(IPersonBlock)
    
    def create(self, data):
        person = Person(**data)
        return person


class EditForm(EditFormWithImage):
    """Person block edit form
    """
    form_fields = Fields(IPersonBlock)
    label = _(u"Edit Person block")
    description = _(u"This form allow you to edit your person block.")


class Renderer(ImagePortletRenderer):
    """Browser view to render a person block
    """
    render = ViewPageTemplateFile('templates/person.pt')

    def personal_details(self):
        return self.data.details
