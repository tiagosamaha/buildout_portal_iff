ABOUT

 Structured Document is a content type allowing people to structure
 their document into chapter then into paragraphs.


DEPENDANCIES

 This product depends on :

   Plone : 3.1.1 or later (http://plone.org)


INSTALLATION

 This is a python package, meant to live in your $instance/lib/python.
 To install the product :

  - uncompress the archive in the $instance/lib/python folder or get the last
    svn version with the following command in your $instance/lib/python:
    'svn co https://tracker.trollfot.org/svn/projects/StructuredDocument/trunk/ sd'

  - add a file named 'sd-configure.zcml' in the $instance/etc/package-includes
    folder

  - this file must contain : '<include package="sd.app" />'

 Note : '$instance' is the path where your Zope instance lives
 (eg. /var/zope2.10/instances/my-instance)


CREDITS

 - All code by Souheil Chelfouh <souheil@chelfouh.com>


TRANSLATION TEAM
 
 [French]
 Souheil Chelfouh


LICENSE

 This product is distributed under the GPL license
 (See file LICENSE.GPL or LICENSE.txt)

 Icons used in this product are taken from the Gnome Project.
 http://art.gnome.org. They are distributed under GPL license.


THANKS TO...

 Randomly: Jean Nicolas Bès, Thierry Benita, Jan Ulrich Hasecke,
           Sylvain Viollon, Olivier Laurelli and some others...