#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unittest
from BeautifulSoup import BeautifulSoup

from Products.CMFPlone.utils import getToolByName
from Products.Five.viewlet.manager import ViewletManager
from zope.interface import alsoProvides
from zope.component import getMultiAdapter

from iff.theme.tests.base import TestCase
from iff.theme.browser.viewlets import NewsFocusViewlet
from iff.theme.browser.viewletmanager import HeaderFocusViewletManager
from iff.theme.browser.interfaces import (IHeaderFocusViewletManager,
                                          IThemeSpecific,)

def getViewlet(portal):
    request = portal.REQUEST
    alsoProvides(request,IThemeSpecific)
    context = portal
    view = getMultiAdapter((context,request), name="plone")
    klass = ViewletManager("iff.headerfocus",
                                    IHeaderFocusViewletManager,
                                    bases=(HeaderFocusViewletManager,))
    viewletmanager = klass(context,request,view)
#    viewlet = getMultiAdapter((context, request, view,
#        viewletmanager,),name="iff.newsfocus")
    viewlet = viewletmanager['iff.newsfocus']
    return viewlet



class NewsFocusViewletFunctionalTestCase(TestCase):

    def defineSplitedNewsScenario(self):
        folder = (
                ('Folder1','Campus 1'),
                ('Folder2''Campus 2'),
                ('Folder3','Campus 3'),)
        contents =[
            ('New1', 'Test News Item 1'),
            ('New2', 'Test News Item 2'),
            ('New3', 'Test News Item 3'),
            ('New4','Test News Root Item 4'),]
        pw = self.portal.portal_workflow
        self.loginAsPortalOwner()
        self.portal.invokeFactory('Folder', id='campus', title='Campus')
        campus_folder = self.portal['campus']
        for position in xrange(0,3):
            name = folder[position][0]
            title = folder[position][1]
            campus_folder.invokeFactory('Folder', id=name, title=title)
            campus = campus_folder[name]
            campus.invokeFactory('Folder',id='noticias',title='Notícias')
            campus.invokeFactory('Folder',id='eventos',title='Eventos')
            pw.doActionFor(campus ,'publish')
            news_item = contents[position]
            news_name = news_item[0]
            news_title = news_item[1]
            news_folder = campus['noticias']
            news_folder.invokeFactory('News Item', id=news_name, title=news_title)
            pw.doActionFor(news_folder[news_name] ,'publish')
        news_root = contents[-1]
        news_name = news_root[0]
        news_title = news_root[1]
        self.portal.invokeFactory('News Item',id=news_name,title=news_title)
        pw.doActionFor(self.portal[news_name] ,'publish')
        self.logout()
        return contents


    def defineRootNewsScenario(self):
        self.loginAsPortalOwner()
        contents =[
            ('New1', 'Test News Item 1'),
            ('New2', 'Test News Item 2'),
            ('New3', 'Test News Item 3'),]
        for name, title in contents:
            self.portal.invokeFactory('News Item', id=name, title=title)
            self.portal.portal_workflow.doActionFor(self.portal[name] ,'publish')
        self.logout()
        return contents

    def test_IfNewsFocusViewletIsRenderedNone(self):
        viewlet = getViewlet(self.portal)
        viewlet.update()
        self.assertEquals(u"\n", viewlet.render())

    def test_SearchNone(self):
        viewlet = getViewlet(self.portal)
        self.assertEquals(viewlet.news(),[])

    def test_SearchContents(self):
        contents = self.defineRootNewsScenario()
        viewlet = getViewlet(self.portal)
        contents.reverse() #ordena pela noticias mais recentes
        self.assertEquals([(item.id, item.Title) for item in viewlet.news()], contents)
        news = viewlet.news()
        first_news = news[0]
        self.assertEquals(first_news.id, 'New3')

    def test_IfNewsFocusViewletIsRendered(self):
        self.defineSplitedNewsScenario()
        viewlet = getViewlet(self.portal)
        viewlet.update()
        html = BeautifulSoup(viewlet.render())
        self.assertEquals('Test News Item 3', str(html.find(text='Test News Item 3')))


def test_suite():
    suite = unittest.makeSuite(NewsFocusViewletFunctionalTestCase)
    return suite
if __name__ == '__main__': unittest.main(defaultTest='test_suite')
