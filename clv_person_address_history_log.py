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


def myo_person_address_log_export_sqlite(client, args, db_path, table_name):

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()
    try:
        cursor.execute('''DROP TABLE ''' + table_name + ''';''')
    except Exception as e:
        print('------->', e)
    cursor.execute('''
        CREATE TABLE ''' + table_name + ''' (
            id INTEGER NOT NULL PRIMARY KEY,
            person_address_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    myo_person_address_log = client.model('myo.person.address.log')
    person_address_log_browse = myo_person_address_log.browse(args)

    person_address_log_count = 0
    for person_address_log in person_address_log_browse:
        person_address_log_count += 1

        print(
            person_address_log_count, person_address_log.id, person_address_log.values,
            person_address_log.date_log, person_address_log.notes
        )

        person_address_id = None
        if person_address_log.person_address_id:
            person_address_id = person_address_log.person_address_id.id

        user_id = None
        if person_address_log.user_id:
            user_id = person_address_log.user_id.id

        notes = None
        if person_address_log.notes:
            notes = person_address_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           person_address_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (person_address_log.id,
                        person_address_id,
                        user_id,
                        person_address_log.date_log,
                        person_address_log.values,
                        person_address_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> person_address_log_count: ', person_address_log_count)
