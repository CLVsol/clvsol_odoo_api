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

from clv_history_marker import *


def myo_lab_test_result_export_sqlite(client, args, db_path, table_name):

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
            date_analisis,
            patient_id,
            survey_user_input_id,
            base_document_id,
            base_survey_user_input_id,
            professional_id,
            person_user_id,
            criterion_ids,
            results,
            diagnosis,
            state,
            active,
            active_log,
            new_id INTEGER
            );
        '''
    )

    client.context = {'active_test': False}
    lab_test_result_model = client.model('myo.lab_test.result')
    lab_test_result_browse = lab_test_result_model.browse(args)

    lab_test_result_count = 0
    for lab_test_result_reg in lab_test_result_browse:
        lab_test_result_count += 1

        print(lab_test_result_count, lab_test_result_reg.id, lab_test_result_reg.name.encode("utf-8"))

        lab_test_type_id = None
        if lab_test_result_reg.lab_test_type_id:
            lab_test_type_id = lab_test_result_reg.lab_test_type_id.id

        date_analisis = None
        # if lab_test_result_reg.date_analisis:
        #     date_analisis = lab_test_result_reg.date_analisis

        patient_id = None
        if lab_test_result_reg.patient_id:
            patient_id = lab_test_result_reg.patient_id.id

        survey_user_input_id = None
        if lab_test_result_reg.survey_user_input_id:
            survey_user_input_id = lab_test_result_reg.survey_user_input_id.id

        base_document_id = None
        if lab_test_result_reg.base_document_id:
            base_document_id = lab_test_result_reg.base_document_id.id

        base_survey_user_input_id = None
        if lab_test_result_reg.base_survey_user_input_id:
            base_survey_user_input_id = lab_test_result_reg.base_survey_user_input_id.id

        professional_id = None
        if lab_test_result_reg.professional_id:
            professional_id = lab_test_result_reg.professional_id.id

        person_user_id = None
        if lab_test_result_reg.person_user_id:
            person_user_id = lab_test_result_reg.person_user_id

        results = None
        if lab_test_result_reg.results:
            results = lab_test_result_reg.results

        diagnosis = None
        if lab_test_result_reg.diagnosis:
            diagnosis = lab_test_result_reg.diagnosis

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                lab_test_type_id,
                date_analisis,
                patient_id,
                survey_user_input_id,
                base_document_id,
                base_survey_user_input_id,
                professional_id,
                person_user_id,
                criterion_ids,
                results,
                diagnosis,
                state,
                active,
                active_log
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (lab_test_result_reg.id,
                  lab_test_result_reg.name,
                  lab_test_type_id,
                  date_analisis,
                  patient_id,
                  survey_user_input_id,
                  base_document_id,
                  base_survey_user_input_id,
                  professional_id,
                  person_user_id,
                  str(lab_test_result_reg.criterion_ids.id),
                  results,
                  diagnosis,
                  lab_test_result_reg.state,
                  lab_test_result_reg.active,
                  lab_test_result_reg.active_log,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> lab_test_result_count: ', lab_test_result_count)


def clv_lab_test_result_import_sqlite(
        client, lab_test_result_args, db_path, table_name, lab_test_type_table_name,
        person_table_name, res_users_table_name, history_marker_name,
        lab_test_criterion_table_name, lab_test_unit_table_name
):

    # history_marker_id = clv_history_marker_get_id(client, history_marker_name)

    lab_test_result_model = client.model('clv.lab_test.result')
    lab_test_request_model = client.model('clv.lab_test.request')
    lab_test_type_model = client.model('clv.lab_test.type')
    lab_test_criterion_model = client.model('clv.lab_test.criterion')
    lab_test_unit_model = client.model('clv.lab_test.unit')
    patient_model = client.model('clv.person')
    # hr_employee_model = client.model('hr.employee')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()

    lab_test_result_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            name,
            lab_test_type_id,
            date_analisis,
            patient_id,
            survey_user_input_id,
            base_document_id,
            base_survey_user_input_id,
            professional_id,
            person_user_id,
            criterion_ids,
            results,
            diagnosis,
            state,
            active,
            active_log,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        lab_test_result_count += 1

        print(lab_test_result_count, row['id'], row['name'])

        new_patient_id = False
        if row['patient_id']:

            patient_id = row['patient_id']

            cursor2.execute(
                '''
                SELECT code
                FROM ''' + person_table_name + '''
                WHERE id = ?;''',
                (patient_id,
                 )
            )
            patient_code = cursor2.fetchone()[0]

            new_patient_id = patient_model.search([
                ('code', '=', patient_code),
            ])[0]

        new_test_type_id = False
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

        new_lab_test_request_id = False
        lab_test_request_code = row['name']
        new_lab_test_request_id = lab_test_request_model.search([
            ('code', '=', lab_test_request_code),
        ])[0]

        previous_state = row['state']
        if previous_state == 'draft':
            reg_state = 'draft'
            state = 'new'
        if previous_state == 'transcribed':
            reg_state = 'done'
            state = 'available'

        new_criterion_ids = False
        if row['criterion_ids'] != '[]':

            criterion_ids = row['criterion_ids'].split(',')
            new_criterion_ids = []
            for x in range(0, len(criterion_ids)):
                criterion_id = int(re.sub('[^0-9]', '', criterion_ids[x]))

                cursor3.execute(
                    '''
                    SELECT
                        id,
                        code,
                        name,
                        result,
                        unit_id,
                        normal_range,
                        lab_test_type_id,
                        lab_test_result_id,
                        sequence,
                        active,
                        new_id
                    FROM ''' + lab_test_criterion_table_name + '''
                    WHERE id = ?;''',
                    (criterion_id,
                     )
                )

                for row3 in cursor3:

                    new_unit_id = False
                    if row3['unit_id']:

                        unit_id = row3['unit_id']

                        cursor2.execute(
                            '''
                            SELECT code
                            FROM ''' + lab_test_unit_table_name + '''
                            WHERE id = ?;''',
                            (unit_id,
                             )
                        )
                        unit_code = cursor2.fetchone()[0]
                        unit_code = unit_code.replace('/', '_')
                        unit_code = unit_code.replace('²'.decode('utf-8'), '2')
                        unit_code = unit_code.replace('(', '').replace(')', '').replace('-', '_')
                        unit_code = unit_code.replace('aaa', 'aaaa')
                        unit_code = unit_code.replace('º'.decode('utf-8'), 'o')

                        new_unit_id = lab_test_unit_model.search([
                            ('code', '=', unit_code),
                        ])[0]

                    values = {
                        'code': row3['code'],
                        'name': row3['name'],
                        'result': row3['result'],
                        'unit_id': new_unit_id,
                        'sequence': row3['sequence'],
                        'normal_range': row3['normal_range'],
                        # 'lab_test_type_id': new_test_type_id,
                        # 'lab_test_result_id': new_lab_test_result_id,
                        'active': row3['active'],
                    }
                    new_criterion_id = lab_test_criterion_model.create(values).id
                    new_criterion_ids.append((4, new_criterion_id))

        values = {
            'code': '/',
            'code_sequence': 'clv.lab_test.result.code',
            'patient_id': new_patient_id,
            'lab_test_type_id': new_test_type_id,
            'lab_test_request_id': new_lab_test_request_id,
            'date_analysis': row['date_analisis'],
            'reg_state': reg_state,
            'state': state,
            'active': row['active'],
            'active_log': row['active_log'],
            # 'employee_id': employee_id,
            # 'history_marker_id': history_marker_id,
            'criterion_ids': new_criterion_ids,
        }
        lab_test_result_id = lab_test_result_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (lab_test_result_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> lab_test_result_count: ', lab_test_result_count)
