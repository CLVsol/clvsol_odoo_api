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


def myo_document_log_export_sqlite(client, args, db_path, table_name):

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
            document_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    client.context = {'active_test': False}
    myo_document_log = client.model('myo.document.log')
    document_log_browse = myo_document_log.browse(args)

    document_log_count = 0
    for document_log in document_log_browse:
        document_log_count += 1

        print(
            document_log_count, document_log.id, document_log.values,
            document_log.date_log, document_log.notes
        )

        document_id = None
        if document_log.document_id:
            document_id = document_log.document_id.id

        user_id = None
        if document_log.user_id:
            user_id = document_log.user_id.id

        notes = None
        if document_log.notes:
            notes = document_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           document_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (document_log.id,
                        document_id,
                        user_id,
                        document_log.date_log,
                        document_log.values,
                        document_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> document_log_count: ', document_log_count)


def clv_document_log_import_sqlite(client, args, db_path, table_name, document_table_name, res_users_table_name):

    document_log_model = client.model('clv.document.log')
    document_log_browse = document_log_model.browse([])
    document_log_browse.unlink()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            document_id,
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

    document_log_count = 0
    for row in cursor:
        document_log_count += 1

        print(
            document_log_count, row['id'], row['document_id'], row['user_id'], row['date_log'],
            row['values_'], row['action'], row['notes']
        )

        if row['document_id']:

            document_id = row['document_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + document_table_name + '''
                WHERE id = ?;''',
                (document_id,
                 )
            )
            document_id = cursor2.fetchone()[0]

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

        if document_id is not False:
            values = {
                'document_id': document_id,
                'user_id': user_id,
                'date_log': row['date_log'],
                'values': row['values_'],
                'action': row['action'],
                'notes': row['notes'],
            }
            document_log_id = document_log_model.create(values).id

            cursor2.execute(
                '''
                UPDATE ''' + table_name + '''
                SET new_id = ?
                WHERE id = ?;''',
                (document_log_id,
                 row['id']
                 )
            )

    conn.commit()
    conn.close()

    print()
    print('--> document_log_count: ', document_log_count)


def clv_document_log_export_sqlite_10(client, args, db_path, table_name):

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
            document_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    # client.context = {'active_test': False}
    myo_document_log = client.model('clv.document.log')
    document_log_browse = myo_document_log.browse(args)

    document_log_count = 0
    for document_log in document_log_browse:
        document_log_count += 1

        print(
            document_log_count, document_log.id, document_log.values,
            document_log.date_log, document_log.notes
        )

        document_id = None
        if document_log.document_id:
            document_id = document_log.document_id.id

        user_id = None
        if document_log.user_id:
            user_id = document_log.user_id.id

        notes = None
        if document_log.notes:
            notes = document_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           document_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (document_log.id,
                        document_id,
                        user_id,
                        document_log.date_log,
                        document_log.values,
                        document_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> document_log_count: ', document_log_count)
