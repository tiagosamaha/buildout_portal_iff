from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from iff.types import typesMessageFactory as _

# -*- extra stuff goes here -*-

class IArteeCultura(Interface):
    """Description of the Example Type"""

class IInformes(Interface):
    """Informes Processo Seletivo / Recursos, Reclassificacao, etc.."""

class IChamada(Interface):
    """Chamada Processo Seletivo"""

class IProcessoSeletivo(Interface):
    """Processo Seletivo / Vestibular / Concomitancia"""

class IPortletContainer(Interface):
    """Portlet Container Content Type"""
