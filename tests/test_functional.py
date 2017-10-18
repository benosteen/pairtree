# -*- coding: UTF-8 -*-
import unittest, tempfile, os, shutil, hashlib
from pairtree import PairtreeStorageFactory
from io import BytesIO


class TestPairtree(unittest.TestCase):

    def setUp(self):
        self.base_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.test_file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'dummy_image.jpg')

    def tearDown(self):
        shutil.rmtree(self.base_dir)

    def test_store_file_should_create_identical_file(self):
        storage_factory = PairtreeStorageFactory()
        store = storage_factory.get_store(store_dir=self.data_dir, uri_base="http://dummy")
        object = store.create_object('test')
        with open(self.test_file_path, 'rb') as test_file:
            object.add_bytestream('dummy.jpg', test_file)

        orig_hash = hashlib.md5(open(self.test_file_path, 'rb').read()).hexdigest()
        created_hash = hashlib.md5(open(os.path.join(object.location, 'dummy.jpg'), 'rb').read()).hexdigest()

        self.assertEqual(orig_hash, created_hash)

    def test_create_object_and_file_should_exist_according_to_store(self):
        storage_factory = PairtreeStorageFactory()
        store = storage_factory.get_store(store_dir=self.data_dir, uri_base="http://dummy")
        id = u'owërdœ.file'
        object = store.create_object(id)
        with open(self.test_file_path, 'rb') as test_file:
            object.add_bytestream('dummy', test_file)

        self.assertTrue(store.isfile(id, 'dummy'))

    def test_create_object_and_file_store_should_be_able_to_retreive_identical_file(self):
        storage_factory = PairtreeStorageFactory()
        store = storage_factory.get_store(store_dir=self.data_dir, uri_base="http://dummy")
        id = u'owërdœ.file'
        object = store.create_object(id)
        with open(self.test_file_path, 'rb') as test_file:
            object.add_bytestream('dummy', test_file)

        retreived_bytestream = object.get_bytestream('dummy')
        orig_hash = hashlib.md5(open(self.test_file_path, 'rb').read()).hexdigest()
        created_hash = hashlib.md5(retreived_bytestream).hexdigest()

        self.assertEqual(orig_hash, created_hash)

    def test_update_object_and_get_through_store_should_get_identical_bytestream(self):

        # create file
        storage_factory = PairtreeStorageFactory()
        store = storage_factory.get_store(store_dir=self.data_dir, uri_base="http://dummy")
        id = u'owërdœ.file'
        object = store.create_object(id)
        with open(self.test_file_path, 'rb') as test_file:
            object.add_bytestream('dummy.txt', test_file)

        # update file
        handle_large_file_2 = BytesIO()
        handle_large_file_2.write(b'baz')
        handle_large_file_2.seek(0)
        object.add_bytestream('dummy.txt', handle_large_file_2)

        handle_large_file_2.close()

        # create check
        string_io_container = BytesIO()
        string_io_container.write(b'baz')

        retreived_bytestream = object.get_bytestream('dummy.txt')
        orig_hash = hashlib.md5(string_io_container.getvalue()).hexdigest()
        created_hash = hashlib.md5(retreived_bytestream).hexdigest()

        self.assertEqual(orig_hash, created_hash)

    def test_delete_file_should_be_removed_from_file_system(self):
        storage_factory = PairtreeStorageFactory()
        store = storage_factory.get_store(store_dir=self.data_dir, uri_base="http://dummy")
        object = store.create_object('test')
        file_path = self.test_file_path
        object.add_file(file_path)
        self.assertTrue(os.path.isfile(os.path.join(object.location, 'dummy_image.jpg')))

        object.del_file('dummy_image.jpg')

        self.assertFalse(os.path.isfile(os.path.join(object.location, 'dummy_image.jpg')))

    def test_delete_object_should_remove_file_from_system(self):
        storage_factory = PairtreeStorageFactory()
        store = storage_factory.get_store(store_dir=self.data_dir, uri_base="http://dummy")
        object = store.create_object('test')
        file_path = self.test_file_path
        object.add_file(file_path)
        self.assertTrue(os.path.isfile(os.path.join(object.location, 'dummy_image.jpg')))

        store.delete_object('test')

        self.assertFalse(os.path.exists(object.location))







