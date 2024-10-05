from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.1'
DESCRIPTION = 'a package containing more utilities for python'
LONG_DESCRIPTION = 'a package containing more utilities for python'

setup(
    name="MoreUtilspy",
    version=VERSION,
    author="oussama errafif",
    author_email="oussamaerra2002@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'numpy', 'pandas', 'matplotlib', 'scikit-learn', 'seaborn', 'nltk', 'scipy', 'tqdm', 'torch', 'torchvision', 'transformers', 'sentencepiece', 'tensorflow', 'keras', 'gensim', 'spacy', 'stanza', 'beautifulsoup4', 'requests', 'flask', 'fastapi', 'uvicorn', 'streamlit', 'dash', 'plotly', 'bokeh', 'dash-bootstrap-components', 'dash-core-components', 'dash-html-components', 'dash-renderer', 'dash-table', 'dash-daq', 'dash-cytoscape', 'dash-canvas', 'dash-uploader', 'dash-extensions', 'dash-leaflet', 'dash-geoplot', 'dash-bio', 'dash-bio-utils', 'dash-cytoscape'
    ], 
    keywords=['python', 'utils'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
