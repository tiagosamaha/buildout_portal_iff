from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='iff.theme',
      version=version,
      description="An installable theme for Plone 3.0",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='iff theme zope plone web nsi',
      author='Gustavo Rezende, Diego Pinheiro, Ronaldo Amaral',
      author_email='<nsigustavo@gmail.com>, <dmpinheiro@gmail.com>, <ronaldinho.as@gmail.com>',
      url='http://iff.edu.br',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['iff'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'BeautifulSoup',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins = ["ZopeSkel"],
      )
