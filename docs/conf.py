#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD 3-Clause license.

# Sphinx config

import os
import sys

from pallets_sphinx_themes import ProjectLink
from sphinx.ext import autodoc

sys.path.insert(0, os.path.abspath('.'))

# Project --------------------------------------------------------------

project = "Deploy-Webhook"
copyright = "2020 Pavle Portic"
author = "Pavle Portic"

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
	'pallets_sphinx_themes',
	'sphinx.ext.autodoc',
	'sphinx.ext.intersphinx',
	'sphinx.ext.viewcode',
	'sphinx_issues',
	'sphinxcontrib.autohttp.flask',
]
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}
issues_github_path = 'TheEdgeOfRage/deploy-webhook'
exclude_patterns = ['_build']
source_suffix = '.rst'

# HTML -----------------------------------------------------------------

html_theme = "werkzeug"
html_context = {
	"project_links": [
		ProjectLink("Source Code", "https://github.com/TheEdgeOfRage/deploy-webhook/"),
		ProjectLink("Issue Tracker", "https://github.com/TheEdgeOfRage/deploy-webhook/issues/"),
		ProjectLink("Docker Hub", "https://hub.docker.com/r/theedgeofrage/deploy-webhook"),
	]
}
html_sidebars = {
	"index": ["project.html", "localtoc.html", "searchbox.html"],
	"**": ["localtoc.html", "relations.html", "searchbox.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
html_title = "Deploy-Webhook documentation"
html_show_sourcelink = False


class SimpleDocumenter(autodoc.MethodDocumenter):
	objtype = 'simple'
	content_indent = ''

	def add_directive_header(self, sig):
		pass


def setup(app):
	app.add_autodocumenter(SimpleDocumenter)
