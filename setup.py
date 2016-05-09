__author__ = 'mmayer'

from setuptools import setup

setup(name='BitArrayX',
      version='0.2',
      description='BitArray with extended Boolean logic 0,1,x where "x" identifies an \
        unknown/undefined/contaminated value.',
      url='https://github.com/mayeranalytics/BitArrayX',
      author='Mayer Analytics',
      author_email='mmayer@mayeranalytics.com',
      license='GPL',
      packages=['BitArrayX'],
      zip_safe=False,
      test_suite='unittest2.collector',
      tests_require=['unittest2'],
)