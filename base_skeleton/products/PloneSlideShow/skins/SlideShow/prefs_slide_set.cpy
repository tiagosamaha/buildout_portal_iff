## Controller Python Script "prefs_slide_set"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=RESPONSE=None
##title=
##

request = container.REQUEST
RESPONSE =  request.RESPONSE


# Set variables request
title = request.get('title', None)
skinlist = request.get('skinlist', None)
portletskinlist = request.get('portletskinlist', None)
enable_portlet = request.get('enable_portlet', None)
slide_default_skin = request.get('slide_default_skin', None)
slide_default_portletskin = request.get('slide_default_portletskin', None)
portlet_transition_interval = request.get('portlet_transition_interval', None)


# PloneslideShow Property Sheet
properties = context.portal_properties.ploneslideshow_properties


if not title:
   request.set('title', 'PloneSlideShow properties')

if not skinlist:
   request.set('skinlist', list(()))

if not portletskinlist:
   request.set('portletskinlist', list(()))

if not enable_portlet:
   request.set('enable_portlet', False)

if not slide_default_skin:
   request.set('slide_default_skin', 'default')

if not slide_default_portletskin:
   request.set('slide_default_portletskin', 'default')

if not portlet_transition_interval:
   request.set('portlet_transition_interval', int(7000))

try:
   properties.manage_editProperties(request)
except:
   return state.set(status='failure', portal_status_message = 'PloneSlideShow settings update failure.')
else:
   return state.set(status='success', portal_status_message='PloneSlideShow settings update.')