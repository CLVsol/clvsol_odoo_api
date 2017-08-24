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

from clv_history_marker import *


def clv_person_address_history_import_sqlite(
    client, args, db_path, table_name, global_tag_table_name, role_table_name, person_table_name, address_table_name,
    history_marker_name
):

    history_marker_id = clv_history_marker_get_id(client, history_marker_name)

    person_address_history_model = client.model('clv.person.address.history')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    person_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            tag_ids,
            person_id,
            address_id,
            role_id,
            sign_in_date,
            sign_out_date,
            notes,
            active,
            active_log,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        person_count += 1

        print(
            person_count, row['id'], row['tag_ids'], row['person_id'], row['address_id'], row['role_id']
        )

        person_id = False
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

        address_id = False
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

        role_id = False
        if row['role_id']:

            role_id = row['role_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + role_table_name + '''
                WHERE id = ?;''',
                (role_id,
                 )
            )
            role_id = cursor2.fetchone()[0]

        values = {
            # 'global_tag_ids': row['tag_ids'],
            'person_id': person_id,
            'address_id': address_id,
            'role_id': role_id,
            'sign_in_date': row['sign_in_date'],
            'sign_out_date': row['sign_out_date'],
            'notes': row['notes'],
            'active': row['active'],
            # 'active_log': row['active_log'],
            'history_marker_id': history_marker_id,
        }
        person_address_history_id = person_address_history_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (person_address_history_id,
             row['id']
             )
        )

        # if row['tag_ids'] != '[]':

        #     tag_ids = row['tag_ids'].split(',')
        #     new_tag_ids = []
        #     for x in range(0, len(tag_ids)):
        #         tag_id = int(re.sub('[^0-9]', '', tag_ids[x]))
        #         cursor2.execute(
        #             '''
        #             SELECT new_id
        #             FROM ''' + global_tag_table_name + '''
        #             WHERE id = ?;''',
        #             (tag_id,
        #              )
        #         )
        #         new_tag_id = cursor2.fetchone()[0]

        #         values = {
        #             'global_tag_ids': [(4, new_tag_id)],
        #         }
        #         person_address_history_model.write(person_address_history_id, values)

        #         new_tag_ids.append(new_tag_id)

        #     print('>>>>>', row[4], new_tag_ids)

    conn.commit()
    conn.close()

    print()
    print('--> person_count: ', person_count)


def clv_person_address_history_export_sqlite_10(client, args, db_path, table_name):

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
            person_id,
            global_tag_ids,
            sign_in_date,
            sign_out_date,
            address_id,
            role_id,
            history_marker_id,
            active,
            new_id INTEGER
            );
        '''
    )

    # client.context = {'active_test': False}
    person_address_history_model = client.model('clv.person.address.history')
    person_address_history_browse = person_address_history_model.browse(args)

    person_address_history_count = 0
    for person_address_history_reg in person_address_history_browse:
        person_address_history_count += 1

        print(person_address_history_count, person_address_history_reg.id,
              person_address_history_reg.person_id.name.encode("utf-8"))

        person_id = None
        if person_address_history_reg.person_id:
            person_id = person_address_history_reg.person_id.id

        sign_in_date = None
        if person_address_history_reg.sign_in_date:
            sign_in_date = person_address_history_reg.sign_in_date

        sign_out_date = None
        if person_address_history_reg.sign_out_date:
            sign_out_date = person_address_history_reg.sign_out_date

        address_id = None
        if person_address_history_reg.address_id:
            address_id = person_address_history_reg.address_id.id

        role_id = None
        if person_address_history_reg.role_id:
            role_id = person_address_history_reg.role_id.id

        history_marker_id = None
        if person_address_history_reg.history_marker_id:
            history_marker_id = person_address_history_reg.history_marker_id.id

        notes = None
        if person_address_history_reg.notes:
            notes = person_address_history_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                person_id,
                global_tag_ids,
                sign_in_date,
                sign_out_date,
                address_id,
                role_id,
                history_marker_id,
                notes,
                active,
                active_log
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
            ''', (person_address_history_reg.id,
                  person_id,
                  str(person_address_history_reg.global_tag_ids.id),
                  sign_in_date,
                  sign_out_date,
                  address_id,
                  role_id,
                  history_marker_id,
                  notes,
                  person_address_history_reg.active,
                  person_address_history_reg.active_log,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> person_address_history_count: ', person_address_history_count)


def clv_person_address_history_import_sqlite_10(
    client, args, db_path, table_name, global_tag_table_name, person_address_role_table_name, person_table_name,
    address_table_name, history_marker_table_name
):

    person_address_history_model = client.model('clv.person.address.history')

    history_marker_model = client.model('clv.history_marker')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    person_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            global_tag_ids,
            person_id,
            address_id,
            role_id,
            history_marker_id,
            sign_in_date,
            sign_out_date,
            notes,
            active,
            active_log,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        person_count += 1

        print(
            person_count, row['id'], row['person_id'], row['address_id'], row['role_id']
        )

        person_id = False
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

        address_id = False
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

        role_id = False
        if row['role_id']:

            role_id = row['role_id']

            cursor2.execute(
                '''
                SELECT new_id
                FROM ''' + person_address_role_table_name + '''
                WHERE id = ?;''',
                (role_id,
                 )
            )
            role_id = cursor2.fetchone()[0]

        new_history_marker_id = False
        if row['history_marker_id']:
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

        person_address_history_browse = person_address_history_model.browse([
            ('person_id', '=', person_id),
            ('sign_in_date', '=', row['sign_in_date']),
            ('history_marker_id', '=', new_history_marker_id),
            ('active', '=', True),
        ])
        if person_address_history_browse.id != []:
            person_id = person_address_history_browse.id[0]

        person_address_history_browse_2 = person_address_history_model.browse([
            ('person_id', '=', person_id),
            ('sign_in_date', '=', row['sign_in_date']),
            ('history_marker_id', '=', new_history_marker_id),
            ('active', '=', False),
        ])
        if person_address_history_browse_2.id != []:
            person_address_history_browse = person_address_history_browse_2
            person_id = person_address_history_browse_2.id[0]

        if person_address_history_browse.id == []:

            values = {
                # 'global_tag_ids': row['tag_ids'],
                'person_id': person_id,
                'address_id': address_id,
                'role_id': role_id,
                'sign_in_date': row['sign_in_date'],
                'sign_out_date': row['sign_out_date'],
                'notes': row['notes'],
                'active': row['active'],
                'active_log': row['active_log'],
                'history_marker_id': new_history_marker_id,
            }
            person_address_history_id = person_address_history_model.create(values).id

        else:

            person_address_history_id = person_address_history_browse.id[0]

            values = {
                'category_ids': [(5,), ],
            }
            person_address_history_model.write(person_address_history_id, values)

            values = {
                # 'global_tag_ids': row['tag_ids'],
                # 'person_id': person_id,
                'address_id': address_id,
                'role_id': role_id,
                # 'sign_in_date': row['sign_in_date'],
                'sign_out_date': row['sign_out_date'],
                'notes': row['notes'],
                'active': row['active'],
                'active_log': row['active_log'],
                # 'history_marker_id': new_history_marker_id,
            }
            person_address_history_model.write(person_address_history_id, values)

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (person_address_history_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> person_count: ', person_count)
