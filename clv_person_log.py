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


def myo_person_log_export_sqlite(client, args, db_path, table_name):

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
            person_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    client.context = {'active_test': False}
    myo_person_log = client.model('myo.person.log')
    person_log_browse = myo_person_log.browse(args)

    person_log_count = 0
    for person_log in person_log_browse:
        person_log_count += 1

        print(
            person_log_count, person_log.id, person_log.values,
            person_log.date_log, person_log.notes
        )

        person_id = None
        if person_log.person_id:
            person_id = person_log.person_id.id

        user_id = None
        if person_log.user_id:
            user_id = person_log.user_id.id

        notes = None
        if person_log.notes:
            notes = person_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           person_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (person_log.id,
                        person_id,
                        user_id,
                        person_log.date_log,
                        person_log.values,
                        person_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> person_log_count: ', person_log_count)


def clv_person_log_export_sqlite_10(client, args, db_path, table_name):

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
            person_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    # client.context = {'active_test': False}
    person_log = client.model('clv.person.log')
    person_log_browse = person_log.browse(args)

    person_log_count = 0
    for person_log in person_log_browse:
        person_log_count += 1

        print(
            person_log_count, person_log.id, person_log.values,
            person_log.date_log, person_log.notes
        )

        person_id = None
        if person_log.person_id:
            person_id = person_log.person_id.id

        user_id = None
        if person_log.user_id:
            user_id = person_log.user_id.id

        notes = None
        if person_log.notes:
            notes = person_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           person_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (person_log.id,
                        person_id,
                        user_id,
                        person_log.date_log,
                        person_log.values,
                        person_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> person_log_count: ', person_log_count)


def clv_person_log_import_sqlite(client, args, db_path, table_name, person_table_name, res_users_table_name):

    person_log_model = client.model('clv.person.log')
    person_log_browse = person_log_model.browse([])
    person_log_browse.unlink()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            person_id,
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

    person_log_count = 0
    for row in cursor:
        person_log_count += 1

        print(
            person_log_count, row['id'], row['person_id'], row['user_id'], row['date_log'],
            row['values_'], row['action'], row['notes']
        )

        if row['person_id']:

            person_id = row['person_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + person_table_name + '''
                WHERE id = ?;''',
                (person_id,
                 )
            )
            person_id = cursor2.fetchone()[0]

        if row['user_id']:

            user_id = row['user_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + res_users_table_name + '''
                WHERE id = ?;''',
                (user_id,
                 )
            )
            user_id = cursor2.fetchone()[0]
            if user_id is None:
                user_id = 1

        values = {
            'person_id': person_id,
            'user_id': user_id,
            'date_log': row['date_log'],
            'values': row['values_'],
            'action': row['action'],
            'notes': row['notes'],
        }
        person_log_id = person_log_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (person_log_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> person_log_count: ', person_log_count)
