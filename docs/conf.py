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

from sphinx.ext import autodoc

sys.path.insert(0, os.path.abspath('.'))

extensions = [
	'pallets_sphinx_themes',
	'sphinx.ext.autodoc',
	'sphinx.ext.intersphinx',
	'sphinx.ext.viewcode',
	'sphinx_issues',
	'sphinxcontrib.autohttp.flask',
]

primary_domain = 'py'
default_role = 'py:obj'

intersphinx_mapping = {'python': ('https://python.readthedocs.io/en/latest/', None)}

source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']

project = 'deploy-webhook'
copyright = '2020 Pavle Portic'

html_theme = 'flask'


class SimpleDocumenter(autodoc.MethodDocumenter):
	objtype = 'simple'
	content_indent = ''

	def add_directive_header(self, sig):
		pass


def setup(app):
	app.add_autodocumenter(SimpleDocumenter)
