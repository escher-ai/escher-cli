from os import path

from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README'), encoding='utf-8') as f:
    long_description = f.read()
setup(name="escher-cli",
      description="A command line utility that runs your command line scripts from a yaml script",
      long_description=long_description,
      version="0.0.0",
      url="https://github.com/episodeyang/escher-cli",
      author="Ge Yang",
      author_email="yangge1987@gmail.com",
      license=None,
      keywords=["escher", "escher-cli", "experiment", "experimentation", "script runner", "deep learning",
                "machine learning"],
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Science/Research",
          "Programming Language :: Python :: 3"
      ],
      scripts=['bin/escher'],
      packages=["escher"],
      install_requires=["params_proto", "pathos", "pathlib", "munch", "ruamel.yaml"]
      )
