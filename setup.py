from setuptools import setup

setup(name="dave",
      description="A command line utility that runs your command line scripts from a yaml script",
      long_description="Dave runs your machine learning scripts from a yaml configuration file",
      version="0.0.0",
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
      packages=["dave"],
      install_requires=[""]
      )
