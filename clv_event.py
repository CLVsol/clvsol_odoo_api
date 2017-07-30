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


def clv_event_export_sqlite_10(client, args, db_path, table_name):

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
            global_tag_ids,
            category_ids,
            name,
            code,
            employee_id,
            planned_hours,
            date_inclusion,
            date_foreseen,
            date_start,
            date_deadline,
            sequence,
            history_marker_id,
            notes,
            state,
            active,
            active_log,
            person_ids,
            new_id INTEGER
            );
        '''
    )

    # client.context = {'active_test': False}
    event_model = client.model('clv.event')
    event_browse = event_model.browse(args)

    event_count = 0
    for event_reg in event_browse:
        event_count += 1

        print(event_count, event_reg.id, event_reg.code, event_reg.name.encode("utf-8"))

        employee_id = None
        if event_reg.employee_id:
            employee_id = event_reg.employee_id.id

        planned_hours = None
        if event_reg.planned_hours:
            planned_hours = event_reg.planned_hours

        date_inclusion = None
        if event_reg.date_inclusion:
            date_inclusion = event_reg.date_inclusion

        date_foreseen = None
        if event_reg.date_foreseen:
            date_foreseen = event_reg.date_foreseen

        date_start = None
        if event_reg.date_start:
            date_start = event_reg.date_start

        date_deadline = None
        if event_reg.date_deadline:
            date_deadline = event_reg.date_deadline

        sequence = None
        if event_reg.sequence:
            sequence = event_reg.sequence

        history_marker_id = None
        if event_reg.history_marker_id:
            history_marker_id = event_reg.history_marker_id.id

        notes = None
        if event_reg.notes:
            notes = event_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                global_tag_ids,
                category_ids,
                name,
                code,
                employee_id,
                planned_hours,
                date_inclusion,
                date_foreseen,
                date_start,
                date_deadline,
                sequence,
                history_marker_id,
                notes,
                state,
                active,
                active_log,
                person_ids
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (event_reg.id,
                  str(event_reg.global_tag_ids.id),
                  str(event_reg.category_ids.id),
                  event_reg.name,
                  event_reg.code,
                  employee_id,
                  planned_hours,
                  date_inclusion,
                  date_foreseen,
                  date_start,
                  date_deadline,
                  sequence,
                  history_marker_id,
                  notes,
                  event_reg.state,
                  event_reg.active,
                  event_reg.active_log,
                  str(event_reg.person_ids.id),
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> event_count: ', event_count)


def clv_event_import_sqlite_10(
    client, args, db_path, table_name,
    global_tag_table_name, category_table_name, hr_employee_table_name, person_table_name, history_marker_table_name
):

    event_model = client.model('clv.event')

    global_tag_model = client.model('clv.global_tag')
    event_category_model = client.model('clv.event.category')
    history_marker_model = client.model('clv.history_marker')
    hr_employee_model = client.model('hr.employee')
    person_model = client.model('clv.person')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    event_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            global_tag_ids,
            category_ids,
            name,
            code,
            employee_id,
            planned_hours,
            date_inclusion,
            date_foreseen,
            date_start,
            date_deadline,
            sequence,
            history_marker_id,
            notes,
            state,
            active,
            active_log,
            person_ids,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        event_count += 1

        print(event_count, row['id'], row['name'].encode('utf-8'), row['code'])

        new_global_tag_ids = False
        if row['global_tag_ids'] != '[]':

            global_tag_ids = row['global_tag_ids'].split(',')
            new_global_tag_ids = []
            for x in range(0, len(global_tag_ids)):
                tag_id = int(re.sub('[^0-9]', '', global_tag_ids[x]))

                cursor2.execute(
                    '''
                    SELECT name
                    FROM ''' + global_tag_table_name + '''
                    WHERE id = ?;''',
                    (tag_id,
                     )
                )
                tag_name = cursor2.fetchone()[0]

                global_tag_browse = global_tag_model.browse([('name', '=', tag_name), ])
                new_tag_id = global_tag_browse.id[0]
                new_global_tag_ids.append((4, new_tag_id))

        new_category_ids = False
        if row['category_ids'] != '[]':

            category_ids = row['category_ids'].split(',')
            new_category_ids = []
            for x in range(0, len(category_ids)):
                category_id = int(re.sub('[^0-9]', '', category_ids[x]))

                cursor2.execute(
                    '''
                    SELECT name
                    FROM ''' + category_table_name + '''
                    WHERE id = ?;''',
                    (category_id,
                     )
                )
                category_name = cursor2.fetchone()[0]

                event_category_browse = event_category_model.browse([('name', '=', category_name), ])
                new_category_id = event_category_browse.id[0]

                new_category_ids.append((4, new_category_id))

        new_history_marker_id = False
        cursor2.execute(
            '''
            SELECT name
            FROM ''' + history_marker_table_name + '''
            WHERE id = ?;''',
            (row['history_marker_id'],
             )
        )
        history_marker_name = cursor2.fetchone()[0]
        history_marker_browse = history_marker_model.browse([('name', '=', history_marker_name), ])
        new_history_marker_id = history_marker_browse.id[0]

        employee_id = False
        cursor2.execute(
            '''
            SELECT name
            FROM ''' + hr_employee_table_name + '''
            WHERE id = ?;''',
            (row['employee_id'],
             )
        )
        user_name = cursor2.fetchone()
        if user_name is not None:
            user_name = user_name[0]
            hr_employee_browse = hr_employee_model.browse([('name', '=', user_name), ])
            employee_id = hr_employee_browse.id[0]

        new_person_ids = False
        if row['person_ids'] != '[]':

            person_ids = row['person_ids'].split(',')
            new_person_ids = []
            for x in range(0, len(person_ids)):
                person_id = int(re.sub('[^0-9]', '', person_ids[x]))

                cursor2.execute(
                    '''
                    SELECT name
                    FROM ''' + person_table_name + '''
                    WHERE id = ?;''',
                    (person_id,
                     )
                )
                person_name = cursor2.fetchone()[0]

                person_browse = person_model.browse([('name', '=', person_name), ])
                new_person_id = person_browse.id[0]

                new_person_ids.append((4, new_person_id))

        state = row['state']
        if state is None:
            state = 'draft'

        values = {
            'global_tag_ids': new_global_tag_ids,
            'category_ids': new_category_ids,
            'name': row['name'],
            'code': row['code'],
            'employee_id': employee_id,
            'planned_hours': row['planned_hours'],
            'date_inclusion': row['date_inclusion'],
            'date_foreseen': row['date_foreseen'],
            'date_start': row['date_start'],
            'date_deadline': row['date_deadline'],
            'sequence': row['sequence'],
            'history_marker_id': new_history_marker_id,
            'notes': row['notes'],
            'state': state,
            'active': row['active'],
            'active_log': row['active_log'],
            'person_ids': new_person_ids,
        }
        event_id = event_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (event_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> event_count: ', event_count)
