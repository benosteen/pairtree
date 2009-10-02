from pairtree import *

# Get the store 'factory'
f = PairtreeStorageFactory()

# For a new store it is very important to set uri_base
# This restriction can be relaxed if necessary
store = f.get_store(store_dir="data", uri_base="info:local/", shorty_length=2, hashing_type='md5')

# Creates a directory in the cwd called 'data' and adds some pairtree boilerplate
# files

# Create object - this method throws an exception if the object already
# exists
# Use get_object if you do not care whether it existed on disc and just want a
# object to write and read from.
foobar = store.get_object('foobar')
# foobar = store.get_object('foobar')

# Add a byte sequence
md5hash = foobar.add_bytestream('foobar.txt', """Can just be an in memory string of bytes""")

print "%s hash of foobar.txt = %s" % (md5hash)

# Faking a file handle to a large file we'd rather streamed than copy into
# memory
from StringIO import StringIO
handle_to_large_file = StringIO()
handle_to_large_file.write('Foo bar foo bar foo bar foo bar foo bar foo bar')
handle_to_large_file.seek(0)
# End fakery...

# Store the large file in the root of the pairtree object and
# call it 'large_file.txt'
md5hash = foobar.add_bytestream('large_file.txt', handle_to_large_file)

print "%s hash of large file = %s" % (md5hash)

print foobar.list_parts()

# Create a file on disc
fn = open('/tmp/foo.txt', 'w')
fn.write('bah and foo')
fn.close()

# stream file from on disc location into the pairtree object
# but put it into a 'data/mine' directory
print "%s file hash = %s" % (foobar.add_file('/tmp/foo.txt', 'data/mine'))

# create a new object to test 'split-end' handling
foobartoo = store.create_object('foobartoo')
print "foomanchu.txt - %s: %s" % (foobartoo.add_bytestream('foomanchu.txt', 'Nothing to see here. Move along'))

# Results should be mostly unchanged from before
# with the only addition being the data directory
print foobar.list_parts()

# Results should just be foomanchu.txt
print foobartoo.list_parts()

# create a new object to test recursive path deletion
# in objects
foobarthree = store.create_object('foobarthree')

store.delete_object('foobarthree')

