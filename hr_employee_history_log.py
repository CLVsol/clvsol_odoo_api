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


def hr_employee_history_log_export_sqlite_10(client, args, db_path, table_name):

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
            employee_history_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    # client.context = {'active_test': False}
    employee_history_log = client.model('hr.employee.history.log')
    employee_history_log_browse = employee_history_log.browse(args)

    employee_history_log_count = 0
    for employee_history_log in employee_history_log_browse:
        employee_history_log_count += 1

        print(
            employee_history_log_count, employee_history_log.id, employee_history_log.values,
            employee_history_log.date_log, employee_history_log.notes
        )

        employee_history_id = None
        if employee_history_log.employee_history_id:
            employee_history_id = employee_history_log.employee_history_id.id

        user_id = None
        if employee_history_log.user_id:
            user_id = employee_history_log.user_id.id

        notes = None
        if employee_history_log.notes:
            notes = employee_history_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           employee_history_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (employee_history_log.id,
                        employee_history_id,
                        user_id,
                        employee_history_log.date_log,
                        employee_history_log.values,
                        employee_history_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> employee_history_log_count: ', employee_history_log_count)


def hr_employee_history_log_import_sqlite_10(
    client, args, db_path, table_name, hr_employee_table_name, res_users_table_name
):

    employee_history_log_model = client.model('hr.employee.history.log')
    employee_history_log_browse = employee_history_log_model.browse([])
    employee_history_log_browse.unlink()

    address_model = client.model('clv.address')
    res_users_model = client.model('res.users')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            employee_history_id,
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

    employee_history_log_count = 0
    for row in cursor:
        employee_history_log_count += 1

        print(
            employee_history_log_count, row['id'], row['employee_history_id'], row['user_id'], row['date_log'],
            row['values_'], row['action'], row['notes']
        )

        employee_history_id = False
        if row['employee_history_id']:
            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + hr_employee_table_name + '''
                WHERE id = ?;''',
                (row['employee_history_id'],
                 )
            )
            employee_history_id = cursor2.fetchone()[0]

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
            'employee_history_id': employee_history_id,
            'user_id': user_id,
            'date_log': row['date_log'],
            'values': row['values_'],
            'action': row['action'],
            'notes': row['notes'],
        }
        employee_history_log_id = employee_history_log_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (employee_history_log_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> employee_history_log_count: ', employee_history_log_count)
