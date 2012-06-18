from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='django-offload-utils',
      version=version,
      description="Utilities to offload long loading pages",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='offloading task-management django web',
      author='Kyle Terry',
      author_email='kyle@aquameta.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'django-celery',
          'django-jsonfield',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
