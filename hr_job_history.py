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


def hr_job_history_export_sqlite_10(client, args, db_path, table_name):

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
            employee_id,
            job_id,
            sign_in_date,
            sign_out_date,
            history_marker_id,
            notes,
            active,
            new_id INTEGER
            );
        '''
    )

    # client.context = {'active_test': False}
    job_history_model = client.model('hr.job.history')
    job_history_browse = job_history_model.browse(args)

    job_history_count = 0
    for job_history_reg in job_history_browse:
        job_history_count += 1

        print(job_history_count, job_history_reg.id, job_history_reg.job_id.name.encode("utf-8"))

        employee_id = None
        if job_history_reg.employee_id:
            employee_id = job_history_reg.employee_id.id

        job_id = None
        if job_history_reg.job_id:
            job_id = job_history_reg.job_id.id

        sign_in_date = None
        if job_history_reg.sign_in_date:
            sign_in_date = job_history_reg.sign_in_date

        sign_out_date = None
        if job_history_reg.sign_out_date:
            sign_out_date = job_history_reg.sign_out_date

        history_marker_id = None
        if job_history_reg.history_marker_id:
            history_marker_id = job_history_reg.history_marker_id.id

        notes = None
        if job_history_reg.notes:
            notes = job_history_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                employee_id,
                job_id,
                sign_in_date,
                sign_out_date,
                history_marker_id,
                notes,
                active
                )
            VALUES(?,?,?,?,?,?,?,?)
            ''', (job_history_reg.id,
                  employee_id,
                  job_id,
                  sign_in_date,
                  sign_out_date,
                  history_marker_id,
                  notes,
                  job_history_reg.active,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> job_history_count: ', job_history_count)


def hr_job_history_import_sqlite_10(
    client, args, db_path, table_name,
    hr_employee_table_name, hr_job_table_name, history_marker_table_name
):

    job_history_model = client.model('hr.job.history')

    history_marker_model = client.model('clv.history_marker')
    hr_employee_model = client.model('hr.employee')
    hr_job_model = client.model('hr.job')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    job_history_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            employee_id,
            job_id,
            sign_in_date,
            sign_out_date,
            history_marker_id,
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

        print(job_history_count, row['id'], row['job_id'])

        new_history_marker_id = False
        cursor2.execute(
            '''
            SELECT name
            FROM ''' + history_marker_table_name + '''
            WHERE id = ?;''',
            (row['history_marker_id'],
             )
        )
        history_marker_name = cursor2.fetchone()[0]
        history_marker_browse = history_marker_model.browse([('name', '=', history_marker_name), ])
        new_history_marker_id = history_marker_browse.id[0]

        employee_id = False
        cursor2.execute(
            '''
            SELECT name
            FROM ''' + hr_employee_table_name + '''
            WHERE id = ?;''',
            (row['employee_id'],
             )
        )
        employee_name = cursor2.fetchone()
        if employee_name is not None:
            employee_name = employee_name[0]
            hr_employee_browse = hr_employee_model.browse([('name', '=', employee_name), ])
            employee_id = hr_employee_browse.id[0]

        job_id = False
        cursor2.execute(
            '''
            SELECT name
            FROM ''' + hr_job_table_name + '''
            WHERE id = ?;''',
            (row['job_id'],
             )
        )
        job_name = cursor2.fetchone()
        if job_name is not None:
            job_name = job_name[0]
            hr_job_browse = hr_job_model.browse([('name', '=', job_name), ])
            job_id = hr_job_browse.id[0]

        values = {
            'employee_id': employee_id,
            'job_id': job_id,
            'sign_in_date': row['sign_in_date'],
            'sign_out_date': row['sign_out_date'],
            'history_marker_id': new_history_marker_id,
            'notes': row['notes'],
            'active': row['active'],
        }
        job_history_id = job_history_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (job_history_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> job_history_count: ', job_history_count)
