# conf.py located in proj_root/docs/source/conf.py

import os
import sys

# Add the project root to the path to make the vulcan_utils package available to Sphinx
sys.path.insert(0, os.path.abspath('../../'))

project = 'Vulcan Utils'
copyright = '2024, Jacob Holland'
author = 'Jacob Holland'
release = '0.0.1'

extensions = [
    'sphinx.ext.autodoc',  # Automatically document code
    'sphinx.ext.viewcode',  # Add "View Source" links to the documentation
    'sphinx.ext.napoleon',  # Support for Google and Numpy docstring styles
    'sphinx_rtd_theme',  # ReadTheDocs theme
    "myst_parser",  # Markdown support using MyST
]

html_theme = 'sphinx_rtd_theme'
templates_path = ['_templates']
exclude_patterns = []
html_static_path = ['_static']
