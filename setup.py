import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid', 
    'pyramid_debugtoolbar',
    'voteit.core',
    'betahaus.viewcomponent',
    'betahaus.pyracont',
    'lingua',
    'Babel',
    'colander',
    'deform',
]

setup(name='voteit.tools',
      version='0.0',
      description='voteit.tools',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='VoteIT dev team',
      author_email='info@voteit.se',
      url='http://www.voteit.se',
      keywords='web pyramid pylons voteit',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="voteit.tools",
      entry_points = """\
      """,
      paster_plugins=['pyramid'],
      )

