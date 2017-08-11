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
