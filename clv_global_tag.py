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


def myo_tag_export_sqlite(client, args, db_path, table_name):

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
            parent_id,
            name,
            code,
            description,
            notes,
            color,
            new_id INTEGER
            );
    ''')

    client.context = {'active_test': False}
    myo_tag = client.model('myo.tag')
    tag_browse = myo_tag.browse(args)

    tag_count = 0
    for tag in tag_browse:
        tag_count += 1

        print(tag_count, tag.id, tag.code, tag.name.encode("utf-8"), tag.notes)

        parent_id = None
        if tag.parent_id:
            parent_id = tag.parent_id.id

        notes = None
        if tag.notes:
            notes = tag.notes

        color = None
        if tag.color:
            color = tag.color

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           parent_id,
                           name,
                           code,
                           description,
                           notes,
                           color
                           )
                       VALUES(?,?,?,?,?,?,?)''',
                       (tag.id,
                        parent_id,
                        tag.name,
                        tag.code,
                        tag.description,
                        notes,
                        color
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> tag_count: ', tag_count)


def clv_tag_export_sqlite(client, args, db_path, table_name):

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
            parent_id,
            name,
            code,
            description,
            notes TEXT,
            color,
            new_id INTEGER
            );
    ''')

    client.context = {'active_test': False}
    clv_tag = client.model('clv_tag')
    tag_browse = clv_tag.browse(args)

    tag_count = 0
    for tag in tag_browse:
        tag_count += 1

        print(tag_count, tag.id, tag.code, tag.name.encode("utf-8"), tag.notes)

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           code,
                           description,
                           notes
                           )
                       VALUES(?,?,?,?,?)''',
                       (tag.id,
                        tag.name,
                        tag.code,
                        tag.description,
                        tag.notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> tag_count: ', tag_count)


def clv_global_tag_export_sqlite_10(client, args, db_path, table_name):

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
            parent_id,
            name,
            code,
            description,
            notes TEXT,
            color,
            new_id INTEGER
            );
    ''')

    # client.context = {'active_test': False}
    clv_global_tag = client.model('clv.global_tag')
    global_tag_browse = clv_global_tag.browse(args)

    global_tag_count = 0
    for global_tag in global_tag_browse:
        global_tag_count += 1

        print(global_tag_count, global_tag.id, global_tag.code, global_tag.name.encode("utf-8"), global_tag.notes)

        code = None
        if global_tag.code:
            code = global_tag.code

        description = None
        if global_tag.description:
            description = global_tag.description

        notes = None
        if global_tag.notes:
            notes = global_tag.notes

        color = None
        if global_tag.color:
            color = global_tag.color

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           code,
                           description,
                           notes,
                           color
                           )
                       VALUES(?,?,?,?,?,?)''',
                       (global_tag.id,
                        global_tag.name,
                        code,
                        description,
                        notes,
                        color,
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> global_tag_count: ', global_tag_count)


def clv_global_tag_import_sqlite(client, args, db_path, table_name):

    global_tag_model = client.model('clv.global_tag')

    conn = sqlite3.connect(db_path)
    # conn.text_factory = str
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            parent_id,
            name,
            code,
            description,
            notes,
            color,
            new_id
        FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])

    tag_count = 0
    for row in cursor:
        tag_count += 1

        print(
            tag_count, row['id'], row['parent_id'], row['name'].encode('utf-8'), row['code'],
        )

        values = {
            'name': row['name'],
            'code': row['code'],
            'description': row['description'],
            'notes': row['notes'],
            'color': row['color'],
        }
        tag_id = global_tag_model.create(values).id

        cursor2.execute(
            '''
            UPDATE ''' + table_name + '''
            SET new_id = ?
            WHERE id = ?;''',
            (tag_id,
             row['id']
             )
        )

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            parent_id,
            name,
            code,
            description,
            notes,
            color,
            new_id
        FROM ''' + table_name + '''
        WHERE parent_id IS NOT NULL;
    ''')

    tag_count_2 = 0
    for row in cursor:
        tag_count_2 += 1

        print(tag_count_2, row['id'], row['parent_id'], row['name'], row['code'], row['new_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['parent_id'],
             )
        )
        new_parent_id = cursor2.fetchone()[0]

        print('>>>>>', row['id'], row['new_id'], row['parent_id'], new_parent_id)

        values = {
            'parent_id': new_parent_id,
        }
        global_tag_model.write(row['new_id'], values)

    conn.commit()
    conn.close()

    print()
    print('--> tag_count: ', tag_count)
    print('--> tag_count_2: ', tag_count_2)
