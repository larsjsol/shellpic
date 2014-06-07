#!/usr/bin/env bash
# -*- coding: utf-8; mode: Shell-script -*-

set -e #exit on error

ARCH=$(uname -i)

cd $(dirname $0)

# set up the envioronment
mkdir -p workdir
rm -rf workdir/* # ensure that we start with a clean slate
virtualenv workdir
source workdir/bin/activate

# install shellpic
ln -s /usr/lib/$ARCH-linux-gnu/libfreetype.so workdir/lib/
ln -s /usr/lib/$ARCH-linux-gnu/libjpeg.so workdir/lib/
ln -s /usr/lib/$ARCH-linux-gnu/libz.so workdir/lib/
pip install -e ..


