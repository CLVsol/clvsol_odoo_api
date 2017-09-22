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


def clv_person_mng_export_sqlite_10(client, args, db_path, table_name):

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
            name,
            gender,
            birthday,
            estimated_age,
            responsible_name,
            responsible_id,
            caregiver_name,
            caregiver_id,
            state,
            notes,
            street,
            street2,
            zip,
            state_id,
            country_id,
            phone,
            mobile,
            l10n_br_city_id,
            district,
            number,
            person_id,
            address_id,
            active,
            active_log,
            action_person,
            action_address,
            action_person_address,
            new_id INTEGER
            );
        '''
    )

    # client.context = {'active_test': False}
    person_mng_model = client.model('clv.person.mng')
    person_mng_browse = person_mng_model.browse(args)

    person_mng_count = 0
    for person_mng_reg in person_mng_browse:
        person_mng_count += 1

        print(person_mng_count, person_mng_reg.id, person_mng_reg.name.encode("utf-8"))

        gender = None
        if person_mng_reg.gender:
            gender = person_mng_reg.gender

        birthday = None
        if person_mng_reg.birthday:
            birthday = person_mng_reg.birthday

        estimated_age = None
        if person_mng_reg.estimated_age:
            estimated_age = person_mng_reg.estimated_age

        responsible_name = None
        if person_mng_reg.responsible_name:
            responsible_name = person_mng_reg.responsible_name

        responsible_id = None
        if person_mng_reg.responsible_id:
            responsible_id = person_mng_reg.responsible_id.id

        caregiver_name = None
        if person_mng_reg.caregiver_name:
            caregiver_name = person_mng_reg.caregiver_name

        caregiver_id = None
        if person_mng_reg.caregiver_id:
            caregiver_id = person_mng_reg.caregiver_id.id

        notes = None
        if person_mng_reg.notes:
            notes = person_mng_reg.notes

        street = None
        if person_mng_reg.street:
            street = person_mng_reg.street

        street2 = None
        if person_mng_reg.street2:
            street2 = person_mng_reg.street2

        zip = None
        if person_mng_reg.zip:
            zip = person_mng_reg.zip

        state_id = None
        if person_mng_reg.state_id:
            state_id = person_mng_reg.state_id.id

        country_id = None
        if person_mng_reg.country_id:
            country_id = person_mng_reg.country_id.id

        phone = None
        if person_mng_reg.phone:
            phone = person_mng_reg.phone

        mobile = None
        if person_mng_reg.mobile:
            mobile = person_mng_reg.mobile

        l10n_br_city_id = None
        if person_mng_reg.l10n_br_city_id:
            l10n_br_city_id = person_mng_reg.l10n_br_city_id.id

        district = None
        if person_mng_reg.district:
            district = person_mng_reg.district

        number = None
        if person_mng_reg.number:
            number = person_mng_reg.number

        person_id = None
        if person_mng_reg.person_id:
            person_id = person_mng_reg.person_id.id

        address_id = None
        if person_mng_reg.address_id:
            address_id = person_mng_reg.address_id.id

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                global_tag_ids,
                name,
                gender,
                birthday,
                estimated_age,
                responsible_name,
                responsible_id,
                caregiver_name,
                caregiver_id,
                state,
                notes,
                street,
                street2,
                zip,
                state_id,
                country_id,
                phone,
                mobile,
                l10n_br_city_id,
                district,
                number,
                person_id,
                address_id,
                active,
                active_log,
                action_person,
                action_address,
                action_person_address
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (person_mng_reg.id,
                  str(person_mng_reg.global_tag_ids.id),
                  person_mng_reg.name,
                  gender,
                  birthday,
                  estimated_age,
                  responsible_name,
                  responsible_id,
                  caregiver_name,
                  caregiver_id,
                  person_mng_reg.state,
                  notes,
                  street,
                  street2,
                  zip,
                  state_id,
                  country_id,
                  phone,
                  mobile,
                  l10n_br_city_id,
                  district,
                  number,
                  person_id,
                  address_id,
                  person_mng_reg.active,
                  person_mng_reg.active_log,
                  person_mng_reg.action_person,
                  person_mng_reg.action_address,
                  person_mng_reg.action_person_address,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> person_mng_count: ', person_mng_count)


def clv_person_mng_import_sqlite_10(
        client, args, db_path, table_name, global_tag_table_name, person_table_name, address_table_name,
        res_country_state_table_name, res_country_table_name, l10n_br_base_city_table_name
):

    person_mng_model = client.model('clv.person.mng')
    global_tag_model = client.model('clv.global_tag')
    address_model = client.model('clv.address')
    person_model = client.model('clv.person')
    res_country_state_model = client.model('res.country.state')
    res_country_model = client.model('res.country')
    l10n_br_base_city_model = client.model('l10n_br_base.city')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor2 = conn.cursor()

    person_mng_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            global_tag_ids,
            name,
            gender,
            birthday,
            estimated_age,
            responsible_name,
            responsible_id,
            caregiver_name,
            caregiver_id,
            state,
            notes,
            street,
            street2,
            zip,
            state_id,
            country_id,
            phone,
            mobile,
            l10n_br_city_id,
            district,
            number,
            person_id,
            address_id,
            active,
            active_log,
            action_person,
            action_address,
            action_person_address,
            new_id INTEGER
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        person_mng_count += 1

        print(person_mng_count, row['id'], row['name'].encode('utf-8'))

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

        responsible_id = False
        if row['responsible_id']:
            cursor2.execute(
                '''
                SELECT code
                FROM ''' + person_table_name + '''
                WHERE id = ?;''',
                (row['responsible_id'],
                 )
            )
            person_code = cursor2.fetchone()
            if person_code is not None:
                person_code = person_code[0]
                person_browse = person_model.browse([('code', '=', person_code), ])
                responsible_id = person_browse.id[0]

        caregiver_id = False
        if row['caregiver_id']:
            cursor2.execute(
                '''
                SELECT code
                FROM ''' + person_table_name + '''
                WHERE id = ?;''',
                (row['caregiver_id'],
                 )
            )
            person_code = cursor2.fetchone()
            if person_code is not None:
                person_code = person_code[0]
                person_browse = person_model.browse([('code', '=', person_code), ])
                caregiver_id = person_browse.id[0]

        state_id = False
        if row['state_id']:
            cursor2.execute(
                '''
                SELECT name
                FROM ''' + res_country_state_table_name + '''
                WHERE id = ?;''',
                (row['state_id'],
                 )
            )
            res_country_state_name = cursor2.fetchone()
            if res_country_state_name is not None:
                res_country_state_name = res_country_state_name[0]
                res_country_state_browse = res_country_state_model.browse([('name', '=', res_country_state_name), ])
                state_id = res_country_state_browse.id[0]

        country_id = False
        if row['country_id']:
            cursor2.execute(
                '''
                SELECT name
                FROM ''' + res_country_table_name + '''
                WHERE id = ?;''',
                (row['country_id'],
                 )
            )
            res_country_name = cursor2.fetchone()
            if res_country_name is not None:
                res_country_name = res_country_name[0]
                res_country_browse = res_country_model.browse([('name', '=', res_country_name), ])
                country_id = res_country_browse.id[0]

        l10n_br_city_id = False
        if row['l10n_br_city_id']:
            cursor2.execute(
                '''
                SELECT name
                FROM ''' + l10n_br_base_city_table_name + '''
                WHERE id = ?;''',
                (row['l10n_br_city_id'],
                 )
            )
            l10n_br_base_city_name = cursor2.fetchone()
            if l10n_br_base_city_name is not None:
                l10n_br_base_city_name = l10n_br_base_city_name[0]
                l10n_br_base_city_browse = l10n_br_base_city_model.browse([('name', '=', l10n_br_base_city_name), ])
                l10n_br_city_id = l10n_br_base_city_browse.id[0]

        person_id = False
        person_id = False
        if row['person_id']:
            cursor2.execute(
                '''
                SELECT code
                FROM ''' + person_table_name + '''
                WHERE id = ?;''',
                (row['person_id'],
                 )
            )
            person_code = cursor2.fetchone()
            if person_code is not None:
                person_code = person_code[0]
                person_browse = person_model.browse([('code', '=', person_code), ])
                person_id = person_browse.id[0]

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

        state = row['state']
        if state is None:
            state = 'draft'

        person_mng_browse = person_mng_model.browse([('name', '=', row['name']), ('active', '=', True)])
        if person_mng_browse.id != []:
            person_mng_id = person_mng_browse.id[0]

        person_mng_browse_2 = person_mng_model.browse([('name', '=', row['name']), ('active', '=', False)])
        if person_mng_browse_2.id != []:
            person_mng_browse = person_mng_browse_2
            person_mng_id = person_mng_browse_2.id[0]

        if person_mng_browse.id == []:

            values = {
                'global_tag_ids': new_global_tag_ids,
                'name': row['name'],
                'gender': row['gender'],
                'birthday': row['birthday'],
                'estimated_age': row['estimated_age'],
                'responsible_name': row['responsible_name'],
                'responsible_id': responsible_id,
                'caregiver_name': row['caregiver_name'],
                'caregiver_id': caregiver_id,
                'state': state,
                'notes': row['notes'],
                'street': row['street'],
                'street2': row['street2'],
                'zip': row['zip'],
                'state_id': state_id,
                'country_id': country_id,
                'phone': row['phone'],
                'mobile': row['mobile'],
                'l10n_br_city_id': l10n_br_city_id,
                'district': row['district'],
                'number': row['number'],
                'person_id': person_id,
                'address_id': address_id,
                'active': row['active'],
                'active_log': row['active_log'],
                'active_log': row['action_person'],
                'active_log': row['action_address'],
                'active_log': row['action_person_address'],
            }
            person = person_mng_model.create(values)
            person_mng_id = person.id

        else:

            person_mng_id = person_mng_browse.id[0]

            values = {
                'global_tag_ids': [(5,), ],
            }
            person_mng_model.write(person_mng_id, values)

            values = {
                'global_tag_ids': new_global_tag_ids,
                'name': row['name'],
                'gender': row['gender'],
                'birthday': row['birthday'],
                'estimated_age': row['estimated_age'],
                'responsible_name': row['responsible_name'],
                'responsible_id': responsible_id,
                'caregiver_name': row['caregiver_name'],
                'caregiver_id': caregiver_id,
                'state': state,
                'notes': row['notes'],
                'street': row['street'],
                'street2': row['street2'],
                'zip': row['zip'],
                'state_id': state_id,
                'country_id': country_id,
                'phone': row['phone'],
                'mobile': row['mobile'],
                'l10n_br_city_id': l10n_br_city_id,
                'district': row['district'],
                'number': row['number'],
                'person_id': person_id,
                'address_id': address_id,
                'active': row['active'],
                'active_log': row['active_log'],
                'active_log': row['active_log'],
                'active_log': row['action_person'],
                'active_log': row['action_address'],
                'active_log': row['action_person_address'],
            }
            person_mng_model.write(person_mng_id, values)

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (person_mng_id,
             row['id']
             )
        )

    conn.commit()

    conn.commit()
    conn.close()

    print()
    print('--> person_mng_count: ', person_mng_count)
