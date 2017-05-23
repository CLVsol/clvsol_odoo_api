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


def myo_address_log_export_sqlite(client, args, db_path, table_name):

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
            address_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    myo_address_log = client.model('myo.address.log')
    address_log_browse = myo_address_log.browse(args)

    address_log_count = 0
    for address_log in address_log_browse:
        address_log_count += 1

        print(
            address_log_count, address_log.id, address_log.values,
            address_log.date_log, address_log.notes
        )

        address_id = None
        if address_log.address_id:
            address_id = address_log.address_id.id

        user_id = None
        if address_log.user_id:
            user_id = address_log.user_id.id

        notes = None
        if address_log.notes:
            notes = address_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           address_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (address_log.id,
                        address_id,
                        user_id,
                        address_log.date_log,
                        address_log.values,
                        address_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> address_log_count: ', address_log_count)
