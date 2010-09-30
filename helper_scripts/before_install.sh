#!/bin/sh

PLONE_HOME=/usr/local/Plone

DEPENDENCIES='
python2.4
python-imaging
gcc
g++
make
bzip2
python2.4-dev
build-essential
libssl-dev
libpcre3-dev
pkg-config
ppthtml
xlhtml 
wv
xsltproc
unzip
pdftohtml' 

for package in $DEPENDENCIES
do
    if (! dpkg -s $package > /dev/null 2> /dev/null)
    then
        `apt-get install -y $package`
    fi
done

`./$PLONE_HOME/Python-2.4/bin/easy_install imsvdex`
