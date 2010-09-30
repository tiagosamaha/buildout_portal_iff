# -*- coding: utf-8 -*-

from Acquisition import aq_parent, aq_inner, aq_base
from xml.sax import saxutils
from zope.app.form import browser
from zope.app.form.browser import widget
from zope.app.form import interfaces as forminterfaces
from zope.cachedescriptors.property import Lazy
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile \
                                                as PageTemplateFile

_marker = object()

class FileUploadWidget(widget.SimpleInputWidget):

    @property
    def canonical_object(self):
        canonical = self.context
        while getattr(aq_base(canonical), 'context', False):
            canonical = canonical.context
        return canonical

    def __call__(self):

        context = self.canonical_object.context
        existWidget = PageTemplateFile('templates/exist.pt').__of__(context)
        emptyWidget = PageTemplateFile('templates/empty.pt').__of__(context)
        
        kwargs = {'name': self.name,
                  'filename': '',
                  'modified_name': self._modified_name}

        if type(self._data) is not type(_marker):
            filename = getattr(self._data, 'filename', '')
            if not filename:
                filename = getattr(self._data,'__name__', '')
            kwargs['filename'] = filename

            return existWidget(name = self.name,
                               modified_name = self._modified_name,
                               required = self.context.required,
                               filename = filename)
            
        return emptyWidget(name = self.name,
                           modified_name = self._modified_name,
                           required = self.context.required)

           
    def _getFormInput(self):
        modify = int(self.request.get('_modify_%s' % self.name, 0))
        if not modify:
            return None
        return self.request.get(self.name, None) or None

    def hasInput(self):
        return (int(self.request.get(self._modified_name, 0)) > 0)

    @Lazy
    def _modified_name(self):
        return "_modify_%s" % self.name
