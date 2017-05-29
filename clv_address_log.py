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


def myo_address_log_export_sqlite(client, args, db_path, table_name):

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
            address_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    client.context = {'active_test': False}
    myo_address_log = client.model('myo.address.log')
    address_log_browse = myo_address_log.browse(args)

    address_log_count = 0
    for address_log in address_log_browse:
        address_log_count += 1

        print(
            address_log_count, address_log.id, address_log.values,
            address_log.date_log, address_log.notes
        )

        address_id = None
        if address_log.address_id:
            address_id = address_log.address_id.id

        user_id = None
        if address_log.user_id:
            user_id = address_log.user_id.id

        notes = None
        if address_log.notes:
            notes = address_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           address_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (address_log.id,
                        address_id,
                        user_id,
                        address_log.date_log,
                        address_log.values,
                        address_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> address_log_count: ', address_log_count)


def clv_address_log_import_sqlite(client, args, db_path, table_name, address_table_name, res_users_table_name):

    address_log_model = client.model('clv.address.log')

    conn = sqlite3.connect(db_path)
    # conn.text_factory = str
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            address_id,
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

    address_log_count = 0
    for row in cursor:
        address_log_count += 1

        print(
            address_log_count, row['id'], row['address_id'], row['user_id'], row['date_log'],
            row['values_'], row['action'], row['notes']
        )

        if row['address_id']:

            address_id = row['address_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + address_table_name + '''
                WHERE id = ?;''',
                (address_id,
                 )
            )
            address_id = cursor2.fetchone()[0]
            print('>>>>>', row['address_id'], address_id)

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
            print('>>>>>', row['user_id'], user_id)

        values = {
            'address_id': address_id,
            'user_id': user_id,
            'date_log': row['date_log'],
            'values': row['values_'],
            'action': row['action'],
            'notes': row['notes'],
        }
        address_log_id = address_log_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (address_log_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> address_log_count: ', address_log_count)
