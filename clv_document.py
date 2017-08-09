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
            person_id,
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

    client.context = {'active_test': False}
    document_model = client.model('myo.document')
    document_browse = document_model.browse(args)

    document_person_model = client.model('myo.document.person')

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

        person_id = None
        document_person_browse = document_person_model.browse([('document_id', '=', document_reg.id)])
        if document_person_browse.id != []:
            person_id = document_person_browse.person_id.id[0]

        address_id = None
        if document_reg.address_id:
            address_id = document_reg.address_id.id

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
                person_id,
                address_id,
                active,
                active_log,
                base_document_id,
                survey_id,
                survey_user_input_id,
                base_survey_user_input_id
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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
                  person_id,
                  address_id,
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


def clv_document_import_sqlite(
        client, args, db_path, table_name, global_tag_table_name, category_table_name,
        survey_survey_table_name, person_table_name, address_table_name, res_users_table_name,
        history_marker_name
):

    history_marker_id = clv_history_marker_get_id(client, history_marker_name)

    document_model = client.model('clv.document')
    SurveySurvey = client.model('survey.survey')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    document_count = 0

    data = cursor.execute(
        '''
        SELECT
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
            person_id,
            address_id,
            active,
            active_log,
            base_document_id,
            survey_id,
            survey_user_input_id,
            base_survey_user_input_id,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        document_count += 1

        print(document_count, row['id'], row['name'].encode('utf-8'), row['code'], row['tag_ids'], row['category_ids'])

        previous_state = row['state']
        if previous_state == 'draft':
            reg_state = 'draft'
            state = 'new'
        if previous_state == 'revised':
            reg_state = 'revised'
            state = 'available'
        if previous_state == 'waiting':
            reg_state = 'done'
            state = 'waiting'
        if previous_state == 'done':
            reg_state = 'done'
            state = 'returned'
        if previous_state == 'canceled':
            reg_state = 'cancelled'
            state = 'discarded'

        new_tag_ids = False
        if row['tag_ids'] != '[]':

            tag_ids = row['tag_ids'].split(',')
            new_tag_ids = []
            for x in range(0, len(tag_ids)):
                tag_id = int(re.sub('[^0-9]', '', tag_ids[x]))
                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + global_tag_table_name + '''
                    WHERE id = ?;''',
                    (tag_id,
                     )
                )
                new_tag_id = cursor2.fetchone()[0]

                new_tag_ids.append((4, new_tag_id))

        category_ids = False
        if row['category_ids'] != '[]':

            category_ids = row['category_ids'].split(',')
            new_category_ids = []
            for x in range(0, len(category_ids)):
                category_id = int(re.sub('[^0-9]', '', category_ids[x]))
                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + category_table_name + '''
                    WHERE id = ?;''',
                    (category_id,
                     )
                )
                new_category_id = cursor2.fetchone()[0]

                new_category_ids.append((4, new_category_id))

        survey_id = False
        if row['survey_id']:

            survey_id = row['survey_id']

            cursor2.execute(
                '''
                SELECT code
                FROM ''' + survey_survey_table_name + '''
                WHERE id = ?;''',
                (survey_id,
                 )
            )
            survey_code = cursor2.fetchone()[0]

            survey_survey_id = SurveySurvey.search([
                ('code', '=', survey_code),
            ])[0]

        person_id = False
        address_id = False
        if survey_code == 'QSF17':
            if row['address_id']:

                address_id = row['address_id']

                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + address_table_name + '''
                    WHERE id = ?;''',
                    (address_id,
                     )
                )
                address_id = cursor2.fetchone()[0]
        else:
            if row['person_id']:

                person_id = row['person_id']

                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + person_table_name + '''
                    WHERE id = ?;''',
                    (person_id,
                     )
                )
                person_id = cursor2.fetchone()[0]

        values = {
            'global_tag_ids': new_tag_ids,
            'category_ids': new_category_ids,
            'name': row['name'],
            'code': row['code'],
            'date_requested': row['date_requested'],
            'date_document': row['date_document'],
            'date_foreseen': row['date_foreseen'],
            'date_deadline': row['date_deadline'],
            'reg_state': reg_state,
            'state': state,
            'notes': row['notes'],
            'active': row['active'],
            'active_log': row['active_log'],
            # 'base_document_id': row['base_document_id'],
            'survey_id': survey_survey_id,
            # 'survey_user_input_id': row['survey_user_input_id'],
            # 'base_survey_user_input_id': row['base_survey_user_input_id'],
            'person_id': person_id,
            'address_id': address_id,
            'history_marker_id': history_marker_id,
        }
        document_id = document_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (document_id,
             row['id']
             )
        )

    conn.commit()

    data = cursor.execute('''
        SELECT
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
            person_id,
            address_id,
            active,
            active_log,
            base_document_id,
            survey_id,
            survey_user_input_id,
            base_survey_user_input_id,
            new_id
        FROM ''' + table_name + '''
        WHERE base_document_id IS NOT NULL;
    ''')

    document_count_2 = 0
    for row in cursor:
        document_count_2 += 1

        print(document_count_2, row['id'], row['name'].encode('utf-8'), row['code'], row['base_document_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['base_document_id'],
             )
        )
        new_base_document_id = cursor2.fetchone()[0]

        values = {
            'base_document_id': new_base_document_id,
        }
        document_model.write(row['new_id'], values)

    conn.commit()

    conn.commit()
    conn.close()

    print()
    print('--> document_count: ', document_count)
    print('--> document_count_2: ', document_count_2)
