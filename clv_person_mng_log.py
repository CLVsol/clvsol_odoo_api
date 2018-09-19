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


def clv_person_mng_log_export_sqlite_10(client, args, db_path, table_name):

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
            person_mng_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    # client.context = {'active_test': False}
    person_mng_log = client.model('clv.person.mng.log')
    person_mng_log_browse = person_mng_log.browse(args)

    person_mng_log_count = 0
    for person_mng_log in person_mng_log_browse:
        person_mng_log_count += 1

        print(
            person_mng_log_count, person_mng_log.id, person_mng_log.values,
            person_mng_log.date_log, person_mng_log.notes
        )

        person_mng_id = None
        if person_mng_log.person_mng_id:
            person_mng_id = person_mng_log.person_mng_id.id

        user_id = None
        if person_mng_log.user_id:
            user_id = person_mng_log.user_id.id

        notes = None
        if person_mng_log.notes:
            notes = person_mng_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           person_mng_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (person_mng_log.id,
                        person_mng_id,
                        user_id,
                        person_mng_log.date_log,
                        person_mng_log.values,
                        person_mng_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> person_mng_log_count: ', person_mng_log_count)


def clv_person_mng_log_import_sqlite_10(
    client, args, db_path, table_name, person_mng_table_name, res_users_table_name
):

    person_mng_log_model = client.model('clv.person.mng.log')
    person_mng_log_browse = person_mng_log_model.browse([])
    person_mng_log_browse.unlink()

    person_mng_model = client.model('clv.person.mng')
    res_users_model = client.model('res.users')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            person_mng_id,
            user_id,
            date_log,
            "values",
            action,
            notes,
            new_id
        FROM ''' + table_name + '''
        ORDER BY id;
    ''')

    print(data)
    print([field[0] for field in cursor.description])

    person_mng_log_count = 0
    for row in cursor:
        person_mng_log_count += 1

        print(
            person_mng_log_count, row['id'], row['person_mng_id'], row['user_id'], row['date_log'],
            row['values'], row['action'], row['notes']
        )

        person_mng_id = False
        if row['person_mng_id']:
            cursor2.execute(
                '''
                SELECT name
                FROM ''' + person_mng_table_name + '''
                WHERE id = ?;''',
                (row['person_mng_id'],
                 )
            )
            person_mng_name = cursor2.fetchone()[0]
            person_mng_browse = person_mng_model.browse([('name', '=', person_mng_name), ])
            person_mng_id = person_mng_browse.id[0]

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

        values = {
            'person_mng_id': person_mng_id,
            'user_id': user_id,
            'date_log': row['date_log'],
            'values': row['values'],
            'action': row['action'],
            'notes': row['notes'],
        }
        person_mng_log_id = person_mng_log_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (person_mng_log_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> person_mng_log_count: ', person_mng_log_count)
