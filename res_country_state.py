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


def res_country_state_export_sqlite(client, args, db_path, table_name):

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
            name,
            code,
            country_id,
            ibge_code,
            new_id INTEGER
            );
        '''
    )

    client.context = {'active_test': False}
    res_country_state_model = client.model('res.country.state')
    res_country_state_browse = res_country_state_model.browse(args)

    res_country_state_count = 0
    for res_country_state_reg in res_country_state_browse:
        res_country_state_count += 1

        print(res_country_state_count, res_country_state_reg.id, res_country_state_reg.name.encode("utf-8"))

        country_id = None
        if res_country_state_reg.country_id:
            country_id = res_country_state_reg.country_id.id

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                code,
                country_id,
                ibge_code
                )
            VALUES(?,?,?,?,?)
            ''', (res_country_state_reg.id,
                  res_country_state_reg.name,
                  res_country_state_reg.code,
                  country_id,
                  res_country_state_reg.ibge_code,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> res_country_state_count: ', res_country_state_count)
    print()


def res_country_state_export_sqlite_10(client, args, db_path, table_name):

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
            name,
            code,
            country_id,
            ibge_code,
            new_id INTEGER
            );
        '''
    )

    # client.context = {'active_test': False}
    res_country_state_model = client.model('res.country.state')
    res_country_state_browse = res_country_state_model.browse(args)

    res_country_state_count = 0
    for res_country_state_reg in res_country_state_browse:
        res_country_state_count += 1

        print(res_country_state_count, res_country_state_reg.id, res_country_state_reg.name.encode("utf-8"))

        country_id = None
        if res_country_state_reg.country_id:
            country_id = res_country_state_reg.country_id.id

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                code,
                country_id,
                ibge_code
                )
            VALUES(?,?,?,?,?)
            ''', (res_country_state_reg.id,
                  res_country_state_reg.name,
                  res_country_state_reg.code,
                  country_id,
                  res_country_state_reg.ibge_code,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> res_country_state_count: ', res_country_state_count)
    print()
