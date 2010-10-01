#!/bin/sh

CURRENT_DIRECTORY=`pwd`
PLONE_HOME=/usr/local/Plone
ZEOCLUSTER_HOME=zeocluster

`cp -r $CURRENT_DIRECTORY/after_install/sd $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client1/lib/python`
`cp $CURRENT_DIRECTORY/after_install/sd-configure.zcml $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client1/etc/package-includes`

`cp -r $CURRENT_DIRECTORY/after_install/sd $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client2/lib/python`
`cp $CURRENT_DIRECTORY/after_install/sd-configure.zcml $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client2/etc/package-includes`

`cp -r $CURRENT_DIRECTORY/after_install/sd $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client3/lib/python`
`cp $CURRENT_DIRECTORY/after_install/sd-configure.zcml $PLONE_HOME/$ZEOCLUSTER_HOME/parts/client3/etc/package-includes`

`cp $CURRENT_DIRECTORY/after_install/sitecustomize.py $PLONE_HOME/Python-2.4/lib/python2.4`

`cp $CURRENT_DIRECTORY/cluster_scripts/startCluster.sh $PLONE_HOME/$ZEOCLUSTER_HOME`
`cp $CURRENT_DIRECTORY/cluster_scripts/stopCluster.sh $PLONE_HOME/$ZEOCLUSTER_HOME`
`cp $CURRENT_DIRECTORY/cluster_scripts/restartCluster.sh $PLONE_HOME/$ZEOCLUSTER_HOME`
