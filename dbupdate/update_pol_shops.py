# -*- coding: utf-8 -*-
import re

import requests
from beertools.util import get_line_parser, parsers

from db import run_upserts

URL = 'http://www.vinmonopolet.no/api/butikker'


FIELDS = [
    {'name': 'Datotid', 'parser': parsers.string_parser},
    {'name': 'Butikknavn', 'parser': parsers.string_parser},
    {'name': 'Gateadresse', 'parser': parsers.string_parser},
    {'name': 'Gate_postnummer', 'parser': parsers.string_parser},
    {'name': 'Gate_poststed', 'parser': parsers.string_parser},
    {'name': 'Postadresse', 'parser': parsers.string_parser},
    {'name': 'Post_postnummer', 'parser': parsers.string_parser},
    {'name': 'Post_poststed', 'parser': parsers.string_parser},
    {'name': 'Telefonnummer', 'parser': parsers.string_parser},
    {'name': 'Kategori', 'parser': parsers.string_parser},
    {'name': 'GPS_breddegrad', 'parser': parsers.float_parser},
    {'name': 'GPS_lengdegrad', 'parser': parsers.float_parser},
    {'name': 'Ukenummer', 'parser': parsers.int_parser},
    {'name': 'Apn_mandag', 'parser': parsers.string_parser},
    {'name': 'Apn_tirsdag', 'parser': parsers.string_parser},
    {'name': 'Apn_onsdag', 'parser': parsers.string_parser},
    {'name': 'Apn_torsdag', 'parser': parsers.string_parser},
    {'name': 'Apn_fredag', 'parser': parsers.string_parser},
    {'name': 'Apn_lordag', 'parser': parsers.string_parser},
    {'name': 'Ukenummer_neste', 'parser': parsers.int_parser},
    {'name': 'Apn_neste_mandag', 'parser': parsers.string_parser},
    {'name': 'Apn_neste_tirsdag', 'parser': parsers.string_parser},
    {'name': 'Apn_neste_onsdag', 'parser': parsers.string_parser},
    {'name': 'Apn_neste_torsdag', 'parser': parsers.string_parser},
    {'name': 'Apn_neste_fredag', 'parser': parsers.string_parser},
    {'name': 'Apn_neste_lordag', 'parser': parsers.string_parser},
]


def get_ids():
    data = requests.get('http://www.vinmonopolet.no/butikker')
    res = []
    for line in data.text.splitlines():
        line = line.strip()
        if line.startswith('var shopName ='):
            matches = re.findall(r'\"(.+?)\"', line)
            res.append(matches[0])

        if line.startswith('window.open("'):
            matches = re.findall(r'\?butikk_id=(.+?)\"', line)
            res.append(matches[0])

    shops = {}
    for id, name in zip(res[1::2], res[0::2]):
        shops[name] = id
    return shops


def parse_line(line, parser):
    line = line.split(';')
    return parser(line)


def save_shops(shops):
    sql = '''
        INSERT INTO pol_shop (id, name, street_address, street_zipcode, street_place, post_address, post_zipcode, post_place, phone, category, lon, lat)
        VALUES (%(id)s, %(Butikknavn)s, %(Gateadresse)s, %(Gate_postnummer)s, %(Gate_poststed)s, %(Postadresse)s, %(Post_postnummer)s, %(Post_poststed)s, %(Telefonnummer)s, %(Kategori)s, %(GPS_lengdegrad)s, %(GPS_breddegrad)s)
        ON CONFLICT (id) DO UPDATE
        SET (id, name, street_address, street_zipcode, street_place, post_address, post_zipcode, post_place, phone, category, lon, lat) = 
        (%(id)s, %(Butikknavn)s, %(Gateadresse)s, %(Gate_postnummer)s, %(Gate_poststed)s, %(Postadresse)s, %(Post_postnummer)s, %(Post_poststed)s, %(Telefonnummer)s, %(Kategori)s, %(GPS_lengdegrad)s, %(GPS_breddegrad)s);
    '''
    run_upserts(sql, shops)


def read():
    r = requests.get(URL)
    r.encoding = 'ISO-8859-1'
    lines = r.text.splitlines()
    parser = get_line_parser(FIELDS)
    shops = [parse_line(line, parser) for line in lines[1:]]
    shop_ids = get_ids()
    for shop in shops:
        shop['Kategori'] = int(shop['Kategori'].replace('Kategori ', ''))
        shop['id'] = shop_ids.get(shop['Butikknavn'], None)
    save_shops(shops)


if __name__ == '__main__':
    read()
