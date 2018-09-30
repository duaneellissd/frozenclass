
from setuptools import setup

setup( name='frozenclass',
       version='1.1',
       description='Class decorator to prevent attribute spelling mistakes',
       long_description='This decorator helps prevent simple spelling typos for class attributes by introducing a freeze() and thaw() methods',
       url='http://github.com/duaneellissd/frozenclass',
       author='Duane Ellis',
       author_email='duane@duaneellis.com',
       keywords=['frozen-class', 'decorator', 'typo-prevention' ],
       license='PSF - Same as Python',
       platforms='any',
       test_suite='tests',
       packages=['frozenclass'] )

