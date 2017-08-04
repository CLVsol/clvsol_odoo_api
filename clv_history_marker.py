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

import sqlite3


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


def clv_history_marker_export_sqlite_10(client, args, db_path, table_name):

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()
    try:
        cursor.execute('''DROP TABLE ''' + table_name + ''';''')
    except Exception as e:
        print('------->', e)
    cursor.execute('''
        CREATE TABLE ''' + table_name + ''' (
            id INTEGER NOT NULL PRIMARY KEY,
            name,
            code,
            description,
            notes TEXT,
            active,
            new_id INTEGER
            );
    ''')

    # client.context = {'active_test': False}
    clv_history_marker = client.model('clv.history_marker')
    history_marker_browse = clv_history_marker.browse(args)

    history_marker_count = 0
    for history_marker in history_marker_browse:
        history_marker_count += 1

        print(history_marker_count, history_marker.id, history_marker.code, history_marker.name.encode("utf-8"))

        code = None
        if history_marker.code:
            code = history_marker.code

        description = None
        if history_marker.description:
            description = history_marker.description

        notes = None
        if history_marker.notes:
            notes = history_marker.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           code,
                           description,
                           notes,
                           active
                           )
                       VALUES(?,?,?,?,?,?)''',
                       (history_marker.id,
                        history_marker.name,
                        code,
                        description,
                        notes,
                        history_marker.active,
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> history_marker_count: ', history_marker_count)


def clv_history_marker_import_sqlite_10(client, args, db_path, table_name):

    history_marker_model = client.model('clv.history_marker')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    job_history_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            name,
            code,
            description,
            notes,
            active,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        job_history_count += 1

        print(job_history_count, row['id'], row['name'])

        history_marker_browse = history_marker_model.browse([('name', '=', row['name']), ('active', '=', True)])
        if history_marker_browse.id != []:
            history_marker_id = history_marker_browse.id[0]

        history_marker_browse_2 = history_marker_model.browse([('name', '=', row['name']), ('active', '=', False)])
        if history_marker_browse_2.id != []:
            history_marker_browse = history_marker_browse_2
            history_marker_id = history_marker_browse_2.id[0]

        if history_marker_browse.id == []:

            values = {
                'name': row['name'],
                'code': row['code'],
                'description': row['description'],
                'notes': row['notes'],
            }
            history_marker_id = history_marker_model.create(values).id

        else:

            history_marker_id = history_marker_browse.id[0]

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (history_marker_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> job_history_count: ', job_history_count)
