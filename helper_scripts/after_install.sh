#!/bin/sh

PLONE_HOME=/usr/local/Plone
ZEOCLUSTER_HOME=zeocluster

`cp -r $PLONE_HOME/$ZEOCLUSTER_HOME/after_install/sd $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client1/lib/python`
`cp $PLONE_HOME/$ZEOCLUSTER_HOME/after_install/sd-configure.zcml $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client1/etc/package-includes`

`cp -r $PLONE_HOME/$ZEOCLUSTER_HOME/after_install/sd $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client2/lib/python`
`cp $PLONE_HOME/$ZEOCLUSTER_HOME/after_install/sd-configure.zcml $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client2/etc/package-includes`

`cp -r $PLONE_HOME/$ZEOCLUSTER_HOME/after_install/sd $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client3/lib/python`
`cp $PLONE_HOME/$ZEOCLUSTER_HOME/after_install/sd-configure.zcml $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client3/etc/package-includes`

`cp $PLONE_HOME/$ZEOCLUSTER_HOME/after_install/sitecustomize.py $PLONE_HOME/Python-2.4/lib/python2.4`
