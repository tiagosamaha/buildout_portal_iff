from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_quadra_folderviews():
    """Set up the additional products required for the Quadra Folderviews.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    
    # Load the ZCML configuration for the quadra.folderviews package.
    # This includes the other products below as well.
    
    fiveconfigure.debug_mode = True
    import quadra.folderviews
    zcml.load_config('configure.zcml', quadra.folderviews)
    fiveconfigure.debug_mode = False
    
    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.
    
    ztc.installPackage('quadra.folderviews')
    
# The order here is important: We first call the (deferred) function which
# installs the products we need for the Quadra package. Then, we let 
# PloneTestCase set up this product on installation.

setup_quadra_folderviews()
ptc.setupPloneSite(products=['quadra.folderviews'])

def baseAfterSetUp( self ):
    """Code that is needed is the afterSetUp of both test cases.
    """

    # This looks like a safe place to install Five.
    ztc.installProduct('Five')

    # XXX monkey patch everytime (until we figure out the problem where
    #   monkeypatch gets overwritten somewhere) 
    try:
        from Products.Five import pythonproducts
        pythonproducts.setupPythonProducts(None)
    except ImportError:
        # Not needed in Plone 3
        pass
    
class QuadraFolderviewsFunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
     """
    def afterSetUp(self):
        baseAfterSetUp(self)
    
    def beforeTearDown(self):
        pass    
