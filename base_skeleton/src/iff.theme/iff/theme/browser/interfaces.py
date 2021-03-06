from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "iff_theme" theme, this interface must be its layer
       (in theme/viewlets/configure.zcml).
    """

class IHeaderFocusViewletManager(IViewletManager):
    """
    Header Focus Viewlet Manager
    """

class INewsViewletManager(IViewletManager):
    """
    News Viewlet Manager
    """

