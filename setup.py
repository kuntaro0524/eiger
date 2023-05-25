#!/usr/bin/env python3
from distutils.core import setup
from dectris_eiger import __version__ as ver


setup(name="dectris_eiger",
      version=ver,
      description="API to the Dectris Eiger detector.",
      author="Sven Festersen",
      author_email="festersen@physik.uni-kiel.de",
      requires=["requests"],
      packages=["dectris_eiger"]
     )
