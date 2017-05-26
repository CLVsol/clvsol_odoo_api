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


def survey_survey_export_sqlite(client, args, db_path, table_name):

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
            code,
            description,
            new_id INTEGER
            );
        '''
    )

    survey_model = client.model('survey.survey')
    survey_browse = survey_model.browse(args)

    survey_count = 0
    for survey_reg in survey_browse:
        survey_count += 1

        print(survey_count, survey_reg.id, survey_reg.title.encode("utf-8"))

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                title,
                code,
                description
                )
            VALUES(?,?,?,?)
            ''', (survey_reg.id,
                  survey_reg.title,
                  survey_reg.code,
                  survey_reg.description,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> survey_count: ', survey_count)
    print()
