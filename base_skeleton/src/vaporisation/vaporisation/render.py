# -*- coding: utf-8 -*-
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.portlets.portlets.base import Renderer
from interfaces import ISteamer, ICloudRenderer


class Renderer( Renderer ):
    """ Renders a tag cloud """

    implements( ICloudRenderer )
    
    render = ViewPageTemplateFile('browser/cloud.pt')

    def __init__(self, context, request, view, manager, data):
        super(Renderer, self).__init__(context, request, view, manager, data)
        self.subjects = None
        putils = getToolByName(context, 'plone_utils')
        self.encoding = putils.getSiteEncoding()
        self.portal_url = getToolByName(context, 'portal_url')()


    def Title(self):
        return self.data.name


    def isJointNavigation(self):
        return self.data.joint


    def currentSubjects(self):
        subjects = self.request.form.get('Subject', None)
        if subjects:

            if isinstance(subjects, str):
                subjects = (subjects,)
            
            encoding = self.encoding
            self.subjects = [unicode(k, encoding)
                             for k in subjects]
        else:
            self.subjects = list()
        return self.subjects

    
    def removableTags(self):        
        tags = (self.subjects is not None and self.subjects
                or self.currentSubjects())
        
        if not tags:
            return None

        if len(tags) == 1:
            return (dict(name=tags.pop(),
                         link=self.portal_url),)
        
        removable = list()
        base_url  = 'cloud_search?Subject_usage:ignore_empty=operator:and'
        query     = '%s/%s' % (self.portal_url, base_url)
        tag_url   = '&Subject:list=%s'
        
        for tag in tags:
            tags_url = '&'.join([tag_url % k for k in tags if k != tag])
            removable.append(
                dict(name=tag,
                     link="%s%s" % (query, tags_url))
                )
        return removable


    def getVaporizedCloud(self):
        subjects = (self.subjects is not None
                    and self.subjects
                    or self.currentSubjects())
        return ISteamer(self.data).getVaporizedCloudFor(subjects)


    def getLinkPath(self):
        
        if not self.data.joint:
             return ("%s/cloud_search?Subject_usage:ignore_empty=operator:"
                     "and&Subject:list="
                     % self.portal_url)

        tags  = self.subjects
        query = self.request['QUERY_STRING']
        
        if query:
            return ("%s/cloud_search?%s&Subject:list=" %
                    (self.portal_url, query))
        
        return ("%s/cloud_search?Subject_usage:ignore_empty=operator:and"
                "&Subject:list=" % self.portal_url)
