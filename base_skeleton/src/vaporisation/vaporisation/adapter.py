"""
Adapters for the tagcloud
"""

# -*- coding: utf-8 -*-
from random import shuffle
from zope.component import adapts
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from interfaces import ISteamer, IVaporizedCloud


class Steamer( object ):

    adapts( IVaporizedCloud )
    implements( ISteamer )
    
    def __init__(self, context):
        self.context = context

    def getStepForTag(self, tag):
        """ Only used for display purposes """

        def calculateTagSize(step):
            return int(100 + step * 10)

        occurence = self.context.tagsTree[tag]['weight']

        if self.context.lowest == self.context.highest:
            return 100, occurence

        lowest  = float(self.context.lowest)
        highest = float(self.context.highest)

        step = ((float(occurence) - lowest) /
                (highest - lowest) *
                self.context.steps)

        return calculateTagSize(step), occurence


    def getTagsFromTree(self, keywords):
        """ Returns a list of dicts with the needed infos """
        
        tags = list()

        for keyword in keywords:
            if keyword in self.context.tagsTree:
                size, weight = self.getStepForTag(keyword)
                tags.append(dict(name=keyword,
                                 weight=weight,
                                 size=size))
        return tags


    def getConnectionsFor(self, keywords):
        """ Will retrieve the related keywords of the given keyword """
        
        tags = None
        for keyword in keywords:            
            if keyword in self.context.tagsTree:
                tag = self.context.tagsTree[keyword]
                if tags is None:
                    tags = set(tag['connections'])
                else:
                    tags = tags.intersection(set(tag['connections']))

        if tags is None:
            return list()

        return self.getTagsFromTree(tuple(tags))


    def getVaporizedCloudFor(self, subjects=None):
        """ Returns the available clouds and relatives """
        
        if not self.context.joint or not subjects:
            return self.getTagsFromTree(self.context.keywords)

        return self.getConnectionsFor(subjects)


    def updateWitnessWeights(self, value):
        """ Witnesses are just used as weight for fonts """
        
        if value > self.context.highest:
            self.context.highest = value
        if value < self.context.lowest:
            self.context.lowest = value


    def updateTree(self, keywords):
        """ Triggered on the update """
        
        tags = self.context.tagsTree
        for keyword in keywords:
            if keyword in self.context.tagsTree:
                self.context.tagsTree[keyword]['weight'] += 1
                addition = [k for k in keywords
                            if k != keyword and
                            k not in self.context.tagsTree[keyword]['connections']]
                self.context.tagsTree[keyword]['connections'].extend(addition)

            else:
                tag = dict(weight = 1,
                           connections = [k for k in keywords if k != keyword])
                self.context.tagsTree[keyword] = tag

            self.updateWitnessWeights(self.context.tagsTree[keyword]['weight'])
        self.context.tagsTree = tags


    def restrictTree(self):
        """ Will return a shuffled result """

        def sort_by_weight(key1, key2):
            return cmp(self.context.tagsTree[key2]['weight'],
                       self.context.tagsTree[key1]['weight'])

        keywords = self.context.tagsTree.keys()
        keywords.sort(sort_by_weight)

        if self.context.limit:
            keywords = keywords[:self.context.limit]

        for toDelete in self.context.tagsTree.keys():
            if toDelete not in keywords:
                del self.context.tagsTree[toDelete]

        self.context.keywords = keywords
        shuffle(self.context.keywords)


    def setTree(self):
        """ Initialize the cloud """

        catalog  = getToolByName(self.context, 'portal_catalog')
        putils   = getToolByName(self.context, 'plone_utils')
        encoding = putils.getSiteEncoding()

        self.context.tagsTree = dict()

        # First, we get all the keywords used in our portal
        # Then we transform the keywords into unicode objects
        # And we keep an untouched list of keywords (for the form vocabulary)
        subjects = catalog.uniqueValuesFor('Subject')
        self.context.all_keys = [unicode(k, encoding) for k in subjects]
        self.context.all_keys.sort()
        self.context.keywords = [k for k in self.context.all_keys]

        # Now, taking care of the restricted keywords, we build
        # a restricted list and query all the objects using them,
        # via the portal catalog.
        keywords = [k.encode(encoding) for k in self.context.keywords
                    if k not in self.context.restrict]
        objects  = catalog(Subject = keywords)

        # Using the main method, we build the references between the tags.
        # We build a list of tags for each objects, verifying the restriction.
        for obj in objects:
            self.updateTree([unicode(k, encoding) for k in obj.Subject
                              if k in keywords])

        if self.context.limit or len(self.context.restrict):
            self.restrictTree()
