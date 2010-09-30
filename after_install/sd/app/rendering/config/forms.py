# -*- coding: utf-8 -*-

from zope.formlib import form
from zope.component import queryUtility
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.form.base import AddForm as PloneAddForm
from plone.app.form.base import EditForm as PloneEditForm
from sd.common.adapters.storage.interfaces import IStorage
from sd.config.interfaces import IConfigurationSheetType
from sd.common.forms.base import base_template
from sd import _


class GeneratedForm(object):
    """Mixin
    """
    template = base_template
    form_name = _(u"configuration_form_name",
                  default=u"Rendering customization options")
    label = _(u"configure_display", default=u"Display configuration")
    
    @property
    def util(self):
        return queryUtility(IConfigurationSheetType, self.id, None)

    @property
    def form_fields(self):
        fields = form.FormFields(self.util.schema)
        return fields.omit('name')
    

class EditForm(GeneratedForm, PloneEditForm):

    @property
    def id(self):
        return self.context.name


class AddForm(GeneratedForm, PloneAddForm):

    id = None
        
    def create(self, data):
        sheet = self.util.configurationFactory()
        form.applyChanges(sheet, self.form_fields, data)
        return sheet

    def createAndAdd(self, data):
        ob = self.create(data)
        return self.add(ob)

    def nextURL(self):
        return self.context.absolute_url()
    
    def add(self, obj):
        storage = IStorage(self.context)
        storage.store(obj)

        # Create the appropriate message and mark as finished.
        self._finished_add = True
        messager = IStatusMessage(self.request)
        messager.addStatusMessage(u"Configuration done.", type="info")
        return True
