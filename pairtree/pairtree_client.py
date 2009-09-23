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

from pairtree_object import PairtreeStorageObject

class PairtreeStorageClient(object):
    def __init__(self, uri_base, store_dir, shorty_length):
        self.store_dir = store_dir
        self.uri_base = None
        if uri_base:
            self.uri_base = uri_base
        self.shorty_length = shorty_length
        self._init_store()

    def id_encode(self, id):
        multichar_mapping = {'"':'^22',
                             '<':'^3c',
                             '?':'^3f',
                             '*':'^2a',
                             '=':'^3d',
                             '^':'^5e',
                             '+':'^2b',
                             '>':'^3e',
                             '|':'^7c',
                             ',':'^2c'
                            }
        new_id = []
        for char in id:
            new_id.append(multichar_mapping.get(char, char))
        return "".join(new_id).translate(string.maketrans('/:.','=+,'))
    
    def id_decode(self, id):
        multichar_mapping = {'22':'"',
                             '3c':'<',
                             '3f':'?',
                             '2a':'*',
                             '3d':'=',
                             '5e':'^',
                             '2b':'+',
                             '3e':'>',
                             '7c':'|',
                             '2c':','
                            }
        dec_id = id.translate(string.maketrans('=+,','/:.'))
        index = 0
        new_id = []
        print len(dec_id)
        while index < len(dec_id):
            if dec_id[index] == '^':
                code = "".join(dec_id[index+1:index+3]).lower()
                if code in multichar_mapping:
                    new_id.append(multichar_mapping[code])
                    index = index + 2
                else:
                    raise Exception("Unknown character code found.")
            else:
                new_id.append(dec_id[index])
            index = index +1
        return "".join(new_id)

    def _get_id_from_dirpath(self, dirpath):
        path = self._get_path_from_dirpath(dirpath)
        return self.id_decode("".join(path))

    def _get_path_from_dirpath(self, dirpath):
        head, tail = os.path.split(dirpath)
        path = [tail]
        while not self.store_dir == head:
            head, tail = os.path.split(head)
            path.append(tail)
        path.reverse()
        return path

    def _id_to_dirpath(self, id):
        enc_id = self.id_encode(id)
        dirpath = self.store_dir
        while enc_id:
            dirpath = os.path.join(dirpath, enc_id[:self.shorty_length])
            enc_id = enc_id[self.shorty_length:]
        return dirpath

    def _init_store(self):
        if not os.path.exists(self.store_dir):
            if self.uri_base:
                os.mkdir(self.store_dir)
                f = open(os.path.join(self.store_dir, "pairtree_version0_1"), "w")
                f.write("This directory conforms to Pairtree Version 0.1. Updated spec: http://www.cdlib.org/inside/diglib/pairtree/pairtreespec.html")
                f.close()
                f = open(os.path.join(self.store_dir, "pairtree_prefix"),"w")
                f.write(self.uri_base)
                f.close()
            else:
                raise NotAPairtreeStoreException("""No uri_base set for a non-existent
                                                    store - store cannot be instanciated""")
        else:
            if os.path.exists(os.path.join(self.store_dir, "pairtree_version0_1")):
                """Seems to be a pairtree0_1 compliant 'store'"""
                if os.path.exists(os.path.join(self.store_dir, "pairtree_prefix")):
                    """Read the uri base of this store"""
                    f = open(os.path.join(self.store_dir, "pairtree_prefix"),"r")
                    prefix = f.read().strip()
                    f.close()
                    self.uri_base = prefix
            else:
                raise NotAPairtreeStoreException

        if not os.path.isdir(self.store_dir):
            raise NotAPairtreeStoreException

    def list_ids(self):
        # TODO: Need to make sure this corresponds to pairtree spec...
        objects = set()
        paths = [os.path.join(self.store_dir, x) for x in os.listdir(self.store_dir) if os.path.isdir(os.path.join(self.store_dir, x))]
        d = None
        if paths:
            d = paths.pop()
        while d:
            for t in [x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))]:
                if len(t)>self.shorty_length:
                    objects.add(self._get_id_from_dirpath(d))
                else:
                    paths.append(os.path.join(d, t))
            if paths:
                d = paths.pop()
            else:
                d =False
        return objects

    def _create(self, id):
        dirpath = self._id_to_dirpath(id)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        else:
            raise ObjectAlreadyExistsException
        return PairtreeStorageObject(id, self)

    def list_parts(self, id, path):
        dirpath = os.path.join(self._id_to_dirpath(id))
        if path:
            dirpath = os.path.join(self._id_to_dirpath(id), path)
        if not os.path.exists(dirpath):
            raise ObjectNotFoundException
        return os.listdir(dirpath)

    def put_stream(self, id, path, stream_name, bytestream, buffer_size = 1024 * 8):
        """Can be either a bytestring, or a filelike object which supports
           bytestream.read(chunk_size)"""
        dirpath = os.path.join(self._id_to_dirpath(id))
        if path:
            dirpath = os.path.join(self._id_to_dirpath(id), path)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        f = open(os.path.join(dirpath, stream_name), "wb")
        try:
            # Stream file-like objects in with buffered reads
            if hasattr(bytestream, 'read'):
                if not buffer_size:
                    buffer_size = 1024 * 8
                chunk = bytestream.read(buffer_size)
                while chunk:
                    f.write(chunk)
                    chunk = bytestream.read(buffer_size)
            else:
                f.write(bytestream)
        finally:
            f.close()

    def get_stream(self, id, path, stream_name, streamable=True):
        file_path = os.path.join(self._id_to_dirpath(id), stream_name)
        if path:
            file_path = os.path.join(self._id_to_dirpath(id), path, stream_name)
        if not os.path.exists(file_path):
            raise PartNotFoundException(id=id, path=path, stream_name=stream_name,file_path=file_path)
        f = open(file_path, "rb")
        if streamable:
            return f
        else:
            bytestream = f.read()
            f.close()
            return bytestream

    def del_stream(self, id, stream_name):
        file_path = os.path.join(self._id_to_dirpath(id), stream_name)
        if path:
            file_path = os.path.join(self._id_to_dirpath(id), path, stream_name)
        if not os.path.exists(file_path):
            raise PartNotFoundException(id=id, path=path, stream_name=stream_name,file_path=file_path)
        os.remove(file_path)

    def exists(self, id):
        dirpath = os.path.join(self._id_to_dirpath(id))
        return os.path.exists(dirpath)

    def _get_new_id(self):
        id = "%.14d" % random.randint(0,99999999999999)
        while self.exists(id):
            id = "%.14d" % random.randint(0,99999999999999)
        return id

    def get_object(self, id=None, create_if_doesnt_exist=True):
        if not id:
            id = self._get_new_id()
            return self._create(id)
        elif self.exists(id):
            return PairtreeStorageObject(id, self)
        elif create_if_doesnt_exist:
            return self._create(id)
        else:
            raise ObjectNotFoundException

    def create_object(self, id):
        if self.exists(id):
            raise ObjectAlreadyExistsException
        else:
            return self._create(id)

