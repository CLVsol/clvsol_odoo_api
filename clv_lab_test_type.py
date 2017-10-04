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


def myo_lab_test_type_export_sqlite(client, args, db_path, table_name):

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
            code,
            date_inclusion,
            notes,
            criterion_ids,
            active,
            active_log,
            new_id INTEGER
            );
        '''
    )

    client.context = {'active_test': False}
    lab_test_type_model = client.model('myo.lab_test.type')
    lab_test_type_browse = lab_test_type_model.browse(args)

    lab_test_type_count = 0
    for lab_test_type_reg in lab_test_type_browse:
        lab_test_type_count += 1

        print(lab_test_type_count, lab_test_type_reg.id, lab_test_type_reg.code,
              lab_test_type_reg.name.encode("utf-8"))

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                code,
                criterion_ids,
                active
                )
            VALUES(?,?,?,?,?)
            ''', (lab_test_type_reg.id,
                  lab_test_type_reg.name,
                  lab_test_type_reg.code,
                  str(lab_test_type_reg.criterion_ids.id),
                  True,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> lab_test_type_count: ', lab_test_type_count)


def clv_lab_test_type_export_sqlite_10(client, args, db_path, table_name):

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
            code,
            history_marker_id,
            survey_id,
            date_inclusion,
            active,
            active_log,
            new_id INTEGER
            );
        '''
    )

    # client.context = {'active_test': False}
    clv_lab_test_type_model = client.model('clv.lab_test.type')
    clv_lab_test_type_browse = clv_lab_test_type_model.browse(args)

    lab_test_type_count = 0
    for lab_test_type_reg in clv_lab_test_type_browse:
        lab_test_type_count += 1

        print(lab_test_type_count, lab_test_type_reg.id, lab_test_type_reg.name.encode("utf-8"))

        history_marker_id = None
        if lab_test_type_reg.history_marker_id:
            history_marker_id = lab_test_type_reg.history_marker_id.id

        survey_id = None
        if lab_test_type_reg.survey_id:
            survey_id = lab_test_type_reg.survey_id.id

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                code,
                history_marker_id,
                survey_id,
                date_inclusion,
                active,
                active_log
                )
            VALUES(?,?,?,?,?,?,?,?)
            ''', (lab_test_type_reg.id,
                  lab_test_type_reg.name,
                  lab_test_type_reg.code,
                  history_marker_id,
                  survey_id,
                  lab_test_type_reg.date_inclusion,
                  lab_test_type_reg.active,
                  lab_test_type_reg.active_log,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> lab_test_type_count: ', lab_test_type_count)
    print()


def clv_lab_test_type_import_sqlite_10(
        client, args, db_path, table_name, history_marker_table_name, survey_survey_table_name
):

    lab_test_type_model = client.model('clv.lab_test.type')
    history_marker_model = client.model('clv.history_marker')
    survey_survey_model = client.model('survey.survey')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor2 = conn.cursor()

    lab_test_type_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            name,
            code,
            history_marker_id,
            survey_id,
            date_inclusion,
            active,
            active_log,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        lab_test_type_count += 1

        print(lab_test_type_count, row['id'], row['name'].encode('utf-8'))

        history_marker_id = False
        if row['history_marker_id']:
            cursor2.execute(
                '''
                SELECT name
                FROM ''' + history_marker_table_name + '''
                WHERE id = ?;''',
                (row['history_marker_id'],
                 )
            )
            history_marker_name = cursor2.fetchone()
            if history_marker_name is not None:
                history_marker_name = history_marker_name[0]
                history_marker_browse = history_marker_model.browse([('name', '=', history_marker_name), ])
                history_marker_id = history_marker_browse.id[0]

        survey_id = False
        if row['survey_id']:
            cursor2.execute(
                '''
                SELECT code
                FROM ''' + survey_survey_table_name + '''
                WHERE id = ?;''',
                (row['survey_id'],
                 )
            )
            survey_survey_code = cursor2.fetchone()
            if survey_survey_code is not None:
                survey_survey_code = survey_survey_code[0]
                survey_survey_browse = survey_survey_model.browse([('code', '=', survey_survey_code), ])
                survey_id = survey_survey_browse.id[0]

        lab_test_type_browse = lab_test_type_model.browse([('name', '=', row['name']), ('active', '=', True)])
        if lab_test_type_browse.id != []:
            lab_test_type_id = lab_test_type_browse.id[0]

        lab_test_type_browse_2 = lab_test_type_model.browse([('name', '=', row['name']), ('active', '=', False)])
        if lab_test_type_browse_2.id != []:
            lab_test_type_browse = lab_test_type_browse_2
            lab_test_type_id = lab_test_type_browse_2.id[0]

        if lab_test_type_browse.id == []:

            # values = {
            #     'name': row['name'],
            #     'code': row['code'],
            #     'history_marker_id': history_marker_id,
            #     'survey_id': survey_id,
            #     'date_inclusion': row['date_inclusion'],
            #     'active': row['active'],
            #     'active_log': row['active_log'],
            # }
            # survey_survey = lab_test_type_model.create(values)
            # lab_test_type_id = survey_survey.id
            lab_test_type_id = False

        else:

            lab_test_type_id = lab_test_type_browse.id[0]

            values = {
                # 'name': row['name'],
                # 'code': row['code'],
                'history_marker_id': history_marker_id,
                'survey_id': survey_id,
                'date_inclusion': row['date_inclusion'],
                'active': row['active'],
                'active_log': row['active_log'],
            }
            lab_test_type_model.write(lab_test_type_id, values)

        if lab_test_type_id is not False:
            cursor2.execute(
                '''
               UPDATE ''' + table_name + '''
               SET new_id = ?
               WHERE id = ?;''',
                (lab_test_type_id,
                 row['id']
                 )
            )

    conn.commit()

    conn.commit()
    conn.close()

    print()
    print('--> lab_test_type_count: ', lab_test_type_count)
