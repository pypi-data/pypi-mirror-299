from setuptools import setup, find_packages
import codecs
import os
import pandas
import string
import warnings
import pandas as pd
import gensim.downloader as api
from nltk.tokenize import word_tokenize

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
VERSION = '1.7'
DESCRIPTION = 'Library to get sentence vectors using SIF and uSIF'
LONG_DESCRIPTION = 'This library will let get a single vector for a sentence for a dimension'


setup(
    name="marcel_fse",
    version=VERSION,
    author="Marcel Tino",
    author_email="<marceltino92@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['gensim','nltk','pandas','wordfreq'],
    keywords=[])
