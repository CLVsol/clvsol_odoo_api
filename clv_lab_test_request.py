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
