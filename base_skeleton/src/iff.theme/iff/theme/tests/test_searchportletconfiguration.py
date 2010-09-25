import unittest

from Products.PloneTestCase import PloneTestCase as ptc
from Products.Five.viewlet.manager import ViewletManager
from zope.publisher.browser import TestRequest
from zope.component import (
    getMultiAdapter,
    ComponentLookupError,
    getAdapters,
    getUtility,
    )
from plone.portlets.interfaces import (
    IPortletType,
    IPortletManager,
    IPortletAssignment,
    IPortletDataProvider,
    IPortletRenderer,
    )

from iff.theme.portlets import searchportletconfiguration

class SearchPortletConfigurationTestCase(ptc.PloneTestCase):
    data = {
            'header':'titulo',
            'target_collection':None,
            'limit':5,
            'show_more':False,
            'show_dates':True,
            'image':'http://nohost/plone/img.png'}
    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name='iff.theme.SearchPortletConfiguration')
        self.assertEquals(portlet.addview,
                          'iff.theme.SearchPortletConfiguration')

    def test_interfaces(self):
        portlet = searchportletconfiguration.Assignment(**self.data)
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(IPortletType, name='iff.theme.SearchPortletConfiguration')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]# retira os portlests padroes
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
       
        addview.createAndAdd(data=self.data)

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                        searchportletconfiguration.Assignment))

    def _getRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager,
            name='plone.rightcolumn',
            context=self.portal)
        assignment = searchportletconfiguration.Assignment(**self.data)
        return getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)

    def test_obtain_renderer(self):
        renderer = self._getRenderer()
        self.failUnless(isinstance(renderer, searchportletconfiguration.Renderer))
        self.renderer = renderer

    def test_view_portlet(self):
        renderer = self._getRenderer()
        self.assertEquals(renderer.data.image, "http://nohost/plone/img.png")


def test_suite():
    return unittest.makeSuite(SearchPortletConfigurationTestCase)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
