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

from clv_history_marker import *


def myo_person_export_sqlite(client, args, db_path, table_name):

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
            tag_ids,
            category_ids,
            name,
            alias,
            code,
            random_field,
            user_id,
            gender,
            marital,
            birthday,
            estimated_age,
            date_reference,
            spouse_id,
            father_id,
            mother_id,
            responsible_id,
            identification_id,
            otherid,
            rg,
            cpf,
            country_id,
            date_inclusion,
            state,
            notes,
            address_id,
            is_patient,
            active,
            active_log,
            new_id INTEGER
            );
        '''
    )

    client.context = {'active_test': False}
    person_model = client.model('myo.person')
    person_browse = person_model.browse(args)

    person_count = 0
    for person_reg in person_browse:
        person_count += 1

        print(person_count, person_reg.id, person_reg.code, person_reg.name.encode("utf-8"))

        alias = None
        if person_reg.alias:
            alias = person_reg.alias

        user_id = None
        if person_reg.user_id:
            user_id = person_reg.user_id.id

        birthday = None
        if person_reg.birthday:
            birthday = person_reg.birthday

        estimated_age = None
        if person_reg.estimated_age:
            estimated_age = person_reg.estimated_age

        date_reference = None
        if person_reg.date_reference:
            date_reference = person_reg.date_reference

        marital = None
        if person_reg.marital:
            marital = person_reg.marital

        spouse_id = None
        if person_reg.spouse_id:
            spouse_id = person_reg.spouse_id.id

        father_id = None
        if person_reg.father_id:
            father_id = person_reg.father_id.id

        mother_id = None
        if person_reg.mother_id:
            mother_id = person_reg.mother_id.id

        responsible_id = None
        if person_reg.responsible_id:
            responsible_id = person_reg.responsible_id.id

        identification_id = None
        if person_reg.identification_id:
            identification_id = person_reg.identification_id

        otherid = None
        if person_reg.otherid:
            otherid = person_reg.otherid

        rg = None
        if person_reg.rg:
            rg = person_reg.rg

        cpf = None
        if person_reg.cpf:
            cpf = person_reg.cpf

        country_id = None
        if person_reg.country_id:
            country_id = person_reg.country_id.id

        notes = None
        if person_reg.notes:
            notes = person_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                tag_ids,
                category_ids,
                name,
                alias,
                code,
                random_field,
                user_id,
                gender,
                marital,
                birthday,
                estimated_age,
                date_reference,
                spouse_id,
                father_id,
                mother_id,
                responsible_id,
                identification_id,
                otherid,
                rg,
                cpf,
                country_id,
                date_inclusion,
                state,
                notes,
                address_id,
                is_patient,
                active,
                active_log
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (person_reg.id,
                  str(person_reg.tag_ids.id),
                  str(person_reg.category_ids.id),
                  person_reg.name,
                  alias,
                  person_reg.code,
                  person_reg.random_field,
                  user_id,
                  person_reg.gender,
                  marital,
                  birthday,
                  estimated_age,
                  date_reference,
                  spouse_id,
                  father_id,
                  mother_id,
                  responsible_id,
                  identification_id,
                  otherid,
                  rg,
                  cpf,
                  country_id,
                  person_reg.date_inclusion,
                  person_reg.state,
                  notes,
                  person_reg.address_id.id,
                  person_reg.is_patient,
                  person_reg.active,
                  person_reg.active_log,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> person_count: ', person_count)


def clv_person_export_sqlite_10(client, args, db_path, table_name):

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
            random_field,
            employee_id,
            gender,
            marital,
            birthday,
            estimated_age,
            date_reference,
            spouse_id,
            father_id,
            mother_id,
            responsible_id,
            caregiver_id,
            identification_id,
            otherid,
            rg,
            cpf,
            country_id,
            date_inclusion,
            reg_state,
            state,
            history_marker_id,
            notes,
            address_id,
            person_address_role_id,
            active,
            active_log,
            community_ids,
            event_ids,
            new_id INTEGER
            );
        '''
    )

    # client.context = {'active_test': False}
    person_model = client.model('clv.person')
    person_browse = person_model.browse(args)

    person_count = 0
    for person_reg in person_browse:
        person_count += 1

        print(person_count, person_reg.id, person_reg.code, person_reg.name.encode("utf-8"))

        employee_id = None
        if person_reg.employee_id:
            employee_id = person_reg.employee_id.id

        birthday = None
        if person_reg.birthday:
            birthday = person_reg.birthday

        estimated_age = None
        if person_reg.estimated_age:
            estimated_age = person_reg.estimated_age

        date_reference = None
        if person_reg.date_reference:
            date_reference = person_reg.date_reference

        marital = None
        if person_reg.marital:
            marital = person_reg.marital

        spouse_id = None
        if person_reg.spouse_id:
            spouse_id = person_reg.spouse_id.id

        father_id = None
        if person_reg.father_id:
            father_id = person_reg.father_id.id

        mother_id = None
        if person_reg.mother_id:
            mother_id = person_reg.mother_id.id

        responsible_id = None
        if person_reg.responsible_id:
            responsible_id = person_reg.responsible_id.id

        caregiver_id = None
        if person_reg.caregiver_id:
            caregiver_id = person_reg.caregiver_id.id

        identification_id = None
        if person_reg.identification_id:
            identification_id = person_reg.identification_id

        otherid = None
        if person_reg.otherid:
            otherid = person_reg.otherid

        rg = None
        if person_reg.rg:
            rg = person_reg.rg

        cpf = None
        if person_reg.cpf:
            cpf = person_reg.cpf

        country_id = None
        if person_reg.country_id:
            country_id = person_reg.country_id.id

        history_marker_id = None
        if person_reg.history_marker_id:
            history_marker_id = person_reg.history_marker_id.id

        notes = None
        if person_reg.notes:
            notes = person_reg.notes

        person_address_role_id = None
        if person_reg.person_address_role_id:
            person_address_role_id = person_reg.person_address_role_id.id

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                global_tag_ids,
                category_ids,
                name,
                code,
                random_field,
                employee_id,
                gender,
                marital,
                birthday,
                estimated_age,
                date_reference,
                spouse_id,
                father_id,
                mother_id,
                responsible_id,
                caregiver_id,
                identification_id,
                otherid,
                rg,
                cpf,
                country_id,
                date_inclusion,
                reg_state,
                state,
                history_marker_id,
                notes,
                address_id,
                person_address_role_id,
                active,
                active_log,
                community_ids,
                event_ids
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (person_reg.id,
                  str(person_reg.global_tag_ids.id),
                  str(person_reg.category_ids.id),
                  person_reg.name,
                  person_reg.code,
                  person_reg.random_field,
                  employee_id,
                  person_reg.gender,
                  marital,
                  birthday,
                  estimated_age,
                  date_reference,
                  spouse_id,
                  father_id,
                  mother_id,
                  responsible_id,
                  caregiver_id,
                  identification_id,
                  otherid,
                  rg,
                  cpf,
                  country_id,
                  person_reg.date_inclusion,
                  person_reg.reg_state,
                  person_reg.state,
                  history_marker_id,
                  notes,
                  person_reg.address_id.id,
                  person_address_role_id,
                  person_reg.active,
                  person_reg.active_log,
                  str(person_reg.community_ids.id),
                  str(person_reg.event_ids.id),
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> person_count: ', person_count)


def clv_person_import_sqlite(
        client, args, db_path, table_name, global_tag_table_name, category_table_name, address_table_name,
        res_users_table_name, history_marker_name
):

    history_marker_id = clv_history_marker_get_id(client, history_marker_name)

    person_model = client.model('clv.person')
    hr_employee_model = client.model('hr.employee')

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
            category_ids,
            name,
            alias,
            code,
            random_field,
            user_id,
            gender,
            marital,
            birthday,
            estimated_age,
            date_reference,
            spouse_id,
            father_id,
            mother_id,
            responsible_id,
            identification_id,
            otherid,
            rg,
            cpf,
            country_id,
            date_inclusion,
            state,
            notes,
            address_id,
            is_patient,
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

        print(person_count, row['id'], row['name'].encode('utf-8'), row['code'], row['tag_ids'], row['category_ids'])

        previous_state = row['state']
        if previous_state == 'draft':
            reg_state = 'draft'
            state = 'new'
        if previous_state == 'revised':
            reg_state = 'revised'
            state = 'available'
        if previous_state == 'waiting':
            reg_state = 'done'
            state = 'waiting'
        if previous_state == 'selected':
            reg_state = 'done'
            state = 'selected'
        if previous_state == 'unselected':
            reg_state = 'done'
            state = 'unselected'
        if previous_state == 'canceled':
            reg_state = 'canceled'
            state = 'unavailable'

        new_tag_ids = False
        if row['tag_ids'] != '[]':

            tag_ids = row['tag_ids'].split(',')
            new_tag_ids = []
            for x in range(0, len(tag_ids)):
                tag_id = int(re.sub('[^0-9]', '', tag_ids[x]))
                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + global_tag_table_name + '''
                    WHERE id = ?;''',
                    (tag_id,
                     )
                )
                new_tag_id = cursor2.fetchone()[0]

                new_tag_ids.append((4, new_tag_id))

        new_category_ids = False
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

                new_category_ids.append((4, new_category_id))

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

        employee_id = False
        cursor2.execute(
            '''
            SELECT name
            FROM ''' + res_users_table_name + '''
            WHERE id = ?;''',
            (row['user_id'],
             )
        )
        user_name = cursor2.fetchone()
        print('>>>>>>>>>>', user_name)
        if user_name is not None:
            user_name = user_name[0]
            print('>>>>>>>>>>>>>>>', user_name)
            hr_employee_browse = hr_employee_model.browse([('name', '=', user_name), ])
            employee_id = hr_employee_browse.id[0]

        values = {
            'global_tag_ids': new_tag_ids,
            'category_ids': new_category_ids,
            'name': row['name'],
            # 'alias': row['alias'],
            'code': row['code'],
            'random_field': row['random_field'],
            # 'employee_id': employee_id,
            'gender': row['gender'],
            'marital': row['marital'],
            'birthday': row['birthday'],
            'estimated_age': row['estimated_age'],
            'date_reference': row['date_reference'],
            # 'spouse_id': row['spouse_id'],
            # 'father_id': row['father_id'],
            # 'mother_id': row['mother_id'],
            # 'responsible_id': row['responsible_id'],
            'identification_id': row['identification_id'],
            'otherid': row['otherid'],
            # 'rg': row['rg'],
            # 'cpf': row['cpf'],
            # 'country_id': row['country_id'],
            'date_inclusion': row['date_inclusion'],
            'reg_state': reg_state,
            'state': state,
            'notes': row['notes'],
            'address_id': address_id,
            # 'is_patient': row['is_patient'],
            'active': row['active'],
            'active_log': row['active_log'],
            'history_marker_id': history_marker_id,
        }
        person = person_model.create(values)
        person_id = person.id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (person_id,
             row['id']
             )
        )

        if person.address_id.employee_id is not False:
            if (employee_id is not False) and (person.address_id.employee_id.id != employee_id):
                notes = 'Address Employee: ' + person.address_id.employee_id.name + '\n'
                notes = notes + 'Person Employee:' + hr_employee_browse.name[0] + '\n'
                values = {
                    'notes': notes,
                }
                person_model.write(person_id, values)

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            tag_ids,
            category_ids,
            name,
            alias,
            code,
            random_field,
            user_id,
            gender,
            marital,
            birthday,
            estimated_age,
            date_reference,
            spouse_id,
            father_id,
            mother_id,
            responsible_id,
            identification_id,
            otherid,
            rg,
            cpf,
            country_id,
            date_inclusion,
            state,
            notes,
            address_id,
            is_patient,
            active,
            active_log,
            new_id
        FROM ''' + table_name + '''
        WHERE spouse_id IS NOT NULL;
    ''')

    person_count_2 = 0
    for row in cursor:
        person_count_2 += 1

        print(person_count_2, row['id'], row['name'].encode('utf-8'), row['code'], row['spouse_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['spouse_id'],
             )
        )
        new_spouse_id = cursor2.fetchone()[0]

        values = {
            'spouse_id': new_spouse_id,
        }
        person_model.write(row['new_id'], values)

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            tag_ids,
            category_ids,
            name,
            alias,
            code,
            random_field,
            user_id,
            gender,
            marital,
            birthday,
            estimated_age,
            date_reference,
            spouse_id,
            father_id,
            mother_id,
            responsible_id,
            identification_id,
            otherid,
            rg,
            cpf,
            country_id,
            date_inclusion,
            state,
            notes,
            address_id,
            is_patient,
            active,
            active_log,
            new_id
        FROM ''' + table_name + '''
        WHERE father_id IS NOT NULL;
    ''')

    person_count_3 = 0
    for row in cursor:
        person_count_3 += 1

        print(person_count_3, row['id'], row['name'].encode('utf-8'), row['code'], row['father_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['father_id'],
             )
        )
        new_father_id = cursor2.fetchone()[0]

        values = {
            'father_id': new_father_id,
        }
        person_model.write(row['new_id'], values)

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            tag_ids,
            category_ids,
            name,
            alias,
            code,
            random_field,
            user_id
            gender,
            marital,
            birthday,
            estimated_age,
            date_reference,
            spouse_id,
            father_id,
            mother_id,
            responsible_id,
            identification_id,
            otherid,
            rg,
            cpf,
            country_id,
            date_inclusion,
            state,
            notes,
            address_id,
            is_patient,
            active,
            active_log,
            new_id
        FROM ''' + table_name + '''
        WHERE mother_id IS NOT NULL;
    ''')

    person_count_4 = 0
    for row in cursor:
        person_count_4 += 1

        print(person_count_4, row['id'], row['name'].encode('utf-8'), row['code'], row['mother_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['mother_id'],
             )
        )
        new_mother_id = cursor2.fetchone()[0]

        values = {
            'mother_id': new_mother_id,
        }
        person_model.write(row['new_id'], values)

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            tag_ids,
            category_ids,
            name,
            alias,
            code,
            random_field,
            user_id,
            gender,
            marital,
            birthday,
            estimated_age,
            date_reference,
            spouse_id,
            father_id,
            mother_id,
            responsible_id,
            identification_id,
            otherid,
            rg,
            cpf,
            country_id,
            date_inclusion,
            state,
            notes,
            address_id,
            is_patient,
            active,
            active_log,
            new_id
        FROM ''' + table_name + '''
        WHERE responsible_id IS NOT NULL;
    ''')

    person_count_5 = 0
    for row in cursor:
        person_count_5 += 1

        print(person_count_5, row['id'], row['name'].encode('utf-8'), row['code'], row['responsible_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['responsible_id'],
             )
        )
        new_responsible_id = cursor2.fetchone()[0]

        values = {
            'responsible_id': new_responsible_id,
        }
        person_model.write(row['new_id'], values)

    conn.commit()
    conn.close()

    print()
    print('--> person_count: ', person_count)
    print('--> person_count_2: ', person_count_2)


def clv_person_import_sqlite_10(
        client, args, db_path, table_name, global_tag_table_name, category_table_name, address_table_name,
        history_marker_table_name
):

    person_model = client.model('clv.person')
    global_tag_model = client.model('clv.global_tag')
    category_model = client.model('clv.person.category')
    address_model = client.model('clv.address')
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
            category_ids,
            name,
            code,
            random_field,
            employee_id,
            gender,
            marital,
            birthday,
            estimated_age,
            date_reference,
            spouse_id,
            father_id,
            mother_id,
            responsible_id,
            caregiver_id,
            identification_id,
            otherid,
            rg,
            cpf,
            country_id,
            date_inclusion,
            reg_state,
            state,
            history_marker_id,
            notes,
            address_id,
            active,
            active_log,
            community_ids,
            event_ids,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        person_count += 1

        print(person_count, row['id'], row['name'].encode('utf-8'), row['code'])

        reg_state = row['reg_state']
        if reg_state is None:
            reg_state = 'draft'

        state = row['state']
        if state is None:
            state = 'new'

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
                global_tag_name = cursor2.fetchone()
                if global_tag_name is not None:
                    global_tag_name = global_tag_name[0]
                    global_tag_browse = global_tag_model.browse([('name', '=', global_tag_name), ])
                    new_global_tag_id = global_tag_browse.id[0]

                    new_global_tag_ids.append((4, new_global_tag_id))

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
                category_name = cursor2.fetchone()
                if category_name is not None:
                    category_name = category_name[0]
                    category_browse = category_model.browse([('name', '=', category_name), ])
                    new_category_id = category_browse.id[0]

                new_category_ids.append((4, new_category_id))

        address_id = False
        if row['address_id']:
            cursor2.execute(
                '''
                SELECT code
                FROM ''' + address_table_name + '''
                WHERE id = ?;''',
                (row['address_id'],
                 )
            )
            address_code = cursor2.fetchone()
            if address_code is not None:
                address_code = address_code[0]
                address_browse = address_model.browse([('code', '=', address_code), ])
                address_id = address_browse.id[0]

        reg_state = row['reg_state']
        if reg_state is None:
            reg_state = 'draft'

        state = row['state']
        if state is None:
            state = 'new'

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

        person_browse = person_model.browse([('code', '=', row['code']), ('active', '=', True)])
        if person_browse.id != []:
            person_id = person_browse.id[0]

        person_browse_2 = person_model.browse([('code', '=', row['code']), ('active', '=', False)])
        if person_browse_2.id != []:
            person_browse = person_browse_2
            person_id = person_browse_2.id[0]

        if person_browse.id == []:

            values = {
                'global_tag_ids': new_global_tag_ids,
                'category_ids': new_category_ids,
                'name': row['name'],
                'code': row['code'],
                'random_field': row['random_field'],
                'gender': row['gender'],
                'marital': row['marital'],
                'birthday': row['birthday'],
                'estimated_age': row['estimated_age'],
                'date_reference': row['date_reference'],
                'identification_id': row['identification_id'],
                'otherid': row['otherid'],
                # 'rg': row['rg'],
                # 'cpf': row['cpf'],
                # 'country_id': row['country_id'],
                'date_inclusion': row['date_inclusion'],
                'reg_state': reg_state,
                'state': state,
                'notes': row['notes'],
                'address_id': address_id,
                'active': row['active'],
                'active_log': row['active_log'],
                'history_marker_id': new_history_marker_id,
            }
            person = person_model.create(values)
            person_id = person.id

        else:

            person_id = person_browse.id[0]

            values = {
                'global_tag_ids': [(5,), ],
                'category_ids': [(5,), ],
            }
            person_model.write(person_id, values)

            values = {
                'global_tag_ids': new_global_tag_ids,
                'category_ids': new_category_ids,
                'name': row['name'],
                # 'code': row['code'],
                'random_field': row['random_field'],
                'gender': row['gender'],
                'marital': row['marital'],
                'birthday': row['birthday'],
                'estimated_age': row['estimated_age'],
                'date_reference': row['date_reference'],
                'identification_id': row['identification_id'],
                'otherid': row['otherid'],
                # 'rg': row['rg'],
                # 'cpf': row['cpf'],
                # 'country_id': row['country_id'],
                'date_inclusion': row['date_inclusion'],
                'reg_state': reg_state,
                'state': state,
                'notes': row['notes'],
                'address_id': address_id,
                'active': row['active'],
                'active_log': row['active_log'],
                'history_marker_id': new_history_marker_id,
            }
            person_model.write(person_id, values)

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (person_id,
             row['id']
             )
        )

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            name,
            code,
            spouse_id,
            new_id
        FROM ''' + table_name + '''
        WHERE spouse_id IS NOT NULL;
    ''')

    person_count_2 = 0
    for row in cursor:
        person_count_2 += 1

        print(person_count_2, row['id'], row['name'].encode('utf-8'), row['code'], row['spouse_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['spouse_id'],
             )
        )
        new_spouse_id = cursor2.fetchone()[0]

        person_browse_3 = person_model.browse([('code', '=', row['code']), ])

        if person_browse_3.spouse_id:
            if person_browse_3.spouse_id.id == new_spouse_id:
                values = {
                    'spouse_id': new_spouse_id,
                }
                person_model.write(row['new_id'], values)

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            name,
            code,
            father_id,
            new_id
        FROM ''' + table_name + '''
        WHERE father_id IS NOT NULL;
    ''')

    person_count_3 = 0
    for row in cursor:
        person_count_3 += 1

        print(person_count_3, row['id'], row['name'].encode('utf-8'), row['code'], row['father_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['father_id'],
             )
        )
        new_father_id = cursor2.fetchone()[0]

        person_browse_3 = person_model.browse([('code', '=', row['code']), ])

        if person_browse_3.father_id:
            if person_browse_3.father_id.id == new_father_id:
                values = {
                    'father_id': new_father_id,
                }
                person_model.write(row['new_id'], values)

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            name,
            code,
            mother_id,
            new_id
        FROM ''' + table_name + '''
        WHERE mother_id IS NOT NULL;
    ''')

    person_count_4 = 0
    for row in cursor:
        person_count_4 += 1

        print(person_count_4, row['id'], row['name'].encode('utf-8'), row['code'], row['mother_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['mother_id'],
             )
        )
        new_mother_id = cursor2.fetchone()[0]

        person_browse_3 = person_model.browse([('code', '=', row['code']), ])

        if person_browse_3.mother_id:
            if person_browse_3.mother_id.id == new_mother_id:
                values = {
                    'mother_id': new_mother_id,
                }
                person_model.write(row['new_id'], values)

    conn.commit()

    data = cursor.execute('''
        SELECT
            id,
            name,
            code,
            responsible_id,
            new_id
        FROM ''' + table_name + '''
        WHERE responsible_id IS NOT NULL;
    ''')

    person_count_5 = 0
    for row in cursor:
        person_count_5 += 1

        print(person_count_5, row['id'], row['name'].encode('utf-8'), row['code'], row['responsible_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['responsible_id'],
             )
        )
        new_responsible_id = cursor2.fetchone()[0]

        person_browse_3 = person_model.browse([('code', '=', row['code']), ])

        if person_browse_3.responsible_id:
            if person_browse_3.responsible_id.id == new_responsible_id:
                values = {
                    'responsible_id': new_responsible_id,
                }
                person_model.write(row['new_id'], values)

    data = cursor.execute('''
        SELECT
            id,
            name,
            code,
            caregiver_id,
            new_id
        FROM ''' + table_name + '''
        WHERE caregiver_id IS NOT NULL;
    ''')

    person_count_6 = 0
    for row in cursor:
        person_count_6 += 1

        print(person_count_6, row['id'], row['name'].encode('utf-8'), row['code'], row['caregiver_id'])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row['caregiver_id'],
             )
        )
        new_caregiver_id = cursor2.fetchone()[0]

        person_browse_3 = person_model.browse([('code', '=', row['code']), ])

        if person_browse_3.caregiver_id:
            if person_browse_3.caregiver_id.id == new_caregiver_id:
                values = {
                    'caregiver_id': new_caregiver_id,
                }
                person_model.write(row['new_id'], values)

    conn.commit()
    conn.close()

    print()
    print('--> person_count: ', person_count)
    print('--> person_count_2: ', person_count_2)
    print('--> person_count_2: ', person_count_3)
    print('--> person_count_2: ', person_count_4)
    print('--> person_count_2: ', person_count_5)
    print('--> person_count_2: ', person_count_6)
