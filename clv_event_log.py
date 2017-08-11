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


def clv_event_log_export_sqlite_10(client, args, db_path, table_name):

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
            event_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    # client.context = {'active_test': False}
    event_log = client.model('clv.event.log')
    event_log_browse = event_log.browse(args)

    event_log_count = 0
    for event_log in event_log_browse:
        event_log_count += 1

        print(
            event_log_count, event_log.id, event_log.values,
            event_log.date_log, event_log.notes
        )

        event_id = None
        if event_log.event_id:
            event_id = event_log.event_id.id

        user_id = None
        if event_log.user_id:
            user_id = event_log.user_id.id

        notes = None
        if event_log.notes:
            notes = event_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           event_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (event_log.id,
                        event_id,
                        user_id,
                        event_log.date_log,
                        event_log.values,
                        event_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> event_log_count: ', event_log_count)


def clv_event_log_import_sqlite_10(client, args, db_path, table_name, event_table_name, res_users_table_name):

    event_log_model = client.model('clv.event.log')
    event_log_browse = event_log_model.browse([])
    event_log_browse.unlink()

    event_model = client.model('clv.event')
    res_users_model = client.model('res.users')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            event_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id
        FROM ''' + table_name + '''
        ORDER BY id;
    ''')

    print(data)
    print([field[0] for field in cursor.description])

    event_log_count = 0
    for row in cursor:
        event_log_count += 1

        print(
            event_log_count, row['id'], row['event_id'], row['user_id'], row['date_log'],
            row['values_'], row['action'], row['notes']
        )

        event_id = False
        if row['event_id']:
            cursor2.execute(
                '''
                SELECT code
                FROM ''' + event_table_name + '''
                WHERE id = ?;''',
                (row['event_id'],
                 )
            )
            event_code = cursor2.fetchone()[0]
            event_browse = event_model.browse([('code', '=', event_code), ])
            event_id = event_browse.id[0]

        # if row['event_id']:

        #     event_id = row['event_id']

        #     cursor2.execute(
        #         '''
        #         SELECT new_id
        #         FROM ''' + event_table_name + '''
        #         WHERE id = ?;''',
        #         (event_id,
        #          )
        #     )
        #     event_id = cursor2.fetchone()[0]

        user_id = False
        if row['user_id']:
            cursor2.execute(
                '''
                SELECT login
                FROM ''' + res_users_table_name + '''
                WHERE id = ?;''',
                (row['user_id'],
                 )
            )
            user_login = cursor2.fetchone()[0]
            res_users_browse = res_users_model.browse([('login', '=', user_login), ])
            user_id = res_users_browse.id[0]

        # if row['user_id']:

        #     user_id = row['user_id']

        #     cursor2.execute(
        #         '''
        #         SELECT new_id
        #         FROM ''' + res_users_table_name + '''
        #         WHERE id = ?;''',
        #         (user_id,
        #          )
        #     )
        #     user_id = cursor2.fetchone()[0]
        #     if user_id is None:
        #         user_id = 1

        values = {
            'event_id': event_id,
            'user_id': user_id,
            'date_log': row['date_log'],
            'values': row['values_'],
            'action': row['action'],
            'notes': row['notes'],
        }
        event_log_id = event_log_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (event_log_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> event_log_count: ', event_log_count)
