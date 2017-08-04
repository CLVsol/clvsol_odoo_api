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


def hr_job_export_sqlite(client, args, db_path, table_name):

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
    job_model = client.model('hr.job')
    job_browse = job_model.browse(args)

    job_count = 0
    for job_reg in job_browse:
        job_count += 1

        print(job_count, job_reg.id, job_reg.name.encode("utf-8"))

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                active
                )
            VALUES(?,?,?)
            ''', (job_reg.id,
                  job_reg.name,
                  True,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> job_count: ', job_count)
    print()


def hr_job_export_sqlite_10(client, args, db_path, table_name):

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
    job_model = client.model('hr.job')
    job_browse = job_model.browse(args)

    job_count = 0
    for job_reg in job_browse:
        job_count += 1

        print(job_count, job_reg.id, job_reg.name.encode("utf-8"))

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                active
                )
            VALUES(?,?,?)
            ''', (job_reg.id,
                  job_reg.name,
                  True,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> job_count: ', job_count)
    print()


def hr_job_import_sqlite(client, args, db_path, table_name):

    hr_job_model = client.model('hr.job')

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

    hr_job_count = 0
    for row in cursor:
        hr_job_count += 1

        print(
            hr_job_count, row['id'], row['name'].encode('utf-8'), row['active'],
        )

        hr_job_browse = hr_job_model.browse([('name', '=', row['name']), ('active', '=', True)])
        if hr_job_browse.id != []:
            hr_job_id = hr_job_browse.id[0]

        hr_job_browse_2 = hr_job_model.browse([('name', '=', row['name']), ('active', '=', False)])
        if hr_job_browse_2.id != []:
            hr_job_browse = hr_job_browse_2
            hr_job_id = hr_job_browse_2.id[0]

        if hr_job_browse.id == []:

            values = {
                'name': row['name'],
                'active': row['active'],
            }
            hr_job_id = hr_job_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (hr_job_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> hr_job_count: ', hr_job_count)
