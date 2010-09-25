quadra.folderviews Package Readme
=========================

Overview
--------

This product adds another view available in views pannel for the ATFolder type.
It's a portlet-like view, one portlet is created for each subfolder found in the targeted folder and another one for non-folderish documents.
It gets every subfolder of the folder and shows the five last elements created in this folder, adding a link like '...' if there's more than five elements into it, it's a direct link to the selected folder like "{portal_url}/folder/subfolder1".
For non-folderish documents they are all grouped in one single portlet called "Documents" but not limited to the five last ones created.

It uses a lot of plone's default classes so that you can customize it easily and that you won't have to modify the folderporlet.css (which mainly sets a default height for the subfolders portlets and a default width of 31%)

There are 3 mains elements:
  - the template : folderview.pt
  - the python script with the associated class and methods: folderview.py
  - the associated stylesheet remaining in browser/stylesheets : folderportlet.css

    I'd like to thank the following people and communities for the products i've used to inspirate myself:
    -"Matt Howell":http://www.matticus.com and sponsored by "sharp i.t.":http://www.sharpit.com
    - Plone Help Center's (PHC) helpcenter_view:
      "Plone Help Center":http://svn.plone.org/svn/collective/PloneHelpCenter/trunk/skins/plone_help_center/helpcenter_view.pt
    - Plone How To:
      "Creating a Plone Help Center like view for folders":http://plone.org/documentation/how-to/boxedfolderlisting
        
New for Plone 3.0+ : This product doesn't create a directory anymore.
