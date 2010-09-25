====================
Quadra Folderview
====================
    
    First, we must perform some setup. We use the testbrowser that is shipped
    with Five, as this provides proper Zope 2 integration. Most of the 
    documentation, though, is in the underlying zope.testbrower package.
    
    
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    
    
    The following is useful when writing and debugging testbrowser tests. It lets 
    us see all error messages in the error_log.
    
    
    >>> self.portal.error_log._ignored_exceptions = ()
    
    Login as administrator user
    ---------------------------------------------------------------------------
    
    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser.open(portal_url + '/login_form?came_from=' + portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

    
    Adding test folder "Folder1" with id="folder1"
    ---------------------------------------------------------------------------
    
    >>> browser.open(portal_url)
    
    ###### adds the folder
    
    >>> browser.getLink(id='folder').click()
    >>> browser.getControl(name='title').value = "Folder1"
    >>> browser.getControl(name='form_submit').click()
    
    ###### check if our new folder exists
    
    >>> 'folder1' in self.portal.objectIds()
    True
    
    ###### now we should be in the folder context
    
    See if Portlet-like-View is available
    ---------------------------------------------------------------------------
    
    >>> browser.getLink(id='Porlet-like-View').url.endswith("selectViewTemplate?templateId=Porlet-like-View")
    True
