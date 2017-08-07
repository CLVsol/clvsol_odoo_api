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
