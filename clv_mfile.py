#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2016-Today  Carlos Eduardo Vercelino - CLVsol
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


def fmng_entity_export_sqlite(client, args, db_path, table_name):

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
            name,
            alias,
            entity_code_base,
            image,
            url,
            description,
            info TEXT,
            entity_code_size,
            parent_id INTEGER,
            ct_url,
            is_album,
            inclusion_date,
            entity_code,
            path,
            new_id INTEGER
            );
    ''')

    fmng_entity = client.model('fmng.entity')
    fmng_entity_browse = fmng_entity.browse(args)

    fmng_entity_count = 0
    for fmng_entity_reg in fmng_entity_browse:
        fmng_entity_count += 1

        parent_id = False
        if fmng_entity_reg.parent_id is not False:
            parent_id = fmng_entity_reg.parent_id.id

        print(fmng_entity_count, fmng_entity_reg.id, parent_id, fmng_entity_reg.entity_code_base,
              fmng_entity_reg.entity_code, fmng_entity_reg.inclusion_date, fmng_entity_reg.name.encode("utf-8")
              )

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           alias,
                           entity_code_base,
                           image,
                           url,
                           description,
                           info,
                           entity_code_size,
                           parent_id,
                           ct_url,
                           is_album,
                           inclusion_date,
                           entity_code,
                           path
                           )
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                       (fmng_entity_reg.id,
                        fmng_entity_reg.name,
                        fmng_entity_reg.alias,
                        fmng_entity_reg.entity_code_base,
                        fmng_entity_reg.image,
                        fmng_entity_reg.url,
                        fmng_entity_reg.description,
                        fmng_entity_reg.info,
                        fmng_entity_reg.entity_code_size,
                        parent_id,
                        fmng_entity_reg.ct_url,
                        fmng_entity_reg.is_album,
                        str(fmng_entity_reg.inclusion_date),
                        fmng_entity_reg.entity_code,
                        fmng_entity_reg.path,
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> fmng_entity_count: ', fmng_entity_count)


def fmng_entity_import_sqlite(client, args, db_path, table_name):

    conn = sqlite3.connect(db_path)
    # conn.text_factory = str
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            name,
            alias,
            entity_code_base,
            image,
            url,
            description,
            info,
            entity_code_size,
            parent_id,
            ct_url,
            is_album,
            inclusion_date,
            entity_code,
            path,
            new_id
        FROM ''' + table_name + ''';
    ''')

    clv_mfile = client.model('clv.mfile')

    print(data)
    print([field[0] for field in cursor.description])
    fmng_entity_count = 0
    for row in cursor:
        fmng_entity_count += 1

        print(fmng_entity_count, row['id'], row['entity_code_base'], row['entity_code_size'],
              row['inclusion_date'], row['new_id'])

        values = {
            'name': row['name'],
            'alias': row['path'],
            'code': row['entity_code'],
            'code_size': row['entity_code_size'],
            'description': row['description'],
            'notes': row['info'],
            'date_inclusion': row['inclusion_date'],
            'active': True,
            'url': row['url'],
        }
        file_id = clv_mfile.create(values).id

        try:
            values = {
                'image': row['image'],
            }
            clv_mfile.write(file_id, values)
        except Exception as e:
            print('>>>>>', e)

        cursor2.execute('''
                       UPDATE ''' + table_name + '''
                       SET new_id = ?
                       WHERE id = ?;''',
                        (file_id,
                         row['id']
                         )
                        )

    conn.commit()
    conn.close()

    print()
    print('--> fmng_entity_count: ', fmng_entity_count)


def clv_file_category_export_sqlite(client, args, db_path, table_name):

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
            notes TEXT,
            new_id INTEGER
            );
    ''')

    clv_file_category = client.model('clv_file.category')
    file_category_browse = clv_file_category.browse(args)

    file_category_count = 0
    for file_category in file_category_browse:
        file_category_count += 1

        parent_id = False
        if file_category.parent_id is not False:
            parent_id = file_category.parent_id.id

        print(file_category_count, file_category.id, parent_id, file_category.code,
              file_category.name.encode("utf-8"), file_category.notes)

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           parent_id,
                           name,
                           code,
                           notes
                           )
                       VALUES(?,?,?,?,?)''',
                       (file_category.id,
                        parent_id,
                        file_category.name,
                        file_category.code,
                        file_category.notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> file_category_count: ', file_category_count)


def clv_mfile_category_import_sqlite(client, args, db_path, table_name):

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
            notes,
            new_id
        FROM ''' + table_name + ''';
    ''')

    clv_mfile_category = client.model('clv.mfile.category')

    print(data)
    print([field[0] for field in cursor.description])
    mfile_category_count = 0
    for row in cursor:
        mfile_category_count += 1

        print(mfile_category_count, row['id'], row['parent_id'], row['name'], row['code'], row['notes'])

        values = {
            'parent_id': row['parent_id'],
            'name': row['name'],
            # 'code': row['code'],
            'notes': row['notes'],
        }
        category_id = clv_mfile_category.create(values).id

        cursor2.execute('''
                       UPDATE ''' + table_name + '''
                       SET new_id = ?
                       WHERE id = ?;''',
                        (category_id,
                         row['id']
                         )
                        )

    conn.commit()
    conn.close()

    print()
    print('--> mfile_category_count: ', mfile_category_count)


def clv_file_export_sqlite(client, args, db_path, table_name):

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
            name,
            alias,
            code,
            code_size,
            description,
            notes TEXT,
            date_inclusion,
            active,
            url,
            ct_url,
            parent_id INTEGER,
            category_ids,
            tag_ids,
            image,
            new_id INTEGER
            );
    ''')

    clv_file = client.model('clv_file')
    file_browse = clv_file.browse(args)

    file_count = 0
    for file_reg in file_browse:
        file_count += 1

        parent_id = False
        if file_reg.parent_id is not False:
            parent_id = file_reg.parent_id.id

        print(file_count, file_reg.id, parent_id, file_reg.code, file_reg.name.encode("utf-8"))

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           alias,
                           code,
                           code_size,
                           description,
                           notes,
                           date_inclusion,
                           active,
                           url,
                           ct_url,
                           parent_id,
                           category_ids,
                           tag_ids,
                           image
                           )
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                       (file_reg.id,
                        file_reg.name,
                        file_reg.alias,
                        file_reg.code,
                        file_reg.code_size,
                        file_reg.description,
                        file_reg.notes,
                        file_reg.date_inclusion,
                        file_reg.active,
                        file_reg.url,
                        file_reg.ct_url,
                        parent_id,
                        str(file_reg.category_ids.id),
                        str(file_reg.tag_ids.id),
                        file_reg.image
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> file_count: ', file_count)


def clv_mfile_import_sqlite(client, args, db_path, table_name, category_table_name, tag_table_name):

    conn = sqlite3.connect(db_path)
    # conn.text_factory = str
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            name,
            alias,
            code,
            code_size,
            description,
            notes,
            date_inclusion,
            active,
            url,
            ct_url,
            parent_id,
            category_ids,
            tag_ids,
            image,
            new_id
        FROM ''' + table_name + ''';
    ''')

    clv_mfile = client.model('clv.mfile')

    print(data)
    print([field[0] for field in cursor.description])
    mfile_count = 0
    for row in cursor:
        mfile_count += 1

        print(mfile_count, row['id'], row['code'], row['date_inclusion'],
              row['category_ids'], row['tag_ids'], '', row['new_id'])

        values = {
            'name': row['name'],
            'alias': row['alias'],
            'code': row['code'],
            'code_size': row['code_size'],
            'description': row['description'],
            'notes': row['notes'],
            'date_inclusion': row['date_inclusion'],
            'active': row['active'],
            'url': row['url'],
            'image': row['image']
        }
        file_id = clv_mfile.create(values).id

        cursor2.execute('''
                       UPDATE ''' + table_name + '''
                       SET new_id = ?
                       WHERE id = ?;''',
                        (file_id,
                         row['id']
                         )
                        )

        if row['category_ids'] != '[]':
            category_ids = row['category_ids'].split(',')
            new_category_ids = []
            for x in range(0, len(category_ids)):

                category_id = int(re.sub('[^0-9]', '', category_ids[x]))
                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + category_table_name + '''
                    WHERE id = ?;''',
                    (category_id,
                     )
                )
                new_category_id = cursor2.fetchone()[0]

                values = {
                    'category_ids': [(4, new_category_id)],
                }
                clv_mfile.write(file_id, values)

                new_category_ids.append(new_category_id)

            print('>>>>>', row['category_ids'], new_category_ids)

        if row['tag_ids'] != '[]':

            tag_ids = row['tag_ids'].split(',')
            new_tag_ids = []
            for x in range(0, len(tag_ids)):
                tag_id = int(re.sub('[^0-9]', '', tag_ids[x]))
                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + tag_table_name + '''
                    WHERE id = ?;''',
                    (tag_id,
                     )
                )
                new_tag_id = cursor2.fetchone()[0]

                values = {
                    'global_tag_ids': [(4, new_tag_id)],
                }
                clv_mfile.write(file_id, values)

                new_tag_ids.append(new_tag_id)

            print('>>>>>', row['tag_ids'], new_tag_ids)

    conn.commit()
    conn.close()

    print()
    print('--> mfile_count: ', mfile_count)


def clv_mfile_import_parent_id_sqlite(client, args, db_path, table_name):

    conn = sqlite3.connect(db_path)
    # conn.text_factory = str
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            name,
            alias,
            code,
            code_size,
            description,
            notes,
            date_inclusion,
            active,
            url,
            ct_url,
            parent_id,
            category_ids,
            tag_ids,
            image,
            new_id
        FROM ''' + table_name + '''
        WHERE parent_id != 0;
    ''')

    clv_mfile = client.model('clv.mfile')

    print(data)
    print([field[0] for field in cursor.description])
    mfile_count = 0
    for row in cursor:
        mfile_count += 1

        print(mfile_count, row['id'], row['code'], row['date_inclusion'],
              row['category_ids'], row['tag_ids'], '', row['new_id'])

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
        clv_mfile.write(row['new_id'], values)

    conn.commit()
    conn.close()

    print()
    print('--> mfile_count: ', mfile_count)
