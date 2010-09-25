ADD_CONTENT_PERMISSION = 'PloneSlideShow: Add Plone Slide Show'
PROJECTNAME = 'PloneSlideShow'
SKINS_DIR = 'skins'
SKINNAME = 'SlideShow'
META_TYPE = 'slideshow'
PORTAL_TYPE = 'Portal Slide Show'
TITLE = 'Plone Slide Show'
DESCRIPTION = 'Slide Show for Plone'
LISTPROPERTIES = (('slide_default_skin', 'string', 'default1'),
                  ('slide_default_portletskin','string','blue_style'),
                  ('portletskinlist', 'lines' , ['alert','blue_style','feminino','forest','graffs','gray','smile']),
                  ('enable_portlet','boolean',0),
                  ('with_description','boolean',1),
                  ('portlet_transition_interval','int',7000),
                  ('skinlist', 'lines' , ['aura','simple','default1','silver1','brown','dark_blue','default2','violet','blue','iff']),)

GLOBALS = globals()
