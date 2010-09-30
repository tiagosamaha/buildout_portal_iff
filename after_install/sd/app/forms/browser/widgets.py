# -*- coding: utf-8 -*-

from OFS.Image import File
from Products.Five.browser.pagetemplatefile \
     import ZopeTwoPageTemplateFile as Page
from zope.app.form.browser.widget import SimpleInputWidget
from sd.common.widgets.file import FileUploadWidget
from sd.app.forms.objects import MinimalTerm


class TermWidget(SimpleInputWidget):

    def __call__(self):
        edited = self.context.context
        template = Page('templates/dict_widget.pt').__of__(edited)
        if self._data is None:
            return template(name = self.name, key = u"", value = u"")
        return template(name = self.name,
                        key = self._data.label,
                        value = self._data.value)

    def _toFieldValue(self, input):
        if isinstance(input, list) and len(input) == 2:
            return MinimalTerm(*input)
        return u""


class ImageUploadWidget(FileUploadWidget):

    def __call__(self):

        edited = self.context.context
        
        if isinstance(self._data, File):
            existWidget = Page('templates/exist_widget.pt').__of__(edited)
            baseUrl = self.request.get("URL1")
            filename = (getattr(self._data,'filename', '') or
                        getattr(self._data,'__name__', ''))

            image_url = '%s/++thumbnail++%s.preview' % (baseUrl,
                                                        filename)
            
            return existWidget(name = self.name,
                               thumb = image_url,
                               modified_name = self._modified_name,
                               required = self.context.required,
                               filename = filename)

        emptyWidget = Page('templates/empty_widget.pt').__of__(edited)
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
