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


def myo_lab_test_unit_export_sqlite(client, args, db_path, table_name):

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
            description,
            notes,
            active,
            new_id INTEGER
            );
        '''
    )

    client.context = {'active_test': False}
    lab_test_unit_model = client.model('myo.lab_test.unit')
    lab_test_unit_browse = lab_test_unit_model.browse(args)

    lab_test_unit_count = 0
    for lab_test_unit_reg in lab_test_unit_browse:
        lab_test_unit_count += 1

        print(lab_test_unit_count, lab_test_unit_reg.id, lab_test_unit_reg.code.encode("utf-8"),
              lab_test_unit_reg.name.encode("utf-8"))

        description = None
        if lab_test_unit_reg.description:
            description = lab_test_unit_reg.description

        notes = None
        # if lab_test_unit_reg.notes:
        #     notes = lab_test_unit_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                code,
                description,
                notes,
                active
                )
            VALUES(?,?,?,?,?,?)
            ''', (lab_test_unit_reg.id,
                  lab_test_unit_reg.name,
                  lab_test_unit_reg.code,
                  description,
                  notes,
                  True,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> lab_test_unit_count: ', lab_test_unit_count)
