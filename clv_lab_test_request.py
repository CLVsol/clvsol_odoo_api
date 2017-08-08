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

from clv_history_marker import *


def myo_lab_test_request_export_sqlite(client, args, db_path, table_name):

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
            lab_test_type_id,
            date_requested,
            patient_id,
            survey_user_input_id,
            person_user_id,
            employee_id,
            date_received,
            state,
            active,
            new_id INTEGER
            );
        '''
    )

    client.context = {'active_test': False}
    lab_test_request_model = client.model('myo.lab_test.request')
    lab_test_request_browse = lab_test_request_model.browse(args)

    lab_test_request_count = 0
    for lab_test_request_reg in lab_test_request_browse:
        lab_test_request_count += 1

        print(lab_test_request_count, lab_test_request_reg.id, lab_test_request_reg.name.encode("utf-8"))

        lab_test_type_id = None
        if lab_test_request_reg.lab_test_type_id:
            lab_test_type_id = lab_test_request_reg.lab_test_type_id.id

        date_requested = None
        if lab_test_request_reg.date_requested:
            date_requested = lab_test_request_reg.date_requested

        patient_id = None
        if lab_test_request_reg.patient_id:
            patient_id = lab_test_request_reg.patient_id.id

        survey_user_input_id = None
        if lab_test_request_reg.survey_user_input_id:
            survey_user_input_id = lab_test_request_reg.survey_user_input_id.id

        person_user_id = None
        if lab_test_request_reg.person_user_id:
            person_user_id = lab_test_request_reg.person_user_id

        employee_id = None
        if lab_test_request_reg.employee_id:
            employee_id = lab_test_request_reg.employee_id

        date_received = None
        if lab_test_request_reg.date_received:
            date_received = lab_test_request_reg.date_received

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                lab_test_type_id,
                date_requested,
                patient_id,
                survey_user_input_id,
                person_user_id,
                employee_id,
                date_received,
                state,
                active
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
            ''', (lab_test_request_reg.id,
                  lab_test_request_reg.name,
                  lab_test_type_id,
                  date_requested,
                  patient_id,
                  survey_user_input_id,
                  person_user_id,
                  employee_id,
                  date_received,
                  lab_test_request_reg.state,
                  lab_test_request_reg.active,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> lab_test_request_count: ', lab_test_request_count)


def clv_lab_test_request_import_sqlite(
        client, lab_test_request_args, db_path, table_name, lab_test_type_table_name,
        person_table_name, res_users_table_name, history_marker_name
):

    history_marker_id = clv_history_marker_get_id(client, history_marker_name)

    lab_test_request_model = client.model('clv.lab_test.request')
    lab_test_type_model = client.model('clv.lab_test.type')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    lab_test_request_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            name,
            lab_test_type_id,
            date_requested,
            patient_id,
            survey_user_input_id,
            person_user_id,
            employee_id,
            date_received,
            state,
            active,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        lab_test_request_count += 1

        print(lab_test_request_count, row['id'], row['name'])

        person_id = False
        if row['patient_id']:

            person_id = row['patient_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + person_table_name + '''
                WHERE id = ?;''',
                (person_id,
                 )
            )
            person_id = cursor2.fetchone()[0]

        lab_test_type_id = False
        lab_test_type_ids = []
        if row['lab_test_type_id']:

            lab_test_type_id = row['lab_test_type_id']

            cursor2.execute(
                '''
                SELECT code
                FROM ''' + lab_test_type_table_name + '''
                WHERE id = ?;''',
                (lab_test_type_id,
                 )
            )
            lab_test_type_code = cursor2.fetchone()[0]

            new_test_type_id = lab_test_type_model.search([
                ('code', '=', lab_test_type_code),
            ])[0]
            lab_test_type_ids.append((4, new_test_type_id))

        previous_state = row['state']
        if previous_state == 'draft':
            state = 'draft'
        if previous_state == 'tested':
            state = 'tested'
        if previous_state == 'canceled':
            state = 'cancelled'

        values = {
            'code': row['name'],
            'person_id': person_id,
            'date_requested': row['date_requested'],
            'lab_test_type_ids': lab_test_type_ids,
            'state': state,
            'active': row['active'],
            'active_log': True,
            'history_marker_id': history_marker_id,
        }
        lab_test_request_id = lab_test_request_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (lab_test_request_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> lab_test_request_count: ', lab_test_request_count)
