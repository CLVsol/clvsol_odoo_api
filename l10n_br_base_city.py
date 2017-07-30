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


def l10n_br_base_city_export_sqlite(client, args, db_path, table_name):

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
            state_id,
            ibge_code,
            new_id INTEGER
            );
        '''
    )

    client.context = {'active_test': False}
    l10n_br_base_city_model = client.model('l10n_br_base.city')
    l10n_br_base_city_browse = l10n_br_base_city_model.browse(args)

    l10n_br_base_city_count = 0
    for l10n_br_base_city_reg in l10n_br_base_city_browse:
        l10n_br_base_city_count += 1

        print(l10n_br_base_city_count, l10n_br_base_city_reg.id, l10n_br_base_city_reg.name.encode("utf-8"))

        state_id = None
        if l10n_br_base_city_reg.state_id:
            state_id = l10n_br_base_city_reg.state_id.id

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                state_id,
                ibge_code
                )
            VALUES(?,?,?,?)
            ''', (l10n_br_base_city_reg.id,
                  l10n_br_base_city_reg.name,
                  state_id,
                  l10n_br_base_city_reg.ibge_code,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> l10n_br_base_city_count: ', l10n_br_base_city_count)
    print()


def l10n_br_base_city_export_sqlite_10(client, args, db_path, table_name):

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
            state_id,
            ibge_code,
            new_id INTEGER
            );
        '''
    )

    # client.context = {'active_test': False}
    l10n_br_base_city_model = client.model('l10n_br_base.city')
    l10n_br_base_city_browse = l10n_br_base_city_model.browse(args)

    l10n_br_base_city_count = 0
    for l10n_br_base_city_reg in l10n_br_base_city_browse:
        l10n_br_base_city_count += 1

        print(l10n_br_base_city_count, l10n_br_base_city_reg.id, l10n_br_base_city_reg.name.encode("utf-8"))

        state_id = None
        if l10n_br_base_city_reg.state_id:
            state_id = l10n_br_base_city_reg.state_id.id

        cursor.execute('''
            INSERT INTO ''' + table_name + '''(
                id,
                name,
                state_id,
                ibge_code
                )
            VALUES(?,?,?,?)
            ''', (l10n_br_base_city_reg.id,
                  l10n_br_base_city_reg.name,
                  state_id,
                  l10n_br_base_city_reg.ibge_code,
                  )
        )

    conn.commit()
    conn.close()

    print()
    print('--> l10n_br_base_city_count: ', l10n_br_base_city_count)
    print()
