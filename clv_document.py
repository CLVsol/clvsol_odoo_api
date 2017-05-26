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


def myo_document_export_sqlite(client, args, db_path, table_name):

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
            tag_ids,
            category_ids,
            name,
            code,
            date_requested,
            date_document,
            date_foreseen,
            date_deadline,
            user_id,
            state,
            notes,
            address_id,
            active,
            active_log,
            base_document_id,
            survey_id,
            survey_user_input_id,
            base_survey_user_input_id,
            new_id INTEGER
            );
        '''
    )

    document_model = client.model('myo.document')
    document_browse = document_model.browse(args)

    document_count = 0
    for document_reg in document_browse:
        document_count += 1

        print(document_count, document_reg.id, document_reg.code, document_reg.name.encode("utf-8"))

        user_id = None
        if document_reg.user_id:
            user_id = document_reg.user_id.id

        notes = None
        if document_reg.notes:
            notes = document_reg.notes

        base_document_id = None
        if document_reg.base_document_id:
            base_document_id = document_reg.base_document_id.id

        survey_id = None
        if document_reg.survey_id:
            survey_id = document_reg.survey_id.id

        survey_user_input_id = None
        if document_reg.survey_user_input_id:
            survey_user_input_id = document_reg.survey_user_input_id.id

        base_survey_user_input_id = None
        if document_reg.base_survey_user_input_id:
            base_survey_user_input_id = document_reg.base_survey_user_input_id.id

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                tag_ids,
                category_ids,
                name,
                code,
                date_requested,
                date_document,
                date_foreseen,
                date_deadline,
                user_id,
                state,
                notes,
                address_id,
                active,
                active_log,
                base_document_id,
                survey_id,
                survey_user_input_id,
                base_survey_user_input_id
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (document_reg.id,
                  str(document_reg.tag_ids.id),
                  str(document_reg.category_ids.id),
                  document_reg.name,
                  document_reg.code,
                  document_reg.date_requested,
                  document_reg.date_document,
                  document_reg.date_foreseen,
                  document_reg.date_deadline,
                  user_id,
                  document_reg.state,
                  notes,
                  document_reg.address_id.id,
                  document_reg.active,
                  document_reg.active_log,
                  base_document_id,
                  survey_id,
                  survey_user_input_id,
                  base_survey_user_input_id,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> document_count: ', document_count)
