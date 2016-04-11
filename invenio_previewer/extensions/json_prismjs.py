# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Previews a JSON file."""

from __future__ import absolute_import, print_function

import json
from collections import OrderedDict

from flask import current_app, render_template

previewable_extensions = ['json']


def render(file):
    """Pretty print the JSON file for rendering."""
    with file.open() as fp:
        file_content = fp.read().decode('utf-8')
        parsed_json = json.loads(file_content, object_pairs_hook=OrderedDict)
        return json.dumps(parsed_json, indent=4, separators=(',', ': '))


def validate_json(file):
    """Validate a JSON file."""
    max_file_size = current_app.config.get(
        'PREVIEWER_MAX_FILE_SIZE_BYTES', 1 * 1024 * 1024)
    if 'size' in file.file and file.file['size'] > max_file_size:
        return False

    with file.open() as fp:
        try:
            json.loads(fp.read().decode('utf-8'))
            return True
        except:
            return False


def can_preview(file):
    """Determine if the given file can be previewed."""
    return (file.is_local() and
            file.has_extensions('.json') and
            validate_json(file))


def preview(file):
    """Render appropiate template with embed flag."""
    return render_template(
        'invenio_previewer/json_prismjs.html',
        file=file.file,
        content=render(file),
        js_bundles=['previewer_prism_js'],
        css_bundles=['previewer_prism_css'],
    )