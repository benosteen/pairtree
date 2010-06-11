from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name="Pairtree",
      version="0.5.5",
      description="Pairtree FS implementation.",
      long_description="""\
From http://www.cdlib.org/inside/diglib/pairtree/pairtreespec.html : Pairtree, a filesystem hierarchy for holding objects that are located by mapping identifier strings to object directory (or folder) paths two characters at a time. If an object directory (folder) holds all the files, and nothing but the files, that comprise the object, a "pairtree" can be imported by a system that knows nothing about the nature or structure of the objects but can still deliver any object's files by requested identifier. The mapping is reversible, so the importing system can also walk the pairtree and reliably enumerate all the contained object identifiers. To the extent that object dependencies are stored inside the pairtree (e.g., fast indexes stored outside contain only derivative data), simple or complex collections built on top of pairtrees can recover from index failures and reconstruct a collection view simply by walking the trees. Pairtrees have the advantage that many object operations, including backup and restore, can be performed with native operating system tools.
""",
      author="Ben O'Steen",
      author_email="bosteen@gmail.com",
      url="http://packages.python.org/Pairtree/",
      scripts = ['bin/ppath'],
      license="http://www.apache.org/licenses/LICENSE-2.0",
      packages=find_packages(),
      test_suite = "tests.test.TestPairtree",
      )

