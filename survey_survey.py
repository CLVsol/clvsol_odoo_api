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


def survey_survey_export_sqlite_10(client, args, db_path, table_name):

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
            title,
            description,
            code,
            history_marker_id,
            new_id INTEGER
            );
        '''
    )

    # client.context = {'active_test': False}
    survey_survey_model = client.model('survey.survey')
    survey_survey_browse = survey_survey_model.browse(args)

    survey_count = 0
    for survey_reg in survey_survey_browse:
        survey_count += 1

        print(survey_count, survey_reg.id, survey_reg.title.encode("utf-8"))

        history_marker_id = None
        if survey_reg.history_marker_id:
            history_marker_id = survey_reg.history_marker_id.id

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                title,
                description,
                code,
                history_marker_id
                )
            VALUES(?,?,?,?,?)
            ''', (survey_reg.id,
                  survey_reg.title,
                  survey_reg.description,
                  survey_reg.code,
                  history_marker_id,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> survey_count: ', survey_count)
    print()


def survey_survey_import_sqlite_10(
        client, args, db_path, table_name, history_marker_table_name
):

    survey_survey_model = client.model('survey.survey')
    history_marker_model = client.model('clv.history_marker')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor2 = conn.cursor()

    survey_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            title,
            description,
            code,
            history_marker_id,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        survey_count += 1

        print(survey_count, row['id'], row['title'].encode('utf-8'))

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

        survey_survey_browse = survey_survey_model.browse([('title', '=', row['title']), ('active', '=', True)])
        if survey_survey_browse.id != []:
            survey_id = survey_survey_browse.id[0]

        survey_survey_browse_2 = survey_survey_model.browse([('title', '=', row['title']), ('active', '=', False)])
        if survey_survey_browse_2.id != []:
            survey_survey_browse = survey_survey_browse_2
            survey_id = survey_survey_browse_2.id[0]

        if survey_survey_browse.id == []:

            # values = {
            #     'title': row['title'],
            #     'description': row['description'],
            #     'code': row['code'],
            #     'history_marker_id': history_marker_id,
            # }
            # survey_survey = survey_survey_model.create(values)
            # survey_id = survey_survey.id
            survey_id = False

        else:

            survey_id = survey_survey_browse.id[0]

            values = {
                # 'title': row['title'],
                'description': row['description'],
                # 'code': row['code'],
                'history_marker_id': history_marker_id,
            }
            survey_survey_model.write(survey_id, values)

        if survey_id is not False:
            cursor2.execute(
                '''
               UPDATE ''' + table_name + '''
               SET new_id = ?
               WHERE id = ?;''',
                (survey_id,
                 row['id']
                 )
            )

    conn.commit()

    conn.commit()
    conn.close()

    print()
    print('--> survey_count: ', survey_count)
