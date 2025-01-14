import os
import sys

sys.path.insert(0, os.path.abspath(".."))

import mistune
import sphinx_typlog_theme

project = "Mistune"
copyright = "2019, Hsiaoming Yang"
author = "Hsiaoming Yang"

# The full version, including alpha/beta/rc tags
version = mistune.__version__
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_typlog_theme"
html_theme_path = [sphinx_typlog_theme.get_path()]
html_theme_options = {
    "description": (
        "A fast yet powerful Python Markdown parser " "with renderers and plugins"
    ),
    "color": "#3E7FCB",
    "github_user": "lepture",
    "github_repo": "mistune",
    "twitter": "lepture",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_sidebars = {
    "**": [
        "logo.html",
        "github.html",
        "sponsors.html",
        "globaltoc.html",
        "links.html",
        "searchbox.html",
    ]
}


def setup(app):
    sphinx_typlog_theme.add_badge_roles(app)
    sphinx_typlog_theme.add_github_roles(app, "lepture/mistune")
