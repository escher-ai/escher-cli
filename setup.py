from os import path

from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README'), encoding='utf-8') as f:
    long_description = f.read()
setup(name="dave",
      description="A command line utility that runs your command line scripts from a yaml script",
      long_description=long_description,
      version="0.7.0",
      url="https://github.com/episodeyang/dave",
      author="Ge Yang",
      author_email="yangge1987@gmail.com",
      license=None,
      keywords=["dave", "experiment", "experimentation", "script runner"],
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Science/Research",
          "Programming Language :: Python :: 3"
      ],
      scripts=['bin/dave'],
      packages=["dave"],
      install_requires=["params_proto", "pathos", "pathlib", "munch", "ruamel.yaml"]
      )
