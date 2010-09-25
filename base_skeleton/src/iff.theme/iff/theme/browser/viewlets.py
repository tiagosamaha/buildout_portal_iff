#!/usr/bin/env python
#-*- coding:utf-8 -*-


from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase as PloneViewletBase
from Products.Five.viewlet.viewlet import ViewletBase
from Products.CMFPlone.utils import getToolByName
from iff.theme.config import content, state
from zope.component import getMultiAdapter
import textwrap
import re

from vaporisation.render import Renderer

class NewsFocusViewlet(ViewletBase):

    render = ViewPageTemplateFile('newsfocus.pt')

    def _search(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog.searchResults(
                    portal_type=content,
                    sort_on ='Date',
                    sort_order='reverse',
                    review_state=state)

    def link(self):
        return "search?portal_type:list=%s&sort_on=Date&sort_order=reverse&review_state:list=%s&submit=Buscar"%(content, state)

    def news(self):
        searchResults = list(self._search())
        #searchResults.reverse()
        return dict(enumerate(searchResults))


class ImageFocusViewlet(ViewletBase):
    render = ViewPageTemplateFile('imagefocus.pt')


class TagCloudViewlet(PloneViewletBase,Renderer):


    def __init__(self, context, request, view, manager):
        PloneViewletBase.__init__(self,context,request,view,manager)
        self.data = None

    def index(self):
        return "\n"

class NewsViewlet(ViewletBase):

    render = ViewPageTemplateFile('news.pt')

    def link(self):
        return "search?portal_type:list=%s&sort_on=Date&sort_order=reverse&review_state:list=%s&submit=Buscar"%('News Item', 'published')

    def _search(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog.searchResults(
                    portal_type=content,
                    sort_on ='Date',
                    sort_order='reverse',
                    review_state="published")

    def news(self, lines=3, cols=3):
        news_cataloged = list(self._search())[:lines*cols]
        #result.reverse()#TODO: usar o catalogo para reverter
        newsList = [
            {'title':focus_news.Title,
             'description':focus_news.Description,
             'campus':self.campusTitle(focus_news),
             'date':self.transformDate(focus_news.Date),
             'url':focus_news.getURL()}
                for focus_news in news_cataloged]
        result = []
        for i in range(lines):
            result.append([])
            for j in range(cols):
                result[i].append(newsList[(i*cols)+j])
        return result

    def transformDate(self, datetime):
        # Retiranda a hora e invertendo a data para formata BR
        datetime = datetime
        dateSplitHours = datetime.split(' ')
        date = dateSplitHours[0].split('-')
        date.reverse()
        date = date[0]+'/'+date[1]+'/'+date[2]
        return date
        
    
    def _campus_nameOrNone(self, url):
        # Alterando valor de /  para 5 pq quando nao vai pelo IP nao funciona
        if url.count("/") < 5 or not "/campus/" in url:
            return None
        # Anterior http, null, host, portalid, folder_campus, campus_name
        http, null, host, folder_campus, campus_name = url.split("/")[:5]
        if not folder_campus == "campus":
            return None
        assert not http == "http", "Formato da url de noticia invalida."
        return campus_name

    def campusTitle(self, news):
        url = news.getURL() #TODO: seria mais OO perguntar a noticia, qual campus ele pertence
        campus_name = self._campus_nameOrNone(url)
        if not campus_name:
            return "Geral"
        else:
            return self.context.campus[campus_name].Title()
