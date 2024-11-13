# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))  # Path to your go1pylib package

# -- Project information -----------------------------------------------------
project = 'go1pylib'
author = 'Chinmay Nehate'
release = '0.1.5'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',        # Support for Google/NumPy style docstrings
    'sphinx_autodoc_typehints',   # Type hint support
    'myst_parser'                 # Support for Markdown if README.md is used
]

# Support for both .rst and .md files in Sphinx
source_suffix = ['.rst']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and directories to ignore when looking for source files.
exclude_patterns = []

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
}

# Paths for static files (such as style sheets)
html_static_path = ['_static']

# -- Options for autodoc -----------------------------------------------------
autodoc_typehints = 'description'

# -- Options for napoleon ----------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# -- Options for myst-parser -------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "substitution",
    "tasklist",
]
