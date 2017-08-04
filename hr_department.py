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


def hr_department_create(client, department_name):

    hr_department_model = client.model('hr.department')

    hr_department_browse = hr_department_model.browse([('name', '=', department_name), ])
    if hr_department_browse.id == []:

        values = {
            'name': department_name,
        }
        hr_department_model.create(values)


def hr_department_export_sqlite(client, args, db_path, table_name):

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()
    try:
        cursor.execute('''DROP TABLE ''' + table_name + ''';''')
    except Exception as e:
        print('------->', e)
    cursor.execute(
        '''
        CREATE TABLE ''' + table_name + ''' (
            id INTEGER NOT NULL PRIMARY KEY,
            name,
            active,
            new_id INTEGER
            );
        '''
    )

    client.context = {'active_test': False}
    department_model = client.model('hr.department')
    department_browse = department_model.browse(args)

    department_count = 0
    for department_reg in department_browse:
        department_count += 1

        print(department_count, department_reg.id, department_reg.name.encode("utf-8"))

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                active
                )
            VALUES(?,?,?)
            ''', (department_reg.id,
                  department_reg.name,
                  True,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> department_count: ', department_count)
    print()


def hr_department_export_sqlite_10(client, args, db_path, table_name):

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()
    try:
        cursor.execute('''DROP TABLE ''' + table_name + ''';''')
    except Exception as e:
        print('------->', e)
    cursor.execute(
        '''
        CREATE TABLE ''' + table_name + ''' (
            id INTEGER NOT NULL PRIMARY KEY,
            name,
            active,
            new_id INTEGER
            );
        '''
    )

    # client.context = {'active_test': False}
    department_model = client.model('hr.department')
    department_browse = department_model.browse(args)

    department_count = 0
    for department_reg in department_browse:
        department_count += 1

        print(department_count, department_reg.id, department_reg.name.encode("utf-8"))

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                active
                )
            VALUES(?,?,?)
            ''', (department_reg.id,
                  department_reg.name,
                  True,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> department_count: ', department_count)
    print()


def hr_department_import_sqlite(client, args, db_path, table_name):

    hr_department_model = client.model('hr.department')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            name,
            active,
            new_id
        FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])

    hr_department_count = 0
    for row in cursor:
        hr_department_count += 1

        print(
            hr_department_count, row['id'], row['name'], row['active'],
        )

        hr_department_browse = hr_department_model.browse([('name', '=', row['name']), ('active', '=', True)])
        if hr_department_browse.id != []:
            hr_department_id = hr_department_browse.id[0]

        hr_department_browse_2 = hr_department_model.browse([('name', '=', row['name']), ('active', '=', False)])
        if hr_department_browse_2.id != []:
            hr_department_browse = hr_department_browse_2
            hr_department_id = hr_department_browse_2.id[0]

        if hr_department_browse.id == []:

            values = {
                'name': row['name'],
                'active': row['active'],
            }
            hr_department_id = hr_department_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (hr_department_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> hr_department_count: ', hr_department_count)
