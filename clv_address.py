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


def myo_address_export_sqlite(client, args, db_path, table_name):

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
            parent_id,
            name,
            alias,
            code,
            random_field,
            user_id,
            zip,
            country_id,
            state_id,
            city,
            l10n_br_city_id,
            street,
            number,
            street2,
            district,
            phone,
            mobile,
            fax,
            email,
            state,
            notes,
            is_residence,
            active,
            active_log,
            new_id INTEGER
            );
        '''
    )

    client.context = {'active_test': False}
    address_model = client.model('myo.address')
    address_browse = address_model.browse(args)

    address_count = 0
    for address_reg in address_browse:
        address_count += 1

        print(address_count, address_reg.id, address_reg.code, address_reg.name.encode("utf-8"))

        parent_id = None
        if address_reg.parent_id:
            parent_id = address_reg.parent_id.id

        alias = None
        if address_reg.alias:
            alias = address_reg.alias

        user_id = None
        if address_reg.user_id:
            user_id = address_reg.user_id.id

        city = None
        if address_reg.city:
            city = address_reg.city

        street = None
        if address_reg.street:
            street = address_reg.street

        number = None
        if address_reg.number:
            number = address_reg.number

        street2 = None
        if address_reg.street2:
            street2 = address_reg.street2

        district = None
        if address_reg.district:
            district = address_reg.district

        phone = None
        if address_reg.phone:
            phone = address_reg.phone

        mobile = None
        if address_reg.mobile:
            mobile = address_reg.mobile

        fax = None
        if address_reg.fax:
            fax = address_reg.fax

        email = None
        if address_reg.email:
            email = address_reg.email

        notes = None
        if address_reg.notes:
            notes = address_reg.notes

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                tag_ids,
                category_ids,
                parent_id,
                name,
                alias,
                code,
                random_field,
                user_id,
                zip,
                country_id,
                state_id,
                city,
                l10n_br_city_id,
                street,
                number,
                street2,
                district,
                phone,
                mobile,
                fax,
                email,
                state,
                notes,
                is_residence,
                active,
                active_log
                )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (address_reg.id,
                  str(address_reg.tag_ids.id),
                  str(address_reg.category_ids.id),
                  parent_id,
                  address_reg.name,
                  alias,
                  address_reg.code,
                  address_reg.random_field,
                  user_id,
                  address_reg.zip,
                  address_reg.country_id.id,
                  address_reg.state_id.id,
                  city,
                  address_reg.l10n_br_city_id.id,
                  street,
                  number,
                  street2,
                  district,
                  phone,
                  mobile,
                  fax,
                  email,
                  address_reg.state,
                  notes,
                  address_reg.is_residence,
                  address_reg.active,
                  address_reg.active_log,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> address_count: ', address_count)


def clv_address_import_sqlite(
        client, args, db_path, table_name, global_tag_table_name, category_table_name,
        res_country_table_name, res_country_state_table_name, l10n_br_base_city_table_name,
        res_users_table_name, history_marker_name
):

    history_marker_id = clv_history_marker_get_id(client, history_marker_name)

    address_model = client.model('clv.address')
    res_country_model = client.model('res.country')
    res_country_state_model = client.model('res.country.state')
    l10n_br_base_city_model = client.model('l10n_br_base.city')
    hr_employee_model = client.model('hr.employee')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    address_count = 0

    data = cursor.execute(
        '''
        SELECT
            id,
            tag_ids,
            category_ids,
            parent_id,
            name,
            alias,
            code,
            random_field,
            user_id,
            zip,
            country_id,
            state_id,
            city,
            l10n_br_city_id,
            street,
            number,
            street2,
            district,
            phone,
            mobile,
            fax,
            email,
            state,
            notes,
            is_residence,
            active,
            active_log,
            new_id
        FROM ''' + table_name + ''';
        '''
    )

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        address_count += 1

        print(address_count, row['id'], row['name'].encode('utf-8'), row['code'], row['tag_ids'], row['category_ids'])

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

        new_country_id = False
        cursor2.execute(
            '''
            SELECT name
            FROM ''' + res_country_table_name + '''
            WHERE id = ?;''',
            (row['country_id'],
             )
        )
        country_name = cursor2.fetchone()[0]
        res_country_browse = res_country_model.browse([('name', '=', country_name), ])
        new_country_id = res_country_browse.id[0]

        new_state_id = False
        cursor2.execute(
            '''
            SELECT name
            FROM ''' + res_country_state_table_name + '''
            WHERE id = ?;''',
            (row['state_id'],
             )
        )
        country_state_name = cursor2.fetchone()[0]
        res_country_state_browse = res_country_state_model.browse([('name', '=', country_state_name), ])
        new_state_id = res_country_state_browse.id[0]

        new_l10n_br_city_id_id = False
        cursor2.execute(
            '''
            SELECT ibge_code
            FROM ''' + l10n_br_base_city_table_name + '''
            WHERE id = ?;''',
            (row['l10n_br_city_id'],
             )
        )
        l10n_br_city_ibge_code = cursor2.fetchone()[0]
        l10n_br_base_city_browse = l10n_br_base_city_model.browse([('ibge_code', '=', l10n_br_city_ibge_code), ])
        new_l10n_br_city_id_id = l10n_br_base_city_browse.id[0]

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
            # 'random_field': row['random_field'],
            'employee_id': employee_id,
            'zip': row['zip'],
            'country_id': new_country_id,
            'state_id': new_state_id,
            'city': row['city'],
            'l10n_br_city_id': new_l10n_br_city_id_id,
            'street': row['street'],
            'number': row['number'],
            'street2': row['street2'],
            'district': row['district'],
            'phone': row['phone'],
            'mobile': row['mobile'],
            'fax': row['fax'],
            'email': row['email'],
            'reg_state': reg_state,
            'state': state,
            'notes': row['notes'],
            # 'is_residence': row['is_residence'],
            'active': row['active'],
            'active_log': row['active_log'],
            'history_marker_id': history_marker_id,
        }
        address_id = address_model.create(values).id

        cursor2.execute(
            '''
           UPDATE ''' + table_name + '''
           SET new_id = ?
           WHERE id = ?;''',
            (address_id,
             row['id']
             )
        )

    conn.commit()
    conn.close()

    print()
    print('--> address_count: ', address_count)
