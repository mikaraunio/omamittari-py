import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

def requires():
    with open("requirements.txt", "r") as f:
        return [r.strip() for r in f.readlines()]

setup(name='omamittari',
      version='0.9.0',
      description='A Python client for the OmaMittari electricity API',
      url='https://github.com/mikaraunio/omamittary-py',
      author='Mika Raunio',
      author_email='mika+pypi@raun.io',
      license='BSD',
      packages=['omamittari'],
      install_requires=requires(),
      long_description=read('README.md'),
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Utilities",
          "License :: OSI Approved :: BSD License",
          "Intended Audience :: Developers",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Topic :: Home Automation",
          "Topic :: Software Development :: Libraries",
          "Topic :: Utilities",
      ],
      )
