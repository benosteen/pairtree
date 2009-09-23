#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
FS Pairtree storage
==============

Conventions used:

From http://www.cdlib.org/inside/diglib/pairtree/pairtreespec.html version 0.1

"""

from pairtree_client import PairtreeStorageClient

class PairtreeStorageFactory(object):
    def get_store(self, store_dir="data", uri_base=None, shorty_length=2):
        return PairtreeStorageClient(uri_base, store_dir, shorty_length)
