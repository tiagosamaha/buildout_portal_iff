# -*- coding: utf-8 -*-
from zope.formlib import form
from zope.event import notify
from plone.app.portlets.portlets.base import AddForm
from cloud import Cloud
from events import TreeUpdateEvent
from interfaces import ICustomizableCloud, ISteamer


class AddForm( AddForm ):
    """ This is the tagcloud add form, rendering the customizable fields """

    def create(self, data):
        cloud = Cloud(**data)
        notify(TreeUpdateEvent(cloud.__of__(self.context)))
        return cloud

    # The form fields
    form_fields = form.Fields( ICustomizableCloud )
