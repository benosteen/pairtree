#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
FS Pairtree storage
==============

Conventions used:

From http://www.cdlib.org/inside/diglib/pairtree/pairtreespec.html version 0.1

"""

import os, sys, shutil

import codecs

import string

from storage_exceptions import *

class PairtreeStorageObject(object):
    def __init__(self, id, fs_store_client):
        self.fs = fs_store_client
        self.id = id
        self.uri = "%s%s" % (self.fs.uri_base, id)

    def add_bytestream(self, filename, bytestream, path=None, buffer_size=None):
        if buffer_size:
            return self.fs.put_stream(self.id, path, filename, bytestream, buffer_size)
        return self.fs.put_stream(self.id, path, filename, bytestream)

    def add_bytestream_by_path(self, filepath, bytestream, buffer_size=None):
        path, filename = os.path.split(filepath)
        if buffer_size:
            return self.add_bytestream(filename, bytestream, path, buffer_size)
        return self.add_bytestream(filename, bytestream, path)

    def get_bytestream(self, filename, streamable=False, path=None):
        return self.fs.get_stream(self.id, path=path, stream_name=filename, streamable=streamable)

    def get_bytestream_by_path(self, filepath, streamable=False):
        path, filename = os.path.split(filepath)
        return self.get_bytestream(filename, streamable, path)

    def add_file(self, from_file_location, path=None, new_filename=None, buffer_size=None):
        if os.path.exists(from_file_location):
            if not new_filename:
                _, new_filename = os.path.split(from_file_location)
            fh = open(from_file_location, 'rb')
            if buffer_size:
                self.fs.put_stream(self.id, path, new_filename, bytestream=fh, buffer_size=buffer_size)
            self.fs.put_stream(self.id, path, new_filename, bytestream=fh)
            fh.close()
        else:
            raise FileNotFoundException

    def del_file(self, filename, path=None):
        return self.fs.del_part(self.id, partid)

    def del_file_by_path(self, filepath, bytestream):
        path, filename = os.path.split(filepath)
        return self.del_file(filename, path)

    def list_parts(self, path=None):
        return self.fs.list_parts(self.id, path)

    def download_fetchtxt_urls(self, fetchtxt, retry_on_checksum_error = True):
        pass

    def add_bagit_information(self):
        pass

    def remove_bagit_information(self):
        pass

