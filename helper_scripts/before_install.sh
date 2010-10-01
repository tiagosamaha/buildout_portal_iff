#!/bin/sh

PLONE_HOME=/usr/local/Plone

DEPENDENCIES='
python2.4
python2.4-dev
python-imaging
python-setuptools
gcc
g++
make
bzip2
build-essential
libssl-dev
libpcre3-dev
pkg-config
ppthtml
xlhtml 
wv
xsltproc
unzip
poppler-utils
psmisc' 

for package in $DEPENDENCIES
do
    if (! dpkg -s $package > /dev/null 2> /dev/null)
    then
        apt-get install -y $package
    fi
done

easy_install-2.4 imsvdex
