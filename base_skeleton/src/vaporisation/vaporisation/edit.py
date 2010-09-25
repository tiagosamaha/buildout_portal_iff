# -*- coding: utf-8 -*-
from zope.formlib import form
from zope.event import notify
from plone.app.form.validators import null_validator
from plone.app.portlets.portlets.base import EditForm
from events import TreeUpdateEvent
from interfaces import ISteamer, ICustomizableCloud
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('vaporisation')


class EditForm( EditForm ):
    """ A not-so-basic edit form with an update action """

    def redirectFromForm( self ):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    
    @form.action(_(u"Save"), condition=form.haveInputWidgets, name=u'save')
    def handle_save_action(self, action, data):
        if form.applyChanges(self.context,
                             self.form_fields,
                             data,
                             self.adapters):
            self.status = _(u"Changes saved and tagcloud updated.")
            notify(TreeUpdateEvent(self.context))
        else:
            self.status = _(u"No changes.")
        return self.redirectFromForm()


    @form.action(_(u"Cancel"), validator=null_validator, name=u'cancel')
    def handle_cancel_action(self, action, data):
        return self.redirectFromForm()


    @form.action(_(u"Update cloud"), name=u'update')
    def handle_update_action(self, action, data):
        notify(TreeUpdateEvent(self.context))
        self.status = _(u"Changes saved and tagcloud updated.")
        return self.redirectFromForm()

    # The fields
    form_fields = form.Fields( ICustomizableCloud )
