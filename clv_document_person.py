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


def myo_document_person_export_sqlite(client, args, db_path, table_name):

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
            document_id,
            person_id,
            role_id,
            notes,
            active,
            new_id INTEGER
            );
        '''
    )

    client.context = {'active_test': False}
    document_person_model = client.model('myo.document.person')
    document_person_browse = document_person_model.browse(args)

    document_person_count = 0
    for document_person_reg in document_person_browse:
        document_person_count += 1

        print(
            document_person_count, document_person_reg.id,
            document_person_reg.document_id.name.encode("utf-8"),
            document_person_reg.person_id.name.encode("utf-8")
        )

        role_id = None
        if document_person_reg.role_id:
            role_id = document_person_reg.role_id.id

        notes = None
        if document_person_reg.notes:
            notes = document_person_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                document_id,
                person_id,
                role_id,
                notes,
                active
                )
            VALUES(?,?,?,?,?,?)
            ''', (document_person_reg.id,
                  document_person_reg.document_id.id,
                  document_person_reg.person_id.id,
                  role_id,
                  notes,
                  document_person_reg.active,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> document_person_count: ', document_person_count)
