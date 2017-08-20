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
import re


def clv_person_history_export_sqlite_10(client, args, db_path, table_name):

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
            person_id,
            category_ids,
            sign_in_date,
            sign_out_date,
            reg_state,
            state,
            employee_id,
            address_id,
            person_address_role_id,
            date_reference,
            age_reference,
            estimated_age,
            responsible_id,
            caregiver_id,
            history_marker_id,
            active,
            new_id INTEGER
            );
        '''
    )

    # client.context = {'active_test': False}
    person_history_model = client.model('clv.person.history')
    person_history_browse = person_history_model.browse(args)

    person_history_count = 0
    for person_history_reg in person_history_browse:
        person_history_count += 1

        print(person_history_count, person_history_reg.id, person_history_reg.person_id.name.encode("utf-8"))

        person_id = None
        if person_history_reg.person_id:
            person_id = person_history_reg.person_id.id

        sign_in_date = None
        if person_history_reg.sign_in_date:
            sign_in_date = person_history_reg.sign_in_date

        sign_out_date = None
        if person_history_reg.sign_out_date:
            sign_out_date = person_history_reg.sign_out_date

        employee_id = None
        if person_history_reg.employee_id:
            employee_id = person_history_reg.employee_id.id

        address_id = None
        if person_history_reg.address_id:
            address_id = person_history_reg.address_id.id

        person_address_role_id = None
        if person_history_reg.person_address_role_id:
            person_address_role_id = person_history_reg.person_address_role_id.id

        date_reference = None
        if person_history_reg.date_reference:
            date_reference = person_history_reg.date_reference

        age_reference = None
        if person_history_reg.age_reference:
            age_reference = person_history_reg.age_reference

        estimated_age = None
        if person_history_reg.estimated_age:
            estimated_age = person_history_reg.estimated_age

        responsible_id = None
        if person_history_reg.responsible_id:
            responsible_id = person_history_reg.responsible_id.id

        caregiver_id = None
        if person_history_reg.caregiver_id:
            caregiver_id = person_history_reg.caregiver_id.id

        history_marker_id = None
        if person_history_reg.history_marker_id:
            history_marker_id = person_history_reg.history_marker_id.id

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                person_id,
                category_ids,
                sign_in_date,
                sign_out_date,
                reg_state,
                state,
                employee_id,
                address_id,
                person_address_role_id,
                date_reference,
                age_reference,
                estimated_age,
                responsible_id,
                caregiver_id,
                history_marker_id,
                active
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (person_history_reg.id,
                  person_id,
                  str(person_history_reg.category_ids.id),
                  sign_in_date,
                  sign_out_date,
                  person_history_reg.reg_state,
                  person_history_reg.state,
                  employee_id,
                  address_id,
                  person_address_role_id,
                  date_reference,
                  age_reference,
                  estimated_age,
                  responsible_id,
                  caregiver_id,
                  history_marker_id,
                  person_history_reg.active,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> person_history_count: ', person_history_count)


def clv_person_history_import_sqlite_10(
    client, args, db_path, table_name,
    person_table_name, category_table_name, hr_employee_table_name, history_marker_table_name,
    address_table_name, person_address_role_table_name
):

    person_history_model = client.model('clv.person.history')

    person_model = client.model('clv.person')
    category_model = client.model('clv.person.category')
    hr_employee_model = client.model('hr.employee')
    address_model = client.model('clv.address')
    person_address_role_model = client.model('clv.person.address.role')
    history_marker_model = client.model('clv.history_marker')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor2 = conn.cursor()

    person_history_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            person_id,
            category_ids,
            sign_in_date,
            sign_out_date,
            reg_state,
            state,
            employee_id,
            address_id,
            person_address_role_id,
            date_reference,
            age_reference,
            estimated_age,
            responsible_id,
            caregiver_id,
            history_marker_id,
            active,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        person_history_count += 1

        print(person_history_count, row['id'], row['person_id'], row['sign_in_date'], row['history_marker_id'])

        person_id = False
        cursor2.execute(
            '''
            SELECT code
            FROM ''' + person_table_name + '''
            WHERE id = ?;''',
            (row['person_id'],
             )
        )
        person_code = cursor2.fetchone()
        print('>>>>>>>>>>', row['person_id'], person_code)
        if person_code is not None:
            person_code = person_code[0]
            clv_person_browse = person_model.browse([('code', '=', person_code), ])
            person_id = clv_person_browse.id[0]

        new_category_ids = False
        if row['category_ids'] != '[]':

            category_ids = row['category_ids'].split(',')
            new_category_ids = []
            for x in range(0, len(category_ids)):
                category_id = int(re.sub('[^0-9]', '', category_ids[x]))
                cursor2.execute(
                    '''
                    SELECT name
                    FROM ''' + category_table_name + '''
                    WHERE id = ?;''',
                    (category_id,
                     )
                )
                category_name = cursor2.fetchone()
                if category_name is not None:
                    category_name = category_name[0]
                    category_browse = category_model.browse([('name', '=', category_name), ])
                    new_category_id = category_browse.id[0]

                new_category_ids.append((4, new_category_id))

        employee_id = False
        cursor2.execute(
            '''
            SELECT code
            FROM ''' + hr_employee_table_name + '''
            WHERE id = ?;''',
            (row['employee_id'],
             )
        )
        employee_code = cursor2.fetchone()
        if employee_code is not None:
            employee_code = employee_code[0]
            hr_employee_browse = hr_employee_model.browse([('code', '=', employee_code), ])
            employee_id = hr_employee_browse.id[0]

        reg_state = row['reg_state']
        if reg_state is None:
            reg_state = 'draft'

        state = row['state']
        if state is None:
            state = 'new'

        address_id = False
        cursor2.execute(
            '''
            SELECT code
            FROM ''' + address_table_name + '''
            WHERE id = ?;''',
            (row['address_id'],
             )
        )
        address_code = cursor2.fetchone()
        print('>>>>>>>>>>', row['address_id'], address_code)
        if address_code is not None:
            address_code = address_code[0]
            clv_address_browse = address_model.browse([('code', '=', address_code), ])
            address_id = clv_address_browse.id[0]

        person_address_role_id = False
        cursor2.execute(
            '''
            SELECT code
            FROM ''' + person_address_role_table_name + '''
            WHERE id = ?;''',
            (row['person_address_role_id'],
             )
        )
        person_address_role_code = cursor2.fetchone()
        print('>>>>>>>>>>', row['person_address_role_id'], person_address_role_code)
        if person_address_role_code is not None:
            person_address_role_code = person_address_role_code[0]
            clv_person_address_role_browse = \
                person_address_role_model.browse([('code', '=', person_address_role_code), ])
            person_address_role_id = clv_person_address_role_browse.id[0]

        responsible_id = False
        cursor2.execute(
            '''
            SELECT code
            FROM ''' + person_table_name + '''
            WHERE id = ?;''',
            (row['responsible_id'],
             )
        )
        person_code = cursor2.fetchone()
        print('>>>>>>>>>>', row['responsible_id'], person_code)
        if person_code is not None:
            person_code = person_code[0]
            clv_person_browse = person_model.browse([('code', '=', person_code), ])
            responsible_id = clv_person_browse.id[0]

        caregiver_id = False
        cursor2.execute(
            '''
            SELECT code
            FROM ''' + person_table_name + '''
            WHERE id = ?;''',
            (row['caregiver_id'],
             )
        )
        person_code = cursor2.fetchone()
        print('>>>>>>>>>>', row['caregiver_id'], person_code)
        if person_code is not None:
            person_code = person_code[0]
            clv_person_browse = person_model.browse([('code', '=', person_code), ])
            caregiver_id = clv_person_browse.id[0]

        new_history_marker_id = False
        if row['history_marker_id']:
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

        person_history_browse = person_history_model.browse([
            ('person_id', '=', person_id),
            ('sign_in_date', '=', row['sign_in_date']),
            ('history_marker_id', '=', new_history_marker_id),
            ('active', '=', True),
        ])
        if person_history_browse.id != []:
            person_id = person_history_browse.id[0]

        person_history_browse_2 = person_history_model.browse([
            ('person_id', '=', person_id),
            ('sign_in_date', '=', row['sign_in_date']),
            ('history_marker_id', '=', new_history_marker_id),
            ('active', '=', False),
        ])
        if person_history_browse_2.id != []:
            person_history_browse = person_history_browse_2
            person_id = person_history_browse_2.id[0]

        if person_history_browse.id == []:

            values = {
                'person_id': person_id,
                'category_ids': category_ids,
                'sign_in_date': row['sign_in_date'],
                'sign_out_date': row['sign_out_date'],
                'reg_state': reg_state,
                'state': state,
                'employee_id': employee_id,
                'address_id': address_id,
                'person_address_role_id': person_address_role_id,
                'date_reference': row['date_reference'],
                'age_reference': row['age_reference'],
                'estimated_age': row['estimated_age'],
                'responsible_id': responsible_id,
                'caregiver_id': caregiver_id,
                'history_marker_id': new_history_marker_id,
                'active': row['active'],
            }
            person_history = person_history_model.create(values)
            person_history_id = person_history.id

        else:

            person_history_id = person_history_browse.id[0]

            values = {
                'category_ids': [(5,), ],
            }
            person_history_model.write(person_history_id, values)

            values = {
                # 'person_id': person_id,
                'category_ids': category_ids,
                # 'sign_in_date': row['sign_in_date'],
                'sign_out_date': row['sign_out_date'],
                'reg_state': reg_state,
                'state': state,
                'employee_id': employee_id,
                'address_id': address_id,
                'person_address_role_id': person_address_role_id,
                'date_reference': row['date_reference'],
                'age_reference': row['age_reference'],
                'estimated_age': row['estimated_age'],
                'responsible_id': responsible_id,
                'caregiver_id': caregiver_id,
                # 'history_marker_id': new_history_marker_id,
                'active': row['active'],
            }
            person_history_model.write(person_history_id, values)

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (person_history_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> person_history_count: ', person_history_count)
