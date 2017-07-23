#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from __future__ import print_function


def clv_history_marker_get_id(
    client, history_marker_name, history_marker_code=False,
    history_marker_description=False, history_marker_notes=False
):

    history_marker_model = client.model('clv.history_marker')
    history_marker_browse = history_marker_model.browse([('name', '=', history_marker_name), ])
    history_marker_id = history_marker_browse.id

    if history_marker_id == []:
        values = {
            'name': history_marker_name,
            'code': history_marker_code,
            'description': history_marker_description,
            'notes': history_marker_notes,
        }
        history_marker_id = history_marker_model.create(values).id
    else:
        history_marker_id = history_marker_id[0]

    return history_marker_id
