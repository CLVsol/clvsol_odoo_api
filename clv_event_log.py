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


def clv_event_log_export_sqlite_10(client, args, db_path, table_name):

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
            event_id,
            user_id,
            date_log,
            values_,
            action,
            notes,
            new_id INTEGER
            );
    ''')

    # client.context = {'active_test': False}
    event_log = client.model('clv.event.log')
    event_log_browse = event_log.browse(args)

    event_log_count = 0
    for event_log in event_log_browse:
        event_log_count += 1

        print(
            event_log_count, event_log.id, event_log.values,
            event_log.date_log, event_log.notes
        )

        event_id = None
        if event_log.event_id:
            event_id = event_log.event_id.id

        user_id = None
        if event_log.user_id:
            user_id = event_log.user_id.id

        notes = None
        if event_log.notes:
            notes = event_log.notes

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           event_id,
                           user_id,
                           date_log,
                           values_,
                           action,
                           notes
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (event_log.id,
                        event_id,
                        user_id,
                        event_log.date_log,
                        event_log.values,
                        event_log.action,
                        notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> event_log_count: ', event_log_count)
