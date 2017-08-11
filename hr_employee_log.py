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


def hr_employee_log_export_sqlite_10(client, args, db_path, table_name):

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
            employee_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    # client.context = {'active_test': False}
    hr_employee_log = client.model('hr.employee.log')
    hr_employee_log_browse = hr_employee_log.browse(args)

    hr_employee_log_count = 0
    for hr_employee_log in hr_employee_log_browse:
        hr_employee_log_count += 1

        print(
            hr_employee_log_count, hr_employee_log.id, hr_employee_log.values,
            hr_employee_log.date_log, hr_employee_log.notes
        )

        employee_id = None
        if hr_employee_log.employee_id:
            employee_id = hr_employee_log.employee_id.id

        user_id = None
        if hr_employee_log.user_id:
            user_id = hr_employee_log.user_id.id

        notes = None
        if hr_employee_log.notes:
            notes = hr_employee_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           employee_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (hr_employee_log.id,
                        employee_id,
                        user_id,
                        hr_employee_log.date_log,
                        hr_employee_log.values,
                        hr_employee_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> hr_employee_log_count: ', hr_employee_log_count)


def hr_employee_log_import_sqlite_10(client, args, db_path, table_name, hr_employee_table_name, res_users_table_name):

    hr_employee_log_model = client.model('hr.employee.log')
    hr_employee_log_browse = hr_employee_log_model.browse([])
    hr_employee_log_browse.unlink()

    hr_employee_model = client.model('hr.employee')
    res_users_model = client.model('res.users')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            employee_id,
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

    hr_employee_log_count = 0
    for row in cursor:
        hr_employee_log_count += 1

        print(
            hr_employee_log_count, row['id'], row['employee_id'], row['user_id'], row['date_log'],
            row['values_'], row['action'], row['notes']
        )

        employee_id = False
        if row['employee_id']:
            cursor2.execute(
                '''
                SELECT code
                FROM ''' + hr_employee_table_name + '''
                WHERE id = ?;''',
                (row['employee_id'],
                 )
            )
            employee_code = cursor2.fetchone()[0]
            hr_employee_browse = hr_employee_model.browse([('code', '=', employee_code), ])
            employee_id = hr_employee_browse.id[0]

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
            'employee_id': employee_id,
            'user_id': user_id,
            'date_log': row['date_log'],
            'values': row['values_'],
            'action': row['action'],
            'notes': row['notes'],
        }
        hr_employee_log_id = hr_employee_log_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (hr_employee_log_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> hr_employee_log_count: ', hr_employee_log_count)
